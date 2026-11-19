# QA_TECH s12 (film 13, TAKE gate) - FAIL

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s12/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS; planned cuts 729 / 846 'no visible change' (brick-dominated; by eye: facade framing change at g 780, crowd cut at g 843 i.e. 3 early per G1).
1. g 836-841 (6 frames): Pullman's head enters from below frame edge and sits across the caption band: head centre y ~890 / chin ~930 at g 840, still chin > 880 until ~g 841. FAIL per rule (head >= 880). Fix: re-render g 820-842 ending the crane with a tilt-down so Pullman rises into frame from the sides, or start him already standing at y < 800.
2. g 720-815 (shot 12): framing is an extreme close crop of brick wall (~85 % bricks, windows, cornice), rich only ~60x100 px at the top; no street, no Pullman, no dense set. Violates client taste (no constant extreme close-ups, show the dense set) and plan ('medium two-shot from street'). Fix: pull back to a hotel_front wide with rich in the top window and Pullman visible below, even if rich is small; push-in on rich for the 2nd framing.
3. g 815-842: rich leaves the top of frame at g ~815 while Q1 runs to narr 28.09 (g 846): the last ~1 s of the quote has no speaker on screen. Fix: keep rich in frame until g 846 (crane stops higher / the plan's two framings).
4. g 720-780: rich stands rigid in the window, no leaning/pointing at Pullman; talk_mouth active for the whole shot (all inside Q1, OK).
5. g 843-917 (shot 13): crowd cards fill the whole bottom half; foreground lady heads sit at y ~790-875, i.e. chins touch the band (within 5-10 px of y 880) at g 844-870 for the left/right foreground cards; borderline. Fix: lower camera tilt or move the foreground cards back ~0.5 D.
6. g 843-917: crowd 'laugh and point' reads weakly: foreground ladies smile with arms up, only 3-4 faces laugh; nobody points at Pullman. Pullman carries the jack on shoulder correctly (attached). Bottom 20 % is smooth mud with no detail.
7. Nickname beat: shared jump at g 895 is present (29.73 + 0.10 s). OK.
8. G1 cut offset (843 vs 846, 720 vs 729 pre-roll).
Join s12->s14: crowd (g 917) -> street/trench (g 912+): hard cut, OK.
