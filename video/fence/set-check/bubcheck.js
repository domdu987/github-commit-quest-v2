// lists every speech bubble whose tail (left: var(--tail), relative to the bubble) falls outside the bubble's own width
const { chromium } = require("playwright");
(async () => {
  const url = process.argv[2];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(url, { waitUntil: "networkidle" }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const r = await p.evaluate(() => [...document.querySelectorAll(".bubble")].map((el) => {
    const cs = getComputedStyle(el); const tail = parseFloat(cs.getPropertyValue("--tail")) || 40;
    return { id: el.id, left: parseFloat(el.style.left), w: el.offsetWidth, tail, text: el.textContent.trim().slice(0, 40) };
  }));
  r.forEach((x) => console.log((x.tail > x.w - 50 ? "BAD " : "ok  ") + JSON.stringify(x)));
  await b.close();
})();
