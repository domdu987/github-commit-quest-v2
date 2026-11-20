# QA-art: style board, film 20 (set3d20), 2026-11-20

Reviewer: QA-art (Opus). Look approval belongs to QA-art (HANDOFF §3, client decision 2026-11-19).
Looked at: `film/v3/set3d20/styleboard/board.jpg`, sb1_site / sb2_tower_dusk / sb3_resto at 720x1280 and downscaled to 360x640 (phone check),
`hue_report.txt`, BRIEF.md, shot_plan.md, QA_TEAM.md, HANDOFF §3, production-lessons §2 and §8-10, bible colour-light §1 and sets §1.3 and §9.2,
references `film/analysis/sheets/*.jpg` and the approved board `film/v3/set3d10/contact_small.jpg`, and the preset values in `styleboard/sb.py`.

## Measured (my own pass, full-res, 0-255 luma; bible sets §9.2 / colour-light §1.3 targets in brackets)

| still | top 1/8 [40-90] | middle band [105-150] | bottom 1/8 [30-70] | V>0.95 share [0.02-0.09] | dark V<0.25 [0.08-0.15] | luma p1 [~20-30] | mean S [0.40-0.60] | shade hue (hue_report) [240-260] |
|---|---|---|---|---|---|---|---|---|
| sb1_site | 150 | 163 | **172** | **0.27** | 0.08 | 2 | 0.40 | 245 OK |
| sb2_tower_dusk | 77 | 113 | 86 | 0.08 | 0.04 (dusk exterior, fine) | 11 | 0.57 | 240 OK (edge) |
| sb3_resto | **164** | 140 | 47 | **0.16** | **0.01** | 32 | 0.50 | **345 OUT** (red 77 %) |

Reading: the SITE is washed out and bottom-heavy bright (pale sand ground in full sun; the bible wants the bottom darkest). The RESTO is bright at the top
(pale lilac ceiling, 30 % of the frame) and has almost no darks; its hue is dominated by the crimson rug. Only the DUSK still sits inside the targets.

## Scores (1-10)

| still | density / ornament | lighting & colour | composition / phone | key-image clarity | match to refs & client taste | verdict |
|---|---|---|---|---|---|---|
| sb1_site | 4 | 5 | 4 | **3** | 4 | **FIX-AND-REBOARD** |
| sb2_tower_dusk | 6 | 7 | 7 | 9 | 7 | **APPROVED-WITH-FIXES** |
| sb3_resto | 4 | **3** | 4 | **3** | 3 | **FIX-AND-REBOARD** |

The builder's weakness list is accurate; I agree with every item and rank them below.

---

## sb1_site: Champ de Mars building site (shots 3, 4, 5, 11, 12, 13, 14)

What works: Eiffel red-brown lattice colour (`iron #b05a38/#d27c4c`), blue-violet shade hue (245), Trocadéro with two towers sits right in the gap,
sharp, no DOF. Warm sun and blue sky are complementary as in clip A exteriors.

What fails: at phone size the structure reads as a **rectangular iron gantry / portal** seen from underneath (a flat grid deck on four splayed posts),
not as the Eiffel Tower. Reasons: the camera (`loc (-24,-104,1.7)`, 22 mm, look at z 17) is close and low, so we see the underside of the first-platform
deck and the legs leaning OUT toward the frame edges; nothing above the platform continues upward and inward; the legs look straight, not curved.
The ground is a flat pale peach (`sand #e6d3a8/#f2e6c6`) in full sun filling the lower 45 % (bottom eighth 172 against 30-70). Sacks read as
marshmallows, rope coils as cheese wheels, the horse as a sausage, the forges as brown boxes with an orange jelly dome. Fewer than 12 readable objects.

