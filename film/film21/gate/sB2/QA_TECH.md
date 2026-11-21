# QA-tech sB2 v3 (film-13 QA, team5 6d883ba)

Verdict: FAIL (1 blocking issue)

Checked: every 5th frame g295-415 (6 fps) at 360x640 and full size, the last take frames, QA.md, meta.json, GROUND.md, rhythm (median 23.0, p90 30.3), plan row B2. Colour and exposure ignored (normalised at the conform).

Passes: no black, magenta or blank frames, no frozen runs, no pops (0 cuts detected). Crane over the pavilions, flight north over the river with the bridge at the left, and the climb to Abbey Craig are all there in order. Parade is in English red/gold, and the costumes are consistent. The Scots' mouths stay closed (g405-418). The landing is low and looks up, with the five Scots against sky and light shafts (fixes the old looking-down fail). Scots heads sit at y ~600-720 (< 880). GROUND FAIL 0 (the SUNK lines are canvas margin, accepted). Smoke and river glitter direction is consistent with the flight. No Thai text in the take.

## Issues

1. g378-418, BLOCKING. The landing beat barely reads at phone size, so the old fail ("Scots small, on screen only briefly") is only half fixed. At 360x640 the Scots are specks at g385-400 (about 5-8 % of frame height), still small at g405 (about 12 %), and reach only about 22 % of frame height (not the 30-38 % in QA.md) in the last ~8 frames (g410-418). So the Scots are readable for about 0.3 s at the very end of the take, and the camera is still moving at the cut. The frame is also unbalanced at the end: the bottom ~30 % is empty dark slope and the top ~45 % is empty blue sky, with the group in a thin band. The spear shift and the lean are tiny at this size, so they are hard to see on a phone. Fix: land earlier (reach the low position by about g392) and hold still for at least 1.0-1.5 s with the Scots at 30-40 % of frame height. To do that, move the camera closer and lower (about 3 m from the shelf lip) and tilt up less, so the dead slope is cropped to under 15 % of the frame and the group fills the middle third. Keep the spear swing, the lean and the nose scratch inside the held part, and make the spear shift read bigger (spears visibly tilting against the sky). Re-render only g376-418.

2. g410-418, non-blocking. Only 2 of the 5 Scots show a spear (left and right); the plan says they all shift their spears. Fix: give the other three a spear in hand, or have them shift or lean in some visible way.

3. g414-418, non-blocking. The foreground dirt at the bottom of the frame looks soft, which looks like motion streak or soft texture from the camera still creeping at the cut. The client rule is sharp, no DOF. Fix: hold the camera still for the last 15 frames (solved by fix 1).

4. g384-386, non-blocking. The fast climb gives soft, streaked frames and a 2.7 px jitter second (known from qa_auto). Acceptable as a real whip move, but keep it to 3 frames or fewer.

5. g300-325, non-blocking. Small parade extras and horsemen cross y 880 at the bottom of the frame (g305-320), where the caption band will be. They are tiny background extras, not hero heads, so it is acceptable. Check that the caption does not hide the key beat.

6. g295-325, non-blocking. The "ENGLISH CAMP" sign is dark navy with low contrast and is lit from behind. It is readable, but the text is English in a Thai film. Check that it fits the film's sign rules, or drop it.

7. g410-418, non-blocking. The red and black spiky grass tufts at the Scots' feet look like small flames or thorns. Fix: recolour them green or yellow-brown.

Continuity with neighbours (B1 last frame, next take first frame) not checked here: the neighbour takes were not supplied. The D6 in (g295-297 from B1 at P_CAMP) shows the same camp, tents and parade, consistent with the QA.md note.
