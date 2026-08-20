# Trocar por um token de longa duração

**Criada em:** 2026-08-20
**Prioridade:** média

## Por quê

O token atual (`IGAA...`) vale cerca de 60 dias. Quando expirar, a
publicação para de funcionar com erro 190.

## Renovar (só funciona com token ainda válido)

```
curl "https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=SEU_TOKEN"
```

Ou gerar um novo no painel da Meta e rodar de novo:

```
python instagram/scripts/descobrir_id.py
```

## Prazo

Antes de meados de outubro de 2026.
