# Logo reveal — WD (9:16)

Animacao cinematica de revelacao do logo REAL "WD" (extraido do arquivo que
voce enviou na conversa, nao recriado a mao). Formato vertical 1080x1920,
30 fps, 9,5 s.

## Sobre a fonte do logo
`wd-logo.png` e o arquivo original exato que voce colou no chat (recuperado
do historico da sessao e decodificado bit a bit — mesmos pixels, mesmo
alfa). A animacao usa essa imagem diretamente: extrusao, relevo (emboss) e
reflexo sao todos calculados em cima do canal alfa da propria imagem, entao
o desenho do "WD" nunca foi redesenhado.

## O que tem aqui
- `wd-logo-reveal-9x16.mp4` — video final (H.264)
- `animacao.html` — a animacao em SVG/CSS/JS (funcao `seek(t)` controla o tempo)
- `wd-logo.png` — o logo original (fundo transparente), usado como fonte

## Linha do tempo
1. 0,0–1,1 s — fundo escuro elegante, logo quase invisivel
2. 1,1–4,3 s — varredura de luz da esquerda para a direita revela o logo;
   as duas metades (W e D, cortadas no ponto mais fino do traco) se encaixam
   suavemente na posicao final
3. 4,3–5,7 s — profundidade: sombra e reflexo sutis
4. 5,8–7,1 s — segunda varredura de brilho (polimento)
5. 6,9–9,5 s — brilho suave atras do logo e frame final limpo

Camera fixa, sem zoom, sem rotacao, sem distorcao.

## Regenerar o video
```bash
npm i playwright-core
node -e "const{chromium}=require('playwright-core');(async()=>{const fs=require('fs');fs.mkdirSync('frames',{recursive:true});const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/animacao.html');for(let f=0;f<285;f++){await p.evaluate(t=>window.seek(t),f/30);await p.screenshot({path:'frames/f'+String(f).padStart(4,'0')+'.png'});}await b.close();})()"
ffmpeg -framerate 30 -i frames/f%04d.png -c:v libx264 -preset slow -crf 17 \
  -pix_fmt yuv420p -movflags +faststart wd-logo-reveal-9x16.mp4
```
