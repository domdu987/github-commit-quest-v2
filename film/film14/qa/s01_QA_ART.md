# QA-art, film 14 take s01 (hook, shots 1-3, 0-6 s), TAKE gate (key shot)
Frames: qa_art_frames/f001-f025.png (4 fps; fN = t (N-1)/4 s), phone tile qa_art_frames/phone_all.jpg (180x320 per frame), plus phone_sheet.jpg and contact.jpg.
Compared with the approved styleboard film/v3/set3d14/styleboard/board.jpg (DAY) and the client-taste rules.

## Verdict: FIX-FIRST
The light and palette match the board, and the take is sharp. The hook image does not read on a phone in the first 2 s, though.
Shot 1 is a wide where the woman in the front is the biggest, brightest thing. The farmer is small up the ladder. The "beehive" is a
small brown box (f003: about 75x40 px at full res, 20x10 px at phone size) with no bees, and the top 35-40 % of every frame is empty
gradient sky. A blind viewer sees "people laughing at a man on a ladder", not "a man hanging a beehive". In shots 2-3 the big
foreground props (black chicken, pumpkin vines, gourd, cob basket) take the bottom third and pull the eye away from the subject.

## Scores (1-10)
| area | score | note |
|---|---|---|
| Set density / ornament | 6 | Maize wall, acacias, stools and stones are good. But the top ~40 % is bare sky, and the huts and snowy peak from the board DAY panel are missing. The density sits in the foreground clutter, not in the world. |
| Lighting & colour | 7 | Warm golden key, long blue-violet shadows on red laterite. Matches the board's DAY. The sky gradient is flat and takes up too much of the frame. |
| Composition / framing | 4 | Shot 1: the subject (farmer + hive) is small and placed upper-left of centre, and the woman dominates (f003-f009; at f008 she is cut by the right edge with her face half the frame width). Shot 2: the chicken, vines and gourd fill y 900-1280, and the fence/hive is barely visible (a tin roof at left). Shot 3: gourd, cob basket and pumpkin crowd the bottom edge, and the hive is cut by the left edge. |
| Character acting | 6 | The laughing faces (tears, open mouths) read well. The farmer's smug side-eye plus hand sweep in shot 3 (f018-f025) reads as "calm, sure of himself": good. Shot 2 villagers spread their arms but do not point at anything; no clear eyeline to the farmer or fence. |
| Key moment (hook image) clarity | 3 | It fails the phone test: in the first 2 s the hive is not recognisable as a hive (no bees, no tin roof until the push-in at ~1.75 s, and it is half hidden behind the farmer's legs and ladder at f008). |
| Overall match to references | 5 | Right world and light. Framing is weaker than the board and the approved films: they show the set, and here the sky and foreground props fill the frame. |

## Changes (most score per change first)
1. **Shot 1 (0-2.2 s): make the hive + farmer the hero from frame 0.**
   - Camera: lower, closer to the fence, tilt down. Target the f008-style framing at g0 and push gently from there; do not start wide.
   - Farmer + hive: upper-middle third. Hive at least ~200 px wide on the full-res frame, under its little tin roof, in front of the
     farmer's body (not hidden by his legs or the ladder). He lifts it by its bar onto the wire.
   - Bees: give the hive a trickle of bees, 6-10 cards round the entrance (set_bees low), so it reads as a beehive on a phone.
   - Villagers: move the woman and kid back about 1.5 m and toward the frame edges as laughing side wedges, roughly 60 % of their current screen size, with eyelines and pointing up at the farmer.
   - Sky: no more than about 20 % of the frame.
2. **Shot 2 (2.2-4.1 s): clear the foreground and put the target in the shot.**
   - Remove the black chicken, the pumpkin vines and the gourd from the lower third, or push them to a corner at no more than about 12 % of the frame height.
   - Re-aim the camera so the fence, hive and ladder farmer are visible between or behind the villagers.
   - Change the arms from spread to pointing at the fence (v_kid_laugh_point-style for at least 2 of them).
   - Fix or remove the flat grey basin card floating between the woman and the kid (f011-f015): it reads as a blank rectangle.
3. **Shot 3 (4.1-6.0 s): re-frame on the hive.**
   - Drop the gourd, cob basket and pumpkin out of the bottom edge, or set them small at the side.
   - Pan or truck right so the whole hive, its roof and the wire running to the next posts sit fully in frame beside the farmer.
   - Lower the horizon so the fence line recedes along the maize. This is the fence_line preset idea; the posts on the right are already there.
4. **All three shots: fill the upper frame with the set, not empty gradient.** Add the board's DAY background (thatched huts, granary, the snowy Mt Kenya peak, more acacias), either through camera height/tilt or by moving them into the sight lines. Keep the existing light preset.
