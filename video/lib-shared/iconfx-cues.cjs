// Dump every IconFX sound cue a built composition scheduled: node iconfx-cues.cjs http://localhost:PORT/index.html > iconfx_cues.json
// Each entry is { t (seconds on the main timeline), type (a synth.py sfx kind), gain }; append them to mix.py's CUES as (None, t, type, gain).
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(process.argv[2]); await p.waitForTimeout(3000);
  console.log(JSON.stringify(await p.evaluate(() => (window.IconFX ? window.IconFX.cues : [])), null, 1)); await b.close(); })();
