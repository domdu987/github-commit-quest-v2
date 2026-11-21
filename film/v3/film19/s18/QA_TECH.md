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

## Round 13 (director QA-tech) - FAIL (marginal: ffmpeg-gray p90 9.97 vs 10)
Take v2 g1375-1476 (102 f, 720x1280, 30 fps). Frames: /tmp/qa19_r13/s18/ (f6_*.jpg 6 fps, full_000..101.png every frame, index = g-1375; sheet.jpg, wil.jpg crops). Script /tmp/qa19_r13/m.py.
Numbers (in-shot g1384-1467, 84 frames / 83 consecutive pairs, 90x160 bilinear):
- luma 98.44 (85-110) PASS; per-frame 89.5-106.3. saturation 0.654 (>= 0.47) PASS.
- frame-diff mean-RGB grey: median 5.33, p90 10.20 PASS. ffmpeg gray: median 5.24 PASS, **p90 9.97 FAIL (< 10, by 0.03)**. Min 1.75, max 16.6 (snap peak g1431-1435). With g1384-1468 (84 pairs): RGB 5.24 / 10.19, gray 5.16 / 9.97, still fail. meta.json 5.33 / 10.21 agrees with the RGB method only.
- Cause: g1384-1404 is flat 1.8-1.9 (21 pairs, a quarter of the shot, the new +0.1 EV lift didn't add motion) and g1440-1467 settles at 2.7-6. Fix: more motion in the first 0.7 s (start the slide/push or the orbit ramp about 10 f earlier, or a gentle ease-in rather than a dead start), or a slightly stronger snap decay. Even +0.1 of p90 gives margin; aim for 10.3+ on gray.
Checks:
- William: g1384-1409 looks down at the H4 (eyes closed), g1410-1426 head turn / glance up, g1434+ H4 raised overhead on the screen-left (island) side with open-mouth excited face held to the end, warm sparkle on the watch about g1436-1454, hop g1436-1456. Change about every 1 s; longest near-static stretch about 1.1 s. PASS. Open mouth is a held expression, not talking. PASS. Watch now clearly readable.
- Island: clear green dome with palms at the left horizon; width about 32 % at g1440 and 36 % at g1467 (mask measure; the request was 20-25 %, so it is larger, fine), also about 27 % from g1425. Clearly in frame on the word. PASS. Note: the ship still sails toward the camera while the island sits at left horizon level with / behind the hull, so "ahead of the ship" is only partly met (it reads as beside the ship). QA-art to judge; not a tech item.
- Bow wave: smaller, matte white spray with wake rings. No cut by frame edge (ship whole). Face about 3 % of frame height. Head y about 590-700 (< 880). William on the forecastle deck, a sail panel hides his shins from g1445 (contact not fully visible, not floating). No prop through a face. No pops (only the planned snap g1431-1437), no black frames, no frozen runs (min diff 1.75). Pure-white (>=250) fraction <= 0.02 %, no blown-out holes, no bare planes.
VERDICT: FAIL on the single number (gray p90 9.97). Everything else passes; re-measure after adding early motion.

## Round 14 (director QA-tech) - PASS
Take v3 g1375-1476 (102 f). Frames: /tmp/qa19_r14/s18/ (f6_*.jpg, full_000..101.png, sheet.jpg, wil.jpg). Same method as round 13 (/tmp/qa19_r13/m.py).
Numbers (in-shot g1384-1467, 84 frames / 83 pairs, 90x160 bilinear):
- luma 102.04 (85-110) PASS; per-frame 91.9-111.1 (a few frames touch 111, mean is what counts). saturation 0.622 (>= 0.47) PASS.
- frame-diff mean-RGB grey: median 6.90, p90 12.38 PASS. ffmpeg gray: median 6.71, p90 12.17 PASS. g1384-1468 window: gray 6.78 / 12.15, RGB 6.86 / 12.37. Min 2.32 (no frozen run), max 19.9 (snap). Matches team numbers (6.71 / 12.17).
Checks:
- Early pan g1384-1412 works: the near-static stretch is gone (diffs now >= 2.3 from the first pair). No blur or smear: edge-energy (sharpness) is constant g1384-1407 (8.6-9.3) and rises with the push, crops are crisp, no ghosting.
- William: looks down at the H4 g1384-1409, glances up g1410-1426, H4 overhead on the island (screen-left) side with open-mouth excited face from g1434, sparkle about g1436-1454, hop g1436-1456. Change about every 1 s, longest static about 1.1 s. PASS. Open mouth is a held expression.
- Island: green dome with palms at left horizon, about 33 % of width at g1440 and 31 % at g1467 (27 % at g1425); clearly in frame on the word. PASS. Same note as R13: it sits beside/behind the bow rather than strictly ahead (QA-art call).
- No character cut by frame edge; face about 3 % of height; head y about 590-700 (< 880); William on the forecastle deck (sail panel hides shins late, not floating); no prop through a face; no pops except the planned snap, no black frames; pure-white fraction <= 0.13 % (foam only), no blown-out holes, no bare planes.
- NOTE: the violet glow at the bow waterline is still visible as a lavender tint under the hull (not a hole, not blown out). QA-art matter.
VERDICT: PASS.
