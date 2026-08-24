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
import tempfile
import time
from pathlib import Path

import requests

import api

ENV_PATH, TOKEN, IG_ID, FLUXO, BASE_URL = api.carregar_credenciais()

# A API do Instagram nao aceita arquivo local: a imagem precisa estar numa
# URL publica. Estes sao os hosts gratuitos que usamos, em ordem de tentativa.
# Se um cair (acontece), o proximo assume.
#
# ATENCAO: sao hosts publicos e anonimos. A imagem fica acessivel por link
# para qualquer pessoa que tenha a URL. Nao use com material sigiloso.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"


def _catbox(nome, dados, tipo):
    resp = requests.post(
        "https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": (nome, dados, tipo)},
        headers={"User-Agent": UA},
        timeout=120,
    )
    url = resp.text.strip()
    return url if url.startswith("https://") else None


def _litterbox(nome, dados, tipo):
    resp = requests.post(
        "https://litterbox.catbox.moe/resources/internals/api.php",
        data={"reqtype": "fileupload", "time": "1h"},
        files={"fileToUpload": (nome, dados, tipo)},
        headers={"User-Agent": UA},
        timeout=120,
    )
    url = resp.text.strip()
    return url if url.startswith("https://") else None


def _tmpfiles(nome, dados, tipo):
    resp = requests.post(
        "https://tmpfiles.org/api/v1/upload",
        files={"file": (nome, dados, tipo)},
        headers={"User-Agent": UA},
        timeout=120,
    )
    url = resp.json().get("data", {}).get("url", "")
    # A resposta traz a pagina de visualizacao; /dl/ e o link direto do arquivo.
    return url.replace("tmpfiles.org/", "tmpfiles.org/dl/", 1) if url.startswith("http") else None


def _zerox(nome, dados, tipo):
    resp = requests.post(
        "https://0x0.st",
        files={"file": (nome, dados, tipo)},
        headers={"User-Agent": UA},
        timeout=120,
    )
    url = resp.text.strip()
    return url if url.startswith("http") else None


def _uguu(nome, dados, tipo):
    resp = requests.post(
        "https://uguu.se/upload",
        files={"files[]": (nome, dados, tipo)},
        headers={"User-Agent": UA},
        timeout=120,
    )
    arquivos = resp.json().get("files", [])
    url = arquivos[0].get("url", "") if arquivos else ""
    return url if url.startswith("http") else None


def _bashupload(nome, dados, tipo):
    resp = requests.put(
        f"https://bashupload.com/{nome}",
        data=dados,
        headers={"User-Agent": UA},
        timeout=120,
    )
    for pedaco in resp.text.split():
        if pedaco.startswith("https://bashupload.com/"):
            # ?download=1 devolve o arquivo cru; sem isso vem a pagina HTML.
            return pedaco + "?download=1"
    return None


def _tempsh(nome, dados, tipo):
    resp = requests.post(
        "https://temp.sh/upload",
        files={"file": (nome, dados, tipo)},
        headers={"User-Agent": UA},
        timeout=120,
    )
    url = resp.text.strip()
    return url if url.startswith("http") else None


# Sao todos hosts anonimos e gratuitos, entao caem sem aviso: ja vimos os
# quatro primeiros fora ao mesmo tempo. Por isso a lista e longa. Se um dia
# nenhum responder, rode:
#     python instagram/scripts/publish_instagram.py --testar-hosts
HOSTS = [
    ("catbox", _catbox),
    ("litterbox", _litterbox),
    ("tmpfiles", _tmpfiles),
    ("0x0", _zerox),
    ("uguu", _uguu),
    ("bashupload", _bashupload),
    ("temp.sh", _tempsh),
]

# A API de publicacao da Meta aceita SOMENTE JPEG. PNG e recusado com
# "The image format is not supported", entao convertemos antes de subir.
def preparar_jpeg(caminho):
    """Devolve (arquivo_jpeg, e_temporario)."""
    arquivo = Path(caminho)
    if arquivo.suffix.lower() in (".jpg", ".jpeg"):
        return arquivo, False

    try:
        from PIL import Image
    except ImportError:
        print("ERRO: falta a biblioteca de imagem para converter PNG em JPEG.")
        print("  Rode: pip install pillow")
        sys.exit(1)

    with Image.open(arquivo) as img:
        destino = Path(tempfile.gettempdir()) / f"ig-{arquivo.stem}.jpg"
        img.convert("RGB").save(destino, "JPEG", quality=92, optimize=True)
    return destino, True


# Tudo isto o Pillow abre e converte para JPEG antes de subir, entao a
# Meta nunca ve outra coisa. WEBP entrou porque o banco de imagens usa
# WEBP: e 14x mais leve que PNG sem diferenca visivel.
FORMATOS = (".png", ".jpg", ".jpeg", ".webp")


