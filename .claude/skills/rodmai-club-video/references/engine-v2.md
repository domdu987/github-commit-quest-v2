# Engine v2: โค้ด เครื่องมือ และกับดัก

ระบบ: SVG + GSAP 3.14 บน HyperFrames 0.8.185 (เรนเดอร์ด้วย headless Chromium) · timeline เดียว paused ลงทะเบียนที่ `window.__timelines.main`
ทุกอย่างต้อง deterministic: สุ่มด้วย seeded RNG (`Pop2.mk(seed)`) ห้าม `Math.random`/`Date`

## สารบัญ
1. workspace และคำสั่ง build / ดูเฟรม / เรนเดอร์
2. ช็อต (`add`) และ helper
3. ชั้นภาพ และ look
4. ตัวละคร rig2
5. ชุดฉาก v2 และการเขียน lib ของเรื่องใหม่
6. PopUI (กราฟิกบนจอ)
7. กับดักที่เจอแล้ว

---

## 1. workspace และคำสั่ง

```bash
K=.claude/skills/rodmai-club-video/scripts
W=<scratchpad>/work
bash $K/setup_workspace.sh $W <story>1 <story>2 <story>3    # hf/lib hf/rig synth.py music + โฟลเดอร์ตอน
cd $W/<story>1
# ... lines.json → voices (audio-and-delivery.md) → python3 timing.py → schedule.json ... เขียน body.part
cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py
(cd $W/hf/<story>1 && (python3 -m http.server 8860 >/dev/null 2>&1 &))     # เสิร์ฟ 1 พอร์ตต่อ 1 ตอน
node $K/snap.cjs 8860 $W/<story>1/snap 3.9 7.2 12.5                          # ดูเฟรม (ต้องไม่มี PAGEERROR)
python3 $K/sheet.py $W/<story>1/snap $W/<story>1/snap/sheet.jpg 6
node $K/origin_check.cjs 8860 body.part && node $K/edgecheck.cjs 8860 schedule.json
```

- **ไฟล์ของแต่ละตอน**
  - `head.part`: CSS + helper + ประกาศ timeline · `helpers.part`: `split` `capsFrom` `tf` `put`
  - `body.part`: ช็อตทั้งหมดของตอน · `sigcard.part`: การ์ดเก่า (คงไว้ให้ template ทำงาน) · `foot.part`: badge + `Engine.build`
- **lib ใหม่ของเรื่อง** (เช่น `hf/lib/<story>.js`) ต้องทำ 2 อย่าง:
  1. เพิ่มชื่อในลิสต์ copy ของ `make.py`
  2. ใส่ `<script src="assets/<story>.js">` ใน `head.part` หลัง `pop2*.js` และก่อน `rig2.js`/`popcast.js` ถ้าเรื่องใช้ cast ใหม่
- **ห้ามรัน `make.py` ของตอนที่กำลังเรนเดอร์** (ไฟล์ใน `hf/<proj>` จะเปลี่ยนกลางเรนเดอร์)
- แก้ `*.part` แล้วต้อง `cat … > ep.tmpl.html` ก่อน `make.py` ทุกครั้ง ถ้าลืม ช็อตใหม่จะไม่ขึ้นและจอดำ

## 2. ช็อตและ helper

