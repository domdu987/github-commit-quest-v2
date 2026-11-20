# QA s19 (shot 19, SHIP ship_coast DAY_JAMAICA, g 1468..1580 + 9 handle frames each side, take g 1459..1589) -- re-render after the TAKE gate (QA_TECH FAIL)
- Frame-diff in-shot (90x160 grey): median 6.64, p90 13.50 (target 4 / 12): met.
- Framing (the gate's findings): all three heads, hats, raised hands and the H4 stay inside the frame on every frame (checked on the final raw/*.json: head x 123..605 px incl. margins, head centre y 472-739, chin <= ~840, head w <= 202 px; feet inside). The earlier push-in close-up is gone: the camera is found by a projection search (all three heads + hats + hands inside x 8..712, y>=8, feet <= 1272, no head overlaps) and is a moderate drift (push 3 %/s, slide, arc -5 deg/s) + a snap x1.1 with a pan on "แค่ห้าวินาที" (event g 1497, g 1495..1509) + a second beat (two quick camera bumps g 1526-1542 and 1556-1572) and a bigger cheer (hops x3.6 on the word).
- Sea edge / lavender sky patch (gate items 3-4): gone with the smaller arc (-5 deg/s) and no orbit towards the sea edge; set_sea/set_roll keyed with t = (g - first_g)/30 (t = g/30 floods the beach).
- Sailors re-spaced at +-1.35 D from William (no tangent under the H4).
- Cast: william19 centre (H4 up in the right hand, tricorne in the left), sailor19_a (right), sailor19_b (left) cheering ~3 Hz; mouths still (grins). No text, no DOF, no caption_shade.
- Planned cut at g 1581 is flagged "no visible change" by qa_auto only because the handle continues the same 3D move (as in s01).
- Joins: shot 18 dissolve in 13 f; hard cut out to shot 20.
