# QA_TECH s18

## Round 2 - FAIL
Checked: qa_auto PASS, meta g0 1384/g1 1468 handles 9/9 DIS 11 OK, no actors, no text, no black/magenta/frozen, mouths n/a. Snap g1430-1446 on จาไมกา present.
1. framediff median 3.11 / p90 7.85 (limits 4 / 12): fails both. Fix: stronger slide/push, more foreground motion (spray, swell crest), a larger snap.
2. g1415-1468: after the push the ship is cut by the LEFT frame edge (stern and most of the hull gone) and a large blue gull flies through the sails clipped at the left edge (g ~1440-1450). Fix: slide the camera the other way or push less so the whole ship stays in frame; keep the gull behind/away.
3. g1384-1440: a blown-out white sun glint on the water right of the ship reads as a hole; NOTE (bow wave 'sled' kept small, OK).

## Round 5: FAIL
Checked 6 fps + cut g1384/g1468 +-3 (take g1375-1476), qa_auto PASS. No actors, no text/black/magenta/frozen. Frame-diff g1385-1467: median 2.75 / p90 9.23 (rule 4 / 10): worse than round 2 on the median (3.11).
Earlier: R2-1 NOT FIXED; R2-2 ship clipping FIXED (whole ship stays in frame, no gull clipping); R2-3 sun glint still a blown-out white blob (NOTE).
1. g1385-1467 (frame-diff): median 2.75 < 4 (and p90 9.23 < 10). Fix: stronger slide/push (>= 10 %/s), bigger snap on จาไมกา (g1430-1446, x1.4+), foreground swell/spray motion; re-measure.
NOTES: g1384-1445 white sun glint on the water reads as a hole; small ship far lower half teal.
