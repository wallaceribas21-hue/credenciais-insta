# Site da assessoria

Landing page estática da Assessoria WR. Sem build, sem dependência: é HTML, CSS e
um arquivo de JavaScript. Abrir `index.html` no navegador já mostra o site pronto.

```
site/
├── index.html
└── assets/
    ├── style.css
    └── app.js
```

Para ver localmente com servidor (evita bloqueio de fonte em alguns navegadores):

```
npx serve site
```

## De onde vem o visual

O padrão veio de `DESIGN_teste_2.md` — o sistema escuro da Dala.

| Regra | Como aparece aqui |
|---|---|
| Preto puro `#000000` em tudo | Não existe painel, card, borda ou sombra na página inteira |
| Hierarquia por escala, nunca por peso | **Todo título é peso 400.** O que separa um título de outro é o tamanho |
| Corpo em peso 200 | 18px ultraleve — é a assinatura do sistema |
| Violeta `#8052ff` só em botão preenchido | Aparece no menu, no hero e no envio do formulário. Em nenhum outro lugar |
| Âmbar `#ffb829` para rótulo e ênfase | Todo rótulo em caixa alta e os preços |
| Duas colunas assimétricas | Título à esquerda, texto à direita, alternando o lado do visual |
| Sem grade de cards, sem tabela de preço | Serviços, método e planos são linhas de texto, não caixas |

### A escala é fechada

O erro da primeira versão foi ter tamanho de letra fora de uma escala. Agora só
existem **oito degraus**, declarados no topo do `style.css`, e nenhum elemento da
página usa tamanho fora desta lista:

| Classe | Tamanho | Peso | Onde |
|---|---|---|---|
| `.t-display` | 113px | 400 | título do hero |
| `.t-hlg` | 78px | 400 | abertura de seção |
| `.t-h` | 48px | 400 | depoimento |
| `.t-hsm` | 42px | 400 | título de item |
| `.t-h2xs` | 24px | 400 | pergunta, preço, nome de cliente |
| `.t-body` | 18px | 200 | texto corrido |
| `.t-label` | 14px | 600 | rótulo em caixa alta |
| `.t-caption` | 12px | 400 | letra miúda |

O tracking é declarado em `em`, não em `px`: assim a compressão do título
acompanha o tamanho quando ele encolhe no celular. Era isso que estava quebrado
antes.

### O espaçamento

Base de 6px, como o sistema pede. Um único ritmo vertical governa a página:

- **120px** entre seções (96px no celular)
- **96px** entre a abertura da seção e o conteúdo, e entre um item e o próximo
- **60px** entre as duas colunas
- **30px** entre rótulo, título, texto e botão dentro de um bloco
- **18px** entre um título e o subtítulo dele
- **12px** entre linhas de uma lista

Tipografia: Inter, a substituta indicada pelo sistema para a PPNeueMontreal,
nos pesos 200, 400 e 600.

## A constelação

A imagem da marca é desenhada em canvas por `app.js`: milhares de triângulos de
1px em violeta, âmbar, verde, magenta e azul. Duas formas:

- `data-constelacao="curva"` — no hero, uma fita que sobe da esquerda para a direita
- `data-constelacao="orbita"` — na seção do relatório, partículas convergindo para um ponto

A densidade acompanha o tamanho da tela, a animação para quando o canvas sai da
tela e some inteira se o sistema pedir menos movimento.

## O que ainda precisa de decisão sua

- **WhatsApp** — o número `5500000000000` aparece em `index.html` e na constante
  `WHATSAPP` de `assets/app.js`. Trocar nos dois lugares.
- **Preço dos planos** — R$ 1.500 e R$ 2.900 são exemplo, não proposta fechada.
- **Depoimentos** — os três textos são de exemplo. Substituir por fala real de
  cliente, com autorização, ou tirar a seção.
- **Lista de clientes** — os nomes vieram de `marca/PERFIL.md`. Confirmar quais
  podem ser citados publicamente antes de publicar.
- **Formulário** — hoje monta a mensagem e abre o WhatsApp. Para receber por
  e-mail, precisa de um serviço de formulário (Formspree, Netlify Forms) ou de um
  endpoint próprio.
- **Uma licença poética do sistema** — a Dala não tem formulário, e o sistema
  proíbe borda. Os campos usam só um fio de 1px embaixo, porque sem nenhuma marca
  ninguém entende onde clicar. É o único ponto onde saí da regra.
