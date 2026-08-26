# O que a wr-copy aprendeu

Ler antes de gerar ideias. O que ele **edita** vale mais que o que ele
elogia: elogio é educação, corte é preferência.

---

## 001 — IA postou sozinho
Família do gancho: confissão + prova ("esse post não fui eu que fiz")
Publicado. Post ID `18081723827691045`.
Resultado: ainda não medido.

## 002 — Quanto mais tempo
Família do gancho: confissão ("pedi um post e veio horrível")
Escrito, não publicado.

---

## Padrões observados até aqui

- Ele reclama de legibilidade antes de qualquer outra coisa. Texto que
  não lê de primeira é o defeito que ele enxerga primeiro, sempre.
- Ele quer imagem em tudo. Slide sem imagem ele chama de vazio.
- Ele corta enrolação. Explicação longa antes do ponto ele não aceita.
- Pede economia de token com frequência: entregar direto vale mais que
  entregar completo.

## Ainda sem dado

- Qual família de gancho ele escolhe quando tem cinco na frente
- Se ele edita a copy antes de publicar, e o quê
- O que performa: salvamento, comentário ou direct

---

## 003 — A IA aprende o meu estilo
Escolheu: **confissão** ("pedi um post pra IA e veio horrível")
Descartou: contra-senso, número seco, bastidor, pergunta que acusa
Pediu: **4 slides** no lugar de 8
Formato: **só o de capa** (foto sangrando + texto por cima). Viu os três
e reprovou "texto + 1 imagem" e "texto + 2 imagens".
Copy: aprovada sem edição nenhuma. Primeira vez que isso acontece.
Arte: aprovada de primeira, no Higgsfield.
**Publicado.** Post ID `18175135111439230`.

Editou a legenda duas vezes, e as duas viraram regra:
1. Tirou as linhas em branco entre parágrafos. Acha horrível o texto
   esparramado.
2. Cortou de 1397 para 646 caracteres e trocou o ângulo: a legenda
   também foi escrita pela IA, e o ponto é fazer reparar no nível do
   post inteiro. A prova deixou de ser contada e passou a ser a própria
   coisa que a pessoa está lendo.

## A virada que vale mais que o resto

Ele apontou o erro que eu vinha repetindo: **eu estava preso em montar
design em CSS quando o modelo de imagem fazia melhor.** E a correção não
era trocar de ferramenta, era trocar o briefing.

Prompt que trava o modelo:
> "objeto no topo ocupando 55%, texto embaixo alinhado à esquerda"

Prompt que solta:
> "THE STORY: o momento em que quase todo mundo desiste e ele não.
>  Você escolhe a imagem que carrega isso."

Mesma ferramenta, mesmo custo. Resultado incomparável.

## Padrão confirmado

- Ele decide rápido quando vê, e trava quando lê descrição.
  **Mostrar sempre vale mais que explicar.**
- Ele pede economia de token em quase toda mensagem. Entregar direto
  vale mais que entregar completo.

---

## A fórmula do post de prompt (investigada, não deduzida)

Wallace mandou investigar de onde a `@brandsdecoded__` tirou o prompt do
Ogilvy. Resposta: **eles não inventaram nada.**

O memorando é real. David Ogilvy mandou "How to Write" para todos os
funcionários da Ogilvy & Mather em **7 de setembro de 1982**, com 10
regras. Está documentado no Open Culture, no Farnam Street e em uma
dezena de outros lugares. As 10 regras numeradas dentro do prompt deles
são tradução quase literal das regras originais:

| No prompt deles | Regra original |
|---|---|
| escreva como uma pessoa fala | 2. write the way you talk |
| palavras e frases curtas | 2. short words, short sentences |
| elimine jargões | 3. never use jargon words |
| verifique citações | 5. check your quotations |
| trechos que melhoram na segunda leitura | 6. read it aloud the next morning |
| deixe claro o que o leitor faz depois | 7. make it crystal clear |
| diga quando escrever não é o formato | 10. if you want ACTION, don't write |

**O que eles construíram foi o invólucro**, não o conteúdo: a estrutura
de saída (DIAGNÓSTICO GERAL, PROBLEMAS CRÍTICOS, O QUE JÁ FUNCIONA,
CORTE, CLAREZA DA AÇÃO, NOTA FINAL) e a regra final que preserva a voz
de quem escreveu.

### A regra que fica

