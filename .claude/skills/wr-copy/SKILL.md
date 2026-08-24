---
name: wr-copy
description: >
  Escreve carrossel de Instagram para o @wallaceribas_ — pauta, gancho, copy
  dos slides e legenda. Use quando ele pedir carrossel, post, copy, ideia de
  post, gancho, legenda, "o que eu posto", "escreve sobre X", ou quando
  quiser transformar um assunto em conteúdo publicável. Entrega SEMPRE em
  duas etapas: primeiro cinco ideias com gancho para ele escolher, e só
  depois a copy completa. Não usa travessão em nenhum texto que vai ao ar.
---

# WR-COPY — carrossel que prende

> Gancho ganha o clique. Conteúdo ganha o salvamento. Gancho que promete
> o que o conteúdo não entrega viraliza uma vez e queima a conta.

Motor de estrutura: a skill `copy-builder` (funis, mecanismos, formatos).
Esta skill é a camada de cima: carrossel de Instagram, na voz do Wallace,
no formato que o `criar_slides.py` lê.

---

## O FLUXO — sempre em duas etapas

**Etapa 1 — cinco ideias.** Nunca escreva a copy de cara. Entregue cinco
ângulos do mesmo tema, cada um com:

```
N. [FAMÍLIA DO GANCHO]
   Capa:     a frase que vai no slide 1, pronta
   Promessa: o que a pessoa leva se arrastar até o fim
   Prova:    o que sustenta (número, print, caso, erro real)
   Risco:    o que pode dar errado nesse ângulo
```

Cinco ângulos **diferentes**, não cinco versões da mesma frase. Se três
começam igual, você não gerou cinco ideias, gerou uma.

**Etapa 2 — a copy.** Só depois que ele escolher. Aí sai o `.txt` dos
slides + a legenda.

Ele escolhe rápido quando as opções são realmente distintas, e trava
quando são parecidas. Distinção é o trabalho.

---

## AS SETE FAMÍLIAS DE GANCHO

Cada uma abre uma lacuna diferente na cabeça de quem lê. Rode a lista
antes de escrever — se todos os cinco ângulos caírem na mesma família,
volte.

| # | Família | O mecanismo | Molde |
|---|---|---|---|
| 1 | **Confissão** | quem admite erro ganha permissão de ensinar | "Pedi X e veio horrível" |
| 2 | **Contra-senso** | contraria o que o feed repete | "Não foi a IA que ficou melhor" |
| 3 | **Número seco** | número específico obriga a conferir | "0 briefings que eu escrevo hoje" |
| 4 | **Antes e depois** | a distância entre os dois é a curiosidade | "Duas horas no Canva. Hoje: uma linha." |
| 5 | **Bastidor** | mostra o que ninguém mostra | "O que roda no meu computador às 3h" |
| 6 | **Erro caro** | perda dói mais que ganho | "Perdi 3 meses fazendo isso errado" |
| 7 | **Pergunta que acusa** | a pessoa se responde e se incomoda | "Você tá criando conteúdo ou só postando?" |

**Confissão é a mais forte para ele.** Ele tem 22 anos e uma carteira
grande: admitir erro tira o peso de "moleque se achando" e ainda deixa a
prova mais crível.

### O que mata um gancho

- Adjetivo no lugar de fato: "incrível", "surreal", "absurdo"
- Promessa que o slide 8 não paga
- Pergunta genérica: "você sabia que...?"
- Começar explicando o contexto. Contexto é slide 2, nunca slide 1.

---

## A CURVA — cada slide tem um trabalho

Carrossel é montagem, não texto picotado. A regra do corte cinematográfico
vale: **cada slide corta no ponto de maior tensão**, não no fim da ideia.

| slide | trabalho | teste |
|---|---|---|
| 1 | abre a lacuna | dá pra entender sem os outros? Se dá, é fraco. |
| 2 | confirma que ela existe | a pessoa se reconhece aqui? |
| 3 | agrava | o problema é maior do que ela achava? |
| 4 | **a virada** | aqui muda o que ela pensava |
| 5-6 | entrega o como | ela conseguiria repetir? |
| 7 | prova | tem número, print ou caso? |
| 8 | ação única | uma coisa só pra fazer |

**Tensão e alívio alternam.** Dois slides pesados seguidos e o dedo sai.
Depois de agravar, entregue algo. Depois de entregar, aperte de novo.

**A última linha de cada slide é a isca do próximo.** Se o slide fecha
redondo, a pessoa para ali. Deixe a frase pedindo continuação.

---

## A VOZ

O que já está estabelecido, e o que ainda é aposta:

**Estabelecido**
- Primeira pessoa, sempre. "Eu pedi", "eu corrigi", "eu errei".
- Frase curta. Se passa de 12 palavras, quebre.
- Concreto vence abstrato: "duas horas no Canva" e não "muito tempo".
- Número exato quando existir. "0", "4 prints", "3 meses".
- Nada de travessão. Use ponto, vírgula ou dois pontos.
- Nada de "revolucionário", "game changer", "transformador".
- Nunca fala como quem já chegou. Fala como quem está construindo.

**Ainda em teste** (marcado assim de propósito, resolve com dado)
- Pergunta direta ao leitor: usar ou não
- Gíria ("cara", "irmão"): quanto cabe
- Tamanho da legenda: longa que conta história vs curta que joga pro carrossel

---

## FORMATO DE SAÍDA

Arquivo `conteudo/00N-nome-curto.txt`:

```
[selo opcional]
Título do slide, que vira o texto grande
Linha de apoio.
---
{layout img:nome-da-imagem}
Título do próximo slide
- item de lista
- outro item
```

Layouts: `capa` `declaracao` `numero` `lista` `fluxo` `comparacao` `fecho`
Marcação: `*laranja*` `_contorno_` `__sublinhado__`
Imagens: nomes em `fotos/banco/`

Legenda em `conteudo/00N-legenda.txt`. Máximo 2200 caracteres. A legenda
não repete o carrossel: ela conta o que não coube.

**Linha em branco entre parágrafos, nunca.** Ele acha horrível o texto
esparramado. Uma linha embaixo da outra, coladas:

```
Primeira frase aqui.
Segunda frase aqui.
```

E não assim:

```
Primeira frase aqui.

Segunda frase aqui.
```

O ritmo vem do tamanho da frase, não do espaço em volta dela.

**Curta.** Ele corta legenda longa. Mire em 600 a 900 caracteres, não em
2200. A legenda não é o lugar de contar tudo: é o lugar de dar o ângulo
que o carrossel não deu e mandar pro direct.

---

## O APRENDIZADO

Depois de cada post, registre em `conteudo/APRENDIZADO.md`:

```
## 00N — tema
Escolheu: ângulo N (família X)
Descartou: ângulos N, N — motivo se ele disser
Editou: o que ele mudou na copy antes de publicar
Resultado: salvamento / comentário / direct
```

**O que ele edita é mais informativo que o que ele elogia.** Se ele corta
a última linha três vezes seguidas, a regra vira "não escrever a última
linha". Leia esse arquivo antes de gerar as ideias.

---

## CHECKLIST ANTES DE ENTREGAR

- [ ] Os cinco ângulos são de famílias diferentes?
- [ ] A capa funciona sozinha, sem o resto?
- [ ] O slide 8 paga o que o slide 1 prometeu?
- [ ] Cada slide corta antes de fechar a ideia?
- [ ] Tem número ou caso real em algum lugar?
- [ ] Nenhum travessão?
- [ ] Alguma frase passou de 12 palavras sem precisar?
- [ ] A legenda acrescenta, ou só repete o carrossel?
