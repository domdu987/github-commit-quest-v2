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

## Round 11 (director QA-tech) - FAIL (marginal: one number, 9.95 vs 10)
Take g1375-1476 (102 f, 720x1280, 30 fps). Frames: /tmp/qa19_r11/s18/ (6 fps f6_*.jpg, plus every frame g1426-1448 around the snap).
Numbers (in-shot g1384-1467, qa_stats.py formula, ffmpeg bilinear 90x160 grey):
- luma 100.75 (85-110) PASS; per-frame luma 91.0-109.6, so no frame leaves the band. All 102 f incl. handles: 100.68.
- saturation 0.641 (>= 0.47) PASS.
- frame-diff, 83 consecutive pairs g1384->1385 .. g1466->1467: median 4.78 (>= 4) PASS; p90 9.95 (>= 10) FAIL. Other windows: g1385-1467 median 4.89 / p90 9.97; g1384-1468 4.89 / 9.93; g1383-1468 4.78 / 9.92. No window reaches 10. (meta.json says 4.79 / 9.96, which agrees.) Range min 2.27, max 18.6 (snap g1433-1437).
Checks: no black/magenta frames, no frozen runs (smallest pair diff 2.27), no pops (only the snap, g1433-1437 diffs 15-19, smooth push+pan, and the planned dissolves outside the shot). No character cut by a frame edge (ship whole in frame the whole shot; clouds clip at the edge, fine). William face about 2-4 % of frame height (<= 35 %), head y about 600-700 (< 880). Nothing floats: William stands on the forecastle deck throughout; hull with a white bow wave/foam, no bare planes, sky/sea fully textured. No prop through a face (the long jib sail passes beside his head from g~1445 but not over it). Mouth: closed smile, no movement. Blown-out: pure-white fraction at most 0.48 % of the frame (g1401), only small glint dots and foam; no holes.
Issues:
1. Frame-diff p90 9.95 < 10 (g1384-1467). Fails the rule by 0.05. Fix: slightly more motion at the quiet ends of the shot, e.g. a stronger first-half slide/push (g1384-1427, diffs there are the lowest) or a larger/longer snap; then re-measure with the same range. Median is fine.
2. William still: the card holds one pose (smile, watch arm raised) for the whole shot, g1384-1467 (2.8 s); it only rides the ship's roll. Breaks I.5 (nobody still > 1.5 s). Fix: add an action, e.g. raise the watch and look at it, a head turn or a wave, with a visible change about every second, and a small expression change on the snap (g1438). Not judged by pixel tracking (no cv2 here); visual check of crops at g1384/1440/1467.
3. g1384-1425 (NOTE): sun glint still shows as 2-4 bright white blobs on the lower-third water (g1384-1412 largest). Reads as a sparkle, not a hole, but still the brightest thing in the bottom third. Lower further (x0.01) or drop it.
4. g1384-1440 (NOTE): William is about 2-4 % of frame height and in front of the sails, so the watch is barely readable; at g1450-1467 a foresail panel covers his lower legs/feet, so contact with the deck is hard to see. Fix: move him to the bow rail clear of the jib, or crane/push more on him after the snap.
Colour (round 10 blocker, luma 122.7) FIXED. Sun-glint lowering and camera drift in g1444-1467 confirmed present (no parking).

## Round 12 (director QA-tech) - PASS
Take g1375-1476 (102 f, 720x1280, 30 fps). Frames: /tmp/qa19_r12/s18/ (f6_*.jpg at 6 fps, snap_1425..1450.jpg every frame, full_*.png, crops wil.jpg / wil2.jpg).
Numbers (in-shot g1384-1467, 84 frames / 84 consecutive pairs, 90x160 bilinear):
- luma 100.7 (85-110) PASS; per-frame 89.8-111.7 (mean is what counts; two or three frames touch 111). saturation 0.640 (>= 0.47) PASS.
- frame-diff mean-RGB grey: median 5.87, p90 11.03 PASS (>= 4 / >= 10). ffmpeg gray: median 5.82, p90 10.81 PASS. Min 1.98, max 17.8 (snap peak g1431-1435). meta.json 5.99 / 11.06 agrees within method noise.
Checks:
- William acts: g1384-1416 looks down at the watch (eyes closed/down); g1424-1432 head turn/glance up; g1436+ raises watch toward the island, hand on hip, excited eyes, small hop g1436-1456; g1448-1467 holds up. Visible change about every 1 s; longest near-static stretch g1384-1416 (about 1.1 s, only small head/arm drift) < 1.5 s PASS.
- Island: green sand-rim dome with palms is a sliver at the left horizon from g1425, clear on the snap (g1438, about 6 % width) and about 14 % of width at g1467; the snap pans toward it PASS (R11 art issue fixed).
- No character cut by a frame edge (ship whole throughout, at g1467 William is at x about 516 of 720). Face about 3 % of frame height (<= 35 %). Head y about 590-700 (< 880). William's feet are on the forecastle deck, no float. No prop through a face. No pops (only the planned snap), no black/magenta, no frozen runs (min diff 1.98), mouth closed (no movement). Pure-white fraction <= 0.43 % per frame; no blown-out holes; no bare planes. Bow foam is matte white, no sun glint blobs.
NOTES (non-blocking):
1. g1384-1398: diffs are flat ~2.0-2.3 (quiet start), steady but the slowest part; the median is carried by g1400-1470.
2. g1444-1467: a foreground foresail panel covers William's shin/feet region, so deck contact is only partly visible (the legs end on the deck line behind the panel). Not floating, but crop at g1450+ shows no contact shadow.
3. g1384-1410: a small log floats in the sea at lower left, reads as a prop and is fine.
4. William's pose change in g1384-1416 is subtle at phone size (head about 26-40 px); the clear action is g1436+.
