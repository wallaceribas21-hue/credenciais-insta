# Banco de imagens

Recortes WEBP com fundo transparente, no mesmo padrao visual: objeto unico,
preto e branco, luz dura vindo de cima a esquerda, sombra projetada.

## Como usar num carrossel

No arquivo de conteudo, escolha a imagem pelo nome:

```
{declaracao img:cerebro}
Nao foi a IA que ficou mais *inteligente*
Foi o _contexto_ que ela passou a ter.
```

Depois rode normalmente:

```
python instagram/scripts/criar_slides.py conteudo/003-seu-post.txt --estilo poster --fotos fotos
```

O script acha `fotos/banco/cerebro.webp`, apara a borda vazia, decide se a
imagem entra ao lado do texto ou numa faixa em cima (depende da proporcao
dela) e encolhe o titulo para nao passar por baixo.

Se o nome nao existir, ele avisa e lista o que tem. Nao renomeie arquivo
para encaixar num slide: quem manda na imagem e a copia.

## O que tem hoje

| arquivo | o que e | cabe bem em |
| --- | --- | --- |
| `relogio` | despertador mecanico antigo | tempo, prazo, urgencia |
| `pastas` | pilha de pastas de escritorio | processo, burocracia, acumulo |
| `telefone` | telefone de disco | atendimento, direct, contato |
| `maquina-escrever` | maquina de escrever | copy, escrita, conteudo |
| `cadeado` | cadeado de ferro aberto com a chave | destravar, liberar, acesso |
| `escada` | escada de madeira aberta | crescer, subir de nivel, etapa |
| `cerebro` | cerebro anatomico de gesso | inteligencia, aprendizado, IA |
| `engrenagens` | engrenagens de metal encaixadas | automacao, sistema, operacao |
| `mao-celular` | mao de estatua segurando celular | IA + humano, redes sociais |
| `caixa-registradora` | caixa registradora antiga | venda, faturamento, loja |
| `megafone` | megafone de metal | anuncio, trafego, alcance |

## Para gerar mais

Mesmo prompt base, so trocando o objeto:

```
Black and white studio photograph of <OBJETO>, single object centered,
isolated on pure flat white background, hard directional light from upper
left casting a crisp shadow, high contrast monochrome, sharp fine detail,
vintage editorial still life, no text, no logos
```

Peca sempre `absolutely no cast shadow on the background, no shadow`. A
sombra projetada sobrevive ao recorte do branco e vira uma mancha preta
solida ao lado do objeto.

Modelo: Recraft V4.1, `model_type: utility`, `background_color: #FFFFFF`,
1:1, resolucao 2k. Depois recorte o fundo branco (o branco de fora, nao o
branco de dentro do objeto), reduza para 1200px e salve como WEBP com
transparencia: fica 14x mais leve que o PNG sem diferenca visivel.

Manter o mesmo prompt base e o que faz as imagens parecerem da mesma marca,
e nao um monte de foto solta.
