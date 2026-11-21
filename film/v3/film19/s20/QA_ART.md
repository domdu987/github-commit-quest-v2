# QA-art, TAKE gate: s20 (HALL hall_low DAY, the astronomer's "ฟลุ๊ค!"): FIX-FIRST, 6.0

Frames checked (take index): 12, 35, 55, 62, 75, 92 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s20_*.png

| Criterion | Score |
|---|---|
| Set density / ornament | 9 |
| Lighting & colour | 8 |
| Composition / phone legibility | 6 |
| Acting (smug shrug) | 4 |
| Key moment ("ฟลุ๊ค!") | 5 |
| Match to refs / client taste | 7 |
| **Overall** | **6.0** |

## What works
- The hall is rich: chandelier, arched window, moon picture, telescope, red and gold. The low angle makes the astronomer pompous. The wig, star coat and pince-nez read. Heads end at y 756 or above. No text.

## Why FIX-FIRST
1. **The shrug is invisible.** The hands sit behind the huge wig and coat. At g 1626-1646 they show only as small dark mitts at the coat edge, and at 360x640 they cannot be seen at all. The snap (k 1.6) then crops the arms out. What reads is a man standing with his mouth open, not "palms up, a fluke!".
2. **"Smug" turns into "shouting".** During the quote the round open talk_mouth shapes (take index 55-75) make him look shocked or yelling. The smug half-lid only returns after the window (take index 92).
3. The frame-diff is low (3.79 / 9.66). Bigger arm action would also help this.

## Fixes (shot.py)
1. Arms outside the silhouette. In pose_of, for arm_r and arm_l, set hand to (+/-1.30, 0.95) at the peak, with layer="front", shape="open", stretch 1.35, bend 0.6 (elbows out, palms up at shoulder height, clear of the wig). Raise the pump to sgn*0.22 and +0.35. The palms must show as two clear white or skin shapes outside the wig at 360x640.
2. Shoulders: add squash (1.04, 0.96) on the pump and head_roll -10 so the shrug reads in the body.
3. Snap: k 1.6 to 1.3 and peak 2.0 to 1.6, so both palms stay inside x 40-680 at g 1633-1660.
4. Mouth: during the window, cap the open shapes with talk_mouth(g, 0.6) and blend with "smirk" (one mouth corner up). Keep expr "smug" with brows half-lid, so the line is spoken smugly, not shouted.

## Round 3 (re-render 09:17): FIX-FIRST, 6.0

Frames checked (take index / g): 20/1592, 45/1617, 58/1630, 64/1636, 75/1647, 92/1664 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey3/s20_*.png

shot.py is unchanged since 08:06. The pose code is still hand +/-0.16, +0.30 pump, squash 0.02, head_roll -6, snap k 1.5, talk_mouth(g, 1.0). None of the round-1 shot.py fixes were applied.

| Earlier fix | Status |
|---|---|
| 1. Arms out of the silhouette, palms up and visible | OPEN. At g 1630-1664 the hands are still small dark mitts at the coat edge, about 30 px at full size, at hip height under the wig lappets. At 360x640 they cannot be seen. There is no palms-up shape. |
| 2. Shoulder squash / head roll on the pump | OPEN. Squash 0.02 is not visible. The lean shows a little. |
| 3. Smaller snap so the palms stay in frame | OPEN (k 1.5, peak 2.0). It does not matter until the arms read. |
| 4. Smug mouth instead of a shout | OPEN. At g 1636 and 1647 a big round black "O" sits under half-lid brows, so he reads as yelling. The smirk only returns at g 1664. |

| Criterion | Score |
|---|---|
| Set density / ornament | 9 |
| Lighting & colour | 8 |
| Composition / phone legibility | 6 |
| Acting (smug shrug) | 4 |
| Key moment ("ฟลุ๊ค!") | 5 |
| Match to refs / client taste | 7 |
| **Overall** | **6.0** |

Blockers: the round-1 fixes 1 and 4 (palms-up arms outside the wig: hand (+/-1.30, 0.95), layer "front", shape "open", stretch 1.35, pump sgn*0.22 / +0.35; mouth talk_mouth(g, 0.6) blended with "smirk"). Then lower the snap to k 1.3 / peak 1.6. If the white or light-grey gloves come from astro19's hand colour, use skin or white so the palms read against the navy coat.

## Round 4 (re-render 09:20): FIX-FIRST, 6.5

Frames checked (g): 1600, 1617, 1624, 1633, 1640, 1647, 1656, 1667 at full size and 360x640, plus phone_grid.png.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey4/s20_*.png

