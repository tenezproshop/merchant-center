# Proposta: alinhar o frete do Google Shopping ao frete cobrado no site

**Data:** 26/10/2026 · **Responsável:** equipe de e-commerce · **Decisão pedida:** aprovar a mudança

## Resumo
O Merchant Center (Google Shopping) informa **frete R$ 0 em todas as faixas de preço**. No site, o frete grátis vale **a partir de R$ 399**, e abaixo disso o frete é calculado pela Frenet. Propomos informar ao Google **R$ 24,00 para pedidos abaixo de R$ 399** e manter **R$ 0 a partir de R$ 399**.

## Situação atual
- No Google, o serviço "Frete Grátis*" tem R$ 0 nas duas faixas de preço (lido pela API do Merchant Center em 26/10/2026).
- No site, a Shopify entrega o cálculo à Frenet, com frete grátis acima de R$ 399.
- Nos últimos 100 pedidos, os que pagaram frete (abaixo de R$ 399) ficaram na maioria entre R$ 19 e R$ 27, com mediana de cerca de R$ 23. Alguns chegaram a R$ 31–44.
- Cerca de 4 em cada 10 pedidos com entrega nesse período pagaram frete (contagem aproximada).
- Alguns pedidos abaixo de R$ 399 tiveram frete R$ 0, provavelmente por o valor de tabela ser maior que o subtotal após desconto. Não foi verificado.

## Proposta
| Faixa de preço do pedido | Frete informado ao Google |
|---|---|
| Até R$ 398,99 | R$ 24,00 |
| R$ 399,00 ou mais | R$ 0 |

R$ 24 fica um pouco acima da mediana cobrada, de propósito: informar menos do que o cobrado aumenta o risco de reprovação.

## Prós
- **Reduz o risco de reprovação** por frete divergente. A reprovação tira produtos do Google e zera o desempenho deles.
- **Elimina a promessa falsa de frete grátis** nos itens abaixo de R$ 399.
- **Menos abandono no carrinho:** o cliente que clica esperando frete grátis e vê o valor só no carrinho tende a desistir. Informar antes filtra o clique pouco qualificado.
- **Conversão por clique tende a subir**, porque o cliente já chega sabendo o custo.
- **Alinha com a política de frete grátis a partir de R$ 399**, que passa a funcionar como incentivo visível para aumentar o ticket.
- **Mudança simples e reversível:** é uma alteração de tabela, sem impacto no site.

## Contras e riscos
- **Menos cliques nos itens abaixo de R$ 399.** O selo de frete grátis ajuda o clique, e ele deixa de aparecer nesses itens. O efeito não foi medido, então não há estimativa de queda.
- **Pode perder competitividade em preço total** frente a concorrentes que mostram frete grátis.
- **R$ 24 é uma estimativa.** A Frenet calcula por CEP e peso, e o Merchant Center não tem como replicar esse cálculo. Alguns clientes verão valor diferente no carrinho (de R$ 19 a R$ 44).
- **Efeito fora da área de melhoria:** a tabela de frete só pode ser alterada no Merchant Center. A Shopify não consegue enviar essa regra ao Google, pois ela está dentro da Frenet.

## Como medir (sugestão)
- Registrar antes: cliques, CTR, custo, conversões e receita dos últimos 30 dias (os dados estão no `desempenho.csv`).
- Comparar após 14 dias, olhando separadamente produtos abaixo e acima de R$ 399.
- Se a queda de cliques não vier acompanhada de ganho de conversão, reavaliar o valor (por exemplo R$ 22 ou R$ 20).

## Alternativa
Manter como está. Evita a queda potencial de cliques, mas mantém o risco de reprovação e de suspensão por informação divergente, que seria um impacto bem maior.

## Recomendação
Aprovar a mudança para R$ 24,00 abaixo de R$ 399 e acompanhar por 14 dias.
