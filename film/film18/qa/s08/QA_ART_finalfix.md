# QA-art FINAL-fix s08: FIX-FIRST

- Reviewer: QA-art, FINAL-gate fix check, 2026-11-20.
- Take: `take.mkv`, 86 frames, g588-673 (in-shot g597-673).
- What I checked:
  - every 5th frame on a phone sheet;
  - full-res frames at g600, 640, 648, 660, 668 and 673;
  - a 2-frame-step crop sequence of the moved soldier over g636-654;
  - a frame-by-frame crop of g645-648;
  - per-frame difference.
- Evidence is in `scratchpad/qa18fix/`: `s08_sheet.jpg`, `s08_full.jpg`, `s08_full2.jpg`, `s08_faces.jpg`, `s08_left.jpg`, `s08_soldier_seq.jpg`, `s08_pop.jpg` and `s08_oldnew.jpg`.

## Blocker B2 (spear-rack shafts through a soldier's face, g640-673): GONE
- No soldier now stands behind the foreground spear rack on any frame. The rack (left third) is clear of every head.
- The moved soldier stands right of the general and laughs from g648. The general laughs from g636.

## NEW blocker: the moved soldier's spear vanishes in one frame at g648 (glitch / pop)
- From g588 to g647 the moved soldier holds a full-length spear: a gold leaf tip with a red tassel, about 550 px tall (about 45 % of frame height), in the sky right of his head.
- On g648, when he snaps into the laugh pose (right arm up), the spear disappears completely. It is not in his hand, it does not fall, and it is gone for the rest of the shot (g648-673).
- It sits centre-right on the laugh beat. On a phone, a tall gold prop simply vanishing reads as a glitch.
- It was introduced by this fix: the soldier is a different rig or position from v1, which had no figure right of the general at this time.
- Also, while he holds the spear, its shaft runs behind his head and comes out of the top of his hat. That is not in front of the face, so it is not a rule fail. It goes away with the fix below.
- **Fix (cheap, only this soldier):** take the spear off him for the whole take, so he matches the empty-handed laughing pose.
  - Or keep it in his left hand through the laugh pose.
  - Then re-render s08 (86 frames, about 13 s per frame) and re-encode.
  - Nothing else needs to change.

## Beat on phone (the Yan general laughs at Jimo): READS
- The general (gold helmet, red plume) is clearly framed and centred. He goes from a stern look to a big laugh with tears, and the soldier catches the laugh.

## Other hard rules
- **Caption band:** clear. Chins are at about y 600-615.
- **Half-cut main character:** none.
- **Pole through a face:** none from the rack.
- **Floating:** none.
- **See-through:** none.

## Notes (non-blocking)
- **N-s08-1:** From about g660 a dark vertical post with a small lamp enters from the top-left edge (x 0-70, y 0-735) as the camera drifts. It reads as a foreground post, not a glitch, and is clear of faces.
- **N-s08-2:** The soldier's body overlaps the general's right shoulder a little (g648-673). The faces are separate, so this is fine.
- **N-s08-3:** Motion is low (frame diff about 3-5 per frame). Accepted at the calibrated gate.
