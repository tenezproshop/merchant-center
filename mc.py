#!/usr/bin/env python3
"""CLI para a Google Merchant API (sucessora da Content API for Shopping).

Comandos que alteram dados só simulam; acrescente --aplicar para enviar ao Google.

Consulta:      list, get, search, datasources
Saúde:         health, watch
Relatórios:    performance, prices, price-insights, bestsellers
Em massa:      discount, end-discount, csv, label, auto-labels, update
Textos:        texts-export, texts-apply
Desfazer:      batches, undo, clear
Promoções:     promo-list, promo-create
"""
import argparse
import sys

from merchant import bulk, promotions, reports
from merchant import supplemental as sup
from merchant.api import account, call, from_money, money, product_id, report, show


def cmd_register(args):
    # Passo único: vincula o projeto GCP da conta de serviço à conta Merchant Center.
    show(call("POST", f"/accounts/v1/{account()}/developerRegistration:registerGcp",
              json={"developerEmail": args.email}))


def cmd_datasources(args):
    show(call("GET", f"/datasources/v1/{account()}/dataSources"))


def cmd_list(args):
    params = {"pageSize": args.limit}
    if args.page_token:
        params["pageToken"] = args.page_token
    data = call("GET", f"/products/v1/{account()}/products", params=params)
    if args.raw:
        return show(data)
    for p in data.get("products", []):
        attrs = p.get("productAttributes", {})
        price = attrs.get("price", {})
        print(f"{product_id(p):<30} {from_money(price) or 0:>10.2f} {price.get('currencyCode', ''):<4} {attrs.get('title', '')}")
    if data.get("nextPageToken"):
        print(f"\nPróxima página: --page-token {data['nextPageToken']}")


def cmd_get(args):
    show(call("GET", f"/products/v1/{account()}/products/{args.product_id}"))


def cmd_search(args):
    # Busca por título via relatório (MCQL) — a API de produtos não filtra por texto.
    term = args.term.replace("'", "\\'")
    show(list(report(
        "SELECT id, offer_id, title, price, availability, aggregated_reporting_context_status "
        f"FROM product_view WHERE title LIKE '%{term}%' LIMIT {args.limit}"
    )))


