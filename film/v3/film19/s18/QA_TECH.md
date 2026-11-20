# QA_TECH s18

## Round 2 - FAIL
Checked: qa_auto PASS, meta g0 1384/g1 1468 handles 9/9 DIS 11 OK, no actors, no text, no black/magenta/frozen, mouths n/a. Snap g1430-1446 on จาไมกา present.
1. framediff median 3.11 / p90 7.85 (limits 4 / 12): fails both. Fix: stronger slide/push, more foreground motion (spray, swell crest), a larger snap.
2. g1415-1468: after the push the ship is cut by the LEFT frame edge (stern and most of the hull gone) and a large blue gull flies through the sails clipped at the left edge (g ~1440-1450). Fix: slide the camera the other way or push less so the whole ship stays in frame; keep the gull behind/away.
3. g1384-1440: a blown-out white sun glint on the water right of the ship reads as a hole; NOTE (bow wave 'sled' kept small, OK).
