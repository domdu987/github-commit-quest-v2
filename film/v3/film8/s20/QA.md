# s20 QA: film 8, shots 20-21 (the ending): desert_ice plain at the dome, SUMMER

Delivered: `take.mkv` split as `take.mkv.partaa` + `take.mkv.partab` (49.9 MB > 45 MB; rejoin with `cat take.mkv.part* > take.mkv`),
libx264rgb crf 6, 30 fps, **first_g 1661, 178 frames** (g 1661..1838, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio).
g 1661..1666 = 6-frame in-handle (the walk + truck continue backward, rendered in 3D); g 1667..1751 = shot 20 (plan 55.57-58.40 s);
g 1752..1838 = shot 21 (plan 58.40 s to the end; g 1838 is the last film frame, N = 1839, no out-handle).
Also `meta.json` (first_g, n_frames, g0 1667, g1 1839, transition_in cut, events), `cues.json` (10 cues), `contact.jpg` (16 frames, cyan
line = y 880), `compare.jpg` (g 1720 beside ref a t0061, g 1812 beside ref b t0029). Scripts: `shot.py` (probe / stills / final),
`deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`; shared helpers `../common.py`. `raw/`, `frames/`, `work/` are not in git.

## Staging
- **Shot 20** (dome_wide build, custom camera): the queue walks east in single file along the bank lane y 8.8 (between mud channels 3
  and 4; the lane leads straight to the porch door): the merchant first (walk cycle, worried, sweat + heat shimmer, the heavy coin purse
  in his right hand), then the woman with her water jar on the shoulder, the old man with his stick, the boy, a second woman fanning
  herself (enters frame at the left / stays partly off left: the queue reads as continuing). Farid waits at the porch door, arms folded,
  calm smile. Walk 0.052 D/frame (28-frame cycle, speed 0.7-0.8, no foot sliding visible at this size). Camera south-west over the mud
  channels, z 2.75 -> 2.7, az 52 -> 55, pitch +5 -> 5.5, 22 mm, trucks 1.85 D east (slower than the queue).
- **Shot 21**: medium two-shot from the south over channel 3 looking north: merchant (19.75, 8.8) left, farid (21.45, 8.8) right before
  the porch (its brick side at the right edge), the couched camel, jars, palms, mat with ice blocks behind. Merchant `merchant_pay`
  (sheepish grin, blush, sweat, scratching the back of his turban, purse held out); farid (mirrored) calmly holds out one ice block
  (g 1798..1812), they **swap at g 1817** (purse -> farid, block -> merchant), the merchant looks down at his one block (grinning ->
  worried at g 1828), farid happy; hold to the end. Camera z 2.45 -> 2.4, az 6 -> 9, slow push 0.75 D.
- Runtime dressing (`dress()`, desert.py untouched): couched camel with red saddle cloth + kilim bags (14.8, 16.6), two standing camels
  far north, 4 date palms, 3 water jars + a straw mat with 3 ice blocks north of the porch, shrubs, 14 rocks. Channels `set_ice('mud')`.

## Client rules
- **No depth of field** (common.Take). Everything sharp, dome steps to the tip.
- **User taste**: wide (shot 20: queue, mud channels, the whole stepped dome, palms) and medium two-shot (shot 21), calm continuous moves,
  warm summer light, no text signs.
- **Heads above y 880**: every head that is on screen is above 880 (qa: the boy / woman2 rows with bottoms > 880 are all frames where
  that head is off frame left, x + w/2 < 0; checked per frame). Shot 20 merchant centre y 715-720 (0.56 H, wide); shot 21 merchant
  645-651 (0.50-0.51 H), farid 666-669 (0.52 H), head widths 130-154 px.
- **Mouths**: only the merchant, only g 1797..1827 ("ข้าจะซื้อหมดเลย" 59.79-60.80 s + 0.10) via `talk_mouth`; elsewhere static
  expression mouths (worried / grinning / smile).

## Timing
| g | what | caption |
|---|---|---|
| 1661-1666 | in-handle: queue walking | ("ด้วยซ้ำ" ends 55.58) |
| 1667-1751 | shot 20: merchant + queue walk to the dome door, farid waits | "ส่วนพ่อค้าน้ำ" 55.58, "ต้องควักเงิน" 56.38, "ซื้อน้ำแข็ง" 57.25, "ทั้งโดม" 57.95 |
| 1752 | CUT to the two-shot | "ตามที่" 58.43 |
| 1752-1796 | sheepish, scratching the turban, purse held out; farid holds the block | "ลั่นวาจาไว้ว่า" 58.82 |
| 1797-1827 | lip-sync; 1798-1812 farid holds the block out; 1817 swap | "ข้าจะซื้อหมดเลย" 59.79-60.80 |
| 1828-1838 | merchant looks at his one block, farid happy; slow push to the end | |

## Checks (`work/qa.txt`)
Popcheck: one jump, the planned cut 1751 -> 1752 (42.7 levels). Near-still transitions: none (median change 2.15 levels). No black /
magenta frames, no retried frames.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s20 shot 20 wide (g 1661-1751)                 12.5   31.1    0.2    0.7    0.0   50.4    3.3    1.8  0.37 0.64 0.05
s20 shot 21 two-shot (g 1752-1838)              9.7   38.8    0.5    0.9    0.0   46.6    1.4    2.1  0.38 0.69 0.02
s20 all                                        11.1   35.0    0.3    0.8    0.0   48.4    2.3    2.0  0.38 0.67 0.04
ref a t0061 (day/sunset wide)                  54.5   26.1    1.9    0.0    0.0    0.0    3.9   13.6  0.49 0.68 0.26
ref b t0029 t0033 (day two-shot)                9.5    9.4    0.0    0.0    0.7   66.0    6.3    8.2  0.27 0.68 0.10
```
Warm summer (orange 31-39, as the set's SUMMER frames) under a blue sky; magenta <= 2.1; shade blue, never magenta. Dark fraction low
(the set's airy look; not graded here).

## Seconds per frame
14.2 s wall / 28.0 s CPU mean (2 threads, two processes at once): shot 20 wide and shot 21 two-shot similar (see meta.json). 178 frames
in ~22 min wall.

## Differences from the plan
- Farid hands the block over by a swap of props (purse and block change hands at g 1817) rather than a separate take-the-purse beat.
- The queue is 4 townsfolk (woman with jar, old man, boy, a second woman fanning); in shot 21 they are off frame (hidden).
