# s25 / s28 / s29 TAKE-gate QA (film 15, shots 25-31, THE REVEAL, g1329-1803), KEY takes, QA-tech + QA-art

| take | shots | g (with handles) | verdict |
|---|---|---|---|
| s25 | 25-27 | 1323-1517 | **FAIL** |
| s28 | 28 | 1502-1593 | **FAIL** |
| s29 | 29-31 | 1578-1811 | **FAIL**. Two cheap, local fixes. |

Source: origin/render15/team5 @ 0bd6ba1, film/v3/film15/{s25,s28,s29}. The s25 and s29 take.mkv files were rebuilt from their parts (195 / 92 / 234 frames, 720x1280, 30 fps).
I checked every 5th frame (6 fps) plus every cut ±3 frames (1329, 1392, 1470, 1510, 1586, 1652, 1746, 1804) at full size and at phone size (360x640), and compared them with s24 (last frames) and s32r2 (first frames).

**Summary.**
- The light, set, kit and framing are good. The arch in shots 26/27 is big and easy to read on a phone: hips on the bar, head hanging below it on one side, legs hanging below it on the other.
- **The mechanism the narration describes is not animated.** Dick reaches his final draped pose by g1386, before shot 26 starts. He then holds that exact pose, motionless, through all of shots 26 and 27 and into shot 29 (g1386-1592, about 6.9 s). Only the camera moves.
- As a result:
  - "Head over first, then back, then legs" is never shown.
  - The hard rule "nobody frozen" is broken.
  - The p90 motion target fails in s25 and s28.

Timing convention: the team uses WORKER15's g = round(t*30), while the brief for this review gives g = round((t+0.10)*30). The difference is 3 frames, which is inside the ±0.3 s tolerance. Below I give both where it matters. Every take uses the same convention, so this is not an issue.

## Automatic checks
- **qa_auto: PASS on all three takes.** Magenta 0 %. No frozen, black or pop frames.
  - qa_auto reports "no visible change ±2" at 1392, 1470 and 1652. That is a detector artefact: my 90x160 frame diffs at the cuts are 37.2 (1392), 27.3 (1470), 41.3 (1652) and 60.2 (1746), and every cut is on plan.
- motion_check (target median ≥ 4, p90 ≥ 12):

| take | cuts passed | median | p90 | result |
|---|---|---|---|---|
| s25 | 1329,1392,1470,1510 | 4.2 | **6.0** | **FAIL (p90)** |
| s28 | 1510,1586 | 4.1 | **6.6** | **FAIL (p90)** |
| s29 | 1586,1652,1746,1804 | 5.3 | 12.2 | PASS (just) |

- Near-static runs (diff < 2.5 for 8 or more frames): only g1640-1651 in s29 (12 frames, Dick lying on the foam). That is acceptable.
- The camera-only motion in shots 26-28 passes the median, but the figure itself is still. That is a picture problem that the diff numbers hide.

