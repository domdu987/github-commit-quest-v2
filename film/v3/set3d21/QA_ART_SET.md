# QA-art, SET gate, set3d21 (film 21, Stirling Bridge)

Reviewer: Opus QA-art. The client delegated set approval to this review.
Inputs: contact.jpg (each tile viewed at full 720x1280 from contact_tiles/), contact_small.jpg (the phone check), hue.md, API.md, styleboard/QA_ART.md (R1/R2), shot_plan.md, BRIEF.md, QA_TEAM.md, production-lessons §2 and §8-10, bible sets.md §9, colour-light.md, cast21/sheet.jpg.
Own checks: Laplacian sharpness by band, the head json of every tile, and 7 draft test renders of proposed fixes (scratchpad: splash size 1.8 at an earlier age, camp_table at half distance, riverbank yawed right 25/45 deg, bridge_end_north raised, hill_eye without the fg spears and heather).

## VERDICT: FIX-FIRST on 4 tiles. The other 11 presets are PASS-WITH-NOTES and may start rendering now.

- **FIX-FIRST (builder, before any shot on them renders):**
  - camp_table (shots 10 and 28, the ENDING)
  - camp_bank (shots 11, 12, 18, 19 and 25: the mocker and the false payoff)
  - riverbank (shots 29 and 30)
  - river_low together with `splash()` (shots 30 and 31: the last image)

  These four carry the key beats. They cannot be repaired per shot: the dressing, the marks and the splash geometry are built around the preset camera, or the prop that has to read is not in the build.
  The fixes are cheap: about 4 s build and 75-140 s render per tile. Re-render these 4 tiles plus one splash strip; I re-check only those.
- **PASS-WITH-NOTES:** hill_over, hill_eye, hill_low, bridge_deck, bridge_high, bridge_end_north, bridge_end_south, valley_wide, valley_loop, valley_river, camp_wide. The fixes the director noticed on these (dark fg poles, the orange post, magenta) are object hides and camera offsets that I tested or that are trivial. They go to the render teams below as per-preset instructions.
- **Hard rules hold:** no DOF or haze. The top band is sky (low Laplacian is expected) on every ground tile. valley_loop's top band is 315 against 337 in the middle band, and valley_wide's grey hill face is 277, so it is texture, not blur. Shade hue is 230-267 everywhere and in band (240-260) on the ground tiles.
- **Head-band breaches the contact sheet did not flag.** API.md says "all heads above y 880", but:
  - camp_wide `k1` sits at cy 1109 and `k2` at cy 995
  - valley_river `e1` sits at cy 910

  The teams must re-stage these (see the notes). QA-tech fails any head at y 880 or below.
- **Lenses: hill_over 32 mm and camp_bank 30 mm are accepted** as the exception R2 allowed (fix 1 option "lens 28-32"). At 22 mm the hook bridge in hill_over falls to about 190 px (the target is at least 240). The camera cannot go further forward without the ledge hiding the bridge. Every other preset stays at 22 mm. The director lists this as a camera-rule exception in the client report (FYI, not an override of a FAIL).
- **Blue-heavy tiles:** hill_low 55, bridge_end_north 61, riverbank 66.
  - This is accepted for exteriors near the clip-A exterior row (blue about 53).
  - hill_low is sky by design (shot 6 is "spears up against the sky").
  - bridge_end_north drops to 56 with the camera offset below.
  - riverbank (66) is over even for an exterior, and its fix below (sky 30 % or less) brings it down.
  - The earthy Scots tunics and the red/blue/gold English cast add the warm share in the takes.

