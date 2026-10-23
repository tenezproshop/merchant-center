# Auditoria do catálogo – Google Merchant Center (Tenez) · 3ª rodada

**Data:** 23/10/2026, 11h30 (horário de Brasília) · **Modo:** somente leitura (nada foi alterado no Google, na Shopify ou em `dados/`)
**Comparada com:** 2ª rodada, de hoje cedo (versão anterior deste arquivo no histórico da branch) e 1ª rodada (branch `auditoria-catalogo-2026-10-22`)

> ⚠️ **O sync de categorias ainda não terminou.** Às 11h07 o app atualizou 787 produtos, mas **541 ainda não foram reprocessados**: nenhuma atualização no Google desde 11h08. **432 dos 434 problemas de categoria que restam estão nesses 541 produtos.** Quando o sync terminar, a maior parte deles deve sumir.

---

## 0. Resumo do que mudou hoje

| | 22/10 | 23/10 cedo | **23/10 11h30** |
|---|---:|---:|---:|
| Produtos no catálogo | 1.344 | 1.336 | **1.328** |
| Problemas (total) | 5.169 | 5.136 | **3.775** |
| Crítico | 21 | 22 | **20** |
| Alto | 2.611 | 2.594 | **1.295** |
| Médio | 914 | 903 | 852 |
| Baixo | 1.623 | 1.617 | 1.608 |
| Produtos com status ALTO | 1.147 | 1.140 | **778** |
| Produtos sem nenhum problema | 7 | 7 | **32** |
| Reprovados (algum destino) | 16 | 17 | **15** |
| Reprovados em Shopping / anúncios grátis | 12 | 13 | **11** |

**O que foi resolvido desde hoje cedo** (todos pelos syncs do app de feed, a partir dos campos da Shopify):

| Problema | Cedo | Agora |
|---|---:|---:|
| **Gênero `unissex` contradizendo o título** | 725 | **1** |
| **Faixa etária "adulto" em produto infantil** | 50 | **4** |
| **Categoria em inglês ou polonês** | 40 | **0** |
| **Categoria genérica demais** | 632 | 279 *(278 nos produtos ainda não reprocessados)* |
| **Tênis (calçado) classificado como o esporte "Tênis"** | 205 | 92 *(todos ainda não reprocessados)* |
| **Categoria incompatível com o tipo** | 99 | 37 *(36 ainda não reprocessados)* |
| **Produtos em rascunho na Shopify que continuavam no Google** | 7 | **0** |
| **Reprovados por "página indisponível"** | 12 | **10** |

Gênero no Google agora: 493 masculino, 429 feminino e 406 unissex (antes: 1.330 unissex). Faixa etária: 46 infantil (antes: 10).

**Outras mudanças:**
- **Saíram do Google** os 7 produtos em rascunho (Raquete AMA Poison Bee, Polo Adidas Climacool Bordô, Toalha INNI Roxo) e o **Vestido Nike Tênis Dri-Fit – Estampado**. O vestido virou rascunho na Shopify e tinha 100 cliques em 30 dias; confirme se foi intencional.
- **Deixaram de estar reprovados:**
  - **Raquete Wilson Blade Júnior 26 V10** (89 cliques/mês)
  - **AMA Poison Bee**, que saiu do feed
- **Correção na regra da auditoria:** as munhequeiras em "Acessórios para roupas > Pulseiras (de relógio)" agora contam como categoria certa. É assim que o Google em português chama a categoria *Wristbands* (ID 1893), e esse é o código que está na Shopify.

**Aumentaram um pouco:**
- **Aviso de imagem pequena:** 79 → 80.
- **Variantes de cores diferentes com a mesma foto:** 23 → 33. Esse número depende das cores informadas no feed; os casos estão listados em `irregularidades.csv`.

---

## 1. Totais

- **Produtos baixados:** 1.328, conferidos com `mc.py health` (1.328) e com o `product_view` do relatório (1.328).
- **Estoque:** 823 em estoque e 505 fora de estoque.
- **Desempenho (23/09 a 22/10):** 1.321.790 impressões e 11.961 cliques, mas só **0,15 conversão**, ou seja, nenhuma venda registrada. Ligue o acompanhamento de conversões.
- **Preço de referência:** 645 produtos.
- **Problemas da conta:** nenhum. **Custom labels:** nenhum produto tem.
- **Promoção do Google 84205 "10% off on all products":** continua **REPROVADA**, porque o desconto não é aplicado no checkout.

