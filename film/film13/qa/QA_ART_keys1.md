# QA-art, TAKE gate, film 13 key shots (s01, s02, s17, s26), round 1
Reviewer: QA-art (Opus). Rules: film/QA_TEAM.md (QA-art + Stricter QA C), production-lessons.md section 2.
Frames: 2 fps full size plus every 3rd frame around the key beats, judged on a 360x640 phone sheet with a y 880 guide line.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qaart13/
(*_phone_2fps*.jpg, *_dense_*.jpg, s01_base.jpg, s02_drift.jpg). Frame refs: i = take frame index, g = first_g + i.

Common to all four: sharp, no DOF, no text signs, heads above y 880, the camera moves in every shot (mean 5-frame diff 6-42, never
frozen). The lit 3D world is warm and handsome on the street set. Two problems come back in several takes: the floor/mud/rug fills
35-50 % of the frame, and the key physical fact (height or rise) is not staged so that a phone viewer sees it.

| take | density | light/colour | composition | acting | key moment | match | verdict |
|---|---|---|---|---|---|---|---|
| s01 hook | 7 | 8 | 5 | 6 | **3** | 6 | **FIX-FIRST** |
| s02 tea (2-3) | 4 | 6 | 5 | 6 | **3** | 5 | **FIX-FIRST** |
| s17 false payoff (17-19) | 5 | 6 | 5 | 6 | 6 | 5 | **FIX-FIRST** (light) |
| s26 ending (26-30) | 7 | 6 | 6 | 7 | **4** (fall 8, drop 3) | 6 | **FIX-FIRST** |

---------------------------------------------------------------------------------------------------------------
## s01, shot 1 (hook): "a six-storey hotel rising off the ground". Score 5/10, FIX-FIRST
What works: a beautiful frontal facade (red brick, cream trim, lit sash windows, awnings, portico), warm key, blue sky, dense.
Why it fails the hook: on the phone sheet nothing says that the building is off the ground or rising.
- The base of the hotel is hidden: Pullman, three workers and the front stair stand across the foundation line, and the stair reaches
  the ground, so the hotel reads as grounded (s01_base.jpg, i0/i30/i62). Only one crib pier at the far left hints at jacking.
- The crane goes up while the lift goes up (0.55 -> 0.65 = 0.36 D). In frame the hotel moves DOWN (cornice y ~90 at i0 -> ~180 at
  i62). The eye reads the camera move as the building sinking, the opposite of the hook.
- The lower 30-35 % of the frame is flat mud with a smeared, low-detail puddle reflection (i30-i62). It is not blurred, but it looks
  soft on the phone and adds nothing.
- The dust motes are invisible at phone size.
Fixes (in order of value):
1. Show the gap. Stage the frame so that a band of dark void plus glowing timber cribbing and jackscrews is visible under the whole
   ground floor, across the full width, at about y 750-900 (raise h for this shot to 0.8-0.9 if needed; it is a flash-forward). Move
   the stair aside or leave it hanging, its foot visibly short of the mud.
2. Make the hotel rise IN FRAME: lock the camera height, or crane DOWN slowly / push in, and key the lift faster (0.4 -> 0.7 over
   2.1 s) so the facade climbs about 60-100 px against a fixed reference (street lamp, neighbour building, worker in the foreground).
3. Clear the base: move Pullman and the workers to the sides or to the foreground edge so nobody covers the foundation line. Put one
   worker small beside the cribbing for scale.
4. Lift the camera slightly or tilt up so the mud takes <= 20 % of the frame. Replace the puddle with darker wet mud or remove it.
5. Bigger, brighter dust/grit chunks falling from the foundation edge (about 4-8 px at phone size) to sell the movement.

---------------------------------------------------------------------------------------------------------------
## s02, shots 2-3: guests sip tea; tea perfectly still. Score 4.5/10, FIX-FIRST
Shot 2 (g 63-107): the lady and gentleman are readable, cute and calm, and the window is large. But:
- The room is bare: a plain window wall and ceiling beams. No wallpaper, painting, chandelier, curtains or side table in the frame.
  The rug fills the lower 40 % (i0-i45). The brief asks for velvet, wallpaper, chandelier and paintings.
- The street drift is not visible on the phone (s02_drift.jpg: the skyline barely shifts between i6 and i50; the push in dominates).
  The sky has stepped lime/violet cloud slabs above the window that look like a rendering glitch.
- Sips are small: cup to mouth reads only at full size.
Shot 3 (g 108-158, tea_close): this is the weakest key frame.
- The camera is at rim height, so the tea surface shows only as a thin red sliver (i60-i105). Stillness cannot be read when the
  surface is not visible. Compare s17 shot 18, where the camera is above the cup and the tea disc reads clearly. Use that setup.
- The window is a narrow strip at the left edge. Half the frame is a dark purple curtain or pillar, so the "rooftops sliding down"
  half of the gag is lost.
- The low-poly cup facets are visible at this size.
Fixes:
1. Re-shoot shot 3 from above the cup (like s17 shot 18): a round, mirror-like tea disc that reflects the window, in the lower-middle,
   with the open window filling the upper 50 % of the frame. The rooftops/spire in it must slide down visibly (>= 80-120 px over 1.7 s;
   raise the drift gain or key a faster h for this shot).
2. Shot 2: give the street outside a clear reference near the sill (a rooftop with a chimney or the church spire), and drift it fast
   enough to travel >= 60 px on the phone. Fix the stepped cloud slabs.
