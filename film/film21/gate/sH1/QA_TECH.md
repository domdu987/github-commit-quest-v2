# QA-tech sH1 (film-13 QA, team9 5d1d82b)
Checked: all 110 frames (frame diff), every 5th frame at 360x640 plus g1309-1313, 1319, 1329, 1334 at full size; qa_auto PASS.

**Verdict: FAIL**

## Plan coverage
Scots run in with spears (g1239-1274), the camera overtakes and swoops over the river to the bridgehead (g1279-1304), the Scots wall closes with banners (g1309-1324), and the deck ends at the wall (g1329-1344). The English lose helmets (flying helmets visible g1329 and g1334). The camera ends level, with the English standing in rows, hopping back.

## Issues
1. g1308-1312, BLOCKING: a flat bright-green polygon (bush or tree at the lens) covers the right half of the frame at g1309-1311, and frame diff spikes to 43 at g1311. It reads as a pop and hides the Scots wall. Fix: cull or move this object out of the camera path (or move the camera 2 m left) for g1305-1314.
2. g1274-1304, non-blocking: for about 26 frames no cast is visible (bare dirt at g1279, then river and far valley). The swoop is planned, but it is empty. Fix: keep the runners or the red column in the lower half of the frame.
3. g1329-1344, non-blocking: most English keep their helmets (only 1-3 helmets in the air at g1329-1334; all helmeted again at g1339-1344). The helmet-loss beat is weak. Fix: a bare-head variant or more flying helmets for the front rank.
4. g1334-1344, non-blocking: Scots wall cards at y 300-500 are tiny and read as a blue blob. Heads of the English are at y 700-1000, hmm top rows at about y 800-840; none are at or below y 880 except the g1329 front English (face at y 760-830, chin about 840). Within the limit.
5. No frozen runs, no black or magenta frames, no mouth issues. Colour ignored.
