"""
verificar_conexao.py — Testa se as credenciais do Instagram estao funcionando.

Uso:
    python verificar_conexao.py

Roda isso ANTES de tentar publicar. Se passar nos 3 testes, esta tudo pronto.
Funciona com os dois fluxos (token IGAA... ou EAA...).
"""
import sys

import requests

import api

ENV_PATH, TOKEN, IG_ID, FLUXO, BASE_URL = api.carregar_credenciais()


def main():
    print("\n=== Verificando conexao com o Instagram ===\n")

    print("[1/3] Credenciais no .env")
    if not ENV_PATH:
        print("  FALHOU: nenhum .env encontrado.")
        print("  Rode: python instagram/scripts/descobrir_id.py")
        sys.exit(1)
    if not IG_ID or not TOKEN:
        print(f"  FALHOU: .env encontrado em {ENV_PATH}, mas faltam valores.")
        print("  Rode: python instagram/scripts/descobrir_id.py")
        sys.exit(1)
    if FLUXO is None:
        print("  FALHOU: token nao reconhecido (deveria comecar com IGAA ou EAA).")
        sys.exit(1)
    print(f"  OK  ({ENV_PATH})")
    print(f"      fluxo: {api.nome_fluxo(FLUXO)}")

    print("\n[2/3] Token valido")
    try:
        resp = requests.get(
            f"{BASE_URL}/me",
            params={"fields": "id,username", "access_token": TOKEN},
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"  FALHOU: sem acesso a API da Meta ({e})")
        sys.exit(1)
    dados = resp.json()
    if "error" in dados:
        print(f"  FALHOU: {api.explicar_erro(dados)}")
        sys.exit(1)
    print("  OK")

    print("\n[3/3] Conta acessivel e pronta para publicar")
    campos = "id,username,account_type" if FLUXO == api.FLUXO_INSTAGRAM else "id,username,name"
    resp = requests.get(
        f"{BASE_URL}/{IG_ID}",
        params={"fields": campos, "access_token": TOKEN},
        timeout=30,
    )
    dados = resp.json()
    if "error" in dados:
        print(f"  FALHOU: {api.explicar_erro(dados)}")
        sys.exit(1)
    print("  OK")

    print("\n--- Tudo certo! ---")
    print(f"  Conta:  @{dados.get('username', '?')}")
    if dados.get("name"):
        print(f"  Nome:   {dados['name']}")
    if dados.get("account_type"):
        print(f"  Tipo:   {dados['account_type']}")
    print(f"  ID:     {dados.get('id', IG_ID)}")
    print("\nJa pode publicar:")
    print('  python instagram/scripts/publish_instagram.py --images slides/*.png --caption "sua legenda"\n')


if __name__ == "__main__":
    main()
