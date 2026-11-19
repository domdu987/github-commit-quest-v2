# s07 v6 TAKE-gate re-check (shot 10 only, g664-758), round 6   VERDICT: FAIL (3 blockers)

Checked: all 362 frames extracted (g403-764, n = g - 403); phone sheet (180x320, cyan line = y 880) g658/664/668/.../764; full size g700;
2x crops of old man/kid g668/712/756 and farmer/uncle g680/740; kid/spoon every frame g664-699 at 3x, g664-672/694 at 4x, g672 at 8x; per-frame mean abs diff g640-764.
Working files: scratchpad/takes/qa6/ (phone_sheet.jpg, oldman.png, farmer_uncle.png, kid_hits.png, spoon_strip.png, spoon4x.png, spoon8x_672.png, all/).
Narration: "คนทั้งหมู่บ้านหัวเราะตาม แล้วเรียกเขาว่า ไอ้บ้าผึ้ง"

## Tech: PASS
- Cut at g664 (diff 62.9) only. Elsewhere 2.5-3.6 (small bobs and the spoon swing). No pops.
- Heads: all visible heads y ~440-650, chins well above y 880 in every frame. Heads ~105-125 px wide (team claims ~115; matches).
- Left edge: farmer's hat brim starts at x ~25 and the veil at x ~45. **He no longer clips** (v5 non-blocker fixed).
- Right edge: the old man's white body/robe runs to x 720 behind the kid. He is clipped, but this is moot because he is hidden (blocker 1).

## Re-check of round 5 items
| round 5 item | status | evidence |
|---|---|---|
| B1 uncle's arm covers the old man's mouth/beard | FIXED as stated, but REPLACED by a worse problem | The uncle's free arm is now on his own belly (dark hand at about x 465, y 615) and touches no face. But the swap put the old man directly behind the kid's head (blocker 1). |
| B2 kid does not bang the pot | PARTLY | A spoon (spoon14) and a pot (pot14) are now visible, and the bowl lands on the pot face about every 7-8 frames (bowl on pot at ph 1, 7-9, 15-16, 23, 30-31 of each 36-frame cycle). The handle is only ~3-4 px including outline (needs >= 6). In the "raised" position the bowl tucks up behind the kid's chin and arm, not into open air, so the visible travel is ~15-20 px of bowl popping in and out from under the chin. The brown handle sits over the brown fence post. At phone size it reads as a faint stir or dip, not a bang (blocker 3). |
| Should-fix: uncle's point needs an index finger 40-60 px short of the farmer | FAIL | The pointing arm is now in open air (no hive contact, good), but it is bent with the hand raised to about x 285, y 555 and the finger points UP, above the hive and beside the fence post. At phone size it reads as a raised hand or "wait", not a point at the farmer (blocker 2). |

## Acting checks
| check | status | evidence |
|---|---|---|
| Farmer = worried target with hive | PASS | Wide round eyes, 'o' mouth, sweat drop, both hands on the hive box, the whole shot. Inside the left edge. |
| Uncle points AT the farmer while laughing | FAIL | He laughs (eyes shut, open mouth, belly hand). The point aims up, not screen-left at the farmer's face. |
| Old man cackles | FAIL | Not visible. Only his white cap crown shows above the kid's yellow cap, plus a sliver of robe and his stick. His face is fully behind the kid's head and cap in every frame g664-758 (oldman.png). The phone sheet shows a three-person crowd. |
| Kid laughs and bangs the pot | PARTLY | Laughing face reads well. The bang is weak (see B2 above). |
| No face covered | FAIL | Old man's face is 100 % covered by the kid's head and cap. |

## Blockers (round 6)
1. **Old man's face is completely hidden behind the kid's head and cap, all shot (g664-758). He is also cut off at the right edge.** Do not stack him directly behind the kid. Put him in the ~60 px gap between the uncle and the kid, behind them (e.g. x ~ -1.0 instead of -0.2, keep depth 3.9). His head centre should sit at least 120 px from the kid's head centre and fully inside x 720. If four people do not fit at 18.5 mm, drop him: three people are better than a hidden fourth.
2. **The uncle's point does not aim at the farmer.** Straighten the screen-left arm to near horizontal at the farmer's head height (y ~ 550-570), with the index finger pointing screen-left. Put the fingertip at about x 250, 40-60 px short of the farmer's face (his face ends at x ~200), clear of the hive and the post. Hold it all shot.
3. **The pot bang does not read at phone size.** Thicken the spoon handle to 6-8 px with a dark outline. Raise the spoon into open air beside the face (bowl up to screen-right of the kid's head, not tucked under his chin), so the bowl travels at least 25 px visibly per hit. Land each hit on the pot face with a 1-2 frame hold, and optionally add a small hit flash or "clang" lines. Keep 3 hits per burst on the 8-frame grid. (The bowl also lands at ph 30-31, inside the code's "hold" window ph 24-35. Check that the solve matches the plan.)

## Non-blocking
- Heads ~115 px (below the 150 target) with ~380 px of empty ground below; fine for captions.
- Shot 8 pinch claw, grey foreground twigs (unchanged).
