# Logo "W" 3D — Wallace Ribas / Wind (4K, 9:16)

Versao 3D premium do simbolo "W" em imagem estatica vertical 2160x3840 (4K), vista frontal reta, sem perspectiva e sem rotacao.

## Aviso importante sobre a fonte do traco
Este simbolo chegou como imagem colada na conversa (nao como arquivo no
repositorio), e o ambiente onde isso rodou nao tinha acesso ao arquivo em
disco. O traco vetorial em `logo-3d.html` foi reconstruido a mao a partir da
observacao visual da imagem — nao e uma extracao pixel-a-pixel do original.
A leitura geral (tick curto a esquerda + swoosh maior a direita formando o
"W") foi validada visualmente, mas se houver qualquer arquivo original
(SVG/AI/Figma/PNG em alta) do logo, o ideal e salva-lo em `marca/` e usar
ele como fonte de verdade — aí este traco pode ser substituido por um
tracado exato.

## O que tem aqui
- `w-logo-3d-4k-9x16.png` — imagem final em 4K
- `logo-3d.html` — a arte em SVG (geometria do glifo + tratamento 3D)

## Efeito 3D aplicado
- Extrusao limpa para baixo (fatias empilhadas, sem perspectiva)
- Relevo sutil nas bordas (luz superior-esquerda, sombra inferior-direita)
- Sheen de estudio sutil sobre o glifo
- Sombra suave projetada + sombra de contato
- Fundo mantendo a paleta laranja-para-escuro do original, com spot de luz e vinheta

## Regenerar a imagem
```bash
npm i playwright-core
node -e "const{chromium}=require('playwright-core');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox']});const p=await b.newPage({viewport:{width:2160,height:3840}});await p.goto('file://'+process.cwd()+'/logo-3d.html');await p.screenshot({path:'w-logo-3d-4k-9x16.png'});await b.close();})()"
```
