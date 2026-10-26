# Auditoria do catálogo – Google Merchant Center (Tenez) · 5ª rodada (completa)

**Data:** 26/10/2026, 14h56 (horário de Brasília) · **Modo:** somente leitura (nada foi alterado no Google, na Shopify ou em `dados/`)
**Comparada com:** a 4ª rodada (23/10, 14h30). As versões anteriores deste arquivo estão no histórico da branch.

---

## 0. O que mudou desde 23/10

### 0.1 O Google agora recebe os produtos de duas fontes

Há uma **fonte nova na conta: "Shopify App API"** (o app oficial da Shopify). **1.081 dos 1.334 produtos agora vêm dela** e só **253 continuam vindo do Simprosys**. Nas duas rodadas anteriores, os 1.332 produtos vinham do Simprosys. Nas ofertas que passaram para a fonte nova, mudaram, em ordem de volume:

| Campo | Produtos que mudaram | O que mudou |
|---|---:|---|
| Link, frete, quantidade, descrição, categoria | cerca de 1.050 a 1.080 | O link passa a usar `utm_source=google&utm_medium=product_sync` (antes vinha do Simprosys); a descrição vem em texto simples, sem HTML; a categoria vem como **código numérico** (187, 5322, 3906…); o frete vem como serviço padrão `SHIPPING` |
| Título | 823 | Sem a vírgula antes do tamanho: "Branco, M" virou "Branco M" |
| Marca | 141 | Passou a ser enviada em produtos que antes não tinham (AMA, Nike, On Running) |
| Cor | 626 | Cores informadas de outro jeito ("branco e azul" virou "Branco"; produtos sem cor passaram a ter) |
| Gênero / faixa etária | 190 / 163 | Passaram a seguir a categoria da Shopify (masculino, feminino, infantil) |
| Material | 75 | Novo atributo enviado |
| Condição, `identifierExists`, `itemGroupId` do Simprosys | cerca de 970 / 1.070 / 930 | Deixaram de ser enviados no formato antigo. O `itemGroupId` agora vem como `shopify_ZZ_<id do produto>` |

**Resultado nos problemas:** a fonte nova resolveu parte do que estava aberto, mas trouxe efeitos novos (§0.3 e §0.4).

### 0.2 Aviso novo de "anúncios locais grátis"

O Google passou a avaliar um **destino novo, "FREE_LOCAL_LISTINGS" (anúncios locais grátis)**. **1.081 produtos estão reprovados nele** por `local_stores_lack_inventory` ("Missing local inventory data"). Isso não afeta Shopping nem anúncios grátis online: os mesmos produtos continuam aprovados nesses destinos. Como a loja vende só online, o aviso vai continuar enquanto o programa estiver ligado. Desative o programa de anúncios locais gratuitos no Merchant Center ou ignore. Registrei como **baixo** e ele **não entra** nas contagens de problemas e de reprovados abaixo (mas continua no `irregularidades.csv`).

### 0.3 O que melhorou

| Problema | 23/10 | Agora |
|---|---:|---:|
| Sem marca | 164 | **28** |
| `identifierExists=false` em produto de marca | 152 | **27** |
| Vestuário/calçado sem cor | 418 | **211** |
| Sem imagens adicionais | 502 | **116** |
| Categoria em código numérico sem conferência | 25 | 7 (e 20 estão agora marcadas como incompatíveis, veja §3) |
| GTIN inválido | 1 | **0** |
| Títulos idênticos entre produtos diferentes | 10 | 2 |
| Atributo diferente entre variantes do mesmo grupo | 46 | 17 |
| Reprovados por "página indisponível" | 10 | **9** |

### 0.4 O que piorou ou ficou novo com a fonte nova

