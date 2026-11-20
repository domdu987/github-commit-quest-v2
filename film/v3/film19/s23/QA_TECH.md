# QA_TECH s23 - PASS (non-blocking notes)
Checked: qa_auto PASS (cut g1933 not visible, expected), 6 fps + cut +-3 sheet g1847-1937, meta g0 1856 / g1 1932 (plan 61.86-64.44 -> 1856/1932 OK), DIS 15 in with 9 f handle, hard cut out with 9 f handle OK, framediff median 4.44 / p90 12.31 OK. Old Harrison (white hair, spectacles, brown coat) OK, EVENING hall_door OK, H4 watch attached to his right hand throughout, smile fixed, no lip movement, head centre y 534-631 (bottom 693), no text/blur/clipping, snap g1896-1915 + crane/arc visible.
Issues (non-blocking):
1. g1847-1902 (plan coverage): "shuffles in at the door" does not read. Harrison stays at the same place inside the recess behind the open leaf (walk-in-place); he never crosses the door line, only the camera moves. Fix: translate him from the recess to the front of the door over g1847-1880 (move the actor, not only the cycle).
2. g1847-1937: shoes have no readable contact shadow on the dark floor; slight float on the lifted-foot frames (g1862, g1892). Fix: add a blob shadow.
3. g1907-1937: he is small (head ~ 120 px) after the arc; the "king hears about it" beat has low phone legibility. Note only.

## Round 2 - FAIL (marginal)
Checked: qa_auto FAIL on blur g1847-1853 only (these are the 9 in-handle frames where Harrison is behind the door leaf; not in-shot, NOTE); 6 fps + cut +-3 sheet g1847-1937; meta g0 1856 / g1 1932 OK, DIS 15 in, cut out, 9 f handles OK; frame-diff median 4.41 / p90 11.34 (measured; meta says 11.34, round 1 had 12.31).
Verification of round 1: 1 shuffle-in FIXED (Harrison now travels from the recess past the leaf and out to the room front; reads as entering). 2 contact shadow PARTLY (a faint blob exists on the lit boards, none readable on dark boards; NOTE). 3 small head: head 100-125 px g1907-1937, NOTE.
Issues:
1. p90 11.34 < 12 (hard limit). Fix: stronger slide/arc in g1870-1895 where pairs sit at 3.5-4.5, or a second small snap.
Notes: (a) g1847-1858 Harrison half hidden behind the open door leaf (reads as a peek, ok). (b) the hall is very dark g1907-1937, low phone legibility; old Harrison, spectacles, H4 in right hand, evening light and fixed smile all OK; head centre y 450-600, none near 880.

## Round 4: PASS
Checked 6 fps + cut g1933 +-3 (take g1847-1941). qa_auto FAIL on blur g1847-1851 only: handle frames with Harrison behind the door leaf, sharp by eye (false positive, as in round 2). No text, black/magenta, frozen; mouth fixed smile. Frame-diff g1857-1932 median 4.53 / p90 12.95: R2-1 FIXED (>= 4 / >= 10). Entrance through the door, H4 in the right hand, evening light, head centre y 450-650, none near 880.
Notes: g1907-1937 the hall is very dark and Harrison small (~100 px): low phone legibility; contact shadow faint.