Fixes, ordered by impact:
1. **Make it read as the Eiffel Tower (camera + geometry).**
   - Camera: pull back and up, `loc ≈ (-40, -300, 30)`, look at `(0, 0, 45)`, lens 22. Only the whole footprint shows the curved-leg silhouette. The 125 m square base and the four legs must sit fully in frame, top of the legs around y 250-350.
     This is also the shot 3 "high crane down" start, so it costs nothing extra.
   - Geometry: the four legs must **lean inward and converge** toward a common axis. Above the first platform (57 m), build the four stubs of the second
     stage, already leaning inward with a visibly narrower footprint (≈ 40 % of the base width). The eye then completes the pyramid/spire.
   - Give each leg a **concave curved outer edge**. Use the `tower()` exponential profile, not a straight slant.
   - Put a pale stone masonry pier under each leg foot, `#cbb89a` lit and `#6a6488` shade.
   - Replace the flat grid deck with the real first-platform **box girder band**: a deep lattice belt about 7 m tall, red-brown, with a lighter top rail.
     Add the **big decorative arch** spanning between the front legs below it.
2. **Construction kit that says "Eiffel 1887-88".**
   - Timber scaffold towers, one under each leg mid-span: open square trestles in pale timber `#c89a64/#a87444`, 3-4 tiers with X-bracing, about 30-45 m high, propping the leaning legs.
   - Creeper cranes: a small jib crane with a hanging hook on the inclined top of each leg (the stub ends). These are the most iconic period cue.
   - One or two tall timber derricks with guy ropes.
   - For stage 0 (shot 3), the board still should show **legs only + scaffolds + creepers**, the famous 1887 silhouette.
3. **Ground and foreground (fixes the washed-out bottom).**
   - Ground: replace `sand` with trampled earth `#c9895a` / `#a86a44`, add darker gravel patches `#8a5a3c`, wheel ruts and plank walkways.
   - Put a foreground shade element in the nearest 15 %: the corner of a girder stack or a shed eave in shadow across the lower left. Bottom eighth target 30-70.
   - Exposure: drop the key from 15 to about 11, or add exposure -0.25. Target V>0.95 below 0.09.
4. **Replace the blob props with readable, story props.**
   - Stacks of red-lead **I-girders** with visible flanges, lit `#b4482e`, ends cut, 3-5 layers on timber sleepers. Shot 12 slides along exactly this.
   - Rivet kegs with hoops.
   - Rope as **torus coils with 3-4 visible turns** `#b08a58` with ink line, or cut the coils.
   - Sacks: delete them, or make them tied hessian `#a88458` with a neck and folds, never white.
   - Wheelbarrows, ladders, buckets of rivets.
5. **Forges that read as forges.**
   - A small brick or iron hearth on legs `#5a3a30`, with a conical hood and a thin chimney, plus a bellows.
   - Glowing coal bed as a flat emitter (`#ff8a2a`, strength ≥ 20 so it blooms 12-24 px), a little smoke wisp, and a glowing rivet in tongs on top.
   - Remove the orange translucent dome.
6. **Horse.** Make the draught horse a flat cut-out card like the cast: a clear profile with an arched neck, head, mane, four thin legs and hooves, and harness to the cart.
   Or drop it and use a hand-cart. A 3D tube-and-ellipsoid horse will always read as a sausage.
   Also add 3-5 worker stand-ins on the scaffold and the ground for scale and life.

Verdict: **FIX-AND-REBOARD**. The key image (half-built Eiffel Tower) does not read. Re-render this one still after fixes 1-3 and send it back to QA-art.

---

## sb2_tower_dusk: finished tower, 1909 dusk, antenna + radio hut (shots 1 [day], 15, 18-23, 27)

What works: this is the best image of the board. At 360x640 it reads instantly as the Eiffel Tower:
- curved splayed legs, the big arch, both platforms, a tapering lattice spire;
- warm red-brown iron against a blue-violet sky, a sunset gradient at the horizon, a lit-window city ring and an avenue with lamp-posts;
- shade hue 240, sat 0.57, luma bands inside targets.

Fixes, ordered by impact (the set builder applies them, no re-board):
1. **Blown platform lamps.**
   - Lower `lampsm` emission from 40 to about 10-12, and reduce the count per gallery side (36 to about 20) so the cores stay separate dots.
   - Halo 12-24 px, not a merged white bar. The two galleries should read as warm strings (`#ffcf80` core, `#d7a273` halo), not overexposed stripes.
