# s09 QA: film 3, shots 9-10, harbor set WINTER

Delivered: `take.mkv` = g 741..925 (185 frames, first_g 741, 720x1280, 12 samples, 2 threads, libx264rgb crf 6).
- g 741..746: in-handle for the 9-frame dissolve from shot 8.
- g 747..836: shot 9. Painting runs g 747..779; the cut-in runs g 780..836.
- g 837..917: shot 10.
- g 918..925: out-handle for the 12-frame dissolve into shot 11.
All handles are rendered in 3D. Raw renders are in `raw/s9` (painting), `raw/s19` (cut-in, to g 843) and `raw/s10` (from g 830). Also `meta.json`, `cues.json`, `contact.jpg`, the scripts `shot.py`, `take3.py` and `deliver3.py`, and `work/qa.txt`.

## Timing
| event | g | s (film) |
|---|---|---|
| shot 9a: low camera along the tank foot, looking up the wall. Tommy (nearest) and both workers paint. set_paint climbs 0 -> 0.142, so the brown rises from the foot past the first seam at z 3. Brush tips are pinned to the wall at the paint line and stroke up and down. Slow push and tilt up | 741-779 | 24.70-25.97 |
| hard cut-in on "tae ko aep ao" (25.9 s): days later, the tank all brown. Tommy crouches and sneaks the tin bucket back under the drip, with his hand pinned to the bail | 780 | 26.00 |
| bucket set down / released | 794 / 797 | |
| glances left (802-815), then right and up toward the drip (818-832), small smirk (833-) | | |
| drops fall into the bucket every 22 f; the fill rises 0.08 -> 0.13 | 797- | |
| dissolve 9 -> 10 (10 f, smoothstep, mixed in this take) | 832-841 | |
| shot 10, Commercial Street: worker1 (pointing back at the tank) and worker2 (holding his belly) laugh in front of the camera. Mouths are held, not animated. Slow eased drift | 837-886 | |
| crash zoom onto the sweating brown seam (camera forward 13 D, lens 22 -> 230 mm, quint) on "thang nguea taek" (29.6 s = g 891) | 887-893 | |
| hold on the seam: dark seep strips, drops, the bucket at its foot. Slow push, out-handle | 893-925 | |

## Staging
| shot | head | width px | centre y (H) | below y 880 |
|---|---|---|---|---|
| 9a | tommy (main) / worker2 / worker1 | 127-148 / 96-109 / 76-86 | 0.49-0.53 | none |
| 9b | tommy | 232-266 | 0.43-0.45 | none |
| 10 before the zoom | worker1 / worker2 | 192-349 / 180-304 | 0.47-0.57 | none |
Pins: the 9b hand on the bail has 0.000 D error. In 9a the brush tips have 0.0 mean error on most frames. On 10-12 frames per painter the brush cannot reach the target point at the bottom of the stroke (max 0.45-0.51 D). There the brush stops short of the wall; at 130 px heads that is a gap of about 15-20 px in the worst frame. head_flip is False everywhere (key from screen-left). Nobody turns their back to the camera, and nobody's mouth moves.

## Camera / pops
Camera speed:
- 9a: min 1.4, median 6.0 px/frame.
- 9b: min 0.56, median 2.4.
- 10: min 0.41, median 3.1. The zoom peak at g 889 is a lens change; it is reported as 8051 px of point travel at depth 8 D.

No frame is static. Frames flagged by the frame-difference check are the cut at g 780 and the crash zoom (889-892). There are no near-still frames, no retried frames and no black or magenta cards.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s09 shot 9 (g 747-836)                         70.0    9.4    0.0    0.1    0.0   16.9    0.6    3.0  0.39 0.54 0.09   OUT: red,orange
s09 shot 10 (g 837-917)                        41.1   10.3    0.1    0.7    0.1   44.6    0.7    2.3  0.47 0.51 0.08   OUT: red,orange,blue
```
Shot 9 is red-heavy: the brown-painted tank fills the cut-in, and the set paints brown at hue 16-24. This is the same red bias as the set's REVIEW (WARM/NOON tank cameras at 79 percent red). Shot 10 is blue in the street half (shaded cobbles, sky) and red on the zoomed seam. Darks are in band (0.08-0.09) thanks to the shaded post and barrel and the street shade. Magenta is 2-3. Render time: 10.6-12.5 s wall / 21-24 s CPU per frame.

## Differences from the plan
- Painting: the paint line only climbs to z 3.4, just past the first seam, during the painting part (brush reach). The cut-in shows the tank already fully brown ("every morning", later).
- The shot 9 cut-in camera is frontal on the bucket (heading +6 to -2), not bucket_insert, so tommy and the bucket stand side by side.
- The shot 10 punch-in is a crash zoom along the street axis onto the seam, which faces down the street, not a cut.
- Runtime set changes, the same as in s06: animated glossy drops, darker seep strips (the set's gloss bloomed yellow), a darker bucket fill, and shade-only foreground post and barrel. harbor.py is not edited.
