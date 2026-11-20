# TAKE7 QA s03 (T03, round 5, team4) - verdict: FAIL (1 blocker; 3 small notes)

Checked: all 242 frames (g170-411) numerically (every frame for motion, every 2-4 for dark share), full-size views of g171/198/203/300/378 and 6-frame contact sheets (240x427 and 360x640 scale), dissolve joins vs s02/s06 frames. qa_stats2.py needs a video path (take.mkv not assembled here), so colour stats were computed from the frames.

## Round-4 blockers
1. Deck underside g362-411 - NOT FIXED (measured). Near-black share (luma<25) of the top 35 %: g366 7.6 %, g370 19.2 %, g374 38 %, g378 50.8 %, g380 51 %, g386 36.8 %, g390 29.3 %, g398 16.7 %, g410 8.3 %. It is now dark brown (RGB ~32/15/2), not pure black, and the wood grain reads, but it is still a heavy dark slab, worse than the 25-35 % in round 4 at its peak. Luma<40 share of the top 35 % at g378 is 56.6 %. The point light did not lift it enough. The floating white translucent bulb is STILL there (top centre, g366-380, ~70 px, ghost-white, over the scaffold). Fix: lift the underside material (emission or albedo so luma >= ~45) or add a fill light aimed at the underside; or pitch up / raise the camera so the deck covers <15 % of the top at g370-390; hide the white bulb prop (it sits at roughly x 430-500, y 0-70 at g378).
2. White dome bottom-left g186-210 - mostly fixed. The floating black dots are gone; a pale gravel disc remains (~100 px, ~3-4 % of the frame, g186-215) with a small dark spike in the middle, reads as a satellite dish / tent. Note only: recolour it to match the dirt or hide it.
3. Eiffel findable at the start - PASS (soft). g171: a glowing sphere with a vertical light shaft (~25 px / 90 px) marks the table, visible on a phone; Eiffel himself is ~1 px. Size: ~4.7 % (30/640) at g203, ~8 % at g230, ~44 % at g300 (head and hat 180 px; legs to the floor). BIGZOOM: <5 % to 35 % crossed at g ~288, i.e. 9.8 s, over about 3.9 s of move from g171, inside 3-6 s. OK.
4. Flag pole - the flag is gone but a thin bare wooden stick still sticks up through the white awning (g215-290, centre-right). Reads as a pole through the roof. Note: hide pole or lower it.
5. Wheelbarrow - gone. Dark scatter - the small near-black boxes are mostly gone; a few remain (a black tyre, black bags, two brown toy cows with black outline g198-260). Cosmetic.

## Full pass
- Faces <=35 %: head 180 px of 1280 (14 %) at g300, OK. Ground <=25 %: OK (ground is wide at g186-250 as a dirt plane ~40 % of the frame in the wide, with props; it is the set, not a character, and carried over from round 4, which did not flag it).
- No hard cut inside: highest in-shot step is 38.6 (mean luma delta) at g324, the whipping pan across the yard (motion blur), 3 frames wide, not a cut. Motion median 13.2, p90 27.8, none still.
- Colour: luma 120 (g170) -> 89 (g300) -> 64 (g380, dark deck) -> 75 (g411); sat 0.40 at g170, 0.51 g196, 0.60-0.67 after g250; 0.37 at g362 (sky). Mean sat across the take is OK. Luma is 64-75 over g374-411, under the 85-110 target, because of the slab.
- Dissolves: handle frames are plain takes (luma s02 86 -> s03 120 in; s03 74 -> s06 82 out); the 13-frame dissolve will hide a 34-luma step on the in-join (blue interior -> warm exterior), as in round 4. Both fine; no pop.
- Floating/geometry: crane hook beside the leg (g320-350) reads as a crane. The leg is still slightly curved at g340. The landing is g290-300, later than the word (g268), unchanged and noted before. Riveters still stacked two per platform (g378-411); the hat/arm overlap the leg beam at g285-300.

## Fix list
- g366-411: lift deck underside to luma >= 45 or re-aim so it covers <15 % of the top 35 % at g370-390 (measure again); hide the white bulb g346-380.
- Optional: hide the stick through the awning (g215-290); recolour/hide the gravel disc (g186-215).
Re-render only g340-411 (plus a check); the rest of the take is PASS.
