# Publicar o primeiro carrossel de teste

**Criada em:** 2026-08-20
**Prioridade:** média
**Responsável:** Wallace

## O que é

Depois que a conexão estiver funcionando (tarefa 001), publicar um carrossel
simples para validar o fluxo inteiro de ponta a ponta.

## Passos

- [ ] Preparar 2 ou 3 imagens de teste (`.png` ou `.jpg`, quadradas 1080x1080)
- [ ] Rodar com `--dry-run` primeiro e conferir que não dá erro
- [ ] Publicar de verdade (sem `--dry-run`)
- [ ] Conferir no app do Instagram se o post apareceu certo
- [ ] Apagar o post de teste, se for o caso

## Pronto quando

O carrossel aparece no perfil do Instagram com todos os slides na ordem certa
e a legenda correta.

## Observações

- Depende da tarefa 001 estar concluída
- Carrossel aceita de 2 a 10 imagens
- Comando:
  ```
  python instagram/scripts/publish_instagram.py --images slides/*.png --caption "teste"
  ```
- Lembrar: as imagens passam pelo catbox.moe (host público). Não usar
  material sigiloso no teste.
