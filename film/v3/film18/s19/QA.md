# QA s19 (render team 5, film 18) round 5 - frames g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Frame-diff in-shot (n=87): median **8.37**, p90 **11.47**. qa_auto: "blur" g1505-1520 = the whip and its landing on sky/sand (ruled a whip, not blur, by QA-tech).
- Oxen leave the holes in 6 waves 15 frames (7.5 D at 15 D/s) apart, so the spacing along the run is more than 1.5 body lengths; the flame of one ox no longer lands on the next one's head or neck at the frames named (g1446, 1481, 1491 re-checked at 6 fps).
- 6 Qi silhouettes behind the oxen (first g1417, then every 5 frames).
- The purple ditch strip is NOT fixed: I tried hiding/re-texturing `banks`, `bridge`, `road`, `water`, `fields` and the ground material; none of them changed it, so it is some other set element. Left for `dress_ground`.
- Bare ground about 30-35 % (see above).

## Round 6: ground dressing
Re-rendered with `J.dress_ground` (density 0.45, keep-clear along the herd lanes): `J.ground_share` 0.09 / 0.07 / 0.07 / 0.06 at g1435 / 1460 / 1485 / 1505 (target <= 0.25). Frame-diff median 8.92, p90 11.73. qa_auto blur flag = whip landing (as before). The purple ditch strip is still visible (set element not identified).
