"""Saúde do catálogo, avisos de mudança de status e relatórios de desempenho."""
import json
import subprocess
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

from .api import (DATA_DIR, account, all_products, from_money, normalize, performance_by_offer, report,
                  request, save_csv)

SEVERITY_ORDER = {"DISAPPROVED": 0, "DEMOTED": 1, "NOT_IMPACTED": 2}
SEVERITY_PT = {"DISAPPROVED": "REPROVADO", "DEMOTED": "REBAIXADO", "NOT_IMPACTED": "ALERTA"}


def cmd_health(args):
    products = list(all_products())
    by_context = defaultdict(Counter)
    issues, issue_products, rows = {}, defaultdict(set), []

    for p in products:
        attrs = p.get("productAttributes", {})
        status = p.get("productStatus", {})
        for d in status.get("destinationStatuses", []):
            ctx = d.get("reportingContext", "?")
            if d.get("disapprovedCountries"):
                by_context[ctx]["reprovado"] += 1
            elif d.get("pendingCountries"):
                by_context[ctx]["pendente"] += 1
            elif d.get("approvedCountries"):
                by_context[ctx]["aprovado"] += 1
        for i in status.get("itemLevelIssues", []):
            key = (i.get("code"), i.get("severity"))
            issues.setdefault(key, i)
            issue_products[key].add(p["offerId"])
            rows.append({
                "offer_id": p["offerId"], "titulo": attrs.get("title", ""), "link": attrs.get("link", ""),
                "severidade": SEVERITY_PT.get(i.get("severity"), i.get("severity")), "codigo": i.get("code"),
                "atributo": i.get("attribute", ""), "destino": i.get("reportingContext", ""),
                "descricao": i.get("description", ""), "detalhe": i.get("detail", ""),
                "documentacao": i.get("documentation", ""),
            })

    print(f"Produtos no catálogo: {len(products)}\n")
    print("Status por destino:")
    for ctx, c in sorted(by_context.items()):
        print(f"  {ctx:<34} aprovados {c['aprovado']:>5}  pendentes {c['pendente']:>4}  reprovados {c['reprovado']:>4}")

    print("\nProblemas (por número de produtos afetados):")
    for key in sorted(issues, key=lambda k: (SEVERITY_ORDER.get(k[1], 9), -len(issue_products[k]))):
        i = issues[key]
        attr = f" ({i['attribute']})" if i.get("attribute") else ""
        print(f"  [{SEVERITY_PT.get(key[1], key[1]):<9}] {len(issue_products[key]):>5} produtos  {i.get('description', key[0])}{attr}")

    if args.csv:
        save_csv(args.csv, rows)

    resp = request("GET", f"/accounts/v1/{account()}/issues", params={"languageCode": "pt-BR"})
    if resp.ok:
        acc = resp.json().get("accountIssues", [])
        print(f"\nProblemas da conta: {len(acc) or 'nenhum'}")
        for a in acc:
            print(f"  [{a.get('severity')}] {a.get('title')}: {a.get('detail', '')}")


def _snapshot():
    snap = {}
    for p in all_products():
        status = p.get("productStatus", {})
        snap[p["offerId"]] = {
            "titulo": p.get("productAttributes", {}).get("title", ""),
            "reprovado_em": sorted(d["reportingContext"] for d in status.get("destinationStatuses", [])
                                   if d.get("disapprovedCountries")),
            "problemas": sorted({f"{SEVERITY_PT.get(i.get('severity'), i.get('severity'))}: {i.get('description')}"
                                 for i in status.get("itemLevelIssues", [])
                                 if i.get("severity") != "NOT_IMPACTED"}),
        }
    return snap


def cmd_watch(args):
    """Compara o status atual com a última execução e registra o que mudou."""
    DATA_DIR.mkdir(exist_ok=True)
    snap_file, log_file = DATA_DIR / "status-anterior.json", DATA_DIR / "alertas.log"
    current = _snapshot()
    if not snap_file.exists():
        snap_file.write_text(json.dumps(current, ensure_ascii=False))
        print(f"Primeira execução: fotografei o status de {len(current)} produtos. "
              "Nas próximas, aviso o que mudou.")
        return
    previous = json.loads(snap_file.read_text())
    events = []
    for oid, now in current.items():
        before = previous.get(oid)
        if before is None:
            events.append(f"NOVO        {now['titulo']}")
            continue
        if now["reprovado_em"] and not before["reprovado_em"]:
            events.append(f"REPROVADO   {now['titulo']} — {'; '.join(now['problemas']) or 'ver Merchant Center'}")
        elif before["reprovado_em"] and not now["reprovado_em"]:
            events.append(f"APROVADO    {now['titulo']}")
        else:
            for prob in set(now["problemas"]) - set(before["problemas"]):
                events.append(f"PROBLEMA    {now['titulo']} — {prob}")
    for oid in set(previous) - set(current):
        events.append(f"REMOVIDO    {previous[oid]['titulo']}")

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if events:
        with open(log_file, "a", encoding="utf-8") as f:
            f.writelines(f"{stamp}  {e}\n" for e in events)
        print(f"{len(events)} mudança(s) desde a última verificação:")
        for e in events:
            print(f"  {e}")
        print(f"\nHistórico em {log_file}")
        if args.notificar:
            reprovados = sum(e.startswith("REPROVADO") for e in events)
            msg = f"{len(events)} mudança(s) no catálogo, {reprovados} reprovação(ões)"
            subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "Merchant Center"'],
                           check=False)
    else:
        print(f"{stamp}: nenhuma mudança de status.")
    snap_file.write_text(json.dumps(current, ensure_ascii=False))