| Problema | Antes | Agora | Observação |
|---|---:|---:|---|
| **Sem GTIN e sem MPN** (marca presente, sem identificador) | 0 | **155** | O Simprosys enviava `identifierExists=false` ou MPN; a fonte nova não envia. O Google ainda não acusou, por isso classifiquei como médio |
| **Preço promocional sem data de fim** | 27 | **202** | O Simprosys criava uma janela automática de 30 dias; a fonte nova não envia data |
| **Gênero contradizendo o título** (feminino enviado como masculino) | 3 | **14** | Na Shopify o gênero está certo; o app enviou masculino. Camiseta Adidas Tênis Climacool Feminina Branca (3 tamanhos), Tênis On Roger Advance Pro Feminino (2) e Tênis Yonex Power Sonicage Lilás Feminino (9) |
| **Sem gênero** | 0 | 5 | Bonés On Running Lightweight e Testeira Lacoste |
| **Sem faixa etária** | 0 | 30 | Bonés On Running Lightweight, meias Adidas e outros |
| **Sem tamanho** | 7 | 19 | Camisetas Lacoste, meias Adidas/Fila/On e Saia Adidas Plissada Infantil |
| **Categoria sem valor** | 0 | 3 | Mochilas e raqueteiras AMA Supreme (produtos novos) |
| **Condição não enviada** | 0 | 976 | O Google assume "novo". É opcional; classifiquei como baixo |
| **Peso de envio vazio** | 0 | 7 | Produtos novos AMA Supreme e Toalha Fila |

### 0.5 Mudanças no catálogo
- **Saíram do feed:** Vestido Tênis On Running Court Dress Split Roxo (P, PP, M), Boné Unissex On Running João Fonseca Branco, Saia Nike Court Dri-Fit Feminina Vermelha (rascunho na Shopify) e Meias Adidas Amortecimento Bordô.
- **Entraram:** Raquete Heroes Starlight Ruby (324g/25b), Mochilas e Raqueteiras Beach Tennis AMA Supreme (6 ofertas: Kronos, Azul e Caramelo, Bege e Marrom) e Toalha Fila Quick Dry Azul Marinho.
- **Não há mais produto em rascunho da Shopify no Google.** Conferi na Shopify: 224 produtos estão em rascunho e nenhum deles aparece no feed.

---

## 1. Totais

| | 22/10 | 23/10 cedo | 23/10 11h30 | 23/10 14h30 | **26/10 14h56** |
|---|---:|---:|---:|---:|---:|
| Produtos no catálogo | 1.344 | 1.336 | 1.328 | 1.332 | **1.334** |
| Problemas (total)* | 5.169 | 5.136 | 3.775 | 2.337 | **1.824** |
| Crítico | 21 | 22 | 20 | 20 | **19** |
| Alto | 2.611 | 2.594 | 1.295 | 885 | **499** |
| Médio | 914 | 903 | 852 | 849 | **558** |
| Baixo | 1.623 | 1.617 | 1.608 | 583 | **748** |
| Produtos com status Alto | 1.147 | 1.140 | 778 | 647 | **437** |
| Produtos sem nenhum problema | 7 | 7 | 32 | 243 | **351** |
| Reprovados (destinos online) | 16 | 17 | 15 | 15 | **14** |
| Reprovados em Shopping e anúncios grátis | 12 | 13 | 11 | 11 | **10** |

\* Sem os dois avisos informativos novos: estoque local (1.081) e condição não enviada (976), que somam **2.057** ocorrências e estão no `irregularidades.csv` como baixo. Contando tudo, são 3.881 ocorrências.

