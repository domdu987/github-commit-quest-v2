# รูพญานาค EP.1: เรนเดอร์ที่เครื่องเลน B/C

ผู้ประสานงานกำหนดให้เรนเดอร์จริงที่เครื่องเลน B/C เพราะเครื่องเลน D ช้า (ราว 6 วิ/เฟรม และ -w 4 ค้าง)

- **commit:** ใช้ commit ล่าสุดของ `prod/lane-d` ที่ข้อความแจ้งผู้ประสานงานระบุไว้ แล้ว checkout โฟลเดอร์ `video/rupnak/` จาก commit นั้น
- **ภาพ:** 1080×1920 · 60fps · `-f 60 -w 4` · คุณภาพเริ่มต้น (looks)
- **ความยาว:** 119.181 วิ ≈ 7151 เฟรม

## build

ต้องมี workspace ที่มี `hf/lib` และ `hf/rig` (สร้างจาก `setup_workspace.sh`)

- `build.sh` copy `lib/*.js` ลง `hf/lib` ให้เอง
- `lib/rig2-fingers.js` จะไปแทน `hf/lib/rig2.js` · เป็น rig เดิมที่เพิ่ม flag `fingers` แบบเปิดเฉพาะเมื่อสั่ง ตัวละครเรื่องอื่นได้ภาพเหมือนเดิมทุกอย่าง

```
bash video/rupnak/build/build.sh 1 <workspace>/hf rk1                                   # ทั้งตอน
TK_RANGE="0 63.016667" bash video/rupnak/build/build.sh 1 <workspace>/hf rk1-a          # เฟรม 0–3780 (3781 เฟรม)
TK_RANGE="63.016667 119.183333" bash video/rupnak/build/build.sh 1 <workspace>/hf rk1-b # เฟรม 3781–7150 (3370 เฟรม)
cd <workspace>/hf/rk1 && npx --yes hyperframes@0.8.185 render -f 60 -w 4 -o <out>/raw.mp4 .
```

- **TK_RANGE:** ใช้แบบเดียวกับ `video/takhian/RENDER-SPLIT.md`
  - คลิปทุกชิ้นเลื่อนเวลาไป −a แล้ว timeline หลักเล่นจาก a ถึง b
  - เลน D ตรวจแล้ว: ภาพช่วงเทียบกับภาพทั้งตอนที่เวลาเดียวกันได้ PSNR 70.6 dB · ต่างแค่ grain นิดเดียว
- **จุดแบ่ง 63.016667 วิ:** เป็นเฟรมแรกของช็อต know0 (ภาพผ่าครึ่ง) ต่อด้วย concat แบบ copy ได้

## เสียงและการ mux

- เสียงอยู่ใน `ep1/`:
  - `mix.wav` · −14.0 LUFS · peak −2.0 dBFS · ยาว 119.181 วิ เท่ากับ schedule
  - `vo_stem.wav` · `music_stem.wav`
- ผลตรวจอยู่ใน `ep1-gate/audiochecks.txt`: hisscheck PASS (flatness 0.31) · musiccheck PASS
- mux ตาม `render.sh <hf> <ep dir> <name> --mux`:
  - HQ = copy ภาพจาก raw + AAC 256k
  - share = CRF 21
- ชื่อไฟล์: `EP1-rupnak-din-yaek-pen-wong-HQ.mp4` / `-share.mp4`
