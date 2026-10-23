# Auditoria do catálogo – Google Merchant Center (Tenez) · 2ª rodada

**Data:** 23/10/2026 · **Modo:** somente leitura (nada foi alterado no Google, na Shopify ou em `dados/`)
**Comparada com:** auditoria de 22/10/2026 (branch `auditoria-catalogo-2026-10-22`)

---

## 0. O que mudou desde ontem

**Resumo:** os dados que o Google tem de cada produto **quase não mudaram**.
- **Nenhum** dos problemas de cadastro apontados ontem foi corrigido: gênero, categoria, cor, marca, identificadores, imagens, títulos e descrições.
- Comparei atributo por atributo os 1.334 produtos que estão nos dois downloads. Só mudaram:

| Atributo | Produtos alterados | Exemplo |
|---|---:|---|
| Janela da promoção (`salePriceEffectiveDate`) | 15 | renovação automática da janela de 30 dias do Simprosys |
| Preço promocional (`salePrice`) | 5 | Camisa Nike Seleção Brasil 2026/27 passou a ter promo de R$ 349 |
| Disponibilidade | 5 | 2 voltaram ao estoque, 3 esgotaram |

- **10 ofertas saíram do feed:**
  - Camiseta Lacoste Regular Fit Block Color Azul (4 tamanhos)
  - Raquete Nox Nova87 2026
  - Calça Nike Court Laranja (2)
  - Camiseta On Running Court-T Swing (3)

  As três últimas estão como rascunho na Shopify.
- **2 ofertas entraram:**
  - Bola DHS D40+ 3 estrelas
  - Tênis On The Roger Pro 3 João Fonseca Roxo 38
- **Data de processamento:** pelo menos 1.095 dos 1.336 produtos foram processados pela última vez pelo Google em **20/10**, antes da auditoria de ontem. Nada do que foi feito chegou ainda aos produtos.

**Por que suas atualizações podem não aparecer:**
1. **A mudança foi feita na Shopify.** Ela só chega ao Google quando o Simprosys sincroniza. Pode levar horas, ou exigir uma sincronização manual no app.
2. **A mudança foi feita no Merchant Center** (edição de produto, regra de atributo ou feed suplementar pela interface). O processamento pode levar até algumas horas. Pela API, não encontrei nenhuma fonte de dados nova: as fontes continuam sendo só o feed do Simprosys, a suplementar da CLI (vazia) e as de promoções.
3. **O pedido de revisão de reprovação** não altera os dados. Só muda o status quando o Google reanalisa, o que pode levar alguns dias.

👉 Se puder me dizer **o que** foi alterado e **onde**, consigo verificar especificamente se já chegou. Uma terceira rodada daqui a 24 h deve mostrar o efeito.

**Mudanças nos problemas:**

| | 22/10 | 23/10 |
|---|---:|---:|
| Produtos no catálogo | 1.344 | **1.336** |
| Problemas (total) | 5.169 | **5.136** |
| Crítico | 21 | **22** |
| Alto | 2.611 | 2.594 |
| Médio | 914 | 903 |
| Baixo | 1.623 | 1.617 |
| Reprovados (algum destino) | 16 | **17** |
| Reprovados em Shopping / anúncios grátis | 12 | **13** |

A queda no total vem quase toda dos 10 produtos que saíram do feed (44 problemas foram embora com eles). Nos produtos que continuam:
- **Resolvidos (15):**
  - 2 reprovações por "página indisponível": Shorts Ama Sport Bege e Short On Running 7" Court Branco
  - 9 alertas de preço acima da referência, por variação do relatório do Google
  - 3 produtos que voltaram ao estoque ou saíram da lista de esgotados
  - 1 produto que voltou a ter impressão
- **Novos (20):**
  - **3 novas reprovações por "página indisponível":**
    - Raquete Infantil Wilson Blade Júnior 26 V10 (89 cliques e 9.831 impressões em 30 dias)
    - Shorts Nike Pro Feminino 3" Vermelho GG
    - Raquete AMA Poison Bee 2026
  - **7 ofertas de produtos em rascunho na Shopify que continuam no Google** (verificação nova, veja §2.4)
  - Oscilações de preço de referência e de estoque

