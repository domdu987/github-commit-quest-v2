# ภาพ กล้อง ไอคอน และ API ที่ใช้จริง (ชุดจอมโกหก)

โค้ดต้นแบบ: `video/jk-ep1/production/body_shots.part` (เมือง เมฆ เมืองในฝัน) · `video/jk-ep3/production/body_shots.part` (โรงเตี๊ยม หน้าต่าง ลานเมือง) · `video/jk-ep2/…` (ตรอก การ์ดเล่าเรื่อง เงาบนผนัง)

## 1. สเปกช็อต (`shot(key, {...})` → `Engine.build`)
| ฟิลด์ | ความหมาย |
|---|---|
| `...city(k)` `...cloud(k)` `...town(k)` `...townN(k)` `...inn(k)` `...alley(k)` | ฉาก + แสงประจำฉาก (DAY/NIGHT) · `setOpts` เช่น `{ manhole:true, dark:true, dusk:true, dragon:{x,y,s,flip} , rows }` |
| `camAt: fr(wx, wy, s, sx=540, sy=760)` | ให้จุดโลก (wx,wy) อยู่ที่จุดจอ (sx,sy) ที่สเกล s · `face(x, y=1400, s=3.2, flip, sx, sy)` เล็งหน้า · `faceSit/faceStand` ใน ep3 |
| `cam: { keys:[{t, ...fr(), drift:{x,s}, glide}] }` | หลายเฟรมมิ่งในช็อตเดียว: ตัดฉับ (ไม่มี glide) หรือเลื่อนเข้าหา key ที่มี `glide` วินาที · `push` = s ต่อวินาทีตอนค้าง |
| `shake: fn(t)` | คืนเลข (สั่นแนวนอน) หรือ `{x,y,r}` (โยก+เอียง) ใช้ `JKC.hand/impact/dutch/pov` |
| `dark, grade:{top,bottom,op,blend}, blur:{far,mid,set,act,fg,glow}` | ความมืด เกรดสี โฟกัส (blur ต่อชั้น) |
| `actors: [ME(who,x,y,track,extra) \| A(who,x,y,s,track,extra) \| KID(...)]` | `track` = `[{t, mode, eyes, mouth}, …]` · `extra`: `flip, path:[{t,x,y}], moveTo:{x,dur}, talk` |
| `captions` (อัตโนมัติจาก `caps(k)`) · `sfxText:[{text,x,y,size,rot,color,t,end}]` · `cards` · `bubbles` | ตัวหนังสือในจอ (พิกัดแนวตั้ง 1080×1920 แปลงอัตโนมัติในแนวนอน) |
| `extra(L)` | วาดเพิ่มก่อนนักแสดง (OTS, bucketPOV, ของประกอบ) |
| `fx(tl, id, t0, L)` | แอนิเมชันเพิ่ม: `hud(id, …)`, ไอคอน `JKI.*`, กล้องพิเศษ `JKC.*`, ของใน `grp(L.light)` (จอ) / `grp(L.act)` (โลก) |

ชั้นภาพ: `L.sky far mid set act fg` (โลก, parallax ต่างกัน) · `L.glow` (แสงเหนือความมืด ติดกับ set) · `L.light` (จอ: ไอคอน การ์ด แฟลช) · `L.screen` (จอเต็มเฟรมเสมอ: แถบดำ เงาข้ามไหล่ POV) · `.act-front` ในฉาก = เฟอร์นิเจอร์ที่บังนักแสดง

