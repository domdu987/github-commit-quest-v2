# QA: first 5 seconds, version 3 (true 3D)

Film: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/out/proto_v3.mp4` (720x1280, 30 fps, 150 frames, 5.000 s, H.264 + AAC 192k Thai narration delayed 0.1 s). Picture frames without captions: `v3/out/frames/f_0001.png` to `f_0150.png` (output frame g is file number g + 1). Blender frames before post: `v3/out/raw/` with one json per frame in `raw/meta/`.

Timing source: `audio/th/hook_timing.json` was already FINAL when the final render started (`provisional = false`, narration WAV present); it was re-read immediately before the render and no polling was needed.

All numbers below are measured on the delivered frames or computed from the camera path that rendered them. Tools: `v3/shots/qa_*.py`, `probe.py`, `popcheck.py` (see `v3/README.md`). Working data: `v3/tmp/shots/` (`motion.json`, `light/`, `parallax_*.json`, `captions.json`, `trackend.json`, `score/`).

## 1. Result in one table

| Check | Target | Measured | Verdict |
|---|---|---|---|
| Light: same surface in shadow / lit (linear luminance) | reference 0.11 to 0.33 (brief); a/t32.0 floor 0.15 measured here; reviewer's pairs 0.08 to 0.25 | median 0.30 to 0.31 on six frames, p10 0.16 to 0.28 (the floor is the 0.16) | inside the brief's band, at its weak end |
| Light: shade cooler and violet | lit hue 24 to 27 -> shade hue 246 to 252 | lit hue 0 to 71 -> shade hue 240 to 314 | yes |
| Light: cast-shadow edge width | 4 to 21 px (brief); a/t32.0 2.1 to 2.5 px near edge, 12.7 px far edge measured here | medians 5.0 to 7.8 px in shots 2 and 3; 11.8 and 21.0 px in the insert (camera 1.3 to 2.2 D from the wall); actors' own shadows 2.0 to 2.8 px | in range; the close insert is at the top |
| Light: actors cast hard shadows | yes | 8700 to 44600 px of actor-cast shadow per frame (0.9 to 4.8 percent of the frame) | yes |
| Light: hero's shadow not on the track (shot 2) | not on the track | 0 of 41 track samples under an actor's shadow at g 52 and g 66 | yes |
| Depth: frame pairs 0.5 s apart explained by a flat 2D zoom or pan | reference A 12 percent, B 43 percent; v2 near 100 | v3 11.1 percent (15 of 135); v2 91.1 percent; reference by the same script A 10.9, B 42.6 | like clip A |
| Depth: near head / far head in the two-shot | 1.36 to 1.46 | 1.40 to 1.47 | yes (1.47 on the last frames before the push) |
| Camera angles | low, high, close insert, snap, whip | insert 1.44 to 1.84 D up, pitched +13 to +23 deg, raking 22 to 39 deg; low angle 1.17 to 1.20 D, +15.2 to +15.9 deg; high angle 3.30 to 3.73 D, -20.3 to -21.3 deg | yes |
| Framing changes in 5 s | at least 4 | 5: snap push 0.33 s, pull-out 1.10 to 1.57 s, snap on the jab 2.00 s, whip 2.30 to 2.60 s (cut 2.433 s), snap push 3.60 to 4.00 s | yes |
| Camera static | never more than 6 frames | 0 frames below 0.25 px per frame (slowest 0.33) | yes |
| Camera linear | never | longest constant-speed run 4 frames | yes |
| Heads above the caption band, centre 0.35 to 0.59 H | y < 880 | lowest head edge 753; main head centre 0.38 to 0.50 H | yes |
| Registration of pencil and eraser | 2 px | 0.00 px by the solver on all 84 pinned frames; track end found in the rendered plates within -2.1 to +1.3 px of the target along the track | yes |
| Final frame cost | 6 s target, 9 s limit | 4.52 s wall (take A, 36 frames) and 5.16 s wall (take B, 12 frames) on 4 threads with the machine to itself; 17.2 and 19.7 CPU s | yes |
| Captions | Thai, hard swaps, x 360, y 900, no head touched | 7 phrases, centre x 359 to 360.5, centre y 892 to 906, height 39 to 67 px, nearest head 104 px above | yes |

## 2. Measured tables

### Timing (from audio/th/hook_timing.json, provisional = False)

| Item | Output frame g | Time s | Rule |
|---|---|---|---|
| Clip length | 150 frames | 5.000 | max(5.0, speech_end 4.214 + 0.4) |
| Shot 2 (framing change centred on) | 39 (pull-out g 33-47) | 1.300 | first beat-2 phrase "ชี้ตรงเข้า" at 1.414 s, picture leads by 3.4 frames |
| Shot 3 (cut inside the whip) | 73 | 2.433 | first beat-3 phrase "แล้วหัวหน้า" at 2.517 s, picture leads by 2.5 frames |
| Jab lands on New York | 60 | 2.000 | phrase "นิวยอร์ก" 1.982-2.517 s |
| Eraser touches the map | 94 | 3.133 | phrase "ก็ลบทิ้ง" starts 3.132 s |
| Rubbing, erase 0 -> 0.60 -> 1.0 | 94 -> 109 -> 122 | 3.133 -> 3.633 -> 4.067 | last phrase "เฉยเลย" 3.637-4.664 s: erase 0.60 to 1.0 under it |
| Hero wide-eyed (closed frame of the blink) | 108 | 3.600 | start of the last phrase |

### Registration of the pinned prop (tip drawn on the card against the world target, through the camera of each frame; 720x1280 px)

| Shot | Prop | Frames g | max px | mean px | solver residual max (D) | arm stretch |
|---|---|---|---|---|---|---|
| 1 insert | pencil on the growing end of the track | 7-38 (32) | 0.00 | 0.00 | 0.0000 | |
| 2 low angle | pencil on the growing end, jab at New York | 39-61 (23) | 0.00 | 0.00 | 0.0000 | |
| 3 two-shot | eraser face on the upper end of what is left of the track | 94-122 (29) | 0.00 | 0.00 | 0.0000 | |

### Heads (projected from the cards; width = head diameter on screen; y from the top; frame 720x1280)

| Shot | Frames g | Actor | Head width px | Centre x px | Centre y px | Centre y / H | Lowest head edge y (must be < 880) |
|---|---|---|---|---|---|---|---|
| 2 low angle (before the snap) | 47-56 | hero | 179 to 188 | 244 to 264 | 603 to 628 | 0.47 to 0.49 | 718 |
| 2 low angle (after the snap) | 67-68 | hero | 252 to 252 | 265 to 270 | 491 to 492 | 0.38 to 0.38 | 607 |
| 3 two-shot (settled) | 80-107 | hero | 221 to 248 | 554 to 562 | 629 to 636 | 0.49 to 0.50 | 753 |
| 3 two-shot (settled) | 80-107 | boss | 158 to 168 | 261 to 308 | 486 to 494 | 0.38 to 0.39 | 579 |
| 3 after the snap push | 120-149 | hero | 288 to 310 | 533 to 536 | 600 to 601 | 0.47 to 0.47 | 748 |
| 3 after the snap push | 120-149 | boss | 186 to 196 | 163 to 191 | 436 to 468 | 0.34 to 0.37 | 563 |

- near head / far head, 3 two-shot (settled): 1.40 to 1.47 (reference two-shots 1.36 to 1.46)
- near head / far head, 3 after the snap push: 1.55 to 1.59 (reference two-shots 1.36 to 1.46)

### Camera per shot (true camera path)

| Shot | Frames g | Height above the floor (D) | Pitch (deg, + = up) | Yaw (deg, + = looking toward +x) | Corner speed px/frame min / median / max |
|---|---|---|---|---|---|
| shot1 | 0-39 | 1.44 to 1.84 | +13.0 to +23.0 | -39.0 to -10.3 | 2.73 / 32.43 / 153.5 |
| shot2 | 47-72 | 1.17 to 1.20 | +15.2 to +15.9 | +8.0 to +28.3 | 0.69 / 7.38 / 202.1 |
| shot3 | 79-149 | 3.30 to 3.73 | -21.3 to -20.3 | -10.1 to -7.6 | 0.33 / 1.86 / 33.7 |

### Framing changes (camera corner speed above 12 px per frame)

| Move | Frames g | Start s | Peak s | End s | Peak px/frame | Peak / mean speed |
|---|---|---|---|---|---|---|
|  | 0-1 | 0.000 | 0.000 | 0.067 | 13 | 1.03 |
|  | 10-46 | 0.333 | 0.467 | 1.567 | 154 | 2.35 |
|  | 60-64 | 2.000 | 2.067 | 2.167 | 110 | 1.79 |
| contains the cut at g 73 | 69-77 | 2.300 | 2.400 | 2.600 | 202 | 1.93 |
|  | 113-116 | 3.767 | 3.800 | 3.900 | 34 | 1.40 |

- longest static run (camera slower than 0.25 px per frame): 0 frames; slowest frame 0.33 px per frame
- longest constant-speed (linear) run while moving: 4 frames [[20, 21], [25, 26], [27, 28], [40, 41], [96, 99]]

- delivered frames of take A rendered with 2 threads (two processes side by side): 37 frames, 12 samples: wall 9.26 s mean (8.69 to 9.97), CPU 18.10 s mean (17.15 to 19.21) per frame; frames re-rendered by the black-card check: []
- delivered frames of take A rendered with 4 threads (one process, machine to itself): 36 frames, 12 samples: wall 4.52 s mean (4.25 to 4.98), CPU 17.21 s mean (16.25 to 19.09) per frame; frames re-rendered by the black-card check: []
- delivered frames of take B rendered with 2 threads (two processes side by side): 77 frames, 12 samples: wall 10.26 s mean (8.97 to 11.23), CPU 20.15 s mean (17.58 to 22.73) per frame; frames re-rendered by the black-card check: []

### Light on our frames (measurement passes of the film frames, 720x1280)

| Frame g | Sunny / lit / in cast shadow (share of frame) | Same surface shade / lit, linear p10 / median / p90 | The same as display luma, median | Lit -> shade colour (hue) | Cast-shadow edge 10-90 %, p10 / median / p90 / max px (n) | Actor-cast shadow px (share) | Actor shadow edge median px | Track samples under an actor's shadow |
|---|---|---|---|---|---|---|---|---|
| 10 | 0.93 / 0.63 / 0.20 | 0.27 / 0.30 / 0.42 | 0.58 | #836a4a -> #453950 (34 -> 271) | 8.8 / 11.8 / 13.9 / 16.0 (796) | 16003 (0.017) | 2.0 | 12 of 41 visible samples (any cast shadow: 0) |
| 26 | 0.93 / 0.68 / 0.15 | 0.28 / 0.30 / 0.38 | 0.57 | #75776c -> #40405b (71 -> 240) | 12.8 / 21.0 / 27.5 / 38.8 (563) | 8733 (0.009) | 2.5 | 1 of 41 visible samples (any cast shadow: 0) |
| 52 | 0.73 / 0.28 / 0.38 | 0.24 / 0.31 / 0.50 | 0.62 | #88514a -> #462b4e (7 -> 286) | 2.2 / 6.2 / 10.8 / 14.2 (359) | 23993 (0.026) | 2.8 | 0 of 41 visible samples (any cast shadow: 0) |
| 66 | 0.74 / 0.34 / 0.32 | 0.20 / 0.31 / 0.50 | 0.62 | #8e3d3d -> #492b42 (0 -> 314) | 3.8 / 7.8 / 14.5 / 19.2 (471) | 44587 (0.048) | 2.2 | 0 of 41 visible samples (any cast shadow: 0) |
| 100 | 0.82 / 0.32 / 0.44 | 0.16 / 0.30 / 0.45 | 0.57 | #bf554e -> #53314f (4 -> 307) | 2.0 / 5.2 / 7.8 / 12.2 (481) | 17098 (0.019) | 2.6 | 3 of 41 visible samples (any cast shadow: 1) |
| 125 | 0.77 / 0.30 / 0.41 | 0.16 / 0.30 / 0.49 | 0.59 | #c8544f -> #53314f (2 -> 307) | 2.0 / 5.0 / 7.2 / 12.5 (430) | 23653 (0.026) | 2.5 | 0 of 0 visible samples (any cast shadow: 0) |

### Share of frame pairs 0.5 s apart that a flat 2D zoom or pan explains

| Input | Pairs | Flat-2D pairs | Share | Median inlier ratio F / H / similarity (matched pairs) |
|---|---|---|---|---|
| reference clip A, stills 0.5 s apart (published: 12 percent (16 of 129)) | 129 | 14 | 10.9 % | 0.50 / 0.24 / 0.11 |
| reference clip B, stills 0.5 s apart (published: 43 percent (55 of 129)) | 129 | 55 | 42.6 % | 0.62 / 0.32 / 0.28 |
| v2 (flat), v2/out/frames, every pair g, g + 15 | 135 | 123 | 91.1 % | 0.72 / 0.62 / 0.61 |
| v3 (3D), v3/out/frames, every pair g, g + 15 | 135 | 15 | 11.1 % | 0.58 / 0.42 / 0.13 |

RATIO = 0.51 (a pair is flat when the similarity keeps at least RATIO of the fundamental-matrix inliers), calibrated on the reference stills.


### Notes on the tables

- **Registration.** The 0.00 px is the solver's own residual: the tip of the drawn prop is placed where the sight line from the lens to the world target cuts the actor's card, and the arm is solved to it (the hero's arm stretches up to the puppet's limit 1.30 for the first strokes at the storm symbol). It is not an independent measurement. Two independent looks: (1) `qa_trackend.py` finds the end of the red ink in the pixels of the 15 actor-free plates and compares it with the target pixel: along the track -2.05 to +1.31 px (mean -0.47); sideways within 1 px on g 37 to 45, 2.95 px on g 36, and 6.2 to 6.8 px on g 12 to 15, where the red storm symbol next to the 5 to 13 percent long line skews the fitted axis (a limit of the check, the crops show the point on the line). (2) 3x crops of the rendered frames with a cross-hair on the target, `v3/tmp/shots/regcrops_pencil.jpg` (g 8, 12, 20, 28, 34, 48, 56, 60) and `regcrops_eraser.jpg` (g 94 to 121): viewed, the pencil point sits on the cross-hair and on the end of the line in all eight; the eraser block is centred on its target. The stage review measured the same mechanism with rendered markers at 0.45 px worst.
- **Light.** Each row is a film frame rendered again as passes (key on, key at zero, key without shadows, key without the actors' shadow casters; `qa_light.py`). "Same surface shade / lit" compares the same pixels with and without the key, after the grade, in linear luminance. The reference cannot be measured that way, so for the reference a lit and a shaded patch of one surface were read from the still: a/t32.0 floor planks `#926546` lit against `#2c2938` in the newspaper's shadow = 0.152 linear (0.39 display), hue 24 -> 252; edge of that shadow 2.1 to 2.5 px at the near side, 12.7 px at the far side (`v3/tmp/shots/ref_light_a32.json`, tool `set3d/review/rmeasure.py`). The set review reports 0.083 to 0.25 for four reference pairs and 1.7 to 12.6 px. Our floor reads 0.16, our walls, map and wainscot 0.28 to 0.31: the median is at the weak end of the brief's 0.11 to 0.33.
- **Track under shadow.** g 10: 12 of 41 samples are the 2 percent of line right under the pencil, whose own shadow touches its point (it should). g 100: 3 of 41 next to the eraser, the chief's forearm shadow over the stretch he is rubbing (physically right, see `set3d/API.md` 5). In shot 2 nothing falls on the track.
- **Flat-2D share.** SIFT matches between frames 15 apart, RANSAC at 1 px for a fundamental matrix, a homography and a similarity; a pair counts as "flat 2D zoom or pan" when the similarity keeps at least 0.51 of the fundamental-matrix inliers, a pair with fewer than 30 matches (a cut, a whip) counts as not flat. The 0.51 was set once so that the reference stills reproduce the published shares (A 10.9 against 12.4 percent, B 42.6 against 42.6 percent). The 15 flat pairs of v3 start at g 0, g 20 to 29 (inside the insert, where one plane, the wall map, fills the frame during the follow move), g 43, 44 and g 55, 57, 59 (inside the low-angle medium, between the pull-out and the snap). No pair of shot 3 is flat. Nine pairs have too few matches (they straddle a snap, the pull-out or the whip).
- **Head ratio.** 1.47 is reached on g 105 to 107, the end of the drift before the push; after the push onto the hero the ratio is 1.55 to 1.59 by design (the camera is closer to him).

