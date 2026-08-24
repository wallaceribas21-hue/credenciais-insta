# 📸 Publicar no Instagram pelo Claude Code

Guia completo para conectar sua conta e publicar carrosséis automaticamente.

> ⚠️ **Leia primeiro:** os passos 4 em diante precisam rodar **no seu computador**,
> não aqui na sessão web do Claude Code. O motivo está explicado no final,
> em [Por que não dá pra fazer tudo aqui](#por-que-não-dá-pra-fazer-tudo-aqui).

---

## Antes de começar

**Conta do Instagram Profissional** (Business ou Creator) —
Instagram → Configurações → Conta → Tipo de conta.
Se for pessoal: converta para Creator. É gratuito e você não perde seguidores.

---

## Existem dois caminhos — os scripts aceitam os dois

A Meta tem duas formas de autorizar publicação, e o token de cada uma é
diferente. **Escolha uma.** Os scripts detectam qual você usou pelo prefixo
do token e se ajustam sozinhos.

| | **A. Instagram Login** | **B. Facebook Login** |
|---|---|---|
| Token começa com | `IGAA...` | `EAA...` |
| Servidor | `graph.instagram.com` | `graph.facebook.com` |
| Precisa de Página do Facebook? | ❌ não | ✅ sim |
| Dificuldade | mais simples | mais passos |

> 💡 Se você seguiu um tutorial e acabou com um token `IGAA...`, você usou o
> **caminho A**. Está certo — pule direto para o Passo 4.

---

## Passo 1 — Criar/abrir o app

Acesse **https://developers.facebook.com/apps** e entre.

Escolha um app existente ou crie um novo (tipo **Business**, nome qualquer).

---

## Passo 2 — Configurar o produto

### Caminho A — Instagram Login (recomendado)

1. No menu lateral do app: **Instagram** → **Configuração da API**
2. Escolha **"Configurar a API do Instagram com o login do Instagram"**
3. Em **Gerar tokens de acesso**, clique em **Adicionar conta**
4. Faça login com a **@wallaceribas_** e autorize

### Caminho B — Facebook Login

1. Abra o **Graph API Explorer**: developers.facebook.com/tools/explorer
2. Em **"Meta App"**, escolha seu app
3. Em **"User or Page"**, selecione a Página **WR 03- Wallace**
   (não deixe em "Usuário")

---

## Passo 3 — Gerar o token

### Caminho A

Clique em **Gerar token** ao lado da conta. Copie — começa com `IGAA...`

Permissões necessárias (o fluxo já pede automaticamente):
`instagram_business_basic`, `instagram_business_content_publish`

### Caminho B

1. **"Add a Permission"** → adicione as 3:
   `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`
2. **"Generate Access Token"** → autorize (Continuar → OK)
3. Copie — começa com `EAA...`

> 🔒 **Esse token é uma senha.** Ele dá acesso para publicar na sua conta.
> Não mande por WhatsApp, não cole em chat, não suba pro GitHub.
> Se vazar, revogue em: App → Configurações → Básico.

---

## Passo 4 — Instalar as dependências

```bash
pip install -r instagram/requirements.txt
```

---

## Passo 5 — Descobrir o ID e salvar as credenciais

Um comando faz tudo — descobre o `INSTAGRAM_BUSINESS_ID` e escreve o `.env`:

```bash
python instagram/scripts/descobrir_id.py
```

Ele pede o token (digitação oculta — não aparece na tela nem fica no
histórico do terminal), detecta qual caminho você usou e resolve o resto:

**Caminho A (`IGAA...`)** — pega o ID direto, sem escolher nada:

```
Fluxo detectado: Instagram Login (graph.instagram.com)

  Conta:  @wallaceribas_
  Tipo:   BUSINESS
  ID:     17841...
```

**Caminho B (`EAA...`)** — lista suas contas para você escolher:

```
Fluxo detectado: Facebook Login (graph.facebook.com)

  [1] @wallaceribas_          Pagina: WR 03- Wallace  <- Pagina WR 03- Wallace
  [2] @outraconta             Pagina: Outra Página

Qual usar? (1-2)
```

Nos dois casos o `.env` é criado com permissão `600` (só você lê).

> O `.env` já está no `.gitignore`. Ele **nunca** vai pro GitHub.

<details>
<summary>Prefere fazer na mão?</summary>

```bash
cp instagram/.env.example instagram/.env
```

**Caminho A** — o `/me` já devolve tudo:
```bash
curl "https://graph.instagram.com/v23.0/me?fields=user_id,username&access_token=SEU_TOKEN"
```

**Caminho B** — procure a Página com `instagram_business_account`:
```bash
curl "https://graph.facebook.com/v19.0/me/accounts?fields=id,name,instagram_business_account&access_token=SEU_TOKEN"
```

Preencha o `.env` com o que voltou (o `FACEBOOK_PAGE_ID` só existe no caminho B):
```
INSTAGRAM_BUSINESS_ID=17841400000000000
FACEBOOK_PAGE_ID=512007262005431      # só no caminho B — Página "WR 03- Wallace"
INSTAGRAM_ACCESS_TOKEN=IGAA... ou EAA...
```
</details>

---

## Passo 6 — Testar a conexão

```bash
python instagram/scripts/verificar_conexao.py
```

Se passar nos 3 testes e mostrar `@wallaceribas_`, está funcionando. ✅

---

## Passo 7 — Publicar

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

## Validade do token

O token dura cerca de **60 dias**. Enquanto ele ainda está válido, renovar é
um comando. Se deixar vencer, não dá para renovar: tem que refazer o Passo 3
inteiro no site da Meta.

```bash
python instagram/scripts/renovar_token.py
```

Ele fala com a Meta, grava o token novo direto no `.env` e reinicia a contagem
de 60 dias. Você não copia nada. Pode rodar quantas vezes quiser, e cada vez
empurra o vencimento para 60 dias à frente.

**Como você fica sabendo que está perto:** não precisa lembrar. A partir de
15 dias antes, o `publish_instagram.py` avisa sozinho toda vez que você
publica. O `verificar_conexao.py` mostra o prazo sempre.

> O `INSTAGRAM_TOKEN_EXPIRA_EM` no `.env` é quem guarda a data. Ele só passa a
> existir depois da primeira renovação, então rode uma vez agora para começar
> a contagem.

**Se usa o Caminho B (`EAA...`)**, o script precisa de mais duas linhas no
`.env`, porque a Meta exige o app para esse fluxo:

```
META_APP_ID=...
META_APP_SECRET=...
```

Pegue em developers.facebook.com → seu App → Configurações → Básico.

**Se já venceu**, não tem renovação: rode o Passo 3 de novo e depois o
`descobrir_id.py` com o token novo.

---

## Deu erro?

| Mensagem | O que é | Solução |
|---|---|---|
| `OAuthException #190` | Token expirado | Gere um novo (Passo 3) |
| `OAuthException #200` | Faltam permissões | Volte ao Passo 3 e adicione as 3 |
| `#100 image_url required` | Imagem local | O script já resolve — confira o caminho do arquivo |
| `Instagram account not found` | Conta não é Business | Converta em Configurações → Conta |
| `Pages not found` | Página não vinculada | Vincule em Instagram → Configurações → Página vinculada |
| `#9007` | Limite de 25 posts/24h | Espere e tente de novo |
| `Unsupported request` | Token e servidor trocados | Os scripts já resolvem — não edite `META_API_VERSION` na mão |

O `verificar_conexao.py` já traduz esses erros automaticamente.

---

## Por que não dá pra fazer tudo aqui

Esta sessão do Claude Code roda **num container na nuvem**, não no seu computador.
Duas consequências:

1. **A API da Meta está bloqueada** pela política de rede do ambiente —
   tanto `graph.facebook.com` quanto `graph.instagram.com` respondem `403`
   no proxy. Então validar token, descobrir o ID, testar e publicar não
   funcionam daqui.

2. **O container é temporário.** Um `.env` salvo aqui é apagado quando
   a sessão termina. Credencial precisa ficar na sua máquina.

Por isso este repositório guarda o **código e as instruções**, e os passos que
usam o token rodam no seu computador. Baixe o repositório com:

```bash
git clone https://github.com/wallaceribas21-hue/credenciais-insta
```