def checar_formato(caminho):
    """Erro cedo e com o nome do arquivo, nao no meio do upload."""
    if Path(caminho).suffix.lower() not in FORMATOS:
        raise ValueError(
            f"Formato nao suportado em {Path(caminho).name}: "
            f"{Path(caminho).suffix} (use {', '.join(FORMATOS)})")


def hospedar_imagem(caminho):
    """Converte para JPEG e sobe para o primeiro host que responder."""
    checar_formato(caminho)

    arquivo, temporario = preparar_jpeg(caminho)
    try:
        # Le uma vez e reusa: cada host tentado receberia o mesmo arquivo.
        dados = arquivo.read_bytes()
        nome = arquivo.name
    finally:
        if temporario:
            # Limpeza nunca pode derrubar a publicacao.
            try:
                arquivo.unlink()
            except OSError:
                pass
    return _tentar_hosts(nome, dados, "image/jpeg")


def _tentar_hosts(nome, dados, tipo):
    problemas = []
    for nome, enviar in HOSTS:
        try:
            url = enviar(nome, dados, tipo)
        except requests.RequestException as e:
            problemas.append(f"{nome}: {type(e).__name__}")
            print(f"    {nome} falhou, tentando o proximo...")
            continue
        if url:
            print(f"    hospedada em {nome}: {url}")
            return url
        problemas.append(f"{nome}: resposta inesperada")
        print(f"    {nome} recusou, tentando o proximo...")

    raise RuntimeError(
        f"nenhum host aceitou {nome}. Tentativas: {'; '.join(problemas)}"
    )


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


def testar_hosts():
    """Sobe um PNG minusculo em cada host e diz quais responderam.

    Quando a publicacao falha em todos, isto separa 'a internet dele' de
    'os hosts cairam', que exigem respostas diferentes.
    """
    import base64
    # 1x1 preto, o menor PNG valido que existe
    minusculo = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
        "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
    print("\nTestando os hosts de imagem...\n")
    vivos = []
    for nome, funcao in HOSTS:
        try:
            url = funcao("teste.png", minusculo, "image/png")
            if url:
                print(f"  OK       {nome:12s} {url}")
                vivos.append(nome)
            else:
                print(f"  RECUSOU  {nome:12s} respondeu, mas sem link")
        except Exception as e:
            print(f"  FALHOU   {nome:12s} {type(e).__name__}")
    print()
    if vivos:
        print(f"{len(vivos)} de {len(HOSTS)} de pe: {', '.join(vivos)}")
        print("Pode publicar normalmente.")
    else:
        print("Nenhum host respondeu.")
        print("Se a sua internet esta boa, foram eles que cairam: tente mais tarde.")


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

    # O dry-run tem de reprovar tudo que a publicacao reprovaria. Antes ele
    # so olhava credencial, entao dizia OK e a publicacao morria no formato.
    try:
        for img in imagens:
            checar_formato(img)
    except ValueError as e:
        print(f"ERRO: {e}")
        sys.exit(1)

    print(f"\nPublicando {len(imagens)} slides (conta {IG_ID})")
    print(f"Fluxo: {api.nome_fluxo(FLUXO)}")
    if dry_run:
        print("\n[DRY RUN] Credenciais, formatos e imagens OK. Remova --dry-run para publicar.")
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
    parser.add_argument("--images", nargs="+", help="2 a 10 imagens .png/.jpg/.webp")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--caption", help="legenda do post")
    grupo.add_argument("--caption-file", help="arquivo .txt com a legenda (evita problema de aspas)")
    parser.add_argument("--dry-run", action="store_true", help="valida sem publicar")
    parser.add_argument("--testar-hosts", action="store_true",
                        help="testa qual host de imagem esta de pe agora")
    args = parser.parse_args()

    # Diagnostico nao publica nada, entao nao pede legenda nem imagem.
    if args.testar_hosts:
        testar_hosts()
        sys.exit(0)
    if not args.images:
        parser.error("informe --images, ou use --testar-hosts sozinho")
    if not args.caption and not args.caption_file:
        parser.error("informe --caption ou --caption-file")

    if args.caption_file:
        arquivo = Path(args.caption_file)
        if not arquivo.is_file():
            print(f"ERRO: arquivo de legenda nao encontrado: {args.caption_file}")
            sys.exit(1)
        legenda = arquivo.read_text(encoding="utf-8").strip()
    else:
        legenda = args.caption

    # A Meta corta a legenda em 2200 caracteres.
    if len(legenda) > 2200:
        print(f"ERRO: legenda com {len(legenda)} caracteres. O limite do Instagram e 2200.")
        sys.exit(1)

    run(expandir(args.images), legenda, args.dry_run)
