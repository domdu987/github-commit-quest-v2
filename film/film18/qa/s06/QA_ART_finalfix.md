# QA-art FINAL-fix s06: PASS

- Reviewer: QA-art, FINAL-gate fix check, 2026-11-20.
- Take: `take.mkv`, 72 frames, g459-530.
- What I checked:
  - every 4th frame on a 240x427 phone sheet, with the caption band marked;
  - full-res frames at g459, 463, 467, 471, 519, 523, 527 and 530;
  - a skin-mask scan of every frame for y 880-950;
  - per-frame difference (area 90x160).
- Evidence is in `scratchpad/qa18fix/`: `s06_sheet.jpg`, `s06_head.jpg`, `s06_tail.jpg`, `s06_oldnew.jpg` and `s06_chin.png`.

## Blocker B1 (Tian Dan cut by the left edge, g500-530): GONE
- Tian Dan (yellow robe, black cap) is fully inside the frame on every frame of the take.
- At g500-530 his cap and robe sit well inside the left edge, at about x 360-500 of 720.
- I compared g527 with the conformed v1: in v1 his cap and face were clipped, and here he is whole.
- His walk bounce still reads. There is no pop when the camera lock takes over (frame diff 2.7-13.1, smooth, with the punch at g497-502).

## Beat on phone ("สิบตัว", oxen collected): READS
- Ten plain oxen fill the frame behind Tian Dan, and the carriers (child and old man with baskets) give scale and life.
- The oxen are plain (no coats, no blades), which is correct for s05-s07.

## Hard rules
- **Caption band (y 880-950):** no main-character face.
  - Tail (g525-530): the basket child's chin touches y 881-882 (1-2 px). The caption "สิบตัว" sits clear of it. Note only.
  - Head (g459-473): the same child exits right with his chin down to y 886-948 while half out of frame. This is **byte-identical to the conformed v1**: the skin-mask numbers match frame for frame. The re-render did not change it, it was passed at FINAL, and the centred caption does not overlap him. Note only.
- **Half-cut main character:** none.
  - The old man (g467-475, right edge) and the blue-robed man (tail, left edge) are clipped extras, which the rules allow.
- **Pole through a face:** none.
- **Glitches or see-through artefacts:** none. No pops, flicker or transparency.
- **Floating:** none. Everyone's feet are on the street.

## Notes (non-blocking)
- **N-s06-1:** If s06 is ever re-rendered again, keep the basket child's chin 20 px or more above y 880 at the head and tail.
