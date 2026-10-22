# Auditoria do catálogo – Google Merchant Center (Tenez)

**Data:** 22/10/2026 · **Conta:** Merchant Center da loja tenez.com.br · **Modo:** somente leitura (nenhum dado foi alterado)

Arquivos desta pasta:

| Arquivo | Conteúdo |
|---|---|
| `produtos.json` | JSON completo dos 1.344 produtos (atributos + `productStatus` com `itemLevelIssues`), baixado com `merchant.api.all_products()` |
| `saude.csv` | Saída de `mc.py health` (uma linha por problema × destino, como o Google informa) |
| `desempenho.csv` | `mc.py performance --dias 30` (22/09 a 21/10/2026) |
| `precos.csv` | `mc.py prices` (preço de referência do Google, 642 produtos) |
| `irregularidades.csv` | **Uma linha por problema** (Google + pente fino), com gravidade, campo, valor atual, como corrigir e onde |
| `resumo-por-produto.csv` | **Uma linha por produto**: contagem por gravidade, status geral, cliques/impressões e nota de urgência |
| `auditar.py` | Script que gera os dois CSVs a partir dos arquivos acima (dá para rodar de novo sem chamar a API) |

---

## 1. Totais

- **Produtos baixados:** 1.344. Batem com o total da conta (`mc.py health` = 1.344 e `product_view` do relatório = 1.344).
- **Disponibilidade:** 829 em estoque e 515 fora de estoque.
- **Desempenho em 30 dias:** 1.430.703 impressões e 13.034 cliques. Conversões: **0,15** no período inteiro (um único produto, R$ 194,40). Na prática não há vendas registradas, então a priorização usou cliques e impressões. ⚠️ Isso sugere que o acompanhamento de conversões do Google Ads/GA4 não está ligado ao Merchant Center. Vale conferir.
- **Problemas da conta:** nenhum (API de issues da conta).
- **Custom labels:** **nenhum** produto tem rótulo personalizado. O único gravado pela CLI (`customLabel4 = teste`, lote 20261021-152058) já foi desfeito (lote 20261021-152339), e `dados/suplementar.json` está vazio. Portanto não há valores fora do padrão. Também não há segmentação por rótulo para as campanhas.

| Gravidade | Ocorrências | Produtos com ao menos uma |
|---|---:|---:|
| Crítico (reprovado ou sem exibição) | 21 | 17 |
| Alto (perde desempenho) | 2.611 | 1.147 *(status geral "ALTO")* |
| Médio | 914 | 89 *(status geral "MÉDIO")* |
| Baixo | 1.623 | 84 *(status geral "BAIXO")* |
| **Total** | **5.169** | 1.337 com algum problema; 7 sem nenhum |

Origem: 104 linhas vêm do Google (itemLevelIssues agrupados por produto e código) e 5.065 do pente fino.
Onde corrigir: Shopify 4.328 · Simprosys 807 · Merchant Center 34.

---

## 2. O que o Google aponta

Ao todo, 99 produtos têm algum `itemLevelIssue`: 292 ocorrências por destino, sendo 102 DISAPPROVED e 190 NOT_IMPACTED. Não há nenhum DEMOTED.

### 2.1 Reprovados: 16 produtos (12 deles também em Shopping e anúncios grátis)

| Código | Produtos | Destinos | Atributo | O que fazer |
|---|---:|---|---|---|
| `landing_page_error` – Product page unavailable | 11 | **Todos** (Shopping, anúncios grátis, Display, Demand Gen, Vídeo) | link | Ver abaixo |
| `sexual_interests_policy_violation` + `restricted_nfs_policy_violation` | 4 (Sunga Nike Outline Swoosh P/M/G/GG) | Display, Demand Gen, Vídeo (em Shopping e anúncios grátis é só alerta) | – | Trocar a imagem principal por foto sem modelo e pedir revisão, ou aceitar a restrição. Estão fora de estoque. |
| `image_too_small` | 1 (Top Nike Pro Dri-Fit Swoosh Feminino – Preto) | Todos | image link | Subir uma imagem maior na Shopify |

