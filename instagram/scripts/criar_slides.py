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
FUNDOS = ("creme", "laranja", "preto")

# Ritmo do carrossel: um fundo calmo entre cada fundo forte, para o feed
# nao ficar nem monotono nem cansativo.
RITMO = ("creme", "preto", "creme", "laranja", "creme", "preto", "creme", "laranja",
         "creme", "preto")

# Cada slide recebe uma combinacao de elementos graficos diferente, para a
# arte nao se repetir. As receitas alternam de forma previsivel.
# Espaco disponivel para o recorte em cada layout. A imagem e encaixada
# dentro dessa caixa preservando a proporcao, entao um sujeito largo cresce
# na horizontal e um sujeito alto cresce na vertical, sempre bem aproveitado.
CAIXAS = {
    "capa":       {"w": 600, "h": 560, "dir": 46, "base": 300},
    "declaracao": {"w": 540, "h": 580, "dir": 40, "base": 205},
    "numero":     {"w": 480, "h": 540, "dir": 36, "base": 225},
    "lista":      {"w": 400, "h": 400, "dir": 40, "topo": 74},
    "fluxo":      {"w": 400, "h": 400, "dir": 36, "topo": 74},
    "comparacao": {"w": 380, "h": 380, "dir": 44, "topo": 70},
    "fecho":      {"w": 430, "h": 380, "centro": True, "topo": 96},
}


MARGEM_PALCO = 76   # a margem lateral do texto
FOLGA = 34          # respiro minimo entre a imagem e a letra


def caixa_do_recorte(layout, medida):
    """Decide onde o recorte entra, a partir da forma da imagem.

    A regra vem do desenho, nao da conveniencia:

    - Sujeito ALTO (busto, pessoa) fica AO LADO do texto. O texto encolhe
      exatamente ate onde a imagem comeca, com folga.
    - Sujeito LARGO (uma fila de objetos, um leque) fica ACIMA do texto,
      ocupando o quadro todo. Espremer um sujeito largo na lateral tapa
      a letra e ainda deixa ele pequeno demais para ser lido.

    Devolve (estilo_do_recorte, largura_maxima_do_titulo_ou_None).
    """
    caixa = CAIXAS.get(layout, CAIXAS["declaracao"])
    largura, altura = caixa["w"], caixa["h"]
    proporcao = (medida[0] / medida[1]) if medida else 1.0

    # Layouts com o texto ja embaixo colocam a imagem no topo de qualquer jeito.
    topo_fixo = "topo" in caixa or caixa.get("centro")

    if proporcao >= 1.25 and not topo_fixo:
        # Faixa larga no topo: o sujeito respira e o titulo fica inteiro.
        # A faixa nao pode descer ate o selo: 430px e o teto seguro.
        largura = min(1080 - MARGEM_PALCO * 2, round(caixa["h"] * proporcao * 1.35))
        altura = round(largura / proporcao)
        if altura > 430:
            altura = 430
            largura = round(altura * proporcao)
        estilo = f"width:{largura}px;height:{altura}px;right:{caixa['dir']}px;top:96px"
        return estilo, None

    if medida:
        escala = min(largura / medida[0], altura / medida[1])
        largura, altura = round(medida[0] * escala), round(medida[1] * escala)

    partes = [f"width:{largura}px", f"height:{altura}px"]
    if caixa.get("centro"):
        partes += [f"left:{round((1080 - largura) / 2)}px", f"top:{caixa['topo']}px"]
        return ";".join(partes), None
    if "topo" in caixa:
        partes += [f"right:{caixa['dir']}px", f"top:{caixa['topo']}px"]
        # Imagem no topo e texto embaixo: so o titulo curto precisa de limite.
        return ";".join(partes), 1080 - caixa["dir"] - largura - MARGEM_PALCO - FOLGA

    partes += [f"right:{caixa['dir']}px", f"bottom:{caixa['base']}px"]
    # Imagem na lateral: o texto vai exatamente ate onde ela comeca.
    limite = 1080 - caixa["dir"] - largura - MARGEM_PALCO - FOLGA
    return ";".join(partes), limite


CARIMBO = "Wallace<br>Ribas"

RECEITAS = [
    '<div class="camada reticula canto-sd"></div>'
    '<div class="disco" style="width:170px;height:170px;left:-70px;top:150px"></div>',

    '<div class="barra-diag" style="top:200px"></div>'
    '<div class="camada reticula faixa-baixo"></div>',

    '<div class="camada reticula coluna-esq"></div>'
    '<div class="carimbo" style="top:120px;right:96px">__CARIMBO__</div>',

    '<div class="disco" style="width:520px;height:520px;right:-170px;top:-130px"></div>'
    '<div class="camada hachura" style="inset:auto 0 0 0;height:190px;'
    '-webkit-mask-image:linear-gradient(to top,#000 6%,transparent 88%)"></div>',

    '<div class="camada reticula faixa-baixo"></div>'
    '<div class="camada reticula canto-sd"></div>',

    '<div class="carimbo" style="top:130px;left:92px">__CARIMBO__</div>'
    '<div class="camada reticula canto-sd"></div>',
]

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
        selo, layout, numerao, fundo = "", "declaracao", "", ""
        while linhas:
            linha = linhas[0]
            if linha.startswith("[") and linha.endswith("]"):
                selo = linha[1:-1].strip()
            elif linha.startswith("{") and "}" in linha:
                fecha = linha.index("}")
                dentro = linha[1:fecha].strip().lower().split()
                layout = dentro[0] if dentro else "declaracao"
                for extra in dentro[1:]:
                    if extra in FUNDOS:
                        fundo = extra
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
                       "fundo": fundo, "titulo": linhas[0], "itens": itens,
                       "apoio": apoio})

    if not slides:
        print("ERRO: o arquivo esta vazio.")
        sys.exit(1)
    if len(slides) > 10:
        print(f"ERRO: {len(slides)} slides. O Instagram aceita no maximo 10.")
        sys.exit(1)
    return slides


