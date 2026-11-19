VERDICT: FAIL. Blocker: shot 12 (g821-863) shows only 3 hives for the whole shot, at both phone size and full size. It reads as "three hives in a row", not "many". Fix (no crop can solve this, see below): re-render g821-869 with the same light and lens. Yaw the camera about 12-15 deg left, or truck it about 2-3 m right and back, so the front leg recedes across the frame and 6+ roofed hives are visible. Also remove the yellow flower stalks in front of the far hives (x 0-200, y 470-560).

Take: r29/film/v3/film14/s11/take.mkv. 117 frames, g753-869, 720x1280, 30 fps, h264, 3.90 s. meta.json: shot 11 = g759-820, shot 12 = g821-863, handles of 6 frames.
Team v5 note claims "about 6 hives distinct (3 large + 3 small)". Not confirmed: the "3 small" are not hives (see check 1).
Frames: scratchpad/takes/qa_s11v5/
- all/ holds every frame, named by g number.
- s12_phone.jpg is the phone sheet for g818-866, every 4th frame, with a cyan line at y 900.
- cont_full.jpg shows g820, g821, g842 and g863.
- g863_band.png and bands_821_842.png show the hive band at full size.
- g863_left_4x.png is the far-left area at 4x.
- g863_phone_band_4x.png is the hive band at phone size, enlarged 4x.

## Checks
| # | Check | Result |
|---|---|---|
| 1 | Hive count | **FAIL.** There are 3 roofed hives in every frame of g821-863, at both phone size and full size. The front hive is at x 470-720 (cut off by the right edge), the middle hive at x 300-520 and the far hive at x 190-330. The far-left area (x 0-200, y 470-560) holds yellow flower discs on green stalks and a tree trunk. None of them is a hive box or roof, even at 4x (g863_left_4x.png). No 4th hive is visible. |
| 2 | Reads "many hives" in about 1 s | **FAIL.** It reads as 3 hive stands along the maize, which is barely more than shot 11's ONE. The step from 1 to "ten" does not land. |
| 3 | Size and height | OK. The hives are large and clear: boxes about 80-150 px wide, roofs at y about 440-560, boxes at y about 540-660. The band sits well above the caption at y 900. Size is not the problem; count is. |
| 4 | Ground and sky | Weak, non-blocking. Sky with trees and mountains covers y 0 to about 430 (about 33 %). Bare laterite with grass tufts covers about y 640-1280 (about 50 %). The hive band is only about 20 %. |
| 5 | Pops; cut at g821 | PASS. The cut at g821 is a single-frame change (diff 54.5). Shot 12 frame-to-frame diffs ease smoothly from 3.2 up to 5.0 and back down to 3.0, through the handle to g869, with no spikes, black frames or magenta. |
| 6 | Camera moves | PASS. Slow lateral dolly plus push, eased. Diffs are 3.0-5.0 on every frame and the camera never holds. |
| 7 | No text | PASS. |
| 8 | Light continuity with shot 11 | PASS, with a note. Both shots have warm, low DAY sun, long shadows and the same laterite and maize. Shot 11's sky is yellow-orange, while shot 12 looks the other way and has a lilac sky with pink clouds. The cut reads as the same afternoon, so this is acceptable. |
| - | Shot 11 unchanged | PASS. The frames match v3: mean absolute difference 0.0-0.55, which is encode noise only. |

## Why a conform crop or zoom cannot fix it
Only 3 hives exist in the frame. Any crop of the 720x1280 frame keeps 3 or fewer. For example, a 9:16 crop of 405x720 at (100,300) would enlarge the hives to about 1.8x, but it would still show 3, and they would look soft after upscaling. Cropping makes the count worse, not better.

## Fix (cheapest real one)
Re-render shot 12 only: 49 frames, g821-869, at about 62 s/frame, so about 50 minutes. Keep the lens (36-38), the light and the move.
1. Yaw the camera about 12-15 deg left, toward the receding end of the front leg, or truck it about 2-3 m right and back. The leg should run diagonally across the frame from the lower right toward the upper-left middle. Hives 4-7 then come into frame at about x 60-250 instead of being hidden off frame left or behind the tree.
2. Delete or lower the yellow flower stalks and the near tree trunk that sit in front of the far hives.
3. Target at g850: at least 6 separate roofs visible, with the far ones at least 40 px wide at full size (10 px at phone size). Tilting down by about 3 deg more is optional; it puts the band at about y 450-750 and cuts some sky.
