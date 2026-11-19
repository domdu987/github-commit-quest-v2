# QA s17 (render team 5, film 18) — frames g1309-1387 (+6 handles each side: take.mkv g1303-1393, 91 frames), jimo_in NIGHT
Render: Cycles 12 samples 720x1280, 2 threads, 16-30 s/frame (shared cores). Per-frame cards (c18.py). Rendered four times (see history).

## Frame-diff (90x160 grey, in-shot g1309-1387, n=78)
median **6.26**, p90 **19.81** (min 0.41, max 21.44). Target >= 4 / >= 12: met.
Camera: push 0.03/s, slide -30 px/s, a slow +-3 deg sway every 8 frames and six quick +-10 deg swings (g1316-1320, 1333, 1350, 1356, 1371, 1378).

## qa_auto
PASS.

## Brief items (TEAMS.md / QA_ART_SET_R2 instruction 8)
- Oxen nose-first to the breaches: 6 dragon-coat oxen on the marks (x -41 .. -13.5, y 8.4) travelling -y (toward the wall), cards turned 50 deg off the camera axis so their heads point at the holes.
- NO lit tail before "จุดไฟ" 47.13 s: flame = -1 on every card, tails carry unlit reed bundles; checked every frame g1303-1393 on the 6 fps sheet. Nothing on screen is on fire except the wall torches and the lantern light of the set.
- A townsperson ties reeds: an old man bends (lean 14-32 deg, 4-drawing cycle every 3 frames) at an ox tail; a woman and an old man carry reed baskets to the tails; Tian Dan (point pose) behind. Old man moved toward the lens.
- Real reed foreground prop: the set's upright-rod "reeds" prop was hidden (it read as a slatted screen) and replaced by a real tied bundle of 9 reeds with two red cords, laid low in the lower-left corner, parented to the camera at about 15 % scale. It reads grey-yellow under the night light.
- The set's world reed-jar objects at the lens (`jars`, `reeds`) were hidden: they stood next to the camera start and blocked the frame (the dark cut object at the right edge QA-art noted). Braziers inside the oxen row skipped.
- Ox cards re-baked from the current cast18.

## Checks (6 fps)
Heads above y 880 (heads at y 330-700 of 1280 for the old man). Feet and hooves on the ground with contact shadows. Mouths still. Props held (baskets). Continuity: holes 12, same wall as s16 / s18.

## History / deviations
- First final ended in a huge ox card filling the frame (push 0.09 + snaps ran the camera into the oxen); softened. Second ran median 2.4, third p90 10; the sway + quick swings above is the fourth and final version.
- Tian Dan is mostly off the left of the frame (the lens frames the oxen and the old man); he shows in the first 1.5 s.
