# s16 QA: film 6, shots 16-19 (quote 2 + the snatch + the afternoon re-weigh), bakery MORNING (16-17) / AFTERNOON (18-19)

Delivered: `frames/g_1233.png .. g_1583.png` (351 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions / audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 1233). Shots: 16 = g 1239..1334, 17 = 1335..1420, 18 = 1421..1514, 19 = 1515..1577 (plan bounds
round(t*30)); in-handle g 1233..1238 and out-handle g 1578..1583 rendered in 3D. Also `meta.json`, `cues.json`, `contact.jpg`, `compare.jpg`.
Scripts: `shot.py` (16,17 = one MORNING build, 18,19 = one AFTERNOON build: `final 16,17 ...` / `final 18,19 ...`), `deliver.py` +
`deliver_cfg.json`, `qa.py` (-> `work/qa.txt`), `sheet.py`; helpers `../common.py`.

## Framings (a change every 1.0-2.0 s)
| g | shot / framing | action |
|---|---|---|
| 1233-1284 (1.7 s) | 16A low two-shot over the counter | henry's belly laugh (laughing drawing: eyes shut, tears, bouncing squash); kit (hidden stool, left) looks up worried. From g 1271 (quote) henry turns smug, arms crossed, lip-sync |
| 1285-1334 (1.7 s) | 16B low punch-in on henry | smug, arms crossed high on the chest, talking "ส่วนข้าซื่อสัตย์" (kit moved off frame left) |
| 1335-1378 (1.5 s) | 17A across the cooling table, close | kit's basket of 13 on the table, steam; henry (behind it) reaches in g 1337-1347, plucks the pale 13th off the top (basket drawing 13 -> 12 at g 1348), holds it up at his chest; kit's smile drops (g 1351) |
| 1379-1420 (1.4 s) | 17B two-shot at the table end | henry holds the loaf and wags his finger at kit (angry, closed mouth); kit droops |
| 1421-1466 (1.5 s) | 18A AFTERNOON, window_out | kit alone tiptoes (sneak cycle) toward the counter with a morning loaf on his palm, glancing both ways |
| 1467-1514 (1.6 s) | 18B over the counter from the street | kit beside the hand balance, looks round, lifts the loaf over and lays it on the empty pan (g 1489: the set's pan loaf takes over); the beam swings from -8 (weights down) to about level |
| 1515-1547 (1.1 s) | 19A small_scale_insert ECU (slow push) | the loaf side of the beam RISES: ease from +1 to -8 deg (lighter than the weights) |
| 1548-1583 (1.2 s) | 19B from the street over the counter | the tilted balance; kit's head peeks over the counter behind it, eyes go wide (shocked, g 1556) |

## Client rules
- **No depth of field** (`common.Take`). Sharp. In 16B the opening's hanging bundles (`opening_bundles`, within ~1 D of the low camera,
  texture magnified into a soft smear) are hidden (keyed `hide_render`) for that framing only.
- **Mouths only on the quote**: henry lip-syncs (`cast6.talk_mouth`) only g 1271..1334 (quote 2 "พวกนั้นมันโกง ส่วนข้าซื่อสัตย์", captions
  42.28-44.43 s; the shot ends at g 1334). The laugh before it ("ลุงเฮนรี่หัวเราะ" is narration) is the static laughing drawing (open grin,
  no lip-sync). Shots 17-19: static expression mouths only.
- **Heads above the caption band / 0.35-0.59 H**: see the table; all heads whole above y 880 (17A after the kit fix below), centres
  0.36-0.58 H.
- **Continuity**: the 13th loaf is the pale one (basket_svg 13 -> 12 when henry takes it; henry then holds the cast loaf prop).
  Afternoon (18-19): AFTERNOON light preset, steam off (the loaves are cold), oven burning low (0.7).

## Staging (`work/qa.txt`)
| framing | actor | head width px | centre x | centre y (H) |
|---|---|---|---|---|
| 16A | kit / henry | 210-224 / 194-205 | 148-161 / 496-509 | 0.54 / 0.50-0.53 |
| 16B | henry | 240-250 | 340 | 0.49 |
| 17A | henry / kit | 306-324 / 308-327 | 188-198 / 635-652 | 0.36-0.37 / 0.54-0.55 |
| 17B | henry / kit | 322-341 / 261-273 | 612-627 / 127-138 | 0.43 / 0.53 |
| 18A | kit (walking) | 172-203 | 213-460 | 0.55-0.58 |
| 18B | kit | 288-305 | 190-200 | 0.49 |
| 19B | kit | 327-345 | 474-481 | 0.54-0.55 |
17A: henry stands on a hidden 0.4 D step and kit on 0.16 D behind / beside the table end so the basket rim sits at henry's belly: at
floor height the snatching hand projected onto his moustache. The basket card faces the camera of each framing (keyed per frame).
18B: the loaf is carried by a world pin of kit's hand along an arc onto the left pan (pan position from the beam geometry; the set's
loaf object is not usable as a target while hidden).

## Pops / checks
Pops outside the cuts: g 1350 -> 1351 (kit's happy -> sad reaction, deliberate snap), g 1423/1457/1477 (sneak-cycle gaze flips, 3.4-4.2
levels, small). 7 cuts inside the take (43-73 levels). Near-still pairs: g 1332, 1467, 1582 (single pairs, slow push / hold). No black or
magenta frames, no clipped sprites, no retried frames.

## Colour (`hue_report.row`, final frames)
```
s16 shot 16 (g 1233-1334)                      53.1   37.7    0.7    0.2    0.0    0.5    2.4    5.3  0.43 0.54 0.08
s16 shot 17 (g 1335-1420)                      56.3   28.9    0.6    0.0    0.0    1.6    1.6   10.9  0.31 0.59 0.07
s16 shot 18 (g 1421-1514)                      49.9   36.4    0.6    0.0    0.0    1.2    2.0   10.0  0.39 0.54 0.06
s16 shot 19 (g 1515-1583)                      40.5   45.0    2.8    0.0    0.0    0.5    3.3    7.9  0.46 0.54 0.06
ref a t0001 t0046 t0047                        32.1   44.2    4.9    0.3    0.0    7.0    6.1    5.4  0.34 0.47 0.12
```
The bakery set's warm look (bakery_API 7). Shot 17's "magenta" 10.9 is the pink-cream plaster of the back wall / window light
behind the table (warm pink, not a magenta cast on the shade). 17A was re-rendered with kit raised 0.06 D (first pass: his head bottom crossed y 880 by ~12 px in g 1351-1378).

## Seconds per frame
17.6 (16) / 21.8 (17) / 16.3 (18) / 19.2 (19) s wall per frame; take mean 18.6 s wall / 36.2 s CPU (two 2-thread processes on 4 cores).

## Differences from the plan
- Shot 16 "counter low": two framings (two-shot with kit, then henry solo).
- Shot 17 "table_insert ECU of the hand": a close shot across the cooling table with henry's face in frame. The cast cards read badly from
  the steep top-down insert, and at hand height his card filled the frame. The snatch reads, and the finger wag is a separate two-shot.
- Shot 18 "window_out": 18A is the window_out preset camera (look lowered to keep kit's head above the band); 18B is a street-side
  framing over the counter so the hand balance and the loaf on the pan read.
- Shot 19: 19A is small_scale_insert (aim nudged toward the loaf pan); 19B adds kit's wide eyes over the counter.
