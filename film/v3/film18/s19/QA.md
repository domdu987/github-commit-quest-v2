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