## R2 fix list, checked
| R2 fix | status |
|---|---|
| 1 camp_bank bridge and Scots read (BLOCKER) | **Partly done.** The bridge is about 318 px long, but only about 22-24 px tall with its piers (target 35 or more). About 5 riders, 10-12 px tall, are readable at full size. On the phone sheet the bridge is a 10 px line. The far Scots: about 15 lit figures, 7-8 px tall, under the crag, with no visible spear glints. Accepted for the Scots, not for the bridge → FIX-FIRST |
| 2 camp_bank clean frame (BLOCKER) | **Partly done.** The tents are off the water and the black stubs are gone. **Still open:** one full-height banner pole at x about 455-470 splits the frame and cuts the bridge; the lower 50 % is still the spike-grass carpet (no path or mud); no sunlit red/cream pavilion faces → FIX-FIRST |
| 3 valley_loop wakes | Done: short V trails, no zebra bars |
| 4 valley_loop hill and cork | Partly done. The cork slot is clear. The Scots line on the hill's shade side is still a dark seam (not lit tan bodies). Not blocking: the reveal reads at phone size |
| 5 valley_loop camp | Done enough: grouped clusters, varied tents, lanes. Pavilions still read a bit as umbrellas from above. Accepted |
| 6 hill_over foreground | Mostly done: bottom eighth luma 78 (was 62-68; target 80-110), violet 6.3. The far range is still mottled pink/green. Accepted |
| 7 remaining presets | All 15 exist with fg, marks and hooks. The bridges have a deck two horses wide, piers and foam collars. camp_table has the chest, the scale, coin stacks and a blank ledger, **but the scale does not read** (see FIX-FIRST) |
| R1 9 settable counts | Done: `place_troops` covers bridge, causeway, meadow and south |

## Per tile (score 1-10, one line)
| # | tile | score | note |
|---|---|---|---|
| 1 | hill_over | **7** | A good hook. The bridge is about 280 px long at frame centre, with knights two by two, the camp, the castle rock at upper left and the teal river. The edge shafts are thin (about 3 % dark columns). The lower 35 % is a spiky orange/brown carpet, darker than it should be but acceptable |
| 2 | hill_eye | **5** | Two dark spears at 1.5 and 1.7 m make about 150 px of black bars (20 % of the width). The 1.8 m heather mound is a pink dome (magenta 13). The crag behind is in deep shade. Tested: hiding the fg spears and heather gives magenta 4.4, dark 0.08, val 0.45. Team-fixable |
| 3 | hill_low | **6** | The low angle into the sky works for shots 6 and 21. Abbey Craig reads here as a bald smooth dome (no crag, few gorse). Heads s1, horn and s3 are at cy 804-851 (below the 450-760 band). The spear fg crosses s3. Blue 55 is sky: OK |
| 4 | bridge_deck | **7** | Reads at once: rails, plank grain, two horses' width, the hill with its pines behind. The rail post fg is fine. The top 30 % is plain sky (the push removes it) |
| 5 | bridge_high | **6** | The best "only crossing / jam" image: 16 knights two by two along the deck, the loop beyond. **The flat orange post (about 170x500 px) reads as a cartoon block.** White criss-cross wake strokes right of the bridge read as scratches. The loop meadow is a bare yellow plate |
| 6 | bridge_end_north | **5** | As delivered: a black spear bar 90 px wide at left, sky 45 %, and the bridge mouth hidden behind the cards. Tested offset (below): the deck, the knights, the causeway and the camp across the water all read, sky about 30 % |
| 7 | bridge_end_south | **5** | Two full-height spear poles (about 60 px each) box the frame like bars. The bottom 40 % is empty sand. The bridge mouth itself is good: posts, rails, deck at knee height |
| 8 | valley_wide | **6** | The establishing shot reads: loop, bridge, camp, castle rock, fields with hedges. The near Abbey Craig is a pale mottled egg with a glowing orange rim and a thin crag read. The upper-left range is a heavy dark shade mass |
| 9 | valley_loop | **7** | The reveal works on the phone: pear loop, bridge neck, camp outside, hill with crag. The Scots on the hill are in shadow and barely read. The pavilions are umbrella-ish |
| 10 | valley_river | **7** | Pretty and clear: river band, the crag with red-trunk pines, the far bank line. A blown-white foam strip lies on the near bank. Head `e1` is at cy 910 (in the caption band) |
| 11 | camp_wide | **7** | Dense, lit and alive: pavilions, parade knights, smoke, river, hill. The right-hand lawn is empty green. Heads `k1` at cy 1109 and `k2` at cy 995 are below the caption line |
| 12 | camp_table | **4** | The table is 5.7 m away and Cressingham's head is about 60 px. **The scale does not read** (a thin gold beam against the yellow meadow, behind a canopy pole). The chest is a grey box. The bottom 45 % is shaded sand. The canopy reads as a beach parasol. The ending (shot 28) cannot play here. Tested half distance: the table fills the frame but the scale is still not visible |
| 13 | camp_bank | **5** | The water and the crag with the Scots are there and the light is warm, but the bridge is a 22 px line, the centre banner pole splits the frame through the bridge, and the lower half is spike grass. Cressingham's card at 3.6 m is huge: his head is about 160 px |
| 14 | riverbank | **4** | **No water near the cast.** The English stand on a dry meadow 5-9 m from the lens and the channel is about 20 m off frame right. Tested yaw 25 and 45 deg: water appears only far right and far away. Shot 30 ("they jump into the Forth") has nothing to jump into. Sky 45 %, lilac shade, blue 66 |
| 15 | river_low | **4** | The three splashes at ages 0.35/0.55/0.8 read as white-lilac boat hulls or swans. Tested size 1.8 at ages 0.2-0.42: they read as lilac crystal lumps with a thin glowing stick, still not spray crowns. A blown-white foam band runs across the near bank (y 850-1050). The cattails are oversized brown cylinders. This is the last image of the film |

