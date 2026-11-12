# s15 QA: film 2, shot 15 (the August night gathers), tower set DUSK -> NIGHT_STORM

Delivered: `take.mkv` = frames g 1143..1254 (112 frames, first_g 1143, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), `meta.json`, `cues.json`,
`contact.jpg` (16 frames, label strip shows the storm share of the frame), take script `shot.py`, delivery `deliver.py` (uses `../s12/deliver_lib.py`).
Raw passes `raw/dusk`, `raw/storm` with per-frame json, numbers in `work/qa.txt` (not in git).

## Method
Two true-3D passes of one camera move: `T.build("DUSK")` and `T.build("NIGHT_STORM")`, both with set_rod(0) (that night there is no rod), no
actors, market stall hidden. In both passes the sky dome turns slowly (0.055 deg per frame) so the clouds drift. In the storm pass the
lit windows are split into 4 random groups whose emission is keyed on one after another (g 1196, 1209, 1222, 1234, 5-frame ease) and one far
sheet-lightning flicker is keyed (g 1238-1240, flash 0.25-0.32). `deliver.py` mixes the passes per pixel with a cloud-front mask: storm
where P(g) + N(x, y, g) - y > 0 (y = row / 1280), soft over +-0.07 H; P eases (smoothstep) from -0.2 at g 1170 to 1.3 at g 1242; N is
4-octave value noise (amplitude 0.11 H) drifting 2.5 px/frame to the right; just behind the front the picture is darkened by up to 22 percent
(the leading edge of the cloud bank). The front enters the sky at the top on "สิงหาคม", covers half the frame on "เมฆดำก็ตั้งเค้า" (g 1197-1219) and
passes over the square on "เหนือเมือง อีกครั้ง"; under it the golden light turns to the blue storm night and the windows come on.

## Timing
| event | g |
|---|---|
| in-handle (12-frame dissolve from shot 14), pure dusk | 1143-1150 |
| shot 15 starts, dusk, slow push + tilt up | 1151 |
| cloud front enters the frame / storm share 0.34 / 0.84 / 1.0 | 1187 / 1199 / 1215 / 1231 |
| speed change of the push (G_CLOUD) | 1197 |
| reframe up toward the sky over the tower | 1214-1224 |
| window groups on | 1196, 1209, 1222, 1234 |
| far flicker | 1238-1240 |
| out-handle (10-frame dissolve into shot 16), pure storm | 1248-1254 |

## Camera (fastest of 9 screen points at depth 35 D, px/frame)
min 0.28, median 1.55, peak 27.8 (g 1219, the reframe); static runs none; constant-speed runs 1163-1176 (14 f, middle of the first slow
segment: a 0.2 linear share is mixed in so it never parks) and 1237-1241. The changing cloud front itself changes the frame every frame.
Popcheck: no pops; one near-still transition 1253 -> 1254 (last handle frame, the camera settles). No magenta frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s15 dusk part (g 1151-1170)                    52.6   12.2    0.0    0.1    0.0    8.5   17.6    9.0  0.43 0.70 0.00
s15 front passing (g 1171-1230)                36.4    7.4    0.2    0.1    0.0   41.7    9.3    4.8  0.52 0.55 0.01
s15 storm part (g 1231-1247)                    0.0    0.2    0.9    0.0    0.0   98.3    0.6    0.0  0.62 0.40 0.00
s15 all (g 1143-1254)                          34.0    7.4    0.3    0.1    0.0   43.2    9.9    5.1  0.52 0.56 0.01
ref a t0072 t0080                               3.9    0.9    0.0    0.0    0.1   83.0    7.9    4.2  0.53 0.55 0.05
```
Dusk: golden red with the set's violet dusk sky (violet 17.6, magenta 9.0: from the DUSK preset's sky, under the magenta 10 limit). Storm:
blue-dominant as expected at night, no magenta. Darks are low (wide exterior without a foreground mass). Seconds per frame: 8.5 s wall /
16.0 s CPU per pass, two passes per frame (17.1 s wall).

## Differences from the plan
- "animate sky card/cloud cards": done as a 2D mix of two 3D passes with a moving noise-edged cloud front (plus the turning sky dome in
  both passes); the 3D light really changes from DUSK to NIGHT_STORM under the front, but the cloud front itself is a matte, not geometry.
- The rod is absent (set_rod(0)): padre handed it back in shot 14, and shot 16 shows the empty spire.
- No people in the square (it is evening and the storm is coming).
