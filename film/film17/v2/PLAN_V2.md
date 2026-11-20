# Film 17 v2 plan: "ไอ้ช่างวัดหู" remake (PREP ONLY, remake not yet confirmed)

Status: plan only. Nothing rendered, no sessions, no commits. Written 2026-11-20 against the client rules on
`origin/claude/new-session-73ou27` (`film/QA_TEAM.md` sections G, H, I; `film/ref_shorts/`).

**Kept exactly from v1:**
- narration.wav (placed at +0.10 s) and script_th.txt
- captions.json (STT-retimed, FINAL_AUDIO_R2 PASS), timing.json, music and SFX beds
- the sentence table and the quote windows
- end frame: g 2052 = 68.40 s, hard cut on "ตัวเอง"
- frame rule: t = narration time, film time = t + 0.10, g = round(film time × 30)

**What changes:** the picture only. We go from 27 cut shots (sat 0.384, brown/navy, extreme close-ups, the same office
angle again and again) to 8 long travelling takes, 7 hard cuts, 2 BIGZOOMs, cobalt and gaslight amber.

---

## 1. Reference findings (R1-R7, sheets at 1 frame / 2 s, numbers from README / qa_stats2.py)

**R1 crash** (38 cuts / 60 s, sat 0.29, luma 108)
- Sunny prairie road, then a stormy night with headlights in fog. Ride-along inside the sheriff's car.
- Low-angle road shots. The signature is a red neon arrow sign, "DON'T HIT THIS TREE".
- The outlier: copy only the ride-along and the night headlights, NOT the cut rate.

**R2 pachinko** (4 cuts, sat 0.52, vivid 54 %, luma 89)
- Purple/pink neon alley with wet reflections. A long one-point dolly down the red-stool pachinko aisle.
- Warm amber prize counter, then cold blue alley. Signs: PRIZE HALL, PRIZE COUNTER, THANK YOU.
- Moves between places by dissolving through a doorway.

**R3 job nobody wants** (1 cut, sat 0.44, luma 135)
- The camera follows the boss walking through the office and pushes through the "CAREER DEVELOPMENT ROOM" door.
- A push into the wall clock carries the time jump (transition detail).
- Green walls, cobalt carpet, yellow sun shafts. The end is a blue night with lamp-lit interiors and a crane down the tower.

**R4 grave bell** (6 cuts, sat 0.52, vivid 55 %, luma 112)
- Deep blue snowy night, amber lit windows, lanterns and a candle in the bedroom: warm pools in cold blue.
- Cutaway cross-section of the grave. Slow push-ins. Purple/violet interiors.

**R5 storm oil** (11 cuts, sat 0.65, vivid 75 %, luma 111)
- Camera orbits the deck, cranes up and off the ship to the open storm, then swoops onto the pirate ship.
- Pushes through a porthole into the galley.
- Signature: storm blue, yellow oil and a red hull. God rays. A galley lamp is the key light.

**R6 pink cell** (~10 real cuts, sat 0.37, luma 140)
- A hot-pink cell against a cold grey-blue cell block, with hard sun shafts through barred windows.
- An aerial swoop from the sky over the fields down to the prison. Signs: P-618, POD C.

**R7 coaster** (2 cuts, sat 0.48, vivid 48 %, luma 106)
- Ride-along on the coaster car, extreme wide park shots down to the character.
- Moonlit night with string lights, then a sunny day. Signature: blue sky, green grass, red car. Signs: GRAND OPENING, FIRST!.

**Techniques we copy (8):**
1. Follow a walking character through connected rooms and push THROUGH a labelled door into the next scene (R3).
2. Crane up and out from the character to the whole town, then swoop back down on the next beat (R5, R6).
3. Push through an object as the transition, so it is never a cut: window, door, clock face, drawer, card (R3 clock, R5 porthole).
4. Pools of light: amber practicals inside a deep-blue world, with wet street reflections (R2, R4).
5. Visible light shafts with dust: window sun in the measuring room, skylight shafts in the archive (R3, R6).
6. One-point symmetric dolly down a long aisle. Our archive hall is the "pachinko aisle" (R2, R6 cell block).
7. One dominant colour field with a complementary accent: cobalt plus amber, red as the accent (R5 blue/yellow/red, R2 purple).
8. Short sharp signs that say where we are, and close-ups only as ~1 s pushes on punch lines (R2, R3, R6).

---

## 2. Signature colour: "Préfecture cobalt + gaslight amber", red kepis as accent

**Palette (base albedo before light):**

| colour | hex | used on |
|---|---|---|
| Préfecture cobalt | `#1F4FD0` | dusk sky, corridor walls, measuring-room ceiling and dado, archive vault, door paint |
| gaslight amber | `#FFA62B` | every practical light (lamps, windows, card lamp), drawer fronts (honey `#D9822B`), measuring-room upper walls (ochre `#E8A33A`) |
| kepi red | `#D7262E` | kepi bands, awnings, sign banners, the runner border, the GRAND banner, the "MARTIN" card tab |

