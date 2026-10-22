"""Acesso à Merchant API: autenticação, chamadas, paginação e relatórios."""
import json
import os
import sys
import threading
import unicodedata
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

BASE = "https://merchantapi.googleapis.com"
SCOPES = ["https://www.googleapis.com/auth/content"]
DATA_DIR = ROOT / "dados"

_local = threading.local()


def env(name):
    value = os.getenv(name)
    if not value:
        sys.exit(f"Defina {name} no arquivo .env (veja .env.example)")
    return value


def session():
    # Uma sessão por thread: as atualizações em massa rodam em paralelo.
    if not hasattr(_local, "session"):
        # Conteúdo do JSON numa variável (ambiente da nuvem) tem prioridade sobre o arquivo.
        raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if raw:
            creds = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=SCOPES)
        else:
            path = Path(env("GOOGLE_APPLICATION_CREDENTIALS"))
            if not path.is_absolute():
                path = ROOT / path
            creds = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
        _local.session = AuthorizedSession(creds)
    return _local.session


def request(method, path, **kwargs):
    return session().request(method, f"{BASE}{path}", timeout=60, **kwargs)


def call(method, path, **kwargs):
    resp = request(method, path, **kwargs)
    if not resp.ok:
        sys.exit(f"Erro {resp.status_code}:\n{resp.text}")
    return resp.json() if resp.text else {}


def show(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def account():
    return f"accounts/{env('MERCHANT_ID')}"


def data_source(value=None):
    value = value or env("DATA_SOURCE")
    return value if value.startswith("accounts/") else f"{account()}/dataSources/{value}"


def money(value, currency="BRL"):
    return {"amountMicros": str(round(value * 1_000_000)), "currencyCode": currency}


def from_money(m):
    return int(m.get("amountMicros", 0)) / 1_000_000 if m else None


def normalize(text):
    text = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def all_products():
    token = None
    while True:
        params = {"pageSize": 1000}
        if token:
            params["pageToken"] = token
        data = call("GET", f"/products/v1/{account()}/products", params=params)
        yield from data.get("products", [])
        token = data.get("nextPageToken")
        if not token:
            return


def product_id(p):
    return p["name"].split("/")[-1]


def report(query):
    """Executa uma consulta MCQL e devolve cada linha já sem o nome da view."""
    token = None
    while True:
        body = {"query": query, "pageSize": 1000}
        if token:
            body["pageToken"] = token
        resp = request("POST", f"/reports/v1/{account()}/reports:search", json=body)
        if not resp.ok:
            sys.exit(f"Erro {resp.status_code} no relatório:\n{resp.text}")
        data = resp.json()
        for row in data.get("results", []):
            yield next(iter(row.values()))
        token = data.get("nextPageToken")
        if not token:
            return


def performance_by_offer(start, end):
    """Soma impressões/cliques/conversões por produto. A chave é o offer_id em minúsculas,
    porque o relatório devolve os IDs assim (shopify_zz_...) e o catálogo não."""
    totals = {}
    for r in report(
        "SELECT offer_id, impressions, clicks, conversions, conversion_value "
        f"FROM product_performance_view WHERE date BETWEEN '{start}' AND '{end}'"
    ):
        oid = (r.get("offerId") or "").lower()
        if not oid:
            continue
        t = totals.setdefault(oid, {"impressions": 0, "clicks": 0, "conversions": 0.0, "revenue": 0.0})
        t["impressions"] += int(r.get("impressions", 0) or 0)
        t["clicks"] += int(r.get("clicks", 0) or 0)
        t["conversions"] += float(r.get("conversions", 0) or 0)
        t["revenue"] += from_money(r.get("conversionValue")) or 0
    return totals


def save_csv(path, rows):
    import csv
    if not rows:
        print(f"Nada para salvar em {path}")
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSalvo em {path} ({len(rows)} linhas)")
