# s27 QA: film 6, take s27 = shots 27, 28 (market AFTERNOON), the "run" + "plant the 13th"

Delivered `frames/g_2210..2452.png` (243 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions/audio) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 2210). Shot boundaries: 27 = g 2216-2368, 28 = g 2369-2446 (hard cut at g 2369); in-handle g 2210-2215,
out-handle g 2447-2452. `meta.json`, `cues.json` (9 cues), `contact.jpg`, `compare.jpg`, `QA.md`. Scripts: `shot.py`, `deliver.py` +
`deliver_cfg.json`, `qa.py`, `sheet.py`; helpers in `../common.py`. Raw + per-frame json in `raw/s27`, `raw/s28`.

## The take (5 framings)
| g | shot/framing | what |
|---|---|---|
| 2210-2262 | 27 a | down the lane to Henry's glowing bakery front: kit bursts out with the pale 13th loaf held high and runs at camera (run cycle) |
| 2263-2316 | 27 b | low tracking ahead of kit through the crowd; townsfolk with rotten veg turn to look |
| 2317-2368 | 27 c | medium tracking: kit SHOUTS the quoted line (lip-sync) |
| 2369-2410 | 28 d | HARD CUT to the big balance: kit skids onto a crate beside the bread pan, still shouting up at the inspector, loaf high |
| 2411-2452 | 28 e | ECU on the bread pan: kit's hand brings the pale loaf over the pile and plants it on top (set_loaves 13 at g 2424), pats, withdraws |

## Client rules
- **No depth of field anywhere**: common.Take switches DOF off at build and before every render; sharp throughout.
- **Mouths only on quoted lines**: kit's mouth moves ONLY on the one quoted line (plan shot 27 shout, 77.27-80.21 s = g 2321-2409), via
  `cast6.talk_mouth`. Before and after, and everyone else, static expression mouths. (This is the film's one kit-quote.)
- **Heads above the caption band**: every in-frame head centre y well above 880, head bottom < 880 on every frame (qa.py "below 880: none").
  Two near-lane crowd figures were pushed to the north flank in b/c so their heads clear.
- **Comic, not cruel**: the crowd only holds raised veg; nothing is thrown at a person in this take.
- **Continuity**: the 13th loaf is THE PALER loaf. Kit's held loaf is drawn with a lighter BREAD palette (swapped only on kit's sprites), and
  the loaf added to the pile is the set's pale loaf #13 (`set_loaves(13)`), so the loaf he carries == the loaf that lands. The beam stays at
  `set_big_scale(-7)` on every frame of this take (it tips only in the next take, shot 29). The same runtime dial + needle as s24 are present
  (the balance is the same prop across 24-29).

## Motion / rig
- Kit's run is `cast6.cycle("kit", g/16, "run")` with the loaf kept in the raised screen-right hand (arms="l"); the camera tracks him in b/c
  (rig computed from his floor position each frame) with a framing change every ~1.5 s.
- The plant (e): kit stands on a runtime market crate at the pan's front-right; his screen-left hand is pinned (`held_on_palm`, side="l") to a
  world path that brings the loaf from his side, over the pile, and down onto the 13th-loaf spot at g 2424 (where `set_loaves` flips 12->13),
  then pats and withdraws. IK reach error <= ~0.25 D on the approach, 0 at the plant.

## Checks (qa.py): see work/qa.txt
Frame-change median, the internal cuts (a->b g 2263, b->c g 2317, the HARD CUT to shot 28 g 2369, d->e g 2411), popcheck, magenta/black,
hue row vs ref a market. Heads table. s_per_frame.

## Differences from the plan
- Plan shot 27 is one run; split into a (burst out + run) / b (through the crowd) / c (the shout) for the pacing grammar. Shot 28 split into
  d (skid in) / e (ECU plant). The hard cut the plan asks for is at g 2369 (d), the "plants the loaf" at g 2424 (e).
- Kit plants the loaf from a market crate at the pan's front-right (the pan top is 2.2 D up; the 2.48 D boy needs the lift to reach the pile
  centre), a runtime prop added in shot.py (the set is untouched).
- The beam does NOT move in this take (that is shot 29's beat); here it is held at -7 with 12 loaves until g 2424, then 13.
