# Banco de imagens para apresentações

Pasta única com tudo que deixa uma apresentação mais bonita: logo da Wind,
fotos do Wallace, fotos de eventos e bastidores. A ideia é nunca mais caçar
imagem na hora de montar slide — está tudo aqui, organizado.

## Estrutura

```
apresentacoes/
├── logos/        logo da Wind (PNG sem fundo, versões clara e escura)
├── wallace/      fotos do Wallace (retrato, palco, escritório)
├── eventos/      fotos dos eventos e imersões que ele produziu
├── bastidores/   rotina, escritório, gravações — o dia a dia
└── clientes/     logos e materiais de clientes (usar com cuidado em público)
```

## Como adicionar imagens

Qualquer um dos caminhos funciona:

1. **Pelo GitHub no navegador:** abra a subpasta → `Add file` → `Upload files`.
2. **Pelo chat com o Claude:** mande a imagem na conversa e diga em qual
   subpasta ela entra — ele salva, renomeia e faz o commit.
3. **Pelo computador:** copie os arquivos para a subpasta e faça commit.

## Padrão de nome

`o-que-e-onde-quando.ext` — tudo minúsculo, sem espaço nem acento.

Exemplos:

- `logos/wind-branco-sem-fundo.png`
- `wallace/wallace-palco-imersao-2025.jpg`
- `eventos/imersao-marketing-plateia-2025.jpg`
- `bastidores/escritorio-gravacao-podcast.jpg`

## Padrão de arquivo

| Regra | Por quê |
|---|---|
| Logo sempre em **PNG sem fundo** | encaixa em qualquer slide, claro ou escuro |
| Foto em **JPG ou WEBP**, até ~2 MB | repositório leve, qualidade suficiente pra slide |
| Largura mínima **1600 px** | não fica embaçada em tela cheia |
| Nada de print com marca d'água ou baixa qualidade | derruba o nível da apresentação |

## O que já existe em outras pastas (não duplicar aqui)

- `marca/direcoes/` — estudos visuais no estilo Wind (capas de teste)
- `marca/Wallace-Ribas-Identidade-Visual.pdf` — identidade visual
- `fotos/banco/` — banco de imagens de objetos para os carrosséis

## Fonte no Google Drive

A pasta compartilhada **"Wind Copany"** no Drive (do studioauura@gmail.com)
hoje só tem **vídeos brutos** (.MOV de 50–250 MB) das captações — grandes
demais pro repositório. Quando quiser uma cena de lá numa apresentação,
peça pro Claude extrair um frame do vídeo e salvar aqui como imagem.
