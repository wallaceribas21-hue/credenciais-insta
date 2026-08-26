# Perfil de marca — @wallaceribas_

> Fonte da verdade para criação de conteúdo e design.
> Todo skill de copy ou design deve ler este arquivo antes de produzir qualquer coisa.
>
> **Status:** 🟢 base definida — refinando identidade visual
> **Última atualização:** 2026-08-20

---

## 1. Quem fala

| Campo | Valor |
|---|---|
| Conta | @wallaceribas_ |
| Tipo | Creator (MEDIA_CREATOR) |
| Nome | Wallace Ribas |
| Idade | 22 anos |
| Tempo de mercado | 2 anos como prestador de serviço de marketing |

**Trajetória:** já produziu eventos, imersões e vídeos de lifestyle no YouTube.
Hoje o conteúdo é sobre marketing, ideias, inovações e cases.

**Escala real da operação:** administra 33 Páginas do Facebook e dezenas de
contas de anúncio — WIND Company, Clínica Ômega, Fleury, CV Hotéis, The Barber
Exclusive, Ideal Alimentos, Berg Pneus, Topmake, entre outras.

> ⚠️ **Esse é o maior ativo de conteúdo dele e está subaproveitado.** Aos 22 anos
> com essa carteira, o diferencial não é "saber marketing" — é o **volume de
> casos reais** que ele vê por dentro toda semana. Conteúdo genérico de tráfego
> qualquer um faz; o que ninguém replica é o repertório de quem roda dezenas de
> contas ao mesmo tempo.

---

## 2. Para quem fala

Duas audiências, atendidas pelo mesmo perfil:

| Público | Quem é | O que quer | Como converte |
|---|---|---|---|
| **A. Donos de negócio local** | Clínicas, barbearias, hotéis, lojas | Vender mais, parar de queimar verba | Contrata serviço |
| **B. Jovens que querem empreender** | Quer viver de marketing, gosta de ver a rotina | Aprender a ser gestor, ter essa vida | Compra mentoria/formação |

**Ponto de atenção:** são públicos com dores diferentes. O dono de negócio quer
**resultado**; o jovem quer **caminho**. Um mesmo post raramente serve os dois
bem — melhor alternar do que tentar agradar os dois de uma vez.

---

## 3. Objetivo do conteúdo

Atrair os dois lados: novos clientes de serviço **e** pessoas que querem
aprender a viver de marketing.

---

## 4. Pilares de conteúdo

| # | Pilar | Do que trata | Público |
|---|---|---|---|
| 1 | **Cases reais** | O que funcionou (e o que quebrou) nas contas que ele roda | A |
| 2 | **Ideias e inovação** | Sacadas, testes, coisa nova que ninguém tá fazendo | A + B |
| 3 | **Bastidor / rotina** | Como é a vida de quem gerencia dezenas de contas aos 22 | B |
| 4 | **Ensino técnico** | Como fazer, passo a passo, o que estudar | B |

---

## 5. Tom de voz

⚠️ **Ainda não definido.** Ele descreveu como "um mix" e nunca fez carrossel.

**Como vamos resolver:** definir na prática. Os primeiros carrosséis vão testar
tons diferentes, e o que performar melhor (salvamento e comentário, não curtida)
vira o padrão. Este campo se preenche com dado, não com achismo.

**Ponto de partida sugerido:** direto e concreto, apoiado em número e caso real —
porque é o que a carteira dele permite e ninguém consegue copiar.

---

## 6. Identidade visual

### Cores

**Laranja e preto.** Foi a identidade das duas empresas anteriores dele, e ele
quer manter — já associa a ele.

| Uso | Hex | Observação |
|---|---|---|
| Preto base | `#0A0A0B` | fundo principal |
| Laranja marca | `#FF6B1A` | destaque, números, CTA |
| Branco texto | `#FFFFFF` | títulos |
| Cinza apoio | `#9A9AA0` | texto secundário |

> Hex ainda **provisórios** — definidos por mim, aguardando validação visual.

### Tipografia

**Montserrat** (300 / 400 / 600 / 700 / 800), embutida no repositório em
`instagram/fontes/` — funciona sem internet.

A escolha veio da referência: a Wind usa uma geométrica desse tipo, e o
recurso central não é a fonte em si, é o **contraste de peso dentro da mesma
frase**.

### Referência: @windcompany_

Wallace mandou o feed da Wind como o padrão de qualidade esperado.
O que extraí, olhando o grid:

| Elemento | O que a Wind faz |
|---|---|
| **Fundo** | Foto com gradiente escuro por cima — quase nunca cor chapada |
| **Tipografia** | Peso misto na mesma frase: "**As jogadas** de marketing **mais inteligentes**" |
| **Caixa** | Sentence case, **não** caixa alta |
| **Laranja** | Doses pequenas e cirúrgicas — selo, uma palavra, um sublinhado |
| **Selo** | Retângulo laranja com texto curto: "do último mês!", "10 PALAVRAS" |
| **Assinatura** | `WIND \| COMPANY` no topo, pequena, com letter-spacing largo |
| **Rodapé** | "Arraste para o lado" |

**O erro que eu tinha cometido:** minha primeira proposta era caixa alta
pesada (Anton), laranja como grande brilho de fundo, estilo racing. A Wind é
o oposto — editorial, sentence case, laranja contido. Corrigido.

