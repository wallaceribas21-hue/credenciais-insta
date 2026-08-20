# ✅ Publicar o primeiro carrossel

**Concluída em:** 2026-08-20
**Post ID:** 18081723827691045
**Conta:** @wallaceribas_

## O que foi publicado

Carrossel de 8 slides sobre o que a IA executa dentro de uma empresa,
usando a própria integração como exemplo. Estilo poster.

- Copy: `conteudo/001-ia-postou-sozinho.txt`
- Legenda: `conteudo/001-legenda.txt`
- Slides: `conteudo/carrossel-01/`

## Os cinco erros que apareceram no caminho

Vale guardar, porque qualquer um deles derruba a publicação de novo:

| Erro | Causa | Correção |
|---|---|---|
| `as_uri()` com caminho relativo | O padrão `--saida slides` é relativo | `.resolve()` no caminho |
| Legenda quebrada no PowerShell | Texto longo com quebra de linha vira vários argumentos | `--caption-file` |
| `SSLEOFError` no catbox | Host instável | Quatro hosts em cadeia |
| `The image format is not supported` | **A Meta só aceita JPEG**, não PNG | Converte no envio |
| `PermissionError WinError 32` | Arquivo aberto não pode ser apagado no Windows | Lê para bytes e fecha antes |

## Pendente

- [ ] Print do feed no story, que é a prova real do post
- [ ] Trocar por um token de longa duração antes de expirar