---

## 1. Totais de hoje

- **Produtos baixados:** 1.336. Bate com `mc.py health` (1.336) e com o `product_view` do relatório (1.336). Estão em `produtos.json`, com atributos e `productStatus` completos.
- **Estoque:** 824 em estoque e 512 fora de estoque.
- **Desempenho (23/09 a 22/10):** 1.346.020 impressões e 12.186 cliques. Ainda **0,15 conversão** (R$ 194,40) no período, ou seja, sem vendas registradas. A priorização continua por cliques e impressões. ⚠️ Vale ligar o acompanhamento de conversões.
- **Preço de referência:** 650 produtos (`precos.csv`).
- **Problemas da conta:** nenhum. **Custom labels:** nenhum produto tem.
- **Promoções do Google:**
  - A promoção **84205 "10% off on all products"** (01/07 a 31/12) está **REPROVADA** em Shopping e anúncios grátis desde 11/09. Motivo do Google: *"No or a lower discount found — Promotions must provide customers with discounts that can be applied at checkout"*. O desconto anunciado não é aplicado no checkout.
  - As outras 6 estão paradas (STOPPED).

| Gravidade | Ocorrências |
|---|---:|
| Crítico | 22 |
| Alto | 2.594 |
| Médio | 903 |
| Baixo | 1.617 |
| **Total** | **5.136** |

Status geral por produto: CRÍTICO 18 · ALTO 1.140 · MÉDIO 88 · BAIXO 83 · OK 7.
Origem: Google 105, pente fino 5.031. Onde corrigir: Shopify 4.293 · Simprosys 809 · Merchant Center 34.

---

## 2. O que o Google aponta hoje

São 100 produtos com algum problema: 298 ocorrências por destino, sendo 108 DISAPPROVED e 190 NOT_IMPACTED. Não há nenhum DEMOTED.

### 2.1 Reprovados: 17 produtos (13 também em Shopping e anúncios grátis)

| Código | Produtos | Destinos |
|---|---:|---|
| `landing_page_error` – Product page unavailable | **12** | todos |
| `sexual_interests_policy_violation` + `restricted_nfs_policy_violation` | 4 (Sunga Nike Outline Swoosh P/M/G/GG, fora de estoque) | Display, Demand Gen, Vídeo |
| `image_too_small` | 1 (Top Nike Pro Dri-Fit Swoosh Feminino – Preto) | todos |

### 2.2 Os 12 com "página indisponível": conferência na Shopify (somente leitura, 23/10)

| Situação na Shopify | Produtos | O que fazer |
|---|---|---|
| **Rascunho (DRAFT), não publicado** | Raquete AMA Poison Bee 2026 – Gigio Cariani | A causa é real: a página não existe. Publique o produto ou deixe-o arquivado; o Simprosys precisa tirá-lo do feed (§2.4). |
| Ativo, publicado, com estoque e handle igual ao link | os outros 11, incluindo Wilson Ultra 100 V5 RG (110 cliques), Wilson Blade Júnior 26 V10 (89 cliques), Asics Gel Resolution X Rosa 40 (53 cliques) e Óculos Mormaii Smash (52 cliques) | A página existe; provável falha do Googlebot ao acessá-la (antibot, redirecionamento de país/moeda, lentidão). Faça o **teste ao vivo** na Inspeção de URL do Search Console e peça nova análise. Nove deles já estavam reprovados ontem. |

### 2.3 Avisos e pendentes (iguais a ontem)
- **79 produtos com "imagem pequena para a próxima exigência"**, que vai virar reprovação.
- **4 títulos em maiúsculas** (Head Speed MP).
- **1 pendente:** Raquete Yonex Percept 100 – Midnight Navy, com imagem em análise em Demand Gen.

### 2.4 Nova verificação: feed × status na Shopify
Consultei na Shopify todos os produtos em rascunho ou arquivados: são 220, todos em rascunho. **7 ofertas de 3 deles continuam no feed do Google:**
- Camisa Polo Adidas Climacool Bordô (M/G/GG)
- Raquete AMA Poison Bee 2026 (3 pesos)
- Toalha INNI Roxo

