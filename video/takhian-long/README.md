# ต้นตะเคียนกลางนา ฉบับเต็ม 16:9 (YouTube · ลง 9 พ.ย. 2569 09:30)

โต๊ะภาพ 1 (เลน C) ตามคำสั่งผู้ประสานงาน 5 พ.ย. · TEAM-CHARTER §7

## โครงเรื่อง (247.857 วิ ≈ 4:08)
1. EP.1 ทั้งตอน `hook` → `none` (ตัดการ์ด `next` ที่ชี้ไป EP.2 ของ Shorts)
2. บทเชื่อม 13.5 วิ (บรรทัดใหม่ 3 ประโยค อนุมัติแล้ว 5 พ.ย.)
   - `xwait` ผู้บรรยาย: "ฝนยังกระหน่ำ… ทุกคนยังยืนนิ่ง ไม่มีใครขยับ"
   - `xkid` ต้น: "ยาย… นางจะมาเอาพวกเราไปด้วยไหม"
   - `xnow` ผู้บรรยาย: "แต่นาทีนี้… ลุงรอไม่ได้แล้ว"
   - `xchap` การ์ดบท "ตอนที่ 2 อย่ากลัวจับตัวเขา" ใช้เสียง n02 เดิมของ EP.2
3. EP.2 `fear` → `end` (ตัดฮุก `hook` กับ `cmd`)

## build
- kit ภาพรุ่นใหม่ `video/takhian/upgrade/` (build, src, ep1, ep2) จาก `ccr-fb88c4b3-kcqyid` วางเป็น `<kit>/video/takhian/` แล้วใส่โฟลเดอร์ `full/` นี้เป็น `<kit>/video/takhian/full/` พร้อม `video/longform/landscape.js`
- `bash full/build_full.sh <workspace hf> tkfull landscape`
  - body = common + { EP.1 } + { บทเชื่อม } + { EP.2 } ในบล็อกแยกกัน
  - key ของ EP.2 ที่ชนกับ EP.1 (hook, cmd, buff, joke) เปลี่ยนเป็น `e2_<key>` · id ฉากที่ชน (cr, no, rp, sp, tr) ใส่ q นำหน้า
  - ช็อตที่ตัด (next, e2_hook, e2_cmd) ยังอยู่ใน schedule แบบ `skip` (ต้องมีให้ D(key) อ่านได้) แต่ ADD ในบล็อกข้ามไป
- เสียงพากย์ใหม่: `full/vo/tts.py` (fal gemini-3.1-flash-tts · Puck / Leda · สไตล์เดิมจาก mklines.py) · ผ่าน Whisper: x01 cer 0.013 · x02 0.071 (อัดซ้ำ 1 ครั้ง) · x03 0.057

## ตรวจก่อนเรนเดอร์
- `precheck/cuts-01..11.jpg`: ทุกช็อต 2 จุด (ต้นช็อต + 70%) ภาพละ 480×270 จาก build แนวนอน

## เสียง (`full/mix.py`)
- สูตรทะเลลดของ `video/release/audio/takhian-tide-mix` (suno1 ไม่มี EQ · −30 dB RMS · duck 0.65) ทั้งเรื่อง
- ต้องมีข้าง `full/`: `../lib/mixcore.py` (จาก takhian-tide-mix/lib) · `../sfxlib/` (prod/lane-b) · `../music/takhian-theme.mp3` = `video/music/suno1.mp3` · `vo/` (EP.1 ตาม id เดิม · EP.2 เป็น `e2_<id>` · x01–x03)
- suno1 ยาว 133.6 วิ: เล่นจาก 0 สำหรับ EP.1 กับบทเชื่อม เฟดออก 0.6 วิเข้าการ์ดตอนที่ 2 แล้วเริ่มใหม่จาก 0 บนการ์ด
- dip ทั้งหมดวางก่อน boost (dip ของ mixcore ใช้ค่าต่ำสุด จะยกเลิก boost ที่วางก่อนหน้า)
- เพลงที่ยกหลังฟ้าผ่า 2 จุด ×1.2 (Shorts ใช้ ×1.6): รอบแรก musiccheck ข้อ "ระหว่างประโยค" ได้ −26.0 เพราะเรื่องเต็มมีช่วงไม่มีเสียงพูดยาวแค่ 3 ช่วง · เพลงเฟดใต้การ์ดจบ 2.5 วิ
- ผล: musiccheck PASS (−34.2 · −28.7 · 19.5 LU · 4%) · hisscheck PASS · −14.2 LUFS · peak −2.4 dBFS

## edgecheck แนวนอน
- `full/edgecheckL.cjs` = edgecheck.cjs ของ skill ที่เปลี่ยน viewport เป็น 1920×1080 และขอบ 6 px ตามขนาดนั้น
