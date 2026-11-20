# QA-art — TAKE gate round 2, film 20 key camera-travel takes (2026-11-20, Opus)

Inputs: v3/film20/{s03,s15,s18,s24,s27} take.mkv (s03/s24 rebuilt from parts; s18 take.mkv == cat of parts), meta.json, QA.md,
QA_AUTO.md; shot_plan.md incl. the §I re-plan; QA_TEAM.md (client taste, QA-art, Stricter C, §G, §H, §I); ref_shorts R3/R4/R5 sheets;
my round-1 notes TAKE_ART.md.
Frames at 2 fps, full size (720x1280) and 360x640, in
/tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeart2/<take>/{full,ph}/ plus
labelled phone rows <take>_phone.jpg. Frame numbers are global g (tile n ~ first_g + 15·(n-1)).

Scores 1-10: set = set richness (§H), light = light & colour (§I key + rim, warm/cool, red-orange vs blue), comp = composition &
phone legibility, act = acting (§I), key = key-moment clarity & beauty, cam = camera travel (§I) / BIGZOOM (§H),
chan = "same channel as the reference Shorts?".

| take | set | light | comp | act | key | cam | chan | verdict |
|---|---|---|---|---|---|---|---|---|
| s03 BIGZOOM 1 + crane | 4 | 6 | 4 | 6 | 5 | 4 | 4 | **FIX** (major) |
| s15 FALSE PAYOFF | 7 | 8 | 7 | 7 | 8 | 7 | 7 | **FIX** (small) |
| s18 REVEAL dusk -> wire -> hut | 6 | 8 | 6 | 6 | 7 | 8 | 7 | **FIX** (small) |
| s24 BIGZOOM 2 | 3 | 5 | 5 | 5 | 4 | 6 | 3 | **FIX** (major: room) |
| s27 ENDING pull-out | 5 | 7 | 6 | 5 | 7 | 8 | 6 | **FIX** (small, shares the s24 room fix) |

No take passes yet. s15, s18 and s27 are close. s03 and s24 have a big problem each: s03 does not start
extreme wide, and in s24 the restaurant is an undressed blockout.

---

## s03 — BIGZOOM 1 (g 170-411): FIX
Works: the landing on Eiffel (g 260-290) is a good medium. He is warm-lit and proud, with a clear point-up and a blink swap, and
reads well at phone size. The crane up the leg (g 320-395) has strong red-orange lattice against a deep-blue sky, working cranes,
and riveters acting on the platforms. The colour is on brand.

Problems:
1. **It is not a BIGZOOM (§H).** g 170 starts about 40 m off the ground beside one leg. Paris is a single row of identical blocks
   on the horizon, and Eiffel cannot be found at phone size. There is no "whole city from high and far". The way in crosses bare
   orange ground (40-50 % of the frame at g 170-215) rather than roofs, scaffolds and crowds.
2. **Black bars across the frame** (§G "no bars or poles through a face"):
   - At g 200-225 a near-black vertical pole runs top to bottom, right beside Eiffel's body.
   - From g 170 to g 215, and again at g 305, a long diagonal crane jib/cable slashes the whole frame.
   - At phone size both read as render scratches.
3. **The landing set is the emptiest frame in the film.** Behind Eiffel (g 230-300) is a huge untextured pale pier slab with
   speckle noise, about 50 % of the frame. The plan table is a saturated pure-blue block with a black slab edge, filling the bottom
   35 % at g 230-260, and it reads as a blue keyboard rather than plans. On top of the pier wall a riveter is cut at the waist by
   the wall edge (g 200-245), so he reads as a head floating on the wall.
4. g 290: Eiffel is half cut by the right edge on the travel. g 305: the frame is all slab.

Fixes:
- F1 (g 170-230, camera path): start **3-4x further and higher**, at distance about 400 D and elevation 45-55°, framed so the
  Seine, the Trocadéro, the rooftop sea and all four rising legs on their piers are in frame, with the plan table plus a warm forge
  glow at frame centre. Keep the same smootherstep, but route the descent over the roofs and past a scaffold so set detail passes
  close to the lens on the way down (§H "passes through set detail").
- F2 (g 170-310): hide the black vertical pole and the crane cable for the whole take, or move them so they never cross the frame.
  No dark line may cross Eiffel.
