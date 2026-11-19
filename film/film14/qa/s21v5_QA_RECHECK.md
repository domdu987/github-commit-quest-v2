VERDICT: PASS. The g1410 blocker is fixed. At the cue the hive's left end stops at the near post's face. Nothing shows beyond the post (0 hive pixels, against 98 in v4), and the slots and landing board stay visible. There is still a small tuck of about 3-8 px behind the post's edge, which is within measurement accuracy (note only). The seams at g1397/1398 and g1429/1430 are clean. g1390 and g1430 are unchanged and still pass. Everything else from v4 still passes.

# QA_RECHECK film 14, take s21 v5 (shot 21, used g1368-1452, file g1362-1458, n = g - 1362)

`scratchpad` = /tmp/claude-0/-home-user-github-commit-quest-v2/e31886ca-36bb-5aa1-b287-510d4c90ddec/scratchpad

The frames and sheets are in a new folder, scratchpad/qa_s21v5/:
- f/ holds all 97 v5 frames, named by g.
- ph/ holds 180x320 phone frames for g1386-1434.
- zLeft_v4top_v5bottom.jpg compares the near post at g1406-1413, v4 against v5, at 2x.
- zLeft1408_1412_3x.jpg shows g1408-1412 at 3x.
- knock1390.jpg, knock1410.jpg and knock1430.jpg are full-res crops of each cue ±3 frames.
- phone1406_1414.jpg and phone1410_zoom.jpg are at phone size.
- seam1397.jpg covers g1396-1399, and seam1429.jpg covers g1428-1431.
- track_raw.txt and track_table.txt hold the track. metrics.txt holds per-frame data: frame diff for v5 and v4, sky, top-150 rows, mid luma, ground RGB and high-pass noise.

The tools are in scratchpad/qa_s21v5_tools/. track.py is the same tracker as in v4 (accuracy about ±3 px). The folder also has diff and sheet scripts.

## 0. What changed against v4
I compared each frame of v5 with v4, using per-pixel RGB.
- Only g1398-1429 differ. In those frames, 280-6100 pixels differ by more than 20 levels.
- Every other frame (g1362-1397 and g1430-1458) differs only by re-encode noise: mean 0.05-0.52, max ≤ 33, and at most 1 pixel above 20.
- So the splice is exactly where the team said, and g1390, g1430, the cuts and the handles are untouched.

## 1. g1408-1412 at the near post: PASS (note)

| g | hive L | L post right edge | gap L | hive px beyond post (v4 → v5) |
|---|---|---|---|---|
| 1406 | 122 | 107 | 15 | 0 → 0 |
| 1407 | 118 | 108 | 10 | 0 → 0 |
| 1408 | 109 | 108 | 1 | 0 → 0 |
| 1409 | 106* | 109 | -3* | 0 → 0 |
| **1410** | 116 visible (post 84-115) | 115 | about -3 to -8 (see below) | **98 → 0** |
| 1411 | 113 | 107 | 6 | 0 → 0 |
| 1412 | 121 | 111 | 10 | 0 → 0 |

\* At this frame the end is partly behind the post. The tracker's 10th-percentile value clamps at the post edge.

**Full size:**
- At g1410 nothing hive-coloured is left of the post. In v4 the roof lip and landing board showed at x 68-84. Now there are 0 pixels there.
- The upper slot is visible from x 117, 18 px long. At g1409 and g1411 it is 20-21 px long, so it is not hidden.
- The lower slot and the landing board are visible right of the post face.
- To estimate the hidden overlap, I aligned g1409 and g1411 onto g1410 by template match. The predicted true left end is:
  - about x 113 at slot and board level, which is about 3 px behind the 115 edge;
  - about x 100-108 at the top corner of the roof lip, which is about 7-10 px behind.
- The hive hangs just behind the post's plane on an oblique camera, so a tuck this small reads as touching the face. It is within the ±6 px measurement band. In v4 the hive went about 35 px behind the post and showed on its far side.
- **Note:** contact is first reached at g1408-1409 (gap 1 and then -3), one or two frames before the cue. The hive keeps creeping a few px behind the edge into g1410. It is not visible as such.

**Phone (phone1406_1414.jpg, phone1410_zoom.jpg):**
- On g1410 the hive end sits flush against the post. Both slots stay readable and nothing peeks out beyond the post.
- It reads as the hive bumping the post, not sliding behind it.

