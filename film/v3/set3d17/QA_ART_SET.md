# QA-art (Opus, strict): SET gate, film 17 (set3d17 + cast17)

Date 2026-11-19. Per BRIEF.md "Client decision 2026-11-19", this verdict stands in for the client's approval of the set and cast. The sheets go to the client as FYI.

What I reviewed:
- All 20 full-res tiles in `contact_work/final/*.png` (720x1280) plus their `.json`, `contact.jpg`, `hue.md` and `API.md`.
- `cast17/sheet.jpg`, `stage_test*.png` and `cast17/API.md`.
- BRIEF.md, shot_plan.md (33 shots), QA_TEAM.md (incl. Stricter QA), the style-board review `styleboard/QA_ART.md`, and the approved `set3d10/contact.jpg`.
- My own measurements:
  - `qa_auto.py` magenta metric on every tile (R>180, B>180, G<80): **0.000 on all 20 tiles**;
  - head/chin positions from the tile `.json`;
  - zoom crops of the clock, calipers, card and drawer box.

## VERDICT: FIX-FIRST (short)

This is a beautiful set. The records-office canyon is the best location the series has built, and the light model now matches the series look. No DOF, no readable text, and the cast is strong.

Four things would visibly hurt the film:
- a black camera hood covers Bertillon in 6 shots;
- reveal step 2 (the box) cannot be read;
- the hero card does not show Dupont, and it has no bottle (shots 27-28);
- in measure_high, gas globes the size of heads float among the queue's heads.

All four are small, local fixes, about 60-75 min for a Sonnet builder including draft re-renders. Once they are in and re-checked (the acceptance numbers are below), rendering may start without a new full review. A QA-tech check of the re-rendered tiles is enough.

## Scores (1-10)

| area | score | note |
|---|---|---|
| Density | 7 | **Records 9**: thousands of drawers, pilasters, ladder, pulled drawers, desks, boxes, skylight shafts. **Reveal 7.** **Measure 6**: the instruments are all there, but the bottom 40 % of measure_wide is bare planks and measure_door is a bare wall plus door. **Street 6**: rich facades, but the lower half of street_wide is empty setts and there is no street life. |
| Light / colour | 8 | One hard warm key with crisp shadows. Shade is painted blue-violet (never brown). Terracotta-ochre walls over a dark wainscot, navy runner. Colours are pleasing and period. The hue-family "magenta" of 10-19 % is warm wood mixed with violet ambient, not true magenta: the qa_auto metric is 0 on every tile, so no take will FAIL on it. Shade 230-238 / 255-261 is visually still blue-violet. **Weak spot**: EVENING_INT does not read as evening (see fix 6). |
| Composition: measure | 6 | measure_chair is a strong hook frame. measure_low and measure_door are spoiled by the tripod hood. measure_high has lamp globes among the heads and a blown globe in the caption band. In measure_wide the chair head is only 32 px. |
| Composition: records | 8 | Off-centre canyon, foreground props, depth through light. Some marks sit in the caption band (see notes). |
| Composition: reveal | 6 | drawer_big and card_hero read. drawer_box does not: the box is a dim brown lump at the bottom of the drawer, and the light shaft hits the cards instead. The bottom 35 % of all three tiles is rug (caption band, acceptable). |
| Composition: street | 6 | Good dusk palette and lit windows. street_wide is a small subject over a big empty foreground. |
| Period credibility | 7 | Good: gasoliers with pipes, toise, arm-span scale, foot board, sliding calipers, tripod camera, Black Maria, mansards, frosted skylights. Problems: **the police wagon has shafts but no horse** (shots 4-5 "arrives", horse SFX). Some blue-grey slabs stick out of the street facades at odd angles. |
| Cast design / readability | 8 | Distinct silhouettes by hat (top hat / kepi / flat cap / derby / beret / bare head), 33 poses, 7 expressions, no text, and a good ending group. Risks: inspector17 vs gendarme_a are both navy kepi with a red band and a brown/black moustache. The inspector's "huge curled" moustache reads as normal at phone size and is no bigger than gendarme_b's. |
| Cast-on-set fit | 6 | The palette suits the terracotta walls. Weak spots: 14/33 marks have dark backdrops (black-coated Bertillon and the prefect in the records canyon); several staged marks are off-frame or below y 880; the cast's 2D `seat17="chair"` would double the 3D chair; heads are tiny in measure_wide. |
| Reveal clarity | 5 | The chain big drawer -> box -> card works in the 3D world, but step 2 is unreadable and step 3's card does not show Dupont or the bottle gag. After fixes 2-3, expected 8. |

