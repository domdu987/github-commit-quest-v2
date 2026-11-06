
// ---------------------------------------------------------------- ต้นตะเคียนกลางนา ฉบับเต็ม (16:9) only — appended to takhian.js by
// full/build_full.sh; the Shorts builds never load it. Review c47e401 (6 Nov 2569) round-3 fixes:
//   B1  the cab sets fill the 16:9 frame: the outer cab reaches x −700…1780 (the widened stage), side windows left and right of the
//       A-pillars, the dashboard and the door cards run the full width (Tk.cabIn, Tk.cab)
//   B7  the photo is planted: a small framed black-and-white photo of the young farmer stands in the shrine doorway between ตา and ยาย,
//       in every shrine of the long cut (EP.1 buff/sci1 onward), so "รูปในศาล" in EP.2 pays off something already seen
//   B7  C.taYoung: the young grandfather of the flashback (as in the photo: งอบ, white shirt, indigo farmer trousers)
(() => {
  const Tk = window.Tk, INK = "#1e1a16";
  const f1 = (v) => (+v).toFixed(1);
  const mk = (seed) => () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
  const FULL = "M0,0H1080V1920H0Z", WIDE = "M-700,0H1780V1920H-700Z";
  const sw = (s, a, b) => { if (s.indexOf(a) < 0) throw new Error("longkit: missing " + a.slice(0, 60)); return s.split(a).join(b); };

  // B1 · inside the pickup from the back seat, looking out the windshield, now as wide as the page
  const cabIn0 = Tk.cabIn;
  Tk.cabIn = (o = {}) => {
    const c = cabIn0(o), r = mk((o.seed || 91) + 7);
    const sideL = "M-640,560Q-330,420 40,350L4,1166Q-330,1176 -640,1196Z";
    const sideR = "M1720,560Q1410,420 1040,350L1076,1166Q1410,1176 1720,1196Z";
    let frame = sw(c.frame, `<path d="${FULL} ${c.hole}"`, `<path d="${WIDE} ${c.hole} ${sideL} ${sideR}"`);
    // the dashboard and its top edge run on into the doors
    frame = sw(frame, `<path d="M0,1160Q540,1110 1080,1160V1920H0Z" fill="#1e252c"/>`,
      `<path d="M-700,1196L-640,1196Q-330,1176 0,1160Q540,1110 1080,1160Q1410,1176 1720,1196L1780,1196V1920H-700Z" fill="#1e252c"/>`);
    frame = sw(frame, `<path d="M0,1180Q540,1130 1080,1180" stroke="#36404a" stroke-width="10" fill="none"/>`,
      `<path d="M-700,1216Q-330,1196 0,1180Q540,1130 1080,1180Q1410,1196 1780,1216" stroke="#36404a" stroke-width="10" fill="none"/>`);
    // window frames, B-pillars at the far edges, door cards with armrest, handle and speaker grille, roof grab handles
    let x = `<path d="${sideL}" fill="none" stroke="#0a0e12" stroke-width="22"/><path d="${sideR}" fill="none" stroke="#0a0e12" stroke-width="22"/>`;
    x += `<path d="M-700,0V1920M-660,0L-640,1196" stroke="#12171c" stroke-width="70"/><path d="M1780,0V1920M1740,0L1720,1196" stroke="#12171c" stroke-width="70"/>`;
    [-1, 1].forEach((sd) => { const X = (v) => (sd < 0 ? v : 1080 - v);
      x += `<path d="M${X(-640)},1290Q${X(-330)},1262 ${X(-40)},1252" stroke="#2e363e" stroke-width="16" fill="none" stroke-linecap="round"/>`;
      x += `<path d="M${X(-600)},1420Q${X(-330)},1390 ${X(-80)},1384L${X(-80)},1430Q${X(-330)},1436 ${X(-600)},1470Z" fill="#283038" stroke="#0e1216" stroke-width="5"/>`;
      x += `<rect x="${Math.min(X(-260), X(-170))}" y="1316" width="90" height="26" rx="10" fill="#3a444e" stroke="#0e1216" stroke-width="4"/>`;
      x += `<circle cx="${X(-420)}" cy="1640" r="70" fill="#151a1f" stroke="#2a323a" stroke-width="6"/>${[0, 1, 2, 3].map((k) => `<circle cx="${X(-420)}" cy="1640" r="${16 + k * 14}" fill="none" stroke="#0a0e12" stroke-width="3"/>`).join("")}`;
      x += `<path d="M${X(-460)},300Q${X(-380)},250 ${X(-300)},280" stroke="#0e1216" stroke-width="18" fill="none" stroke-linecap="round"/>`; });
    // the side glass: tinted (so the eye stays on the windshield), its own rivulets and drops
    const glassS = (hole, box) => `<path d="${hole}" fill="#0a1622" opacity=".32"/>` + Tk.wetGlass(r, hole, box);
    return { ...c, frame: frame + x, glass: c.glass + glassS(sideL, [-600, 0, 460, 1160]) + glassS(sideR, [1080, 1680, 460, 1160]) };
  };

  // B1 · the side window (ต้น watches ลุง run to the tree): the window wall runs the full width — front-door window on the left,
  // B-pillar, the rear-door window, the door card under both
  const cab0 = Tk.cab;
  Tk.cab = (o = {}) => {
    const c = cab0(o); if (o.view === "windshield") return c;
    const r = mk((o.seed || 88) + 5), front = "M-640,440Q-640,380 -580,380H-90Q-40,380 -40,430V1300H-640Z", back = "M1120,430Q1120,380 1170,380H1660Q1720,380 1720,440V1300H1120Z";
    const hole = "M70,420Q70,360 130,360H980Q1040,360 1040,420V1300H70Z";
    let frame = sw(c.frame, `<path d="${FULL} ${hole}"`, `<path d="${WIDE} ${hole} ${front} ${back}"`);
    frame = sw(frame, `<path d="M0,1330H1080V1920H0Z" fill="#20262c"/>`, `<path d="M-700,1330H1780V1920H-700Z" fill="#20262c"/>`);
    frame = sw(frame, `<path d="M0,1420Q540,1360 1080,1420"`, `<path d="M-700,1440Q-300,1380 0,1420Q540,1360 1080,1420Q1400,1380 1780,1440"`);
    let x = `<path d="${front}" fill="none" stroke="#0a0e12" stroke-width="22"/><path d="${back}" fill="none" stroke="#0a0e12" stroke-width="22"/><path d="M-640,1300H-40M1120,1300H1720" stroke="#2a3036" stroke-width="30"/>`;
    x += `<path d="M1080,300V1920" stroke="#141a20" stroke-width="80"/><path d="M1080,300V1920" stroke="#0a0e12" stroke-width="6" opacity=".8"/><path d="M-40,300V1920" stroke="#141a20" stroke-width="60"/>`;
    x += `<rect x="-460" y="1500" width="130" height="30" rx="12" fill="#3a444e" stroke="#0e1216" stroke-width="4"/><rect x="1300" y="1500" width="130" height="30" rx="12" fill="#3a444e" stroke="#0e1216" stroke-width="4"/>`;
    x += `<path d="M-640,1600Q-340,1570 -60,1570L-60,1620Q-340,1620 -640,1650Z" fill="#283038" stroke="#0e1216" stroke-width="5"/><path d="M1140,1570Q1420,1570 1720,1600L1720,1650Q1420,1620 1140,1620Z" fill="#283038" stroke="#0e1216" stroke-width="5"/>`;
    const glassS = (h, box) => `<path d="${h}" fill="#0a1622" opacity=".3"/>` + Tk.wetGlass(r, h, box);
    return { frame: frame + x, glass: c.glass + glassS(front, [-620, -60, 400, 1290]) + glassS(back, [1140, 1700, 400, 1290]) };
  };

  // B7 · the photo planted in the shrine: ตา and ยาย step aside, the framed photo stands between them in the lit doorway
  Tk.miniPhoto = (x, y, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-23" y="-58" width="46" height="58" fill="#6a4020" stroke="${INK}" stroke-width="2.4"/><rect x="-18" y="-53" width="36" height="48" fill="#d6d0c2"/>
    <path d="M-18,-53H18V-34Q8,-40 0,-37Q-8,-40 -18,-34Z" fill="#8a867c"/><path d="M-5,-5V-36H5V-5Z" fill="#7a7468"/><rect x="-5" y="-26" width="10" height="3" fill="#c83a2a" opacity=".7"/>
    <g transform="translate(-9,-20)"><path d="M-5,15Q-6,4 0,3Q6,4 5,15Z" fill="#4a4640"/><ellipse cy="-1" rx="3.6" ry="4.2" fill="#b0aa9e"/><path d="M-7,-3Q0,-9 7,-3Q0,-4.5 -7,-3Z" fill="#5a564e"/></g>
    <rect x="-18" y="-53" width="36" height="48" fill="#7a6a50" opacity=".2"/><path d="M-16,-50L4,-30" stroke="#fff" stroke-width="2" opacity=".55"/><path d="M-23,-1H23" stroke="#c83a2a" stroke-width="3"/>
    <path d="M-20,-1q5,-5 10,0q5,-5 10,0q5,-5 10,0q5,-5 10,0" stroke="#f2c230" stroke-width="2" fill="none"/></g>`;
  const shrine0 = Tk.shrine;
  Tk.shrine = (x, y, s = 1, o = {}) => {
    let g = shrine0(x, y, s, o);
    g = sw(g, `<g transform="translate(-17,-310)">`, `<g transform="translate(-35,-310)">`);
    g = sw(g, `<g transform="translate(17,-310)">`, `<g transform="translate(35,-310)">`);
    const a = `<path d="M-56,-308V-394Q-56,-430 0,-442Q56,-430 56,-394V-308" stroke="url(#tkShGold)"`;
    return sw(g, a, Tk.miniPhoto(0, -312, 1.15) + a);
  };

  // B7 · the young grandfather (the man in the photo): งอบ, white shirt, indigo farmer trousers
  const C = Rig.CAST, LN = (w = 2.6) => `stroke="${Rig2.LINE}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
  const ngob = `<g transform="translate(0,26)"><path d="M-120,-588Q0,-700 120,-588Q0,-604 -120,-588Z" fill="#c8a868" ${LN()}/><path d="M-90,-610Q0,-680 90,-610" stroke="#a88a4a" stroke-width="4" fill="none"/><path d="M-60,-630Q0,-676 60,-630" stroke="#a88a4a" stroke-width="4" fill="none"/></g>`;
  const b = (C.taJun && C.taJun.v2) || {};
  C.taYoung = { v2: { ...b, faceTop: ngob, hair: { ...(b.hair || {}), c: "#16100c", s: "#000", sh: "#4a3a30" }, top: { kind: "shirt", c: "#eceae2", sleeve: "long", neck: "collar", collar: "#d8d4c8", button: "#fff" }, print: "",
    bottom: { kind: "jeans", c: "#2a3450" }, feet: { kind: "bare" }, extra: "" } };
})();
