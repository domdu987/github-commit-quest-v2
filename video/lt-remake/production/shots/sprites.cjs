// Our own characters (the jk rig of the 2D clips) -> transparent PNG sprites for the 3D stage.
// usage: node sprites.cjs <port> <jobs.json>
// job: { id, who, track:[{t,mode,eyes,mouth,...}], blinks:[...], dur, flip, ppx (px per rig unit), canvas:[x0,y0,x1,y1] (rig units, feet at 0,0, y down),
//        frames:[{t, out}] }  -> writes each out PNG; prints JSON {id, w, h} per job
const pw = require('playwright'); const fs = require('fs');
(async () => {
  const [port, jobsPath] = process.argv.slice(2); const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
  const b = await pw.chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1600, height: 1600 } });
  p.on('pageerror', (e) => console.error('PAGEERROR', e.message));
  await p.goto(`http://localhost:${port}/index.html`, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  await p.evaluate(() => { document.documentElement.style.background = 'transparent'; document.body.style.background = 'transparent';
    const NS = 'http://www.w3.org/2000/svg'; const dd = document.createElementNS(NS, 'svg'); dd.id = 'sprdefs'; dd.setAttribute('width', 0); dd.setAttribute('height', 0); dd.style.cssText = 'position:absolute;left:-10px;top:-10px';
    const defs = document.createElementNS(NS, 'defs'); document.querySelectorAll('defs > *').forEach((d) => { if (d.id) defs.appendChild(d.cloneNode(true)); }); dd.appendChild(defs);
    for (const c of [...document.body.children]) c.style.display = 'none';
    document.body.appendChild(dd);
    const s = document.createElementNS(NS, 'svg'); s.id = 'spr'; s.style.cssText = 'position:fixed;left:0;top:0;background:transparent;overflow:visible';
    document.body.appendChild(s); });
  const out = [];
  for (const j of jobs) {
    const [x0, y0, x1, y1] = j.canvas; const W = Math.round((x1 - x0) * j.ppx), H = Math.round((y1 - y0) * j.ppx);
    await p.setViewportSize({ width: Math.max(W, 64), height: Math.max(H, 64) });
    await p.evaluate((j) => { const s = document.getElementById('spr'); const [x0, y0, x1, y1] = j.canvas;
      s.setAttribute('width', Math.round((x1 - x0) * j.ppx)); s.setAttribute('height', Math.round((y1 - y0) * j.ppx));
      s.setAttribute('viewBox', `${x0} ${y0} ${x1 - x0} ${y1 - y0}`); s.innerHTML = '';
      const NS = 'http://www.w3.org/2000/svg'; const g = document.createElementNS(NS, 'g'); g.setAttribute('transform', `scale(${j.flip ? -1 : 1},1)`); s.appendChild(g);
      const aid = 'S' + j.id.replace(/[^a-zA-Z0-9]/g, '');
      if (j.pre) { try { (new Function(j.pre))(); } catch (e) { console.error('pre', e); } }
      window.__stl = gsap.timeline({ paused: true });
      const list = j.actors || [{ who: j.who, track: j.track, blinks: j.blinks, dx: 0, flip: false }];
      list.forEach((a, k) => { const sub = document.createElementNS(NS, 'g'); const id2 = k ? aid + 'x' + k : aid;
        sub.setAttribute('transform', `translate(${a.dx || 0},${a.dy || 0}) scale(${a.flip ? -1 : 1},1)`); g.appendChild(sub);
        if (a.talk) a.track.talk = a.talk; Rig.build(sub, id2, Rig.CAST[a.who]); Rig.drive(window.__stl, id2, 0, j.dur, a.track, a.blinks || [0.9, 2.7, 4.6]); });
      if (j.extra) { try { (new Function('aid', 'tl', j.extra))(aid, window.__stl); } catch (e) { console.error(e); } }
    }, j);
    const anc = [];
    for (const f of j.frames) {
      const a = await p.evaluate(([t, j]) => { window.__stl.seek(Math.max(0, t), false);
        const aid = 'S' + j.id.replace(/[^a-zA-Z0-9]/g, ''); const s = document.getElementById('spr'); const r = s.getBoundingClientRect(); const [x0, y0] = j.canvas; const o = {};
        (j.anchors || []).forEach((q) => { const el = document.querySelector(q.sel.replace('{aid}', aid)); if (!el) return; const pt = s.createSVGPoint(); pt.x = q.x; pt.y = q.y;
          const m = pt.matrixTransform(el.getScreenCTM()); o[q.name] = [+(x0 + (m.x - r.left) / j.ppx).toFixed(2), +(y0 + (m.y - r.top) / j.ppx).toFixed(2)]; });
        return o; }, [f.t, j]);
      if (f.out) { const el = await p.$('#spr'); await el.screenshot({ path: f.out, omitBackground: true }); }
      anc.push(a);
    }
    out.push({ id: j.id, w: W, h: H, anchors: anc });
  }
  console.log(JSON.stringify(out)); await b.close();
})();