## QA-tech checklist
| check | result |
|---|---|
| Heads above y 880 | OK in all three. The lowest head is the hanging head in shot 27 at about y 740. Podium heads in shot 31 are at about y 650. |
| No text, letters or numbers | OK. The scoreboard is patterned, the flags are generic stripes, and the podium plaques are line-ruled with no glyphs. |
| Mouths | OK. No quote window here. The open "O" in the fall (g1604) and the wide eyes on landing are expressions. |
| Grounding | OK for the run, the lying, sitting and the podium. **The coach in shot 31 stands on the front rim of the upper stand, about 40 px tall** (see s29 fix 3). |
| Shot 25: curve, plant, rise | **weak**. Dick runs at the lens, face front, with only a slight curve. The plant and rise happen at the standard (g1360-1386). **g1374-1382: the bar is drawn across his chest and arm while he rises, so he looks impaled.** He is already fully draped by g1386 (46.1-46.2 s), so the rise and the "head over" are compressed into the last frames of shot 25. |
| Shot 26: part by part (head 46.4, back 47.2, legs 47.8, ±0.3 s) | **FAIL.** The pose at g1392, 1416, 1434 and 1469 is identical. Head, back and legs never cross the bar in sequence, and the body never travels. The head is already over at g1386. "Back over" has no distinct moment. The legs only go over at the flick in shot 29 (g1593-1603, about 53 s). |
| Shot 27: KEY ∩ arch ≥ 50 % width, head and legs below the bar | **OK as a still image.** The arch spans about 65-70 % of the width (feet x≈60 to head x≈600). The hips are on the bar, the head hangs below on the right and the feet hang below on the left, against the dark stand. But it is frozen (see above). The head card hangs upright, face the right way up, which reads as "hanging", not as a backward fold. That is acceptable on a phone. |
| Shot 28: straddle rival flat, whole body high above the bar | **partly.** The whole body is clearly high above the bar (about 1.6 D gap). But: (a) he is tilted about 25° with one leg straight up, so he reads as a starfish or cartwheel, not "lying flat, face down"; (b) he hangs frozen in the sky for 2.5 s with only a pose switch at about g1545 (a pop) and no rise or fall; (c) the gap is so large that he looks unrelated to the bar; (d) g1552-1593: his raised leg is cropped by the top edge. |
| Shot 29: legs flick, drop onto the foam | Flick **OK** (g1593-1603, the legs whip up, which reads well). Drop **broken**: **g1607-1622, the bar is drawn in front of Dick's face and body as he falls** (g1610-1616 the bar crosses straight through his head). It reads as him hitting or crashing through the bar, five seconds before "the bar doesn't tremble at all". He lands g1626-1640 and lies on the foam; that part is OK. |
| Shot 30: bar does not move, light TENSE→EVE at about 56.6 s | Bar: **OK, it does not move.** Light: **OK.** It ramps g1698-1708 (top-of-frame RGB goes from 173/107/118 to 186/133/151), about 0.35 s, which reads as a pop. **Notes:** Dick sits up (g1666-1696) and looks into the lens, not at the bar. The bar is half cropped by the top edge (g1708-1743). The red/white FG "bar peg" at lower right reads on a phone like a fallen piece of bar lying on the mat. |
| Shot 31: stadium erupts, podium + gold, flash bulbs, coach jaw-drop | Podium, gold medal, cheering rival and flash bulbs (g1750, 1763, 1778, 1798) are **OK**. The PUSH! lands at g1776 (59.1 s + 0.10), **OK**. The crowd "eruption" is only flashes and is weak. **The coach jaw-drop is invisible.** He is about 40 px tall on the stand rim and is hidden behind Dick's hair at g1785-1795. Rival2 is cropped at the right edge in the last frames (team note). |
| Dissolve handles 27→28, 28→29 | **OK.** s25 out g1510-1517 (8), s28 in g1502-1509 / out 1586-1593 (8 / 8), s29 in g1578-1585 (8). That is at least half of the 11-frame dissolve plus 2. The s29 out handle into s32 is 8. |
| Continuity with s24 / s32 | **OK.** Same kit (white vest, red/blue chest stripes, navy shorts), same bar, and the same TENSE light from s24 g1328 into s25 g1329. The EVE (s29 out) to DAY (s32) change is covered by the planned dissolve. The bar is the same red/white pole. |
| Cut timing | All cuts on plan within ±1 frame. |

## QA-art (phone, 360x640)
- **s25: clarity 5/10, beauty 7/10.**
  - On a phone you get a big, clear image of Dick hanging backwards over the bar, and that sells "backwards".
  - It does **not** show "head first, then back, then legs". The narration counts three moves while the picture shows a statue and a camera drift.
  - The mechanism the client asked for (the body crosses part by part while the rest hangs below) is the whole point of the film, and it is not on screen.
- **s28: clarity 5/10, beauty 6/10.**
  - "That guy is way up high" reads.
  - "Lies flat, face down, the whole body lifted at once" does not: it looks like a frozen starfish in the sky, far above the bar.
- **s29: clarity 6/10, beauty 7/10.**
  - The flick reads, the landing reads and the podium is warm and festive.
  - But the fall reads as "his face hits the bar", which cuts against the aha line. The coach's reaction is lost.
- Would a viewer who hears the narration SEE the mechanism? **Half.** They see the ∩ with the head and legs below the bar, but they do not see it happen part by part.

## Fixes