## 2. ฉากและความมีมิติ (`jkset.js` + `jkdepth.js`)
- ฉากกว้าง −2400…3800 (ใช้ได้กับแนวนอนทุกสเกล) · พื้นที่ y ≈ 1400 · ตัวละครสูง ~520
- `JKD.dress[set](L, tl, sh, id, o)` ถูกเรียกอัตโนมัติ (`sh.depth !== false`): กรวยแสง (op ×0.6) เงาสัมผัส หมอก ฝุ่น นก ควัน + ของตกแต่ง · ดีบั๊ก `?nodepth ?nomotes ?nodeco`
- โคม/แดด/เตาผิง: ค่าที่ลดแล้ว (tavern lamp r300 op .55, fireplace .6/.22, alley .65/.35, cloud rays .26/.18, town sun .35, city warm .7/.45) **อย่าเพิ่ม**
- มังกร `JK.dragon(fill, {stroke, sw, dash, detail:false, ko:true, heads:"prefix"})` สามหัว หันขวา กว้าง ~640 ขอบ x −310…350 y −300…166 เท้า y 146 · `ko` = ตา X ปากหุบ ลิ้นห้อย ปีกตก · `heads` ให้ `#<prefix>h0..2` สำหรับโยกหัว (เงาบนผนัง EP.2) · โหมด stroke = รูปชอล์ก (วาดส่วนหลักอย่างเดียว ไม่รก)
- ในฉากเมือง `setOpts.dragon:{x:1780,y:1290,s:1.6}` (นอนสลบหลังฉากด้านขวา ไม่บังช็อตใกล้) · ตัวยักษ์กลางเมือง (EP.3 c13) `translate(1150,1640) scale(-3.1,3.1) rotate(-3)` + `stars()` ที่หัว (420,960)

## 3. ตัวละคร v2 (`flat.js` + `jkcast.js` + `sig.js`)
- `Rig.FLAT = true` · ชิ้นส่วนห่อด้วย `.flSq` (ย่อยืด) `.flBr` (หายใจ) `.flHb` (หัวโยก) `.flHs` (ผม) · `life()` เดินอัตโนมัติ: หายใจ 1.013, หัว ±0.6°, ผม ±1.4°, เนคไท ±2.2°, ผ้าพันคอ ±5°, ตาเหลือบทุก ~2.6 วิ
- ท่า (`mode`): idle walk fall startle knocked raise laugh sitChair + ท่าแสดง `shrug facepalm cheer cower think coverEars despair relief pray fold nod no` และแบบนั่ง `sitCheer sitPray sitCower sitDespair sitCoverEars sitHoldHead sitFacepalm`
- ตา: normal wide closed side happy sad squint · ปาก: flat o smile scream laugh smirk grin pout grit · หูแดง `ears(tl, aid, at, on)` · `Rig.squash(tl, id, at, 0.2)` ตอนลงพื้น
- ตัวเอกใส่ถัง = `jkYouBucket` · ถือหนังสือ = `jkYouBook` · เด็ก `jkKidLizard` (s 0.64) · กษัตริย์เด็กดาบแสง `jkKen` · ลูกค้าในร้าน `PATRONS(mode, eyes, mouth)` (x 150 440 560 1010 1250)
- ระวังเฟอร์นิเจอร์ act-front: โรงเตี๊ยม เคาน์เตอร์ x 970–1530 (top 1138) โต๊ะ x 160–420 / 560–820 สตูล 150 440 560 840 → คนยืนต้องเว้นช่อง (เด็กที่ 920 พอดี)

## 4. กล้อง (`jkcam.js` → `JKC`)
| ตัวช่วย | ใช้เมื่อ | ตัวอย่างจริง |
|---|---|---|
| `JKC.move(frA, frB, at, glide)` | เครน/ซูมฉับ (glide สั้น 0.12–0.14 = ฉับ, 1.5–2 = เครน) | เปิดเมือง `move(fr(820,700,0.9,540,700), fr(820,1060,0.95,540,1000), 2.0, 1.6)` · โดนไล่ออก `move(fr(760,1060,1.0,540,1000), fr(640,1020,1.5,440,980), F("a05",0,1)-0.05, 0.14)` |
| `JKC.impact(at, dur, amp, extra?)` | กระแทก ตกพื้น | `shake: JKC.impact(1.6, 0.55, 16, JKC.dutch(5))` |
| `JKC.dutch(deg)` | เอียง (ใช้ร่วมกับ impact เท่านั้น — ไม่ใช้ในช็อตพูด) | |
| `JKC.hand(amp, roll)` | มือถือสั่น (ผู้ใช้ไม่ชอบในช็อตพูด; ใช้เฉพาะวิ่ง/วุ่นวาย) | |
| `JKC.whipOut(tl,id,at,dir)` / `whipIn` | วิปแพนเข้าเหตุการณ์ (ใส่ท้ายช็อตก่อน + ต้นช็อตถัดไป) | a06→a07 ตกท่อ |
| `JKC.rack(tl, L, at, fromBlur, toBlur, dur)` | โฟกัสเบลอ→ชัด ตอนตื่น | `rack(tl,L,t0+0.4,{act:9,far:6,mid:6},{act:0,far:2,mid:1},0.8)` |
| `JKC.ots(L, {side,color,hair})` | ข้ามไหล่ตอนคุย | a12 |
| `JKC.back(L, {color,s})` | หลังหัวตอนอ่านป้าย | a19 |
| `JKC.bars(tl, L, at, dur, h)` | แถบดำตอนร่วง/ฉากใหญ่ | a18, c13, d12 |
| `JKC.bucketPOV(L)` + `shake: JKC.pov(7,4.5)` | สายตาลอดถัง (มุก) | c08 — เอาตัวเอกออกจาก actors |
| `JKC.shaftPOV` `JKC.topdownTown` | มี แต่ **ผู้ใช้ไม่เอา** (ตกท่อให้ตกเฉยๆ · ไม่เอามุมจากฟ้า) | |
| ค่ายึด: `camAt: ... push: 0.01–0.03` | ช็อตนิ่ง + push-in ช้าๆ | ทุกช็อตพูดคุย |

