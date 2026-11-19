# QA_TECH s10 (film 13, TAKE gate) - FAIL

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s10/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS; pop g650 = cut 10->11 (3 early per G1).
1. g 612-649 (narr ~20.4-21.6 s): rich's mouth is wide open (laugh) for 38 frames before Q1 opens at g 653 (+-4). Rule: mouth only inside quote windows. The plan says 'laugh_big, no mouth sync'; frames show open mouth flapping from g ~612. Fix: use a closed-mouth laugh (eyes squeezed, shoulders shaking, tear) until g 649, or get a documented override (second opus reviewer, QA_TEAM E).
2. g 585-649 (shot 10): plan 'rich in armchair with tea, looks out the window'. Delivered: standing in front of the wall under a chandelier, no armchair/window, no look out. Frames 585-610 he faces camera with a deadpan frown, then laughs; no eye-line to a window. Fix: use suite_window preset with the armchair, rich turning head to the window before laughing.
3. g 650-731 (shot 11): rich holds no cup (cup left on the table, visible at right) though he held cup + saucer through g 585-649: prop continuity pop at the cut. Fix: cup stays in his hand or is placed down visibly.
4. g 650-731: plan 'points down at Pullman far below'. He points right/up with a raised finger (sideways), looks at camera. Eye-line/gesture does not target anything. Fix: pose point_down, head turned to window.
5. g 650-690: chandelier lump enters top of frame and is clipped by the frame top for 40 frames; rich head sits at y ~ 480-560 with nothing else, 40 % empty carpet foreground (y 780-1280). Fix: frame tighter on rich + window.
6. Mouth in Q1 (650/653-731+): open and varying; lip activity starts g ~648 which is inside 653 +-4.5. OK.
7. G1 cut offset (650 vs 653; shot 10 start 591 vs 594; handle g 585-590 present).
Heads < 880. Scale OK. Join s10->s12: s10 ends in suite (g 731) while s12 begins on the facade at g 720; plan cut 729 is covered by both takes' handles: OK.
