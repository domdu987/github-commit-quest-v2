/* ============================================================
   HyperFrame — เอนจินไทม์ไลน์แบบ "เฟรมแน่นอน" (deterministic)
   ทุกอย่างบนจอเป็นฟังก์ชันของเวลา t เท่านั้น ไม่มี CSS animation / rAF
   เรนเดอร์ด้วยการเรียก HF.seek(t) แล้วถ่ายภาพหน้าจอทีละเฟรม
   ============================================================ */
window.HF = (() => {
  const W = 720, H = 1280;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const E = {
    linear: t => t,
    inQuad: t => t * t,
    outQuad: t => 1 - (1 - t) * (1 - t),
    inOutQuad: t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
    inCubic: t => t * t * t,
    outCubic: t => 1 - Math.pow(1 - t, 3),
    inOutCubic: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
    outExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
    inExpo: t => t === 0 ? 0 : Math.pow(2, 10 * t - 10),
    outBack: t => { const c = 1.70158, d = c + 1; return 1 + d * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); },
    outElastic: t => t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - .75) * (2 * Math.PI) / 3) + 1,
    inOutSine: t => -(Math.cos(Math.PI * t) - 1) / 2,
    outSine: t => Math.sin(t * Math.PI / 2),
  };
  // seg: ความคืบหน้า 0..1 ของช่วง [start, start+dur]
  const seg = (t, start, dur, ease = E.inOutCubic) => ease(clamp((t - start) / dur));
  // kf: คีย์เฟรม [[t,v],[t,v],...] -> ค่า ณ เวลา t (รองรับค่าเป็นตัวเลข)
  function kf(t, keys, ease = E.inOutCubic) {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      if (t <= keys[i][0]) {
        const [t0, v0] = keys[i - 1], [t1, v1] = keys[i];
        const e = Array.isArray(ease) ? (ease[i - 1] || E.inOutCubic) : ease;
        return lerp(v0, v1, e(clamp((t - t0) / (t1 - t0))));
      }
    }
    return keys[keys.length - 1][1];
  }
  // สุ่มแบบกำหนดผลได้ (hash) — ใช้สำหรับฝุ่น/สั่น/กะพริบ
  function hash(n) { let x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
  function noise(t, seed = 0) { // 1D value noise, เรียบ
    const i = Math.floor(t), f = t - i, u = f * f * (3 - 2 * f);
    return lerp(hash(i + seed * 1000), hash(i + 1 + seed * 1000), u) * 2 - 1;
  }
  const shake = (t, amp, freq = 20, seed = 0) => ({ x: noise(t * freq, seed) * amp, y: noise(t * freq, seed + 7) * amp });
  // flicker: ไฟกะพริบ 0..1
  const flicker = (t, speed = 30, seed = 0, min = 0.6) => min + (1 - min) * (0.5 + 0.5 * noise(t * speed, seed));

  // ---------- DOM helpers ----------
  const $ = (id, root = document) => root.querySelector('#' + id);
  const attr = (el, o) => { for (const k in o) el.setAttribute(k, o[k]); };
  const tf = (el, { x = 0, y = 0, s = 1, r = 0, ox = 0, oy = 0 }) =>
    el.setAttribute('transform', `translate(${x} ${y}) translate(${ox} ${oy}) rotate(${r}) scale(${s}) translate(${-ox} ${-oy})`);
  const show = (el, on) => el.style.display = on ? '' : 'none';
  const op = (el, v) => el.setAttribute('opacity', clamp(v));
  // กล้อง: zoom เข้าจุด (cx,cy) ด้วย scale s และหมุน r (องศา)
  const cam = (el, { x = 360, y = 640, s = 1, r = 0, dx = 0, dy = 0 }) =>
    el.setAttribute('transform', `translate(${360 + dx} ${640 + dy}) scale(${s}) rotate(${r}) translate(${-x} ${-y})`);
  const fmt = n => n.toLocaleString('en-US');
  const pad2 = n => String(Math.max(0, Math.floor(n))).padStart(2, '0');

  // ---------- Timeline ----------
  const shots = [];
  let overlays = []; // {start,end,init,update}
  let world, ui;
  function shot(def) { shots.push(def); return def; }
  function overlay(def) { overlays.push(def); return def; }
  function mount(worldEl, uiEl) {
    world = worldEl; ui = uiEl;
    for (const s of shots) {
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('id', 'shot-' + s.id); g.style.display = 'none';
      world.appendChild(g); s.g = g; s.init && s.init(g);
    }
    for (const o of overlays) { o.init && o.init(ui); }
  }
  function seek(t) {
    for (const s of shots) {
      const on = t >= s.start && t < s.end;
      show(s.g, on);
      if (on) s.update && s.update(t - s.start, s.g, t, s.end - s.start);
    }
    for (const o of overlays) o.update && o.update(t);
  }
  return { W, H, E, clamp, lerp, seg, kf, hash, noise, shake, flicker, $, attr, tf, show, op, cam, fmt, pad2, shot, overlay, mount, seek, shots };
})();