**Página indisponível (11 produtos):** consultei a Shopify só para leitura e os 11 estão **ACTIVE, publicados, com estoque e com o mesmo handle do link enviado**. A página existe, e o mais provável é falha de rastreamento do Googlebot (app antibot/proteção, redirecionamento por país/moeda, lentidão). Correção sugerida:
1. Teste ao vivo na Inspeção de URL do Search Console.
2. Se a página abrir, peça nova análise no Merchant Center.

Entre esses produtos estão a **Raquete Wilson Ultra 100 V5 Roland Garros** (113 cliques e 17.470 impressões em 30 dias) e o **Tênis Asics Gel Resolution X Rosa 40** (58 cliques).

### 2.2 Com aviso (não reprovados)

- `image_too_small_for_high_resolution` (*Image too small for upcoming enforcement*): **79 produtos**, em Shopping e Vídeo. Ainda não tem impacto, mas o próprio Google avisa que vai virar reprovação. Classifiquei como **alto**.
- `title_all_caps`: 4 produtos (RAQUETE DE TÊNIS HEAD SPEED MP L2/L3, com títulos duplicados).
- `restricted_nfs_policy_violation` como alerta em Shopping e anúncios grátis: são as mesmas 4 sungas.

### 2.3 Pendentes

- 1 produto: **Raquete de Tênis Yonex Percept 100 – Midnight Navy**, pendente em Demand Gen / Discover (`attribute_pending_review`, imagem em análise). É só aguardar e, se for reprovado, trocar a imagem.

---

## 3. Os 10 problemas mais frequentes

| # | Problema | Produtos | Gravidade | Onde corrigir |
|---|---|---:|---|---|
| 1 | Peso de envio vazio (o Simprosys manda `{"unit":"kg"}` sem valor) | 1.032 | baixo* | Shopify (peso da variante) |
| 2 | **Gênero `UNISEX` contradiz o título** (439 "Masculino" + 290 "Feminino") | 729 | alto | Simprosys (mapeamento de gênero) |
| 3 | **Categoria do Google genérica demais** (ex.: só "Vestuário e acessórios") | 640 | alto | Shopify (categoria) / Simprosys |
| 4 | Fora de estoque e ainda no feed (69 deles tiveram 1.459 cliques em 30 dias) | 515 | baixo / médio | Shopify (repor ou arquivar) |
| 5 | Sem imagens adicionais | 503 | médio | Shopify |
| 6 | **Vestuário/calçado sem cor** (obrigatório no Brasil) | 420 | alto | Shopify (opção/metacampo "Cor") |
| 7 | **Calçado classificado como o esporte "Tênis"** e não como sapato | 205 | alto | Shopify (categoria) |
| 8 | **Sem marca** (todos têm a marca no título: AMA, On, Adidas, Nike, Fila…) | 170 | alto | Shopify + Simprosys |
| 9 | **`identifierExists=false` em produto de marca de fabricante** | 158 (+12 de marca não identificada) | alto | Shopify (EAN) + Simprosys |
| 10 | Categoria do Google incompatível com o tipo (ex.: overgrip em "Grips para câmeras") | 98 | alto | Shopify (categoria) |

\* O frete da conta (`shippingSettings`) é uma tabela fixa que **não depende do peso**: R$ 0 até R$ 399 e R$ 0 acima disso. Por isso o peso vazio hoje não tira nenhum produto do ar. ⚠️ Mesmo assim, o serviço se chama "Frete Grátis*" e cobra R$ 0 nas duas faixas. Se a loja cobra frete abaixo de R$ 399, o Google está anunciando frete grátis indevidamente (risco de reprovação por divergência de frete). **Confirme no Merchant Center → Frete e devoluções.**

