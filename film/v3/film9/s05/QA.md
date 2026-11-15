# s05 QA: film 9, shots 5-7 (the boss laughs, the nickname), wall_site DAY

Delivered: `take.mkv.partaa..partac` (= `take.mkv` split at 40 MB: `cat take.mkv.part* > take.mkv`; libx264rgb crf 6, 30 fps,
first_g 264, 249 frames g 264..512, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio). Plan range g 270..506
(9.01-16.90 s) + 6 handle frames each side rendered in 3D (g 264..269 = shot 5 set-up backwards, the general still off screen;
g 507..512 = shot 7 set-up continued). Set: the client-approved `set3d9/wall.py` (commit 5d511aa). Also `meta.json`, `cues.json`
(10 cues, film seconds), `contact.jpg` (16 frames, cyan line = y 880). Scripts: `shot.py` (probe / stills / final), `c9.py` (film8/common.py
switched to cast9 + wall.py), `take_info.py`, `deliver.py`, `qa.py` (-> `work/qa.txt`), `sheet.py`, `gp.py` (ground point under a pixel,
for staging). One build (wall_site, DAY), three set-ups joined by the plan's cuts at g 339 and 433.

## Client rules
- **No depth of field**: `cam.data.dof.use_dof = False` + `W.setup_dof(scene, None, None, cam=cam)` at build and before every render.
- **User taste**: wide / medium framings in the dense lit set (cauldron + steam + scaffolds + banners; the low two-shot in front of the
  stove; the workers with the cauldron, the scaffolds and the gate tower behind); calm, always-moving cameras (0.35 sine + 0.65 linear
  pushes / drifts); no text signs.
- **Heads above the caption band**: every head bottom < 880 on every frame (`work/qa.txt`). Main heads: shot 5 general 0.55-0.59 H,
  shot 6 general 0.41-0.43 H / lin 0.46 H, shot 7 workers 0.51-0.59 H.
- **Mouths only on the quote**: the general's mouth moves only g 333..432 (narration 10.98-14.43 s "ข้าวเหนียวเนี่ยนะ เอ็งจะทำขนม
  ให้กำแพงกินเหรอ!"), cast9 `talk_mouth` driven by the narration RMS envelope (smile in the silences). Before g 333 his laugh mouth is a
  static open shape; lin and the workers have static mouths (smile / laughing).

## Timing
| g | what | narration |
|---|---|---|
| 264-296 | shot 5 (cauldron): the general strides in from screen-left (walk cycle), lin stirs on his platform, steam | "แม่ทัพที่คุม" 8.98 |
| 296-300 | he stops at the stove, looks at the rice soup (surprised) | |
| 300-338 | big belly laugh (squash bounce), lin keeps stirring | "งานหัวเราะ" 9.89 = g 300, "ลั่น" 10.61 |
| 333- | lip-sync starts with the quote | "ข้าวเหนียว" 10.98 = g 332 |
| 339 | CUT: low two-shot (two_shot_low) | |
| 339-350 | still laughing | "เนี่ยนะ" 11.87 |
| 345-355 | blends into the mock: points at lin (blink at 350 hides the expression switch) | |
| 355-410 | points and mocks, lip-sync; lin, arms folded, calm smile, looks at him | "เอ็งจะทำขนม" 12.35, "ให้กำแพงกิน" 13.18 |
| 410-432 | blends back into the belly laugh (blink at 414) | "เหรอ!" 13.98 |
| 433 | CUT: three workers laughing and pointing at lin (small at the cauldron behind them) | "คนงาน" 14.43 |
| 488 | laugh peak (lean back) | "ไอ้ช่างขนม" 16.17 = g 488 |
| 507-512 | out-handle | |

## Staging and set-ups
| set-up | camera | figures |
|---|---|---|
| 5 cauldron | (-9.6, 24.6, 5.6) -> (-10.3, 23.6, 5.4), look (-11.8..-12, 12, 2.2), 22 mm | lin on `lin_stir` (platform, z 1.5), mirrored so he stirs into the wok; general walks (-5.7, 17.8) -> (-9.5, 17.4) |
| 6 two_shot_low | the preset pulled back 2.4 D and raised 0.9 D: (-4.3, 24.6, 2.7) -> (-4.6, 24.0, 2.65), look (-6.6..-6.8, 14, 1.9), 22 mm | general (-4.5, 19.4) in front of the plank stack (on the preset mark he stood behind it and read as standing on it); lin on `two_shot_lin` |
| 7 workers | closer medium (QA_TECH 7): (-25.1, 24.9, 3.6) -> (-24.8, 24.4, 3.55), look (-13.5, 13.5..13.8, 1.0), 22 mm | worker_a (-20.4, 22.2), worker_b (-21.05, 21.45) laughing and pointing screen-right at lin; worker_c (-22.7, 20.9) mirrored, points back at him |
Wall heights lin 16 / general 16 keyed every frame (before the race; month 1 = 18 / 21 in shot 10). Steam 1.0, flames keyed every frame.
Sprites 256 px/D (shots 5, 7), 320 px/D (shot 6).

## Checks (`work/qa.txt`)
- Pops: only the two planned cuts (338 -> 339, 432 -> 433). No near-still transitions (< 0.35 levels); frame change median 3.6.
- No black / magenta frames, no retried frames. The general's head crosses the left frame edge g 264-284: he walks in from off screen.
- Fixed after the first final: the laugh <-> mock switch in shot 6 popped (g 350 -> 351, 417 -> 418); now blended over 10 / 8 frames with
  puppet.lerp_pose, the expression change behind blinks; 32 frames re-rendered.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s05 shot 5 (g 270-338)                         14.2   69.1    1.6    0.3    0.0   10.5    2.0    2.2  0.42 0.65 0.03
s05 shot 6 (g 339-432)                         16.0   49.1    1.3    0.1    0.0   27.3    4.5    1.6  0.46 0.60 0.04
s05 shot 7 (g 433-506)                         10.5   64.8    0.3    0.4    0.0   21.7    1.3    1.0  0.51 0.64 0.03
s05 all                                        13.6   60.2    1.0    0.3    0.0   20.7    2.7    1.6  0.47 0.63 0.03
ref a t0062 t0072 (day wide / medium)          23.6   12.5    1.0    0.0    0.0   55.3    2.8    4.7  0.58 0.65 0.14
```
Warm golden DAY of the approved set (orange-heavy; the blue sits in the sky and the shade), value matches the ref; magenta <= 2.2.

## Seconds per frame
16.8 s wall / 33.0 s CPU mean (2 threads, two render processes at once on 4 cores, 12 samples). Above the set's 19-33 CPU s range only by
the cast cards; the set notes this container is ~1.45x slower than round 1.