## FIX-FIRST list (builder; re-render these 4 tiles + a splash strip)
1. **river_low and `splash()`: a spray crown that reads at phone size (also used in riverbank shot 30).**
   - The crown sheet:
     - make it **white emission-lit foam**, not a shaded diffuse surface: the inner/outer faces must not turn lilac (shade at most 15 % darker than lit, hue 200-230 if anything)
     - open it outward: the tips flare out 30-45 deg
     - break it into **12-16 separate tapered spikes**, each ending in a droplet bead, instead of a closed scalloped wall
   - Size 1 height: the crown about 1.4-1.8 m tall at age 0.25-0.4. The central column 0.18-0.25 m thick, 2.5-3 m tall with a bead cap.
   - Droplets: **60-90 per splash**, radius 0.06-0.14 m (8-20 px at 12-18 m), on arcs that land outside the crown.
   - Optional: a low mist puff of 6-10 white flat discs at the base. No round blob stacks (production-lessons §9).
   - river_low preset:
     - default ages 0.15 / 0.3 / 0.45, `size` 1.6-2.0
     - the three crowns spread across x 120-620 at y 560-760 (the water band), each crown at least 150 px tall in the final frame
     - kill the blown-white foam band (white share V > 0.95 at most 9 %)
     - cattails 40 % thinner and shorter
   - Target: on the 360x640 sheet a blind look says "splashes", not "boats/swans/lumps".
2. **riverbank: put the water in front of the English (shots 29-30).**
   - Move or turn the camera so the **loop channel runs across the frame, x 300-720 at y 620-800**, with the bank edge 1-3 m from the marks. Example: put the camera on the bank looking along it, with the water on the right half.
   - Marks e1-e4 stand on the mud or reed strip at the waterline, heads 560-720.
   - The bridge stays visible in the background (blocked by the spear wall in shot 29).
   - Sky at most 30 % of the frame. Blue at most 55. Warm the near meadow shade (it reads lilac).
   - Check that `K.splash()` points 3-6 m out into the channel land at x 250-650.
3. **camp_table: build the ending table to be read (shots 10 and 28).**
   - Camera 2.6-3.2 m from the table front, 1.2-1.4 m high, 22 mm. The table spans 70-85 % of the frame width at y 560-800.
   - **The coin chest in the fg/middle ground** at frame left (x 60-300), lid hinge visible, lid at least 120 px tall when open, iron bands inked.
   - **The scale** at frame right (x 430-640), at least 150 px tall, the beam at least 140 px wide, 5-6 cm thick, dark silver pans with ink outlines, against the water or sky (not the yellow meadow), with no pole in front.
   - Coin stacks and the ledger between them, gold reading at phone size.
   - Cressingham's mark behind the table centre, head at y 470-560 and about 110-140 px tall. The empty-table state (shot 28) must still read as "his place": add his stool or a cloak hung on it.
   - The canopy edge may cross the top 20 % only. The barrel and rope fg stay at the frame edges.
   - The bottom: show the front of the table and a rug or worn grass, not 45 % shaded sand.
