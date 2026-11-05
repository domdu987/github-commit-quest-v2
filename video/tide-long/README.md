# ทะเลลด ฉบับเต็ม · YouTube 16:9

EP.1–3 ต่อกันเป็นเรื่องเดียว พร้อมบทเชื่อม 2 ช่วง ยาว 5:28 · 1920×1080 · 60 fps · −14 LUFS

| ไฟล์ | คืออะไร |
|---|---|
| `LONG-tide-16x9-share.mp4` | ไฟล์สำหรับลง ขนาด 90.5 MB เข้ารหัส 2 รอบ (ภาพ 2.0 Mbps เสียง AAC 160k) sha256 `9e55415f50390e0fa11d578ced9c4810c4f335896a7a012e0010866383bfc4a6` |
| `thumb.jpg` | ปก 1280×720: คลื่นลูกที่สองสูงท่วมยอดมะพร้าว ภาพจาก 2:53 ของคลิป |
| `src/PLAN.md` | แผนเรนเดอร์และประกอบ บทเชื่อม chapters ข้อความ YouTube ผลตรวจ และสิ่งที่แก้จากตอนที่ส่งไปแล้ว |
| `src/tools/` | `prepare.sh` (ดึงตอนจาก repo แล้ว patch) · `build.sh <n>` · การแก้ภาพสำหรับ 16:9 · `edgecheckL.cjs` · `snap.py` |
| `src/bridge/` | บทเชื่อมและเสียงพากย์ที่อัดใหม่ |
| `src/assemble.sh` | รวม 3 ส่วนกับเสียงทั้งเรื่องเป็นไฟล์ HQ |
| `src/thumb16_tide.py` | สคริปต์ทำปก (`SC=1.3 OX=-192 OY=-150 python3 thumb16_tide.py <ภาพ EP.2 วินาที 63.0> <โฟลเดอร์ฟอนต์> thumb.jpg`) |
| `src/mix/checks.txt` | ผล musiccheck · hisscheck · ความดังของแต่ละส่วนและทั้งเรื่อง |

- ต้นฉบับ HQ 396 MB (AAC 256k) ส่งให้เจ้าของทางแชท sha256 `4edab3963f98ff061db5bbd164f8399f6f79a7ce4e9a448bcd68c673ded6229c`
- ชื่อ คำอธิบาย และคอมเมนต์ปักหมุด อยู่ที่ `video/release/sheets/tide-upload.md` ส่วนคิวลงอยู่ที่ `video/release/day-2026-11-07.json`
- ทำใหม่ตั้งแต่ต้น: `bash src/tools/prepare.sh` แล้วรัน `src/tools/build.sh 1`, `2`, `3` เรนเดอร์ตาม `PLAN.md` §3 แล้วรัน `bash src/assemble.sh`
