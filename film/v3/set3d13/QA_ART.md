# QA-art, SET gate, set3d13 (film 13, "ไอ้แม่แรง", Tremont House)

## VERDICT: FIX-FIRST
The street is ready. The four key moments are not.

The street matches the film 10 bar: a warm red-brick hotel with cream trim, awnings, a cart and horse, mirror puddles, plank walks and the rosy MORNING sky. It is sharp, has no DOF and no text, and the DAY light is warm.

The four key moments this film depends on do not read yet:
- **Hook:** the lift gap is too small.
- **Ending:** the door above the stair does not show a drop.
- **Tea stillness:** the cup is lavender and the tea reads as milk.
- **Cellar reveal:** the cutaway looks like a board game on an empty plain.

The suite interiors are also below the street's level. All of this can be fixed in one round with camera moves, lights and prop placement. No new modelling is needed apart from lowering the suite's opposite buildings.

Inputs reviewed:
- contact.jpg at full size, and the finals in work/final/ for front_stair, under_wide, hotel_front, tea_close, suite_two, jack_close, under_rows, mud_low, street_wide MORNING and suite_window.
- hue_rows.txt.
- set3d10/contact_small.jpg as the quality bar.
- ref/a and ref/b frames.
- analysis/sheets/window_0.jpg.
- cast13/sheet_client.jpg.

## Scores (1-10) per preset
Columns: D = density/ornament, L = light & colour, C = composition/phone legibility, K = clarity of the key moment the preset carries.

| preset | D | L | C | K | note |
|---|---|---|---|---|---|
| street_wide DAY lift 0.7 | 8 | 8 | 7 | 5 | Beautiful set and leading plank line. The hotel's lifted base is hidden behind the cart, horse and barrels. Bottom 30% is empty mud. |
| street_wide MORNING lift 1 fill 0.5 | 8 | 8 | 6 | **3** | Ending wide (shot 28): nothing shows the hotel is 2 m up. The cart and horse sit exactly in front of the gap. |
| hotel_front DAY lift 0.7 | 7 | 8 | 6 | **4** | Hook: the gap is a ~40 px dark sliver at y 810-850. At the planned h 0.30-0.36 it would be ~20 px, which is invisible on a phone. Lower 30% is dead mud. Two pale faceted blobs (sacks?) at x 430-560 read as unidentifiable objects. |
| front_stair DAY / MORNING lift 1 | 7 | 7 | **4** | **3** | Ending: the telegraph pole runs dead centre through the door and stair. The grey stone plinth reads as a solid wall, so the 3.6 D void is just a thin band behind the stair. No one would see "no ground under his foot". Bottom 35% is empty mud. |
| mud_low DAY lift 0.5 | 7 | 8 | 6 | 6 | The puddle reflection is lovely. The horse's head is a brown blob cropping into the top-left corner. |
| rain_street RAIN | 7 | 7 | 7 | 7 | A good pivot mood. Magenta is 28 %, over the ≤10 % rule. |
| crowd_street DAY lift 0.8 | 8 | 8 | 7 | 7 | Works for the nickname. The same two pale faceted blobs sit in the foreground (y ~1150-1250 full res). |
| under_wide CELLAR lift 0.2 | 6 | 5 | 5 | 5 | The flat dark-violet ceiling fills the top 40%. The jacks are only a 280 px band. The bottom 30% is planks and mud with nothing on it. The oil-lamp pools and vent shafts that should carry the warmth are not visible. |
| under_rows CELLAR cut 1 | 5 | 6 | 5 | **4** | Count/reveal: a roofless brick box on an endless flat tan plane with a horizon. It reads as a board game or diagram, not "under a building". Without beams, the plank caps on the jacks read as little tables. |
| jack_close CELLAR jack 30 | 6 | 6 | 5 | 5 | The lever is a pale pole floating diagonally, not socketed in the jack head, with no hands on it. Dark wedge blocks cover the left edge and bottom-left. The thread is navy-black with no warm highlight. |
| suite_window SUITE | 5 | 6 | 5 | 5 | The opposite buildings are 9-11-storey identical grid blocks (anachronistic, flat, not the 3-4-storey shops in the brief). The flat tiled ground runs to the horizon. The floor and sill fill the lower 45%. |
| suite_room SUITE | 7 | 7 | 6 | 6 | The chandelier glow and velvet chair are nice. Magenta is 29 %. The rug is very busy. |
| tea_close SUITE tea 0 | 6 | **4** | 5 | **4** | The cup, saucer and pot are lavender (all in shade). The tea reads as pink milk, so "mirror-still tea" is not legible. The chandelier crashes into the top third. A second cup overlaps the hero cup. |
| suite_two SUITE | 5 | 5 | **4** | 5 | The rich man is cut at the left frame edge. The bottom 30% is a smeary striped rug that looks soft at 720 (check sharpness). Shade hue is 236 (OUT, needs 240-260). |