> **Documento real + invólucro de execução.**
> A autoridade vem de um artefato verificável que existe fora do post.
> A utilidade vem da estrutura que a gente escreve por cima.
> Princípio inventado e atribuído a alguém não é nenhum dos dois: é
> palpite com nome famoso em cima, e derruba o post se alguém checar.

**Eu quebrei essa regra na primeira versão do 005.** Escrevi sete
princípios "no jeito do Alfredo Soares" e atribuí a ele. Nenhum saía de
documento nenhum. Wallace percebeu antes de publicar.

A correção veio do próprio Alfredo: o livro **"Todos somos uma marca"**
(Editora Gente, 2023) tem no subtítulo o framework inteiro, e ele é
exatamente sobre conteúdo que vende. Quatro etapas declaradas na obra:
**audiência, demanda, conversão, retenção**, por meio de **influência,
conteúdo e experiência**. Documento real, verificável, e sobre o assunto
certo.

### Cuidado com cargo atual

Bio de palestrante e página de livraria envelhecem. Encontrei "presidente
da Loja Integrada" em várias fontes, mas a mais específica dava agosto de
**2018**. Não dá pra afirmar cargo atual daqui. A copy usa só o que é
datado e checável: Xtech em 2014, R$ 547 milhões em três anos, venda para
a VTEX em 2017, cofundação do G4 em 2019, três livros.

---

## Segunda ref: a mesma conta postou sobre o Alfredo (print de 26/08)

Carrossel de 6 slides, "O empresário que posta 12x por dia e fatura 500
milhões. estratégia genial ou tiro no pé?".

### O número que interessa

| | post do Ogilvy | post do Alfredo |
|---|---|---|
| curtidas | **873** | **352** |
| formato | entregou o prompt pronto | só decodificou a estratégia |

Menos da metade das curtidas. O recorte não deixa ler o número de
comentários do post do Alfredo, então não dá pra comparar essa coluna,
mas a diferença de curtida na mesma conta e no mesmo mês já diz o
suficiente:

> **Decodificar rende menos que entregar a ferramenta.** O post que dá
> uma coisa pra pessoa usar hoje ganha do post que explica o que outra
> pessoa faz.

Isso confirma o caminho do 005: o prompt fica.

### As duas capas da conta, e quando cada uma entra

Eu tinha lido isso errado como "serifada quando o assunto é luxo". Não é.

| tipo de post | tipografia da capa |
|---|---|
| **ferramenta** (Ogilvy + prompt) | condensada, caixa alta, urgente |
| **ensaio / análise** (Alfredo, YSL) | serifada editorial, caixa baixa |

Ogilvy é pessoa e usou condensada; Alfredo é pessoa e usou serifada. O
que separa não é o assunto, é a **promessa**. Utilitário grita, ensaio
sussurra. O 005 é ferramenta, então condensada está certo.

### O mecanismo que eles decodificaram, e que vale ouro

A leitura deles do método do Alfredo: ele **amplia a fonte de pautas**.
Rotina, negócios, conversas, notícias e acontecimentos do mercado viram
ponto de partida. Depois ele **interpreta o acontecimento pela ótica de
quem vende e opera empresas**.

> "Assuntos amplos permitem entrar em conversas maiores do que 'como
> vender melhor'. Mas a interpretação quase sempre devolve o público
> para seus territórios."

E a frase que fecha: **não precisa começar todo conteúdo ensinando uma
técnica de vendas.**

Isso entrou no prompt do 005. A seção OS PRÓXIMOS 5 POSTS agora proíbe
começar por técnica e exige que cada post parta de um acontecimento de
fora do nicho, com a leitura vindo depois. O prompt deixou de só auditar
o passado e passou a gerar pauta.

### A prova certa para o nosso ângulo

Meu slide 2 provava o Alfredo com venda (Xtech, VTEX, R$ 547 milhões).
Mas o nosso carrossel é sobre conteúdo, e para isso a prova é outra:
**mais de 12 mil publicações e 1,6 milhão de seguidores.** Volume próprio
mata a pergunta "por que eu ouviria ele sobre isso". Corrigido.

### Cargo: resolvido pela bio dele

A bio do @alfredosoares diz: pai da Antônia, autor de 4 best-sellers,
cofundador do @g4.business, sócio na VTEX, Loja Integrada e CRM Bônus.
Então não é "presidente da Loja Integrada" hoje, é **sócio**. A copy usa
cofundador do G4 e autor de quatro best-sellers, que é o que a fonte
dele mesmo afirma.