def cmd_update(args):
    attrs = {}
    if args.price is not None:
        attrs["price"] = money(args.price, args.currency)
    if args.sale_price is not None:
        attrs["salePrice"] = money(args.sale_price, args.currency)
    for field in ("title", "description", "availability", "link", "image_link"):
        value = getattr(args, field)
        if value is not None:
            attrs[sup.FIELDS[field]] = value
    if not attrs:
        sys.exit("Nada para atualizar: informe ao menos um campo (--price, --title, ...)")
    sup.apply({args.product_id: attrs}, f"Atualizar {args.product_id}", not args.aplicar)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def command(name, func, help, filters=False, apply=False):
        p = sub.add_parser(name, help=help, description=func.__doc__ or help)
        p.set_defaults(func=func)
        if filters:
            sup.add_filter_args(p)
        if apply:
            p.add_argument("--aplicar", action="store_true", help="envia de verdade (sem isso, só simula)")
        return p

    # Configuração e consulta
    p = command("register", cmd_register, "registra o projeto GCP na conta (executar uma vez)")
    p.add_argument("--email", required=True, help="e-mail do desenvolvedor responsável")
    command("datasources", cmd_datasources, "lista as fontes de dados (feeds)")
    p = command("list", cmd_list, "lista produtos")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--page-token")
    p.add_argument("--raw", action="store_true", help="mostra o JSON completo")
    p = command("get", cmd_get, "detalha um produto")
    p.add_argument("product_id", help="formato idioma~feedLabel~offerId")
    p = command("search", cmd_search, "busca produtos pelo título")
    p.add_argument("term")
    p.add_argument("--limit", type=int, default=50)

    # Saúde do catálogo
    p = command("health", reports.cmd_health, "saúde do catálogo: aprovações e problemas")
    p.add_argument("--csv", help="salva o detalhe por produto neste arquivo CSV")
    p = command("watch", reports.cmd_watch, "avisa o que mudou de status desde a última execução")
    p.add_argument("--notificar", action="store_true", help="mostra notificação do macOS se houver mudanças")

    # Relatórios
    p = command("performance", reports.cmd_performance, "impressões, cliques e vendas por produto")
    p.add_argument("--dias", type=int, default=30)
    p.add_argument("--min-cliques", type=int, default=20, help="cliques mínimos para 'aparece e não vende'")
    p.add_argument("--csv")
    p = command("prices", reports.cmd_prices, "seu preço comparado ao preço de referência do mercado")
    p.add_argument("--margem", type=float, default=5, help="%% de diferença considerada 'na média'")
    p.add_argument("--csv")
    p = command("price-insights", reports.cmd_price_insights, "preços sugeridos pelo Google e impacto previsto")
    p.add_argument("--csv")
    p = command("bestsellers", reports.cmd_bestsellers, "mais vendidos no Brasil e se você tem cada um")
    p.add_argument("--categoria", default="988", help="ID da categoria principal do Google "
                   "(988 = Artigos esportivos, 166 = Roupas e acessórios)")
    p.add_argument("--sub", help="trecho da subcategoria em inglês, ex.: Tennis, Shoes, Shorts")
    p.add_argument("--limite", type=int, default=200)
    p.add_argument("--mostrar", type=int, default=30)
    p.add_argument("--csv")

    # Atualizações em massa
    p = command("discount", bulk.cmd_discount, "aplica %% de desconto (preço promocional)", filters=True, apply=True)
    p.add_argument("--desconto", type=float, required=True, help="percentual, ex.: 15")
    p.add_argument("--inicio", help="AAAA-MM-DD (padrão: hoje)")
    p.add_argument("--fim", help="AAAA-MM-DD")
    p.add_argument("--todos", action="store_true", help="aplica ao catálogo inteiro")
    p = command("end-discount", bulk.cmd_end_discount, "remove o preço promocional gravado", filters=True, apply=True)
    p.add_argument("--todos", action="store_true")
    p = command("csv", bulk.cmd_csv, "aplica alterações de uma planilha CSV", apply=True)
    p.add_argument("arquivo")
    p = command("label", bulk.cmd_label, "define um rótulo personalizado (custom label)", filters=True, apply=True)
    p.add_argument("--slot", type=int, choices=range(5), required=True)
    p.add_argument("--valor")
    p.add_argument("--remover", action="store_true")
    p.add_argument("--todos", action="store_true")
    p = command("auto-labels", bulk.cmd_auto_labels, "rótulos automáticos: desempenho, margem e promoção", apply=True)
    p.add_argument("--dias", type=int, default=30)
    p.add_argument("--top", type=int, default=10, help="%% dos produtos com mais vendas/cliques = mais-vendidos")
    p.add_argument("--margem-alta", type=float, default=50)
    p.add_argument("--margem-baixa", type=float, default=30)
    p.add_argument("--liquidacao", type=float, default=30, help="desconto mínimo (%%) para 'liquidacao'")
    p = command("update", cmd_update, "atualiza campos de um produto", apply=True)
    p.add_argument("product_id", help="formato idioma~feedLabel~offerId")
    p.add_argument("--price", type=float)
    p.add_argument("--sale-price", type=float)
    p.add_argument("--currency", default="BRL")
    p.add_argument("--title")
    p.add_argument("--description")
    p.add_argument("--availability", choices=["IN_STOCK", "OUT_OF_STOCK", "PREORDER", "BACKORDER"])
    p.add_argument("--link")
    p.add_argument("--image-link")

    # Textos
    p = command("texts-export", bulk.cmd_texts_export, "exporta títulos/descrições para revisão", filters=True)
    p.add_argument("arquivo")
    p.add_argument("--limite", type=int)
    p = command("texts-apply", bulk.cmd_texts_apply, "envia os textos aprovados da planilha", apply=True)
    p.add_argument("arquivo")

    # Desfazer
    command("batches", bulk.cmd_batches, "lista os lotes enviados")
    p = command("undo", bulk.cmd_undo, "desfaz um lote inteiro", apply=True)
    p.add_argument("lote")
    p = command("clear", bulk.cmd_clear, "remove da fonte suplementar tudo de um produto", apply=True)
    p.add_argument("product_ids", nargs="*")
    p.add_argument("--tudo", action="store_true", help="todos os produtos gravados por este programa")

    # Promoções
    p = command("promo-list", promotions.cmd_promo_list, "lista as promoções do Google")
    p.add_argument("--raw", action="store_true")
    p = command("promo-create", promotions.cmd_promo_create, "cria promoção (cupom, desconto, frete grátis)",
                filters=True, apply=True)
    p.add_argument("--id", required=True, help="identificador único, ex.: black-friday-2026")
    p.add_argument("--titulo", required=True, help="texto exibido, ex.: 10%% off em raquetes Head")
    p.add_argument("--modalidade", choices=["percentual", "valor", "frete"], required=True)
    p.add_argument("--valor", type=float, help="percentual ou valor em R$ (não usado para frete)")
    p.add_argument("--cupom", help="código do cupom; sem isso, desconto automático")
    p.add_argument("--compra-minima", type=float)
    p.add_argument("--link", help="página da promoção no site")
    p.add_argument("--inicio", help="AAAA-MM-DD (padrão: hoje)")
    p.add_argument("--fim", required=True, help="AAAA-MM-DD")

    args = parser.parse_args()
    if args.cmd == "promo-create" and args.modalidade != "frete" and args.valor is None:
        parser.error("--valor é obrigatório para modalidade percentual ou valor")
    args.func(args)


if __name__ == "__main__":
    main()