```js
add("key", {                                   // key ต้องมีใน schedule.json (ไม่มีจะถูกข้ามเงียบๆ)
  set: "kitchen2", setOpts: { id: "k8", time: "late" },   // Sets[set](L, setOpts) · id ของ set ≠ id ของช็อต
  dark: 0.15,                                  // ตั้งเองทุกช็อต (ค่าเริ่มต้น 0.35 = หม่นเทา) กลางวัน 0
  blur: { far: 2, mid: 0, set: 0, fg: 0 },     // px ต่อชั้น · fg มีเบลอ 7px ติดมาเป็นค่าเริ่มต้น (class fgblur) ต้องสั่ง fg: 0 ถ้าอยากชัด
  light: LAMP, grade: GLATE,                   // preset ด้านล่าง · light: false = ไม่ใส่แสงบนตัวละคร
  cam: { keys: [{ t: 0, ...fr(620, 1200, 2.0, 540, 1000) }, { t: 2.4, glide: 1.2, ...CU(400, 1500, 1.05) }] },  // drift: {x,y,s} ต่อวิ
  shake: (t) => 3 * Math.sin(t * 23),
  actors: [THONG(512, 1160, 1.05, [{ t: 0, mode: "seatWave", eyes: "wide", mouth: "scream" }], { flip: true, moveTo: { x, y, dur, ease } })],
  captions: caps("key", undefined, { quote: true }),      // ซับตามท่อนใน schedule
  extra(L, id) { /* SVG ก่อนสร้างนักแสดง */ },
  fx(tl, id, t0, L) { /* tween หลังสร้างทุกอย่าง; เวลาเป็นวินาทีของทั้งคลิป → t0 + ... */ },
});
```

- เวลาในช็อต: `vo(k,i)` เสียงที่ i เริ่ม · `voEnd(k,i)` · `F(k,i,j)` ท่อนซับที่ j ของเสียง i · `D(k)` ความยาวช็อต
- กล้อง: `fr(wx, wy, s, sx=540, sy=760)` วางจุด (wx,wy) ของฉากไว้ที่ (sx,sy) บนจอด้วยซูม s · `CU(x, y, s, sy)` เฟรมหน้าตัวละครสเกล s ที่ยืนที่ (x,y)
- `split(k, at, A, B)` = ช็อตเดียว (เสียงเดียว) สองการตั้งกล้อง/สองฉาก · `capsFrom(k, at, lines, o)` ซับของช่วงหลัง
- `oneHand(id, i)` ลบของในมือหลังของนักแสดงที่ i · `tf(tl, sel, t, dur, "transform…")` tween attr.transform · `put(el, html)`
- preset แสงที่ใช้แล้ว (ประกาศใน body.part):
  - `SUN` `RAINY` `DUSK` `FIRE` `MOON` `LAMP` `TUBE` `DASH`
  - รูปแบบ `{ from: "left"|"right", rim, rimOp, shade, shadeOp, cast: {len, op}|false, vol: false }`
  - `vol: false` เสมอ ไม่งั้นแสงไล่บนตัวจะเป็นลายไม้
- เกรด: `GDAY GRAIN GDUSK GFIRE GNIGHT GLATE GROAD` = `{ top, bottom, op }`
- ซับคำพูด: `caps(k, [lineIdx…], { quote: true, hold })` · ฟองคำพูด `bub(k, i, x, y, tail)`

## 3. ชั้นภาพและ look

| ชั้น | parallax | ใช้กับ |
|---|---|---|
| `L.sky` 0.05 · `L.far` 0.25 · `L.mid` 0.6 | ช้ากว่ากล้อง | ฟ้า ทิวเขา ทุ่ง |
| `L.set` 1 · `L.act` 1 | ตามกล้อง | ฉากหลัก · นักแสดง (engine ใส่เอง) |
| `L.fg` 1.5 + เบลอ 7px | เร็วกว่ากล้อง | ใบไม้/เสาหน้ากล้องให้ความลึก |
| `L.glow` | ตามกล้อง อยู่เหนือ `dark` และนักแสดง | แสงไฟ ตาเรือง ป้ายมีไฟ **ของที่ต้องทับนักแสดงให้คม** (ขอบกระบะ ประตูรถ กรอบกระจกหน้า มุ้ง) |
| `L.light` | ติดจอ ไม่ขยับตามกล้อง | การ์ด ชิป ซับเสริม ฝุ่นบนเลนส์ |

