# QA-art, TAKE gate: s24 (shot 24, HALL hall_table EVENING, the King times the watch) — FIX-FIRST

Frames checked (take index / g): 9/1933, 30/1954, 50/1974, 75/1999, 85/2009, 103/2027, 112/2036 (full size + 360x640).
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artend/s24_*.jpg

| Criterion | Score |
|---|---|
| Set density / ornament | 8 |
| Lighting & colour | 6 |
| Composition / phone legibility | 4 |
| Acting (squint, watch compare) | 6 |
| Key moment ("every day, ten weeks") | 4 |
| Match to refs / client taste | 6 |
| **Overall** | **5.5** |

## Why FIX-FIRST
This shot carries the hardest idea of the ending: the King timed it himself, every day, for ten weeks. At phone size it does not read.
- For the first two thirds the King is a 80-110 px head at the far end of a long table (f 9-75). His gold watch and the H4 are under 20 px, so "comparing two watches" is invisible; he just looks like a grumpy man behind candelabra.
- The candle stubs (the time-lapse device) are only in frame from about f 45 to f 80 and show at most 5 of 10. On the snap word "สิบสัปดาห์" (g 2006, take index 82) the camera has already slid past them: at the key word the stubs are OUT of frame.
- The ending (f 95-112, the frames that cut to s25) is filled by a foreground candelabra whose flames clip to flat white cylinders (about 150 x 300 px of blown highlight); the King is cut at the right edge behind it. This is the "candle passing the lens" problem QA.md mentions, still present.
- Lower 30 % of f 9-50 is the dark underside of the table: dead area.

## Fixes (shot.py)
1. Camera: start closer and keep the King, both watches and the stub row in one frame for the whole shot. Move `CAM_LOC0` to about (-0.6, 0.6, 2.6) and `CAM_LOOK0` to about (0.2, 4.25, 2.3) (looking at `KING_M`), `push=0.07`, `slide_px=-40`, `arc_deg_s=6`. Target: King head 160-230 px wide, centre y 500-620 throughout.
2. Snap: aim the snap at the stub row plus the King, not past them: `shift=(0.6, -0.2)` (a small downward pan) instead of (2.00, 0.30), `k=1.25`. At g 2006 all ten stubs and the King's face must be in frame together.
3. Stubs: keep `stubs_at(g)` but stage the row across the near table edge in frame lower third (y 820-1000 at f 82), left to right, so the count visibly grows; land 10 by g 2006 (currently at G1-1 = 2027): `stubs_at = clamp((g-G0)/(G_SNAP-G0))*10`. The time-lapse should peak on "สิบสัปดาห์", not after it.
4. Candelabra: keep it out of the last 20 frames (or behind the King), or drop its flame emission so nothing clips; the last frame before the cut must be the King, not a blown candle. If you want a FG prop, use the cold stub row, not a lit candelabra.
5. Pose: make the watches readable: raise both hands to face height (hand y 0.75-0.95 instead of 0.45-0.87), keep the H4 (silver) and the gold watch about 0.5 D apart beside the eyes, and scale both watch props about 1.5x. Keep the squint.

## Continuity
Chair present (`set_kings_chair(True)`, red chair right of the King), King stands beside it, same as s26 (KING_M there is beside the chair). Blue coat consistent. Window dusk blue, warm interior: EVENING consistent with s25/s26. The H4 is in the King's left hand here; it disappears in s26.
