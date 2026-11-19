VERDICT: FAIL. 1 blocker remains: the knocks. The rendered hive does not do what QA.md and probe_table.txt describe. It still swings like a pendulum, moves the opposite way to the probe, never stops on a cue, and at g1410 and g1430 it passes in front of the right post. The sky blocker is FIXED: g1368 is within about 1-6 % of shot 20 g1367, and g1452 matches shot 22 g1453.

# QA_RECHECK film 14, take s21 v3 (shot 21, used g1368-1452, file g1362-1458, n = g - 1362)

Frames and sheets are in scratchpad/qa_s21v3/ (scratchpad = /tmp/claude-0/-home-user-github-commit-quest-v2/e31886ca-36bb-5aa1-b287-510d4c90ddec/scratchpad):
- f/ holds all 97 s21 v3 frames, named by g.
- n/ holds conform/takes/s20 frames for g1356-1367 (shot 20) and g1453-1466 (shot 22). They were checked identical to qa_s21v2/n.
- z1390.jpg, z1410.jpg, z1420.jpg and z1430.jpg are full-res crops of the hive and posts around each event. knock{1390,1410,1430}.jpg are cue ±3 frames at 240 px. knock_phone.jpg is at 160 px. pass1410.jpg is also there.
- cut1368.jpg, cut1453.jpg, cut1453_pair.jpg, cut1453_blend.jpg and cut1453_hive.jpg cover the cuts.
- metrics.txt holds sky, luma, ground RGB and frame diff for every frame.
- track2.txt holds the unit-1 hive edges and post columns, measured by colour segmentation in the band y650-695.
- hive_vel.txt holds hive velocity relative to the near post, which removes the camera move.
- track2_v2frames.txt is the same tracker run on the v2 frames.
- overview.jpg, ground.jpg, bees1440.jpg, edge1439.jpg.

## Blockers from the v2 report

| # | v2 blocker | v3 status |
|---|---|---|
| 1 | knocks not on the cue frames, and the stray stop at g1419 | **NOT FIXED** (see check 1). The g1419 stop is softened. |
| 2 | sky about 45 % brighter than shot 20 at g1368 | **FIXED** (see check 3) |

## 1. Each cue frame reads as the hive hitting a post: FAIL (blocking)

On screen the left (near) post is at x about 70-105 and the right post at about 355-450, drifting with the push-in. Unit 1 sits between them. Directions below are screen directions.

The render does not match the team's probe table:
- g1384-1390: the probe says the hive moves right by 6-11 px per frame into the right post. The render moves it **left** by 4-6 px per frame, away from the right post.
- g1404-1410: the probe says the hive moves left into the left post. The render moves it **right** by 22-29 px per frame, over the right post.
- The motion curve is the same pendulum as in v2 (compare track2_v2frames.txt): turns at about g1397, 1410, 1423 and 1437. It is not a keyed slide with hard stops.
- probe_table.txt therefore does not describe this take. Either the "slide" keys were not used in the render, or their sign or axis is flipped and the hook swing is still on.

Per cue:
- **g1390**:
  - The hive is mid-swing, moving left. Its right end is 66 px from the right post and the gap is growing: 58 → 66 → 80 → 96.
  - Its left end has reached the near post, but it does not stop there. It slides **behind** the near post: the landing board shows left of the post at g1392-1397, and the hive keeps going about 55 px.
  - Nothing stops on g1390. The relative speed actually rises after it: -4, -9, -9, -18.
  - Read: a camera jolt while the hive drifts behind a post.
- **g1410**:
  - This is the turn of the swing, a soft ease: +22, +17, +9, then about 0 at g1410, then back.
  - The hive is fully **in front of the right post**. It covers the post completely from g1405 to g1414 (pass1410.jpg, z1410.jpg).
  - It is nowhere near the left post: the gap is about 128 px.
  - Read: a soft turn in front of a post. This is the v2 problem again.
- **g1430**:
  - The hive's right end reaches the right post's edge (gap 1 px) at full speed (+23 to +24 px per frame).
  - It keeps going about 85 px **in front of** the post, at +16, +12, +19, +15, +12, +8, to a soft turn at g1437 (z1430.jpg).
  - There is no stop and no rebound.
  - Read: the hive slides across the post. This is the v2 problem again.
- **Phone (knock_phone.jpg)**:
  - The hive is a brown box about 40 px wide.
  - At g1410 and g1430 it plainly overlaps the right post.
  - With the SFX, each cue reads as a camera bump with no hit.
- **Camera bump**: still frame-exact. The near post shifts +5, -8, +4 px over k, k+1, k+2. The frame-diff spike is 6.0-6.3 against a 2.7-3.5 baseline.

Team claims against the render:

| Team claim | Measured |
|---|---|
| Hive end touches the post's inner face with a gap of exactly 0 at g1390 R, g1410 L and g1430 R | No: 66 px from R at g1390, in front of R at g1410, and passing in front of R at g1430 |
| 35-45 px run-in | Run-ins exist but go the wrong way, and none of them ends on a post |
| 11-18 px rebound | None |
| Driven by hand | Not visible. The render shows the hook's pendulum. |

Fix direction:
- Check that the rendered blend actually uses the slide keys. Run the probe on the render file itself, not on a separate PROBE=1 scene.
- Check the screen direction of the offset sign.
- Keep the hive in the posts' depth plane so that it can neither slide behind the near post nor pass in front of the far one.

## 2. No other hard stops: PASS (with note)
- Camera-compensated velocities are in hive_vel.txt.
- Every reversal is a soft 4-6 frame ease. That includes the turn at about g1419-1423: -22, -17, -15, -11, -6, -2. It is softer than v2's -26 → -9 → -1.
- No frame shows a 0-2 px stop after fast motion.
- Note: there are also no hard stops on the cues (check 1).

## 3. Grade continuity at both cuts: PASS (with notes)

| | shot 20 g1367 | s21 g1368 | s21 g1410 | s21 g1452 | shot 22 g1453 |
|---|---|---|---|---|---|
| sky top RGB (y 10-70) | 94.7/89.0/202.3 | 100.2/94.4/206.3 | 100.2/94.2/206.3 | 101.0/95.0/207.8 | 101.0/94.9/207.6 |
| top 150 rows RGB | 110.4/103.6/216.4 | 111.6/105.2/218.2 | 113.9/107.1/219.7 | 116.6/109.5/222.2 | 116.5/109.0/218.0 |
| luma y400-880 | 86.4 | 49.4 | 46.9 | 45.4 | 67.5 (swarm) |
| luma y880 and below | 64.5 | 41.3 | 40.3 | 36.4 | 45.2 |
| ground RGB (y1000+) | 96/44/35 | 75/31/38 | 73/30/36 | 67/27/30 | 82/33/28 |

- **g1368: sky FIXED.**
  - The sky top is +6 / +6 / +2 % against g1367, and the top 150 rows are within 1-2 %. Shot 20's own sky rises from 73 to 95 over g1356-1367, so 100 on the next frame continues that trend.
  - Stars are visible on both sides (cut1368.jpg).
- **Team claim "linear ramp"**: not what was rendered, but not needed. The sky top is constant (100-101 / 94-95 / 206-208) for the whole take, because shot 20's end and shot 22's start already match.
- **Note (director's eye)**:
  - The lower frame drops a lot at g1368: the mid band goes from 86 to 49 and the ground from 96/44/35 to 75/31/38. v2 was 57 in the mid band.
  - The change of place (fire-lit yard → hive row with no fire) motivates it, and it is not a sky mismatch.
  - The ground keeps darkening slowly through the shot, from 75 to 67.
- **g1453**:
  - The sky matches (101/95/208 vs 101/95/208).
  - Shot 22's ground is about 20 % brighter and warmer (82/33/28 vs 67/27/30). This is minor and masked by the swarm, the same as in v2.

## 4. No size or position jump into shot 22: PASS (with note)
- Posts, roofs, wire and ground line up exactly (cut1453_blend.jpg).
- Unit 1 at g1452 spans x about 90-375 and y about 635-730, roughly level.
- Shot 22 at g1453 shows the hive at x about 88-330 (the right part is under the bees) and y about 605-695. It is yawed, with the front entrance showing.
- That leaves about a 30 px vertical offset and a pose change, the same as v2. The bee burst masks it.
- The hive is at the end of its swing (+2, +1 px), so there is no motion jump.

## 5. Action above y 880: PASS
- The hive bottom is at y 730 or above.
- Bees are at y 190-620.
- Below y 880 there is only ground, grass and soft moving leaf-shadow dapple (ground.jpg).

## 6. No unintended pops: PASS (with note)
- Frame diff is a smooth 1.6-3.8 outside the six bump frames (g1390-1391, g1410-1411, g1430-1431).
- Bees enter singly from about g1442 (bees1440.jpg).
- Note: a pale 3-5 px sliver sits at the far-left edge under the near roof (x 0-5, y about 255-270) from g1439 to g1449 (edge1439.jpg). It is negligible.
- The ground dapple brightness wanders by ±4 (g1386-1405). This is soft shadow motion, not a pop.

## 7. Camera moves: PASS
- Steady push and drift of 1-2 px per frame from g1362 to g1452: the near post goes from x 64 to 105 and the right post from 335 to 470.
- There is a bump at each cue.
- The handles g1453-1458 hold (diff 0.4-0.7).

## 8. No text: PASS
