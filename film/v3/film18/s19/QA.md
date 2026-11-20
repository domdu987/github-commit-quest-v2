# QA s19 (render team 5, film 18) round 8 - frames g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Frame-diff in-shot (n=87): median **12.63**, p90 **16.16**. qa_auto: "blur" at the whip landing g1505-1520 (low-detail sky/sand), as ruled before.
- Camera pitched down about 7 deg (look z 10.6 -> 7.0) and moved closer (15, -15.5, 1.1): the hole row sits at about y 0.55; the first oxen are about 25-35 % of frame height (previously 15-22 %), 14-20 D from the holes.
- Near tail flames scaled 1.3 (from 0.8) for oxen within 20 D; every charging ox keeps `face='rage'`; warm pools under the flames.
- 6 Qi silhouettes (g1417 + every 5 frames).
- Warm foreground props: `J.prop_pot` jars / bowls / pots and `J.prop_helmet` on the lane; they are placed in the world near the first-frame camera, so they only come into view at the end of the move (g1505-1520, the whip landing), not through the shot.
- Hidden: `hglow` pools, breach rubble, mist halo quads. `J.gapfill` ran.
- NOT fixed (4th time): the purple diagonal strip at the bottom right in the first 80 frames. It is not the `tunnel` material (re-texturing furrows changed nothing), not any single object (hiding every mesh singly left the pixel unchanged), and not covered by a dark earth plane at z 0.1 / 0.18. Pitching the camera up would clear it but conflicts with the 6-8 deg pitch-down note.
