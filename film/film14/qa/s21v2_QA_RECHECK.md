VERDICT: FAIL -- 2 blockers remain. (1) The knocks still don't read: on all three sound frames the only visible event is a 5 px camera bump; the hive never visibly meets a post. (2) The night grade jumps at g 1368: the sky is about 45 % brighter than shot 20 and has half the stars. Fixed: dust is gone, the g 1453 jump is gone (posts and camera match exactly, the hive is within about 30 px), and the g 1453 sky matches.

# QA_RECHECK film 14, take s21 v2 (shot 21, used g 1368-1452, file g 1362-1458, n = g - 1362)

Frames and sheets are in scratchpad/qa_s21v2/ (scratchpad = /tmp/claude-0/-home-user-github-commit-quest-v2/e31886ca-36bb-5aa1-b287-510d4c90ddec/scratchpad):
- f/ holds all 97 s21 frames, named by g.
- n/ holds all 383 frames of conform/takes/s20, named by g (shot 20 = g ..1367, shot 22 = g 1453..).
- knock{1390,1410,1430}.jpg (240 px) and knock*_phone.jpg (120 px) show contact ±3 frames, with a cyan line at y 880.
- zoom{k}{a,b,c}.jpg are full-res crops at contact ±3. pass1430.jpg and hitch1418.jpg are extra motion crops.
- cut1368.jpg and cut1453.jpg show each cut ±3 frames. cut1453_pair.jpg and cut1453_hive.jpg show 1452 / 1453 / blend.
- bees1440.jpg, blob1444.jpg, overview.jpg.
- metrics.txt has per-frame diff, sky top RGB, sky %, luma, luma below y 880, star count and white-chip count.
- shake.txt has background shift per frame. trk_hive_*.txt has the hive track (SAD block match, screen px).

## Blockers from the v1 report

| # | v1 blocker | v2 status |
|---|---|---|
| 1 | blob dust | **FIXED**: no dust anywhere. The white-chip count is 0 for g 1416-1447. The only whites are far lamps at x 570-720, y 614-692 (g 1362-1395) and stars. |
| 2 | knocks don't read | **NOT FIXED**: see check 1 |
| 3 | night grade vs 20 / 22 | **HALF**: g 1453 matches. g 1368 is worse than v1 (see check 2). |
| 4 | 180 px / 1.3x jump at g 1453 | **FIXED** (see check 3) |

## 1. Contacts read at phone size: FAIL (blocking)

Hive = unit 1, the near hive. Positions are screen x of the hive track, in px per frame.

The camera bump is real and lands on the exact frames: a global shift of (+2, -5) on g k, (-6, +11) on k+1 and (+5, -6) on k+2. The frame-diff spike is 6.6-7.7 against a 4.4-4.8 baseline. The hive motion, however, does not match the claim ("run-in, hard stop on contact, 12-14 px rebound"):

- **g 1390**: there is no hive motion on screen at all. From g 1384 to 1395 the hive drifts by 1 px per frame or less; it moves only with the camera bump. Any run-in happens in depth and does not show. The hive hangs between the near post (x about 140) and the right post (x about 330), with about 85 px of clear gap on its right. Nothing touches anything. Read: the camera jolts on a still hive.
- **g 1410**: the run-in decelerates (+31, +31, +29, +26, +21, +13, +2 over g 1403-1409). That is a pendulum easing into its apex at g 1409, not a hard stop. The contact frame is the start of the return (-9, -3, -11, then -32/-26/-28), which is a full back-swing, not a 12-14 px rebound. On screen the hive sits in front of the right post (it overlaps the post), and its left edge is about 140 px from the near post. Read: a swing turnaround with a camera jolt.
- **g 1430**: the run-in accelerates well (+7, +12, +17, +22, +26, +29, +31). But there is **no stop**: after g 1430 the hive keeps going at +17, +17, +22, +20, +16, +10, +4 px. That is about 100 px past the contact frame, sliding *in front of* the right post (pass1430.jpg). On the contact frame its right end only lines up with the post's edge. Read: the hive brushes past the post.
- **Phone (120 px)**: the hive is a low-contrast brown box about 35 px wide in dark corn. With the knock SFX on these frames, the audience sees a camera shake and a hive that is not touching anything.
- **Unscripted "knock" at g 1419**: the leftward swing (-28, -28, -26, -23) brakes hard to -9 and then -1 just as the hive's left end meets the near post (hitch1418.jpg). This reads more like a hit than any of the three scripted contacts, but it has no sound and lands 9 frames off the 1410 cue.
- **Fix direction**: put the contacts where the hive's screen silhouette actually meets a post, in the screen plane (not in depth). Make it a real stop of 0-2 px on the contact frame with a short counter-move. Kill the g 1419 brake, or move a cue to it.

