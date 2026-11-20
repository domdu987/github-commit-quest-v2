# QA-art s04 (vista: two towns hold, push to Jimo, 9.89-12.81 s), TAKE gate, Vista round 4 — FIX-FIRST
I reviewed take.mkv at 6 fps (art11/f/NNN.png, g = 295 + 5*(NNN-1)) at full size and on art11/psheet_1-3.jpg (360x640, cyan line = y 880).

## Earlier changes
1. Moat and plank material: The moat is DONE. It is now a textured brown, glinting water or mud ring, and no flat grey remains. The plank is NOT done. The long flat navy slab still lies diagonally across Jimo's yard in every frame (g 380-385, f/019.png, x 70-310, y 580-680), right where the push lands.
2. Pennant cloth: DONE. The field of Yan flags reads as lit black silk with red borders, a strong "sea of enemy flags".

## New problem: Jimo's red flag leaves the frame
The push closes on Jimo's flagpole, so the red Qi cloth leaves the top edge from g 355. From g 375 to the end only a bare pole remains (f/017-019). The last image of the beat is a town with an empty pole surrounded by black flags. On the phone that reads as "Jimo lost its flag", the opposite of "not yet fallen". The take notes list this as a deviation.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 6 | 7 | 5 | n/a (no cast) | 6 |

For the first 2 s the beat is strong: one lit town with a red flag in a field of about 35 black ones. Ju shows as a warm glow at the top left. It is lost in the last 0.5 s.

## Verdict: FIX-FIRST
1. **Keep the red Qi flag fully in frame to the last frame (g 355-391):** Aim the push at the flag's mid-height rather than the yard, or scale the Jimo flag to about 0.3, or stop the push about 10 % earlier. The whole red cloth must sit at least 40 px below the top edge on every frame, and the lit windows must stay in frame.
2. **Navy yard plank:** Texture it as timber or earth, or hide it (same set fix as s03 change 3). Check g 360-391 for zero flat navy areas.

## Notes
- A smaller Ju glow with more wall silhouette would make "two towns" readable without the narration.
- Frame-diff median 4.9 / p90 5.3. The push is steady and has no pulse. A held +15 % snap on "จี๋โม่" (g 360) is still optional.
- The moat ring's mottled texture has a hard rectangular-looking edge at the bottom at g 375-391. Softening it is polish.
