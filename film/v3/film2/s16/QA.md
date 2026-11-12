# s16 QA: film 2, shot 16 (the bolt seeks the highest point), tower NIGHT_STORM, no rod

Delivered: `take.mkv` = g 1241..1343 (103 frames, `first_g` 1241, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), no captions or audio.
Shot range [g0, g1) = [1248, 1337) (t 41.60-44.57); handles 7 frames each side (g 1241-1247, 1337-1343) rendered in 3D for the
10-frame dissolves in and out. `meta.json`, `cues.json` (10 cues), `contact.jpg` (16 frames, labels above the picture). Script `shot.py`
(+ `common.py`), deliverables `deliver.py` (+ `deliver_common.py`), checks `qa_cam.py`, `popcheck.py`. Raw frames + per-frame json in `raw/` (not in git).

## Timing (film frame g = round((t + 0.10) * 30))
| event | g | narration |
|---|---|---|
| wide on the tower top in the storm, slow eased push and rise; cloud flicker | 1241-1266 (flicker 1262-1265) | "ที่เด็กคนนั้นรู้ก็คือ" |
| tilt up into the sky (where it will come from) | 1262-1276 | |
| stepped leader appears at the top of frame, grows in 3-frame steps | 1283 | "ฟ้าผ่าจะหา" 1285 |
| leader hesitates, five side branches fork off into empty sky and die | 1289-1312 | |
| snap punch-in on the spire (9 frames, quint) | 1299-1308 | "จุดที่สูง" 1303 |
| the leader bends back toward the empty finial; upward streamer off the finial | 1304-1316 (streamer 1312) | |
| contact on the finial top + return stroke, flash flicker (1, .35, 1, .25, .75, .15, .45, .1, 0), camera jolt | 1317-1328 | "ที่สุดเสมอ" 1318 |
| finial glow fades, storm continues, camera keeps creeping | 1329-1343 | |
Framing changes: 1241 (dissolve in), 1262-1276 (tilt up), 1283 (bolt enters), 1299-1308 (punch-in), 1317 (strike/jolt): gaps 0.7-1.1 s, then the creep to the end (0.9 s).

## Camera (`qa_cam.py`, fastest of 9 screen points, px per frame)
min 0.52, median 4.1, peak 395 (g 1303, the snap punch-in). Static runs (< 0.25 px): none. Constant-speed runs: g 1324-1327 (4 frames, inside the strike jolt's decay).
Popcheck (`popcheck.py`, median frame diff 1.23): spikes only at the intended events: cloud flicker 1262-1266, punch-in 1302-1307, strike flash flicker 1317-1328. No near-still transitions.

## Staging
No actors (the plan's shot is the bolt and the empty spire). Finial top on screen (720x1280): (355, 699) in the wide, (348, 751) after the punch-in = 0.55-0.59 H, centred.
Rod: `set_rod(0)` throughout (the spire is empty); the set's own bolts hidden. The bolt is this take's own: a jagged polyline designed in the screen plane of the punch-in camera through the finial (so it reads in both framings), revealed by `bevel_factor_end` (stepped leader, branches) and replaced on contact by a thicker, brighter return stroke with an additive glow; `T.flash()` drives the flash light and the sky / plate.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s16 all (g 1241-1343)                           0.0    0.0    0.0    0.0    0.0   99.6    0.3    0.1  0.69 0.37 0.06
```
Night storm: blue-dominant as expected for NIGHT_STORM (the set's own NIGHT_STORM stills measure 97 percent blue); no magenta cast (0.1), violet 0.3; the warm windows of the mid town are tiny accents. Dark share 0.06.

Seconds per frame: 5.5 s wall / 10.0 s CPU mean (2 threads, another render running at the same time).

## Differences from the plan
- Plan camera "chamber_high_down / wide": a custom wide from the south-west, 16-24 D up (the tower top, the spire and a big sky; chamber_high_down looks down at the square and has no sky for the bolt), punch-in on the spire on "จุดที่สูง".
- The bolt touches the finial (return stroke + flash) on "ที่สุดเสมอ" instead of stopping short; this is the mechanism explanation, the real strike comes in shot 20.