2. **Wire is a hairline.**
   - Raise `wire_r` from 0.12 to about 0.35-0.45 so it is about 2-3 px on a phone, slightly brighter (`emit_k` 0.5 to 1.5, colour `#f4e8d8`). Shot 19 whip-tilts along this wire.
   - Historically several wires fanned from the summit: use 3-4 wires converging to an anchor post next to the hut, with small insulators.
3. **Spark is a ball.**
   - Replace the 1.1 m halo sphere with a spark gap: two brass balls `#cba048` on rods over a bench, joined by a thin jagged blue-white arc (`#e6f2ff` core, ≥ 60 strength).
   - Keep only a small halo `#9ac0ff` reaching 12-24 px. The current 60 px white disc reads as a moon or ball lamp at phone size.
4. **Hut is a plain box.**
   - Plank walls with battens `#9a6a40/#6e4a2c`, a pitched tar-paper roof with overhang `#3a3450`, a door, a lit window with mullions, a stovepipe and a lean-to with batteries/jars.
   - Add a soldier stand-in or a sentry box beside it. Shots 18 and 22 also need the **demolition wagon**, crowbars and scrap cart at the foot: add them now.
     This fills the empty bottom 15 % of the avenue (density is currently about 12 objects, the exterior minimum).
5. **Clouds and stars.**
   - Replace the flat lozenge clouds with stacked bumpy-top cumulus like the approved set3d10 board: tops `#fcd5b1`, bellies `#ca6a9c` to `#8a78cc`, 2-3 depth layers.
   - Stars: none in the dusk preset (keep the sky gradient clean); allow a sparse, faint set (≤ 15, small, `#c8d0ff`) only for NIGHT shot 21.
6. Foreground: put a dark lamp-post or bench within 1-2 D of the lens at one side (production-lessons §10) so the dusk wide has a shade layer and parallax.

Verdict: **APPROVED-WITH-FIXES**.

---

## sb3_resto: restaurant inside the tower, first floor (shots 2, 24, 25, 26, 27)

What fails:
- At phone size it reads as a **bright hotel banquet hall dressed for a fête**, not "inside the Eiffel Tower".
- The tricolour bunting covers the iron Warren trusses, which are the one cue that says "we are in the tower". The bunting is also invented: the brief does not ask for it.
- The pink-lilac coffered ceiling (`ceil #d6d2e4/#e8e2f0`) takes about 30 % of the frame and is the brightest area (top eighth 164 against 40-90).
- The crimson rug fills the lower right third, which makes red 77 % of chroma.
- The tablecloths are bell/lampshade cones (`r2=0.62` taper).
- The room is sparse: about 14 objects, with no gilt mirrors, no buffet, no diners and a grey stand-in block in mid-frame.
- Window views are pale and washed out (V>0.95 16 %, darks 1 %).

Fixes, ordered by impact:
1. **Show the iron, lose the bunting.**
   - Delete the bunting entirely.
   - Make the Warren trusses the ceiling's main feature: riveted red-brown iron `#9a4a30/#c46a40` with ink lines, crossing the room at full depth.
   - Bring the inclined leg member into frame, near camera right, lattice-braced, and continue it **outside** the windows. Add diagonal lattice girders crossing the window glass from outside, silhouetted against the sky and Paris.
   - Window view: Paris roofs (cream walls, blue-grey zinc roofs), the Seine and the Trocadéro, seen from about 57 m up (looking down), with no tower.
     This is the reveal of shots 2 and 26; it has to be legible at 360x640.
2. **Ceiling and camera.**
   - Recolour the ceiling to warm ochre/brown coffers `#9a5a2e` lit / `#5a3448` shade with gilt strips `#d4a840`. The reference lamp-lit ceiling is `#c03c12` orange; never lilac or white.
   - Lower the camera's view of it: look z from 1.5 to about 1.1, or `shift` from -0.04 to about -0.10, so the ceiling is 15-18 % of the frame (bible: ceiling 0-18 %).
   - Add 3-4 gilt gas chandeliers hanging into the frame as warm emitters that bloom.
