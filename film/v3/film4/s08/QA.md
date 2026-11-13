# s08 QA: film 4, shot 8 (the master laughs: the first quoted line), pagoda set v2, DAY

Delivered: `take.mkv` = `frames/g_0480.png .. g_0599.png` (120 frames, 720x1280, 12 samples, 2 threads, no captions, no audio);
`meta.json` (first_g 480, n_frames 120, transitions, parts, DOF), `cues.json` (8 cues), `contact.jpg`, `compare.jpg`.
Scripts: `shot.py`, `take_cfg.py` + `deliver.py` (QA numbers in `work/qa.txt`). Raw renders + json in `raw/p1..p3`.

Shot 8 = [480, 593) (16.00 .. 19.78 s). Hard cut in from s07 (new sentence). Out-handle g 593..599 rendered in 3D (8C camera keeps
moving): use it for a 10-frame dissolve into s09, or cut at g 592.

## Timing
| part | g | what | ref a |
|---|---|---|---|
| 8A | 480-510 | eye-level two-shot: master near (screen-right) points up-left at the pagoda, smug; kenta far (screen-left) by the pagoda platform, worried; on "หัวเราะ" (g 495) the master bursts out laughing (eyes shut, static grin); slow push | t0011 |
| 8B | 511-563 | snap punch-in g 508-514 (middle g 511) into a low angle (pitch +27) on the laughing master; lip-sync on the quote from g 511 ("เสาที่ไม่ค้ำ"); on "ไอ้หนู" (g 547) he opens his eyes, grins and jabs a finger down toward kenta (off screen-left); drift | t0013 |
| 8C | 564-599 (cut, plan 18.7 s) | three townspeople (merchant, woman2, farmer) laughing and pointing at the pagoda; the master's rigid tower behind them right, the pagoda left; small laugh-bounce on the camera; push | t0015 / t0047 |
Framing changes g 480, 508-514, 564 (1.0 s, 1.7 s with a drift inside, then 1.2 s to the end of the shot).

## Mouths (rule: only inside the quoted line)
Master: closed smirk to g 492, static "grin" g 493-510 (no movement), lip-sync g 511-563 only (a new drawing every 2 frames from
talk_a / talk_b / talk_o, "flat" for one drawing at each word boundary: 530, 547, 557); the quote continues over 8C (to g 596) where he is
off screen. Kenta: static "wavy". Townspeople: static laughing grins (no movement).

## Staging (work/qa.txt)
| part | head | width px | centre x | centre y (H) | below 880 |
|---|---|---|---|---|---|
| 8A | master | 158 -> 183 | 372-418 | 0.52-0.54 | none |
| 8A | kenta (far) | 43-45 | 186-205 | 0.52 | none |
| 8B | master | 212 -> 277 | 255-346 | 0.47-0.52 | none |
| 8C | merchant / woman2 / farmer | 129-143 / 150-169 / 134-149 | 113-146 / 289-310 / 501-529 | 0.47-0.52 | none |
Near/far 8A: 183 / 45 = 4.1. Kenta leaves the frame at the bottom-left edge during the snap (g 512-514 his head crosses y 880 while
exiting); from g 515 he is moved out of the set (the qa.txt kenta numbers for 8B after g 514 are that parking spot, off screen).
head_flip False (DAY key screen-left in all three cameras). Nobody's back to camera.
Popcheck: one pop, the cut 563->564. Near-still: g 480 only (the cut-in frame); no black / magenta frames, no retries, no clipped sprites.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 part 1 (g 480-510)                         12.6   36.9    0.0    0.1    0.0   42.4    4.5    3.5  0.36 0.67 0.02
s08 part 2 (g 511-563)                          8.1    6.0    0.0    0.0    0.0   82.9    1.2    1.8  0.48 0.61 0.06
s08 part 3 (g 564-599)                          7.9   36.4    1.2    0.1    0.2   43.1    4.1    7.0  0.36 0.65 0.04
s08 all (g 480-599)                             9.1   21.2    0.3    0.0    0.1   62.9    2.7    3.6  0.42 0.64 0.05
ref a t0011 t0013 t0015 t0047                  45.4   32.0    1.8    0.2    0.0   10.9    5.3    4.4  0.41 0.47 0.12
```
Blue high / red low against the (interior, red-throne) reference: exterior DAY courtyard with sky; 8B is a low angle into the sky (blue 83).
Shade blue-violet, magenta <= 7.

## Seconds per frame
9.51 s wall / 18.6 s CPU mean (2 threads). Per part: 8A 10.4 / 20.3, 8B 7.2 / 14.0, 8C 12.2 / 24.0.

## Differences from the plan / the reference
- Custom courtyard cameras, not the set's street_eye (the plan's two-shot needs master near + kenta far by the pagoda; street_eye is in the street).
- DOF focus on a world point at the master's head (the card origin is at the feet, which blurred his head in the low angle).
- The master's quote runs to g 596; the plan's cut to the townspeople at 18.7 s (g 564) leaves its last 1 s over 8C, as planned.