- `#id-dark` (multiply) อยู่ระหว่างนักแสดงกับ glow · ของใน glow ไม่โดนความมืด → ใช้ดาร์กเองถ้าจำเป็น
- ทุกช็อตมี vignette + grain จาก `Engine.look` · `#flashw` `#black` `#fxred` ใช้ร่วมกันทั้งคลิป

## 4. ตัวละคร rig2 (`rig2.js` + cast ของเรื่อง แบบ `popcast.js`)

```js
C.name = { v2: { skin, iris, lash, blush, lip, bags, w (กว้าง), limb (ความหนาแขนขา), headScale (1.12),
  hair: { c, s, sh, front: (x) => svg, back: (x) => svg },          // ผมสองชั้น ชั้นหลังหมุนตามหัว
  top: { kind: "tee|tank|shirt|blouse|singlet|coat", c, sleeve: "short|elbow|long|none", neck, collar, button },
  bottom: { kind: "jeans|shorts|sarong|trousers", c }, feet: { kind: "sneaker|boot|bare|sandal" },
  print, extra, face, faceTop } };                                   // ลวดลายเสื้อ เครื่องประดับ ริ้วรอย หมวก
```
- **ตา:** normal side wide closed pain glow dead worry angry
- **ปาก:** smile flat o frown scream snarl laugh
- **ท่า (`mode`):** idle walk run crouch sit (นั่งพื้น ขาไปข้างหน้า สะโพกลง 290·c) sitChair lie tremble holdHead raise phoneEar point torch whistle wave phoneLook shamble lunge zrun swing push fall
  - ท่าที่ประกาศใน body ของเห็ดปอบ: `selfie laugh shiver stick crouchTorch stir reach seatWave sitWind drive`
- **ท่าใหม่:** `Rig.MODES.x = (u, o) => ({ ...Rig.MODES.idle(u, o), uaF, faF, uaB, faB, torso, head, hair, bodyY })`
  - แขน F ค่าลบ = ยกออกด้านข้าง · แขน B ค่าบวก = ยกออกด้านข้าง
  - `hair` = ผมสะบัด
  - ท่าที่ไม่มีอยู่จริงทำให้ทั้ง timeline พัง
- **ของในมือ:** cast variant `{ ...Rig.CAST.mint, hand: Pop2.PROP.phone() }` (ฝ่ามือที่ (0,118) ของกลุ่มมือ) แล้ว `oneHand(id, i)` ใน fx
- **ตำแหน่งของร่างกาย:** `x, y` = เท้า · ส่วนสูง ~620·s · `flip` = หันกลับ · `blinks: [t…]`
  - `moveTo` = เดินไปจุดหมาย · `path: [{t,x,y,flip}]` = เดินตามจุดหลายจุด (ใช้กับบันได)
  - **เปลี่ยน mode → blend 0.22 วิเอง** · ตาเปลี่ยนเป็น wide → สะดุ้งเอง

## 5. ชุดฉาก v2 และการเขียน lib ของเรื่องใหม่

