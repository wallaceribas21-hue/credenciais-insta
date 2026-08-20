# 📸 Publicar no Instagram pelo Claude Code

Guia completo para conectar sua conta e publicar carrosséis automaticamente.

> ⚠️ **Leia primeiro:** os passos 4 em diante precisam rodar **no seu computador**,
> não aqui na sessão web do Claude Code. O motivo está explicado no final,
> em [Por que não dá pra fazer tudo aqui](#por-que-não-dá-pra-fazer-tudo-aqui).

---

## Antes de começar

Confirme os 3 pré-requisitos:

1. **Conta do Instagram Profissional** (Business ou Creator)
   Instagram → Configurações → Conta → Tipo de conta
   Se for pessoal: converta para Creator. É gratuito e você não perde seguidores.

2. **Página do Facebook vinculada** ao Instagram
   Instagram → Configurações → Conta → Página vinculada

3. **Acesso ao Facebook** que administra essa Página

---

## Passo 1 — Abrir o Graph API Explorer

Acesse: **https://developers.facebook.com/tools/explorer**

Entre com o Facebook que administra a Página.

No canto superior direito, em **"Meta App"**, escolha um app existente.
Se não tiver nenhum: **Criar App** → tipo **Business** → nome qualquer (ex: `MeuBot`) → confirmar.

---

## Passo 2 — Selecionar a Página

Logo abaixo, no campo **"User or Page"**, selecione **sua Página do Facebook**.

> Não deixe em "Usuário" — tem que ser a Página.

---

## Passo 3 — Gerar o token

1. Clique em **"Add a Permission"** e adicione as **3 permissões**:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`

2. Clique em **"Generate Access Token"**

3. Autorize na janela que abrir (Continuar → OK em tudo)

4. Copie o token que aparece (começa com `EAA...`)

> 🔒 **Esse token é uma senha.** Ele dá acesso para publicar na sua conta.
> Não mande por WhatsApp, não cole em chat, não suba pro GitHub.

---

## Passo 4 — Descobrir o ID do Instagram

No seu computador, com o token em mãos:

```bash
curl "https://graph.facebook.com/v19.0/me/accounts?fields=id,name,instagram_business_account&access_token=SEU_TOKEN"
```

A resposta traz suas Páginas. Procure a que tem `instagram_business_account`:

```json
{
  "name": "Minha Página",
  "id": "1234567890",                          <- FACEBOOK_PAGE_ID
  "instagram_business_account": {
    "id": "17841400000000000"                  <- INSTAGRAM_BUSINESS_ID
  }
}
```

---

## Passo 5 — Salvar as credenciais

Copie o modelo e preencha:

```bash
cp instagram/.env.example instagram/.env
```

Abra o `instagram/.env` e preencha os 3 valores:

```
INSTAGRAM_BUSINESS_ID=17841400000000000
FACEBOOK_PAGE_ID=1234567890
INSTAGRAM_ACCESS_TOKEN=EAA...
META_API_VERSION=v19.0
```

> O `.env` já está no `.gitignore`. Ele **nunca** vai pro GitHub.

---

## Passo 6 — Instalar as dependências

```bash
pip install -r instagram/requirements.txt
```

---

## Passo 7 — Testar a conexão

```bash
python instagram/scripts/verificar_conexao.py
```

Se aparecer o seu `@usuario` e a contagem de seguidores, está funcionando. ✅

---

## Passo 8 — Publicar

```bash
# Testar sem publicar de verdade:
python instagram/scripts/publish_instagram.py \
  --images slides/*.png \
  --caption "minha legenda" \
  --dry-run

# Publicar pra valer:
python instagram/scripts/publish_instagram.py \
  --images slides/*.png \
  --caption "minha legenda"
```

**Regras do carrossel:** de 2 a 10 imagens, formato `.png` ou `.jpg`.

> 📤 As imagens são enviadas para o **catbox.moe** antes de ir pro Instagram —
> a API da Meta só aceita imagem que já esteja numa URL pública, não aceita
> arquivo do seu computador. Isso significa que a imagem fica acessível por link
> para quem tiver a URL. Não use com material sigiloso.

---

## O token expira em 1 hora

O token do Graph API Explorer é de curta duração. Para um token de ~60 dias:

```bash
curl "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=SEU_TOKEN_ATUAL"
```

`APP_ID` e `APP_SECRET` ficam em: developers.facebook.com → seu App → Configurações → Básico.

---

## Deu erro?

| Mensagem | O que é | Solução |
|---|---|---|
| `OAuthException #190` | Token expirado | Gere um novo (Passo 3) |
| `OAuthException #200` | Faltam permissões | Volte ao Passo 3 e adicione as 3 |
| `#100 image_url required` | Imagem local | O script já resolve — confira o caminho do arquivo |
| `Instagram account not found` | Conta não é Business | Converta em Configurações → Conta |
| `Pages not found` | Página não vinculada | Vincule em Instagram → Configurações → Página vinculada |

O `verificar_conexao.py` já traduz esses erros automaticamente.

---

## Por que não dá pra fazer tudo aqui

Esta sessão do Claude Code roda **num container na nuvem**, não no seu computador.
Duas consequências:

1. **`graph.facebook.com` está bloqueado** pela política de rede do ambiente
   (o proxy responde `403` na conexão). Então nada que fale com a Meta API
   — validar token, descobrir o ID, testar, publicar — funciona daqui.

2. **O container é temporário.** Um `.env` salvo aqui é apagado quando
   a sessão termina. Credencial precisa ficar na sua máquina.

Por isso este repositório guarda o **código e as instruções**, e os passos que
usam o token rodam no seu computador. Baixe o repositório com:

```bash
git clone https://github.com/wallaceribas21-hue/credenciais-insta
```
