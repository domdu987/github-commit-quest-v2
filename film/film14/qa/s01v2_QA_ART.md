# QA-art, film 14 take s01 v2 (hook, shots 1-3, g0-186), TAKE gate (key shot)
Frames: qa_art_frames/f001-f025.png (4 fps, fN = (N-1)/4 s, take-local), phone tile qa_art_frames/phone_all_1.jpg (180x320/frame),
hang check qa_art_frames/z/hang.jpg (g38-50 every 2nd frame). Compared with film/v3/set3d14/styleboard/board.jpg (DAY), the earlier
s01 QA_ART (v1) and the client-taste rules.

## Verdict: FIX-FIRST (one blocking fix, the rest are small)
Big step up from v1. The hook now reads on a phone in the first second: a farmer in a beekeeper hat up a ladder, a hive with bees in
his hands, two villagers laughing at him from the right; the DAY board palette, mountain, acacias and huts fill the top (f001-f009).
What blocks: the hook's one action, the "hang", is a teleport. At g44 the hive in his hands disappears and a different hive under a
big tin roof pops in lower-left, behind the ladder (hang.jpg frames 3-4). The viewer never sees him hang it; on a phone it reads as a
jump cut inside the shot. Shots 2 and 3 fall back to the v1 problems (empty sky / empty ground, small subject).

## Scores (1-10)
| area | score | note |
|---|---|---|
| Set density / ornament | 7 | Shot 1 is dense and beautiful (maize wall, acacias, huts, snowy peak). Shot 2: top ~35 % is bare gradient sky, mountain gone. Shot 3: bottom ~45 % is bare laterite. |
| Lighting & colour | 8 | Matches the DAY board: golden key, blue-violet shadows, sharp. Shot 2 sky blows to pale yellow at the top. |
| Composition / framing | 6 | Shot 1 good (subject upper-middle, hive ~200 px, sky ~20 %); kid and woman are cut by the right edge (kid half off-frame f006-f009). Shot 2: farmer ~250 px, villagers squeezed into edge pairs and cut. Shot 3: farmer and hive sit in the top half above a big empty floor; the ladder stands in front of the hive. |
| Character acting | 6 | Laughing faces with tears read; woman/kid point up at him. Farmer's smug side-eye in shot 3 reads. But no hanging action, and the shot 3 "sweep toward the hills" is a small wave, not a sweep. |
| Key moment (hook) clarity | 7 | "Man with a beehive, village laughing" reads in 1 s on the phone. "Hanging it on the fence" does not (teleport). |
| Overall match to references | 7 | Right world, light and density in shot 1; shots 2-3 thinner than the board and the approved films. |

## Changes (by impact)
1. **Shot 1, g36-55: make the hang a continuous action.** Keep the same hive object: he lifts it by its bar onto the wire hook
   where it already is in his hands (upper right of his body), and the tin roof is already on the posts from g0 (in frame, top
   right). No swap to a different hive/roof/position at g44. If a swap is unavoidable, match the hung hive's screen position, size
   and the roof to the held one exactly and keep the ladder behind the hive.
2. **Shot 2 (g66-122): tilt down / lower the camera so the sky is <= 20 %** and the mountain and acacias are back in the top; truck
   in ~1 m so the farmer on the ladder is ~400 px tall between the villagers; pull the two edge pairs ~10 % inward so no head is cut.
3. **Shot 3 (g123-186): raise the framing** (tilt down less / lift camera target ~0.6 m) so the ground is <= 25 % of the frame and
   farmer + hive sit in the middle third; move the ladder behind or to the left of the hive. Make the arm sweep big: full arm
   extended toward the mountain, held 0.5 s, and let the pan follow his hand to the peak.
4. **Shot 1: bring the kid ~80 px left** so his whole head and pointing arm are in frame (f006-f009 he is half cut).