### s25 (FAIL). Fixes 1-4 are blocking
1. **g1380-1469: animate the crossing part by part. This is the main fix.**
   - Tween the card so the body travels over the bar and only one part crosses at each beat:
     - **g1392-1395 (46.4 s):** head and shoulders just past the bar and starting to drop. Hips still rising on the take-off side.
     - **g1416-1419 (47.2 s):** back and hips at the apex on the bar, in the ∩ key pose (head hanging below on the far side, legs below on the near side).
     - **g1434-1437 (47.8 s):** thighs and knees come over the bar, with the shins and feet still hanging below on the near side.
   - Ease between the beats so the movement is continuous, with no preset pops.
   - Shot 25 must end (g1391) with only the head at the bar, not the full drape.
2. **g1470-1509, shot 27: no frozen figure.**
   - Keep the ∩ (hips over the bar, head and feet below), but give it life: a slow continuous drift or roll over the bar of about 0.2 D and 3-5° across the 1.35 s, with the hanging head and feet swaying a little.
   - The out handle (g1510-1517) continues the same drift, and s29's in handle (1578-1585) picks it up from there.
3. **g1374-1386, shot 25: the bar passes through Dick's chest.**
   - Keep the card fully on one side of the bar in depth while he rises, either ≥ 0.3 D toward the camera all the way or behind it, so the bar never overlaps his torso.
   - Turn him so his back or shoulder is to the bar at take-off (side or back view), so "backwards" is set up before he goes over.
4. **Motion p90 6.0 → ≥ 12.**
   - The body travel from fix 1 adds a lot of it.
   - Add a quick eased PUSH of 15-20 % in 0.4 s on "ห้อยอยู่ใต้" (49.05 s, g1472-1484).
   - In shot 26, make the lateral track follow the travelling body faster.
   - Re-run motion_check.
5. (minor) Shot 25: give the run a visible J-curve. Start wider left and bend in toward the bar, instead of running straight at the lens.

### s28 (FAIL). Fixes 6-7 are blocking
6. **g1510-1585: make the straddle a real jump, not a hanging figure.**
   - Over the 2.5 s, rise in from the left, roll over the bar **belly-down and horizontal** (the torso flat and parallel to the bar, face turned down toward it, the lead leg along the bar), and come down to the right.
   - Make the apex flat at about **g1540-1560 (51.57-52.39 s "ทั้งตัวขึ้น")**, with the whole body about 0.6-0.8 D above the bar. Then the "lift the whole body" gap reads against the bar instead of floating in the sky.
   - Tween the straddle_a→b switch at g1545 (it pops now).
7. **p90 6.6 → ≥ 12.** The jump trajectory from fix 6 plus a slide that follows it will lift it. Re-run motion_check.
8. g1552-1593: keep the raised leg inside the frame. Pull back about 10 % or lower the camera tilt.

### s29 (FAIL). Fixes 9-10 are blocking. Only g1600-1625 and shot 31 need a re-render
9. **g1603-1625, shot 29: the bar crosses Dick's face as he drops.**
   - Keep the falling card clear of the bar in depth (fully on the camera side, ≥ 0.5 D), or start the drop from below the bar line, so the bar never overlaps his head or body.
   - The bar must look untouched before the aha line.
10. **Shot 31, g1746-1803: the coach jaw-drop must read.**
    - Place coach_stands at least 12 % of frame height, in a clear gap in the stands (left or right third), not behind Dick's head and not standing on the stand rim.
    - Give him a visible jaw-drop: closed mouth → open mouth at about g1776 on the PUSH!. Or use a 0.5 s insert of him if the plan allows.
11. (minor) Shot 30, g1666-1745: Dick should look up at the bar after he sits up (head or eyes turned up-left toward it), as the plan says.
    - Frame the whole bar end on its peg rather than half of it cut off by the top edge, so "it does not tremble" is visibly true.
    - Recolour or reposition the FG peg at lower right so it does not read as a fallen piece of bar.
12. (minor) Shot 31: keep rival2 inside the right edge to the end of the handle. Thicken the "erupt": crowd_mode cheer plus more stand flashes over g1776-1803.

Re-check after the fixes:
- Phone sheets of g1380-1470 at 6 fps, with the part-by-part beats visible at 1392 / 1416 / 1434.
- Shot 28 apex, flat and belly-down.
- Shot 29 g1600-1625 without bar overlap.
- Shot 31 coach.
- motion_check on s25 and s28.
