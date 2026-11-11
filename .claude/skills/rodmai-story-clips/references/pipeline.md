# ขั้นตอนทำจริง ทีละคำสั่ง (ทำตามได้เลย)

ตัวย่อ: `MW` = `<scratchpad>/mw` · `ST` = ชื่อย่อเรื่อง (จอมโกหก = `jk`) · โฟลเดอร์ตอน `MW/$ST/epN` · โปรเจกต์ HyperFrames `MW/hf/${ST}N` · สคริปต์ skill เดิม `R=.claude/skills/rodmai-club-video/scripts` · สคริปต์ skill นี้ `S=.claude/skills/rodmai-story-clips/scripts`

## ขั้น 0 · workspace
```bash
bash $R/setup_workspace.sh $MW                      # hf/lib hf/rig synth.py เพลง
cp video/jk-ep3/lib/*.js $MW/hf/lib/                # ไลบรารีชุดจอมโกหก (ใหม่กว่าชุดกลาง)
mkdir -p $MW/$ST && cp -r video/jk-ep1/production $MW/$ST/ep1 && cp video/jk-ep1/production/synth.py $MW/$ST/synth.py
cp video/jk-ep1/production/musicbed.py $MW/$ST/ && mkdir -p $MW/music/suno && cp video/jk-ep1/music/suno/*.mp3 $MW/music/suno/
cp $S/renderq.sh $S/mkland.py $S/qa_splice.py $MW/$ST/     # เครื่องมือประจำเรื่อง (renderq อ่าน ST จาก env)
```
`make.py` ของแต่ละตอนชี้ `PROJ = ../../hf/<proj>` และคัดลอก `hf/lib/*.js` เข้า `hf/<proj>/assets/` ทุกครั้งที่รัน → แก้ไลบรารีแล้ว **ต้อง build ใหม่ทุกตอนที่ได้รับผล**

## ขั้น 1 · เรื่องและบท
- **สูตรเรื่องมี 2 แบบ (เจ้าของ 6 พ.ย. 2569) เลือกตามที่เจ้าของสั่ง:**
  - **สูตร A ตลก (จอมโกหก/บางระจัน/ช่างเชื่อม):** ตัวเอกกาก ได้พลังพิลึก เรื่องบานปลายมุกต่อมุก · โครง 4 ตอนตามบรรทัดถัดไป
  - **สูตร B ลุ้น มีตัวร้าย (คนเดินดิน `video/stories/s4/TELL.md`):** ตัวเอกไม่มีพลัง แก้ปัญหาด้วยสมอง · ทุกตอน = ปัญหา→แก้→ปัญหาใหม่→แก้ (3–4 รอบ) → ค้างไว้ด้วยอันตราย · มีนาฬิกานับถอยหลัง (7 วัน) · ตัวร้ายที่คนทั้งเมืองเชื่อ · กฎ 4 ข้อที่ข้อสุดท้ายซ่อนไว้ใช้ตอนจบ · EP.1 ตั้งโลก+ปัญหา+ค้นพบภัย · EP.2 เตรียมรับมือทั้งที่ไม่มีใครเชื่อ · EP.3 ภัยมาจริง ช่วยทุกคน แล้วเผยตัวร้าย · EP.4 เอาชนะด้วยกฎข้อสุดท้าย
  - **สูตร C ผสม (`TELL_mix.md`):** โครงสูตร B แต่ทุกรอบปัญหามี "มุกจ่าย" 1 มุก + มุกวิ่ง 3 เส้น (หมาที่บินไม่ได้ ลุงแรงเท่าช้าง เลข 812 ขั้น) — เจ้าของขอดูเทียบ (6 พ.ย.) ยังไม่ได้เลือก
- โครง 4 ตอน (ตอนละ 60–80 วิ): EP.1 ฮุค+ตั้งกติกา (กฎ 3 ข้อ ข้อ 3 ตัวเล็กเป็นระเบิดเวลา) · EP.2 คนแรกที่เชื่อ · EP.3 ของโตขึ้นเป็นขั้น (จิ้งจก→ตะกวด→จระเข้→มังกรน้อย→มังกรเท่าตึก) · EP.4 หักมุม + คลี่กฎข้อ 3 + ค้างไว้สำหรับภาคต่อ
- `lines.json` = รายการ `{id, text, cap, voice?, style?}` · `cap` แบ่งด้วย " / " · `[เหลือง]` `{กล่องแดง}` · id ตั้งตามย่อหน้า (`p03_2`) ฮุคใช้ `j1h`
- ตรวจคำที่เป็นภาพทุกคำ (grep "หัว" "สี" "ตัวเท่า") ว่าฉาก/ตัวละครจะวาดตรง

## ขั้น 2 · เสียงและจังหวะ
```bash
cd $MW/$ST/ep1 && python3 ../../hf/lib/voice.py lines.json vo        # fal gemini-3.1-flash-tts · cache ตาม sha ของข้อความ (ไม่เสียซ้ำ)
python3 ../../hf/lib/voice_qa.py vo                                   # ถอดเสียงเทียบบท แก้คำอ่านผิดแล้วอัดเฉพาะบรรทัดนั้น (เปลี่ยน take)
python3 timing.py                                                     # → schedule.json (ช็อต เวลาเริ่ม ความยาว fragments ของคำบรรยาย)
```
`timing.py`: แต่ละช็อตระบุบรรทัดเสียง `"p03_2"` หรือ `("p03_2", gap)` · `pre/post/min` ต่อช็อต · ฮุคยาว 3.0 วิพอดี