- F3 (landing, g 230-300): dress the pier face. Give it the site's stone-block texture and add a ladder, hanging ropes, 2-3 workers
  carrying a girder past behind him, and smoke from the forge. Swap the blue table top for a cream sheet of plans with blue lines,
  tilt it so only its near edge is in the bottom 15 %, and kill the black slab. Move the pier-top riveter back so his full body
  stands on the pier, or hide him.
- F4 (g 285-310): keep Eiffel fully in frame until the aim leaves him, or let him exit cleanly. No half-body on the edge.

## s15 — FALSE PAYOFF (g 988-1096): FIX (small)
Works: this is a big improvement and now looks like the channel. The characters are large and readable. The EXPOSITION
UNIVERSELLE 1889 banner, the red-orange tower and the deep-blue sky make a strong signature colour pair. The seal is readable, and
the smile-drop with the sweat drop on the snap (g 1063-1078) is clear and funny. The crowd moves and the FG back-card adds depth.

Problems:
1. **The document floats (§G).** Both men stand hands-on-hips, and the sealed paper hangs in the air beside them with no hand on
   it (the official at g 988-1003, Eiffel at g 1033-1092, which includes the payoff frame).
2. The official is cut in half by the right frame edge at g 1018-1048, a blocking item under §G.
3. From g 1033 the orbit loses the tower. The middle of the take is a blank white pavilion slab behind Eiffel, and the "20-year
   permit FOR THE TOWER" link is weakest right there.
4. The snap end frame (g 1078-1092) puts hat plus head at about 37 % of the frame height. That is OK as a 1 s punctuation
   (§I.6), but no bigger.

Fixes:
- F1: parent the document to a hand. On the official, use one arm extended holding it (g 988-1020). On Eiffel, use one hand up at
  chest holding it, with the other hand on the hip (g 1020-1092). No paper without a hand.
- F2 (g 1015-1050): reduce the orbit, or let the official step out of frame fully before g 1018. Never half a body on the edge.
- F3 (g 1030-1092): bias the aim so the tower's legs and first platform stay in the top-left quarter behind Eiffel through the
  snap, which also replaces the white slab.

## s18 — REVEAL: dusk -> summit -> wire -> hut (g 1210-1434): FIX (small)
Works: this is the best travel take in the film and matches R5/R3 most closely.
- The violet dusk with the lit lamp-necklace tower is gorgeous.
- The crane to the full tower (g 1315-1330) and the whip down the white antenna wires to the lit hut (g 1345-1375) read clearly,
  and they reveal something (the hut is off screen before the whip).
- The push through the window into the hut works, and the dusk tower stays visible through the hut window inside, giving warm
  and cool in one frame.
- Old Eiffel's worried swap and the officer, wagon and demolition men read at phone size.

Problems:
1. g 1210-1300: the bottom 40 % is empty blue-violet ground with an odd dark shadow blob and a lone crate block. At phone size it
   is a dead floor.
2. g 1388-1396: on the window crossing, a huge orange vertical batten fills the centre third, and the telegraphist is half cut on
   the left edge (g 1390).
3. Inside (g 1400-1434):
   - The telegraphist's hands are not on the Morse key. The arm hangs at his side, so "taps the key" does not read.
   - The spark is warm yellow-white on a yellow desk. The plan's blue-white spark is lost in the orange room.
   - The room is one flat orange-brown, with no rim light on him.

Fixes:
- F1 (g 1210-1300): lower the camera aim about 6° or raise the horizon so the ground is at most 25 %. Dress the near ground with
  the scrap cart, rope coils, crowbars on the cobbles and a gas lamp pool of warm light.
- F2 (g 1385-1398): offset the dive path about 0.3 D so the camera passes between window battens, not into one, and keep the
  telegraphist fully in or fully out of frame.
- F3 (g 1400-1434): put his right hand on the key knob, keyed down on every tap, and the left hand at the headphone. Make the
  spark blue-white (hue ~200, strong emission), with a cool point light that flashes on his face and the wall on each tap. Add a
  small warm oil lamp on the shelf as the key, so warm key plus cool spark rim are in the same frame. Optional: a "T.S.F." sign
  over the door.

## s24 — BIGZOOM 2 (g 1724-1858): FIX (major)
Works: the opening frame is a strong extreme wide. The whole red-orange tower stands over a blue-roofed Paris and green Champ
de Mars, it reads instantly, and the push up the lattice is smooth and fast. The pass through the first-platform girders
(g 1770-1784) is the right idea.

