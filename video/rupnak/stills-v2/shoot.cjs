// node shoot.cjs <port> <out dir> scene1 scene2 …   → <out>/<scene>.png (1080×1920)
let playwright; try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }
const fs = require('fs');
(async () => {
  const [port, out, ...scenes] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  for (const s of scenes) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
    p.on('pageerror', (e) => console.log('PAGEERROR', s, e.message));
    await p.goto(`http://localhost:${port}/index.html?s=${s}`); await p.waitForSelector('body[data-ready="1"]');
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
    await p.screenshot({ path: `${out}/${s}.png` }); await p.close(); console.log('shot', s);
  }
  await b.close();
})();
