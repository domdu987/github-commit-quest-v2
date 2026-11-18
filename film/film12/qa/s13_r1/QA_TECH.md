# QA-tech s13 (shots 13-14, DUSK_RAIN) - TAKE gate, g 850-1055
Checked: all 41 f6 frames at full size (g850-g1050), cut g945 (+-3), phone sheet, and every frame g945-g1055 (cropped on the coachman's head) for lip-sync.
Plan coverage: shot 13 shows the dusk street with ONE umbrella among bare-headed people (the umbrella is tiny at phone size); shot 14 shows the head coachman shouting. Light DUSK_RAIN throughout, Hanway same coat/umbrella as s10. Coachman colours (olive coat, brown hat, red nose) consistent. No blur/grain/black/frozen, no text, no pops. Cut g945 is a clean hard cut; dissolve handle g850-g857 is shot 13 as planned.

## VERDICT: FAIL

## Issues
1. g850-g944 heads crossing y 880 (client rule): foreground crowd cards have heads at y about 940-1170 (full frame 720x1280): brown-coat man at lower left (head y about 1120-1170 at g865-g935, hat cut by the bottom edge at g925-g935), green-coat man and red-coat woman at lower right (heads y about 960-1070, g850-g944), teal woman (y about 900-960). Fix: restrict crowd cards to y < 860 head height (move the camera crane or the cards up the street) and remove or push back the near cards.
2. g925-g935 clipping: the brown-coat man's head/hat at the bottom-left is cut by the bottom edge of the frame. Fix: remove or move him.
3. g945-g992 mouth moves before the quote (rule: mouth moves ONLY 33.00-34.95 s, g993-1052): in the "still" phase the coachman's mouth toggles between a toothy open grin and a closed smile in a regular rhythm (toothy at about g945-946, 951-952, 969-970, 976-978, 987-992; closed in between), with winks at g975 and g981. It reads as a mouth flap and as a laugh. Fix: one fixed closed (or fixed grin) mouth for the whole of g945-g992; keep the wink only if the mouth stays frozen.
4. Lip-sync window g993-g1052 is correct: mouth open at g993 (start within 0 frames), closed again from g1053 (within +-4 frames of g1052, inside +-0.15 s). No issue, but note mouth motion is a simple 2-state open/close at about 6-frame cycle, no variation with syllables (non-blocking).
5. g993-g1052 eye-line/acting: eyes squeezed shut (X-eyes) for the whole shout, then half-lidded after; the coachman never looks at the street/Hanway, so the taunt has no eye-line. Fix: open eyes looking down toward the road where Hanway is (camera left/below), at least during the first half of the line.
6. Shot 14 coverage: plan says "others nod" - no other coachmen visible or nodding (QA.md confirms not done). Non-blocking for the beat but plan item missing. Fix: add 1-2 other coachmen on adjacent boxes (frame edge) nodding, or widen the box_seat shot.
7. g850-g944 / phone sheet: "street crowded" reads weakly: about 12 foreground cards plus a far-back mass of grey blocky placeholder figures (they look like blocks, not people, at g850-g940); the ONE umbrella is Hanway's, about 15 px wide at phone size and low contrast against the dark cobbles, so "one umbrella among bare heads" is not legible on the phone sheet. Fix: a closer crane end-pose with Hanway large (or lit by a lamp), more people around him, replace the block crowd with cards or darken it behind mist.
8. g945-g1055 floating: the coachman stands on the plank with his coat hem at the box edge, feet are small dark ovals under the hem at y about 880-900 and there is no contact shadow on the plank; he looks pasted on the box. Fix: sit/stand him lower with a contact shadow and overlap the front panel over his feet.
9. g970-g1000 whip: the whip is a thin straight stick that does not bend or trail and in the raised-arm poses (g1000-g1010, g1045) it crosses the lantern at the left; the whip hand and the arm that waves are different from the other poses (arm appears/disappears between g993 and g1000 where the pose changes). Check for a one-frame arm pop at g1000 (pose change shout -> point_mock). Fix: blend the pose change over 3-4 frames or keep the arm raised continuously.
10. g1053-g1055 handle frames: coachman has a flat sour mouth (closed) - fine; no issue.

Notes (not failures): Hanway's head is at y about 850 (below the 880 limit only by a small margin) at g940; the shot 13 crane move is smooth (no frozen frames); coach colours match s10 (red/yellow coach, brown horses).

## Fix summary
Blocking: 1, 2, 3 (mouth moving outside the window). Also fix 7 so the key beat reads on the phone.
