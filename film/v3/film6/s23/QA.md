# s23 QA: film 6, shot 23 (the hooded man walks to the square centre, the crowd parts, hood off -> hard cut to the King's inspector), market AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 1841, 100 frames = g 1841..1940, 720x1280, 12 samples, 2 threads, denoise FAST,
no captions / audio), `frames/` (local, gitignored), `meta.json`, `cues.json` (7 cues), `contact.jpg`, `compare.jpg` (g 1870 beside ref a
t0062, g 1925 beside ref a t0051), `work/qa.txt`. Scripts: `shot.py`, `deliver.py` + `deliver_lib.py`.
Range: plan 61.57-64.50 s -> [g 1847, g 1935); handles 6 + 6 rendered in 3D.

## Client rules
- **No depth of field / no blur**: DOF off at build and before every render. No streaks. (Soft cloud edges = the set's painted sky.)
- **Heads above the caption band**: every visible head bottom <= 895 -> checked: no head bottom below y 880 (inspector centre 0.44-0.51 H,
  royal 0.46-0.47 H, townsfolk 0.50-0.63 H). Low angles push background heads down toward the band, so in 23b the parted townsfolk are
  restaged beside the inspector (not behind) and one (man1b) is hidden; in 23c the crowd is out of frame.
- **Mouths**: no quoted line -> static mouths only (townsfolk "shocked" O, stunned; inspector closed).
- **Continuity**: hooded until the hood is thrown back (hood 1 -> 0.15 over g 1898-1911, never the bare hooded head), blink g 1913-1915,
  HARD CUT g 1916 to `inspector_royal` (hood down, royal tabard with three lions, gold chain of office), as WORKER6 asks.

## Framings
| g | framing | action | narration |
|---|---|---|---|
| 1841-1886 | 23a eye level in the square, 24 mm, looking north (slow push) | the hooded man strides toward us out of the crowd (walk cycle 18 f); four townsfolk step aside left / right (g 1846-1878) and turn their heads after him | "ชายคนนั้น เดินไปกลางตลาด" |
| 1887-1915 | 23b low medium (pitch +14..15), 24 mm | he settles into a planted stance (5-frame blend g 1886-1890), both hands up, throws back the hood (g 1898-1911); blink g 1913-1915 | "ถอดผ้าคลุมออก" 63.11 (g 1896) |
| 1916-1940 | 23c HARD CUT, lower and closer (pitch +31..34), 26 mm | inspector_royal: stern, one hand raised, chain glinting; blink g 1934 | "เขาคือ ผู้ตรวจ..." 64.05 |

## Checks (`work/qa.txt`)
- Heads: inspector 92-220 px, royal 309-317 px, townsfolk 98-196 px.
- Popcheck (cuts 1887, 1916 excluded): none (the walk -> stance snap at g 1890 of the first render was fixed with a lerp_pose blend and
  g 1886-1890 re-rendered). No near-still pairs; median frame change 2.9 levels. No black / magenta frames, none retried.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s23 shot 23 (g 1847-1934)                      31.9   19.9    0.4    0.3    0.1   40.7    3.1    3.6  0.43 0.70 0.03
s23 23a walk (g 1841-1886)                     47.8   20.9    0.6    0.4    0.1   23.2    3.3    3.7  0.39 0.70 0.02
s23 23b-c reveal (g 1887-1940)                 21.3   18.1    0.3    0.2    0.0   53.9    2.6    3.4  0.48 0.70 0.05
ref a t0062 t0072                              23.6   12.5    1.0    0.0    0.0   55.3    2.8    4.7  0.58 0.65 0.14
```
The low angles fill with sky (blue 54, like the ref day exteriors at 55). Market AFTERNOON is light with few deep darks (set look,
bakery_API 7); no magenta cast (3.6).

## Seconds per frame
13.0 s wall / 24.3 s CPU mean (2 threads, two processes at once). Sprites 400 px/D (inspector), 256 px/D (townsfolk).

## Differences from the plan
- Plan preset `square_eye` is used as the direction (eye level, looking north) with custom closer cameras; the walk is toward the
  camera (no back to camera) rather than across. Pillory / balance are off to the sides of the 23a frame (balance arm at top right).
- Townsfolk are woman1 x2 + man1 x2 (no extra crowd cast exists). Guards are not in this shot.
