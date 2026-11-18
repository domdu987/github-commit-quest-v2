# QA_TECH s02 (film 13, TAKE gate) - FAIL

Checked: qa_auto every frame (plan cuts passed), 6 fps + every cut +-3 frames, full-size key frames, join with neighbours. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13/s02/ (sheet_*.jpg, full/<g>.jpg). Take files untouched.

Global note G1 (all takes): delivered cuts sit at round(t*30) of the plan table, i.e. 3 frames (0.10 s) EARLIER than the plan's g = round((t+0.10)*30) (e.g. shot 3 at 108 vs 111, shot 11 at 650 vs 653, shot 17 at 1107 vs 1110, s26 cuts 1740/1772/1868/1906 vs 1743/1775/1871/1909). qa_auto reports every planned cut as 'no visible change' or as a pop 3 frames off for that reason. Fix: conform must cut at the plan g (handles cover it) or the take must be re-keyed +3 frames; in-shot cues (e.g. nickname jump g895, splash g1893) are not consistently offset either.

Auto: PASS; pop g108 (= the shot 2->3 cut, 3 early per G1), 'no change' at 66/111 (cut offset).
1. g 57-107 (shot 2): beat 'through the window the street drifts down a hair' not shown. Window shows only a distant flat roof field/skyline, no street, hotel edge or any visible downward drift; the background is static for 45 frames. Fix: key the camera/set_lift so the visible street/neighbour roofs slide down ~1-2 % of frame height, include a neighbour facade edge as reference.
2. g 57-107: guests small and low; lower 45 % of the frame is empty carpet (y 700-1280). Gentleman holds a cup, the lady holds only a saucer (no cup on it) from g 57-107 (hand/prop mismatch). Fix: re-frame closer/lower carpet share; give the lady a cup.
3. g 108-164 (shot 3): the tea surface, the point of the shot ('mirror-still'), is almost hidden: only a thin pink sliver behind the cup rim. Cup rim is clipped at the left frame edge (x 0) and a second cup/teapot is cropped at right. The window behind (rooftops 'sliding down') occupies a 150x400 px sliver, no visible slide. Fix: tilt down/raise the camera so the liquid disc is visible, centre the cup, widen the window area.
4. g 57-107: faint horizontal scan-line/moire on carpet and glass (low sample count); phone sheet shows shimmer. Fix: higher samples or texture filtering.
5. G1 cut offset (108 vs 111).
Heads < 880 (guest heads y 330-560). Mouths closed. Join s01->s02 OK (hard cut). Next shot 4 (rain street, g 162) not delivered; s02 ends in tea_close at 164, consistent with plan.