Problems:
1. **The restaurant is an undressed blockout** (§H "no bare backdrops"; §I "rich set"):
   - From g 1784 to the end the frame is horizontal orange and grey bands, an empty wall and a giant low-poly decagonal white
     table filling the bottom 40 %.
   - There are no other diners, no waiter, no chairs visible, no chandelier and no window frames, and nothing is on the plate.
   - It looks nothing like the reference interiors (R4 parlour, R5 galley). This is the BIGZOOM payoff and it lands on the
     poorest set in the film.
2. **Maupassant cannot be found at the start (§H).** No window is lit or marked, so the zoom has no target.
3. **The "first happy bite" (g 1817) does not read** at phone size. The fork is a thin line and the plate is an empty disc.
4. g 1784-1799: a flat orange facade plus a yellow blob (pendant lamp) fill the frame for about 0.5 s. These are the soft frames.
   There is also a black floor-seam line under the table.

Fixes:
- F1 (the s24/s25/s27 restaurant set): dress it like a Belle Époque restaurant.
  - Two or three other diners' tables, and a waiter card walking with a tray (acting).
  - Bentwood chairs, a gas chandelier with warm glow plus wall sconces, potted palm, red velvet banquette, a framed mirror and
    gilt trim instead of the flat bands, and iron lattice girders visible through windows behind him.
  - Replace the decagon with a round table at 32+ segments under a draped cloth.
  - Put a plate with a roast chicken, a baguette and a wine bottle on it.
  - Fix the floor seam.
  This one fix also removes the s27 "blur" flag, which only reacts to the flat pane.
- F2 (g 1724-1770): make his window the brightest warm spot on the first platform: interior lamps on, glass glow, a small red
  awning or a "RESTAURANT" sign (Latin). Then the eye finds the target in the first second.
- F3 (g 1805-1830): enlarge the bite. Raise the fork with a visible chunk of food to the mouth, keyed on g 1817, with cheek-bulge
  chew frames. Keep him at 35-45 % of the frame height and the table edge at no more than 25 %.
- F4 (g 1780-1800): shorten the facade crossing to at most 4 frames, or aim it across the lit gallery railing rather than a blank
  panel.

## s27 — ENDING crash pull-out (g 1964-2045): FIX (small)
Works: the pull-out itself is excellent and very on-channel. It moves from Maupassant through the lattice to the whole tower over
the fair, with flags, stalls, crowds, a lamp-post and a blue sky. The last frame is beautiful, and the 12-frame settle lands
correctly on the hard cut.

Problems:
1. g 1964-1975: a thick brown diagonal post (the preset FG iron post 1 D from the lens) slashes the left third of the opening
   medium. This is the same "bar across the frame" note as round 1.
2. The start is the same empty blockout room as s24: flat bands, a decagon table and an empty plate, with eyes shut and smug but
   nothing to eat. It is the 3-hit QA_AUTO blur flag.
3. Flags: the hero flag on the left at g 2009-2045 is horizontal red-white-blue (it reads as the Dutch flag), and the stall roofs
   carry US flags. In s15 the French tricolour is correct (vertical blue-white-red).
4. After g 1994 nothing tells the eye where he is. The joke ("he eats inside the tower") needs his window to stay findable.

Fixes:
- F1 (g 1964-1990): hide fg_iron_sh, or move it out of the camera path for the whole take.
- F2: use the dressed restaurant from s24 F1, and give him a forkful at the mouth on the first frame.
- F3 (g 1995-2045): rotate the hero flag texture 90° to a vertical blue-white-red tricolour, and swap the US stall pennants for
  tricolours or plain bunting.
- F4 (g 1990-2045): keep his window lit warm (as in s24 F2), slightly brighter than the rest of the first-floor gallery, so the
  tiny Maupassant is still findable on the last frame.

## Cross-take
- Colour: all five takes carry the signature red-orange iron against blue (sky or dusk violet), as §I.3 asks. s18 and s15 are
  the strongest.
- §G floating/cutting: s15 (document, half-cut official), s03 (half-cut riveter on the pier, black pole near Eiffel), s18 (half-cut
  telegraphist at g 1390). Re-check all five on every 0.5 s phone tile after the fixes.
- Re-submit s03 and s24 to the TAKE gate with new contact and phone sheets. s15, s18 and s27 can pass on a sheet check once the
  fixes above are visible.
