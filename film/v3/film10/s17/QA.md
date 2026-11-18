# s17 QA: film 10, shots 17-19 (the reveal): sea, SEA_DAY
Delivered: take.mkv (g 1084..1433, 350 frames, first_g 1084; g0 1090, g1 1428; handles 6+6) split into take.mkv.part* (cat to rebuild). 720x1280, 12 samples, ~29 CPU s (topdown), ~17 (pov).
- 17 topdown A: torpedo (scaled 1.8) creeps up, ship sails right, gold buoy (moved to x 64) fades in and pulses; camera tracks right. No lines/arrows.
- 18 periscope_pov: lens overlay, dazzle ship; translucent cyan ghost (facing the other way, offset +30) fades in over it to 0.8; cyan aim buoy lights at the end.
- 19 topdown C: torpedo runs at the ghost's course (cyan buoy x -41), crossing ~g 1347; wake passes behind the real stern; ship sails on toward the gold buoy; ghost fades 0.8->0.4.
- Torpedo/sea time continuous with s15 (u 0.09 at g 1090, s 1.6). Cuts at g 1194 and 1296. qa_auto PASS. No DOF, no text. Phone sheet reviewed: buoy, ghost and wake read; ghost over the stripes is busy at phone size in 19.
- Set changes at runtime only: lead buoy moved +23 D, torpedo scaled 1.8, periscope head/mast hidden in the pov shot.