ฉากที่มีแล้ว (อ่านหัวไฟล์แต่ละไฟล์สำหรับ option และ id):
- `pop2.js`: `village2` (หมู่บ้านอีสาน กลางวัน/เย็น/คืน บ้านใต้ถุนสูง ถนนแดง แอ่งน้ำ), `Pop2.particles` (dust rain firefly ember steam wisp), `Pop2.mk` `f1` `put` `blob` `cloud2` `tree2` `tuft` `puddle`
- `pop2kok.js`: `kok2` (ป่าโคก จอมปลวก เห็ด), `mushHero`, `Pop2.mush2/mound2/trunk2`
- `pop2kitchen.js`: `kitchen2` (ครัวใต้ถุน เตาอั้งโล่ หม้อแกง ตะเกียง), `Pop2.flicker`
- `pop2room.js`: `bedroom2` (มุ้ง), `gap2` (มองผ่านร่องพื้น), `Pop2.ghost2` (ผีดำตาเขียว eat/peer/stand), `Pop2.eyePair`
- `pop2more.js`: `clock2` `legend2` (หนังตะลุง) `potTop` `testsTop` `potX` `printsTop` `sign2` (การ์ดท้าย), `Pop2.pobFace` `trail` (รอยเท้า) `PROP` `fence`
- `pop2hosp.js`: `nightRoad2` (กระบะไทยสัดส่วนจริง `o.s ≈ 2.25·c`, `bedFront`/`doorFront`), `cab2` (คนขับผ่านกระจกหน้า), `erFront2`, `ward2`, `benchTop`, `Pop2.truck`
- `pop2end.js`: `board2` (กระดานกราฟอาการ), `Pop2.yaiBack`, `feet2`
- `pop2ui.js`: `PopUI` (หัวข้อ 6)
- `maps.js` + `mapsdata.js` (`video/lib-shared/`, setup ใส่ให้ทุกตอนอัตโนมัติ): แผนที่เดินทาง (กติกา S12 ทุกการเดินทางต้องมีแผนที่)
  - `Sets.mapTH(L, { id, x, y, s, route: [[lon, lat]…], from, to, vehicle: "bus"|"van"|"moto"|"ambulance", region: [lon, lat, r, "อีสาน"], toIcon })` ประเทศไทยจริง (Natural Earth 1:50m) พร้อมประเทศรอบข้าง
  - `Maps.route(tl, id, t0, { go: [เริ่ม, ถึง] })` หมุดต้นทางตก → เส้นทางวาดตามพร้อมพาหนะวิ่งบนหัวเส้น → ภูมิภาคเรืองแสง → หมุดปลายทางตกพร้อมวงคลื่น
  - กล้องซูมเข้าหมุดปลายทางตอนจบด้วย `cam.keys` (`glide`) แล้วตัดเข้าฉากที่ไปถึง · `Maps.P(lon, lat)` คืนพิกัดในแผนที่
  - แผนที่ระดับหมู่บ้าน (บ้าน → ศาลา AED) ให้ทำเป็น set ของเรื่องเองโดยใช้ `Maps.smooth` กับ `Maps.VEH`
- ตัวอย่างกราฟิกระดับมืออาชีพ (กติกา V8): `video/mm/lib/mmui.js` ของผีแม่ม่าย
  - ฟลิปชาร์ต อสม. ที่หัวใจบีบ/เต้นระริกได้ จอ ECG กวาดตามจังหวะ ป้ายตรายาง และการ์ดกฎห้อยสายคล้องคอพร้อมไอคอนที่ขยับ
  - ใช้เป็นแม่แบบ: เส้นหมึก 4–5 สีแบน + เงา 1 ชั้น + ไฮไลต์ 1 ชั้น · เข้าด้วย back/elastic/bounce ไล่ทีละชิ้น · มีการเคลื่อนไหวรองหลังเข้า · ตัดภาพในวงกลมไอคอนด้วย clipPath

**lib ของเรื่องใหม่** (`hf/lib/<story>.js`) ใช้แบบเดียวกับ pop2*.js:
```js
(function () {
  const { mk, f1, put, blob } = Pop2;
  Sets.DEFS += `<linearGradient id="xxSky" …/>`;           // gradient ใหม่ตั้งชื่อนำหน้าด้วยรหัสเรื่อง
  function place2(L, o = {}) {
    const id = o.id || "pl", r = mk(o.seed || 7), G = o.ground ?? 1400;
    put(L.sky, `…`); put(L.far, `…`); put(L.mid, `…`); put(L.set, `…`); put(L.glow, `…`); put(L.fg, `…`);
  }
  Object.assign(Sets, { place2 });
})();
```
- ทุกชั้นต้องมีของ ฉากกว้างต้องเกินขอบจอ (−1300…2400) เผื่อกล้องเลื่อน · id ของชิ้นที่จะขยับ = `${id}-ชื่อ` บน `<g>` ห่อที่ไม่มี transform
- เขียนหัวไฟล์อธิบาย option และ id ทุกฉาก (คนถัดไปอ่านหัวไฟล์อย่างเดียว)
- gradient ของชิ้นที่ต้องวาดซ้ำทับนักแสดง (ประตูรถ ขอบกระบะ) ใช้ `gradientUnits="userSpaceOnUse"` ไม่งั้นสีของชิ้นที่วาดซ้ำจะไม่ตรงกับตัวเดิม

