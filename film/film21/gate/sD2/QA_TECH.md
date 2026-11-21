# film-13 QA: QA-tech sD2 v3 (team4 68b6ea5)

Take: g642-796 (155 frames, 720x1280, 30 fps), cut in and cut out. Method: every 5th frame (f6, 31 frames), the 1 fps sheet, full-size ffmpeg frames for g645-705 (every 3rd frame for g646-672) and every frame for g784-796 (mouth). Checked against the QA_TEAM_film13 checklist and §B. §G-§L not applied. Colour and exposure are left to the grade. qa_auto PASS. Jitter is clean except the planned CU1 push (g756-765).

## Verdict: PASS (0 blocking)

## v2 blocking items
1. Background soldier's head stacked on Cressingham's hat (g660-755): FIXED. The e1 soldier is gone. Only sky, crag and water sit behind the hat in every sampled frame.
2. Foreground spear poles through Cressingham's face and Surrey's (g685-712): FIXED. The two near spears stop below his chin (tips about y 770 against a face centre about y 640 at g692-705) and cross only his coat. They are well clear of Surrey.

## Checklist
- Mouth: it moves inside the window only. It is open from the whip (g642+), still a small "o" at g791, and closed into a smirk from g792 to g796. PASS.
- Heads below y 880: always above it (the CU1 head centre is about y 450). PASS.
- Frozen, black or magenta frames, and pops: none (qa_auto). The whip at g642-647 is planned. PASS.
- Blur/DOF: none. The only streak is on the whip frames. PASS.
- Plan coverage (row D2): whip in, side-track with the point at the crag (saltires readable), bridge in frame by about g722, stop, CU1 push with the purse slap at g758 (glint and coins), "ประหยัดดี" CU, ease-out to P_BANK by g793, handles keep moving. PASS.
- Feet and props: cards stand on the sand with shadows, and the purse stays on the belt. GROUND.md shows 0 FAIL. The 28 SUNK pegs and sacks look fine. PASS.
- Thai text: none in the take.

## Notes (non-blocking)
1. g646-650: Surrey's face is half hidden behind Cressingham's hat ruff, and the tall spear rack stands at his shoulder. He is clear from g651. Optionally slide Surrey 0.2 m to the right for those frames.
2. g762-777: the raised pointing hand is out of frame on the left (a CU crop; the head and hat are inside the frame).
3. g759-763: the glint star is still about as wide as his torso. Shrink it if the shot is re-rendered for any reason.
