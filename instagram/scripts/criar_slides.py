"""
criar_slides.py — Transforma um arquivo de texto em slides prontos pro Instagram.

Uso:
    python criar_slides.py carrossel.txt
    python criar_slides.py carrossel.txt --marca "WALLACE RIBAS" --foto capa.jpg

Formato do arquivo — cada slide separado por uma linha com ---

    [selo em laranja]
    Titulo do slide com _peso leve_ e *palavra laranja*
    Linha de apoio, tambem aceita marcacao.
    ---
    Proximo slide

Marcacoes disponiveis:
    *texto*     -> laranja
    _texto_     -> peso leve (o contraste de peso da referencia Wind)
    __texto__   -> sublinhado laranja
    [texto]     -> selo laranja (so na primeira linha do slide)

Precisa do navegador, instalado uma unica vez:
    pip install playwright
    playwright install chromium
"""
import argparse
import base64
import html
import mimetypes
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TEMPLATES = {"wind": AQUI / "template.html", "poster": AQUI / "template-poster.html"}
FONTES = AQUI.parent / "fontes"

# Titulo curto pode ser grande; titulo longo precisa encolher para caber.
FAIXAS = {
    "wind":   [(30, 82), (60, 70), (95, 60), (135, 52), (999, 46)],
    "poster": [(24, 118), (48, 96), (78, 80), (115, 66), (999, 56)],
    "poster-capa": [(24, 156), (44, 128), (70, 104), (100, 86), (999, 72)],
}


def tamanho_titulo(texto, estilo, capa=False):
    limpo = re.sub(r"[*_]", "", texto)
    chave = f"{estilo}-capa" if capa and f"{estilo}-capa" in FAIXAS else estilo
    faixas = FAIXAS[chave]
    for limite, tam in faixas:
        if len(limpo) <= limite:
            return tam
    return faixas[-1][1]


def marcar(texto):
    """Escapa HTML e aplica as marcacoes de estilo.

    A ordem importa: __sublinhado__ antes de _leve_, senao o primeiro
    par de underscores seria consumido pela regra de peso leve.
    """
    t = html.escape(texto)
    t = re.sub(r"__([^_]+)__", r'<span class="sub">\1</span>', t)
    t = re.sub(r"\*([^*]+)\*", r'<span class="cor">\1</span>', t)
    t = re.sub(r"_([^_]+)_", r'<span class="leve">\1</span>', t)
    return t


def ler_slides(caminho):
    arquivo = Path(caminho)
    if not arquivo.is_file():
        print(f"ERRO: arquivo nao encontrado: {caminho}")
        sys.exit(1)

    slides = []
    for bloco in arquivo.read_text(encoding="utf-8").split("---"):
        linhas = [l.strip() for l in bloco.strip().splitlines() if l.strip()]
        if not linhas:
            continue
        # Primeira linha entre colchetes vira selo; o titulo passa a ser a seguinte.
        selo = ""
        if linhas[0].startswith("[") and linhas[0].endswith("]"):
            selo = linhas[0][1:-1].strip()
            linhas = linhas[1:]
        if not linhas:
            print(f"ERRO: um slide tem o selo '[{selo}]' mas nenhum titulo depois.")
            sys.exit(1)
        slides.append({"selo": selo, "titulo": linhas[0], "apoio": linhas[1:]})

    if not slides:
        print("ERRO: o arquivo esta vazio.")
        sys.exit(1)
    if len(slides) > 10:
        print(f"ERRO: {len(slides)} slides. O Instagram aceita no maximo 10.")
        sys.exit(1)
    return slides


def foto_embutida(caminho):
    """Converte a foto em data URI para o navegador ler sem servidor."""
    if not caminho:
        return "none"
    arquivo = Path(caminho)
    if not arquivo.is_file():
        print(f"ERRO: foto nao encontrada: {caminho}")
        sys.exit(1)
    tipo = mimetypes.guess_type(arquivo.name)[0] or "image/jpeg"
    dados = base64.b64encode(arquivo.read_bytes()).decode()
    return f"url('data:{tipo};base64,{dados}')"