| Gravidade | Ocorrências |
|---|---:|
| Crítico | 20 |
| Alto | 1.295 |
| Médio | 852 |
| Baixo | 1.608 |
| **Total** | **3.775** |

**Status geral por produto:** CRÍTICO 16 · ALTO 778 · MÉDIO 227 · BAIXO 275 · OK 32.
**Onde corrigir:** Shopify 3.710 · Merchant Center 33 · Simprosys 32. Os problemas de gênero, faixa etária e categoria que eram do mapeamento do app foram resolvidos.

---

## 2. O que o Google aponta

São 99 produtos com algum problema: 288 ocorrências por destino, sendo 96 DISAPPROVED e 192 NOT_IMPACTED.

### 2.1 Reprovados: 15 produtos (11 também em Shopping e anúncios grátis)

| Código | Produtos | Situação |
|---|---:|---|
| `landing_page_error` – página indisponível | **10** | Todos estão **ACTIVE, publicados e com estoque** na Shopify (conferido às 11h30). A página existe: faça o teste ao vivo na Inspeção de URL do Search Console e peça nova análise no Merchant Center. |
| Política de conteúdo adulto | 4 (Sunga Nike Outline Swoosh, sem estoque) | Só em Display, Demand Gen e Vídeo. Trocar a foto por uma sem modelo, ou aceitar a restrição. |
| `image_too_small` | 1 (Top Nike Pro Dri-Fit Swoosh Feminino – Preto) | Trocar a imagem principal. |

Os 10 com página indisponível:
- Wilson Ultra 100 V5 RG (110 cliques/mês)
- Asics Gel Resolution X Rosa 40 (53)
- Óculos Mormaii Smash (52)
- Wilson Heritage 12PK
- Top Nike Pro Swoosh Vermelho
- Bola Wilson RG 3 tubos
- Shorts Nike Pro 3" Vermelho
- Shorts Adidas Essential
- Raqueteira Yonex Gearlogic Bege
- Regata Nike Court Vermelha

### 2.2 Avisos e pendentes
- **80 produtos com "imagem pequena para a próxima exigência"**, que vai virar reprovação.
- **4 títulos em maiúsculas** (Head Speed MP).
- **1 pendente** em Demand Gen (Yonex Percept 100, imagem em análise).

---

## 3. Os 10 problemas mais frequentes (agora)

| # | Problema | Produtos | Gravidade | Onde corrigir |
|---|---|---:|---|---|
| 1 | Peso de envio vazio | 1.024 | baixo* | Shopify |
| 2 | Fora de estoque e ainda no feed | 505 | baixo / médio | Shopify |
| 3 | Sem imagens adicionais | 498 | médio | Shopify |
| 4 | **Vestuário/calçado sem cor** (obrigatória no Brasil) | 414 | alto | Shopify |
| 5 | Categoria genérica demais | 279 | alto | **aguardando o fim do sync** |
| 6 | **Sem marca** | 162 | alto | Shopify + app |
| 7 | **`identifierExists=false` em produto de marca** | 150 | alto | Shopify + app |
| 8 | Tênis (calçado) como o esporte "Tênis" | 92 | alto | **aguardando o fim do sync** |
| 9 | Imagem pequena para a próxima exigência (Google) | 80 | alto | Shopify |
| 10 | Descrição curta | 54 | médio | Shopify |

\* O frete da conta é uma tabela fixa e não depende do peso: R$ 0 até R$ 399 e R$ 0 acima disso. ⚠️ Confirme se o frete é mesmo grátis abaixo de R$ 399.

