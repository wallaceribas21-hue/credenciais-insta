"""
renovar_token.py — Estica a validade do token por mais ~60 dias.

Uso:
    python instagram/scripts/renovar_token.py

O token da Meta dura cerca de 60 dias. Enquanto ele ainda esta VALIDO, uma
chamada renova por mais 60. Se deixar expirar, nao da para renovar: tem que
refazer o caminho inteiro no site da Meta.

Por isso este script existe: renovar e barato, expirar e caro.
Pode rodar quantas vezes quiser, sempre reinicia a contagem.
"""
import sys
from datetime import date, timedelta

import requests

import api

ENV_PATH, TOKEN, IG_ID, FLUXO, BASE_URL = api.carregar_credenciais()


def renovar_instagram(token):
    """Caminho A (IGAA). Nao precisa de app id nem secret."""
    resp = requests.get(
        "https://graph.instagram.com/refresh_access_token",
        params={"grant_type": "ig_refresh_token", "access_token": token},
        timeout=30,
    )
    return resp.json()


def renovar_facebook(token):
    """Caminho B (EAA). Precisa de META_APP_ID e META_APP_SECRET no .env."""
    import os

    app_id = os.getenv("META_APP_ID")
    segredo = os.getenv("META_APP_SECRET")
    if not app_id or not segredo:
        print("ERRO: o caminho Facebook precisa de META_APP_ID e META_APP_SECRET no .env.")
        print("      Pegue em developers.facebook.com -> seu App -> Configuracoes -> Basico.")
        sys.exit(1)
    resp = requests.get(
        f"{BASE_URL}/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": segredo,
            "fb_exchange_token": token,
        },
        timeout=30,
    )
    return resp.json()


def gravar_no_env(caminho, token_novo, vence_em):
    """Reescreve so as duas linhas que mudam, preservando o resto do arquivo.

    Grava em memoria e so entao substitui: se algo falhar no meio, o .env
    antigo continua inteiro. Perder o .env custa mais que nao renovar.
    """
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    saida, achou_token, achou_data = [], False, False
    for linha in linhas:
        if linha.startswith("INSTAGRAM_ACCESS_TOKEN="):
            saida.append(f"INSTAGRAM_ACCESS_TOKEN={token_novo}")
            achou_token = True
        elif linha.startswith("INSTAGRAM_TOKEN_EXPIRA_EM="):
            saida.append(f"INSTAGRAM_TOKEN_EXPIRA_EM={vence_em}")
            achou_data = True
        else:
            saida.append(linha)
    if not achou_token:
        saida.append(f"INSTAGRAM_ACCESS_TOKEN={token_novo}")
    if not achou_data:
        saida.append(f"INSTAGRAM_TOKEN_EXPIRA_EM={vence_em}")
    caminho.write_text("\n".join(saida) + "\n", encoding="utf-8")


def main():
    print("\n=== Renovando o token do Instagram ===\n")

    if not ENV_PATH or not TOKEN:
        print("ERRO: nao achei o token no .env.")
        print("      Rode: python instagram/scripts/descobrir_id.py")
        sys.exit(1)
    if FLUXO is None:
        print("ERRO: token nao reconhecido (deveria comecar com IGAA ou EAA).")
        sys.exit(1)

    print(f"Fluxo: {api.nome_fluxo(FLUXO)}")
    print(f"Antes: {api.dias_restantes_texto()}\n")

    if FLUXO == api.FLUXO_INSTAGRAM:
        dados = renovar_instagram(TOKEN)
    else:
        dados = renovar_facebook(TOKEN)

    if "error" in dados:
        print(f"FALHOU: {api.explicar_erro(dados)}")
        print("\nSe o token ja expirou, nao da para renovar. Gere um novo:")
        print("  instagram/README.md -> Passo 3")
        sys.exit(1)

    token_novo = dados.get("access_token")
    if not token_novo:
        print(f"FALHOU: a Meta respondeu sem token novo: {dados}")
        sys.exit(1)

    segundos = int(dados.get("expires_in", 60 * 24 * 3600))
    vence_em = (date.today() + timedelta(seconds=segundos)).isoformat()
    gravar_no_env(ENV_PATH, token_novo, vence_em)

    print("--- Renovado! ---")
    print(f"  Validade nova: {segundos // 86400} dias (ate {vence_em})")
    print(f"  Gravado em:    {ENV_PATH}")
    print("\nNao precisa copiar nada. O .env ja esta atualizado.\n")


if __name__ == "__main__":
    main()
