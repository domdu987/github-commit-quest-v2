# ช่างเชื่อมสายฟ้า ฉบับรีเมค (บทเจ้าของ 13 พ.ย. 2569) — ฉาก 3D จริง + ตัวละครสไตล์ skill reference-style-shorts

- บท: `../stories/s8/TELL_v2_owner.md` · เสียงพากย์ 75 บรรทัด Enceladus tempo 1.3 (`production/lines.json`, สร้างด้วย `mklines.py` → `voice.py` → `voice_qa.py`)
- ฉาก (Blender bpy 5.3, Cycles CPU, ใช้ `office3d` ของ skill เป็นไลบรารี): `production/sets/roof3d.py` ดาดฟ้าตึก 7 ชั้นกลางพายุ (ป้ายโฆษณาเจ๊หงส์ ทางเดินเหล็ก สายฟ้า เมืองฝั่งธน) · `soi3d.py` ซอยตึกแถว ร้านเหล็กดัดเจ๊หงส์ เสาไฟ+หม้อแปลง กล้วย มอเตอร์ไซค์ · ภาพนิ่ง `roof_stills.jpg` `soi_stills.jpg`
- ตัวละคร (เจ้าของเลือก 13 พ.ย.: "ออกแบบตัวละครใหม่ เอาแบบนี้" = หัวกลมขาว เส้นหมึกหนา แขนขาเส้นยาง): `production/cast/lt_cast.py` (ต่อยอด `v2/puppet` + `v3/cast/cast_ext.py` ของ skill) welder hong kim nurse nb_man nb_woman · 24 ท่าใน `lt_cast.POSES` · ภาพ `lineup_s.jpg` `poses_s.jpg`
- คลิปทดลอง EP.1 ช่วงแรก 26 วิ: `production/shots/lt_look2.py sprites|render <shot>` → `lt_finish2.py mix|frames|mux` (ไฟล์ lt_look.py / lt_finish.py = รุ่นตัวละครเก่า ltcast เก็บไว้เป็นบันทึก)
- ต้องมี: skill pipeline ที่แตกไว้ใน `scratchpad/r3d/` (v2/puppet, v3/set3d, v3/cast) · พอร์ต 8790 เสิร์ฟ hf/lt1 สำหรับรุ่นเก่าเท่านั้น
