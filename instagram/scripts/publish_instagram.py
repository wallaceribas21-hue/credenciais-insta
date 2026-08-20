"""
publish_instagram.py — Publicacao de carrossel no Instagram.

Uso:
    python publish_instagram.py --images slides/*.png --caption "sua legenda"
    python publish_instagram.py --images a.png b.png --caption "teste" --dry-run

Funciona com os dois fluxos (token IGAA... ou EAA...).
Rode antes: python descobrir_id.py
"""
import argparse
import glob
import sys
import time
from pathlib import Path

import requests

import api

ENV_PATH, TOKEN, IG_ID, FLUXO, BASE_URL = api.carregar_credenciais()

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def hospedar_imagem(caminho):
    """A API do Instagram so aceita URL publica, entao subimos a imagem primeiro.

    ATENCAO: catbox.moe e um host publico e anonimo. A imagem fica acessivel
    por link para qualquer pessoa que tenha a URL. Nao use com material sigiloso.
    """
    arquivo = Path(caminho)
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


def post(caminho_api, dados, contexto):
    """POST na API da Meta, com erro traduzido."""
    resp = requests.post(f"{BASE_URL}/{caminho_api}", data={**dados, "access_token": TOKEN}, timeout=60)
    resultado = resp.json()
    if "id" not in resultado:
        raise RuntimeError(f"{contexto}: {api.explicar_erro(resultado)}")
    return resultado["id"]


def criar_container(caminho):
    container_id = post(
        f"{IG_ID}/media",
        {"image_url": hospedar_imagem(caminho), "is_carousel_item": "true"},
        "erro ao enviar imagem",
    )
    print(f"    container: {container_id}")
    return container_id


def criar_carrossel(ids, legenda):
    carrossel_id = post(
        f"{IG_ID}/media",
        {"media_type": "CAROUSEL", "children": ",".join(ids), "caption": legenda},
        "erro ao montar carrossel",
    )
    print(f"    carrossel: {carrossel_id}")
    return carrossel_id


def esperar_processar(container_id, tentativas=12, intervalo=5):
    for i in range(tentativas):
        resp = requests.get(
            f"{BASE_URL}/{container_id}",
            params={"fields": "status_code", "access_token": TOKEN},
            timeout=30,
        )
        dados = resp.json()
        if "error" in dados:
            raise RuntimeError(f"erro ao checar processamento: {api.explicar_erro(dados)}")
        status = dados.get("status_code", "")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"a Meta rejeitou o carrossel: {dados}")
        print(f"    processando... {i * intervalo}s")
        time.sleep(intervalo)
    raise TimeoutError(f"nao ficou pronto em {tentativas * intervalo}s. Tente publicar de novo.")


def expandir(padroes):
    """Resolve padroes como slides/*.png.

    O PowerShell do Windows nao expande curingas para programas externos
    (o bash do Linux/Mac expande), entao fazemos isso aqui para o comando
    funcionar igual nos dois sistemas.
    """
    arquivos = []
    for padrao in padroes:
        if any(c in padrao for c in "*?["):
            achados = sorted(glob.glob(padrao))
            if not achados:
                print(f"ERRO: nenhuma imagem encontrada em '{padrao}'.")
                print("  Confira se a pasta existe e se os arquivos sao .png ou .jpg.")
                sys.exit(1)
            arquivos.extend(achados)
        else:
            arquivos.append(padrao)
    return arquivos


def run(imagens, legenda, dry_run=False):
    if not IG_ID or not TOKEN:
        print(f"ERRO: credenciais ausentes ({ENV_PATH or 'nenhum .env encontrado'}).")
        print("Rode: python instagram/scripts/descobrir_id.py")
        sys.exit(1)
    if FLUXO is None:
        print("ERRO: token nao reconhecido (deveria comecar com IGAA ou EAA).")
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

    print(f"\nPublicando {len(imagens)} slides (conta {IG_ID})")
    print(f"Fluxo: {api.nome_fluxo(FLUXO)}")
    if dry_run:
        print("\n[DRY RUN] Credenciais e imagens OK. Remova --dry-run para publicar.")
        return

    try:
        print("\nPasso 1/3 - enviando imagens")
        ids = [criar_container(img) for img in imagens]

        print("\nPasso 2/3 - montando carrossel")
        carrossel_id = criar_carrossel(ids, legenda)

        print("\nPasso 3/3 - publicando")
        esperar_processar(carrossel_id)
        post_id = post(f"{IG_ID}/media_publish", {"creation_id": carrossel_id}, "erro ao publicar")
    except (RuntimeError, TimeoutError, ValueError) as e:
        print(f"\nFALHOU: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"\nFALHOU: problema de rede ({e})")
        sys.exit(1)

    print(f"\nPublicado! Post ID: {post_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publica um carrossel no Instagram.")
    parser.add_argument("--images", nargs="+", required=True, help="2 a 10 imagens .png/.jpg")
    parser.add_argument("--caption", required=True, help="legenda do post")
    parser.add_argument("--dry-run", action="store_true", help="valida sem publicar")
    args = parser.parse_args()
    run(expandir(args.images), args.caption, args.dry_run)
