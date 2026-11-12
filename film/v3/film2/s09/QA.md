# s09 QA: film 2, shot 9 (the priest laughs), tower set DAY, bell chamber

Delivered: `take.mkv` (g 605..724, 120 frames, first_g 605, 720x1280, 12 samples, 2 threads, libx264rgb crf 6) from `frames/g_0605.png .. g_0724.png` (not in git). g 605..718 = shot 9 ([g0, g1) = [605, 719)); g 719..724 = 6-frame out-handle (camera keeps drifting on nico, rendered in 3D) for the 9-frame dissolve into shot 10. Hard cut in (no in-handle). `meta.json`, `cues.json` (9 cues, film seconds), `contact.jpg` (16 frames, labels above the picture). Scripts: `shot.py` (take), `deliver.py` (frames, mkv, meta, cues, contact, `work/qa_numbers.json`).

## Timing (g = round((t + 0.10) * 30))
| event | g | s |
|---|---|---|
| hard cut in, two-shot in depth (cubic-out settle + creep) | 605 | 20.17 |
| "บาทหลวงหัวเราะ": padre laughs, mouth held wide open (laugh is not speech), body bounce, tears | 609-646 | |
| snap reframe onto padre (quint, 10 frames), lands t 21.2 | 632-642 (639) | 21.07-21.40 |
| quoted line "เหล็กแท่งเดียว จะไปสู้ฟ้าได้ยังไง ไอ้หนู": padre's mouth moves | 647-721 | 21.57-24.03 |
| push-in step on "จะไปสู้ฟ้า" (g 676) | 670-678 | |
| snap past padre's shoulder onto nico on "ไอ้หนู" (g 703); nico's brow tightens | 696-705 | |
| out-handle | 719-724 | |
Framing changes: 605, 632-642, 670-678, 696-705, then drift: gaps 0.9, 0.93, 0.87, 0.67 s (+ handle). Never static: smallest frame-to-frame change 1.12 levels (mean abs, 180x320), no still runs, no pops (`work/qa_numbers.json`).

## Staging (from raw/g_*.json)
| phase | head | width px | centre x | centre y (H) |
|---|---|---|---|---|
| two-shot g 605-631 | padre (near, main) | 220-237 | 135-160 | 562-591 (0.44-0.46) |
| | nico (far) | 158-166 | 446-456 | 724-733 (0.57) |
| padre close g 642-695 | padre (main) | 341-441 | 226-257 | 525-594 (0.41-0.46) |
| | nico | 202-222 | 554-564 | 727-748 |
| nico g 705-724 | nico (main) | 235-251 | 435 | 578-593 (0.45-0.46) |
| | padre (shoulder and hat brim at the left edge, out of frame centre) | | -179..-94 | |
Near/far head ratio in the two-shot 1.39-1.43 (target 1.36-1.46). No head below y 880 (heads in frame). head_flip False (key from screen-left). Nobody's back to the camera.
Mouth: lip-sync from the narration's RMS envelope at film frame g (narration +0.10 s): flat < 0.12, talk_a < 0.40, else talk_b (talk_o every 5th hold); a new drawing at most every 2 frames, 75 frames g 647..721 only. Outside the quote the mouth is the laugh drawing of padre_laugh (open, still). Nico never opens his mouth.

## Colour (hue_report.row on the 120 final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s09 g 605-724                                  14.6   34.6    0.3    1.8    0.1   28.8   14.6    5.3  0.37 0.44 0.38   OUT: red,violet,sat,val,dark
ref a t0010                                    26.3   28.6    2.2    0.2    0.0   31.2    3.9    7.6  0.27 0.51 0.07
```
Orange, blue and magenta in band; shade on the chamber walls and floor reads blue-violet (no magenta). Out of band because padre fills 30-60 % of the frame from g 642: his black cassock and hat (dark share 0.38, value 0.44) and his violet-grey `limb_edge` plus the dark bronze bell interior (violet 14.6); red is low because the red share in this set comes from brick, which padre covers. The two-shot alone is close to the set's own chamber_eye row. Not changed: it is the cast's costume.
Seconds per frame: 12.29 s wall / 23.67 s CPU mean (2 threads, two render processes on the machine).

## Differences from the plan
- Snap reframe onto padre lands at g 639 (t 21.2) as planned; added a small push step (g 676) and a snap onto nico on "ไอ้หนู" (g 703) to keep the 1.2-1.6 s framing rhythm in a 3.8 s shot; the out-handle stays on nico.
- The close camera moves 0.55 D to the left of chamber_eye so nico stays next to padre's head instead of being cut by the right edge.
- Rod: set_rod(0) on the spire (it is in nico's hands, prop of nico_hold_rod); bell at rest.
- Market stall hidden as in s01 (not visible from the chamber anyway).