def montar_html(slide, numero, total, marca, foto_css, estilo):
    modelo = TEMPLATES[estilo].read_text(encoding="utf-8")
    corpo = "".join(f"<p>{marcar(l)}</p>" for l in slide["apoio"])
    if estilo == "poster":
        arrasta = "Arraste &rarr;" if numero < total else "Fim"
    else:
        arrasta = (
            '<span>Arraste para o lado</span><span class="seta">&rarr;</span>'
            if numero < total else "<span>Fim</span>"
        )
    trocas = {
        "__FONTES__": FONTES.as_uri(),
        "__FOTO__": foto_css,
        "__TEM_FOTO__": "none" if foto_css == "none" else "block",
        "__NUM__": f"{numero:02d}",
        "__MARCA__": html.escape(marca),
        "__SELO__": f'<div class="selo">{html.escape(slide["selo"])}</div>' if slide["selo"] else "",
        "__TAM__": str(tamanho_titulo(slide["titulo"], estilo, numero == 1)),
        "__CAPA__": "capa" if numero == 1 else "",
        "__TITULO__": marcar(slide["titulo"]),
        "__APOIO__": f'<div class="apoio">{corpo}</div>' if corpo else "",
        "__CONTADOR__": f"{numero:02d} / {total:02d}",
        "__ARRASTA__": arrasta,
    }
    for chave, valor in trocas.items():
        modelo = modelo.replace(chave, valor)
    return modelo


def main():
    parser = argparse.ArgumentParser(description="Cria slides de carrossel a partir de um .txt")
    parser.add_argument("arquivo", help="arquivo de texto com os slides separados por ---")
    parser.add_argument("--marca", default="WALLACE RIBAS", help="assinatura no topo do slide")
    parser.add_argument("--foto", default="", help="imagem de fundo (opcional)")
    parser.add_argument("--saida", default="slides", help="pasta onde salvar (padrao: slides)")
    parser.add_argument("--estilo", default="wind", choices=list(TEMPLATES),
                        help="wind = escuro moderno; poster = creme retro")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERRO: o navegador de renderizacao nao esta instalado.")
        print("\nRode estes dois comandos uma unica vez:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)

    slides = ler_slides(args.arquivo)
    foto_css = foto_embutida(args.foto)
    pasta = Path(args.saida).resolve()
    pasta.mkdir(parents=True, exist_ok=True)

    antigos = sorted(pasta.glob("slide-*.png"))
    for velho in antigos:
        velho.unlink()
    if antigos:
        print(f"Removi {len(antigos)} slide(s) do carrossel anterior.\n")

    print(f"Criando {len(slides)} slides (estilo {args.estilo})...\n")
    temp = pasta / "_render.html"
    try:
        with sync_playwright() as p:
            # CHROMIUM_PATH permite usar um Chromium ja instalado no sistema.
            atalho = os.getenv("CHROMIUM_PATH")
            navegador = p.chromium.launch(executable_path=atalho) if atalho else p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": 1080, "height": 1080})
            for i, slide in enumerate(slides, start=1):
                temp.write_text(montar_html(slide, i, len(slides), args.marca, foto_css, args.estilo), encoding="utf-8")
                pagina.goto(temp.as_uri())
                pagina.wait_for_timeout(340)  # deixa as fontes carregarem
                destino = pasta / f"slide-{i:02d}.png"
                pagina.screenshot(path=str(destino))
                print(f"  {destino}  —  {re.sub(r'[*_]', '', slide['titulo'])[:46]}")
            navegador.close()
    except Exception as e:
        print(f"\nERRO ao renderizar: {e}")
        print("Se falar em executavel faltando, rode: playwright install chromium")
        sys.exit(1)
    finally:
        temp.unlink(missing_ok=True)

    print(f"\nPronto! {len(slides)} slides em '{pasta}/'")
    print("\nProximo passo — conferir sem publicar:")
    print(f'  python instagram/scripts/publish_instagram.py --images {pasta}/*.png --caption "sua legenda" --dry-run')


if __name__ == "__main__":
    main()
