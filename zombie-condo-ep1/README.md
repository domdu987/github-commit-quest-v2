# ซอมบี้ระบาด EP.1 — "คอนโดชั้น 23"

วิดีโอสั้นแนวตั้ง (720×1280, 30 fps, ~80 วิ) สร้างทั้งเรื่องจากโค้ด: ภาพเป็น **SVG** ทุกช็อต
ขับเคลื่อนด้วยเอนจิน **HyperFrame** (ไทม์ไลน์แบบเฟรมแน่นอน) เสียงบรรยาย/SFX จาก **fal.ai**

- บท + สตอรีบอร์ดละเอียด: [`script/SCRIPT.md`](script/SCRIPT.md)
- ผลลัพธ์: `out/zombie-condo-ep1.mp4`

## โครงสร้าง

```
hyperframe/hyperframe.js   เอนจิน: seek(t) → คีย์เฟรม/อีสซิง/กล้อง/สั่น/กะพริบ/นอยส์ (deterministic ทุกเฟรม)
scenes/art.js              ไลบรารีวาด SVG: ปอ (พนักงานออฟฟิศ), แมวส้ม, ซอมบี้, เส้นขอบฟ้ากรุงเทพ, ทางเดิน/ลิฟต์, ภาพตัดตึก 23 ชั้น, ห้องน้ำ, ก๊อก+เกจ, ประตูหนีไฟ, สมุด + ไอคอน 23 ตัว (ART.icon)
scenes/ui.js               ซับไตเติล, HUD การ์ด, ชิปขั้นตอน, ตราประทับ, ป้ายชื่อ, การ์ดเสบียง, การ์ดจบ, post-FX (แฟลช/เฟด/red pulse)
scenes/shots.js, shots2.js ช็อต 1–19 (มุมกล้อง ภาพ เอฟเฟกต์ ไอคอนขยับ แสง/เงา)
scenes/index.html          หน้าเรนเดอร์ (เปิดในเบราว์เซอร์ได้: ?t=12.5 ดูเฟรมเดียว, ?play เล่นสด)
audio/lines.json           บทบรรยาย 13 คลิป (10 บีต; "อย่า." และหักมุมแยกคลิปเพื่อคุมความเงียบ)
audio/tts.js               สร้างเสียงไทยผ่าน fal.ai → MiniMax speech-02-hd (language_boost=Thai)
audio/timeline.js          คำนวณไทม์ไลน์จากความยาวเสียงจริง + ช่องหายใจ → timeline.json, voice.wav
audio/subs.json, align.js  ชิ้นซับไตเติล + จับเวลาด้วย fal.ai Whisper (timestamp ระดับตัวอักษร) → cues.json
audio/sfx.js               SFX/แอมเบียนต์ 18 ชิ้น ผ่าน fal.ai stable-audio-25
audio/mix.js               วางเสียงทั้งหมดบนไทม์ไลน์ + loudnorm → mix.wav
render/render.js           Playwright/Chromium ถ่ายทุกเฟรม (หลาย worker) → ffmpeg → MP4
render/snap.js             ถ่ายภาพนิ่งหลายเวลาเป็น contact sheet เพื่อตรวจภาพ
```

## หลักการ HyperFrame

ทุกอย่างบนจอเป็นฟังก์ชันของเวลา `t` (ไม่มี CSS animation / requestAnimationFrame)
`HF.shot({start, end, init(g), update(lt, g, t, dur)})` — `init` สร้าง SVG ครั้งเดียว, `update` ตั้งค่าทุกเฟรม
ตัวช่วย: `kf(t, [[t0,v0],[t1,v1],…], ease)`, `seg(t, start, dur, ease)`, `cam(el, {x,y,s,r})`, `shake`, `flicker`, `noise`
ผลคือเรนเดอร์ซ้ำได้เฟรมต่อเฟรมเป๊ะ ๆ และแบ่งงานเรนเดอร์ขนานได้

## สร้างใหม่ทั้งหมด

ต้องมี Node 22+, Playwright + Chromium, ffmpeg และสิทธิ์เรียก fal.run (`FAL_KEY` หรือ proxy ที่แทรก key ให้)

```bash
./build.sh            # tts → timeline → align → sfx → mix → render
node render/snap.js 1.5 20 45 71   # ตรวจภาพเฉพาะเวลา → out/sheet.png
```

เปลี่ยนบท: แก้ `audio/lines.json` + `audio/subs.json` แล้วลบ `audio/clips/*.mp3`, `audio/whisper/*.json` ก่อนรัน `build.sh`