### Captions (measured on the MP4 against the same frames without captions, `qa_captions.py`)

| Phrase (as in the timing file) | Beat | Frames g shown | Box x0, y0, x1, y1 | Height px | Centre x, y | Gap to the nearest head above it (px) |
|---|---|---|---|---|---|---|
| เขาลากเส้น | 1 | 3-15 | 224, 873, 496, 925 | 53 | 360.0, 899.0 | no head above |
| บนแผนที่อากาศ | 1 | 16-42 | 168, 863, 553, 926 | 64 | 360.5, 894.5 | 133.5 |
| ชี้ตรงเข้า | 2 | 43-59 | 250, 859, 469, 925 | 67 | 359.5, 892.0 | 132.7 |
| นิวยอร์ก | 2 | 60-75 | 257, 874, 462, 926 | 53 | 359.5, 900.0 | 201.1 |
| แล้วหัวหน้า | 3 | 76-93 | 225, 873, 493, 925 | 53 | 359.0, 899.0 | 132.4 |
| ก็ลบทิ้ง | 3 | 94-109 | 268, 862, 451, 925 | 64 | 359.5, 893.5 | 104.4 |
| เฉยเลย | 3 | 110-139 | 267, 887, 453, 925 | 39 | 360.0, 906.0 | 129.5 |