Todas estão fora de estoque. Isso indica que o Simprosys nem sempre remove do feed o produto que vira rascunho: a Calça Nike Court e a Camiseta On Court-T saíram, essas não. Classifiquei como **alto**: corrija no Simprosys (forçar sincronização ou excluir do feed).

---

## 3. Os 10 problemas mais frequentes (hoje)

| # | Problema | Produtos | Gravidade | Onde corrigir |
|---|---|---:|---|---|
| 1 | Peso de envio vazio (só a unidade "kg") | 1.029 | baixo* | Shopify |
| 2 | **Gênero `UNISEX` contradiz o título** (Masculino/Feminino) | 725 | alto | Simprosys |
| 3 | **Categoria do Google genérica demais** | 632 | alto | Shopify / Simprosys |
| 4 | Fora de estoque e ainda no feed (63 deles tiveram 1.551 cliques em 30 dias) | 511 | baixo / médio | Shopify |
| 5 | Sem imagens adicionais | 502 | médio | Shopify |
| 6 | **Vestuário/calçado sem cor** (obrigatória no Brasil) | 415 | alto | Shopify |
| 7 | **Calçado classificado como o esporte "Tênis"** | 205 | alto | Shopify |
| 8 | **Sem marca** | 166 | alto | Shopify + Simprosys |
| 9 | **`identifierExists=false` em produto de marca de fabricante** | 154 | alto | Shopify + Simprosys |
| 10 | Categoria incompatível com o tipo (câmeras, ortodônticos, colecionáveis, badminton…) | 99 | alto | Shopify |

\* A tabela de frete da conta é fixa e não depende do peso: R$ 0 até R$ 399 e R$ 0 acima disso. ⚠️ Confirme se a loja realmente dá frete grátis abaixo de R$ 399. Se não der, o Google está anunciando frete grátis por engano.

Demais achados, todos inalterados em relação a ontem salvo indicação:
- Faixa etária "adulto" em produto infantil: 50
- Categoria em inglês ou polonês: 40
- Categoria como ID numérico, para conferir: 25
- Sem categoria: 1
- GTIN repetido: 58
- GTIN inválido: 1 (Overgrip Head Prime Tour – Preto, `72479415053`)
- Marca trocada: 2 (Meia Nike = Yonex; Squash Dunlop = Tecnifibre)
- Marca fora do padrão de escrita: 32
- Atributo diferente entre variantes: 46
- Variantes de cores diferentes com a mesma foto: 23
- Preço de variante destoando das demais: 7
- Descrição curta: 54 (6 iguais ao título)
- Título curto: 43
- Título idêntico: 10
- Promoção sem data de fim: 27
- Em estoque e com 0 impressão em 30 dias: 23
- Preço ≥ 60% acima da referência: 14

**Continuam sem nenhuma ocorrência:** título vazio, longo ou promocional; descrição vazia ou com HTML quebrado; preço zero ou moeda ≠ BRL; promoção ≥ preço cheio, vencida ou com desconto >70%; imagem ausente; link sem https ou fora do domínio; pré-venda sem data; variante sem `itemGroupId`; custom labels fora do padrão.

---

## 4. Os 20 produtos mais urgentes

Critério igual ao de ontem: pontos de gravidade (crítico 100, alto 20, médio 5, baixo 1) × impacto (`1 + ln(1+cliques) + 0,5·ln(1+impressões/100) + 5·conversões`), com peso pela metade para produtos sem estoque. A lista completa está em `resumo-por-produto.csv`.

