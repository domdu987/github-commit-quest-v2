# QA-art s26 (ending: the general runs home chased by oxen, 65.27-70.40 s), TAKE gate re-render — FIX-FIRST (ending, strict)
I reviewed take.mkv at 6 fps (art9/gNNNN.png, g 1950-2110) at full size 720x1280 and on the 360x640 sheets art9_phone_0-4.jpg (cyan line = y 880).

## Earlier changes
1. Lower frame and no rail strips: DONE. The silk strips are gone, period props sit on the verges, and plain road is about 22-27 %.
2. Panic face: NOT DONE. In every frame (g 1950-2110) the general has round eyes and a CLOSED small smile under the moustache (crop_g2075.png, g 2105). No scream mouth, raised brows or sweat drops are visible at full size or on the phone. The render notes say the scream mouth was added, so it is either not applied to this instance or drawn under the moustache/face layer.
3. Lead ox beside him at the cut: DONE. From g 2085 its rage face shows at his right side and reads well.

## Also
- **Sky:** A lavender cap with a curved lower edge and a pink rim crosses the top of every frame (y 0-130). On the phone it looks like a sky-dome seam, not a dawn gradient.
- **Final frames, g 2095-2111:** The cup has left the frame (only a gold spike at x 0-60). The lead ox's mouth sits at y 850-940, so the caption "ตลอดทาง" will cross it.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 6 | 7 | 7 | 4 | 7 |

A phone viewer gets "the dressed oxen chase the general home" against a lovely warm dawn wall. But he looks calm and pleased, so the last laugh (he has to RUN from the oxen) does not land.

## Verdict: FIX-FIRST
1. **Panic face, whole take:** Make the scream actually render. Draw a wide wavy open mouth BELOW the moustache, at least 40 px tall at full size, plus raised tilted brows and 2-3 sweat drops of at least 14 px at 360 wide, layered ABOVE the face and moustache. Check a frame at full size before the full render. Keep the profile look-back at g 2070-2080.
2. **Sky:** Remove the curved dome edge. Use a smooth vertical dawn gradient (lavender to peach) with no visible arc anywhere in frame, or pitch the camera so the seam is out of frame.
3. **Final image, g 2090-2111:** Truck about 60 px left, or move him about 0.3 D right, so the cup stays in frame in his raised hand. Keep the lead ox's chin at y 860 or above, so the cut lands on a scared general, his cup and a roaring ox above the caption.
