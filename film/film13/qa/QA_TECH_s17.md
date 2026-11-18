# QA_TECH s17 (film 13, TAKE gate) - PASS

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s17/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS; pops g1170 (cut 17->18) and g1252 (18->19) are 3 early per G1; no frozen/black/blur.
Non-blocking notes (verified at 6 fps + cuts +-3):
1. g 1107-1169 (shot 17, plan 'MORNING / two days later'): lighting/sky identical to the afternoon suite shots; nothing signals the time jump. Fix (optional): shift sun colour/angle to a cooler morning key.
2. g 1107-1169: rich 'cup in hand' - cup is held at belly but no hand/fingers visible on it (arm hidden). Eye-line is toward camera, not out of the window ('looks out of the window, smug'). Small head of rich (y 280-500), lower 45 % carpet.
3. g 1170-1251 (shot 18): tea surface now visible and still (ripple 0), push-in present, window slightly shifts. OK. Cup rim at left slightly cropped g 1170-1176 only.
4. g 1252-1302 (shot 19, Q2 g 1255-1300 +-4): mouth closed g 1252-1257, moves 1258-1296, still open at 1301-1302 (1 frame past 1300, within +-0.15 s). OK. The raised cup sits against the gentleman guest's hat/ear (overlap, reads as the guest holding it) at g 1271-1302. Fix (optional): nudge the cup arm 0.3 D to the right.
5. G1 cut offset (1107/1170/1252 vs 1110/1173/1255). Heads < 880. Join s16->s17 OK. Next shot 20 (under_wide, g 1300) not delivered; take ends in shot 19 at 1302, covering it.