3. **Floor and rug: give the room its cool dark block (fixes the hue).**
   - Replace the big crimson rug with a navy carpet `#26395e` (shade `#17153a`) with a crimson border `#562025` (bible palette, reference B hall). Keep parquet `#6b3723/#946645` visible in the aisles.
   - Rug at most 25 % of the frame. This alone moves red from 77 % toward 35-40 % and adds the 14-30 % blue the band wants.
4. **Exposure and walls.**
   - key 32 to about 18, `winfill` 900 to about 350, `fill` 40 to about 15. Targets: V>0.95 at most 0.09, dark 0.08-0.15, mid-band luma 105-150.
   - Walls: `wallres #f0e4cc` is too pale for a large surface (rule: nothing large brighter than V 0.80). Use a cream-gold upper wall `#c8a878` over a dark mahogany wainscot `#491309/#6b3723`, with crimson panels `#8c2a2e` only between mirrors.
5. **Density and dressing (target 20-26 distinct objects in the wide).**
   - Tablecloths as straight-drop cylinders (`r2 = r`) with 6-8 fold flutes, cream `#f3ead6` (never white).
   - 2-3 tall **gilt mirrors** on the right wall `#d4a840` frames with a dim mauve glass `#7e6a78`, and a **buffet/sideboard** with silver domes, bottles and fruit.
   - Potted palms, a coat stand, a waiter's station, more table settings (wine bottles, carafes, bread baskets), and 4-6 diner stand-ins at the back tables.
   - Foreground: a chair back or wine glass in shade within 1-2 D of the lens (shots 24 and 25 both plan one).
   - Remove the grey stand-in block from the hero sightline.
6. **Shade-hue exception.** **Not acceptable as is; must be fixed, with a narrow exception.**
   - Bible rule 3 allows red surfaces to shade "deep crimson", and warm-lit interiors may leave the band if QA.md says why. So crimson cloth or banquettes shading at hue 345-355 is fine.
   - The 345 mean here does not come from warm practicals. 43 % of the frame is "shade", mostly the crimson rug and the pink ceiling, so the whole frame turns red/magenta-leaning. The interior band (red 30-41, blue 14-30) is missed by a mile.
   - After fixes 2-4, re-run `hue_check.py`. Pass condition: shade on non-red surfaces (parquet, cloths, walls, ceiling) at hue 230-260, overall red ≤ 45 %, blue ≥ 12 %, magenta ≤ 10 %.
     A remaining whole-frame shade mean up to about 270 is acceptable with a note in QA.md. 345 is not.

Verdict: **FIX-AND-REBOARD**. The location does not read as "inside the tower" and colour/exposure are far outside the band.
Re-render this one still after fixes 1-4 and send it back to QA-art.

---

## Summary for the director

- sb1_site: **FIX-AND-REBOARD**. Fix the Eiffel read: camera back and up; legs curved, converging inward with second-stage stubs; timber scaffold towers, creeper cranes, stone piers.
  Also darken and texture the ground with a foreground shade layer, replace the blob props with I-girder stacks and real forges, and make the horse a cut-out card.
- sb2_tower_dusk: **APPROVED-WITH-FIXES**. Tame the lamps (lampsm 40 to 10-12), thicken the wire (3-4 wires, r 0.35-0.45), add a jagged arc spark gap, detail the hut and add the demolition wagon, use cumulus clouds, no stars at dusk.
- sb3_resto: **FIX-AND-REBOARD**. Remove the bunting and show the iron trusses and leg passing outside the windows. Make the ceiling warm ochre at 15-18 % of the frame, use a navy carpet with crimson border, cut exposure, darken the walls, use straight-drop cloths, add mirrors, buffet and diners.
  The shade-hue exception is refused except for red surfaces themselves.
- Re-board only sb1 and sb3 (two stills). The SET gate still applies afterwards.

---
---

# v2 re-review (board v2, 2026-11-20)

I re-looked at sb1, sb2 and sb3 at 720x1280 and at 360x640, and used the v2 `hue_report.txt` numbers.

## Decision: the LOOK is approved. The full set build proceeds now.

