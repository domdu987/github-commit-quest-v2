# ep1/sets: the sets of SCENES 02-04 (X1 dressing, X1s, X2, CAB, equipment wall, service stair, UND)

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`, this folder = `PROJ/ep1/sets`.
Everything is built by code on top of the hook's set. `v11/set`, `v4/set_expressway`, `v8/cast` and `v10/film` are imported and not edited. No image generation, no network.
Units as in the rest of the project: 1 BU = 1 D = 0.6 m, Z up, deck top z = 0, path length s = world Y and lateral offset o = world X for s < 420, traffic runs +s, the left barrier (hard shoulder) is at x = -22.15, the street under the deck is at z = -30. Object index: 1 road, 2 cast, 3 car bodies, 4 the rest.

## Files

| File | What |
|---|---|
| `sets.py` | `dress(A, key)` for `X1`, `X1s`, `X2`, `X2c`, `CAB`, `UND`; `register()` adds those locations to `ep1/pipe/stage_ep.LOCATIONS` (the hook's `Stage` plus the dressing) |
| `core.py` | Helpers: boxes / tubes / lathes parented to a root, unique emission materials (`emit`, `set_emit`, `key_emit`), wet see-through glass, alpha cards, lights (`spot`, `point`, `light(name, energy, on)`), glass crumbs, puddle decals, `smash_glass`, `cut_gap`, `hide_rows`, `retarget(cam)`, code-drawn textures (`draw_tex`, cached in `tex/`), `REG` |
| `x1.py` | SCENE 02 dressing of the rescue zone |
| `sedan.py` | The overturned sedan (X1s) |
| `x2.py` | Zone 2: truck moved, taxi, lorry, gate, top of the stair |
| `stair.py` | The flight-and-landing module and its tower |
| `cab.py`, `gear.py` | Cab interior; equipment wall |
| `under.py` | The street under the expressway |
| `rig.py`, `camdefs.py`, `tests.py`, `sheet.py`, `queue.sh` | Proof stage (deck + two v8 puppets through v10's `Act`), the planned camera positions, the stills / cost / final runs, the sheet and the cost table |
| `hook_cams.py`, `check_hook.py`, `hookcheck.py` | The hook's 72 cameras dumped without rendering (`out/hook_cams.json`), a frustum test, and the built-set visibility check (`out/hook_check.md`) |
| Proofs | `sets_sheet.png`, `sets_final_sheet.png`, `cost_table.md`, `out/stills/`, `out/final/`, `out/cost/` |
| v2 proofs | `sets_sheet_v2.png` (before / after of every changed camera), `sets_169_check.png` (every planned camera of every set at 16:9), `out/stills_v2/`, `out/stills_w169/`, `out/stills_diag/`, `out/measure_*.json`, `out/lum_v2.json`, `out/v1_cost/` (the v1 cost records), `queue3.sh`, `queue4.sh`; v1 sources in `_v1_src/` |

## How a shot gets a set

```python
import sys; sys.path.insert(0, PROJ + "/ep1/sets")
import sets; sets.register()                  # once per process, before stage_ep.build(...)
# shot module:  LOC = "CAB"      F.sets["cab"]["anchors"], F.sets["x2"]["anchors"], ...
# or on any built deck:
import beauty as B; A = B.build(); R = sets.dress(A, "X1s"); core.retarget(camera)
```

- One location per Blender process. `X1s` contains `X1`; `CAB` and `UND` contain `X2`.
- Dressing built after the Stage exists: call `core.retarget(F.cam)` (the register builder does) so steam cards face the camera.
- **Not tested through `run_ep.py`**: `Stage.begin()` restores what it moved itself; it does not know these modules' switches (alarm, beacons, shutter, taken items, cab switches, fog, crack, mirror plate, wipers). A shot must set every one it cares about in `setup()` / `frame()`; all of them are plain setters, so a frame stays a pure function of its number.
- Post levels are the standing ones (RAIN 0.2, SPLASH 0.25, HAZE 0.3, TILT 0, DOF 0.25, BLOOM 0.55).
- **Per-location post options: `sets.post(key, **more)`** (also `F.sets_post` after `register()`); a shot's `frame()` should return them merged with its own.
  - `CAB`: `{"sparkle": 0}`. `post9.sparkle` scatters wet-road glints over every pixel of object index 1 and 4; all dressing here is index 4, so without this the seats, head lining and equipment wall are sprinkled with white specks (they were, in the first proofs). Add `"rain": False` for inserts that do not look out.
  - `UND`: `{"sparkle": 0, "RAIN": 0, "SPLASH": 0, "flat": {"GLOW": 0.07, "AMB": 0.30}}`; v2 proofs use `"exposure": 2.05` there (and on the stair). The rain there is geometry; `flat` goes to `stage8.tune_flat` through `Stage._stage` and takes the white halo off the v8 puppets, which in a dark set outlines them like stickers. Use the same `flat` on the stair.

## 1. X1: SCENE 02 dressing (`x1.py`)

`R = x1.dress(A, alarm_car="l1_b", with_alarm=True)`; `x1.alarm(on)`; `x1.burst(point, normal, t)` (window-glass burst, ballistic, t seconds since impact, `None` hides it); `x1.show(False)` (the hook's set again); `x1.roof_route(start, goal)`.

Nothing of the hook's set is moved, recoloured or removed.

| Added | Detail |
|---|---|
| Rescue truck, rear and lane side | Mud flaps, wheel-arch lips, lug nuts, step bumper with tread and tow hook, tail-door frame seams, T-handle, hinges, dark vent window, red / yellow reflector strip, two locker-door seams with latches, grab rail at the rear corner, drip rail, tie hooks, amber side marker and two red rear markers (lit), axle, differential, leaf springs, exhaust, spare wheel under the bed |
| Alarm car | Any jam car by name. Six amber indicator lamps and both headlamps flash on a 10-frame cycle (0.42 s; the other cars' hazards are 20 frames), with two amber point lights and two headlight spots. Off = parts hidden, headlamp materials restored |
| Roofs | `R["roof_route"]`: the chain of car tops from `l3_a` to the bus with the smallest possible longest jump: landing point, leaving point and roof height per car |
| Bus | Anchors only (it is the hook's `bus_a`, s 92-112, lane 3) |

Anchors (`R["anchors"]`, world): `wheel_seat` (the junior's hips against the lane-side rear tyre), `wheel_hub`, `kong_kneel`, `side_crouch`, `corner` and `corner_top` (the vertical edge of S54), `tail_hide` (Kong flat against the tail door), `tail_door`, `out_side`, `out_tail` (unit vectors out of the side panel and the tail), `light_bar`, `lamp_base`, `lamp_aim`, `alarm_car`, `alarm_bonnet`, `alarm_flank`, `alarm_flank_l`, `alarm_front`, `bus_roof`, `bus_roof_front`, `bus_hide` (shoulder side of the bus: out of sight from the lanes), `bus_tail`, `bus_lane_side`, `delivery_box`.

Lights: `x1_corner_glow` (red, 26 W, at the rear-corner marker), `x1_alarm_L_front`, `x1_alarm_L_rear`, `x1_alarm_head_-1`, `x1_alarm_head_1`. The hook's own: `beacon_red_0/1`, `beacon_blue_0/1`, `beacon_throw_red/blue`, `flood_key`, `work_lamp`.

Camera-safe: the wheel and the corner from the lanes (looking -X to -X-Y), no further than 5.4 D out from the wheel (lane 2's SUV `l2_b` stands there). The wheel side is in the truck's own shadow: place the tripod work lamp (`B.place_work_lamp_safe(A, cam, heads, base=anchors["lamp_base"][:2], aim=anchors["lamp_aim"])`), as the hook's shots did. Do not look under the truck from behind the tail: the under-body is five dark parts, not a chassis.

Things to know:
- **There is no white hatchback next to the wreck.** The lane beside the hero car's driver door is empty for 20 D (it is where Kong takes the call). The default alarm car is the taxi `l1_b` (lane 1, 13 D ahead of Kong's mark, 32 D from the truck's wheel). `l3_a` is a green hatchback, but it stands 9 D from where the junior sits, which contradicts S40's "far left". S28-S30 have to be staged on one of the two.
- **The roofs do not form a run.** The best chain is l3_a, hero car, car_ahead, l3_c, l2_c, l3_d, a shoulder car, bus; its jumps are 3.8, 2.8, 6.5, 3.3, 5.4, 4.8, 5.0 D (2.3 to 3.9 m). No cars were added to close the gaps, because every gap is inside hook frames. S56's "one long step" is three or four leaps.

## 2. X1s: the overturned sedan (`sedan.py`)  -- rebuilt in v2

`R = sedan.build(A)`; `sedan.show(False)`. Body colour `#7a1e22` (v1 `#6a1c20`).

