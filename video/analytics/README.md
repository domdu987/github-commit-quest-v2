# ข้อมูลช่องรายวัน (Herman model 6.1 sol → Claude)

ผู้ใช้ตั้งไว้ 31 ต.ค. 2569: Herman ส่งข้อมูลช่องให้ทุกวัน · Claude วิเคราะห์แล้วทำคลิปถัดไปให้ดีขึ้น · Hermes เป็นคนลงคลิปในช่อง (แพ็กเกจใน `video/release/`)

## ส่งอะไร (ทุกคลิปที่ยังมีคนดู · แยกแพลตฟอร์ม)

ไฟล์ `video/analytics/daily/YYYY-MM-DD.json` (หรือวางในแชทก็ได้) หนึ่งไฟล์ต่อวัน:

```json
{
  "date": "2026-11-01",
  "channel": { "platform": "tiktok", "followers": 0, "follows_today": 0, "profile_views": 0, "views_today": 0 },
  "clips": [
    {
      "id": "sink-ep1",
      "platform": "tiktok",
      "posted_at": "2026-10-31T21:30+07:00",
      "views": 0, "reach": 0,
      "avg_watch_s": 0, "length_s": 62, "completion_pct": 0,
      "retention": { "1": 100, "2": 0, "3": 0, "5": 0, "10": 0, "20": 0, "30": 0, "45": 0, "60": 0 },
      "likes": 0, "comments": 0, "shares": 0, "saves": 0, "follows_from_clip": 0,
      "sources_pct": { "for_you": 0, "following": 0, "profile": 0, "search": 0, "sound": 0, "other": 0 },
      "audience": { "new_pct": 0, "returning_pct": 0 },
      "top_comments": ["…"]
    }
  ]
}
```

- `id` ใช้ชื่อเดียวกับใน `video/release/*.json` · `platform` เป็น `tiktok` | `ig` | `fb` | `yt` · ตัวเลขที่ไม่มีให้ใส่ `null`
- ถ้าได้กราฟการรักษาผู้ชมทุกวินาที ให้ส่งทั้งกราฟ (`retention` เป็น { วินาที: % }) ยิ่งละเอียดยิ่งชี้ช็อตได้แม่น

## Claude ทำอะไรกับข้อมูล

- เทียบกราฟการรักษาผู้ชมกับ `schedule.json` ของตอนนั้น → ช็อต/ประโยคไหนคนเลื่อนทิ้ง (ทุกจุดที่ตกเกิน 5% ภายใน 2 วิ)
- ฮุก: % ที่อยู่ถึงวิ 3 · คำสั่ง "อย่า…" มาทันไหม · ปกและเฟรมแรกได้คลิกไหม
- ความยาวกับการดูจบ · ช่วงการ์ดความรู้กับยอดเซฟ/แชร์ · หักมุมกับยอดคอมเมนต์ (คนดูย้อนหาความพลาดไหม)
- เทียบข้ามเรื่องและแพลตฟอร์ม แล้วสรุปเป็นข้อแก้ที่ทำได้จริงในคลิปถัดไป
- รายงานลง `video/analytics/reports/YYYY-MM-DD.md` และบันทึกบทเรียนที่ยืนยันแล้วลง skill (`references/growth-playbook.md`)
