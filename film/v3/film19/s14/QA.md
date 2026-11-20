# s14 QA: film 19, shot 14, the REVEAL IMAGE (WORKSHOP shop_clock DAY, set_clock([1, 4]))
- Take g 1007..1104 (98 frames, 720x1280, 8 spp). Shot = g 1016..1095 (33.86-36.52 s); in-handle g 1007..1015 (dissolve 11 f in), out-handle g 1096..1104 (dissolve 11 f out). take.mkv crf 6, first_g 1007. QA_AUTO PASS.
- Image: the big brass H1 (bars rocking, set_balance every frame) at left, the small silver H4 (tick marks, two hands, no numerals) on its red cloth beside it, Harrison (default, greying, apron) standing behind with a happy smile, holding out an open palm toward the H4 (g ~1039-1055, then a small thrust on the snap). Captions: "แล้วเขาก็ย่อ" g 1017, "มันเหลือแค่" g 1038, "เรือนกลม ๆ" g 1059, "เท่าจานรอง" g 1079.
- Camera: wide start (0.9,-2.4,2.5) so the H1 reads big and the H4 small; push 15 %/s, slide -30 px/s, arc 10 deg/s; snap x2.0 (20 f, g 1071..1091, peak 2.8, pan) onto the H4 on "เท่าจานรอง"; H4 tick marks readable in the close-up; still moving at the end.
- Heads 100-211 px wide, centre y 507-583, bottom max 637 (< 880). No text, no DOF, no caption_shade, fixed mouth.
- Frame-diff in-shot (79 pairs): **median 3.45 (below the 4.0 target), p90 13.86 (meets 12)**. The draft read 4.30 / 12.80; the final comes out lower on this bright warm shot (the first 2 s, a wide with little contrast change, are the weak part). Stronger drift (slide -60/-80) pushed Harrison out of the frame at the snap, so I kept him in frame instead.
- s/frame 20.7 wall / 40.8 CPU (two processes).
- Deviations: custom camera (the preset starts too close to show the H1 + H4 size contrast); median frame-diff under target as above. Set H4 is the set's hero-scale watch (about 30 cm), as set3d19 defines it. The H4 overlaps Harrison's lower body (he stands behind it).

## Re-render (lantern set fix)
- Re-rendered with the new iron-cage lantern (h19_shop.py from film19/main); no other change. Frame-diff median 3.44 (still under 4.0), p90 13.86.

## Round 2 re-render (QA_ART 6.5 / QA_TECH FAIL)
- Camera from (0.9,-2.4,2.9) looking down (look z 1.9), push 20 %/s, slide -10, rise 25, arc 8; snap x1.65 (director asked 1.45) with shift (0.65, -0.35), peak 2.5, so the H1 stays the left ~40 % of the frame beside the H4 on its cloth, and Harrison and his palm stay in frame (head x 469-623). The lower frame is floor / bench top, not the washed apron blur. His palm now points at the H4 (hand x 0.95, stretch 1.25 from g 1039).
- Frame-diff in-shot: **median 3.43 (under 4)**, p90 11.18 (under 12). Drafts read 4.30 / 10.58; the final comes out lower again. I could not raise it without cropping the H1 or Harrison out at the snap.

## Round 3 (director's relaxed per-take rule: median >= 4, p90 >= 10)
- Push 30 %/s, rise 40 px/s, arc 12 deg/s, snap shift (0.7, -0.35): frame-diff in-shot median 4.16, p90 11.30. Meets the per-take rule. Framing as in round 2 (H1 left, H4 centre, Harrison and his palm right); in the out-handle after g 1095 Harrison drifts to the right edge (handle only).

## Round 4 (director round-3: median 3.43-3.73 under 4; keep Harrison's hair off the right edge g1088-1095)
- Snap framing unchanged (x1.65, shift (0.7, -0.35), peak 2.5). More drift in the wide before the snap: push 24 %/s (was 20), slide -35 px/s (was -10), arc 14 deg/s (was 8); Harrison's mark moved 1.1 D left so the extra drift does not carry him out of frame. His head right edge is x 673 at g1088 and 707 at g1095 (< 720), hair clear of the edge; H1 stays in frame (bars x ~116 at g1095).
- Frame-diff in-shot: median 4.43, p90 12.84. QA_AUTO PASS. s/frame 22.5 wall / 44.2 CPU.

## Round 5 (director QA-art round 4: 6.6 regression after the 1.1 D mark move)
- Harrison's mark back near the approved spot (0.3 D left, the director's maximum), approved drift restored (push 22 %/s, slide -10, rise 25, arc 8), snap framing x1.65 with SNAPSX 0.6 (shift (0.6, -0.35)) instead of moving him. The wide gets its extra frame-diff from a small handheld sway (0.07 D, 1.5 Hz, +0.035 D vertical, no net drift) instead of more slide/arc, so the camera does not travel right and the H4 does not slide over the H1 upright.
- Checked on the final frames: his head's right edge is at most x 690 over g 1084-1095 (30 px inside 720, whole face and hair in frame); the palm reaches across toward the H4; the cloth is clear of his chin; the H4 dial sits right of the H1 post (the post only grazes the dial's top-left edge at g 1088).
- Frame-diff in-shot: median 4.79, p90 11.44. QA_AUTO PASS. s/frame 21.6 wall / 42.3 CPU.

## Gate G check (face size / edges)
- Max head width 237 px or less over the shot (about 20 % of the frame height); g 1083-1095 head right edge <= x 690: whole face in frame. qa_stats: saturation 0.56, brightness 95.8.

## Round 8 (QA-art round 7, 6.8 FIX) - re-render
- Palm: it is now above the red cloth: the arm sweeps out at shoulder height over g 1039-1050 (arm drawn in front, hand y 0.95 -> 0.30), toward the H4, and is visible in the wide (g 1040-1078); small "ta-da" bounce on "เท่าจานรอง" (g 1079-1087: lean back, squash 1.035/0.965, hop 0.05 D). The cloth itself still stands up (set geometry); the arm is simply drawn above it.
- Never still: eyes on the H4 first (g 1016-1055), then a proud look at the lens (g 1056-1068); expression smile -> happy -> grinning; chest-puff breathing (squash 1.2 %, 1.25 Hz) and a 1.25 Hz lift; blinks at g 1028, 1048, 1066, 1090. No one-expression hold over 1.5 s.
- H1 moved 0.14 D left (root.x keyed every frame): the corner post no longer lands on the H4's crown at g 1063-1095; clear gap between the clocks.
- Snap tilted up 0.13 D (shift (0.7, -0.22)); snap framing otherwise as accepted. Mark, drift and sway unchanged.
- Frame-diff in-shot: median 4.73, p90 10.91. QA_AUTO PASS.
