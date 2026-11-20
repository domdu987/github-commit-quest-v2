# QA-art round 11 s26: PASS (notes)
s26 is the ending: the general runs home chased by oxen (g 1958-2111). I extracted every 5th frame (g = 1950 + 5*(NNN-1)), viewed them at full size 720x1280 with lines at y 860 and 880, and zoomed the nearest ox heads at g 2075-2110.

## Round-10 fixes
1. **Nearest ox mouth at y 860 or above: DONE.** I measured the lowest dark outline of the open mouth on rendered pixels. It sits at y 827 at g 2075, 855 at g 2080, 843 at g 2085, 847 at g 2090, 840 at g 2095 and 850 at g 2105. On the last frame (g 2110) the visible ox mouths are at about y 830-850. Nothing roars into the caption band.
2. **Dark foreground prop, plain dirt 25 % or less: PARTLY done, accepted.** The dropped helmet is in the bottom-left corner for the whole take and slides with the move. I estimate plain dirt at about 28-30 % of the frame (pixel mask plus a geometric check, y about 860-1280 minus the helmet, legs and feet). It peaks near 30 % at g 2010-2025. That is in the 25-30 % note band, so it does not block.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 7 | 7 | 7 |

## Notes (not blocking)
- The helmet is small and half cut by the left edge. Scaling it up about 1.3x, or adding a broken pennant pole lying in the lower right, would bring the dirt under 25 %.
- Repeat notes: raised, tilted brows would make the scream read as panic, and a faint warm rim from the dawn sky on the general would help seat him in the set.
- Frame-diff p90 7.2, below the 9 guide. The tracking pull and the push are visible, so I accept it.
