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
LAYOUTS = ("capa", "declaracao", "numero", "lista", "fluxo", "comparacao", "fecho")

FAIXAS = {
    "wind":   [(30, 82), (60, 70), (95, 60), (135, 52), (999, 46)],
    "poster": [(24, 118), (48, 96), (78, 80), (115, 66), (999, 56)],
    "poster-capa": [(24, 156), (44, 128), (70, 104), (100, 86), (999, 72)],
}


def tamanho_titulo(texto, estilo, capa=False, layout="declaracao"):
    limpo = re.sub(r"[*_]", "", texto)
    # Layouts com muito conteudo abaixo precisam de titulo menor.
    if layout in ("lista", "fluxo", "comparacao", "numero"):
        return {"numero": 58, "comparacao": 56}.get(layout, 52)
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
        # [selo] e {layout} podem vir em qualquer ordem, antes do titulo.
        selo, layout, numerao = "", "declaracao", ""
        while linhas:
            linha = linhas[0]
            if linha.startswith("[") and linha.endswith("]"):
                selo = linha[1:-1].strip()
            elif linha.startswith("{") and "}" in linha:
                fecha = linha.index("}")
                layout = linha[1:fecha].strip().lower()
                if layout not in LAYOUTS:
                    print(f"ERRO: layout '{layout}' nao existe. Use: {', '.join(LAYOUTS)}")
                    sys.exit(1)
                resto = linha[fecha + 1:].strip()
                if resto:
                    linhas[0] = resto
                    continue
            else:
                break
            linhas = linhas[1:]

        # No layout numero, a linha seguinte e o proprio numero gigante.
        if layout == "numero" and linhas:
            numerao, linhas = linhas[0], linhas[1:]

        if not linhas:
            print("ERRO: um slide tem selo ou layout mas nenhum titulo depois.")
            sys.exit(1)

        # Linhas que comecam com "- " sao itens; o resto e texto de apoio.
        itens = [l[2:].strip() for l in linhas[1:] if l.startswith("- ")]
        apoio = [l for l in linhas[1:] if not l.startswith("- ")]
        slides.append({"selo": selo, "layout": layout, "numerao": numerao,
                       "titulo": linhas[0], "itens": itens, "apoio": apoio})

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


def montar_corpo(slide):
    """Cada layout desenha o miolo do slide do seu proprio jeito."""
    layout, itens = slide["layout"], slide["itens"]

    if layout == "lista" and itens:
        linhas = "".join(
            f'<div class="item"><span class="marca-item">{i:02d}</span>'
            f'<span class="txt-item">{marcar(x)}</span></div>'
            for i, x in enumerate(itens, start=1)
        )
        return f'<div class="lista">{linhas}</div>'

    if layout == "fluxo" and itens:
        etapas = "".join(
            f'<div class="etapa"><div class="trilho"><div class="bolha">{i}</div>'
            f'<div class="fio-v"></div></div>'
            f'<div class="corpo-etapa">{marcar(x)}</div></div>'
            for i, x in enumerate(itens, start=1)
        )
        return f'<div class="fluxo">{etapas}</div>'

    if layout == "comparacao" and itens:
        lados = []
        for i, bruto in enumerate(itens[:2]):
            rotulo, _, valor = bruto.partition("|")
            classe = "antes" if i == 0 else "depois"
            lados.append(
                f'<div class="lado {classe}"><div class="rotulo">{marcar(rotulo.strip())}</div>'
                f'<div class="valor">{marcar(valor.strip())}</div></div>'
            )
        return f'<div class="versus">{"".join(lados)}</div>'

    return ""


def montar_html(slide, numero, total, marca, foto_css, estilo):
    modelo = TEMPLATES[estilo].read_text(encoding="utf-8")
    corpo = "".join(f"<p>{marcar(l)}</p>" for l in slide["apoio"])
    layout = slide["layout"] if numero > 1 else "capa"
    classes = " ".join(filter(None, ["capa" if numero == 1 else "", f"l-{layout}"]))
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
        "__TAM__": str(tamanho_titulo(slide["titulo"], estilo, numero == 1, layout)),
        "__CLASSES__": classes,
        "__NUMERAO__": f'<div class="numerao">{html.escape(slide["numerao"])}</div>' if slide["numerao"] else "",
        "__CORPO__": montar_corpo(slide),
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
                print(f"  {destino}  [{slide['layout']}]  {re.sub(r'[*_]', '', slide['titulo'])[:38]}")
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
