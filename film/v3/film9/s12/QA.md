# s12 QA: film 9, shots 12-13 (the false payoff: the first rain), wall_site RAIN

Delivered: `take.mkv.partaa` + `take.mkv.partab` (= `take.mkv` split -b 40M, 64.8 MB; `cat take.mkv.part* > take.mkv`), libx264rgb crf 6,
30 fps, **first_g 881, 166 frames (g 881..1046)**, 720x1280, 12 samples, 2 threads, OIDN (prefilter FAST). Plan range g 887..1040
(29.57-34.70 s); in-handle g 881..886, out-handle g 1041..1046, both rendered in 3D. `meta.json`, `cues.json` (7 cues), `contact.jpg`
(16 frames, cyan line = y 880). Scripts: `shot.py`, `c9.py` (own helper: film8/common.py -> cast9 + set3d9/wall.py), `take_conf.py`,
`deliver.py`, `qa.py` (-> work/qa.txt). One build (two_sections, RAIN; heights lin 20 / general 26 = month 2), cut at g 960 (plan 12 -> 13).

## Beats
| g | what | caption |
|---|---|---|
| 881-911 | rain (set_rain 1); Lin, wet, at the foot of his rice section, looks down at the mortar beside him; the rice mortar goes soft and wet (set_mortar_wet 0.55 -> 1.0 by g 941: glossy joints, milky runs down the bricks); the general's taller grey section at the left edge | "ฝนแรกมาถึงปูน" 29.60, "ข้าวเหนียว" 30.42 |
| 912-959 | he looks up into the rain, worried, palm out | "ยังนิ่ม อยู่เลย" 31.08-31.95 |
| 960 | CUT to the general on top of his section in the rain | "แม่ทัพตะโกนว่า" 31.95 |
| 963-1039 | **lip-sync**: he shouts and laughs (general_rain_shout, wet, pointing down at the site, fist up, body shake); mouth = cast9.talk_mouth | "เห็นมั้ย ขนมเปียกฝนก็เละ!" 33.01-34.68 |
| 1040-1046 | mouth held still (open shout shape), push continues (out-handle) | |

Camera: shot 12 medium from the site on Lin (z 4.5 -> 4.3, 24 mm, push 1.8 D); shot 13 along the general's top (x 15.6 -> 13.6, 20 mm,
push 2.1 D). 0.35 sine + 0.65 linear moves.

## QA-team rules (work/qa.txt)
- **Wide/medium, dense, lit 3D set**: shot 12 shows Lin's brick face with the wet runs, the general's section, ladder, buckets, the mortar
  trough, brick pile; shot 13 the paved walk, crenels, banners, crane, the plain. RAIN light (cool overcast, wet sheen, puddles).
- **Sharp, no blur**: no DOF; Laplacian variance min 326 / median 370 (rain streak overlay only).
- **No text signs**: none.
- **Grounded**: Lin's feet and contact shadow on the wet ground between bucket and trough; the general on the wall-top paving.
- **Heads above y 880**: max head bottom 809 (shot 12), 553 (shot 13). Lin's head centre 0.57-0.58 H; the general's 0.35-0.40 H.
- **Mouths still except the quote**: only the general's mouth moves, g 963..1039 (brief: ~32.0-34.6 s). Lin's worried mouth is static.
- Popcheck: only the planned cut 959 -> 960. No near-still frames (median change 3.70). No black / magenta frames, no retries.

## Hue (hue_report)
```
s12 shot 12 (g 887-959)   red 48.4 orange 29.2 green 2.2 blue 17.5 magenta 2.5  sat 0.16 val 0.46
s12 shot 13 (g 960-1040)  red 27.2 orange 41.8 green 6.3 blue 23.3 magenta 0.7  sat 0.18 val 0.55
```
Low saturation is the set's RAIN preset (wall_API: "RAIN frames are low-saturation"); no grade applied.

## Seconds per frame
11.5 s wall / 22.5 s CPU mean (shot 12 ~15 s wall / 30 s CPU, shot 13 ~8 s wall / 15.6 s CPU), two processes of 2 threads.

## Differences from the plan / notes
- Shot 12 is a closer custom camera on Lin (QA_TECH note: two_sections RAIN figures too small); his look-up is a head / gaze move
  (pitch 0.35 -> -1.1) on "ข้าวเหนียว".
- Lip-sync runs 32.0-34.6 s as the brief asks; the narration's quote itself is 33.01-34.68 s (the general's mouth already moves under
  "แม่ทัพตะโกนว่า"). Trim to g 993..1039 in the conform if the director wants it on the quote only.
