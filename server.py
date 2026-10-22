#!/usr/bin/env python3
"""Servidor MCP (conector do claude.ai) com os comandos de consulta e simulação do mc.py.

Nunca envia alterações ao Google: as ferramentas de desconto só simulam. Para aplicar,
use o mc.py com --aplicar (o undo depende da pasta dados/, que não persiste no Cloud Run).

O endereço do conector é https://SEU-SERVICO/<MCP_TOKEN>/mcp — sem o token certo, 404.
"""
import contextlib
import io
import os
import sys
import threading

import uvicorn
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from mc import build_parser

MAX_CHARS = 60_000
_lock = threading.Lock()  # os comandos imprimem em stdout; um por vez

server = MCPServer(
    name="merchant-center",
    title="Merchant Center (Tenez)",
    instructions="Consulta e relatórios do Google Merchant Center da Tenez. "
                 "As ferramentas de desconto só simulam; nada é enviado ao Google.",
)


def run(*argv):
    """Executa um comando do mc.py e devolve o que ele imprimiria no terminal."""
    argv = [str(a) for a in argv]
    if "--aplicar" in argv:
        return "Este conector não aplica alterações; use o mc.py com --aplicar."
    out = io.StringIO()
    with _lock, contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            args = build_parser().parse_args(argv)
            args.func(args)
        except SystemExit as e:  # call() e o argparse encerram com sys.exit(mensagem)
            if e.code not in (None, 0):
                print(e.code)
    text = out.getvalue().strip() or "(sem saída)"
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + f"\n\n... saída cortada ({len(text)} caracteres no total)"
    return text


def opt(flag, value):
    return [flag, value] if value not in (None, "") else []


def filters(busca, marca, tipo, em_estoque):
    return opt("--busca", busca) + opt("--marca", marca) + opt("--tipo", tipo) + (["--em-estoque"] if em_estoque else [])


# Consulta

@server.tool()
def listar_produtos(limite: int = 25, page_token: str | None = None) -> str:
    """Lista produtos: ID, preço e título. Use page_token para a próxima página."""
    return run("list", "--limit", limite, *opt("--page-token", page_token))


@server.tool()
def detalhar_produto(product_id: str) -> str:
    """JSON completo de um produto. product_id no formato idioma~feedLabel~offerId."""
    return run("get", product_id)


@server.tool()
def buscar_produtos(termo: str, limite: int = 50) -> str:
    """Busca produtos pelo título (preço, disponibilidade e status)."""
    return run("search", termo, "--limit", limite)


@server.tool()
def fontes_de_dados() -> str:
    """Lista as fontes de dados (feeds) da conta."""
    return run("datasources")


# Saúde e relatórios

@server.tool()
def saude_catalogo() -> str:
    """Aprovados/reprovados por destino, problemas mais comuns e seus motivos."""
    return run("health")


@server.tool()
def desempenho(dias: int = 30, min_cliques: int = 20) -> str:
    """Impressões, cliques e vendas por produto; quem não aparece e quem tem cliques sem venda."""
    return run("performance", "--dias", dias, "--min-cliques", min_cliques)


@server.tool()
def precos_vs_mercado(margem: float = 5) -> str:
    """Seu preço comparado ao preço de referência do mercado (margem em % = 'na média')."""
    return run("prices", "--margem", margem)


@server.tool()
def sugestoes_de_preco() -> str:
    """Preços sugeridos pelo Google e o impacto previsto em cliques e vendas."""
    return run("price-insights")


@server.tool()
def mais_vendidos(categoria: str = "988", sub: str | None = None, limite: int = 200, mostrar: int = 30) -> str:
    """Mais vendidos no Brasil e se a loja tem cada um. categoria: 988 = Artigos esportivos,
    166 = Roupas e acessórios. sub: trecho da subcategoria em inglês (Tennis, Shoes, Shorts)."""
    return run("bestsellers", "--categoria", categoria, *opt("--sub", sub), "--limite", limite, "--mostrar", mostrar)


@server.tool()
def listar_promocoes() -> str:
    """Lista as promoções cadastradas no Google."""
    return run("promo-list")


@server.tool()
def lotes_enviados() -> str:
    """Lotes de alterações enviados por este servidor (o histórico do computador não aparece aqui)."""
    return run("batches")


# Simulações (nunca enviam)

@server.tool()
def simular_desconto(desconto: float, busca: str | None = None, marca: str | None = None,
                     tipo: str | None = None, em_estoque: bool = False, inicio: str | None = None,
                     fim: str | None = None, todos: bool = False) -> str:
    """Simula um preço promocional de X% nos produtos filtrados (busca no título, marca exata,
    trecho do tipo). Datas AAAA-MM-DD. Exige um filtro ou todos=true. Não envia nada."""
    return run("discount", "--desconto", desconto, *filters(busca, marca, tipo, em_estoque),
               *opt("--inicio", inicio), *opt("--fim", fim), *(["--todos"] if todos else []))


@server.tool()
def simular_fim_desconto(busca: str | None = None, marca: str | None = None, tipo: str | None = None,
                         em_estoque: bool = False, todos: bool = False) -> str:
    """Simula a remoção do preço promocional gravado nos produtos filtrados. Não envia nada."""
    return run("end-discount", *filters(busca, marca, tipo, em_estoque), *(["--todos"] if todos else []))


def main():
    token = os.getenv("MCP_TOKEN", "")
    if len(token) < 32:
        sys.exit("Defina MCP_TOKEN com pelo menos 32 caracteres (ex.: openssl rand -hex 24)")
    app = server.streamable_http_app(
        streamable_http_path=f"/{token}/mcp",
        stateless_http=True,
        # Cloud Run fica atrás de um proxy com domínio próprio; o token no caminho faz a proteção.
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))


if __name__ == "__main__":
    main()
