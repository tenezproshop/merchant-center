#!/usr/bin/env python3
"""Pente fino do catálogo (somente leitura).

Lê auditoria/produtos.json (baixado com merchant.api.all_products()), auditoria/desempenho.csv,
auditoria/precos.csv e gera auditoria/irregularidades.csv e auditoria/resumo-por-produto.csv.
Não chama a API e não grava nada fora de auditoria/.
"""
import csv
import html
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DIR = Path(__file__).resolve().parent
HOJE = datetime(2026, 10, 22, tzinfo=timezone.utc) if len(sys.argv) < 2 else \
    datetime.fromisoformat(sys.argv[1]).replace(tzinfo=timezone.utc)
DOMINIO = "tenez.com.br"
LABELS_PADRAO = {"mais-vendidos", "normal", "sem-exposicao", "margem-alta", "margem-media", "margem-baixa",
                 "liquidacao", "em-promocao", "preco-cheio"}

GRAV_ORDEM = {"crítico": 0, "alto": 1, "médio": 2, "baixo": 3}
GRAV_PESO = {"crítico": 100, "alto": 20, "médio": 5, "baixo": 1}


def norm(t):
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def money(m):
    return int(m["amountMicros"]) / 1e6 if m and "amountMicros" in m else None


def texto(desc):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", desc or ""))).strip()


# --------------------------------------------------------------------------- tipos de produto
SAPATOS = {"Tênis para jogar Tennis", "Tênis Running e Treino", "Tênis Casual e Sneakers", "Tênis esportivo"}
ROUPAS = {"Camisetas", "Shorts", "Saias", "Camisas Polo", "Vestidos", "Regatas", "Leggings", "Tops", "Bermudas",
          "Jaquetas", "Calças", "Sungas", "Meias"}
ACESS_VEST = {"Bonés", "Viseiras", "Munhequeiras", "Bandanas e Faixas de Cabelo", "Óculos de Sol"}

PALAVRAS_TIPO = {
    **{t: ["tenis"] for t in SAPATOS},
    "Camisetas": ["camiseta", "camisa", "blusa", "t-shirt"], "Shorts": ["short", "bermuda"],
    "Saias": ["saia", "skort"], "Camisas Polo": ["polo"], "Vestidos": ["vestido"],
    "Regatas": ["regata", "tank"], "Leggings": ["legging", "calca"], "Tops": ["top"],
    "Bermudas": ["bermuda", "short"], "Jaquetas": ["jaqueta", "casaco", "corta"], "Calças": ["calca"],
    "Sungas": ["sunga"], "Meias": ["meia"], "Bonés": ["bone"], "Viseiras": ["viseira"],
    "Munhequeiras": ["munhequeira"], "Bandanas e Faixas de Cabelo": ["bandana", "faixa", "testeira", "headband"],
    "Óculos de Sol": ["oculos"], "Mochilas": ["mochila"], "Mochila": ["mochila"],
    "Raquetes de Beach Tennis": ["raquete"], "Raquete de Beach Tennis": ["raquete"],
    "Raquetes de Tênis para Performance": ["raquete"], "Raquetes de Tênis Infantil e Júnior": ["raquete"],
    "Raquetes de Tênis Intermediário": ["raquete"], "Raquetes de Squash": ["raquete"],
    "Raquetes de Pickleball": ["raquete"], "Raquetes de Tênis de Mesa": ["raquete"],
    "Cordas Set Individual": ["corda"], "Cordas Rolo": ["corda"], "Overgrips": ["overgrip", "grip"],
    "Cushion Grip": ["grip"], "Antivibradores": ["antivibrador"], "Toalhas": ["toalha"],
    "Pochetes": ["pochete"], "Chaveiros": ["chaveiro"], "Rebatedores": ["rebatedor"],
    "Bolsas Esportivas": ["bolsa", "mala", "bag"],
    **{t: ["raqueteira", "bolsa", "mochila", "bag"] for t in (
        "Raqueteiras para 12 raquetes", "Raqueteiras para 9 raquetes", "Raqueteiras para 6 raquetes",
        "Raqueteiras para 3 raquetes", "Raqueteiras Infantis", "Raqueteira Tênis",
        "Raqueteiras e Mochilas de Beach Tennis")},
    **{t: ["bola"] for t in ("Bolas de Tênis - Caixa", "Bolas de Tênis - Infantil", "Bolas de Tênis - Pack Econômico",
                             "Bolas de Tênis - Tubo Individual", "Bolas de Beach Tennis", "Bolas de Pickleball",
                             "Bolas de Squash", "Bolas para Autógrafo")},
}

# Categoria do Google esperada para cada tipo (prefixos aceitos, em pt-BR e no equivalente em inglês).
VEST = "Vestuário e acessórios"
ESP_TENIS = "Artigos esportivos > Artigos para prática de esportes > Tênis"
PADEL = "Artigos esportivos > Atividades ao ar livre > Jogos ao ar livre > Tênis de plataforma e padel"
ESPERADA = {}
for t in SAPATOS:
    ESPERADA[t] = ([f"{VEST} > Sapatos", "Apparel & Accessories > Shoes"], f"{VEST} > Sapatos")
for t in ROUPAS - {"Meias", "Sungas"}:
    ESPERADA[t] = ([f"{VEST} > Roupas", "Apparel & Accessories > Clothing"],
                   f"{VEST} > Roupas > (subcategoria do tipo, ex.: Roupas esportivas / Shorts / Short-saia)")
ESPERADA["Meias"] = ([f"{VEST} > Roupas > Roupas íntimas e meias > Meias", "Apparel & Accessories > Clothing > Underwear & Socks > Socks"],
                     f"{VEST} > Roupas > Roupas íntimas e meias > Meias")
ESPERADA["Sungas"] = ([f"{VEST} > Roupas > Roupas de banho", "Apparel & Accessories > Clothing > Swimwear"],
                      f"{VEST} > Roupas > Roupas de banho")
for t in ("Bonés", "Viseiras"):
    ESPERADA[t] = ([f"{VEST} > Acessórios para roupas > Chapéus", "Apparel & Accessories > Clothing Accessories > Hats"],
                   f"{VEST} > Acessórios para roupas > Chapéus")