Red is the accent only, never more than about 10 % of a frame.

**Banned as large areas:** brown wainscot, navy-black ceilings, cream/grey stone and paper walls, peach haze.
- Stone gets warm ochre `#D9B07A` and is lit amber/blue.
- Paper piles stay small.

**Targets (film/qa_stats2.py, blocking at TAKE and FINAL):**
- mean saturation ≥ 0.50 (v1: 0.384)
- vivid % ≥ 45 (v1: 22)
- mean luma 85-110
- no single take below sat 0.47

How qa_stats2 measures: frames scaled to 90×160 at 30 fps; per-pixel sat = (max-min)/max; vivid % = the share of pixels with sat > 0.5.
So large mid-bright cobalt and amber fields count. Black, white and grey count against us.

**Grade:**
- `grade()` saturation 1.05 → 1.20.
- Add a vibrance lift on the 0.25-0.5 band. Do not push already-vivid pixels.
- Shadows keep the painted blue-violet (SHADE hue 230-250).
- Check `bertillon_hue.py` and `qa_stats2.py` on the set contact sheet BEFORE any take is rendered (SET gate).

**Lighting recipe per location:** every frame needs a visible motivated key, a rim on every character, and warm + cool in frame.

| location | motivated key (warm) | cool fill / counter | rim on cast | new preset |
|---|---|---|---|---|
| Paris street, dusk | 16 gas street lamps (amber pools on wet setts), the Préfecture door glow, wagon lantern | cobalt sky dome (zenith `#1A3FB8`, a thin amber horizon), blue SHADE | cool sky-blue rim from behind; amber rim when the cast passes a lamp | `BLUE_HOUR_EXT` (from DUSK_EXT: sun_k 0.35, lamp_k 1.6, windows 70 % lit) |
| façade → corridor | wall gas brackets every 2.5 m, so the travelling camera crosses amber/blue bands | cobalt walls; blue transom light from the street | warm rim from the lamp ahead of the walker | `GASLIGHT_INT` |
| measuring room | low amber sun through the open French window: hard shaft + dust over the chair and bench; 2 gasoliers | blue sky bounce from the window, blue shade on the cobalt dado | warm rim from the window (camera on the room side); cool rim from the corridor door | `SUNSET_INT` (DAY_INT with an amber sun and a 30 % higher sky fill) |
| archive hall, day | 5 skylight shafts (pale blue-white) with dust, banker lamps (amber) on desks | cobalt vault and gallery ironwork | amber rim from the desk lamps | `ARCHIVE_DAY` |
| archive hall, night (false payoff) | ONE banker lamp + candle on Bertillon's desk; amber gasoliers at 40 % | moonlight-blue skylight shafts | moon rim (blue) | `ARCHIVE_NIGHT` (keep luma ≥ 85: lift the cobalt walls, do not crush) |
| reveal at the GRAND bank | amber spot on the drawer and box (`box_lamp`), the green banker lamp | hall in cobalt half-light | warm rim from the drawer lamp | `ARCHIVE_DAY` + `box_lamp` 2× |

`stage_cast` rim: on for every member (today only bertillon, prefect and inspector17). Add `rim_col` = warm or cool per preset.

---

## 3. Set upgrade spec: one connected world `prefecture17`

**One Blender scene, one coordinate frame** (today `build()` makes a new scene per location).
- Units are metres. Street floor z 0. Interior floor z 1.2: a raised ground floor, 5 steps inside the door.
- **Street:** today's `street`, carriageway along +y. The Préfecture façade replaces `station` and sits on the plane x = 6.0, facing −x.
- **Measuring room:** today's `measure`, moved by (+9.2, +12.0, +1.2). Its left (window) wall lies IN the façade at x 6.0; the window is world y 12-14.4, z 3.15-4.6.
- **Corridor:** x 6.0-16.0, y 4.0-7.4. It runs from the main door (façade, y 4.6-6.8) along the front of the measuring room.
- **Archive hall:** x 13.0-21.0, y 2-34, vault 9 m. The measuring-room right-wall door (world x 12.4, y 9.0-10.2) opens through a 0.6 m passage into it.
- **Reveal assembly:** today's `reveal` (big drawer, `box`, hero card) is built INTO the GRAND bank of the hall at y ≈ 26, west wall.

Every location reaches the next without a cut. Takes switch off what they cannot see (`world_build(take)` visibility sets).

### 3a. Paris street at dusk (+ the rooftop plate for BIGZOOM 1)

