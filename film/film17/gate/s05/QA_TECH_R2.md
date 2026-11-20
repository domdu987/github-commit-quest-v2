# QA-tech s05 R2 (shot 13, render17/team2 e553276, g645-731, used g651-725): PASS (no blockers; 4 should-fix)

Viewed full size (720x1280): g655, 670, 680, 685, 690, 710, 715, 725, plus 2x zooms of the mimic (g655, g725), the phone sheet, and a per-frame analysis of take.mkv (87 frames, 360x640: Laplacian, frame diff, beret tracking). Auto: PASS, rhythm 4.46 / 13.62.

## Claims
- B1 (mimic): TRUE. The beret prisoner is in the foreground-left. Head is ~140 px at g655 and ~105 px at g725, about 130 in the middle. A silver caliper in his raised right hand sits at head/ear height: a ~300 px L-shaped beam with a fixed jaw, hand knob at the right end by his right ear, and the bar running behind his head and down to the left. The hand holds it (black knob grip). The beam is larger than the claimed 90 px, which helps. It reads as "instrument at the ear" on the phone sheet (g645-720). The admitted bar-not-open-pair is acceptable. The bar is occluded by the head, not see-through. Bounce is ~10 frames per cycle (about 3 Hz), roughly +-6 px at 720 wide. Small but visible.
- B2 (camera): TRUE, direction measured. Bertillon head ~110 px (g655) to ~85 px (g725) = -23 % in 2.3 s, about 10 %/s pull-out. The mimic shrinks 140 to 105 px. The chandelier and clock also move. Lateral slide present. Frame diff shows 3 smooth ramps (take idx ~22-34, 35-43, 66-78, peak 14-21) and no single-frame pops. Characters are cards on the set, they move with it, no pops.
- B3 (hood): MOSTLY TRUE. Nobody is hidden. The inspector (top right, blue kepi) is a full laughing face with eyes arcs, open mouth, tears and a visible arm. The dark hood cloth (x550-650, y590-780, g685-725) covers his torso and legs. Minor.
- Pointing: TRUE. Blue gendarme's arm toward Bertillon is ~150 px, the green gendarme's arm is visible (~110 px) all through g655-725. Prisoner pointing: only the mimic's own gag and the bench prisoners in the background. No eye-lines toward Bertillon (everyone faces the camera).
- Bounce phase offsets: not measured per character (only the mimic, period ~10 frames). Visually the others move less. Treat as claimed-but-weak.

## Checks
- Chins: all above y 880 (mimic lowest ~830 at g680, Bertillon ~790). OK.
- Mouths: open held "ah", laugh arcs with tears, no lip-sync. OK.
- Blur: min Laplacian ratio 0.84 of the median. No blur frames (limit 3). OK.
- Freeze: min frame diff 2.7, no frozen hold. No black or magenta (magenta 0 %).
- Dust: a few faint specks, well below 0.5.
- See-through cards or beam shafts: none. Beam is occluded by the head, sits in front of the green gendarme at g725 (hand-held, so OK).
- Props held: calipers by hand. Bookstack on the stool (x170-250, y820-960) is not held; it is set dressing, carried over from R1 S5, still unexplained.

## Blocking
None.

## Should-fix
S1. Mimic is cropped by the left frame edge during the slide: g680-g690 and g710-g715 (head x < 0..15 px, beam tip off frame, ~y 720-800). Reduce the slide or move him ~60 px right.
S2. Blown-out near-lens chandelier globes cover the top-right (g685-g715, x430-720, y0-310, pure white, no contour). Distracting, and it competes with the laugh. Raise or move the fixture, or fade the lamp emission.
S3. The dark hood cloth looks like a black sack hanging in front of the inspector/gendarme (g655-725). Tuck or shrink it so the inspector's torso reads.
S4. Eye-lines and bounce: laughers look at the lens, not at Bertillon, and non-mimic bounce is small. The bookstack on the stool is a loose prop; remove or attach it.
