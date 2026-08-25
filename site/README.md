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

O padrão veio de `DESIGN_apple.md` — o sistema de página de produto da Apple.
As regras que estruturam tudo:

| Regra | Como aparece aqui |
|---|---|
| Fundo alterna `#ffffff` e `#f5f5f7` | Cada `<section>` usa `.band--paper` ou `.band--canvas`. É o que separa as seções — **não existe linha divisória.** |
| Sem sombra | Nenhum `box-shadow` no arquivo. Hierarquia vem do fundo e do raio. |
| Raio 28px em card e imagem | `--radius-cards`. Botão é pílula (`--radius-buttons: 980px`). |
| Azul só em botão preenchido | `#0071e3` apenas em `.btn--filled`. Link de texto usa `#0066cc`. Nenhum outro uso. |
| Título grande com tracking negativo | `.display` em 96px com `-1.44px`; `.heading` em 56px com `-0.28px`. |
| Corpo em 17px | `--text-body-sm`, peso 400, tracking `-0.022em`. |
| Cor vem da imagem, não da interface | Os campos pastel (`.field--citrus`, `.field--blush`, `.field--sky`) são o único lugar com cor. |
| Laranja `#b64400` uma vez por página | Só no selo "Novo" da seção de serviços. |

Tipografia: SF Pro quando existe no sistema (Mac e iPhone), Inter como
substituta em qualquer outro lugar.

## O que ainda precisa de decisão sua

Estes pontos estão preenchidos com valor de exemplo e precisam do número real
antes de o site ir ao ar:

- **WhatsApp** — o número `5500000000000` aparece em `index.html` (dois links) e na
  constante `WHATSAPP` em `assets/app.js`. Trocar nos três lugares.
- **Preço dos planos** — R$ 1.500 e R$ 2.900 são exemplo, não proposta fechada.
- **Depoimentos** — os três textos são de exemplo. Substituir por fala real de
  cliente, com autorização, ou tirar a seção.
- **Números do relatório** — os valores dentro dos cartões pastel (R$ 4.200,
  187 contatos) ilustram o formato do relatório; não são dado de conta real.
- **Lista de clientes** — os nomes vieram de `marca/PERFIL.md`. Confirmar quais
  podem ser citados publicamente antes de publicar.
- **Formulário** — hoje monta a mensagem e abre o WhatsApp. Se quiser recebimento
  por e-mail, precisa de um serviço de formulário (Formspree, Netlify Forms) ou
  de um endpoint próprio.
- **Política de privacidade e termos** — os links do rodapé estão vazios.