4. **camp_bank: finish R2 blockers 1-2.**
   - **Remove the centre banner pole** at x about 455-470 (or move it into the fg banner pole at x ≥ 640).
   - **The bridge reads:** at least 35 px tall with its piers and at least 300 px long. Do this by moving the camera about 40-55 m toward the bridge along the bank (for example from (-140, -17.3) to about (-90, -15)) with the lens at 22-30. Re-place the marks and `camp_fg` so x 260-560 at the bridge's height stays clear.
   - At least 4 knight pairs on the deck, each at least 12 px.
   - Replace the near spike grass (the lower 40 %) with a worn bank path, mud and reeds toward the water, as R2 asked.
   - Bring one sunlit red/cream pavilion face into the right third.
   - Cressingham's card: at 3.6 m his head is about 160 px, so let his chest cross the frame edge. Target head 120-140 px, cx 150-230, cy 520-620.
   - Keep the far Scots line: at least 15 figures, at least 7 px, with spear glints added (a gold or steel tip of 2-3 px).

Re-check criteria:
- the 4 tiles at 720x1280 plus the phone sheet
- heads 450-760
- magenta ≤ 10
- bridge height measured in camp_bank
- a splash strip river_low at ages 0.1 / 0.25 / 0.4 / 0.6 / 0.9

## Notes for render teams (per preset)
General, all presets:
- Heads at cy 450-760, never 880 or lower. Check `head_report()` after your first frame.
- If you move the camera more than about 1 m or 5 deg, call `K.stage_placeholders(A)` again or use billboards.
- Hiding an fg prop: `for o in bpy.data.objects: if o.name.startswith(PREFIX): o.hide_render = True`. In `fg_generic`, the posts and spears are in `fg_generic_wood` and `fg_generic_steel`, gorse and reeds in `fg_generic_g_*`, rocks and heather in `fg_generic_r_*`.
- To add your own fg spear: `B = K.Batch(96); x, y = K.at_px(K.PRESETS[p], d, xp); K.spear(B, (x, y, K.ground(x, y)), tilt=(tx, ty), h=3.4); B.finalize('fg_team')`.
- A fg shaft or post may cover at most **50 px of width** at its widest and must never sit dead vertical at the frame edge for the whole shot. Lean it 8-20 deg or let it enter from a corner.
- Lens 22 mm except hill_over (32) and camp_bank (30). Moves per the shot plan (6-10 %/s push or pull with a 40 px/s slide, or the snaps).

