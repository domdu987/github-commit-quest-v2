# ทะเลลด ฉบับเต็ม · YouTube 16:9: render and assembly plan

- **Slot:** อ. 10 พ.ย. 2569, 09:30. Final by 9 พ.ย., 22:00 (Bangkok). The `video_long` item is in `video/release/day-2026-11-10.json`.
- **State:** all three parts are render-ready. The film is one story, with narrated bridges where EP.2 and EP.3 used to open on their hooks.
- **Working folder:** `/tmp/claude-0/-home-user-github-commit-quest-v2/4f94749f-8122-57a4-aa41-e38e84dcb96c/scratchpad/tidelong/`. All paths below are relative to it (written as `tidelong/…`).

## 1. Part order, lengths and trims

| # | Part | Build | Length | Frames @60 | Starts in film | In/out trim |
|---|---|---|---|---|---|---|
| 1 | EP.1 ทะเลถอย อย่าคอยดู. Ends on "คลื่นลูกแรก… / ไม่ใช่ลูกที่ใหญ่ที่สุด" plus a 1.1 s hold. The choice and the end card are cut in the schedule. | `tidelong/build/ep1` | 113.000 s | 6780 | 0:00.000 | none |
| 2 | EP.2′ คลื่นแรกไป อย่าไว้ใจ. Bridge A replaces the hook. Ends on "แล้วไลฟ์ก็ดับ" plus a held beat on the dead stream. The choice and the end card are cut. | `tidelong/build/ep2` | 102.500 s | 6150 | 1:53.000 | none |
| 3 | EP.3′ หนีไม่ทัน ขึ้นชั้นสูง. Bridge B replaces the hook. Ends on its own "ทะเลลด / ตอนจบ" card. | `tidelong/build/ep3` | 113.250 s | 6795 | 3:35.500 | none |
| | **The film** | | **328.750 s (5:28.75)** | **19725** | | |

- **No trims at assembly:** each part's `#root` duration is exactly its length. Each length is a multiple of 0.25 s (15 frames, 12000 samples), so HyperFrames' `ceil(duration*fps)` gives exact frames and every `mix.wav` has the same length as its video.
- **EP.3's last card** is "ทะเลลด / ตอนจบ" on the evacuation sign. It is not a follow or next-episode CTA, so it stays as the film's ending, redrawn full width.
- **Corner badge:** "ทะเลลด" in all three parts, not "ทะเลลด · EP.N". The 0:00 hook stays as EP.1's ("ถ้าวันหนึ่ง… คุณเห็นทะเลลดลงไปไกล / อย่าลงไปเก็บ").

## 2. The bridges

Narrator: Puck, the series' narrator style string verbatim, tempo 1.2. Recorded with `video/tide-ep1/lib/voice.py` into `tidelong/bridge/` and checked with fal Whisper (`asr.json`). Every line states only what the story already shows:

| Line | Spoken | Caption | Length | Whisper (CER) | Shown over | Grounded in |
|---|---|---|---|---|---|---|
| b01 | จูนตัดสินใจ… วิ่งลงไปตามยาย | `จูนตัดสินใจ… / วิ่งลงไป[ตามยาย]` | 2.32 s | จูนตัดสินใจวิ่งลงไปตามยาย (0.00) | **brA** (new): จูน on the hill makes up her mind and bolts | EP.1's choice "วิ่งลงไปตามยาย"; EP.2 opens with her dashing down the steps |
| b02 | ลงไปหาทะเล… ที่กำลังจะกลับมา | `ลงไปหาทะเล… / ที่{กำลังจะกลับมา}` | 2.54 s | ลงไปหาทะเลที่กำลังจะกลับมา (0.00) | **open** (EP.2's own): she runs down, the bay drawn back behind her | EP.1 "ทะเลหายไปอีกแล้ว", "คลื่นลูกแรก… ไม่ใช่ลูกที่ใหญ่ที่สุด"; EP.2's second wave |
| — | (no voice) | — | — | — | **grab**: the old hand clamps her wrist at 0.3 s with the sting, as before | |
| b03 | ย้อนกลับไป… ก่อนคลื่นลูกที่สองจะมาถึง | `ย้อนกลับไป… / ก่อน[คลื่นลูกที่สอง]จะมาถึง` | 2.88 s | ย้อนกลับไป ก่อนคลื่นลูกที่ 2 จะมาถึง (0.09, digit only) | **brB** (new): EP.2's siren angle, the tower blaring over the hotel and the shop | ARC EP.3 "ย้อนดูยาย"; EP.3 opens at the second wave, ยาย's side |
| b04 | ยายยังอยู่ที่ร้าน… กอดรูปเก่าไว้ | `ยาย[ยังอยู่ที่ร้าน]… / กอด[รูปเก่า]ไว้` | 2.84 s | ยายยังอยู่ที่ร้าน กอดรูปเก่าไว้ (0.00) | **yai0** (new): close on ยาย at her shop, hugging the photo | EP.2 shop shot ("รูปนี้… ยายไม่ทิ้ง"); EP.3 hook |
| b05 | คนแถวนั้น… วิ่งไปขึ้นรถ | `คนแถวนั้น… / วิ่งไป{ขึ้นรถ}` | 2.03 s | คนแถวนั้นวิ่งไปขึ้นรถ (0.00) | **hook** (EP.3's own): people run past the shop to the pickups; then **cars** (no voice) | ARC EP.3 "คนวิ่งไปขึ้นรถ ถนนเลียบหาดติด" |

Recording notes:
- **b04:** Gemini rejected "…" twice (HTTP 422). voice.py then recorded the comma variant, as designed. The caption keeps "…".
- **b05:** the first wording was "วิ่งไปที่รถ". Its CER of 0.20 passed, but Whisper heard the key word "รถ" as "โรน้ำ" (A2). It was re-recorded with ARC's own words, "วิ่งไปขึ้นรถ".

**Cost:** 6 TTS calls, 169 characters, about $0.01. Plus 6 Whisper calls on clips under 3 s, under $0.01. The total is about $0.02, well under the $0.50 cap. No SFX were bought: the series' SFX are synthesized.

## 3. Render commands (one at a time; about 105 frames/min means about 65, 59 and 65 min)

```bash
mkdir -p /dev/shm/tidelong /dev/shm/tmp
S=/tmp/claude-0/-home-user-github-commit-quest-v2/4f94749f-8122-57a4-aa41-e38e84dcb96c/scratchpad/tidelong
cd $S/build/ep1 && TMPDIR=/dev/shm/tmp npx --yes hyperframes@0.8.185 render -f 60 -o /dev/shm/tidelong/ep1.mp4   # 6780 frames
cd $S/build/ep2 && TMPDIR=/dev/shm/tmp npx --yes hyperframes@0.8.185 render -f 60 -o /dev/shm/tidelong/ep2.mp4   # 6150 frames
cd $S/build/ep3 && TMPDIR=/dev/shm/tmp npx --yes hyperframes@0.8.185 render -f 60 -o /dev/shm/tidelong/ep3.mp4   # 6795 frames
```

- Run each one with `run_in_background` and a 2 h timeout, or chain them with `setsid nohup` (SKILL.md §4).
- All three builds carry `.clip[style*="visibility: hidden"] { display: none !important; }`.
- A 5 s test render of each part, through its first cut, is in `/dev/shm/tidelong/t5_ep1b.mp4`, `t5_ep2.mp4` and `t5_ep3.mp4`. The result is in §7. Measured speed was about 120–250 frames/min, so the full parts should take less than the skill's 105 frames/min estimate.

## 4. Assembly and junction treatment

- **Video:** hard cuts. Each part opens on a shot that carries on from the previous image:
  - EP.1's wide of the drawn-back bay cuts to จูน on the hill.
  - The dead live stream cuts to the warning tower before the second wave.
- **Audio crossfade length: 0 ms.** The joins are sample-exact butt joins, with no overlap:
  - Each outgoing part fades its own music to nothing inside its mix. EP.1 fades over its last 1.0 s. EP.2′ fades over 0.5 s as the stream dies on "ดับ", then holds about 0.9 s of silence.
  - Each incoming part restarts suno1 from 0 s, and suno1's first second is near-silent. The next narrator line starts 0.3 s in.
  - Measured join A: −57 dB in the last 100 ms out, −56 dB in the first 100 ms in. Join B: digital silence out, −53 dB in.
  - An overlapping `acrossfade` would shorten the audio by its own length and push the sync off by that much at each join.
- **Joined track:** `tidelong/mix/film_mix.wav` is the three mixes already joined. It is 328.750 s, −14.0 LUFS integrated, true peak −1.1 dBFS, LRA 4.1.
- **`tidelong/assemble.sh`** does the rest:
  - It checks the three renders' frame counts.
  - It concats the video with stream copy.
  - It muxes `film_mix.wav` as AAC 256k at 48 kHz, with `-t 328.75`.
  - It prints duration, loudness and sha256. Default output: `/dev/shm/tidelong/LONG-tide-16x9-HQ.mp4`.

## 5. Chapters (paste into the description; every chapter is 10 s or longer)

```
0:00 ทะเลลดลงไปไกล… อย่าลงไปเก็บ
0:42 ตำนานละบูน คลื่นยักษ์เจ็ดชั้น
1:09 ทำไมทะเลถึงลดก่อนคลื่นมา
1:23 ตาจุ่นเป่าหอยสังข์
1:34 คลื่นลูกแรก
1:53 คลื่นแรกไป อย่าไว้ใจ
2:17 สึนามิไม่ได้มาลูกเดียว
2:52 คลื่นลูกที่สอง
3:06 ไลฟ์ของจูน
3:35 หนีไม่ทัน ขึ้นชั้นสูง
4:01 ขึ้นที่สูงไม่ทัน ต้องไปที่ไหน
4:13 หลายชั่วโมงต่อมา
4:36 ความลับ 22 ปีของตาจุ่น
5:12 วันพุธถัดมา
```

## 6. YouTube copy (from `video/tide/CAPTIONS.md`)

**Title:** `ทะเลลดลงไปไกล ปลาดิ้นเต็มหาด… อย่าลงไปเก็บ | ทะเลลด ฉบับเต็ม`

**Description:**
```
ถ้าวันหนึ่ง… คุณเห็นทะเลลดลงไปไกล ปลาดิ้นอยู่เต็มหาด 🌊 อย่าลงไปเก็บ!

ทะเลลด ฉบับเต็ม: 3 ตอนต่อกันเป็นเรื่องเดียว

กฎของยาย
"ทะเลถอย อย่าคอยดู"
"คลื่นแรกไป อย่าไว้ใจ"
"หนีไม่ทัน ขึ้นชั้นสูง"

ในคลิปมีความรู้ใช้ได้จริง: ทำไมน้ำทะเลลดก่อนคลื่นมา คลื่นเร็วแค่ไหน และทำไมไม่ต้องรอเสียงเตือน · ทำไมสึนามิไม่ได้มาลูกเดียว แต่ละลูกห่างกันนานแค่ไหน ต้องอยู่บนที่สูงถึงเมื่อไหร่ และถ้าถูกคลื่นพัดต้องทำอะไร · ขึ้นที่สูงไม่ทันต้องไปที่ไหน ตึกต้องสูงกี่ชั้น ต้องห่างฝั่งกี่กิโลเมตร และทำไมควรหนีด้วยเท้า ไม่ใช่รถ

ปี 2547 ที่ชายหาดแห่งหนึ่ง ลูกแรกสูง 2–3 เมตร… ลูกที่สามสูงเกิน 10 เมตร

ยายหายไปจากบนเขา ไลฟ์ของจูนยังเปิดอยู่… และความลับ 22 ปีของตาจุ่น

แหล่งอ้างอิงอยู่ในคอมเมนต์ปักหมุด · ตัวละครและหมู่บ้านในเรื่องเป็นเรื่องสมมติ

0:00 ทะเลลดลงไปไกล… อย่าลงไปเก็บ
0:42 ตำนานละบูน คลื่นยักษ์เจ็ดชั้น
1:09 ทำไมทะเลถึงลดก่อนคลื่นมา
1:23 ตาจุ่นเป่าหอยสังข์
1:34 คลื่นลูกแรก
1:53 คลื่นแรกไป อย่าไว้ใจ
2:17 สึนามิไม่ได้มาลูกเดียว
2:52 คลื่นลูกที่สอง
3:06 ไลฟ์ของจูน
3:35 หนีไม่ทัน ขึ้นชั้นสูง
4:01 ขึ้นที่สูงไม่ทัน ต้องไปที่ไหน
4:13 หลายชั่วโมงต่อมา
4:36 ความลับ 22 ปีของตาจุ่น
5:12 วันพุธถัดมา

#ทะเลลด #สึนามิ #26ธันวา #ทะเลอันดามัน #เอาตัวรอด #RodMaiClub
```

**Pinned comment** (the three episodes' source lists merged, verbatim from CAPTIONS.md, duplicates dropped):
```
📚 แหล่งอ้างอิง
"สังเกตเห็นน้ำทะเลลดระดับลงอย่างรวดเร็ว ให้รีบออกห่างจากชายหาดให้มากที่สุด หรือหนีขึ้นที่สูง… ในทันที": กรมป้องกันและบรรเทาสาธารณภัย (จุลสาร ลด.หยุด.ภัย มิ.ย. 2561)
"ถ้าท้องคลื่นเข้าถึงฝั่งก่อน… ดูเหมือนระดับน้ำจะลดลงอย่างกะทันหัน" / "อาจจะมีความเร็วได้ถึง 950 กม./ชั่วโมง… พอๆกับความเร็วของเครื่องบินเจ็ท": กรมอุตุนิยมวิทยา
ใกล้ฝั่งคลื่นช้าลงเหลือราว 20–30 ไมล์/ชม. "still faster than a person can run" และ "Do not wait for an official tsunami warning": NOAA (U.S. National Weather Service)
"หอสัญญาณ 130 แห่งในอันดามัน… มีการทดสอบทุก 08.00 น.ทุกวันพุธ": ปภ. ผ่าน Thai PBS (18 ธ.ค. 2567)
"คลื่นยักษ์เจ็ดชั้นในภาษามอแกน เรียกว่า ละบูน": ศูนย์มานุษยวิทยาสิรินธร (2565) · UNESCO (2567)
ปี 2547 มีคนเดินลงไปบนพื้นทะเลที่โผล่ขึ้นมา เก็บปลาและถ่ายรูป: NOAA · UNESCO · National Geographic
แผ่นดินไหวไกลๆ ทำให้เกิดสึนามิได้ โดยที่ชายฝั่งแทบไม่รู้สึกสั่น: NOAA · USGS
"A tsunami is a series of waves, and often the first isn't the largest": UNESCO-IOC
"The time between waves ranges from five minutes to two hours": NOAA (U.S. National Weather Service)
ปี 2547 ที่ชายหาดแห่งหนึ่ง "09.38 น. คลื่นสูงประมาณ 2-3 เมตร… 09.43 น. คลื่นสูง 6-7 เมตร… 10.03 น. คลื่นสูงเกินกว่า 10 เมตร": กรมทรัพยากรธรณี
"อยู่ในบริเวณที่ปลอดภัยจนกว่าจะมีประกาศยกเลิกการเตือนภัย เพราะอาจมีคลื่นสึนามิตามมาอีกหลายระลอก": กรมป้องกันและบรรเทาสาธารณภัย (จุลสาร ลด.หยุด.ภัย มิ.ย. 2561)
ข้อความจริงของหอเตือนภัย "โปรดทราบ โปรดทราบ ขณะนี้เกิดคลื่นสึนามิ ขอให้ออกจากชายหาดให้ไกลที่สุด ไปยังพื้นที่สูงโดยด่วน": Thai PBS (27 มิ.ย. 2568)
"If swept up by a tsunami, look for something to use as a raft": UNESCO-IOC · USGS
ปี 1960 ที่ฮิโล หลายคนกลับลงไปเพราะได้ยินว่าคลื่นแรกเล็กและอันตรายผ่านไปแล้ว แล้วเจอคลื่นลูกที่ใหญ่ที่สุด: USGS
"หากเป็นพื้นราบต้องอยู่ในระยะห่างไม่ต่ำกว่า 3 กิโลเมตร กรณีหนีขึ้นที่สูงต้องอยู่เหนือระดับน้ำทะเลไม่ต่ำกว่า 15 เมตร หรือเข้าไปหลบในอาคารที่มั่นคงแข็งแรงและมีความสูงมากกว่า 4 ชั้นขึ้นไป": กรมป้องกันและบรรเทาสาธารณภัย (จุลสาร ลด.หยุด.ภัย มิ.ย. 2561)
"Plan to evacuate on foot if you can; roads may be impassable due to damage, closures, or traffic jams": NOAA
ปี 2547 รถที่ขับหนีคลื่นชนกันบนถนน: Thai PBS (26 ธ.ค. 2567)
"The cancellation of a tsunami warning does not mean the danger has passed" และอย่าเข้าอาคารที่เสียหายหรือมีน้ำล้อมรอบ จนกว่าเจ้าหน้าที่จะบอกว่าปลอดภัย: NOAA (U.S. National Weather Service)
ปี 2547 ชาวมอแกนที่หมู่เกาะสุรินทร์ ผู้อาวุโสเห็นน้ำทะเลลดผิดปกติแล้วพาทุกคนขึ้นที่สูง แทบทั้งหมดรอด: ศูนย์มานุษยวิทยาสิรินธร · UNESCO
ตัวละครและหมู่บ้านในเรื่องเป็นเรื่องสมมติ
สายด่วนนิรภัย ปภ. 1784 · สายด่วนแผ่นดินไหว 1182 กด 3
```

## 7. Checks (run on the final files)

**Picture:**
- `tidelong/sheets/cuts/ep{1,2,3}_NN.jpg` has one frame per cut: 28 + 26 + 23 = 77 cuts, in 960×540 tiles, each labelled with time, shot and landscape band. Every cut was looked at.
- The 16:9 edge walk (`tools/edgecheckL.cjs`, every 0.25 s) found nothing off-frame at rest: `tidelong/sheets/edge_ep{1,2,3}.txt`. What it flagged are only entrance motions:
  - the rule and knowledge boards dropping in from above, 0.1 s into their shots;
  - a map label leaving during the fly-in.

  After the live overlay's margin tweak there are 13 flags in all: 6 in EP.1, 5 in EP.2′, 2 in EP.3′.
- 5 s test renders (`#root` set to 5 s, through each part's first cut; `/dev/shm/tidelong/t5_ep1b.mp4`, `t5_ep2.mp4`, `t5_ep3.mp4`):
  - All three gave 300 frames at 1920×1080 and 60 fps, in 1 min 17 s, 2 min 31 s and 2 min 34 s.
  - Every clip after the first cut paints. There are no black tiles, so the display:none rule holds in the real render.
  - EP.1's first test exposed bare strips at both edges in the opener's last frames, where the camera eases out to zoom 1.0. The mid-shot snapshots had missed them, because the sand's base rectangle ended at x −600…1700. It was widened, and the re-render is clean.
  - Every shot's first and last frame (its widest zoom) was then also snapshotted: `tidelong/sheets/ends/`, 154 frames, all checked.

**Sound** (`tidelong/mix/checks.txt`):

| Part | musiccheck: under voice / between lines / voice over music / music missing | hisscheck: flatness · pause floor | Loudness |
|---|---|---|---|
| EP.1 | PASS: −33.3 / −31.0 / 18.9 LU / 0 % | PASS: 0.39 · −85 dBFS | −14.0 LUFS, peak −1.01 dBFS |
| EP.2′ | PASS: −31.8 / −32.6 / 17.8 LU / 15 % | PASS: 0.36 · −85 dBFS | −14.0 LUFS, peak −1.01 dBFS |
| EP.3′ | PASS: −33.8 / −29.2 / 19.3 LU / 4 % | PASS: 0.39 · −81 dBFS | −14.0 LUFS, peak −1.01 dBFS |
| Film | PASS: −32.9 / −31.7 / 18.7 LU / 13 % | PASS: 0.38 · −82 dBFS | −14.0 LUFS, true peak −1.1 dBFS |

**hisscheck history:** the delivered tide mixes themselves fail hisscheck (flatness 0.66 / 0.72 / 0.48). The source is the synthesized SFX bus, which measures 0.80 on its own. It is now low-passed at 4.5 kHz, the fix SKILL.md A4 prescribes. Splashes and whooshes are a little duller than in the Shorts.

## 8. What changed against the delivered episodes

Diffs are in `tidelong/diffs/` (`ep1.diff`, `ep2.diff`, `ep3.diff` and `libs.diff`).

**Schedules (each episode's own `timing.py`):**
- EP.1 drops `choice` and `end`.
- EP.2 adds `brA`, `open`(b02) and a silent `grab`, and drops `choice` and `end`.
- EP.3 adds `brB` and `yai0`, puts b05 on `hook`, and makes `cars` silent.
- The last shots are held 0.12 to 0.15 s longer, to reach the 0.25 s grid.

**EP.3 working copy:** `video/tide/ep3` lagged the delivered `video/tide-ep3/composition` by two fixes, now brought in:
- n03's caption in three parts;
- the test-tone word "ปู๊ด… ทดสอบ…" at x 680.

With those, all three original episodes rebuild byte-identical to the delivered compositions before any long-version edit.

**Libraries:** each part is built with the libraries it was delivered with (`video/tide-epN/lib`).

**Mixes (each episode's own `mix.py`):**
- New cues for the bridge shots; no choice or end-card cues.
- Music fades as described in §4.
- One static gain to −14 LUFS, measured through a soft knee that keeps peaks at or under −1 dBFS. This replaces single-pass loudnorm, so `vo_stem.wav` and `music_stem.wav` are exactly what is in `mix.wav`.
- The SFX bus is low-passed at 4.5 kHz.

**16:9 fixes:** all apply only when `window.LANDSCAPE` is set. They live in `ep*/land.part`, `tools/landfix.part` and `tools/patch_libs.py`.

| Shot | Problem in plain landscape mode | Fix |
|---|---|---|
| EP.1 open, 0:00 | The title-in-sand set stopped short, leaving seams down both sides of the film's first frame, and bare strips once the camera eases out to zoom 1.0 | Sand base, ripples, sheen and water extended to x −1100…2200 |
| EP.1 photo, 0:23 | ยาย's arm ended in a stump in mid-air; the wall's ends showed | Closer camera (1.6) and band y0 330 |
| EP.1 rule, 0:36 | The fitted board hid ยาย's head | Band y0 340 |
| EP.1 cup, 0:55 | The terrace rail's cut ends and a black floor showed; the caption covered the glass | Camera 1.5 and y0 420; the glass now sits above the caption |
| EP.1 know1/know2, 1:09 | Dark strip down the left edge | Section sky and floor widened |
| EP.1 clue, 1:46 | Edges of the sand patch and bare sky on the right | Starts at camera 1.2 |
| EP.1 fish; EP.2 live, comment, close | The live overlay was a phone-width column in the middle: header cropped off, comment rows in the caption band | Laid out as a landscape stream UI (`liveL`): header top-left, comments and pinned comment down the left, buttons and gift down the right, all above the captions |
| EP.2 rule, 2:06 | The fitted board hid ตาจุ่น's face | Band y0 430 |
| EP.2 wall, 2:52 | The second wave was a strip in the middle of the frame | Wall columns span x −780…1860 |
| EP.3 stair, 3:57 | ยาย climbed behind the fitted rule board | Camera shifted so she climbs to the right of it |
| EP.3 photo and clip, 4:36 | The caption covered the photo's base and the clipping's own caption line | Band y0 120 / 150 |
| EP.3 end, 5:25 | "ตอนจบ" was a vertical strip in a black frame | Full-width dusk card (no fit), with the hill continued to both edges |

**Open, not fixed (would need re-staging):**
- **Shadow-puppet screens** (EP.1 legend 0:42, EP.3 moken 5:06): a portrait screen centred in a dark room, with wide dark sides. They read as a lit screen in the dark.
- **EP.2 knowledge boards** (series and heights, 2:17–2:52): centre-fitted portrait boards. The text is small but legible at 1080p. There is no room to enlarge them above the caption band.
- **Foreground framing elements:** half the evacuation sign at the left edge in EP.1 wave1 (1:35), and the corner of a blue sign under the badge in a few hill shots.
- **EP.1 cup:** a small dark wedge of floor remains in the bottom-right corner.
- **Not part of this job:** the 16:9 thumbnail, the release JSON entry and the upload sheet.

## 9. Files and rebuild

- `tidelong/build/ep{1,2,3}/`: the render-ready HyperFrames projects. Each has `index.html` and `assets/` (fonts, its own libs, `landscape.js`).
- `tidelong/mix/ep{1,2,3}/{mix,vo_stem,music_stem}.wav` and `mix.log`; `tidelong/mix/film_mix.wav`; `tidelong/mix/checks.txt`.
- `tidelong/ep{1,2,3}/`: the episode working copies. They hold `lines.json`, `timing.py`, `schedule.json`, `make.py`, `mix.py`, the parts and `vo/` (delivered wavs plus the bridge takes).
- `tidelong/bridge/`: the bridge lines, their takes (mp3/wav), `durations.json` and `asr.json`.
- `tidelong/sheets/cuts/`: one frame per cut, plus the sheets.
- `tidelong/sheets/ends/`: each shot's first and last frame, plus the sheets.
- Also `sheets/edge_ep*.txt` and `sheets/live_check.jpg`.
- `tidelong/tools/`:
  - `prepare.sh`: fresh copies from the repo plus every patch: `patch_timing.py`, `patch_bridges.py`, `patch_libs.py`, `patch_mix.py`.
  - `build.sh <n>`: the episode's own `make.py`, then `land.py` (the README's 16:9 edits, the display:none rule and the film badge).
  - `snap.py`: snapL.cjs plus contact sheets.
  - `edgecheckL.cjs`, `landfix.part`, `land{1,2,3}.part`.
- **To rebuild from scratch:**
  1. `bash tools/prepare.sh`
  2. `tools/build.sh 1`, then 2, then 3
  3. `cd ep1 && MIXOUT=$S/mix/ep1 python3 mix.py`, and the same for ep2 and ep3

  Re-running the mixes after a prepare gives bit-identical files.
