# Pasta de imagens do carrossel

Coloque aqui as imagens que entram nas artes. O gerador procura pelo
numero do slide.

## Como nomear

| Arquivo | O que faz |
|---|---|
| `recorte-04.png` | Sujeito **sem fundo** (PNG com transparencia) colado sobre a cor. O titulo passa por tras dele. |
| `foto-04.jpg` | Foto **com fundo**, entra numa moldura inclinada em duotone. |

O numero e o do slide. `recorte-01` vai no slide 1, `recorte-04` no slide 4.

Slide sem imagem nao quebra: a arte usa so as texturas graficas.

## Como usar

```
python instagram/scripts/criar_slides.py conteudo/002-quanto-mais-tempo.txt --estilo poster --fotos fotos
```

## Por que voce precisa baixar na mao

O ambiente do Claude Code na nuvem bloqueia o CDN do Higgsfield (403 no
proxy), entao ele gera a imagem mas nao consegue trazer o arquivo.

O caminho e: voce baixa, salva aqui, e faz commit. No proximo `git pull`
do lado dele o arquivo aparece, e a partir dai ele monta e confere a arte
com a imagem de verdade.
