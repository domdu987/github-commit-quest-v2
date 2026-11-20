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
