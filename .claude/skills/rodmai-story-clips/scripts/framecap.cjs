// node framecap.cjs <port> <t> <out.png>  — one clean frame (captions, HUD, badge, sound words hidden) of index.html at time t, 1080×1920
const pw = require('playwright');
(async () => { const [port, t, out] = process.argv.slice(2); const b = await pw.chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://localhost:${port}/index.html`); await p.waitForTimeout(2500);
  await p.addStyleTag({ content: '.capwrap, .bubble, .sfxw, .badge, #grain, .clip > div, .sghud, .capbox { display: none !important; }' });
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false); document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(600); await seek(t); await p.waitForTimeout(1500); await p.evaluate(() => document.fonts.ready); await seek(t); await p.waitForTimeout(800);
  await p.screenshot({ path: out }); await b.close(); })();
