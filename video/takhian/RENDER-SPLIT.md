# ต้นตะเคียนกลางนา: แบ่งเรนเดอร์ 3 เลน

> **คำเตือน (2 พ.ย. 2026 เวลา 10:45Z):** ช่วงที่ไม่ได้เริ่มที่ 0 วิเรนเดอร์ช้ามาก
> - วัดได้ราว 0.05–0.1 เฟรม/วิ ขณะที่ช่วงที่เริ่มที่ 0 ได้ราว 3.6 เฟรม/วิ
> - สาเหตุคือ `tweenFromTo` ต้องเลื่อน timeline ทั้งเรื่องทุกเฟรม
> - ให้เรนเดอร์ทั้งตอน หรือใช้เฉพาะช่วงที่เริ่มที่ 0
> - EP.1 ฉบับสุดท้ายเรนเดอร์ทั้งตอนครั้งเดียวจาก 618743f
> - **รอยตัดจริงคือ ceil(start×60):** strike = เฟรม 6341–6680 · speak (EP.2) = 1591–1802

- **commit ที่ล็อก:** commit แรกที่เพิ่มไฟล์นี้บน `prod/lane-b`
  - เลขอยู่ในข้อความที่เลน B ส่งให้ผู้ประสานงาน
  - ทุกเลน checkout commit เดียวกันนี้
- **ภาพ:** 1080×1920 ที่ 60fps
- **เครื่องมือ:** hyperframes 0.8.185 · `-f 60 -w 4` · ใช้ค่าคุณภาพเริ่มต้น (looks) ทุกเลน
  - เลน C วัดแล้ว: ราว 2.3 เฟรม/วิบนเครื่อง 4 คอร์
- **สเปกไฟล์ช่วง:** ต้องตรงกันทุกเลน เพื่อต่อแบบ stream copy ไม่ต้องเข้ารหัสซ้ำ
  - h264 High · yuv420p · 1080×1920 · 60/1 fps
  - จำนวนเฟรมตรงช่วงพอดี · ไม่มีเสียง
  - ใช้ `render_range.sh` ของเลน C ได้ (ตัดเฟรม [0, N) พอดี)
  - เลน C มี join_ep2.sh ที่ทดสอบต่อแล้ว

## ช่วงเฟรม

ทุกช่วงตัดที่รอยตัดช็อตพอดี และเวลาตรงเฟรม (เฟรม/60)

| เลน | ตอน | TK_RANGE (วินาที) | เฟรม | จำนวนเฟรม | รอยตัด |
|---|---|---|---|---|---|
| B | EP.1 | `0 80.6` | 0–4835 | 4836 | จบก่อนช็อต spread |
| D | EP.1 | `80.6 124.733333` | 4836–7483 | 2648 | ตั้งแต่ช็อต spread ถึงจบ |
| C | EP.2 | `0 80.65` | 0–4838 | 4839 | จบก่อนช็อต rule3 |
| D | EP.2 | `80.65 120.666667` | 4839–7239 | 2401 | ตั้งแต่ช็อต rule3 ถึงจบ |

- **ความยาวเต็ม:** EP.1 = 7484 เฟรม (124.733 วิ) · EP.2 = 7240 เฟรม (120.667 วิ)

## build ช่วงของตัวเอง

ต้องมี workspace ที่มี `hf/lib` กับ `hf/rig` (จาก `setup_workspace.sh`) และใน `hf/lib` ต้องมีไฟล์เหล่านี้ตรงตามที่ make.py เรียก:

- hornet / hn* ← `video/hornet-ep1/lib/`
- logtruck / ltcast ← `video/logtruck-ep1/lib/`
- chalawan ← `video/chalawan/src/`
- disaster ← `video/hooks/disaster/src/`
- hooks.js ← **`video/chalawan/src/hooks.js`**

ตัวอย่างสำหรับเลน D EP.1:

```
TK_RANGE="80.6 124.733333" video/takhian/build/build.sh 1 <workspace>/hf tk1-d
cd <workspace>/hf/tk1-d && npx --yes hyperframes@0.8.185 render -f 60 -w 4 -o <out>/EP1-part2.mp4
```

- รันด้วย `run_in_background` และ timeout 7200000
- `build.sh` copy `src/takhian.js` และ `src/stormfx.js` ลง `hf/lib` ให้เอง
- ถ้าไม่ตั้ง `TK_RANGE` จะได้ทั้งตอน
- **วิธีที่ช่วงทำงาน:** foot.part เลื่อนเวลาเริ่มของทุก clip ไป −a แล้วให้ timeline หลักเล่น timeline จริงจาก a ถึง b
  - เฟรม n ของช่วงจึงเท่ากับเฟรม round(a×60)+n ของทั้งตอน
  - เลน B ตรวจแล้ว: ภาพช่วงกับภาพทั้งตอนที่เวลาเดียวกันต่างกัน 0 พิกเซล

## ส่งไฟล์และต่อไฟล์

1. เลน D push `EP1-part2.mp4` และ `EP2-part2.mp4` (ภาพล้วน ไม่มีเสียง) ไว้ที่ `video/takhian-kit/out/` บน `prod/lane-c`
2. ตรวจจำนวนเฟรมก่อนต่อ:
   ```
   ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 <part>.mp4
   ```
   ต้องได้ตามตารางข้างบน
3. เลน B ต่อ EP.1 · เลน C ต่อ EP.2 (ตัวอย่างนี้คือ EP.1):
   ```
   printf "file 'EP1-part1.mp4'\nfile 'EP1-part2.mp4'\n" > parts.txt
   ffmpeg -v error -f concat -safe 0 -i parts.txt -c copy raw.mp4
   ```
4. mux กับ `video/takhian/ep<N>/mix.wav` ล่าสุดตาม `render.sh <hf> <ep dir> <name> --mux`:
   - HQ = copy ภาพ + AAC 256k
   - share = CRF 21
5. ชื่อไฟล์: `EP1-takhian-tonkhian-klang-na-HQ.mp4` · `EP2-takhian-tonkhian-klang-na-HQ.mp4` (และ `-share.mp4`)
6. **ตรวจหลังต่อ:**
   - sheet 1 fps ทั้งตอน
   - ดูรอยต่อที่ 80.6 วิ (EP.1) และ 80.65 วิ (EP.2) ทีละเฟรม ต้องไม่มีเฟรมซ้ำหรือเฟรมหาย
   - ความยาวภาพต้องเท่ากับเสียงภายใน 1 เฟรม
