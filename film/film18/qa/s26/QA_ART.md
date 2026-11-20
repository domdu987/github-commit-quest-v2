# QA-art s26 (ending: the general runs home chased by oxen, 65.27-70.40 s), TAKE gate round 9 — FIX-FIRST (ending, strict; two small changes)
I reviewed take.mkv at 6 fps (art11/f/NNN.png, g = 1950 + 5*(NNN-1)) at full size (art11/h.png, g 2055 and g 2105 with a y 880 line; art11/c32.png zoom) and on art11/psheet_1-4.jpg (360x640).

## Earlier changes
1. Ox head above the caption: ALMOST done. The nearest ox at the right edge on the final frames (g 2095-2111) has the bottom of its open-mouth outline at about y 885-890, measured on the zoomed pixels (art11/c32.png). It is no longer at 915-940, but it is still about 10 px into the band I asked to keep clear (860). The take notes say "max chin 757", which does not match the pixels.
2. Cup and fist in frame: DONE. The whole jue cup and the fist sit at x 30-200 on the last frame.
3. Warm sky: DONE. There is a smooth pale-gold to peach to pink gradient with no arc, and the last frame glows.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 6 | 7 | 7 |

The joke lands on the phone. The armoured general sprints away screaming, with his cup still up, in front of the warm Jimo gate. Rage-faced dragon oxen with smoking tails gain on him, and the push holds on him and the nearest ox at "ตลอดทาง".

## Verdict: FIX-FIRST (small; the next take should PASS)
1. **Nearest ox mouth at y 860 or above, g 2085-2111:** Move that ox about 0.3 D farther back, or lower it 0.15 D. Do not raise the camera look-at, which would add bare ground. Measure the lowest dark outline pixel of the mouth on the rendered last frame.
2. **Bare ground in the bottom third:** Plain dirt below the feet is about 30-32 % of the frame for the whole shot (y 880-1280 minus the legs). Add one dark, lit foreground prop low in a corner and sliding with the move, such as a dropped Yan helmet, a broken pennant pole or the tipped wine jar from g 1960. Aim for 25 % or less plain ground.

## Notes
- g 1960-1990 (f/003-009): the tipped orange wine jar sits in front of the lead ox's lower face. Moving it 40 px left or down would show the full rage face during "ส่วนขุนพลเยียน".
- Raised, tilted brows would make the scream read as panic rather than a grin at phone size (repeat note).
- A faint warm rim on the general's sprite from the dawn sky would seat him in the light of the set.
- Frame-diff median 6.0 / p90 7.3, below the 9 guide. The tracking and the held push from g 2068 are visible, so I accept it.
