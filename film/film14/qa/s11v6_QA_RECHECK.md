VERDICT: PASS (shot 12, g821-863). A phone viewer reads "a long row of hives along the field" at once. Count: 6 roofed hives at g821 and 6 roofs (5 with a visible box) at g863. That is one fewer than the team's 6-7 / 7, but it meets the director's bar of about 5-6 clearly separate hives. There are no technical faults. Shot 11 is unchanged.

Take: r30/film/v3/film14/s11/take.mkv. 117 frames, g753-869 (n 0-116), 720x1280, 30 fps, h264. meta.json: shot 11 = g759-820, shot 12 = g821-863, with 6-frame handles.
Frames are in scratchpad/takes/qa_s11v6/:
- all/ holds every frame, named by g number.
- s12_phone.jpg is the phone sheet at 180x320 for g819-863, every 4th frame, with a cyan line at caption y 900.
- cont_full.jpg shows g820, g821, g842 and g863.
- g821_band.png and g863_band.png are full-size crops of y 500-800.
- g863_phone_band_4x.png is the hive band at phone size, enlarged 4x.
- g821_left_3x.png and g863_left_3x.png show the far-left hives at 3x.

## Checks
| # | Check | Result |
|---|---|---|
| 1 | Hive count | **PASS.** At g821 there are 6 roof+box pairs. From far to near, the roofs sit at x about 0-55 (cut by the left edge, box visible), 35-120, 105-215, 200-345, 340-535 and 580-720. At g863 there are 5 full pairs at x about 0-70, 55-145, 130-245, 230-385 and 385-595, plus a 6th roof at x 645-720 whose box is off frame right. Full size and phone size give the same count. At phone size the smallest roofs are about 12-18 px wide and still separate (g863_phone_band_4x.png). The flower stalks are gone. The far-left area holds only maize, small seedlings and grass tufts. Team count (6-7 / 7) is about 1 high, which is not material. |
| 2 | Reads "many hives" in about 1 s | **PASS.** The row recedes diagonally into the left edge, which implies more hives beyond the frame. On the phone sheet the regular rhythm of orange roofs reads instantly as "a row of many hives", clearly a step up from shot 11's one. |
| 3 | Pops; cut at g821 | **PASS.** The cut is a single-frame change (diff 45.1). Shot 12 frame-to-frame diffs ease smoothly from 2.65 up to 4.17 (g842) and back to 2.71 (g863). The handle g864-869 is steady at about 2.6. There are no spikes, black frames or magenta. |
| 4 | Camera moves | **PASS.** Slow eased lateral dolly and push, moving on every frame, never held. |
| 5 | No text | **PASS.** |
| 6 | Light continuity with shot 11 | **PASS.** Same warm, low afternoon sun, long shadows, laterite and maize. The sky shifts from orange to lilac and pink near the horizon, as in v5, which was accepted. Shot 12 is brighter overall (mean 136 vs 115) because sunlit ground fills the frame. It does not read as a different time of day. |
| - | Shot 11 unchanged (n 6-67) | **PASS.** Mean absolute difference to v5 is 0.00-0.54, which is encode noise only. |
| - | Ground share (note only) | Sky and mountains cover y 0 to about 520 (about 40 %). The hive band covers about 520-770 (about 20 %). Bare laterite with tufts covers about 770-1280 (about 40-50 %). This is not a blocker, because the hives stay readable. The caption at y 900 sits on empty ground, which is good for legibility. |

## Conform crop or zoom
**Not recommended.** A 90 % crop (648x1152) only enlarges the frame by 1.11x, and every placement costs an edge hive:
- Centred (36,64): drops the leftmost hive at g821 (box at x 15-35).
- Left-anchored (0,40): drops the front hive's box at g821 (x 650-710).
Either way the count falls to 5. The receding left edge is what sells "many", so keep it.
If editorial wants less ground anyway, the least harmful box is 684x1216 at (0,32), which is 95 %, left-anchored. It keeps all 6 at g821 except the front box's last few pixels, and it trims about 32 px of sky and about 32 px of ground. The gain is marginal.