The direction is right on all three stills, and the key images read at phone size:
- the half-built Eiffel Tower;
- the finished tower with its antenna;
- the restaurant inside the iron.

Everything left is dressing, framing and grade work for the real set. No further board round is needed.
Every item below is a **mandatory set-build fix**. QA-art checks each one, with its number, at the SET gate on the named cameras with stand-in actors.
If any number misses at the SET gate, the result is FIX-FIRST for that camera, not a re-board.

| still | v2 scores (density / light & colour / phone composition / key image / overall) | v2 verdict |
|---|---|---|
| sb1_site | 6 / 6 / 6 / **8** / 6 | **APPROVED-WITH-FIXES** |
| sb2_tower_dusk | 6 / 8 / 7 / 9 / 8 | **APPROVED-WITH-FIXES** (v1 fixes confirmed) |
| sb3_resto | 5 / 6 / 5 / **7** / 6 | **APPROVED-WITH-FIXES** |

### What v2 fixed

- **sb1_site:** the four curved legs now lean inward and converge, with creeper cranes on the stubs, timber scaffold towers and the arch.
  The Trocadéro is framed under the arch. At 360x640 it reads as the Eiffel Tower under construction. The forges now read (hood, chimney, glowing bed).
  The girder stacks are real I-girders. V>0.95 is down from 27 % to 1 %.
- **sb2_tower_dusk:**
  - lamps are separate warm dots, not a blown bar;
  - 4 wires are visible;
  - the stars are gone;
  - the hut has planks, a door and a lit window;
  - a horse and cart now fill the bottom left.
- **sb3_resto:**
  - the bunting is gone; the Warren trusses dominate and lattice crosses the windows outside;
  - the ceiling is warm ochre with coffers;
  - there is a navy carpet with a crimson border;
  - luma is 64/109/42 and dark is 12.7 %, both in band;
  - V>0.95 is 7.6 %.

## Mandatory set-build fixes (checked at the SET gate)

### SITE (cameras site_wide, site_table, site_leg_low, site_fence, site_girders, site_rivet, site_rise)

1. **Ground colour and brightness.** The ground now reads salmon/pink. Change it to warm ochre earth: lit `#c98a54` / `#b07444`, with darker trampled patches `#8a5a3a`, plank walkways and wheel ruts.
   - Bottom eighth luma must be **≤ 70** (it is 111 now). Get there through a foreground element in shade covering the nearest 15 % of the frame plus the darker ground, not through a vignette.
   - Shade hue mean **240-260** (it is 266 now, median 255). The pink ground pushes the shade toward violet; ochre will pull it back.
2. **Foreground 1-2 D from the lens** in every SITE camera (production-lessons §10): a girder end, a shed corner, a barrel stack or a scaffold post, in shade, in the nearest 15 %.
   The barrels in v2 sit about 6-8 m away. Too far.
3. **Scale of the construction cues.**
   - Creeper cranes: jib at least 3x thicker, readable at **≥ 40 px** on 720 wide in site_wide.
   - Timber scaffold towers: **≥ 1/3 of the leg height**, in pale timber `#c89a64` with X-bracing, clearly under each leg.
   - **5-8 workers** (stand-in cards, ≥ 60 px tall in site_wide) on the scaffolds and the ground.
4. **Sky.** The top 40 % is an empty grey-blue gradient. Raise its saturation (top `#3a62c8`, horizon `#f2c89a`) and add 2-3 bands of bumpy-top cumulus as in set3d10.
   Top eighth luma 40-90 is OK at 99 only if clouds break it up. In site_wide, frame the tower so empty sky is **≤ 30 %** of the frame.
5. **Leftover blobs.** Delete the smooth brown mound in the foreground. If a heap is needed, use a gravel heap with stones and shovel. Every man-made prop gets the 3 px ink hull.
   Density in the wide: **12-18 distinct objects** plus life (workers, horse cart, smoke from the forges).
6. **Stage states.** Stage 0, 1, 2 and 3 must all render the tower as converging and tapering (no portal state in any stage).
   Show the second-stage stubs in stage 1, as on this board.

