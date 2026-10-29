// Clip covers (ปกคลิป): a clean frame of a stored episode + the series lockup + the hook, 1080×1920 JPG.
// Serve the folder that holds the episodes first:  (cd video && (python3 -m http.server 8890 >/dev/null 2>&1 &))
// usage: node cover.cjs <base url> <covers.json> [only-id …]
//   base url  e.g. http://localhost:8890  (each entry's "page" is relative to it, e.g. "koi-ep1/composition/index.html")
//   covers.json: [{ id, page, out, t, zoom: { s, x, y }, hideLight, series, ep, epTitle, finale, setup, cmd, glow, logoInk }]
//     t         the frame (seconds) · zoom: scale s around screen point (x, y) to frame the subject · shift { x, y }: move the frame
//               (px, after the zoom) so the subject sits in the clear band between the title (≈ y 640) and the hook (≈ y 1150)
//     setup     the situation, "/" breaks the line, [word] = yellow box · cmd: the counter-instinct order (red box, "/" breaks)
//     glow      the series colour (title glow and rim) · finale: true → "ตอนจบ" pill · bright: lift a dark frame (1.2–1.4)
// Everything the viewer needs sits inside y 250–1650: TikTok's profile grid crops covers to 3:4 around the centre.
// Captions, bubbles, sound words, the badge and HTML cards are hidden; hideLight also hides SVG cards in the light layer.
let playwright;
try { playwright = require('playwright'); } catch (e) { playwright = require('/opt/node22/lib/node_modules/playwright'); }
const fs = require('fs');
const path = require('path');

const CSS = (c) => `
  @font-face { font-family: CvK; font-weight: 900; src: url(assets/fonts/f3.ttf); }
  @font-face { font-family: CvK; font-weight: 700; src: url(assets/fonts/f2.ttf); }
  .capwrap, .bubble, .sfxw, .badge, #grain, .clip > div { display: none !important; }
  ${c.hideLight ? '[id$="-light"] { display: none !important; }' : ''}
  #cv { position: absolute; inset: 0; z-index: 9999; font-family: CvK; pointer-events: none; }
  #cv .sh-t { position: absolute; left: 0; right: 0; top: 0; height: 760px;
    background: linear-gradient(180deg, rgba(4,5,7,.9) 0%, rgba(4,5,7,.62) 42%, rgba(4,5,7,0) 100%); }
  #cv .sh-b { position: absolute; left: 0; right: 0; bottom: 0; height: 980px;
    background: linear-gradient(0deg, rgba(4,5,7,.95) 0%, rgba(4,5,7,.78) 40%, rgba(4,5,7,0) 100%); }
  #cv .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 78% 60% at 50% 46%, transparent 55%, rgba(0,0,0,.55) 100%); }
  #cv .brand { position: absolute; top: 262px; left: 0; right: 0; text-align: center; font: 700 34px/1 CvK; letter-spacing: 16px;
    color: rgba(244,236,216,.82); text-shadow: 0 3px 10px rgba(0,0,0,.8); }
  #cv .logo { position: absolute; top: 300px; left: 40px; right: 40px; text-align: center; white-space: nowrap; font-weight: 900; line-height: 1.12;
    color: #f6efe0; -webkit-text-stroke: 7px ${c.logoInk || '#140e0a'}; paint-order: stroke fill;
    text-shadow: 0 0 34px ${c.glow}, 0 0 80px ${c.glow}, 0 10px 0 rgba(0,0,0,.55); }
  #cv .ep { position: absolute; top: 548px; left: 0; right: 0; display: flex; justify-content: center; align-items: center; gap: 18px; }
  #cv .ep b { font: 900 52px/1 CvK; color: #fff6ea; background: #d8312a; padding: 10px 24px 16px; border-radius: 18px;
    box-shadow: 0 0 0 5px #140e0a, 0 10px 24px rgba(0,0,0,.6); }
  #cv .ep b.fin { background: #e2b53c; color: #1d1610; }
  #cv .ep span { font: 900 58px/1 CvK; color: #f6efe0; -webkit-text-stroke: 5px #140e0a; paint-order: stroke fill; text-shadow: 0 6px 14px rgba(0,0,0,.7); }
  #cv .hook { position: absolute; left: 44px; right: 44px; bottom: 300px; text-align: center; }
  #cv .setup { font-weight: 900; line-height: 1.32; color: #fffaf0; -webkit-text-stroke: 8px #120c08; paint-order: stroke fill;
    text-shadow: 0 8px 18px rgba(0,0,0,.8); white-space: nowrap; }
  #cv .setup .in { display: inline-block; }
  #cv .setup i { font-style: normal; color: #1d1610; -webkit-text-stroke: 0; background: #f2c55c; border-radius: 16px; padding: 0 .16em 4px;
    box-shadow: 0 0 0 5px #120c08; text-shadow: none; }
  #cv .cmd { display: inline-block; margin-top: 34px; font-weight: 900; line-height: 1.12; color: #fff; background: #d8312a; white-space: nowrap;
    padding: 8px 44px 26px; border-radius: 30px; transform: rotate(-2.5deg);
    box-shadow: 0 0 0 9px #120c08, 0 0 60px rgba(216,49,42,.55), 0 22px 44px rgba(0,0,0,.7); text-shadow: 0 6px 0 rgba(0,0,0,.35); }`;

