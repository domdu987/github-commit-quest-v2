# s26 QA: film 7, shots 26-27 (85.77-91.49 s): the Florence dealer's shop, the offer and the arrest

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 2567, 184 frames = g 2567..2750, 720x1280, 12 samples, 2 threads, denoise
FAST, no captions / audio). g 2573..2744 = shots 26-27 ([g0, g1) = [2573, 2745)); g 2567..2572 in-handle and g 2745..2750 out-handle,
both rendered in 3D (6 frames each). transition_in = dissolve (from shot 25, the attic). Also `meta.json`, `cues.json` (10 cues),
`contact.jpg` (16 frames, cyan line = y 880), `compare.jpg` (g 2605 beside ref a t0015, g 2735 beside ref a t0045).
Scripts: `shot.py` (probe / stills / final, 4 set-ups), `deliver.py`, `qa.py` (-> `work/qa.txt`); shared `../common.py`.

## Set-ups (framing change every 1.3-1.8 s; cuts on the narration)
| id | g | shot | what | camera |
|---|---|---|---|---|
| 1 | 2567-2611 | 26 | two-shot over the desk: vincenzo (1913, normal clothes, smug) pulls the wrapping cloth off the panel (g 2586-2597), presents it with an open palm, grinning; the dealer behind the desk leans in, stunned | 18 mm, slow push |
| 2 | 2612-2657 | 26 | CUT on "เสนอขาย" (87.07): the dealer holds the panel up and inspects it through his pince-nez (`dealer_inspect`, panel x1.35; the desk panel hidden while he holds it) | 24 mm, slow push |
| 3 | 2658-2697 | 27 | the panel back on the desk in the foreground; the dealer smiles at vincenzo (off screen right), then winks and beckons to screen-right (`dealer_signal`, g 2676-2696) | 22 mm, slow push |
| 4 | 2698-2750 | 27 | CUT on "แล้วพาตำรวจ" (90.01): wide with the shop window on the Duomo; two police agents run in from screen-right (4-frame camera bump on the burst), vincenzo startled (shocked, sweat), the first agent grabs his arm (g 2716) -> `vincenzo_arrested` (hands behind, head down) | 20 mm, slow drift |

## Client rules
- **No depth of field**: `common.Take` (dof off at build and before every render). Everything sharp.
- **Mouths**: no quoted line in 26-27 -> no lip-sync; the `mouth` keys of the STORY poses (`dealer_smile`, `police_arrest`) are dropped,
  expression mouths are static.
- **Heads above y 880** (work/qa.txt): set-up 1 vin centre 0.55 H / dealer 0.44-0.45 H; 2 dealer 0.51 H; 3 dealer 0.51-0.52 H;
  4 vin 0.52-0.54 H, police 0.46-0.49 H. No head bottom below 880 on any frame.
- **Dense set**: the shop's salon hang, cabinets, bust, chandelier, the desk lamp; plus a runtime wrapping-cloth prop (`s26_cloth`).

## Checks
Popcheck: jumps only at the three planned cuts (2611/2612, 2657/2658, 2697/2698) plus the grab pose change 2715/2716 (4.9 levels, the
action). No near-still pairs, no black / magenta frames, no retried frames.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s26 set-up 1 (g 2567-2611)                     13.6   43.3    5.8    0.3    0.4   22.3    3.4   10.8  0.26 0.38 0.29
s26 set-up 2 (g 2612-2657)                      9.6   63.7    6.5    0.5    0.3   16.2    1.2    2.0  0.35 0.45 0.28
s26 set-up 3 (g 2658-2697)                     11.7   45.6   11.3    0.3    0.7   24.1    1.8    4.6  0.30 0.41 0.29
s26 set-up 4 (g 2698-2750)                      9.4   43.2    5.1    0.5    0.1   27.9    5.0    8.9  0.28 0.38 0.34
s26 all                                        10.7   51.1    7.1    0.4    0.4   21.9    2.6    5.8  0.30 0.41 0.30
ref a t0015                                    61.5   22.6    0.2    0.0    0.0   11.9    1.2    2.6  0.46 0.49 0.06
```
Warm lamp-lit shop with green damask walls (the set's SHOP_DAY); darker and less saturated than the ref's red throne rooms (set-wide
gap noted in louvre_API 7). Shade is blue (22), magenta 5.8 overall (10.8 in set-up 1: the vincenzo cheek blush + purple-grey shade on
the green walls). Not graded here.

## Seconds per frame
17.96 s wall / 34.75 s CPU mean (12 samples, 2 threads, two render processes at once on 4 cores, 4 actors in set-up 4).

## Differences from the plan / notes
- "dealer_inspect" is staged with the dealer lifting the panel off the desk (set-up 2); in set-ups 1/3/4 it lies on the desk.
- Vincenzo is off screen in set-up 3 (the signal happens "behind his back"); police enter from frame right (the shop's front door is
  behind the cameras; no door is modelled).
- First final was rejected by QA: set-ups 1-2 had head bottoms below y 880 at the end of their pushes -> cameras tilted down and the push
  shortened, those 91 frames re-rendered (`work/old_raw`).
