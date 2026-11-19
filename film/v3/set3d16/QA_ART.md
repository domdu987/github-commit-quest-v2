# QA-art — SET gate, film 16 (ไอ้บ้าลวด), set3d16

Reviewer: QA-art (opus). Inputs: contact.jpg (27 tiles), every final in telegraph_work/final/ at full 720x1280, a 360x640 phone sheet of all 27 tiles,
styleboard/board.jpg (client-approved), film16/shot_plan.md, analysis/sheets (rail_0 etc.), set3d10/contact_small.jpg.
Placeholder actors ignored for look; judged only for size, placement and readability.

## Verdict: **FIX-FIRST**

The CHAMBER is close to the board and almost ready to ship. The STUDIO is clean but sparse. The LINE is the problem, and it carries 20 of the 30 shots.
It holds the hook image, the trench reveal, the pulse reveal and the train race, and in these tiles **none of those four key images reads yet**, even at full size,
and less on a phone:
- the bottle neck reads as a teal plunger cap;
- the pulse is two flat white discs beside the wire;
- the trench cut-away looks like a blue water-slide;
- line_trench shows neither the plough nor the mules;
- line_wagon shows no bottles;
- rain is missing in 2 of the 3 RAIN tiles.

Fix these and re-shoot the sheet before any render team starts.

## Scores (1-10)

| Category | LINE | STUDIO | CHAMBER |
|---|---|---|---|
| Set density / ornament | 6 | 5 | 8 |
| Lighting & colour (warm practicals, complementary colour, depth through light) | 6 | 7 | 6 |
| Composition / framing (shows the set, subject readable, phone legibility) | 4 | 5 | 5 |
| Character staging (placeholders: size, position, eye-room for the beat) | 4 | 6 | 5 |
| Key moment clarity & beauty (hook / reveal / ending) | **3** | 6 | 6 |
| Overall match to board + references | 5 | 6 | 7 |
| **Location mean** | **4.7** | **5.8** | **6.2** |

**Film-level set score: 5.2 / 10.** Set3d10 at the same gate was about 7.5: dense, foreground-rich harbour, consistent sky, reads at phone size.

## Global issues (all LINE presets)

1. **Sky "halo ring".** A hard, bright orange-yellow arc crosses the sky in every outdoor tile: L01-L04 at y≈700, L06/L15 at y≈250, L16 at y≈200.
   - It reads as a rainbow, or as a render artefact. The board sky is a smooth vertical gradient (blue top, warm low band at the horizon).
   - Fix: replace the radial or sun-centred sky ramp with a vertical gradient that peaks 0-60 px above the horizon line.
   - In low-angle cams (line_close), keep the warm band below the frame's lower third.
2. **Empty sky / ceiling in the top 30-40 %.**
   - Outdoors (L01-L04, L06, L15, L16), about 35 % of the frame is plain gradient. Add 2-3 board-style cumulus clouds in the upper third, larger and flatter-lit.
   - Indoors (S02-S04, C03-C05, C07), the ceiling eats the top 25-35 %. Tilt the cams down 4-6°, or lower the cam 0.3 D, so the chandelier or beams sit at y≈80-200 and no more.
3. **Steam smoke is one white sphere** (L05-L09). It reads as a light bulb on the chimney, which is the exact "snowman blob" the client rejected in film 10 (§9).
   - Replace it with a trailing plume of 6-9 overlapping puffs that shrink and cool from white to lavender. Lay it back along the train's motion, as in the board LINE panel (puff chain).
4. **Grass is over-saturated and too dense in the foreground.**
   - In L05, L08-L10 and L15 the yellow blades clip to pure #FFFF00. They fill the lower 40 % and hide the actors.
   - Fix: drop grass emission/saturation by about 25 %.
   - Thin the foreground blades to 3-5 deliberate tufts at 1-2 D from the lens (the §10 rule wants foreground props, not a wall).
