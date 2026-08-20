"""
criar_slides.py — Transforma um arquivo de texto em slides prontos pro Instagram.

Uso:
    python criar_slides.py carrossel.txt
    python criar_slides.py carrossel.txt --tema claro
    python criar_slides.py carrossel.txt --arroba @wallaceribas_

O arquivo de texto e simples: cada slide separado por uma linha com ---

    Como triplicar seu alcance
    O que ninguem te conta
    ---
    1. Poste no horario que SEU publico esta online
    Nao o horario que a internet diz
    ---
    Salva esse post
    pra nao esquecer

A primeira linha de cada slide vira o titulo (maior).
As linhas seguintes viram o texto de apoio (menor).
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TAMANHO = 1080
MARGEM = 96

# Onde procurar fontes, em ordem de preferencia, em cada sistema.
FONTES = {
    "bold": [
        "C:/Windows/Fonts/segoeuib.ttf",           # Windows — Segoe UI Bold
        "C:/Windows/Fonts/arialbd.ttf",            # Windows — Arial Bold
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # Mac
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
    ],
    "regular": [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}

TEMAS = {
    # Identidade @wallaceribas_ — laranja e preto.
    "wr-preto": {
        "fundo": (10, 10, 11),
        "fundo2": (24, 16, 10),
        "titulo": (255, 255, 255),
        "texto": (154, 154, 160),
        "destaque": (255, 107, 26),
        "marcador": "barra",
    },
    "wr-laranja": {
        "fundo": (255, 107, 26),
        "fundo2": (224, 82, 8),
        "titulo": (10, 10, 11),
        "texto": (60, 26, 8),
        "destaque": (10, 10, 11),
        "marcador": "barra",
    },
    "wr-bloco": {
        "fundo": (10, 10, 11),
        "fundo2": (10, 10, 11),
        "titulo": (255, 255, 255),
        "texto": (154, 154, 160),
        "destaque": (255, 107, 26),
        "marcador": "faixa",
    },
    "escuro": {
        "fundo": (13, 17, 29),
        "fundo2": (28, 26, 56),
        "titulo": (255, 255, 255),
        "texto": (176, 186, 204),
        "destaque": (99, 102, 241),
        "marcador": "barra",
    },
    "claro": {
        "fundo": (247, 245, 240),
        "fundo2": (232, 228, 220),
        "titulo": (17, 22, 34),
        "texto": (82, 90, 105),
        "destaque": (79, 70, 229),
        "marcador": "barra",
    },
}


def achar_fonte(peso, tamanho):
    for caminho in FONTES[peso]:
        if Path(caminho).is_file():
            return ImageFont.truetype(caminho, tamanho)
    print(f"AVISO: nenhuma fonte '{peso}' encontrada, usando a padrao (vai ficar feio).")
    return ImageFont.load_default(tamanho)


def ler_slides(caminho):
    """Le o arquivo e devolve [(titulo, [linhas de apoio]), ...]."""
    arquivo = Path(caminho)
    if not arquivo.is_file():
        print(f"ERRO: arquivo nao encontrado: {caminho}")
        sys.exit(1)

    blocos = [b.strip() for b in arquivo.read_text(encoding="utf-8").split("---")]
    slides = []
    for bloco in blocos:
        if not bloco:
            continue
        linhas = [l.strip() for l in bloco.splitlines() if l.strip()]
        slides.append((linhas[0], linhas[1:]))

    if not slides:
        print("ERRO: o arquivo esta vazio.")
        sys.exit(1)
    if len(slides) > 10:
        print(f"ERRO: {len(slides)} slides. O Instagram aceita no maximo 10.")
        sys.exit(1)
    return slides


def quebrar(texto, fonte, largura_max, draw):
    """Quebra o texto em linhas que cabem na largura."""
    palavras, linhas, atual = texto.split(), [], ""
    for palavra in palavras:
        teste = f"{atual} {palavra}".strip()
        if draw.textlength(teste, font=fonte) <= largura_max:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def fundo_degrade(cores):
    """Degrade vertical suave entre as duas cores do tema."""
    img = Image.new("RGB", (TAMANHO, TAMANHO), cores["fundo"])
    draw = ImageDraw.Draw(img)
    c1, c2 = cores["fundo"], cores["fundo2"]
    for y in range(TAMANHO):
        p = y / TAMANHO
        draw.line(
            [(0, y), (TAMANHO, y)],
            fill=tuple(int(c1[i] + (c2[i] - c1[i]) * p) for i in range(3)),
        )
    return img


def desenhar_slide(titulo, apoio, numero, total, cores, arroba, capa):
    img = fundo_degrade(cores)
    draw = ImageDraw.Draw(img)
    largura = TAMANHO - MARGEM * 2

    # A capa (slide 1) tem texto maior para prender a atencao.
    tam_titulo = 76 if capa else 60
    f_titulo = achar_fonte("bold", tam_titulo)
    f_apoio = achar_fonte("regular", 38)
    f_meta = achar_fonte("bold", 26)

    # Barra de destaque no topo do bloco de texto.
    linhas_t = quebrar(titulo, f_titulo, largura, draw)
    linhas_a = []
    for linha in apoio:
        linhas_a.extend(quebrar(linha, f_apoio, largura, draw))

    alt_t = len(linhas_t) * int(tam_titulo * 1.25)
    alt_a = len(linhas_a) * 56 + (40 if linhas_a else 0)
    y = (TAMANHO - alt_t - alt_a) // 2

    if cores["marcador"] == "faixa":
        # Faixa laranja atras da primeira linha do titulo — destaca de longe.
        larg_faixa = draw.textlength(linhas_t[0], font=f_titulo)
        draw.rectangle(
            [MARGEM - 20, y - 14, MARGEM + larg_faixa + 24, y + int(tam_titulo * 1.18)],
            fill=cores["destaque"],
        )
    else:
        # Barrinha curta acima do titulo.
        draw.rounded_rectangle(
            [MARGEM, y - 56, MARGEM + 72, y - 44], radius=6, fill=cores["destaque"]
        )

    for i, linha in enumerate(linhas_t):
        # Na faixa, a primeira linha fica preta sobre o laranja.
        cor = cores["fundo"] if (cores["marcador"] == "faixa" and i == 0) else cores["titulo"]
        draw.text((MARGEM, y), linha, font=f_titulo, fill=cor)
        y += int(tam_titulo * 1.25)

    if linhas_a:
        y += 40
        for linha in linhas_a:
            draw.text((MARGEM, y), linha, font=f_apoio, fill=cores["texto"])
            y += 56

    # Rodape: "01/04 · @conta" na esquerda, seta de arrasta na direita.
    rodape_y = TAMANHO - MARGEM - 20
    contador = f"{numero:02d}/{total:02d}"
    draw.text((MARGEM, rodape_y), contador, font=f_meta, fill=cores["destaque"])

    if arroba:
        x = MARGEM + draw.textlength(contador, font=f_meta) + 16
        draw.text((x, rodape_y), f"· {arroba}", font=f_meta, fill=cores["texto"])

    # Seta so nos slides que tem proximo.
    if numero < total:
        f_seta = achar_fonte("bold", 40)
        larg = draw.textlength("→", font=f_seta)
        draw.text((TAMANHO - MARGEM - larg, rodape_y - 12), "→", font=f_seta, fill=cores["destaque"])

    return img


def main():
    parser = argparse.ArgumentParser(description="Cria slides de carrossel a partir de um .txt")
    parser.add_argument("arquivo", help="arquivo de texto com os slides separados por ---")
    parser.add_argument("--tema", default="wr-preto", choices=list(TEMAS), help="cores do slide")
    parser.add_argument("--arroba", default="", help="seu @ no rodape (ex: @wallaceribas_)")
    parser.add_argument("--saida", default="slides", help="pasta onde salvar (padrao: slides)")
    args = parser.parse_args()

    slides = ler_slides(args.arquivo)
    cores = TEMAS[args.tema]
    pasta = Path(args.saida)
    pasta.mkdir(parents=True, exist_ok=True)

    # Limpa slides antigos para nao misturar carrosseis.
    antigos = sorted(pasta.glob("slide-*.png"))
    for velho in antigos:
        velho.unlink()
    if antigos:
        print(f"Removi {len(antigos)} slide(s) do carrossel anterior.\n")

    print(f"Criando {len(slides)} slides (tema {args.tema})...\n")
    for i, (titulo, apoio) in enumerate(slides, start=1):
        img = desenhar_slide(titulo, apoio, i, len(slides), cores, args.arroba, capa=(i == 1))
        destino = pasta / f"slide-{i:02d}.png"
        img.save(destino, "PNG", optimize=True)
        print(f"  {destino}  —  {titulo[:48]}")

    print(f"\nPronto! {len(slides)} slides em '{pasta}/'")
    print("\nProximo passo — conferir sem publicar:")
    print(f'  python instagram/scripts/publish_instagram.py --images {pasta}/*.png --caption "sua legenda" --dry-run')


if __name__ == "__main__":
    main()
