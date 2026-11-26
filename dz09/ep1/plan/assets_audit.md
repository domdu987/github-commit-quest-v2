# DEAD ZONE 09, EP.1 full episode: assets audit (production supervisor)

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`.
Written 2026-11-26 while the hook final render was running (4 workers, load average 5.2-5.6). Paper work only: nothing was rendered, no network call was made, nothing outside `ep1/plan/` was written.
Every number marked "measured" comes from a file named beside it. Everything marked "estimate" is a guess that must be measured on a 24-frame test before it is relied on.

## 0. The five numbers to remember

| | |
|---|---|
| New footage | 5:45 = 345 s = **8,280 frames** (scene sum 52 + 75 + 70 + 65 + 85 = 347 s = 8,328 frames) |
| Measured final cost (hook final in progress, 409 frames, `v10/film/out/final_720x1280/log_*.jsonl`) | **66.7 CPU s / frame at 100 %**, **38.8 at 75 %**; wall per worker 71.5 / 43.0 s (9 % over CPU because the machine is shared) |
| Recommended plan (option ii) | **110 CPU h = 30 wall h** of final render, **149 CPU h = 41 wall h** with a 35 % allowance; plus drafts 24 CPU h = 6.5 wall h per full pass |
| Missing assets | 7 set pieces (about 11 builder-days), 6 new characters or variants plus about 12 motion cycles (about 6-7 builder-days), about 130-155 shot modules |
| Source to back up | **6.9 MB** (435 files of code, docs, JSON, fonts, uploads) + 25 MB code-drawn textures + 126 MB audio (paid takes inside); the tree is 13 GB only because of 9.5 GB PNG and 3.2 GB EXR |

## 1. Sets

### 1.1 What exists

One location exists: the elevated expressway at night. It is a stack of four modules, each importing the one below read-only: `v4/set_expressway` (geometry, vehicles, textures) -> `v6/set` (beauty pass) -> `v9/set` (moonlit night) -> `v11/set` (reference-E finish, the film default). `v2/sets` and `v3/set3d` are a 1938 weather office from an earlier project and are of no use here.

| Group | Exists (module / function) |
|---|---|
| Deck | Path s -260..3000 D (straight to 420, then a 1500 D left curve): `expressway.build_deck`, `sweep`, `P(s, o, z)`, `heading(s)`. Two carriageways of 3 lanes + shoulder, median F-barrier with W-beam, outer F-barriers with rails, slab 2.4 D deep, piers every 50 D **down to a city floor at z = -30 D (18 m)**, expansion joints, drains. 1 D = 0.6 m |
| Road surface | `beauty.m_asphalt9` + `beauty.WET`: puddles, ripple rings from the frame number, cracks, ruts, lane paint; 1,300 glass shards, 180 wet leaves, skid arcs, 1,400 grit chips |
| Vehicles (`vehicles.py`) | `car(name, kind, ..., doors_open, crumple, crumple_door, hero, interior, broken_glass, tilt)` for sedan, taxi, hatch, pickup, SUV, van; `split_door`, `dent`, `crumple_front`, `add_interior` (two seats, bench, dash, RHD wheel), `hero_glass` (see-through cracked glass); `motorbike` (green delivery box); `rescue_truck` (white pickup, livery canopy, 2 red + 2 blue domes, flood mast; anchors `flood_head`, `tailgate`, `side_door`); `truck6` (6-wheel box truck, "mid / far detail"); `bus`; `cutter` (3D, 29 parts) |
| Gridlock | 19 individually built cars at s -10..95 (hero sedan with crumpled door and driver seat, burning SUV on the opposing side), the rescue pickup on the shoulder at s 21, 4 motorbikes, 1 bus, 2 `truck6` (s 124 lane 1, s 168 lane 2), then 339 instanced cars to s 1350 |
| Debris | 7 cones, 3 water barriers, bags, shoe, umbrella, phone, hubcap, mirror, **medic bag, open cutter case, crowbar** (3D set dressing), cable from the mast |
| Signs | Gantry at s 180 (green signs Din Daeng / Rama IX, amber LED board), lit green exit sign `A["exit_sign"]` at s 53, 4 uni-pole billboards (3 lit, wordless), scaffold billboard. All textures are drawn by `tex.py` with Thai set in Kanit |
| Skyline | 76 far towers + 70 nearer + 44 behind the deck start, 140 low-rise boxes beside and under the deck, a painted street-light ground plane, 4 HV pylons, telecom poles with cables, about 60 trees |
| Lights | Moon key + road-only moon glint, sky fill, 10 sodium spots + far bulbs, truck flood (20 kW), beacon domes with red / blue throw spots (12-frame cycle), hazards (20-frame cycle), 4 headlight spots, tail lamps, fire flicker, aviation lights, movable tripod work lamp (`place_work_lamp_safe`, `glare_check`), cabin practicals (`pov_windscreen`), `add_cone`, `practical(light, gain)` |
| Post | `post11.process`: ink outlines, wet streaks under lights (road pixels, index 1), halo, lit rain, haze, lens blur, grade; master levels `post11.LEVELS` (user's: RAIN 0.2, SPLASH 0.25, HAZE 0.3, TILT 0, DOF 0.25, BLOOM 0.55) |
| Film props (`v10/film/stage.py`) | drawn radio, phone with 5 Thai screens (`missed`, `ended`, `incoming`, `again`, ...), drawn two-handed cutter (`cutter.py`), sparks, door hinge, foreground props (pillar, wheel, lip, pole, post, cone) |

Not in any set: people inside cars other than the hero driver (README "not done"), any location off the deck, any moving vehicle (every car is static; wheels do not turn).

### 1.2 What scenes 02-06 need and do not have

Effort is builder-days for one set builder; add about a third for the independent review pass that every earlier set needed. Render cost impact is against the hook's measured 38.8 (75 %) / 66.7 (100 %) CPU s per frame and is an estimate.

| Need (scene) | Exists? | Build from | Effort | Render cost impact |
|---|---|---|---|---|
| **Rescue truck, exterior as a hero vehicle** (03, 04) | Partly: `V.rescue_truck`, parked, opaque, static | Call `V.car("pickup", interior=True, hero=True, doors_open=...)` inside a copy of `rescue_truck`, four opening doors through `split_door`, turning wheels (`add_wheels` objects rotated by distance), a root that moves along `X.P(s, o)`; parent `beacon_throw_*`, `flood_key` and their post cones (`add_cone`) to the root, because `finish11` places them in world space. The pickup must seat four: check `TYPES["pickup"]` cab length, else lengthen to a double cab | 1.0 | None parked; a moving truck changes nothing per frame (scene sync is paid anyway) |
| **Truck cab interior** (03) | Only the sedan's: `add_interior` | `add_interior` on the truck + a dash with a siren switch and radio, practicals in the manner of `pov_windscreen` (`pov_dome`, `pov_dash`), rain streak dressing on the glass. **Raise the cab roof** so seated puppets keep full size: the hook driver is drawn at 2.03 BU against Kong's 2.86 to fit under the sedan roof, and four principals cannot shrink 29 % when they get in | 0.75 | Through-glass shots measured cheap (S18 29.7) but grainy behind glass at 5 spp (v11 known gap): give those shots 6-8 spp, +20-50 % on about 20 s of film |
| **Equipment bay** (04) | No: the canopy is one closed box with a livery texture | Replace the canopy box by a shell with a side hatch on a hinge (`Stage.door()` pattern), shelves from `kit.box`, the existing 3D cutter, crowbar, medic bag and cutter case moved in as owned props, a bay lamp | 0.5 | None |
| **Overturned sedan** (03) | No (`tilt` only steers the wheels) | `V.car("sedan", interior=True, hero=True, crumple=..., broken_glass=...)`, then roll the root 90 deg and lift it by half its width; `dent`, `crumple_front`. The lofted body has no underside: add a floor pan, exhaust, axles and a spinning-down wheel. Shards from the `detail9` scatter, steam card from `build_fx` | 0.75 | None |
| **Blocking lorry** (03) | Partly: `V.truck6` is mid / far detail | A hero copy of `truck6` set across lanes 1-2 ahead of the truck (yaw about 70-90 deg): bevels (`beauty.bevel_pass`), cab glass, hazards, tail lamps, mud, an own wordless livery | 0.5 | None |
| **Service stairway** (03 end, 04) | No | Gap in the outer barrier (a boolean cut, or two `X.sweep` calls around the gap), a steel gate, then a switchback stair tower fixed to a pier: treads and landings `kit.box`, rails `kit.cyl`, `m_steel` + v6 grime, grating as an alpha texture from `tex.py`, one bulkhead lamp per landing. Drop 30 D = 18 m = about six flights | 1.5 | Open grating is alpha: +5-10 % on stair shots. Flat camera-facing cards cut through treads and rails unless shots are side-on |
| **Street under the expressway** (04 end, 05) | Far detail only: `build_city` ground plane and boxes at z = -30 | A new location module: wet asphalt (`m_asphalt9`), kerb, footpath, shophouse fronts with shutters and wordless signs (`tex.py`), parked cars and motorbikes (`V.car`, `V.motorbike`), street lamps (`mast_proto`), cables (v6 telecom poles), trees (`detail9`); the slab underside and piers already exist overhead. Under the deck there is no rain: RAIN 0 with drip lines at the deck edges | 2.5 | No sky light: darker and noisier, maybe 6 spp (+10-20 %). The deck top (19 cars + 339 instances) can be hidden, which takes time off scene sync. Net about the hook's cost |
| **Riverside hospital, shut steel gate** (06) | No | Main block from `m_towers` window textures on boxes, perimeter wall (`m_concrete` + grime), a sliding steel gate of bars (`kit.cyl`, `m_steel`), gate posts, guard booth with a lit window, a light-box sign (Thai "โรงพยาบาล" with a fictional name through `tex.py`, green cross, no real logo). River: a dark plane with the puddle shader and **object index 1**, so `post11` wet streaks draw the far-bank lights for free; far bank = existing tower rows | 2.0 | About the hook's wides. Thin bars alias at 75 %: gate close shots are class A |
| **Construction building** (06 end) | No | Concrete frame (`kit.box`, `m_concrete`), scaffolding in the manner of `build_gantry` and the scaffold billboard, safety net as alpha planes, corrugated hoarding (`tex.py`), the tripod work lamp as the site lamp, cones and water barriers from debris. Only about 30-40 s plays here: build one ground-floor bay and its approach, not a building | 1.5-2.0 | Netting alpha: +10-15 % on those shots |
| Scene 02 extras | Set exists | Glass burst (the `sparks_at` pattern with shard sprites), roof heights by `F.top(x, y)`, more distant smoke plumes and far beacons for the city-wide rise, a wristwatch insert (drawn card like the radio) | 0.5 | None |

Total set work: about 11-12 builder-days. Build each location as its own module (`deck`, `street`, `hospital`, `site`) so that a render process builds only the location its scene needs.

## 2. Cast

### 2.1 Who exists (`v8/cast/draw8.py`, 1,721 lines; `stage8.py`; `gait8.py`)

| Spec | State |
|---|---|
| `kong`, `kong_wet` | Sheet figure 1, 45 measured proportions inside the bands. Expressions determined, serious, neutral, tired, guilty, alarmed, shouting. Props: cutter, phone, radio |
| `crew`, `crew_wet` (the junior) | **James's proportions** (4.49 D), crest hair, long-sleeve rescue uniform. Expressions neutral, shouting, scared, joy |
| `driver` | **Khun Tos's build** (4.22 D, shoulders 0.82 D, no glasses), grey-green skin `#c4cdb2`, white eyes with red pupils, torn white shirt, dark red tie. Poses still, head lift, lunge, bite |
| `namnuea` | A full spec already exists (ponytail, maroon hoodie, grey trousers, red sneakers); so far used only as the phone avatar |
| `extras(n, seed)` | 10 roles, checked pairwise distinct by `_check_unique`; the film uses 10 at 110 px per unit as idle background people. Role 1 is a **delivery rider with a green jacket, green box and helmet** |
| Motion | Walk (0.61 m/s) rendered and measured: planted-foot drift 0.06 cm. Run (1.36 m/s jog): geometry and drift only, never rendered. Arm presets include `wheel`, `lap`, `carry`, `reach`, `claw`, `guard`, `point`, `cross`; legs `stand wide step lunge crouch` and seated |

