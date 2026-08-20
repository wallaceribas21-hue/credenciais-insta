"""
publish_instagram.py — Publicacao de carrossel no Instagram via Meta Graph API.

Uso:
    python publish_instagram.py --images slides/*.png --caption "sua legenda"
    python publish_instagram.py --images a.png b.png --caption "teste" --dry-run

Requer um .env com INSTAGRAM_BUSINESS_ID e INSTAGRAM_ACCESS_TOKEN.
Veja o .env.example na pasta instagram/.
"""
import argparse
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


def carregar_env():
    """Procura o .env subindo a partir da pasta do script."""
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

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def hospedar_imagem(caminho):
    """A API do Instagram so aceita URL publica, entao subimos a imagem primeiro.

    ATENCAO: catbox.moe e um host publico e anonimo. A imagem fica acessivel
    por link para qualquer pessoa que tenha a URL. Nao use com material sigiloso.
    """
    arquivo = Path(caminho)
    if not arquivo.is_file():
        raise FileNotFoundError(f"Imagem nao encontrada: {caminho}")

    tipo = MIME.get(arquivo.suffix.lower())
    if tipo is None:
        raise ValueError(f"Formato nao suportado: {arquivo.suffix} (use .png ou .jpg)")

    with arquivo.open("rb") as f:
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload"},
            files={"fileToUpload": (arquivo.name, f, tipo)},
            timeout=120,
        )
    url = resp.text.strip()
    if not url.startswith("https://"):
        raise RuntimeError(f"Falha ao hospedar {arquivo.name}: {url}")
    print(f"    hospedada: {url}")
    return url


def criar_container(caminho):
    resp = requests.post(
        f"{BASE_URL}/{IG_ID}/media",
        data={
            "access_token": TOKEN,
            "image_url": hospedar_imagem(caminho),
            "is_carousel_item": "true",
        },
        timeout=60,
    )
    dados = resp.json()
    if "id" not in dados:
        raise RuntimeError(f"Erro ao criar container: {dados}")
    print(f"    container: {dados['id']}")
    return dados["id"]


def criar_carrossel(ids, legenda):
    resp = requests.post(
        f"{BASE_URL}/{IG_ID}/media",
        data={
            "access_token": TOKEN,
            "media_type": "CAROUSEL",
            "children": ",".join(ids),
            "caption": legenda,
        },
        timeout=60,
    )
    dados = resp.json()
    if "id" not in dados:
        raise RuntimeError(f"Erro ao montar carrossel: {dados}")
    print(f"    carrossel: {dados['id']}")
    return dados["id"]


def esperar_processar(container_id, tentativas=12, intervalo=5):
    for i in range(tentativas):
        resp = requests.get(
            f"{BASE_URL}/{container_id}",
            params={"fields": "status_code,status", "access_token": TOKEN},
            timeout=30,
        )
        dados = resp.json()
        status = dados.get("status_code", "")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"Meta retornou erro no processamento: {dados}")
        print(f"    processando... {i * intervalo}s")
        time.sleep(intervalo)
    raise TimeoutError(
        f"Container nao ficou pronto em {tentativas * intervalo}s. Tente publicar de novo."
    )


def publicar(container_id):
    resp = requests.post(
        f"{BASE_URL}/{IG_ID}/media_publish",
        data={"access_token": TOKEN, "creation_id": container_id},
        timeout=60,
    )
    dados = resp.json()
    if "id" not in dados:
        raise RuntimeError(f"Erro ao publicar: {dados}")
    return dados["id"]


def run(imagens, legenda, dry_run=False):
    if not IG_ID or not TOKEN:
        origem = ENV_PATH or "nenhum .env encontrado"
        print(f"ERRO: credenciais ausentes ({origem}).")
        print("Preencha INSTAGRAM_BUSINESS_ID e INSTAGRAM_ACCESS_TOKEN no .env.")
        sys.exit(1)
    if not 2 <= len(imagens) <= 10:
        print(f"ERRO: carrossel precisa de 2 a 10 imagens (recebi {len(imagens)}).")
        sys.exit(1)

    faltando = [i for i in imagens if not Path(i).is_file()]
    if faltando:
        print("ERRO: imagens nao encontradas:")
        for i in faltando:
            print(f"  - {i}")
        sys.exit(1)

    print(f"\nPublicando {len(imagens)} slides no Instagram (conta {IG_ID})")
    if dry_run:
        print("[DRY RUN] Credenciais e imagens OK. Remova --dry-run para publicar de verdade.")
        return

    try:
        print("\nPasso 1/3 - enviando imagens")
        ids = [criar_container(img) for img in imagens]

        print("\nPasso 2/3 - montando carrossel")
        carrossel_id = criar_carrossel(ids, legenda)

        print("\nPasso 3/3 - publicando")
        esperar_processar(carrossel_id)
        post_id = publicar(carrossel_id)
    except (RuntimeError, TimeoutError, FileNotFoundError, ValueError) as e:
        print(f"\nFALHOU: {e}")
        sys.exit(1)

    print(f"\nPublicado! Post ID: {post_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publica um carrossel no Instagram.")
    parser.add_argument("--images", nargs="+", required=True, help="2 a 10 imagens .png/.jpg")
    parser.add_argument("--caption", required=True, help="legenda do post")
    parser.add_argument("--dry-run", action="store_true", help="valida sem publicar")
    args = parser.parse_args()
    run(args.images, args.caption, args.dry_run)
