// YouTube thumbnail 1280×720 for a landscape long-form: node thumb.cjs <port> <t> <out.jpg>
const { chromium } = require('playwright');
(async () => {
  const [port, t, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', (e) => console.log('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`, { timeout: 600000 }); await p.waitForTimeout(3000);
  const seek = (t) => p.evaluate((t) => { window.__timelines.main.seek(+t, false);
    document.querySelectorAll('.clip').forEach((c) => { const s = +c.dataset.start, d = +c.dataset.duration; c.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden'; }); }, t);
  await seek(0.2); await p.waitForTimeout(1000); await seek(t); await p.waitForTimeout(1500); await seek(t); await p.waitForTimeout(800);
  await p.evaluate(() => {
    const st = document.createElement('style'); st.textContent = `
      @font-face { font-family: TK; font-weight: 900; src: url(assets/fonts/f3.ttf); }
      .capwrap, .bubble, .sfxw, .badge, #grain { display: none !important; }
      .clip { transform-origin: 960px 540px; transform: translate(440px, 60px) scale(1.5); filter: brightness(1.12) saturate(1.1); }
      #th { position: absolute; inset: 0; z-index: 9999; font-family: TK; pointer-events: none; }
      #th .sh { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(4,5,7,.92) 0%, rgba(4,5,7,.7) 34%, rgba(4,5,7,0) 58%); }
      #th .sb { position: absolute; left: 0; right: 0; bottom: 0; height: 330px; background: linear-gradient(0deg, rgba(4,5,7,.85), rgba(4,5,7,0)); }
      #th .logo { position: absolute; left: 70px; top: 70px; font: 900 168px/1.1 TK; color: #f6efe0; -webkit-text-stroke: 9px #140e0a; paint-order: stroke fill;
        text-shadow: 0 0 40px #3a8ad8, 0 0 90px #3a8ad8, 0 10px 0 rgba(0,0,0,.55); }
      #th .full { position: absolute; left: 82px; top: 300px; font: 900 64px/1 TK; color: #1d1610; background: #e2b53c; padding: 12px 30px 20px; border-radius: 20px;
        box-shadow: 0 0 0 6px #140e0a, 0 12px 26px rgba(0,0,0,.6); }
      #th .setup { position: absolute; left: 70px; top: 460px; font: 900 76px/1.25 TK; color: #fffaf0; -webkit-text-stroke: 9px #120c08; paint-order: stroke fill; text-shadow: 0 8px 18px rgba(0,0,0,.8); }
      #th .cmd { position: absolute; left: 60px; top: 690px; font: 900 112px/1.1 TK; color: #fff; background: #d8312a; padding: 6px 44px 26px; border-radius: 30px; transform: rotate(-2.5deg);
        box-shadow: 0 0 0 10px #120c08, 0 0 60px rgba(216,49,42,.55), 0 22px 44px rgba(0,0,0,.7); text-shadow: 0 6px 0 rgba(0,0,0,.35); }`;
    document.head.appendChild(st);
    document.getElementById('root').insertAdjacentHTML('beforeend', `<div id="th"><div class="sh"></div><div class="sb"></div>
      <div class="logo">นาทีก่อนจม</div><div class="full">ฉบับเต็ม · ครบ 3 ตอน</div>
      <div class="setup">คนที่คุณรักยังอยู่ใต้น้ำ…</div><div class="cmd">อย่ากระโดดลงไปช่วย!</div></div>`);
  });
  await p.evaluate(() => document.fonts.ready);
  let prev = null;
  for (let k = 0; k < 8; k++) { await p.waitForTimeout(k ? 700 : 1500); const s = await p.screenshot({ type: 'png' }); if (prev && s.equals(prev)) break; prev = s; }
  require('fs').writeFileSync(out + '.png', prev); await b.close();
})();