| # | Produto | Estoque | Cliques 30d | Impr. 30d | Status | Principais problemas |
|---|---|---|---:|---:|---|---|
| 1 | Tênis Asics Gel Resolution X Saibro/Clay Rosa – Masculino, 40 | sim | 53 | 5.539 | CRÍTICO | Página indisponível; sem cor; gênero |
| 2 | Raquete de Tênis Infantil Wilson Blade Júnior 26 V10 | sim | 89 | 9.831 | CRÍTICO | **Página indisponível (nova)** |
| 3 | Raquete de Tênis Wilson Ultra 100 V5 Roland Garros – Limited Edition | sim | 110 | 16.290 | CRÍTICO | Página indisponível |
| 4 | Shorts Nike Dri-FIT Tempo Feminino – Preto | sim | 54 | 2.363 | ALTO | Sem cor; gênero; categoria genérica; imagem pequena (aviso); sem marca; identifierExists=false |
| 5 | Shorts Lacoste Esportivos Ultra Dry Masculino – Preto, 2GG | sim | 73 | 2.424 | ALTO | Sem cor; gênero; categoria genérica; sem marca; identifierExists=false |
| 6 | Top Nike Pro Swoosh Feminino – Vermelho | sim | 11 | 625 | CRÍTICO | Página indisponível; sem cor; gênero; categoria genérica |
| 7 | Tênis On Running The Roger Pro Fire Clay Masculino – Verde, 44 | sim | 186 | 13.612 | ALTO | Gênero; calçado como "esporte tênis"; sem marca; identifierExists=false |
| 8 | Óculos De Sol Mormaii Smash Vini Font – Camaleão | sim | 52 | 2.816 | CRÍTICO | Página indisponível |
| 9 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 326g / 26.8b | sim | 487 | 29.200 | ALTO | Categoria incompatível; sem marca; identifierExists=false |
| 10 | Tênis Fila Master Ace Clay/Saibro Masculino – Branco/Marinho, 39 | sim | 26 | 2.583 | ALTO | Sem cor; gênero; calçado como "esporte tênis"; sem marca; identifierExists=false |
| 11 | Vestido Nike Tênis Dri-Fit – Estampado | sim | 100 | 3.239 | ALTO | Sem cor; categoria genérica; sem marca; identifierExists=false |
| 12 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 25.0b | sim | 180 | 10.989 | ALTO | Categoria incompatível; sem marca; identifierExists=false |
| 13 | Raqueteira Wilson Heritage 12PK – Off White/Marrom | sim | 14 | 2.455 | CRÍTICO | Página indisponível |
| 14 | Tênis On Running The Roger Pro 3 Clay João Fonseca Masculino – Branco/Azul | sim | 126 | 8.078 | ALTO | Sem cor; gênero; calçado como "esporte tênis" |
| 15 | Tênis Nike Zoom GP Challenge Pro Saibro/Clay – Masculino, 41 | sim | 201 | 11.713 | ALTO | Sem cor; gênero; calçado como "esporte tênis" |
| 16 | Camisa Polo Adidas Tênis Masculina – Preta, P | sim | 54 | 2.237 | ALTO | Gênero; categoria genérica; sem marca; identifierExists=false |
| 17 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 26.2b | sim | 94 | 8.491 | ALTO | Categoria incompatível; sem marca; identifierExists=false |
| 18 | Tênis On Running THE ROGER Clubhouse Pro All Court Masculino – Branco/Azul | sim | 91 | 8.704 | ALTO | Sem cor; gênero; calçado como "esporte tênis" |
| 19 | Regata Nike Court Feminina – Vermelha | sim | 4 | 204 | CRÍTICO | Página indisponível; sem cor; gênero; categoria genérica |
| 20 | Shorts Adidas Essential Três Listras Masculino – Preto, M | sim | 9 | 508 | CRÍTICO | Página indisponível; gênero |

Fora de estoque e com muitos cliques (vale repor):
- Camisa Nike Seleção Brasil 2026/27 EGG (218 cliques)
- **Tênis Nike Zoom GP Challenge Pro 43** (197 cliques; esgotou desde ontem)
- Raquete AMA New Kronos 319g (160 cliques)
- Raquete AMA Poison Bee 319g (117 cliques; está em rascunho na Shopify)
- Tênis On The Roger Pro 3 João Fonseca (109 cliques)

---

## 5. Plano de correção (em ordem)