## 6. PopUI (กราฟิกบนจอ ใส่ `L.light`)

- `PopUI.rule(tl, L.light, t0, dur, { active, done, y, s, out })` การ์ดกฎ 3 ข้อ (ข้อความอยู่ใน `PopUI.RULES` ของเรื่อง)
- `PopUI.source(tl, L.light, t0, dur, { text, y: 1810 })` ชิปที่มา
- `PopUI.phone(tl, L.light, t0, dur, { mode: "nosignal"|"camera"|"photo", y, out })` มือถือในมือ
- `PopUI.timeline(…, { y })` แถบเวลา "กิน → 4–6 ชม. → อาการ" (นาฬิกาหมุนแค่เข็ม)
- `PopUI.choice(…, { q, a, b, secs, y, iconB, possessed: { at, side, glitch, who } })` ตัวเลือกท้าย
- `PopUI.form(…, { rows: [[label, answer, at]], y })` แบบฟอร์ม/ประวัติ · `PopUI.tag(x, y, text, { icon, w, color, rot, id })` ป้ายกระดาษปักดิน (คืน SVG)
- `PopUI.sfx(tl, layer, t0, dur, text, x, y, o)` คำเสียง Sriracha
- `PopUI.ICON.<ชื่อ>(x, y, s)` ไอคอนวาดมือ (กล่อง 100 หน่วย)
  - ที่มีแล้ว: mush mushQ basketX hospital belly skull check cross clock spoon rice shallot fire palette nose shape pot
  - และจาก pop2hosp: throat saltglass lungs vomit bag photo people form liver doctor trend bowl
- **เรื่องใหม่:** ทำ `<story>ui.js` ที่วาดการ์ดในลายมือของโลกเรื่องนั้น โดยใช้ PopUI เป็นต้นแบบ

## 7. กับดักที่เจอแล้ว

**GSAP บน SVG**
- gradient แบบ objectBoundingBox บนเส้นตรงแนวตั้ง/แนวนอน (กล่องกว้างหรือสูง 0) จะไม่ระบายอะไรเลย → ใช้สีทึบหรือ `gradientUnits="userSpaceOnUse"` (ท่อเลือดของหัวใจเคยเป็นสีดำเพราะเหตุนี้)
- ของที่ต้องซ่อนจนถึงจังหวะเข้า (หมุด ป้าย พาหนะ) ต้อง `tl.set(..., { opacity: 0 }, t0)` ตอนต้นช็อต ไม่งั้นจะโผล่ค้างก่อนเวลา เพราะ `immediateRender: false`
- ห้าม tween `x/y/rotation/scale` บน `<g>` ที่มี attribute `transform` เพราะ GSAP จะล้าง translate เดิม แล้วของจะกระโดดไปมุมจอ
  - ให้ใส่ id บน `<g>` ห่อชั้นนอกที่ไม่มี transform แล้ว tween ตัวนั้น หรือ tween `attr: { transform }`
- **`svgOrigin` ใช้พิกัดเดียวกับที่รูปทรงข้างใน element วาดไว้** (พิกัดของ parent เมื่อ element ไม่มี transform) ไม่ใช่พิกัดจอ (ทดสอบแล้ว 28 ต.ค. 2026)
  - ถ้าใส่พิกัดจอให้ของที่อยู่ในกลุ่มที่ translate ไว้ ของจะเหวี่ยงมาจากนอกจอ · ตรวจด้วย `origin_check.cjs`