def fotos_da_pasta(pasta):
    """Procura foto-01, foto-02... na pasta e casa cada uma com o seu slide."""
    if not pasta:
        return {}
    diretorio = Path(pasta)
    if not diretorio.is_dir():
        print(f"ERRO: pasta de fotos nao encontrada: {pasta}")
        sys.exit(1)
    achadas = {}
    for arquivo in sorted(diretorio.iterdir()):
        casa = re.match(r"(foto|recorte)-?(\d+)", arquivo.stem, re.I)
        if casa and arquivo.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            achadas[(casa.group(1).lower(), int(casa.group(2)))] = arquivo
    return achadas


def aparar_transparencia(arquivo):
    """Corta a moldura transparente em volta do recorte.

    O gerador de imagem quase nunca centraliza o sujeito: sobra vazio de um
    lado e ele acaba aparecendo pequeno e torto no slide. Aparando a borda,
    o enquadramento fica igual para qualquer imagem que chegue.

    Devolve (bytes_png, True) quando aparou, ou (None, False) quando nao ha
    o que aparar ou a imagem nao tem transparencia.
    """
    try:
        from PIL import Image
    except ImportError:
        return None, None

    import io
    with Image.open(arquivo) as img:
        if img.mode not in ("RGBA", "LA"):
            return None, img.size
        limites = img.convert("RGBA").getchannel("A").getbbox()
        if not limites:
            return None, img.size
        largura, altura = img.size
        # Se ja esta justo, nao mexe.
        if limites == (0, 0, largura, altura):
            return None, img.size
        buffer = io.BytesIO()
        cortada = img.crop(limites)
        cortada.save(buffer, "PNG", optimize=True)
        sobra = 100 - round(100 * (limites[2] - limites[0]) * (limites[3] - limites[1])
                            / (largura * altura))
        print(f"    aparei {sobra}% de borda vazia em {arquivo.name}")
        return buffer.getvalue(), cortada.size


def foto_embutida(caminho, aparar=False):
    """Converte a imagem em data URI. Devolve (uri, medida_em_px_ou_None)."""
    if not caminho:
        return "none", None
    arquivo = Path(caminho)
    if not arquivo.is_file():
        print(f"ERRO: imagem nao encontrada: {caminho}")
        sys.exit(1)

    if aparar:
        cortada, medida = aparar_transparencia(arquivo)
        if cortada:
            return f"url('data:image/png;base64,{base64.b64encode(cortada).decode()}')", medida

    tipo = mimetypes.guess_type(arquivo.name)[0] or "image/jpeg"
    dados = base64.b64encode(arquivo.read_bytes()).decode()
    medida = None
    if aparar:
        _, medida = aparar_transparencia(arquivo)
    return f"url('data:{tipo};base64,{dados}')", medida


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


def montar_html(slide, numero, total, marca, foto_css, recorte, estilo):
    modelo = TEMPLATES[estilo].read_text(encoding="utf-8")
    corpo = "".join(f"<p>{marcar(l)}</p>" for l in slide["apoio"])
    layout = slide["layout"] if numero > 1 else "capa"
    fundo = slide["fundo"] or RITMO[(numero - 1) % len(RITMO)]
    recorte_css, recorte_medida = recorte
    tem_foto = foto_css != "none"
    tem_recorte = recorte_css != "none"
    classes = " ".join(filter(None, [
        f"l-{layout}", f"f-{fundo}",
        "" if tem_foto else "sem-foto",
        "" if tem_recorte else "sem-recorte",
    ]))
    if tem_recorte:
        estilo_recorte, limite = caixa_do_recorte(layout, recorte_medida)
        limite_css = (f"<style>.palco h1,.palco .apoio,.palco .regua"
                      f"{{max-width:{max(limite, 320)}px}}</style>") if limite else ""
    else:
        estilo_recorte, limite_css = "", ""

    # Sem foto, a receita grafica precisa preencher mais o quadro.
    receita = RECEITAS[(numero - 1 + (0 if (tem_foto or tem_recorte) else 3)) % len(RECEITAS)]
    receita = receita.replace("__CARIMBO__", CARIMBO)
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
        "__DECORACAO__": receita,
        "__RECORTE__": recorte_css,
        "__CAIXA_RECORTE__": estilo_recorte,
        "__LIMITE_TEXTO__": limite_css,
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
    parser.add_argument("--foto", default="", help="uma imagem para todos os slides")
    parser.add_argument("--fotos", default="", help="pasta com foto-01/recorte-01... uma por slide")
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
    foto_unica = foto_embutida(args.foto)[0]
    mapa_fotos = fotos_da_pasta(args.fotos)
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
                temp.write_text(montar_html(
                    slide, i, len(slides), args.marca,
                    foto_embutida(mapa_fotos[("foto", i)])[0] if ("foto", i) in mapa_fotos else foto_unica,
                    foto_embutida(mapa_fotos[("recorte", i)], aparar=True) if ("recorte", i) in mapa_fotos else ("none", None),
                    args.estilo), encoding="utf-8")
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