## Style-board fixes (styleboard/QA_ART.md): were they applied?

| # | status |
|---|---|
| 1 | Yes. Light model: blue-violet shade by emission. p1 is 0.105-0.123 on 16/20 tiles. Dim pixels in 240-260 beat 0-45 on most tiles. |
| 2 | Yes. Terracotta-ochre walls, a 1.3 m dark wainscot and a navy ceiling; no pale planes. |
| 3 | Yes. Gradient sky, frosted skylights and mansard roofs. Vivid blue is under 1.5 % except records_desk at 3.0 %. |
| 4 | Yes. Matte surfaces, drawn plank textures and the ink hull. |
| 5 | Yes. All the instruments, a clock without numerals, kepis and gasoliers; the blue blocks are gone. |
| 6 | Yes. Pilasters, ladder, 14 pulled drawers, boxes, desk with a green lamp, off-centre camera, navy runner; the full reveal chain and a proper Bertillon card. |

## Hard-rule check

| rule | result |
|---|---|
| Sharp, no DOF | PASS |
| Wide, dense, lit 3D set | PASS (measure / street could be denser) |
| Warm key + blue-violet shade | PASS |
| No readable text | PASS. The clock has dot markers and hands only. Calipers have ticks only. Card, notices, ledgers and sign boards are greeked or blank. |
| Reveal inside the 3D world | PASS (clarity fixes below) |
| Heads above y 880 | PASS on the recommended marks. FAIL on records_aisle `aisle0` (head cy 910) and records_ladder `ladder_foot` (chin 945): see the notes. |

## FIX LIST for the builder (prioritised; ~75 min total; re-render only the touched tiles in draft, then final for the contact)

**P1: blocking**

1. **Tripod hood in measure_low and measure_door (shots 3, 6, 10, 17, 22, 33).**
   - **Problem.**
     - In `measure_low` the black hood of the camera on the tripod (prop at (0.95, 0.55)) fills the right-centre of the frame and hides the `clerk` mark, where Bertillon stands. Ring luma there is 66, and the head is half covered.
     - In `measure_door` the same hood is a dark slab over the left 25 % of the frame.
   - **Fix.** Do not move the tripod: that would break continuity with measure_wide and measure_chair.
     - `measure_low`: move the camera to about (0.3, 0.55, 0.5), with the look-at kept at (0.9, 2.4, 1.5). The tripod then lies behind and beside the lens. This also makes the shot tighter, which suits the ear inserts.
     - `measure_door`: turn the look-at to about (3.2, -2.9, 1.3), or slide the camera to about (-1.6, 0.2, 1.5). Keep the door and the kepi rack in frame.
   - **Acceptance.**
     - No tripod or hood pixels overlap any staged head or torso.
     - The hood covers at most 8 % of either frame.
     - `clerk` and `chair` heads have cy 450-760.
     - The foreground prop is still 1-2 units from the lens.

