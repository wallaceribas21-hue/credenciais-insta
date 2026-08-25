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

### O feed de decodificação de marca — print de 25/08/2026

> Handle lido do print: `@brandsdecoded` (confirmar com ele).
> **Não abro o Instagram desta sessão:** a rede devolve 403 no CONNECT
> para `instagram.com`. Testado. O print resolve melhor e mais barato
> que o link, então o print é o caminho oficial.

Oito capas no grid. O que se repete em todas as oito:

| Camada | O que a conta faz |
|---|---|
| **Fundo** | Still cinematográfico sangrando o quadro inteiro. Nunca cor chapada, nunca recorte. |
| **Véu** | Degradê preto subindo do rodapé até a metade. O texto sempre nasce dentro dele. |
| **Kicker** | Uma linha pequena, sentence case, cinza claro, **acima** do título. É ela que dá o contexto que o título não dá. |
| **Título** | Condensada pesada, caixa alta, terço inferior, 3 ou 4 linhas, largura inteira. |
| **Destaque** | **UMA** expressão do título em laranja. Sempre o sujeito da frase: TIKTOK SHOP, PAGODE, MARKETING, DAVID OGILVY. |
| **Assinatura** | Rodapé centralizado: bolinha laranja + @handle + selo. Discreta, sempre no mesmo lugar. |
| **Fórmula do título** | "COMO X VIROU Y", "POR QUE X", "O QUE X EXPLICA SOBRE Y". Decodifica um movimento, não ensina passo a passo. |

**A exceção que confirma a regra:** o card da YSL troca a condensada por
uma serifada editorial em caixa baixa. Quando o assunto é luxo, a
tipografia vira o assunto. É variação consciente, não inconsistência.

**O que dá pra puxar sem virar cópia:** a estrutura kicker + título +
destaque único + assinatura centralizada. Isso é forma, e forma se usa.

**O que não dá pra puxar:** o ângulo de revista. Eles decodificam o
mercado **de fora**, lendo notícia. O Wallace decodifica **de dentro** de
33 páginas e dezenas de contas de anúncio. Mesmo formato, autoridade
diferente. Se ele copiar o ângulo deles, vira mais uma conta que comenta
o mercado. Se usar a forma deles com o dado da carteira, não tem
concorrente.

---

## Como usar este arquivo

1. O tema tem que caber num **pilar** (seção 4) e mirar **um público** (seção 2)
2. Os slides usam as **cores** (seção 6)
3. A estrutura segue o **formato** (seção 7)

Se algo não estiver definido aqui, **pergunte antes de inventar**.