shot.py now has hand (+/-1.30, 0.95) with layer "front", talk_mouth(g, 0.6) blended with the smirk, and snap k 1.4 (accepted instead of 1.3) but still peak 2.6. Squash is still 0.02 and head_roll still -6.

| Earlier fix | Status |
|---|---|
| 1. Arms out of the silhouette, palms up | FIXED in the wide (g 1617-1633): both arms are clear of the wig at shoulder height and the spread reads at 360x640. The hands are still small dark-grey mitts, though, and do not read as open palms against the dark wood and navy. |
| 2. Shoulder squash / head roll | OPEN (0.02 / -6). The lean pump carries the shrug a little. |
| 3. Hands in frame through the snap | OPEN. With k 1.4 and peak 2.6, from g 1640 to the end both hands and cuffs are cut off at x 0 and x 720 (g 1640, 1647, 1656, 1667). For the punch of the line he reads as "wig and coat", not as a shrug. |
| 4. Smug mouth, not a shout | FIXED. There is a small "o" or flat slot under the half-lid brows (g 1633, 1647, 1656), with a still smirk at g 1600-1624. The mouth only moves in the window. |

Acting 6, Key moment 6, Composition 6. **Overall 6.5.**

Blockers: keep k 1.4, but lower the snap peak from 2.6 to about 1.6, or pull the hands in to about +/-1.05 during the snap, so both hands stay inside x 40-680 from g 1633 to 1667. Make the palms white or skin so they read as open palms.

## Round 5 (re-render 09:33): FIX-FIRST, 7.0

Frames checked (g): 1610, 1625, 1635, 1645, 1655, 1665 at full size (frame index = g - 1572), plus 2x crops of both frame edges at g 1645/1655/1665.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey5/s20_g*.png, edges.png

shot.py: hx eases 1.30 -> 1.00 over G_QUOTE-5..G_QUOTE+8 (plus 0.04 pump), squash 0.04, head_roll -10. Snap is still k 1.4, peak 2.6, shift (-0.60, -0.30).

| Earlier fix | Status |
|---|---|
| 1. Arms out, palms up | HOLDS (g 1625, 1635): the spread is clear of the wig. |
| 2. Squash / head roll | FIXED. The -10 roll and the 0.04 squash read as a tilted, smug shrug at g 1645 and 1655. |
| 3. Hands in frame through the snap | MUCH BETTER, NOT MET. Both cuffs and hands are now on screen in every frame, so it reads as a shrug and not "wig and coat". Measured hand extents: g 1635 about x 25-85 and 585-635 (OK). At g 1645 the left hand is x 42-105, but the right fingertips touch x 720. At g 1655 the left fingertips touch x 0, and the right hand is cut through the palm (x 687-720, fingers off frame). At g 1665 the left fingertips are at about x 5 and the right hand is x 650-710. The x 40-680 band from Round 4 is missed at g 1645-1665. |
| 4. Smug mouth | HOLDS. The flat slot at g 1635-1655 and the small "o" at g 1665. |
| Nice-to-have: light palms | Still dark mitts (not a blocker). |

Acting 7, Key moment 6.5, Composition 6.5. **Overall 7.0.**

Blocker (one small change): the snap keeps pushing in after g 1641, so hx 1.00 is not enough. Either take hx to about 0.85 from g 1641 to the end (and drop the 0.04 sideways pump), or lower the snap peak from 2.6 to about 2.2. The goal is that the right hand at g 1655 and the left fingertips at g 1655/1665 sit inside x 40-680. Everything else is approved, so do not touch it.

## Round 6 (re-render 11:19): PASS, 7.3

Frames checked (g): every frame from 1605 to 1673 (take index 33-101, frame index = g - 1572). I looked at edge crops (x 0-120 and x 600-720, y 480-1020) with guides at x 40 and x 680, and at g 1605, 1620, 1633, 1642, 1655, 1673 at full size.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey7/s20/f*.png, /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey7/s20_edges_{0,1,2}.png

shot.py: hx now eases 1.15 -> 0.72 over G_QUOTE-5..G_QUOTE+8, and the sideways pump is 0. The snap is unchanged (k 1.4, peak 2.6, shift (-0.60, -0.30)). Nothing else changed.

| Earlier fix | Status |
|---|---|
| 3. Both hands inside x 40-680 through the snap | FIXED. No hand, cuff or fingertip crosses x 40 or x 680 on any frame from g 1605 to 1673. The left hand enters about g 1616 at x ~65-115 and stays at x >= 60. Through the hold (g 1660-1673) it sits at x ~85-120. The right hand stays at x <= 665, with its closest approach at g 1655-1657 (x ~600-660). It is under the wig at about x 560-600 in the hold. |
| 1, 2, 4 (arms out, squash / roll, smug mouth) | HOLD. At g 1633-1655 the spread is clear of the wig. The -10 roll reads. The mouth is a flat slot or small "o" with a smirk. |