**v2 (director: "the car reads as a red blob").** v1 lay on its right side with the roof toward the lanes, so every camera saw one flat red roof panel. The car now lies on its **LEFT** side, as the plan says: **belly and wheels toward the lanes (+X)**, roof toward the barrier (0.85 D gap), nose toward the truck (+s), the driver's (right) flank up. Root (tyre plane) x -18.89, s -5.2; the car occupies s -9.1 .. -1.3, x -21.4 .. -18.8 (`core.world_box`).

| Read cue | What is built |
|---|---|
| Wheels | Four wheels with their own mesh copy and a wet tyre material (`ep1_x1s_tyre`, coat 0.6); the front pair on full lock (`tilt` 0.55) so they stand out of the outline; two are in the air |
| Underside | `_underside()`: floor pan, sills, rails, tunnel, heat shield, subframe and cross-member, sump, gearbox, two drive shafts, lower arms, under-tray, exhaust down-pipe / catalyst / resonator / silencer / tail pipe, fuel tank, rear beam, trailing arms, coil springs, spare-wheel well, brake line (grime, rust and exhaust-steel materials) |
| Nose | Both headlamps burn (`x1s_head_on`, 3.2) and now stand one over the other; the number plate reads vertical; grille slats vertical; bumper half off |
| Lamps | Tail lamps on (`tail` material + `x1s_tail_lamps` 90 W red), hazards on the upper flank (20-frame cycle), the lower headlamp's beam runs along the shoulder toward the truck (`x1s_headlight` 900 W + rain cone) |
| Rim / separation | `x1s_rim`: 14 kW sodium-orange spot from 14 D behind, 7.5 D up (the mast toward the horde); `x1s_rim_lane`: 6 kW cold edge from the lane side behind; `x1s_belly_fill` 1.1 kW cold point on the lane side (the belly faces away from the moon); `x1s_tail_glow` (l3_e's tail lamps) kept |
| Damage | Crushed roof, buckled driver's door (upper) dented inward and ajar 5 deg, empty windscreen with teeth, cracked rear and upper side glass, airbag; the lower mirror is ground off and lies on the road; antenna snapped |
| Debris | Glass at the opening and on the lane side, the briefcase in a puddle in front of the nose, papers, shoe, hub cap, antenna, mirror, oil under the engine; steam from the engine bay on the belly side (v1's hung in front of the opening) |

The **windscreen opening faces the barrier and the truck at 45 deg** (`out_windscreen`), and the moon (`MOON_DIR` comes from -X +Y). Praew works it from the strip between the bonnet and the barrier (`praew_mark`, 0.8 D from the barrier). **Tos (right-hand drive) is now on the UPPER side**, hanging in his belt under the buckled driver's door: `tos_inside` is on the upper half of the cabin; the door edge in S66 presses down on him. This changes the plan's "low side" note.

Anchors: `root`, `nose`, `windscreen`, `out_roof`, `out_nose`, `out_belly`, `out_windscreen`, `roof_mid`, `belly_mid`, `wheels` (four world points), `praew_mark`, `kong_mark` (in front of the nose, lane side), `tos_inside`, `tos_out`, `door_gap` (the A-pillar gap of the upper door: z 2.8, chest height for Kong), `upper_flank`, `briefcase`, `approach_from`.

Lights: `x1s_headlight`, `x1s_dome` (220 W warm, cabin), `x1s_hazard`, `x1s_tail_lamps`, `x1s_tail_glow`, `x1s_belly_fill`, `x1s_rim`, `x1s_rim_lane`.

Camera-safe: from the shoulder north of the nose (S62, S63, S65) and from the lanes abeam (the underside, see the D_LANE diagnostic). From the shoulder the belly is always seen at a grazing angle (the hook-free strip is only x < -18.5 .. -17.5 wide); the underside reads squarely only from lane 3 / lane 2. Not from above the barrier line, not from the south end.

Hook check after the rebuild (`out/hook_check.md`, 72 hook cameras, 4 % margin, ray-cast): sedan (75 objects), its debris (48) and its steam card are in **no** hook frame.

## 3. X2: zone 2 (`x2.py`)

`R = x2.build(A, flights=10)`; `x2.move_truck(A, s, o, yaw)`, `x2.truck_home(A)`; `x2.beacons(on)`, `x2.headlights(on)`, `x2.brake(level)`, `x2.flood(on)`, `x2.gate(open_deg)`.

| Piece | Where | Detail |
|---|---|---|
| Rescue truck | s 194, x -16.9 | The hook's truck moved with its beacon lights, throws, rain cones and flood (flood off, work lamp hidden). Two 5.2 kW headlight spots with cones, a brake light. Half in lane 3, half on the shoulder, because of the taxi |
| Taxi | s 194.5, on the shoulder | 0.5 D from the truck's barrier side. Rear right window smashed with teeth in the frame (`taxi_window`), a rear door open on the barrier side, lit roof sign, red `ว่าง` (vacant) lamp |
| Lorry | s 214 | `V.truck6` slewed 100 degrees across the shoulder and lanes 3 and 2, cab at the barrier. Wordless side livery, under-run bars, marker lamps, hazards, mirrors, tank, exhaust stack, rear doors with lock bars, one leaf swung open, cartons on the road, skid marks, a diesel pool. The existing swerved jam car `row_1_7` closes lane 1 |
| Gate | s 208.1 | A 2.2 D gap cut in the barrier and its rails, end blocks, posts, lintel, a mesh leaf with a chevron kick plate, latch and chain, checker threshold, a lit green way-out sign drawn for this film (running figure, door, arrow; no lettering) |
| Stair | behind the gate | See 6 |
| Debris | between truck and gate | Cones, a helmet, glass, two puddles |

Three jam instances are hidden (`R["hidden_rows"]`). The plan's "150 D further on" is 173 D here: the lorry lies under the sodium mast at s 210, and the gantry's green pools are behind the truck, on the road the horde comes down.

Anchors: `truck`, `truck_fwd`, `truck_right`, `crew_door`, `crew_door_out` (the hand-span), `driver_window`, `truck_rear`, `truck_right_side`, `truck_roof`, `truck_nose`, `light_bar`, `flare_land`, `path_to_gate` (four points), `taxi_window`, `taxi_roof`, `taxi_nose`, `lorry_cab`, `lorry_side_mid`, `lorry_rear`, `lorry_roof`, `gate`, `gate_inside`, `gate_outside`, `gate_sign`, `gate_hinge`, `stair_*`.

Lights: `x2_truck_head_-1/1`, `x2_truck_brake`, `x2_taxi_sign`, `x2_lorry_hazard_L/F`, `x2_gate_sign_glow`, `stair_lamp_0_light`, and the set's `sodium_5_-1/1`, `sign_dindaeng_pool`, `sign_rama9_pool`.

Camera-safe: anywhere on the deck. From behind the truck stay in the gap between lanes 2 and 3 (x about -12.5): lane 3 has a jam car 4 D behind the tail.

Not built: **the X2c hero exterior** (an opening crew door, see-through cab glass on the pickup, a body that rocks). The exterior is still the hook's opaque pickup. S77, S107 and S110 need it; S90 and S95 can be shot through the cab's own windscreen (4).

## 4. CAB: the cab from inside (`cab.py`)

`R = cab.build(A)` (after `x2.build`, or on X1 alone for S78-S80); the cab is parented to the truck's root, so it stands where the truck stands and travels with `cab.drive(A, s, o, yaw)`.

Interior 3.5 wide, 5.0 long, 3.3 high, floor 0.5 above the road, right-hand drive. It is taller than the pickup the hook shows, so that four full-size seated puppets fit; it is only for views from inside or through its own windscreen. While it is shown the pickup's body is hidden and its beacon lights are raised 0.95 D to clear the roof (`cab.exterior(True)` undoes both).

Built: floor, mats, tunnel, head lining, door panels with arm rests, pockets, pulls and grab handles, belts, two bucket seats with head rests, a low-backed rear bench, dashboard with a hooded instrument cluster (code-drawn dials, no brand), steering wheel and column, stalks, a centre stack turned to the driver with four rocker switches, a radio with a lit display and a handset on a coiled cord, vents, glove box, hand brake, gear stick, a helmet, clipboard and bottle, raked wet windscreen, A posts, header, sun visors, interior mirror, two wipers, bonnet with scuttle and washer jets, two wing mirrors, wet side glass (two panes and a quarter light each side).

| Call | Effect |
|---|---|
| `cab.switch("siren" / "beacon" / "flood" / "radio", on)` | Rocker tilts, its LED and a small glow light up; the rockers are back-lit (emission 0.22 off, 0.65 on; red siren, blue beacon). Tape labels: `ไซเรน`, `ไฟวับวาบ`, `สปอตไลต์`, `วิทยุ`. It does not switch the beacons: call `x2.beacons(on)` too |
| `cab.wipers(t)` | Both blades, 0.9 s there and back; `None` parks them |
| `cab.mirror(k)` | Wing-mirror plate 0, 1 or 2: the horde as black upper bodies with raised arms between blurred headlights, through rain (code-drawn; alternate for jitter on twos). `None` = empty road |
| `cab.fog(level, "driver" / "rear_right")` | Breath fog on a right-hand window |
| `cab.crack(0 / 1 / 2)` | The rear left window: one crack from the corner, then branched |
| `cab.dome(on)`, `cab.dash(gain)` | Roof lamp (off by default), instrument glow |
| `cab.ambient(watts=48, console=22)` | The base light of the cab (`cab_ambient`, `cab_console`); the first build had 9 / 9 W and faces were unreadable |
| `cab.seat(name, legs_bu)` | Soles point for a seated flat puppet (`legs_bu = (actor.spec["legs"] + 0.06) * actor.sc`, `pitch_override = 0`) on `drv`, `pas`, `rr`, `rl` |
| `cab.clear_shoulder(s0, s1)` | Hides jam instances on the shoulder for the travelling shots |
| `cab.anchors()` | Re-reads the anchors after the cab has moved |

Seats, per the continuity sheet: Kong `drv` (+X), James `pas`, Tos `rr` (behind Kong), Praew `rl`.

Anchors: `fwd`, `right`, `floor_z`, `hip_z`, `roof_z`, `hip_<seat>`, `head_<seat>`, `win_driver`, `win_passenger`, `win_rear_right`, `win_rear_left`, `outside_driver`, `outside_rear_left`, `windscreen`, `bonnet`, `console`, `switch_<name>`, `wheel`, `mirror_r`, `mirror_l`, `gear_wall`, `shutter_handle`, `between_seats`, `footwell_driver`.

Lights: `cab_dash` (teal, 40 W), `cab_console` (22 W on the switch panel), `cab_radio_glow`, `cab_ambient` (48 W cool, no fixture: stands for the glow of the wet glass), `cab_dome` (off), `cab_glow_<switch>`, plus whatever is outside (beacons above, sodium, headlights).

Camera-safe: anywhere inside between the dash and the equipment wall, clip start 0.02. From the bench, the driver's own window is behind his seat back: the face-at-the-glass shot is framed on the rear right window in the proof; with Kong's profile as an edge it needs the camera on the passenger seat. From outside only through the windscreen, from the bonnet; never show the cab's sides or roof from outside.

Things to know:
- The glass is wet (bead bump and frosted dots). There are **no running streaks and no cleared wiper fan**: the wipers move over glass that does not change.
- The mirrors show a drawn plate, not a reflection.
- The moving shots were not rendered. `cab.drive` moves truck, cab and lights; the hook's taxi `sh_a` stands on the shoulder at s 54 with a door open, so a drive along the shoulder has to start beyond it or swing round it.

### v2 (director: S84 and S81 nearly black)

| Change | Value |
|---|---|
| Instrument glow | `cab_dash` 40 -> 95 W (`DASH_W`), cluster emission 2.2 -> 3.4 (`CLUSTER_EMIT`), `cab_console` 22 -> 30 W (`CONSOLE_W2`) |
| Radio | face emission 1.4 -> 3.2 (`cab_radio2` texture: the level bars plus a plain Thai channel line `ช่อง 3`), `cab_radio_glow` 3 -> 14 W, moved below the face so it does not wash the tape labels |
| Tape labels | back-light 0.12 -> 0.15 (`LABEL_EMIT`); glyphs checked at full size: `ไซเรน`, `ไฟวับวาบ`, `สปอตไลต์`, `วิทยุ` (tone marks and upper vowels inside the tape) |
| Beacon sweep | `cab_sweep_red` / `cab_sweep_blue`: 650 W, 36 deg spots just above the bonnet in front of the glass, aimed back and up; each on a pivot whose yaw is keyed +-38 deg over the 12-frame beacon period (red and blue half a period apart; pure function of the frame). They light the occupants' heads and shoulders, the wheel rim, the head lining and the shutter. **`cab.switch("beacon", True)` turns them on** (also `cab.sweep(on, gain)`); off at build |
| Camera | S81 now switches `beacon` and `radio` on; S84 is framed 0.08 lower so the labels sit mid-frame and the lit radio display fills the bottom |

## 5. The equipment wall (`gear.py`, built by `cab.build`)

Behind the rear bench: a locker 3.3 wide, 1.8 high, 1 deep, roll shutter, two strip lamps.

`gear.shutter(t)` 0 closed .. 1 open (the strip lamps follow); `gear.lamp(on, energy)`; `gear.take(name, taken=True)` for `cutter`, `crowbar`, `radio`, `pouch`; `R["gear"]["items"][name]` is the item's root if a hand should carry it instead.

| Stays | Shape and mark |
|---|---|
| Trauma bag | Big orange bag, grey band, red cross on a white patch, handle |
| Defibrillator | Lime case, white heart with a small bolt inside it, handle |
| Oxygen | Green cylinder, white shoulder, gauge, strap, an O2 mark |
| Charger | Dark box, **empty slot**, two contacts, amber LED, battery mark, cord |
| Flare box | Red box with a flame mark, five flares standing in it (`R["gear"]["flares"]`) |
| Helmets | White and yellow, lamp and band |
| Rope | Coil on a peg, a carabiner |
| Extinguisher | Red cylinder, lever, hose, band |
| Stretcher | Folded, standing in the left column: two poles, orange canvas, straps |

| Leaves | Where it sits |
|---|---|
| Cutter | The set's 3D tool (three green LEDs) on two cradles at the front of the lower tier |
| Crowbar | In two spring clips across the top |
| Chest radio | In a cradle on the shelf, red LED on, volume knob on top |
| First-aid pouch | Small, red, white cross, on a hook in front of the defibrillator |

Tape labels on the shelf edges, plain Thai nouns in Kanit: `เชือก`, `ออกซิเจน`, `ปฐมพยาบาล`, `พลุสัญญาณ` (on the flare box front, under the flame mark), `แบตเตอรี่`, `ถังดับเพลิง`, `หมวกนิรภัย`, `เปลสนาม`. No brand names anywhere.

Lights: `gear_lamp`, `gear_lamp2` (cool white, on with the shutter).

Camera-safe: from the cab, looking -Y. The whole wall needs 20 mm from between the front seats; at the plan's 35 mm a frame holds about one tier.

## 6. The service stair (`stair.py`, built by `x2.build`)

One flight module (channel stringers, ten bar-grating treads with a yellow nosing, tube handrails and knee rails on stanchions) and one landing module (grating, joists, toe plate, rails), all real geometry, instanced as ten flights of 3 D from the gate landing (z 0) to the street (z -30); four columns, ties at every landing, cross bracing on the outer face, brackets into the slab edge. A caged lamp fixture at every second landing; **only the gate landing's is lit** (`stair.lamp(k, on, energy)`).

`stair.tread(k, i)` = centre of tread i of flight k (a planted foot); `stair.path(step)` = every landing and tread, top to bottom. Even flights are against the deck and go down toward -s, odd flights are the outer lane and come back toward +s.

Anchors (`REG["stair"]["anchors"]`): `gate_landing`, `foot`, `foot_exit`, `lamp_top`, `x_in`, `x_out`, `s_a`, `s_b`, `box`.

Camera-safe: along X, from the street side (x about -40) or from the next pier under the deck, so that the upright cards stand in the plane of the flights. Two or three flights per frame; it was not designed to be seen whole and the lower eight flights have no light of their own.

v2: when `under.build` runs (sets STAIR / UND only; X2 is unchanged), the cages on landings 2, 4, 8, 10 burn at 900 W (landing 6's is dead, landing 0 keeps 420 W) and a further cage `stair_lamp_foot` stands on the street-side column at the foot, 4.4 D up, facing the street (900 W). The beacon spill from the deck lights the outer face and the foot (see 7).

## 7. UND: the street under the expressway (`under.py`)

`U = under.build(A)` after `x2.build`; `under.far_lamp(gain)`, `under.glow(gain)`, `under.sky(strength)`, `under.bounce(watts, loc)`, `under.fill(watts, loc)`, `under.deck_top(False)`, `under.frame(g)` (only if drivers are disabled).

Built: wet asphalt ground (the deck's own shader, index 1), kerbed pier islands with hazard-striped faces and bands, downpipes and outfall puddles, two cable trays under the slab, rain curtains off both deck edges and thin drips along four expansion joints (alpha cards that fall with the frame number), puddle lines where they land, a footpath, shophouse fronts as dark blocks with roll shutters, awnings and two lit windows, nine parked cars on this side and three across (instances of the jam's cars), six motorbikes at a pier, a shuttered food stall with stools, bin bags, a bin, cones, a fence line, telephone poles with a transformer and sagging wires, one sodium street lamp at s 266, the stair foot.

Anchors: `ground_z`, `far_lamp`, `far_lamp_pool`, `pier_200`, `pier_250`, `pier_face_200`, `stall`, `bikes`, `kerb_x`, `edge_x`, `stair_foot`, `stair_foot_exit`, `group_mark` (the four at the stair foot), `tos_apart` (at the pier), `walk_line` (the black side of the street).

Lights: `und_far_sodium` (8 kW, with a rain cone), `und_glow_wash` (4.5 kW cool, from the far end, no fixture), `und_sky_side` (a soft SUN, 0.8 W/m2, cold, coming in under the stair-side deck edge 12 degrees below the horizontal: the only light that reaches the ground and the pier faces along the whole street; `under.sky(0)` gives the plan's literal black), `und_edge_sky` (1.8 kW cold spot at the stair-side edge), `und_soffit` (not a lamp: a plane 0.06 under the slab with emission 0.09, not sampled as a light; the wet ground is a mirror and the hook's slab underside is unlit, so without it S112 is black on black; `under.soffit(k)`), `und_bounce` (400 W cool point, no fixture, 5.5 D up near the group: `under.bounce(watts, loc)` moves it with them), `und_fill` (0 by default; the proof of S122 uses it at 22 W as the phone).

Camera-safe: along the street in either direction between x -22 and -6, and across toward the stair side. The shophouses are blocks: keep them beyond 15 D and dark. Do not look up at the slab from close: the underside is the hook build's plain concrete with two trays.

### v2 (director: far too dark, figures tiny)

`under._practicals_v2()` (built by `under.build`), all practicals with a source the story allows; levels in `under.py` constants:

| Practical | Where | Light |
|---|---|---|
| Sodium street lamps `und_street_<s>_<w/e>` | kerb side, s 190, 211 (beside the stair), 242; far side s 222, 262 (plus v1's s 266) | 18 kW spots, 120 deg, rain cones (`STREET_W`) |
| Pier lamps `und_pier_<s>_<w/e>` | bulkheads on the pier faces 8 D up: 150 (both), 250 (both), 300 (w); **pier 200's is dead** (S122 stays dark at Kong's pier) | 5 kW mercury-green-white down (`PIER_W`) + 5 kW up-wash onto the slab (`PIER_UP_W`): the lit soffit is what the wet street mirrors |
| Shop lightboxes `und_sign_soup` / `und_sign_pharm` | projecting from the shop fronts at s 203.5 (behind the stair from S112) and s 232; code-drawn, plain Thai nouns `ข้าวต้ม / โต้รุ่ง` and `ขายยา` with a cross; no names | emission 2.4 + 380 W glow each |
| Beacon spill `und_strobe_<red/blue>_<out/in>` | no fixture: the light bar on the deck above the gate; "out" beyond the tower's outer rail, "in" past the tower's ends and the slab edge down to the stair foot | 24 kW (in x0.75), keyed exactly like the hook's `beacon_red_0` (12 frames; red peaks frames 3-6, blue 9-12). `under.strobes(on)` |
| Stair cages | see 6 | |
| Soffit | the slab underside is now concrete that takes light (+ the old faint glow 0.20) | `under.soffit(k)` |
| Base levels | side sky 0.8 -> 2.0 W/m2, glow wash 4.5 -> 6 kW, edge sky 1.8 -> 2.4 kW, bounce 400 -> 600 W | |
| Puddles | three more at the stair foot | |

Setters: `under.lamps(gain)` (street + pier, down and up), `under.strobes(on)`, `under.signs(on)`, plus v1's `far_lamp`, `glow`, `sky`, `soffit`, `bounce`, `fill`.
New anchors: `street_lamps`, `pier_lamps`, `signs`.

**16:9 extension (far side):** the far side of the street was open ground to the skyline; a wide S122 / S133 showed a wet plain. Added `_far_side()`: kerb (x 31.9), footpath (x 32-41), a row of shophouse fronts at x 45.4 (s 123-345, 11-21 D tall) with shutters, awnings and three lit windows, three telephone poles with wires; the ground plane now runs to x +58.

Post: `UND_POST` exposure 1.6 -> 2.05 (S111 too). Stills that should show the beacon spill use frame 4 (red) or 10 (blue) (`frame` in the camdef).

## Proof runs

```
python3 tests.py still X1S [--cam S63] [--tier draft|final] [--size 360x640]    # out/stills/
python3 tests.py cost  CAB                                                      # 24 draft frames -> out/cost_CAB.json
python3 tests.py final UND                                                      # 720x1280 final tier at 75 % and 100 % -> out/final/
python3 tests.py hookcheck                                                      # out/hook_check.md
python3 tests.py sheet ; python3 tests.py table
python3 tests.py still UND --tag v2                                             # (v2) out/stills_v2/ + one JSON per still: CPU and figure heights
python3 tests.py still UND --size 640x360 --tag w169                            # (v2) the 16:9 check from the same camera positions (36 mm on the long side)
python3 tests.py still X1S --cam D_LANE,D_NE,D_UP --tag diag                    # (v2) diagnostic views (camdefs.DIAG), not shots
python3 tests.py measure UND [--camdefs _v1_src] --tag v1                       # (v2) figure heights only, no render
python3 tests.py sheet2                                                         # (v2) sets_sheet_v2.png and sets_169_check.png
```

## Hook check (`out/hook_check.md`, built set, 72 hook cameras, 4 % frame margin, ray-cast occlusion)

Re-run after the v2 sedan (2026-11-28):

| Added by EP.1 | Hook shots whose frame holds any of it | Not hidden by the set in |
|---|---|---|
| Overturned sedan (75 objects with the underside), its debris (48), its steam card | none | none |
| Truck hardware (54 small parts) | S04, S05, S08, S09 | S04 at 26 D, S05 at 49 D (the tail and lane side; the largest single part, the step bumper, is about 100 x 5 px in S05) |
| Alarm lamps on `l1_b` | 11 shots | S03, S24 (they are hidden unless `x1.alarm(True)`) |

The hook cameras were dumped from `shot.frame()` only (no `late()`), at three frames per shot. UND / STAIR / CAB are not in the hook at all.

## v2 camera changes (`camdefs.py`; director: a standing figure >= 35 % of the frame height in W shots, >= 60 % in M)

Measured by `tests.py measure` (soles to head as a fraction of the 9:16 frame height):

| Camera | v1 | v2 | Change |
|---|---|---|---|
| S111 W side 28 mm | Kong 15 %, crew 16 % (15 D) | Kong 38 %, crew 46 % | 6.2 D from Kong; frame 4 (red beat) |
| LOW (not planned) 35 mm | 17 % / 16 % | Kong 36 %, crew 29 % (on the lower flight) | 7.0 D |
| S112 (plan EW) 24 mm | 4 % / 4 % (46 D) | Kong 36 %, crew 46 % | looks out from under the deck at the stair foot; frame 10 (blue beat). The plan's "very small" is overruled by the 35 % floor |
| S122 W 28 mm | Kong 18 % | Kong 36 % | 6.1 D; Kong turned away from the pier, phone light on his -X side |
| S133 (plan EW) 35 mm | Kong 12 %, crew 10 % | last figure 38 %, next 25 % | 7.4 D behind the last of them |
| S62 / S63 / S65 | | crew 16 % (far, W) / 50 % / 99 % | re-aimed for the v2 sedan; S62 Kong 49 % in the right foreground |
| S81, S84 | | | S81: beacon + radio rockers on; S84: framed 0.08 lower |

No M shots are in STAIR / UND. CAB / GEAR (seated, close) were not measured against the floor.

## 16:9 check (`sets_169_check.png`)

Every planned camera of every set, at its planned position, at 640x360 with the same lens (36 mm on the long side: a 16:9 frame is wider and shorter than the 9:16 one). Checked for empty or unfinished space at the sides:

| Set | Result |
|---|---|
| X1 (S34, S54, S29, S57) | holds: the hook's deck and jam fill both sides |
| X1s (S62, S63, S65) | holds at the sides; in S63 the left third looks down empty lanes south of the sedan (the hook's deck; dressing there would enter hook frames, not added) |
| X2 (S82, S97, S98, S107) | holds |
| CAB (S78, S81, S84, S88), GEAR (S100, S101, S102, WALL) | holds: the cab is a closed box; S84 shows a third rocker and its label (`สปอตไลต์`) at the right edge |
| STAIR (S111, LOW) | holds: the tower is wider than the frame |
| UND (S112, S122, S133) | **extended**: the far side of the street was open ground; added the far kerb, footpath, shophouse row, lit windows, poles and wires, ground to x +58 (see 7) |

Not rendered at 16:9 final. The 16:9 frames crop the figures vertically (they need their own framing through `F.pick`), which was not addressed.

## Known gaps and weak points

- **X2c is not built** (opening crew door, see-through pickup cab, rocking body).
- Nothing was rendered through `ep1/pipe/run_ep.py`. No moving shot was rendered (cab drive, wipers in motion, alarm rhythm, glass burst, shutter, falling rain cards, the v2 beacon sweep and spill were checked on single frames only).
- v2 sedan: the underside reads squarely only from the lanes (diagnostic D_LANE / D_NE); from the planned shoulder cameras it is seen at a grazing angle, so S62 / S63 read "on its side" mainly through the vertical number plate, the stacked headlamps, the steered front tyre and the rim light. **S65 is still weak**: Praew fills the left half and the cabin through the opening is a dark mass with warm glints, not a readable windscreen frame (no Tos card was placed). The S62 foreground has an out-of-focus orange hook prop at the bottom and the headlight beam on the road is very bright. Tos's side (now upper) changes the plan's note.
- v2 UND / STAIR: brighter (mean luminance 0.07-0.10 -> 0.12-0.15, near-black pixels 30-58 % -> 9-22 %) but still darker than the hook's deck shots (about 0.2-0.3). The beacon spill is weak in S112 at frame 10; it reads mostly on the tower's top in S111. In S111 Kong's head is near the top edge. The pier lamps are small in frame; the street-lamp pools hardly read at grazing angles (the wet asphalt is mostly a mirror). The far-side shophouses hide part of the skyline in S122.
- Cab: glass has beads but no running water and no wiper fan; mirrors are a drawn plate; S78's face behind the beaded, fogged glass is grey and speckled at draft size. The sweep lights are a cheat (spots just outside the windscreen, not the roof bar).
- Equipment wall: at 30 px the defibrillator's bolt still reads as a notch in the heart; from the front of the cab the seat backs and the actors cover most of the wall (S100).
- X1: the wheel side has no practical of its own (the S34 proof uses the tripod work lamp at 2.8 kW). In the S29 proof a white out-of-focus foreground edge crosses the lower left; in S54 a hook prop (the orange case) covers the crouching figure's body.
- Costs: see `cost_table.md` (v2 section).

## Checker's pass (2026-11-26)

Defects fixed in this folder (each marked `(checker)` in the code):

| Where | Defect | Fix |
|---|---|---|
| `cab.py` | The centre stack leaned back into `cab_dash_top`: all four rocker switches were buried inside the dash slab and invisible from everywhere (the "black rockers" of S84) | Stack moved 0.26 toward the seats; rockers back-lit |
| `cab.py` | Faces unreadable under 9 W | `AMBIENT_W` 48, `CONSOLE_W` 22, `cab.ambient()` |
| `cab.py` `_label_tex` | `ไฟวับวาบ`, `สปอตไลต์`, `ปฐมพยาบาล` ran off the tape at both ends | The word is shrunk until it fits with its marks |
| `gear.py` | Bolt split the heart; no `พลุสัญญาณ` label | Bolt inside the heart; label on the flare box |
| `sedan.py` | The upper door bulged 0.5 D out of the flank (the "spike"); roof unlit | Inward dent, `x1s_roof_fill`, body `#6a1c20` |
| `under.py` | S112 black on black; figures unreadable; stair unlit below the top | `und_soffit`, `und_sky_side`, `und_bounce`, higher glow / edge sky |
| `core.py` `puddle` | `hash(name)` seeds the outline: salted per process, so each worker and each resume drew a different puddle | `zlib.crc32` |
| `core.py` `draw_tex` | Texture cache written in place (four workers start together) | Temp file + rename |
| `hookcheck.py` | Crashed on the now-empty puddle group (the table in `out/hook_check.md` could not be regenerated) | Empty groups are skipped |
| post | White "sparkle" specks on every interior and under-deck surface | `sets.POST`, `sets.post()`, `F.sets_post` |
| `sheet.py`, `tests.py` | Captions overlapped on the sheet; no multi-frame final cost | Captions fitted; `final` mode adds `--steady N` frames |

One frame was rendered through the film's own `Stage` (`stage_ep.build("CAB")`, `begin`, `frame`, `render`; `ep1/chk/sets/pipe_test.py`, `pipe_CAB.png`): `begin()` changed none of the set's lights or the truck's position. That is not `run_ep.py` and not a moving shot.
