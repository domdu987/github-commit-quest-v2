# s28 QA: film 7, shots 28-29 (91.49-99.33 s): the painting is back, the crowd, the match-dissolve, her smile

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 2739, 247 frames = g 2739..2985, 720x1280, 12 samples, 2 threads, denoise
FAST, no captions / audio). g 2745..2979 = shots 28-29 ([g0, g1) = [2745, 2980)); g 2739..2744 in-handle and g 2980..2985 out-handle,
rendered in 3D (6 frames each). transition_in = dissolve (from s26, the Florence shop). Also `meta.json`, `cues.json` (9 cues),
`contact.jpg` (16 frames, cyan line = y 880), `compare.jpg` (g 2800 beside ref a t0015, g 2975 beside ref a t0105).
Scripts: `shot.py` (probe / stills / final, 6 set-ups), `deliver.py` (also does the match-dissolve), `qa.py` (-> `work/qa.txt`).

## Set-ups (framing change every 1.2-1.6 s)
| id | g | shot | what | camera |
|---|---|---|---|---|
| 1 | 2739-2780 | 28 | eye level at the rope: she hangs alone again ("ภาพที่เคยไม่มีใครมอง"), then four visitors stream in from both frame edges (walk cycles, g 2751-2776) and stop at the rope, turned to her | 24 mm, slow push, z 2.3 |
| 2 | 2781-2829 | 28 | CUT on "กลายเป็นภาพ" (92.70): reverse from beside her: 15 faces packed behind the red rope looking up at her (stare / point / gasp), edging forward | 18 mm, slow push |
| 3 | 2830-2864 | 28 | side view along the wall: the crowd in profile pressing toward her, she in her gilt frame and glass on the right | 22 mm, slow track |
| 4 | 2865-2911 | 29 | high oblique over the queue lanes: the EMPTY wall (four hooks, unfaded patch), the reopening queue staring | 22 mm, slow linear push |
| 5 | 2900-2945 | 29 | the same camera path: the painting back, 15 people pressed to the rope pointing; deliver.py cross-dissolves id 4 -> id 5 over g 2900-2911 (12 f, identical camera: the match-dissolve); then the push accelerates toward her | 22 mm |
| 6 | 2946-2985 | 29 | punch-in on "ทำให้มันดัง" (98.54): ECU of her face behind the glass, slow push in to the smile (to the end + handle) | 30 mm |

## Client rules
- **No depth of field**: `common.Take`; everything sharp (the far salon hang in set-up 2 included).
- **Mouths**: no quoted line -> no lip-sync; STORY `mouth` keys dropped (crowd_point's talk_o), static expression mouths.
- **Heads above y 880** (all visible heads, every frame): max head bottom 822 / 858 / 836 / 843 / 868 px (set-ups 1-5). Main head
  centres 0.37-0.57 H in set-ups 1-3; the wide queue set-ups 4-5 range 0.43-0.63 H (wides exempt). Set-up 6 has no actor.
- **Dense set**: the salon hang on every wall, torchères, rope stanchions, the queue lanes; crowds of 4-15 cast7 visitors.

## Checks
Popcheck: jumps only at the four cuts (2780/2781, 2829/2830, 2864/2865, 2945/2946). Near-still: g 2739 only (first in-handle frame,
she hangs alone, camera push just starting). No black / magenta frames, no retried frames.
Gotcha found here: with 8+ crowd cards (+ shadow proxies, contact decals) stacked along one ray, the set's `transparent_max_bounces = 8`
turned the crowd's top into an opaque grey block hiding the painting: shot.py sets 64.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s28 set-up 1 (g 2739-2780)                     59.3   36.0    1.6    0.5    0.0    0.6    0.3    1.7  0.59 0.62 0.02
s28 set-up 2 (g 2781-2829)                     42.3   38.8    0.4    0.1    0.0    3.1    2.0   13.3  0.33 0.53 0.10
s28 set-up 3 (g 2830-2864)                     61.9   29.5    2.6    0.1    0.0    0.3    0.5    5.0  0.53 0.62 0.03
s28 set-up 4 (g 2865-2911)                     43.2   50.5    4.0    0.4    0.0    0.4    0.2    1.3  0.42 0.65 0.00
s28 set-up 5 (g 2900-2945)                     35.6   57.9    4.2    0.4    0.0    0.7    0.1    1.2  0.42 0.65 0.00
s28 set-up 6 (g 2946-2985)                     53.3   37.5    6.7    0.0    0.0    0.2    2.0    0.2  0.37 0.62 0.01
s28 all                                        50.0   41.7    3.2    0.3    0.0    0.8    0.7    3.3  0.44 0.61 0.03
ref a t0015                                    61.5   22.6    0.2    0.0    0.0   11.9    1.2    2.6  0.46 0.49 0.06
ref a t0105                                    32.0   57.1    0.8    0.0    0.0    7.4    1.8    1.0  0.30 0.50 0.06
```
Red damask + gold close to ref a t0015 (red 50-62). Magenta 13.3 in set-up 2 is the cast's aubergine skirts / purple hat ribbons filling
the frame (costume colour, not shade; the shade there is blue-grey). Not graded.

## Seconds per frame
18.18 s wall / 35.24 s CPU mean (12 samples, 2 threads, two render processes at once on 4 cores; up to 18 crowd cards).

## Differences from the plan / notes
- The crowd cannot turn its back (2D cards): set-up 1 has them in profile, set-up 2 is the reverse angle (faces toward her = toward the
  lens), set-up 3 profile; the high queue shots show 3/4 faces as the set's placeholders do.
- The match-dissolve is inside the take (deliver.py, g 2900-2911); both sides are rendered with the identical camera.
- First final rejected by QA (heads below y 880 near the end of the shot-29 push and in set-up 3): cameras re-aimed, the nearest queue
  members removed, set-ups 3-5 re-rendered (`work/old_raw`).