- **Produtos baixados:** 1.334, conferidos com `mc.py health` (1.334) e com o `product_view` do relatório (1.334).
- **Estoque:** 829 em estoque e 505 fora de estoque.
- **Fonte dos dados:** Shopify App API 1.081 · Simprosys 253.
- **Gênero:** 521 masculino, 410 feminino, 241 unissex e **162 sem gênero**. **Faixa etária:** 44 infantil, 1.135 adulto e **155 sem faixa etária**. Nessa contagem, sem valor aparece quando a fonte nova não envia o atributo.
- **Desempenho (26/09 a 25/10):** 1.254.432 impressões e 11.229 cliques, com só **0,15 conversão** no mês, ou seja, nenhuma venda registrada. Ligue o acompanhamento de conversões.
- **Preço de referência:** 640 produtos.
- **Problemas da conta:** nenhum. **Custom labels:** nenhum produto tem.
- **Promoção do Google 84205 "10% off on all products":** continua **REPROVADA** (o desconto não é aplicado no checkout).
- **Peso de envio:** preenchido em 1.327 dos 1.334 produtos.

**Status geral por produto:** CRÍTICO 15 · ALTO 437 · MÉDIO 292 · BAIXO 239 · OK 351.
**Origem:** Google 1.183 (1.081 são o aviso de estoque local), pente fino 2.698. **Onde corrigir:** Shopify 1.531, Merchant Center 1.118 (1.081 do estoque local) e Simprosys ou app 1.232.

---

## 2. O que o Google aponta

São 97 produtos com algum problema nos destinos online (eram 99). **Reprovados nos destinos online: 14 produtos, dos quais 10 também em Shopping e anúncios grátis.**

### 2.1 Reprovados

| Código | Produtos | Situação |
|---|---:|---|
| `landing_page_error`: página indisponível | **9** | Todos estão **ACTIVE e publicados** na Shopify (conferido hoje). A página existe: fazer o teste ao vivo na Inspeção de URL do Search Console e pedir nova análise no Merchant Center. |
| Conteúdo adulto restrito e interesses sexuais | 4 (Sunga Nike Outline Swoosh, sem estoque) | Só em Display, Demand Gen e Vídeo. Trocar a foto por uma sem modelo, ou aceitar a restrição. |
| `image_too_small` | 1 (Top Nike Pro Dri-Fit Swoosh Feminino - Preto) | Trocar a imagem principal. |

Os 9 com página indisponível:
- Wilson Ultra 100 V5 RG (96 cliques/mês)
- Óculos Mormaii Smash (45)
- Wilson Heritage 12PK
- Bola Wilson RG 3 tubos
- Raqueteira Yonex Gearlogic Bege
- Top Nike Pro Swoosh Vermelho
- Shorts Adidas Essential
- Regata Nike Court Vermelha
- Raquete AMA Poison Bee 2026 (variante 320g/25.2b)

O Shorts Nike Pro Feminino 3" Vermelho deixou de estar reprovado desde a rodada anterior.

### 2.2 Avisos e pendentes
- **79 produtos com "imagem pequena para a próxima exigência"** (antes 80).
- **4 títulos em maiúsculas** (Head Speed MP).
- **1 pendente** em Demand Gen (Yonex Percept 100, imagem em análise).
- **1.081 produtos reprovados só nos anúncios locais grátis** (§0.2).

---

## 3. Os 10 problemas mais frequentes (sem os avisos informativos)

| # | Problema | Ofertas | Gravidade | Onde corrigir |
|---|---|---:|---|---|
| 1 | Sem data de fim no preço promocional | 202 | baixo | Shopify + app |
| 2 | Sem GTIN e sem MPN (marca presente) | 155 | médio | Shopify + app |
| 3 | Sem imagens adicionais | 116 | médio | Shopify |
| 4 | Fora de estoque e ainda no feed (61 deles tiveram 1.175 cliques em 30 dias) | 505 | baixo / médio | Shopify |
| 5 | **Vestuário/calçado sem cor** | 211 | alto | Shopify + app |
| 6 | Imagem pequena para a próxima exigência (Google) | 79 | alto | Shopify |
| 7 | Descrição curta | 56 | médio | Shopify |
| 8 | GTIN repetido em outra oferta | 58 | alto | Shopify |
| 9 | Título curto | 45 | médio | Shopify |
| 10 | Sem faixa etária | 30 | alto | Shopify + app |