5. **The lead pipe is a saturated blue/white candy tube everywhere** (L05-L16). The story says *grey lead pipe*.
   - Use a dull grey metal (≈#7a7d84, rough 0.5) with a warm sun highlight. Blue belongs to the leak sparks only, so the sparks must be the only blue-cyan glow in the LINE.
6. **Blue-violet shade.** It is correct in L02, L05, L06, L11 and L14. hue_report flags L01, L03, L04, L08, L09 and L10 (shade 186-218 or 268).
   - Retint the ground fill and sky-shade in AFTER_RAIN and RAIN toward 245, and in line_rail DAY toward 240, to stay inside the 240-260 rule.

## Per-preset fixes

### LINE

**line_close (L01 AFTER_RAIN, L02 DAY, L03 RAIN, L04 pulse) — shots 1, 20, 23, 24. HOOK + REVEAL. Score 3.**
- The bottle neck is about 45 px wide and opaque teal. On a phone it is about 20 px and reads as a pole cap.
  - Make it **2x larger**, so the neck at the pole top is about 90 px wide in the frame.
  - Model the recognisable beer-bottle shoulder and lip, and make it **transparent green glass**: transmission 0.8, IOR 1.45, tint #3fae5a.
  - Add a hard specular **glint**, a small sun-sparkle star of 6-10 px, on the neck in DAY and AFTER_RAIN. "It glints" is in the plan.
  - Keep the neck at y 330-420 so it sits well above the caption band.
- The wire must visibly **drape over the glass neck**: a loop wrapped once around the neck under the lip.
  - Today it leaves the side of the cap at the pole's left. The rhyme in shot 23 and the "does not leak" beat both depend on the wire touching the glass.
- The ladder and the pole form an A-frame: the ladder top touches the pole top, the ladder foot is 2 m away, and Morse floats beside the pole.
  - Lean the ladder **against** the pole (foot ≤ 1.0 m from the pole base). Put Morse's mark on the top rungs with his hands at the neck.
- Cut the foreground grass to **3 blades** (one dark L, two R) and lower them so no blade crosses the pole or the bottle.
  - Today 12+ dark blades cut across the pole in the lower half and read as scratches on a phone.
- Lift the camera about 1.0 D, or reduce the tilt-up 8°, so the treeline/fence sits at y≈1050 and the bottle at y≈350 (better use of the sky).
- **L03 RAIN:**
  - **No rain is visible.** Add streak particles over the whole frame: 150-250 thin streaks, 30-60 px long, 25 % opacity, slight slant.
  - Darken the pole to a wet value (−35 % albedo, add specular).
  - The sparks are 4 round cyan blobs about 40 px across. Make them smaller (12-18 px) and more numerous (8-12), crawling *down* the pole into a puddle at the base, with a small blue light on the puddle.
- **L04 pulse:**
  - The pulse is two flat, semi-transparent white-cyan **discs** floating left of the wire, off the wire path. On a phone they read as lens flares.
  - Make it a bead *on* the wire: a 14-18 px hot core plus a 40 px glow, plus a 120-200 px comet trail along the wire's curve.
  - At the hero frame, park it **on the glass neck**, with a cyan rim-glow inside the glass. The pole wood below stays dark (no spark): that is the reveal.
  - Add a variant tile with the bead just past the neck.

**line_wide (L05 DAY, L06 DUSK, L07 RAIN) — shots 2, 19. Score 5.**
- The bottle row "marching to the horizon" is barely readable: the necks are 8-15 px.
  - Bring the near pole to x≈560-640 and enlarge it, with its neck about 40 px.
  - Line up 8+ poles diminishing to the vanishing point. Raise the camera 0.5 D so the row is not lost in the grass.
- Morse is missing at the ladder foot (shot 2). Add a stand mark at the near pole base, head at y≈560.
- The large plain orange disc (pole stump or table top) in the lower right (x 450-720, y 900-1280) is a dead shape. Replace it with a crate + spool + coil group.
- Smoke: see global #3.
- **L07 RAIN:** rain exists only as 12 long, perfectly vertical white lines in the upper-left quarter (they read as scratches).
  - Spread the streaks over the full frame and shorten them (see the L03 spec).
  - Add a darker overcast gradient. Keep the warm band at the horizon, as the board does, so the frame is not all grey-violet.

**line_rail (L08 DAY, L09 pulse) — shots 3, 25, 27. Score 4.**
- **L09 is identical to L08: the pulse at 0.2 is off-frame.** The race (shot 25) has no image yet.
  - Choose a pulse parameter that puts the bead in frame on the near span (x 200-500, y 100-300), with a long trail.
  - Make a race variant with the train **moving**: wheel blur is not allowed (no blur rule), so show it with rods, pistons and a slanted plume.
- The train is parked mid-frame, small (about 300 px), behind the fence.
  - Bring it 30 % closer, or move the cam to the rail side, so the loco fills about 45 % of the width in shot 25.
- No **station platform** for shot 27. The red buildings read as barns.
  - Add a plank platform with an edge, a station sign board with no text (a blank sign is fine), lamp posts and benches, and 4-6 waving placeholder slots.
- The foreground is 45 % grass and nothing else. Replace it with 1-2 props at 1-2 D (crate, rail spike keg) plus 3-5 tufts.
- Birds on the wire: nice, keep them.

**line_trench (L10 DAY) — shot 13. Score 2.**
- **No plough or mule team reads.** Only a plough handle is visible, about 40 px, behind the grass; there are no mules and no furrow.
  - Re-aim the cam at the plough: a low side tracking view, plough + 2 mules filling about 50 % of the width, at y 600-850.
  - Show the open brown furrow and the grey pipe unrolling from a drum into it.
- The foreground crate (x 0-380, y 850-1280) is cut by the frame and blocks a quarter of the frame. Move it to the corner, 1.5 D, about 20 % of the frame.

**line_trench_high (L11 DAY→DUSK) — shot 14. Score 5.**
- The DAY→DUSK mix is lovely. But the furrow is read only as a thin blue stripe (the pipe) beside the track.
  - Make the furrow a **dark-brown open earth stripe** 2-3x the pipe's width, with a light spoil ridge.
  - The plough team must be visible at the head of the furrow (tiny at the highest snap is fine; it must be in frame at all three heights).
- Check all 3 snap heights as tiles. Only one was rendered.

**line_trench_end (L12 DUSK, L13 RAIN) — shots 15, 17, 21. Score 4.**
- The tree canopy is a near-black mass over the top 45 % of the frame and kills the dusk sky.
  - Move the tree 3 m back and to the right, or crop the cam left, so the sky band shows behind the actors' heads.
- The test key and register on the crate are about 60 px and unreadable. Shot 15 is about pressing the key.
  - Push the cam in, or scale the key station 1.5x, with the brass catching a warm rim light.
  - Place the coil and crate at 1-2 D in the foreground, not the hammer handle at the centre.
- Shot 21 puts the key on the **wagon**. Either add a wagon tail behind the key or change the plan line; it must match line_wagon.
- **L13 RAIN:** **no rain streaks at all**; only the puddle says rain. Add the streak spec, wet sheen on the crates and coil, and drip rings in the puddle.
- The actors stand in a row facing the camera. Give the worker marks a lean-in toward the key (heads converging on it).

**trench_cut (L14 DUSK) — shot 16. REVEAL. Score 3.**
- The idea is good: there is a spiral wire wrap inside the pipe. But it reads as a **blue water-slide or ditch seen from the inside**, not a cut-away of the ground.
  - Make it a true section: the camera looks at a cut **face of soil**, dark brown and damp with pebbles and roots, and the pipe sits embedded in that face.
  - Show grass and the furrow surface on top, with the dusk sky as a thin band above.
- The bright yellow plank across the top (y 320-380, full width) is a hard flat bar that splits the frame. Remove it, or make it a dark timber, half width.
- The pipe is saturated blue. Make it grey lead (global #5).
- Show the **split** clearly at the hero position (frame centre, y 600-750):
  - a peeled-open lead seam, about 150 px long;
  - torn cloth wrapping in a light cream colour, so it reads against the grey;
  - the copper wire visible inside;
  - 10-15 small blue sparks leaking *into* the damp soil, with a faint cyan light on the soil.
- Today the sparks are a cluster at the vanishing point, about 100 px, and invisible on a phone.

**line_road (L15 DUSK) — shot 18. Score 3.**
- The buggy does not read: no mule shows, and the mocker stands on a red cart in front of a red barn (red on red).
  - Move the barn out of frame, or re-colour the cart dark green/black. Show the mule head and ears plus the shafts on the left.
  - Seat the mocker *in* the buggy, leaning out, at a low angle. The foreground would be the furrow edge with the pipe.
- The yellow barrel on the right edge (x 560-720) is pure saturated yellow and pulls the eye. Darken it or remove it.
- About 35 % of the top is sky with the halo arc. Add clouds and the furrow line leading to the buggy.

**line_wagon (L16 AFTER_RAIN) — shot 22, "the answer is glass". Score 3.**
- **No bottles are visible.** The bottle crate is hidden behind the wagon side board from this low angle.
  - Raise the cam 1.2 D, or lower the wagon side boards. Put the crate of green bottles in the frame centre-left with 15 necks clearly visible and a glint on each.
  - Morse lifts one bottle at about y 450-550 against the bright after-rain sky.
- The wagon body is a dark, flat brown box. Add a warm sun rim on its top edges and wet sheen.
- Halo arc in the sky (global #1).

### STUDIO

**studio_wide (S01) — shot 4. Score 6.**
- Warm, clean, and the window light patch on the carpet is good.
- Too bare for "canvases, frames, plaster busts":
  - add 3-4 canvases leaning on the back wall;
  - add 2 more framed paintings on the walls;
  - add a plaster bust on a plinth;
  - add a drape over a chair.
- The view outside the window is a cluster of hard-edged blocky houses that read as a 2D cutout. Soften it and push it back (aerial perspective) so it reads as outside.

**studio_easel (S02) — shot 5. Score 5.**
- There are no paint jars or brushes in the foreground (plan: "slide past paint jars in FG"), and the wife's oval portrait is not in frame.
  - Put the side table with jars, brushes and the oval portrait at 1-1.5 D, lower-left (x 0-300, y 900-1280).
- The ceiling takes the top 28 %. Tilt down 5°.

**studio_door (S03) — shot 6. Score 6.**
- The palette on the floor reads well (yellow disc with colour dabs).
- There is a white slab at the left edge (x 0-40, y 950-1280), probably a canvas edge, clipped by the lens. Remove it or bring it fully into frame.
- The stool for "he sinks onto a stool" is not in frame. Add it at Morse's right.
- The messenger mark overlaps Morse's head. Separate the two marks by 0.5 m.

**studio_window (S04) — shot 7. Score 5.**
- Outside should be "a long road to the horizon". Today it is a narrow street of townhouses. Re-dress it: a road vanishing to a low horizon, with fields.
- The coil of copper wire and the horseshoe magnet are not on set. Add them on the sill or table at hand height, and a blue spark light rig.
- Morse is small, at the centre of an empty room (head about 60 px). Push in 25 % for the snap push.
- The ceiling takes the top 30 %.

### CHAMBER

**chamber_wide_high (C01 DAY, C02 NIGHT) — shots 8, 11. Score 7.**
- Dense, gilt and crimson, a good match to the board. The C02 night candles are warm and lovely.
- The **sun shafts are hard-edged translucent slabs**. On the left and right tiers they read as glass panes and wash the desks to beige, and one slab cuts across the front table.
  - Use a soft volumetric falloff, or lower the opacity to about 35 %.
  - Keep the shafts off the telegraph table.
- The tiers are empty. Shot 11 needs "the whole chamber laughs". Provide 12-20 congressman marks in the tiers (placeholders) in the gate tile.
- Morse at the table is about 30 px tall (about 15 px on a phone). For shot 8 that is fine as a crane start, but the crane must end closer.
- C02: Morse at the door is invisible; the door is about 20 px. That is fine for the wide, but the ending is staged at chamber_table (see C07).

**chamber_low (C03 DAY, C04 NIGHT) — shots 9, 10, 28. Score 3.**
- **C03 is the weakest interior tile.**
  - A giant translucent sun-shaft slab crosses the right half of the frame diagonally and washes it out.
  - The mail sacks are big beige egg or potato shapes that read as boulders.
  - The globe is cropped at the right edge.
  - The mocker's head is half hidden behind a sack.
  - The ceiling takes the top 35 %.
- Fixes:
  - Remove the slab from this cam.
  - Make the sacks canvas mail sacks with a cinched neck, a rope tie, a stencil band (no text) and letters spilling out. Group them low, *around* the mocker, not in front of him.
  - Lower the cam to desk height with the **inkwell + quill** at 1 D, lower-left (plan, shot 9).
  - Put the mocker's head at y 450-600 with clear sky-wall behind it.
  - Drop the globe, or move it fully into frame.
- **C04 NIGHT** is cold blue-grey and dim, not candle-warm. Add warm practicals (desk candles, wall sconces lit) and lift ambient warmth.

**chamber_table (C05 DAY, C06 money, C07 NIGHT) — shots 12, 26, 29, 30. Score 6.**
- C05 is the best tile in the set:
  - the register is clear;
  - the tape with dots and dashes reads on a phone;
  - the floor coil of tape is good.
- Two things on C05:
  - The slab shaft on the right again washes the tiers. Soften it.
  - The tape seems to emerge from the mocker mark. Move the mocker mark 0.8 m right, behind the table.
- **C06 money bag:** the bag is a smooth brown gourd/pot with a knob. It does not read as money.
  - Use a cloth sack with a gathered, tied neck, a slumped bottom and 4-6 gold coins spilling on the green cloth. No "$" text is needed.
  - Add a bounce-squash variant.
  - The mocker should be visible in the background, arms folded.
- **C07 NIGHT ending (shot 30):**
  - The room is still lit almost like day: the white ceiling is bright.
  - Kill the ambient to about 15 % and let the **candle in the mocker's hand** plus the chandelier be the key light, with a warm pool around the stool and a falloff to dark tiers.
  - The mocker on the stool is cut by the left frame edge (x 0-90). Bring him to x≈200-300, head y≈500.
  - **Morse peeking at the door is not in frame.** The ending gag needs it. Re-aim so the rostrum door (lit doorway, warm crack of light) is visible at the upper right, with Morse's mark in it.
  - The tape pile round his boots: good, keep it.

## Phone (360x640) legibility — what fails

| Item | Today on the phone | Must be |
|---|---|---|
| Bottle neck (L01-L04) | ~20 px teal cap | ≥ 40 px green glass with glint |
| Pulse bead (L04, L09) | 2 pale discs / absent | bright bead on the wire + trail, ≥ 10 px core |
| Trench split (L14) | ~50 px cyan cluster at the vanishing point | ≥ 75 px split + sparks at the centre |
| Plough + mules (L10) | absent | team ≥ 50 % of the width |
| Bottle crate (L16) | absent | ≥ 10 necks visible |
| Rain (L03, L13) | absent | full-frame streaks |
| Key on crate (L12) | ~30 px | ≥ 60 px brass |
| Money bag (C06) | reads as a pot | sack + coins |
| Morse at the door (C07) | absent | lit doorway, head ≥ 25 px |
| Register tape (C05) | reads | keep |

## Top 8 fixes (priority order)

1. **line_close bottle insulator.**
   - Make it 2x, in transparent green glass with a sun glint, the neck at y≈350.
   - Drape the wire *over* the neck.
   - Lean the ladder against the pole.
   - Cut the foreground grass to 3 blades.
2. **Pulse bead (L04/L09).** A hot bead *on* the wire with a comet trail. Park it on the glass neck for the reveal tile (dark pole below), and put it in frame in line_rail for the race.
3. **trench_cut.**
   - Make it a true soil cut-face, with grey lead pipe split open, cream torn cloth and copper wire.
   - Put the sparks at the frame centre, leaking into damp brown soil.
   - Remove the yellow bar across the top.
4. **line_trench / line_trench_high.** Re-aim on the plough + 2 mules, with an open brown furrow and the pipe unrolling. The furrow must read at all 3 snap heights.
5. **Rain + sky.**
   - Add full-frame rain streaks in all RAIN tiles (L03, L07, L13).
   - Remove the orange halo arc from every outdoor sky.
   - Add board-style clouds in the empty top third.
6. **Steam plume.** Replace the single white sphere with a trailing chain of shrinking puffs. Also add the station platform and a closer, moving train for line_rail.
7. **chamber_low.**
   - Remove the shaft slab.
   - Make real mail sacks grouped behind the mocker, with the inkwell + quill in the foreground.
   - Warm the night with candles.
   - In all chamber cams, soften the sun-shaft slabs to soft volumetrics and keep them off the table and the tiers.
8. **The ending and the money: chamber_table NIGHT + money bag.**
   - Use real night: candle-key light, dark tiers, the mocker in frame at x≈250, and Morse visible in the lit doorway.
   - Make the money bag a tied cloth sack with spilled coins.
   - Also on line_wagon and line_road: raise the cam so the crate of green bottles reads, and fix the buggy (mule visible, no red-on-red).

Secondary fixes, not blocking alone:
- Grass saturation −25 %.
- Lead pipe grey everywhere.
- Ceilings to ≤ 20 % of the frame.
- Studio dressing (canvases, busts, the jars FG, the wire coil + magnet, a road outside the window).
- Fix the hue_report CHECK tiles toward shade 240-260.

---

# Re-check (after fix round 1, commit 1727aeb)

Inputs:
- contact.jpg. It holds **30 tiles**, not 31: make_contact.py lists 30 and telegraph_work/final has 30 PNGs. L05 bottle_macro is new.
- Every final at 720x1280.
- A fresh 360x640 phone sheet of all 30 tiles.
- styleboard/board.jpg and film16/shot_plan.md.

The cyan line at y≈880 on the contact sheet is the caption-band guide. It is not in the finals (checked the pixels), so it is fine.
Placeholder actors are again judged only for size, placement and readability.

## Verdict: **FIX-FIRST** (short list: 6 blocking items, mostly small)

This is a real step up. The hook is now strong:
- the green glass neck with a star glint;
- the ladder leaning against the pole;
- clean foreground;
- board-style clouds;
- the halo arc is gone.

The chamber night is now warm and candle-lit. The bottle row reads to the horizon.

What still fails is the **reveal chain**:
- the pulse reads as a string of fairy lights;
- trench_cut reads as an icicle cave over a glossy floor;
- "the answer is glass" shows opaque green crayons in shadow.

The grey lead pipe is still candy blue/white. These are set assets, so a camera move in the takes cannot fix them.

## Scores (1-10), first review → re-check

| Category | LINE | STUDIO | CHAMBER |
|---|---|---|---|
| Set density / ornament | 6 → 7 | 5 → 6 | 8 → 8 |
| Lighting & colour | 6 → 6 | 7 → 7 | 6 → 7 |
| Composition / framing (incl. phone) | 4 → 5 | 5 → 6 | 5 → 6 |
| Character staging (placeholder marks) | 4 → 5 | 6 → 6 | 5 → 6 |
| Key moment clarity & beauty | 3 → 5 | 6 → 6 | 6 → 6 |
| Overall match to board + references | 5 → 6 | 6 → 6 | 7 → 7 |
| **Location mean** | 4.7 → **5.7** | 5.8 → **6.2** | 6.2 → **6.7** |

**Film-level set score: 6.0 / 10** (was 5.2). Inside LINE the spread is wide:
- line_close: 8 (L01/L02 are near the board's CLOSE panel);
- line_wide: 7;
- trench_cut: 3;
- line_rail: 4;
- line_wagon: 4.

## Status of the first review's fixes

| First-review item | Status |
|---|---|
| Bottle neck 2x, green glass, glint (L01-L04) | **FIXED.** Reads on the phone (about 35 px with the star). |
| Wire drapes over the neck | Fixed enough. The wire meets the neck top; the take's push will sell it. |
| Ladder leaned against the pole; FG grass on line_close | **FIXED.** |
| Sky halo arc; empty top third | **FIXED.** The gradient is smooth and the clouds read as board cumulus. A few are egg-shaped single blobs (L09, L11, L18), a minor issue. |
| Rain in L03/L07(now L08)/L13(now L16) | **FIXED.** Full-frame streaks. They are still 100 % white and dense (L03 reads as a shower spray fanning from the top). See the non-blocking list. |
| Pole sparks crawl down the wet pole (L03) | **FIXED.** 7 small cyan beads down the pole. Good. |
| Pulse = a bead *on* the wire + trail; parked on the glass | **NOT FIXED.** See B1. |
| Steam plume (single sphere) | Improved. It is now a tapering column. It is vertical, not laid back along the motion: the take can lean it. |
| Grass saturation / density | Fixed in line_wide and line_close. **Not fixed** in L18 line_road (see the non-blocking list). |
| Lead pipe grey | **NOT FIXED.** See B5. |
| line_rail: pulse in frame, closer train | **NOT FIXED.** See B4. |
| Station platform (shot 27) | Partly. A white station house sits at the rail with the train in. There is still no platform edge, lamp posts, benches or waving slots, and 50 % of the frame is empty ground. Non-blocking (shot 27 is 1.3 s). |
| line_trench: plough + mules | Improved. 2 mules, the plough beam and the drum reel show, but the team is about 20 % of the width, behind the Cornell mark. Camera matter. |
| trench_high: furrow at all 3 heights | Improved. 3 snap tiles exist and the team shows in all 3 (tiny in snap 3). The furrow is still mostly the blue/white pipe line, not a brown earth trench. It follows B5. |
| trench_end: canopy, key size, rain | **FIXED** (sky shows, the key station reads at about 100 px, rain is there). The "wagon" in the label is a grey shed box. Make it a wagon tail, or change the shot 21 line. |
| trench_cut: true soil section | **NOT FIXED.** See B2. |
| line_road: red on red, mule, barrel | Fixed: green buggy, white house, no barrel. The mule is only a rump at the right edge, and a wall of foreground grass is back. Non-blocking (camera). |
| line_wagon: bottles visible | Partly. A crate shows, but see B3. |
| Studio: jars/brushes FG, oval portrait, stool, messenger separated | **FIXED** in S02/S03. |
| Studio: dressing, road outside, coil + magnet | Partly or not fixed. S04 still shows blue hills and houses with no road. The coil, magnet and spark are under 20 px on the sill and invisible on the phone. |
| Chamber shafts | **FIXED.** Soft beams in C01; the slab is gone in C03-C06. |
| Congressmen in the tiers (C01) | **FIXED.** |
| chamber_low sacks, inkwell + quill FG | Improved. The sacks have tied necks and spilled letters. Remaining problems: the quill is a 400 px beige paddle, one sack under the table reads as a boulder, and the globe is still cut at the right edge. |
| C04 night warmth | n/a. C04 is now the mail-sack DAY tile. The NIGHT look is proven in C02/C07. |
| Money bag | Improved. It reads as a tied cloth sack, but there are **no coins**, so it reads as "a sack" rather than "money". Non-blocking: the narration carries it. Coins are still advised. |
| C07 night ending | Mostly fixed. Candle-warm, dark tiers, the mocker on the stool at x≈250, the tape pile round the stool: lovely. **Morse in the doorway is still not visible.** See B6. |

## BLOCKING: must fix before the client sees the set (asset, light or mark changes; no camera move can fix these)

**B1. Pulse look (L04, L05; shots 24, 25). REVEAL.**
- Today set_pulse draws about 7 separate spheres, spaced 40-90 px apart at full size.
- In L05 they are 90 px cream-white discs; on the phone they read as ping-pong balls or fairy lights on a string, not current.
- In L04 one disc floats left of the neck, off the wire.
- Fix:
  - Use one hot core (cyan-white, 16-20 px at line_close and 30-40 px in the macro) with a **continuous tapered trail** along the wire curve.
  - Build the trail from 20-30 lags at a small spacing, shrinking and fading to the wire, so it merges into one comet.
  - Use cyan, not cream.
  - At the L05 hero position add the cyan rim-glow inside the glass. Keep the pole wood below darker than in L01 (the "does not leak" read).

**B2. trench_cut (L17; shot 16). REVEAL.**
- The top third is good: the soil face with pebbles and the dusk sky band.
- But the bottom 40 % is a dark **glossy reflective floor** with soft light blobs. It reads as an interior or ice, not soil.
- The torn cloth is a row of white triangular **teeth or icicles**.
- The sparks are cyan **rings or donuts** that read as UI bubbles.
- On the phone, the frame reads as a shark mouth or a cave.
- Fix:
  - Make the lower frame damp brown soil: rough 0.8, no mirror spec, a few pebbles and roots.
  - Make the pipe grey lead with a peeled seam.
  - Make the cloth ragged cream strips hanging *from the seam* (irregular, not a row of equal triangles), with the copper wire clearly orange inside.
  - Make the sparks solid small cores (no ring) leaking down into the soil, with a faint cyan light on the soil.

**B3. line_wagon (L19; shot 22, "the answer is glass").**
- The crate holds about 12 **opaque solid-green cylinders** with no glass and no glint, and the whole wagon sits in blue-violet shade.
- It reads as crayons in a dull box. This beat has a snap push on "แก้ว" (glass), so the glass must sparkle.
- Fix:
  - Use the same glass material as the line_close neck, with a star glint on 3-5 necks.
  - Put the crate in the sun with a warm rim on the wagon's top edges and wet sheen.
  - Move it off the big spool so Morse's mark has clear after-rain sky behind his raised hand. Today the spool sits behind his head.

**B4. line_rail (L09; shots 3, 25).**
- The train is **not in the tile**: only a grey cylinder end shows at the left edge (x 0-60).
- The pulse is a 6 px dot at the right edge.
- The lower 45 % is flat, empty yellow ground.
- Fix: re-shoot the tile with set_train placing the loco at about 45 % of the width, with the plume, and the pulse bead (per B1) on the near span ahead of it.
- Also put one foreground prop at 1-2 D (crate or keg).
- This is cheap (hooks plus one prop), but the race image must be proven before the client OK.

**B5. Lead pipe material (L11-L16, L18, L17).**
- It is still a saturated blue/white candy stripe (snaps) or pure blue (trench_end).
- The story says grey lead, and blue must be kept for the sparks alone, or the leak reveal loses its colour logic.
- Fix: one material, dull grey metal ≈#7a7d84, rough 0.5, with a warm highlight.
- In the same pass, make the open furrow beside it read as **dark-brown earth**: today the trench is read only through the pipe.

**B6. C07 ending: Morse at the door (shot 30).**
- The lit doorway is in frame (good), but it is empty.
- Morse's mark (head y 607, 31 px) sits behind the register/instrument, below the door.
- Fix: move the mark into the doorway (head about y 480, ≥ 50 px at full size, so ≥ 25 px on the phone), half-hidden by the door leaf.
- This is a key-shot gag; QA-art must pass it at the TAKE gate anyway.

## NON-BLOCKING: render workers handle these by camera, framing or staging in their takes (set fixes welcome but not required)

- **L18 line_road.**
  - Raise the cam about 0.5 D, or start the move above the grass, so no blade crosses the buggy wheels. Today the foreground blades fill the lower 45 %.
  - Re-aim right so the mule head and ears show.
  - Trimming the 3-4 nearest blades in the set is a 1-line fix and is advised.
- **Chamber ceilings (C03-C06) and studio ceilings (S01-S04).**
  - The ceiling takes 25-35 % and is near-white overexposed in C03/C04. Tilt down 4-6°, as asked in the first review.
  - C03/C04 also have a hot light patch on the bare floor in the lower third; frame it out or put the FG table lower.
  - Optional set tweak: lower the ceiling emission/exposure by about 30 %.
- **C03/C04 props.**
  - Halve the quill: today it reads as a paddle.
  - Keep the globe out of frame.
  - These are small set edits; if not done, frame the quill partly out.
- **L11 line_trench.** Push in and lower toward the team so the mules and plough fill about 50 % of the width; the mules exist now.
- **L10 station.** Push in on the platform side; stage the waving cast across the empty foreground.
- **L06/L07 line_wide.** The Morse mark at the ladder foot is not visible; stage him at the near pole in shot 2. Lean the steam plume back along the motion in the take.
- **Rain (L03, L08, L16).** Streak opacity is about 100 % and the streaks are long. 30-40 % opacity is advised, so the bottle and pole stay the subject in shot 20. The pure #0000ff-blue puddles (L08, L16) would look better dark and reflective.
- **S04 studio_window.**
  - The coil, magnet and spark are tiny. The snap push on "พริบตา" must end close on the sill.
  - Scale the coil and magnet 2x and the spark 2x if the set is touched anyway.
  - The road outside is still missing; frame the window as light.
- **C06.** Add 4-6 coins on the cloth if the set is touched; otherwise the push on the sack plus the narration carries the beat.
- **L15 coil.** The foreground coil reads as a brown tyre or cake. Frame it partly out, or give it rope or wire texture.
- **hue_report CHECK.** L02, L03, L09, L10, L11, L12, L14, L17 and L18 are outside 240-260; L02 is at 289.6. This is QA-tech's call; the shade tint can move with the B5 pass.

## Phone (360x640) re-check

| Item | First review | Now on the phone |
|---|---|---|
| Bottle neck (line_close) | 20 px teal cap | **reads**: about 35 px green glass + star |
| Pulse (L04/L05) | pale discs | **fails**: a chain of beads / ping-pong balls (B1) |
| Trench split (L17) | 50 px cluster | **fails**: reads as teeth and rings over a glossy floor (B2) |
| Plough + mules (L11) | absent | weak: visible, about 20 % of the width |
| Bottle crate (L19) | absent | **fails as glass**: a green block, no glint (B3) |
| Rain (L03, L08, L16) | absent | **reads** (too strong) |
| Key on crate (L15) | 30 px | **reads**: about 50 px |
| Train in line_rail (L09) | small | **absent** (B4) |
| Money bag (C06) | a pot | reads as a sack; no coins |
| Morse at the door (C07) | absent | **absent** (B6); the doorway itself reads |
| Register tape (C05/C07) | reads | reads, lovely in C07 |

After B1-B6, re-render only these tiles: L04, L05, L09, L11-L19 and C07. If the B-items land as specified, I expect SHIP at about 7.
