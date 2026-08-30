# Logo reveal — Pepsi (9:16)

Animacao cinematica de revelacao do logo em formato vertical 1080x1920, 30 fps, 9,5 s.

## O que tem aqui
- `pepsi-logo-reveal-9x16.mp4` — video final (H.264, pronto para Reels/TikTok/Shorts)
- `animacao.html` — a animacao em SVG/CSS/JS, deterministica (funcao `seek(t)` controla o tempo)
- `render-frames.js` — renderiza os 285 frames no Chromium headless (Playwright)
- `archivo-black.ttf` — fonte do wordmark (Google Fonts, licenca OFL)

## Linha do tempo
1. 0,0–1,1 s — fundo escuro elegante, logo quase invisivel
2. 1,1–4,3 s — varredura de luz da esquerda para a direita revela o logo; as tres partes (onda vermelha, wordmark, onda azul) se encaixam suavemente na posicao final
3. 4,3–5,7 s — profundidade: sombra e reflexo sutis
4. 5,8–7,1 s — segunda varredura de brilho (polimento)
5. 6,9–9,5 s — brilho suave atras do logo e frame final limpo

Camera fixa, sem zoom, sem rotacao, sem distorcao.

## Regenerar o video
```bash
npm i playwright-core
node render-frames.js   # gera frames/f0000.png ... f0284.png
ffmpeg -framerate 30 -i frames/f%04d.png -c:v libx264 -preset slow -crf 17 \
  -pix_fmt yuv420p -movflags +faststart pepsi-logo-reveal-9x16.mp4
```
