# QA-tech sB2 v4 (film-13 QA, team5 e0be015)
Checked: all 124 frames (frame diff, phase correlation, sharpness), g367-372 and g376-387 every frame, the landing hold g387-418, full-size crops at g350/366/378, QA.md, QA_AUTO.md, GROUND.md, plan row B2. Colour/exposure ignored (conform).

**Verdict: PASS**

## Checks on the v3 blocker and the gate questions
- Landing: the camera arrives at g386 and holds g387-418 (32 frames = 1.07 s) with a gentle drift (about 0.7 px per frame, phase-correlation r 0.8-0.9, no shake). It is low and looks up at the five Scots against the sky and the pine light shaft. The group fills about 35-40 % of frame height (heads y about 510-680, all above y 880), and the dead slope is cropped to the bottom fifth. The spear swing, the lean and the nose scratch all play inside the hold. Mouths are closed. The v3 blocker is fixed.
- qa_auto "suspected blur" g364-383: this is not softness. At full size, tree, shadow and rock edges are crisp at g366 and g378. The low Laplacian score comes from large smooth-shaded slopes, dark shade and sky while the camera travels fast down the hill foot. The renderer has no DOF and no motion blur. Acceptable.
- Splice g369/370: clean. The motion continues (dy 6.2 to 4.7 px per frame, diff 26.0 to 25.5), and the light shafts, trees and river edge are continuous. No jump.
- No black, magenta or frozen frames. Plan beats in order: crane over the pavilions, flight north across the river with the bridge at the left, climb Abbey Craig, land low on the Scots.

## Non-blocking
1. g383-387: the descent ends in a hard stop. The Scots grow from about 8 % to 38 % of frame height in 3 frames (diff 40-61), and then the camera stops dead at g387 (diff 4). It reads like a snap-zoom. Ease out over 6-8 frames (g380-388) if a re-render happens anyway.
2. g385-418: the bright yellow light shaft behind the Scots' legs, together with the dark and red spiky tufts in front, makes them look as if they stand in flames. Recolour the tufts or move the shaft above the knees.
3. 4 of 5 Scots carry a spear (the horn blower does not). Known and accepted.
