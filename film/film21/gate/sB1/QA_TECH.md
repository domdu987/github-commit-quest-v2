# QA-tech sB1 (film 21, g159-298 + handles to 301): PASS
Method: 6 fps (29 frames) plus first/last 4 frames, viewed in 4-up strips; g298, g230 and g301 at full size. 143 frames confirmed (g159-301).

## Verdict
PASS. No blocking defect. Notes below should go to QA-art / the director.

## Checks
- qa_auto blur flag g223-237: FALSE POSITIVE. Full-size g230 is sharp (tree edges, tent seams, shadow edges crisp, no DOF, no motion streak). The frames are a steep top-down swoop over low-detail dark ground, so the Laplacian drops. Accept.
- Camera: high valley, glide south over river (g159-200), steep dive over the camp (g205-240), pull out to a low approach, land at the camp with the sign at left of centre. One continuous move, no pops or frozen runs. g299-301 continue the move (the sign grows), as handles should.
- Sign "ENGLISH CAMP": readable at full size from about g270 (white text on dark blue board, g283-301 clearly legible); too small to read before that. On the phone sheet it is legible from about g280. OK.
- Banners, fire smoke and light shafts: shafts visible g255-301; smoke plumes and banners visible. Knights on caparisoned horses parade from about g250 and are visible at g298 (7.74 s = g 292).
- Heads above y 880: all cast tiny and well above 880. No face above 35 %. Nothing cut at the frame edge. No blood. No mouths (cast too small).
- Floating: nothing floating. Cast has contact shadows.
- Colour: saturated, sky blue, green and orange. Rim light on cards is a known film-wide limitation, noted, not failed.
- Join in: hard cut at g159 (plan CUT 1); no previous take needed.

## Issues (non-blocking)
1. g205-240: the frame is very dark and murky (VIVID grade at the steep dive) while g159-200 and g250+ are bright. It reads as a brightness dip mid-move. Fix (optional): lift the grade through the dive (cam_path VIVID ease), keep luma 85-110.
2. g250-301: the lower 40-50 % of the frame is a plain green meadow with a few tents, which is close to the "empty flat ground" of §H3. Fix: add props, people or a fence to the foreground, or tilt up so the camp fills the frame at P_CAMP.
3. g235-301: the grey crescent "smoke" billboards look like flat grey slabs (hard-edged curved blades), especially g215-230. Fix: soften or tint them as smoke, or swap for particles.
4. g298: the parade is tiny, riders about 20 px high, so "knights on caparisoned horses" reads weakly on a phone. Fix if cheap: end slightly lower or closer.
5. The cast cards read as flat 2D against a boxy 3D set (known set limitation, rim light as well).

## Director note (2026-11-20 18:30): PASS REVOKED for palette continuity
B1 was rendered on the OLD valley palette (red/lime neon fields, murky mid-dive). After the set palette fix (08c9d4b) it would visibly clash with its neighbours. It is being re-rendered by team 7 on the new palette, with the same path and the same end at P_CAMP.
