# s15 QA: film 10, shots 15-16 (attack): sea, SEA_DAY
Delivered: take.mkv (g 992..1095, 104 frames, first_g 992; g0 998, g1 1090; handles 6+6), 720x1280, 12 samples, ~17 CPU s/frame (shot 15), ~22 (shot 16).
- Shot 15 (g 998-1046): periscope_close, push-in + orbit, captain (cast10 uboat_captain, uboat_periscope -> uboat_aim, fist up g 1024-1038). Head centre y 0.38-0.52 H, chin < 760. 3D periscope hidden (cast draws its own). Mouth shut (no quote).
- Shot 16 (g 1047-1089): torpedo_chase, U-boat dives under the torpedo, torpedo u 0..0.09, s 0..1.6; continues in s17 at u 0.09, s 1.6.
- No DOF, no text, no lines. qa_auto PASS (QA_AUTO.md, phone_sheet.jpg).
- Known: the wake ribbon's square start edge is visible for ~10 frames (g 1058-1070) at the bottom; set limitation.
- Cut at g 1047 only (shot 15 -> 16).
