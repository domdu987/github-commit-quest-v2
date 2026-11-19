# QA s26 (film 14, shots 26-27, g 1758-1919)
- Scripts: team 5's s25 v2 (f77981f); only RANGES changed (26: g1758-1839, 27: g1840-1919); no dissolve baked.
- Shot 27 elephant grade: team 5's material tint had no effect (elephants pale vs soil), replaced by the s15 v3 method (sprite pixels x0.52 + tint (0.78,0.82,1.0), larger darker contact shadows offset along the moon shadow); old shot-27 frames discarded and re-rendered.
- qa_auto on the whole take reports 'suspected blur on 80 frames' (all of shot 27): false positive, the sharpness check is relative to the take median and shot 27 (dark night) sits next to the bright dawn shot. Each half passes alone (shot 26 only: PASS, shot 27 only: PASS).
- Mouths all held/still; no lip-sync. Heads far above y 880 (farmer head y 660-740, elephant heads y 250-560).
- Not eyeballed frame by frame at 6 fps beyond the phone sheet (every 0.5 s) and drafts.

## v2 (director recheck: trunk pops)
- Shot 27 re-rendered: one trunk pose ('sniff') per elephant for the whole shot (no 14-frame swaps), cards turned to at most ~20 deg from the lens (elephant_b at the left edge was 27-34).
- qa_auto on the FULL take (--first_g 1758 --cuts 1840): no pops, no frozen runs, magenta 0 %; only the known false-positive 'suspected blur' on shot 27 (relative sharpness vs the bright dawn shot, confirmed by the director).
