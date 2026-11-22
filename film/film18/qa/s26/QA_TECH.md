# QA-tech round 19 s26: PASS
Checked: every frame g2015-2095 at full size (720x1280 frames extracted from take.mkv, wall band + oxen crop y 440-900, 6-frame montages at 1:1, 14 sheets, all 81 frames viewed), a flat-patch detector (local std over 9x9, y 300-900) on every frame, full frames g1958/1990/2066/2111 with the y 880-950 band marked, frame-diff over g1958-2111, caption-band bright share.

## Round-18 blocker: FIXED
- No flat mauve/beige/tan rectangle anywhere on the wall base or around the oxen, g2015-2095. The brick texture is continuous behind the herd (g2023-2052, where round 18 had 95x65 px and 190x40 px boxes) and behind the single ox head at g2078-2092 (the tan rectangle at x ~335-440 is gone). The detector finds no flat block over 20 px in the wall band beyond sky and cartoon fills (ox caparison, armour), which are by design.
- transparent_max_bounces = 64 accepted as the root cause fix.

## Re-confirmed
- BIGZOOM: general ~2 % at g1958 (tiny, in his warm pool, findable), ~45 % at g2066 (head top y ~300, within 35-60 %), ~54 % at g2111. One continuous move: no frame-diff spike (max 12.6, no cut), no pulse.
- General findable from g1958 (warm pool; clear of the 即墨 plaque and banner).
- No halos or colour fringes; the white/blue rim is a clean outline.
- Ox mouths max y ~830-850 (<= 860). No face in y 880-950 (general's mouth is above y 600 from g2066; only boots and ground in the band). No pole through a face.
- No glitches: no black/blank frames, no flicker, no dark prism or navy slab at the bottom.
- Measured here (90x160 grey, in-shot g1958-2111): frame-diff median 8.89, p90 10.76, max 12.65 (the director's 9.97 / 12.32 uses another metric; same picture). Caption-band bright share max 3.8 %. Ground max 0.297 taken from the director.
- qa_auto blur flag on the extreme wide (g1950-~2010): accepted.

## Notes (not blockers)
- g1959-1962 frame-diff is 1.3-2.6 (slow start of the move, no static run).
- g2043-2047: a thin pale light streak at the right edge near y ~600 (under 10 px tall).
- g2078-2090: the general's back is close to the right edge, face/arm/cup inside.
- Moire on the extreme-wide roofs and banding on the field panels were accepted earlier.
