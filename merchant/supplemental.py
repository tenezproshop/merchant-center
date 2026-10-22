"""Gravações na fonte suplementar, com histórico de lotes para poder desfazer.

A API não permite ler o que já foi gravado numa fonte suplementar, então este
módulo guarda localmente (dados/suplementar.json) o valor atual de cada campo
que enviamos, e cada lote em dados/lotes/<id>.json com o "antes" e o "depois".
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from .api import DATA_DIR, account, data_source, normalize, request

STATE_FILE = DATA_DIR / "suplementar.json"
BATCH_DIR = DATA_DIR / "lotes"
WORKERS = 8

# Colunas aceitas em CSV / argumentos -> atributo da Merchant API.
FIELDS = {
    "price": "price",
    "sale_price": "salePrice",
    "sale_period": "salePriceEffectiveDate",
    "availability": "availability",
    "title": "title",
    "description": "description",
    "link": "link",
    "image_link": "imageLink",
    **{f"custom_label_{i}": f"customLabel{i}" for i in range(5)},
}


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    DATA_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=1, ensure_ascii=False))


def _mask_path(key):
    # customLabel4 -> custom_label_4, salePriceEffectiveDate -> sale_price_effective_date
    return "product_attributes." + re.sub(r"(?<=[a-z])(?=[A-Z0-9])", "_", key).lower()


def _write(pid, new_attrs, changed_keys):
    """Grava um produto. new_attrs é o conjunto completo de campos que deve ficar na fonte."""
    ds = data_source()
    path = f"/products/v1/{account()}/productInputs/{pid}"
    if not new_attrs:
        resp = request("DELETE", path, params={"dataSource": ds})
        return resp.ok or resp.status_code == 404, resp.text

    # Campos no updateMask e ausentes do corpo são apagados da fonte.
    mask = ",".join(_mask_path(k) for k in changed_keys)
    body = {"productAttributes": {k: new_attrs[k] for k in changed_keys if k in new_attrs}}
    resp = request("PATCH", path, params={"dataSource": ds, "updateMask": mask}, json=body)
    if resp.status_code == 404:
        lang, feed_label, offer_id = pid.split("~", 2)
        resp = request("POST", f"/products/v1/{account()}/productInputs:insert",
                       params={"dataSource": ds},
                       json={"offerId": offer_id, "contentLanguage": lang, "feedLabel": feed_label,
                             "productAttributes": new_attrs})
    return resp.ok, resp.text


def apply(changes, label, dry_run=True):
    """changes: {product_id: {atributo: valor ou None para remover}}."""
    state = load_state()
    items = []
    for pid, attrs in changes.items():
        before_all = state.get(pid, {})
        changed = {k: v for k, v in attrs.items() if before_all.get(k) != v}
        if changed:
            items.append({"product_id": pid,
                          "before": {k: before_all.get(k) for k in changed},
                          "after": changed})

    print(f"{label}: {len(items)} produto(s) com alteração ({len(changes) - len(items)} já estavam iguais)")
    for it in items[:15]:
        print(f"  {it['product_id']}")
        for k, v in it["after"].items():
            print(f"      {k}: {_fmt(it['before'][k])} -> {_fmt(v)}")
    if len(items) > 15:
        print(f"  ... e mais {len(items) - 15}")
    if dry_run or not items:
        if dry_run and items:
            print("\nSimulação apenas. Rode de novo com --aplicar para enviar ao Google.")
        return None

    def run(it):
        pid = it["product_id"]
        new_attrs = {**state.get(pid, {}), **it["after"]}
        new_attrs = {k: v for k, v in new_attrs.items() if v is not None}
        ok, text = _write(pid, new_attrs, list(it["after"]))
        return it, new_attrs, ok, text

    batch_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    done, failed = [], []
    with ThreadPoolExecutor(WORKERS) as pool:
        for n, (it, new_attrs, ok, text) in enumerate(pool.map(run, items), 1):
            if ok:
                if new_attrs:
                    state[it["product_id"]] = new_attrs
                else:
                    state.pop(it["product_id"], None)
                done.append(it)
            else:
                failed.append({**it, "error": text[:500]})
            if n % 50 == 0:
                print(f"  {n}/{len(items)}...")

    save_state(state)
    if not done:
        print(f"\nNenhum produto enviado; {len(failed)} com erro.")
        for f in failed[:5]:
            print(f"  ERRO {f['product_id']}: {f['error'][:300]}")
        return None
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    batch = {"id": batch_id, "label": label, "created": datetime.now().isoformat(timespec="seconds"),
             "undone": False, "items": done, "failed": failed}
    (BATCH_DIR / f"{batch_id}.json").write_text(json.dumps(batch, indent=1, ensure_ascii=False))
    print(f"\nLote {batch_id}: {len(done)} enviados, {len(failed)} com erro.")
    for f in failed[:5]:
        print(f"  ERRO {f['product_id']}: {f['error'][:200]}")
    print(f"Para desfazer: python mc.py undo {batch_id} --aplicar")
    return batch


def _fmt(v):
    if isinstance(v, dict) and "amountMicros" in v:
        return f"{int(v['amountMicros']) / 1_000_000:.2f} {v.get('currencyCode', '')}"
    return "(vazio)" if v is None else str(v)


def list_batches():
    if not BATCH_DIR.exists():
        return []
    return [json.loads(p.read_text()) for p in sorted(BATCH_DIR.glob("*.json"))]


def undo(batch_id, dry_run=True):
    path = BATCH_DIR / f"{batch_id}.json"
    if not path.exists():
        raise SystemExit(f"Lote {batch_id} não encontrado. Veja: python mc.py batches")
    batch = json.loads(path.read_text())
    if batch.get("undone"):
        raise SystemExit(f"O lote {batch_id} já foi desfeito.")
    changes = {it["product_id"]: it["before"] for it in batch["items"]}
    result = apply(changes, f"Desfazer lote {batch_id} ({batch['label']})", dry_run)
    if result is not None:
        batch["undone"] = result["id"]
        path.write_text(json.dumps(batch, indent=1, ensure_ascii=False))


def clear(product_ids, dry_run=True):
    """Remove tudo o que a fonte suplementar tem para esses produtos."""
    state = load_state()
    changes = {pid: {k: None for k in state.get(pid, {})} for pid in product_ids}
    known = {pid: c for pid, c in changes.items() if c}
    unknown = [pid for pid, c in changes.items() if not c]
    if known:
        apply(known, "Limpar fonte suplementar", dry_run)
    # Produtos gravados fora do programa (sem histórico local): apaga direto.
    for pid in unknown:
        if dry_run:
            print(f"  {pid}: será apagado da fonte suplementar (sem histórico local)")
            continue
        resp = request("DELETE", f"/products/v1/{account()}/productInputs/{pid}",
                       params={"dataSource": data_source()})
        print(f"  {pid}: {'apagado' if resp.ok else 'não havia registro' if resp.status_code == 404 else resp.text[:200]}")
    if dry_run and unknown:
        print("\nSimulação apenas. Rode de novo com --aplicar.")


def add_filter_args(parser):
    g = parser.add_argument_group("filtros de produtos")
    g.add_argument("--busca", help="trecho do título (ignora acentos e maiúsculas)")
    g.add_argument("--marca", help="marca exata, ex.: Asics")
    g.add_argument("--tipo", help="trecho do tipo de produto (product type), ex.: Raquetes")
    g.add_argument("--ids", help="arquivo com um offer_id ou product_id por linha")
    g.add_argument("--em-estoque", action="store_true", help="só produtos em estoque")


def select(products, args):
    ids = None
    if getattr(args, "ids", None):
        ids = {line.strip() for line in open(args.ids, encoding="utf-8") if line.strip()}
    out = []
    for p in products:
        a = p.get("productAttributes", {})
        if args.busca and normalize(args.busca) not in normalize(a.get("title")):
            continue
        if args.marca and normalize(args.marca) != normalize(a.get("brand")):
            continue
        if args.tipo and not any(normalize(args.tipo) in normalize(t) for t in a.get("productTypes", [])):
            continue
        if ids is not None and p["offerId"] not in ids and p["name"].split("/")[-1] not in ids:
            continue
        if args.em_estoque and a.get("availability") != "IN_STOCK":
            continue
        out.append(p)
    return out


def require_filter(args):
    if not any([args.busca, args.marca, args.tipo, args.ids]) and not getattr(args, "todos", False):
        raise SystemExit("Informe um filtro (--busca, --marca, --tipo, --ids) ou --todos para o catálogo inteiro.")