Outros achados relevantes, fora do top 10:
- **Faixa etária "adulto" em produto infantil/juvenil:** 50 produtos (Infantil, Júnior, GS, Kids no título). Todos os 1.344 têm `ageGroup=ADULT`.
- **Raquetes de Beach Tennis** em categorias de squash ou de tênis comum (18 incompatíveis + 5 em inglês + 4 por ID numérico).
- **Categoria em outro idioma** (inglês e até polonês, "Sprzęt sportowy > Sport > Tenis"): 40 produtos. **ID numérico** (1065, 3906, 187…): 26 produtos. Não consegui validar esses IDs contra a taxonomia oficial (o arquivo do Google está bloqueado neste ambiente), então ficaram como "conferir". **Sem categoria:** 1 (Cushion Grip Wilson Featherthin).
- Categorias claramente erradas:
  - Munhequeiras em "Saúde e beleza > Suportes e aparelhos **ortodônticos**" (8) e em "Pulseiras (de relógio)" (3)
  - Overgrips em "**Câmeras** > Grips para câmeras" (6)
  - Bonés, camisetas e meias em "Artigos esportivos **colecionáveis** > Acessórios para fãs" (44)
  - Raqueteiras em "**Bolas** de tênis" e "**Badminton**"
  - Bolsas Esportivas em "Bolas de tênis" (3)
  - Bolas de Squash em "Bolas de tênis"
- **GTIN repetido:** 55 ofertas.
  - 33 são variantes do mesmo produto com o mesmo EAN.
  - 22 são produtos diferentes com o mesmo EAN: por exemplo, o tubo de 3 bolas Dunlop AO e o pack de 3 tubos usam o mesmo GTIN, e o mesmo acontece com a caixa de 24 tubos e o pack de 3 da Babolat Gold. Kits e multipacks precisam de GTIN próprio, ou sem GTIN e com `multipack`.
- **GTIN inválido:** 1. O Overgrip Head Prime Tour – Preto tem `72479415053` (11 dígitos), que é inválido mesmo completando com zero à esquerda.
- **Marca errada no feed:**
  - "Meia **Nike** Court Multiplier" com marca **Yonex**
  - "Raquete de Squash **Dunlop** Sonic Core" com marca **Tecnifibre**
- **Marca fora do padrão de escrita:** 32 produtos ("HEAD" × "Head", "HEROE´S", "Shark Beach Tenis").
- **Atributo diferente entre variantes do mesmo produto:** 44 produtos. É principalmente a marca presente em umas variantes e ausente em outras.
- **Variantes de cores diferentes com a mesma imagem principal:** 23.
- **Preço de variante destoando das demais tamanhos (>15%):** 7. Exemplo: Camiseta Adidas Clube Roxa P/M a R$ 129 contra R$ 179 nas demais.
- **Descrição curta (<150 caracteres):** 58. Seis delas são iguais ao título (ex.: "Bermuda Fila Gain Train Masculina").
- **Títulos curtos (<30):** 43. Os 6 shorts "Le Coq Sportif- Azul, G" não dizem o que é o produto.
- **Títulos idênticos entre produtos diferentes:** 10.
- **Preço promocional sem data de fim:** 28, enquanto os outros 213 têm a janela automática de 30 dias. Entre eles estão os mais clicados: Mormaii Vitória Marchezini, Nox Nova87 e Heroes Starlight Ruby.
- **Em estoque e aprovado, mas com 0 impressão em 30 dias:** 23.
- **Preço ≥ 60% acima da referência do Google:** 17 (baixo, só para conferir). Exemplo: Bola Wilson US Open 3 tubos R$ 219 contra referência de R$ 82. Pode ser comparação com produto de outra quantidade.

**Nenhuma ocorrência** encontrada para:
- Título vazio ou >150 caracteres, ou com texto promocional
- Descrição vazia, >5.000 caracteres, com HTML quebrado ou com entidades (`&nbsp;` etc.)
- Preço zero, moeda ≠ BRL, promocional ≥ preço cheio, promoção vencida, desconto >70% (o maior é 54%)
- Sem imagem, imagem/link sem https, domínio diferente de tenez.com.br, link fora de `/products/`
- Pré-venda sem data, condição ausente
- Variante faltando no título, variante sem `itemGroupId`, custom labels fora do padrão

