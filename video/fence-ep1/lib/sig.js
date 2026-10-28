// The channel signature beat, shared by every series: "ถูกหมด / ทุกข้อ… / ผิดแค่… / ข้อเดียว" over a checklist that fails.
// Sig.ui now builds the notebook-paper version (sigPaper: ticked in red pen, then torn); the older failing-terminal card (sigCard) stays for reuse.
// Usage in a template, for the shot keyed "sig" whose only voice line is s01:
//   ui: [Sig.ui(F, "คืนนี้ · เช็กลิสต์เอาตัวรอด", [["ไม่วิ่ง", true], ..., ["???", false]], D("sig"))],
//   cam: { keys: Sig.cam(F, { x, y, s }) }, shake: Sig.shake(F), fx(tl, id, t0) { Sig.fx(tl, id, t0, F, D("sig")); }
(function () {
  document.head.insertAdjacentHTML("beforeend", `<style>
    .zchk { position: absolute; left: 80px; width: 920px; z-index: 52; opacity: 0; font-family: Kanit; }
    .zchk .zc-in { position: relative; padding: 26px 36px 30px; border-radius: 28px; overflow: hidden;
      background: linear-gradient(180deg, rgba(16,20,22,.95), rgba(7,9,11,.97)); border: 4px solid rgba(244,236,216,.3); box-shadow: 0 24px 60px rgba(0,0,0,.7); }
    .zchk .zc-scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(255,255,255,.04) 0 2px, transparent 2px 6px); pointer-events: none; }
    .zchk .zc-bar { position: absolute; left: 0; right: 0; top: 0; height: 110px; background: linear-gradient(180deg, transparent, rgba(255,60,50,.32), transparent); opacity: 0; pointer-events: none; }
    .zchk .zc-h { display: flex; align-items: center; gap: 16px; margin-bottom: 14px; }
    .zchk .zc-dot { width: 20px; height: 20px; border-radius: 50%; background: #ff4a3a; box-shadow: 0 0 14px #ff4a3a; flex: none; }
    .zchk .zc-h b { font: 700 30px/1 Kanit; letter-spacing: 4px; color: #f2c55c; flex: 1; }
    .zchk .zc-tally { font: 900 46px/1 Kanit; color: #7fd1b9; min-width: 120px; text-align: right; }
    .zchk .zc-r { position: relative; display: flex; align-items: center; gap: 26px; padding: 14px 14px; margin: 0 -14px; border-top: 2px solid rgba(244,236,216,.1); opacity: 0; border-radius: 16px; }
    .zchk .zc-sw { position: absolute; inset: 0; overflow: hidden; border-radius: 16px; pointer-events: none; }
    .zchk .zc-sweep { position: absolute; top: 0; bottom: 0; left: 0; width: 40%; background: linear-gradient(90deg, transparent, rgba(127,209,185,.45), transparent); opacity: 0; pointer-events: none; }
    .zchk .zc-box { width: 86px; height: 86px; border-radius: 18px; border: 5px solid rgba(244,236,216,.55); flex: none; position: relative; box-sizing: border-box; }
    .zchk .zc-box svg { position: absolute; left: -5px; top: -5px; width: 86px; height: 86px; overflow: visible; }
    .zchk .ck { fill: none; stroke: #7fd1b9; stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 90; stroke-dashoffset: 90; }
    .zchk .xx { position: absolute; left: -5px; top: -5px; width: 86px; height: 86px; opacity: 0; } .zchk .xx svg { left: 0; top: 0; }
    .zchk .xx path { stroke: #fff; stroke-width: 12; stroke-linecap: round; }
    .zchk .zc-t { font: 900 60px/1.1 Kanit; color: #f4ecd8; position: relative; }
    .zchk .bad .zc-t { color: #ff8a7a; letter-spacing: 8px; }
    .zchk .zc-box svg.zc-crack { left: 38px; top: 38px; width: 2px; height: 2px; overflow: visible; pointer-events: none; }
    .zchk .zc-crack path { fill: none; stroke-linejoin: round; stroke-linecap: round; stroke-dasharray: 1000; stroke-dashoffset: 1000; }
    .zchk .zc-crack .c1 { stroke: rgba(0,0,0,.6); stroke-width: 7; } .zchk .zc-crack .c2 { stroke: rgba(255,240,230,.92); stroke-width: 2.6; }
  </style>`);
  GameUI.C.sigCard = {
    html: (id, o) => {
      const r = (() => { let q = 23; return () => ((q = (q * 1664525 + 1013904223) % 4294967296) / 4294967296); })();
      let cracks = "";
      for (let k = 0; k < 7; k++) {
        let x = 0, y = 0, d = "M0,0", br = "";
        const ang = -1.7 + k * 0.29;
        for (let j = 0; j < 8; j++) {
          const a2 = ang + (r() - 0.5) * 0.8, L = 45 + r() * 75;
          x += Math.cos(a2) * L; y += Math.sin(a2) * L; d += `L${x.toFixed(0)},${y.toFixed(0)}`;
          if (j === 2 || j === 5) { const ba = a2 + (r() > 0.5 ? 0.9 : -0.9); br += `M${x.toFixed(0)},${y.toFixed(0)}l${(Math.cos(ba) * 70).toFixed(0)},${(Math.sin(ba) * 70).toFixed(0)}l${(Math.cos(ba + 0.4) * 40).toFixed(0)},${(Math.sin(ba + 0.4) * 40).toFixed(0)}`; }
        }
        cracks += `<path class="c1" d="${d}${br}"/><path class="c2" d="${d}${br}"/>`;
      }
      return `<div id="${id}" class="zchk" style="top:${o.top ?? 470}px"><div class="zc-in" id="${id}-in"><div class="zc-scan"></div><div class="zc-bar" id="${id}-bar"></div>
        <div class="zc-h"><span class="zc-dot" id="${id}-dot"></span><b>${o.title}</b><span class="zc-tally" id="${id}-tally">✓ 0</span></div>
        ${o.items.map(([txt, ok], i) => `<div class="zc-r ${ok ? "ok" : "bad"}" id="${id}-r${i}"><span class="zc-sw"><i class="zc-sweep"></i></span><span class="zc-box">${ok
          ? `<svg viewBox="0 0 86 86"><path class="ck" d="M20,45 L37,61 L67,25"/></svg>`
          : `<span class="xx"><svg viewBox="0 0 86 86"><path d="M22,22L64,64M64,22L22,64"/></svg></span><svg class="zc-crack" id="${id}-crack">${cracks}</svg>`}</span><span class="zc-t">${txt}</span></div>`).join("")}
        </div></div>`;
    },
    anim(tl, id, t0, o) {
      const A = (t) => o.t0abs + t, el = document.getElementById(id), inner = document.getElementById(`${id}-in`);
      const bar = document.getElementById(`${id}-bar`), tally = document.getElementById(`${id}-tally`), dot = document.getElementById(`${id}-dot`);
      const qtx = el.querySelector(`#${id}-r${o.items.length - 1} .zc-t`), S3 = o.show[o.items.length - 1], X = o.mark[o.items.length - 1];
      const GL = ["???", "?▓?", "▒?░", "??▓", "░▒▓", "?!?", "▓?▒", "?░?"];
      const h = (n) => { const v = Math.sin(n * 127.1 + 311.7) * 43758.5453; return v - Math.floor(v); };
      // entrance: flicker on like a failing screen, with a colour split that settles
      tl.fromTo(`#${id}`, { opacity: 0, scale: 1.08, filter: "drop-shadow(14px 0 0 rgba(255,40,60,.8)) drop-shadow(-14px 0 0 rgba(40,220,255,.8))" },
        { opacity: 1, scale: 1, filter: "drop-shadow(0px 0 0 rgba(255,40,60,0)) drop-shadow(0px 0 0 rgba(40,220,255,0))", duration: 0.32, ease: "power3.out", immediateRender: false }, t0);
      o.items.forEach(([, ok], i) => {
        tl.fromTo(`#${id}-r${i}`, { opacity: 0, x: -50 }, { opacity: 1, x: 0, duration: 0.2, ease: "power3.out", immediateRender: false }, A(o.show[i]));
        if (ok) {
          tl.fromTo(`#${id}-r${i} .ck`, { strokeDashoffset: 90 }, { strokeDashoffset: 0, duration: 0.18, ease: "power2.out", immediateRender: false }, A(o.mark[i]));
          tl.fromTo(`#${id}-r${i} .zc-box`, { borderColor: "rgba(244,236,216,.55)", boxShadow: "0 0 0 0 rgba(127,209,185,.9)" }, { borderColor: "#7fd1b9", boxShadow: "0 0 0 22px rgba(127,209,185,0)", duration: 0.4, immediateRender: false }, A(o.mark[i]));
          tl.fromTo(`#${id}-r${i} .zc-sweep`, { opacity: 1, x: -380 }, { opacity: 0, x: 1100, duration: 0.45, ease: "power2.out", immediateRender: false }, A(o.mark[i]));
          tl.to(`#${id}-r${i}`, { opacity: 0.42, filter: "saturate(.3)", duration: 0.3 }, A(S3) + 0.05);   // the good news fades while ??? takes over
        } else {
          tl.fromTo(`#${id}-r${i} .zc-box`, { borderColor: "rgba(244,236,216,.55)" }, { borderColor: "#ff5a4a", duration: 0.12, repeat: 7, yoyo: true, immediateRender: false }, A(S3));
          tl.fromTo(`#${id}-r${i} .xx`, { opacity: 0, scale: 3.2 }, { opacity: 1, scale: 1, transformOrigin: "50% 50%", duration: 0.14, ease: "power4.in", immediateRender: false }, A(X));
          tl.fromTo(`#${id}-r${i} .zc-box`, { backgroundColor: "rgba(216,50,42,0)", borderColor: "#ff5a4a", boxShadow: "0 0 0 0 rgba(255,90,74,.95)" },
            { backgroundColor: "rgba(216,50,42,1)", borderColor: "#ff5a4a", boxShadow: "0 0 0 40px rgba(255,90,74,0)", duration: 0.45, immediateRender: false }, A(X) + 0.12);
          tl.fromTo(`#${id}-r${i}`, { backgroundColor: "rgba(216,50,42,0)" }, { backgroundColor: "rgba(216,50,42,.35)", duration: 0.2, immediateRender: false }, A(X) + 0.12);
        }
      });
      tl.fromTo(`#${id}-crack path`, { strokeDashoffset: 1000 }, { strokeDashoffset: 0, duration: 0.3, stagger: 0.015, ease: "power3.out", immediateRender: false }, A(X) + 0.12);
      // per-frame state: tally, scrambling ???, heartbeat border, scan bar, shake, dying-screen flicker
      const clock = { t: 0 }, Dsh = o.dur;
      const render = () => {
        const t = clock.t, sus = Math.min(1, Math.max(0, (t - S3) / (X - S3))), after = t >= X + 0.12;
        const n = o.mark.filter((m, i) => o.items[i][1] && t >= m).length;
        tally.textContent = after ? "✗ 1" : `✓ ${n}`; tally.style.color = after ? "#ff5a4a" : "#7fd1b9";
        qtx.textContent = t >= S3 && t < X + 0.12 ? GL[Math.floor(t * 18) % GL.length] : "???";
        const beat = Math.pow(Math.max(0, Math.sin((2 * Math.PI * (t - S3)) / 0.38)), 4) * (t >= S3 && !after ? 0.35 + 0.65 * sus : 0);
        inner.style.borderColor = after ? "#ff4a3a" : `rgba(255,${Math.round(236 - 170 * beat)},${Math.round(216 - 160 * beat)},${(0.3 + 0.7 * beat).toFixed(2)})`;
        inner.style.boxShadow = after ? "0 0 46px rgba(255,60,50,.55), 0 24px 60px rgba(0,0,0,.7)" : `0 0 ${Math.round(50 * beat)}px rgba(255,60,50,${(0.8 * beat).toFixed(2)}), 0 24px 60px rgba(0,0,0,.7)`;
        bar.style.opacity = t >= S3 && !after ? (0.4 + 0.5 * sus).toFixed(2) : 0;
        bar.style.transform = `translateY(${Math.round((((t - S3) * 1.7) % 1) * 560 - 110)}px)`;
        dot.style.opacity = Math.floor(t * (after ? 8 : 2.5)) % 2 ? 0.25 : 1;
        const amp = after ? 2 + 20 * Math.exp(-(t - X) * 5) : t >= S3 ? 1 + 6 * sus * sus : 0, k = Math.floor(t * 30);
        const fl = after && t > X + 0.4 && h(k * 3.1) > 0.82 ? 0.45 : 1;
        inner.style.transform = `translate(${((h(k) - 0.5) * 2 * amp).toFixed(1)}px,${((h(k + 0.5) - 0.5) * 2 * amp).toFixed(1)}px) rotate(${((h(k + 0.25) - 0.5) * amp * 0.12 + (after ? -1.6 : 0)).toFixed(2)}deg)`;
        inner.style.opacity = fl;
      };
      tl.to(clock, { t: Dsh, duration: Dsh, ease: "none", immediateRender: false, onUpdate: render }, o.t0abs);
      render();
    },
  };

  // ---------- the signature as a sheet of notebook paper (user 28 Oct: "เอาเป็นกระดาษติ๊กถูก แล้วฉีกขาด"):
  // a ruled page slaps onto the screen and is taped; each line is written in, a red pen ticks it; on "ผิดแค่…" the last line
  // (pencil "???") gets a shaky red circle and the page trembles; on "ข้อเดียว" a red ✗ slashes it and the page tears across
  // above that line — the bottom strip falls away, the top swings on its tape, and a stamp hits it. The page is drawn twice
  // (two clip-paths either side of the tear) so it reads as one sheet until it parts.
  document.head.insertAdjacentHTML("beforeend", `<style>
    .zpap { position: absolute; left: 70px; width: 940px; z-index: 52; opacity: 0; font-family: Kanit; }
    .zpap .zp-sh, .zpap .zp-piece, .zpap .zp-clip { position: absolute; inset: 0; }
    .zpap .zp-piece { filter: drop-shadow(0 20px 24px rgba(0,0,0,.55)) drop-shadow(0 3px 2px rgba(0,0,0,.35)); }
    .zpap .zp-pg { position: absolute; inset: 0; overflow: hidden; background: #f2ead6;
      background-image: radial-gradient(ellipse at 22% 12%, rgba(255,255,255,.7), transparent 55%), radial-gradient(ellipse at 85% 92%, rgba(140,110,60,.22), transparent 60%), radial-gradient(ellipse at 60% 45%, rgba(120,95,50,.08), transparent 70%); }
    .zpap .zp-lines { position: absolute; left: 0; right: 0; top: 126px; bottom: 0; background: repeating-linear-gradient(180deg, transparent 0 116px, rgba(64,104,178,.36) 116px 118px); }
    .zpap .zp-mg { position: absolute; top: 0; bottom: 0; left: 108px; width: 3px; background: rgba(206,64,54,.55); box-shadow: 6px 0 0 rgba(206,64,54,.18); }
    .zpap .zp-hole { position: absolute; left: 34px; width: 32px; height: 32px; border-radius: 50%; background: #121416; box-shadow: inset 0 4px 5px rgba(0,0,0,.7), 0 1px 0 rgba(255,255,255,.5); }
    .zpap .zp-tape { position: absolute; top: -26px; width: 190px; height: 58px; background: rgba(226,212,170,.82); box-shadow: 0 2px 4px rgba(0,0,0,.18); z-index: 3;
      clip-path: polygon(0 8%, 6% 0, 12% 10%, 20% 2%, 30% 9%, 40% 1%, 52% 8%, 64% 0, 76% 9%, 88% 2%, 100% 8%, 100% 92%, 90% 100%, 78% 91%, 66% 99%, 52% 92%, 40% 100%, 28% 91%, 16% 99%, 6% 92%, 0 100%); }
    .zpap .zp-h { position: absolute; left: 136px; right: 44px; top: 30px; height: 70px; display: flex; align-items: center; gap: 20px; }
    .zpap .zp-title { font: 700 34px/1.1 Kanit; color: #2b4a8f; flex: 1; transform: rotate(-1deg); transform-origin: 0 50%; }
    .zpap .zp-tally { font: 900 60px/1 Kanit; color: #c8302b; transform: rotate(-5deg); min-width: 130px; text-align: right; }
    .zpap .zp-r { position: absolute; left: 132px; right: 40px; height: 118px; display: flex; align-items: center; gap: 30px; opacity: 0; }
    .zpap .zp-box { width: 92px; height: 92px; flex: none; overflow: visible; }
    .zpap .zp-box path { fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .zpap .bx { stroke: #2b2722; stroke-width: 5; stroke-dasharray: 420; stroke-dashoffset: 420; }
    .zpap .ck { stroke: #c8302b; stroke-width: 13; stroke-dasharray: 160; stroke-dashoffset: 160; }
    .zpap .x1, .zpap .x2 { stroke: #c8302b; stroke-width: 15; stroke-dasharray: 140; stroke-dashoffset: 140; }
    .zpap .zp-t { position: relative; font: 800 58px/1.1 Kanit; color: #24211d; white-space: nowrap; }
    .zpap .zp-ink { display: inline-block; clip-path: inset(-20% 100% -30% 0); }
    .zpap .bad .zp-t { color: #5f5a54; letter-spacing: 8px; font-weight: 700; }
    .zpap .zp-circ { position: absolute; left: -34px; top: -26px; width: calc(100% + 68px); height: calc(100% + 52px); overflow: visible; }
    .zpap .zp-circ path { fill: none; stroke: #c8302b; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 1400; stroke-dashoffset: 1400; }
    .zpap .zp-stamp { position: absolute; right: 22px; font: 900 50px/1 Kanit; color: #c8302b; border: 8px double #c8302b; border-radius: 10px; padding: 8px 24px 12px;
      transform: rotate(-11deg); opacity: 0; mix-blend-mode: multiply; letter-spacing: 2px; }
    .zpap .zp-fib, .zpap .zp-tear { position: absolute; left: 0; top: 0; overflow: visible; pointer-events: none; }
    .zpap .zp-fib { opacity: 0; }
    .zpap .zp-tear path { fill: none; stroke-linecap: round; stroke-linejoin: round; }
  </style>`);
  GameUI.C.sigPaper = {
    html: (id, o) => {
      const n = o.items.length, W = 940, HEAD = 126, ROW = 118, H = HEAD + n * ROW + 48;
      let q = 41; const r = () => ((q = (q * 1664525 + 1013904223) % 4294967296) / 4294967296);
      const wob = (a) => (r() - 0.5) * a;
      // a hand-drawn square and a check that overshoots it, slightly different every row
      const box = () => `M${8 + wob(4)},${10 + wob(4)}C${34 + wob(6)},${7 + wob(5)} ${62 + wob(6)},${9 + wob(5)} ${84 + wob(4)},${9 + wob(4)}C${86 + wob(5)},${34 + wob(6)} ${85 + wob(5)},${60 + wob(6)} ${84 + wob(4)},${83 + wob(4)}C${60 + wob(6)},${86 + wob(5)} ${32 + wob(6)},${85 + wob(5)} ${9 + wob(4)},${84 + wob(4)}C${7 + wob(5)},${60 + wob(6)} ${8 + wob(5)},${34 + wob(6)} ${10 + wob(4)},${12 + wob(4)}`;
      const ck = `M10,50C18,56 27,64 34,76C46,50 64,24 98,-4`;
      // the tear: across the page just above the last line, rising a little to the right, ragged
      const yL = HEAD + (n - 1) * ROW - 2, pts = [];
      for (let x = 0; x <= W; x += 36) pts.push([Math.min(W, x + (x && x < W ? wob(14) : 0)), yL + 18 - (x / W) * 34 + (x && x < W ? wob(22) : 0)]);
      pts[pts.length - 1][0] = W;
      const P = (p) => `${p[0].toFixed(0)}px ${p[1].toFixed(0)}px`;
      const top = `polygon(0px -60px, ${W}px -60px, ${pts.slice().reverse().map(P).join(", ")})`;
      const bot = `polygon(${pts.map(P).join(", ")}, ${W}px ${H + 40}px, 0px ${H + 40}px)`;
      const line = `M${pts.map((p) => `${p[0].toFixed(0)},${p[1].toFixed(0)}`).join("L")}`;
      const holes = [90, H / 2, H - 90].map((y) => `<i class="zp-hole" style="top:${(y - 16).toFixed(0)}px"></i>`).join("");
      const rows = o.items.map(([txt, ok], i) => `<div class="zp-r zp-r${i} ${ok ? "ok" : "bad"}" style="top:${HEAD + i * ROW}px"><svg class="zp-box" viewBox="0 0 92 92"><path class="bx" d="${box()}"/>${ok
        ? `<path class="ck" d="${ck}"/>` : `<path class="x1" d="M6,4L90,90"/><path class="x2" d="M88,2L4,88"/>`}</svg><span class="zp-t"><span class="zp-ink">${txt}</span>${ok ? "" :
        `<svg class="zp-circ" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M8,52C6,18 40,6 66,10C92,14 98,40 94,60C88,90 40,96 18,82C2,70 4,40 30,24" vector-effect="non-scaling-stroke"/></svg>`}</span></div>`).join("");
      const page = `<div class="zp-pg"><div class="zp-lines"></div><div class="zp-mg"></div>${holes}
        <div class="zp-h"><b class="zp-title">${o.title}</b><span class="zp-tally">✓ 0</span></div>${rows}
        <div class="zp-stamp" style="top:${HEAD + 2 * ROW + 2}px">ผิด 1 ข้อ</div>
        <svg class="zp-fib" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><path d="${line}" stroke="#fffdf4" stroke-width="12" fill="none" stroke-linejoin="round"/><path d="${line}" stroke="#d9cdb0" stroke-width="3" stroke-dasharray="3 5 1 4" fill="none"/></svg></div>`;
      return `<div id="${id}" class="zpap" style="top:${o.top ?? 430}px; height:${H}px"><div class="zp-sh" id="${id}-sh">
        <i class="zp-tape" style="left:96px; transform:rotate(-7deg)"></i><i class="zp-tape" style="right:262px; transform:rotate(5deg)"></i>
        <div class="zp-piece" id="${id}-full">${page}</div>
        <div class="zp-piece" id="${id}-top" style="visibility:hidden"><div class="zp-clip" style="clip-path:${top}">${page}</div></div>
        <div class="zp-piece" id="${id}-bot" style="visibility:hidden"><div class="zp-clip" style="clip-path:${bot}">${page}</div></div>
        <svg class="zp-tear" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><path class="tr1" d="${line}" stroke="rgba(30,24,16,.75)" stroke-width="5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
          <path class="tr2" d="${line}" stroke="#fffaf0" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg></div></div>`;
    },
    anim(tl, id, t0, o) {
      const A = (t) => o.t0abs + t, n = o.items.length, el = document.getElementById(id), sh = document.getElementById(`${id}-sh`);
      const tallies = el.querySelectorAll(".zp-tally"), S3 = o.show[n - 1], X = o.mark[n - 1];
      const h = (k) => { const v = Math.sin(k * 127.1 + 311.7) * 43758.5453; return v - Math.floor(v); };
      // slapped on and taped
      tl.fromTo(`#${id}`, { opacity: 0, y: 220, rotation: -8 }, { opacity: 1, y: 0, rotation: -1.5, duration: 0.45, ease: "back.out(1.5)", immediateRender: false }, t0);
      tl.fromTo(`#${id} .zp-tape`, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power3.in", stagger: 0.08, immediateRender: false }, t0 + 0.3);
      o.items.forEach(([, ok], i) => {
        const R = `#${id} .zp-r${i}`;
        tl.fromTo(R, { opacity: 0 }, { opacity: 1, duration: 0.1, immediateRender: false }, A(o.show[i]));
        tl.fromTo(`${R} .bx`, { strokeDashoffset: 420 }, { strokeDashoffset: 0, duration: 0.24, ease: "power1.inOut", immediateRender: false }, A(o.show[i]));
        tl.fromTo(`${R} .zp-ink`, { clipPath: "inset(-20% 100% -30% 0%)" }, { clipPath: "inset(-20% 0% -30% 0%)", duration: ok ? 0.38 : 0.5, ease: "power1.inOut", immediateRender: false }, A(o.show[i]) + 0.12);
        if (ok) {
          tl.fromTo(`${R} .ck`, { strokeDashoffset: 160 }, { strokeDashoffset: 0, duration: 0.2, ease: "power2.in", immediateRender: false }, A(o.mark[i]));
          tl.fromTo(`${R} .zp-box`, { scale: 1 }, { scale: 1.12, transformOrigin: "50% 50%", duration: 0.07, yoyo: true, repeat: 1, immediateRender: false }, A(o.mark[i]) + 0.18);
          tl.to(`${R}`, { opacity: 0.55, duration: 0.3 }, A(S3) + 0.1);   // the good lines fade back while ??? takes over
        } else {
          tl.fromTo(`${R} .zp-circ path`, { strokeDashoffset: 1400 }, { strokeDashoffset: 0, duration: 0.45, ease: "power1.inOut", immediateRender: false }, A(S3) + 0.45);
          tl.fromTo(`${R} .x1`, { strokeDashoffset: 140 }, { strokeDashoffset: 0, duration: 0.11, ease: "power3.in", immediateRender: false }, A(X));
          tl.fromTo(`${R} .x2`, { strokeDashoffset: 140 }, { strokeDashoffset: 0, duration: 0.11, ease: "power3.in", immediateRender: false }, A(X) + 0.1);
        }
      });
      // the tear: a ragged line runs across, the strip with the ✗ falls away, the top swings on its tape, a stamp hits it
      const T = A(X) + 0.24, S = T + 0.2;
      tl.fromTo(`#${id} .zp-tear path`, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.2, ease: "power2.in", immediateRender: false }, T);
      tl.set(`#${id} .zp-fib`, { opacity: 1 }, S); tl.set([`#${id}-top`, `#${id}-bot`], { visibility: "visible" }, S); tl.set(`#${id}-full`, { visibility: "hidden" }, S); tl.to(`#${id} .zp-tear`, { opacity: 0, duration: 0.1 }, S);
      tl.fromTo(`#${id}-bot`, { x: 0, y: 0, rotation: 0 }, { x: 240, y: 1500, rotation: 34, transformOrigin: "15% 85%", duration: 1.35, ease: "power2.in", immediateRender: false }, S);
      tl.fromTo(`#${id}-bot`, { skewX: 0 }, { skewX: 6, duration: 0.18, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, S + 0.1);   // the strip flutters as it drops
      tl.fromTo(`#${id}-top`, { rotation: 0, y: 0, x: 0 }, { rotation: -4.5, y: -26, x: -12, transformOrigin: "50% 0%", duration: 0.55, ease: "back.out(2.6)", immediateRender: false }, S);
      tl.fromTo(`#${id} .zp-stamp`, { opacity: 0, scale: 2.4 }, { opacity: 0.92, scale: 1, transformOrigin: "50% 50%", duration: 0.16, ease: "power4.in", immediateRender: false }, S + 0.42);
      tl.fromTo(`#${id}-top`, { scale: 1 }, { scale: 1.025, transformOrigin: "50% 30%", duration: 0.06, yoyo: true, repeat: 1, immediateRender: false }, S + 0.56);
      // per-frame: the tally, and the page trembling harder from "ผิดแค่…" until it tears
      const clock = { t: 0 };
      const render = () => {
        const t = clock.t, nOk = o.mark.filter((m, i) => o.items[i][1] && t >= m + 0.15).length, after = t >= X + 0.1;
        tallies.forEach((e) => { e.textContent = after ? "✗ 1" : `✓ ${nOk}`; });
        const sus = Math.min(1, Math.max(0, (t - S3) / Math.max(0.2, X - S3))), k = Math.floor(t * 30);
        const amp = t >= X && t < X + 0.6 ? 9 * (1 - (t - X) / 0.6) : t >= S3 && t < X ? 0.8 + 4.5 * sus * sus : 0;
        sh.style.transform = `translate(${((h(k) - 0.5) * 2 * amp).toFixed(1)}px,${((h(k + 0.5) - 0.5) * 2 * amp).toFixed(1)}px) rotate(${((h(k + 0.25) - 0.5) * amp * 0.14).toFixed(2)}deg)`;
      };
      tl.to(clock, { t: o.dur, duration: o.dur, ease: "none", immediateRender: false, onUpdate: render }, o.t0abs);
      render();
    },
  };

  const f = (F, j) => F("sig", 0, j);
  // reveal and tick times for n items (the last one is the ??? row): ticks spread over "ถูกหมด… ทุกข้อ…"
  function ui(F, title, items, dur, top = 440) {
    const n = items.length - 1, a = f(F, 0), b = f(F, 1) + 0.15;
    const mark = items.slice(0, n).map((_, i) => (n === 1 ? b : a + 0.3 + ((b - a - 0.3) * i) / (n - 1)));
    const show = mark.map((m, i) => Math.min(m - 0.2, a + 0.05 + i * 0.25));
    return { type: "sigPaper", t: 0.05, title, items, show: [...show, f(F, 2)], mark: [...mark, f(F, 3)], top, dur };
  }
  // a slow push that steps in on "ผิดแค่…" and again on "ข้อเดียว" (zoom about the frame centre)
  const cam = (F, k) => [{ t: 0, ...k, drift: { s: 0.02 } }, { t: f(F, 2), ...k, s: k.s * 1.04, drift: { s: 0.045 } }, { t: f(F, 3), ...k, s: k.s * 1.12, drift: { s: 0.02 } }];
  const shake = (F) => (t) => (t > f(F, 3) && t < f(F, 3) + 0.5 ? 14 * Math.sin(t * 63) * (f(F, 3) + 0.5 - t) / 0.5 : 0);
  function fx(tl, id, t0, F, dur) {
    const X = f(F, 3), P = f(F, 2);
    Fx.desat(tl, `#${id} .stage`, t0, undefined, 0.2);
    Fx.heart(tl, t0 + P, X - P, 0.38, 0.45); Fx.tunnel(tl, t0 + P, t0 + X + 0.35, 0.6);
    Fx.glitch(tl, `#${id}`, t0 + P, 0.12, 8, 73);
    Fx.punch(tl, `#${id} .stage`, t0 + X, 1.1, 0.5); Fx.glitch(tl, `#${id}`, t0 + X, 0.35, 16, 74);
    tl.fromTo("#fxred", { opacity: 0.9 }, { opacity: 0, duration: 0.7, immediateRender: false }, t0 + X);
    tl.fromTo("#flashw", { opacity: 0.5 }, { opacity: 0, duration: 0.12, immediateRender: false }, t0 + X);
    Fx.heart(tl, t0 + X + 0.2, dur - X - 0.2, 0.5, 0.5);
  }
  window.Sig = { ui, cam, shake, fx };
})();
