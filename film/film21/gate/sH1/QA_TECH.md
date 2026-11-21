# QA-tech sH1 v5 (film-13 QA, team9 e32b60b)
Checked: all 110 frames (frame diff, phase correlation, optical flow on the sky/hill region, near-black block scan, sharpness), full-size frames at both splices (g1273-1278, g1324-1335), g1300-1326 every frame, handles g1342-1348 against sH2a take frames 1-7, QA.md, QA_AUTO.md, GROUND.md (FAIL 0), plan row H1. Colour/exposure ignored (conform).

**Verdict: FAIL** (4 blocking issues)

## v4 blockers
- Tree canopy g1308-1312: FIXED. No green slab anywhere g1296-1338; the meadow tree stays mid-distance.
- Black rectangles at the right edge: NOT FIXED, they moved to g1308-1311 (issue 3). Gone at g1312-1314 and g1324-1328.

## Blocking
1. **g1326/1327, pop at the splice.** The camera jumps from the low side view at the wall's west end (English running in, warm orange light, bush and stone in the foreground) to a high frontal view of the English block (long cool-purple shadows, dark grass tuft, a different bush). Frame diff 57 against 20-22 on the neighbouring frames. The effective seam is here, not at g1332/1333.
2. **g1327-1332 frozen camera, then g1332/1333 pop.** Optical flow on the sky/hills is 0.0 px for 5 frames (the cast still animates, diff 3-5). Then at g1333 the camera jumps back and to the right (diff 35.6; the cloud, banner and wall all shift). The "unchanged" g1333-1348 does not continue from g1332.
   Fix for 1+2: render g1327-1338 on the v5 path. Keep the camera moving through g1327-1332 and blend into the v4/H2a path by g1338 (position and velocity continuous). Use the same light/world state as g1326. Check: frame diff stays under 30 at g1326-1334 and there are no zero-motion runs.
3. **g1308-1311, solid black rectangle.** Near-black (RGB about 7/6/11) solid block, 75-99 x 52-70 px, at x 513-720, y 506-580. It sits at the foot of the right saltire poles, behind the flank Scots, and moves right with the pan. The banners hidden from g1306 are not what causes it: the poles and blue banners are still visible in these frames. Fix: find the object at those pixels at g1309-1310 (object-index pass), then hide it or give it its material, and re-render g1305-1314. Check: no 20x20 block with RGB < 40 outside hair anywhere in the take.
4. **g1306-1310, heads in the caption band.** The near flank group at the lower left has faces at y about 860-975 (clearest at g1309: two faces at x 0-100, y 860-970). Fix: keep that group 2-3 m farther from the lens, or raise the camera's look target, so every head stays above y 860 during g1305-1311. Re-render it in the same range as issue 3.

## Second-2 jitter (12.5 px, g1299-1328): fast smooth motion, not shake
Optical flow on the sky/hill region traces one continuous arc. The camera accelerates left-up to 27/27 px per frame (g1299-1306), swings right-down at 30-39 px per frame (g1309-1314), then decays to 15 px per frame (g1317-1322) and 5 px per frame (g1323-1326). The direction never reverses. The only reversal is a single 3-4 px vertical dip at g1321-1323, the slam bump: one cycle, which is acceptable. The phase-correlation numbers at g1302-1316 have r < 0.1 and are not reliable.

## Non-blocking
- g1275/1276 splice: the camera goes from about 1 to 11, 28, then 33 px per frame within 2 frames (a kink rather than a pop), and the distant English red column at y about 660 lengthens by one frame. Small at phone size. Ease the overtake in over g1270-1280 if you are re-rendering anyway.
- g1239-1275: the planned 5 Hz ride shake (dy +-10 px per frame). The client dislikes shake: halve the amplitude or let it decay by g1260.
- g1343/1344: a camera step (diff 30 against 15) inside the H2a match. It is present in H2a as well and sits inside the D6, so it does not block H1.
- Still correct: wall card ranks (blue Scots cards with faces, g1316-1345); chins above y 880 g1327-1345 (lowest about y 850); handles = H2a (mean diff 4.1-4.8 at g1342-1345, sky 0.8-2.1); no black/magenta/frozen frames; mouths closed; plan beats present (ride g1239-1275, overtake and swoop g1276-1306, slam g1316, English hop back, helmets in the air).
