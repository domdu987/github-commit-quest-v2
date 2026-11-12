# s11 QA: film 3, shot 11 (winter passes), harbor set WINTER, street_wide

Delivered: `take.mkv` = g 910..1007 (98 frames, first_g 910), 720x1280, 12 samples, 2 threads, no captions or audio.
g 918..1007 = shot 11 ([g0, g1) = [918, 1008)); g 910..917 = 8-frame in-handle (half of the 12-frame dissolve + 2) rendered
in 3D with the shot's own camera before its start. Out: hard cut to shot 12 (no handle). `meta.json`, `cues.json` (6 cues),
`contact.jpg` (16 frames). Scripts: `shot.py` (the take), `lib3.py` (helpers shared by takes s11/s12/s13/s15, identical copies),
`deliver.py` (frames, take.mkv, meta, cues, contact sheet; `deliver.py qa` prints the numbers below).

## Timing
| event | g | s (film) |
|---|---|---|
| in-handle (dissolve from shot 10, 12 f) | 910..917 | 30.33 |
| shot 11 starts ("ผ่านไปทั้งฤดูหนาว") | 918 | 30.60 |
| push speeds up / second segment ("ถังก็ยัง") | 953 | 31.77 |
| hard cut to shot 12 | 1008 | 33.60 |

## Picture
- street_wide family camera (2, -63, 23.2) -> (2.55, -55.2, 20.4), looking at the tank end of Commercial Street; slow eased push and
  sink in two segments with a 35 % constant-speed share (never parks). Snow falls through the whole shot: 6500 camera-facing octagon
  flakes in a world box over the street (deterministic in g, wobble + drift, size grows with distance so far flakes stay 2-4 px and
  near ones are a few px larger). Snow settles: the kerb / sidewalk heaps grow in height x0.55 -> x1.15.
- The tank is painted brown (set_paint 1, end state of shot 9) and stands unchanged at the end of the street.
- Life (tiny, wide shot): worker1 and worker2 trudge up the street (two-drawing walk, hunched), kid1 throws snowballs, kid2 plays.

## Staging (raw/s11/*.json)
| actor | head w px | centre y (H) | heads below y 880 |
|---|---|---|---|
| worker1 | 17-19 | 0.64-0.65 | none |
| worker2 | 16-18 | 0.63-0.64 | none |
| kid1 / kid2 | 14-17 | 0.60-0.62 | none |
Wide establishing shot: the head-centre band 0.35-0.59 does not apply (wides exempt). No mouths move. Nobody's back to the camera.

## Checks
Popcheck: no pops. No near-still transitions (snow + push). No black/magenta cards, no retried frames.
Render: 10.7 s wall / 17.9 s CPU per frame (mean of 98; two render processes running).

## Colour (`hue_report.row` on the final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s11 shot 11 (g 918-1007)                       22.2    1.3    0.0    0.3    0.2   72.3    1.2    2.5  0.44 0.59 0.04
ref b t0010 t0030 (exteriors)                   8.6    3.4    0.0    0.0    0.0   77.4    3.4    7.2  0.46 0.66 0.08
```
Winter exterior with open sky: blue-dominant as the reference exteriors (77 %) and the set's WINTER street stills (66-75 %);
violet and magenta in band, the shade on the street and the west rows reads blue-violet. Dark share 0.04 (the shaded street is
mid-blue, not near black; snowflakes lighten it further).

## Differences from the plan
- None in content. The push is gentle (as planned: "slow push"); framing change by the speed change at g 953 and the continuous
  push; the falling snow keeps every frame moving.