ESPERADA["Bandanas e Faixas de Cabelo"] = (
    [f"{VEST} > Acessórios para roupas > Acessórios para cabelo", f"{VEST} > Acessórios para roupas > Bandanas",
     "Apparel & Accessories > Clothing Accessories > Hair Accessories"],
    f"{VEST} > Acessórios para roupas > Acessórios para cabelo > Faixas de cabeça")
ESPERADA["Munhequeiras"] = (["Apparel & Accessories > Clothing Accessories > Wristbands", f"{VEST} > Acessórios para roupas > Munhequeiras"],
                            "a subcategoria 'Wristbands' de Vestuário e acessórios > Acessórios para roupas (nome em pt-BR ou ID numérico)")
ESPERADA["Óculos de Sol"] = ([f"{VEST} > Acessórios para roupas > Óculos de sol"], f"{VEST} > Acessórios para roupas > Óculos de sol")
for t in ("Raquetes de Beach Tennis", "Raquete de Beach Tennis"):
    ESPERADA[t] = ([f"{PADEL} > Raquetes de tênis de plataforma e padel",
                    "Sporting Goods > Outdoor Recreation > Outdoor Games > Platform & Paddle Tennis > Platform & Paddle Tennis Paddles"],
                   f"{PADEL} > Raquetes de tênis de plataforma e padel")
for t in ("Raquetes de Tênis para Performance", "Raquetes de Tênis Infantil e Júnior", "Raquetes de Tênis Intermediário"):
    ESPERADA[t] = ([f"{ESP_TENIS} > Raquetes de tênis", "Sporting Goods > Athletics > Tennis > Tennis Racquets"],
                   f"{ESP_TENIS} > Raquetes de tênis")
for t in ("Raqueteiras para 12 raquetes", "Raqueteiras para 9 raquetes", "Raqueteiras para 6 raquetes",
          "Raqueteiras para 3 raquetes", "Raqueteiras Infantis", "Raqueteira Tênis", "Raqueteiras e Mochilas de Beach Tennis",
          "Bolsas Esportivas"):
    ESPERADA[t] = ([f"{ESP_TENIS} > Acessórios para raquetes de tênis > Bolsas para raquetes de tênis", "Malas e bolsas",
                    "Sporting Goods > Athletics > Tennis > Tennis Racquet Accessories > Tennis Racquet Bags"],
                   f"{ESP_TENIS} > Acessórios para raquetes de tênis > Bolsas para raquetes de tênis")
for t in ("Mochilas", "Mochila"):
    ESPERADA[t] = ([f"{ESP_TENIS} > Acessórios para raquetes de tênis > Bolsas para raquetes de tênis", "Malas e bolsas > Mochilas"],
                   "Malas e bolsas > Mochilas (ou ... > Bolsas para raquetes de tênis, se for raqueteira-mochila)")
for t in ("Bolas de Tênis - Caixa", "Bolas de Tênis - Infantil", "Bolas de Tênis - Pack Econômico",
          "Bolas de Tênis - Tubo Individual", "Bolas de Beach Tennis", "Bolas para Autógrafo"):
    ESPERADA[t] = ([f"{ESP_TENIS} > Bolas de tênis"], f"{ESP_TENIS} > Bolas de tênis")
ESPERADA["Bolas de Squash"] = (["Artigos esportivos > Artigos para prática de esportes > Raquetebol e squash"],
                               "Artigos esportivos > Artigos para prática de esportes > Raquetebol e squash (bolas)")
for t in ("Cordas Set Individual", "Cordas Rolo"):
    ESPERADA[t] = ([f"{ESP_TENIS} > Acessórios para raquetes de tênis > Corda da raquete de tênis"],
                   f"{ESP_TENIS} > Acessórios para raquetes de tênis > Corda da raquete de tênis")
for t in ("Overgrips", "Cushion Grip"):
    ESPERADA[t] = ([f"{ESP_TENIS} > Acessórios para raquetes de tênis > Fita e cabos de raquete de tênis"],
                   f"{ESP_TENIS} > Acessórios para raquetes de tênis > Fita e cabos de raquete de tênis")
ESPERADA["Antivibradores"] = ([f"{ESP_TENIS} > Acessórios para raquetes de tênis"], f"{ESP_TENIS} > Acessórios para raquetes de tênis")
ESPERADA["Toalhas"] = (["Casa e jardim > Lençóis e roupas de cama > Toalhas"], "Casa e jardim > Lençóis e roupas de cama > Toalhas")

MARCAS_CONHECIDAS = ["nike", "adidas", "on running", "asics", "fila", "wilson", "yonex", "lacoste", "babolat", "head",
                     "mormaii", "k-swiss", "le coq", "tecnifibre", "dunlop", "inni", "shark", "luxilon", "genesis",
                     "solinco", "kona", "nox", "heroe", "ama", "tourna", "joma", "penn", "quicksand", "prokennex",
                     "emit", "drop shot", "sexy", "quick"]
PROMO_RE = re.compile(r"frete gr[aá]tis|promo[cç]|\bpromo\b|oferta|desconto|liquida|imperd[ií]vel|black friday|"
                      r"queima|\d+ ?% ?off|compre j[aá]|melhor pre[cç]o|barat[oa]|cupom|\bpix\b", re.I)
INFANTIL_RE = re.compile(r"infantil|j[uú]nior|\bjr\b|\bkids?\b|juvenil|\bgs\b|\bbaby\b|crian[cç]a", re.I)


def gtin_valido(g):
    if not g.isdigit() or len(g) not in (8, 12, 13, 14):
        return False, "formato inválido (precisa ter 8, 12, 13 ou 14 dígitos numéricos)"
    if len(set(g)) == 1:
        return False, "todos os dígitos iguais"
    digits = [int(c) for c in g]
    body, check = digits[:-1], digits[-1]
    total = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(body)))
    calc = (10 - total % 10) % 10
    if calc != check:
        return False, f"dígito verificador errado (calculado {calc}, informado {check})"
    padded = g.zfill(14)
    if padded[1:4] in ("978", "979") and len(g) == 13:
        return True, "ISBN"
    if padded[1] == "2" or padded[1:3] in ("02", "04") and len(g) == 12:
        return False, "prefixo de uso interno/loja (faixa 2xx/02/04), não é GTIN de fabricante"
    return True, ""


