# POST QUEUE — คิวคลิปรอโพสต์ (อ่านโดย AI extension ทุกชั่วโมง)

## คำสั่งสำหรับ AI ที่มาอ่านไฟล์นี้ / Instructions for the posting agent
1. Look at the table below. Take rows whose status is `READY`, oldest first. Post at most **1 clip per check**.
2. **Before posting, prevent duplicates:** open YouTube Studio → Content and search for the exact **Title**.
   If a video with that title already exists, the clip is already posted: skip it (and mark it POSTED, see step 5).
3. Download the video from the **Video** link. Chrome must be logged in to GitHub; the repo is private.
4. Upload it as a YouTube Short, vertical 9:16, about 60 s.
   - Title = the **Title** column.
   - Description = the full caption text under that clip's heading below.
   - Audience: "No, it's not made for kids".
   - Visibility: Public.
5. After it is published, edit this file on GitHub (pencil icon) and change that row's status from `READY` to `POSTED <date>`. Commit directly to the same branch.
6. If a captcha or "verify you are human" appears: STOP, do not try to solve or bypass it, and tell the owner. If another error happens (upload error, file picker blocked), do NOT retry more than once. Leave the status as `READY` and stop until the next hour.

Branch: `claude/new-session-73ou27`. Only rows with status `READY` may be posted. `WAIT` means not finished yet.

| # | Film | Title | Video | Status |
|---|---|---|---|---|
| 10 | ไอ้ช่างม้าลาย | ไอ้ช่างม้าลาย | film/release10/zebra_v2.mp4 | POSTED (manually by owner, 2026-11-18) — do not post |
| 11 | ไอ้หมอวัว | ไอ้หมอวัว | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release11/cowdoc_v1.mp4 | POSTED (manually by owner, 2026-11-19) — do not post |
| 13 | ไอ้แม่แรง | ไอ้แม่แรง | https://github.com/domdu987/github-commit-quest-v2/raw/film13/main/film/release13/maeraeng_v1.mp4 | WAIT (client posts himself) |
| 16 | ไอ้บ้าลวด | ไอ้บ้าลวด | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release16/wire_v2.mp4 | WAIT (client to review; client posts himself) |
| 17 | ไอ้ช่างวัดหู | ไอ้ช่างวัดหู | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release17/ear_v1.mp4 | WAIT (client to review; client posts himself) |
| 18 | ไอ้เสมียนวัว | ไอ้เสมียนวัว | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release18/oxclerk_v1.mp4 | WAIT (client to review; client posts himself) |
| 15 | ไอ้ปลาดิ้น | ไอ้ปลาดิ้น | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release15/fosbury_v2.mp4 | WAIT (client posts himself; v2 remake to QA_TEAM G/H/I, FINAL gate PASS 2026-11-20; music C) |
| 23 | ไอ้กองทัพลูกโป่ง | ไอ้กองทัพลูกโป่ง | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release23/ghost_v1.mp4 | WAIT (client to review; client posts himself) |
| 19 | ไอ้ช่างไม้ | ไอ้ช่างไม้ | https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/release19/harrison_v1.mp4 | WAIT (client to review; client posts himself) |

## Captions
(Each READY clip gets a heading here, `### <#> <Title>`, followed by the exact description text to paste.)

### 11 ไอ้หมอวัว
หมอคนนี้ขูดหนองจากมือสาวรีดนมวัว แล้วเอามาป้ายใส่แขนเด็ก 🐄💉 หมอใหญ่หัวเราะเยาะ "เดี๋ยวเด็กมันก็งอกเขาวัวหรอก!" ทั้งหมู่บ้านเรียกเขาว่า "ไอ้หมอวัว"...

แล้วใครกันแน่ที่ต้องอาย ดูให้จบ 😂

#ไอ้หมอวัว #วัคซีน #เรื่องจริง #ประวัติศาสตร์ #ประวัติการแพทย์ #เรื่องเล่า #การ์ตูน #shorts

### 16 ไอ้บ้าลวด
ชายคนนี้เอาคอขวดเบียร์ไปคว่ำบนหัวเสา แล้วบอกว่าข่าวจะวิ่งเร็วกว่ารถไฟ 🍺⚡ ทั้งสภาหัวเราะ ผู้แทนคนหนึ่งลั่นวาจา "ถ้าลวดของเอ็งส่งข่าวได้จริง ข้าจะมานั่งเฝ้ามันเอง!" ทุกคนเรียกเขาว่า "ไอ้บ้าลวด"...

แล้วใครกันแน่ที่ต้องมานั่งเฝ้าลวด ดูให้จบ 😂

#ไอ้บ้าลวด #โทรเลข #รหัสมอร์ส #เรื่องจริง #ประวัติศาสตร์ #สิ่งประดิษฐ์ #เรื่องเล่า #การ์ตูน #shorts