---

## 4. Os 20 produtos mais urgentes

**Critério:** urgência = pontos de gravidade × fator de impacto. Os pontos valem 100 por crítico, 20 por alto, 5 por médio e 1 por baixo. O fator de impacto é `1 + ln(1+cliques) + 0,5·ln(1+impressões/100) + 5·conversões`, com peso pela metade para produtos fora de estoque. A lista completa está ordenada em `resumo-por-produto.csv` (coluna `urgencia`).

| # | Produto | Estoque | Cliques 30d | Impr. 30d | Status | Principais problemas (crítico/alto) |
|---|---|---|---:|---:|---|---|
| 1 | Tênis Asics Gel Resolution X Saibro/Clay Rosa – Masculino, 40 | sim | 58 | 6.234 | CRÍTICO | Página indisponível; sem cor; gênero UNISEX × "Masculino" |
| 2 | Shorts Ama Sport Masculino – Bege | sim | 16 | 1.060 | CRÍTICO | Página indisponível; gênero; categoria genérica; sem marca; identifierExists=false |
| 3 | Raquete de Tênis Wilson Ultra 100 V5 Roland Garros – Limited Edition | sim | 113 | 17.470 | CRÍTICO | Página indisponível |
| 4 | Shorts Nike Dri-FIT Tempo Feminino – Preto | sim | 53 | 2.366 | ALTO | Sem cor; gênero; categoria genérica; imagem pequena (aviso); sem marca; identifierExists=false |
| 5 | Shorts Lacoste Esportivos Ultra Dry Masculino – Preto, 2GG | sim | 69 | 2.399 | ALTO | Sem cor; gênero; categoria genérica; sem marca; identifierExists=false |
| 6 | Top Nike Pro Swoosh Feminino – Vermelho | sim | 11 | 625 | CRÍTICO | Página indisponível; sem cor; gênero; categoria genérica |
| 7 | Tênis On Running The Roger Pro Fire Clay Masculino – Verde, 44 | sim | 199 | 14.507 | ALTO | Gênero; calçado como "esporte tênis"; sem marca; identifierExists=false |
| 8 | Óculos De Sol Mormaii Smash Vini Font – Camaleão | sim | 53 | 3.048 | CRÍTICO | Página indisponível |
| 9 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 326g / 26.8b | sim | 490 | 29.657 | ALTO | Categoria incompatível; sem marca; identifierExists=false |
| 10 | Tênis Fila Master Ace Clay/Saibro Masculino – Branco/Marinho, 39 | sim | 30 | 2.786 | ALTO | Sem cor; gênero; calçado como "esporte tênis"; sem marca; identifierExists=false |
| 11 | Vestido Nike Tênis Dri-Fit – Estampado | sim | 95 | 3.093 | ALTO | Sem cor; categoria genérica; sem marca; identifierExists=false |
| 12 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 25.0b | sim | 178 | 10.815 | ALTO | Categoria incompatível; sem marca; identifierExists=false |
| 13 | Raqueteira Wilson Heritage 12PK – Off White/Marrom | sim | 15 | 2.632 | CRÍTICO | Página indisponível |
| 14 | Tênis Nike Zoom GP Challenge Pro Saibro/Clay – Masculino, 41 | sim | 212 | 12.564 | ALTO | Sem cor; gênero; calçado como "esporte tênis" |
| 15 | Tênis On Running The Roger Pro 3 Clay João Fonseca Masculino – Branco/Azul | sim | 129 | 8.012 | ALTO | Sem cor; gênero; calçado como "esporte tênis" |
| 16 | Camisa Polo Adidas Tênis Masculina – Preta, P | sim | 53 | 2.245 | ALTO | Gênero; categoria genérica; sem marca; identifierExists=false |
| 17 | Raquete de Beach Tennis AMA Athena Boreal Limited 2026, 322g / 26.2b | sim | 102 | 9.007 | ALTO | Categoria incompatível; sem marca; identifierExists=false |
| 18 | Tênis On Running THE ROGER Clubhouse Pro All Court Masculino – Branco/Azul | sim | 95 | 9.347 | ALTO | Sem cor; gênero; calçado como "esporte tênis" |
| 19 | Shorts Adidas Essential Três Listras Masculino – Preto, M | sim | 9 | 538 | CRÍTICO | Página indisponível; gênero |
| 20 | Regata Nike Court Feminina – Vermelha | sim | 4 | 204 | CRÍTICO | Página indisponível; sem cor; gênero; categoria genérica |

