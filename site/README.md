# Site da assessoria

Landing page estática. Sem build, sem dependência: HTML, CSS e um arquivo de
JavaScript. Abrir `index.html` já mostra o site pronto.

```
site/
├── index.html
└── assets/
    ├── style.css
    └── app.js
```

Para ver com servidor local: `npx serve site`

---

## A ideia

A página é **uma cena só**, não uma pilha de blocos. Uma constelação de
triângulos vive atrás de tudo e nunca sai da tela — o que muda é a forma que ela
assume conforme você rola:

| Momento | Forma | O que diz |
|---|---|---|
| Hero | `curva` | uma fita que sobe: a verba voltando |
| Números | `dispersa` | a poeira cobre a tela inteira: a escala da carteira |
| Serviços | `marca` | **a constelação se monta na marca** |
| Relatório | `orbita` | tudo gira em volta de um centro |
| Depoimento | `onda` | a fala do cliente |
| Planos | `grade` | estrutura, opção, ordem |
| Fecho | `ponto` | tudo converge num ponto único e assenta |

Cada seção pede a forma pelo atributo `data-forma`. Quem manda é a seção que
estiver no centro da tela. As partículas não pulam: cada uma migra no seu próprio
tempo, então a troca de forma leva cerca de dois segundos e é ela que dá a
sensação de continuidade entre as seções.

**Trocar a marca é uma linha.** No topo de `app.js`:

```js
var MARCA = 'M11 13 20 35 24 23 28 35 37 13';   // traçado do W
var MARCA_CAIXA = 48;                            // viewBox do traçado
var MARCA_TRACO = 6.4;                           // espessura
```

Esse mesmo traçado desenha a logo no cabeçalho (`index.html`, dois lugares).
Colando aqui o `path` do arquivo real da WIND, a constelação passa a montar a
logo de verdade e o cabeçalho acompanha.

---

## Os outros movimentos

| Onde | O que acontece |
|---|---|
| Topo da página | fio laranja de 2px marcando o progresso da rolagem |
| Títulos | entram palavra por palavra, subindo de dentro de uma máscara |
| Números | contam de zero até o valor quando entram na tela |
| Serviços | a seção **trava na tela** por três alturas de viewport; a rolagem troca os três passos sem sair do lugar |
| Depoimento | a frase acende **palavra por palavra** conforme você desce |
| Clientes | letreiro contínuo que acelera quando você rola rápido |

Tudo isso desliga sozinho se o sistema pedir menos movimento
(`prefers-reduced-motion`), e a constelação para de animar quando sai da tela.

---

## O sistema visual

Base: `DESIGN_teste_2.md` (Dala). Acento trocado do âmbar para o **laranja da
marca**, porque a identidade em `marca/SISTEMA.md` já é laranja e preto.

| Regra | Como aparece |
|---|---|
| Preto puro em tudo | Nenhum card, nenhuma sombra |
| Hierarquia por escala, nunca por peso | **Todo título é peso 400** |
| Corpo em peso 200 | 18px ultraleve |
| Violeta `#8052ff` só em botão preenchido | Menu, hero e envio. Mais nada |
| Laranja `#ff6b1a` para rótulo, número e preço | O único outro cromático da interface |
| Texto na esquerda, constelação na direita | Nunca se sobrepõem |

### A escala é fechada

Oito degraus, declarados no topo do `style.css`. Nada na página usa tamanho fora
desta lista:

| Classe | Tamanho | Peso | Onde |
|---|---|---|---|
| `.t-display` | 113px | 400 | título do hero e os números |
| `.t-hlg` | 78px | 400 | abertura de seção |
| `.t-h` | 48px | 400 | depoimento |
| `.t-hsm` | 42px | 400 | título de item |
| `.t-h2xs` | 24px | 400 | preço, nome de cliente |
| `.t-body` | 18px | 200 | texto corrido |
| `.t-label` | 14px | 600 | rótulo em caixa alta |
| `.t-caption` | 12px | 400 | letra miúda |

O tracking é em `em`, nunca em `px`: a compressão acompanha o tamanho quando o
título encolhe no celular.

### O ritmo vertical

Base de 6px. Um conjunto só de medidas: **120px** entre seções, **96px** entre
itens, **60px** entre colunas, **36px** entre blocos, **30px** dentro de um
bloco, **24px** entre título e apoio, **12px** entre linhas de lista.

### No celular

O palco fixo dos serviços deixa de travar e os três passos empilham. A
constelação vai para o centro com opacidade menor, para não brigar com a leitura.

---

## O que ainda precisa de decisão sua

- **A logo de verdade** — hoje é o traçado que desenhei. Ver a seção da marca acima.
- **WhatsApp** — `5500000000000` em `index.html` e na constante `WHATSAPP` do `app.js`.
- **Preços** — R$ 1.500 e R$ 2.900 são exemplo.
- **Depoimento** — texto de exemplo. Trocar por fala real com autorização.
- **Lista de clientes** — veio de `marca/PERFIL.md`. Confirmar quem pode ser citado.
- **Formulário** — monta a mensagem e abre o WhatsApp. Para receber por e-mail,
  precisa de um serviço de formulário ou endpoint próprio.
- **Uma licença poética** — o sistema proíbe borda e não tem formulário. Os campos
  usam um fio de 1px embaixo, porque sem nenhuma marca ninguém entende onde
  clicar. É o único ponto onde saí da regra.