### O que ainda falta

- **Fotos.** É a diferença estrutural. A Wind constrói tudo sobre imagem;
  sem foto, a metade de cima do slide fica vazia. Wallace precisa de um banco
  de imagens (próprias ou de banco gratuito).
- **Logo próprio.** Hoje a assinatura é o nome em texto. A Wind tem o "W".

---

## 7. Formato do carrossel

⚠️ **Primeira vez.** Nada validado ainda.

**Marcação do arquivo de texto** (`instagram/scripts/criar_slides.py`):

| Escrevo | Vira |
|---|---|
| `*palavra*` | laranja |
| `_palavra_` | peso leve — o contraste da Wind |
| `__palavra__` | sublinhado laranja |
| `[texto]` na 1ª linha | selo laranja |
| `---` | separa os slides |

**Estrutura de partida (6 slides):**

| Slide | Função |
|---|---|
| 1 | Capa — a promessa, o gancho |
| 2 | O problema / contexto |
| 3-5 | O conteúdo em si |
| 6 | CTA — salvar, comentar, seguir |

---

## 8. Referências analisadas

### @brandsdecoded__ — grid + o carrossel do Ogilvy aberto (25/08/2026)

> **Não abro o Instagram desta sessão:** a rede devolve 403 no CONNECT
> para `instagram.com`. Testado. Print é o caminho oficial, e é mais
> barato que o link de qualquer jeito.
>
> Métricas do post do Ogilvy, 4 dias no ar: **873 curtidas, 757
> comentários, 538 compartilhamentos, 5 reposts.** Comentário quase
> empatando com curtida é o número que interessa.
>
> ⚠️ As artes são geradas: a marca d'água **"Powered by Content Machine"**
> aparece no topo de todos os cards, e o retrato do slide 3 é uma pose que
> não existe em foto histórica. É pipeline de IA, não estúdio.

#### Anatomia da capa (corrigida — eu tinha invertido)

De cima para baixo, na ordem real:

| Posição | O que tem |
|---|---|
| Topo esquerdo | marca d'água da ferramenta, cinza, minúscula |
| Topo direito | @handle repetido, minúsculo |
| Quadro | retrato colorizado sangrando, o personagem olhando pra câmera |
| **Acima do título** | **a assinatura: bolinha laranja + @handle + selo azul, centralizada** |
| Título | condensada pesada caixa alta, 3 linhas, largura inteira, uma expressão em laranja |
| **Rodapé** | **barra preta com seta laranja `→` + uma linha em caixa alta menor** |

A assinatura fica **acima** do título, não no rodapé. E a linha de apoio
fica **abaixo** do título, dentro de uma barra preta chapada, aberta por
uma seta laranja. Era o contrário do que eu tinha escrito.

#### Anatomia do carrossel (5 slides)

| # | Fundo | Tipografia | Trabalho |
|---|---|---|---|
| 1 | retrato sangrando | condensada caps + barra preta | o gancho |
| 2 | **bege claro** | **serifada editorial grande**, caixa baixa, nome em laranja | quem é o personagem e por que ele importa |
| 3 | foto no topo, **bloco preto** embaixo | sans branca + lista com setas `→` | o que a ferramenta faz |
| 4 | bege claro | sans bold + **caixa monoespaçada** | **o prompt inteiro, de graça** |
| 5 | não capturado | — | provável CTA |

**A lição que vale mais que o layout:** o slide 4 entrega a ferramenta
completa, sem pedir comentário, sem link na bio, sem e-mail. E mesmo
assim deu 757 comentários. Reter a entrega não é o que gera conversa;
entregar coisa boa demais é.

**A troca de fundo é o ritmo.** Preto, bege, preto, bege. Igual à regra
de alternância que já está no `SISTEMA.md`, só que com bege no lugar do
branco.

#### O que dá e o que não dá pra puxar

**Dá:** a estrutura de 5 slides, a alternância de fundo, a assinatura
acima do título, a barra preta com seta, e a entrega da ferramenta
inteira no slide 4.

**Não dá:** o ângulo de revista. Eles decodificam o mercado **de fora**,
lendo notícia sobre gente morta ou gigante. O Wallace decodifica **de
dentro** de 33 páginas e dezenas de contas de anúncio. Se copiar o
ângulo, vira mais uma conta que comenta o mercado. Se usar a forma com o
dado da carteira, não tem concorrente.

#### Restrição nova: personagem vivo

Ogilvy morreu em 1999 e o rosto dele é material histórico. Se o
personagem for **um empresário vivo**, gerar o rosto dele em modelo de
imagem é fabricar foto de pessoa real. Não fazemos isso. Os caminhos
honestos são três, nesta ordem de preferência:

1. **Pedir a foto por direct**, explicando o post. Custa uma mensagem e
   é o jeito mais garantido de a pessoa ver o carrossel.
2. **Foto de imprensa dele**, com crédito visível no card.
3. **Não mostrar o rosto**: uma cena que carrega o conceito, e o nome só
   na tipografia.

---

## Como usar este arquivo

1. O tema tem que caber num **pilar** (seção 4) e mirar **um público** (seção 2)
2. Os slides usam as **cores** (seção 6)
3. A estrutura segue o **formato** (seção 7)

Se algo não estiver definido aqui, **pergunte antes de inventar**.
