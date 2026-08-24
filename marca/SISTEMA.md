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
