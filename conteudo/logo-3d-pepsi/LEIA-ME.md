# Logo 3D — Pepsi (4K, 9:16)

Versao 3D premium do logo em imagem estatica vertical 2160x3840 (4K), vista frontal reta, sem perspectiva e sem rotacao.

## O que tem aqui
- `pepsi-logo-3d-4k-9x16.png` — imagem final em 4K
- `logo-3d.html` — a arte em SVG (mesma geometria vetorial da animacao em `../logo-reveal-pepsi/`)

## Efeito 3D aplicado (sem alterar o design)
- Extrusao limpa para baixo (fatias empilhadas escurecidas, sem perspectiva)
- Relevo sutil nas bordas de cada forma (luz superior-esquerda, sombra inferior-direita)
- Gradientes muito sutis proximos das cores originais (iluminacao de estudio)
- Sombra suave no fundo + sombra de contato
- Fundo de estudio escuro com spot e vinheta

## Regenerar a imagem
```bash
npm i playwright-core
node ../logo-reveal-pepsi/render-frames.js  # nao e necessario; use o comando abaixo
node -e "const{chromium}=require('playwright-core');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});const p=await b.newPage({viewport:{width:2160,height:3840}});await p.goto('file://'+process.cwd()+'/logo-3d.html');await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:'pepsi-logo-3d-4k-9x16.png'});await b.close();})()"
```
A fonte `archivo-black.ttf` esta em `../logo-reveal-pepsi/` — copie para esta pasta antes de regenerar.
