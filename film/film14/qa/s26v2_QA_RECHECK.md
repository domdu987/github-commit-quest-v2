VERDICT: PASS. The trunk pops are gone. No trunk or limb covers another elephant's face. Everything that passed before in shot 27 still passes. Shot 26 is unchanged.

# QA_RECHECK s26 v2 (film 14, shots 26-27, g1758-1919, 162 frames)

Take: scratchpad/takes/r24/film/v3/film14/s26/take.mkv (720x1280, 30 fps, h264, 162 frames). take.mkv.partaa+partab are byte-identical to take.mkv. meta.json is unchanged from v1: first_g 1758, shot 27 starts at g1840 (cut), g1 1913.
Previous report: film/film14/qa/s26_QA_RECHECK.md (1 blocker: trunk pops at g1854, 1868, 1882, 1896, 1910).

## What changed (shot.py diff r21 -> r24; c14.py, sheet.py and meta.json are identical)
- `shot27()`: `tr = 'sniff'` for every elephant on every frame. This replaces the `k//14` toggle between 'reach' and 'sniff'. In cast14 TRUNKS, 'sniff' is the low pose (a0 -28°, a1 -58°) and 'reach' is the near-horizontal forward pose (22°, 8°) that crossed the face behind. So the team kept the low pose.
- `yaw_fixed = 0.4 * atan2(...)`: each card turns 40% of the way toward the lens, so the remaining angle is 0.6 x the old angle. elephant_b's worst case of 34° becomes about 20°, which matches the team's "about 20°" claim.
- No other code changed.

## Method
- All 162 frames were decoded to scratchpad/takes/qa_s26v2/all/ (f000 = g1758).
- metrics.txt has, for each frame: luma, mean frame diff, max 16x16 block diff above y 880, and the diff against the v1 frames (qa_s26/all).
- A 32x32 block-diff spike detector ran on the herd region (y 380-880) over g1840-1919 and was compared against v1.
- Visual strips at full resolution covered each old pop frame ±1 (trunk_1854/1868/1882/1896/1910.png). Visual sheets covered the herd across the shot (herd_sheet.png, s27_overview.jpg), a 2x zoom of the trunks and the calf's face (zoom_trunks.png), and a boosted ground crop (ground_boost.png).

## Checks

| # | check | result |
|---|---|---|
| 1 | Trunk pops gone (every frame g1840-1919) | **PASS.** The tusked elephant's trunk stays in one low pose from mouth to ground through the whole shot. It moves only with the walk, head_dip and the camera, and does not jump on any frame. This was checked visually at ±1 frame around g1854, 1868, 1882, 1896 and 1910. Above y 880, the max 16x16 block diff around those frames is now 41/27/31/37/37 against neighbours of 26-41, with no bump (v1 had 38-41 against about 28-30). On the herd-region spike detector, the old pop frames now score 0.91-1.24x the local median. v1 scored up to 1.36x at g1882. The remaining small peaks (≤1.24x, e.g. g1910, g1867) line up with the 5-frame mouth chomps and blinks, which are not trunk motion. Mean frame diff runs smoothly from 4.2 to 2.9 over g1841-1918. |
| 2 | No trunk or limb across another elephant's face | **PASS.** The tusked elephant's trunk runs down and to the left, across the lighter elephant's chest and forelegs, and its tip ends in the leaves. It passes behind the calf's crown tuft, and the calf, which is in front, occludes it. The calf's eyes and face are always clear (zoom_trunks.png at g1862, 1890, 1910, 1919). The calf's own trunk is low, by its mouth, and sits over ground and leaves. The lighter elephant's trunk hangs thin and straight down. No raised trunk appears anywhere in the shot. |
| 3a | Dark blue night elephants | PASS (unchanged). At g1900 the tusked elephant's body is RGB (52, 52, 64), luma 53. The calf is (61, 56, 78), and the soil is luma 27. B is higher than R on the cards. Mean shot-27 luma is 75-78, the same as v1. |
| 3b | Contact shadows | PASS. In the boosted crops there is a dark blue-black pool under the calf and under the adults' feet, and no foot reads as floating. |
| 3c | Stalks fall | PASS. Tall maize hides the herd at g1840. The stalks are mostly down by about g1858 and fully down by g1894, the same as v1. |
| 3d | Low camera, always moving | PASS. CAM27 is unchanged (2.40-2.45 m high, truck left). Frame diff is 2.87 or more on every frame g1841-1918. g1919 is 0.99 because the camera move ends at g1918; it is the last handle frame (after g1 1913), and v1 was the same (0.97). |
| 3e | Heads above y 880 | PASS. Adult heads are at y about 450-600 and the calf's head at about 680-780. |
| 3f | Cut at g1840 clean | PASS. There is one hard cut, diff 70.0 (v1: 70.04), with neighbours at 7.25 and 4.26. There is no flash and no duplicate frame. |
| 3g | Cards turned ≤ about 20° | PASS by code: the remaining angle is 0.6 x the old angle, so 34° becomes about 20°. In the frames, no card reads as a flat sliver, and elephant_b at the left edge reads as a normal profile. |
| 4 | Shot 26 unchanged | **PASS.** Decoded frames g1758-1803 are bit-identical to v1. g1804-1839 differ only by encoder noise: mean abs diff 0.08-0.48 and max 16 levels. The noise is spread uniformly over the textured ground and none of it is in the sky (s26_vs_r21_diffx16_f081.png). The GOP structure is identical. This is consistent with x264 lookahead seeing the new shot-27 frames after the I-frame at g1840 (36 frames back). It is not a render change. |

## Non-blocking notes (carried over, optional)
- The warm golden fill on the foreground grass in shot 27 (y 950-1280, mostly under the caption band) is still there.
- QA_AUTO.md still reports the known false positive "suspected blur" on shot 27 (relative sharpness metric). It was checked in v1, and nothing in the render path changed.

Artifacts: scratchpad/takes/qa_s26v2/ (all/, metrics.txt, metrics.py, s27_overview.jpg, trunk_1854.png, trunk_1868.png, trunk_1882.png, trunk_1896.png, trunk_1910.png, herd_sheet.png, zoom_trunks.png, ground_boost.png, s26_vs_r21_diffx16_f046/072/081.png).
