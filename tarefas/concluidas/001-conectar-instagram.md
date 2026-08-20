# ✅ Conectar o Instagram ao Claude Code

**Concluída em:** 2026-08-20

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
| `INSTAGRAM_BUSINESS_ID` | `17841408395593838` ✅ |
| Fluxo usado | Instagram Login (token `IGAA...`) |
| Tipo da conta | MEDIA_CREATOR |

## Passos

- [x] Confirmar que a @wallaceribas_ é Business/Creator
- [x] Clonar o repositório na máquina local
- [x] `pip install -r instagram/requirements.txt`
- [x] Gerar o token (caminho A `IGAA...` ou caminho B `EAA...` — tanto faz)
- [x] `python instagram/scripts/descobrir_id.py`
      (detecta o caminho, descobre o ID e escreve o `.env` sozinho)
- [x] `python instagram/scripts/verificar_conexao.py` → tem que passar nos 3 testes
- [ ] Trocar por um token de longa duração (~60 dias) — pendente

## Resultado

`verificar_conexao.py` passou nos 3 testes com a conta @wallaceribas_.
Configuração concluída em 2026-08-20.

**Falta só:** trocar pelo token de longa duração antes que o atual expire.

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
