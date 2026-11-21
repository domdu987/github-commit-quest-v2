# QA-tech s05 (shot 13, render17/team5 d1bbc7c, g645-731, used g651-725): FAIL

Viewed full size: g655, 675, 695, 710, 725 (f6) plus phone sheet, a 12-frame crop strip g685-696 (taken at take index 40-51, i.e. g685-696) and zooms of the mimic. Auto: PASS, rhythm 5.09/12.64, magenta 0 %.

## Blocking
B1. The mimic does not read (whole used range, checked g680, g700, g725). The beret prisoner (x~210-290, y~570-740) has a thin grey sliver at his cheek/collar, about 8x30 px, which is a barely-visible caliper stub. It is not at the ear, not recognisably calipers, and invisible at 360x640. This is the shot's gag and the plan beat "calipers on his own ear". Fix: the mimic needs a clear open caliper pair or hand-pinch next to his ear, at least 60-80 px long, in a contrasting colour. Put him on the near side or a foreground slot, or raise his head and hand, so it reads at phone size. Bounce him at 3 Hz.
B2. Camera move is a push-in, not the planned 7 %/s pull-out. Bertillon's head grows from ~105 px (g655) to ~190 px (g725). That is about +80 % in 2.3 s, so roughly 25 %/s. The chandelier and clock also grow. This is the wrong direction and well above the 6-10 %/s rule. Fix: reverse to a pull-out of about 7 %/s with a slide.
B3. The tripod hood is clipping and hiding people. The inspector (blue kepi, right edge) and the right gendarme are partly behind the dark hood and camera body, from g655 to g725 (x 580-720, y 560-780). The inspector is only a half-face and does not read as a laugher or pointer. The team admits this. Fix: move the tripod and hood out of the line of the cast or delete the camera from this shot (the tripod can stay low in the foreground).

## Should-fix
S1. Bertillon is neutral, mouth closed, hands at his sides (g655-725). That is acceptable for the target of the mockery, but nobody visibly looks at him. All laughers face the camera, and the point arms are small. Add a head turn or eye-line toward Bertillon and larger point arms, since the arm shapes are only ~60-80 px.
S2. Pointing reads only for the left prisoner (g655-725, arm toward x~190) and the blue gendarme (arm to x~500). The green gendarme's arm is hidden behind the hood (g655-695). The pointing therefore reads as three people only, and at 360 px the arms are thin.
S3. Bounce amplitude is small: the beret prisoner shifts roughly 4-6 px per frame in the g685-696 strip, with no obvious bounce on the others. It reads as a sway, not as a ~0.06 D bounce at 3 Hz. Increase the amplitude and add per-character phase offsets.
S4. The mouths are open-held "ah" shapes and the eyes are laugh arcs with tears. No lip-sync, so this is OK. Note that the blue gendarme's mouth is hard to see at phone size.
S5. The bookstack on the stool at the lower left (x 180-270, y 830-1000) has no purpose. It is a loose prop floating beside the empty floor, not held by anyone. It is a stool plus a book stack, which is set dressing. Confirm it is not leftover geometry from another set.

## Passed checks
- Chins: all chins are above y 880 (Bertillon's lowest is ~y 790 at g725; the left prisoner ~y 750).
- No blur: all frames sharp.
- No frozen run, black, blank or magenta frames (auto PASS, in-shot median 5.09, p90 12.64).
- No see-through cards, no beam shafts on characters, no rings or rods. Dust specks are sparse and faint, below 0.5.
- Camera is high angle as planned.
- Laugh faces read at phone size (open-mouth, tears, closed-eye arcs).
- Bertillon is identifiable (pince-nez, goatee, black coat), but he stands in the foreground at the centre-right.

Verdict: FAIL on B1, B2 and B3. Return to team 5 for a re-render.
