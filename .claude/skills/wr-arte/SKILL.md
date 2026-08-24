---
name: wr-arte
description: >
  Gera as artes do carrossel do @wallaceribas_ no Higgsfield, com o texto já
  dentro da imagem. Use quando ele pedir arte, card, imagem do carrossel,
  "gera as artes", "faz o visual", ou depois que a copy da wr-copy for
  aprovada. Formato 4:5. O prompt conta a HISTÓRIA do slide, nunca o layout.
---

# WR-ARTE — o Higgsfield desenha, eu não

> Modelo de imagem não é diagramador. Se você mandar coordenada, ele trava
> e devolve arte morta. Se você contar o que a cena significa, ele resolve
> melhor do que você pediria.

Isso foi aprendido caro: semanas montando slide em CSS quando o modelo
fazia melhor em um passo. O erro não era a ferramenta, era o briefing.

---

## O MODELO

`nano_banana_pro` — Google, tag `text-rendering`, aceita 4:5 e 2K.

⚠️ **Ele cai em `nano_banana_2` na conta atual.** Testado nos dois modos:
com saldo ilimitado o servidor recusa (*"Unlimited generations aren't
supported"*), com crédito ele aceita mas roda o 2. O 2 escreveu português
com acento corretamente, então serve. Confira o campo `model` na resposta
antes de afirmar qual rodou.

Não use `recraft_v4_1` para arte com texto. Ele escreveu "PRRA" no lugar
de "PRA" e inventou palavras que ninguém pediu.

---

## A ESTRUTURA DO PROMPT

Quatro blocos, nesta ordem. Os dois do meio são o que faz funcionar.

```
1. Create a striking 4:5 social media card for a Brazilian
   marketing entrepreneur.

2. THE STORY: <o que o slide significa, em sentimento, não em objeto>
   You choose the image that carries that feeling.
   Cinematic still, not stock photography. Deep shadows, one light
   source, real texture.

3. BRAND: near black background, one accent of vivid orange #FF6B1A,
   white type.

4. TYPE, exactly as written, heavy condensed uppercase sans-serif,
   very large, lower third:
   "<TITULO EXATO>"
   with only the word <PALAVRA> in orange.
   Underneath, one small line in neutral grotesque, light grey:
   "<linha de apoio exata>"
   Tiny monospaced WALLACE RIBAS top left.
   Tiny monospaced 0N/0T bottom left.
   Spell every Portuguese word letter by letter exactly as given,
   accents included. No other text anywhere in the image.
```

### O que FIXAR e o que SOLTAR

| fixar sempre | soltar sempre |
|---|---|
| cores da marca | qual objeto aparece |
| texto, letra por letra | enquadramento |
| onde a tipografia mora | luz, ângulo, cenário |
| "no other text anywhere" | como a imagem conta a história |

**"THE STORY" descreve sentimento, não coisa.** Escreva "o momento em que
quase todo mundo desiste e ele não desistiu, uma estrada que continua
depois de onde os outros voltaram" e não "uma estrada com um carro".

O modelo escolhe melhor que você quando entende o porquê.

---

## OS FORMATOS DE CARD

| formato | quando |
|---|---|
| **capa** — foto sangrando, texto por cima no terço de baixo | o padrão dele. Foi o único que aprovou. |
| **texto + 1 imagem** | uma ideia, um objeto |
| **texto + 2 imagens** | comparação, antes e depois |

Comece sempre pela capa. É o que ele escolheu quando viu os três.

---

## VERIFICAÇÃO — obrigatória

Modelo de imagem desenha forma de letra, não escreve. Português com
acento erra mais.

**Nunca diga que a arte está pronta sem alguém ter lido as palavras.**
Se você não consegue ver a imagem, mostre com `show_generation_by_ids`
e peça a leitura dele, apontando as palavras de risco (as com acento e
as em cor de destaque).

Se uma errar: refaça **só aquela**, não o lote.

---

## O FLUXO

1. Copy aprovada pela `wr-copy`
2. Um prompt por slide, seguindo a estrutura acima
3. `generate_image_batch` com todos de uma vez
4. `jobs_wait` até terminar
5. `show_generation_by_ids` — ele vê e lê
6. Refaz só o que falhou

**Não baixe as imagens para verificar.** A rede daqui não alcança o CDN
do Higgsfield e os hosts de arquivo caem. Mostrar no widget e pedir a
leitura dele custa quase nada e é mais confiável.