`uploads/character_sheet.webp` and `character_sheet_v2.webp` are **the same file** (md5 a08330774d20...): there is one sheet with nine figures. Only Kong, James and Khun Tos were measured (`spec/sheet_proportions.md`).

### 2.2 Who is missing

| Character | Sheet figure to match | What to build | Effort |
|---|---|---|---|
| **Dr. Praew** | Figure 3: hair in a bun with loose strands, open white coat over blue scrubs, stethoscope, ID badge, blue gloves, red bag with a white cross, white shoes | New spec: hair style `bun`, outfit `coat` (a hem layer that hangs below the hips between legs and torso), props `stethoscope`, `medbag`; wet variant; expressions calm, command, worried, stern. Measure her on the sheet first (not done) | 1.0 |
| **Khun Tos** | Figure 5: rectangular black glasses, swept hair, navy jacket, white shirt, khaki trousers, brown belt, black shoes, watch, arms crossed | Start from the `driver` proportions (already inside Tos's bands). Variants `tos`, `tos_wet`, `tos_torn` (sleeve ripped, wound covered by the other hand), `tos_bleed` (blood through the cuff, scene 06). **He shares the infected driver's silhouette**: glasses and the navy jacket must carry the difference | 0.75 |
| **James** | Figure 4: spiky hair, joyful face, green jacket with a scooter patch, green box on his back, white helmet with a dark visor, black trousers, green sneakers | Mostly reassembly: `crew` proportions + the rider role's jacket, box and helmet. **Remove the rider from `extras`**, or the audience sees two Jameses | 0.5 |
| **The junior, bitten then infected** | `crew_wet` + the driver's infected treatment | Three variants: `crew_bitten` (wound and blood on the side the hook shows in S21-S24: read it from the final frames and lock it), `crew_dying` (pale, eyes closed), `crew_infected` (grey-green skin, white eyes, the driver's `lunge` / `bite` faces ported to his face) | 0.5 |
| **Crowd of infected** | Sheet style, own designs | `infected(spec)`: skin tint, eyes, torn cloth and blood overlays, claw hands, applied to extras. The generator repeats roles after 10: add 6-10 roles (or hair / palette permutations that still pass `_check_unique`) for 16-20 distinct figures | 1.0 |
| **Hospital guard** | None on the sheet: derive in the sheet's style | One extras-type spec: dark uniform, cap (the cap exists), torch. Seen through the gate bars | 0.25 |
| **Nam Nuea** | Figure 2 (spec exists) | Recommendation: **voice and phone screen only**, as in the hook. Add two screens (`signal lost`, falling signal bars) beside the existing `incoming`. Showing her needs an evacuation-bus interior the screenplay does not ask for | 0.1 |