**Outros achados relevantes:**
- **Sem marca (28) e `identifierExists=false` em produto de marca (27):** todos são ofertas que ainda vêm do Simprosys e não migraram para a fonte nova.
- **Gênero errado, feminino como masculino:** 14 ofertas (§0.4), todas da fonte nova. Conferi dois desses produtos na Shopify (Tênis Yonex Power Sonicage Lilás Feminino e Camiseta Adidas Tênis Climacool Feminina Branca) e o "Gênero-alvo" está **Feminino**, então o erro está no app que envia. A camiseta Adidas tem as tags Feminino e Masculino ao mesmo tempo, o que pode confundir o app; no Yonex só há a tag Feminino, então a causa não é clara. Vale conferir a regra de gênero do app.
- **Categoria incompatível (20 ofertas):** 16 variantes ainda com o código **1065** (esporte tênis em vez de sapato): Tênis Asics Gel Resolution X e Resolution x Feminino, Nike Vapor Lite 3 Feminino e On Roger Advantage Pro Feminino, mais a Raqueteira Wilson Pro Staff Classic 12R. Além delas, 2 ofertas da Raquete Mormaii Vitória Marchezini (**3906**, deveria ser 499850), a Raquete Heroes Starlight Ruby (**499848**, que é de pickleball, deveria ser 499850) e a Raqueteira Wilson Blade V10 X9 (**6551**, deveria ser 3638).
- **Sem categoria do Google:** 3 ofertas (AMA Supreme). **Sem tipo de produto:** 1.
- **Identificadores:** 58 ofertas com GTIN repetido (a mesma quantidade das rodadas anteriores) e 2 marcas trocadas (Meia Nike = Yonex; Squash Dunlop = Tecnifibre).
- **Variantes:** 19 sem tamanho, 8 com preço destoando das demais e 15 grupos com cores diferentes usando a mesma foto.
- **Textos:** 2 títulos idênticos, 6 descrições iguais ao título e 32 marcas fora do padrão de escrita.
- **Desempenho e preço:** 28 produtos em estoque e sem nenhuma impressão em 30 dias; 13 com preço ≥ 60% acima da referência do mercado.
- **Tamanho em formato de código:** 1 oferta com tamanho "tamanho-unico".
- **Códigos de categoria:** conferi os códigos numéricos pelas categorias da Shopify (187 = Sapatos, 5322 = Roupas esportivas, 3906 = raquetes de tênis, 499850 = raquetes de beach tennis/padel, 3638 = raqueteiras, 3113 = bolas de tênis etc.). Os códigos 4077 e 4126 (Toalha Fila) não puderam ser conferidos e foram aceitos.

**Continuam sem nenhuma ocorrência:** título vazio, longo ou promocional; descrição vazia ou com HTML quebrado (a fonte nova manda texto simples); preço zero ou moeda ≠ BRL; promoção ≥ preço cheio, vencida ou com desconto >70%; imagem ausente; link sem https ou fora do domínio; pré-venda sem data; custom labels fora do padrão; produtos em rascunho no feed.

---

## 4. Os 20 produtos mais urgentes

Mesmo critério das rodadas anteriores: gravidade × cliques e impressões, com peso pela metade para produtos sem estoque. A lista completa está em `resumo-por-produto.csv`.