> **Regra geral:** corrija na **Shopify** ou nas regras do **Simprosys**. Não use a fonte suplementar (`mc update`/`csv`/`texts-apply`) para correções permanentes: o campo fica travado e as mudanças da Shopify deixam de chegar ao Google.

1. **Reprovações por página indisponível (12):**
   - **Poison Bee:** publique o produto ou garanta que ele saia do feed.
   - **Os outros 11:** teste ao vivo no Search Console e peça nova análise no Merchant Center. A Wilson Blade Júnior entrou na lista hoje e já tem 9,8 mil impressões por mês.
2. **Feed × Shopify (Simprosys):** remova do feed as 7 ofertas de produtos em rascunho e confira por que o Simprosys não as tirou automaticamente.
3. **Promoção 84205 reprovada (Merchant Center + Shopify):** crie na Shopify o desconto automático de 10% que a promoção anuncia, ou encerre a promoção.
4. **Imagens (Shopify):**
   - Troque a imagem do Top Nike Pro Dri-Fit Preto, que está reprovado.
   - Substitua as 79 imagens com aviso: filtre `categoria = google:image_too_small_for_high_resolution`.
   - Sungas: use foto sem modelo.
5. **Gênero e faixa etária (Simprosys):** mapeie o gênero e a faixa etária a partir de tags ou metacampos da Shopify. Isso corrige cerca de 775 produtos.
6. **Categoria do Google (Shopify, por tipo):**
   - Calçados → "Vestuário e acessórios > Sapatos"
   - Roupas → "… > Roupas > …"
   - Beach tennis → "… > Raquetes de tênis de plataforma e padel"
   - Corrija também os absurdos e as categorias em inglês ou polonês.

   A categoria sugerida para cada produto está em `como_corrigir`.
7. **Cor e tamanho (Shopify):** 415 sem cor e 18 sem tamanho.
8. **Marca e identificadores (Shopify + Simprosys):**
   - Fornecedor e EAN nos 166 sem marca, e tirá-los da regra "identifier exists = no".
   - Corrigir as 2 marcas trocadas, o EAN inválido e os EAN repetidos (multipacks com GTIN próprio).
9. **Frete (Merchant Center):** confirmar a regra de frete grátis abaixo de R$ 399. Cadastrar pesos na Shopify.
10. **Estoque e conteúdo (Shopify):**
    - Repor os esgotados com procura e arquivar os descontinuados.
    - Imagens adicionais.
    - Descrições e títulos curtos.
    - Títulos em maiúsculas ou sem marca.
    - Fotos por cor.
    - Preços destoantes.
    - Datas de fim nas promoções.
11. **Acompanhamento:**
    - Ligar o rastreamento de conversões.
    - Criar custom labels para segmentar campanhas.
    - Repetir esta auditoria depois que as mudanças forem processadas.

---

### Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| `produtos.json` | JSON completo dos 1.336 produtos (`merchant.api.all_products()`) |
| `saude.csv` | `mc.py health` |
| `desempenho.csv` | `mc.py performance --dias 30` |
| `precos.csv` | `mc.py prices` |
| `irregularidades.csv` | Uma linha por problema (Google + pente fino) |
| `resumo-por-produto.csv` | Uma linha por produto, com contagem por gravidade, status e urgência |
| `shopify-verificacao.json` | Status na Shopify dos 12 produtos com "página indisponível" (consulta só leitura, 23/10) |
| `shopify-rascunhos.txt` | IDs dos 220 produtos em rascunho na Shopify (consulta só leitura, 23/10) |
| `auditar.py` | Script que gera os CSVs a partir dos arquivos acima. Mudanças desde ontem: usa a data do dia, verifica produtos em rascunho que estão no feed e detalha o "página indisponível" com o status da Shopify. |

**Critérios e limites:** são os mesmos da 1ª rodada (veja o `RELATORIO.md` da branch `auditoria-catalogo-2026-10-22`). O site tenez.com.br continua inacessível deste ambiente, então os links foram conferidos pela API da Shopify, só para leitura. Os IDs numéricos de categoria não foram validados contra a taxonomia.