const mark = (s) => s.split('/').map((ln) => ln.trim().replace(/\[([^\]]+)\]/g, '<i>$1</i>')).join('<br>');

(async () => {
  const [base, cfgPath, ...only] = process.argv.slice(2);
  if (!base || !cfgPath) { console.error('usage: node cover.cjs <base url> <covers.json> [only-id …]'); process.exit(2); }
  const all = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  const list = only.length ? all.filter((c) => only.includes(c.id)) : all;
  const b = await playwright.chromium.launch({ args: ['--no-sandbox'] });
  for (const c of list) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
    p.on('pageerror', (e) => console.log('PAGEERROR', c.id, e.message));
    await p.goto(`${base}/${c.page}`);
    await p.waitForTimeout(2500);
    const seek = (t) => p.evaluate((t) => {
      window.__timelines.main.seek(+t, false);
      document.querySelectorAll('.clip').forEach((el) => {
        const s = +el.dataset.start, d = +el.dataset.duration;
        el.style.visibility = (+t >= s && +t < s + d) ? 'visible' : 'hidden';
      });
    }, t);
    await seek(0.2); await p.waitForTimeout(800);
    await seek(c.t); await p.waitForTimeout(1200);
    await seek(c.t); await p.waitForTimeout(500);
    await p.evaluate(({ c, css, setup, cmd }) => {
      const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
      if (c.zoom || c.shift) document.querySelectorAll('.clip').forEach((el) => {
        const z = c.zoom || { s: 1, x: 540, y: 960 }, sh = c.shift || { x: 0, y: 0 };
        el.style.transformOrigin = `${z.x}px ${z.y}px`; el.style.transform = `translate(${sh.x || 0}px, ${sh.y || 0}px) scale(${z.s})`;
      });
      if (c.bright) document.querySelectorAll('.clip').forEach((el) => { el.style.filter = `brightness(${c.bright})`; });
      const root = document.getElementById('root');
      root.insertAdjacentHTML('beforeend', `<div id="cv"><div class="sh-t"></div><div class="sh-b"></div><div class="vig"></div>
        <div class="brand">ROD MAI CLUB</div><div class="logo">${c.series}</div>
        <div class="ep"><b class="${c.finale ? 'fin' : ''}">${c.finale ? `EP.${c.ep} · ตอนจบ` : `EP.${c.ep}`}</b><span>${c.epTitle}</span></div>
        <div class="hook"><div class="setup"><span class="in">${setup}</span></div><div class="cmd">${cmd}</div></div></div>`);
    }, { c, css: CSS(c), setup: mark(c.setup), cmd: mark(c.cmd) });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    // shrink each text block until it fits its width (long series names and long orders)
    await p.evaluate(({ c }) => {
      // measure an inline-block around the text: a block's scrollWidth does not see centred overflow
      const fit = (el, size, max, inner = el) => { let s = size; el.style.fontSize = s + 'px'; while (inner.getBoundingClientRect().width > max && s > 40) { s -= 4; el.style.fontSize = s + 'px'; } };
      const logo = document.querySelector('#cv .logo'); logo.innerHTML = `<span style="display:inline-block">${logo.innerHTML}</span>`;
      fit(logo, c.logoSize || 200, 1000, logo.firstChild);
      fit(document.querySelector('#cv .setup'), c.setupSize || 84, 990, document.querySelector('#cv .setup .in'));
      const cmd = document.querySelector('#cv .cmd');
      let s = c.cmdSize || 156; cmd.style.fontSize = s + 'px';
      while (cmd.getBoundingClientRect().width > 990 && s > 50) { s -= 4; cmd.style.fontSize = s + 'px'; }
    }, { c });
    // heavy SVG frames repaint in tiles: shoot until two shots in a row are identical (a half-painted cover is never saved)
    fs.mkdirSync(path.dirname(c.out), { recursive: true });
    let prev = null, shot = null;
    for (let k = 0; k < 8; k++) {
      await p.waitForTimeout(k ? 700 : 1200);
      shot = await p.screenshot({ type: 'png' });
      if (prev && shot.equals(prev)) break;
      prev = shot;
    }
    await p.screenshot({ path: c.out, type: 'jpeg', quality: 92 });
    console.log('cover', c.id, '→', c.out);
    await p.close();
  }
  await b.close();
})();