2. **Reveal step 2, `drawer_box` (shot 25): make the box the subject.**
   - Give the `box` card box a light ochre / cream body (V about 0.75) with a dark lid lining.
   - Lift it so its top sits flush with the drawer rim.
   - Add a small warm spot or point light (the lamp table's banker lamp, or a 0.3 m area light aimed at the box) so the box is the brightest non-emitter in frame. Keep the rest of the drawer about 25 % darker.
   - Move the sun shaft off the cards, or narrow it to the box.
   - Bring the camera in until the box spans at least 40 % of the frame width.
   - **Acceptance.** The box is at least 290 px wide at 720. Its mean luma is at least 1.4x the drawer interior. It reads as a box at 360x640.

3. **Hero card = Dupont, plus the bottle (shots 26-28): `bertillon_tex.py` card art AND `cast17.card_svg`.**
   - Draw both portrait frames as **Dupont without the cap**: ginger hair, stubble dots, a ruddy cheek and the red neckerchief at the collar line. One frame is front, one is a true side profile with a visible ear.
   - Replace the squiggle "name" line at the top right with a small drawn **empty bottle** icon in a framed name panel (outline glass, no label text).
   - Keep the hand, ear sketch and greeked rows.
   - Apply the same art to the cast `card` prop, so the 3D card (shot 26) and the held 2D card (shots 27-29) match.
   - **Acceptance.**
     - The ginger hair and the bottle can be told apart at 360x640 in card_hero.
     - No letters or digits anywhere.

4. **measure_high (shot 13): lamps vs heads.**
   - The second gasolier's white globes hang at the same screen height and size as the bench heads (bench0-3 at y 506-565), which confuses them at phone size.
   - The foreground gas-bracket globe is a blown white blob in the caption band (bottom right, y 990-1280).
   - **Fix.** For this preset:
     - raise the camera look-at about 0.4 or slide the camera about 0.6 toward +x, so the gasolier sits at least 1 head-D clear of every bench head;
     - swap the foreground prop for an unlit object (kepi on the coat rack, or the stool with ledgers), or move it so no emitter falls below y 880.
   - **Acceptance.** No emitter globe within 1.2 head radius of any staged head, and no bloom below y 880.

**P2: do if time remains (strongly recommended; each about 10-15 min)**

5. **Stage lists in PRESETS**: change the `stage` lists to marks that are in frame, with head cy 450-760 and chin < 880:
   - measure_wide: replace bench1/bench2 (off-frame) with in-frame bench or queue marks;
   - measure_high: queue0 (off-frame);
   - drawer_big: inspector (off-frame, chin 929);
   - records_desk: desk_stand (off-frame, overlapping);
   - records_aisle: aisle0 (head cy 910);
   - records_ladder: ladder_foot (chin 945);
   - measure_door: door_in and door_mid overlap (separate them by at least 1 head-D, or use door_out / queue1).

   Re-run `head_ring_luma` and list the in-band marks in API.md.
6. **EVENING_INT must read as evening** (shot 14 D11 "three months", shot 20 "two months later, candle low"). In records and measure:
   - skylight / window sky to dark navy `#2a2d5c` .. `#3c3a78`;
   - sun key down to 0.25x (or off);
   - lamp_k 2.5;
   - a warm pool radius about 1.2 m around the desk lamp and gas brackets.

   Acceptance: frame mean luma about 15-20 % below DAY_INT, with the skylights visibly dark.
7. **measure_wide near floor**: add 3-5 props in the empty lower 40 % (y -3.5..-1.5): a crate stack, coal scuttle, a second small rug, a stool with a kepi, a bucket. Keep a clear path to the chair. Target: no empty plank area larger than 25 % of the frame.

**P3: optional, otherwise handled in the takes**

8. A horse for the Black Maria (simple blocky dark-bay horse in the shafts, matte, inked), or the render notes below.
9. Two or three larger "long-head" drawer sizes in the records runs for shot 19 (small / medium / large).

## Notes for render teams (per preset; valid after the fixes)

**General**
- Use cast17 `seat17=None` on every seated pose inside the measuring room and on the bench: the set has its own 3D chair and bench, and the 2D chair would double it.
- Put a puppet `rim` (warm, about 0.5) on **bertillon, prefect and inspector17** whenever their mark has ring luma below 95: the records canyon, the toise corner and beside the wagon. Black coats otherwise sink into the brown cabinets.
- Inspector vs gendarme_a: keep them apart in frame and key the inspector's action. If cast17 allows, scale the inspector's `curl17` moustache about 1.3x so he reads at phone size.
- Run `key_life()` on every frame (flicker, dust, pendulum, smoke): it is the "life" the client asks for.
- Colour: the hue-family magenta of 10-19 % is expected in the records, reveal and street shots. qa_auto's magenta check measures 0. Do not grade it away.

**measure_chair**: hook (1), 11, 12, 16, 23, 28, 32
- The best frame. Chair head about 90 px, Bertillon at `clerk` big at right.
- The foreground calipers table is the hook prop. Use DAY_INT.

**measure_wide**: 2, 9, 18, **31 ending**
- The chair head is only 32 px at the preset camera. For **shot 31** start with the camera moved about 55 % of the way toward the chair (about (-0.4, -1.5, 1.5)), so the seated inspector's head is at least 70 px, and push in from there.
- Kepi-rack foreground: use the coat rack near the door, not the gas standard.
- Queue marks (shot 2): bench0/bench3, queue0/queue1 after fix 5.

**measure_low**: 3, 10, 17, 33
- Ear inserts (3, 33) need the camera at about 0.5-0.7 m from the head; frame shot 33 exactly like shot 3 (callback).
- The red crate/ledger stack foreground is very saturated. Keep it below y 880 only at the frame edge, or lower its saturation in the take if it competes with the captions.

**measure_door**: 6, 22
- Use `door_out` or `queue1` + `door_mid`; door frame foreground.
- Escort group spacing: `ESCORT_SPACING` 1.30 D.

**measure_high**: 13
- The whole room laughing. Heads are about 50-60 px; that is acceptable for one establishing shot, so keep the pull-out modest (7 %/s max).

**records_aisle**: 7, 19, 21, 30
- Do not stand anyone at `aisle0` (head below 880).
- For the doorway shout (21), put the inspector at the far end (aisle2/aisle_far) with a warm rim, and Bertillon near at `aisle1`.
- High-angle crane (30): pop cards on the pulled drawers p0..p7 / q0..q5.

**records_desk**: 8, 14, 20
- Shot 8 (two cards with the same face, one with a moustache): place two cast `card` props flat on the green baize next to the fanned cards. Use the cast card art, not new drawings.
- Prefect (14): stand him at `desk_clerk` or a new mark about 0.5 m left of `desk_stand`; `desk_stand` as staged is off-frame.
- Use EVENING_INT (after fix 6) for 14 and 20.

**records_low**: 15, 29
- Keep `low_a`, with a warm rim on Bertillon.
- The beard dissolve (29) happens on dupont, behind him. Give dupont a mark with ring luma at least 95, such as `wall_look` with the strip lights.

**records_ladder**: unplanned
- Use only `ladder_up`.

**drawer_big / drawer_box / card_hero**: 24-27
- Whip/snap between them (16 f).
- Key `set_drawer('big')`, `set_box_lid` and `set_card_lift` on every frame.
- No cast card in drawer_big at the preset: the `inspector` mark is off-frame.
- Shot 27 (card next to dupont's face): stage dupont at `pair_r` behind the card. Over-the-shoulder Bertillon at `pair_l`, with a rim on him.

**street_wide / street_wagon**: 4, 5
- DUSK_EXT only; street_wide DAY_INT is a comparison tile and is not to be used.
- Unless fix 8 is done, **do not show the wagon "arriving" from the front**: keep it parked, rear/side on (as in the presets), crop the shafts, and let the horse SFX carry it.
- Wagon marks have ring luma 55: give the cast a warm rim, or use `street_a-c` / `steps_top` (160).
- Shot 4 crane-down: start high on the mansards and lamps and end low with the lamp-post foreground, so the empty setts never fill the lower half.

## Not blocking (for the record)
- Shade hue 230-238 (measure_wide / measure_low / records_desk) and 255-261 (records_aisle).
- Blue share 9-10 % in measure_door / drawer_big / card_hero.
- p1 above 0.12 in a few tiles.

All of these are within visual tolerance. The look is clearly blue-violet in shade and warm in light.
