"""Atualizações em massa: promoções de preço, CSV, rótulos personalizados e textos."""
import csv
from datetime import date, timedelta

from . import supplemental as sup
from .api import all_products, from_money, money, performance_by_offer, product_id, save_csv

TZ = "-03:00"  # horário de Brasília


def period(start, end):
    """Datas AAAA-MM-DD -> intervalo RFC3339 (início 00:00, fim 23:59:59)."""
    if not start and not end:
        return None
    start = start or date.today().isoformat()
    if not end:
        raise SystemExit("Informe --fim junto com --inicio.")
    return {"startTime": f"{start}T00:00:00{TZ}", "endTime": f"{end}T23:59:59{TZ}"}


def cmd_discount(args):
    sup.require_filter(args)
    products = sup.select(list(all_products()), args)
    interval = period(args.inicio, args.fim)
    changes = {}
    for p in products:
        price = p.get("productAttributes", {}).get("price")
        if not price:
            continue
        value = from_money(price)
        sale = round(value * (1 - args.desconto / 100), 2)
        changes[product_id(p)] = {"salePrice": money(sale, price.get("currencyCode", "BRL")),
                                  "salePriceEffectiveDate": interval}
    sup.apply(changes, f"Desconto de {args.desconto:g}% ({len(products)} produtos)", not args.aplicar)


def cmd_end_discount(args):
    sup.require_filter(args)
    products = sup.select(list(all_products()), args)
    changes = {product_id(p): {"salePrice": None, "salePriceEffectiveDate": None} for p in products}
    sup.apply(changes, "Encerrar desconto", not args.aplicar)


def _parse_value(column, raw, currency):
    raw = raw.strip()
    if raw == "":
        return ...  # célula vazia: não mexe no campo
    if raw.upper() in ("-", "LIMPAR", "REMOVER"):
        return None
    if column in ("price", "sale_price"):
        return money(float(raw.replace(",", ".")), currency)
    if column == "availability":
        return raw.upper()
    return raw


