# Como usar o Claude sem queimar dinheiro

Observado nesta conta, não teoria. Cada item aqui aconteceu.

---

## A regra que vale mais que todas as outras

> **Conversa nova para tarefa nova.**

Toda mensagem reprocessa a conversa inteira desde o começo. Numa conversa
longa, uma pergunta de dez palavras custa o mesmo que reler tudo o que
já foi dito. Uma conversa de quatro horas cobra caro por "oi".

Isso parece um problema porque você perderia o contexto. Não perde, e é
exatamente por isso que existem as skills.

**O contexto não mora na conversa, mora no repositório:**

| arquivo | o que guarda |
| --- | --- |
| `.claude/skills/wr-copy/` | como escrever a copy |
| `.claude/skills/wr-arte/` | como gerar as artes |
| `marca/PERFIL.md` | público, pilares, tom |
| `marca/SISTEMA.md` | cores, tipografia, formato |
| `conteudo/APRENDIZADO.md` | o que ele escolheu e o que cortou |

Numa conversa nova eu leio o que preciso e começo trabalhando. Uma
conversa nova pedindo carrossel custa uma fração do que custa a mesma
pergunta no fim de uma conversa longa.

**Quando continuar na mesma conversa:** enquanto está mexendo na mesma
coisa. Ajustar a copy que acabou de sair, corrigir a arte que acabou de
ser gerada.

**Quando abrir nova:** assunto novo. Post novo, tema novo, problema novo.

---

## Imagem é o que mais pesa

Uma imagem no chat custa cerca de 1.500 unidades. Oito slides custam
12.000. Três rodadas de ajuste custam 36.000 só para eu olhar arte.

| em vez de | faça | economia |
| --- | --- | --- |
| mandar 8 slides soltos | uma folha com os 8 juntos | 8x |
| mandar 11 imagens novas | zipar e mandar o zip | quase tudo |
| mandar print do erro | escrever o que está errado | quase tudo |
| eu conferir os 8 slides | eu conferir só o que mudou | 4x |

**Zip não custa token de imagem.** E vem em qualidade cheia, o que me
deixa achar defeito que no chat comprimido eu não acho: foi assim que
apareceram as três imagens com sombra virada em mancha preta.

---

## Descrever em vez de mostrar

O que você percebe, você fala. O que é técnico, deixa eu ver.

**Funciona muito bem:**
- "slide 5, o texto encosta na imagem"
- "essa copy não parece minha"
- "o slide 3 tá vazio"

Isso me diz onde procurar e vale mais que a imagem, porque já vem com o
diagnóstico.

**Precisa da imagem:**
- defeito que você não tem como saber que é defeito
- julgamento de qualidade fina

---

## O que desperdiçou de verdade aqui

Registrado para não repetir:

1. **Meses de design em CSS** quando o modelo de imagem fazia melhor em
   um passo. O erro não era a ferramenta, era o briefing: eu mandava
   coordenada quando devia contar a história.
2. **Ciclos de conferência de arte inteira** quando só um slide mudou.
3. **Tentar baixar imagem** que a rede daqui não alcança. Testei três
   caminhos antes de aceitar que o zip tem que passar por você.
4. **Perguntar o que já estava escrito** no PERFIL.md.
5. **Colar dois comandos de uma vez** no PowerShell. Eles grudam
   (`--fotos fotosexplorer C:\...`) e o erro parece do script. Um
   comando, um Enter, espera terminar.
6. **Nomear arquivo copiando a tabela inteira** que eu escrevi, seta e
   tudo. Quando eu passar nome de arquivo, passo o nome cru.

---

## O fluxo mais barato para um post

```
conversa nova
  você: "quero um post sobre X"
    eu: 5 ideias com gancho
  você: escolhe uma
    eu: copy + legenda
  você: aprova ou aponta em texto
    eu: as 4 artes, mostradas de uma vez
  você: aprova ou diz qual refazer
    eu: refaço só aquela, e publico
```

Sem print, sem zip, sem download. A arte aparece no visualizador e você
lê dali.
