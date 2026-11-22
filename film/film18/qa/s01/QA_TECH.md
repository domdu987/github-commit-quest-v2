# QA-tech round 16 s01: FAIL
Checked: all 162 frames, 4-frame steps g60-95 plus 1:1 left-edge crops at g60/64/72/76/80/84/88, ends g20/g155. Ground (director) 0.280 OK.

## Blockers
1. g72-g90: oxen half-cut by the left frame edge (rule "no half-cut characters"). A dragon-coated ox is about 60 % off-screen at g72-80 (head out of frame, only rump and hind legs in); a second ox rear/hooves are cut at x 0-30 at g82-88. Fix: remove the herd oxen in the left strip (about x < 90 px at y 500-800) for g70-92, or shift the herd/camera so they leave frame completely by g70.

## Previous blocker status
- Plaque post: FIXED. At g60-68 the post stands right of the ox face at x ~130-150 (g60) and x ~85-130 (g64), no face under it. The plaque board itself overlaps the top of the g60 ox's forehead (note). No rider remains.
- No rider is present at g76-90.

## Notes
- Hero g155: Tian Dan ~42 % tall, head far above 860, one cap, clean. No pulsing, mouths still, no placeholders.
- g20: Tian Dan tiny but the rich set reads (roofs, braziers, 70 oxen).
- Brazier shaft still glows as a white bar at g155 (x ~800 on the 360 tile).