## ขั้น 3 · ภาพ (ทำทุกช็อตใน `body_shots.part`)
ไฟล์ประกอบหน้า: `head.part` (CSS, fr, caps) + `sigcard.part` + `helpers.part` + `body_head.part` (helpers ของเรื่อง: DAY/NIGHT, shot(), hud, chip, ME/A/KID, acting) + `body_shots.part` (ช็อต) + `foot.part`
```bash
cd $MW/$ST/ep1
python3 -c "open('body.part','w').write(open('body_head.part').read()+'\n'+open('body_shots.part').read())"
cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py
(cd ../../hf/${ST}1 && nohup python3 -m http.server 8773 >/dev/null 2>&1 &)      # เสิร์ฟหน้า
node $S/snapq.cjs 8773 "" snap/a05.png 12.9                                      # 1 เฟรม ณ เวลา (วินาทีของทั้งตอน)
python3 $S/sheetL.py 8773 schedule.json sheet.jpg                                 # ใช้กับแนวตั้งได้: ส่ง w h ให้ snapq ใน sheetL ถ้าต้องการ
```
สั่งทำช็อต: `shot("a05", { ...city("a05"), camAt: fr(...) | cam: JKC.move(...), push, shake, dark, grade, blur, actors: [...], sfxText, captions, extra(L), fx(tl,id,t0,L) })` — ดูความหมายทุกฟิลด์ใน `look-camera-icons.md`
กฎตรวจภาพนิ่งก่อนส่ง: ทุกช็อตมี 1 เฟรม + ช็อตที่กล้องขยับมี 3 เฟรม (ต้น กลาง ท้าย) · ดูทีละใบว่า ใครอยู่ตรงไหน หน้าใคร ป้าย/ไอคอนอ่านออก ไม่ทับคำบรรยาย ไม่ทะลุเฟอร์นิเจอร์ แสงไม่กลบ

## ขั้น 4 · มิกซ์ เรนเดอร์ QA ส่ง
```bash
cd $MW/$ST/ep1 && python3 mix.py                      # sfx_cues.json → synth.py → sfx.wav · musicbed → mix.wav (−14 LUFS)
cd $MW/$ST && ST=$ST bash renderq.sh 1                # ← สั่งเป็น background task (timeout 7200000) · ได้ ep1/EP1-<name>-HQ.mp4 + -share.mp4
cd ep1 && bash $R/qa_video.sh EP1-<name>-HQ.mp4 mix.wav
python3 ../qa_splice.py EP1-<name>-HQ.mp4 EP1.qa_splice.jpg a02 a05 a07 a11 a18    # ช็อตที่มีกล้อง/แก้
node $S/blackscan.cjs 8773 scan/ep1 && python3 - <<'EOF'
from PIL import Image
rows=[l.split() for l in open('scan/ep1/list.txt')]; flag=[]
for cid,t,f in rows:
    im=Image.open(f).convert('RGB').resize((270,370)); px=im.load()
    n=sum(1 for x in range(270) for y in range(370) if max(px[x,y])<=3); frac=n/(270*370)
    if 0.0005<frac<0.5: flag.append((cid,t,round(frac*100,2)))
print('flagged', flag)   # ไปดูเฟรมที่ถูก flag ด้วยตา (แถบดำ/เฟดดำที่ตั้งใจจะโผล่ด้วย)
EOF
python3 -I $S/hiss.py mix.wav vo/*.wav
```
ปก: โปรเจกต์ `cover/` ของตอน (parts + `foot.part` มีตัวแปร `?v=mitr` เลือกฟอนต์) จับด้วย snapq ที่ 1080×1920 → `cover.jpg` · ฟอนต์ Mitr ขอบดำ อ่านออกตอนย่อเล็ก ตัวเอกซ้าย การ์ด/ของสำคัญกลาง ตัวหนังสือขวา
`CAPTIONS.md`: ชื่อคลิป (ของกาก/ตลก + ชื่อเรื่อง + EP) · คำอธิบาย (ฮุค 1 บรรทัด, เรื่องย่อ 3 บรรทัด, ปริศนาชวนคอมเมนต์, CTA ดูเรื่องเต็ม YouTube, แฮชแท็ก) · คอมเมนต์ปักหมุด · "เรื่องและตัวละครเป็นเรื่องสมมติ"
ส่งไฟล์ HQ ทันทีที่ผ่าน QA แล้วรอความเห็น · แก้ → ภาพนิ่งช็อตที่แก้ → เรนเดอร์ใหม่ (ตอนที่ไลบรารีร่วมเปลี่ยน ต้องเรนเดอร์ใหม่ทุกตอน และสแกนกล่องดำทุกหน้า)

## ขั้น 5 · ตอนยาว 16:9 (รายละเอียดใน `landscape-and-longcut.md`)
```bash
cd $MW/$ST && for p in "ep1 ${ST}1" "ep2 ${ST}2" "ep3 ${ST}3" "ep4 ${ST}4"; do set -- $p; python3 mkland.py $1 $2; (cd $1L && python3 -c "open('body.part','w').write(open('body_head.part').read()+'\n'+open('body_shots.part').read())" && cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py); done
(cd ../hf/${ST}1L && nohup python3 -m http.server 8782 >/dev/null 2>&1 &) ; python3 $S/sheetL.py 8782 ep1L/schedule.json ep1L/sheet1.jpg   # ดูทุกช็อต แก้ด้วย LAND_ADJ ถ้าช็อตไหนเพี้ยน
ST=$ST bash renderq.sh 1L 2L    # background task · แล้ว 3L 4L อีก task
python3 $S/long169L.py long_plan.json     # plan: parts ของ ep1L..ep4L (from/to ตัดฮุค+การ์ดท้าย) xfade 0.2 out LONG-<name>-16x9.mp4
bash $R/qa_video.sh LONG-<name>-16x9.mp4 "" 16 ; ffmpeg -ss <รอยต่อ±0.2> …   # ดูเฟรมรอยต่อ + ช็อตเด่นทุกตอน
ffmpeg -i LONG-<name>-16x9.mp4 -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 160k -movflags +faststart LONG-<name>-16x9-share.mp4   # ≤ 95 MB สำหรับ repo
```
ปก 16:9: โปรเจกต์ `cover169/` (head.part แนวนอน, CAM `fr(610,838,2.8,420,500)`, คอลัมน์ขวา title/pill) → `LONG-<name>-thumb.jpg` · `YOUTUBE.md` ใส่เวลาแบ่งตอนที่ `long169L.py` พิมพ์