- tween ที่เริ่มทีหลังต้องใส่ `immediateRender: false` · ของที่ต้องซ่อนก่อนเวลาให้ `tl.set(sel, { opacity: 0 }, t0)`
- tween `attr.transform` ต้องมีค่าเริ่มต้นรูปแบบเดียวกันอยู่ใน element ก่อน
- lint ห้าม template literal ใน `querySelector` → ใช้ `getElementById(id).querySelectorAll(".x")`

**engine**
- **ฉากในห้อง: ผนังหลังต้องอยู่ `L.set`** ไม่ใช่ `L.mid` (parallax 0.6 ทำให้ผนัง ประตู รูป นาฬิกา เลื่อนผิดกับพื้น และกล้องซูมใกล้แล้วเฟรมผิด) ใส่ `L.mid` ได้แค่วิวนอกหน้าต่าง
- **ปากขยับตอนพูด:** ใส่ `talk: [[เริ่ม, จบ, "o"]…]` ในตัวเลือกนักแสดง (rig.js อ่าน `track.talk`) ใช้ helper `TALK(k, i, mouth)` = `[vo(k,i), voEnd(k,i), mouth]` ทุกบรรทัดของตัวละคร
- **คนคุกเข่าข้างคนนอน:** วางคนคุกเข่าไว้ "หน้า" ขอบที่นอน (y มากกว่า) แล้วใส่ก่อนคนนอนในลิสต์ actors ให้ตัวคนนอนบังหน้าแข้ง แขนลงแนวดิ่งถึงไหล่ ห้ามเอียงลำตัว (torso) เพราะในมุมหน้าตรงจะดูเหมือนลอย
- `extra()` วาดก่อนสร้างนักแสดง ของที่ต้องทับนักแสดงให้ใส่ `L.glow` หรือใส่ใน `fx()`
- `dark` ค่าเริ่มต้น 0.35 → ฉากกลางวันหม่น ตั้งเองทุกช็อต · `fg` เบลอ 7px และ parallax 1.5 → ของหน้ากล้องที่ต้องคมและติดกับตัวละคร (พวงมาลัย มือ) ใส่ `L.glow`
- แสง `vol` แบบไล่ทำให้ตัวละครใกล้กล้องเป็นลายไม้ → `vol: false`
- `add()` ข้าม key ที่ไม่มีใน schedule เงียบๆ: ช็อตหายไม่ใช่ error ให้ดู sheet
- ท่าที่ไม่มีจริง → timeline พังทั้งคลิป

**ตรวจภาพ**
- screenshot แรกหลังโหลดอาจเป็นเฟรมค้างหรือดำ → `snap.cjs` ถ่ายเฟรมทิ้ง 2 รอบแล้ว (รอบสองที่เวลาแรกที่ขอ) ถ้ายังดำให้ถ่ายเวลานั้นซ้ำ
- ต้อง `seek(t, false)` (เปิด events) ไม่งั้นกล้องไม่ขยับ
- `npx hyperframes check` หมดเวลาบ่อย ให้ดู console ผ่าน `snap.cjs` แทน (ต้องไม่มี PAGEERROR)

**เครื่องมือ**
- เรนเดอร์ด้วย `nohup … &` ใน Bash ธรรมดาจะโดนยกเลิก ต้องใช้ `run_in_background` และตั้ง `timeout: 7200000` (ค่าเริ่มต้น 30 นาทีฆ่างาน)
- ห้าม `pkill -f`/`pgrep -f` ด้วย pattern ที่อยู่ในบรรทัดคำสั่งของตัวเอง (จะฆ่า shell ตัวเอง) ให้ใช้ `ps -eo pid,args | grep` แล้วเลือก PID
- เซิร์ฟเวอร์ `http.server` ตายได้เมื่อ container รีสตาร์ต ถ้า snap ขึ้น `ERR_CONNECTION_REFUSED` ให้เปิดใหม่