Fora de estoque, mas com muitos cliques no período (demanda perdida, vale repor):
- Camisa Nike Seleção Brasil 2026/27 EGG (222 cliques)
- Raquete AMA New Kronos 2026 319g (162 cliques)
- Raquete AMA Poison Bee 2026 (124 cliques)
- Tênis On The Roger Pro 3 João Fonseca (120 cliques)
- Raquete AMA New Kronos 318g (103 cliques)

---

## 5. Plano de correção (em ordem)

> **Regra geral:** corrija na **Shopify**, ou nas regras do **Simprosys** que leem a Shopify. Não use a fonte suplementar (`mc update`/`csv`/`texts-apply`) para correções permanentes: o campo gravado ali fica *travado* e mudanças futuras na Shopify deixam de chegar ao Google até rodar `undo`/`clear`. A fonte suplementar serve só para testes rápidos e temporários.

1. **Reprovados por "página indisponível" (11 produtos, Merchant Center + Search Console).** Os produtos estão ativos e publicados na Shopify. Teste as URLs na Inspeção de URL (teste ao vivo) e verifique se algum app de proteção/antibot, geolocalização ou redirecionamento de moeda bloqueia o Googlebot. Depois peça nova análise. É o que mais rende rápido: a Wilson Ultra 100 V5 RG sozinha tem 17 mil impressões por mês.
2. **Imagens (Shopify).** Troque a imagem do Top Nike Pro Dri-Fit Preto, que está reprovado. Comece já os **79** avisos de "imagem pequena para a próxima exigência", porque eles vão virar reprovação. A lista está filtrando `categoria = google:image_too_small_for_high_resolution`. Sungas: foto sem modelo, se quiser voltar a Display e Demand Gen.
3. **Gênero e faixa etária (Simprosys, corrige ~780 produtos de uma vez).**
   - Hoje o Simprosys manda `gender=unisex` e `age_group=adult` como padrão para quase tudo.
   - Configure o mapeamento a partir de tags ou metacampos da Shopify: Masculino → male, Feminino → female, Infantil/Júnior/GS → kids.
   - Para isso, os produtos precisam dessas tags ou metacampos na Shopify (dá para fazer em massa pelo tipo e pelo título).
4. **Categoria do Google (Shopify, por tipo de produto).** Ajuste a *Categoria do produto* na Shopify, ou a regra de categoria do Simprosys, **por tipo**:
   - Tênis (calçado) → "Vestuário e acessórios > Sapatos". Hoje 205 estão como o esporte tênis e 26 só como "Vestuário e acessórios".
   - Roupas → "Vestuário e acessórios > Roupas > …". Hoje 622 produtos, entre roupas, acessórios e alguns calçados, estão só como "Vestuário e acessórios".
   - Raquetes de beach tennis → "… > Tênis de plataforma e padel > Raquetes de tênis de plataforma e padel".
   - Corrija também os absurdos (câmeras, ortodônticos, colecionáveis, badminton, bolas para raqueteiras).
   - Elimine as categorias em inglês e polonês.
   - A coluna `como_corrigir` traz a categoria sugerida para cada produto.

   Com a categoria certa, o Google passa a exigir cor e tamanho em roupas e calçados, então faça o passo 5 junto.