3. Dress the suite in shot 2: wallpaper and a gilt-framed painting on a side wall, a chandelier corner at the top, a curtain swag and a
   tea table with a pot. Lower the camera or tilt up so the rug is <= 25 % of the frame.
4. Make one sip read: the cup goes clearly to the mouth for >= 10 frames, then a contented eye-close.
5. Smooth the cup (more segments) or keep it smaller in frame.

---------------------------------------------------------------------------------------------------------------
## s17, shots 17-19 (false payoff + Q2). Score 5.5/10, FIX-FIRST (light, mainly shot 19)
Shot 17 (g 1107-1169): the smug rich man with his top hat and green check coat reads well. The window view down to the city is nice.
- He faces the camera instead of looking out of the window (plan: "looks out the window, smug"). Turn him three-quarter to the glass,
  or have his glance go window -> camera.
- The rug takes the bottom 45 %. A large cropped cup at the right edge is a confusing fragment.
Shot 18 (g 1170-1251): GOOD. The tea disc is visible and mirror-still, with the window reflected and a slow push. This is the best read
of "nothing moved" in the film. Keep it. (Optionally hold the push a little tighter so the disc fills more of the frame.)
Shot 19 (g 1252-1296, Q2 "เห็นมั้ย ไม่ขยับสักนิ้ว!"):
- The "cup raised" is unclear. His thin arm crosses into the gentleman's face, and the cup sits beside the gentleman's ear (i165-i195).
  On the phone it reads as the gentleman's cup, or as him poking the gentleman.
- It is a flat line-up of three figures against the window. The rug fills the bottom 40 % and the room is bare (same as s02 shot 2).
- The mouth moves inside Q2 only (OK).
Fixes:
1. Shot 19: re-pose so the cup is raised in front of his own chest/face on the open side (away from the gentleman), with a clear gap.
   Or swap the side and put the guests behind him. Toast toward the camera on "เห็นมั้ย".
2. Shot 19/17: lower the camera / tilt up and dress the room (painting, wallpaper, chandelier, curtain) so the rug is <= 25 % of the
   frame. Fix the stepped cloud slabs at the top of the window.
3. Shot 17: give him the look out of the window (three-quarter profile to the glass), then a smug glance back. Remove or reframe the
   half cup at the right edge.
4. Keep shot 18 as is.

---------------------------------------------------------------------------------------------------------------
## s26, shots 26-30 (ending). Score 6/10, FIX-FIRST
What works: shot 27 (g 1740-1771) is strong. The portico edge sits on visible glowing cribbing and jackscrews, his panic face is big
and clear, and the foot comes off the edge. Shot 29 (g 1868-1905) is a fun, readable comic fall: a pre-step, the hat flies, a
tumble, he lands sitting with dizzy marks, with no injury. Shot 30 (purse, g 1906-1994) reads at phone size: a muddy, sulking rich
man and a calm Pullman with the purse.
The core of the gag, "the door is 2 m above the stair", is not readable:
- Shot 28 wide (i105-i196): the front stair runs straight up to the portico, so he could simply walk down. The cribbing glow is only a
  thin strip behind the crowd. The townsfolk line (6-8 cards) stands across the hotel base and hides the exact spot that should
  show the height. The rich man in the door is about 20 px tall. The sky is a dull olive-khaki (MORNING), and the warmth of the hook is gone.
- Shot 26 (i6-i68): for the first ~0.7 s he is hidden behind a column (i0-i20), and the low pavement foreground fills the lower 45 %.
- Shot 29: the stair is visible but you still can't tell that its top ends below the portico floor. He lands on dry-looking ground
  with a small brown puddle and sphere "splash" blobs, and does not go INTO the mud.
- Shot 30: the "sit_in_mud" pose reads as standing on short legs. The hat floats above his head (i240-i323). The purse hand-off is
  ambiguous: Pullman already holds it while the rich man's arm touches it. The lower 15-20 % is a smeared grey puddle reflection.
Fixes (in order of value):
1. Make the stair-to-door gap a hard visual fact in shots 28 and 29. Cut or lower the top flight of the stair so it stops clearly 2 m
   below the portico lip, with dark void and lit cribbing/jacks between them and a missing-step silhouette against the light. Frame
   shot 28 three-quarter or side-on to the stair so the step-off edge and the gap are in profile.
2. Shot 28: clear the townsfolk from the base (move them to the edges, small), crane in toward the portico during the shot so he is
   >= 60 px tall by its end, and use the warm DAY/MORNING sky (blue with warm key) instead of the olive sky.
3. Shot 29: land him IN mud. Use a dark wet mud patch at the stair foot that he sinks into to the waist, with a big brown splash crown
   (flat cards or a sculpted splash, not spheres) for 4-6 frames, and mud streaks on the coat.
4. Shot 30: re-seat him (sit pose with legs forward in the mud, body lower), put the hat on the head or knocked crooked on his head,
   and stage the purse hand-off cleanly: the purse in HIS raised hand first (g 1906-1930), then Pullman takes it (g ~1940).
   Remove or darken the smeared puddle at the bottom.
5. Shot 26: start with him already visible in the doorway (not hidden by the column), and lower the camera tilt so the pavement
   foreground is <= 30 %.

---------------------------------------------------------------------------------------------------------------
## Summary
- None of the four key takes passes yet. s17 is closest (one re-pose plus dressing). s01 and s26 carry the film's two most important
  images (the floating hotel, the 2 m drop) and both fail at phone size for the same reason: the gap under or below the hotel is
  hidden or not staged.
- Reusable assets: s17 shot 18 (the tea read), s26 shots 27 and 29 (panic plus fall), the s01 facade lighting.
