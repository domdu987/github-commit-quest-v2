# s24 QA: film 6, take s24 = shots 24, 25, 26 (market AFTERNOON), the "fail"

Delivered `frames/g_1929..2221.png` (293 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions/audio) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1929). Shot boundaries: 24 = g 1935-2052, 25 = g 2053-2129, 26 = g 2130-2215; in-handle g 1929-1934,
out-handle g 2216-2221 (both rendered in 3D). `meta.json` (first_g 1929, n_frames 293, transition_in/out = cut), `cues.json` (11 cues),
`contact.jpg` (16), `compare.jpg` (4 finals beside ref a), `QA.md`. Scripts: `shot.py` (probe/stills/final), `deliver.py` + `deliver_cfg.json`,
`qa.py`, `sheet.py`; shared helpers in `../common.py`. Raw + per-frame json in `raw/s24..s26`.

## The take (7 framings, a cut every 1.0-2.0 s)
| g | shot/framing | what |
|---|---|---|
| 1929-1974 | 24 A | inspector_royal (hood down, tabard + chain) at the big balance, basket of 12, turns to the bread pan; slow push |
| 1975-2018 | 24 B | tips the basket over the bread pan: 12 loaves tumble on (set_loaves 0->12 as the basket drawing empties 12->0) |
| 2019-2052 | 24 C | wide frontal of the whole balance: 12 loaves on the pan, the beam stays DOWN on the weights side; he looks up at it |
| 2053-2092 | 25 D | ECU: the brass needle sits off the red centre mark of the dial (runtime prop) |
| 2093-2129 | 25 E | low close-up of the inspector under the tilted beam, brows down ("a hair short") |
| 2130-2176 | 26 F | pillory side: guard1 (leaning back) + guard2 drag pale henry (heels in) toward the pillory; the board at frame-left |
| 2177-2221 | 26 G | over the crowd: woman1 (tomato) + man1 (cabbage) raise rotten veg (g 2180-2190); henry hauled on toward the steps |

## Client rules
- **No depth of field anywhere**: `common.Take` sets `cam.data.dof.use_dof=False` and `B.setup_dof(scene,None,None,cam)` at build and
  before every render. Everything sharp: the balance frame, banners, the house rows, the cobbles.
- **Mouths only on quoted lines**: shots 24-26 have NO quote -> no lip-sync. Every face is its static expression mouth (inspector
  determined/angry, henry shocked, guards angry, townsfolk angry).
- **Heads above the caption band**: every in-frame head centre y 543-756, head bottom < 880 on every frame (qa.py: "below 880: none"
  for all 8 actors). Two near-lane crowd members were pushed to the north flank so their heads clear.
- **Comic, not cruel**: the veg is only raised (cartoon rotten tomato/cabbage), henry is dragged by the arms (heels digging in), no injury.
- **Continuity**: inspector is hood-down inspector_royal (shot 23 dropped the hood); the pile is 12 loaves (the short dozen); the beam is
  held at set_big_scale(-7) on EVERY frame of the take (it tips only in a later take). The paler 13th loaf is NOT here yet.

## The beam and the dial
`B.set_big_scale(-7)` and `B.set_loaves(n)` are keyed every frame (n = 0 before the pour, growing to 12 by g 2014). The plan wants an ECU
that the beam "does not move, a hair short": the set has no gauge, so shot.py adds a runtime **dial** (a cream plate with ticks and a red
centre mark, on an iron bracket) and an iron **needle parented to `big_beam_pivot`**, so the needle swings with the beam. At -7 it reads
clearly left of the red mark. The dial/needle are built in `Take.make_dial()` and never touch the set module (rule 5). Small (only the ECU
D and the close-up E frame it).

## Staging and heads (qa.py)
| actor | head w px | centre x | centre y (H) |
|---|---|---|---|
| inspector | 78-295 (push/ECU) | 121-405 | 0.42-0.56 |
| henry | 101-183 | 269-639 | 0.52-0.54 |
| guard1 / guard2 | 90-193 | 200-760 | 0.48-0.54 |
| woman1 / man1 (fg veg, G) | 221-291 | 51-694 | 0.47-0.49 |
Guards' hands are pinned onto henry's `hand_l` / `hand_r` world points (from his rendered sprite anchors), so each guard grabs a wrist;
their legs are a walk cycle. The pour uses the cast `basket` pose key (loaves 12->0, tilt, pour phase), with the off hand lifting the
basket base (anchor `basket_base`).

## Checks (qa.py)
- Frame-change median 2.64 levels; the 6 internal cuts register 58-83 levels (clean hard cuts at g 1975, 2019, 2053, 2093, 2130, 2177).
- Popcheck (excluding the planned cuts): none. No magenta/black frames, no retried frames, no clipped sprites.
- "near-still (<0.35)": isolated single frames at the first/last frame of slow-push framings (e.g. the start of the in-handle, the frame
  either side of a cut); no run of >6 static frames.

## Colour (hue_report)
```
set                                    red orange yellow green cyan blue violet magenta  sat  val dark
s24 all (g 1929-2221)                 43.5  21.2   0.6   0.1  0.1 24.2   5.3    5.1    0.45 0.66 0.05
ref a market (t0065 t0105 t0121)      33.0  49.9   7.8   4.5  0.0  1.7   0.5    2.6    0.40 0.60 0.02
```
The market AFTERNOON set as it measures (bakery_API 7 known gap: brighter/flatter than the ref day exteriors). Red is high because the big
red royal banners on the balance fill the ECU/close frames (D/E) and the guards' red tabards fill F; blue is the sky. Not graded here (set
look, identical for every market shot). If the director wants it closer to ref A, warm/darken the market in the conform for all market shots
alike.

## Differences from the plan / notes
- Plan shot 24 is one line; I split the 3.93 s into A (approach) / B (pour) / C (reveal the unmoving beam) for the "a cut every 1.0-2.0 s"
  grammar, and shot 25 into D (ECU dial) / E (inspector), shot 26 into F (drag) / G (crowd veg) — camera-preset switches inside a take, which
  the brief encourages.
- No `big_scale_insert` preset is used for C: that preset is tight on the pan; C is a custom wider frontal so the whole A-frame, both pans
  and the standing inspector read (the beam tilt is the point of the shot).
- The dial + needle are a runtime addition (see above); the set has no scale-gauge hook.
- s_per_frame: 11.60 s wall / 21.54 s cpu mean (2 threads, two processes on 4 cores).
