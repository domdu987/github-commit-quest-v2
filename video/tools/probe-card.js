const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on("pageerror", (e) => console.log("pageerror:", e.message)); p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.log(m.type(), m.text()); });
  await p.goto(process.argv[2], { waitUntil: "networkidle" }); await p.waitForTimeout(400);
  for (const t of [35.3, 36.5, 38.2, 39.5]) {
    const r = await p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(t, false);
      const g = document.querySelector("#s4 .cdn"); const shs = g ? [...g.querySelectorAll(".pd")].map((pd) => [...pd.querySelectorAll(".sh")].map((s) => s.dataset.v + ":" + (s.style.opacity || "css")).join(" ")) : null;
      return { id: g && g.id, cls: g && g.className, shs, black: getComputedStyle(document.getElementById("black")).opacity, dur: tl.duration() }; }, t);
    console.log(t, JSON.stringify(r));
  }
  await b.close();
})();
