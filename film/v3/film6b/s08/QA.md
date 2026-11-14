# s08 QA: film 6b, shots 8-12 (10.48-20.74 s), bakery MORNING

Delivered: `take.mkv` = frames g 308..627 (320 frames, first_g 308, 720x1280, 12 samples, 2 threads, no captions, no audio),
libx264rgb crf 6. 86.7 MB, so committed as `take.mkv.partaa/ab/ac` (`split -b 40M`; rejoin with `cat take.mkv.part* > take.mkv`).
Shots g 314..621 ([g0, g1) = [314, 622)) + 6 handle frames each side, rendered in 3D. Hard cuts in and out.
Also `meta.json`, `cues.json` (13 cues), `contact.jpg`, `compare.jpg` (4 finals beside the ref "pink" big-face CU), `work/qa.txt`.
Scripts: `shot.py` (probe / stills / final), `signs.py` + `raster_fonts.js` (Thai signs), `deliver.py`, `qa.py`; reuses `../../film6/common.py`.

## Shots
| shot | g | framing | picture |
|---|---|---|---|
| 8 | 314-359 | low CU, push up (22->23 mm) | Henry huge from below, squinting at a loaf held by his eye; hanging board "ร้านลุงเฮนรี่" above |
| 9 | 360-398 | ECU, slow arc | loaf pan + tag "500 ก." riding the pan; beam wobbles and stops dead level on "เป๊ะ" (g 392); Henry's face behind the beam |
| 10 | 399-437 / 438-465 | MCU behind the balance -> punch-in CU | drops a crumb (lands g 418, beam dips +4.5), plucks it back (g 436, level); finger wag + smug on "ไม่ขาด ไม่เกิน" |
| 11 | 466-493 / 494-499 / 500-533 | CU kit + basket -> snap zoom -> CU Henry | kit slips the 13th loaf on top (g 480), grins, then worries; Henry turns (g 486); snap zoom; eyes wide (shocked, clenched teeth), purple starts creeping in |
| 12 | 534-591 / 592-621 | low CU, kit in the foreground -> punch-in ECU | YELL: anger_fill 0.25 -> 1.0 (purple), steam puffs from the ears, pointing at kit; kit cowers with sweat, cap tipped back; camera shake grows |

## Rules
- No DOF; sharp throughout. No motion blur (the snap zoom is 5 frames of camera move without blur).
- Mouths: only Henry in shot 12, from the narration RMS envelope (g 536..621: clench / talk_a / talk_b / talk_o, a new drawing every 2 frames).
  Before that every mouth is the static mouth of its expression. In the out-handle g 622-627 the mouth stays clenched.
- Heads above y 880: all frames (qa.txt). Main head centre 0.42-0.55 H, except shot 9 (0.23-0.27 H): that ECU frames the balance tag
  and Henry's face is the background over the beam. Head widths: shot 8 43-55 % W, 10 43-73 %, 11 kit 41-56 % / Henry 71 %, 12 38-67 %.
- Never static: the longest still run is 0 frames, with a median change of 5.9 levels. Framing changes at 360, 399, 438, 466, 494, 534 and 592.
- No black or magenta frames, and no retried frames. The jump at 565->566 (27) is shake + steam, not a pop.

## Colour (complementary)
Two cool-blue area lights (0.12, 0.30, 1.0; 4500 W + 5000 W) wash the back wall and the upper back wall only, so the loaves and brass stay warm.
The blue share goes from 0.3 % (set as built) to 17.6 %:
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 all (g 308-627)                            48.9   21.0    0.5    0.0    2.3   17.6    5.9    3.7  0.33 0.69 0.03
ref a t0001 t0046 t0047                        32.1   44.2    4.9    0.3    0.0    7.0    6.1    5.4  0.34 0.47 0.12
```
The value is high (0.69) and the darks are few, which is the bakery set look. If the conform grades the bakery darker, apply it to all bakery shots alike.

## Cost
16.3 s wall / 32.1 s CPU per frame (two 2-thread processes on 4 cores).

## Differences from the plan
- Shot 8: no magnifying glass in the cast props, so Henry squints at a loaf held up beside his eye instead.
- Shot 10: on removal the crumb hops up into Henry's pinch rather than being picked up. His hand cannot go lower than about 0.45 D above
  the pan, because on a 2D card the hand would fall behind the counter.
- Shot 12: kit's cap is tipped back by animating the cast's `hat_tilt` per frame (-5 -> 38 deg). The cap is not blown off.
- Signs: Kanit Black embedded in the SVG and rasterised with Chromium after `document.fonts.ready` (raster.js does not wait for fonts).
