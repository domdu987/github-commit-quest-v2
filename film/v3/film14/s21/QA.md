# QA s21 v4 (film 14, shot 21, g 1362-1458, 97 frames)
- qa_auto PASS on the full take. Sky ramp unchanged: g1368 top-150-row RGB 111.6/105.2/218.2 vs team 4 g1367 110.4/103.6/216.4; g1452 116.6/109.5/222.2 vs g1453 116.5/109.0/218.0.
## Why v3's keys did not show (director's finding confirmed)
The hive's pivot rides the wire's own bow (1.1 Hz ring-down; along the oblique camera that is a ~250 px pendulum), which buried my x-keys; my probe table used Blender data with a wrong hive half-length (0.725 vs the 0.66 body) and ignored parallax.
## v4 changes
- Wire bow (PUSH_A) cut to 0.10 m; unit 1's hook swing/rotation disabled; unit 1's hive + bar world position set LAST by hand each frame (x keyed, y = rest + 0.27 m (level with / just behind the post front), z rest) after set_wire_push + view_layer.update().
- Keys: soft pre-swing to -0.15 m (g1366-1376), run-in accelerating (u^2.8) to the cue offsets 0.30 (g1390, right post), -0.20 (g1410, left post), 0.34 (g1430, right post) m, rebound 15 px over 2 frames, rest apex, next run. Offsets were calibrated by eye on rendered crops at YOFF 0.27 (the camera is oblique, so the contact offset differs per post and per cue frame).
- 5 px post/roof shake for 2 frames + 1-frame 5 px camera bump on each cue. Frame diff (mean abs luma 360x640): g1390 5.65/5.91 (neighbours 2.2-2.3), g1410 5.67/5.75 (2.5), g1430 5.89/5.79 (2.7).
## Hive vs post, MEASURED FROM RENDERED PNGs (measure.py)
Method: 360x640 / 6-sample re-renders of each frame with (A) everything, (B) hive_1 hidden, (C) posts hidden; hive mask = |A-B|, post mask = |A-C|; columns reported at 720 px width. Accuracy about +-6 px (dark hive end vs dark post, 6-sample noise, post penumbra).
- Cue frames: g1390 hive right end 344 vs right post left edge 358 -> gap 14 px; g1410 hive left end 118 vs left post right edge 126 -> gap -8 px (8 px overlap: the hive end just reaches the post edge); g1430 hive right end 418 vs post 428 -> gap 10 px. So at the cues the hive ends are within ~14 px of / at the post edge; NOT exactly 0, tolerance of the measurement included. Honest status: contact reads as 'touching' on the crops, gap 0 exactly is not demonstrated.
- The track (full table below) shows a monotone accelerating run-in to each cue, then a rebound, no pendulum.

| g | hive visible left x | hive visible right x | left post right edge | right post left edge | gap L (hive-left minus post edge) | gap R (post edge minus hive-right) |
|---|---|---|---|---|---|---|
| 1384 | 100 | 306 | 96 | 348 | 4 | 42 |
| 1385 | 100 | 312 | 96 | 350 | 4 | 38 |
| 1386 | 116 | 318 | 98 | 350 | 18 | 32 |
| 1387 | 118 | 324 | 98 | 352 | 20 | 28 |
| 1388 | 126 | 334 | 98 | 352 | 28 | 18 |
| 1389 | 138 | 338 | 98 | 354 | 40 | 16 |
| 1390 **cue** | 154 | 344 | 104 | 358 | 50 | 14 |
| 1391 | 142 | 342 | 96 | 354 | 46 | 12 |
| 1392 | 136 | 342 | 98 | 358 | 38 | 16 |
| 1393 | 136 | 344 | 100 | 360 | 36 | 16 |
| 1394 | 136 | 344 | 100 | 360 | 36 | 16 |
| 1395 | 138 | 346 | 100 | 362 | 38 | 16 |
| 1396 | 136 | 346 | 100 | 364 | 36 | 18 |
| 1397 | 136 | 348 | 102 | 366 | 34 | 18 |
| 1398 | 136 | 350 | 102 | 366 | 34 | 16 |
| 1399 | 138 | 350 | 102 | 368 | 36 | 18 |
| 1400 | 138 | 350 | 102 | 370 | 36 | 20 |
| 1401 | 136 | 350 | 104 | 372 | 32 | 22 |
| 1402 | 134 | 350 | 104 | 372 | 30 | 22 |
| 1403 | 136 | 348 | 104 | 374 | 32 | 26 |
| 1404 | 136 | 342 | 106 | 376 | 30 | 34 |
| 1405 | 122 | 344 | 106 | 378 | 16 | 34 |
| 1406 | 122 | 342 | 106 | 380 | 16 | 38 |
| 1407 | 120 | 340 | 108 | 382 | 12 | 42 |
| 1408 | 114 | 336 | 108 | 384 | 6 | 48 |
| 1409 | 110 | 330 | 108 | 384 | 2 | 54 |
| 1410 **cue** | 118 | 320 | 126 | 390 | -8 | 70 |
| 1411 | 110 | 336 | 106 | 386 | 4 | 50 |
| 1412 | 114 | 342 | 110 | 390 | 4 | 48 |
| 1413 | 114 | 344 | 110 | 392 | 4 | 48 |
| 1414 | 116 | 346 | 112 | 394 | 4 | 48 |
| 1415 | 116 | 348 | 112 | 396 | 4 | 48 |
| 1416 | 116 | 350 | 112 | 398 | 4 | 48 |
| 1417 | 120 | 352 | 114 | 400 | 6 | 48 |
| 1418 | 120 | 354 | 114 | 402 | 6 | 48 |
| 1419 | 122 | 358 | 114 | 404 | 8 | 46 |
| 1420 | 122 | 362 | 116 | 406 | 6 | 44 |
| 1421 | 126 | 366 | 116 | 408 | 10 | 42 |
| 1422 | 130 | 368 | 116 | 408 | 14 | 40 |
| 1423 | 144 | 374 | 118 | 412 | 26 | 38 |
| 1424 | 148 | 380 | 118 | 414 | 30 | 34 |
| 1425 | 152 | 386 | 118 | 416 | 34 | 30 |
| 1426 | 156 | 392 | 120 | 418 | 36 | 26 |
| 1427 | 170 | 402 | 120 | 418 | 50 | 16 |
| 1428 | 174 | 408 | 122 | 422 | 52 | 14 |
| 1429 | 186 | 414 | 122 | 422 | 64 | 8 |
| 1430 **cue** | 200 | 418 | 128 | 428 | 72 | 10 |
| 1431 | 190 | 418 | 120 | 426 | 70 | 8 |
| 1432 | 184 | 418 | 124 | 428 | 60 | 10 |
| 1433 | 184 | 420 | 126 | 430 | 58 | 10 |
| 1434 | 184 | 420 | 126 | 432 | 58 | 12 |
| 1435 | 184 | 422 | 126 | 434 | 58 | 12 |
| 1436 | 186 | 420 | 128 | 436 | 58 | 16 |