---

## 008 — a regra de tamanho que eu vinha quebrando

Ele leu o carrossel e disse que so entendeu os slides 4 e 5. Os dois que
tinham **uma ideia so cada**. Os slides 2 e 3, que eu tinha escrito com
tres ou quatro paragrafos, nao passaram.

O diagnostico dele veio na mesma mensagem: *"ta muito grande os textos,
mesmo que possa ser mais escrito nao pode ficar tao poluido com so
texto"*.

> **Slide de carrossel aguenta uma ideia, nao tres.**
> Se voce precisa de tres, sao tres slides.

Numeros que passam a valer:

| slide | teto |
| --- | --- |
| capa | 12 palavras no titulo, mais a barra |
| corpo | **entre 20 e 35 palavras** |
| fecho | 25 palavras |

O 008 foi de 5 slides pesados para 6 slides leves. Nenhum passa de 34
palavras. A copy encolheu quase pela metade e nao perdeu nenhuma ideia,
porque o que saiu era ligacao entre ideias, e ligacao quem faz e o
arrasto do dedo, nao o texto.

**Eu vinha escrevendo ensaio e chamando de carrossel.** O erro apareceu
em todas as versoes anteriores e ele reclamou de legibilidade tres vezes
antes de eu ouvir. O `APRENDIZADO` ja dizia na primeira linha: *ele
reclama de legibilidade antes de qualquer outra coisa*.

## E a imagem nao e enfeite, e metade do slide

Regra nova dele: **toda arte tem imagem, inclusive as de texto.** Imagem
de fundo, complementar, nao decorativa. Slide de cor chapada com texto em
cima ele chama de vazio, e ja chamou antes.

As fotos do Alfredo em palco foram liberadas por ele para producao de
conteudo positiva, e ele autorizou alterar em IA. Entao a foto real entra
como **base** e o Higgsfield trabalha por cima, em vez de inventar rosto.

---

## 010 — aprovado de primeira depois de nove tentativas

"ficou incrivel, boa demais". Vale entender o que fez esse funcionar,
porque foram nove versoes ate chegar nele.

### O erro que se repetiu nove vezes

**Eu tratava cada correcao dele como motivo pra recomecar do zero.**
Ele apontava um slide e eu trocava o carrossel inteiro: personagem,
tese, formato. A frase que resolveu foi dele:

> "irmao vc nao precisa mudar a historia, estamos apenas modelando"

**Regra nova: correcao mexe so na peca apontada.** Se eu achar que
precisa mexer em mais, pergunto antes em vez de reescrever.

### O que a historia precisava, e que faltava em todas as versoes

A trajetoria estava certa desde o comeco. Faltava a **diferenciacao
real**, e ela nao estava em nenhuma frase dele, estava na trajetoria:

**Alfredo e publicitario.** Antes da Xtech ele tinha o Marketing Shop,
uma agencia que fazia de arte grafica a site para empresa pequena. Em
2014 trocou a agencia, que dava lucro, pela plataforma. Os concorrentes
dele eram empresas de tecnologia; ele era o unico que ja tinha passado
anos fazendo o marketing daquele mesmo dono de loja.

> Quem entende o cliente ganha de quem entende o produto.

Diferenciacao boa nao e uma frase que a pessoa disse. E uma coisa que
aconteceu e que ninguem tinha ligado.

### As perguntas aceleram

Ele disse: *"eu gosto bastante do trabalho com perguntas suas pois
acredito que te deixe mais assertivo"*. Confirmado na pratica. As tres
perguntas antes do 010 cortaram mais caminho que as nove versoes
anteriores juntas.

**Perguntar antes de escrever, sempre.** E perguntar sobre decisao, nao
sobre aprovacao.

### O formato que ficou de pe

| slide | funcao |
| --- | --- |
| 1 | capa: fato estranho + o numero que paga o fato, nome na barra |
| 2 | contexto curto |
| 3 | a escolha, com tensao |
| 4 | a sacada, terminando na frase que a pessoa leva |
| 5 | o prompt inteiro |
| 6 | CTA de diagnostico |

Prompt e CTA juntos foi escolha dele: o prompt rende salvamento, o CTA
abre o direct. Nenhum slide passa de 42 palavras.
