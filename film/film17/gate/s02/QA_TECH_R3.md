# QA-tech film17 s02 round 3 (shots 4-6, render17/team2 c2c810e) - VERDICT: PASS (0 blocking, 3 should-fix)
Checked 52 frames g138-341 (every 5th + g219-225, g282-288), 17 viewed at full size (g138,178,213,225,243,248,253,258?,268,273,282,293,308,313,318,328,338), phone sheet, QA_AUTO (PASS), rhythm 4.18/12.52 (pass).
Standard checks: no black/blank/magenta/frozen frames; hard cuts g222 and g285 clean; image sharp, no blur; no see-through cards, no beam shafts on characters; dust none visible; all chins well above y 880 (shot 5 tallest: chins ~y 740-780 at g273-282; shot 6 thief chin ~y 700-720 at g338); mouths closed everywhere (no quote windows), no mouth motion.

## R2 items
- N1 (blue gendarme grip) PARTIAL/FIXED. g243-282: the blue gendarme's arm now extends across and his white cuff meets the thief's upper arm/shoulder (contact reads, g253 x~380 y~760; g273 x~490 y~815). Green gendarme: arm + dark hand dot on thief's shoulder, clear. Blue arm ends in a cuff with NO visible hand sprite; the "pinned hand" claim is only true for green. See S1.
- N2 (hand to brim) FIXED. Hand/fingertip touches the beret brim in front of the face from ~g251 (g253 sleeve up, fingertip at brim y~640) and holds g258, g268, g273 (forearm covers his left eye edge, reads as a salute/tip). Team's g246-270 hold: raise starts g249-251 (g243 and g248 arms still down), so true hold ~g251-284. Closed smile with blush, one-side eyebrow = smirk; reads at phone size.
- N3 (blue gendarme overlaps wagon, shot 4) PARTIAL. g193-218 he stands in front of the wagon rear; at g213 he blocks the rear/door. Acceptable, reads as arrival+escort wait.
- N4 (quill beside thief's hand) FIXED. No quill/pen in g323-338. No floating prop in shot 6.
- N5 (stool clip at left edge g285-298) NOT fixed: dark coat-stand/stool edge still clips left frame edge g285-298; in g338 a dark clipped object at left edge x0-30, y~900-1200 (g333-338). Minor, S2.
- N6 (door hard panel) minor, unchanged; door now swung open and reads as wagon door.
- Smile -> flat at g313 (team question): NOT present. Thief mouth is flat/half-lidded in every shot-6 frame (g285-338, crops compared at g285,288,298,303,323,333); no expression pop, frame-diff on the face region shows only camera-motion change, no spike at g313. The smile belongs to shot 5 only; the change smile->flat is the g285 cut, which is fine.

## Beats at phone size
- Shot 4: wagon visible from depth g138, grows, stops ~g198, green gendarme by lantern, blue gendarme walks to camera. PASS (station door still just a lit white rectangle: weak but acceptable).
- Shot 5: door open, thief standing between two gendarmes with grips, raises hand to brim, closed smirk. "Pulled out" is implied by open door + thief already out, not an animated step-down; acceptable. PASS.
- Shot 6: desk with ledger/books visible, thief shrugs (both hands up, flat face), gendarme raises hand and waves (g318-338) toward the door. PASS.

## Should-fix (non-blocking)
S1 g243-282 shot 5: blue gendarme's grip has no hand sprite (cuff only). Add a hand dot like the green one at the cuff end, x~380-490/y~760-815.
S2 g285-298, g333-338 shot 6: clipped dark object at left frame edge (coat-stand/stool), up to ~30 px wide, y 900-1200 at g338. Shift it out or crop.
S3 g273-282 shot 5: crowding as push-in grows: green gendarme and blue gendarme are cut by frame edge (blue head touches right edge x~720 at g282); keep push 5-10 % smaller. Thief eyes look at camera in shot 6 rather than the gendarme (eye-line, minor).