## ขั้น 6 · เก็บเข้า repo
```bash
bash $R/store.sh $MW/$ST/ep1 $MW/hf/${ST}1 ${ST}-ep1 EP1-<name>     # ทำทุกตอน (ตอนที่มีหลายแบบ เก็บแบบที่ผู้ใช้เลือก)
cp $MW/$ST/ep1/{cover.jpg,CAPTIONS.md,mix.py,sfx_cues.json,musicbed.py} video/${ST}-ep1/production/ ; cp $MW/$ST/synth.py video/${ST}-ep1/production/
mkdir -p video/${ST}-long/production && cp LONG-<name>-16x9-share.mp4 LONG-<name>-thumb.jpg YOUTUBE.md video/${ST}-long/ && cp long_plan.json $S/long169L.py $S/mkland.py $S/renderq.sh video/${ST}-long/production/ && cp -r cover169 video/${ST}-long/production/
# video/release/<ST>.json: series, rules, episodes[{id,order,title,status final|archive,video_hq,video_repo,cover,caption,pinned_comment,hashtags,sha256,bytes}], youtube_long{…,chapters}
git add video/${ST}-ep* video/release && git commit -F msg.txt && git push -u origin <branch>
```
commit ทีละก้อนที่สมบูรณ์ (ตอนที่ผ่าน QA แล้ว) · ข้อความ commit ไม่มีชื่อโมเดล · ไฟล์ > 95 MB ไม่เข้า repo

## บทเรียนจากเรื่องที่ 2 · บางระจัน แบต 3% (5 พ.ย. 2569)
- **เสียงเล่าต้องเป็น Enceladus** ทุกเรื่องของช่อง (เจ้าของทักทันทีเมื่อใช้ Puck): ใส่ `"voice": "Enceladus"` ทุกบรรทัดใน `lines.json` เพราะ `voice.py` default เป็น Puck · บรรทัดตัวละครอื่น (เช่น ผู้ช่วยในมือถือ) ใส่ voice/style ของตัวเองได้
- **TTS อ่านคำสั่ง style ออกมาด้วย** เมื่อบรรทัดสั้น (ไฟล์ยาว 6–12 วิทั้งที่บทมี 2 วิ): `voice_qa.py` จับได้ (LONG BAD) แต่อัดซ้ำก็ไม่หาย → ตัดเอาเฉพาะวรรคท้ายด้วย `autotrim.py <ep>` (หรือ `trimvo.py <ep> <id> <วินาที>`) ก่อนรัน `timing.py`
- ซับ 1 ท่อนยาวได้ไม่เกิน ~38 ตัวอักษร (58px) ไม่อย่างนั้นล้นจอทั้งสองข้าง (ไม่มีการตัดบรรทัด) → แยกท่อนด้วย " / " · และ `voice_qa.py --fix` เขียน `lines.json` ทับตอนจบ ถ้าแก้ cap ระหว่างที่มันรันอยู่ต้องแก้ใหม่
- คลิปสั้น ≤ 90 วิ: ถ้าเสียงรวมเกิน ลดท้ายช็อตใน `timing.py` ตัดบรรทัดสีสัน 1 บรรทัด และ/หรือ `atempo=1.05` ทั้งตอน (ยังฟังเป็นธรรมชาติ)
- ไฟล์ช่วยของเรื่องใช้ร่วมทุกตอน: `common.part` (look/ฉาก/prop/phone UI) → ต่อหน้าด้วย `scripts/build.sh <epN|epNL|cover>` (body = body_head + ../common.part + body_shots; ข้าม timing.py เมื่อไม่มี vo/)
- GSAP บน `<g>` ที่มี `transform="translate(x,y)"` อยู่แล้ว: `x`/`y` ใน tween เป็นค่าสัมบูรณ์ (แทนที่ translate เดิม) ไม่ใช่บวกเพิ่ม → ใส่ค่าตำแหน่งจริงเสมอ (หัวควายตกพื้น/ควายยักษ์หาย เพราะเรื่องนี้) · อย่า tween `x` บนกลุ่มนักแสดงที่ flip (scale ติดลบ) จะพัง ให้ใส่การสั่นในท่าแทน
- ท่าแขนของ rig: ทั้งสองแขนหมุนทางเดียวกัน (ลบ = ไปข้างหน้า) ไม่ได้กลับด้าน → "กอดอก" ที่อ่านออกคือ `foldX` (uaF −26 / faF +128, uaB +30 / faB −128) ส่วน `fold` เดิมได้แขนกางเป็นตัว V · มัดติดเสา = แขนแนบตัว (6/4) · นั่งกอดเข่า = bodyY 288 ต้นขา −150 หน้าแข้ง +150 · หมอบกราบ = เข่าติดพื้น bodyY 150 ลำตัว 52
- ของที่ต้องยืนตรงกับฉากหลัง (คนยืนในประตู ข้าศึกหลังรั้ว) ต้องอยู่ชั้น parallax เดียวกัน (set=act=1): `brRoom {doorFront}` · `brCamp {enemy, fenceFront}` (รั้ว+เงาข้าศึกย้ายมาชั้น set) · พุ่มไม้ที่เด็กโผล่ออกมา = วาดสำเนาพุ่มไม้ใน `fx` (L.act ทับนักแสดง) ไม่ใช่ fg (parallax 1.5 เลื่อนไม่ตรง)
- `F(k,i,j)` clamp j ไว้ที่ท่อนสุดท้าย (ใน head.part และ mix.py) ไม่งั้นท่อนเดียวแต่เรียก j=1 ได้ NaN เงียบๆ · ใน mix.py `D` เป็น dict (`D["e14"]`)
- sheet อ่านง่าย: `sheet9.py <port> <schedule> <prefix> [key=frac …]` (3×3 ช่อง 360×640, 3 เบราว์เซอร์พร้อมกัน) · ปกใช้โปรเจกต์ `cover/` (x01=EP.1, x02=EP.2 เลือกข้อความด้วย `?ep=`) และ `cover169/` (head ของฝาแฝดแนวนอน; ค่ากล้องเขียนแบบแนวตั้งแล้ว head แปลงให้ sx×1.78 sy×0.56 s×0.75)
- แผนตอนยาวเขียนเป็นคีย์ช็อต (`long_plan.tmpl.json`: `"START:c02"`) แล้ว `mkplan.py` เติมเวลาจาก schedule ของฝาแฝดแนวนอน → ไม่ต้องจดเลขใหม่ทุกครั้งที่จังหวะเสียงเปลี่ยน
- ตอนที่ 3–4 ไม่ต้องเรนเดอร์แนวตั้ง (ไม่ลงเป็นคลิปสั้น) เรนเดอร์เฉพาะฝาแฝดแนวนอนสำหรับตอนยาว ประหยัด ~1.5 ชม.

