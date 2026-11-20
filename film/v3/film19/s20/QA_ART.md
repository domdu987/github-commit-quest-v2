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
