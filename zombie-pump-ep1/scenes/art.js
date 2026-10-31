/* ============================================================
   ART — ไลบรารีวาดภาพ SVG สไตล์เวกเตอร์แฟลต โทนอุ่น (ตามตัวอย่างช่อง)
   ทุกฟังก์ชันคืนค่าเป็นสตริง SVG; ส่วนที่ขยับได้ติด class ไว้ให้ shots.js ควบคุม
   ============================================================ */
window.ART = (() => {
  const P = { // palette
    skin: '#e9b78c', skinD: '#c98f66', hair: '#2a1d16', cap: '#2e9b5a', capD: '#237a46',
    jacket: '#30a05d', jacketD: '#227a45', stripe: '#f4f1e8', pants: '#2b2b33', shoe: '#f2efe6', shoeD: '#b9b3a4',
    dog: '#c67a3c', dogD: '#9a5a26', dogL: '#e2a66a', nose: '#2a1d16',
    asphalt: '#43434c', asphaltD: '#35353d', concrete: '#cfc6b6', concreteD: '#b3a893', line: '#efe5c8',
    white: '#f5f2ea', orange: '#f28b2b', orangeD: '#c86a16', blue: '#1f6fb2', red: '#d7342c', yellow: '#f5c542',
    glass: '#9ad2e6', metal: '#8d939c', metalD: '#5c6169', dark: '#15161c', cream: '#f6efe0', green: '#5c8a4a',
  };
  const joint = (x, y, r = 7, c = P.skin) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;

  // ---------- ตัวละครหลัก "ต้น" ไรเดอร์ส่งอาหาร (ด้านข้าง หันขวา) ----------
  // จุดกำเนิด (0,0) = กลางเท้า, สูง ~ 330 หน่วย. ส่วนที่หมุนได้: .armB .armF .legB .legF .head (หมุนรอบข้อต่อ)
  function tonSide({ helmet = false } = {}) {
    const arm = (cls, c, cd) => `<g class="${cls}" transform="translate(0 -232)">
        <rect x="-9" y="-6" width="18" height="70" rx="9" fill="${c}"/>
        <g class="${cls}-fore" transform="translate(0 60)">
          <rect x="-8" y="-4" width="16" height="62" rx="8" fill="${cd}"/>
          ${joint(0, 0, 8, c)}
          <circle cx="0" cy="62" r="10" fill="${P.skin}"/>
        </g>
        ${joint(0, 0, 9, c)}
      </g>`;
    const leg = (cls, c) => `<g class="${cls}" transform="translate(0 -118)">
        <rect x="-11" y="-6" width="22" height="66" rx="10" fill="${c}"/>
        <g class="${cls}-shin" transform="translate(0 58)">
          <rect x="-10" y="-4" width="20" height="56" rx="9" fill="${P.pants}"/>
          ${joint(0, 0, 9, c)}
          <path d="M-12 46 h30 a10 10 0 0 1 10 10 v4 h-44 z" fill="${P.shoe}"/>
          <path d="M-12 56 h40 v4 h-40z" fill="${P.shoeD}"/>
        </g>
        ${joint(0, 0, 10, c)}
      </g>`;
    const headTop = helmet
      ? `<path d="M-40 -2 a40 40 0 0 1 80 0 v8 h-80z" fill="${P.cap}"/><path d="M-40 6 h80 v10 a6 6 0 0 1 -6 6 h-68 a6 6 0 0 1 -6 -6z" fill="${P.capD}"/><rect x="-6" y="8" width="52" height="30" rx="6" fill="#1b2430" opacity=".85"/>`
      : `<path d="M-38 -4 a38 34 0 0 1 76 0 v8 h-76z" fill="${P.cap}"/><path d="M-38 4 h92 a6 6 0 0 1 0 12 h-92z" fill="${P.capD}"/>`;
    return `<g class="ton">
      <ellipse cx="6" cy="2" rx="46" ry="9" fill="#000" opacity=".22"/>
      ${leg('legB', P.pants)}
      ${arm('armB', P.jacketD, P.jacketD)}
      <!-- ลำตัว -->
      <g class="torso">
        <path d="M-30 -232 h60 a10 10 0 0 1 10 10 v96 a12 12 0 0 1 -12 12 h-56 a12 12 0 0 1 -12 -12 v-96 a10 10 0 0 1 10 -10z" fill="${P.jacket}"/>
        <path d="M-40 -170 h80 v12 h-80z" fill="${P.stripe}" opacity=".9"/>
        <path d="M-40 -150 h80 v6 h-80z" fill="${P.stripe}" opacity=".5"/>
        <!-- สายกระเป๋า -->
        <path d="M-28 -228 L34 -140" stroke="${P.dark}" stroke-width="7" stroke-linecap="round" opacity=".8"/>
        <rect x="-26" y="-236" width="52" height="10" rx="5" fill="${P.jacketD}"/>
      </g>
      ${leg('legF', P.pants)}
      <!-- หัว -->
      <g class="head" transform="translate(4 -246)">
        <circle cx="0" cy="-2" r="12" fill="${P.skin}"/>
        <g transform="translate(0 -30)">
          <rect x="-34" y="-30" width="72" height="66" rx="24" fill="${P.skin}"/>
          <path d="M-34 -10 q0 -32 36 -32 q36 0 36 30 v-2 q-8 -18 -36 -18 q-28 0 -36 20z" fill="${P.hair}"/>
          ${headTop}
          <circle cx="18" cy="2" r="4" fill="${P.hair}"/>
          <path d="M8 -6 q10 -4 18 0" stroke="${P.hair}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <path d="M20 18 q6 2 10 -2" stroke="${P.skinD}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <ellipse cx="38" cy="10" rx="5" ry="7" fill="${P.skinD}"/>
        </g>
      </g>
      ${arm('armF', P.jacket, P.jacketD)}
    </g>`;
  }
  // ท่าเงา (silhouette) สำหรับช็อตไกล/กลางคืน
  function tonSilhouette() { return `<g style="filter:brightness(0.08)">${tonSide({ helmet: true })}</g>`; }

  // ---------- หมาปั๊ม (ด้านข้าง หันขวา) ----------
  // ส่วนที่ขยับ: .dog-head .dog-jaw .dog-tail .dog-earF .dog-earB .legs
  function dogSide({ sit = false } = {}) {
    const legs = sit ? `
      <path d="M-40 -8 q-2 -40 24 -42 l0 42z" fill="${P.dogD}"/>
      <rect x="-14" y="-40" width="14" height="40" rx="6" fill="${P.dog}"/>
      <rect x="30" y="-36" width="14" height="36" rx="6" fill="${P.dog}"/>
      <path d="M-44 -4 h22 v6 h-22z M26 -4 h22 v6 h-22z" fill="${P.dogD}"/>` : `
      <g class="legs">
        <rect class="dl1" x="-36" y="-56" width="13" height="56" rx="6" fill="${P.dogD}"/>
        <rect class="dl2" x="26" y="-56" width="13" height="56" rx="6" fill="${P.dogD}"/>
        <rect class="dl3" x="-26" y="-56" width="13" height="56" rx="6" fill="${P.dog}"/>
        <rect class="dl4" x="38" y="-56" width="13" height="56" rx="6" fill="${P.dog}"/>
      </g>`;
    return `<g class="dog">
      <ellipse cx="6" cy="2" rx="60" ry="8" fill="#000" opacity=".22"/>
      ${legs}
      <g class="dog-tail" transform="translate(-44 -70)">
        <path d="M0 0 q-30 -10 -24 -50" stroke="${P.dog}" stroke-width="12" stroke-linecap="round" fill="none"/>
        <path d="M-22 -44 q-2 -10 -4 -16" stroke="${P.dogL}" stroke-width="8" stroke-linecap="round" fill="none"/>
      </g>
      <path d="M-46 -${sit ? 56 : 54} q4 -44 50 -46 h22 q30 0 34 36 v${sit ? 30 : 10} q0 10 -10 10 h-86 q-10 0 -10 -10z" fill="${P.dog}"/>
      <path d="M-30 -64 q30 -14 70 -8 v8 q-40 -4 -70 6z" fill="${P.dogD}" opacity=".6"/>
      <path d="M-10 -${sit ? 30 : 44} h60 q6 0 6 6 v${sit ? 20 : 20} h-66z" fill="${P.dogL}" opacity=".8"/>
      <g class="dog-head" transform="translate(50 -92)">
        <g class="dog-earB" transform="translate(-14 -14)"><path d="M0 0 l-6 -36 l22 22z" fill="${P.dogD}"/></g>
        <g class="dog-jaw" transform="translate(8 10)"><path d="M0 0 h50 q8 0 8 8 q0 6 -8 6 h-50z" fill="${P.dogD}"/></g>
        <path d="M-22 -6 q0 -26 28 -26 h20 q22 0 26 20 l14 4 q6 2 4 8 l-18 2 q-4 12 -24 12 h-26 q-24 0 -24 -20z" fill="${P.dog}"/>
        <path d="M14 -18 q10 -2 36 6" stroke="${P.dogL}" stroke-width="6" stroke-linecap="round" fill="none" opacity=".7"/>
        <circle cx="48" cy="-4" r="5" fill="${P.nose}"/>
        <circle cx="18" cy="-10" r="4" fill="${P.hair}"/><circle cx="19.5" cy="-11.5" r="1.3" fill="#fff"/>
        <g class="dog-earF" transform="translate(4 -24)"><path d="M0 4 l-2 -34 l24 26z" fill="${P.dog}"/><path d="M2 2 l-1 -24 l16 18z" fill="${P.dogL}" opacity=".8"/></g>
      </g>
    </g>`;
  }
  // หน้าหมาใกล้ ๆ (หันหน้าเข้ากล้อง) สำหรับช็อตปิด
  function dogFace() {
    return `<g class="dogface">
      <g class="earL" transform="translate(-120 -140)"><path d="M0 40 l-30 -110 l80 60z" fill="${P.dogD}"/><path d="M4 30 l-20 -78 l54 44z" fill="${P.dogL}" opacity=".7"/></g>
      <g class="earR" transform="translate(120 -140)"><path d="M0 40 l30 -110 l-80 60z" fill="${P.dogD}"/><path d="M-4 30 l20 -78 l-54 44z" fill="${P.dogL}" opacity=".7"/></g>
      <path d="M-130 -90 q0 -80 130 -80 q130 0 130 80 v110 q0 70 -70 70 h-120 q-70 0 -70 -70z" fill="${P.dog}"/>
      <path d="M-60 -20 q60 -40 120 0 v110 q-60 30 -120 0z" fill="${P.dogL}" opacity=".85"/>
      <g class="eyeL" transform="translate(-62 -40)"><ellipse rx="16" ry="18" fill="${P.hair}"/><circle cx="-5" cy="-6" r="5" fill="#fff"/></g>
      <g class="eyeR" transform="translate(62 -40)"><ellipse rx="16" ry="18" fill="${P.hair}"/><circle cx="-5" cy="-6" r="5" fill="#fff"/></g>
      <path d="M-30 40 q30 -16 60 0 q-10 26 -30 26 q-20 0 -30 -26z" fill="${P.nose}"/>
      <path d="M0 66 v18 M-24 90 q24 14 48 0" stroke="${P.hair}" stroke-width="5" fill="none" stroke-linecap="round"/>
    </g>`;
  }

  // ---------- ซอมบี้เงาดำ (ด้านข้าง) ส่วนขยับ: .zarm .zhead ----------
  function zombie(c = '#101017') {
    return `<g class="zombie">
      <rect x="-14" y="-130" width="12" height="70" rx="5" fill="${c}"/>
      <rect x="2" y="-130" width="12" height="70" rx="5" fill="${c}"/>
      <path d="M-24 -230 h48 q6 0 6 6 v96 h-60 v-96 q0 -6 6 -6z" fill="${c}"/>
      <g class="zhead" transform="translate(6 -236)"><rect x="-26" y="-50" width="52" height="56" rx="20" fill="${c}"/></g>
      <g class="zarm" transform="translate(18 -214)"><rect x="-8" y="-6" width="80" height="14" rx="7" fill="${c}"/></g>
      <g class="zarm2" transform="translate(-16 -210)"><rect x="-8" y="-6" width="70" height="14" rx="7" fill="${c}"/></g>
    </g>`;
  }

  // ---------- ปั๊มน้ำมัน: หลังคา ตู้จ่าย ร้าน ----------
  function canopy(w = 760, lights = 5) {
    let ls = '';
    for (let i = 0; i < lights; i++) {
      const x = -w / 2 + (i + .5) * (w / lights);
      ls += `<g class="clight" transform="translate(${x} 60)"><ellipse rx="110" ry="180" fill="url(#lightCone)" class="cone"/><rect x="-22" y="-8" width="44" height="10" rx="4" fill="#fffbe6" class="bulb"/></g>`;
    }
    return `<g class="canopy">
      <g class="cols">${[-w / 2 + 110, w / 2 - 110].map(x => `<rect x="${x - 12}" y="60" width="24" height="430" fill="${P.concreteD}"/><rect x="${x - 12}" y="60" width="8" height="430" fill="${P.concrete}"/>`).join('')}</g>
      ${ls}
      <rect x="${-w / 2}" y="-10" width="${w}" height="70" rx="6" fill="${P.white}"/>
      <rect x="${-w / 2}" y="-10" width="${w}" height="22" rx="6" fill="${P.orange}"/>
      <rect x="${-w / 2}" y="48" width="${w}" height="12" fill="${P.concreteD}"/>
      <rect x="${-w / 2 + 40}" y="-50" width="140" height="40" rx="6" fill="${P.blue}"/>
      <text x="${-w / 2 + 110}" y="-21" font-family="Kanit" font-weight="700" font-size="22" fill="#fff" text-anchor="middle">ปั๊ม</text>
    </g>`;
  }
  function dispenser() {
    return `<g class="dispenser">
      <rect x="-60" y="-10" width="120" height="26" rx="6" fill="${P.concreteD}"/>
      <rect x="-40" y="-170" width="80" height="166" rx="8" fill="${P.white}"/>
      <rect x="-40" y="-170" width="80" height="30" rx="8" fill="${P.orange}"/>
      <rect x="-30" y="-130" width="60" height="38" rx="4" fill="#18202b"/>
      <text class="dispnum" x="0" y="-104" font-family="Kanit" font-weight="600" font-size="20" fill="#7cf29a" text-anchor="middle">0.00</text>
      <rect x="-30" y="-84" width="60" height="6" rx="3" fill="${P.concreteD}"/>
      <rect x="24" y="-74" width="14" height="40" rx="4" fill="${P.metalD}"/>
      <path class="hose" d="M44 -60 q30 10 30 40 v30" stroke="${P.dark}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <rect x="-24" y="-60" width="24" height="46" rx="4" fill="${P.concrete}"/>
    </g>`;
  }
  function shopFront(w = 420, h = 230) {
    return `<g class="shop">
      <rect x="${-w / 2}" y="${-h}" width="${w}" height="${h}" fill="${P.concrete}"/>
      <rect x="${-w / 2}" y="${-h - 36}" width="${w}" height="40" rx="4" fill="${P.white}"/>
      <rect x="${-w / 2 + 20}" y="${-h - 28}" width="190" height="26" rx="4" fill="${P.red}"/>
      <text x="${-w / 2 + 115}" y="${-h - 9}" font-family="Kanit" font-weight="700" font-size="19" fill="#fff" text-anchor="middle">มินิมาร์ท 24 ชม.</text>
      <g class="shopglass">
        <rect x="${-w / 2 + 14}" y="${-h + 16}" width="${w - 28}" height="${h - 30}" fill="${P.glass}" opacity=".9" class="glassfill"/>
        <g class="shelves">${[0, 1, 2].map(i => `<rect x="${-w / 2 + 30}" y="${-h + 60 + i * 46}" width="${w / 2 - 50}" height="8" fill="${P.concreteD}" opacity=".8"/>`).join('')}
          ${[0, 1, 2].map(i => [0, 1, 2, 3, 4].map(j => `<rect x="${-w / 2 + 36 + j * 30}" y="${-h + 40 + i * 46}" width="20" height="20" rx="3" fill="${['#f28b2b', '#2f9e5a', '#f5c542', '#d7342c', '#1f6fb2'][(i + j) % 5]}" opacity=".85"/>`).join('')).join('')}
        </g>
        <g class="freezers">${[0, 1, 2].map(i => `<rect x="${8 + i * 60}" y="${-h + 36}" width="52" height="${h - 60}" rx="4" fill="#e8f3f7" class="fz"/><rect x="${12 + i * 60}" y="${-h + 42}" width="44" height="${h - 72}" rx="3" fill="#9fd6ec" class="fzglass"/>`).join('')}</g>
        <rect x="${-w / 2 + 14}" y="${-h + 16}" width="${w - 28}" height="${h - 30}" fill="url(#glassShine)" opacity=".5"/>
      </g>
      <rect x="-30" y="-110" width="60" height="110" fill="${P.metalD}" opacity=".35"/>
    </g>`;
  }
  function restroomBlock() {
    return `<g class="restroom">
      <rect x="-120" y="-180" width="240" height="180" fill="#b9ad98"/>
      <rect x="-120" y="-190" width="240" height="14" fill="#8e836f"/>
      <rect x="-36" y="-150" width="72" height="150" fill="#4e5a66"/>
      <rect x="-30" y="-144" width="60" height="144" fill="#5e6b78" class="doorpanel"/>
      <rect x="-60" y="-176" width="120" height="22" rx="3" fill="${P.blue}"/>
      <text x="0" y="-160" font-family="Kanit" font-weight="600" font-size="15" fill="#fff" text-anchor="middle">ห้องน้ำ</text>
      <circle cx="18" cy="-70" r="5" fill="#d9d2c0"/>
    </g>`;
  }
  // ประตูห้องน้ำแบบใกล้ (ช็อตปิดเรื่อง)
  function doorClose() {
    return `<g class="doorclose">
      <rect x="-360" y="-900" width="720" height="1200" fill="#6f6553"/>
      <g class="wallgrain">${Array.from({ length: 14 }, (_, i) => `<rect x="-360" y="${-900 + i * 86}" width="720" height="2" fill="#000" opacity=".08"/>`).join('')}</g>
      <rect x="-200" y="-760" width="400" height="760" fill="#2f3842"/>
      <rect x="-186" y="-746" width="372" height="746" fill="#45515e" class="doorpanel"/>
      <rect x="-150" y="-700" width="300" height="250" rx="6" fill="#3b4652"/>
      <rect x="-150" y="-400" width="300" height="330" rx="6" fill="#3b4652"/>
      <rect x="-120" y="-820" width="240" height="46" rx="6" fill="${P.blue}"/>
      <text x="0" y="-786" font-family="Kanit" font-weight="600" font-size="30" fill="#fff" text-anchor="middle">ห้องน้ำ</text>
      <g class="knob" transform="translate(130 -330)"><circle r="18" fill="#c9c2b2"/><circle r="8" fill="#8f887a"/><rect x="-6" y="-60" width="12" height="30" rx="3" fill="#c9c2b2"/><rect x="-3" y="-52" width="6" height="14" rx="2" fill="#4a4740" class="lockslot"/></g>
      <rect x="-360" y="0" width="720" height="300" fill="#4a4237"/>
      <g class="gaplight" opacity="0"><ellipse cx="0" cy="4" rx="260" ry="40" fill="#ffe9a8" filter="url(#blur10)" opacity=".7"/><rect x="-186" y="-12" width="372" height="14" fill="#fff3c4" filter="url(#softglow)"/><path d="M-186 2 L-260 120 L260 120 L186 2z" fill="#ffe9a8" opacity=".35"/></g>
      <g class="feet" opacity="0"><rect x="-70" y="-11" width="50" height="13" rx="4" fill="#1a1408"/><rect x="20" y="-11" width="50" height="13" rx="4" fill="#1a1408"/><path d="M-70 2 L-80 90 L-20 90 L-20 2z M20 2 L20 90 L80 90 L70 2z" fill="#1a1408" opacity=".55"/></g>
    </g>`;
  }

  // ---------- ยานพาหนะ ----------
  function motorbike() {
    return `<g class="bike">
      <ellipse cx="0" cy="4" rx="130" ry="10" fill="#000" opacity=".22"/>
      <g class="wheel wb" transform="translate(-86 -34)"><circle r="34" fill="${P.dark}"/><circle r="22" fill="${P.metal}"/><circle r="6" fill="${P.dark}"/></g>
      <g class="wheel wf" transform="translate(96 -34)"><circle r="34" fill="${P.dark}"/><circle r="22" fill="${P.metal}"/><circle r="6" fill="${P.dark}"/></g>
      <path d="M-86 -40 l40 -30 h70 l30 36 h40 l-10 -20 h20 l20 54 h-56 l-14 -24 h-110 z" fill="${P.red}"/>
      <path d="M-60 -78 h70 l14 10 h-90z" fill="${P.dark}"/>
      <path d="M68 -84 l34 -34 l8 6 l-26 30z" fill="${P.metalD}"/>
      <rect x="92" y="-124" width="26" height="8" rx="4" fill="${P.dark}" class="throttle"/>
      <rect x="-150" y="-150" width="90" height="80" rx="8" fill="${P.jacket}"/>
      <rect x="-142" y="-142" width="74" height="64" rx="6" fill="${P.jacketD}" opacity=".4"/>
      <path d="M-30 -56 l-56 20 M60 -56 l26 20" stroke="${P.metalD}" stroke-width="8" stroke-linecap="round"/>
    </g>`;
  }
  function pickup(c = '#eef0ee') {
    return `<g class="pickup">
      <ellipse cx="0" cy="4" rx="190" ry="10" fill="#000" opacity=".22"/>
      <path d="M-190 -40 v-60 h120 l40 -60 h110 a14 14 0 0 1 14 14 v106z" fill="${c}"/>
      <path d="M-180 -100 h110 v-40 h-110z" fill="${c}" opacity=".9"/>
      <path d="M-60 -106 l34 -48 h50 v48z" fill="#2b3a4a"/>
      <path d="M-190 -42 h380 v12 h-380z" fill="#8b8f93"/>
      <g transform="translate(-120 -34)"><circle r="30" fill="${P.dark}"/><circle r="16" fill="${P.metal}"/></g>
      <g transform="translate(120 -34)"><circle r="30" fill="${P.dark}"/><circle r="16" fill="${P.metal}"/></g>
      <rect x="80" y="-74" width="14" height="8" rx="2" fill="${P.yellow}" class="hl"/>
    </g>`;
  }
  function gallon(c = P.yellow) {
    return `<g class="gallon">
      <ellipse cx="0" cy="2" rx="40" ry="6" fill="#000" opacity=".2"/>
      <path d="M-34 -8 v-80 a8 8 0 0 1 8 -8 h52 a8 8 0 0 1 8 8 v80 a8 8 0 0 1 -8 8 h-52 a8 8 0 0 1 -8 -8z" fill="${c}"/>
      <path d="M-26 -96 v-10 h20 v10z" fill="${c}"/><rect x="-10" y="-112" width="22" height="10" rx="3" fill="${P.dark}"/>
      <rect x="-22" y="-80" width="40" height="18" rx="4" fill="${P.dark}" opacity=".15"/>
      <path d="M-26 -62 h50 v30 h-50z" fill="#000" opacity=".1"/>
    </g>`;
  }
  function generator() {
    return `<g class="generator">
      <ellipse cx="0" cy="6" rx="150" ry="14" fill="#000" opacity=".3"/>
      <rect x="-130" y="-140" width="260" height="150" rx="14" fill="${P.red}"/>
      <rect x="-140" y="-156" width="280" height="24" rx="8" fill="${P.dark}"/>
      <rect x="-130" y="-60" width="260" height="70" rx="12" fill="#1d1f26"/>
      <g class="fan" transform="translate(-60 -70)"><circle r="46" fill="#2b2f38"/><circle r="40" fill="#15171c"/>
        <g class="fanblades">${[0, 60, 120, 180, 240, 300].map(a => `<path d="M0 0 l10 -30 a30 30 0 0 1 -20 0z" fill="#8a909a" transform="rotate(${a})"/>`).join('')}</g><circle r="8" fill="#555"/></g>
      <rect x="20" y="-124" width="90" height="56" rx="6" fill="#2b2f38"/>
      <circle cx="40" cy="-96" r="10" fill="#111"/><circle class="genled" cx="90" cy="-96" r="8" fill="#5a1a1a"/>
      <rect x="20" y="-56" width="90" height="36" rx="6" fill="#0d0f14"/>
      <rect x="30" y="-48" width="18" height="20" rx="3" fill="${P.yellow}"/><rect x="60" y="-48" width="18" height="20" rx="3" fill="${P.yellow}"/>
      <rect x="-20" y="-20" width="24" height="24" rx="4" fill="#111"/>
      <rect x="-118" y="-170" width="30" height="20" rx="4" fill="${P.metalD}"/>
      <g class="exhaust" transform="translate(-103 -176)"></g>
      <rect x="-150" y="-10" width="300" height="14" rx="6" fill="#222"/>
    </g>`;
  }
  function freezerUnit() {
    return `<g class="freezer">
      <rect x="-50" y="-200" width="100" height="200" rx="6" fill="#e8f0f3"/>
      <rect x="-42" y="-190" width="84" height="150" rx="4" fill="#8fd0ea" class="fzglass"/>
      <rect x="-42" y="-190" width="84" height="150" rx="4" fill="url(#glassShine)" opacity=".5"/>
      ${[0, 1, 2].map(i => `<rect x="-36" y="${-180 + i * 48}" width="72" height="4" fill="#cfe5ee"/>${[0, 1, 2, 3].map(j => `<rect x="${-34 + j * 18}" y="${-178 + i * 48 + 6}" width="12" height="20" rx="2" fill="${['#f28b2b', '#1f6fb2', '#2f9e5a', '#d7342c'][(i + j) % 4]}"/>`).join('')}`).join('')}
      <rect x="-50" y="-36" width="100" height="36" rx="4" fill="#cfd8dc"/>
      <circle class="fzled" cx="0" cy="-18" r="4" fill="#2bd46b"/>
    </g>`;
  }
  // คนเงา (พนักงาน/ลูกค้า) ยืนหน้าตรง
  function personFront(c = '#3a3f4a', h = 1) {
    return `<g class="person" transform="scale(${h})">
      <rect x="-18" y="-130" width="14" height="60" rx="6" fill="${c}"/><rect x="4" y="-130" width="14" height="60" rx="6" fill="${c}"/>
      <rect x="-30" y="-230" width="60" height="110" rx="14" fill="${c}"/>
      <rect x="-24" y="-270" width="48" height="50" rx="18" fill="${c}"/>
    </g>`;
  }

  // ---------- พื้นหลัง ----------
  function skyDusk() {
    return `<rect x="-400" y="-100" width="1520" height="900" fill="url(#skyDusk)"/>
      <circle class="sun" cx="560" cy="300" r="54" fill="#ffd08a"/>
      <g class="clouds" opacity=".55">${[[-200, 120, 1.2], [260, 80, .9], [700, 160, 1.1]].map(([x, y, s]) => `<g transform="translate(${x} ${y}) scale(${s})"><ellipse rx="110" ry="26" fill="#fff"/><ellipse cx="-50" cy="-10" rx="60" ry="26" fill="#fff"/><ellipse cx="50" cy="-8" rx="70" ry="30" fill="#fff"/></g>`).join('')}</g>`;
  }
  function skyNight() {
    return `<rect x="-400" y="-100" width="1520" height="900" fill="url(#skyNight)"/>
      <circle cx="560" cy="200" r="34" fill="#f2ead6" opacity=".9"/>
      <g class="stars">${Array.from({ length: 40 }, (_, i) => `<circle cx="${-300 + ((i * 97) % 1300)}" cy="${20 + ((i * 53) % 380)}" r="${1 + (i % 3) * .6}" fill="#fff" opacity=".7"/>`).join('')}</g>`;
  }
  function treeline(y, c = '#4b6b3a', n = 14, far = false) {
    let s = '';
    for (let i = 0; i < n; i++) {
      const x = -400 + i * (1500 / n), h = far ? 60 + ((i * 37) % 40) : 110 + ((i * 53) % 70);
      s += `<ellipse cx="${x}" cy="${y - h * .4}" rx="${h * .6}" ry="${h * .55}" fill="${c}"/><rect x="${x - 6}" y="${y - h * .3}" width="12" height="${h * .35}" fill="#5a4330"/>`;
    }
    return `<g class="treeline">${s}</g>`;
  }
  function road(y, w = 1600) {
    return `<g class="road">
      <rect x="${-w / 2}" y="${y}" width="${w}" height="400" fill="${P.asphalt}"/>
      <rect x="${-w / 2}" y="${y}" width="${w}" height="10" fill="${P.concreteD}"/>
      <g class="roadline">${Array.from({ length: 24 }, (_, i) => `<rect x="${-w / 2 + i * 80}" y="${y + 60}" width="44" height="8" fill="${P.line}" opacity=".8"/>`).join('')}</g>
    </g>`;
  }
  // ฝุ่นลอย (particles) — ตำแหน่งคำนวณจาก t ใน shots.js
  function dust(n = 24, cls = 'dust') {
    return `<g class="${cls}">${Array.from({ length: n }, (_, i) => `<circle class="p" r="${1.5 + (i % 3)}" fill="#fff4d6" opacity=".5"/>`).join('')}</g>`;
  }

  // ---------- Defs (gradients/filters) ใช้ร่วมทุกฉาก ----------
  function defs() {
    return `<defs>
      <linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a3f73"/><stop offset=".45" stop-color="#d9775e"/><stop offset=".8" stop-color="#f6b56a"/><stop offset="1" stop-color="#fbe0a8"/></linearGradient>
      <linearGradient id="skyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070a18"/><stop offset=".7" stop-color="#15203d"/><stop offset="1" stop-color="#2a2f4a"/></linearGradient>
      <radialGradient id="lightCone" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#fff3c4" stop-opacity=".55"/><stop offset="1" stop-color="#fff3c4" stop-opacity="0"/></radialGradient>
      <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6d0" stop-opacity=".9"/><stop offset=".4" stop-color="#ffd27a" stop-opacity=".35"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
      <radialGradient id="redglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff5a4a" stop-opacity=".9"/><stop offset=".5" stop-color="#d7342c" stop-opacity=".35"/><stop offset="1" stop-color="#d7342c" stop-opacity="0"/></radialGradient>
      <radialGradient id="headlight" cx="0" cy=".5" r="1"><stop offset="0" stop-color="#fff9df" stop-opacity=".9"/><stop offset="1" stop-color="#fff9df" stop-opacity="0"/></radialGradient>
      <linearGradient id="glassShine" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/><stop offset=".6" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <linearGradient id="groundCut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a5a3a"/><stop offset=".35" stop-color="#9c7a52"/><stop offset=".36" stop-color="#6b4f33"/><stop offset=".7" stop-color="#8a6a46"/><stop offset=".71" stop-color="#4f3b28"/><stop offset="1" stop-color="#3a2b1c"/></linearGradient>
      <linearGradient id="fuel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7c948"/><stop offset="1" stop-color="#d9962a"/></linearGradient>
      <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf6ea"/><stop offset="1" stop-color="#eee5d2"/></linearGradient>
      <filter id="blur3"><feGaussianBlur stdDeviation="3"/></filter>
      <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
      <filter id="blur10"><feGaussianBlur stdDeviation="10"/></filter>
      <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="1" result="n"/><feColorMatrix type="saturate" values="0"/></filter>
      <clipPath id="clipFrame"><rect x="0" y="0" width="720" height="1280"/></clipPath>
    </defs>`;
  }
  return { P, tonSide, tonSilhouette, dogSide, dogFace, zombie, canopy, dispenser, shopFront, restroomBlock, doorClose, motorbike, pickup, gallon, generator, freezerUnit, personFront, skyDusk, skyNight, treeline, road, dust, defs };
})();
