// "นับวัน" channel lockup on the end card: tear-off calendar logo with a heart, wordmark, handle.
(() => {
  const st = document.createElement('style');
  st.textContent = `.brand { position: absolute; left: 0; right: 0; margin: 0 auto; width: max-content; display: flex; align-items: center; gap: 22px; padding: 18px 34px 18px 20px; border-radius: 34px; background: rgba(255,255,255,.1); border: 2px solid rgba(255,255,255,.25); transform-origin: 50% 50%; }
  .brand .btx { display: flex; flex-direction: column; line-height: 1; }
  .brand b { font: 700 64px/1 Kanit; color: #fff; letter-spacing: .01em; }
  .brand small { font: 500 30px/1.2 Kanit; color: #ffd6e4; margin-top: 8px; }`;
  document.head.appendChild(st);
  function brandLogo(size) {
    return `<svg width="${size}" height="${size}" viewBox="0 0 100 100"><rect x="10" y="16" width="80" height="76" rx="16" fill="#fff" stroke="#33252a" stroke-width="5"/>
      <path d="M10,32 Q10,16 26,16 L74,16 Q90,16 90,32 L90,38 L10,38 Z" fill="#f04f7f" stroke="#33252a" stroke-width="5" stroke-linejoin="round"/>
      <rect x="28" y="6" width="9" height="20" rx="4.5" fill="#33252a"/><rect x="63" y="6" width="9" height="20" rx="4.5" fill="#33252a"/>
      <path d="M50,82 C30,70 32,52 50,61 C68,52 70,70 50,82 Z" fill="#f04f7f" stroke="#33252a" stroke-width="4"/>
      <path d="M78,92 L90,80 L90,92 Z" fill="#e9e3ea" stroke="#33252a" stroke-width="4" stroke-linejoin="round"/></svg>`;
  }
  const S = SHOTS[SHOTS.length - 1];
  const y = window.BRAND_TOP || 1360;
  const el = html('div', 'brand', S.ui); el.style.top = y + 'px';
  el.innerHTML = `${brandLogo(104)}<div class="btx"><b>นับวัน</b><small>ติดตาม @nabwan.th</small></div>`;
  const up = S.update;
  S.update = lt => {
    up(lt);
    const t0 = 1.75, k = spring(lt, t0, 14, 6.5);
    el.style.opacity = fadeIn(lt, t0, 0.15);
    el.style.transform = `translateY(${((1 - k) * 40).toFixed(1)}px) scale(${(0.85 + 0.15 * k).toFixed(3)})`;
  };
})();
