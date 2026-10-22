# Merchant Center CLI

CLI em Python para consultar, analisar e atualizar produtos via **Google Merchant API** (v1).

> **Segurança:** todo comando que altera dados só **simula** e mostra o que mudaria.
> Acrescente `--aplicar` para enviar ao Google. Todo envio vira um **lote** que pode ser desfeito.

## Configuração (uma vez)

1. Ative a **Merchant API** no projeto GCP da conta de serviço.
2. No Merchant Center, adicione o e-mail da conta de serviço como **Administrador**.
3. Coloque o JSON da conta de serviço nesta pasta como `service-account.json`.
4. `cp .env.example .env` e preencha `MERCHANT_ID` e `DATA_SOURCE` (fonte suplementar via API).
5. `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
6. `.venv/bin/python mc.py register --email seu-email@empresa.com`

Nos exemplos abaixo, `mc` = `.venv/bin/python mc.py`.

## Consulta

```
mc list --limit 20                 # lista produtos
mc get pt~BRL_25260949594~SKU      # detalhe completo de um produto
mc search "tenis"                  # busca pelo título
```

## Saúde do catálogo

```
mc health --csv saude.csv          # aprovados/reprovados por destino + problemas e motivos
mc watch --notificar               # o que mudou de status desde a última execução
```

`watch` guarda uma "foto" em `dados/status-anterior.json` e registra mudanças em `dados/alertas.log`.
Para avisos automáticos, agende-o (ex.: de hora em hora).

## Relatórios

```
mc performance --dias 30 --csv desempenho.csv   # impressões, cliques, vendas; quem nunca aparece
mc prices --csv precos.csv                      # seu preço vs. preço de referência do mercado
mc price-insights --csv sugestoes.csv           # preço sugerido pelo Google e impacto previsto
mc bestsellers --sub Tennis                     # mais vendidos no Brasil e se você tem cada um
```

## Atualizações em massa

Filtros disponíveis: `--busca`, `--marca`, `--tipo`, `--ids arquivo.txt`, `--em-estoque` (ou `--todos`).

```
mc discount --marca Asics --desconto 15 --fim 2026-11-30          # simula
mc discount --marca Asics --desconto 15 --fim 2026-11-30 --aplicar
mc end-discount --marca Asics --aplicar                           # remove o preço promocional
mc csv alteracoes.csv --aplicar                                   # planilha
mc label --slot 3 --valor black-friday --tipo Raquetes --aplicar  # rótulo personalizado
mc auto-labels --aplicar                                          # rótulos automáticos
mc update pt~BRL_...~SKU --price 199.90 --aplicar                 # um produto
```

**Planilha CSV:** colunas `offer_id` (ou `product_id`) e qualquer uma de `price`, `sale_price`,
`sale_start`, `sale_end` (AAAA-MM-DD), `availability`, `title`, `description`, `link`, `image_link`,
`custom_label_0` … `custom_label_4`. Célula vazia = não mexe; `-` = remove o valor gravado.

**Rótulos automáticos** (para segmentar campanhas no Google Ads):

| Rótulo | Valores |
|---|---|
| 0 – desempenho | `mais-vendidos` (top 10% em vendas/cliques), `normal`, `sem-exposicao` |
| 1 – margem | `margem-alta` / `margem-media` / `margem-baixa` (só se o feed tiver custo) |
| 2 – promoção | `liquidacao` (≥ 30% off), `em-promocao`, `preco-cheio` |

## Textos (títulos e descrições)

```
mc texts-export textos.csv --marca Head     # exporta para revisão
# preencha novo_titulo / nova_descricao (o Claude pode sugerir), revise...
mc texts-apply textos.csv --aplicar
```

## Desfazer

```
mc batches                         # lista os lotes enviados
mc undo 20261021-152058 --aplicar  # desfaz um lote inteiro
mc clear pt~BRL_...~SKU --aplicar  # devolve o produto 100% ao Simprosys/Shopify
mc clear --tudo --aplicar          # limpa tudo que este programa gravou
```

## Promoções do Google

```
mc promo-list
mc promo-create --id pix10-nov --titulo "10% off no Pix" --modalidade percentual --valor 10 \
    --cupom PIX10 --fim 2026-11-30 --aplicar
mc promo-create --id frete-raquetes --titulo "Frete grátis em raquetes" --modalidade frete \
    --tipo Raquetes --compra-minima 300 --fim 2026-11-30 --aplicar
```

O cupom precisa existir e funcionar no checkout da Shopify; o Google analisa em até 24–48 h.

## Como funciona e limites

- Os produtos chegam pelo **Simprosys** (Shopify). Este programa grava numa **fonte suplementar**
  que tem prioridade sobre ele, campo a campo.
- Um valor gravado aqui fica **travado**: mudanças desse campo na Shopify não chegam ao Google até
  você rodar `undo` ou `clear`. Prefira mudanças permanentes direto na Shopify.
- A API não permite ler a fonte suplementar; o programa guarda o que gravou em `dados/`.
  **Não apague essa pasta**, ou o `undo` deixa de funcionar.
- Produtos novos devem entrar pela Shopify.
- Comparação de preços, sugestões e mais vendidos dependem de volume de dados na conta.
- Alterações levam alguns minutos para aparecer em `list`/`get`.
