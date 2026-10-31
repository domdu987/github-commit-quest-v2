/* ============================================================
   UI overlays (HTML บน SVG): ซับไตเติล, HUD การ์ด, ชิปขั้นตอน, ตราประทับ,
   ป้ายชื่อ, การ์ดเสบียง, การ์ดจบ, และ post-FX (flash/fade/red pulse)
   ทุกอย่างเป็นฟังก์ชันของ t ผ่าน HF.overlay
   ============================================================ */
window.UI = (() => {
  const { seg, E, clamp, $, kf } = HF;
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const markup = s => esc(s).replace(/\[(.+?)\]/g, '<span class="hi">$1</span>').replace(/\{(.+?)\}/g, '<span class="yl">$1</span>');

  // ---------- ซับไตเติล: อ่านจาก window.CUES ----------
  HF.overlay({
    init(ui) { this.el = $('sub', ui); this.last = null; },
    update(t) {
      const q = CUES.find(c => t >= c.start && t < c.end && c.text);
      if (!q) { this.el.style.display = 'none'; this.last = null; return; }
      if (this.last !== q) { this.el.innerHTML = markup(q.text); this.last = q; }
      this.el.style.display = '';
      const a = seg(t, q.start, 0.16, E.outBack), o = seg(t, q.start, 0.1, E.linear) * (1 - seg(t, q.end - 0.12, 0.12, E.linear));
      this.el.style.opacity = o; this.el.style.transform = `translateY(${(1 - a) * 14}px) scale(${0.94 + 0.06 * a})`;
    }
  });

  // ---------- HUD การ์ด (เรียงบนซ้าย) ----------
  const hudItems = [];
  function hud(item) { hudItems.push(item); return item; }
  HF.overlay({
    init(ui) {
      this.box = $('hud', ui);
      for (const it of hudItems) {
        const d = document.createElement('div'); d.className = 'card ' + (it.cls || '');
        d.innerHTML = `<div class="ic">${it.icon}</div><div><div class="lb">${it.label}</div><div class="vl"><span class="v"></span>${it.unit ? `<small>${it.unit}</small>` : ''}</div></div>`;
        d.style.display = 'none'; this.box.appendChild(d); it.el = d; it.v = d.querySelector('.v');
      }
    },
    update(t) {
      for (const it of hudItems) {
        const on = t >= it.start && t < it.end;
        it.el.style.display = on ? '' : 'none'; if (!on) continue;
        const a = seg(t, it.start, 0.35, E.outBack), o = seg(t, it.start, 0.15, E.linear) * (1 - seg(t, it.end - 0.2, 0.2, E.linear));
        it.el.style.opacity = o; it.el.style.transform = `translateX(${(1 - a) * -30}px) scale(${0.85 + 0.15 * a})`;
        const v = typeof it.value === 'function' ? it.value(t) : it.value; if (it.v.textContent !== String(v)) it.v.textContent = v;
        if (it.pulse && t >= it.pulse) { const p = 1 + 0.06 * Math.max(0, Math.sin((t - it.pulse) * 14)) * (1 - seg(t, it.pulse, 0.5, E.linear)); it.el.style.transform += ` scale(${p})`; }
      }
    }
  });

  // ---------- ชิปขั้นตอน ----------
  let chipsDef = null;
  function chips(def) { chipsDef = def; }
  HF.overlay({
    init(ui) {
      this.box = $('chips', ui); if (!chipsDef) return;
      this.box.innerHTML = chipsDef.items.map((c, i) => `${i ? '<div class="chip-arrow">›</div>' : ''}<div class="chip"><div class="ic">${c.ic}</div><div class="lb">${c.lb}</div><div class="st">✓</div></div>`).join('');
      this.chips = [...this.box.querySelectorAll('.chip')];
    },
    update(t) {
      if (!chipsDef) return; const d = chipsDef; const on = t >= d.start && t < d.end; this.box.style.display = on ? '' : 'none'; if (!on) return;
      const states = d.state(t);
      this.chips.forEach((el, i) => {
        const a = seg(t, d.start + i * 0.18, 0.3, E.outBack); el.style.opacity = a; el.style.transform = `translateY(${(1 - a) * -20}px) scale(${0.8 + 0.2 * a})`;
        el.classList.toggle('off', states[i] === 'off'); el.querySelector('.st').textContent = states[i] === 'off' ? '✕' : '✓';
        if (states[i] === 'off') { const k = seg(t, d.offAt, 0.4, E.linear); el.style.transform += ` translateX(${Math.sin(k * 40) * (1 - k) * 6}px)`; }
      });
    }
  });

  // ---------- ตราประทับคำเดียว ----------
  const stamps = [];
  function stamp(s) { stamps.push(s); }
  HF.overlay({
    init(ui) { this.el = $('stamp', ui); },
    update(t) {
      const s = stamps.find(x => t >= x.start && t < x.end); this.el.style.display = s ? '' : 'none'; if (!s) return;
      if (this.el.dataset.k !== s.text) { this.el.innerHTML = `<span>${esc(s.text)}</span>`; this.el.dataset.k = s.text; }
      const a = seg(t, s.start, 0.22, E.outExpo); const sh = HF.shake(t, 6 * (1 - seg(t, s.start, 0.5, E.linear)), 40, 3);
      this.el.style.opacity = seg(t, s.start, 0.05, E.linear) * (1 - seg(t, s.end - 0.15, 0.15, E.linear));
      this.el.style.transform = `translate(${sh.x}px,${sh.y}px) scale(${2.2 - 1.2 * a}) rotate(${-6 + 4 * a}deg)`;
    }
  });

  // ---------- ป้ายชื่อตัวละคร ----------
  let tag = null; function nametag(d) { tag = d; }
  HF.overlay({
    init(ui) { this.el = $('nametag', ui); if (tag) this.el.innerHTML = `<div class="av">${tag.avatar || ''}</div><div><div class="nm">${esc(tag.name)}</div><div class="rl">${esc(tag.role)}</div></div>`; },
    update(t) {
      if (!tag) return; const on = t >= tag.start && t < tag.end; this.el.style.display = on ? '' : 'none'; if (!on) return;
      const a = seg(t, tag.start, 0.4, E.outBack); this.el.style.opacity = seg(t, tag.start, 0.12, E.linear) * (1 - seg(t, tag.end - 0.2, 0.2, E.linear));
      this.el.style.transform = `translate(${tag.x || 0}px,${tag.y || 0}px) scale(${0.7 + 0.3 * a}) rotate(${-4 * (1 - a)}deg)`;
    }
  });

  // ---------- การ์ดเสบียง ----------
  let inv = null; function inventory(d) { inv = d; }
  HF.overlay({
    init(ui) {
      this.el = $('inv', ui); if (!inv) return;
      this.el.innerHTML = `<h3><i>${inv.icon || '📋'}</i>${esc(inv.title)}</h3>` + inv.rows.map(r => `<div class="row"><div class="ri">${r.ic}</div><div class="rt"><b>${esc(r.label)}</b><div class="bar"><i></i></div></div><div class="rv"><span class="v"></span><small>${esc(r.unit || '')}</small></div><div class="ok">✓</div></div>`).join('');
      this.rows = [...this.el.querySelectorAll('.row')];
    },
    update(t) {
      if (!inv) return; const on = t >= inv.start && t < inv.end; this.el.style.display = on ? '' : 'none'; if (!on) return;
      const a = seg(t, inv.start, 0.45, E.outBack); this.el.style.opacity = seg(t, inv.start, 0.15, E.linear) * (1 - seg(t, inv.end - 0.25, 0.25, E.linear));
      this.el.style.transform = `translateY(${(1 - a) * -30}px) scale(${0.9 + 0.1 * a}) rotate(${-2 * (1 - a)}deg)`;
      inv.rows.forEach((r, i) => {
        const el = this.rows[i]; const ra = seg(t, r.at, 0.35, E.outBack); el.style.opacity = ra; el.style.transform = `translateX(${(1 - ra) * -20}px)`;
        const k = seg(t, r.at + 0.1, 0.9, E.outCubic); el.querySelector('.bar i').style.width = (r.bar * k * 100) + '%';
        el.querySelector('.v').textContent = typeof r.value === 'function' ? r.value(k) : r.value;
        const ok = seg(t, r.at + 1.0, 0.3, E.outBack); el.querySelector('.ok').style.transform = `scale(${ok})`;
      });
    }
  });

  // ---------- การ์ดจบ ----------
  let card = null; function endcard(d) { card = d; }
  HF.overlay({
    init(ui) { this.el = $('card', ui); if (card) this.el.innerHTML = `<div class="q">?</div><div class="ep">${esc(card.title)}</div><div class="ln"></div><div class="tz">${esc(card.teaser)}</div>`; },
    update(t) {
      if (!card) return; const on = t >= card.start && t < card.end; this.el.style.display = on ? '' : 'none'; if (!on) return;
      const s = card.start;
      const q = this.el.querySelector('.q'), ep = this.el.querySelector('.ep'), ln = this.el.querySelector('.ln'), tz = this.el.querySelector('.tz');
      const qa = seg(t, s + 0.1, 0.6, E.outBack); q.style.opacity = qa; q.style.transform = `scale(${qa}) rotate(${(1 - qa) * 20}deg)`; q.style.textShadow = `0 0 ${30 + 20 * Math.sin(t * 3)}px rgba(255,255,255,.5)`;
      const ea = seg(t, s + 0.6, 0.5, E.outExpo); ep.style.opacity = ea; ep.style.transform = `translateY(${(1 - ea) * 30}px)`;
      ln.style.transform = `scaleX(${seg(t, s + 0.9, 0.5, E.outExpo)})`;
      const ta = seg(t, s + 1.3, 0.5, E.outCubic); tz.style.opacity = ta; tz.style.transform = `translateY(${(1 - ta) * 16}px)`;
      this.el.style.background = `radial-gradient(ellipse at 50% 40%, rgba(90,20,20,${0.35 * seg(t, s, 1.5, E.linear)}) 0%, #0b0b0f 70%)`;
    }
  });

  // ---------- Post FX ----------
  const fx = { flashes: [], fades: [], reds: [], shakes: [] };
  function flash(t0, dur = 0.12, amp = 0.9) { fx.flashes.push([t0, dur, amp]); }
  function fade(s, e, from, to) { fx.fades.push([s, e, from, to]); }
  function red(s, e, amp = 1) { fx.reds.push([s, e, amp]); }
  HF.overlay({
    init(ui) { this.fl = document.getElementById('flash'); this.fd = document.getElementById('fade'); this.rp = document.getElementById('redpulse'); },
    update(t) {
      let f = 0; for (const [t0, d, amp] of fx.flashes) if (t >= t0 && t < t0 + d) f = Math.max(f, amp * (1 - (t - t0) / d));
      this.fl.style.opacity = f;
      let fdv = 0; for (const [s, e, a, b] of fx.fades) if (t >= s && t < e) fdv = HF.lerp(a, b, E.inOutSine((t - s) / (e - s))); else if (t >= e && b > 0 && t < e + 0.001) fdv = b;
      this.fd.style.opacity = fdv;
      let r = 0; for (const [s, e, amp] of fx.reds) if (t >= s && t < e) r = Math.max(r, amp * (0.5 + 0.5 * Math.sin((t - s) * 9)) * (1 - seg(t, e - 0.3, 0.3, E.linear)));
      this.rp.style.opacity = r;
    }
  });
  return { hud, chips, stamp, nametag, inventory, endcard, flash, fade, red, markup };
})();