## 2. The g1410 knock reads as a hit: PASS
- vRel is the right-end velocity minus the right post's velocity, which removes the camera push. Its sequence is:
  - run-in: -3, -3, -4, -4, -5 (g1405-1409);
  - **-7 on the cue**;
  - rebound +12, then +3;
  - hold at 0, 0, 0 (g1413-1415), with gap L steady at 11 px.
- The run-in is slightly softer than v4's (-9 on the cue). It still accelerates into a stop that lands on the cue frame.
- The cue frame shows the 5 px post shake and the camera bump. Frame diff is 5.25 and 5.39 at g1410-1411, against 2.2 on the neighbouring frames, the same as v4 (5.26 and 5.38).
- **No hard stop elsewhere:**
  - The pre-run hold, g1393-1404, drifts softly. vRel stays between 0 and ±1, then eases to -3.
  - After g1416 the hive eases away and accelerates into g1430: vRel 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5.
  - Outside the three cues, no frame stops from more than 2 px per frame to 0.

## 3. Seams: PASS

| | g1396 | g1397 | **g1398** | g1399 | | g1428 | **g1429** | **g1430** | g1431 |
|---|---|---|---|---|---|---|---|---|---|
| frame diff | 1.94 | 1.95 | 1.98 | 2.00 | | 2.36 | 2.36 | 5.48 (cue, same as v4) | 5.41 |
| top-150 RGB | 113.4/106.8/219.4 | 113.5/106.8/219.5 | 113.5/106.8/219.4 | 113.6/106.9/219.5 | | 114.8/107.9/220.4 | 114.8/107.9/220.5 | 114.8/107.9/220.5 | 115.0/108.0/220.6 |
| ground RGB | 73/30/36 | 73/29/36 | 73/29/35 | 73/29/35 | | 69/28/32 | 69/28/32 | 70/28/32 | 69/28/31 |
| noise (sky / ground) | 3.15/1.48 | 3.30/1.48 | 3.55/1.53 | 3.17/1.49 | | 3.48/1.55 | 3.39/1.55 | 3.23/1.54 | 3.40/1.56 |
| hive L/R | 136/350 | 136/350 | 136/352 | 136/352 | | 180/413 | 189/420 | 198/427 | 189/422 |

- The grade and noise values continue smoothly across both seams. The noise moves within its normal frame-to-frame range of 3.0-3.6 in the sky and 1.44-1.58 on the ground.
- The hive moves smoothly across both seams (gap R at 1428-1430: 8 → 3 → 1).
- There is no pop on seam1397.jpg or seam1429.jpg.

## 4. g1390 and g1430: unchanged, PASS
- Both frames, and their ±3 neighbours outside the splice, are the same as v4 apart from encode noise.
- **g1390:** the gap closes 31 → 25 → 18 → 10 → **6** on the cue. It rebounds to 13 and holds.
- **g1430:** the run-in arrives from the new spliced frames, with gap 16 → 12 → 8 → 3 → **1**. It rebounds to 9 and holds.
  - The approach is a touch flatter than v4 (vRel +4, +4, +4, +5 against +5, +6, +7) but still accelerates into the stop.
  - The knock reads the same at full size and at phone size.

## 5. Everything else from v4: PASS
- **Grade and cuts:** g1362-1397 and g1430-1458 are unchanged. The sky ramp and the cut values at g1368 and g1452/1453 are the same as in v4 (top-150 rows: 111.6/105.2/218.2 at g1368, 116.6/109.5/222.2 at g1452).
- **Shot 22 match:** unchanged.
- **Action above y 880:** the hive bottom is at y 716 or above in the spliced frames.
- **Pops:** the only frame-diff spikes are on the cue frames.
- **Camera push and bumps:** continuous.
- **Text:** none. QA_AUTO passes.
- The v4 notes still stand, because those frames are outside the splice: at the pre-swing (about g1376) and at the end (about g1447) the left end is softly behind the near post. They are not blocking.

## Team claims
| Claim | Measured |
|---|---|
| Only g1398-1429 re-rendered and spliced | **Confirmed** by a per-frame diff against v4. |
| Seams checked, no pop | **Confirmed** (check 3). |
| At g1410 the end stops at the near face, nothing shows beyond, lip and slots visible | **Confirmed**, with about 3-8 px of the end tucked behind the post's edge (within tolerance). |
