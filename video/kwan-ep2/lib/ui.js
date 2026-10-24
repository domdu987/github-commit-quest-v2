// Small top-of-screen knowledge cards and comic captions. Cards stay small (one icon, one short line,
// optional label/value) so the story keeps playing behind them.
(function () {
  const INK = "#2e2a26";
  const ICONS = {
    warn: `<path d="M20,4L37,34H3Z" fill="#e07a4f" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/><path d="M20,14v10M20,28v1" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`,
    co: `<path d="M8,26a8,8 0 0 1 2,-15a10,10 0 0 1 19,-2a8,8 0 0 1 3,17z" fill="#c9c3b6" stroke="${INK}" stroke-width="3"/><text x="20" y="25" text-anchor="middle" font-family="Kanit" font-weight="900" font-size="12" fill="${INK}">CO</text>`,
    head: `<circle cx="20" cy="18" r="12" fill="#e9bc93" stroke="${INK}" stroke-width="3"/><path d="M8,8l-4,-4M32,8l4,-4M20,2v-2" stroke="#e07a4f" stroke-width="3" stroke-linecap="round"/><path d="M14,18l4,-2M26,18l-4,-2M15,25q5,-3 10,0" stroke="${INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`,
    air: `<rect x="5" y="5" width="30" height="30" rx="3" fill="#cfe2e6" stroke="${INK}" stroke-width="3"/><path d="M20,5V35M5,20H35" stroke="${INK}" stroke-width="3"/><path d="M38,12q6,4 0,8M38,22q6,4 0,8" stroke="#5fa8a0" stroke-width="3" fill="none" stroke-linecap="round"/>`,
    phone: `<rect x="11" y="3" width="18" height="34" rx="4" fill="#3d3833" stroke="${INK}" stroke-width="3"/><rect x="14" y="8" width="12" height="20" fill="#cfe2e6"/><circle cx="20" cy="32" r="2" fill="#f4ecd8"/>`,
    cat: `<path d="M8,34V14L12,4L18,12H22L28,4L32,14V34Z" fill="#e07a4f" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/><circle cx="15" cy="20" r="2.4" fill="${INK}"/><circle cx="25" cy="20" r="2.4" fill="${INK}"/>`,
    clock: `<circle cx="20" cy="20" r="15" fill="#f4ecd8" stroke="${INK}" stroke-width="3"/><path d="M20,11v10l7,4" stroke="${INK}" stroke-width="3" fill="none" stroke-linecap="round"/>`,
    fuel: `<rect x="8" y="10" width="24" height="26" rx="4" fill="#c0603e" stroke="${INK}" stroke-width="3"/><path d="M14,10V5h10l4,5" stroke="${INK}" stroke-width="3" fill="none"/><path d="M14,18l12,10M26,18l-12,10" stroke="#f4ecd8" stroke-width="3"/>`,
    ghost: `<path d="M8,36V18a12,12 0 0 1 24,0V36l-4,-4l-4,4l-4,-4l-4,4l-4,-4z" fill="#e8e2d4" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/><circle cx="16" cy="18" r="2.5" fill="${INK}"/><circle cx="24" cy="18" r="2.5" fill="${INK}"/>`,
  };

  // keyword marking: "ไฟดับ = [ปั๊มหยุด]" -> highlighted span
  const mark = (s) => s.replace(/\[([^\]]+)\]/g, '<span class="k">$1</span>').replace(/\{([^}]+)\}/g, '<span class="k kr">$1</span>');

  function card(id, o) {
    const icon = ICONS[o.icon] || ICONS.warn;
    const side = o.side === "right" ? "right:40px" : "left:40px";
    return `<div id="${id}" class="uicard" style="${side}; top:${o.top || 120}px">
      <svg class="ico" viewBox="0 0 40 40" width="58" height="58">${icon}</svg>
      <div>${o.label ? `<div class="lbl">${o.label}</div>` : ""}<div class="txt">${mark(o.text)}</div></div>
      ${o.value ? `<div class="val">${o.value}</div>` : ""}</div>`;
  }

  function caption(id, text) {
    return `<div id="${id}" class="capbox">${mark(text)}</div>`;
  }

  const CSS = `
    .uicard { position:absolute; display:flex; gap:14px; align-items:center; max-width:640px; background:rgba(244,236,216,.95);
      border:4px solid ${INK}; border-radius:16px; box-shadow:5px 5px 0 rgba(46,42,38,.7); padding:12px 20px 14px 14px; opacity:0; }
    .uicard .lbl { font:700 22px/1.1 Kanit; color:#7a6c5d; letter-spacing:2px; }
    .uicard .txt { font:900 38px/1.15 Kanit; color:${INK}; white-space:nowrap; }
    .uicard .val { margin-left:6px; font:900 46px/1 Kanit; color:#b0553a; }
    .uicard .k, .capbox .k { display:inline-block; padding:0 .14em; margin:0 .04em; background:#e07a4f; border:3px solid ${INK}; border-radius:7px; transform:rotate(-2deg); }
    .capwrap { position:absolute; left:0; right:0; top:1630px; display:flex; justify-content:center; pointer-events:none; }
    .capbox { position:absolute; background:#f4ecd8; color:${INK}; border:5px solid ${INK}; border-radius:6px; box-shadow:8px 8px 0 rgba(46,42,38,.85);
      padding:14px 30px 18px; font:900 58px/1.25 Kanit; white-space:nowrap; opacity:0; }
    .bubble { position:absolute; background:#f4ecd8; border:5px solid ${INK}; border-radius:26px; padding:16px 26px 20px; font:900 46px/1.2 Kanit; color:${INK};
      box-shadow:6px 6px 0 rgba(46,42,38,.8); white-space:nowrap; opacity:0; }
    .bubble:after { content:""; position:absolute; bottom:-30px; left:var(--tail, 40px); width:40px; height:32px; background:#f4ecd8; border:5px solid ${INK}; border-top:0;
      clip-path:polygon(0 0,100% 0,30% 100%); }`;

  window.Ui = { card, caption, mark, CSS, ICONS };
})();