Text is copied from the timing file unchanged, each with its `caption_style_prefix` `{\fnKanit Black\fs88}` (written to `v3/out/caps_burn.json`), anchored at (360, 900) by `assemble.py`, hard swaps, shown on every frame of its interval. The tall stacks (ชี้, เข้า, ที่, ก็, ทิ้ง) rise to y = 859; no caption touches a head. Tone marks, upper vowels and the thanthakhat of ยอร์ก were looked at on crops of all seven phrases (`v3/tmp/shots/caption_crops.jpg`): placed correctly. The scoring tool reads a text height of 45 px against the reference's 33 to 42 px for Latin captions; the size comes from the timing file's prefix and was not changed.

### Render time (final quality: 720x1280, Cycles CPU, 12 samples, no denoiser, bloom and grade in Blender)

| Run | Other jobs | Frames | Wall s per frame | CPU s per frame |
|---|---|---|---|---|
| Machine to itself, one process, 4 threads, take A (g 33 to 68, the re-render of pass 1; these are delivered frames) | none | 36 | 4.52 mean (4.25 to 4.98) | 17.2 |
| Machine to itself, one process, 4 threads, take B (g 96 to 101, 123 to 128, timing run) | none | 12 | 5.16 mean | 19.7 |
| Production run: takes A and B as two processes, 2 threads each | only each other | 150 | 8.7 to 10.0 (A), 9.0 to 11.2 (B) per process; 150 frames in 791 s = 5.3 s per finished frame | 17.2 to 19.2 (A), 17.6 to 22.7 (B) |
| For comparison at 16 samples, 4 threads, alone | none | 4 | 6.2 to 7.0 | 23.5 to 27.0 |
| Plate + matte for a streaked frame (pass 2), 4 threads | none | 17 | 7.1 for both | not recorded |