def cmd_csv(args):
    """CSV com product_id (ou offer_id) e colunas: price, sale_price, sale_start, sale_end,
    availability, title, description, link, image_link, custom_label_0..4.
    Célula vazia = não mexe; "-" = remove o valor gravado (volta o da Shopify)."""
    products = {p["offerId"]: p for p in all_products()}
    changes, missing = {}, []
    with open(args.arquivo, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = {k.strip().lower(): (v or "") for k, v in row.items() if k}
            ident = row.get("product_id") or row.get("offer_id", "")
            p = products.get(ident) or products.get(ident.split("~")[-1])
            if not p:
                missing.append(ident)
                continue
            currency = p.get("productAttributes", {}).get("price", {}).get("currencyCode", "BRL")
            attrs = {}
            for column, key in sup.FIELDS.items():
                if column in row:
                    value = _parse_value(column, row[column], currency)
                    if value is not ...:
                        attrs[key] = value
            if row.get("sale_start") or row.get("sale_end"):
                attrs["salePriceEffectiveDate"] = period(row.get("sale_start"), row.get("sale_end"))
            if attrs:
                changes[product_id(p)] = attrs
    if missing:
        print(f"Atenção: {len(missing)} linha(s) com produto não encontrado: {', '.join(missing[:10])}")
    sup.apply(changes, f"Planilha {args.arquivo}", not args.aplicar)


def cmd_label(args):
    sup.require_filter(args)
    products = sup.select(list(all_products()), args)
    key = f"customLabel{args.slot}"
    value = None if args.remover else args.valor
    if value is None and not args.remover:
        raise SystemExit("Informe --valor ou --remover.")
    changes = {product_id(p): {key: value} for p in products
               if args.remover or p.get("productAttributes", {}).get(key) != value}
    sup.apply(changes, f"Rótulo {args.slot} = {value or '(remover)'}", not args.aplicar)


def cmd_auto_labels(args):
    """Rótulo 0: desempenho | rótulo 1: margem | rótulo 2: promoção."""
    products = list(all_products())
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=args.dias - 1)
    perf = performance_by_offer(start, end)

    def score(o):
        r = perf.get(o.lower(), {})
        return (r.get("conversions", 0), r.get("clicks", 0))

    with_clicks = sorted((p["offerId"] for p in products if score(p["offerId"])[1] > 0),
                         key=score, reverse=True)
    top = set(with_clicks[:max(1, len(with_clicks) * args.top // 100)]) if with_clicks else set()

    changes, stats = {}, {}
    has_cost = False
    for p in products:
        a = p.get("productAttributes", {})
        r = perf.get(p["offerId"].lower(), {})
        if p["offerId"] in top:
            perf_label = "mais-vendidos"
        elif r.get("impressions", 0) == 0:
            perf_label = "sem-exposicao"
        else:
            perf_label = "normal"

        price = from_money(a.get("salePrice")) or from_money(a.get("price"))
        cost = from_money(a.get("costOfGoodsSold"))
        margin_label = None
        if cost and price:
            has_cost = True
            m = (price - cost) / price * 100
            margin_label = "margem-alta" if m >= args.margem_alta else "margem-baixa" if m < args.margem_baixa else "margem-media"

        regular, sale = from_money(a.get("price")), from_money(a.get("salePrice"))
        promo_label = "liquidacao" if regular and sale and sale <= regular * (1 - args.liquidacao / 100) \
            else "em-promocao" if regular and sale and sale < regular else "preco-cheio"

        wanted = {"customLabel0": perf_label, "customLabel2": promo_label}
        if margin_label:
            wanted["customLabel1"] = margin_label
        for k, v in wanted.items():
            stats.setdefault(k, {}).setdefault(v, 0)
            stats[k][v] += 1
        diff = {k: v for k, v in wanted.items() if a.get(k) != v}
        if diff:
            changes[product_id(p)] = diff

    names = {"customLabel0": "Rótulo 0 (desempenho)", "customLabel1": "Rótulo 1 (margem)",
             "customLabel2": "Rótulo 2 (promoção)"}
    print(f"Período de desempenho: {start} a {end}\n")
    for k in sorted(stats):
        print(f"{names[k]}: " + ", ".join(f"{v} = {n}" for v, n in sorted(stats[k].items())))
    if not has_cost:
        print("Rótulo 1 (margem): ignorado — os produtos não têm custo (cost_of_goods_sold) no feed.")
    print()
    sup.apply(changes, "Rótulos automáticos", not args.aplicar)


def cmd_texts_export(args):
    products = sup.select(list(all_products()), args)
    if args.limite:
        products = products[:args.limite]
    rows = []
    for p in products:
        a = p.get("productAttributes", {})
        rows.append({
            "product_id": product_id(p), "marca": a.get("brand", ""),
            "tipo": " > ".join(a.get("productTypes", [])[:1]),
            "titulo_atual": a.get("title", ""), "descricao_atual": a.get("description", ""),
            "novo_titulo": "", "nova_descricao": "",
        })
    save_csv(args.arquivo, rows)
    print("Preencha novo_titulo / nova_descricao (deixe vazio para não mexer) e rode texts-apply.")


def cmd_texts_apply(args):
    changes, problems = {}, []
    with open(args.arquivo, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            attrs = {}
            title = (row.get("novo_titulo") or "").strip()
            desc = (row.get("nova_descricao") or "").strip()
            if title:
                if len(title) > 150:
                    problems.append(f"{row['product_id']}: título com {len(title)} caracteres (máx. 150)")
                    continue
                attrs["title"] = title
            if desc:
                if len(desc) > 5000:
                    problems.append(f"{row['product_id']}: descrição com {len(desc)} caracteres (máx. 5000)")
                    continue
                attrs["description"] = desc
            if attrs:
                changes[row["product_id"]] = attrs
    for p in problems:
        print(f"Ignorado — {p}")
    sup.apply(changes, f"Textos de {args.arquivo}", not args.aplicar)


def cmd_batches(args):
    batches = sup.list_batches()
    if not batches:
        print("Nenhum lote enviado ainda.")
    for b in batches:
        status = f"desfeito pelo lote {b['undone']}" if b.get("undone") else "ativo"
        print(f"{b['id']}  {len(b['items']):>5} produtos  {status:<28} {b['label']}")
    state = sup.load_state()
    print(f"\nProdutos com valores gravados na fonte suplementar: {len(state)}")


def cmd_undo(args):
    sup.undo(args.lote, not args.aplicar)


def cmd_clear(args):
    ids = list(args.product_ids)
    if args.tudo:
        ids = list(sup.load_state())
    if not ids:
        raise SystemExit("Informe os product_ids ou --tudo.")
    sup.clear(ids, not args.aplicar)
