# QA s19 (render team 5, film 18) round 14 - g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), NIGHT, cut in / whip out
- Frame-diff in-shot (n=87, 90x160 grey): median **10.59**, p90 **13.45**, min 0.75, max 25.37.
- qa_auto: FAIL only for "suspected blur" g1504-1518 = the designed whip-out at the end of the take (director confirmed this class as a false positive for whip landings).
- Camera pitched down (look z 4.0) from (14.2,-15.5,1.5): projected ox mouth worst 782 px at g1484 (<= 800); no frame with mouth > 860.
- Herd: one near staggered lane (one ox every 18 frames, `face='rage'`, tail flame lean 60) plus 9 far-lane oxen (flames hidden); 5 visible oxen per 0.5 s tile NOT reached in all tiles - typically 2-4 visible (column geometry + the flame-face gap rule trade off against density).
- Flame-to-face gap (card-alpha matte): < 15 px in 3 frames only (g1443 13 px, g1445 14 px, g1457 10 px); all others >= 15.
- Props: pots with warm point lights; helmet moved to (16.2,-9,0); props may still graze the lead ox jaw at isolated frames, not re-verified frame by frame.
- Ground: purple strip covered by `mygap` plane; rendered-PNG colour mask not done (rough low-chroma lower-third proxy 0.86 is dominated by the road/field palette and is not a valid plain-field metric). Honest deviation.
- Qi silhouettes behind oxen at x 44+. Comic, bloodless.

## Section I rim light (final render)
- Frame-diff in-shot (n=87): median **11.21**, p90 **14.19**. qa_auto blur flag only on the whip-out (g1504-1518).
- Moon-blue rim (120,175,255) painted into every character/ox card on the upper/right silhouette edge (cards are unlit emission, so scene lights cannot rim them); plus two blue point lights per frame behind the nearest oxen for the ground. Warm fire key and saturated reds unchanged, no haze added. Layout unchanged; the other s19 caveats above still apply.

## Round 15 (director follow-up, rim version)
Far-lane head-on oxen increased from 9 to 15 (flames hidden, spacing 7 frames, lane depth 64+ D). Frame-diff n=87: median **11.20**, p90 **14.17**. Flame-face gap < 15 px now in g1475-1477 only (was g1443, 1445, 1457; the remaining 3 persisted when I shifted near-lane waves 2-5 by +-3..9 frames - those shifts made it worse). Density: far oxen are small at their depth, so visible oxen per 0.5 s tile is about 3-4 but the 4-per-tile target is not reliably met in every tile. Mouth worst 782 px. qa_auto fails only on the whip-out blur.

## Round 16 (gate 14b)
- Frame-diff n=87: median **11.49**, p90 **15.71**; qa_auto blur flag only on the whip-out.
- Far lane: 18 head-on oxen (spacing 5 frames, flames hidden, lane 64-74 D). Near lane stays every 18 frames: spacing it every 9 frames put flames through every neighbour's face (gap 0 px in nearly all frames, also with flames hidden on alternate oxen or an alternate lane), which contradicts "keep your flame gaps". Flame gaps < 15 px in g1443 and g1475-1477 (g1503-1514 are whip-out frames, camera sliding).
- Density: 4 oxen per 0.5 s tile was NOT verified or reliably reached (far oxen are small); honest miss.
- Props: pot (16.6,-10.6), bowl (18.6,-8.4) removed, helmet moved to (15.6,-17.5); 26 small rubble props along the lower edge. Not frame-checked for g1476-1492 jaw overlap beyond the phone sheet; the tilt-up of 4 deg was not applied (it pushes mouths past 860).
- Ground on RENDERED frames (gshare.py, horizon y 800): median **0.73** by my estimator, which includes the wall base and reads far higher than QA's; target 0.28 NOT demonstrated.

## Round 17 (director 14:28 note: reframe)
Reframed to the director's brief: camera on the herd axis at (30.2,-26,1.7) looking at the wall (nearest hole at x ~0.5), lens 22; oxen (3 holes x staggered every 24 frames, 8 apart) burst out toward the camera at 9 D/s, head-on, ~15-25 % frame height, flames up on the tails; Qi from the outer holes (x 19, 41) behind; culled at y -13 (13 D from the camera); no pot over any ox head in the phone sheet; 75 small rubble props on the ground between run end and camera (corner ones <= 0.55 scale); no big foreground pots.
- Frame-diff n=87: median **18.32**, p90 **23.08**. qa_auto fails only on blur at g1507-1520 (whip-out).
- Ground (shared ground_share.py, every 5th frame): max **0.356** (g1457), median 0.269: the worst frames exceed the 0.30 target. A DENS=0.95 re-render had no effect (identical frames).
- 4+ oxen visible per tile on the phone sheet (not counted per 0.5 s tile); mouth y and flame gaps not re-measured after the reframe (measure mode was written for the old lane layout) - phone sheet shows the lead jaw at about y 770.

## Round 18 (gate 16 follow-up)
Gate 16 judged the older lane layout (pot in the lead's path); the round-17 head-on reframe removed those pots, and no prop is in the oxen's run (props only y -24.5..-14.8, oxen culled at y -13). Rubble raised 75 -> 150 props at the lower edge. Frame-diff n=87: median 19.97, p90 25.21. Ground (shared ground_share.py, every 5th frame): max **0.306**, median 0.227 (0.30 target missed by 0.006). qa_auto: blur flag only on the whip-out. Not re-checked at 2x zoom frame by frame.
