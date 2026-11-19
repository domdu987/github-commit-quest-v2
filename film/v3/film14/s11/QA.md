# s11 QA v3 (shot 12 re-rendered; shot 11 unchanged from v2) (shots 11-12, g759-863, handles 753-758 / 864-869), team 7
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg); 117 frames g753-869, 18 samples, ~62 s/frame (2 procs).
- Director v2 notes: farmer soles now ON the stool top (mark z 0.26, checked on a full-res crop), contact shadow under the stool; shot 12 camera stays 4.6+ m clear of every roof (dolly x -23 -> -17.5, hive height 2.0-2.1 m, lens 40) so no roof fills the frame; hive boxes visible under the roofs; blurry green ground patch removed (ground material no longer uses the grass mask), ground now sharp laterite; sky about 25-30 % in 11, ~35 % in 12.
- Shot 11: orbit + push round the hive, hive reads as a box (top bars, slot, bees), farmer ties it on with a 3-pose 24-frame arm loop, mouth held flat.
- Known gap: only about 7-8 hives are countable in shot 12 (not all 10) at hive height; ground still ~35 % in 12 (a sharp road, no blur).
- Shots 13 and 14 are NOT in this take (team 6 renders them as take s13 from shot.py).

## v3 (shot 12, g821-869 re-rendered, director recheck)
- Camera: crane from the front-right outside corner (17,-3,3.2) up and out to (23,-9,4.6), lens 20 -> 17, looking along the ring's front + right legs; every one of the 10 stage-2 hives carries the same warm gold bee-cluster glow on its bee end, turned toward the lens, so about 9-10 are countable by g850 at phone size.
- Limits: an exterior view shows the ring as an L (front + right legs), not a full arc; an interior view is a wall of maize (hives hidden), and a 4-5 m camera tilted 20-25 deg down would make the ground over 55 % of the frame, so I kept the camera nearly level. Ground ~45 % (sharp laterite).
- qa_auto PASS on the re-encoded take (117 frames, 18 samples). Shot 11 frames unchanged (stronger stool shadow not done).

## v4 (shot 12 re-rendered again, director recheck 2)
- Glow removed. Camera just outside the front-right corner (17.5,-3.5,2.3) -> (15.2,-1.5,2.6), lens 22 -> 24, slow push-in + 0.3 m rise, huts near the corner cleared at runtime; hive boxes with resting bee specks at each entrance; hive boxes about 100-140 px wide near camera.
- Not met: about 6-7 hives are in frame (front leg left, right leg right of the corner), not 9-10; sky ~35 %, ground ~40 %. Ten distinct hives at this size cannot fit one exterior frame (the L spans ~37 m); a wider lens/further camera makes them dots (v3), a tighter one shows fewer.
