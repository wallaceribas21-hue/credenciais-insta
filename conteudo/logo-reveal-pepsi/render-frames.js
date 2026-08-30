const { chromium } = require('playwright-core');
const fs = require('fs');
(async () => {
  const FPS = 30, DUR = 9.5;
  const N = Math.round(FPS * DUR); // 285
  fs.mkdirSync(__dirname + '/frames', { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + __dirname + '/animation.html');
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  for (let f = 0; f < N; f++) {
    const t = f / FPS;
    await page.evaluate(tt => window.seek(tt), t);
    await page.screenshot({ path: `${__dirname}/frames/f${String(f).padStart(4, '0')}.png` });
    if (f % 30 === 0) console.log('frame', f, '/', N);
  }
  await browser.close();
  console.log('done', N);
})();