**Demais achados:**
- **Identificadores:** 58 GTIN repetidos, 1 GTIN inválido (Overgrip Head Prime Tour – Preto) e 2 marcas trocadas (Meia Nike = Yonex; Squash Dunlop = Tecnifibre).
- **Categoria:** 25 com código numérico (1 já reprocessado: Raqueteira Wilson Blade V10 X9 = "6551"; na Shopify, confira o campo de categoria do Google, que deveria ser 3638) e 1 sem categoria.
- **Variantes:** 18 sem tamanho, 7 com preço destoando das demais e 44 com atributos diferentes dentro do mesmo grupo.
- **Textos:** 43 títulos curtos, 10 títulos idênticos e 31 marcas fora do padrão de escrita.
- **Promoções e desempenho:** 27 promoções sem data de fim, 23 produtos em estoque e sem nenhuma impressão em 30 dias e 14 preços ≥ 60% acima da referência do mercado.
- **Restos do gênero e da faixa etária (5 produtos):**
  - Tênis Nike Legend Essential 2 Masculino continua unissex. Ainda não foi reprocessado.
  - 4 bolas e raqueteira infantis continuam como adulto: Bola Wilson US Open Infantil Estágio 1, Wilson US Open Junior Stage 3, Babolat Red Felt Infantil e Raqueteira Babolat Carlitos Junior. Nas duas bolas Wilson, que já foram reprocessadas, falta marcar "Faixa etária = Kids" na categoria do produto na Shopify.
- **Tipo errado na Shopify:** a Bola DHS D40+ é de pingue-pongue, mas o tipo dela é "Bolas de Tênis – Pack Econômico". A categoria do Google já está certa; o que precisa mudar é o tipo.

---

## 4. Os 20 produtos mais urgentes

Mesmo critério das rodadas anteriores: gravidade × cliques e impressões, com peso pela metade para produtos sem estoque. A lista completa está em `resumo-por-produto.csv`.

| # | Produto | Estoque | Cliques 30d | Impr. 30d | Status | Principais problemas |
|---|---|---|---:|---:|---|---|
| 1 | Tênis Asics Gel Resolution X Saibro/Clay Rosa – Masculino, 40 | sim | 53 | 5.539 | CRÍTICO | Página indisponível; sem cor |
| 2 | Raquete de Tênis Wilson Ultra 100 V5 Roland Garros – Limited Edition | sim | 110 | 16.290 | CRÍTICO | Página indisponível |
| 3 | Óculos De Sol Mormaii Smash Vini Font – Camaleão | sim | 52 | 2.816 | CRÍTICO | Página indisponível |
| 4 | Shorts Nike Dri-FIT Tempo Feminino – Preto | sim | 54 | 2.363 | ALTO | Sem cor; categoria genérica*; imagem pequena; sem marca; identifierExists=false |
| 5 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 326g / 26.8b | sim | 487 | 29.200 | ALTO | Categoria incompatível*; sem marca; identifierExists=false |
| 6 | Top Nike Pro Swoosh Feminino – Vermelho | sim | 11 | 625 | CRÍTICO | Página indisponível; sem cor; categoria genérica* |
| 7 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 25.0b | sim | 180 | 10.989 | ALTO | Categoria incompatível*; sem marca; identifierExists=false |
| 8 | Raqueteira Wilson Heritage 12PK – Off White/Marrom | sim | 14 | 2.455 | CRÍTICO | Página indisponível |
| 9 | Tênis On Running The Roger Pro Fire Clay Masculino – Verde, 44 | sim | 186 | 13.612 | ALTO | Calçado como "esporte tênis"*; sem marca; identifierExists=false |
| 10 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 26.2b | sim | 94 | 8.491 | ALTO | Categoria incompatível*; sem marca; identifierExists=false |
| 11 | Bola De Tênis Wilson Roland Garros All Court – C/3 Tubos (9 Bolas) | sim | 8 | 3.025 | CRÍTICO | Página indisponível |
| 12 | Shorts Lacoste Esportivos Ultra Dry Masculino – Preto, 2GG | sim | 73 | 2.424 | ALTO | Sem cor; sem marca; identifierExists=false |
| 13 | Raqueteira Yonex Gearlogic 2026 Dupla Bege – 9 Raquetes | sim | 8 | 1.215 | CRÍTICO | Página indisponível |
| 14 | Regata Nike Court Feminina – Vermelha | sim | 4 | 204 | CRÍTICO | Página indisponível; sem cor; categoria genérica* |
| 15 | Top Nike Swoosh Futura – Preto | sim | 22 | 1.121 | ALTO | Sem cor; categoria genérica*; sem marca; identifierExists=false |
| 16 | Raquete de Beach Tennis AMA New Kronos 2026 6th Generation, 321g | sim | 329 | 28.829 | ALTO | Sem marca; identifierExists=false |
| 17 | Shorts Adidas Essential Três Listras Masculino – Preto, M | sim | 9 | 508 | CRÍTICO | Página indisponível |
| 18 | Legging Nike One Feminina – Preta, 2x | sim | 14 | 575 | ALTO | Categoria genérica*; imagem pequena; sem marca; identifierExists=false |
| 19 | Tênis Fila Master Ace Clay/Saibro Masculino – Branco/Marinho, 39 | sim | 26 | 2.583 | ALTO | Sem cor; sem marca; identifierExists=false |
| 20 | Tênis On Running The Roger Pro 3 Clay João Fonseca Masculino – Branco/Azul | sim | 126 | 8.078 | ALTO | Sem cor; calçado como "esporte tênis"* |

