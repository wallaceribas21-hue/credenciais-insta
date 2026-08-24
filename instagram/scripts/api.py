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


# ---------------------------------------------------------------------------
# Validade do token
#
# A Meta nao avisa que o token vai vencer. Ela so para de aceitar, no meio de
# uma publicacao, com um erro que nao parece ser sobre isso. Entao guardamos a
# data de vencimento no .env e avisamos antes, enquanto renovar ainda e uma
# chamada so.
# ---------------------------------------------------------------------------

AVISAR_A_PARTIR_DE = 15  # dias


def dias_restantes():
    """Dias ate o token vencer, ou None se a data nao estiver registrada."""
    from datetime import date

    bruto = os.getenv("INSTAGRAM_TOKEN_EXPIRA_EM", "").strip()
    if not bruto:
        return None
    try:
        return (date.fromisoformat(bruto) - date.today()).days
    except ValueError:
        return None


def dias_restantes_texto():
    dias = dias_restantes()
    if dias is None:
        return "validade desconhecida (renove uma vez para comecar a contar)"
    if dias < 0:
        return f"VENCIDO ha {-dias} dias"
    return f"{dias} dias restantes"


def avisar_validade():
    """Imprime um aviso so quando falta pouco. Aviso que aparece sempre vira
    paisagem e para de ser lido."""
    dias = dias_restantes()
    if dias is None or dias > AVISAR_A_PARTIR_DE:
        return
    if dias < 0:
        print(f"\n  !! TOKEN VENCIDO ha {-dias} dias. Gere um novo: instagram/README.md\n")
    else:
        print(f"\n  !! O token vence em {dias} dias. Renove agora, leva 5 segundos:")
        print("     python instagram/scripts/renovar_token.py\n")