### TOWER dusk / night (cameras tower_dusk, tower_dusk_summit, tower_hut, tower_night_wide)

1. **Wires.** The 4 wires now read as a white light beam. Lower their brightness to about `#d8ccc0` with emit_k ≤ 0.6 so they are pale lines, **2-3 px** at 720 wide (wire_r ≈ 0.25).
   Add a small insulator and anchor post at the hut end.
2. **Spark gap.** The spark is still a white box/ball at phone size. It must be two brass balls `#cba048` with a thin jagged blue-white arc (`#e6f2ff`).
   The halo must reach **12-24 px** beyond the core, and the arc must flash only on the Morse taps (shot 20).
3. **Clouds.** They are still flat lozenges with a pink underside band. Use stacked bumpy-top cumulus in 2-3 depth layers: tops `#fcd5b1`, bellies `#ca6a9c` to `#8a78cc`.
4. **Demolition wagon** with crowbars, ropes and a scrap cart at the tower's foot, plus a foreground lamp-post or bench within 1-2 D of the lens in tower_dusk.
   Density in the wide **≥ 12 objects**.
5. Keep the v2 lamp values: gallery dots separate, halo 12-24 px, V>0.95 at most 9 % (6.9 % now). In tower_night_wide allow **≤ 15** faint stars only.

### RESTO (cameras resto_wide, resto_table, resto_view, and the window for tower_window_pull)

1. **Fill the empty bottom.** Parquet covers about 40 % of the frame with nothing on it.
   - In resto_wide, lower the camera or tilt it up so the floor is **≤ 25 %** of the frame.
   - Put a foreground chair back, a table edge with a wine glass, or a waiter in shade in the nearest 15 % (shots 24 and 25 plan one).
   - Parquet stripe pitch must be **≥ 6 px** at the far edge on a moving camera, or there will be shimmer. Draft a moving strip to check.
2. **Dressing in frame (interior wide 20-26 distinct objects).** The buffet/sideboard (silver domes, bottles, fruit), **2-3 gilt mirrors** on the right wall, potted palms, a coat stand and **4-6 diner cards** at the back tables must be visible in resto_wide, not out of frame.
3. **Tablecloths.** Replace the drums with a straight drop and **6-8 fold flutes**, cream `#f3ead6`, with hem shadow. Each table gets a full setting: plates, glasses, bottle and bread basket.
4. **Window view (the reveal of shots 2 and 26).** At 360x640 the windows must show, seen from about 57 m:
   - Paris roofs (cream walls, blue-grey zinc roofs);
   - a **clear Seine ribbon** `#5a86c8` with glints;
   - the Trocadéro with its two towers.
   The view must be **≥ 120 px** wide in resto_view, with the tower lattice crossing the glass from outside and no tower visible in the view.
5. **Colour (the shade-hue exception, decided).**
   - The median shade hue of 20 is warm parquet shading orange-brown. Bible rule 3 allows that, so I accept it for wood and crimson surfaces.
   - Required at the SET gate on resto_wide and resto_table: blue **≥ 12 %** (8.6 now), magenta **≤ 10 %** (10.9 now), red **30-45 %**.
   - Shade on cloths, cream walls and the carpet must sit at hue **230-260**.
   - Fix it with more navy carpet in frame, a cooler window fill on the cloths (`winfill` colour toward `#3c5cd0`), and pinker-to-orange crimson (`#a41f2c` toward `#a8301c`) to cut the magenta.
   - Write the remaining warm-shade note into the set's QA.md.
6. **Hero card.** Replace the grey "tombstone" placeholder with a real stand-in card (Maupassant at his window table) for every SET-gate still.
   Head above y 880, contact shadow on the chair.

## Verdict v2 (summary)

- sb1_site: **APPROVED-WITH-FIXES**.
- sb2_tower_dusk: **APPROVED-WITH-FIXES** (v1 fixes confirmed).
- sb3_resto: **APPROVED-WITH-FIXES**.

No more board rounds. The builder proceeds to the full set with the list above, and QA-art verifies each numbered item at the SET gate.
