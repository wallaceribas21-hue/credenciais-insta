# Sistema visual WR

Formato **1080x1350 (4:5)**. Ocupa um quarto a mais de tela no feed que
o quadrado, e e o formato das referencias.

Gerar com:

```
python instagram/scripts/criar_slides.py conteudo/00X-nome.txt --estilo sistema --fotos fotos
```

## A cor nao decora, ela sinaliza

Cada slide tem UMA funcao, e a cor diz qual e. Quem arrasta aprende isso
sem perceber.

| cor | funcao | onde entra |
| --- | --- | --- |
| **PRETO** `#0B0B0B` | para o dedo | capa e viradas de chave |
| **BRANCO** `#FFFFFF` | explica | lista, fluxo, comparacao, numero |
| **LARANJA** `#FF6B1A` | pede acao | o fecho, e so ele |

Branco, nao creme. Creme e papel; branco e o que da o ar que faz parecer
caro. O premium nao esta no enfeite, esta no espaco vazio.

**Um laranja por carrossel, dois no maximo.** Se o laranja aparece toda
hora, ele deixa de significar "olha aqui" e vira so cor de fundo.

## O ritmo

O script escolhe sozinho pela funcao do slide, e nunca deixa dois pretos
seguidos: tensao sem alivio no meio cansa antes do fim.

```
01 PRETO    para o scroll
02 BRANCO   respira, explica
03 BRANCO   continua
04 PRETO    vira a chave
05 BRANCO
06 BRANCO
07 BRANCO
08 LARANJA  acao
```

Para forcar uma cor num slide, escreva na copy: `{declaracao preto}`.

## Tipografia

| papel | fonte | por que |
| --- | --- | --- |
| Titulo | **Fjalla One** | substituta livre da Filmotype Warsaw. Condensada com respiro entre as letras, entao frase longa nao vira bloco. |
| Texto | **Arimo** | clone metrico da Helvetica, mesmas larguras. Neutra, nao geometrica: soa profissional, nao startup. |
| Etiqueta | **Roboto Mono** | numero do slide, "arraste", selo. E a original, nao substituta. |

Cada fonte faz um trabalho so. Titulo grita, texto explica, mono etiqueta.

## Imagem

**No 4:5 a imagem sempre vai para cima e o texto ocupa a largura inteira
embaixo.** Imagem ao lado do texto espreme o titulo em uma palavra por
linha. Foi o erro que a primeira versao cometeu.

A posicao horizontal alterna (direita, esquerda, centro) para o carrossel
nao virar padrao. Capa e fecho ficam sempre centrados.

Duas familias:

- **Recorte** — objeto solto sobre a cor chapada, com a sombra dura da
  marca. E o padrao. Vem de `fotos/banco/`.
- **Cenario** — foto ocupando o quadro inteiro, texto por cima. Entra
  como `foto-NN` na pasta de fotos. Ai o veu escuro liga sozinho, e e ele
  que garante que a copy le sobre qualquer imagem.

## Regras que nao se negociam

1. **Veu com foto de cenario, nunca com recorte.** Com recorte ele so
   apaga a imagem.
2. **Sombra so a da marca.** As imagens do banco vem sem sombra propria;
   o template desenha `drop-shadow(18px 16px 0)`. Duas sombras em
   direcoes diferentes matam o efeito de colagem.
3. **Texto centralizado so em quadro vazio.** Com imagem no topo, o
   texto centralizado sobe e passa por cima dela.


---

# Estilo REVISTA — a linha nova

Vem da referencia de decodificacao de marca. Convive com o sistema
antigo, nao substitui: o sistema serve carrossel didatico, a revista
serve carrossel de analise com ferramenta no fim.

## As cores nao mudam

Preto `#0B0B0B`, laranja `#FF6B1A`, branco. A identidade e dele e ja
carrega duas empresas anteriores. **Muda a tipografia, nunca a cor.**

Detalhe que a gente ganhou de graca: as fotos de palco do Alfredo sao
azuis, luz de evento. Azul e laranja sao complementares. Tipografia
laranja sobre palco azul e o contraste mais forte que existe, e nao
custa nada porque ja esta na foto.

## A tipografia, agora

| papel | fonte | por que |
| --- | --- | --- |
| Capa de ferramenta | **Anton** | condensada pesada, caixa alta. E a que a referencia usa quando promete uma ferramenta. |
| Capa e slide de ensaio | **Newsreader** | serifada editorial, caixa baixa. Desenhada para tela, com italico. Baixada em `instagram/fontes/`. |
| Corpo | **Arimo** | metricas da Helvetica. Neutra, profissional, nao startup. |
| Prompt e etiqueta | **JetBrains Mono** | o bloco de prompt precisa de monoespacada de verdade. |

### A volta do Anton, e por que isso nao e contradicao

O `PERFIL.md` registra que eu propus Anton no comeco e ele foi
reprovado, porque a referencia da epoca era a Wind: editorial, sentence
case, laranja contido. Continua verdade para aquela referencia.

A referencia agora e outra e o objetivo do slide e outro. Capa de
ferramenta grita, capa de ensaio sussurra. Anton volta **so na capa de
ferramenta**. Nos slides de texto quem manda e Newsreader e Arimo.

Se um dia os dois estilos aparecerem no mesmo carrossel, e erro.

## O rosto: resolvido, e sem gerar nada

Ele mandou fotos reais do Alfredo em palco. Entao **nao se gera rosto de
pessoa viva**, se usa a foto que existe. Isso encerra a duvida que estava
aberta desde o 005.

O caminho tecnico: as fotos estao no chat, nao no disco daqui. Quando a
arte comecar, subir pelo widget do Higgsfield (`media_upload_widget`) e
usar como referencia de imagem, nunca pedir ao modelo que desenhe o rosto.

## Como se fala com o Higgsfield nesta linha

Regra dele, e esta certa: **o modelo desenha, a gente nao diagrama.**
O prompt conta a historia da cena e trava so quatro coisas:

1. o texto, letra por letra, com acento
2. as cores da marca
3. onde a tipografia mora (terco de baixo, largura inteira)
4. "no other text anywhere in the image"

Enquadramento, luz, angulo, profundidade e composicao ficam com ele.
Coordenada em prompt de imagem devolve arte morta.
