# QA-tech s09 ROUND 4 (film 17 shots 22-23, g1190-1348, render17/team8 084ef5b) - PASS (no blockers; 3 should-fix)

Checked: all 159 take frames extracted; 14 frames viewed at full size (g1190, 1210, 1260, 1274, 1280, 1290, 1299, 1302, 1310, 1330, 1340, 1345 plus 4-up Dupont and inspector crops); phone_sheet.jpg; per-frame numeric checks on every frame (Laplacian variance, luma, frame diff); beret tracking g1275-1348. QA_AUTO PASS and rhythm 7.62/14.30 taken from files.

## Team claims
1. B1 inspector grin: TRUE. Eyes are smile arcs (g1290, 1302, 1330, 1340), mouth is a visible smile under the moustache, head tilted a few degrees. Dupont's beret no longer touches his face or moustache at g1290/1296/1302/1310/1330 (gap of 60+ px). Caveat: the head reads mostly frontal. The roll is small and, with arc eyes, the gaze toward Bertillon is not readable; Bertillon is at the right, so the grin reads as a general smug grin. Acceptable.
2. B2 head shake: TRUE. Beret x centroid (g:x): 1290:279, 1292:310, 1296:256, 1298-1301:~220, 1303-1307:~268, 1310:203, 1311-1318:~230, 1320-1323:~302, 1325-1329:~238, 1331-1335:~299, 1337-1338:~220, then settled ~243 from g1339. Burst 1 g1291-1310 (right peaks g1292, g1304; left peaks g1299, g1310); burst 2 g1319-1338 (right g1320-23, g1331-35; left g1325-29, g1337-38). Period about 11-12 frames (2.5-2.7 Hz), amplitude about 80 px peak-to-peak (+-40 px), extremes held 4-5 frames, roll visible (tilts in g1299 and g1310 crops). Calm at g1339-1348. Mouth stays flat. Pass. Note: the beret centroid mask is noisy (about 100 px), so the figures are +-10 px.
3. Dupont sunk, dais hides legs: TRUE. No stub legs in g1280, 1299, 1310, 1345. A small brown boot corner shows over the dais edge at g1299 (about 25 px, x 620-650 of the crop), negligible. Torso is cut by the dais at about y 800 and still reads as a seated man in the chair (arms on the rests, both hands out). Chin about y 700-715, well above 880. No head pop.
4. Gendarme cape clears the left edge at g1274: PARTLY. Cape tip and rear foot still touch x 0-3 at about y 780-790 (blue pixels in columns 0-2: 9, 8, 4). Better than R3 but not clear. The gendarme's body is cropped at x 0 from g1266.
5. Inspector trails the group g1190-1210: TRUE. g1190 the blue inspector stands behind and right of the green gendarme (gap about 20 px); g1210 about 45 px behind, stepping. No pop-in.

## Standard checks
- Mouths: none move, no quote window. Inspector's smile is static. PASS.
- Chin above 880: PASS (shot 22 about 540-650; shot 23 Dupont about 715, Bertillon about 400, inspector about 520).
- See-through cards, beam shafts: none. Dust: a few 1-2 px specks on the floor at g1274 (about x 135, y 890), well under 0.5. PASS.
- Blur: Laplacian median 300, min 258 (g1328, 86 %); no frame under 60 %. PASS.
- Frozen: min frame diff 4.8 (g1263); no hold. PASS. Luma 88-109, no black or magenta frame. Only diff spike is the planned cut g1275 (63.5). PASS.
- Leftover geometry: none (the chair, dais, table clamp, jar and stool all sit on their surfaces). PASS.
- Phone size: shot 22 reads (escorted Dupont, inspector trailing, smug). Shot 23 reads: Dupont's flat face and shrug, the shake is clear as a "no", the inspector's smile arcs are visible. PASS.

## Should-fix (non-blocking)
S1. g1280-1348 inspector is cropped by the left edge: kepi and moustache tip touch x 0 at g1290 and about 0-10 at g1330 (moustache left tip). Shift him 15-20 px right, which still clears Dupont's beret (gap is 60+ px).
S2. g1266-1274 gendarme cape and rear foot touch x 0-3. Shift the camera 10-15 px right or pull the gendarme in.
S3. g1280-1345 Dupont's torso has a stair-step notch where the chair armrest cuts the coat and shirt (about x 340-370, y 740-790 at g1290/1330), and the hem is jagged where it meets the dais. Reads as a chair arm overlapping, minor. Tidy the armrest occlusion if time allows.

## Verdict: PASS
Blocking: none.
