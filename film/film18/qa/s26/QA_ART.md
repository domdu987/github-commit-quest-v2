# QA-art s26 (ending: the general runs home chased by oxen, 65.27-70.40 s), TAKE gate round 8 — FIX-FIRST (ending, strict)
Reviewed take.mkv at 6 fps (art10/f, g 1950-2105) at full size and on art10/psheet_0-2.jpg (360x640, cyan = y 880).

## Earlier changes
1. Panic face (general_run_scream): DONE. The wide open mouth with top teeth and tongue now renders below the moustache in every frame. The eyes are wide, and a sweat drop shows on the look-back (g 2075). The jue cup is gripped in a drawn fist and held up. On the phone it reads as a yelling, fleeing general. The brows are still hard to see, which is a note.
2. Sky arc: DONE (no curved seam). But the upper 25 % is now a flat beige-grey with no warmth (y 0-330), the dullest area of the frame on the last image of the film.
3. Final image cup + ox chin: NOT DONE.
   - Cup: from g 2095 the cup is cut by the left edge. At g 2105 (art10/f/031.png) only half the cup shows at x 0-95, and the fist is out of frame.
   - Ox chin: the take notes say the chin max is 821, but the frames show the nearest ox's head reaching y 915-940 (mouth at y 840-940) from g 2085 to the end. The "ตลอดทาง" caption will sit on its roaring mouth, which breaks the client's head-above-880 rule on the punchline frame.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 7 | 6 | 6 | 7 | 7 |

The joke now lands on the phone. The armoured general runs in a panic, screaming with his cup up, and roaring dragon oxen with smoking tails gain on him in front of the warm Jimo wall. What is left is the final image and the dead sky.

## Verdict: FIX-FIRST
1. **Ox head above the caption (g 2080-2111):** Raise the camera's look-at about 60 px (or lift that ox by 0.2 D, or move it 0.4 D farther back). The nearest ox's lowest head point, its open mouth, must stay at y 860 or above on every frame. Measure this on the rendered frame, not from the rig.
2. **Cup and fist in frame (g 2090-2111):** Truck about 80 px left, or move the general 0.3 D right, so the whole cup and the fist stay at least 20 px inside the left edge through the cut.
3. **Warm sky:** Replace the flat beige-grey top with a smooth vertical dawn gradient: pale gold at the top, through peach, to the existing pink at the horizon. Use no arc, and keep the luma at y 0-330 at or above the current value so it stays clean. The last frame of the film should glow.

## Notes
- Raised, tilted brows drawn above the eyes would make the scream more clearly panic and less "grin" at phone size.
- In-shot frame-diff p90 is 7.6, under the 9 guide. The tracking is visible and the held push from g 2068 works, so I accept it.
