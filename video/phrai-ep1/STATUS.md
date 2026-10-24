# ผีพรายน้ำ ("มือพราย") EP.1: งานที่ค้างไว้

ผู้ใช้พักเรื่องนี้ไว้ (24 ต.ค. 2026) เพื่อทำ "หมอกลง" ก่อน โครงเรื่องและแหล่งอ้างอิง: `video/phrai/ARC.md`

- `production/lines.json` บท 34 บรรทัด + `vo/` เสียงทั้งหมด (สร้างแล้ว)
  - Whisper ทักไว้ 9 บรรทัด ต้องอัด take ใหม่ก่อนใช้: n02 d04 r01 d06 n14 d07 d08 d09 r02 (r02 พูดซ้ำวน, เอฟเฟกต์ใต้น้ำแรงไป ให้เบาลงแบบ g01 ของหมอกลง)
- `production/timing.py`, `head.part`, `foot.part`, `make.py`, `mix.py` ยังเป็นของชั้น 23 EP.3 (ยังไม่ได้แก้ SHOTS / ช็อต / เสียง)
- `lib/phrai.js` ฉากร่างแรก (ยังไม่เคย snapshot): riverNight pierDeck pierPOV pierSection porch bedroom underRiver ankleMarks legendPhrai reflections + ตัวละคร praew tong yai mhem
  - ต้องแก้ใน `Phrai.life`: `svgOrigin` ใช้พิกัดของ SVG ราก ใช้กับของที่อยู่ในเลเยอร์กล้องไม่ได้ → เปลี่ยนเป็น tween `attr.transform` แบบ `rotate(a cx cy)` (ดูหัวข้อ 7 ใน HANDOFF)
