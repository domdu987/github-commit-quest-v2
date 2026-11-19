VERDICT: FAIL -- 1) dust is again a solid white clump of flat square cards, not a crown; 2) knocks don't read at phone size: contact is hidden or missing and the hive jolt is only measurable at u1; 3) night grade drifts to bright twilight mid-shot and jumps at g 1368; 4) the hive jumps about 180 px and 1.3x in size at the cut into shot 22.

# QA_RECHECK film 14, take s21 (shot 21, g 1362-1458, n = g - 1362), TAKE gate

What I checked:
- All 97 s21 frames went to scratchpad/takes/qa_s21/f/. All 383 s20 frames went to qa_s21/n/ (n = g - 1301) for the neighbour shots.
- Each knock ±3 frames at 360 px and 120 px (phone), with a cyan line at y 880. I also made 2x grid crops for g k-2 to k+3.
- Both cuts ±3 frames at both sizes. For g 1452 vs 1453 I made a side-by-side and a 50 % blend.
- On every frame I measured frame diff, sky share, sky top RGB, star count, luma, luma below y 880 and white-chip boxes. I also measured hive and background shift (block match) around each knock.
- qa_auto: PASS. It flags both cuts as "no change", which is expected for a single-shot file.

Sheets in scratchpad/takes/qa_s21/:
- phone1.jpg
- knock{1390,1410,1430}.jpg and the matching _phone.jpg
- zoom{1390,1410,1430}.jpg
- cut1368.jpg and cut1368_phone.jpg
- cut1453.jpg, cut1453_phone.jpg and cut1453_pair.jpg
- moon_check.jpg
- metrics.txt

## Checks

### 1. Knocks read at phone size: FAIL (blocking)
The spray fires on the claimed frames (g 1390, 1410 and 1430). That part is fixed from s20 v6, which fired 1-3 frames late.

The jolt was measured as hive shift minus steady drift:

| knock | hive shift at contact | posts/roofs and camera | spray position (x, y) |
|---|---|---|---|
| u3 g 1390 | none (-1 px) | roof patch shakes 4-8 px at g 1390-1392 | x 380-485, y 580-680 |
| u2 g 1410 | +3 px at g 1411, one frame late | small | x 370-470, y 600-710 |
| u1 g 1430 | +5 px on the contact frame, then 6 px vertical at g 1431 | about 3-4 px camera shake | x 130-230, y 630-745 |

- The frame-diff bump at the hits is only +1.2 to +2.3 over neighbouring frames, and the spray causes most of it.
- u3: the hive is the small far one, about 120 px wide. The opaque spray covers the contact point. At 120 px phone size it is a white speck (knock1390_phone.jpg), and no hive-meets-post can be seen.
- u2: the spray sits on the post and hides the actual strike.
- u1: the spray bursts at the hive's LEFT top corner in open corn. The only post is at the hive's right side, so there is no visible contact. This repeats the s20 v6 finding: "a sparkle on the hive, not a knock".

### 2. Dust is a crown, not blobs: FAIL (blocking, regression from s20 v6)
- At 2x (zoom*.jpg), every spray is a solid opaque white mass of overlapping flat square cards, 100-150 px across. At u1 a few square cards stick out as an "X".
- There are no separated chips, droplets or radial arcs. The wisps are hidden inside the mass.
- This is the s20 v5 "lumpy ball" failure again, and the team's QA admits "the spray reads as a bright clump".
- s20 v6 had already fixed this with 10-15 separated chips.

### 3. Night grade vs shots 20 and 22: FAIL (blocking)

| | shot 20 g 1367 | s21 g 1368 | s21 g 1420 (peak) | s21 g 1452 | shot 22 g 1453 |
|---|---|---|---|---|---|
| sky top RGB | 92/86/200 | 111/103/225 | **144/135/249** | 98/92/205 | 98/92/205 |
| star count | 3900 | 1870 | 3100 | 5160 | 6320 |
| sky share | 44 % | 36 % | 33 % | 26 % | 21 % |
| luma below y 880 | 64 | 66 | 45 | 53 | 45 |

- At the g 1368 cut the sky jumps about 20 % brighter and the stars halve.
- Mid-shot the sky climbs to a bright periwinkle, about 45 % brighter than shot 22, so g 1395-1430 reads as twilight. It then ramps back down to match at g 1452. The grade visibly drifts over 2.8 s.
- The g 1453 cut is acceptable for sky colour. However, s21 has hard post shadows across the ground (a strong key light), while shot 22's ground is soft and unshadowed.
- Warm hut windows glow mid-frame at g 1368-1395 (x about 400-560, y about 560-640). This is minor.

### 4. Action above y 880: PASS
- The hive bottoms are at y 827-841 in the knock frames, and the sprays are at y 580-745.
- The lower 35-40 % of the frame is empty ground, which wastes framing and adds to the "far, small" problem at u3.

### 5. No pops except the jolts: FAIL (blocking, at the g 1453 cut)
- Inside the shot, the frame diff is smooth (3.7-10.3) and there are no other spikes.
- At the g 1453 cut, camera, posts and roof line up well, but the end hive does not:
  - At s21 g 1452 the hive spans about x 270-570.
  - At shot 22 g 1453 it spans about x 90-320.
  - That is a jump of about 180 px left and about 1.3x in width (cut1453_pair.jpg).
- The meta claim "hives back to natural size from g 1432-1452" did not land, and the hive is still swinging at the end.

### 6. Camera always moving, no whips: PASS
- Diff stays at 3.7-10.3 per frame through g 1362-1452. There is no static run and no whip.
- The handle frames g 1453-1458 are nearly static (diff 1.5), but they are outside the shot.

### 7. No text: PASS

### Other checks
- Bees: PASS. None before g 1442, then small puffs that lead into shot 22's burst.
- No elephant: PASS.
- Moon: OK. The disc is also in shot 20 (g 1340), and in shot 22 it is hidden by the bees.
- Olive ground patch at lower left, g 1380-1415: reads as a yellow-green smear at phone size (phone1.jpg). Non-blocking, but fix it with blocker 3.
- Sky share: 36 % falling to 26 %, which is within the admitted 30-35 %. Non-blocking.

## Fixes
1. **Dust crown.**
   - Remove the square backing cards and the opaque core.
   - Use 10-15 separate chips (8-14 px) tinted wood or dust (about 200/170/130), launched radially in a 100° upward cone with gravity.
   - Peak width 200-250 px, and the contact point must stay visible through the crown.
   - Add 2 thin low-alpha wisps and fade over 8 frames. The s20 v6 crown code is the starting point.
2. **Contact and jolt.**
   - Emit the crown from the exact point where the hive end meets its post, and fix u1 to come from the post side.
   - Jolt the hive itself by 10-14 px on the contact frame (not +1), then 2 frames of shake.
   - Aim for a diff spike of at least +5 over neighbouring frames.
   - u3 is too far to read at 120 px: frame it larger (hive at least 200 px wide), or let the camera lead onto it 3 frames earlier.
3. **Grade.**
   - Lock the s21 sky to shot 22 (top about 98/92/205) for the whole shot.
   - Match the start to shot 20 (about 92/86/200) with star density of at least 3500 from g 1368. Do not ramp brightness mid-shot.
   - Soften or dim the hard key shadows on the ground to the shot 22 level.
   - Kill the hut window glow and the olive patch.
4. **End match.**
   - From g 1440, ease the end hive to scale 1.0 AND to shot 22's rest position and swing: x about 90-320 at g 1452, hanging from the same crossbar point.
   - Diff s21 g 1452 against shot 22 g 1453 on the hive box before delivery.