**Exists:** setts, kerbs, 2×5 Haussmann blocks, mansards/dormers/chimneys, shopfronts with blank awnings, 12 lamps, wagon (no horse), puddles, chimney smoke, dusk sky.

**Add:**
- **Rooftop plate** `paris_roofscape(r=220)`: low-poly mansard blocks with chimney pots and 30 smoke sources, lit amber windows (60 %) and zinc roofs in cobalt light.
  - The Seine strip with amber lamp reflections.
  - Notre-Dame towers as a far silhouette (Île de la Cité = the Préfecture's real neighbour). **No Eiffel Tower** (built 1887-89).
- Horse (black, low-poly or a cast card on a stand) in the wagon shafts, with a breath puff.
- Crowd (6-10 cards):
  - flâneurs with umbrellas, a newspaper boy waving papers, a lamplighter on a ladder lighting a lamp (life)
  - 2 gendarmes at the door, a fiacre cab passing
- Pigeons on the sills, a café terrace with an awning, a Morris column with posters (short readable text allowed).
- Tricolour flags on the façade (cloth sim or a sine-keyed bend).

**Layers (street_wide travelling):**

| layer | content |
|---|---|
| foreground | lamp post, barrels, flower cart, café chairs (1-2 m from the lens) |
| mid | wagon + horse, thief, gendarmes, steps |
| far | façade, roofs, smoke, Notre-Dame |

**Push-through:** the measuring-room French window (BIGZOOM 1 in; the pivot pulls back out).

### 3b. Préfecture façade → door → corridor (new)

**Façade** `prefecture_facade(B)`:
- 3 storeys + mansard, ochre ashlar, cobalt shutters.
- Arched main door with double doors: hook `set_door('main', 0..1)`.
- **Sign "PRÉFECTURE DE POLICE":** gold letters on a cobalt band over the door, a lit lantern each side.
- A sentry box with a gendarme, steps, the open French window of the measuring room (no bars), other windows lit with silhouettes.

**Corridor** `corridor(B)` (10 × 3.4 m, ceiling 4.5):
- Cobalt walls, red/ochre floor tiles, gas brackets every 2.5 m.
- **Photo-card walls floor to ceiling** with a sign "PHOTOGRAPHIES — SÛRETÉ". 80,000 photos is the fact; instance 2,000 small cards.
- A clerk on a rolling ladder, paper piles, a bench with 3 waiting prisoners, a gendarme with a ledger.
- Doors with signs: **SERVICE D'IDENTIFICATION** (the measuring room; new door in its front wall, world x 9.8-10.8), **ARCHIVES** (far end), **CABINET DU PRÉFET**.

**Push-through:** main door (T2 start), the SERVICE D'IDENTIFICATION door (T2 middle).

**Layers:**

| layer | content |
|---|---|
| foreground | bench end, photo pile, umbrella stand |
| mid | thief + gendarme |
| far | the door signs, lamp pools |

### 3c. Measuring room "SERVICE D'IDENTIFICATION" (exists, upgrade)

**Exists:** chair + head rest on a dais, tripod camera, toise, arm-span scale, foot board, calipers, clerk table + green lamp, bench, coat rack with kepis, stove + smoke, wall clock + pendulum, 2 gasoliers, notices, crates.

**Change and add:**
- Repaint: upper walls ochre `#E8A33A`, dado cobalt (was crimson-brown), ceiling cobalt with honey beams, floor saturated oak `#B5531F`, rug cobalt with a red border.
- The barred window becomes an open French casement (hook `set_window`), so BIGZOOM 1 can enter.
- Sign **SERVICE D'IDENTIFICATION** inside, above the corridor door.
- A wall chart **"11 MESURES"** with 11 drawn pictograms (head, finger, foot, arm, ear ...), 1.2 × 1.6 m, readable at 3 m.
- A wall calendar with a big page "3 MOIS", hook `set_calendar(page)`.
- The archive door becomes a double door with **ARCHIVES →** above it.

**Life:**
- 4 prisoners on the bench (flinch cycle), 2 gendarmes, the photographer clerk under the hood
- pigeons on the window sill, stove smoke, pendulum, dust in the sun shaft

**Layers:**

| layer | content |
|---|---|
| foreground | kepi rack, tripod, ledger stack (1-2 m) |
| mid | chair group |
| far | toise, arm-span scale, chart, window light |

**Push-through:** French window (T1), corridor door (T2), the wall clock face (T3 → T4 match), the archive door (T4).

### 3d. Archive hall "ARCHIVES" (new, grows from `records` + `reveal`)

**Size:** 30 m long, 8 m wide, 9 m barrel vault in cobalt, 5 skylights with shaft prisms + dust.

**Cabinets:** two storeys of honey-amber card cabinets (existing `cabinet_wall`, 2 rows stacked). A cast-iron gallery at 4.2 m with a red-painted rail and a spiral stair. 3 rolling ladders.

**Signs and labels (readable on a phone):**
- Big **ARCHIVES** over the entry.
- Hanging section banners **PETIT** (blue), **MOYEN** (amber), **GRAND** (red), one per third of the hall.
- Drawer labels by size: the PETIT drawers are small (0.30 × 0.20), MOYEN 0.45 × 0.25, GRAND 0.90 × 0.40 (the `big` drawer).
- Labels show "PETIT / MOYEN / GRAND", plus number ranges in the hero row.

**Hero assembly:** the `reveal` set (big drawer `big`, `box`, `box2`, hero card, calipers, lamp table) embedded in the GRAND bank at y ≈ 26.

**Life:**
- 4 clerk cards pushing card trolleys, clerks on the gallery
- falling cards, pigeons in the vault, gasoliers flickering, dust in the shafts

**Story props:**
- Bertillon's desk under the GRAND banner: banker lamp, candle, a card fan.
- Overflow piles for "2 months".
- A chalk tally board "RÉCIDIVISTES 1884" on the gallery rail, hook `set_tally(n)` 0 → 241.

**Layers:**

| layer | content |
|---|---|
| foreground | gallery rail, ladder rungs, drawer edges, a card trolley |
| mid | the group at the desk / GRAND bank |
| far | the canyon of drawers, skylight shafts, the ARCHIVES door |

**Push-through:** archive door (T4), between the gallery railings and past the chandelier (BIGZOOM 2), into the drawer and the box (reveal), the card.

### 3e. What to add to `bertillon.py` vs what exists

| exists (reuse as is) | add |
|---|---|
| `Batch`, materials, ink hull, `grade`, `render`, `key_life`, `set_flicker/smoke/dust/pendulum` | `world_build(take, light)`: all locations in one scene with offsets; per-take visibility and culling (> 45 m: no ink, low-poly) |
| `measure` room + its props, `cabinet_wall`, `rolling_ladder`, `drawer_assembly`, `card_box`, `card_plane`, `set_drawer/box_lid/card_lift/cards_fan` | `prefecture_facade`, `corridor`, `archive_hall` (2 storeys, gallery, spiral stair, banners), `paris_roofscape`, `horse`, `flag`, `pigeons`, `fiacre`, `kiosk` |
| `street` blocks, `police_wagon`, `street_lamp`, `puddles`, `mansard`, `paris_roofs` | `sign(B, text, w, h, fg, bg, font)`: PIL text texture from `film/fonts` (the no-text rule is lifted in QA §I.4); readable ≥ 28 px cap height at the take's nearest distance |
| light presets DAY_INT / EVENING_INT / DUSK_EXT | `BLUE_HOUR_EXT`, `GASLIGHT_INT`, `SUNSET_INT`, `ARCHIVE_DAY`, `ARCHIVE_NIGHT`, and `set_light_mix(a, b, t, frame)` for the in-take night → dawn shift (T5) |
| `camera()`, `project()`, `stand_report.py` | `cam_path(keys, ease)`: Catmull-Rom path + look-at path, per-frame keyed, lens 22 (18 allowed only in BIGZOOM starts); `cam_report.py` prints each segment's char % of frame height, the max face %, and the card-yaw angle per frame |
| `stage_cast` (billboard cards, rim, shadow proxy) | `stage_cast` v2: per-frame yaw clamp (§6), `walk_path(actor, keys)` with foot-locked cycles, `rim_col`, contact decal on stairs and steps |
| hero card texture (Dupont front + profile, bottle) | hero card v2: big readable name **MARTIN** in the name panel + the empty-bottle sketch + measurement rows that can glow (`set_card_rows(k)`) |
| | hooks `set_door(name)`, `set_window`, `set_calendar`, `set_tally`, `set_banner_sway` |

**Cast additions (cast17, small):**
- props `bottle` (empty glass bottle), `fake_moustache`, `stamp`, `photo_pair` (two big photo cards)
- 6-8 Parisian crowd extras by tinting earlier casts
- a Thai paper sign "ไอ้ช่างวัดหู" pinned on Bertillon's back (optional gag, T3)

---

## 4. New shot plan (same narration timeline, 0-68.40 s, g = round((t+0.10)·30), t = narration time)

**Hard cuts (7):** g 336, 651, 850, 1045, 1377, 1695, 1868, all on sentence starts. Inside a take, framing only travels.

**Size rule:**
- `%H` = character height as % of the 1280 px frame (1.7 m at d metres = 1330/d px).
- Wide / medium-wide ≤ 35 %H. Medium 35-60 %H.
- Faces ≤ 35 % everywhere except P1-P3.

**Angle tags:**

| tag | angle |
|---|---|
| HI | high / bird's-eye |
| LO | low hero |
| OTS | over-the-shoulder |
| FG | through a foreground frame |
| TD | top-down |
| TRK | side tracking |
| CR | crane up/down |

**Life and lip-sync:**
- All cast act with props in hand. Nobody holds still for more than 1.5 s.
- Lip-sync only in 16.32-21.59 and 37.48-39.74 (±0.15). The laugh is 15.46-16.32, with no lip-sync.

| seg | t0-t1 | g0-g1 | camera path (start → end, through what) | set / light | action (props) | tags |
|---|---|---|---|---|---|---|
| **T1** 1a | 0.00-3.40 | 0-105 | **BIGZOOM 1.** 45 m up over the roofs across the street (Bertillon 2 %H, a figure in the one amber-lit open window) → glide over chimney smoke, cross above the wagon and the lamps, through the French window → medium 45 %H on Bertillon closing the calipers on a seated prisoner's ear. Ease in-out, 3.4 s | roofscape, street, façade, measure / BLUE_HOUR_EXT outside, SUNSET_INT inside | lamplighter lights a lamp; Bertillon measures (calipers), prisoner_a stiff, eyes sideways | **BIGZOOM**, HI→FG |
| 1b | 3.40-4.85 | 105-148 | side track along the window bench, 45 %H: ear → next ear on "ทีละคน ทีละหู" | measure / SUNSET_INT, sun shaft + dust | Bertillon steps to prisoner_b, clamps the ear; each prisoner flinches | TRK |
| 1c | 4.85-7.17 | 148-218 | pull back out through the French window, crane up to 25 m: the whole street at dusk, **PRÉFECTURE DE POLICE** sign, roofs, Notre-Dame far (5 %H) | street / BLUE_HOUR_EXT | crowd strolls, flags move, wagon trots in (horse) | CR, HI (wide) |
| 1d | 7.17-9.47 | 218-287 | swoop down to the wagon at the steps, end medium-wide 30 %H, lamp post as fg | street | gendarmes pull prisoner_c out; he tips his cap, smirks, hands over a calling card "NOM: ???" | CR→FG |
| 1e | 9.47-11.10 | 287-336 | slow arc, eye-height on the steps, 30 %H | street | desk gendarme stamps "1ère FOIS" on the paper (light sentence); thief strolls up the steps through the door | TRK |
| **T2** 2a | 11.10-12.78 | 336-386 | **cut.** Behind the thief: push THROUGH the opening main doors into the corridor, 20-25 %H, photo walls both sides | façade → corridor / GASLIGHT_INT | gendarme swings the door; clerk on the ladder drops photo cards | FG, TRK (wide) |
| 2b | 12.78-14.72 | 386-445 | side track with the thief past the photo wall, medium-wide 30 %H | corridor | thief finds his own photo, slaps on a huge fake moustache; gendarme compares the photo with him, shrugs, waves him on | TRK |
| 2c | 14.72-16.32 | 445-493 | the thief walks out of frame; camera pushes through the **SERVICE D'IDENTIFICATION** door into the room, wide 25 %H, then a low drift | corridor → measure / SUNSET_INT | inspector, inside, sees Bertillon measuring an ear → laughs 15.46-16.32 (head back, belly bounce 3 Hz); gendarmes join | FG→LO |
| 2d | 16.32-19.66 | 493-593 | arc to OTS behind Bertillon's shoulder, inspector medium 50 %H (face ≤ 18 %) | measure | **lip-sync** "วัดหูโจรเนี่ยนะ! ...สักคน": points at the calipers, flicks them | OTS |
| 2e | 19.66-21.61 | 593-651 | slow low push, inspector 55 %H, kepi rack fg | measure | **lip-sync** "ข้าจะนั่งให้เอ็งวัดหูข้าเองเลย!": taps his own ear, chest out, thumb to chest | LO |
| **T3** 3a | 21.61-24.08 | 651-725 | **cut.** Bird's-eye from the gasolier (12-20 %H), slow rotate + crane down | measure | whole room laughs and points; a gendarme mimes calipers on his ear; prankster pins "ไอ้ช่างวัดหู" on Bertillon's back; Bertillon keeps measuring | HI/TD, CR |
| 3b | 24.08-26.30 | 725-792 | continue the crane down to eye height, wide 30 %H, door in the background | measure | room scatters back to work; prefect (top hat, sash) strides in, raises three fingers; calendar flips to "3 MOIS" | CR (wide) |
| 3c | 26.30-28.25 | 792-850 | low angle under the calipers table: prefect points at the door ("or quit") and leaves; Bertillon 50 %H tightens his pince-nez, grabs the calipers. The camera rises and pushes into the wall clock face (ends on the clock) | measure | pendulum swings; Bertillon determined | LO→FG(clock) |
| **T4** 4a | 28.25-29.97 | 850-902 | **cut (match on the clock face).** Pull out of the clock to medium-wide; the "11 MESURES" chart beside it | measure / SUNSET_INT | queue of prisoners; Bertillon seats one | FG (wide) |
| 4b | 29.97-32.27 | 902-971 | side track 1.2 m/s along the back-wall stations, 30-35 %H | measure | calipers on head → finger gauge → foot board → arm-span → ear (prisoner moved station to station, clerk writes) | TRK |
| 4c | 32.27-32.93 | 971-991 | track slows and dips low under the standing desk, 40 %H | measure | Bertillon writes the card (pen, card) | LO |
| 4d | 32.93-34.74 | 991-1045 | follow the card through the **ARCHIVES →** double door into the hall: drawers with PETIT / MOYEN / GRAND signs, 25 %H | measure → archive / ARCHIVE_DAY | he slides the card into a GRAND drawer, shuts it with his hip | FG, TRK (wide) |
| **T5** 5a | 34.74-36.92 | 1045-1111 | **cut.** Night. Crane down from the gallery rail (fg) onto Bertillon's desk, 15 → 30 %H | archive / ARCHIVE_NIGHT | drawers overflowing, candle low, Bertillon slumped, compares two cards, shakes his head | HI, CR (wide) |
| 5b | 36.92-39.76 | 1111-1196 | OTS from Bertillon's shoulder, push down the aisle to the inspector in the doorway, 45 %H | archive | **lip-sync 37.48-39.74** "เหลืออีกอาทิตย์เดียวนะ ไอ้ช่างวัดหู!": cupped hand; gendarmes snicker behind | OTS |
| 5c | 39.76-42.35 | 1196-1274 | dawn: skylight shafts fade in (`set_light_mix`, 15 f); side track with the escort down the aisle, 30 %H | archive / NIGHT → DAY | gendarme_a + _b march dupont (held) past the inspector, who smirks and follows | TRK (MW) |
| 5d | 42.35-44.72 | 1274-1345 | slow arc to a medium-wide three-shot at the desk under the GRAND banner, 35 %H | archive / ARCHIVE_DAY | dupont on the stool: innocent shrug, shakes his head, mouth closed; inspector grins at Bertillon | FG (desk lamp) |
| 5e | 44.72-45.80 | 1345-1377 | push to medium, 45 %H | archive | Bertillon closes the spreading calipers on dupont's head, reads, eyes narrow | eye→LO |
| **T6** 6a | 45.80-50.40 | 1377-1515 | **cut. BIGZOOM 2.** From the far end of the vault, 8.5 m up, d ≈ 27 m (group 4 %H, red kepis in the amber pool at the GRAND bank) → dive past the chandelier, between the gallery rails, past a rolling ladder → medium two-shot 45 %H. Ease in-out 4.6 s | archive / ARCHIVE_DAY + box_lamp | 45.81 Bertillon yanks the GRAND drawer (`set_drawer big`); 47.07 small calipers on dupont's finger; 47.89 one box glows, he lifts it; 48.77 calipers on his ear; 49.63 lid opens, one card rises (`set_card_lift`) | **BIGZOOM**, HI→FG |
| 6b | 50.40-51.40 | 1515-1545 | **P1** fast push onto the card in his hand (1 s) | archive | measurement rows tick and glow one by one: "ตรงกันทุกช่อง" | punctuation CU (card) |
| 6c | 51.40-53.77 | 1545-1616 | pull back to OTS over dupont's shoulder, 40 %H | archive | Bertillon turns the card: big **MARTIN** in the name panel on "มาร์แตง" (53.25) | OTS |
| 6d | 53.77-55.60 | 1616-1671 | drift to a wide three-shot, 30 %H | archive | dupont caught (eyes wide, sweat); gendarme pulls an empty bottle from his cape, holds it next to the card's bottle sketch | MW |
| 6e | 55.60-56.40 | 1671-1695 | **P2** fast push into the inspector's face (0.8 s) on "ขวดเปล่า" | archive | jaw drop (`inspector_shocked`), moustache droops | punctuation CU |
| **T7** 7a | 56.40-59.64 | 1695-1792 | **cut.** Low hero under the GRAND drawer, Bertillon 50 %H, dupont behind | archive / ARCHIVE_DAY | dupont slaps on the fake moustache (callback to 2b) and swaps caps; Bertillon just holds the card up and taps the calipers on it, rows glow: "กระดูกไม่เปลี่ยน" | LO |
| 7b | 59.64-62.15 | 1792-1868 | crane up and out to top-down over the whole hall (5 %H) | archive | drawers pop open along both walls, gendarmes march a line of thieves in, cards fly up; tally board on the gallery rolls 0 → 241 | CR, TD (wide) |
| **T8** 8a | 62.15-65.17 | 1868-1958 | **cut.** Bird's-eye over the measuring room, crane down through the gasolier ring, wide 25 %H | measure / SUNSET_INT | crowd of gendarmes and prisoners grinning around the chair; inspector red-faced (`flush17` 1), sitting stiff | HI, CR (wide) |
| 8b | 65.17-67.15 | 1958-2018 | arc to OTS behind the grinning crowd (shoulders fg), medium 45 %H | measure | Bertillon calmly opens the calipers and closes them on the inspector's ear; moustache twitches, eyes sideways | OTS, FG |
| 8c | 67.15-68.30 | 2018-2052 | **P3** fast push x1.4 on the jaws on the ear + red face (1.1 s), hard cut at the end | measure | the click; a crowd snort | punctuation CU |

**Checks against the rules:**

| rule | result |
|---|---|
| hard cuts | 7 (target 4-10, max 12) |
| takes | 8, length 3.2-11.1 s: T6 10.6 s, T1 11.1 s, T2 10.5 s, T5 11.06 s |
| BIGZOOM | 2: 1a 0.10-3.50 s film (g 0-105), 6a 45.90-50.50 s film (g 1377-1515), both extreme wide < 5 %H → medium 45 %H |
| angle types | 7 used: HI, LO, OTS, FG, TD, TRK, CR. No more than 2 consecutive segments at the same height and angle |
| close-ups | 3 punctuation pushes (P1 card, P2 jaw drop, P3 ear), each 0.8-1.1 s |
| wide or medium-wide | 17 of 32 segments, plus both BIGZOOM starts; every take opens wide or MW |
| faces | ≤ 35 % outside P1-P3 (medium 45-55 %H gives a head of about 14-18 %) |
| measuring room angles | high, low, OTS, side track, window. Never the same room angle 3 times in a row |

**Story beats from v1, all kept:**

| beat | where |
|---|---|
| hook | 1a-1b |
| Paris and fake names | 1c-1e |
| photo cards + moustache | 2a-2b |
| mockery with lip-sync | 2c-2e |
| nickname laugh | 3a |
| prefect's 3 months | 3b-3c |
| measuring montage | 4a-4c |
| drawers by size | 4d |
| 2 months, false payoff + shout | 5a-5b |
| Dupont brought in | 5c-5d |
| head → drawer, finger → box, ear → card | 5e-6a |
| card "Martin" + bottle | 6c-6e |
| bones don't change | 7a |
| 200+ caught | 7b |
| ending | 8a-8c |

**Sound (conform):** v1 cues at the new times, plus:
- the window whoosh (1a)
- the door creak and corridor murmur (2a, 2c)
- the clock tick push (3c-4a)
- the drawer slam (6a)
- the stamp thunk (1e)
- the tally chalk scratches (7b)

The SFX stay ≥ 16 dB under the voice.

---

## 5. Take split for render teams (6 handle frames each side; g = film frames)

| take | segs | g0-g1 (core) | render range with handles | frames | key shot (QA-art at TAKE) | main path |
|---|---|---|---|---|---|---|
| T1 hook + Paris | 1a-1e | 0-336 | 0-342 (no head handle) | 343 | yes (hook, BIGZOOM) | roofs → window → bench → out → street → steps |
| T2 corridor + mock | 2a-2e | 336-651 | 330-657 | 328 | lip-sync | main door → corridor → ID door → OTS |
| T3 nickname + prefect | 3a-3c | 651-850 | 645-856 | 212 | | gasolier → floor → clock |
| T4 montage + drawers | 4a-4d | 850-1045 | 844-1051 | 208 | | clock → stations → archive door |
| T5 false payoff + crisis | 5a-5e | 1045-1377 | 1039-1383 | 345 | yes (false payoff) | gallery → desk → aisle → desk |
| T6 reveal | 6a-6e | 1377-1695 | 1371-1701 | 331 | yes (reveal, BIGZOOM) | vault → GRAND bank → card → inspector |
| T7 aha + 200 | 7a-7b | 1695-1868 | 1689-1874 | 186 | | low → crane up top-down |
| T8 ending | 8a-8c | 1868-2052 | 1862-2052 (no tail handle) | 191 | yes (ending) | gasolier → chair → ear |
| **total** | | 2052 | | **2144** | | |

**Cost at the brief's ~45 s/frame (2 threads):**
- 2144 × 45 s = 96,480 s ≈ **26.8 CPU-hours**.
- Per take: T1/T5/T6/T2 about 4.1-4.3 h each; T3/T4/T7/T8 about 2.3-2.6 h each.

**Teams: 8 (one per take).** Wall time is about 4.3 h for one clean pass. Plan 2 fix rounds of about 30 % re-render, so about 7-8 h to the TAKE gate.
- Faster option: **11 teams**, splitting T1, T5 and T6 at a mid frame. Each half renders the same scene file and the same `cam_path` by frame range: T1 0-171 / 172-342, T5 1039-1211 / 1212-1383, T6 1371-1536 / 1537-1701. Wall time is about 2.3 h.

**Caution: the measured cost today is higher than 45 s/frame.** API.md §8 says 75-133 s/frame on 4 threads at 64 samples, and the connected world is heavier.
- To reach ~45 s on 2 threads we need: per-take visibility culling, low-poly far plate, 32 samples + OIDN, adaptive 0.03.
- At the SET gate, render 3 test frames per take (start, middle, BIGZOOM start) and re-budget.
- At 100 s/frame the total is about 60 CPU-hours: then use 11-16 teams.

**Order:**
1. Set build + SET gate (QA-art "rich and detailed?", hue/qa_stats2 on the contact sheet).
2. `cam_path` animatics at 360×640, 8 samples, all 8 takes. Director + QA-art check cuts, sizes, BIGZOOM %H, faces, card yaw.
3. Final renders.
4. TAKE gates.
5. Conform with the v1 audio.

---

## 6. Risks and mitigations

**1. Flat cards under a travelling camera** (orbits, OTS, BIGZOOM dives)
- **Risk:** a billboarded card visibly spins as the camera passes it, or reads paper-thin side-on.
- **Mitigations:**
  - `stage_cast` v2 clamps per-frame yaw to ±35° from the card's story facing. Past that, it swaps to the puppet's own `yaw` pose key (±0.6) or the mirrored pose on a cut-free frame where the card is small or occluded.
  - Paths keep the camera ≥ 1.2 m from any card and plan orbits ≤ 60° around a character.
  - `cam_report.py` flags any frame with a yaw rate > 2°/frame on a card above 15 %H.
  - OTS shoulders are near-camera cards facing away (back views exist in the puppet). Otherwise use a dark coat silhouette as fg.

**2. Grounding while travelling** (QA §G.2)
- Contact decal + shadow proxy on every card. Stairs and steps get per-step z.
- Walkers use `walk_path` with foot-lock, and the cast is never shown above the floor plane.
- Check the 0.5 s phone tiles at the TAKE gate.

**3. Long takes vs container restarts**
- Render frame by frame to `frames/gNNNN.png`, deterministically: every hook keyed per frame, seeds = frame.
- `--resume` skips frames that exist and are larger than 50 kB.
- Commit and push every 30 frames to `render17v2/teamN`, so a restart loses at most 30 frames (about 22 min).
- Keep the `.blend` build script plus `cam_path` JSON in git, never only the `.blend`.
- Split takes by frame range across teams if a session dies twice.

**4. Seams at the 7 cuts and the in-take transitions**
- Cuts sit on sentence starts and match v1's g (336, 651, 850, 1045, 1695, 1868; 1377 is new), so conform and captions stay the same.
- The clock match (T3 → T4) uses the same clock asset and screen position on both sides.
- `qa_auto.py --cuts 336,651,850,1045,1377,1695,1868 --first_g 0`.

**5. Colour targets missed** (sat ≥ 0.50, vivid ≥ 45 %)
- Measure the set contact sheet with qa_stats2 before rendering.
- Night archive (5a-5b) and bird's-eye shots (dark floors) are the weak spots: lift the cobalt walls, saturate the floor oak, keep amber pools large.
- The grade can add about +0.04 sat at most; never haze.

**6. Readability of the BIGZOOM starts** (character < 5 % but findable)
- Light the target window or bank as the brightest amber pool in frame; red kepis next to the character.
- Ease-in so the first 0.6 s are near-still.
- The blind viewer must still read the hook by 2.2 s (the narration names it). If not, start 1a at 18 %H of the roofscape instead of 2 %.

**7. Keeping the approved assets**
- Do not touch narration.wav, captions.json, timing.json, the music, SFX stems or `audio/sfx` (FINAL_AUDIO_R2 PASS).
- Keep cast17 (do not edit the poses; only ADD props and extras) and `bertillon.py` v1 presets (add `world_build` beside them).
- Keep the v1 render branches and gate/STATUS.md hashes as the fallback delivery.
- The hero card texture gets a v2 file (`card_bertillon_martin_v2.png`); the v1 file stays.

**8. Text signs**
- Short words only, French or Thai, rendered sharp: ≥ 28 px cap height at their nearest frame, no mip shimmer (test in the animatic).
- Spell-check against this plan: PRÉFECTURE DE POLICE, SERVICE D'IDENTIFICATION, ARCHIVES, PETIT, MOYEN, GRAND, MARTIN, 3 MOIS, 11 MESURES.

**9. Scope**
- The remake is not confirmed. Next step if confirmed: one set-build session (world + lights + signs + `cam_path` + `cam_report`) → SET gate → 8 animatics → teams.
