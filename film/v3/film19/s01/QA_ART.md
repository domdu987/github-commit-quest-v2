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

## Round 2: **FIX-FIRST**, 7/10
I checked full-size g 0, 8, 18, 30, 38, 44, 50 and 56 (from take.mkv), plus contact.jpg and phone_sheet.jpg.

**Round-1 fixes**
- Staging / open V / apron from g 0: **FIXED**. The pose reads as "carpenter presents his machine" from the first frame.
- Start tighter (214 px), less ceiling (beams about 25 % at g 0, about 20 % later): **FIXED**.
- Top-right plank: **FIXED**. meta.json camera string: **FIXED**.
- Lantern: **PARTLY FIXED**. It is dimmer, but see (b).
- Whole H1 in frame after the snap: **OPEN**. The left ball is cut from g 18 on, and at g 50-56 about half the H1 is off the left edge. His right hand and ponytail are also cut at the right edge. QA.md's "stays in frame" claim is wrong.

**Director's concerns**
- (a) At 411 px his face fills 57 % of the width and the machine shrinks below his head. Stop at about 300-320 px.
- (b) **Not acceptable.** After the snap the lantern is the largest block in the lower frame (x 470-690, y 790-1230). It hides his apron, sits in the caption band, and reads as a dark-orange cabinet.
- (c) **Only partly.** Gears read, but a cropped box smaller than his head does not read as "big".

**Fixes (shot.py)**
1. Cap the push so his head is at most about 320 px at g 56. Use a snap of about x1.15, or no drift push after g 49. Retune shift x (0.12 to about 0) so the whole H1 with both balls and both of his hands stay in frame through g 56.
2. Use `key_vis` to hide the stool lantern, or move it about 0.6 D screen-right, out of frame after the snap. Nothing should sit in front of him at y 880 or below.
3. Move the g 55 blink to about g 50 so g 53-56 end on open eyes at the lens. At present the last in-shot frame, g 56, has his eyes closed.
