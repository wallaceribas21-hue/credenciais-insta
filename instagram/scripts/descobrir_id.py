"""
descobrir_id.py — Descobre o INSTAGRAM_BUSINESS_ID e ja escreve o .env.

Uso:
    python descobrir_id.py

Ele pede o token, procura suas Paginas do Facebook, identifica quais tem
Instagram vinculado, mostra os @usuarios e escreve o .env pra voce.

O token e pedido de forma oculta: nao aparece na tela e nao fica no
historico do terminal.
"""
import sys
from getpass import getpass
from pathlib import Path

import requests

API = "https://graph.facebook.com/v19.0"

# Página do Facebook onde está a @wallaceribas_ (descoberta pelo conector da Meta).
PAGINA_PADRAO = "512007262005431"

DIAGNOSTICO = {
    190: "Token invalido ou expirado. Gere um novo no Graph API Explorer.",
    200: "Faltam permissoes. Adicione instagram_basic, instagram_content_publish e pages_read_engagement.",
    102: "Sessao expirou. Gere um token novo.",
}


def checar_erro(dados, contexto):
    if "error" not in dados:
        return
    erro = dados["error"]
    print(f"\nFALHOU em {contexto}: {erro.get('message', 'erro desconhecido')}")
    dica = DIAGNOSTICO.get(erro.get("code"))
    if dica:
        print(f"  -> {dica}")
    sys.exit(1)


def buscar_paginas(token):
    resp = requests.get(
        f"{API}/me/accounts",
        params={
            "fields": "id,name,instagram_business_account",
            "limit": 100,
            "access_token": token,
        },
        timeout=60,
    )
    dados = resp.json()
    checar_erro(dados, "listar Paginas")
    return dados.get("data", [])


def buscar_username(ig_id, token):
    resp = requests.get(
        f"{API}/{ig_id}",
        params={"fields": "username,name", "access_token": token},
        timeout=30,
    )
    dados = resp.json()
    if "error" in dados:
        return None
    return dados.get("username")


def escrever_env(destino, ig_id, page_id, token):
    if destino.exists():
        resposta = input(f"\n{destino} ja existe. Sobrescrever? (s/n) ").strip().lower()
        if resposta != "s":
            print("\nOk, nao mexi no arquivo. Valores para colar manualmente:")
            print(f"  INSTAGRAM_BUSINESS_ID={ig_id}")
            print(f"  FACEBOOK_PAGE_ID={page_id}")
            return

    destino.write_text(
        "# Instagram / Meta — gerado por descobrir_id.py\n"
        f"INSTAGRAM_BUSINESS_ID={ig_id}\n"
        f"FACEBOOK_PAGE_ID={page_id}\n"
        f"INSTAGRAM_ACCESS_TOKEN={token}\n"
        "META_API_VERSION=v19.0\n",
        encoding="utf-8",
    )
    try:
        destino.chmod(0o600)  # so o dono le/escreve
    except OSError:
        pass
    print(f"\n.env escrito em: {destino}")


def main():
    print("\n=== Descobrir o ID do Instagram ===\n")
    print("Cole o token do Graph API Explorer (nao vai aparecer na tela).")
    token = getpass("Token: ").strip()

    if not token:
        print("\nNenhum token informado.")
        sys.exit(1)
    if not token.startswith("EAA"):
        print("\nAviso: tokens da Meta costumam comecar com 'EAA'. Vou tentar assim mesmo.\n")

    print("\nProcurando suas Paginas...")
    paginas = buscar_paginas(token)
    if not paginas:
        print("\nNenhuma Pagina encontrada.")
        print("  -> No Graph API Explorer, selecione a Pagina (nao 'Usuario') antes de gerar o token.")
        sys.exit(1)

    com_ig = [p for p in paginas if p.get("instagram_business_account")]
    print(f"  {len(paginas)} Paginas encontradas, {len(com_ig)} com Instagram vinculado.\n")

    if not com_ig:
        print("Nenhuma Pagina tem Instagram vinculado.")
        print("  -> Instagram → Configuracoes → Conta → Pagina vinculada")
        print("  -> A conta tambem precisa ser Business ou Creator.")
        sys.exit(1)

    print("Contas disponiveis:\n")
    opcoes = []
    for pagina in com_ig:
        ig_id = pagina["instagram_business_account"]["id"]
        username = buscar_username(ig_id, token)
        opcoes.append((pagina, ig_id, username))
        marca = "  <- Pagina WR 03- Wallace" if pagina["id"] == PAGINA_PADRAO else ""
        arroba = f"@{username}" if username else "(username indisponivel)"
        print(f"  [{len(opcoes)}] {arroba:<28} Pagina: {pagina['name']}{marca}")
        print(f"      INSTAGRAM_BUSINESS_ID={ig_id}")

    if len(opcoes) == 1:
        escolha = 0
        print(f"\nSo tem uma conta. Usando ela.")
    else:
        bruto = input(f"\nQual usar? (1-{len(opcoes)}) ").strip()
        if not bruto.isdigit() or not 1 <= int(bruto) <= len(opcoes):
            print("Opcao invalida.")
            sys.exit(1)
        escolha = int(bruto) - 1

    pagina, ig_id, username = opcoes[escolha]
    print(f"\nEscolhida: @{username or '?'} (Pagina {pagina['name']})")

    destino = Path(__file__).resolve().parent.parent / ".env"
    escrever_env(destino, ig_id, pagina["id"], token)

    print("\nProximo passo:")
    print("  python instagram/scripts/verificar_conexao.py\n")


if __name__ == "__main__":
    main()