### 2.3 New poses and cycles, and the planted-feet rule

The rule that the walk already passes: while a foot is on the ground its sole is a fixed world point; the hip drops so the fixed-length leg reaches it; bone lengths never change. `walk8.py measure` checks the sole on the rastered sprite; the pass mark so far is 0.06 cm drift against 30 cm of root travel. Every new cycle below must pass the same check before it is used in a shot.

| Cycle / pose | Who | Notes |
|---|---|---|
| Run, survivors (about 2.2-2.6 m/s) | Kong, Praew, Tos, James | The existing run is a 1.36 m/s jog. Longer flight phase, not longer legs |
| Sprint, infected (about 3.2-3.6 m/s) | junior, crowd | World rule 2: they run fast. Forward lean, arms reaching (`reach`, `claw`). Phase offsets per figure so the crowd does not march |
| Run toward or away from the lens | all | Flat puppets face the camera, so a side run plants visibly and a depth run does not. Use the front / back drawing, tie root advance per step to the step length, and check the sole's world drift along the motion vector |
| Climb onto a car roof, run on it, jump to the next | James, the fleeing extra, infected | Roof heights from `F.top`. Hands on the edge, knee up, stand: 3-4 drawings on twos. On the roof the planted-feet rule applies to the roof point |
| Drag a wounded man backward | Kong + junior | Kong walks backward with planted feet; the junior hangs from Kong's hands and his heels slide by design (wet trail) |
| Crowbar push, crowbar raised | Kong | New drawn prop `crowbar`; reuse the two-hand grip maths of `cutter.hold()` |
| Kneel and press a wound; lying figure | Kong, Praew; junior | `crouch` exists. Lying = the figure drawn horizontal on an upright card; long contact decal |
| Fall back, scoot away | Kong | 4 drawings |
| Drive, ride, brace on impact, climb out | Kong; passengers | `wheel` and seated exist; add switch reach, jolt, step down |
| Stairs down | all four | A gait variant with one tread of drop per step; planted foot per tread |
| Slam against the truck, hands on glass, surge | crowd | 3-drawing loop on twos |
| Sleeve snag, clutch arm, hide arm | Tos | The wound must be tied to the anatomical arm: the drawings mirror with `s`, and near / far limbs swap sides, so a wound drawn on "the near arm" would change arms between shots |
| Refuse, hand up | guard | |

