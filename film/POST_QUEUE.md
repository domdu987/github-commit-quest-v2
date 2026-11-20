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
