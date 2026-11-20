# QA_ART s01 (HOOK), film 19: **FIX-FIRST**, score 6/10

I checked full-size g 0, 6, 12, 24, 36, 42, 50 and 56, plus phone_sheet.jpg.

**Good:** the frames are sharp, the world is lit, dense and warm, the H1 rocks, there is no text, and heads stay at y 540-770 (all above 880). The snap on "นาฬิกา" lands well, and after it (g 42-56) the shot reads as "proud carpenter points at his machine".

**Problems**
- **The hook does not read in the first second.** For g 0-36 (1.2 of the 1.9 s) Harrison's head is about 120-150 px wide and the H1's right post hides half of him. His near arm lies across his chest, so the pose reads as **folded arms or peeking**, not a two-arm presentation. The apron is hidden too, so the phone sheet shows "a box of gears" plus "a face behind it", not a carpenter.
- **Too much ceiling:** beams fill the top 35-40 % (the camera looks 2 deg up), and the bright diagonal plank at the top right pulls the eye.
- **The lantern** is a flat, saturated orange slab at the lower right, the brightest thing in g 0-42. It reads as a blank sign or caption card.
- **After the snap** the frame cuts the H1 at the left edge (balls cropped, g 50-56).
- meta.json `camera` still describes an old pass (push 7, arc 9, x1.4); it should be push 8, arc 15, x1.35.

**Fixes (shot.py)**
1. **Staging:** move Harrison's mark beside the H1 on the camera side, about 0.8 D right of the post and about 1 D further forward (no longer 1.6 D behind it). Re-key `pose_of` and `TADA_R/L` as an open V with both palms up: the clock-side arm out toward the H1, the other arm up and outward, neither arm across the chest. The apron should show from g 0.
2. **Camera:** start tighter, with his head at least 180 px wide on g 0. Move `CAM_LOC0` about 0.8 D closer and lower `CAM_LOOK0` z (about 2.50 to 2.20) so the frame tilts level or down and drops the ceiling. Cut the snap `shift` x from 0.30 to about 0.12 so the whole H1 stays in frame.
3. **Lantern:** lower its emission by about 60 % or `key_vis` it off. At the least, darken and texture its panes.
4. Darken or hide the top-right lit plank, and fix the camera string in meta.json.
