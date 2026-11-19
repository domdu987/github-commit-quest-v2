# QA s21 v3 (film 14, shot 21, g 1362-1458, 97 frames)
- qa_auto PASS on the full take (--first_g 1362).
## 1. Knock timing (hive driven by hand)
- Unit 1's hook swing/twist is disabled (set `hive_swing` returns 0 for its arc); its hive slides along the wire on a keyed curve (shot.py `slide`). The contact limits are measured from the meshes: hive half-length 0.725 m, posts' inner faces x -7.438 / -5.562 -> offset +-0.213 m: the hive END TOUCHES the inner face of its post on the cue frame (never overlaps / in front).
- Pre-swing: g1366-1376 the hive eases to a soft apex 0.15 m short of the left post (no contact), then run-in: 5 frames before each cue it carries ~50-65 % of the travel (hive end moves 45 px before g1390, 35 px before g1410, 44 px before g1430, accelerating), contact frame = hard stop, rebound 11-18 px over 2 frames, rest apex, next run to the other post. Between cues every segment starts from rest and accelerates: the only abrupt stops are the three contacts (no brake at g1419; the old one came from the hook's own swing).
- Contact frames g1390 (right post), g1410 (left post), g1430 (right post). Posts+roofs shake 5 px for 2 frames, 1-frame 5 px camera bump on each cue.
- Frame diff (mean abs luma 360x640): g1390 5.70 / 5.99 (neighbours 2.3-2.4), g1410 5.79 / 5.95 (2.9), g1430 6.06 / 5.81 (2.9-3.0): each contact frame is a spike.
- Screen table (shot.py PROBE=1, same camera + hive keys as the render; hive end vs post inner face, gap 0 exactly at 1390 (R), 1410 (L), 1430 (R)); the full table is probe_table.txt:

| g | hive offset (m) | hive left end x | hive right end x | left post x | right post x | gap L (px) | gap R (px) |
|---|---|---|---|---|---|---|---|
| 1384 | -0.0742 | 119 | 317 | 95 | 346 | -24 | 29 |
| 1385 | -0.0445 | 125 | 321 | 95 | 348 | -30 | 27 |
| 1386 | -0.0083 | 132 | 326 | 96 | 349 | -36 | 23 |
| 1387 | 0.035 | 139 | 332 | 96 | 350 | -43 | 18 |
| 1388 | 0.086 | 148 | 338 | 96 | 351 | -52 | 13 |
| 1389 | 0.1453 | 159 | 346 | 97 | 353 | -62 | 7 |
| 1390 **contact** | 0.2134 | 170 | 354 | 97 | 354 | -73 | 0 |
| 1391 | 0.1384 | 159 | 347 | 98 | 355 | -61 | 8 |
| 1392 | 0.098 | 153 | 345 | 98 | 357 | -55 | 12 |
| 1393 | 0.098 | 154 | 346 | 98 | 358 | -56 | 12 |
| 1394 | 0.0974 | 154 | 347 | 99 | 359 | -55 | 12 |
| 1395 | 0.096 | 155 | 348 | 99 | 361 | -56 | 13 |
| 1396 | 0.0934 | 155 | 350 | 100 | 362 | -55 | 12 |
| 1397 | 0.0894 | 155 | 351 | 100 | 364 | -55 | 13 |
| 1398 | 0.0837 | 155 | 351 | 101 | 365 | -54 | 14 |
| 1399 | 0.0759 | 154 | 352 | 101 | 367 | -53 | 15 |
| 1400 | 0.0659 | 153 | 353 | 102 | 368 | -51 | 15 |
| 1401 | 0.0533 | 152 | 353 | 102 | 370 | -50 | 17 |
| 1402 | 0.038 | 150 | 353 | 103 | 371 | -47 | 18 |
| 1403 | 0.0196 | 147 | 352 | 103 | 373 | -44 | 21 |
| 1404 | -0.002 | 144 | 351 | 104 | 375 | -40 | 24 |
| 1405 | -0.0272 | 140 | 350 | 104 | 376 | -36 | 26 |
| 1406 | -0.0561 | 135 | 348 | 105 | 378 | -30 | 30 |
| 1407 | -0.0889 | 130 | 346 | 106 | 380 | -24 | 34 |
| 1408 | -0.1259 | 123 | 343 | 106 | 381 | -17 | 38 |
| 1409 | -0.1674 | 116 | 340 | 107 | 383 | -9 | 43 |
| 1410 **contact** | -0.2134 | 107 | 336 | 107 | 385 | 0 | 49 |
| 1411 | -0.1438 | 122 | 346 | 108 | 387 | -14 | 41 |
| 1412 | -0.1063 | 130 | 352 | 109 | 389 | -21 | 37 |
| 1413 | -0.1062 | 131 | 354 | 109 | 390 | -22 | 36 |
| 1414 | -0.1056 | 132 | 356 | 110 | 392 | -22 | 36 |
| 1415 | -0.1042 | 133 | 358 | 111 | 394 | -22 | 36 |
| 1416 | -0.1016 | 134 | 360 | 111 | 396 | -23 | 36 |
| 1417 | -0.0974 | 136 | 362 | 112 | 398 | -24 | 36 |
| 1418 | -0.0915 | 138 | 364 | 113 | 400 | -25 | 36 |
| 1419 | -0.0836 | 140 | 367 | 113 | 402 | -27 | 35 |
| 1420 | -0.0733 | 143 | 370 | 114 | 404 | -29 | 34 |
| 1421 | -0.0604 | 147 | 374 | 115 | 406 | -32 | 32 |
| 1422 | -0.0446 | 151 | 377 | 115 | 408 | -36 | 31 |
| 1423 | -0.0258 | 155 | 382 | 116 | 410 | -39 | 28 |
| 1424 | -0.0036 | 161 | 386 | 117 | 412 | -44 | 26 |
| 1425 | 0.0223 | 167 | 391 | 118 | 414 | -49 | 23 |
| 1426 | 0.0519 | 174 | 397 | 118 | 415 | -56 | 18 |
| 1427 | 0.0856 | 181 | 403 | 119 | 417 | -62 | 14 |
| 1428 | 0.1236 | 190 | 409 | 120 | 419 | -70 | 10 |
| 1429 | 0.1661 | 199 | 416 | 121 | 421 | -78 | 5 |
| 1430 **contact** | 0.2134 | 209 | 423 | 121 | 423 | -88 | 0 |
| 1431 | 0.1484 | 198 | 418 | 122 | 425 | -76 | 7 |
| 1432 | 0.1134 | 192 | 416 | 123 | 427 | -69 | 11 |
| 1433 | 0.1104 | 192 | 417 | 124 | 429 | -68 | 12 |
| 1434 | 0.1019 | 192 | 418 | 124 | 431 | -68 | 13 |
| 1435 | 0.0883 | 190 | 418 | 125 | 433 | -65 | 15 |
| 1436 | 0.0704 | 188 | 418 | 126 | 435 | -62 | 17 |

## 2. Grade ramp shot 20 -> shot 22
- World colour multiply (0.79, 0.79, 0.88) and star multiplier x160 at g1368, easing LINEARLY to the plain shot-22 NIGHT (1.0, x16) at g1452.
- g1368 top-150-row mean RGB 111.6/105.2/218.2 vs team 4 shot 20 g1367 110.4/103.6/216.4 (+1.1 / +1.5 / +0.8 %); bright-star pixels 1247 vs 1445.
- g1452 116.6/109.5/222.2 vs team 4 shot 22 g1453 116.5/109.0/218.0 (+0.1 / +0.5 / +1.9 %). Blue of the top strip over time 218.2 -> 222.2 (monotone, no twilight climb).
## 3. Kept from v2
- World built with shot 22's preset camera/lamps/dress, no dust, hives at true scale 1.0, bees only from g1442 as small puffs, g1452 camera = shot 22's first frame, no text, sharp.
- Weak points: unit 2/3 only do the set's swing; the camera is ~7 m from unit 1 so the hive is 125-230 px wide; soft olive ground patch lower-left in early frames.