def _period(days):
    end = date.today() - timedelta(days=1)
    return end - timedelta(days=days - 1), end


def cmd_performance(args):
    start, end = _period(args.dias)
    perf = performance_by_offer(start, end)
    products = {p["offerId"]: p for p in all_products()}

    rows = []
    for oid, p in products.items():
        a = p.get("productAttributes", {})
        r = perf.get(oid.lower(), {})
        imp, clicks, conv = r.get("impressions", 0), r.get("clicks", 0), r.get("conversions", 0)
        if imp == 0:
            group = "nunca aparece"
        elif clicks >= args.min_cliques and conv == 0:
            group = "aparece e não vende"
        elif conv > 0:
            group = "vende"
        else:
            group = "aparece, poucos cliques"
        rows.append({
            "offer_id": oid, "titulo": a.get("title", ""), "disponibilidade": a.get("availability", ""),
            "preco": from_money(a.get("salePrice")) or from_money(a.get("price")),
            "impressoes": imp, "cliques": clicks,
            "ctr_%": round(clicks / imp * 100, 2) if imp else 0,
            "conversoes": conv, "receita": round(r.get("revenue", 0), 2), "grupo": group,
        })

    total_imp = sum(r["impressoes"] for r in rows)
    total_clk = sum(r["cliques"] for r in rows)
    total_conv = sum(r["conversoes"] for r in rows)
    print(f"Período: {start} a {end}")
    print(f"Impressões {total_imp:,} | Cliques {total_clk:,} | Conversões {total_conv:,.0f}".replace(",", "."))
    if total_conv == 0:
        print("Obs.: nenhuma conversão registrada — se você usa Google Ads, verifique se o "
              "acompanhamento de conversões está ligado ao Merchant Center.")
    groups = Counter(r["grupo"] for r in rows)
    print("\nGrupos:")
    for g in ("vende", "aparece e não vende", "aparece, poucos cliques", "nunca aparece"):
        print(f"  {g:<26} {groups.get(g, 0):>5} produtos")

    def top(group, key, n=10):
        sel = sorted((r for r in rows if r["grupo"] == group), key=lambda r: r[key], reverse=True)[:n]
        for r in sel:
            print(f"    {r['impressoes']:>7} imp  {r['cliques']:>5} cliques  {r['titulo'][:70]}")

    print(f"\nMais cliques sem venda (mín. {args.min_cliques} cliques):")
    top("aparece e não vende", "cliques")
    never = [r for r in rows if r["grupo"] == "nunca aparece" and r["disponibilidade"] == "IN_STOCK"]
    print(f"\nEm estoque e sem nenhuma impressão: {len(never)} produtos")
    for r in never[:10]:
        print(f"    {r['titulo'][:80]}")

    if args.csv:
        save_csv(args.csv, rows)


def cmd_prices(args):
    rows = []
    for r in report(
        "SELECT id, report_country_code, offer_id, title, brand, price, benchmark_price "
        "FROM price_competitiveness_product_view WHERE report_country_code = 'BR'"
    ):
        price, bench = from_money(r.get("price")), from_money(r.get("benchmarkPrice"))
        if not price or not bench:
            continue
        rows.append({"offer_id": r.get("offerId"), "titulo": r.get("title", ""), "marca": r.get("brand", ""),
                     "seu_preco": price, "preco_referencia": bench,
                     "diferenca_%": round((price - bench) / bench * 100, 1)})
    if not rows:
        print("O Google ainda não tem preço de referência para os seus produtos "
              "(exige volume de dados suficiente na categoria).")
        return
    rows.sort(key=lambda r: r["diferenca_%"], reverse=True)
    above = [r for r in rows if r["diferenca_%"] > args.margem]
    below = [r for r in rows if r["diferenca_%"] < -args.margem]
    print(f"{len(rows)} produtos com preço de referência do mercado.")
    print(f"  Mais caros que o mercado (> {args.margem:g}%): {len(above)}")
    print(f"  Na média: {len(rows) - len(above) - len(below)}")
    print(f"  Mais baratos (< -{args.margem:g}%): {len(below)}")
    print("\nMais acima do mercado:")
    for r in above[:10]:
        print(f"  {r['diferenca_%']:>+6.1f}%  R$ {r['seu_preco']:>8.2f} vs R$ {r['preco_referencia']:>8.2f}  {r['titulo'][:60]}")
    print("\nMais abaixo do mercado:")
    for r in below[-10:][::-1]:
        print(f"  {r['diferenca_%']:>+6.1f}%  R$ {r['seu_preco']:>8.2f} vs R$ {r['preco_referencia']:>8.2f}  {r['titulo'][:60]}")
    if args.csv:
        save_csv(args.csv, rows)