\* Produto ainda não reprocessado pelo último sync; a categoria deve se corrigir quando o sync terminar.

---

## 5. Plano de correção (atualizado)

> **Regra geral:** corrija na **Shopify** e sincronize pelo **app de feed**, que foi o que funcionou hoje. Não use a fonte suplementar da CLI para correções permanentes.

1. **Terminar o sync de categorias (app).** 541 produtos ainda não foram reprocessados. Se continuarem parados, dispare de novo "sync metafields from Shopify" com **Google product categories** marcado. Depois, rodamos a auditoria de novo.
2. **Página indisponível (10, Search Console + Merchant Center).** Teste ao vivo e peça nova análise. Os produtos estão ativos na Shopify.
3. **Cor (414) e tamanho (18), Shopify + app.** Esse é agora o maior problema de nível alto. Preencha "Cor" na categoria do produto na Shopify, ou como opção da variante, e sincronize **Color** e **Size** pelo mesmo botão de metacampos do app.
4. **Marca e identificadores (Shopify + app).**
   - Os 162 sem marca são os mesmos que vão como "sem identificador": preencha Fornecedor e EAN.
   - Corrija as 2 marcas trocadas, o EAN inválido e os 58 EAN repetidos.
5. **Imagens (Shopify).** Troque a imagem do Top Nike Pro Dri-Fit Preto, que está reprovado, e as 80 imagens com aviso.
6. **Promoção 84205 (Merchant Center + Shopify).** Crie o desconto de 10% no checkout ou encerre a promoção.
7. **Ajustes pontuais na Shopify.**
   - Faixa etária = Kids nas 2 bolas Wilson infantis.
   - Tipo da Bola DHS (pingue-pongue).
   - Campo de categoria do Google da Raqueteira Wilson Blade V10 X9 (= 3638).
   - Confirmar o Vestido Nike Estampado, que saiu do feed.
8. **Frete, estoque e conteúdo.**
   - Confirmar o frete grátis abaixo de R$ 399.
   - Repor os esgotados com procura.
   - Imagens adicionais, descrições e títulos curtos.
   - Pesos das variantes.
9. **Acompanhamento.** Ligar as conversões e criar custom labels.

---

### Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| `produtos.json` | JSON completo dos 1.328 produtos (`merchant.api.all_products()`) |
| `saude.csv` / `desempenho.csv` / `precos.csv` | `mc.py health`, `performance --dias 30` e `prices` |
| `irregularidades.csv` | Uma linha por problema |
| `resumo-por-produto.csv` | Uma linha por produto, com gravidade, status e urgência |
| `shopify-verificacao.json` | Status na Shopify dos 10 produtos com "página indisponível" (só leitura, 23/10 11h30) |
| `shopify-rascunhos.txt` | IDs dos 221 produtos em rascunho na Shopify (só leitura, 23/10 11h30) |
| `auditar.py` | Gera os CSVs a partir dos arquivos acima |

**Limites:**
- O site tenez.com.br não é acessível deste ambiente, então os links foram conferidos pela API da Shopify.
- Os IDs numéricos de categoria não foram validados contra a taxonomia do Google.
