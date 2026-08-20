"""
descobrir_id.py — Descobre o ID da sua conta do Instagram e escreve o .env.

Uso:
    python descobrir_id.py

Aceita os dois tipos de token:
  - IGAA... (Instagram Login)  -> pega o ID direto, sem Pagina do Facebook
  - EAA...  (Facebook Login)   -> lista suas Paginas e acha o Instagram de cada

O token e pedido de forma oculta: nao aparece na tela e nao fica no
historico do terminal.
"""
import sys
from getpass import getpass
from pathlib import Path

import requests

import api

# Página do Facebook onde está a @wallaceribas_ (só usada no fluxo Facebook).
PAGINA_PADRAO = "512007262005431"


def checar_erro(dados, contexto):
    if "error" in dados:
        print(f"\nFALHOU em {contexto}: {api.explicar_erro(dados)}")
        sys.exit(1)


def via_instagram_login(token, base):
    """Fluxo IGAA: o /me ja devolve o ID e o username."""
    print("\nConsultando sua conta...")
    resp = requests.get(
        f"{base}/me",
        params={"fields": "user_id,username,account_type", "access_token": token},
        timeout=30,
    )
    dados = resp.json()
    checar_erro(dados, "consultar a conta")

    # Dependendo do app, o ID vem em "user_id" ou em "id".
    ig_id = dados.get("user_id") or dados.get("id")
    username = dados.get("username", "?")
    tipo = dados.get("account_type", "?")

    if not ig_id:
        print(f"\nFALHOU: a Meta nao devolveu o ID da conta. Resposta: {dados}")
        sys.exit(1)

    print(f"\n  Conta:  @{username}")
    print(f"  Tipo:   {tipo}")
    print(f"  ID:     {ig_id}")

    if tipo not in ("BUSINESS", "MEDIA_CREATOR", "CREATOR", "?"):
        print(f"\n  AVISO: tipo '{tipo}' pode nao permitir publicacao.")
        print("  Converta para Business ou Creator em Configuracoes → Conta.")

    return str(ig_id), ""


def via_facebook_login(token, base):
    """Fluxo EAA: lista as Paginas e procura o Instagram vinculado a cada uma."""
    print("\nProcurando suas Paginas...")
    resp = requests.get(
        f"{base}/me/accounts",
        params={
            "fields": "id,name,instagram_business_account",
            "limit": 100,
            "access_token": token,
        },
        timeout=60,
    )
    dados = resp.json()
    checar_erro(dados, "listar Paginas")

    paginas = dados.get("data", [])
    if not paginas:
        print("\nNenhuma Pagina encontrada.")
        print("  -> No Graph API Explorer, selecione a Pagina (nao 'Usuario').")
        sys.exit(1)

    com_ig = [p for p in paginas if p.get("instagram_business_account")]
    print(f"  {len(paginas)} Paginas, {len(com_ig)} com Instagram vinculado.\n")

    if not com_ig:
        print("Nenhuma Pagina tem Instagram vinculado.")
        print("  -> Instagram → Configuracoes → Conta → Pagina vinculada")
        sys.exit(1)

    opcoes = []
    for pagina in com_ig:
        ig_id = pagina["instagram_business_account"]["id"]
        resp = requests.get(
            f"{base}/{ig_id}",
            params={"fields": "username", "access_token": token},
            timeout=30,
        )
        username = resp.json().get("username")
        opcoes.append((pagina, ig_id, username))
        marca = "  <- Pagina WR 03- Wallace" if pagina["id"] == PAGINA_PADRAO else ""
        arroba = f"@{username}" if username else "(username indisponivel)"
        print(f"  [{len(opcoes)}] {arroba:<26} Pagina: {pagina['name']}{marca}")

    if len(opcoes) == 1:
        escolha = 0
        print("\nSo tem uma conta. Usando ela.")
    else:
        bruto = input(f"\nQual usar? (1-{len(opcoes)}) ").strip()
        if not bruto.isdigit() or not 1 <= int(bruto) <= len(opcoes):
            print("Opcao invalida.")
            sys.exit(1)
        escolha = int(bruto) - 1

    pagina, ig_id, username = opcoes[escolha]
    print(f"\nEscolhida: @{username or '?'} (Pagina {pagina['name']})")
    return str(ig_id), pagina["id"]


def escrever_env(destino, ig_id, page_id, token):
    if destino.exists():
        if input(f"\n{destino} ja existe. Sobrescrever? (s/n) ").strip().lower() != "s":
            print("\nOk, nao mexi no arquivo. Valores para colar manualmente:")
            print(f"  INSTAGRAM_BUSINESS_ID={ig_id}")
            if page_id:
                print(f"  FACEBOOK_PAGE_ID={page_id}")
            return

    linhas = [
        "# Instagram / Meta — gerado por descobrir_id.py",
        f"INSTAGRAM_BUSINESS_ID={ig_id}",
        f"INSTAGRAM_ACCESS_TOKEN={token}",
    ]
    if page_id:
        linhas.insert(2, f"FACEBOOK_PAGE_ID={page_id}")
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    try:
        destino.chmod(0o600)  # so o dono le/escreve
    except OSError:
        pass
    print(f"\n.env escrito em: {destino}")


def main():
    print("\n=== Descobrir o ID do Instagram ===\n")
    print("Cole o token (nao vai aparecer na tela).")
    token = getpass("Token: ").strip()

    if not token:
        print("\nNenhum token informado.")
        sys.exit(1)

    fluxo = api.detectar_fluxo(token)
    if fluxo is None:
        print("\nNao reconheci esse token.")
        print("  Tokens da Meta comecam com 'IGAA' (Instagram Login)")
        print("  ou 'EAA' (Facebook Login). Confira se copiou inteiro.")
        sys.exit(1)

    base = api.base_url(fluxo)
    print(f"\nFluxo detectado: {api.nome_fluxo(fluxo)}")

    if fluxo == api.FLUXO_INSTAGRAM:
        ig_id, page_id = via_instagram_login(token, base)
    else:
        ig_id, page_id = via_facebook_login(token, base)

    escrever_env(Path(__file__).resolve().parent.parent / ".env", ig_id, page_id, token)

    print("\nProximo passo:")
    print("  python instagram/scripts/verificar_conexao.py\n")


if __name__ == "__main__":
    main()
