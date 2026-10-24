// usage: node shot.js <url> <out.png> [w h] [seek seconds for a hyperframes page]
const { chromium } = require("playwright");
(async () => {
  const [url, out, w = "1600", h = "1400", seek] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
  const logs = []; p.on("console", (m) => logs.push(m.type() + ": " + m.text())); p.on("pageerror", (e) => logs.push("pageerror: " + e.message));
  await p.goto(url, { waitUntil: "networkidle" }); await p.waitForTimeout(400);
  if (seek !== undefined) await p.evaluate((t) => { const tl = window.__timelines && window.__timelines.main; if (tl) tl.seek(+t, false); }, seek);
  await p.waitForTimeout(200); await p.screenshot({ path: out }); await b.close();
  logs.filter((l) => !/favicon/.test(l)).forEach((l) => console.log(l)); console.log("saved", out);
})();
