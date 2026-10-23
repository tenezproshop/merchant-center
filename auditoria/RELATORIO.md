# Auditoria do catálogo – Google Merchant Center (Tenez) · 4ª rodada (completa)

**Data:** 23/10/2026, 14h30 (horário de Brasília) · **Modo:** somente leitura (nada foi alterado no Google, na Shopify ou em `dados/`)
**Comparada com:** 3ª rodada (11h30 de hoje), 2ª rodada (cedo) e 1ª rodada (22/10). As versões anteriores deste arquivo estão no histórico da branch.

---

## 0. O que mudou

| | 22/10 | 23/10 cedo | 23/10 11h30 | **23/10 14h30** |
|---|---:|---:|---:|---:|
| Produtos no catálogo | 1.344 | 1.336 | 1.328 | **1.332** |
| Problemas (total) | 5.169 | 5.136 | 3.775 | **2.337** |
| Crítico | 21 | 22 | 20 | 20 |
| Alto | 2.611 | 2.594 | 1.295 | **885** |
| Médio | 914 | 903 | 852 | 849 |
| Baixo | 1.623 | 1.617 | 1.608 | **583** |
| Produtos com status ALTO | 1.147 | 1.140 | 778 | **647** |
| Produtos sem nenhum problema | 7 | 7 | 32 | **243** |
| Reprovados (algum destino) | 16 | 17 | 15 | 15 |
| Reprovados em Shopping / anúncios grátis | 12 | 13 | 11 | 11 |

**Desde as 11h30, o que foi resolvido:**

| Problema | 11h30 | Agora |
|---|---:|---:|
| **Categoria genérica demais** (só "Vestuário e acessórios") | 279 | **0** |
| **Tênis (calçado) classificado como o esporte "Tênis"** | 92 | **0** |
| **Categoria incompatível com o tipo** | 37 | **0** |
| **Sem categoria** | 1 | **0** |
| **Peso de envio vazio** | 1.024 | **0** (o peso foi preenchido em 1.332 produtos) |
| Vestuário/calçado sem tamanho | 18 | 7 |
| Variantes de cores diferentes com a mesma foto | 33 | 23 |

Desde a 1ª rodada: gênero errado foi de 725 para 3 e faixa etária infantil errada, de 50 para 4. Os 40 produtos com categoria em inglês ou polonês foram para 0.

**O sync de categorias terminou às 11h41** (1.303 produtos reprocessados). Hoje, **todos os produtos com tipo conhecido estão na categoria certa**, exceto 25 variantes com código numérico antigo (§3).

**Mudanças no catálogo desde as 11h30:**
- **Voltou ao feed (publicada de novo na Shopify):** Raquete AMA Poison Bee 2026, em 3 pesos. Está **ativa e com estoque**. A variante 320g/25.2b está em estoque (1 unidade) e **continua reprovada por "página indisponível"** (§2).
- **Novos:** 2 variantes de Shorts Nike Dri-FIT Totality Masculino Cinza (G e GG). Estão como **unissex**, enquanto as outras variantes do mesmo shorts estão como masculino.
- **Saiu:** Tênis Asics Resolution 9 All Court Feminino Rosa (não verifiquei o motivo na Shopify).
- **Deixou de estar reprovado:** Tênis Asics Gel Resolution X Rosa 40 (53 cliques/mês).

---

## 1. Totais

- **Produtos baixados:** 1.332, conferidos com `mc.py health` (1.332) e com o `product_view` do relatório (1.332).
- **Estoque:** 828 em estoque e 504 fora de estoque.
- **Gênero:** 493 masculino, 428 feminino e 411 unissex. **Faixa etária:** 46 infantil e 1.286 adulto.
- **Desempenho (23/09 a 22/10):** 1.341.360 impressões e 12.079 cliques, com só **0,15 conversão** no mês, ou seja, nenhuma venda registrada. Ligue o acompanhamento de conversões.
- **Preço de referência:** 646 produtos.
- **Problemas da conta:** nenhum. **Custom labels:** nenhum produto tem.
- **Promoção do Google 84205 "10% off on all products":** continua **REPROVADA**, porque o desconto não é aplicado no checkout.
- **Peso de envio:** preenchido em todos os 1.332. Os valores mais comuns são 300 g (694 produtos), 800 g (331) e 400 g (220). Parecem pesos padrão por tipo de produto; vale conferir se refletem o peso real, principalmente nas raquetes e raqueteiras.