**Overall:**
- Density 7.
- Light & colour 7: street 8, interiors 5.
- Composition 5.5.
- Key moments 4.
- Match to refs / film 10 bar 6: the street is at the bar, the cellar and suite are below it.
- Character acting: n/a here. The cast13 sheet is on-model and has every pose the key shots need (rich_step_out, rich_fall, worker_turn_bar_*, lady_sip_tea).

## The 6 fixes (one builder round, in priority order)

### 1. Ending drop: make "no ground under his foot" unmistakable (front_stair, street_wide MORNING)
- **front_stair camera:** move from (7,-25,3.4)->(0,-3,6.2) to a low three-quarter side view, about **(-13,-13,2.0) -> (0,-2,4.0), 22-24 mm**.
  - From there, the portico floor edge and door threshold (z 6.2) are silhouetted over the old landing (z 2.6).
  - The 3.6 D void between them is seen side-on, with the cribbing piers at (±5,-2.6) and lit gap lamps behind it.
  - Put the door/threshold at about y 450-550 and the landing at about y 780 (above the caption band).
  - Keep the stair rising toward the camera.
- **Remove or move the telegraph pole** standing in front of the stair (the y -13 pole near x 0-3). Shift it to x ≤ -14 or hide it for this preset.
- **Make the void read as air:** put dark ambient-occluded shadow directly under the plinth. Raise the 3 gap-lamp intensities about 2x so you see *through* the gap to warm light and the far mud.
- **Paint the threshold lip:** give the lifted stone plinth a cream highlight edge so the drop edge pops.
- **street_wide MORNING:**
  - Move the stuck cart and horse left, x ≈ -32 (off the hotel base).
  - Or move the camera to **(16,-50,2.2) -> (-2,0,8.5)** so the hotel base, the dangling old stair and the gap sit in the middle of the frame (gap at about y 600-720).
  - Aim lower (look_at z 8.5 instead of 15.5) to cut the empty mud foreground. Losing a little sky is fine.

### 2. Hook lift gap (hotel_front)
- **Camera:** from (-7,-38,1.6)->(0,0,13) 18 mm to **(-4,-24,0.5) -> (0,0,10), 16-18 mm**: a worm's-eye view from the mud, with the hotel still whole to the cornice.
  - The gap band should land at y ~720-860 and be at least 110 px tall at lift 0.7.
  - Put a crib pier and a jack in the near foreground on the left third. This fills the dead mud and gives scale.
- **Plan note for the director:** at the planned h 0.30->0.36 the gap is about 1.1 D (one third of a person) and will not read as "a hotel rising".
  - Recommend shot 1 plays **h 0.55->0.65**. It is a flash-forward, so continuity allows it.
  - Add the dust trickle from the plinth edge.
- Replace the two pale faceted blobs (here and in crowd_street) with readable props: burlap sacks with a tie and brown texture, or barrels. Or delete them.

