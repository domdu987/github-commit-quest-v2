# film17 s06 R2 (shots 14-15, narration 24.08-28.25 s) — render team 5

take: g0 725, g1 850, first_g 719, n_frames 138 (6 handles each side), transition_in dissolve 11 f. 720x1280, 12 samples + OIDN denoise. take.mkv is split (`cat take.mkv.part* > take.mkv`). Shot 14 g719-782 records_desk / EVENING_INT; shot 15 g783-856 records_low / EVENING_INT; hard cut at g783 (frame diff ~24).

## Numbers
- qa_auto.py take.mkv --first_g 719 --cuts 783: PASS (QA_AUTO.md, phone_sheet.jpg); its note about the g783 cut is a false alarm (the cut is a real 24-level jump).
- rhythm.py in-shot (cut excluded): median 5.38, p90 14.12 (targets >= 4 / >= 12).
- Heads: chins < 880 everywhere except the far, tiny walking prefect in g852-856 (882-885, handle frames, a head 28 px radius); heads inside the frame in shot 14 (the earlier right-edge overshoot is gone).

## Director R1 list -> what changed
1. Three fingers: a runtime override of the `three` hand (bright cream glove, ~2.7x bigger, three spread fingers + thumb, ink outline) held still g756-772, beside the prefect's face, inside the frame; camera keeps moving (snap A g746-756 push, snap B g770-780 pull).
2. Prefect arm: bent at the elbow (bend -0.85, stretch 1.0) and he is turned toward Bertillon (yaw 0.45), the gesture points at Bertillon's side of the frame (screen-left).
3. Pince-nez: fingertips on the bridge, arm on the 'top' layer so the hand is drawn in front of the face (g806-816 raise, small push-up wobble after).
4. Scale pop: shot 15 no longer zooms; camera sweeps laterally at constant distance (head ~58-62 px radius for the whole shot), 3 sweeps of 8 frames (g783-791, 808-816, 832-840), no knee crop, no foreground box (fg off in shot 15).
5. Prefect exit: in shot 15 he walks away down the aisle in profile with a walk cycle (cast17.cycle), from beside Bertillon g783 to a small figure at the end. Not back-to-camera (the cast has no back view).
- Should-fix: no mug-shot card on Bertillon (prop_l removed, hand rests on the desk); contact decals stay on; the foreground box no longer covers his feet. Bertillon stays standing at the desk (the set has no chair there): not seated.
- Kept: mouths closed (cast17.silent), shafts hidden, dust 0.4, no DOF.

## Self-check (frames g755, g765, g790, g800, g820, g840 viewed as a 6-up sheet at 360 px tiles of the 720x1280 frames, plus the 6-fps contact sheet)
g755 glove half-raised beside the prefect's head, Bertillon's head near the left edge, inside; g765 glove held, fingers read, arm bent; g790 prefect (profile) beside Bertillon, both full figures, no knee crop; g800 prefect stepping left, Bertillon centre; g820 prefect a small figure at the left edge, Bertillon's hand on his pince-nez; g840 hand on the glasses bridge in front of the face. Not seen at full 720x1280 resolution: the glove fingers and pince-nez contact were judged at tile size.