| # | Produto | Estoque | Cliques 30d | Impr. 30d | Status | Principais problemas |
|---|---|---|---:|---:|---|---|
| 1 | Raquete de Tênis Wilson Ultra 100 V5 Roland Garros - Limited Edition | sim | 96 | 13.485 | CRÍTICO | Página indisponível |
| 2 | Óculos De Sol Mormaii Smash Vini Font - Camaleão | sim | 45 | 2.506 | CRÍTICO | Página indisponível; sem cor |
| 3 | Raqueteira Wilson Heritage 12PK - Off White/Marrom | sim | 11 | 2.120 | CRÍTICO | Página indisponível |
| 4 | Bola De Tênis Wilson Roland Garros All Court - C/3 Tubos (9 Bolas) | sim | 6 | 2.680 | CRÍTICO | Página indisponível |
| 5 | Raqueteira Yonex Gearlogic 2026 Dupla Bege - 9 Raquetes | sim | 8 | 1.215 | CRÍTICO | Página indisponível |
| 6 | Top Nike Pro Swoosh Feminino - Vermelho | sim | 10 | 610 | CRÍTICO | Página indisponível |
| 7 | Shorts Adidas Essential Três Listras Masculino - Preto M | sim | 9 | 472 | CRÍTICO | Página indisponível |
| 8 | Raquete de Beach Tennis Mormaii Vitória Marchezini 2026, 326,3g / 26b | sim | 513 | 22.445 | ALTO | Categoria incompatível (3906); GTIN repetido |
| 9 | Tênis Asics Gel Resolution x Clay / Saibro Feminino - Preto/Rosa 39 | sim | 116 | 5.534 | ALTO | Sem cor; categoria incompatível (1065) |
| 10 | Tênis On Running The Roger Pro Fire Clay Masculino - Verde, 44 | sim | 161 | 11.775 | ALTO | Sem marca; identifierExists=false |
| 11 | Regata Nike Court Feminina - Vermelha | sim | 4 | 204 | CRÍTICO | Página indisponível |
| 12 | Tênis Asics Gel Resolution x Clay / Saibro Feminino - Preto/Rosa 36 | sim | 18 | 1.930 | ALTO | Sem cor; categoria incompatível (1065) |
| 13 | Tênis Asics Gel Resolution x Clay / Saibro Feminino - Preto/Rosa 37 | sim | 16 | 1.690 | ALTO | Sem cor; categoria incompatível (1065) |
| 14 | Boné On Running Lightweight Kids - Verde | sim | 20 | 3.390 | ALTO | Sem gênero; sem faixa etária |
| 15 | Short Saia Adidas Com Short - Preto, G | sim | 5 | 381 | ALTO | Sem cor; sem marca; identifierExists=false |
| 16 | Tênis Asics Gel Resolution x Clay / Saibro Feminino - Preto/Rosa 35 | sim | 12 | 1.306 | ALTO | Sem cor; categoria incompatível (1065) |
| 17 | Boné Unissex On Running Lightweight - Cinza | sim | 16 | 2.813 | ALTO | Sem gênero; sem faixa etária |
| 18 | Raquete de Beach Tennis Heroes Starlight Ruby - 2026 324g / 25b | sim | 418 | 30.852 | ALTO | Categoria incompatível (499848) |
| 19 | Tênis On Running The Roger Pro 3 Clay João Fonseca Feminino - Roxo | sim | 8 | 5.493 | ALTO | Sem cor; GTIN repetido |
| 20 | Boné On Running Lightweight Kids - Lilás | sim | 17 | 1.409 | ALTO | Sem gênero; sem faixa etária |

Fora de estoque e com muitos cliques (vale repor): são 61 produtos, que somam 1.175 cliques em 30 dias. Os maiores estão em `resumo-por-produto.csv`.

---

## 5. Plano de correção (atualizado)

> **Regra geral:** corrija na **Shopify** e sincronize pelo **app de feed**. Não use a fonte suplementar da CLI para correções permanentes.