| Gravidade | Ocorrências |
|---|---:|
| Crítico | 20 |
| Alto | 885 |
| Médio | 849 |
| Baixo | 583 |
| **Total** | **2.337** |

**Status geral por produto:** CRÍTICO 16 · ALTO 647 · MÉDIO 282 · BAIXO 144 · OK 243.
**Origem:** Google 104, pente fino 2.233. **Onde corrigir:** Shopify 2.268, Merchant Center 35, Simprosys/app 34.

---

## 2. O que o Google aponta

São 99 produtos com algum problema: 288 ocorrências por destino, sendo 96 DISAPPROVED e 192 NOT_IMPACTED.

### 2.1 Reprovados: 15 produtos (11 também em Shopping e anúncios grátis)

| Código | Produtos | Situação |
|---|---:|---|
| `landing_page_error` – página indisponível | **10** | Todos estão **ACTIVE e publicados** na Shopify (conferido às 14h30). A página existe: faça o teste ao vivo na Inspeção de URL do Search Console e peça nova análise no Merchant Center. |
| Política de conteúdo adulto | 4 (Sunga Nike Outline Swoosh, sem estoque) | Só em Display, Demand Gen e Vídeo. Trocar a foto por uma sem modelo, ou aceitar a restrição. |
| `image_too_small` | 1 (Top Nike Pro Dri-Fit Swoosh Feminino – Preto) | Trocar a imagem principal. |

Os 10 com página indisponível:
- Wilson Ultra 100 V5 RG (110 cliques/mês)
- Óculos Mormaii Smash (52)
- Wilson Heritage 12PK
- Top Nike Pro Swoosh Vermelho
- Bola Wilson RG 3 tubos
- Shorts Nike Pro 3" Vermelho
- Shorts Adidas Essential
- Raqueteira Yonex Gearlogic Bege
- Regata Nike Court Vermelha
- **Raquete AMA Poison Bee 2026, variante 320g/25.2b.** O produto foi republicado hoje na Shopify; o status do Google deve se atualizar sozinho em alguns dias, mas vale pedir nova análise.

### 2.2 Avisos e pendentes
- **80 produtos com "imagem pequena para a próxima exigência"**, que vai virar reprovação.
- **4 títulos em maiúsculas** (Head Speed MP).
- **1 pendente** em Demand Gen (Yonex Percept 100, imagem em análise).

---

## 3. Os 10 problemas mais frequentes (agora)

| # | Problema | Produtos | Gravidade | Onde corrigir |
|---|---|---:|---|---|
| 1 | Fora de estoque e ainda no feed (60 deles tiveram 1.325 cliques em 30 dias) | 504 | baixo / médio | Shopify |
| 2 | Sem imagens adicionais | 502 | médio | Shopify |
| 3 | **Vestuário/calçado sem cor** (obrigatória no Brasil) | 418 | alto | Shopify + app |
| 4 | **Sem marca** | 164 | alto | Shopify + app |
| 5 | **`identifierExists=false` em produto de marca** | 152 | alto | Shopify + app |
| 6 | Imagem pequena para a próxima exigência (Google) | 80 | alto | Shopify |
| 7 | Descrição curta | 54 | médio | Shopify |
| 8 | Atributo diferente entre variantes do mesmo grupo | 46 | médio | Shopify |
| 9 | Título curto | 43 | médio | Shopify |
| 10 | GTIN repetido em outra oferta | 33 | alto | Shopify |