| preset | shots | frame | avoid | camera offset / object changes |
|---|---|---|---|---|
| hill_over | 1, 22 | The bridge at frame centre between two Scots' backs. Push in 9 %/s toward the bridge, slide left 35 px/s. s22: ride down the run path below the ledge | The dark spiky carpet filling more than 35 % (keep the push aimed at the bridge, not down). The castle rock taking the centre | Preset camera. For s22 start at the preset and move the lens down the slope behind the runners (it must clear the ledge edge by at least 0.5 m). Hide nothing |
| hill_eye | 3, 14, 16 | The five Scots across y 600-700, the grass-chewer s2 for the snap. Gorse lower right as fg | The black bars, the pink dome | **Hide `fg_generic_steel`, `fg_generic_wood` (both spears) and `fg_generic_r_heather`** (tested: magenta 13 → 4.4, dark 0.17 → 0.08). Add one spear at d 2.6 m, xp 690, tilt (-0.25, 0.1), so it leans in from the right edge. Optional: tilt down 3 deg to trade dark tree crowns for lit ground |
| hill_low | 6, 21 | Spears against the sky; the horn blower (`horn`) and Wallace (`w`) for s21 | Heads below 760; the fg spear crossing s3's head | Raise the look target 1.5 m (or tilt up 4 deg) so the heads go from 804-851 to about 700-760. Move the fg spear (in `fg_generic_steel`/`fg_generic_wood`) out of s3, or hide it and keep the gorse and rock. Blue 55 from the sky is accepted |
| bridge_deck | 2, 26 | The two knights side by side filling the deck, rails at knee height | Static sky: start the push already in motion | Preset. For s26 (the turn-back jam) add `place_troops(A, 'bridge', 6)` behind k1/k2 for depth |
| bridge_high | 8, 27 | The bridge full length, the loop beyond, the jam (troops by count) | **The orange post block** | **Hide `fg_generic_wood` and `fg_generic_*` (the post).** Use the pavilion at the lower left as the fg instead, or add one rail post at d 3 m, xp 30, with at most 50 px showing. Optional: drop to z 20 and push so the loop meadow takes less of the frame. Accept the wake strokes (small at push-in) |
| bridge_end_north | 15, 20, 23 | The bridge mouth with the column on the deck, the causeway, the spear-wall slot (y 27-29) | The black spear bar at left; heads in front of the bridge mouth | **Camera (-2.0, 50.0, 4.6) → look (0.0, 22.0, 1.8)** (tested at look z 1.2: everything reads; raise to 1.8 to bring the heads up to ≤ 760). **Hide `fg_generic_steel` and `fg_generic_wood`** (the spear). Keep the reeds and gorse (`fg_generic_g_*`) or add a reed clump at d 2 m, xp 60. Re-stage the placeholders. For s23 use `K.spear_wall(14, 2, rs)` across x -9..9 |
| bridge_end_south | 9 | The two knights wedged on the deck at the bridge mouth | Two full-height spear bars; 40 % empty sand | **Hide `fg_generic_steel` and `fg_generic_wood`.** Add one spear at d 2.4 m, xp 40, tilt (0.25, 0), entering from the lower-left corner. Start point (check the heads): camera (-2.0, -37.5, 2.6) → (0.0, -31.0, 2.6), so the deck fills the lower half. Snap push x1.4 on 17.37 |
| valley_wide | 4 | The loop and the bridge in the middle third; the castle rock at upper left | Ending the move on the near hill blob | Crane down + push toward the bridge/loop (64, 44). Start with the near hill in the lower right; by the end it should be at most 25 % of the frame. No changes |
| valley_loop | 17, 24 | The bottle: loop, bridge neck, the cork slot, the camp | Covering the neck with crowds | For s17 call `place_troops(A, 'meadow', n)` after deleting `crowd_*`. For s24 put a spear-wall block of at least 40x15 px at the north bridge end (`spear_wall`). Optional: one warm area light on the hill's shade face so the Scots line reads (lit tan, at least 3 px) |
| valley_river | 7 | The river band between the banks, the crag with the Scots | Head `e1` at cy 910 | **Move `e1` farther (d 9 m) or drop it**, so the head is at 760 or above. Push 7 %/s + slide. Reeds fg fine |
| camp_wide | 5, 13 | Parade knights past the pavilions, the river and the hill | Heads `k1` (cy 1109) and `k2` (cy 995) | **Move `k1`/`k2` to d 30-40 m (heads 700-760) or drop them**. Put the s13 laughing soldiers on the tent lane at x 150-450, d 25-35. Bias the slide left so the empty right-hand lawn leaves the frame |
| camp_table | 10, 28 | **FIX-FIRST: wait for the rebuild** | | |
| camp_bank | 11, 12, 18, 19, 25 | **FIX-FIRST: wait for the rebuild** | | |
| riverbank | 29, 30 | **FIX-FIRST: wait for the rebuild** | | |
| river_low | 31 | **FIX-FIRST: wait for the rebuild** (and the new `splash()`) | | |

## Re-check R2 (phase B)

Inputs:
- the 4 rebuilt tiles at full size
- `styleboard/phase_b_phone.jpg`
- `styleboard/splash_strip.jpg`
- QA_TEAM §G/§H
- API.md §9 / `grade()` VIVID