ลำดับที่ดี (EP.1 แบบ A): เครนเปิด → ยืนขายของ (นิ่ง) → ซูมฉับโดนไล่ออก → เดินอ่านหนังสือ (นิ่ง drift x) → วิปแพน → ตกท่อ (impact+dutch + เฟดดำ) → ตื่นบนเมฆ (rack) → เครนบนเมฆ → แถวสุ่ม (นิ่ง) → ซูมฉับได้การ์ด → ข้ามไหล่ → การ์ดใกล้ → ซูมฉับโดนหัวเราะ → นิ่ง → แถบดำร่วงลงเมือง → หลังหัวอ่านกระดาน

## 5. ไอคอน (`jkicons.js` → `JKI`)
- `JKI.badge(tl, L.light, t0, dur, {kind, x, y, s, label, tone, at, end})` เหรียญเดี่ยว + ป้าย · `JKI.ring(... {x,y,s,from,to,at,rollAt,count,tone,label,labelAt})` วงแหวน % · `JKI.counter(... {icon,x:44,y:250,w,from,unit,at,steps:[[t,v]],tone,plus})` สติกเกอร์นับ · `JKI.chain(... [{icon,label,tone}], {y, gap, ats|at+step, s})` แถวเหรียญ+ลูกศร
- สัญลักษณ์ (`GLY`): percent believer bucket gecko monitor croc dragon crown … (ใส่ใหม่ในสไตล์เดียวกัน: ink L5 + กระดาษ + สีเน้นเล็กน้อย, มี `-tl` หาง `-wg` ปีก ให้ `idle()` ขยับ)
- การเข้า `enterC`: ซ่อนด้วย autoAlpha จนถึง `at` → พลิกเหรียญ scaleX .06→1.14 rot −40→6 (0.36 วิ) → เด้งกลับ elastic → แฟลช+ฮาโล+แสงวิ่ง+ประกาย 6+กระดาษสี 10 → แสงวิ่งทุก 2.8 วิ ถ้ามี `end` · ป้ายปั๊มเข้า back.out(3.2)
- ตำแหน่งแนวตั้ง: counter ซ้ายบนใต้แถบสถานะ (44,250) · ring กลาง (540,540) · chain ล่าง (y 1500) · badge ข้างหัว (840,420) · ในแนวนอนไลบรารีย้ายให้เอง (counter ≥ 330, chain −250)

## 6. HUD, คำบรรยาย, ป้าย
- แถบสถานะ `.sghud` ซ้ายบน (`hud(id, [[label, value, color], …])` / `hudN(tl,id,t0,rank,[[t,"86%"],…])`) · ป้ายตอน `.badge` ซ้ายล่าง · คำบรรยาย `.capwrap` top 1185 (แนวตั้ง) / 880 (แนวนอน) ฟอนต์ Kanit 54/46
- การ์ดกฎ/การ์ดสกิล: วาดใน `grp(L.light)` ที่ (540,720)/(540,560) + `pop()` · แว่นขยายส่องกฎข้อ 3 (clipPath) ใน a16
- สีประจำ: การ์ด F เทา #c8ccd4 · เหลือง #f2c55c · แดง #d8443a · น้ำเงิน #3a6aa8 · หมึก #2e2a26
