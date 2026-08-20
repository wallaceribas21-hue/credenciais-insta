"""
verificar_conexao.py — Testa se as credenciais do Instagram estao funcionando.

Uso:
    python verificar_conexao.py

Roda isso ANTES de tentar publicar. Se passar nos 3 testes, esta tudo pronto.
"""
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


def carregar_env():
    atual = Path(__file__).resolve().parent
    for pasta in [atual, *atual.parents]:
        candidato = pasta / ".env"
        if candidato.is_file():
            load_dotenv(candidato)
            return candidato
    return None


ENV_PATH = carregar_env()
IG_ID = os.getenv("INSTAGRAM_BUSINESS_ID")
TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
BASE_URL = f"https://graph.facebook.com/{os.getenv('META_API_VERSION', 'v19.0')}"

# Erros comuns da Meta traduzidos para portugues.
DIAGNOSTICO = {
    190: "Token invalido ou expirado. Gere um novo no Graph API Explorer.",
    200: "Faltam permissoes. Adicione instagram_basic, instagram_content_publish e pages_read_engagement.",
    100: "Parametro invalido. Confira se o INSTAGRAM_BUSINESS_ID esta correto.",
    803: "Conta nao encontrada. Confirme que o Instagram e Business/Creator e esta vinculado a Pagina.",
}


def explicar(dados):
    erro = dados.get("error", {})
    codigo = erro.get("code")
    msg = erro.get("message", "erro desconhecido")
    dica = DIAGNOSTICO.get(codigo)
    return f"{msg}" + (f"\n     -> {dica}" if dica else "")


def main():
    print("\n=== Verificando conexao com o Instagram ===\n")

    print("[1/3] Credenciais no .env")
    if not ENV_PATH:
        print("  FALHOU: nenhum .env encontrado.")
        print("  Copie instagram/.env.example para instagram/.env e preencha.")
        sys.exit(1)
    if not IG_ID or not TOKEN:
        print(f"  FALHOU: .env encontrado em {ENV_PATH}, mas faltam valores.")
        print("  Preencha INSTAGRAM_BUSINESS_ID e INSTAGRAM_ACCESS_TOKEN.")
        sys.exit(1)
    print(f"  OK  ({ENV_PATH})")

    print("\n[2/3] Token valido")
    try:
        resp = requests.get(
            f"{BASE_URL}/me",
            params={"fields": "id,name", "access_token": TOKEN},
            timeout=30,
        )
    except requests.RequestException as e:
        print(f"  FALHOU: sem acesso a graph.facebook.com ({e})")
        sys.exit(1)
    dados = resp.json()
    if "error" in dados:
        print(f"  FALHOU: {explicar(dados)}")
        sys.exit(1)
    print(f"  OK  (autenticado como: {dados.get('name', dados.get('id'))})")

    print("\n[3/3] Conta do Instagram acessivel")
    resp = requests.get(
        f"{BASE_URL}/{IG_ID}",
        params={"fields": "id,username,name,followers_count", "access_token": TOKEN},
        timeout=30,
    )
    dados = resp.json()
    if "error" in dados:
        print(f"  FALHOU: {explicar(dados)}")
        sys.exit(1)

    print(f"  OK")
    print("\n--- Tudo certo! ---")
    print(f"  Conta:     @{dados.get('username', '?')}")
    print(f"  Nome:      {dados.get('name', '?')}")
    print(f"  ID:        {dados.get('id')}")
    if "followers_count" in dados:
        print(f"  Seguidores: {dados['followers_count']}")
    print("\nJa pode publicar com publish_instagram.py\n")


if __name__ == "__main__":
    main()