## บทเรียนจากเรื่องที่ 3 · ช่างเชื่อมสายฟ้า (6 พ.ย. 2569)
- **พารัลแลกซ์ของกล้อง (สูตรจริงใน engine.js):** ชั้น p (far .25 mid .6 set/act 1 fg 1.5) วาดด้วย `translate(CX,CY) scale(1+(s-1)p) translate(-CX - x·p, -CY - y·p)` เมื่อ (x,y,s) คือค่ากล้องที่ `fr(wx,wy,s,sx,sy)` คืน (`x = wx-CX-(sx-CX)/s`) → จุดโลกในชั้น set เท่านั้นที่ไปโผล่ที่ (sx,sy) ตรงๆ ของอื่นในชั้น mid/far เลื่อนไปตาม p · ของที่กล้องต้อง "ใส่กรอบ" (ประตูที่แปะรูป ป้ายร้าน หม้อแปลง) ให้วาดในชั้น set (option ของฉาก เช่น `o.drawing` ย้ายประตูมาชั้น set) หรือใช้การ์ด screen-space แทนการพุชไปหาของในชั้น far
- **วัดตำแหน่งจริงของ prop ก่อนวางเอฟเฟกต์:** `node scripts/probe_pt.cjs <port> "" <t> "#s8-a2 .ltArc,#s8-a2" [js ก่อน seek]` คืนพิกัดโลก (ชั้น act/set) ของ bbox → ใช้หาปลายหัวเชื่อม/มือ แล้วลองมุมแขนทีละชุดผ่านอาร์กิวเมนต์ที่ 5 (`Rig.MODES.weld=(u,o)=>({...})`) จนปลายตรงจุดเชื่อม (ไม่ต้อง rebuild)
- **แสงเรืองรอบตัว (aura) ต้องอยู่ใต้ตัวละคร:** `grp(L.set)` ไม่ใช่ `L.glow` (ชั้น glow อยู่เหนือ act → ตัวละครซีดโปร่งเหมือนผี) · ใช้ gradient อ่อน (`ltAura`) และ r ≤ 340 ในช็อตใกล้
- **ป้าย/แท็กในโลก (tagAt) ขยายตามกล้อง:** ช็อตใกล้ (s ≥ 2.4) ใช้ `s: 0.45` ช็อตกว้าง (s ≤ 0.6) ใช้ `s: 2–2.6` ไม่งั้นป้ายล้นเฟรมหรือเล็กจนอ่านไม่ออก
- **ไฟดับ/ไฟติดทั้งฉาก:** รวมแสงทุกดวงไว้ในกลุ่ม `#<setid>-lamps`/`-lights` (รวม cone ของ JKD.dress ด้วย: `put(document.getElementById(`${id}-lights`) || L.glow, …)`) → `blackout()`/`lightsBack()` สลับได้ด้วยคำสั่งเดียว + ย้อมหน้าต่าง `.ltWin` ผ่าน `attr.fill`
- **ฝาตู้/ประตูที่ต้องเปิด:** ฝา = `<g id="…-lid">` → `scaleX:-1, transformOrigin:"0% 50%"` และวาดด้านหลังไว้ใน `.ltLidBack` ที่ pre-mirror ด้วย `transform="scale(-1,1)"` (ไม่งั้นตัวหนังสือกลับด้าน) · บานประตู `#…-leaf` → `scaleX:0.12, transformOrigin:"100% 50%"` อ่านเป็นเปิดเข้าใน
- **split() ต้องห่อด้วย spec():** `split(k, at, spec(k,{camAt…}), spec(k,{…}))` ไม่งั้น `camAt/push` ไม่ถูกแปลงเป็น `cam` (ช็อตครึ่งแรกกลายเป็นมุมกว้าง)
- **A(who,x,y,s,track,extra) ต้องมี s เสมอ** (ลืมแล้วได้ `scale([object Object])` + PAGEERROR) · ME() เติม 0.95 ให้
- **เสียง:** `autotrim.py` เรียกด้วยพาธถูกต้อง (`$MW/../autotrim.py` = scratchpad) · ถ้าตัดผิด (whisper ได้คำเดียว) ให้ listing ช่องเงียบของ `.full.wav` แล้ว `ffmpeg -ss <หลังช่องเงียบใหญ่>` ตรวจซ้ำด้วย voice_qa บนโฟลเดอร์ชั่วคราวที่มี lines.json เฉพาะบรรทัดนั้น · อัดใหม่ (take+1) อาจอ่าน style ซ้ำอีก ตัดจากไฟล์เดิมเร็วกว่า
- **ตรวจเฟรมดำจากหน้าเว็บ ไม่ใช่จากวิดีโอ:** `node blackscan.cjs <port> <outdir>` แล้วนับด้วย numpy (`(r<6)&(g<6)&(b<6)` ในแถบ y 300–1500) — การนับผ่าน `getdata()` ให้ค่าคงที่ 21600 ปลอมทุกเฟรม
- ใช้ `sheetL.py <port> <schedule> <out.jpg>` (ต้องมีนามสกุล) · เวลาจับภาพพร้อมกับเรนเดอร์ 3 worker ช้าลง ~2 เท่า แต่ทำได้
- ฉากใหม่ของเรื่องนี้ (ใช้ซ้ำได้): `ltShop` ซอย/ร้านเหล็กดัด (time day|storm|dusk|night · table/tableX · banana · puddle · rain) · `ltRoof` ดาดฟ้า+โครงป้าย (เชื่อมที่ POST 760) · `ltWard` หอผู้ป่วย/ห้องเด็กอ่อน (nursery · blackout · drawing) · `ltRoom` ทางเดินห้องเช่า (doorFront · ตู้ไฟ #…-box) · `ltSky` ทั้งเขตจากปากซอย (blackout · storm) · helpers ใน `common.part`: arc strike zapLine aura hairSparks phone100 blackout lightsBack lidCard
- **กติกาเสียงจากเจ้าของ (6 พ.ย. 2569):** ห้ามใส่เสียงลม (`wind`) เสียงฝน (`rain`) และเสียงสติงตลก (`trumpet`) ในมิกซ์ — "มันรำคาญ" · ฟ้าร้อง/ฟ้าผ่า (`thunder`/`strike`) ใช้ได้ตามเรื่อง · ถ้าแก้แต่เสียง ไม่ต้องเรนเดอร์ใหม่: `ffmpeg -i HQ.mp4 -i mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac` (ทำทั้ง HQ และ share)
- **กติกาบทจากเจ้าของ (6 พ.ย. 2569): "แต่งเรื่องมาให้ผมอ่านก่อน"** — ก่อนลงมือผลิต ส่งเนื้อเรื่องฉบับอ่าน (ทั้ง 4 ตอน เล่าเป็นเส้นตรง เหตุ→ผล) ให้เจ้าของอนุมัติก่อนเสมอ · เจ้าของทัก EP.2 ของเรื่องที่ 3 ว่า "งง" เพราะฮุกสัญญาเรื่องคิวชาร์จแต่ไปเล่าเฮียกิม+กฎ 3 ข้อ+ย้อน 40 ปีอยู่ 40 วิก่อนถึงคิว → แก้เป็นลำดับเส้นตรง ฮุก→จ่ายผลฮุกทันที→ปัญหา→ที่ปรึกษา→กฎ→วันต่อมา→ใช้กฎ→มุกจบ และตัดกฎที่ไม่ได้ใช้ในตอนออก (ใส่บรรทัดเชื่อมใหม่ 1 บรรทัด "วันต่อมา…" อัดเพิ่ม)
- **ปกแบบมืออาชีพ (เจ้าของสั่ง 6 พ.ย. 2569) — ใช้กับทุกเรื่องต่อจากนี้:** ตัวละครใหญ่ (กล้องใกล้ `face(x,1400,1.8–1.9)` ให้หัวอยู่ ~y 820) · ข้อความ 2 บรรทัดเท่านั้น (บรรทัด 1 ขาว 104px, บรรทัด 2 สีประจำเรื่อง 170px เอียง −2° ขอบดำ 28px) ใส่ `|` ในข้อความเพื่อตัดบรรทัดเอง (ห้ามปล่อยให้คำไทยถูกตัดกลางคำ) · ป้ายชื่อเรื่องเล็กมุมบนซ้าย + พิล EP แดง · ไล่เงาดำจากล่าง (แนวนอน: จากขวา) · **สีตัวหนังสือตามเรื่อง**: จอมโกหก ทอง #ffd84a · บางระจัน เขียวแบต #9dff6a · ช่างเชื่อม ฟ้าสายฟ้า #8ae8ff (เรื่องใหม่เลือกสีจากของสำคัญในเรื่อง) · บล็อก overlay อยู่ใน `cover/foot.part` ("PRO cover overlay") ของแต่ละเรื่อง · ปกจากเฟรมของตอน (ไม่มีโปรเจกต์ปก): `scripts/framecap.cjs <port> <t> out.png` (ซ่อนซับ/HUD/ป้าย) แล้วประกอบกับ overlay ใน HTML (ตัวอย่าง `video/jk-long/production/cover/jk2_cover_pro.html`)
- **ภาพประจำตัวช่อง:** `lt/avatar/avatar.html` (4 แบบ: หน้าตกใจผมตั้งบนเหลือง / +ชื่อ / โมโนแกรม S สายฟ้า / วงกลมขอบดำ) จับภาพ 1024×1024 ด้วย Playwright

## ลุคภาพ AI (6 พ.ย. 2569)
เจ้าของดูเทสต์ฟิลเตอร์แสงเงาแล้วบอก "มันไม่เหมือนในภาพ" → ทางที่ผ่านคือวาดทุกเฟรมด้วย fal (สไตล์รูปต้นแบบ) แล้วขยับในเอนจินเดิม ดู `ai-art.md` ทั้งไฟล์ก่อนเริ่มเรื่องใหม่ในลุคนี้ · งานแรก `video/jk-ep1-ai/`

## บทเรียนจากเรื่องที่ 4 · คนเดินดิน EP.1 (6 พ.ย. 2569 · สูตร B ลุ้น)
- โค้ดเรื่อง: `video/fl-ep1/production` (`common.part` looks/wrappers city/room/klass + helpers FLY/trailAt/ringDim/dogLife/card/arc) · ไลบรารี `flset.js` (flCity: เมืองตึกสูง วงแหวนทอง รังบิน บันไดเหล็ก จอยักษ์ เวที · flRoom · flClass) · `flcast.js` (ตัวละคร + ท่าบิน fly/hover/hang/pulley/dangle/clap/spray/scope/floatPoint + FL.DOG) · `flicons.js` (ring zero stairs scope graph days7 dog captain nofeet tea)
- **บทยาวเกิน:** Enceladus อ่านช้ากว่าที่คิด 21 บรรทัด = 126 วิ → ตัดเหลือ 15 บรรทัด + `tempo: 1.08` ได้ 83.6 วิ → ตอน 95.8 วิ (ยังยาวกว่า 90) ครั้งหน้าเขียนบท ≤ 14 บรรทัด ≈ 75 วิ
- **ห้าม tween `x/y` ด้วย GSAP บนกลุ่มนักแสดง `#id-aN`** (เอนจินตั้ง transform attribute เอง → GSAP ทับ y เป็นค่า tween ตัวละครหายไปข้างบน) ให้ใช้ mode ที่มี bodyY (เช่น `floatPoint`) หรือ `path`
- ท่าบิน: `rootR` หมุนรอบเท้า (+74 = หัวไปทางที่หัน) · บินขึ้นใช้ `ang: 0` ใน track · ห้อยหัว `hang` = rootR 180 วาง y ของนักแสดง = y หัวที่ต้องการ − 520·s
- ตัวละครในจอยักษ์: `Rig.build(groupในฉาก, id, Rig.CAST.x)` แล้ว `Rig.drive(tl, id, t0, dur, track, blinks)` ใน fx ได้ (ไม่ต้องอยู่ใน actors)
- ของที่ครอบด้วย `grp(L.act)` ก่อน actors จะอยู่ใต้ตัวละคร (หมา ป้าย) · ป้าย badge อย่าวางทับตัวละครเล็ก (หมาโดน badge บัง → ย้าย badge ไปมุมซ้าย)
- ฉากเมืองตึกสูง: ตึกไกลอย่าสูงเต็มจอ (top −300…−1700) ไม่งั้นฮุกไม่มีท้องฟ้า · ช่องบินวงกลมใส่น้อย (r()>0.95) สีน้ำเงินเข้มขอบทอง ไม่ใช่จุดดำ · วงแหวนที่ต้องเห็นในช็อตใส่ `ringNear` ในชั้น set (ของในชั้น far เฟรมไม่ได้)
- สคริปต์ตรวจ error ต้องซ่อน clip ที่ไม่ active (`pageerr2.cjs` ใน scratchpad) · ปก: โปรเจกต์ `cover/` ใช้ overlay PRO สี #ffa33c (ส้ม) ของเรื่องนี้

## บทเรียนจากเรื่องที่ 5 · สกิลจอมโกหก v2 — บทใหม่ของเจ้าของ ลุค 3D เทียม (11 พ.ย. 2569)
- โค้ด: `video/jk-v2/` (`lib/jk3d.js` ฉาก 3D เทียม · `production/common.part` looks/AT/ตา v3/ดาบแสง/หู/หลอดความเชื่อ · `production/ep1/` ช็อต k01–k13 · `production/cover/`) · บท `video/stories/s1/TELL_v2_owner.md` · ผลศึกษาคลิปอ้างอิง "The Ancient Jar" อยู่ใน journal ของ workflow (สรุป: ทุกฉากมีโครงสร้างจุดรวมสายตา, แสงสว่างที่ VP, ชั้นไกลจางลง, โคลสอัพมี DOF, โทนสีสดคู่ส้ม-ฟ้า)
- **ฉาก 3D เทียม (`jk3d.js`)**: one-point perspective VP (540,740) พื้น y 1400 D 2.2 · `J3.proj(x,y,z)→[sx,sy,k]` `J3.floorY(z)` `J3.scale(z)` · ฉาก j3Square (ลานหน้ากิลด์: facade ประตูใหญ่ หอคอย กระดานอันดับ เสาคบไฟ ไทยมุงเงา · `time: gold|mauve|dusk|night|doom`) j3Hall j3Cloud (ตู้กาชา เชือกกั้น เคาน์เตอร์ act-front หลุมเมฆ `#id-hole` แสงทอง `#id-burst` ผ่าน `o.gachaX/Z counterX/Z posts hole`) j3Street (ร้านประกัน ฝาท่อ) · วางตัวละครตามความลึกด้วย `AT(who, x, z, track, extra)` ใน common.part (ย่อขนาดตาม k)
- **โทนสีตามรูปของเจ้าของ (11 พ.ย.)**: `time: "mauve"` = ฟ้าไล่ม่วง→ชมพู→พีช ดวงอาทิตย์ซ้ายบน หมอกชมพู (`j3HazeM`) พื้นย้อมม่วง multiply .2 + look `MAUVE` (rim #ffd0b0 จากซ้าย grade ชมพู→ม่วงเข้ม op .2) · ผิวตัวเอก #e8a070
- **ตาตัวละคร v3 (เจ้าของสั่ง "ตาไม่มีตาขาว มีแค่จุด")**: `bigFaces()` ใน common.part แทน `Sig.sigFaces` ของทุกตัวที่ชื่อขึ้นต้น jk — ตาขาวกลม r 9.4 ตาดำกลม r 4–4.8 มีแสงสะท้อน คิ้วหนาโค้ง 5.0–5.4 ปาก o/scream ข้างในแดงเข้ม + ลิ้น · แว่นของตัวเอกวาดเองใน `headTop` (ขอบ 3.4 r 11.6 มีประกายเลนส์) · แรเงาหัว `SHADE` (gradient `v3Shade` ขอบล่างขวาเข้ม ไฮไลต์บนซ้าย rim อุ่นขอบขวา) ใส่หน้าทุก variant ของตา · เจ้าของส่งรูป 3D เป็นต้นแบบ → บอกตรงๆ ว่าริกแบน "คล้าย" ไม่ "เหมือน" (ส่งภาพเทียบข้างกัน)
- **ดาบจี้คอให้อ่านออก**: เคน `lunge` (uaF −48) + ดาบแสง `LSWORD(−22)` ในมือหน้า · ตัวเอก `kneelUp` (bodyY 216 มือชูสองข้าง) · ความสูงมือเคน = คอของคนคุกเข่า → ปรับมุมแขน ไม่ใช่ขยับดาบ · สองช็อตแรก: two-shot ระดับคอ → โคลสอัพหน้า (ดาบใต้คาง) → ไวด์ → ข้ามไหล่ (เงาไหล่เคนใน L.light เบลอ) → หู ECU + ป้าย "ไฟเบรก" กะพริบซิงก์กับหู (`brakeBadge`) → กรอกลับ (◀◀ + เส้นสแกน + whipOut)
- **กล้อง `cam.keys`**: คีย์ที่มี `glide: g` เคลื่อนช่วง [t−g, t] (จบที่ t) ไม่ใช่เริ่มที่ t · คีย์ไม่มี glide = ตัดภาพทันที · อย่าใส่ `drift` กับ `glide` ในคีย์เดียวกัน (ไม่ขยับ) · `split(k, at, A, B)` ต้องห่อด้วย `spec(k, …)` เอง ไม่งั้นไม่มีกล้อง/ไม่มี look (เห็นเป็นมุมเดิม scale 1)
- **ภาพนิ่งจาก Playwright หลอกได้**: ซีกแรกหลังโหลดหน้า ~1 วิแรกเฟรมมืด/มีก้อนสีน้ำเงินทับ (ยังไม่ raster) ไม่ใช่บั๊กของฉาก — เรนเดอร์จริงไม่มี (เช็กด้วย hyperframes 3 วิแรกแล้ว) · `snapt.cjs` ซีกสองรอบ (450 ms) แล้วค่อยถ่าย · ถ้าสงสัยใช้ `settle.cjs`/`hidetest.cjs`/`layerprobe3.cjs`/`probe_tf.cjs` (scratchpad)
- **แขนต้องติดตัว (เจ้าของ 11 พ.ย.: "แขนอย่าให้หลุดออกจากตัว")**: ท่ายกมือห้ามชี้แขนขึ้นตรงหรือขึ้น-หน้าชัน (uaF −124) เพราะต้นแขนถูกหัวบังแล้วดูเหมือนแขนงอกจากหัว → ใช้ต้นแขนยื่นไปหน้าระดับไหล่ + ปลายแขนพับขึ้น (`kneelUp`: uaF −95 faF −75 · แขนหลัง uaB +85 faB +80) · **แขนหลังใช้เครื่องหมายกลับด้าน** (บวก = ไปข้างหน้า) ส่วนแขนหน้า ลบ = ไปข้างหน้า และปลายแขน ลบ = พับไปทางเดียวกับต้นแขน · ทดสอบท่าด้วยโปรเจกต์เล็ก `production/armtest/` (คู่ละช็อต กล้อง 1.7 ดูชัดกว่าเรียง 4 คู่ในเฟรมเดียว)
- `earBlink(..., p, dy)`: ตัวที่คุกเข่าต้องส่ง `dy = bodyY` ไม่งั้นแสงแดงลอยอยู่ที่ความสูงหัวตอนยืน · แคปซูล/ของเล็กที่กลิ้งผ่านหน้าฉาก วางใน `grp(L.glow)` (อยู่เหนือทุกชั้นของ world) ถ้าใน L.act มันหายหลังฉาก
- ซับ: ท่อนละ ≤ 30 ตัวอักษร (ตัด " / " ใน `cap`) · ท่อนที่เป็นเสียงเอฟเฟกต์ ("ตุ้บ!") ซ้ำกับ sfxText → กรองออกจาก `caps(k)` ด้วย `.filter`
- เรนเดอร์ต้องสั่งผ่าน Bash `run_in_background: true` (timeout 30 นาที) — `nohup … &` ในคำสั่งธรรมดาถูกฆ่าทันทีที่คำสั่งจบ ("render_cancelled_parent_exited")
- การ์ดท้ายตอน `NkV.chalkEnd` บรรทัด q ยาวได้ ~12 ตัวอักษร (ตัวใหญ่) ไม่งั้นล้นสองข้าง
- แผนแบ่งตอนจาก workflow (ใช้ตอนทำ EP.2–4): EP.1 องก์ 1 (86 วิ) · EP.2 กระดานผู้กล้า+ความแตกเพราะหูแดง (~61 วิ ปิดที่ดาบจ่อคอ = เฟรมเดียวกับฉากเปิด) · EP.3 บทที่ 1 พูดความจริง + กฎข้อ 3 (~81 วิ) · EP.4 ที่เหลือ+ฉากแถม (~214 วิ ลง YouTube เท่านั้น หรือแบ่ง 5 ตอน)

## ลุค V · สกิลจอมโกหก v2 EP.1 ในลุคคลิปเก่า + แสงมีมิติ (11 พ.ย. 2569 — ลุคที่เจ้าของเลือกจริง)
ลำดับการตัดสินใจของเจ้าของในวันเดียว (อย่าทำซ้ำ): ส่ง EP.1 ลุค A (ฉาก AI) → "กลับไปทำแบบเดิม ไม่เอาแบบนี้" → "เอาแบบที่คุณเคยทำให้ผม ลองส่งเรื่องมาให้ผมดูก่อน" (= ส่ง **คลิป** เก่า ไม่ใช่บท) → "เอาคลิปนี้แหละ แต่ทำแสงให้มีมิติ แล้วเอาเรื่องใหม่มาทำแทนเนื้อเรื่องเก่า" → "เอาเสียงเดิม พูดน้ำเสียงแบบเดิม" → ดูภาพนิ่ง: "หูแดงไปปิดหน้าตัวละคร" · "ไม่เอาฟันแบบนี้"
- โค้ด `video/jk-v2/production/ep1V/` (hf โปรเจกต์ `hf/jk2V`): `body_head.part` = หัว ep1 (ไม่มี helper AI) · `../common.part` (ตา v3 ท่า kneelUp/lunge jkKenLS earBlink beliefBar BLACK) · `body_shots.part` ของ ep1V ทั้งหมด
- **ฉาก**: `jkTown` (`dusk: true` ฉากเปิด/การ์ดท้าย · `rows: ROWS` คำง่าย "เคน · ดาบแสง" ไม่มี "(SSR)" ของ default ใน jkset.js) · `jkCity {manhole}` · `jkCloud` — ตำแหน่งที่ทดสอบแล้ว: ลาน HX 700 (ตัวเอกคุกเข่า flip) KX 400 (เคน lunge) ไทยมุง y 1300–1340 s .72–.8 (x −20/40/1230/1290 ให้อยู่ในเฟรม) · ถนน YX 860 flip, ลูกค้า AX 600, เดินกับหนังสือ y 1520 จาก x 200 ถึงฝาท่อ 1180 (lip path ของ v1 a07) · เมฆ คิว −60/120/280/440(ตัวเอก)/590(เคน) เทพี 1262 หลังเคาน์เตอร์, ตู้ (820,860) คันโยก (650,1170) ปากราง (820,1292) หลุม cx 440 · ลูกบอลกลิ้งใน `grp(L.glow)` จาก (820,1292) ไป (550,1388)
- **แสงมีมิติ (ใน body_shots.part)**: look `*_V` = rim .85–.95 rimW 5 shade .3–.42 shadeW 30 + `cast {len 2.4–2.8, op .42, ao .4}` (เงาวงรีของเอนจินทุกตัว) และ `shadowsV` (NkL.cast เงาทอดจริง) · ทิศแสงต้องตรงกันทั้ง rim/เงา/ลำแสง: เมือง+สวรรค์ from "left" เงา sh +0.35–0.55, ถนน from "right" sh −0.5 · `DEPTH(L,{haze,far,mid,floorY,bokeh})` หมอกชั้นไกล/กลาง + พื้นมืดลงหาเลนส์ + โบเก้ขอบคม (vSoft2 blur 4, r 36–64, op .5) — บนเมฆใช้ far .06 (มากกว่านั้นกลบเมฆไกล) · `RAYS` = NkL.beams (src บน dst ล่าง เอียงตามทิศแสง) · `CITYLIGHT(tl,L,t0,dur)` แอ่งแสงโคม (420,1412) + หน้าต่างร้าน (1060,1424) op .55/.42 + ลำแสงโคม · `LANTERNS` แอ่งแสงโคมกิลด์ (670/1330, 1196) · `BLADE` แอ่งแสงฟ้าที่คอ/หน้า (อย่าวาดเส้นแสงดาบแยก — ดาบในมือมี halo อยู่แล้ว เส้นคงที่จะเป็น "ดาบสองเล่ม") · `earBlinkV` = earBlink แล้วย่อวง r 60·s และย้ายไป L.set (หลังหัว) · `earSpill` = วงรีแดงบนพื้นข้างตัวเท่านั้น · ระเบิดแสงตู้: วงหน้า r ≤ 380 เฟดออก + วงหลังใน L.set (ไม่ขาวทั้งเฟรม) · `vol` (feDiffuseLighting ของเอนจิน) ทดสอบแล้วแทบไม่เห็นต่าง ไม่ใช้
- **เสียง**: `voice.py` + สไตล์/tempo ของคลิป 5 พ.ย. (SKILL.md) → 11 บรรทัด 67.8 วิ ตอน 77.4 วิ · Gemini ตอบ 422 กับประโยครุนแรง ("ฟันคอขาด") → `production/tts_fill.py lines.json vo` ลองแบบเดิม → "..."→"," → "..."→" " → คำอ่อนลง แล้วเซฟ mp3 ชื่อตรง hash ให้ voice.py ตัดต่อ (ซับยังใช้คำเดิม)
- **รีวิวภาพนิ่งด้วย workflow** (4 เลนส์ แสง/องค์ประกอบ/ตัวละคร/บท + refute): แก้ 25 จุดก่อนเรนเดอร์ ที่สำคัญ: ป้ายอันดับคำง่าย · ซับ k01 ใช้ `caps("k01")` จาก lines.json (ประโยคเขียนมือยาวล้นเฟรม) · HUD สลับเป็น "จอมโกหก · F" ตอนเห็นการ์ด (hud สองชุด set opacity) · การ์ดกฎ translate(400,760) สูง 690 ให้เห็นเทพีและไม่ชนซับ · k08 กล้อง sy 1240 ไม่ให้ HUD ทับหัว · การ์ด F ป๊อปข้างตัวเอก (700,700) ไม่ทับหน้า · หลุมเมฆ: lip เริ่มใต้ขอบหลุม (y 1466) + วาดหลุมในกลุ่ม lip · เงาสัมผัสโตขึ้นใต้ตัวที่กำลังตก · เลนส์กฎข้อ 3 ตัว 40 px ค้าง +0.6 วิ · กรอกลับเริ่มที่ `voEnd` · fg blur ในการ์ดท้าย
- เรนเดอร์: Bash `run_in_background` timeout 7200000 (ไม่ใช่ 30 นาที) · เปลี่ยนภาพหลังเริ่มเรนเดอร์ = `pkill -f "hyperframes@0.8.185 render"` แล้วเริ่มใหม่ (exit 144 ในแจ้งเตือน = ถูกฆ่าเอง ไม่ใช่พัง)
