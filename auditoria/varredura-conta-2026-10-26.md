# Varredura técnica da conta do Merchant Center (além do feed de produtos)

**Data:** 26/10/2026 · **Modo:** somente leitura · **Conta:** Tenez Pro Shop (5338435201)

Fontes: Merchant API (conta, site, frete, devoluções, programas, usuários, relacionamentos, fontes de dados, promoções, conversões, cota) e a Shopify (políticas, domínio e perfil de frete).

## O que está certo
- **Problemas da conta:** nenhum.
- **Site:** `tenez.com.br` verificado e reivindicado; HTTPS ativo na Shopify.
- **Telefone verificado**, e-mail de atendimento e endereço (Uberlândia/MG) preenchidos.
- **Programas:** anúncios do Shopping e anúncios grátis ativos no Brasil. A única pendência é para a Coreia (irrelevante).
- **Cota da API:** uso mínimo (cerca de 2.000 de 20.000.000 chamadas).
- **Políticas na Shopify:** contato, privacidade, reembolso, frete, termos de serviço e aviso legal existem.
- **Google Ads, Business Profile (1 listagem) e GA4** estão vinculados.

## Achados, por prioridade

| # | Gravidade | Achado | Onde se corrige |
|---|---|---|---|
| 1 | Alto | **Duas fontes primárias alimentam o mesmo destino** (mesma feed label BRL_25260949594, idioma pt, país BR): "Simprosys Feed" (253 produtos) e "Shopify App API" (1.081). Os dois provedores aparecem como vinculados à conta. Há risco de conflito de dados e de produtos trocando de fonte. | Shopify (decidir a fonte única: canais/apps) |
| 2 | Alto → decisão: manter | **Frete divergente.** O Merchant Center tem um único serviço "Frete Grátis*" com R$ 0 nas duas faixas de preço (até R$ 399 e acima de R$ 399). Na Shopify o frete é calculado pela Frenet, com frete grátis a partir de R$ 399. Proposta feita: R$ 24 abaixo de R$ 399 (ver `proposta-frete-google-2026-10-26.md`). **Decisão do Rafael em 26/10: não alterar por agora.** O risco de reprovação por frete divergente continua. | Merchant Center (a Shopify não envia essa regra ao Google) |
| 3 | Alto (relido em 26/10: sem mudança na API) | **Política de devolução incompleta.** Os métodos são "na loja" e "em quiosque", mas a loja é online (deveria incluir envio pelo correio). O tipo de política está vazio (sem prazo de devolução definido). A URL usa `www.tenez.com.br/trocas-e-devolucoes`, diferente do domínio principal sem `www` e da página de reembolso da Shopify. | Merchant Center (a Shopify não altera esta política) |
| 4 | Informativo | **Checkout no Google reprovado (DISAPPROVED), sem impacto.** O programa de checkout do Google só está habilitado em 15 países, e o Brasil não está entre eles. O modelo de link usa `loja.tenez.com.br` e `{id}`, que não serve para o carrinho da Shopify. Não afeta as vendas e não há correção pela Shopify. Se o status incomodar, cancelar a inscrição no Merchant Center. | Merchant Center |
| 5 | Médio | **Fontes de conversão duplicadas.** Há 5 ativas: GA4 "Tenez G4" e 4 "Shopify Channel App" (MC-FT06DXVT94, MC-11W1MECEX3, MC-5BSRPDZGG0, MC-G1EB6VJZ1Q). Risco de contar a mesma venda mais de uma vez. Mesmo assim o relatório mostra só 0,15 conversão em 30 dias. | App do Google na Shopify e Merchant Center |
| 6 | Médio | **Promoção 84205 "10% off" reprovada** ("No or a lower discount found": o desconto não é aplicado no checkout). As outras 6 estão paradas, com IDs de teste (123456, 10PIX, PIX10, PIX10OFF, PIX_0FF e 83257). | Shopify (criar o desconto) e limpar as antigas |
| 7 | Médio | **Anúncios locais grátis ligados só na fonte nova** (destino FREE_LOCAL_LISTINGS ativo no "Shopify App API" e desligado no Simprosys). É a causa dos 1.081 avisos de estoque local. | Configuração da fonte de dados (Merchant Center) |
| 8 | Baixo | **Acesso de administrador:** 3 contas são ADMIN (tenezproshop@gmail.com, alfinet@alfinet.com.br e a conta de serviço usada pela API). Há 3 acessos de terceiros (fluxismarketing, integracoes@alfinet, henrique@aceleradora3m). Convém conferir se todos ainda precisam. | Merchant Center |
| 9 | Baixo | **Melhorias automáticas todas ligadas:** o Google pode ajustar preço, disponibilidade, condição, imagens e frete sozinho. Isso pode mascarar divergências entre o site e o feed. | Merchant Center |
| 10 | Informativo | Programa de fidelidade "elegível" (não ativo); avaliações de produto "não elegível"; checkout do YouTube "elegível". | Informativo |

## O que não consegui verificar
- **Preferências de e-mail de notificação** (o endpoint não responde) e **notificações por API** (nenhuma assinatura criada).
- **Avaliações de produto** (a API não está habilitada neste projeto) e avaliações da loja.
- **Vínculo com o Search Console** (a API não expõe).
- **Páginas do site** (links de checkout, política de devolução, domínio `loja.tenez.com.br`): sem acesso a partir deste ambiente.
- **Frete e devolução reais cobrados no checkout da Shopify**: li só o perfil (Frenet, sem valores).
