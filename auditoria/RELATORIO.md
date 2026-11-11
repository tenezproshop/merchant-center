# Auditoria do catálogo — Merchant Center Tenez (6ª rodada, 11/11/2026)

Somente leitura. Dados baixados em 11/11/2026 pela Merchant API; desempenho de 12/10 a 10/11/2026.
Arquivos: `irregularidades.csv`, `resumo-por-produto.csv`, `saude.csv`, `desempenho.csv`, `precos.csv`, `produtos.json`.

## 0. O que mudou desde a 5ª rodada (26/10)
- **Uma fonte só.** Todas as 1.289 ofertas vêm agora da Simprosys. O corte da sincronização do app do Google funcionou, e o conflito entre as duas fontes acabou.
- **O catálogo encolheu:** 1.334 → 1.289 ofertas (−45). Não investiguei quais saíram. Há 260 produtos em rascunho na Shopify (eram 224).
- **Reprovações e erros críticos praticamente zerados.** O Google não aponta mais página indisponível, conteúdo adulto nem produto reprovado em anúncios. Resta 1 item crítico: uma imagem em revisão. Em todos os destinos de anúncio, 1.289 ofertas estão aprovadas.
- **Cor:** de 211 para 29 ofertas de vestuário e calçado sem cor. Faixa etária sem preenchimento: de 30 para 0.
- **Rótulos personalizados novos:** a Simprosys passou a enviar `customLabel0` a `customLabel3` em 1.055 ofertas (desempenho, estoque, faixa de ticket, preço cheio ou oferta). Trato como informativo e preciso da sua confirmação de que é intencional. Os valores de `customLabel0` (fraldinha, osso, file, cupim, novo) parecem nomes internos.
- **Piorou:** marca ausente, imagens adicionais ausentes e gênero contraditório (ver abaixo). São efeitos de a Simprosys ser agora a fonte única.

## 1. Totais (sem os avisos informativos)
| | 5ª rodada | 6ª rodada |
|---|---|---|
| Ofertas no Merchant Center | 1.334 | 1.289 |
| Produtos na Shopify (agrupados) | — | 585 |
| Irregularidades | 1.824 | 1.837 |
| Críticas | 19 | 1 |
| Altas | 499 | 496 |
| Médias | 558 | 796 |
| Baixas | 748 | 544 |
| Ofertas com ao menos um problema | 983 | 954 |

Por produto: 1 crítico, 323 alto, 432 médio, 532 baixo e 1 sem problemas. O "OK" caiu de 351 para 1 porque quase toda oferta ganhou o aviso de médio "sem imagens adicionais" ou o baixo "fora de estoque e ainda ativo".

Avisos informativos (fora dos totais): 3.165 de rótulos personalizados e os de condição não enviada. O aviso de estoque local sumiu com o fim da fonte do app.

## 2. Os 10 problemas mais frequentes
1. **Sem imagens adicionais (médio): 464 ofertas.** Eram 116. A Simprosys não envia as fotos extras que o app enviava.
2. **Fora de estoque e ainda ativo no feed (baixo): 441 ofertas**, mais 16 em médio por ter recebido cliques.
3. **Sem marca: 139 ofertas (86 produtos).** Cada uma vem junto com `identifierExists=false`. Os maiores grupos são AMA (38), Adidas (21), On Running (16), Nike (15), Fila (14) e Lacoste (8).
4. **Imagem pequena para a futura exigência do Google (alto): 70 ofertas.**
5. **Sem cor em vestuário e calçado (alto): 29 ofertas.**
6. **Gênero "unissex" contradiz o título "Masculino" (alto): 24 ofertas.** São novas. Antes, o app enviava o gênero certo.
7. **GTIN repetido (alto): 62 ofertas**, entre variantes do mesmo produto ou de produtos diferentes.
8. **Categoria do Google incompatível com o produto (alto):** 20 ofertas com o código genérico 1065 e 9 calçados classificados como esporte tênis.
9. **Marca fora do padrão de escrita (baixo): 26 ofertas.**
10. **Peso de envio vazio (baixo): 28 ofertas.**

## 3. Produtos mais urgentes (pontuação de urgência)
Quase todos são produtos com muita exposição, sem venda e com 2 a 3 problemas altos:
1. Saco de Bola de Beach Tennis Ama Sport com 60 unidades: 8.565 impressões, 112 cliques, 2 conversões.
2. Raquete de Beach Tennis AMA Athena Boreal Limited: 40.107 impressões, 701 cliques.
3. Shorts Lacoste Esportivos Ultra Dry Masculino: 7.962 impressões, 228 cliques.
4. Legging Nike One Feminina.
5. Raquete de Beach Tennis AMA Poison Bee 2026.
6. Raquete de Beach Tennis Mormaii Vitória Marchezini 2026.
7. Tênis On Running The Roger Pro Fire Clay Masculino.
8. Tênis On Running The Roger Pro 3 Clay João Fonseca Masculino.
9. Tênis Asics Gel Resolution X Clay Saibro Masculino.
10. Faixa de Cabelo Adidas Tennis Multiple Width.

A lista completa dos 20 está em `resumo-por-produto.csv`, ordenada pela coluna `urgencia`.

## 4. Desempenho nos últimos 30 dias
- 1.566.379 impressões, 14.776 cliques e **apenas 2 conversões**.
- Só 2 produtos venderam. 165 aparecem e têm cliques sem vender, 692 aparecem com poucos cliques e 430 nunca aparecem.
- Os produtos com mais cliques sem venda são raquetes de beach tennis (Heroes Starlight Ruby: 820 cliques; AMA Athena Boreal: 701; Mormaii Vitória Marchezini: 457).
- Conversões tão baixas para esse volume de cliques podem ser da medição (fontes de conversão duplicadas, já apontadas na varredura da conta). Não confirmei isso.

## 5. Plano de correção, em ordem
1. **Confirmar os rótulos personalizados** da Simprosys (informativo).
2. **Gênero:** corrigir os 24 casos "Unissex" com título "Masculino". No Shopify o gênero está certo, então o ajuste é na Simprosys.
3. **Marca e identificadores:** cadastrar EANs nas variantes pela Shopify, a opção A que propus. É o que faz a Simprosys parar de enviar `identifierExists=false` e voltar a enviar a marca.
4. **Imagens adicionais:** conferir na Simprosys por que as fotos extras não são enviadas.
5. **Cores restantes:** 29 ofertas de vestuário e calçado, pela Shopify.
6. **Categorias do Google:** as 29 ofertas de calçado com categoria errada.
7. **Imagens pequenas:** 70 ofertas, antes da exigência do Google.
8. **Fora de estoque ativo:** decidir o que sai do feed (441 ofertas).

## Limites
- Os "diverge do título" são pistas e não erros confirmados.
- Não verifiquei na Shopify a causa de cada problema nesta rodada.
- O erro de página de destino (landing) não apareceu, então `shopify-verificacao.json` não foi atualizado e está desatualizado.
- A planilha do Drive ainda não foi atualizada com esta rodada.
