# QA-tech sA2 (hard-defects rule, bef3a22)

**PASS** (hard defects only)

Checked consecutive frames g90-130 (frame-by-frame diff, phase-correlation shift, contact sheets).
- Splice g94/95: smooth, continuous slow descent, no jump.
- Roll flip g102/103: none. The river runs diagonally at g101-103 and levels out smoothly by g108; horizon rolls in one direction only.
- Splice g125/126: smooth. The 124-126 frames match, with no cut and no dark frame. Brightness 77, 79, 79.
- No black, blank or magenta frames; no frozen run (g126-130 drift slowly, diff 2-10).
- qa_auto blur g100-116 and jitter 15.5 px in second 0: a fast forward dive through the pine canopy. Motion is monotonic (down and forward, content grows each frame), with no sign-flipping back-and-forth. Blur is motion blur on a fast move, so it is OK.

Notes (not blocking): g100-110 is dark and the exposure ramp is heavy. g116-119 is very busy, with trunks and a rock slab passing close, and g119 is a brightness spike (mean 108).