### 15 ไอ้ปลาดิ้น
ทุกคนกระโดดข้ามไม้หน้าตรง แต่เด็กหนุ่มคนนี้ หันหลังแล้วกระโดดหงายหลังข้ามไป 🤸‍♂️ โค้ชรุ่นเก๋าหัวเราะลั่น "เด็กทำตาม คอหักกันทั้งรุ่น! ถ้าท่านี้ได้เหรียญทอง ข้าจะหงายหลังให้ดูเอง!" คนทั้งเมืองเรียกเขาว่า "ไอ้ปลาดิ้น"...

แล้วโค้ชต้องทำตามที่พูดไว้ไหม ดูให้จบ 😂

#ไอ้ปลาดิ้น #กระโดดสูง #FosburyFlop #โอลิมปิก #เรื่องจริง #กีฬา #เรื่องเล่า #การ์ตูน #shorts

### 23 ไอ้กองทัพลูกโป่ง
ทหารกลุ่มนี้จงใจบุกด้วยรถถังลูกโป่ง ทั้งที่เยอรมันอยู่ใกล้แค่นี้ 🎈🪖 ผู้พันหน่วยข้างๆ หัวเราะลั่น "ถ้าพวกแกหลอกเยอรมันได้ ข้าจะเป่าลูกโป่งให้เองทุกลูก!" ทั้งหน่วยเลยโดนเรียกว่า "ไอ้กองทัพลูกโป่ง"...

แล้วใครกันแน่ที่ต้องนั่งเป่าลูกโป่ง ดูให้จบ 😂

เรื่องจริง: หน่วย 23rd Headquarters Special Troops หรือ "Ghost Army" ของสหรัฐฯ ในสงครามโลกครั้งที่ 2 มีศิลปิน นักออกแบบ และคนทำเสียงราว 1,100 คน ใช้รถถังยางเป่าลม เสียงรถถังจากลำโพง และวิทยุปลอม แกล้งเป็นกองทัพที่ใหญ่กว่าตัวเอง ปฏิบัติการ Viersen (มี.ค. 1945) ใช้หุ่นเป่าลมราว 600 ตัว แกล้งเป็น 2 กองพล ก่อนกองทัพที่ 9 ข้ามแม่น้ำไรน์
*ผู้พันปากดีและฉากเป่าลูกโป่งตอนจบเป็นการแต่งเติมเพื่อความสนุก เรื่องหนุ่มฝรั่งเศสปั่นจักรยานมาเห็นทหารยกรถถังมาจากคำเล่าของทหารผ่านศึก

#ไอ้กองทัพลูกโป่ง #GhostArmy #สงครามโลกครั้งที่2 #เรื่องจริง #ประวัติศาสตร์ #เรื่องเล่า #การ์ตูน #shorts

### 19 ไอ้ช่างไม้
ช่างไม้บ้านนอกคนนี้ทำนาฬิกาที่บอกได้ว่าเรืออยู่ตรงไหนกลางทะเล ⏱️🌊 เรื่องที่นักปราชญ์ทั้งอังกฤษยังทำไม่ได้ นักดาราศาสตร์หัวเราะลั่น "ถ้านาฬิกาของช่างไม้แม่นขนาดนั้น ให้พระราชามาจับเวลาเองเลย!" ทุกคนเรียกเขาว่า "ไอ้ช่างไม้"...

แล้วพระราชามาจับเวลาจริงไหม ดูให้จบ 😂

เรื่องจริงของ จอห์น แฮร์ริสัน กับรางวัลลองจิจูด (ค.ศ. 1714-1773)
ส่วนที่แต่งเพิ่มเพื่อความสนุก: นักดาราศาสตร์ขี้เยาะเป็นตัวละครสมมุติ (รวมหลายคนในคณะกรรมการ ไม่ใช่บุคคลจริงคนใด) คำท้า "ให้พระราชามาจับเวลาเอง" คำว่า "ไอ้ช่างไม้" และคำพูด "ฟลุ๊ค!" ถูกแต่งขึ้น มงกุฎกับเสื้อคลุมของพระราชาในการ์ตูนใส่ไว้ให้ดูออกว่าเป็นพระราชา ส่วนเรื่องที่พระเจ้าจอร์จที่ 3 ทดสอบนาฬิกาด้วยพระองค์เองทุกวันนาน 10 สัปดาห์ (ค.ศ. 1772) เป็นเรื่องจริง

#ไอ้ช่างไม้ #จอห์นแฮร์ริสัน #ลองจิจูด #นาฬิกา #เรือ #เรื่องจริง #ประวัติศาสตร์ #เรื่องเล่า #การ์ตูน #shorts