Own checks:
- sat/luma by the producer's measure (90x160, (max-min)/max)
- `stirling_hue` on the 4 tiles
- 3 drafts re-rendered with `STATE['vivid'] = (1, 1)`, so that VIVID candidates could be tried offline on the true base (river_low, riverbank, camp_table)
- one camp_table team-fix test (Cressingham's mark moved)

### Measured (final tiles as delivered)
| tile | VIVID now | sat | luma | blue | dark | black point p1 | note |
|---|---|---|---|---|---|---|---|
| camp_table | (0.9, 1.45) | 0.625 | 96.5 | 26.8 | 0.03 | 0.031 | |
| camp_bank | (1.52, 1.3) | 0.585 | 106.3 | 22.1 | 0.11 | 0.034 | |
| riverbank | (1.63, 1.59) | 0.506 | 97.7 | **67.3** | **0.25** | 0.016 | dusk look, navy hills |
| river_low | **(6.0, 1.04)** | 0.595 | 102.3 | 51.1 | **0.21** | **0.000** | night sky, green water |

Base without VIVID (draft):
- river_low: sat 0.27, luma 192. The frame is mostly pale sky, sand and white foam, so no sane (gamma, sat) pair reaches luma 110. Gamma 6 reaches it only by turning the scene into night.
- riverbank: sat 0.22, luma 143.
- camp_table: sat 0.47, luma 104. It barely needs a grade.

### How to apply §G (ruling for this set)
- §G's 0.47 / 85-110 is the producer's measure over the whole film (stats.py runs on the video), not a cap that every 1 s shot must hit by brute grading.
- **VIVID gamma may not exceed 1.9.** Above that, skies go navy, water goes green and the black point crushes to 0 (bible: p1 0.08-0.12).
- A bright exterior shot that cannot reach the band at gamma ≤ 1.9 is allowed up to luma 150 with sat ≥ 0.47. It is listed in the take's QA.md.
- The film mean is checked at FINAL. River_low (0.9 s) adds under 1 luma point to the film mean.

### Per tile
| tile | verdict | score | finding | fix (owner) |
|---|---|---|---|---|
| camp_bank | **PASS** | 7 (was 5) | Bridge about 38 px tall with piers, about 430 px long, 5 mounted pairs about 18-20 px. The centre pole is gone. The far Scots read as a dotted line under the crag. Warm. Still open: the lower 45 % spike grass and the rainbow-streaked far hill (VIVID exaggerates the terrain mottling). **New §G breach:** the fg banner pole at x 640-720 runs behind Surrey's head (cx 640): a pole through a face | Team note: Surrey to cx 560-580, or nudge the camera 0.3 m left so the pole sits at x ≥ 680. Extras e1-e3 (heads cy 502-522) stay below the deck line (head top ≥ 480). VIVID stays (1.52, 1.3); optionally (1.4, 1.25) if the far hill stripes look loud |
| riverbank | **PASS** (geometry) | 6 (was 4) | The water now runs along the right half at the marks' feet, the bridge and the camp are in the background, the splash lands 3-6 m out. Colour: blue 67, dark 0.25, p1 0.016, navy hills. That is VIVID (1.63, 1.59) crushing a dusky base. The fg dark spike shards at lower left read as black teeth | Team: **VIVID (1.5, 1.6)** (base-tested: sat 0.48, luma 103, less crush). Pitch down 4-5 deg so the sky is ≤ 25 % (cuts blue). Hide the near dark reed/spike clump at x 0-250, y 900-1280 if it reads as black shards (`fg_generic_g_reed`, `fg_generic_g_cattail`). For shot 29 call `splash(..., age=-1)` (no splash); the default build stages splashes |
| camp_table | **FIX (small builder patch; not a launch blocker)** | 5 (was 4) | The chest (open lid, iron bands) and the scale now read at phone size: the props job is done. But (a) **Cressingham is hidden behind the open chest lid** (head cx 360). Tested: moving his mark +0.35 m right clears the lid, but then **the left scale pan crosses his face** (a §G bar-through-face). There is no gap at centre. (b) The striped rug, in the canopy's shadow, is a grey-violet slab over the bottom 25-30 %. (c) The canopy takes the top 20 %. This is acceptable for shot 28 (empty table) | Builder: (1) move the chest 0.3 m left and the scale 0.35 m right along the table so Cressingham has a clear 0.9 m slot at centre: head cx 330-400, cy 470-540, with no lid edge or pan within 25 px of the head. (2) Rug: shorten it to 1.2 m deep and pull it under the table front, or move it into the sun. Warm red/gold, not violet; the bottom 25 % shows lit worn grass + rug edge. (3) Raise the look target about 0.15 m so the canopy valance stays in the top 15 %. VIVID: **(1.05, 1.1)** (base sat 0.47/luma 104 → about 0.51/100). The current (0.9, 1.45) is oversaturated (vivid share 10 %, p1 0.03) |
| river_low | **FIX (small builder patch; not a launch blocker)** | 5 (was 4) | The splash shape is right now: spiked crown, droplets, ring, readable at ages 0.25-0.6 on the strip. Two problems: (a) the foam material shades pale blue (`foam` has `sm=(0.85, 1.0, 1.15)` + haze), so the spray reads as ice-blue. (b) The central column with its ball cap rises about 2x the crown height: a lollipop on every splash. VIVID (6.0, 1.04) = night sky, toxic green water, p1 0. Reject | Builder: (1) **give `splash()` its own `spray` material**: white `#f6f8fb`, emission-mixed so that lit and shade differ by ≤ 15 %, no blue shade tint, no haze; displayed V ≥ 0.92 after VIVID. (2) **Column**: at most 1.2x the crown height, tapered (0.22 → 0.06 m), and replace the ball cap with 3-5 small droplets breaking off. (3) Preset VIVID **(1.8, 1.3)** (base-tested: sat about 0.52, luma about 150; accepted bright exterior per the ruling above). Set `over['foam_k'] = 0.6` for river_low to shrink the blown-white near-bank band (white share 4.2 %). If the water still reads green, use gamma 1.6 (sat 0.49) |

### §G checks on the 4 tiles (nothing floats, wide, faces)
- All cards stand on the ground with contact shadows; nothing hangs in the sky.
- No face is over 35 % of the frame height (the largest is camp_bank Cressingham, head 160 px = 12.5 %, card about 35 %).
- Bars through faces:
  - camp_bank pole vs Surrey (note above)
  - camp_table pan vs Cressingham if he is moved without the builder patch
- Cut by the frame edge: riverbank e4 (cx 42) is half-cut at the left edge → move to xp 90 or drop.

### §H 3 "rich and detailed?": **YES**
The valley build has:
- dense life: the camp with 19 pavilions plus tents, banners that flutter, smoke, horse lines, parade knights, troops by count on the bridge, causeway and meadow, a 90-figure Scots line
- layered depth on every ground preset: fg props, mid cast, far hill, castle rock
- textured surfaces: plank grain, crag faces, fields with hedges
- warm key against blue-violet shade

Weak spots (notes, not blockers):
- spike-grass ground planes in camp_bank, riverbank and the hill tiles
- the bare yellow loop meadow in bridge_high (fill it with `place_troops('meadow')` when the story allows)

### BIGZOOM feasibility (shots 1 and 24)
- Both start in a valley preset (farms, Scots line, troops) and end on a ground preset whose fg dressing, vegetation and marks are built around that preset's camera. A single valley build has no near-camera grass, reeds or camp_fg at the end point.
- Team method until a builder helper exists:
  - build the end preset (camp_bank for 24; hill_eye/hill_low for 1) and call the valley extras into it: `farms`, `scots_line`, `place_troops`
  - OR render the swoop in two builds with a matched camera path and a hand-off frame high above the river (at 40-60 m, where no near vegetation is in frame), with a 3-frame cross-fade
- QA-art judges at the TAKE gate whether the move reads as one continuous move. The end frame must match the camp_bank tile (Cressingham and Surrey 35-60 % of frame height, the bridge visible).

### FINAL SET verdict: **PASS-WITH-NOTES. Wave-2 takes s04, s07, s09 and s11 may launch now.**
The two builder patches (camp_table centre slot + rug; `splash()` spray material, column and the river_low VIVID/foam values) are small, take about 30 min, and do not change any API signature. Until they land:

| take | presets | start now | waits for patch |
|---|---|---|---|
| s04 | camp_table, camp_bank | camp_bank shots, camp_table camera/move blocking | camp_table final frames with Cressingham (shot 10) |
| s07 | camp_bank | all (Surrey off the pole) | — |
| s09 | valley_loop → camp_bank BIGZOOM, bridge_end_north | all (BIGZOOM per the method above; bridge_end_north per the R1 offset notes) | — |
| s11 | camp_table, riverbank, river_low | camp_table shot 28 (empty table: the current tile works; use VIVID (1.05, 1.1)), riverbank shot 29 | final frames of shots 30-31 (splashes) |

If the patch is late, the s04 fallback is: move `scale_stand*` and `scale_beam*` objects +0.4 m along the table, stage `cress` at the table centre +0.2 m, and pull the camera back 0.4 m. Check that no pan or lid edge is within 25 px of his head.

Re-check after the patch: camp_table with and without Cressingham, plus the splash strip at ages 0.1-0.9 in river_low with the new VIVID. Phone sheet only.