About 2-3 builder-days for the cycles. Continuity sheet to keep per character: wet variants everywhere outside; Kong after scene 04 carries exactly cutter (3 bars), crowbar, radio, small medic bag; who owns the medic bag (Kong's, handed to Praew?) must be decided once; Tos's torn sleeve from scene 04, blood from scene 06; whether James keeps the box and helmet while running on roofs.

## 3. Pipeline

### 3.1 Where the hook's hard-coded times live

| File | Hard-coded |
|---|---|
| `v4/animatic/timing.py` | `NARR0` 0.30, `DUR` 53.32, `TITLE` 50.72, `NF` 1280, the shot table `NEW` (S01-S24 with seconds) |
| `v10/film/common.py` | `AUDIO = audio/narr_ohm`, `CUES` (15 effect times, `dur` 53.32), `CAPS`, `envelope()` over `NF` frames of `narr_final.wav`, `shot_range` (last shot ends at `NF`) |
| `v10/film/cues.py` | `STATIC` 3.243, `LUNGE_FLASH`, `BITE` 43.795, `TITLE` 50.72, `HARD_CUTS = {S21, S22}`, `STRIP` |
| `v10/film/shots/base.py` | `BITE_T`, `PHONE_T`, `LIFT_T` 41.657, `LUNGE_T`, `BITE2_T`, `DOOR_OPEN`; all staging is relative to the hero car |
| `v10/film/finish.py` | `MIX` path, title line `0:00:50.72`-`0:00:53.32`, end of the red cast `fr(45.303)`, `EMPH` (20 exact caption strings), the `.ass` header taken from `audio/narr_v1/preview_v2.ass`, `sheet()` special-cases `S24`, `-t C.DUR`, loops over `range(NF)` |
| `v10/film/noicons.py` | `G_TITLE` 1217 from `v13/icons` timing |
| `v10/film/stage.py` | One set (`B.build()`), four fixed actors, 10 extras at `EXTRA_SPOTS`, marks `K`, `seat`, `door_mid`, `PM`, light names reset in `begin()`, phone strings |
| `audio/narr_ohm/mix_ohm_v2.py` | every effect at a fixed second |

### 3.2 How to generalise (a new package under `ep1/`; `v10/film` stays untouched)

1. **Scene-local timing as data.** `ep1/cut/sc02.json` .. `sc06.json`: narration offset, shots (`id` such as `0314`, `t0`, `t1`, captions), named cues, hard cuts, emphasised words. `common.py` loads the cut for the scene it is asked for. Picture cues are written against caption phrases (`C.word("...")`), not literal seconds; three hook cuts drifted off word boundaries when the voice was re-recorded.
2. **Audio first, per scene.** `audio/ep1/scNN/` holds `script.json`, takes, `narr_final.wav`, `captions_timing.json`, `mix.py`, `mix.wav`. The cut is derived from the caption timing, as in the hook.
3. **Shot modules per scene.** `ep1/shots/sc03/s0314.py` with the existing contract (`ID`, `setup`, `cam`, `frame`, `late`, `PPD`, `SPP`, `PCT`) plus `LOC` (location), `CAST` (specs to build) and `CLASS` (A / B / C).
4. **Stage by location.** `Stage(location, cast)`: a registry of location builders (`deck` = v11 build + EP.1 dressing; `street`; `hospital`; `site`), actors created from the shots' `CAST`, crowd helper. One Blender process serves one (scene, location).
5. **Runner.** `run.py --scene sc03 [--shots ...]`, frames to `out/<tier>_<size>/<scene>/<shot>/f_####.png`. Keep what works: a frame is a pure function of its number, an existing PNG is skipped, workers shard in blocks of 6. Add: write to a temporary name and rename (a killed worker can leave a half PNG), verify PNGs on resume, a per-shot manifest (frame count, code hash, CPU), a queue script that restarts dead workers and runs shot after shot. Blender frame = scene-local frame + a fixed per-scene constant, so re-timing one scene never invalidates another scene's frames.
6. **Per-scene conform.** `finish.py scene sc03`: joins, flashes, captions from that scene's timing, that scene's mix -> `deliver/ep1_sc03_vN.mp4`. Emphasis lists move into the cut JSON. No status icons: `noicons` stays, title mark only at a title.
7. **Master conform.** Concatenate the scenes' finished frame sequences (not their encoded mp4s), one episode `.ass`, one episode mix normalised as a whole (-14 LUFS, <= -1 dBTP), joins at scene boundaries, one encode.

Effort: about 1.5 days including moving the hook in as `sc01` without re-rendering it (its frames stay where they are and are referenced).

## 4. Render budget

### 4.1 Measured basis

| | CPU s / frame | Source |
|---|---|---|
| Draft, 360x640, 2 spp | 10.3 | README, draft v3, 1280 frames |
| Final, 75 %, 5 spp | 38.8 (shots 28.5-55.6) | running final, 245 frames |
| Final, 100 %, 5 spp | 66.7 (shots 65.9-80.5) | running final, 164 frames |
| Wall per worker / CPU | 1.07-1.11 | same logs, load average 5.2-5.6 on 4 cores |
| Hook as a whole (906 frames at 100 %, 374 at 75 %) | 58.5 mean = 20.8 CPU h = 5.7 wall h | computed from the two rows above |
| Fixed part of a frame | about 10 s (scene sync 4.5, post 4-6, staging 0.8) | v4 profile, run log |

Wall hours below = CPU hours x 1.09 / 4.

### 4.2 Three options for 8,280 new frames

| Option | Assumption | CPU s / frame | CPU h | Wall h | With 35 % allowance (CPU h / wall h) |
|---|---|---|---|---|---|
| (i) Everything like the hook | the hook's split, 71 % at 100 % and 29 % at 75 % | 58.5 | **135** | **37** | 182 / 50 |
| (i') Everything at 100 % | | 66.7 | 153 | 42 | 207 / 56 |
| **(ii) Classes** | A 47 % at 100 % (3,882 frames), B 42 % at 75 % (3,510), C 11 % free (888, about 2 s each) | 47.9 | **110** | **30** | **149 / 41** |
| (iii) Cheaper tier on top of (ii) | A at 100 % with 3 spp, about 44 s; B at 75 % with 3 spp, a culled background and 1 bounce, about 25 s (**estimates, not measured**) | 31.4 | **72** | **20** | 98 / 27 |

The 35 % allowance = 20 % re-renders (the hook's review pass re-rendered 432 of 1,280 draft frames, 34 %) + 15 % for crowds and new sets (the hook's 14 puppets cost about 8 CPU s per frame; 20 more are unmeasured).
Drafts: one full pass at 360x640 = 23.7 CPU h = 6.5 wall h. The hook took three passes; budget two = 47 CPU h = 13 wall h.

Classes:
- **A, 100 %:** a principal's face larger than about 0.15 of the frame width; dialogue; inserts with line art; the gate bars.
- **B, 75 %:** wides, the crowd, driving, stairs, anything where figures are small or fast.
- **C, free:** only what is honestly graphic: full-frame phone screens, the watch insert, black, title, end card. Not holds of rendered frames: the production rules forbid moving stills, and beacons and rain change every frame anyway.

Guessed split per scene (the weakest numbers in this document; they move the total by about +-15 %):

| Scene | Length | Frames | A / B / C | Final CPU h | Final wall h | Wall h with allowance | Draft wall h |
|---|---|---|---|---|---|---|---|
| 02, after the bite | 52 s | 1,248 | 60 / 30 / 10 | 18.0 | 4.9 | 6.6 | 1.0 |
| 03, the last rescue truck | 75 s | 1,800 | 40 / 55 / 5 | 24.1 | 6.6 | 8.9 | 1.4 |
| 04, what to leave behind | 70 s | 1,680 | 50 / 45 / 5 | 23.8 | 6.5 | 8.7 | 1.3 |
| 05, the daughter | 65 s | 1,560 | 50 / 25 / 25 | 18.9 | 5.1 | 6.9 | 1.2 |
| 06, the gate | 85 s | 2,040 | 40 / 50 / 10 | 26.2 | 7.1 | 9.6 | 1.6 |
| Sum | 347 s | 8,328 | 47 / 42 / 11 | 110.9 | 30.2 | 40.8 | 6.5 |

What option (iii) would cost in quality: at 3 spp the denoiser does more of the work, and its history here is bad (it turned rain beads into "a shimmering patch between the eyes", and surfaces behind glass are already grainy at 5 spp). Expect crawling wet-road reflections and smeared glass from frame to frame; one bounce loses the contact shade under cars; a culled far background shows as a thinner skyline in wides. The cast's ink lines would not suffer: they depend on render scale and sprite resolution, not on samples.

### 4.3 Recommendation

**Option (ii).** It keeps the user's decision (character shots at 100 %, crisp lines) and saves 25 CPU h against (i). Take from (iii) only the parts that cannot be seen: hide what the camera cannot see per location (the deck top from the street, the 339 instanced rows when looking the other way) and link far practicals away from the cast. Keep 5 spp on class A. Class B shots may drop to 4 spp where the shot says so, as S09 and S24 already do. Any wider use of 3 spp needs a 24-frame flicker test first, and the user should see that test.

### 4.4 Schedule: one scene per night, one clip per morning

The cores cannot draft and final at once. Days build and draft; nights render the final of the scene approved that day. Every final fits one night (largest: scene 06, 7.1 wall h, 9.6 with the allowance).

| Day | Daytime (build, drafts; cores mostly free) | Night (final, 4 workers) | The user receives |
|---|---|---|---|
| 0 (today) | Hook final finishes: 871 frames left, about 4 wall h. Conform. Episode narration script written per scene and approved. Backup 0 | (hook final) | Hook final, 53 s |
| 1 | Pipeline generalised; narration for scenes 02-06 recorded by the lead in one session; scene 02 cast (junior variants, sprint, roof run, drag, crowbar, watch); draft scene 02 (1.0 h) | Final scene 02 (4.9-6.6 h) | Draft scene 02 |
| 2 | Truck exterior / cab / bay, overturned sedan, lorry; Praew, Tos, James, crowd; lookdev stills | Draft scene 03 (1.4 h), then free | **Scene 02 final** (film now runs to 01:45) |
| 3 | Scene 03 fixes; stairway; Tos's sleeve; stairs cycle | Final scene 03 (6.6-8.9 h) | Draft scene 03 |
| 4 | Street set; draft scene 04 (1.3 h) | Final scene 04 (6.5-8.7 h) | **Scene 03 final**, draft scene 04 |
| 5 | Hospital and gate, guard; draft scene 05 (1.2 h) | Final scene 05 (5.1-6.9 h) | **Scene 04 final**, draft scene 05 |
| 6 | Construction site; draft scene 06 (1.6 h) | Final scene 06 (7.1-9.6 h) | **Scene 05 final**, draft scene 06 |
| 7 | Master conform, episode mix and loudness, frame-strip review of motion, re-renders from the allowance | Re-renders | **Scene 06 final**, then **EP.1 06:40** |
| 8 | Reserve | | |

This holds only if set and cast building runs in parallel lanes (about 18 builder-days of work sit in days 1-6) and if each scene's draft is approved the day it is shown. A scene whose draft is not approved moves the nights after it by one.

## 5. Risks

1. **The machine is temporary and the whole project lives in a scratchpad under `/tmp`.** Uptime at the time of writing: 9.5 h. A reboot or cleanup can remove all 13 GB.
   - Back up after every working day (measured sizes): source without renders **6.9 MB** (435 files: `.py` 3.5 MB, docs, JSON, fonts, the sheet); code-drawn textures 25 MB (can be regenerated); audio 126 MB, of which the paid part that matters is `audio/narr_ohm` (43 MB: takes, `narr_final.wav`, `captions_timing.json`, mix).
   - Back up after every finished shot: its final frames. A final frame is 0.83 MB + 0.17 MB depth (415 frames measured). The episode is about 6.8 GB of frames (depth is not needed after conform). Where that is too big to move, keep a per-shot mezzanine: the 53 s draft at CRF 15 is 63 MB, so the episode is about 410 MB.
   - Never back up: `v10/film/out` (5.5 GB), `v8/cast/tmp` raster cache (1.3 GB), EXR passes. Never run whole scenes with `--keep`: kept passes are about 4.4 MB each, four per frame.
   - No durable destination is set up. The only ones in reach are files delivered to the user and the git remote of the working repository, and nothing may be pushed there without the user asking. This needs a decision today.
2. **Paid narration (the lead records it).** `audio/th/tts_fal.py` calls fal.ai `fal-ai/elevenlabs/tts/eleven-v3`, voice Ohm `tKtPl8obOBs5uPMei6yN`; `record.py` checks every take with `fal-ai/elevenlabs/speech-to-text`. The cost unit is **characters sent to the TTS** (plus audio minutes for the check). No price is written anywhere in the project: the lead must read the current rate before recording. Measured on the hook: script 609 characters for 50 s of narration (12.2 characters per second); 27 takes = 903 characters synthesised (x 1.48) and 76.7 s of audio checked; earlier spend 835 (voice pick) + 609 + 321 characters. Episode estimate at the same density: about 4,200 script characters, about 6,300 synthesised with retakes, about 9 minutes checked. Record all five scenes in one session: takes differ from call to call, and a re-record after the picture is cut moves the cuts.
3. **One narrator, four people arguing.** In the hook two people talk on a phone. In scenes 03 and 06 four people shout in one voice. Captions colour key words amber and red already, so colour cannot also mark the speaker. The script must name the speaker in the narration or the caption. A director's decision before recording.
4. **The title is already spent.** The hook ends on the title at 50.72 s; the screenplay puts the title card at 01:45, after the junior turns. Decide: a second short title sting at 01:45, or none.
5. **The 60-second rule is on screen.** The bite is at 43.8 s and the narrator says "in 60 seconds". If the film is read as real time the junior must turn by about 01:44; the screenplay's scene 02 ends at 01:45. The watch insert has to agree with whatever is chosen.
6. **World rule 3 against our own truck.** The infected react to loud sound and moving light. The rescue truck's beacons have flashed since the first shot. The siren moment in scene 03 needs to read as a new cause; decide whether the beacons are off before it.
7. **Flat puppets and camera height.** Cards tilt to the lens up to 40 degrees. Steeper cameras (the rise over the city, a crowd from above) show skewed cards: keep figures small in those shots.
8. **Crowd cost and memory are unmeasured.** Each worker already holds 1.2-1.5 GB (15 GB machine, 4 workers). Test 20 infected in one frame before scene 03 is planned around them.
9. **Shared cores.** Wall time ran 7-11 % over CPU time during the hook final because other work shared the cores. Lookdev stills during a final night slow it further.
10. **Marks and text.** New signs need the Thai glyph check (`phone8`). No real hospital names or brand marks; the red cross on white is a protected emblem (the sheet's white cross on a red bag is the user's own design and stays); the delivery box keeps its own code-drawn scooter pictogram.
11. **Never checked in the hook and inherited here:** playback of motion (only frames and sheets were looked at), 16:9, people inside cars. The episode adds moving vehicles and seated passengers, so the third has to be solved in scene 03.