def main():
    produtos = json.loads((DIR / "produtos.json").read_text())
    desempenho = {}
    if (DIR / "desempenho.csv").exists():
        for r in csv.DictReader(open(DIR / "desempenho.csv", encoding="utf-8")):
            desempenho[r["offer_id"]] = {k: float(r[k] or 0) for k in ("impressoes", "cliques", "conversoes", "receita")}
    referencia = {}
    if (DIR / "precos.csv").exists():
        for r in csv.DictReader(open(DIR / "precos.csv", encoding="utf-8")):
            referencia[r["offer_id"]] = r

    linhas = []

    def add(p, origem, categoria, gravidade, campo, valor, problema, como, onde, destinos=""):
        a = p["productAttributes"]
        linhas.append({
            "product_id": p["name"].split("/")[-1], "offer_id": p["offerId"], "titulo": a.get("title", ""),
            "origem": origem, "categoria": categoria, "gravidade": gravidade, "campo": campo,
            "valor_atual": (str(valor) if valor is not None else "")[:300], "problema": problema,
            "como_corrigir": como, "onde_corrigir": onde, "destinos": destinos,
            "shopify_product_id": shopify_id(p), "disponibilidade": a.get("availability", ""),
        })

    def shopify_id(p):
        for c in p.get("customAttributes", []):
            if c.get("name") == "shopify product id":
                return c["value"].split("/")[-1]
        m = re.match(r"shopify_\w+?_(\d+)_\d+", p["offerId"])
        return m.group(1) if m else ""

    # Índices para checagens entre produtos
    por_titulo, por_desc, por_img, por_gtin, por_shop, por_grupo = (defaultdict(list) for _ in range(6))
    for p in produtos:
        a = p["productAttributes"]
        sid = shopify_id(p)
        por_titulo[a.get("title", "").strip().lower()].append(p)
        d = texto(a.get("description", ""))
        if len(d) >= 50:
            por_desc[d].append(p)
        if a.get("imageLink"):
            por_img[a["imageLink"].split("?")[0]].append(p)
        for g in a.get("gtins", []):
            por_gtin[g].append(p)
        por_shop[sid].append(p)
        if a.get("itemGroupId"):
            por_grupo[a["itemGroupId"]].append(p)

    for p in produtos:
        a = p["productAttributes"]
        st = p.get("productStatus", {})
        sid = shopify_id(p)
        ptype = (a.get("productTypes") or [""])[0]
        title = a.get("title", "") or ""
        nt = norm(title)
        perf = desempenho.get(p["offerId"], {})

        # ------------------------------------------------------------ 1. Google
        por_codigo = defaultdict(list)
        for i in st.get("itemLevelIssues", []):
            por_codigo[(i.get("code"), i.get("attribute", ""))].append(i)
        for (code, attr), iss in por_codigo.items():
            sevs = {i.get("severity") for i in iss}
            reprov = sorted(i.get("reportingContext") for i in iss if i.get("severity") == "DISAPPROVED")
            rebaix = sorted(i.get("reportingContext") for i in iss if i.get("severity") == "DEMOTED")
            outros = sorted(i.get("reportingContext") for i in iss if i.get("severity") not in ("DISAPPROVED", "DEMOTED"))
            if reprov:
                grav = "crítico"
            elif rebaix or code == "image_too_small_for_high_resolution":
                grav = "alto"
            else:
                grav = "médio"
            partes = []
            if reprov:
                partes.append("REPROVADO em " + ", ".join(reprov))
            if rebaix:
                partes.append("REBAIXADO em " + ", ".join(rebaix))
            if outros:
                partes.append("alerta (sem impacto ainda) em " + ", ".join(outros))
            i0 = iss[0]
            campo = attr or i0.get("attribute", "") or "-"
            valor = a.get({"link": "link", "image link": "imageLink", "title": "title"}.get(campo, ""), "") if campo else ""
            como, onde = COMO_GOOGLE.get(code, (f"Seguir a orientação do Google: {i0.get('detail', '')} {i0.get('documentation', '')}".strip(),
                                                "Shopify"))
            add(p, "google", "google:" + code, grav, campo, valor,
                f"{i0.get('description', code)} — {i0.get('detail', '')} [{' | '.join(partes)}]",
                como, onde, ", ".join(sorted({i.get('reportingContext') for i in iss})))

        # ------------------------------------------------------------ 2. Título
        if not title.strip():
            add(p, "pente-fino", "titulo", "crítico", "title", title, "Título vazio", "Preencher o título do produto.", "Shopify")
        else:
            if len(title) < 30:
                add(p, "pente-fino", "titulo", "médio", "title", title, f"Título curto ({len(title)} caracteres; mínimo recomendado 30)",
                    "Incluir marca + tipo + modelo + atributo principal (gênero, cor, tamanho).", "Shopify")
            if len(title) > 150:
                add(p, "pente-fino", "titulo", "médio", "title", title, f"Título longo ({len(title)} caracteres; limite 150)",
                    "Encurtar mantendo o essencial no início.", "Shopify")
            letras = [c for c in title if c.isalpha()]
            if letras and title.upper() == title and "title_all_caps" not in {k[0] for k in por_codigo}:
                add(p, "pente-fino", "titulo", "médio", "title", title, "Título todo em MAIÚSCULAS",
                    "Reescrever com só a primeira letra das palavras em maiúscula.", "Shopify")
            brand = a.get("brand")
            if brand:
                bkey = norm(brand).split()[0].replace("´", "").replace("'", "")
                if bkey not in nt.replace("´", "").replace("'", ""):
                    add(p, "pente-fino", "titulo", "médio", "title", title, f"Marca '{brand}' não aparece no título",
                        "Incluir a marca no título (de preferência no início).", "Shopify")
                outras = [m for m in MARCAS_CONHECIDAS if re.search(rf"\b{re.escape(m)}\b", nt) and m.split()[0] not in norm(brand)]
                if outras and bkey not in nt:
                    add(p, "pente-fino", "identificadores", "alto", "brand", brand,
                        f"Marca do feed ('{brand}') diferente da marca citada no título ({', '.join(outras)})",
                        "Corrigir o campo Fornecedor/Marca (vendor) do produto.", "Shopify")
            palavras = PALAVRAS_TIPO.get(ptype)
            if palavras and not any(w in nt for w in palavras):
                add(p, "pente-fino", "titulo", "médio", "title", title, f"Tipo de produto ('{ptype}') não aparece no título",
                    f"Incluir o tipo (ex.: '{palavras[0].capitalize()}') no título.", "Shopify")
            faltam = []
            for o in a.get("variantOptions", []):
                v = norm(o.get("value", "")).strip()
                if not v or v in ("default title",):
                    continue
                v_cmp = re.sub(r"[\s/]+", "", v)
                if v not in nt and v_cmp not in re.sub(r"[\s/]+", "", nt):
                    faltam.append(f"{o.get('name')}={o.get('value')}")
            if faltam:
                add(p, "pente-fino", "titulo", "médio", "title", title, "Variante não aparece no título: " + "; ".join(faltam),
                    "O título de cada variante deve citar a opção (cor/tamanho/peso). Revisar o nome da variante "
                    "ou a regra de título do Simprosys (append variant title).", "Simprosys")
            dups = [q for q in por_titulo[title.strip().lower()] if q is not p]
            if dups:
                mesmo = all(shopify_id(q) == sid for q in dups)
                add(p, "pente-fino", "titulo", "médio", "title", title,
                    f"Título idêntico a {len(dups)} outro(s) produto(s)"
                    + (" do mesmo produto Shopify (variantes sem diferenciação)" if mesmo else
                       " de produtos Shopify diferentes: " + ", ".join(sorted({shopify_id(q) for q in dups}))),
                    "Diferenciar cada variante/produto no título (tamanho, cor, quantidade).", "Shopify")
            m = PROMO_RE.search(title)
            if m:
                add(p, "pente-fino", "titulo", "alto", "title", title, f"Texto promocional no título ('{m.group(0)}')",
                    "Remover termos promocionais do título (política do Google); usar Promoções do Merchant Center.", "Shopify")
            if re.search(r"\s{2,}|\s,|\(\s|\s\)|-\S*$|\bC/\d", title) and re.search(r"\s{2,}|\s,|\(\s|\s\)", title):
                add(p, "pente-fino", "titulo", "baixo", "title", title, "Espaçamento/pontuação irregular no título (espaço duplo ou antes de vírgula/parêntese)",
                    "Limpar espaços extras.", "Shopify")
            if re.match(r"tenis\b", title, re.I) and not title.lower().startswith("tênis") and ptype in SAPATOS:
                add(p, "pente-fino", "titulo", "baixo", "title", title, "Grafia 'Tenis' sem acento",
                    "Escrever 'Tênis' (é como o cliente busca).", "Shopify")

        # ------------------------------------------------------------ 3. Descrição
        desc = a.get("description", "") or ""
        dtxt = texto(desc)
        if not dtxt:
            add(p, "pente-fino", "descricao", "crítico", "description", "", "Descrição vazia",
                "Escrever descrição (características, material, uso, tecnologias).", "Shopify")
        else:
            if len(dtxt) < 150:
                add(p, "pente-fino", "descricao", "médio", "description", dtxt, f"Descrição curta ({len(dtxt)} caracteres de texto; mínimo recomendado 150)",
                    "Completar com material, tecnologia, indicação de uso, medidas.", "Shopify")
            if norm(dtxt).strip(" .") == norm(title).strip(" ."):
                add(p, "pente-fino", "descricao", "médio", "description", dtxt, "Descrição igual ao título",
                    "Escrever uma descrição de verdade.", "Shopify")
            if len(desc) > 5000:
                add(p, "pente-fino", "descricao", "médio", "description", f"{len(desc)} caracteres",
                    "Descrição acima de 5.000 caracteres (limite do Google; o excedente é cortado)",
                    "Enxugar a descrição na Shopify.", "Shopify")
            ents = sorted(set(re.findall(r"&(?:[a-zA-Z]+|#\d+);", desc)))
            if ents:
                add(p, "pente-fino", "descricao", "médio", "description", " ".join(ents), "Entidades HTML na descrição",
                    "Trocar as entidades por caracteres normais no editor da Shopify.", "Shopify")
            desequil = []
            for tag in ("p", "div", "ul", "ol", "li", "strong", "span", "em", "b", "i", "table", "a"):
                ab = len(re.findall(rf"<{tag}(\s[^>]*)?>", desc, re.I))
                fe = len(re.findall(rf"</{tag}\s*>", desc, re.I))
                if ab != fe:
                    desequil.append(f"<{tag}> {ab} abertas / {fe} fechadas")
            if desequil or re.search(r"<[^>]*$", desc):
                add(p, "pente-fino", "descricao", "médio", "description", "; ".join(desequil) or "tag cortada no fim",
                    "HTML quebrado na descrição (tags sem fechamento)",
                    "Abrir a descrição no modo HTML da Shopify e corrigir as tags.", "Shopify")
            if re.search(r"(?i)https?://|www\.", dtxt):
                add(p, "pente-fino", "descricao", "baixo", "description", re.search(r"(?i)\S*(https?://|www\.)\S*", dtxt).group(0),
                    "Link/URL dentro da descrição", "Remover links externos da descrição.", "Shopify")
            if PROMO_RE.search(dtxt[:400]):
                add(p, "pente-fino", "descricao", "baixo", "description", PROMO_RE.search(dtxt[:400]).group(0),
                    "Texto promocional no início da descrição", "Remover frases de promoção/frete da descrição.", "Shopify")
            if len(dtxt) >= 50:
                outros = {shopify_id(q) for q in por_desc[dtxt]} - {sid}
                if outros:
                    add(p, "pente-fino", "descricao", "médio", "description", dtxt[:120] + "…",
                        f"Descrição idêntica à de {len(outros)} outro(s) produto(s) Shopify: {', '.join(sorted(outros)[:5])}",
                        "Personalizar a descrição de cada produto (modelo, cor, tecnologia).", "Shopify")

        # ------------------------------------------------------------ 4. Preço
        price, cur = money(a.get("price")), (a.get("price") or {}).get("currencyCode")
        sale = money(a.get("salePrice"))
        if not price:
            add(p, "pente-fino", "preco", "crítico", "price", price, "Preço zero ou ausente", "Cadastrar o preço da variante.", "Shopify")
        if cur and cur != "BRL":
            add(p, "pente-fino", "preco", "crítico", "price.currencyCode", cur, "Moeda diferente de BRL", "Enviar preço em BRL.", "Simprosys")
        if sale is not None and price:
            if sale >= price:
                add(p, "pente-fino", "preco", "alto", "salePrice", f"{sale:.2f} (cheio {price:.2f})",
                    "Preço promocional maior ou igual ao preço cheio",
                    "Corrigir 'Comparar com' (compare-at) / preço da variante.", "Shopify")
            else:
                desc_pct = (1 - sale / price) * 100
                if desc_pct > 70:
                    add(p, "pente-fino", "preco", "alto", "salePrice", f"{sale:.2f} de {price:.2f} ({desc_pct:.0f}% off)",
                        "Desconto acima de 70% (suspeito de erro de cadastro)",
                        "Conferir preço e 'Comparar com' da variante.", "Shopify")
            ped = a.get("salePriceEffectiveDate")
            if not ped or not ped.get("endTime"):
                add(p, "pente-fino", "preco", "baixo", "salePriceEffectiveDate", json.dumps(ped) if ped else "",
                    "Preço promocional sem data de fim (os demais promocionais têm janela de 30 dias)",
                    "Verificar por que este item não recebe a janela automática do Simprosys; definir fim da promoção.", "Simprosys")
            else:
                fim = datetime.fromisoformat(ped["endTime"].replace("Z", "+00:00"))
                if fim < HOJE:
                    add(p, "pente-fino", "preco", "alto", "salePriceEffectiveDate", ped["endTime"],
                        "Promoção com data de fim vencida (o Google volta a mostrar o preço cheio)",
                        "Atualizar/remover o preço promocional.", "Shopify")
        elif a.get("salePriceEffectiveDate") and sale is None:
            add(p, "pente-fino", "preco", "baixo", "salePriceEffectiveDate", json.dumps(a["salePriceEffectiveDate"]),
                "Data de promoção sem preço promocional", "Remover a data.", "Simprosys")
        ref = referencia.get(p["offerId"])
        if ref and float(ref["diferenca_%"]) >= 60:
            add(p, "pente-fino", "preco", "baixo", "price", f"R$ {float(ref['seu_preco']):.2f} vs referência R$ {float(ref['preco_referencia']):.2f}",
                f"Preço {float(ref['diferenca_%']):+.0f}% acima do preço de referência do Google",
                "Conferir se preço/quantidade estão corretos (kit x unidade) e se o produto é comparável; senão, rever preço.", "Shopify")

        # ------------------------------------------------------------ 5. Identificadores
        gtins = a.get("gtins", [])
        ie = a.get("identifierExists")
        brand = a.get("brand")
        for g in gtins:
            ok, motivo = gtin_valido(g)
            if not ok:
                add(p, "pente-fino", "identificadores", "alto", "gtin", g, f"GTIN inválido: {motivo}",
                    "Corrigir o código de barras (GTIN/EAN) da variante.", "Shopify")
            outros = [q for q in por_gtin[g] if q is not p]
            if outros:
                mesmo = all(shopify_id(q) == sid for q in outros)
                add(p, "pente-fino", "identificadores", "alto", "gtin", g,
                    f"GTIN repetido em {len(outros)} outra(s) oferta(s)"
                    + (" (variantes do mesmo produto)" if mesmo else " de outros produtos: " + ", ".join(q["offerId"] for q in outros[:3])),
                    "Cada variante precisa do seu próprio EAN; corrigir o código de barras.", "Shopify")
        if not brand:
            sug = [m for m in MARCAS_CONHECIDAS if re.search(rf"\b{re.escape(m)}\b", nt)]
            add(p, "pente-fino", "identificadores", "alto", "brand", "",
                "Sem marca" + (f" (o título cita '{sug[0]}')" if sug else ""),
                "Preencher o Fornecedor (vendor) na Shopify e conferir se o Simprosys envia a marca mesmo com identifierExists=false.",
                "Shopify")
        if ie is False:
            sug = [m for m in MARCAS_CONHECIDAS if re.search(rf"\b{re.escape(m)}\b", nt)]
            if sug:
                add(p, "pente-fino", "identificadores", "alto", "identifierExists", "false",
                    f"identifierExists=false em produto de marca de fabricante ({sug[0]}), que normalmente tem EAN",
                    "Cadastrar o código de barras (EAN) e a marca na variante; tirar o produto da regra "
                    "'identifier exists = no' do Simprosys.", "Shopify")
            else:
                add(p, "pente-fino", "identificadores", "médio", "identifierExists", "false",
                    "identifierExists=false (sem GTIN, marca e MPN)",
                    "Confirmar que o produto realmente não tem EAN; se tiver, cadastrar.", "Shopify")
        elif not gtins:
            if not a.get("mpn"):
                add(p, "pente-fino", "identificadores", "alto", "gtin/mpn", "",
                    "Sem GTIN e sem MPN (e identifierExists não informado)",
                    "Cadastrar o EAN (código de barras) ou o SKU do fabricante como MPN.", "Shopify")
            else:
                add(p, "pente-fino", "identificadores", "médio", "gtin", f"mpn={a.get('mpn')}",
                    "Sem GTIN (só MPN) em produto de marca", "Cadastrar o EAN da variante, se existir.", "Shopify")
        if ie is False and gtins:
            add(p, "pente-fino", "identificadores", "alto", "identifierExists", "false",
                "identifierExists=false mas o produto tem GTIN", "Remover a marcação 'sem identificador'.", "Simprosys")
        if brand and (brand.isupper() and len(brand) > 3 or any(c in brand for c in "´`") or norm(brand) == "shark beach tenis"):
            add(p, "pente-fino", "identificadores", "baixo", "brand", brand,
                "Marca fora do padrão de escrita (maiúsculas, acento agudo no lugar de apóstrofo ou nome com o esporte)",
                "Padronizar o Fornecedor (ex.: 'Head', 'Heroe's', 'Shark').", "Shopify")

        # ------------------------------------------------------------ 6. Imagens
        img = a.get("imageLink", "")
        if not img:
            add(p, "pente-fino", "imagens", "crítico", "imageLink", "", "Sem imagem principal", "Adicionar imagem ao produto/variante.", "Shopify")
        else:
            if not img.startswith("https://"):
                add(p, "pente-fino", "imagens", "alto", "imageLink", img, "Imagem principal sem https", "Usar URL https.", "Shopify")
            outros_img = {shopify_id(q) for q in por_img[img.split("?")[0]]} - {sid}
            if outros_img:
                add(p, "pente-fino", "imagens", "médio", "imageLink", img,
                    f"Mesma imagem principal usada em {len(outros_img)} outro(s) produto(s) Shopify: {', '.join(sorted(outros_img)[:5])}",
                    "Usar foto própria de cada produto.", "Shopify")
            if re.search(r"placeholder|no[-_]?image|sem[-_]?imagem", img, re.I):
                add(p, "pente-fino", "imagens", "crítico", "imageLink", img, "Imagem genérica (placeholder)", "Subir foto real.", "Shopify")
        if not a.get("additionalImageLinks"):
            add(p, "pente-fino", "imagens", "médio", "additionalImageLinks", "", "Sem imagens adicionais",
                "Adicionar mais fotos (ângulos, detalhe, em uso) e associá-las à variante/produto.", "Shopify")
        else:
            nao_https = [u for u in a["additionalImageLinks"] if not u.startswith("https://")]
            if nao_https:
                add(p, "pente-fino", "imagens", "médio", "additionalImageLinks", nao_https[0], "Imagem adicional sem https", "Usar https.", "Shopify")

        # ------------------------------------------------------------ 7. Links
        link = a.get("link", "")
        if not link:
            add(p, "pente-fino", "links", "crítico", "link", "", "Sem link do produto", "Publicar o produto na Loja virtual.", "Shopify")
        else:
            u = urlparse(link)
            if u.scheme != "https":
                add(p, "pente-fino", "links", "alto", "link", link, "Link sem https", "Usar https.", "Shopify")
            if u.netloc.removeprefix("www.") != DOMINIO:
                add(p, "pente-fino", "links", "alto", "link", link, f"Domínio diferente de {DOMINIO}",
                    "Conferir domínio principal na Shopify e no Simprosys.", "Simprosys")
            if not u.path.startswith("/products/"):
                add(p, "pente-fino", "links", "alto", "link", link, "Link não aponta para página de produto (coleção/home)",
                    "Usar o link do produto.", "Simprosys")
            if a.get("variantOptions") and "variant" not in parse_qs(u.query):
                add(p, "pente-fino", "links", "médio", "link", link, "Produto com variantes sem ?variant= no link (cai na variante padrão)",
                    "Ativar o link por variante no Simprosys.", "Simprosys")
        can = a.get("canonicalLink")
        if can and link and urlparse(can).path != urlparse(link).path:
            add(p, "pente-fino", "links", "médio", "canonicalLink", can, "canonicalLink com caminho diferente do link",
                "Conferir o handle do produto.", "Shopify")

        # ------------------------------------------------------------ 8. Disponibilidade e desempenho
        av = a.get("availability")
        aprovado_algum = any(d.get("approvedCountries") for d in st.get("destinationStatuses", []))
        if av == "OUT_OF_STOCK" and aprovado_algum:
            clk = perf.get("cliques", 0)
            add(p, "pente-fino", "disponibilidade", "médio" if clk > 0 else "baixo", "availability", av,
                "Fora de estoque e ainda ativo no feed" + (f" — teve {clk:.0f} clique(s) nos últimos 30 dias (demanda perdida)" if clk else ""),
                "Repor estoque ou, se descontinuado, arquivar/ocultar o produto do canal Google na Shopify.", "Shopify")
        if av in ("PREORDER", "BACKORDER") and not a.get("availabilityDate"):
            add(p, "pente-fino", "disponibilidade", "alto", "availabilityDate", "", "Pré-venda/encomenda sem data de disponibilidade",
                "Informar availability_date.", "Simprosys")
        if av == "IN_STOCK" and desempenho and perf.get("impressoes", 0) == 0 and aprovado_algum:
            add(p, "pente-fino", "desempenho", "médio", "-", "0 impressões em 30 dias",
                "Em estoque e aprovado, mas sem nenhuma impressão nos últimos 30 dias",
                "Revisar título/categoria/preço e se o produto está incluído nas campanhas.", "Merchant Center")

        # ------------------------------------------------------------ 9. Categoria e atributos
        gpc = a.get("googleProductCategory")
        if not gpc:
            add(p, "pente-fino", "categoria", "alto", "googleProductCategory", "", "Sem categoria do Google",
                f"Definir a categoria do produto na Shopify (sugestão: {ESPERADA.get(ptype, ('', 'categoria específica'))[1]}).", "Shopify")
        else:
            if gpc.isdigit():
                add(p, "pente-fino", "categoria", "baixo", "googleProductCategory", gpc,
                    "Categoria enviada como ID numérico (formato aceito, mas difere do resto do catálogo; conferir se o ID corresponde ao tipo)",
                    f"Conferir o ID na taxonomia do Google; sugestão: {ESPERADA.get(ptype, ('', 'categoria específica'))[1]}.", "Shopify")
            elif not gpc.startswith(("Vestuário", "Artigos", "Artes", "Saúde", "Câmeras", "Brinquedos", "Malas", "Casa")):
                add(p, "pente-fino", "categoria", "médio", "googleProductCategory", gpc,
                    "Categoria do Google em outro idioma (inglês/polonês) num feed em português",
                    f"Trocar pela categoria em pt-BR: {ESPERADA.get(ptype, ('', 'categoria equivalente'))[1]}.", "Shopify")
            if ptype in ESPERADA and not gpc.isdigit():
                aceitos, sugestao = ESPERADA[ptype]
                if not gpc.startswith(tuple(aceitos)):
                    generica = gpc in (VEST, f"{VEST} > Acessórios para roupas") or (gpc == ESP_TENIS and ptype not in SAPATOS)
                    if ptype in SAPATOS and re.search(r"(?i)> ?(t[eê]nis|tennis|tenis)$|plataforma e padel$", gpc):
                        motivo = f"Calçado classificado como o esporte tênis (não como sapato) — tipo '{ptype}'"
                    else:
                        motivo = ("Categoria genérica demais para o tipo" if generica
                                  else "Categoria do Google incompatível com o tipo") + f" '{ptype}'"
                    add(p, "pente-fino", "categoria", "alto", "googleProductCategory", gpc, motivo,
                        f"Usar: {sugestao}. Ajustar a 'Categoria do produto' na Shopify (ou o mapeamento de categoria do Simprosys) "
                        "para o tipo inteiro.", "Shopify")
        if not a.get("productTypes"):
            add(p, "pente-fino", "categoria", "médio", "productTypes", "", "Sem tipo de produto", "Preencher 'Tipo' na Shopify.", "Shopify")
        if not a.get("condition"):
            add(p, "pente-fino", "categoria", "médio", "condition", "", "Condição ausente", "Enviar condition=new.", "Simprosys")

        e_roupa, e_sapato, e_acess = ptype in ROUPAS, ptype in SAPATOS, ptype in ACESS_VEST
        if e_roupa or e_sapato or e_acess:
            if not a.get("color"):
                add(p, "pente-fino", "atributos", "alto", "color", "", "Vestuário/calçado sem cor (obrigatório no Brasil)",
                    "Criar a opção 'Cor' na variante ou o metacampo de cor da categoria; mapear no Simprosys.", "Shopify")
            if (e_roupa or e_sapato) and not a.get("size"):
                add(p, "pente-fino", "atributos", "alto", "size", "", "Vestuário/calçado sem tamanho (obrigatório no Brasil)",
                    "Cadastrar a opção 'Tamanho' (mesmo que 'Único').", "Shopify")
        if (e_roupa or e_sapato or e_acess) and not a.get("gender"):
            add(p, "pente-fino", "atributos", "alto", "gender", "", "Sem gênero", "Mapear gênero no Simprosys.", "Simprosys")
        g = a.get("gender")
        tem_m, tem_f = bool(re.search(r"mascul", nt)), bool(re.search(r"femin", nt))
        if g and (tem_m != tem_f):
            esperado = "MALE" if tem_m else "FEMALE"
            if g != esperado:
                add(p, "pente-fino", "atributos", "alto" if (e_roupa or e_sapato or e_acess) else "médio", "gender", g,
                    f"Gênero '{g}' contradiz o título ('{'Masculino' if tem_m else 'Feminino'}')",
                    f"Definir gender={esperado}: no Simprosys, mapear o gênero a partir de tag/metacampo da Shopify "
                    "em vez do padrão 'unisex'.", "Simprosys")
        if INFANTIL_RE.search(title) and a.get("ageGroup") == "ADULT":
            add(p, "pente-fino", "atributos", "alto" if (e_roupa or e_sapato or e_acess) else "médio", "ageGroup", "ADULT",
                f"Faixa etária 'adulto' em produto infantil/juvenil ('{INFANTIL_RE.search(title).group(0)}' no título)",
                "Definir age_group=kids (ou toddler/infant conforme o caso) via tag/metacampo + mapeamento do Simprosys.", "Simprosys")
        if (e_roupa or e_sapato or e_acess) and not a.get("ageGroup"):
            add(p, "pente-fino", "atributos", "alto", "ageGroup", "", "Sem faixa etária", "Mapear age_group no Simprosys.", "Simprosys")
        cor = a.get("color")
        if cor and (e_roupa or e_sapato or e_acess):
            m = re.search(r" - ([^,]+?)(?:,|$)", title)
            if m and "/" in m.group(1) and "/" not in cor and norm(cor) in norm(m.group(1)):
                add(p, "pente-fino", "atributos", "baixo", "color", cor,
                    f"Cor do feed ('{cor}') incompleta em relação ao título ('{m.group(1).strip()}')",
                    "Enviar todas as cores separadas por '/' (até 3).", "Shopify")

        # ------------------------------------------------------------ 10. Frete e peso
        sw = a.get("shippingWeight") or {}
        if "value" not in sw:
            add(p, "pente-fino", "frete-peso", "baixo", "shippingWeight", json.dumps(sw),
                "Peso de envio vazio (só a unidade é enviada). Hoje o frete da conta é tabela fixa e não depende do peso",
                "Cadastrar o peso na variante da Shopify; o Simprosys passa a enviar o valor.", "Shopify")

        # ------------------------------------------------------------ 11. Variantes
        irmaos = por_shop.get(sid, [])
        if not a.get("itemGroupId") and (len(irmaos) > 1 or a.get("variantOptions")):
            add(p, "pente-fino", "variantes", "alto", "itemGroupId", "",
                f"Variante sem itemGroupId (o produto Shopify {sid} tem {len(irmaos)} oferta(s) no feed)",
                "Ativar o envio de item_group_id no Simprosys.", "Simprosys")
        grp = a.get("itemGroupId")
        if grp:
            membros = por_grupo[grp]
            if grp != sid and sid:
                add(p, "pente-fino", "variantes", "médio", "itemGroupId", grp, f"itemGroupId diferente do ID do produto Shopify ({sid})",
                    "Conferir agrupamento.", "Simprosys")
            igt = a.get("itemGroupTitle")
            if igt and not norm(title).startswith(norm(igt).strip()[: max(10, len(igt) - 5)]):
                add(p, "pente-fino", "variantes", "médio", "title", title, f"Título da variante não segue o título do grupo ('{igt}')",
                    "Padronizar: título do produto + opção da variante.", "Shopify")
            if len(membros) > 1:
                precos = [money(q["productAttributes"].get("price")) or 0 for q in membros]
                med = sorted(precos)[len(precos) // 2]
                so_tamanho = all({o["name"] for o in q["productAttributes"].get("variantOptions", [])} <= {"tamanho"} for q in membros)
                if med and price and so_tamanho and abs(price - med) / med > 0.15:
                    add(p, "pente-fino", "variantes", "médio", "price", f"{price:.2f} (mediana do grupo {med:.2f})",
                        "Preço desta variante destoa das demais variantes de tamanho do mesmo produto (>15%)",
                        "Conferir o preço da variante.", "Shopify")
                for campo in ("brand", "gender", "googleProductCategory", "ageGroup"):
                    valores = {q["productAttributes"].get(campo) for q in membros}
                    if len(valores) > 1:
                        cont = Counter(q["productAttributes"].get(campo) for q in membros)
                        if cont[a.get(campo)] < max(cont.values()):
                            add(p, "pente-fino", "variantes", "médio", campo, a.get(campo),
                                f"'{campo}' diferente das outras variantes do grupo ({dict(cont)})",
                                "Uniformizar o atributo nas variantes.", "Shopify")
                cores = Counter(q["productAttributes"].get("color") for q in membros)
                if len(cores) > 1:
                    mesma_img_outra_cor = [q for q in membros if q["productAttributes"].get("imageLink") == img
                                           and q["productAttributes"].get("color") != a.get("color")]
                    if mesma_img_outra_cor:
                        add(p, "pente-fino", "imagens", "médio", "imageLink", img,
                            "Variantes de cores diferentes usando a mesma imagem principal",
                            "Associar a foto da cor certa a cada variante na Shopify.", "Shopify")

        # ------------------------------------------------------------ 12. Custom labels
        for n in range(5):
            v = a.get(f"customLabel{n}")
            if v is None:
                continue
            ok = v in LABELS_PADRAO or (n not in (0, 1, 2))
            if not ok or v != v.strip() or v.lower() != v or v in ("teste", "test"):
                add(p, "pente-fino", "custom-labels", "médio", f"customLabel{n}", v, "Rótulo personalizado fora do padrão",
                    "Usar só os valores do padrão (mais-vendidos, normal, sem-exposicao, margem-*, liquidacao, em-promocao, preco-cheio).",
                    "Merchant Center")

    # Resumo por produto -----------------------------------------------------------------------
    por_prod = defaultdict(list)
    for l in linhas:
        por_prod[l["product_id"]].append(l)
    resumo = []
    for p in produtos:
        a, st = p["productAttributes"], p.get("productStatus", {})
        pid = p["name"].split("/")[-1]
        ls = por_prod.get(pid, [])
        c = Counter(l["gravidade"] for l in ls)
        perf = desempenho.get(p["offerId"], {})
        reprov = sorted(d["reportingContext"] for d in st.get("destinationStatuses", []) if d.get("disapprovedCountries"))
        pend = sorted(d["reportingContext"] for d in st.get("destinationStatuses", []) if d.get("pendingCountries"))
        rebaix = sorted({i.get("reportingContext") for i in st.get("itemLevelIssues", []) if i.get("severity") == "DEMOTED"})
        if c["crítico"]:
            status = "CRÍTICO"
        elif c["alto"]:
            status = "ALTO"
        elif c["médio"]:
            status = "MÉDIO"
        elif c["baixo"]:
            status = "BAIXO"
        else:
            status = "OK"
        pontos = sum(GRAV_PESO[l["gravidade"]] for l in ls)
        impacto = 1 + math.log1p(perf.get("cliques", 0)) + 0.5 * math.log1p(perf.get("impressoes", 0) / 100) + 5 * perf.get("conversoes", 0)
        fator_estoque = 1 if a.get("availability") == "IN_STOCK" else 0.5
        urg = round(pontos * impacto * fator_estoque, 1)
        resumo.append({
            "product_id": pid, "offer_id": p["offerId"], "shopify_product_id": shopify_id(p), "titulo": a.get("title", ""),
            "tipo": (a.get("productTypes") or [""])[0], "marca": a.get("brand", ""), "disponibilidade": a.get("availability", ""),
            "preco": money(a.get("price")), "preco_promocional": money(a.get("salePrice")),
            "critico": c["crítico"], "alto": c["alto"], "medio": c["médio"], "baixo": c["baixo"], "total_problemas": len(ls),
            "status_geral": status, "reprovado_em": ", ".join(reprov), "rebaixado_em": ", ".join(rebaix),
            "pendente_em": ", ".join(pend),
            "impressoes_30d": int(perf.get("impressoes", 0)), "cliques_30d": int(perf.get("cliques", 0)),
            "conversoes_30d": perf.get("conversoes", 0), "receita_30d": perf.get("receita", 0),
            "pontos_gravidade": pontos, "urgencia": urg,
        })

    linhas.sort(key=lambda l: (GRAV_ORDEM[l["gravidade"]], l["categoria"], l["titulo"]))
    resumo.sort(key=lambda r: -r["urgencia"])
    for nome, rows in (("irregularidades.csv", linhas), ("resumo-por-produto.csv", resumo)):
        with open(DIR / nome, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print(f"{len(linhas)} irregularidades em {sum(1 for r in resumo if r['total_problemas'])} produtos")


COMO_GOOGLE = {
    "landing_page_error": ("Consulta somente leitura à Shopify em 22/10/2026: os 11 produtos com este erro estão ACTIVE, "
                           "publicados, com estoque e com o mesmo handle do link — a página existe. Provável falha de "
                           "rastreamento do Googlebot (bloqueio por app de proteção/antibot, lentidão, redirecionamento por "
                           "país/moeda). Testar a URL na Inspeção de URL do Search Console (teste ao vivo) e, estando OK, "
                           "pedir nova análise do produto no Merchant Center.", "Merchant Center"),
    "image_too_small": ("Substituir a imagem principal por uma maior (mín. 250x250 px para vestuário, 100x100 px nos "
                        "demais; recomendado ≥ 800x800 px).", "Shopify"),
    "image_too_small_for_high_resolution": ("Imagem abaixo do novo mínimo que o Google vai passar a exigir: subir foto "
                                            "em alta resolução (recomendado ≥ 1500x1500 px) antes que vire reprovação.", "Shopify"),
    "title_all_caps": ("Reescrever o título sem caixa alta (ex.: 'Raquete de Tênis Head Speed MP').", "Shopify"),
    "sexual_interests_policy_violation": ("Política de anúncios personalizados (interesses sexuais) — a foto de sunga em "
                                          "modelo é tratada como conteúdo sensível. Usar imagem principal só do produto "
                                          "(sem modelo) e pedir revisão; caso contrário, aceitar a restrição nesses destinos.",
                                          "Shopify"),
    "restricted_nfs_policy_violation": ("Conteúdo adulto restrito — mesma causa (foto de roupa de banho em modelo). "
                                        "Trocar a imagem principal e solicitar revisão no Merchant Center.", "Shopify"),
    "image_under_review": ("Imagem em análise pelo Google: aguardar; se continuar reprovada, trocar a imagem.", "Merchant Center"),
}

if __name__ == "__main__":
    main()
