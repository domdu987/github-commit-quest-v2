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
