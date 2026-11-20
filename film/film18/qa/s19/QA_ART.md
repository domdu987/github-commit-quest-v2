# QA-art s19 (oxen burst out of the wall holes, 47.56-50.51 s), TAKE gate round 6 — FIX-FIRST (reveal, practical)
I reviewed take.mkv at 6 fps (art8/gNNNN.png, g 1421-1516) at full size 720x1280 and on the 360x640 sheets art8_phone_0-2.jpg.

## Earlier changes
1. Purple ditch: NOT DONE. There is still a flat purple chevron at the lower left (g 1421-1456, y 1000-1280) and a vertical purple strip at the bottom centre/right (g 1461-1516). It is the most visible colour in the lower third.
2. Ground <= 25 %: FORMALLY done by dressing, but the dressing breaks rule 2. It is untextured blue-grey low-poly rocks and navy spiky tufts (g 1426-1456 lower right; g 1501-1516 after the whip). On the phone they read as placeholder lumps, the same navy spikes that were removed from s20 earlier.
3. Flames off heads: still DONE.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 5 | 4 | 6 | 6 |

"Oxen come out of holes in the wall" reads from g 1466. The burning tail does not read. The tail flames are flat red rectangles with a yellow centre, held horizontal, and on the phone they look like small red flags (g 1471-1496). The oxen are also small (10-18 % of the frame height) under a 35-40 % sky.

## Verdict: FIX-FIRST
## Changes
1. **Tail flames, whole take:** Use the flame card from s22. It is tall and licking, with a yellow-white core and a red rim, it reads as fire, and it is parented to the bundle tip. Lean it back about 30-40°. Give each one a warm point light so a warm pool shows on the ground under every lit tail.
2. **Purple strip, whole take:** Find the object by raycast, e.g. `scene.ray_cast` from the camera through g 1481 pixel (x 560, y 1150). Print the hit object and material, then give it the dirt material in dark brown or hide it. If the raycast is not done, pitch the camera up so y > 1000 holds no purple. It must not appear in any frame.
3. **Ground dressing + scale:** Recolour the rocks and tufts warm brown/ochre (earth clods, dark straw, trampled reed), or replace them. No navy or blue-grey lumps. Bring the camera about 30 % closer to the hole row, so the oxen are 20 % or more of the frame height and the sky is 30 % or less.

Notes: The stone rings around the holes and the dust puffs are good; keep them. The whip landing on the field (g 1506-1516) is fine as a whip.