**Demais achados:**
- **25 variantes de 13 produtos com a categoria antiga em forma de código.** O campo na Shopify está certo, mas o app mandou o valor antigo. Os tênis Asics Gel Resolution, Nike Vapor Lite 3 e On The Roger Advantage Pro continuam como "1065", e a Raquete Mormaii Vitória Marchezini (o produto com mais cliques da loja) como "3906" em vez de 499850. Provavelmente o app guarda uma categoria definida manualmente nesses produtos: abra um deles no app, limpe ou corrija a categoria e sincronize.
- **Identificadores:** 33 produtos com GTIN repetido (58 ofertas), 1 GTIN inválido (Overgrip Head Prime Tour – Preto) e 2 marcas trocadas (Meia Nike = Yonex; Squash Dunlop = Tecnifibre).
- **Variantes:** 7 meias sem tamanho (os números como "38-40" estão só no título; preencha a opção "Tamanho"), 8 variantes com preço destoando das demais e 23 grupos com cores diferentes usando a mesma foto.
- **Textos:** 10 títulos idênticos, 6 descrições iguais ao título e 31 marcas fora do padrão de escrita.
- **Cor incompleta:** 30 produtos têm só uma cor no feed, mas o título cita duas ("Branco/Marinho").
- **Promoções e desempenho:** 27 promoções sem data de fim, 25 produtos em estoque sem nenhuma impressão em 30 dias e 14 preços ≥ 60% acima da referência do mercado.
- **Gênero e faixa etária (7 produtos restantes):**
  - **Shorts Nike Dri-FIT Totality Masculino Cinza G e GG** estão como unissex, e o Tênis Nike Legend Essential 2 Masculino também.
  - **4 produtos infantis estão como adulto:** Bola Wilson US Open Infantil Estágio 1, Wilson US Open Junior Stage 3, Bola Babolat Red Felt Infantil e Raqueteira Babolat Carlitos Junior.
- **Tipo errado na Shopify:** a Bola DHS D40+ é de pingue-pongue, mas o tipo dela é "Bolas de Tênis – Pack Econômico".

---

## 4. Os 20 produtos mais urgentes

Mesmo critério das rodadas anteriores: gravidade × cliques e impressões, com peso pela metade para produtos sem estoque. A lista completa está em `resumo-por-produto.csv`.

| # | Produto | Estoque | Cliques 30d | Impr. 30d | Status | Principais problemas |
|---|---|---|---:|---:|---|---|
| 1 | Raquete de Tênis Wilson Ultra 100 V5 Roland Garros – Limited Edition | sim | 110 | 16.290 | CRÍTICO | Página indisponível |
| 2 | Óculos De Sol Mormaii Smash Vini Font – Camaleão | sim | 52 | 2.816 | CRÍTICO | Página indisponível |
| 3 | Top Nike Pro Swoosh Feminino – Vermelho | sim | 11 | 625 | CRÍTICO | Página indisponível; sem cor |
| 4 | Raqueteira Wilson Heritage 12PK – Off White/Marrom | sim | 14 | 2.455 | CRÍTICO | Página indisponível |
| 5 | Shorts Nike Dri-FIT Tempo Feminino – Preto | sim | 54 | 2.363 | ALTO | Sem cor; imagem pequena; sem marca; identifierExists=false |
| 6 | Bola De Tênis Wilson Roland Garros All Court – C/3 Tubos (9 Bolas) | sim | 8 | 3.025 | CRÍTICO | Página indisponível |
| 7 | Shorts Lacoste Esportivos Ultra Dry Masculino – Preto, 2GG | sim | 73 | 2.424 | ALTO | Sem cor; sem marca; identifierExists=false |
| 8 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 326g / 26.8b | sim | 487 | 29.200 | ALTO | Sem marca; identifierExists=false |
| 9 | Raqueteira Yonex Gearlogic 2026 Dupla Bege – 9 Raquetes | sim | 8 | 1.215 | CRÍTICO | Página indisponível |
| 10 | Raquete de Beach Tennis AMA New Kronos 2026 6th Generation, 321g | sim | 329 | 28.829 | ALTO | Sem marca; identifierExists=false |
| 11 | Shorts Adidas Essential Três Listras Masculino – Preto, M | sim | 9 | 508 | CRÍTICO | Página indisponível |
| 12 | Tênis Fila Master Ace Clay/Saibro Masculino – Branco/Marinho, 39 | sim | 26 | 2.583 | ALTO | Sem cor; sem marca; identifierExists=false |
| 13 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 25.0b | sim | 180 | 10.989 | ALTO | Sem marca; identifierExists=false |
| 14 | Regata Nike Court Feminina – Vermelha | sim | 4 | 204 | CRÍTICO | Página indisponível; sem cor |
| 15 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 26.2b | sim | 94 | 8.491 | ALTO | Sem marca; identifierExists=false |
| 16 | Tênis On Running The Roger Pro Fire Clay Masculino – Verde, 44 | sim | 186 | 13.612 | ALTO | Sem marca; identifierExists=false; categoria antiga ("187" como código) |
| 17 | Boné Nike Court Heritage Unissex – Preto, P/M | sim | 12 | 1.678 | ALTO | Sem cor; sem marca; identifierExists=false |
| 18 | Top Nike Swoosh Futura – Preto | sim | 22 | 1.121 | ALTO | Sem cor; sem marca; identifierExists=false |
| 19 | Saco de Bola de Beach Tennis Ama Sport com 60 Unidades | sim | 113 | 6.633 | ALTO | Sem marca; identifierExists=false |
| 20 | Corda Solinco Hyper G 16L 1.30mm Verde – Set Individual | sim | 57 | 3.683 | ALTO | Sem marca; identifierExists=false |

