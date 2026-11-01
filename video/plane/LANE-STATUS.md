# เลน D · รอดคนเดียว (เครื่องบินตก เกาะกลางแอตแลนติก) · สถานะ

อัปเดต 1 พ.ย. 2569 · branch `prod/lane-d` · **จบเรื่องแล้ว 2 ตอน final** · รอเจ้าของ/แชทประสานงานสั่งหัวข้อถัดไป (F5: ห้ามเริ่มเรื่องใหม่เอง)

**ตัดใหม่ตามเจ้าของ 1 พ.ย.:** เอาประโยค "…พลาดไปแล้ว… ตั้งแต่วินาทีที่ X คุณเห็นไหม" + ภาพย้อนเทปออกทั้ง 2 ตอน · EP.1 74.5 → 70.25 s (sha256 500652a4…) · EP.2 80.5 → 76.5 s (sha256 78bf717e…) · QA ผ่านครบ (hookcheck, edgecheck, origin_check, freezedetect, loudness, Whisper)

| ตอน | ไฟล์ | สรุป |
|---|---|---|
| EP.1 ทิ้งกระเป๋า | `video/plane-ep1/` · HQ `video/release/hq/plane-ep1-HQ.mp4` | 74.5 วิ · −14.0 LUFS · พีก −1.4 · ฮุก 3.15 วิ |
| EP.2 อยู่กับซาก (ตอนจบ) | `video/plane-ep2/` · HQ `video/release/hq/plane-ep2-HQ.mp4` | 80.5 วิ · −13.6 LUFS · พีก −1.4 · ฮุก 2.74 วิ |

- แพ็กเกจ `video/release/plane.json` (ทั้ง 2 ตอน final + sha256) · แคปชัน `video/plane/CAPTIONS.md` · ปก `video/brand/covers/plane.json`
- ARC + แหล่ง `video/plane/ARC.md` · งบ `video/plane/BUDGET.md` (~$0.70 / $3.10) · โลกของเรื่อง `video/plane/lib/` · งานทำต่อ `video/plane/ep1..2/`
- ชุดตรวจ `video/plane/review/` (style frames, ฮุก 3 แบบ, สตอรี่บอร์ด, คลิปทดสอบการขยับ 540p)
