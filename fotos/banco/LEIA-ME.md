# Banco de imagens

Recortes PNG com fundo transparente, no mesmo padrao visual: objeto unico,
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

O script acha `fotos/banco/cerebro.png`, apara a borda vazia, decide se a
imagem entra ao lado do texto ou numa faixa em cima (depende da proporcao
dela) e encolhe o titulo para nao passar por baixo.

Se o nome nao existir, ele avisa e lista o que tem. Nao renomeie arquivo
para encaixar num slide: quem manda na imagem e a copia.

## O que tem hoje

| arquivo | o que e | cabe bem em |
| --- | --- | --- |
| `relogio.png` | despertador mecanico antigo | tempo, prazo, urgencia |
| `pastas.png` | pilha de pastas de escritorio | processo, burocracia, acumulo |
| `telefone.png` | telefone de disco | atendimento, direct, contato |
| `maquina-escrever.png` | maquina de escrever | copy, escrita, conteudo |
| `cadeado.png` | cadeado de ferro aberto com a chave | destravar, liberar, acesso |
| `escada.png` | escada de madeira aberta | crescer, subir de nivel, etapa |
| `cerebro.png` | cerebro anatomico de gesso | inteligencia, aprendizado, IA |
| `engrenagens.png` | engrenagens de metal encaixadas | automacao, sistema, operacao |
| `mao-celular.png` | mao de estatua segurando celular | IA + humano, redes sociais |
| `caixa-registradora.png` | caixa registradora antiga | venda, faturamento, loja |
| `megafone.png` | megafone de metal | anuncio, trafego, alcance |

## Para gerar mais

Mesmo prompt base, so trocando o objeto:

```
Black and white studio photograph of <OBJETO>, single object centered,
isolated on pure flat white background, hard directional light from upper
left casting a crisp shadow, high contrast monochrome, sharp fine detail,
vintage editorial still life, no text, no logos
```

Modelo: Recraft V4.1, `model_type: utility`, `background_color: #FFFFFF`,
1:1, resolucao 2k. Depois recorte o fundo branco (o branco de fora, nao o
branco de dentro do objeto) e salve como PNG com transparencia.

Manter o mesmo prompt base e o que faz as imagens parecerem da mesma marca,
e nao um monte de foto solta.