5. **Cor e tamanho (Shopify).** 420 roupas, calçados e acessórios de vestir estão sem cor e 18 sem tamanho. Crie a opção "Cor", ou preencha o metacampo de cor da categoria, e o tamanho (mesmo "Único"). Envie as cores compostas completas ("Branco/Marinho", não só "Branco").
6. **Marca e identificadores (Shopify + Simprosys).**
   - Os 170 produtos sem marca são exatamente os que vão com `identifierExists=false`. Pelo padrão, é provável que o Simprosys esteja tratando como "sem identificador" os produtos sem código de barras e, nesse caso, sem enviar a marca. Isso é uma hipótese a confirmar na configuração.
   - Preencha o **Fornecedor (vendor)** e o **código de barras (EAN)** das variantes.
   - Tire esses produtos da regra "identifier exists = no".
   - Corrija as marcas trocadas (Meia Nike = Yonex; Squash Dunlop = Tecnifibre), o EAN inválido do Overgrip Head e os 55 EAN repetidos (multipacks com GTIN próprio).
   - Padronize a grafia das marcas (Head, Heroe's, Shark).
7. **Frete (Merchant Center).** Confirme se a tabela "Frete Grátis*" (R$ 0 nas duas faixas, até e acima de R$ 399) reflete o que o checkout cobra. Se não, corrija a faixa abaixo de R$ 399. Depois, cadastre o peso nas variantes da Shopify (1.032 vazios), para o caso de a tabela passar a depender de peso.
8. **Estoque (Shopify).** Reponha os itens fora de estoque com procura (69 tiveram cliques em 30 dias). Arquive ou oculte do canal Google os descontinuados (515 fora de estoque).
9. **Conteúdo (Shopify).**
   - 503 produtos sem imagens adicionais
   - 58 descrições curtas ou iguais ao título
   - 43 títulos curtos (ex.: "Le Coq Sportif- Azul, G" sem dizer que é short)
   - Títulos em maiúsculas (Head Speed MP)
   - Títulos sem marca (Yonex EZONE, Asics Gel-Dedicate)
   - "Tenis" sem acento
   - Fotos certas por cor nas variantes (23)
   - Preços de variantes destoantes (7)
   - Data de fim nas 28 promoções sem janela
10. **Acompanhamento.**
    - Ligue o rastreamento de conversões (hoje 0,15 conversão em 30 dias).
    - Use `mc.py auto-labels` (ou rótulos na Shopify/Simprosys) para segmentar campanhas, porque hoje nenhum produto tem custom label.
    - Rode de novo `auditar.py` após baixar um `produtos.json` novo para medir o avanço.

---

### Critérios e limites desta auditoria

- **Gravidade:**
  - Crítico: reprovado pelo Google em algum destino, ou campo obrigatório ausente (preço, imagem, link, descrição).
  - Alto: perde desempenho ou alcance (atributos obrigatórios de vestuário, categoria errada, identificadores, aviso de reprovação futura).
  - Médio: qualidade de anúncio.
  - Baixo: cosmético ou sem efeito hoje.
- **Itens checados por regra própria:**
  - "Tipo no título": palavras-chave por `productType`.
  - "Marca no título": primeira palavra da marca normalizada, sem acentos e caixa.
  - "Gênero": presença de "mascul"/"femin" no título.
  - "Infantil": Infantil/Júnior/Jr/Kids/Juvenil/GS no título.
  - "Categoria compatível": prefixos aceitos por tipo, definidos em `auditar.py`.
- **Verificação de GTIN:** tamanho 8/12/13/14, dígito verificador GS1 e prefixos internos (2xx).
- **Limites:**
  - O site tenez.com.br não é acessível deste ambiente, então os links não foram testados ao vivo. A verificação dos 11 links reprovados foi feita pela API da Shopify, só para leitura.
  - Os IDs numéricos de categoria não foram validados contra a taxonomia.
  - Não há dados de vendas suficientes para priorizar por conversão.
