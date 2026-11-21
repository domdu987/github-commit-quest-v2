# QA-tech sH2b v2 (team10 0a81a6c)
Checked: every 5th frame g1389-1519 (contact montages), full-size strips g1464-1489 and g1499/1509/1519/1389, meta.json, QA.md, QA_AUTO.md, rhythm. Colour (lemon-yellow mid-swoop, brightness) not scored per the conform policy; the set palette is scored as content.

## Verdict: PASS (3 non-blocking notes, 0 blocking)

## qa_auto "suspected blur" g1469-1485: FALSE POSITIVE (not a defect)
Full-size g1469/1474/1479/1484 are sharp: grass texture, tree line, river and the far-bank soldiers are all crisp. No DOF or motion blur is used (meta.json says so). The detector fired because the low pass skims plain lawn with little detail. It is not a soft or noisy render, and the camera is NOT inside geometry: at g1464-1469 the red/white pavilion passes at the left-bottom edge as a solid roof (no inside-faces, no clipping seen), then it clears. Not the "planned fast swoop blur" either: the move is a smooth descent, and the lack of detail is the content issue in N1.

## Fixed against the old list
| old item | now |
|---|---|
| 1 crimson block unreadable at P_TOP | FIXED: g1389-1420 shows the crimson block, 5 crimson/gold banners at the loop edge and the blue 5-rank wall at the bridge mouth. The omega, bottle and cork read. |
| 2 grey sickle slab g1449-1460 | FIXED: no grey blades in g1429-1484 (smoke now puffs, banners hidden). |
| 3 Surrey cut by the right edge | FIXED: no cut at the edge. He now stands behind Cressingham (see N2). |
| 4 blue camp soldiers | FIXED: camp soldiers are crimson/dark-grey helmets, none blue. The only blue is the Scots wall on the far bank (correct). |
| QA-art: trap behind them in the payoff | PARTLY: river, far bank, crimson block and flags are in the background of g1494-1519, background soldiers turn toward it; the two main faces still look at the lens (N2). |
| QA-art: fill the empty lower half | FIXED: reeds, gorse and the barrel in the foreground. |

## Beat table (film g, caption time)
| g | t | beat | verdict |
|---|---|---|---|
| 1389-1391 | handles | D6 in from H2a, same P_TOP pose | OK (cam_in = P_TOP exactly) |
| 1392-1421 | 46.30-47.3 | P_TOP trap hold ~1 s: loop, crimson block, blue wall, camp south | OK |
| 1422-1455 | 47.3-48.4 | descent and swoop over the camp, pavilions from above, then tent-roof level | OK (pavilion discs from above are a bit flat) |
| 1456-1468 | 48.4-48.8 | low pass between pavilions and ropes (parallax) | OK |
| 1469-1485 | 48.8-49.4 | low pass over a bare lawn, shadow of a tent | WEAK, N1 |
| 1486-1491 | 49.4-49.6 | the two-shot arrives (blink swap) | OK |
| 1487-1494 | 49.5-49.7 | MEDIUM 2-shot: Cressingham about 36-45 % of the frame height (35-60 %: OK), jaw drop, sweat drops, tiptoe soldiers | OK |
| 1495-1519 | 49.73-50.5 | CU3 push on "อยู่อีกฝั่ง": about 0.8 s, head about 22 % of the frame height (under 35 %), mouth a static O, no lip movement | OK |
Total travel from g1392 to the medium: about 3.3 s, wide to medium, eased. Rhythm median 19.9, p90 38.8: no jump cuts (0 cuts detected).

## Checks
- Heads: Cressingham's head bottom about y 800 at g1519 (under 880). No head over the caption band.
- Nothing floats: feet and shadows on the grass, barrel grounded. Cressingham stands with his arms out (T-pose, stiff but not wrong).
- Edge: no one cut at g1499-1519 (a barrel at the left edge only).
- Camera clearance: no clipping, no inside-geometry frames.
- Colour story: English crimson/gold on the bank, the crimson block and flags on the far side; no blue in the camp.
- Bloodless: yes. No lip motion.
- Join: the cut at g1519 goes to I.

## Issues
- N1 (non-blocking, g1469-1485, about 0.55 s): the swoop crosses empty yellow lawn: nothing to parallax against, and the very sparse, flat frame will also trip qa_auto again. Fix (if cheap): add 6-8 grass tufts, a spear rack or two tent ropes in the strip at the camera path, or lift the camera so the river and the tree line sit higher; or whitelist g1469-1485 for the blur flag in qa_auto.
- N2 (non-blocking, g1487-1519): Cressingham and Surrey look into the lens, so the eyeline to the trap is only carried by the background soldiers, and Surrey is almost hidden behind Cressingham by g1519. Fix: yaw Cressingham 20-30 deg toward the river for the push, and shift Surrey 0.3 m to the right so his face stays visible.
- N3 (non-blocking, g1422-1455): the pavilions seen from above read as beach umbrellas; Cressingham is still not findable as a dot at P_TOP (the team lists both as not done). Fix: add a crimson/gold dot (a pavilion flag) at the bank, or accept.
