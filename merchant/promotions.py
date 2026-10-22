"""Promoções do Google (cupom, desconto, frete grátis) exibidas junto com os produtos."""
import os

from . import supplemental as sup
from .api import account, all_products, call, money, request, show
from .bulk import period

PROMO_SOURCE = os.getenv("PROMO_DATA_SOURCE", "10584796100")


def cmd_promo_list(args):
    data = call("GET", f"/promotions/v1/{account()}/promotions", params={"pageSize": 250})
    promos = data.get("promotions", [])
    if not promos:
        print("Nenhuma promoção cadastrada via API.")
    for p in promos:
        a = p.get("attributes", {})
        period_ = a.get("promotionEffectiveTimePeriod", {})
        status = p.get("promotionStatus", {}).get("destinationStatuses", [])
        states = ", ".join(f"{s.get('reportingContext')}: {s.get('status')}" for s in status) or "processando"
        print(f"{p.get('promotionId'):<25} {a.get('longTitle', '')[:50]:<50} "
              f"{period_.get('startTime', '')[:10]} a {period_.get('endTime', '')[:10]}  [{states}]")
    if args.raw:
        show(data)


def cmd_promo_create(args):
    attrs = {
        "longTitle": args.titulo,
        "promotionEffectiveTimePeriod": period(args.inicio, args.fim),
        "promotionDestinations": ["SHOPPING_ADS", "FREE_LISTINGS"],
    }
    if args.cupom:
        attrs.update(offerType="GENERIC_CODE", genericRedemptionCode=args.cupom)
    else:
        attrs["offerType"] = "NO_CODE"

    if args.modalidade == "percentual":
        attrs.update(couponValueType="PERCENT_OFF", percentOff=str(int(args.valor)))
    elif args.modalidade == "valor":
        attrs.update(couponValueType="MONEY_OFF", moneyOffAmount=money(args.valor))
    else:
        attrs["couponValueType"] = "FREE_SHIPPING_STANDARD"
    if args.compra_minima:
        attrs["minimumPurchaseAmount"] = money(args.compra_minima)
    if args.link:
        attrs["promotionUrl"] = args.link

    if any([args.busca, args.marca, args.tipo, args.ids]):
        products = sup.select(list(all_products()), args)
        if not products:
            raise SystemExit("Nenhum produto corresponde ao filtro.")
        attrs.update(productApplicability="SPECIFIC_PRODUCTS",
                     itemIdInclusion=[p["offerId"] for p in products][:1000])
        scope = f"{len(products)} produtos"
    else:
        attrs["productApplicability"] = "ALL_PRODUCTS"
        scope = "todos os produtos"

    body = {
        "promotion": {
            "promotionId": args.id, "contentLanguage": "pt", "targetCountry": "BR",
            "redemptionChannel": ["ONLINE"], "attributes": attrs,
        },
        "dataSource": f"{account()}/dataSources/{PROMO_SOURCE}",
    }
    print(f"Promoção '{args.titulo}' ({args.id}) para {scope}, de {args.inicio or 'hoje'} a {args.fim}.")
    if args.cupom:
        print(f"Cupom: {args.cupom} — ele precisa existir e funcionar no checkout da Shopify.")
    if not args.aplicar:
        show(body)
        print("\nSimulação apenas. Rode de novo com --aplicar para enviar ao Google.")
        return
    resp = request("POST", f"/promotions/v1/{account()}/promotions:insert", json=body)
    if not resp.ok:
        raise SystemExit(f"Erro {resp.status_code}:\n{resp.text}")
    print("Enviada. O Google analisa promoções em até 24-48 h; acompanhe com: python mc.py promo-list")
