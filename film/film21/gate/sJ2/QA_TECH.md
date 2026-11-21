# QA-tech sJ2 (film-13 QA, team11 50d781b)
Checked: all 140 frames (frame diff), every 5th frame at 360x640, full-size g1821/1830/1839/1843/1848; qa_auto PASS.

**Verdict: PASS** (no blocking issues)

## Old fails
1. Camera jump g1787-1788: FIXED. The frame diff is 12.9, 13.5 across it, in line with the neighbours (12-14) and the median 11; no spike anywhere in the take.
2. Faces in the caption band g1813-1847: FIXED. Faces sit at about y 380-720 (g1814 largest at about y 380-700); no head crosses y 880.

## Beats
Whip-in lands on the group by g1714; the head turns toward the bridge (flag and wall visible, g1714-1745), the water, and each other (sweat drops, g1754+). They jump from g1779, splash with crowns at g1799-1809, and three swimmers bob up with floating helmets. Crowns land at g1821, 1830 and 1839 (visible at g1824 large, g1834 second, g1839-1843 third). Hard cut on g1848.

## Non-blocking issues
1. g1824-1848: the three swimmers stand in a fixed row with a near-static pose and neutral, half-lidded faces. Only the mustache shape changes, so "spluttering" does not read. Fix: add head bobs and water spit, wider eyes and mouth.
2. g1839-1848: crown 3 is the weakest, a thin spray behind the right swimmer, mostly hidden by the head. Raise or enlarge it at 1839 and keep it beside, not behind, the heads.
3. g1829-1840: small white hexagon beads in the spray read as polygons; make them round.
4. g1713-1745: the bridge and Scots wall are small and the cards are partly lost against the dark hills. The lit flag does read.
5. g1809-1819: a swimmer card is cropped at the left edge (about 1 head). Minor.
6. English mouths open in drawn shout and gasp expressions (g1774-1790) outside Cressingham's windows; these are fixed face drawings, not lip-sync, accepted.