No other agent's job was running during any of these: every process listing taken during the session showed only this task's own renders (the machine had been restarted and was idle, load 0.1 to 0.4, when the work began). 12 samples were chosen because 16 samples cost 6.2 to 7.0 s and crops of 8, 12 and 16 samples were indistinguishable at film size (`v3/tmp/shots/look5.png`). No frame was re-rendered by the black-card check. Draft frames (360x640, 6 samples) cost 1.4 to 1.7 s at 2 threads.

### Likeness score (`v2/eval/score.py`; it measures colour statistics, line widths, camera motion and caption geometry, not light direction, shadows or perspective)

| Input | Characters (0.30) | Colour (0.15) | Density and light structure (0.15) | Camera and edit (0.20) | Animation life (0.10) | Captions (0.10) | Index | Strict index |
|---|---|---|---|---|---|---|---|---|
| `v3/out/proto_v3.mp4` | 1.000 | 0.978 | 0.980 | 1.000 | 1.000 | 0.963 | **0.990** | 0.990 |
| `v2/out/proto_v2.mp4` | 1.000 | 0.980 | 1.000 | 1.000 | 1.000 | 1.000 | **0.997** | 0.997 |

v3 rows that are "near" instead of "in range": black point p1 0.123 (0.080 to 0.120), contrast p95 - p5 0.563 (0.600 to 0.750), mean luma of the top third 81 (85 to 135) and of the middle third 103 (105 to 150), caption centre y 899.0 (899.5 to 905.5), caption text height 45 px (33 to 42). v2 row "near": hue of the darkest tenth 353 (250 to 345). Snap reframings found by the tool: v3 f11-f46, f61-f64, f70-f78, f113-f116; v2 five. Both scorecards: `v3/tmp/shots/score/proto_v3/scorecard.md`, `v3/tmp/shots/score/proto_v2/scorecard.md`. The tool was built from the numbers v2 was made to meet and cannot see the three things v3 changes (its own README says so); the 0.007 difference is inside its scatter for 5 s clips.