### 3. Tea stillness (tea_close; also helps suite_two)
- **Porcelain:** warm cream-white with a gold rim. Put the hero cup *in the window sunbeam* so it is key-lit, not in violet shade.
- **Tea:** amber-brown (about #8a4a1c to #c07a2e), glossy, and **reflecting a crisp straight mullion line and a sun glint**. A perfectly straight reflection is what sells "not one ripple".
- **Camera:** drop to cup-rim height and look across the cup toward the window: about **(3.2,8.4,31.9) -> (0.4,4.9,31.8), 35-40 mm**.
  - The window and rooftops sit behind the cup (for the "rooftops slide down" in shot 3).
  - The chandelier leaves the frame or only its glow shows at the top edge.
- Move the second cup and pot about 1 D aside so the hero cup's silhouette is clean.

### 4. Cellar reveal: in-world, warm, and clearly under a building (under_wide, under_rows, jack_close)
- **under_wide:** frame it like the aisle shots in the window_0 reference (6-9 s).
  - Camera *inside the aisle between jack columns*, about **(5.3,2,2.0) -> (5.3,40,2.4), 20 mm**, so jack rows frame both sides symmetrically to the vanishing point.
  - Hang 4-5 oil lamps along the aisle at y 8/16/26/40/55 for pools of warm light receding.
  - Make the 6 vent dust shafts cross the aisle.
  - Give the beam undersides a warm bounce so the ceiling is brown-violet, not a flat navy slab.
  - Put 2 workers (worker_turn_bar) in the near rows, left and right thirds.
- **under_rows:** keep the counting view but kill the board-game look.
  - Keep the cross beams (cut only the slab and joists) so every jack visibly pushes a beam. This also stops the caps reading as tables.
  - Pitch the camera steeper (look_at about (5,22,0)) so the pit fills the frame edge to edge and **no horizon or tan plane** shows.
  - Outside the pit, show street mud and the sectioned brick hotel walls rising at the frame edges.
  - Light the pit from the oil lamps (warm inside, violet outside).
- **jack_close:**
  - Make the lever dark iron with a warm rim, socketed into the jack-head hole, with the worker_turn_bar hands on it (the cast pose exists).
  - Place an oil lamp about 2 D camera-right so the thread catches warm highlights.
  - Hide or move the near-left jacks that make the black wedges at the left and bottom-left edges.

### 5. Suite: period view, framing, colour (suite_window, suite_two, suite_room)
- **Opposite buildings:** cut them to 3-4 storeys using the street shops' brick/cream/awning textures (no repeating grid blocks).
  - From the 6th floor you then look *over* their roofs to the church spire and the lake with ships.
  - Replace the flat tiled ground plane to the horizon with the pano skyline ring. The same plane also shows in under_rows.
- **suite_window:** pitch up so the sill and floor are at most 20% of the frame. The street with carts and townsfolk sits in the middle third.
- **suite_two:** camera back and right, about **(-1,7,32.4) -> (-1.5,0,31.6), 22 mm**.
  - Rich man full figure to the knees on the left third, fully inside the frame.
  - Tea table in the foreground right. Window and street behind.
  - Rug at most 15%. Re-check its texture sharpness at 720 (it looks smeared now).
- **SUITE light:**
  - Lower the shade blue from (0.215,0.185,0.55) toward (0.19,0.18,0.46) and pull magenta out. suite_room mag is 29 % and suite_two hue is 236 OUT; target hue 245-255, mag ≤10 %.
  - Let the window sun land on the tea table and the rich man's face.

### 6. Cleanups, colour rule and foreground use (all street presets)
- **mud_low:** pan or move the camera about 2 D right so the horse's head is either fully in frame or out of it, not a brown corner blob.
- **Magenta ≤10 % rule (QA_TEAM A.4):** fix rain_street (28 %), street_wide MORNING (14 %), front_stair MORNING (11 %) and tea_close (12 %).
  - For RAIN, shift the shade and sky toward blue-grey (hue 230-245 in the sky) and drop the violet in the rain streaks.
  - For MORNING, reduce the rose in the sky gradient by about 30%.
- **Foreground mud:** in hotel_front, front_stair and street_wide, the lower 30-40% is bare mud. Either lower the look_at so the set fills the frame, or dress the foreground with a plank walk, a wheelbarrow, a fill pile with a shovel, or a barrel.
  - Film 10's harbour tiles always had props in the foreground third.

## What already passes (keep it)
- The hotel model: brick, cream cornice, lit windows, portico, striped awnings.
- The DAY and MORNING street light and the mirror puddles.
- The rain mood.
- The crowd_street density.
- Sharp everywhere, no DOF, no text.
- Heads are above y 880 in all staged tiles.
