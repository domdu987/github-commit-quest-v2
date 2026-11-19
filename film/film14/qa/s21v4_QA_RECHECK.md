VERDICT: FAIL. One blocker: the g1410 knock. At g1390 and g1430 the hive now hits the right post on the cue frame (gaps 6 px and 1 px, with a stop and rebound). At g1410 the hive's left end goes about 35 px into, and behind, the near (left) post, which is the post's whole width. Its roof lip and landing board stick out on the post's far side, and the entrance slots vanish. Everything else passes: grade, cut to shot 22, y 880, pops, camera move and text.

# QA_RECHECK film 14, take s21 v4 (shot 21, used g1368-1452, file g1362-1458, n = g - 1362)

Frames and sheets are in scratchpad/qa_s21v4/. scratchpad = /tmp/claude-0/-home-user-github-commit-quest-v2/e31886ca-36bb-5aa1-b287-510d4c90ddec/scratchpad.
- f/ holds all 97 v4 frames, named by g.
- n/ holds shot 20 frames g1356-1367 and shot 22 frames g1453-1466, taken from conform/takes/s20. They are identical (diff 0.0) to qa_s21v3/n.
- ph/ holds 180x320 phone frames for g1386-1434.
- knock1390.jpg, knock1410.jpg and knock1430.jpg are full-res crops of each cue ±3 frames.
- knock_phone.jpg, knock_phone_zoom.jpg and phone1410_zoom.jpg are at phone size.
- zLeft.jpg shows the near post at g1376, 1385, 1407, 1409, 1410, 1411, 1413 and 1447, at 2x.
- edge1447.jpg, cuts.jpg and cut1453_hive.jpg cover the end of the shot and the cuts.
- track_raw.txt holds every frame. track_table.txt covers g1380-1440 with the frame diff.
- The tracker is scratchpad/qa_s21v4_tools/track.py. It colour-segments the hive in the band y 550-800. Hive edges are the 10th and 90th percentile row extents. Post edges are the columns that are at least 70 % post-coloured in a 31-row band at the hive's centre. Accuracy is about ±3 px.

## 1. Each cue reads as the hive hitting its post: FAIL at g1410 (blocking). g1390 and g1430 PASS.

There is no pendulum any more. The motion is keyed: an accelerating run-in, a stop on the cue, a 2-frame rebound, then a hold. The bow cut and the hand placement are confirmed by the track.

In the excerpt below, vRel is the hive's right-end velocity minus the right post's velocity, which removes the camera push. The full table is in track_table.txt.

| g | hive L | hive R | L post right edge | R post left edge | gap L | gap R | vRel | fdiff |
|---|---|---|---|---|---|---|---|---|
| 1386 | 105 | 320 | 98 | 350 | 7 | 30 | +5 | 2.14 |
| 1388 | 125 | 335 | 98 | 353 | 27 | 18 | +7 | 2.28 |
| 1389 | 136 | 344 | 99 | 354 | 37 | 10 | +8 | 2.33 |
| **1390** | 151 | 352 | 104 | 358 | 47 | **6** | +4 | **5.64** |
| 1391 | 139 | 347 | 96 | 355 | 43 | 8 | -2 | 5.91 |
| 1392 | 134 | 345 | 100 | 358 | 34 | 13 | -5 | 2.83 |
| 1393 | 134 | 346 | 100 | 359 | 34 | 13 | 0 | 2.18 |
| 1405 | 119 | 346 | 106 | 378 | 13 | 32 | -4 | 2.49 |
| 1406 | 113 | 344 | 107 | 380 | 6 | 36 | -4 | 2.52 |
| 1407 | 106* | 341 | 108 | 381 | -2* | 40 | -4 | 2.54 |
| 1408 | 105* | 337 | 108 | 383 | -3* | 46 | -6 | 2.56 |
| 1409 | 105* | 332 | 109 | 385 | -4* | 53 | -7 | 2.57 |
| **1410** | lip 81, board 68 | 327 | 115 (post spans 84-116) | 389 | **about -35** | 62 | -9 | **5.66** |
| 1411 | 103* | 337 | 107 | 387 | -4* | 50 | +12 | 5.75 |
| 1412 | 108* | 343 | 111 | 390 | -3* | 47 | +3 | 3.14 |
| 1413 | 108* | 345 | 111 | 392 | -3* | 47 | 0 | 2.53 |
| 1426 | 156 | 395 | 121 | 417 | 35 | 22 | +5 | 2.71 |
| 1428 | 175 | 410 | 122 | 421 | 53 | 11 | +6 | 2.70 |
| 1429 | 186 | 419 | 123 | 423 | 63 | 4 | +7 | 2.71 |
| **1430** | 198 | 427 | 129 | 428 | 69 | **1** | +3 | **5.88** |
| 1431 | 189 | 422 | 121 | 425 | 68 | 3 | -2 | 5.79 |
| 1432 | 184 | 420 | 125 | 429 | 59 | 9 | -6 | 3.19 |
| 1433 | 184 | 422 | 126 | 431 | 58 | 9 | 0 | 2.55 |

\* In these frames the hive's left end is hidden behind the near post. The value shown is the post edge, not the hive's real end.

- **g1390, right post: PASS.**
  - The run-in accelerates (+5 to +8 px per frame) and closes the gap 30 → 18 → 10 → **6 px** on the cue.
  - The rebound is 2 frames, to 13 px, then the hive holds still at g1393-1401.
  - It is behind the right post's plane, and no part of it is in front of the post.
  - At phone size the hive meets the post on the bump frame. It reads as a knock.