Fora de estoque e com muitos cliques (vale repor): são 60 produtos, que somam 1.325 cliques em 30 dias. Os maiores estão em `resumo-por-produto.csv`.

---

## 5. Plano de correção (atualizado)

> **Regra geral:** corrija na **Shopify** e sincronize pelo **app de feed**, que foi o que funcionou hoje. Não use a fonte suplementar da CLI para correções permanentes.

1. **Página indisponível (10, Search Console + Merchant Center).** Teste ao vivo e peça nova análise. Todos estão ativos na Shopify. A Wilson Ultra 100 V5 RG sozinha tem 16 mil impressões por mês.
2. **Marca e código de barras (Shopify + app). É agora o maior grupo de problemas de gravidade alta.**
   - Os 164 produtos sem marca são os mesmos que vão como "sem identificador".
   - Preencha o Fornecedor e o EAN na Shopify.
   - Sincronize **Brand** pelo app.
   - Tire esses produtos da regra "identifier exists = no".
   - Corrija as 2 marcas trocadas, o EAN inválido e os 33 produtos com EAN repetido.
3. **Cor (418) e tamanho (7), Shopify + app.** Preencha "Cor" e "Tamanho" na categoria do produto ou como opção da variante e sincronize **Color** e **Size** pelo mesmo botão de metacampos. Nas meias, o tamanho está só no título.
4. **Categorias que sobraram (25 variantes, app).** Abra no app um dos produtos listados no §3, limpe ou corrija a categoria manual e sincronize. Prioridade: a Raquete Mormaii Vitória Marchezini.
5. **Imagens (Shopify).** Troque a imagem do Top Nike Pro Dri-Fit Preto, que está reprovado, e as 80 imagens com aviso. Associe a foto certa a cada cor nos 23 grupos.
6. **Gênero e idade nos 7 restantes (Shopify + app).** "Masculino" nos shorts Totality Cinza G e GG e no Nike Legend Essential 2, e "Faixa etária = Kids" nas bolas e na raqueteira infantis.
7. **Promoção 84205 (Merchant Center + Shopify).** Crie o desconto de 10% no checkout ou encerre a promoção.
8. **Frete (Merchant Center).** Confirme se o frete é mesmo grátis abaixo de R$ 399; hoje a tabela é R$ 0 nas duas faixas. Confira também se os pesos padrão de 300 g, 400 g e 800 g refletem os produtos.
9. **Estoque e conteúdo (Shopify).**
   - Repor os esgotados com procura e arquivar os descontinuados.
   - Imagens adicionais (502).
   - Descrições curtas (54) e títulos curtos (43).
   - Datas de fim nas 27 promoções.
   - Tipo da Bola DHS.
10. **Acompanhamento.** Ligar as conversões e criar custom labels para segmentar campanhas.

---

### Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| `produtos.json` | JSON completo dos 1.332 produtos (`merchant.api.all_products()`) |
| `saude.csv` / `desempenho.csv` / `precos.csv` | `mc.py health`, `performance --dias 30` e `prices` |
| `irregularidades.csv` | Uma linha por problema |
| `resumo-por-produto.csv` | Uma linha por produto, com gravidade, status e urgência |
| `shopify-verificacao.json` | Status na Shopify dos 10 produtos com "página indisponível" (só leitura, 23/10 14h30) |
| `shopify-rascunhos.txt` | IDs dos 221 produtos em rascunho na Shopify (só leitura, 23/10 14h30) |
| `auditar.py` | Gera os CSVs a partir dos arquivos acima |

**Limites:**
- O site tenez.com.br não é acessível deste ambiente, então os links foram conferidos pela API da Shopify.
- Os IDs numéricos de categoria não foram validados contra a taxonomia do Google.
- Os pesos de envio foram aceitos como informados; não há como saber se são os reais.