Note (not a blocker): with hx 0.72, the hands are partly tucked under the wig lappets in the hold (g 1663-1673), so the palms read smaller than at g 1633-1655. The shrug has already landed by then. The palms are still dark mitts.

Acting 7, Key moment 7, Composition 7. **Overall 7.3. PASS.**

## Round 6b (light palms) (re-render 13:11): PASS, 7.6

Frames checked: 3 fps through the whole take, plus g 1609, 1615, 1621, 1622, 1626, 1633, 1635, 1636, 1638, 1641, 1645, 1646, 1651, 1657, 1664, 1667, 1672, at full size and at phone size. I also made 2x crops of the hand rows (g 1621/1636/1657/1667) and edge crops with guides at x 40 and x 680 (g 1635/1638/1645).
Frames: /tmp/qa19_s20art/r6b/f3_*.png, /tmp/qa19_s20art/r6b/g*.png, /tmp/qa19_s20art/r6b/sheet_3fps.png, /tmp/qa19_s20art/r6b/sheet_punch.png, /tmp/qa19_s20art/r6b/hands.png, /tmp/qa19_s20art/r6b/edges.png

Changes: light skin open hands, 1.35x larger, with an ink outline, a palm pad and four fingers (runtime patch of puppet._hand in shot.py). Hand y 0.95 -> 1.10 from G_QUOTE-5. Spread +/-0.80. The x1.12 punch is now a plateau around g 1635-1637. Snap k 1.25 and peak 3.0 are unchanged.

| Check | Result |
|---|---|
| 1. Palms read as "palms up" | YES, at phone size, as two open palms on both sides of the body. This is the big win: in every frame from g 1615 to 1672 the two light hands pop off the navy coat and the dark wood, where before they were invisible mitts. One limit: the four fingers fan DOWN and out, and the hands sit at waist height (y ~880-930 in the push, below the lappet tips). So the gesture is "open palms out, so what?" rather than a strict palms-up-at-the-shoulders shrug. With the head tilt and the smirk it still reads as the shrug. |
| 2a. Hand clipping | NONE. In the edge crops the hands stay well inside x 40-680 (g 1635: left x ~55-120, right x ~535-600; g 1645: right x ~560-640). |
| 2b. Hands over the face or wig | NO. The hands are always in front of the coat, below the face. The right hand nearly touches the tip of the right lappet (g 1638-1645), which is a small tangent but not an overlap. |
| 2c. Pasted-on look | SLIGHT. The white cuff, a short band of navy sleeve, then a flat disc hand: the joint is simple, but it matches the cut-paper card style of the whole cast. Not a blocker. |
| 2d. Face size | UNCHANGED (same camera). Crown to chin is about 27 % at the tightest frame, and the face oval is about 18 %. Within §G. |
| 2e. Beat timing | SAME OR BETTER. The snap starts at g 1628 and the x1.12 plateau holds g 1635-1637 right after "ฟลุ๊ค" (g 1633). It reads as a short accent, not a drift. The second pump is still at g 1651-1663. |
| 2f. Mouth outside the window | OK. meta.json has mouth_window [1626, 1672] and mouth_moving_outside_window_frames []. The mouth is a closed smirk at g 1609-1622 and a small "o" or slot from g 1633. Note that meta's window is g 1626-1672, not the g 1627-1667 named in the brief. g 1665-1672 is the out-handle after the cut, so nothing shows on screen outside the line. |
| Float / clip / set | No change. Feet on the floor in the wide half, a medium cut at the shins in the push, rich hall, nothing through the face. |

| Criterion | 6 | 6b |
|---|---|---|
| Set density / ornament | 9 | 9 |
| Lighting & colour | 8 | 8 |
| Composition / phone legibility | 7 | 7.5 |
| Acting (smug shrug) | 7 | 7.5 |
| Key moment ("ฟลุ๊ค!") | 7 | 7.5 |
| Hands clarity | 6 | 8 |
| Match to refs / client taste | 7 | 7 |
| **Overall** | **7.0** | **7.6** |

**PASS, 7.6, BETTER than Round 6 (7.0) and the earlier pre-trim pass (7.3).**

Optional polish (not blocking; do not re-render for this alone):
1. Rotate the finger fan up and out by about 60-90 degrees (fingertips toward the shoulders and sides, not toward the floor) so it is a literal "palms up" shrug.
2. If the hands are touched again, go to y ~1.20 during g 1633-1645 so the hands rise on "ฟลุ๊ค", then settle. Re-check the x 40-680 band and keep them off the lappet tips.
