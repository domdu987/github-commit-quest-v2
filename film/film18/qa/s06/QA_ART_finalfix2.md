# QA-art FINAL-fix s06: PASS

- Reviewer: QA-art, last FINAL-fix check, 2026-11-20. Take `take.mkv`, 72 frames, g459-530, cut in.
- What I checked:
  - every 4th frame on a 240x427 phone sheet with the band marked (magenta y 860, cyan 880/950);
  - full-res frames g459, 500, 520 (the "สิบตัว" cue), 527, 529 and 530;
  - a crop of the carrier child's whole body every 4 frames, to check feet and contact;
  - a skin-mask scan of every frame for y 880-950;
  - per-frame difference (90x160 area).
- Evidence is in `scratchpad/qafin3/`: `s06_sheet.jpg`, `s06_full.jpg`, `s06_tail.jpg`, `s06_child.jpg`. The old take for comparison is `scratchpad/qa18fix/s06_sheet.jpg`.

## Blocker B1 (Tian Dan cut by the left edge): still GONE
- Tian Dan is whole on every frame. Through the tail his cap and robe sit at about x 330-500. Nothing is in front of him.

## Carrier change (child's chin in the band): FIXED
- No skin pixels in y 880-950 on any of the 72 frames. The lowest skin row is y 753-795.
- The child's face sits at about y 640-720 and her feet at about y 900-930, standing on the street.
- The woman is behind the child. Her face is visible at the head of the take and hidden behind the child from about g495, so only a sliver of blue robe shows. No head is cut.

## Beat on phone ("สิบตัว"): READS. The frame is not emptier.
- At g520 the upper 60 % of the frame is packed: Tian Dan at medium, at least 8-10 plain oxen across the frame (two big ones at right), the carriers at left, and the roofs and dusk sky.
- Bare ground is the bottom ~30 %, the same as or a little less than the previous take, where the middle of the take had about 40 % plain ground.
- The oxen are plain (no coats, no blades), which is correct for s05-s07.

## Hard rules
- **Caption band:** clear on all frames.
- **Pole through a face:** none.
- **Half-cut main character:** none.
- **Glitch, pop or see-through:** none. Frame diff is smooth, 1.9-10.7, with the held punch at g500-501. No transparency.
- **Floating:** none. Feet touch the street.

## Notes (non-blocking)
- **N-s06-2:** The child and the woman are locked to the camera in a near-standing pose, so they glide with the dolly rather than walk. On the dark street at phone size the ground slide is barely visible, and the feet stay on the ground. If s06 is ever touched again, give them the walk cycle.
- **N-s06-3:** From about g500 a pale moon disc with a cloud stripe enters at the top-left edge (x 0-50, y 310-380). It reads as the moon, not a glitch.
