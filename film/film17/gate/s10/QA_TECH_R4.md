# QA_TECH s10 ROUND 4 (g1336-1520, 72847cc) -- PASS (0 blocking, 4 should-fix)
Method: all 185 frames extracted from take.mkv (f6/ frames byte-identical to extracted ones); Laplacian var, frame diff and luma on every frame; full-size views of g1412, 1416, 1510 plus montages (finger 1406-18, boxes 1420-1440, card 1474-1520, approved spot-checks, joins, lid). Rhythm 9.07 / 18.91 (>=4 / >=12): pass.

## Claims
| Claim | Verdict |
|---|---|
| FINGER g1412/1416: calipers+hand span x 0-600, one finger 25-30 px between closing jaws | MOSTLY TRUE, overstated. Real close-up now (Bertillon face left edge, calipers beam x~130-430, Dupont ear/arm to x 720; frame content >=40 % width). A pink finger capsule sits between the jaw tips at g1412 and g1416, so R3 B2 is met. BUT the finger is ~50 px wide (x 335-385), not 25-30; jaws open ~110-135 px and barely move (g1412 tips x~275/410; g1416 ~295/405), so they do not visibly close on it. Calipers' hand not visible (Bertillon's hand out of frame). Reads as "calipers on finger/arm". Accepted. |
| BOXES: dark ~23, lit ~168, one-frame switch, each box | DARK TRUE, LIT NEARLY. Dark = flat 22-23 luma (all five off boxes; g1426 FM/FL 22, g1430 FM 22 / BR 23 / FL 22, g1434 BM/FM/FL/BR 22-23, g1440 all 22-25) vs target <=35. Lit box-top means (70x100 patch incl. rim) at g1420: 118, 128, 135, 126, 146, hero 150 (all >=100; 168 not reproduced, which is fine). Hard single-frame switches, in order: g1422 (front-mid), g1426 (front-left), g1430 (back-right), g1434 (back-mid), g1438 (back-left, checked frame by frame 1437 lit / 1438 black). Hero stays at ~145-150. |
| CARD g1510: 496 px, centred, push-in, warm pool, sharp 15 f | MOSTLY TRUE. Width g1510 ~535 px at the corners (74 %), >=500 and >=70 %: PASS (team understated). Centre x~357, bottom seated in the box behind the drawer front (not floating). Pure push-in from g1477 (card/bbox widens monotonically 263 -> 474+ px by the bright-core measure to g1505, then hold; no pull-out). Sharp: Laplacian 250-260 on g1490-1520 (31 frames). Warm pool: NOT really. Card average is neutral (RGB 182/171/170), shot luma 78-84, surrounding drawers dark; it is the brightest object but reads white/cool, not a warm pool. Unblown (0 % >=248). |

## Regressions / extra checks
- Approved frames unchanged: g1372-1376 Laplacian 82 / 7 / 15 / 6 / 109 identical to R3; g1350, 1373-76, 1390 and 1465 viewed, match R3 descriptions. 3 smear frames only (1373-75).
- Joins: g1421/22 diff 11.0 (just the FM box switch, baseline 8-9), no pop. g1458/1459 diff 13.8 then planned cut 74. Real cuts 1374/75, 1406, 1420 (70), 1459 (75), 1474 (67) all present.
- Blur: QA_AUTO list is a false positive. g1483-90 Laplacian 177-250, g1514-17 ~255; frames sharp by eye. Only g1373-75 are real blur = 3 f, pass.
- Lid g1442-58: hand now carries the lid to the end (R3 S2 fixed); glove still very bright but not checked as clipping blocker.
- Props held, nothing floats: head calipers/cards as R3 (S1 no-hand-on-bar note unchanged), card seated in box, lid in hand. No see-through cards, no beam shafts, no leftover geometry. Dust unchanged 0.4.
- Chins above 880 (Bertillon beard bottom < y 800 throughout), mouths still. Min frame diff outside cuts 3.9 (g1475) -> no frozen hold >1 s. Min mean luma 77 (no black); no magenta.

## Blocking
None.

## Should-fix (non-blocking)
S1. g1406-1419: finger ~50 px, jaws never visibly close, no hand on calipers. Tighten jaws to ~60 px and close over the last 2-3 f before 1420 if re-rendering.
S2. Card shot g1474-1520: no warm pool; card is neutral-white and shot luma 78-84. Dark boxes there read dark grey (~45-50 luma) vs 22 in the box beat, a mild inconsistency.
S3. g1430-1441 camera move crops the leftmost box at x<0 from ~g1430 (lit left box clipped at g1434-37), as R3 flagged.
S4. g1343-1349 caliper bar over Dupont's eyes; no hand on beam g1346-1368 (carry-over from R3).

## Verdict: PASS
R3 B1 (dark 22 vs <=35, lit >=105, hard single-frame switches) and B2 (true close-up, finger between jaw tips) are resolved; card is 535 px / 74 %, centred, push-in, sharp. Approved frames untouched, joins clean.