## 2. Night grade continuity: FAIL at g 1368 (blocking), OK at g 1453

| | shot 20 g 1367 | s21 g 1368 | s21 g 1410 | s21 g 1452 | shot 22 g 1453 |
|---|---|---|---|---|---|
| sky top RGB (y 10-70) | 94/88/202 | **136/127/240** | 120/112/224 | 101/95/207 | 101/94/207 |
| stars | 3090 | 1719 | 2437 | 3380 | 6765 (bees add specks) |
| luma y 400-880 | 86 | 57 | 53 | 45 | 67 (bee swarm) |
| luma below y 880 | 64.5 | 52.3 | 44.4 | 36.3 | 45.2 |

- **g 1368**:
  - The sky jumps about +45 % (v1 was +20 %) to a pale periwinkle, and the stars halve.
  - Shot 20's lit yard (fire, warm props) cuts to darker corn. The mid band drops 86 to 57.
  - Clearly visible in cut1368.jpg.
- **In-shot**:
  - The sky ramps down steadily from 136 to 101 (-26 %), and the ground from 52 to 36, over 2.8 s.
  - There is no twilight bump any more, but the shot visibly "gets darker".
  - The team's preset match was made only at the end frame.
- **g 1453**:
  - Sky top matches (101/95/207 vs 101/94/207). PASS.
  - The ground is about 20 % brighter and warmer in shot 22: y 1000-1280 RGB 66/27/29 vs 81/33/27. This is a minor note and is masked by the bee burst.
- **Continuity note, outside s21's scope but at its cut**: shot 20 g 1365-1367 shows about 15 bees in the air, while s21 has none until g 1443. The director should confirm this is intended.

## 3. No size or position jump at g 1453: PASS
- Posts, roof, wire and ground line up exactly. The near post sits at x 105-135 and the right post at about 470-490 in both frames.
- Hive left edge: about 85 px (s21) vs about 90 px (shot 22).
- The s21 hive is level, at y about 635-730, and about 290 px wide.
- Shot 22's hive is yawed and tilted by its swing, at y about 605-695, with about 240 px visible before the bees cover it.
- That leaves about a 30 px vertical offset plus a pose difference, down from 180 px / 1.3x. The g 1453 swarm masks it.
- The hive is at swing apex at g 1451-1452 (-3, +2 px), so there is no motion jump.

## 4. Action above y 880: PASS
- Hive bottoms are at y 730-750 at most.
- Bees are at y 190-615.
- Nothing below about 760 except ground and grass.

## 5. No unintended pops: PASS (with note)
- Frame diff is a smooth 3.2-5.2 outside the three bump frames.
- No objects pop. The blue tree silhouette behind the roof at g 1442+ is revealed gradually by the camera move (blob1444.jpg).
- The bees enter singly from g 1443.
- Note: the g 1419 hard brake (check 1) is a motion hitch, not a pop.

## 6. Camera moves without whips: PASS
- Background shift is a steady 1-3 px per frame (push-in) from g 1368 to 1452.
- The only spikes are the intended 3-frame bumps at g 1390, 1410 and 1430 (peak 11 px vertical on k+1).
- Handles g 1453-1458 are nearly static (diff 0.6-0.9).

## 7. No text: PASS

## Team claims vs measured
- **"Hard stop + 12-14 px rebound at 1390/1410/1430"**: not on screen. At 1390 there is no hive motion. At 1410 the hive eases to its apex at 1409 and then swings fully back. At 1430 it overshoots by about 100 px.
- **"Accelerating run-in 35-55 px over last 5 frames"**: true only at 1430. At 1410 the run-in decelerates. At 1390 there is none on screen.
- **"5 px camera bump"**: true, frame-exact.
- **"Posts/roofs shake 5 px"**: not separable from the camera bump. No independent post motion is visible.
- **"g 1452 sky matches team 4 g 1453"**: true.
- **"g 1452 camera = shot 22 first frame"**: true.
- **"Hives at true scale"**: consistent with the measurements (check 3).
- **"No dust"**: true.
- **"Bees only small puffs from about g 1442"**: true (first bees at g 1443).
