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

## Conta escolhida

| Campo | Valor |
|---|---|
| Instagram | **@wallaceribas_** |
| Página do Facebook | **WR 03- Wallace** |
| `FACEBOOK_PAGE_ID` | `512007262005431` ✅ já descoberto |
| `INSTAGRAM_BUSINESS_ID` | ⬜ falta — sai do `descobrir_id.py` |

## Passos

- [ ] Confirmar que a @wallaceribas_ é Business/Creator
- [ ] Clonar o repositório na máquina local
- [ ] `pip install -r instagram/requirements.txt`
- [ ] Gerar o token (caminho A `IGAA...` ou caminho B `EAA...` — tanto faz)
- [ ] `python instagram/scripts/descobrir_id.py`
      (detecta o caminho, descobre o ID e escreve o `.env` sozinho)
- [ ] `python instagram/scripts/verificar_conexao.py` → tem que passar nos 3 testes
- [ ] Trocar por um token de longa duração (~60 dias)

## Pronto quando

`verificar_conexao.py` imprime `@wallaceribas_` e os 3 testes passam.

## Observações

- Guia completo: [`instagram/README.md`](../../instagram/README.md)
- O token do Graph API Explorer **expira em 1 hora** — por isso o último passo
- O `.env` está bloqueado pelo `.gitignore`. Nunca subir credencial pro GitHub.
- **Precisa rodar na máquina local**: o ambiente do Claude Code na nuvem
  bloqueia `graph.facebook.com` (403 no CONNECT do proxy)
- Tentei descobrir o `INSTAGRAM_BUSINESS_ID` pelo conector da Meta sem sucesso:
  a consulta `ads_get_ig_accounts` não está liberada em nenhuma das 5 contas
  de anúncio testadas. Por isso o passo do token é inevitável.
- Os scripts aceitam **os dois fluxos** da Meta (token `IGAA...` do Instagram
  Login e `EAA...` do Facebook Login) — `api.py` detecta pelo prefixo e
  aponta para o servidor certo. O `FACEBOOK_PAGE_ID` só é usado no fluxo `EAA`.