## 3. Self-review

Frames were viewed at full size next to the reference stills a/t13.5, a/t16.0, a/t27.5, a/t32.0, a/t58.5, b/t07.0, b/t10.0, b/t24.5 (`v3/out/compare_v3.png`, `v3/out/aspects_v3.png`, `v3/tmp/shots/pass1_low.jpg`, `pass1_high.jpg`), plus every one of the 150 frames on three sheets (`v3/tmp/shots/all_1.jpg` to `all_3.jpg`).

### Before the final render (drafts at 360x640, every frame)

| Found | Fix |
|---|---|
| The work found on disk from the interrupted run (`film.py`, `timing.py`, two contact sheets of every 3rd frame) was sound and already used the final timing; nothing of it had been rendered at full quality. | Continued from it; all 150 frames were rendered again from scratch. |
| Pencil point 40 to 57 px short of the storm symbol on g 2 to 16 (arm out of reach). | Pencil held flatter at the start (-22 instead of -38 degrees) and arm stretch solved per frame up to the puppet's limit 1.30: 0.00 px. |
| A slice of the hero's head cut into the left edge of the insert on g 0 to 12. | Look point of the insert moved 0.31 D to the right. |
| Two-shot too wide (chief's head 135 px, near / far 1.32, the rubbing hardly readable). | Camera 1 D closer and 0.1 D lower: heads 158 to 248 px, ratio 1.40 to 1.47; face framing re-aimed so that the pink smudge stays in frame left of the chief. |
| Rubbing mostly happened after the push, behind the chief's body. | Erase reaches 0.60 by the last phrase and 1.0 when the push lands (g 122). |
| Shot 3 camera parked for 5 frames around g 86 and at the end. | 22 percent of every take-B segment travels at constant speed: slowest frame 0.33 px. |

### Pass 1 (first complete final render)

Five largest visible differences against the reference:

1. LIGHT. No light source in shots 1 and 2: reference interiors (a/t27.5) hang glowing bulbs with a halo in the frame; our shot 2 showed only the dark rim of a lamp shade. **Fixed**: the low-angle camera stands 0.6 D farther back and aims 0.16 D higher, so the pendant lamp at (0.4, -2.6, 4.27) hangs into the top right with its bulb and bloom on g 44 to 61.
2. DEPTH. The low-angle medium looked at the map wall almost square-on and showed a strip of ceiling; a/t16.0 has the ground running to a far vanishing point. **Improved** by the same change: ceiling boards, a beam, the picture rail, floor boards and the rug now converge, and a prop stands close to the lens at the left edge. A first try (camera at x = -1.33) put the desk corner as a dark wedge over 15 percent of the frame; the camera now stays at x > -1.05. 36 frames (g 33 to 68) re-rendered.
3. LIGHT. The actors' shadows lie on the wall and wainscot behind them and as two leg lines on the floor; in a/t32.0 and a/t58.5 the whole figure lies on the ground. Not fixable in the staging: the set's sun stands 10 degrees above the horizon so that the map wall is lit (set review, gap 1).
4. LIGHT. Shade is shallower on the walls (0.28 to 0.31 of lit) than in the reference pairs (0.08 to 0.25); the floor matches (0.16). Left as calibrated by the set review (deeper shade darkens the wall behind the heads).
5. CAMERA. Our high-angle two-shot is tighter than a/t58.5 (heads 158 to 248 px against about 120 px; floor 40 percent of the frame against 60). Kept: the rubbing has to read on a phone.

### Pass 2 (after the re-render)

1. CAMERA / LIGHT. On the 18 fast frames outside the whip (snap push g 12 to 15, pull-out g 35 to 45, snap on the jab g 61 to 63) the streak smeared the hero's face and the pencil; in the reference the plate streaks and the characters stay sharp. **Fixed**: for those frames a plate without the actors and a matte of the actors are rendered (`render_layers.py`), the plate is streaked along the true camera motion and the actors of the film frame are laid over it sharp (`post.py`); the 6 whip frames stay streaked whole. Viewed: `v3/tmp/shots/pass2_streak.jpg`.
2. LIGHT. Actor shadows on the wall instead of the floor: as pass 1, not fixable here.
3. LIGHT. The picture is a little darker than the reference in the upper two thirds (mean luma 81 and 103 against 85 to 135 and 105 to 150) and less contrasty (0.563 against 0.60 to 0.75). Set gains; not changed.
4. DEPTH. A closed room 9 D deep: no far vista, no atmospheric separation, no defocused background as in clip B's close-ups.
5. CAMERA. After the push the chief's body hides the lower half of the rubbed-out track and his eraser passes in front of his own waistcoat for six frames (g 116 to 122); the pink smudge shows only left of his head. Accepted: the two-shot before the push shows the rubbing in the clear.

## 4. Known gaps, by visual impact

1. Actors' shadows fall on the wall behind them, not as whole figures on the floor (sun 10 degrees high; a set decision).
2. Wall shade 0.28 to 0.31 of lit against 0.08 to 0.25 in the reference; picture slightly darker and lower in contrast than the reference in the upper two thirds.
3. Shot 2 ends at a wall 5 D away; the reference low angle has an open horizon.
4. The red track is a ribbon 0.038 D wide: about 30 px in the insert, where it reads as a marker stroke rather than a pencil line.
5. After the push the chief hides the lower half of the erased track (pass 2, item 5).
6. No speed lines on the hero's shock (v2 drew them), no light shafts or dust glow from the window.
7. The pull-out joins shots 1 and 2 without a cut; the scoring tool therefore counts one shot before the whip.
8. Registration is exact by construction; the independent image check covers the track end only (within 2 px), the tip itself was checked on crops.
9. Caption height 45 px against 33 to 42 px for the reference's Latin captions (Thai stacks at the size given by the timing file).