1. **Decidir a fonte única dos produtos.** Hoje o Google recebe 1.081 produtos do app oficial da Shopify (Shopify App API) e 253 do Simprosys. Se a ideia é trocar de fonte, confirme que o Simprosys foi desligado ou limitado para não competir com a nova; se não foi proposital, desative o app novo. Defina qual atributo cada fonte controla, para não voltar a perder campos como `itemGroupId`, `identifierExists` e a janela de promoção.
2. **Página indisponível (9, Search Console + Merchant Center).** Teste ao vivo e peça nova análise. Todos estão ativos na Shopify. A Wilson Ultra 100 V5 RG tem 13 mil impressões por mês.
3. **Anúncios locais grátis (Merchant Center).** Desative o programa para os 1.081 avisos "Missing local inventory data" deixarem de aparecer.
4. **Gênero e faixa etária (app + Shopify).** As 14 ofertas femininas enviadas como masculino estão com o "Gênero-alvo" certo na Shopify; confira a regra de gênero no app (e retire a tag Masculino da Camiseta Adidas Feminina). Preencha gênero e faixa etária dos bonés On Running Lightweight, da testeira Lacoste e das meias Adidas. Corrija também a faixa etária dos 5 produtos infantis.
5. **Categorias (Shopify).** As 16 variantes com o código 1065 (Asics Gel Resolution, Nike Vapor Lite 3 e On Roger Advantage Pro Feminino) precisam do código 187. A Raquete Mormaii Vitória Marchezini e a Heroes Starlight Ruby precisam do 499850. A Wilson Blade V10 X9 precisa do 3638. Preencha a categoria das 3 ofertas AMA Supreme sem categoria.
6. **Cor (211) e tamanho (19), Shopify + app.** Preencha a cor das roupas e calçados que continuam sem ela e o tamanho das camisetas Lacoste, das meias e da Saia Adidas Plissada Infantil.
7. **Marca e código de barras (Shopify + app).** Faltam marca em 28 produtos, mais 27 com identifierExists=false e 155 sem GTIN nem MPN. Preencha o EAN ou o SKU do fabricante (MPN). Corrija os 58 EAN repetidos e as 2 marcas trocadas.
8. **Preço promocional (Shopify + app).** O app novo não envia data de fim para as 202 ofertas em promoção. Confira se isso é aceitável ou se há como enviar a data pela Shopify.
9. **Imagens (Shopify).** Troque a imagem do Top Nike Pro Dri-Fit Preto, que está reprovado, e as 79 imagens com aviso. Associe a foto da cor certa a cada variante nos 15 grupos.
10. **Promoção 84205 (Merchant Center + Shopify).** Crie o desconto de 10% no checkout ou encerre a promoção.
11. **Frete (Merchant Center).** Confirme se o frete é mesmo grátis abaixo de R$ 399; hoje a tabela mostra R$ 0 nas duas faixas. Confira também se os pesos padrão (300 g, 400 g, 800 g) refletem os produtos.
12. **Estoque e conteúdo (Shopify).** Repor os esgotados com procura e arquivar os descontinuados. Imagens adicionais (116), descrições curtas (56) e títulos curtos (45).
13. **Acompanhamento.** Ligar as conversões e criar custom labels para segmentar campanhas.

---

### Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| `produtos.json` | JSON completo dos 1.334 produtos (`merchant.api.all_products()`) |
| `saude.csv` / `desempenho.csv` / `precos.csv` | `mc.py health`, `performance --dias 30` e `prices` |
| `irregularidades.csv` | Uma linha por problema |
| `resumo-por-produto.csv` | Uma linha por produto, com gravidade, status e urgência (sem os avisos informativos; a coluna `avisos_informativos` mostra quantos foram deixados de fora) |
| `shopify-verificacao.json` | Status na Shopify dos 9 produtos com "página indisponível" (só leitura, 26/10) |
| `shopify-rascunhos.txt` | IDs dos 224 produtos em rascunho na Shopify (só leitura, 26/10) |
| `auditar.py` | Gera os CSVs a partir dos arquivos acima. Novidades desta rodada: aceita categorias em código numérico (mapa de códigos por tipo), trata o destino de anúncios locais como aviso informativo e normaliza o `itemGroupId` da fonte nova |

**Limites:**
- O site tenez.com.br não é acessível deste ambiente, então os links foram conferidos pela API da Shopify.
- Os códigos de categoria foram conferidos pelas categorias da Shopify e pelos nomes em português; não consegui baixar a taxonomia oficial do Google.
- Os pesos de envio foram aceitos como informados.
