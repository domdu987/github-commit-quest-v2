/* ============================================================
   ART — ไลบรารีวาด SVG (เรื่อง "คอนโดชั้น 23") สไตล์เวกเตอร์แฟลตโทนอุ่น
   ทุกฟังก์ชันคืนสตริง SVG; ส่วนที่ขยับได้ติด class ให้ shots ควบคุม
   ไอคอนทุกตัววาดเอง (ART.icon) ไม่ใช้อีโมจิ
   ============================================================ */
window.ART = (() => {
  const P = {
    skin: '#eab995', skinD: '#c9906b', hair: '#1f1a1f', blouse: '#f4f1ea', blouseD: '#d9d3c6', pants: '#2b3350', shoe: '#8c6a4f',
    cat: '#e8913a', catD: '#c56d1e', catL: '#f7c58a', nose: '#d96a6a',
    wall: '#e6dccb', wallD: '#c9bda8', floor: '#8f7b63', floorD: '#6e5c47', steel: '#9aa1a8', steelD: '#5f666e', dark: '#15161c',
    cream: '#f6efe0', red: '#d7342c', yellow: '#f5c542', blue: '#2b7bc0', water: '#5fc1e6', waterD: '#2d8fc2', green: '#2f9e5a', orange: '#f28b2b',
    glass: '#9ad2e6', ink: '#2a2622', inkL: '#6b645a',
  };
  const joint = (x, y, r = 7, c = P.skin) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;

  // ---------- ไอคอนชุดใหม่ (วาดเอง) viewBox 0 0 48 48 ----------
  const ICONS = {
    water: `<path d="M24 6 C24 6 10 22 10 30 a14 14 0 0 0 28 0 C38 22 24 6 24 6z" fill="#5fc1e6" stroke="#1f3b4d" stroke-width="3" stroke-linejoin="round"/><path d="M17 30 a7 7 0 0 0 7 7" stroke="#fff" stroke-width="3" stroke-linecap="round" fill="none"/>`,
    bolt: `<path d="M27 4 L12 27 h11 l-3 17 L36 20 H25 z" fill="#f5c542" stroke="#4a3a00" stroke-width="3" stroke-linejoin="round"/>`,
    elevator: `<rect x="8" y="4" width="32" height="40" rx="4" fill="#9aa1a8" stroke="#2a2f36" stroke-width="3"/><rect x="13" y="10" width="10" height="30" fill="#e8eef2" stroke="#2a2f36" stroke-width="2"/><rect x="25" y="10" width="10" height="30" fill="#e8eef2" stroke="#2a2f36" stroke-width="2"/><path d="M20 7 l4 -4 l4 4" stroke="#2a2f36" stroke-width="2.5" fill="none" stroke-linecap="round"/>`,
    stairs: `<path d="M6 42 h9 v-9 h9 v-9 h9 v-9 h9 v-7" stroke="#2a2f36" stroke-width="3.5" fill="none" stroke-linejoin="round" stroke-linecap="round"/><path d="M6 42 h9 v-9 h9 v-9 h9 v-9 h9 v27z" fill="#f28b2b" opacity=".85"/>`,
    firedoor: `<rect x="10" y="4" width="28" height="40" rx="3" fill="#d7342c" stroke="#4a0c08" stroke-width="3"/><rect x="15" y="9" width="18" height="13" rx="2" fill="#f0a39e" opacity=".9"/><rect x="29" y="27" width="6" height="4" rx="2" fill="#f6efe0"/><path d="M4 44 h40" stroke="#4a0c08" stroke-width="3" stroke-linecap="round"/>`,
    people: `<circle cx="17" cy="14" r="7" fill="#f4c99b" stroke="#2a2f36" stroke-width="3"/><path d="M4 42 v-8 a13 13 0 0 1 26 0 v8z" fill="#2b7bc0" stroke="#2a2f36" stroke-width="3" stroke-linejoin="round"/><circle cx="34" cy="16" r="6" fill="#f4c99b" stroke="#2a2f36" stroke-width="3"/><path d="M28 42 v-8 a10 10 0 0 1 16 -8 v16z" fill="#2f9e5a" stroke="#2a2f36" stroke-width="3" stroke-linejoin="round"/>`,
    cat: `<path d="M10 20 l-2 -13 l11 8z M38 20 l2 -13 l-11 8z" fill="#e8913a" stroke="#4a2a0a" stroke-width="3" stroke-linejoin="round"/><ellipse cx="24" cy="27" rx="16" ry="14" fill="#e8913a" stroke="#4a2a0a" stroke-width="3"/><circle cx="18" cy="25" r="2.5" fill="#1f1a1f"/><circle cx="30" cy="25" r="2.5" fill="#1f1a1f"/><path d="M22 31 h4 l-2 3z" fill="#d96a6a"/><path d="M8 30 h7 M8 35 h7 M33 30 h7 M33 35 h7" stroke="#4a2a0a" stroke-width="2" stroke-linecap="round"/>`,
    bottle: `<rect x="19" y="4" width="10" height="6" rx="2" fill="#2b7bc0"/><path d="M17 12 h14 l3 8 v22 a3 3 0 0 1 -3 3 h-14 a3 3 0 0 1 -3 -3 v-22z" fill="#cfeefb" stroke="#1f3b4d" stroke-width="3" stroke-linejoin="round"/><rect x="16" y="26" width="16" height="15" fill="#5fc1e6"/>`,
    noodle: `<path d="M6 20 h36 l-4 20 a4 4 0 0 1 -4 4 h-20 a4 4 0 0 1 -4 -4z" fill="#f28b2b" stroke="#4a2a0a" stroke-width="3" stroke-linejoin="round"/><path d="M12 20 c2 -10 8 -12 12 -12 s10 2 12 12" stroke="#f5c542" stroke-width="3" fill="none"/><path d="M14 20 c4 -6 16 -6 20 0" stroke="#f5c542" stroke-width="3" fill="none"/><path d="M28 6 l8 10" stroke="#8c6a4f" stroke-width="3" stroke-linecap="round"/>`,
    rice: `<path d="M12 44 l2 -26 h20 l2 26z" fill="#f6efe0" stroke="#4a3a2a" stroke-width="3" stroke-linejoin="round"/><path d="M14 18 l-4 -8 h28 l-4 8" fill="#d9d3c6" stroke="#4a3a2a" stroke-width="3" stroke-linejoin="round"/><circle cx="24" cy="31" r="5" fill="#d7342c"/>`,
    gauge: `<path d="M6 34 a18 18 0 0 1 36 0" stroke="#2a2f36" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M6 34 a18 18 0 0 1 10 -15" stroke="#2f9e5a" stroke-width="6" fill="none"/><path d="M32 19 a18 18 0 0 1 10 15" stroke="#d7342c" stroke-width="6" fill="none"/><path d="M24 34 L14 24" stroke="#d7342c" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="34" r="4" fill="#2a2f36"/>`,
    clock: `<circle cx="24" cy="26" r="17" fill="#f6efe0" stroke="#2a2f36" stroke-width="3.5"/><path d="M24 14 v12 l8 5" stroke="#d7342c" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M18 5 h12" stroke="#2a2f36" stroke-width="4" stroke-linecap="round"/>`,
    building: `<rect x="10" y="4" width="28" height="40" fill="#9aa1a8" stroke="#2a2f36" stroke-width="3"/>${[0, 1, 2, 3].map(r => [0, 1].map(c => `<rect x="${15 + c * 11}" y="${9 + r * 8}" width="7" height="5" fill="${(r + c) % 3 ? '#f5c542' : '#2a2f36'}"/>`).join('')).join('')}<rect x="20" y="36" width="8" height="8" fill="#2a2f36"/>`,
    key: `<circle cx="16" cy="18" r="9" fill="#f5c542" stroke="#4a3a00" stroke-width="3"/><circle cx="16" cy="18" r="3" fill="#4a3a00"/><path d="M23 24 l18 18 M34 35 l5 -5 M29 30 l5 -5" stroke="#4a3a00" stroke-width="4" stroke-linecap="round"/>`,
    lobby: `<rect x="4" y="20" width="40" height="24" fill="#d7342c" stroke="#4a0c08" stroke-width="3"/><path d="M4 20 L24 6 L44 20z" fill="#f6efe0" stroke="#4a0c08" stroke-width="3" stroke-linejoin="round"/><rect x="19" y="30" width="10" height="14" fill="#f6efe0"/>`,
    bucket: `<path d="M10 16 h28 l-3 26 a3 3 0 0 1 -3 3 h-16 a3 3 0 0 1 -3 -3z" fill="#2b7bc0" stroke="#163c5e" stroke-width="3" stroke-linejoin="round"/><path d="M12 16 a12 10 0 0 1 24 0" stroke="#163c5e" stroke-width="3" fill="none"/><rect x="12" y="24" width="24" height="6" fill="#5fc1e6" opacity=".9"/>`,
    tank: `<rect x="6" y="14" width="36" height="24" rx="6" fill="#9aa1a8" stroke="#2a2f36" stroke-width="3"/><rect x="9" y="24" width="30" height="11" rx="3" fill="#5fc1e6"/><path d="M14 38 v6 M34 38 v6 M22 6 h4 v8" stroke="#2a2f36" stroke-width="3" stroke-linecap="round"/>`,
    lock: `<rect x="10" y="20" width="28" height="22" rx="4" fill="#f5c542" stroke="#4a3a00" stroke-width="3"/><path d="M16 20 v-6 a8 8 0 0 1 16 0 v6" stroke="#4a3a00" stroke-width="3.5" fill="none"/><circle cx="24" cy="31" r="3" fill="#4a3a00"/>`,
    warning: `<path d="M24 5 L45 42 H3z" fill="#f5c542" stroke="#4a3a00" stroke-width="3" stroke-linejoin="round"/><path d="M24 18 v12" stroke="#4a3a00" stroke-width="4" stroke-linecap="round"/><circle cx="24" cy="36" r="2.5" fill="#4a3a00"/>`,
    pin: `<path d="M24 44 C24 44 10 28 10 18 a14 14 0 0 1 28 0 c0 10 -14 26 -14 26z" fill="#d7342c" stroke="#4a0c08" stroke-width="3" stroke-linejoin="round"/><circle cx="24" cy="18" r="5" fill="#f6efe0"/>`,
    zombie: `<rect x="16" y="4" width="16" height="14" rx="5" fill="#8fbf8f" stroke="#1f3b1f" stroke-width="3"/><rect x="14" y="20" width="20" height="16" rx="3" fill="#5b7a5b" stroke="#1f3b1f" stroke-width="3"/><path d="M6 24 h8 M34 24 h8 M18 36 v8 M30 36 v8" stroke="#1f3b1f" stroke-width="4" stroke-linecap="round"/><circle cx="21" cy="10" r="1.8" fill="#1f3b1f"/><circle cx="27" cy="10" r="1.8" fill="#1f3b1f"/>`,
    up: `<path d="M24 40 V10 M12 22 L24 10 L36 22" stroke="#2a2f36" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
    tap: `<path d="M8 20 h22 a6 6 0 0 1 6 6 v6" stroke="#2a2f36" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M14 20 v-8 h-6 M14 12 h8" stroke="#2a2f36" stroke-width="5" stroke-linecap="round"/><path d="M36 36 c0 3 -2 5 -2 7 a2 2 0 0 0 4 0 c0 -2 -2 -4 -2 -7z" fill="#5fc1e6"/>`,
  };
  const icon = (name, size = 48, extra = '') => `<svg viewBox="0 0 48 48" width="${size}" height="${size}" ${extra}>${ICONS[name] || ''}</svg>`;

  // ---------- ตัวละครหลัก "ปอ" พนักงานออฟฟิศ (ด้านข้าง หันขวา) ----------
  // จุดกำเนิด (0,0)=กลางเท้า สูง ~330. ส่วนหมุน: .armB .armF .legB .legF .head .torso (ใช้กับ walkChar/idleChar)
  function poSide() {
    const arm = (cls, c) => `<g class="${cls}" transform="translate(0 -232)">
        <rect x="-9" y="-6" width="18" height="68" rx="9" fill="${c}"/>
        <g class="${cls}-fore" transform="translate(0 58)"><rect x="-8" y="-4" width="16" height="60" rx="8" fill="${P.skin}"/>${joint(0, 0, 8, c)}<circle cx="0" cy="60" r="10" fill="${P.skin}"/></g>
        ${joint(0, 0, 9, c)}</g>`;
    const leg = (cls, c) => `<g class="${cls}" transform="translate(0 -118)">
        <rect x="-11" y="-6" width="22" height="66" rx="10" fill="${c}"/>
        <g class="${cls}-shin" transform="translate(0 58)"><rect x="-10" y="-4" width="20" height="56" rx="9" fill="${c}"/>${joint(0, 0, 9, c)}<path d="M-12 48 h30 a8 8 0 0 1 8 8 v4 h-42z" fill="${P.shoe}"/></g>
        ${joint(0, 0, 10, c)}</g>`;
    return `<g class="char po">
      <ellipse cx="6" cy="2" rx="44" ry="9" fill="#000" opacity=".22"/>
      ${leg('legB', P.pants)}
      ${arm('armB', P.blouseD)}
      <g class="torso">
        <path d="M-28 -232 h56 a10 10 0 0 1 10 10 v94 a12 12 0 0 1 -12 12 h-52 a12 12 0 0 1 -12 -12 v-94 a10 10 0 0 1 10 -10z" fill="${P.blouse}"/>
        <path d="M-6 -232 v100" stroke="${P.blouseD}" stroke-width="2"/>
        <path d="M-2 -232 l-14 22 l12 10 l12 -10z" fill="${P.blouseD}"/>
        <rect x="-38" y="-130" width="76" height="16" rx="6" fill="${P.pants}"/>
        <rect x="-30" y="-238" width="52" height="10" rx="5" fill="${P.blouseD}"/>
        <!-- บัตรพนักงาน -->
        <path d="M14 -230 v24" stroke="#2b7bc0" stroke-width="3"/><rect x="6" y="-206" width="18" height="24" rx="3" fill="#fff" stroke="#2b7bc0" stroke-width="2"/>
      </g>
      ${leg('legF', P.pants)}
      <g class="head" transform="translate(4 -246)">
        <circle cx="0" cy="-2" r="12" fill="${P.skin}"/>
        <g transform="translate(0 -30)">
          <!-- ผมหางม้า -->
          <path class="ponytail" d="M-30 -10 q-30 10 -34 60 q10 -6 18 -4 q-2 -30 16 -46z" fill="${P.hair}"/>
          <rect x="-34" y="-30" width="72" height="66" rx="24" fill="${P.skin}"/>
          <path d="M-34 -8 q0 -34 36 -34 q38 0 38 30 q-8 -22 -40 -20 q-26 0 -34 24z" fill="${P.hair}"/>
          <path d="M26 -16 q14 10 10 30 q-2 -16 -10 -24z" fill="${P.hair}"/>
          <circle cx="-34" cy="-14" r="7" fill="${P.hair}"/>
          <circle cx="18" cy="2" r="4" fill="${P.hair}"/><circle cx="19.5" cy="0.5" r="1.3" fill="#fff"/>
          <path d="M8 -8 q10 -4 18 0" stroke="${P.hair}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <path d="M18 18 q6 3 12 -1" stroke="${P.skinD}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <circle cx="12" cy="12" r="5" fill="#f2a6a0" opacity=".5"/>
          <ellipse cx="38" cy="10" rx="5" ry="7" fill="${P.skinD}"/>
        </g>
      </g>
      ${arm('armF', P.blouse)}
    </g>`;
  }
  // ---------- แมวส้ม "ส้ม" (ด้านข้าง หันขวา) ส่วนขยับ: .cat-head .cat-tail .cat-earF .cat-earB .cat-mouth ----------
  function catSide({ sit = true } = {}) {
    const stripes = `<path d="M-30 -56 q4 -8 6 -16 M-16 -60 q4 -8 6 -16 M-2 -60 q4 -8 6 -16" stroke="${P.catD}" stroke-width="5" stroke-linecap="round" fill="none" opacity=".8"/>`;
    const body = sit
      ? `<path d="M-40 0 q-6 -70 30 -72 h20 q24 0 26 40 v26 q0 6 -6 6 h-64 q-6 0 -6 -6z" fill="${P.cat}"/><rect x="-6" y="-26" width="14" height="28" rx="6" fill="${P.cat}"/><rect x="22" y="-26" width="14" height="28" rx="6" fill="${P.catL}"/><path d="M-10 -4 h26 a6 6 0 0 1 0 8 h-26z" fill="${P.catL}" opacity=".6"/>`
      : `<path d="M-44 -22 q0 -40 36 -40 h30 q26 0 26 32 v8 q0 8 -8 8 h-76 q-8 0 -8 -8z" fill="${P.cat}"/><g class="legs"><rect class="cl1" x="-38" y="-24" width="11" height="24" rx="5" fill="${P.catD}"/><rect class="cl2" x="28" y="-24" width="11" height="24" rx="5" fill="${P.catD}"/><rect class="cl3" x="-28" y="-24" width="11" height="24" rx="5" fill="${P.cat}"/><rect class="cl4" x="38" y="-24" width="11" height="24" rx="5" fill="${P.cat}"/></g>`;
    return `<g class="cat">
      <ellipse cx="6" cy="2" rx="52" ry="7" fill="#000" opacity=".22"/>
      <g class="cat-tail" transform="translate(-40 ${sit ? -14 : -40})"><path d="M0 0 q-40 -4 -44 -54" stroke="${P.cat}" stroke-width="11" stroke-linecap="round" fill="none"/><path d="M-40 -46 q-2 -6 -4 -10" stroke="${P.catD}" stroke-width="9" stroke-linecap="round" fill="none"/></g>
      ${body}${stripes}
      <g class="cat-head" transform="translate(40 ${sit ? -84 : -58})">
        <g class="cat-earB" transform="translate(-16 -22)"><path d="M0 4 l-4 -32 l24 20z" fill="${P.catD}"/></g>
        <g class="cat-earF" transform="translate(12 -24)"><path d="M0 4 l4 -32 l-24 22z" fill="${P.cat}"/><path d="M-2 2 l3 -20 l-14 14z" fill="#f2a6a0" opacity=".8"/></g>
        <ellipse rx="32" ry="26" fill="${P.cat}"/>
        <path d="M-10 -24 q2 -8 4 -14 M4 -24 q0 -8 2 -14" stroke="${P.catD}" stroke-width="4" stroke-linecap="round"/>
        <ellipse cx="14" cy="8" rx="16" ry="12" fill="${P.catL}"/>
        <circle cx="-4" cy="-4" r="5" fill="#2d6b2d"/><ellipse cx="-4" cy="-4" rx="2" ry="4.5" fill="#111"/>
        <circle cx="18" cy="-6" r="5" fill="#2d6b2d"/><ellipse cx="18" cy="-6" rx="2" ry="4.5" fill="#111"/>
        <path d="M22 6 h6 l-3 3z" fill="${P.nose}"/>
        <g class="cat-mouth" transform="translate(25 10)"><path d="M0 0 q-4 5 -8 2 M0 0 q4 5 8 2" stroke="${P.catD}" stroke-width="2" fill="none" stroke-linecap="round"/></g>
        <path d="M28 4 l16 -4 M28 8 l17 2 M28 12 l15 6" stroke="#fff" stroke-width="1.5" stroke-linecap="round" opacity=".8"/>
      </g>
    </g>`;
  }
  // หน้าแมวใกล้ ๆ (ช็อตปิด) ส่วนขยับ: .earL .earR .eyeL .eyeR .pupilL .pupilR
  function catFace() {
    return `<g class="catface">
      <g class="earL" transform="translate(-110 -120)"><path d="M0 40 l-26 -120 l86 70z" fill="${P.catD}"/><path d="M6 30 l-16 -84 l56 48z" fill="#f2a6a0" opacity=".7"/></g>
      <g class="earR" transform="translate(110 -120)"><path d="M0 40 l26 -120 l-86 70z" fill="${P.cat}"/><path d="M-6 30 l16 -84 l-56 48z" fill="#f2a6a0" opacity=".7"/></g>
      <path d="M-150 -60 q0 -100 150 -100 q150 0 150 100 v90 q0 90 -90 90 h-120 q-90 0 -90 -90z" fill="${P.cat}"/>
      <path d="M-40 -150 q6 -30 10 -50 M0 -156 q0 -30 2 -50 M40 -150 q-6 -30 -10 -50" stroke="${P.catD}" stroke-width="12" stroke-linecap="round"/>
      <path d="M-120 -20 q20 -16 40 0 M80 -20 q20 -16 40 0" stroke="${P.catD}" stroke-width="10" stroke-linecap="round" fill="none" opacity=".8"/>
      <ellipse cx="0" cy="50" rx="80" ry="60" fill="${P.catL}"/>
      <g class="eyeL" transform="translate(-62 -30)"><ellipse rx="26" ry="28" fill="#4caf50"/><ellipse class="pupilL" rx="8" ry="22" fill="#111"/><circle cx="-10" cy="-12" r="6" fill="#fff"/></g>
      <g class="eyeR" transform="translate(62 -30)"><ellipse rx="26" ry="28" fill="#4caf50"/><ellipse class="pupilR" rx="8" ry="22" fill="#111"/><circle cx="-10" cy="-12" r="6" fill="#fff"/></g>
      <path d="M-14 36 h28 l-14 14z" fill="${P.nose}"/>
      <path d="M0 50 v14 M-30 70 q30 20 60 0" stroke="${P.catD}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M-70 60 l-90 -14 M-70 72 l-92 4 M-70 84 l-88 20 M70 60 l90 -14 M70 72 l92 4 M70 84 l88 20" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".85"/>
    </g>`;
  }
  // ---------- ซอมบี้เงา + คนเงา ----------
  function zombie(c = '#101017') {
    return `<g class="zombie"><rect x="-14" y="-130" width="12" height="70" rx="5" fill="${c}"/><rect x="2" y="-130" width="12" height="70" rx="5" fill="${c}"/><path d="M-24 -230 h48 q6 0 6 6 v96 h-60 v-96 q0 -6 6 -6z" fill="${c}"/><g class="zhead" transform="translate(6 -236)"><rect x="-26" y="-50" width="52" height="56" rx="20" fill="${c}"/></g><g class="zarm" transform="translate(18 -214)"><rect x="-8" y="-6" width="80" height="14" rx="7" fill="${c}"/></g><g class="zarm2" transform="translate(-16 -210)"><rect x="-8" y="-6" width="70" height="14" rx="7" fill="${c}"/></g></g>`;
  }
  function personFront(c = '#3a3f4a') {
    return `<g class="person"><rect x="-18" y="-130" width="14" height="60" rx="6" fill="${c}"/><rect x="4" y="-130" width="14" height="60" rx="6" fill="${c}"/><rect x="-30" y="-230" width="60" height="110" rx="14" fill="${c}"/><rect x="-24" y="-270" width="48" height="50" rx="18" fill="${c}"/></g>`;
  }

  // ---------- เมือง: เส้นขอบฟ้ากรุงเทพ ----------
  function skyline(night = false, seed = 1) {
    let s = '';
    const n = 26;
    for (let i = 0; i < n; i++) {
      const h = 120 + ((i * 97 + seed * 31) % 260), w = 46 + ((i * 53) % 50), x = -420 + i * 60;
      const c = night ? ['#141a2e', '#1a2240', '#10152a'][i % 3] : ['#5b5577', '#6d6489', '#4f4a6a'][i % 3];
      s += `<rect x="${x}" y="${-h}" width="${w}" height="${h + 40}" fill="${c}"/>`;
      for (let r = 0; r < Math.floor(h / 26); r++) for (let k = 0; k < Math.floor(w / 16); k++) {
        const lit = ((i * 7 + r * 13 + k * 5) % 7) < (night ? 3 : 2);
        s += `<rect class="win" x="${x + 5 + k * 16}" y="${-h + 8 + r * 26}" width="8" height="12" fill="${lit ? (night ? '#ffd27a' : '#ffe9b0') : (night ? '#0b0f1c' : '#3a3650')}" opacity="${lit ? .9 : .6}"/>`;
      }
    }
    return `<g class="skyline">${s}</g>`;
  }
  function smokeColumns(n = 4) {
    return `<g class="smoke">${Array.from({ length: n }, (_, i) => `<g class="smk" transform="translate(${-200 + i * 300} 0)">${[0, 1, 2, 3, 4].map(j => `<circle class="sp" cx="${j * 6}" cy="${-j * 40}" r="${16 + j * 10}" fill="#2a2a33" opacity="${.55 - j * .08}"/>`).join('')}</g>`).join('')}</g>`;
  }
  // ---------- คอนโด: ระเบียง / โถงลิฟต์ / ทางเดิน ----------
  function balconyRail(w = 900) {
    return `<g class="rail"><rect x="${-w / 2}" y="-8" width="${w}" height="16" rx="6" fill="#2a2f36"/>${Array.from({ length: Math.floor(w / 36) }, (_, i) => `<rect x="${-w / 2 + 10 + i * 36}" y="0" width="6" height="140" fill="#2a2f36"/>`).join('')}<rect x="${-w / 2}" y="136" width="${w}" height="40" fill="#3a3f48"/><rect x="${-w / 2}" y="176" width="${w}" height="200" fill="#8f7b63"/></g>`;
  }
  function elevatorDoors(open = 0) { // open 0..1
    return `<g class="elev">
      <rect x="-150" y="-330" width="300" height="340" rx="6" fill="${P.steelD}"/>
      <rect x="-140" y="-320" width="280" height="320" fill="#0d0f14"/>
      <g class="shaft" opacity="0"><rect x="-140" y="-320" width="280" height="320" fill="#1c222c"/></g>
      <rect class="doorL" x="${-140 - open * 130}" y="-320" width="140" height="320" fill="${P.steel}"/>
      <rect class="doorR" x="${0 + open * 130}" y="-320" width="140" height="320" fill="${P.steel}"/>
      <rect class="doorL2" x="${-140 - open * 130}" y="-320" width="140" height="320" fill="url(#steelShine)" opacity=".5"/>
      <rect class="doorR2" x="${0 + open * 130}" y="-320" width="140" height="320" fill="url(#steelShine)" opacity=".5"/>
      <rect x="-60" y="-380" width="120" height="40" rx="6" fill="#0d0f14"/>
      <text class="floorno" x="0" y="-350" font-family="Kanit" font-weight="700" font-size="28" fill="#ff4d3d" text-anchor="middle">23</text>
      <g class="arrow" transform="translate(42 -360)" opacity="0"><path d="M0 8 v-16 M-6 -2 l6 -6 l6 6" stroke="#ff4d3d" stroke-width="3" fill="none" stroke-linecap="round"/></g>
    </g>`;
  }
  function callPanel() {
    return `<g class="callpanel"><rect x="-40" y="-90" width="80" height="180" rx="10" fill="${P.steel}"/><rect x="-32" y="-82" width="64" height="164" rx="8" fill="#c9cfd5"/>
      <circle class="btnUp" cx="0" cy="-40" r="22" fill="#e8eef2" stroke="#6b7177" stroke-width="3"/><path d="M0 -30 v-20 M-8 -42 l8 -8 l8 8" stroke="#2a2f36" stroke-width="4" fill="none" stroke-linecap="round"/>
      <circle class="btnDn" cx="0" cy="40" r="22" fill="#e8eef2" stroke="#6b7177" stroke-width="3"/><path d="M0 30 v20 M-8 42 l8 8 l8 -8" stroke="#2a2f36" stroke-width="4" fill="none" stroke-linecap="round"/></g>`;
  }
  function corridor() {
    return `<g class="corridor">
      <rect x="-400" y="-100" width="1520" height="1700" fill="${P.wall}"/>
      <path d="M-400 1000 L1120 1000 L1120 1500 L-400 1500z" fill="${P.floor}"/>
      <path d="M-400 1000 h1520 v10 h-1520z" fill="${P.floorD}"/>
      ${[0, 1, 2, 3].map(i => `<g transform="translate(${-120 + i * 330} 1000)"><rect x="-70" y="-300" width="140" height="300" fill="#6b5b48"/><rect x="-62" y="-292" width="124" height="292" fill="#8c7558"/><rect x="-34" y="-330" width="68" height="24" rx="4" fill="#2a2f36"/><text y="-312" font-family="Kanit" font-weight="600" font-size="16" fill="#f6efe0" text-anchor="middle">23${['01', '02', '03', '04'][i]}</text><circle cx="44" cy="-150" r="5" fill="#d9d2c0"/></g>`).join('')}
      ${[0, 1, 2].map(i => `<g class="clight" transform="translate(${-60 + i * 400} 420)"><rect x="-60" y="-8" width="120" height="14" rx="4" fill="#fff6d0"/><ellipse class="cone" rx="170" ry="300" cy="300" fill="url(#lightCone)"/></g>`).join('')}
      <g class="emlight" transform="translate(300 470)" opacity="0"><rect x="-30" y="-14" width="60" height="28" rx="4" fill="#2a2f36"/><circle cx="-12" r="6" fill="#ff5a4a" class="em1"/><circle cx="12" r="6" fill="#ff5a4a" class="em2"/></g>
    </g>`;
  }
  // ---------- ภาพตัดตึก 23 ชั้น + แท็งก์ดาดฟ้า + ปั๊มใต้ดิน ----------
  function towerSection({ floors = 23, fw = 360, fh = 34, x = 0, y = 0 } = {}) {
    let f = '';
    for (let i = 0; i < floors; i++) {
      const yy = y - (i + 1) * fh; const hi = i === floors - 1;
      f += `<g class="fl fl${i + 1}" transform="translate(${x} ${yy})"><rect x="${-fw / 2}" y="0" width="${fw}" height="${fh}" fill="${hi ? '#f5c542' : (i % 2 ? '#c9cfd5' : '#d9dee3')}" stroke="#2a2f36" stroke-width="1.5"/>
        ${[0, 1, 2, 3, 4, 5].map(k => `<rect class="win" x="${-fw / 2 + 14 + k * (fw - 20) / 6}" y="8" width="${(fw - 20) / 6 - 12}" height="${fh - 16}" fill="#9ad2e6" opacity=".8"/>`).join('')}
        <text x="${-fw / 2 - 12}" y="${fh - 10}" font-family="Kanit" font-size="14" fill="#f6efe0" text-anchor="end" opacity=".8">${i + 1}</text></g>`;
    }
    return `<g class="tower">
      <rect x="${x - fw / 2 - 10}" y="${y - floors * fh - 70}" width="${fw + 20}" height="${floors * fh + 70}" fill="#2a2f36"/>
      ${f}
      <!-- ดาดฟ้า + แท็งก์ -->
      <g class="roof" transform="translate(${x} ${y - floors * fh - 70})"><rect x="${-fw / 2 - 10}" y="0" width="${fw + 20}" height="8" fill="#555c66"/>
        <g class="rooftank" transform="translate(0 6)"><rect x="-90" y="0" width="180" height="60" rx="10" fill="${P.steel}" stroke="#2a2f36" stroke-width="3"/><clipPath id="rtclip"><rect x="-86" y="4" width="172" height="52" rx="8"/></clipPath><rect class="tanklvl" x="-90" y="20" width="180" height="40" fill="${P.water}" clip-path="url(#rtclip)"/><rect x="-90" y="0" width="180" height="60" rx="10" fill="none" stroke="#2a2f36" stroke-width="3"/><text class="tanktxt" y="40" font-family="Kanit" font-weight="700" font-size="18" fill="#0d2a3a" text-anchor="middle">40,000 ล.</text></g></g>
      <!-- ชั้นใต้ดิน: ปั๊ม -->
      <g class="basement" transform="translate(${x} ${y})"><rect x="${-fw / 2 - 10}" y="0" width="${fw + 20}" height="70" fill="#1c1f26"/>
        <g class="pump" transform="translate(-100 36)"><rect x="-30" y="-22" width="60" height="44" rx="8" fill="#2b2f38" stroke="#555" stroke-width="2"/><circle class="pumpwheel" r="12" fill="none" stroke="#9aa1a8" stroke-width="4" stroke-dasharray="6 6"/><circle class="pled" cx="22" cy="-14" r="4" fill="#2bd46b"/></g>
        <text x="0" y="44" font-family="Kanit" font-size="14" fill="#9aa1a8" text-anchor="middle">ปั๊มน้ำ ชั้นใต้ดิน</text>
        <g class="lobbymark" transform="translate(0 -17)" opacity="0"><rect x="-60" y="-14" width="120" height="28" rx="14" fill="${P.red}"/><text y="6" font-family="Kanit" font-weight="600" font-size="16" fill="#fff" text-anchor="middle">ล็อบบี้</text></g>
      </g>
      <!-- ท่อน้ำขึ้นแท็งก์ -->
      <rect class="riser" x="${x + fw / 2 - 22}" y="${y - floors * fh - 10}" width="12" height="${floors * fh + 40}" fill="#4a6b85"/>
      <g class="flow">${Array.from({ length: 24 }, (_, i) => `<rect class="fd" x="${x + fw / 2 - 20}" y="${y - i * 34}" width="8" height="12" rx="3" fill="${P.water}"/>`).join('')}</g>
    </g>`;
  }
  // ---------- ห้องน้ำ: อ่าง ถัง ขวด ----------
  function bathroom() {
    const bottle = (x, y, s = 1) => `<g class="bt" transform="translate(${x} ${y}) scale(${s})"><rect x="-16" y="-70" width="32" height="70" rx="6" fill="#d9f1fb" stroke="#1f3b4d" stroke-width="3"/><rect x="-8" y="-84" width="16" height="14" rx="3" fill="#2b7bc0"/><rect class="lvl" x="-14" y="-2" width="28" height="0" fill="${P.water}"/></g>`;
    return `<g class="bathroom">
      <rect x="-400" y="-100" width="1520" height="1700" fill="#dfe8ec"/>
      ${Array.from({ length: 12 }, (_, i) => `<rect x="-400" y="${-100 + i * 120}" width="1520" height="2" fill="#b9c7cf"/>`).join('')}${Array.from({ length: 14 }, (_, i) => `<rect x="${-400 + i * 120}" y="-100" width="2" height="1700" fill="#b9c7cf"/>`).join('')}
      <rect x="-400" y="900" width="1520" height="700" fill="#b3bfc6"/>
      <!-- อ่างอาบน้ำ -->
      <g class="tub" transform="translate(360 900)"><path d="M-300 -140 h600 a20 20 0 0 1 20 20 v120 h-640 v-120 a20 20 0 0 1 20 -20z" fill="#f3f6f7" stroke="#8a9aa3" stroke-width="4"/><clipPath id="tubclip"><rect x="-290" y="-130" width="580" height="124"/></clipPath><rect class="tublvl" x="-300" y="0" width="600" height="130" fill="${P.water}" clip-path="url(#tubclip)" opacity=".9"/><path class="tubwave" d="M-290 -20 q40 -8 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" stroke="#fff" stroke-width="4" fill="none" opacity="0"/>
        <g class="tap" transform="translate(220 -180)"><rect x="-8" y="0" width="16" height="50" fill="${P.steel}"/><path d="M-8 10 h-60 a10 10 0 0 0 -10 10 v10" stroke="${P.steel}" stroke-width="14" fill="none" stroke-linecap="round"/><rect class="stream" x="-84" y="30" width="10" height="0" fill="${P.water}" opacity=".9"/></g></g>
      <!-- ถัง -->
      ${[0, 1, 2].map(i => `<g class="bucket" transform="translate(${90 + i * 140} 1180)"><path d="M-54 -130 h108 l-10 130 h-88z" fill="#2b7bc0" stroke="#163c5e" stroke-width="4"/><clipPath id="bk${i}"><path d="M-50 -126 h100 l-9 122 h-82z"/></clipPath><rect class="lvl" x="-60" y="0" width="120" height="0" fill="${P.water}" clip-path="url(#bk${i})"/><ellipse cx="0" cy="-130" rx="54" ry="10" fill="#1f5f90"/></g>`).join('')}
      <!-- ขวด -->
      <g class="bottles">${[0, 1, 2, 3, 4, 5].map(i => bottle(480 + (i % 3) * 60, 1130 + Math.floor(i / 3) * 90, 1)).join('')}</g>
    </g>`;
  }
  // ---------- ก๊อกใกล้ ๆ (น้ำหยด) ----------
  function tapClose() {
    return `<g class="tapclose">
      <rect x="-400" y="-100" width="1520" height="1700" fill="#dfe8ec"/>
      ${Array.from({ length: 12 }, (_, i) => `<rect x="-400" y="${-100 + i * 150}" width="1520" height="3" fill="#b9c7cf"/>`).join('')}
      <path d="M-400 900 h1520 v700 h-1520z" fill="#f3f6f7"/><path d="M-400 900 h1520 v10 h-1520z" fill="#b3bfc6"/>
      <g transform="translate(360 520)"><rect x="-30" y="-200" width="60" height="200" fill="${P.steel}"/><rect x="-30" y="-200" width="20" height="200" fill="#c9cfd5"/><path d="M-30 -120 h-220 a40 40 0 0 0 -40 40 v60" stroke="${P.steel}" stroke-width="48" fill="none" stroke-linecap="round"/><path d="M-30 -120 h-220 a40 40 0 0 0 -40 40 v60" stroke="#c9cfd5" stroke-width="14" fill="none" stroke-linecap="round" transform="translate(-12 -12)"/><rect x="-40" y="-240" width="80" height="40" rx="8" fill="#2a2f36"/>
        <rect class="stream" x="-300" y="-10" width="24" height="0" fill="${P.water}" opacity=".85"/>
        <g class="drops">${[0, 1, 2].map(i => `<ellipse class="drop" cx="-288" cy="0" rx="8" ry="12" fill="${P.water}" opacity="0"/>`).join('')}</g>
      </g>
      <g class="gauge" transform="translate(560 300)"><circle r="90" fill="#f6efe0" stroke="#2a2f36" stroke-width="6"/><path d="M-62 40 a74 74 0 0 1 124 0" stroke="#2a2f36" stroke-width="6" fill="none"/><path d="M-62 40 a74 74 0 0 1 20 -58" stroke="#d7342c" stroke-width="12" fill="none"/><path d="M42 -18 a74 74 0 0 1 20 58" stroke="#2f9e5a" stroke-width="12" fill="none"/><g class="needle"><path d="M0 0 l-6 10 l-60 -4 l60 -16z" fill="#d7342c"/></g><circle r="10" fill="#2a2f36"/><text y="70" font-family="Kanit" font-weight="600" font-size="18" fill="#2a2622" text-anchor="middle">แรงดันน้ำ</text></g>
    </g>`;
  }
  // ---------- ประตูหนีไฟ + ตู้เหล็ก ----------
  function fireDoorScene() {
    return `<g class="firedoor">
      ${corridor()}
      <g transform="translate(560 1000)"><rect x="-120" y="-380" width="240" height="380" fill="#4a0c08"/><rect x="-110" y="-370" width="220" height="370" fill="${P.red}"/><rect x="-80" y="-340" width="160" height="110" rx="6" fill="#f0a39e" opacity=".9"/><rect x="-60" y="-420" width="120" height="34" rx="6" fill="#2f9e5a"/><text y="-396" font-family="Kanit" font-weight="700" font-size="20" fill="#fff" text-anchor="middle">ทางหนีไฟ</text><rect x="-100" y="-190" width="200" height="16" rx="8" fill="#c9cfd5"/><text class="doortxt" y="-100" font-family="Kanit" font-weight="600" font-size="16" fill="#fff" text-anchor="middle" opacity=".9">เปิดจากฝั่งบันไดไม่ได้</text></g>
      <g class="cabinet" transform="translate(-200 1000)"><rect x="-90" y="-300" width="180" height="300" rx="6" fill="${P.steel}" stroke="#2a2f36" stroke-width="4"/><rect x="-80" y="-290" width="80" height="280" fill="#c9cfd5"/><rect x="0" y="-290" width="80" height="280" fill="#b4bbc2"/><rect x="-14" y="-160" width="8" height="40" rx="3" fill="#2a2f36"/><rect x="6" y="-160" width="8" height="40" rx="3" fill="#2a2f36"/><g class="scrape">${[0, 1, 2].map(i => `<path d="M${-60 + i * 50} 4 l-20 0" stroke="#5a4a3a" stroke-width="3" opacity="0" class="sc"/>`).join('')}</g></g>
    </g>`;
  }
  // ---------- สมุดจด ----------
  function notebook(lines) {
    return `<g class="notebook">
      <rect x="-400" y="-100" width="1520" height="1700" fill="#3b2f2a"/>
      <g opacity=".5">${Array.from({ length: 12 }, (_, i) => `<rect x="-400" y="${-100 + i * 150}" width="1520" height="4" fill="#2a1f1a"/>`).join('')}</g>
      <ellipse class="torch" cx="360" cy="700" rx="520" ry="620" fill="url(#glow)" opacity=".5"/>
      <g transform="translate(360 760) rotate(-4)">
        <rect x="-300" y="-400" width="600" height="800" rx="8" fill="#000" opacity=".35" filter="url(#blur10)"/>
        <rect x="-290" y="-400" width="580" height="800" rx="6" fill="url(#paper)"/>
        <line x1="-210" y1="-400" x2="-210" y2="400" stroke="#e8b4a8" stroke-width="2"/>
        ${Array.from({ length: 16 }, (_, i) => `<line x1="-290" y1="${-340 + i * 48}" x2="290" y2="${-340 + i * 48}" stroke="#cfd8e6" stroke-width="1.5"/>`).join('')}
        <g class="ink" font-family="Sarabun" font-weight="700" font-size="30" fill="#2a3a6b">${lines.map((l, i) => `<text class="l${i}" x="-190" y="${-352 + i * 96}">${l}</text>`).join('')}</g>
        <g class="pen"><rect x="-10" y="-200" width="20" height="230" rx="6" fill="#1b1f27" transform="rotate(35)"/><path d="M0 30 l-8 -8 h16z" fill="#d8d3c4" transform="rotate(35)"/></g>
      </g>
      <g transform="translate(120 1180) rotate(-30)"><rect x="-90" y="-22" width="180" height="44" rx="10" fill="#1b1f27"/><rect x="60" y="-26" width="40" height="52" rx="8" fill="#2b2f3a"/><circle cx="100" cy="0" r="22" fill="#fff6d0" filter="url(#softglow)"/></g>
    </g>`;
  }
  function dust(n = 24, cls = 'dust') { return `<g class="${cls}">${Array.from({ length: n }, (_, i) => `<circle class="p" r="${1.5 + (i % 3)}" fill="#fff4d6" opacity=".5"/>`).join('')}</g>`; }
  function defs() {
    return `<defs>
      <linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3a6e"/><stop offset=".5" stop-color="#c96b6b"/><stop offset=".85" stop-color="#f1a85e"/><stop offset="1" stop-color="#f9d59a"/></linearGradient>
      <linearGradient id="skyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070f"/><stop offset=".7" stop-color="#121a33"/><stop offset="1" stop-color="#2a2740"/></linearGradient>
      <radialGradient id="lightCone" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#fff3c4" stop-opacity=".5"/><stop offset="1" stop-color="#fff3c4" stop-opacity="0"/></radialGradient>
      <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6d0" stop-opacity=".9"/><stop offset=".4" stop-color="#ffd27a" stop-opacity=".35"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
      <radialGradient id="redglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff5a4a" stop-opacity=".9"/><stop offset=".5" stop-color="#d7342c" stop-opacity=".35"/><stop offset="1" stop-color="#d7342c" stop-opacity="0"/></radialGradient>
      <radialGradient id="blueglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9fe3ff" stop-opacity=".9"/><stop offset=".5" stop-color="#5fc1e6" stop-opacity=".3"/><stop offset="1" stop-color="#5fc1e6" stop-opacity="0"/></radialGradient>
      <linearGradient id="steelShine" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient>
      <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf6ea"/><stop offset="1" stop-color="#eee5d2"/></linearGradient>
      <filter id="blur3"><feGaussianBlur stdDeviation="3"/></filter><filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter><filter id="blur10"><feGaussianBlur stdDeviation="10"/></filter>
      <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <clipPath id="clipFrame"><rect x="0" y="0" width="720" height="1280"/></clipPath>
    </defs>`;
  }
  return { P, ICONS, icon, poSide, catSide, catFace, zombie, personFront, skyline, smokeColumns, balconyRail, elevatorDoors, callPanel, corridor, towerSection, bathroom, tapClose, fireDoorScene, notebook, dust, defs };
})();
