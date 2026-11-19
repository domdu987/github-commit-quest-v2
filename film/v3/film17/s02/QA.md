# film17 s02 (shots 4-6) QA
Frames g138..341 (g0 144, g1 336, 6 handle each side), 720x1280, 12 samples + OIDN, ~35-55 s/frame, 2 threads x 2 processes. take.mkv is split: `cat take.mkv.part* > take.mkv`.
Cuts: 222 (shot4->5, same street, hard), 285 (street -> front desk). transition_in dissolve 11.

## qa_auto (film/qa_auto.py --first_g 138 --cuts 222,285): PASS
Note: cut 222 shows no strong change (shot 4 pushes in to the wagon, shot 5 is the closer take on the same spot).
## Rhythm (film17/rhythm.py): in-shot median 5.03, p90 13.45 (targets >= 4 / >= 12)
Camera: eased push + slide in every shot, two snaps each (g166,198 / 238,262 / 298,322).

## Self-check (contact.jpg every 6 f, phone_sheet.jpg, cut +-3)
- Heads above y 880, centres 0.45-0.55 H in shots 5-6; shot 4 is a wide (figures ~200 px at the end, ~110 px at the start).
- Mouths: all poses wrapped in cast17.silent; no quote windows in this take.
- No light-shaft/beam_fx over cast (desk frames checked); dust k 0.5, no visible specks.
- Wagon parked, no horse. Thief (prisoner_c, beret) tips cap g250-276 and smirks; gendarmes flank him. Desk: thief shrugs, gendarme shrugs then waves.
## Known weaknesses
- Shot 4 has no thief (plan has him only from shot 5); gendarme_a marches out of frame left by g~213.
- Puddle reflection of a walking gendarme visible at the bottom near g183.
- Cap tip is a simple raised arm; gendarme grips are escort poses without exact contact.
