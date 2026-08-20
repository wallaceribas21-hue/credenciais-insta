"""
api.py — Detecta qual fluxo da Meta o seu token usa e configura o resto.

Existem DOIS jeitos de publicar no Instagram, com tokens diferentes:

  1. Instagram API com Instagram Login   -> token comeca com "IGAA"
     Servidor: graph.instagram.com
     Nao precisa de Pagina do Facebook. Mais simples.

  2. Instagram API com Facebook Login    -> token comeca com "EAA"
     Servidor: graph.facebook.com
     Precisa de Pagina do Facebook vinculada.

Os dois publicam carrossel do mesmo jeito. Este modulo esconde a diferenca
para os outros scripts nao precisarem se importar.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

FLUXO_INSTAGRAM = "instagram"
FLUXO_FACEBOOK = "facebook"

# Erros comuns da Meta, traduzidos.
DIAGNOSTICO = {
    190: "Token invalido ou expirado. Gere um novo.",
    102: "Sessao expirou. Gere um token novo.",
    200: "Faltam permissoes. Confira as permissoes de publicacao do seu app.",
    100: "Parametro invalido. Confira se o INSTAGRAM_BUSINESS_ID esta correto.",
    803: "Conta nao encontrada. Confirme que o Instagram e Business ou Creator.",
    9007: "Limite de publicacoes atingido (25 posts por 24h). Espere e tente de novo.",
}


def carregar_env():
    """Procura o .env subindo a partir da pasta do script."""
    atual = Path(__file__).resolve().parent
    for pasta in [atual, *atual.parents]:
        candidato = pasta / ".env"
        if candidato.is_file():
            load_dotenv(candidato)
            return candidato
    return None


def detectar_fluxo(token):
    """Descobre o fluxo pelo prefixo do token."""
    if not token:
        return None
    if token.startswith("IGAA"):
        return FLUXO_INSTAGRAM
    if token.startswith("EAA"):
        return FLUXO_FACEBOOK
    return None


def base_url(fluxo):
    """Servidor e versao da API para cada fluxo."""
    if fluxo == FLUXO_INSTAGRAM:
        versao = os.getenv("META_API_VERSION", "v23.0")
        return f"https://graph.instagram.com/{versao}"
    versao = os.getenv("META_API_VERSION", "v19.0")
    return f"https://graph.facebook.com/{versao}"


def nome_fluxo(fluxo):
    if fluxo == FLUXO_INSTAGRAM:
        return "Instagram Login (graph.instagram.com)"
    if fluxo == FLUXO_FACEBOOK:
        return "Facebook Login (graph.facebook.com)"
    return "desconhecido"


def explicar_erro(dados):
    """Transforma o erro da Meta em algo legivel, com dica quando houver."""
    erro = dados.get("error", {})
    msg = erro.get("message", "erro desconhecido")
    dica = DIAGNOSTICO.get(erro.get("code"))
    return msg + (f"\n     -> {dica}" if dica else "")


def carregar_credenciais():
    """Retorna (env_path, token, ig_id, fluxo, base). Nao valida nada online."""
    env_path = carregar_env()
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_id = os.getenv("INSTAGRAM_BUSINESS_ID")
    fluxo = detectar_fluxo(token)
    return env_path, token, ig_id, fluxo, base_url(fluxo)
