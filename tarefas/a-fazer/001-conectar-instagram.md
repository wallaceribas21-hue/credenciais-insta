# Conectar o Instagram ao Claude Code

**Criada em:** 2026-08-20
**Prioridade:** alta
**Responsável:** Wallace

## O que é

Gerar o token da Meta API e preencher o `.env` para conseguir publicar
carrosséis no Instagram automaticamente pelo Claude Code.

O código já está pronto em `instagram/`. Falta só a parte que depende
de credencial — e essa parte precisa rodar na máquina local, porque o
ambiente na nuvem bloqueia `graph.facebook.com`.

## Passos

- [ ] Confirmar que a conta do Instagram é Business/Creator
- [ ] Confirmar que tem Página do Facebook vinculada
- [ ] Gerar o token no Graph API Explorer com as 3 permissões
- [ ] Rodar o `curl` do Passo 4 para descobrir o `INSTAGRAM_BUSINESS_ID`
- [ ] Preencher `instagram/.env` (copiar do `.env.example`)
- [ ] `pip install -r instagram/requirements.txt`
- [ ] `python instagram/scripts/verificar_conexao.py` → tem que passar nos 3 testes
- [ ] Trocar por um token de longa duração (~60 dias)

## Pronto quando

`verificar_conexao.py` imprime o `@usuario` da conta certa e os 3 testes passam.

## Observações

- Guia completo: [`instagram/README.md`](../../instagram/README.md)
- O token do Graph API Explorer **expira em 1 hora** — por isso o último passo
- O `.env` está bloqueado pelo `.gitignore`. Nunca subir credencial pro GitHub.
- Decidir qual das contas usar: o Wallace administra 33 Páginas do Facebook