- **g1430, right post: PASS.**
  - The run-in is +5 to +7 px per frame, and the gap closes 22 → 11 → 4 → **1 px**.
  - The rebound goes to 9 px, then the hive holds.
  - The hive's corner meets the post edge without covering it.
  - It reads as a clean knock.
- **g1410, left (near) post: FAIL.**
  - The run-in is good (vRel -4, -4, -6, -7, then -9 on the cue, then a +12 rebound) and the stop is frame-exact.
  - **The end position is wrong:**
    - The hive's left end reaches the post edge at g1407 and keeps going behind it. On g1410 the post (x 84-116) covers the hive's whole end.
    - The roof lip shows at x 81-84 on the post's FAR side, and the landing board at x 68-82.
    - The entrance slots, which are visible right of the post at g1409 and g1411, are hidden.
    - So the hive end overlaps the post by about 35 px. The tolerance is a gap of 15 px; this is overlap, not gap.
  - **Phone (phone1410_zoom.jpg):**
    - For one frame the slots vanish, and the hive's lip and board peek out left of the post.
    - It reads as the hive sliding into or behind the post, not as hitting its face.
    - It is the mirror image of the "passes in front" failure.
  - **Team claim of -8 px:** their mask is |A − B| (everything vs hive hidden), which only counts hive pixels the near post does not cover. The occluded overlap is invisible to that method. At g1410 their "hive left end 118" is just the post's right edge.
- **Fix (small):**
  - Reduce the g1410 offset by about 35 px on screen. The hive is about 230 px long for 0.66 m, so that is about 0.10 m: roughly -0.20 → **-0.10 m**.
  - Aim the hive's leftmost point (lip and board) at the post's inner face.
  - Verify with a hive-only render (posts hidden) against the post mask, so that occluded overlap is counted.
  - g1390 and g1430 should be kept as they are.

## 2. No other hard stop or unintended contact: PASS (with notes)
- Outside the cues every turn is a soft ease of 3-5 frames: g1376-1380, 1401-1404, 1417-1421 and 1435-1440. The shot ends with an ease to rest at g1449-1452 (vRel -3, -2, -1, 0).
- Each rebound settles from -5 or -6 px per frame to 0 in one frame, at g1393, 1413 and 1433, 3 frames after the cue. With the SFX on the cue this reads as part of the knock, not as a separate hit.
- Note: during the pre-swing (about g1370-1385) and at the end (g1443-1452) the hive's left end also sits behind the near post.
  - At g1376 the slots are cut by the post, and at g1447 the board peeks out on the far side (zLeft.jpg, edge1447.jpg).
  - Both are soft, with no stop, and shot 22 also has the hive behind that post, so neither blocks.
  - The -0.10 m depth or offset check above would tidy them too.

## 3. Grade continuity at both cuts: PASS (unchanged from v3)

| | shot 20 g1367 | s21 g1368 | s21 g1410 | s21 g1452 | shot 22 g1453 |
|---|---|---|---|---|---|
| sky top RGB (y 10-70) | 94.7/89.0/202.3 | 100.2/94.4/206.3 | 100.2/94.2/206.3 | 101.0/95.0/207.8 | 101.0/94.9/207.6 |
| top 150 rows RGB | 110.4/103.6/216.4 | 111.6/105.2/218.2 | 113.9/107.1/219.7 | 116.6/109.5/222.2 | 116.5/109.0/218.0 |
| luma y400-880 | 96.0 | 51.2 | 47.6 | 45.0 | 64.0 (swarm) |
| ground RGB (y1000+) | 96/44/35 | 73/30/37 | 70/28/34 | 67/28/30 | 82/33/28 |

- The sky values are the same as in v3, so the sky ramp is unchanged.
- The lower frame still drops at g1368. That is the change from the fire-lit yard to the hive row, the same as v3, so it is a director's-eye note only.

## 4. No size or position jump into shot 22: PASS (with note, same as v3)
- At g1452 the hive is at x about 95-382 (its left end behind the near post) and y 637-723, at rest (vRel 0).
- At g1453 it is at x about 70-330 and y about 605-700. It is yawed and lighter, and the bee burst masks it.
- That is about a 30 px vertical offset and a pose change, the same as v3.
- Posts, roofs and wire line up (cuts.jpg, cut1453_hive.jpg).

## 5. Action above y 880: PASS
- The hive bottom is at y 723 or above, and bees are at the top.
- Below y 880 there is only ground, grass and leaf dapple.

## 6. No unintended pops: PASS
- Frame diff (mean abs luma at 360x640) rises smoothly from 1.3 to 2.7 across the take.
- Spikes appear only on the cue and the frame after: 5.64/5.91 at g1390, 5.66/5.75 at g1410 and 5.88/5.79 at g1430. This is the intended 5 px post shake plus the camera bump.
- The handles g1453-1458 hold (diff 0.2).
- The vanishing slots at g1410 are part of blocker 1.

## 7. Camera moves: PASS
- The push continues through the shot: the right post's left edge goes from x 344 at g1380 to 466 at g1452, about 1-2 px per frame.
- There is a bump on each cue.

## 8. No text: PASS
- No text was seen in any frame, and QA_AUTO passes.

## Team claims
| Claim | Measured |
|---|---|
| Wire bow cut, hive placed by hand last | **Confirmed.** The pendulum is gone, and the hive does keyed runs, stops and holds. |
| Gaps 14 / -8 / 10 px (±6) | **6 / about -35 (overlap) / 1 px.** g1390 and g1430 are within tolerance. At g1410 the hive end is hidden behind the near post, which the \|A−B\| method cannot see. |
| Frame-diff spikes at each cue, no other hard stop | **Confirmed** (see checks 2 and 6). |