def cmd_price_insights(args):
    rows = []
    for r in report(
        "SELECT id, offer_id, title, price, suggested_price, predicted_impressions_change_fraction, "
        "predicted_clicks_change_fraction, predicted_conversions_change_fraction "
        "FROM price_insights_product_view"
    ):
        price, sug = from_money(r.get("price")), from_money(r.get("suggestedPrice"))
        if not price or not sug:
            continue
        rows.append({"offer_id": r.get("offerId"), "titulo": r.get("title", ""), "preco": price,
                     "preco_sugerido": sug,
                     "impressoes_%": round(float(r.get("predictedImpressionsChangeFraction", 0) or 0) * 100, 1),
                     "cliques_%": round(float(r.get("predictedClicksChangeFraction", 0) or 0) * 100, 1),
                     "conversoes_%": round(float(r.get("predictedConversionsChangeFraction", 0) or 0) * 100, 1)})
    if not rows:
        print("Sem sugestões de preço do Google no momento (exige volume de dados suficiente).")
        return
    rows.sort(key=lambda r: r["conversoes_%"], reverse=True)
    print(f"{len(rows)} produtos com sugestão de preço. Maiores ganhos previstos em conversões:\n")
    for r in rows[:15]:
        print(f"  R$ {r['preco']:>8.2f} -> R$ {r['preco_sugerido']:>8.2f}  conversões {r['conversoes_%']:>+6.1f}%  "
              f"cliques {r['cliques_%']:>+6.1f}%  {r['titulo'][:50]}")
    if args.csv:
        save_csv(args.csv, rows)


def cmd_bestsellers(args):
    where = "report_country_code = 'BR' AND report_granularity = 'WEEKLY'"
    if args.categoria:
        where += f" AND report_category_id = {int(args.categoria)}"
    rows = []
    for r in report(
        "SELECT report_country_code, report_granularity, report_date, report_category_id, rank, previous_rank, title, brand, relative_demand, "
        "inventory_status, brand_inventory_status, category_l1, category_l2, category_l3 "
        f"FROM best_sellers_product_cluster_view WHERE {where} ORDER BY rank"
    ):
        cats = (r.get("categoryL1"), r.get("categoryL2"), r.get("categoryL3"))
        if args.sub and not any(normalize(args.sub) in normalize(c) for c in cats if c):
            continue
        rows.append({
            "ranking": r.get("rank"), "ranking_anterior": r.get("previousRank"),
            "titulo": r.get("title", ""), "marca": r.get("brand", ""),
            "categoria": " > ".join(c for c in cats if c),
            "demanda": r.get("relativeDemand", ""), "seu_estoque": r.get("inventoryStatus", ""),
            "marca_no_seu_catalogo": r.get("brandInventoryStatus", ""), "semana": r.get("reportDate", ""),
        })
    rows = rows[:args.limite]
    if not rows:
        print("Sem dados de mais vendidos para esse filtro (a conta precisa estar elegível ao relatório).")
        return
    missing = [r for r in rows if r["seu_estoque"] == "NOT_IN_INVENTORY"]
    print(f"Top {len(rows)} mais vendidos no Brasil"
          f"{' (categoria ' + str(args.categoria) + (' / ' + args.sub if args.sub else '') + ')' if args.categoria else ''}. "
          f"Você NÃO tem {len(missing)} deles:\n")
    status = {"IN_STOCK": "tem", "OUT_OF_STOCK": "sem estoque", "NOT_IN_INVENTORY": "NÃO TEM"}
    for r in rows[:args.mostrar]:
        print(f"  #{r['ranking']:<4} [{status.get(r['seu_estoque'], r['seu_estoque']):<11}] "
              f"{r['marca'][:15]:<15} {r['titulo'][:60]}")
    if args.csv:
        save_csv(args.csv, rows)
