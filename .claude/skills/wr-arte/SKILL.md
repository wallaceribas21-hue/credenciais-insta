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
| **capa editorial** — kicker + título + destaque único, foto sangrando | **o padrão novo.** Vale para o carrossel inteiro, não só a capa. |
| **capa** — foto sangrando, texto por cima no terço de baixo | a versão anterior, sem kicker. Foi a que ele aprovou no 003. |
| **texto + 1 imagem** | uma ideia, um objeto |
| **texto + 2 imagens** | comparação, antes e depois |

Comece sempre pela capa editorial. Ele reprovou "texto + 1 imagem" e
"texto + 2 imagens" quando viu os três lado a lado.

---

## A CAPA EDITORIAL

Veio do feed de decodificação de marca que ele mandou como referência
(`marca/PERFIL.md`, seção 8). Quatro camadas, sempre nesta ordem de cima
para baixo:

```
        [ still cinematográfico sangrando o quadro ]
        [ degradê preto subindo do rodapé          ]
              ● @wallaceribas_
   TÍTULO CONDENSADO CAIXA ALTA
   EM TRÊS LINHAS, UMA DELAS
   COM UMA EXPRESSÃO EM LARANJA
   ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
   → A LINHA DE APOIO, CAIXA ALTA MENOR
```

A ordem importa e eu já errei ela uma vez: **a assinatura fica ACIMA do
título** e **a linha de apoio fica ABAIXO**, dentro de uma barra preta
chapada aberta por uma seta laranja. Não é kicker em cima.

Regras que fazem a diferença entre parecer a referência e parecer cópia
malfeita:

1. **A barra preta é o segundo gancho.** O título abre a lacuna, a barra
   diz o que a pessoa leva se arrastar. Máximo 10 palavras.
2. **Uma expressão em laranja por card, e ela é o sujeito da frase.**
   Duas expressões laranja e o card perde o ponto de foco.
3. **Título em 3 linhas de 2 a 4 palavras.** Linha de 6 palavras em
   condensada fica com corpo pequeno e some no feed.
4. **A assinatura é sempre igual, sempre no mesmo lugar.** É ela que faz
   oito posts diferentes parecerem uma conta só.

### Rosto de pessoa viva: não gere

Se o carrossel citar um empresário vivo, **não peça o rosto dele ao
modelo.** Isso é fabricar foto de pessoa real, e ainda por cima o modelo
erra a semelhança. Peça a foto por direct (é o jeito mais garantido de a
pessoa ver o post), use foto de imprensa com crédito, ou construa o card
sem rosto nenhum.

### Slide de texto denso: não é trabalho do modelo

Bloco de prompt, lista longa, qualquer coisa acima de umas 15 palavras:
faz no `criar_slides.py`. Modelo de imagem desenha forma de letra. Em 40
linhas ele erra em alguma, e uma letra errada dentro de um prompt quebra
o prompt. Carrossel bom costuma ser híbrido: foto no Higgsfield, texto
denso em CSS.

### O bloco 4 do prompt, para este formato

```
4. TYPE, exactly as written:
   One small line in light grey neutral grotesque, sentence case,
   sitting just above the headline:
   "<kicker exato>"
   Below it, the headline in heavy condensed uppercase sans-serif,
   very large, three lines, full width, lower third:
   "<TITULO EXATO>"
   with only "<EXPRESSAO>" in vivid orange #FF6B1A.
   Centered at the very bottom, small: a solid orange circle
   followed by "@wallaceribas_" in white.
   Spell every Portuguese word letter by letter exactly as given,
   accents included. No other text anywhere in the image.
```

O bloco 2 (THE STORY) continua sendo o que decide se a arte presta.
O degradê entra ali, não no bloco de tipografia:

```
   Cinematic still, full bleed, deep shadows, one light source, real
   texture. A black gradient rises from the bottom edge to the middle
   of the frame so the type reads clean over any image.
```

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
