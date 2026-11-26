# EP.1 "ทางด่วนนรก": opening hook, FINAL shot plan (supervising director's merge)

Scene 01 "สายที่ไม่ได้รับ" complete, plus the first beat of Scene 02 "คนที่กลับมา" ("คนขับพุ่งเข้ากัดเจ้าหน้าที่กู้ภัย. เสียงร้องท่ามกลางสายฝน"). Vertical 720x1280, 24 fps, Thai dialogue with burned-in Thai captions. Every picture shot is a true 3D shot through the v3 pipeline: v2 puppets on emission-only cards in one code-built Blender set, one hard key, blue-violet ambient, 22 mm lens.

**Base and grafts.** The base is the emotion-first plan (Director B). It had the best combined judge score (92 against lean 91.5 and hook-first 82.5) and the highest fidelity. Grafts: the opening timing and several sound ideas come from hook-first (Director A). The production discipline comes from lean (Director C): one set, reused camera setups, H0-H3 handheld levels, rain in post, emissive reflection decals, a budget, render gates and a faithfulness table. Every problem the judges named is fixed or flagged (see "What this merge fixes").

**Clock.** Film time in seconds from frame 0; frame = round(t x 24). All 30 fps constants in the pipeline are converted to seconds x 24 before any render (risk 1). **Every "push ×N", "snap ×N" and "crash" move in this plan is a dolly at a fixed 22 mm** (`camrig.snap` / `key_camera` with no `lens` key); the focal length is never keyed. Dialogue times come from the existing voice takes in `audio/ep1_hook/takes/` (character timestamps in `*.chars.json`). They are not estimates. Re-cut to the final mix.

---

## Header

| Item | Value |
|---|---|
| Total duration | **53.25 s = 1278 frames at 24 fps** (51.75 s of picture + 1.50 s black tail with the radio bookend). Optional standalone post: + 2.00 s title card = 55.25 s (see shot 24) |
| Shot count | **24**: 23 picture shots + 1 black tail. Camera setups: 15, of which 7 are used twice or more |
| Average shot length | **2.25 s** over the 23 picture shots (range 1.00-3.50 s; median 2.00 s). With in-shot snap reframes, the framing changes every 1.4 s on average. Only the head lift (shot 18, 3.50 s) and shot 10 (3.50 s, split by a snap reframe on "สัญญา") reach 3.5 s |
| Joins (23) | 18 hard cuts (4 of them match or punch-in cuts), 2 whip pans, 1 dissolve (8 f), 1 smash to black, 1 static-burst cut |
| Sets | **1**: `expressway3d`, an elevated Bangkok expressway deck at night in heavy rain. It holds the pile-up, the hero sedan with an openable driver door and a minimal interior, Kong's rescue pickup with a red light bar, the gridlock running into haze, light masts, Jersey barriers and the skyline card. All inserts (radio, battery, phone and watch) are 3D props in this set. No second location |
| Cast on screen | **ก้อง Kong** (38, rescue worker; new puppet). **เจ้าหน้าที่กู้ภัย the rescuer** (young teammate, unnamed in the screenplay; asset `rescuer`; new puppet). **คนขับ the driver** (new puppet, slumped and then infected states) |
| Voices off screen | **เสียงวิทยุ**: a rescuer from another unit, radio only. **น้ำเหนือ Namnuea**: phone only. Her face appears only as the contact photo drawn into the phone screen texture (a prop, not an actor) |
| Props | **Kong:** cordless rescue cutter/spreader with a 3-bar battery panel (always in his RIGHT hand, never handed over); smartphone (left hand, left chest pocket) with 3 screen states; wristwatch on the LEFT wrist (red seconds hand, 21:47); shoulder radio on the LEFT shoulder strap with a red TX LED; crowbar (ชะแลง) in a side loop on the LEFT of his backpack, hooked end at hip height. **Rescuer:** Halligan pry bar, white helmet with a headlamp. **Sedan:** driver door (keyed hinge), steering wheel, dashboard hazard tell-tale, seat belt |
| Effects | Rain in post (3 streak layers occluded by a depth pass) + splash rings + drops on glass, phone and radio grille; red light-bar flash (emissive geometry, emissive road smear decals, at most one shadowless red point light, per-card tint + red rim on the puppets); amber hazard (emission only + driver card tint); headlamp (emissive beam card + driver card tint); wet puppets (drip fx, darker wet fills); handheld H0-H3; streaked plates on whips and crash moves; 2-frame red flash on the lunge |
| Palette | EP.1: deep blue shade (hue 240-255), wet grey concrete and asphalt, emergency red. Warm colours only on Kong's orange vest, the small amber hazard blinks and the phone screen. No sodium-orange lamps: masts are cold white LED |
| Captions | Thai, burned in, **Kanit Black** (`fonts/Kanit_900Black.ttf`, already in the project), 50 px, white fill, 4 px black stroke, centre y = 900, hard swap with no animation, phrases of 4-14 Thai characters. **On-screen speakers in white; radio and phone voices in pale blue-grey `#cfd8ee`.** Whole heads stay above y = 880. The scream is never captioned |
| Audio | Voice takes already on disk (no new generation, no paid API): R1 radio, N1 + N2 Namnuea, **K1 + K2 Kong (both voice `jucSq…`; K1b is a different voice and must not be mixed with K2)**, C1 rescuer. SFX on disk: `audio/ep1_hook/sfx/` (rain, radio static, phone vibrate, door pry, cutter, scream, lunge, sirens, car alarm, heartbeat, hit) + `beep.wav`. The other small cues are synthesised locally or taken from CC0 sources (list in Assets). `music/bed_temp.mp3` is NOT used ("ห้ามดนตรีบอกให้ร้องไห้"); only an unpitched sub drone |
| Render estimate | 1242 picture frames + 8 dissolve handles = 1250 Cycles frames at about 16 CPU s, plus plates, sprites and post ≈ **22,400 CPU s ≈ 6.2 CPU h ≈ 1.6 h wall on 4 cores** (17.5 CPU s per final frame against the 18 s budget). See Budget and gates |

### Handheld levels (C), keyed into the camera before render so parallax stays true 3D

| Level | Use | Amplitude (24 fps) |
|---|---|---|
| H0 | dread and silence: the hang-up silence, the head lift | 0 (eased drift only, a constant-speed share so it is never static for more than 6 frames) |
| H1 | breathing: the call | 1.5 px sd, about 1 Hz |
| H2 | work and nerves: rescue work, walking, Kong sensing | 4 px sd, 2 Hz, roll ±0.6° |
| H3 | violence: the lunge and the scream only | 12 px sd, 5 Hz, 1.0-1.5 s, decaying over 10 frames |

### Light model (one key, as LOOK_SPEC)

- **Key:** a sun lamp motivated by the nearer LED light mast. Cool white `#cfd8ff`, angular size 0.8°, elevation 42° (whole-figure shadows fall on the wet deck), from screen-left in every setup except `wide_high` and `high_K`, which look back along the lanes and use `head_flip = True`.
- **Ambient:** blue-violet emission, hue 240-250, with per-surface tints (asphalt toward slate-blue, concrete toward grey-blue, the orange vest untinted). Shade at 0.15-0.31 of lit luminance.
- **Emergency red:** the pickup's light bar is emissive geometry (bloom above scene-linear 1.0), flashing as a **2 Hz double flash, L-L-R-R per second**. Red on the road comes from **emissive smear decals** under and behind the pickup, pulsing in sync. It is NOT glossy ray tracing: the set hides objects from secondary rays, so real reflections would not render. At most **one red point light with shadows off** (the first thing switched off if the gate fails).
- **On the puppets** (cards are never lit): per-frame `tint` driven by the light-bar phase (peak `#ffb0a8`), plus `rim="#ff5a4a"` at 0.4 opacity on R-flash frames. The base night tint is `#dfe4ff` and the ink is `#1e142e`. Phone glow, hazard amber and headlamp are also per-frame tints on the card concerned (uniform tint; see risk 4).
- **Depth haze and soft backgrounds:** the mist and depth pass is mixed toward `#1b2440` (0 at 15 D, 0.75 at 140 D). Where this plan says "soft", it means a **post depth blur from the same Z pass**, not Blender DOF: camrig keeps `use_dof False`, so no extra Cycles noise.

---

## What this merge fixes (every judge-named problem)

| Problem named by the judges | Fix in this plan |
|---|---|
| B: 3.0 s of near-black before the world appears | The radio cuts at **2.50 s** on the static burst into the red puddle; the crane-up reveals the gridlock by **3.00 s** (shots 01-02). A red flash washes the radio at 1.30 s, a snap push onto the LED lands on "เดี๋ยว!", and captions are on screen from frame 0. Why 2.50 and not 2.25: the measured radio take needs 2.50 s even at tempo 1.3 (see shot 01) |
| B: ~19 s of call with no threat on screen; dip at 25-30 s | The motionless driver is planted at 9.0 s (shot 06), and the hazard tick runs as a metronome from then on. The rescuer works the door in depth behind Kong in shots 07, 10, 11 and 13, and glances back at him once (11). No call shot is longer than 3.5 s |
| B: lunge at 47.5 s, too late | The lunge lands at **44.67 s** (shot 21), leaving 7 s of escalation (bite, scream, crowbar) before black |
| B: optional phone glow in shot 20 reads as a new call | Cut. No phone light or notification after the pocketing beat (shot 16) |
| B: head-lift reveal depends on the wheel rim hiding the face | The face is hidden by `head_dy` +0.45, pitch +1.5, roll 25°, lean 40° and the new `infected_slump` closed-eye drawing (C). The eyes open only in shot 21, as a hard swap |
| B: footwell camera; A: passenger-headrest reverse and cabin OTS | No camera inside the cabin. The interior is seen from `door_depth` (outside the door frame) and `windshield_cu` (on the hood, glass as a holdout) |
| B/A: puddle reflections assumed; extra spot lights; hazard and headlamp lights on cards | Emissive decals, one optional shadowless red point light, and the hazard, headlamp and phone glow as emission on the set plus tint on the cards. No extra real lights |
| A/B: rain as Cycles streak cards | Rain, splashes and drops on glass are done in post, occluded by a new Z/mist pass (asset P1) |
| All: "out of focus" with DOF off | Replaced with a post depth blur from the Z pass |
| A: rescuer's scream cut off and arm slack (spends the 60 s turn early) | The rescuer stays alive and screaming at the cut, his hand clamped on the wound (shot 22). Scene 02's "พี่...ผมหนาว" and the 60 s clock are intact |
| A: driver lifts off toward a siren and stands up (runs ahead of the crowbar push) | The driver stays on the rescuer through the cut (shots 21-23). Kong pushes him off in Scene 02, as written |
| A: Kong frozen, crowbar never touched (push-off would be luck) | Kong adjusts the crowbar loop as he walks in (16) and his hand closes on it as he senses danger (20). The hook ends on him ripping it free (23): cause and effect, not coincidence |
| A: mid-film radio hiss implies the radio voice came from this car | Removed. The radio is heard only at the open and voiceless over black at the end (another unit, still dead air) |
| C: Kong hands the cutter to the rookie; cutter left on the road | Kong owns and holds the cutter in his right hand throughout. The rescuer opens the door with his own Halligan bar |
| C: driver wakes on touch (edges toward rule 9) | Nothing wakes him: he comes back on his own (see the check-pass row below). The headlamp beam crosses his face as he twitches, and the moving light is what he lunges at (rule 3). The touch is only a reach that does not land before he moves |
| C: title card moved into the hook | The default cut ends black with the radio squelch. A title card exists only in the standalone-post variant (shot 24), flagged |
| C: 6.0 s and 5.5 s takes | Longest call shot 3.50 s, split by a snap reframe |
| A: 29 shots, 2 sets, shattering window, rolling helmet, two-hand IK | 23 picture shots, 1 set, no breaking glass, no physics props. The cutter is carried one-handed (no two-hand grip) |
| B: crowbar reach over the shoulder near the 0.74 D IK limit | The crowbar rides in a side loop at the left hip. The left hand reaches down and back (within reach), then swings it up |
| All: crowbar on the pack vs Scene 04 picking a ชะแลง from the truck compartment | Kept (it is what makes the Scene 02 push earned). **Flagged to the screenplay owner** (risk 12) |
| B: infected grey head fill needs a new key | Listed as a cast-extension asset (no `puppet.py` edit) |
| Check pass: Kong spoke with two voices (K1b is voice `LILq5…`, K2 is `jucSq…`) | Kong's first line is now take **K1** (same voice as K2), placed at 20.22; shot 11 times and the snap moved to match |
| Check pass: a 6-frame dissolve between two shots from the same setup (09 → 10) in the middle of one sentence reads as a ghosted jump cut | Replaced by an axial punch-in cut ×1.2 on the end of "พ่อ"; shot 10's sizes adjusted |
| Check pass: the driver ignores the shout, the door pop and the chime (31-33 s) but "wakes" for the beam: that contradicts rule 3 (loud sound) | The beam no longer wakes him. He is an unresponsive casualty who has not yet come back (the radio's "ไม่ตอบสนอง" pattern), so nothing reaches him; the twitch marks him coming back, and once his eyes open the moving headlamp and the rescuer's voice are what he goes for (rule 3) |
| Check pass: shot 21 used a lens "crash zoom" (22 mm rule) and an 8-frame dead-still hold (never static over 6 frames) | Crash dolly-out at 22 mm from a start 1.5 D from his face; the hold creeps at 3 %/s |

---

## Timeline at a glance

| # | Time (s) | Frames | Dur | Setup | Angle | Beat | Line | Out |
|---|---|---|---|---|---|---|---|---|
| 01 | 0.00-2.50 | 0-59 | 2.50 | insert_radio | eye-low macro | radio in the dark | วิทยุ: ศูนย์ครับ ... เฮ้ย! | static-burst cut |
| 02 | 2.50-3.75 | 60-89 | 1.25 | puddle_crane | ground → low | red on wet asphalt, crane up | — | cut on the rise |
| 03 | 3.75-5.75 | 90-137 | 2.00 | wide_high | high | the gridlock | — | cut, same axis |
| 04 | 5.75-7.50 | 138-179 | 1.75 | low_medium_K | low | Kong with the cutter | — | match cut on the tool |
| 05 | 7.50-9.00 | 180-215 | 1.50 | insert_battery | raking insert | thumb press: 1, 2, 3 bars | — | whip pan right |
| 06 | 9.00-11.00 | 216-263 | 2.00 | door_eye | eye | the door and the still driver | — | cut on the first buzz |
| 07 | 11.00-13.00 | 264-311 | 2.00 | mcu_K | eye | buzz, glance at the watch | — | match cut on the phone |
| 08 | 13.00-15.00 | 312-359 | 2.00 | insert_phone | high insert | 4 missed calls, 21:47 | (screen text) | punch-in cut |
| 09 | 15.00-16.75 | 360-401 | 1.75 | cu_K_eye | eye | he answers | น้ำเหนือ: พ่อ (pre-lap) | punch-in cut ×1.2 |
| 10 | 16.75-20.25 | 402-485 | 3.50 | cu_K_eye | eye | "พ่อสัญญา..." | น้ำเหนือ | cut |
| 11 | 20.25-23.50 | 486-563 | 3.25 | mcu_K | slightly high | "พ่อมีเคสด่วนลูก..." | ก้อง | cut |
| 12 | 23.50-26.25 | 564-629 | 2.75 | high_K | high wide | "ทุกครั้งเลย..." (the breath) | น้ำเหนือ | dissolve 8 f |
| 13 | 26.25-28.50 | 630-683 | 2.25 | cu_K_low | low | "เดี๋ยวพ่อโทรกลับนะ" | ก้อง | cut |
| 14 | 28.50-31.25 | 684-749 | 2.75 | insert_phone | eye insert | silence, beep, drop, thumb hovers | — | cut (shout pre-laps) |
| 15 | 31.25-33.00 | 750-791 | 1.75 | door_eye | eye | "พี่ก้อง! เปิดได้แล้วครับ!" | เจ้าหน้าที่ | whip pan right |
| 16 | 33.00-35.25 | 792-845 | 2.25 | track_K | low | phone pocketed, he goes | — | cut |
| 17 | 35.25-38.25 | 846-917 | 3.00 | door_depth | eye | rescuer leans in; headlamp; twitch | — | cut |
| 18 | 38.25-41.75 | 918-1001 | 3.50 | windshield_cu | low → eye | the driver lifts his head | — | cut |
| 19 | 41.75-42.75 | 1002-1025 | 1.00 | windshield_cu (reframed) | eye | the rescuer's wrong relief | — | cut, rain drops out |
| 20 | 42.75-44.00 | 1026-1055 | 1.25 | cu_K_eye | eye | Kong senses it, hand on the crowbar | — | cut |
| 21 | 44.00-47.00 | 1056-1127 | 3.00 | door_low | low | eyes open, lunge, bite | (scream) | cut mid-scream |
| 22 | 47.00-48.75 | 1128-1169 | 1.75 | door_low (reframed) | low | the scream in the rain | (scream) | cut |
| 23 | 48.75-51.75 | 1170-1241 | 3.00 | cu_K_low | low | Kong rips the crowbar free | (scream) | smash to black |
| 24 | 51.75-53.25 | 1242-1277 | 1.50 | — | — | black, radio squelch bookend | — | end |

Camera setups used more than once: `door_eye` (06, 15: the closed door and then the open door, same frame), `mcu_K` (07, 11), `insert_phone` (08, 14), `cu_K_eye` (09, 10, 20), `cu_K_low` (13, 23: the face on the promise and then the face in horror), `windshield_cu` (18, 19), `door_low` (21, 22).

---

## Shots

### Shot 01: the radio in the dark (the first-3-second hook)

| Field | Plan |
|---|---|
| Time | 0.00-2.50 s, f0-59 (60 f), 2.50 s |
| Set / setup | expressway3d, `insert_radio`: Kong's shoulder radio as a 3D prop pinned each frame to his `shoulder_l` anchor (C). The rest of the frame is the wet vest and rain-black night |
| Framing / angle / lens | Extreme close-up of the radio top: grille, antenna root, red TX LED at about (360, 560). Slightly low (camera 0.3 D under the radio, pitched up 8°), 22 mm at 0.7 D. About 85 % of the frame below value 0.15 |
| Camera move | **Already moving on frame 0:** eased push at 8 %/s, H1. At 1.72 s ("เดี๋ยว!") a **snap push ×1.5 onto the LED** in 12 frames (C). On "เฮ้ย!" (2.15 s) a 4-frame **flinch jolt**, 10 px down-right, as if Kong flinched (B). Last 3 frames: H3-sized jitter under the static |
| Cast | Kong as the vest and strap only (sprite crop). A rain drip runs off the antenna (fx `drip`) |
| Action | The LED pulses with the voice envelope (emission keyed to the take's loudness). Drops bead and run down the grille (post drops registered to the prop corners). **1.30 s: one red light-bar flash washes over the radio and is gone** (C), the first hint of a world outside. On "เฮ้ย!" the LED stutters 3 times; at 2.42 s the static burst kills it |
| Dialogue / caption (pale blue-grey, radio) | เสียงวิทยุ, take **R1** processed: leading 0.13 s trimmed, the ellipsis pause cut from 0.72 to 0.15 s, gaps tightened, tempo 1.3 with pitch kept (the band-limited radio hides the artefacts). Measured target: **"ศูนย์ครับ" 0.02-0.48 / "คนเจ็บ" 0.50-0.89 / "ไม่ตอบสนอง..." 0.89-1.70 / "เดี๋ยว!" 1.72-2.12 / "เฮ้ย!" 2.15-2.50**. The first caption is on screen from frame 0 |
| Sound | Rain on plastic and fabric, close and muffled (from 0.00); squelch open click 0.00; radio carrier hiss; voice band-passed 300-3000 Hz with dropouts; a wet scuffle thump under "เฮ้ย!"; **`radio_static_cut.wav` burst from 2.42 s swallows the tail of "เฮ้ย!"** and carries 3 frames over the cut. No music |
| Light | No key on this face of the radio (deep navy shade). The LED is emission with bloom. One red flash at 1.30 s (red point light pulse or radio-prop emission tint). Dark pixels far above the 8-15 % band, on purpose |
| Transition out | **Hard cut at 2.50 s on the static burst** (f59→60). The full rain roar slams in on the cut |
| Sets up | An unresponsive casualty and an attack on another unit: the pattern the viewer then watches happen here (shots 17-21) and again in Scene 02. The radio as Kong's kit (Scene 04). The bookend in shot 24 |

### Shot 02: red on wet asphalt, crane up

| Field | Plan |
|---|---|
| Time | 2.50-3.75 s, f60-89 (30 f), 1.25 s |
| Set / setup | expressway3d, `puddle_crane`: a lane between two stopped cars, near Kong's pickup |
| Framing / angle / lens | Starts at ground level, camera 0.25 D above a puddle, pitched down 10°, 22 mm. Ends low: 1.6 D, pitched up 8° |
| Camera move | **Frame 0 already moving:** crane-up snap of 12 frames (2.50-3.00, sine in-out) from 0.25 to 1.6 D, pitch -10° → +8°, revealing taillights stacked to the vanishing point in the rain. By 3.00 s the place reads. Then a slow eased rise with H1 |
| Cast | None (cars, rain, light) |
| Action | The red double flash lights the emissive smear decal in the puddle, and post splash rings break it up. Rain streaks cross the lens at three depths. A nearby car's wipers swing once (a keyed wiper on a background car model) |
| Dialogue / caption | None. The caption band is empty |
| Sound | `rain_heavy_road.wav` full and wide on the cut; a car horn held far left; the light-bar relay ticking; `sirens_city_far.wav` low |
| Light | Key from screen-left. Red decals pulse L-L-R-R. Taillights are small emissions blooming in the haze |
| Transition out | Hard cut on the rise (the next shot continues up the same axis) |
| Sets up | The red light bar as a moving light (rule 3; the siren in Scene 03). EP.1 colours in the first second of the world |

### Shot 03: the gridlock

| Field | Plan |
|---|---|
| Time | 3.75-5.75 s, f90-137 (48 f), 2.00 s |
| Set / setup | expressway3d, `wide_high`: above the shoulder beside the near light mast, looking along the lanes toward the city |
| Framing / angle / lens | Extreme wide, HIGH: 6 D above the deck, pitched down 18°, 22 mm. Pile-up of 3 cars in the middle ground, the pickup with its light bar at right, the gridlock fading into haze, the skyline card beyond. Kong is a 40 px head beside the hero sedan; the rescuer is at its driver door |
| Camera move | Eased push at 9 %/s plus a 0.3 D truck right (true parallax), H1. A constant-speed share so it never settles |
| Cast | **Kong** (tiny): standing, cutter in his right hand, head turning from the car to the queue (yaw +0.3 → -0.4 over 1 s), `determined`. **Rescuer** (tiny): at the driver door, working the Halligan bar in short strokes (0.6 s arm cycle) |
| Action | The scale of the night: one rescue unit against an endless jam. Hazard lights blink out of phase on the stopped cars |
| Dialogue / caption | None |
| Sound | Rain wide; two horns (left, then right); one far siren; the Halligan's metal screech, small, at 4.9 s (`car_door_pry.wav`, distant) |
| Light | Key from screen-right for this reverse view (`head_flip = True`); whole-figure shadows on the wet deck; red decals; haze from the mist pass |
| Transition out | Hard cut down the same axis into the low angle |
| Sets up | The jam (nowhere to drive: Scene 03 truck block). The rescuer already at the door, so "เปิดได้แล้ว" has a cause |

### Shot 04: Kong with the cutter

| Field | Plan |
|---|---|
| Time | 5.75-7.50 s, f138-179 (42 f), 1.75 s |
| Set / setup | expressway3d, `low_medium_K`: road level by the sedan's front wheel |
| Framing / angle / lens | Medium, LOW: 1.2 D above the deck, pitched up 15°, 22 mm. Head 200 px, centre 0.42 H. The crumpled hood is behind him; the light bar glows soft red (post depth blur) behind his shoulder |
| Camera move | Eased orbit 8° plus a push at 7 %/s, H2. At 7.20 a snap tilt down (11 f) toward the cutter, handing off to 05 |
| Cast | **Kong**: yaw -0.3, `determined`, legs `wide`, wet costume variant, `drip` on hair and sleeves. Right hand carries the cutter by its handle (`prop_r` spreader, one-handed). The left forearm wipes rain from his brow (one eased gesture, 10 f, at 6.3). Blink at 6.9. The crowbar shows in its side loop on the left of the pack; the radio is on the left shoulder; the watch is on the left wrist |
| Action | A tired, focused man at work |
| Dialogue / caption | None |
| Sound | Rain on his vest (close, crisp); the cutter's motor ticking as it cools; the Halligan screech off screen left |
| Light | Key from screen-left; tint pulses red on R-flash frames (`rim` on) |
| Transition out | Match cut on the tool (the tilt continues into 05) |
| Sets up | The cutter is Kong's (ownership). The crowbar loop at his hip (shots 16, 20, 23, Scene 02). His beard and vest for continuity |

### Shot 05: battery, three bars

| Field | Plan |
|---|---|
| Time | 7.50-9.00 s, f180-215 (36 f), 1.50 s |
| Set / setup | expressway3d, `insert_battery`: the cutter's status panel, a 3D prop pinned to Kong's `hand_r` |
| Framing / angle / lens | Raking insert at 0.5 D, a 20° rake along the panel, 22 mm. The bars are about 260 px wide at y 450-600, clear of the caption band |
| Camera move | Arrives braking inside the tilt (6 f), then an eased slide along the panel at 40 px/s with a 6 % push, H1 |
| Cast | Kong's gloved hand (sprite crop). **His thumb presses the status button at 7.80; the bars light 1, 2, 3, three frames apart (7.92, 8.04, 8.17)** (B). Rain beads run across the panel |
| Action | The tool is full and ready |
| Dialogue / caption | None: the 3 bars carry it |
| Sound | Button click; a three-step ready chirp in sync with the bars; rain drumming on the housing; the **hazard relay tick pre-laps from 8.80** |
| Light | Bars are green-white emission (small, bloom); the key rakes the plastic; drops catch the red flash |
| Transition out | Whip pan right (5 f off, 5 f on, streaked plate, actors sharp) |
| Sets up | **"ไฟแบต 3 ขีดใน EP.1"**: the battery as a visible countdown resource for later episodes |

### Shot 06: the door and the still driver (the threat planted)

| Field | Plan |
|---|---|
| Time | 9.00-11.00 s, f216-263 (48 f), 2.00 s |
| Set / setup | expressway3d, `door_eye`: the sedan's driver side |
| Framing / angle / lens | Medium two-shot, EYE level, 22 mm. Rescuer in the foreground at the door (head 210 px, x 260); the driver behind the rain-streaked side window (head about 150 px, x 470), slumped |
| Camera move | Whip-on braking over 5 f, then a slow push at 7 %/s toward the window, H2 |
| Cast | **Rescuer**: crouch 0.3, yaw -0.5, `determined`; the Halligan bar's fork in the door seam, two levering pulls (9.3, 10.1); `worried` behind a blink at 10.5 as the door will not give. White helmet, headlamp on. **Driver**: seated, slumped (`head_dy` +0.45, pitch +1.5, `head_roll` 25°, lean 40° forward), `infected_slump` (closed lines, slack mouth), seat belt across his chest. **Totally still: no blink, no breath** |
| Action | The driver is on screen 35 s before he moves. The window glass is intact: a holdout with a rain-run texture, plus the post rain sheet masked by its object ID. No breaking glass |
| Dialogue / caption | None |
| Sound | Halligan screech and metal groan; **the hazard relay tick, dry and close (1.5 Hz): the metronome that runs to the bite**; rain on the car roof |
| Light | Key from screen-left on the rescuer. The cabin is dark except the amber hazard tell-tale blinking on the dash (emission) and the driver card's tint pulsing amber at 1.5 Hz |
| Transition out | Hard cut on the first phone buzz (the buzz pre-laps at 10.80) |
| Sets up | The motionless driver; the tick; the door the rescuer is about to open |

### Shot 07: the buzz, a glance at the watch

| Field | Plan |
|---|---|
| Time | 11.00-13.00 s, f264-311 (48 f), 2.00 s |
| Set / setup | expressway3d, `mcu_K`: Kong at mark K2, 2.5 D from the sedan's rear quarter; the rescuer at the door deep behind him at screen left |
| Framing / angle / lens | Medium close, EYE level (0.3 D above head centre, 3° down), 22 mm. Kong's head 280 px at 0.44 H; the rescuer's head about 70 px at x 170 |
| Camera move | Opens on a snap tilt (12 f) from his chest pocket (the phone glow pulsing through the wet fabric) up to his face, then an eased drift right at 30 px/s, H2 |
| Cast | **Kong**: `determined` → the buzz → he glances down at his left wrist first (**the watch**, pitch +0.6, 11.4: C's guilt glance: he knows the time), then swaps to `worried` behind a blink at 11.8. His left hand pats the chest pocket and draws the phone up into frame (12.2-12.9, `prop_l` phone). **Rescuer** (background): still prying |
| Action | The private world breaks into the job |
| Dialogue / caption | None |
| Sound | `phone_vibrate.wav` in 0.4 s pulses against the vest; rain; the tick; the pry behind |
| Light | Key from screen-left; the phone glow as a cool tint lift on Kong's card for the last 10 frames (uniform tint, kept to 8 %) |
| Transition out | Match cut on the phone's rise into 08 |
| Sets up | The watch (Scene 02 INSERT and the 60 s rule). The phone lives in his left chest pocket (Scene 04, Scene 05) |

### Shot 08: "น้ำเหนือ, 4 สายที่ไม่ได้รับ" and the watch at 21:47

| Field | Plan |
|---|---|
| Time | 13.00-15.00 s, f312-359 (48 f), 2.00 s |
| Set / setup | expressway3d, `insert_phone`: the phone is a 3D prop (0.30 × 0.62 × 0.03 D) pinned to `hand_l`; the watch face on the same wrist at the lower right |
| Framing / angle / lens | Insert over his wrist, HIGH (camera 0.6 D above the screen, pitched down 50°), 22 mm. Screen about 380 px tall, centred at y 520; the watch face at (560, 760), above the caption band |
| Camera move | Eased push at 7 %/s plus a 6° orbit, H1. The phone vibrates ±2 px on each pulse |
| Cast | Kong's hand. At 13.6 his thumb wipes the wet screen once (10 f): the smear clears and the text reads sharp |
| Action | Screen state A (an SVG texture from code): the round contact photo of **Namnuea** (ponytail, maroon hoodie, `happy`), the name "น้ำเหนือ", a red badge **"4 สายที่ไม่ได้รับ"**, accept and decline buttons. Raindrops land and bead (post, registered to the screen corners). **The watch reads 21:47 and its red seconds hand steps once per second** |
| Dialogue / caption | No caption: the screen text is the line, and the caption band is left empty |
| Sound | Buzz close and loud; drops ticking on glass; rain ducked 4 dB; the tick continues |
| Light | The screen is emission (value about 1.2, slight bloom) and the brightest thing in frame; the watch crystal catches a red glint on R frames |
| Transition out | Punch-in cut to Kong's face |
| Sets up | The 4 missed calls and her face (Scene 05 "ครั้งนี้พ่ออย่าผิดสัญญานะ"). **The watch as a known object** for Scene 02 "INSERT: นาฬิกาข้อมือ เวลาผ่านไป" |

### Shot 09: he answers

| Field | Plan |
|---|---|
| Time | 15.00-16.75 s, f360-401 (42 f), 1.75 s |
| Set / setup | expressway3d, `cu_K_eye`: Kong at K2 |
| Framing / angle / lens | Close-up, EYE level, 22 mm at 2.4 D: head 320 px at 0.42 H |
| Camera move | Push-in at 6 %/s, H1, settling as the call connects |
| Cast | **Kong**: `worried`, looking down at the phone (pitch +0.6). **At 15.20 he shuts his eyes for 10 frames** (`sad` brows swapped behind the closed frame): the guilt beat. Eyes open, thumb up into frame bottom, accept at 15.85, phone lifted to his left ear (12 f, done at 16.35), head roll 8° toward it |
| Action | One breath before facing her |
| Dialogue / caption | Pre-lap: **N1 starts at 16.20; "พ่อ" 16.35-16.76** (pale blue-grey) |
| Sound | The last buzz cut short by the accept tone (15.85); his small exhale; rain ducks 4 dB and narrows (subjective focus on the call); line noise opens |
| Light | Key from screen-left; the phone glow fades off his card as the phone goes to his ear |
| Transition out | **Axial punch-in cut ×1.2 at 16.75**, on the tail of "พ่อ" (head 330 → 395 px). Not a dissolve: 09 and 10 share the setup and one sentence, so a dissolve would ghost his face into itself |
| Sets up | His habit of picking the job, which she names in shot 12 |

### Shot 10: "พ่อ วันนี้พ่อสัญญาว่าจะมารับหนูไง"

| Field | Plan |
|---|---|
| Time | 16.75-20.25 s, f402-485 (84 f), 3.50 s |
| Set / setup | expressway3d, `cu_K_eye` (same setup as 09); behind him, soft, the car and the rescuer working the door |
| Framing / angle / lens | Close, tightening to extreme close, EYE level, 22 mm: head 395 px at the cut → about 500 px at the end, centre 0.40 H (bottom of the head at y ≈ 760, above the caption band). **The watch on the wrist that holds the phone faces the lens**, red seconds hand ticking |
| Camera move | Slow push at 3 %/s, H1. **Snap reframe ×1.15 in 14 f on "สัญญา" (17.68)**, then the slow push resumes |
| Cast | **Kong** listening: phone at the ear; listener rule (under 0.04 D travel, mouth still). `neutral` → **blink-swap to `sad` on "สัญญา" (17.70)** (B): brows drop, pitch +1. A small swallow at 19.3 (2-frame squash 0.03 D). Drip falls from his hairline (3 drops over the shot). **Rescuer** (background, soft): two more levering pulls |
| Action | Her words land on his face; the job carries on behind him |
| Dialogue / caption (pale blue-grey, phone) | น้ำเหนือ (N1): **"วันนี้พ่อสัญญา" 16.96-18.04 / "ว่าจะมารับหนูไง" 18.04-19.96** |
| Sound | Her voice band-limited 300-3400 Hz but dry and intimate, with faint indoor room tone from her end; rain on his side -6 dB (never silent); the tick, low; the pry, far |
| Light | Key on his near cheek; red tint pulses, a little stronger on his right side (truck side) |
| Transition out | Hard cut on her breath out |
| Sets up | **"สัญญา"**: the word Scene 05 returns to |

### Shot 11: "พ่อมีเคสด่วนลูก รออีกแป๊บเดียว"

| Field | Plan |
|---|---|
| Time | 20.25-23.50 s, f486-563 (78 f), 3.25 s |
| Set / setup | expressway3d, `mcu_K` (the 07 setup, from the other side): Kong has half-turned away from the crash toward the barrier; the wreck and the rescuer at the door sit behind him in depth |
| Framing / angle / lens | Medium close, slightly HIGH (camera 0.6 D above head height, pitched 8° down), 22 mm. Kong's head 260 px at x 300, 0.45 H; the rescuer about 90 px at x 520, higher in frame. **The job is literally behind him while he makes the excuse** |
| Camera move | Slide left at 40 px/s with a 5 % pull-out, H1; one snap reframe ×1.2 at 21.90 on "รออีก" |
| Cast | **Kong**: `worried`, `talking` (mouth cycles from the take's loudness); a nod at 20.9; on "รออีกแป๊บเดียว" his right hand, still holding the cutter, lifts slightly in a small "wait" gesture (22.2, 9 f). **Rescuer** (background): **turns his head toward Kong at 22.6** (yaw +0.5, checking on him), then back to the door |
| Action | The excuse he has given before. On the last words (22.9-23.4) he takes two slow steps toward the Jersey barrier, which puts him on the `high_K` barrier mark (keep that mark within 1.5 D of K2) |
| Dialogue / caption (white, Kong) | ก้อง (**K1**, the same voice as K2, placed at 20.22): **"พ่อมีเคสด่วนลูก" 20.37-21.82 / "รออีกแป๊บเดียว" 21.90-23.34** |
| Sound | Kong dry and close; rain; the Halligan grinds once under his line; a far horn |
| Light | Key from screen-left; the wreck behind is lit harder than Kong (he turns into the dark) |
| Transition out | Hard cut |
| Sets up | The rescuer who will shout in 15; the teammate waiting on him |

### Shot 12: "ทุกครั้งเลย..." (the breath)

| Field | Plan |
|---|---|
| Time | 23.50-26.25 s, f564-629 (66 f), 2.75 s |
| Set / setup | expressway3d, `high_K`: Kong at the Jersey barrier in three-quarter profile, the jam below and behind him, rain sheets between him and the lens |
| Framing / angle / lens | Wide, HIGH (the angle for a man who has lost): camera 4 D above the deck, 6.5 D away, pitched 12° down, 22 mm. Kong's head about 120 px at 0.52 H; he is small against the jam |
| Camera move | The quietest move in the film: 6 % pull-out (sine), H1 reduced to 0.5 px. No snap |
| Cast | **Kong**: yaw -0.6, phone at the ear. On "ทุกครั้ง" he freezes; at 24.3 he blinks into `sad` with the eyes held closed for 20 frames, pitch +1. **The hand with the cutter sinks 0.1 D (the tool suddenly heavy).** The eyes open at 25.6 |
| Action | Nothing happens, on purpose: rain, red, a man with no good answer |
| Dialogue / caption (pale blue-grey, phone) | น้ำเหนือ (N2, placed at 23.55): **"ทุกครั้งเลย..." 23.76-25.30** |
| Sound | Her line; then the thin hiss of the open line under the rain; the rain bed comes back to full (the world presses in); one far siren rises and falls; the tick, faint at this distance. No music |
| Light | Key from screen-right (`head_flip = True`); his whole-figure shadow runs long across the wet deck; red flashes cross him and the barrier |
| Transition out | Dissolve 8 f |
| Sets up | "ทุกครั้ง": the pattern Scene 05 asks him to break |

### Shot 13: "เดี๋ยวพ่อโทรกลับนะ"

| Field | Plan |
|---|---|
| Time | 26.25-28.50 s, f630-683 (54 f), 2.25 s |
| Set / setup | expressway3d, `cu_K_low` (reused in 23) |
| Framing / angle / lens | Close-up, LOW (1.4 D, pitched up 8°), 22 mm at 2.3 D: head 330 px at 0.45 H. Rain against the lit mast above him; the rescuer at the door soft at screen right |
| Camera move | Push at 8 %/s, H1 |
| Cast | **Kong**: `sad` brows; `talking` on the line; **on the long "นะ" (27.31-28.27) a small `smile` mouth for 6 frames that fails, back to `wavy` behind a blink at 27.9** (B). Head roll 10° toward the phone. **Rescuer** (background): the door seam gives a little; he braces his foot on the sill |
| Action | A promise he means and cannot keep |
| Dialogue / caption (white, Kong) | ก้อง (K2, placed at 25.95; its 0.51 s lead-in is silence): **"เดี๋ยวพ่อ" 26.46-26.83 / "โทรกลับนะ" 26.83-28.27** |
| Sound | His voice soft; rain; one drip on the phone (a tiny click); the tick |
| Light | The red flash fills his face at 27.9, on the failed smile |
| Transition out | Hard cut |
| Sets up | The call-back that never happens (Scene 04 "ยังไม่มีสายจากลูก"; in Scene 05 she calls him) |

### Shot 14: silence on the line, the beep, the thumb that does not press

| Field | Plan |
|---|---|
| Time | 28.50-31.25 s, f684-749 (66 f), 2.75 s |
| Set / setup | expressway3d, `insert_phone` (the 08 build, camera from the other side so it is not a repeat) |
| Framing / angle / lens | Insert, EYE level to the screen, 22 mm at 0.45 D. Screen about 360 px tall, centred at y 540 |
| Camera move | Tilt down with the phone as it comes away from his ear (12 f, eased), then a slow push at 6 %/s, H0 (dead still drift for the silence) |
| Cast | Kong's hand |
| Action | Screen state B: "น้ำเหนือ" and the call timer counting **00:12, 00:13** (the real length of the call on screen). The line stays open in silence ("น้ำเหนือเงียบไป"). **29.60: the screen flips to "สิ้นสุดการโทร 00:13"** and her photo returns. **29.90: a raindrop lands on her photo and runs down across her face** (B). **30.30-31.10: his thumb rises and hovers over "โทรกลับ" and does not press** (C) |
| Dialogue / caption | None |
| Sound | The open line: thin hiss, **one small breath from her side at 29.0** (A), then **the single dry end-call beep at 29.60 (`beep.wav`): the only clean sound in the film**. Rain returns to full level on the beep. The tick continues. **"พี่ก้อง!" pre-laps at 31.12**: the thumb freezes on the shout |
| Light | Screen emission; the drop catches the red flash as it runs |
| Transition out | Hard cut at 31.25 (the shout is already 3 frames in) |
| Sets up | The broken promise, wordless: he chose not to call back. The photo under rain is the image Scene 05 echoes when her call drops ("สัญญาณขาด") |

### Shot 15: "พี่ก้อง! เปิดได้แล้วครับ!"

| Field | Plan |
|---|---|
| Time | 31.25-33.00 s, f750-791 (42 f), 1.75 s |
| Set / setup | expressway3d, `door_eye` (the 06 framing; now the door is open: a before-and-after rhyme) |
| Framing / angle / lens | Medium, EYE level, 22 mm at 4 D: rescuer's head 220 px at x 400, 0.45 H; the open door and the dark cabin at screen left with the slumped driver half seen past the pillar |
| Camera move | **Snap push ×1.4 in 12 f on "เปิดได้แล้ว"** (31.74), then settling, H2 |
| Cast | **Rescuer**: the door pops (hinge keyed 0 → 55° over 8 f at 31.25; he staggers back with it, squash and stretch); yaw +0.5 toward Kong (off right); `shouting` → `excited` (ring eyes, small grin) behind a blink at 32.5: the youngest one did it. Right arm `wave` (beckoning); the Halligan bar stays in his left hand. The headlamp beam (emissive cone card on his head anchor) swings with his head. **Driver**: still slumped, motionless |
| Action | The door is open; the job is back on |
| Dialogue / caption (white, rescuer) | เจ้าหน้าที่กู้ภัย (C1, placed at 31.05): **"พี่ก้อง!" 31.12-31.69 / "เปิดได้แล้วครับ!" 31.74-32.73** |
| Sound | Metal pop and hinge squeal; the shout bright and near; the hazard tick louder now that the door is open; a door-open chime from the dash, pinging once |
| Light | Key on the rescuer and the door; inside, only the amber hazard on the driver card and the headlamp beam |
| Transition out | Whip pan right toward Kong (4 f off, 4 f on, streaked) |
| Sets up | The headlamp: a moving light, which draws the infected (rule 3) once they are active; seen here, explained by nothing. The driver does not react to the shout or the pop: he has not come back yet |

### Shot 16: phone pocketed, he goes

| Field | Plan |
|---|---|
| Time | 33.00-35.25 s, f792-845 (54 f), 2.25 s |
| Set / setup | expressway3d, `track_K`: alongside the sedan, lane lines running to the car |
| Framing / angle / lens | Medium wide, LOW (1.0 D, pitched up 12°), 22 mm: head 160 px at 0.46 H; the wet deck in perspective fills the lower quarter |
| Camera move | Whip-on braking over 4 f, then a truck left of 2 D following Kong (eased), H2: the first time the camera walks with him |
| Cast | **Kong**: near-profile, yaw -0.9 (toward the car, screen left). **Slides the phone into his left chest pocket (33.15-33.65, 12 f: a deliberate beat on the pocket)**. Blink-swap `worried` → `determined` at 33.8 (the job face back on). Walks (head bob 0.47 D, period 16 f at 24 fps), the cutter in his right hand. **His left hand checks the crowbar in its hip loop as he goes** (a habit, 8 f, 34.6), not drawing it |
| Action | He chooses the job, again |
| Dialogue / caption | None |
| Sound | Boots in standing water ×4 (splash rings at the feet); vest rustle; rain; the tick ahead getting closer; the crowbar's small clink in its loop |
| Light | He walks into the key; his shadow runs ahead of him on the deck; red tint back to full amplitude |
| Transition out | Hard cut |
| Sets up | The phone in the pocket and no light from it again (Scene 04 "ก้องมองโทรศัพท์ ยังไม่มีสายจากลูก"). The crowbar within reach of his left hand (20, 23, Scene 02) |

### Shot 17: the rescuer leans in; the headlamp finds the driver

| Field | Plan |
|---|---|
| Time | 35.25-38.25 s, f846-917 (72 f), 3.00 s |
| Set / setup | expressway3d, `door_depth`: the camera **outside** the open door frame, beside the hinge, looking across the rescuer into the cabin |
| Framing / angle / lens | Medium two-shot in depth, EYE level, 22 mm. Rescuer nearer (head 240 px at x 230), leaning in, profile; driver farther (head 170 px at x 470), slumped, face hidden by pose (not by the wheel). Kong arrives in the deep background over the car roof at 37.0 (head about 90 px at x 600) |
| Camera move | Slow push through the door opening at 8 %/s, H1 falling to H0. The door frame and pillar pass at the edges (real occlusion, real parallax) |
| Cast | **Rescuer**: yaw -1.0 (profile), `worried`, a professional checking a patient. His head turns, so **the headlamp beam slides across the cabin and over the driver's face at 36.4** (B). His right hand starts to reach for the driver's shoulder (IK to a world point on the driver card, 37.0 onward) and has not touched it by the cut. **Driver**: motionless, **except a single 2-frame twitch of the hanging hand at 36.6, just as the beam crosses him** (B): the radio's "ไม่ตอบสนอง" becomes this body. The beam does not cause it (the shout and the door pop did not reach him either); he is coming back on his own, and the light only happens to be on him. **Kong**: arrives, `determined`, slows |
| Action | A routine check of an unconscious driver. The light moves; the body answers |
| Dialogue / caption | None (the screenplay gives the rescuer no line here) |
| Sound | Rain on the roof as a muffled drum; the hazard tick and the dash chime louder; the rescuer's breath; Kong's footsteps arriving; from 37.6 the rain bed starts to fall away (-18 dB over 0.6 s); a low sub drone rises (sound design, not music) |
| Light | Inside: amber hazard tint on the driver card at 1.5 Hz; the headlamp beam card; the red flash through the rear window as tint on both cards. Outside: the key on the rescuer's back |
| Transition out | Hard cut |
| Sets up | The twitch in the beam: the first sign he is coming back. The moving light on his face becomes his target in shot 21 (rule 3) |

### Shot 18: the driver lifts his head (the earned hold)

| Field | Plan |
|---|---|
| Time | 38.25-41.75 s, f918-1001 (84 f), 3.50 s |
| Set / setup | expressway3d, `windshield_cu`: camera on the hood, outside, looking in through the windshield. Glass is a holdout with a crack texture; the rain sheet is post, masked to the glass by an object-ID pass |
| Framing / angle / lens | Close-up on the driver, slightly LOW rising to EYE as he rises, 22 mm: head ends 340 px at 0.46 H. The rescuer's arm and lit helmet edge at the door gap, frame right |
| Camera move | A very slow push at 5 %/s that rises 0.3 D with his head, **H0**: dead steady for the first time, because the stillness is the threat |
| Cast | **Driver**: 38.25-39.00 still; **39.00-41.40 the head rises slowly** (`head_dy` +0.45 → 0, pitch +1.5 → -0.2, `head_roll` 25° → 4°, lean 40° → 5°, quintic ease, slow start; the torso follows at half amplitude). **Eyes stay closed (`infected_slump`); the grey head fill `#c5ccd6` reads in the amber blink: something is wrong.** A `drip` from his chin. Frame right, the rescuer's reaching hand pauses in mid-air |
| Action | "คนขับค่อยๆ เงยหน้าขึ้น": the last image of Scene 01, slow and unbroken |
| Dialogue / caption | None |
| Sound | The rain flattened to a hiss through glass; **only the hazard tick**, a wet creak of the seat as he rises; the sub drone holds |
| Light | The amber hazard blinks across his face from below (tint); **the headlamp beam rests on his face from 40.6** (tint lift); red flashes only from behind camera on R beats |
| Transition out | Hard cut |
| Sets up | The face that is about to change; the infected look for the series (grey fill, then blank ring eyes) |

### Shot 19: the rescuer's wrong relief

| Field | Plan |
|---|---|
| Time | 41.75-42.75 s, f1002-1025 (24 f), 1.00 s |
| Set / setup | expressway3d, `windshield_cu` reframed right onto the door gap (same anchor, new look-at) |
| Framing / angle / lens | Medium close on the rescuer leaning into the door gap, EYE level, 22 mm: head 260 px at 0.44 H; the driver's raised head is a grey edge at frame left |
| Camera move | Slight drift right at 20 px/s, H1 |
| Cast | **Rescuer**: yaw -0.4 toward the driver; `worried` → **a small relieved smile** behind a blink at 42.0 (A): brows up, mouth `smile`. He exhales; his hand lowers toward the driver's shoulder |
| Action | He thinks the man is coming round |
| Dialogue / caption | None (no line is added) |
| Sound | His relieved breath out; the tick |
| Light | Key on his face through the door gap; the headlamp beam points at the driver |
| Transition out | Hard cut. **The rain cuts out entirely on the cut for 6 frames** (A), leaving only the tick |
| Sets up | The cost of the next second |

### Shot 20: Kong senses it, his hand on the crowbar

| Field | Plan |
|---|---|
| Time | 42.75-44.00 s, f1026-1055 (30 f), 1.25 s |
| Set / setup | expressway3d, `cu_K_eye` (moved to mark K3, by the sedan's rear door, 3 D behind the rescuer) |
| Framing / angle / lens | Close-up, EYE level, 22 mm: head 340 px at 0.42 H; the rescuer's shoulder soft in the frame-left foreground (side view, not a back view) |
| Camera move | Eased push at 9 %/s, H1 rising to H2 |
| Cast | **Kong**: slows mid-step; `determined` → `worried` → `stunned` behind two blinks; head roll 12°. He sees the grey face beyond the rescuer. **His left hand closes on the crowbar's hook in the hip loop at 43.4** (C) |
| Action | His instinct is faster than his thought |
| Dialogue / caption | None (no added line) |
| Sound | Six frames with no rain (42.75-43.00), only the tick; then the rain returns at full; `heartbeat_low.wav` once, low; the crowbar's clink on its buckle |
| Light | Key from screen-left; full red flash on him at 43.5 |
| Transition out | Hard cut |
| Sets up | His hand already on the crowbar, so the Scene 02 push is not luck ("ห้ามความบังเอิญช่วยพระเอก") |

### Shot 21: the eyes open; the lunge; the bite

| Field | Plan |
|---|---|
| Time | 44.00-47.00 s, f1056-1127 (72 f), 3.00 s |
| Set / setup | expressway3d, `door_low`: low by the front fender, looking along the car at the open door; driver in the seat, the rescuer in the door gap |
| Framing / angle / lens | Starts as an **extreme close-up on the driver's closed eyes** (head about 520 px, i.e. the camera 1.5 D from his face, outside the car at the A-pillar beside the open door's hinge, about 0.3 D below his eye line, pitched up about 10°); a **crash dolly-out ×0.35 in 14 f** (to about 4.3 D, down to 1.2 D height, pitched up 15°) lands on the `door_low` medium (driver + rescuer in the door gap). 22 mm throughout, no lens key |
| Camera move | f1056-1063: on the closed eyes, H0 with a 3 %/s creep-in (**an 8-frame near-hold that is never fully static**, per the 6-frame rule). **f1064 (44.33): the eyes snap open with no blink.** f1065: one frame of total silence. f1066-1079: crash dolly-out, H3. f1080-1127: H3 with a recoil tilt as the rescuer is driven back, decaying to H2 by f1118 |
| Cast | **Driver**: hard swap to `infected` (pupil-less ring eyes, dark lids, wide mouth with teeth, a dark stain at the lip corner): no in-between. Lunge, jump-scare timing: squash 2 f (f1066-67), launch 2 f, airborne 2 f, **contact f1072 (44.67 s)**. The card slides 0.8 D out of the door gap; hands to the rescuer's shoulders (IK to the rescuer card's shoulder anchors); his head drops into the rescuer's left shoulder (roll 30°) and holds. **Rescuer**: `shocked` for one frame, then `shouting` (eyes squeezed, `mouth=("open",0.30,0.20)`); body pushed back (lean -25°), knees buckling (crouch 0.3); **the Halligan bar drops** (a rigid prop card falling to the deck, 46.0). **The bite is hidden behind the door pillar and the driver's own head**; a dark smear `#3a0d14` appears on the orange shoulder on the contact frame. No gore |
| Action | "คนขับพุ่งเข้ากัดเจ้าหน้าที่กู้ภัย" |
| Dialogue / caption | None. The scream is not captioned |
| Sound | f1064 a wet click as the eyes open; f1065 total silence; f1066 `zombie_lunge.wav` plus a car-body thud; contact f1072: a muted impact, then **`man_scream_bite.wav`** raw and close; the Halligan's clang and splash (46.0); the rain slams back; `car_alarm_far.wav` starts down the jam; **the hazard tick keeps going, absurdly calm** |
| Light | **The light bar's R-R double flash is re-timed to land on f1066-1067; those 2 frames are pushed to red in the grade** (the film's one flash, in EP.1 colours). The headlamp beam whips across frame as his head is thrown back |
| Transition out | Hard cut mid-scream |
| Sets up | The bite: rule 1, the 60 s clock (the watch, Scene 02); the speed of the infected (rule 2); he goes for the moving headlamp and the voice at the door (rule 3) |

### Shot 22: the scream in the rain

| Field | Plan |
|---|---|
| Time | 47.00-48.75 s, f1128-1169 (42 f), 1.75 s |
| Set / setup | expressway3d, `door_low` reframed (same anchor, tighter look-at on the rescuer) |
| Framing / angle / lens | Medium close, LOW, 22 mm: the rescuer's head 300 px at 0.45 H, pinned against the door frame; the driver in profile at frame left, his grip on the rescuer's vest and his head at the shoulder |
| Camera move | H3 decaying to H2; a slow 5 %/s push |
| Cast | **Rescuer**: alive, `shouting`, head thrown back (pitch -0.8), **his right hand clamped over the wound on his left shoulder** (A), helmet askew, the headlamp pointing at the sky. **Driver**: still on him (arms gripping, head at the shoulder, small worrying shakes, 2 f each); he does not let go and does not stand |
| Action | "เสียงร้องท่ามกลางสายฝน": the rain hammers both of them |
| Dialogue / caption | None |
| Sound | The scream full and cracking over the rain (second half of `man_scream_bite.wav`, extended with a reversed-tail crossfade); a far siren rising; the tick; the car alarm |
| Light | Red flash on R beats (tint + rim); the key from screen-left; rain lit white in the headlamp beam |
| Transition out | Hard cut |
| Sets up | The wound on the left shoulder (continuity: Kong presses it in Scene 02). He must still nod and say "พี่...ผมหนาว" |

### Shot 23: Kong rips the crowbar free (the last image)

| Field | Plan |
|---|---|
| Time | 48.75-51.75 s, f1170-1241 (72 f), 3.00 s |
| Set / setup | expressway3d, `cu_K_low` (the 13 setup moved to K3: the same face that made the promise, now in horror) |
| Framing / angle / lens | Close-up to extreme close-up, LOW (1.4 D, pitched up 16°), 22 mm: head 330 → 430 px, centre 0.42 H. Rain against the lit mast above him; the light bar soft red behind |
| Camera move | H3 for the first 14 f, decaying to H2; **snap push ×1.6 in 18 f from 50.40**, still moving on the last frame |
| Cast | **Kong**: 48.75-49.5 `shocked` (ring eyes, 0.033 pupils, `drip`), a 2-frame squash on the scream; frozen for 18 frames only. **49.6 a blink into `determined`, then `angry` at 50.0** (heavy brows, pitch -0.6): the rescuer in him overrides the fear. **50.1-50.9: his left hand rips the crowbar out of its hip loop and swings it up across his chest into the foreground** (prop swap from costume element to `prop_l` crowbar hidden in the motion streak; a large card 0.9 D long across the lower right by 51.2). The watch on that wrist flashes past the lens. Weight shifts forward (lean 12°). The cutter is still in his right hand |
| Action | The end of the hook. We do not see the crowbar used: the screenplay's next beat ("ก้องใช้ชะแลงผลักผู้ติดเชื้อออก") is the next part |
| Dialogue / caption | None |
| Sound | The scream from frame left (directional), rising; rain at full; Kong's breath; the crowbar scraping free (50.2); an unpitched rumble building (sub + noise, no melody; `hit_trailer.wav` low-passed) that peaks on the swing; **everything cuts dead at 51.75 with the picture** |
| Light | Full red flash on the card (tint peak + rim) alternating with the cool key; bloom on the light bar |
| Transition out | **Smash to black at 51.75, mid-move, on the scream's peak** |
| Sets up | Scene 02's push with the crowbar; Scene 04's kit; Scene 06's last image "ก้องยกชะแลงขึ้น" (the hook ends on the gesture that ends the episode) |

### Shot 24: black; the radio bookend

| Field | Plan |
|---|---|
| Time | 51.75-53.25 s, f1242-1277 (36 f), 1.50 s |
| Set / setup | None (black) |
| Action | Black. f1242-1249: 8 frames of total silence. **f1250: the radio squelch from shot 01 opens on its own**: carrier hiss, a burst of voiceless static (no words, no new event), and the squelch closes at 53.00. Silence to the end |
| Dialogue / caption | None |
| Sound | As above (`radio_static_cut.wav` reversed into its open, then the squelch click) |
| Transition out | End |
| Sets up | The next part: the radio that opened the film is still open, and nobody is answering. **Title card:** none in the default cut. The screenplay places "TITLE CARD: DEAD ZONE 09" after the aerial shot at the end of Scene 02. **Standalone-post variant only:** append 2.00 s of C's title card ("เขตปิดตาย 09 / DEAD ZONE 09", red `#c8202a` "09" as in the character-sheet logo, a 6-frame flicker-in like a failing light bar, a 3 %/s drift) under the squelch; total 55.25 s. Needs the owner's approval |

---

## Screenplay faithfulness check

| Screenplay beat (Scene 01 + Scene 02 beat 1) | Shot | Note |
|---|---|---|
| จอดำ; radio: "ศูนย์ครับ คนเจ็บไม่ตอบสนอง... เดี๋ยว! เฮ้ย!" | 01 | Near-black macro instead of pure black; every word verbatim |
| เสียงวิทยุขาดหาย | 01 | The static burst kills the line; the cut comes on it |
| CUT TO: red emergency light reflected on the road; multi-car crash; gridlock out of sight | 02, 03 | Red on the asphalt is an emissive decal |
| Kong beside the damaged car holding the cordless cutter; battery 3 bars | 04, 05 | He holds it himself, all the way to the cut |
| Phone vibrates; "น้ำเหนือ — 4 สายที่ไม่ได้รับ"; Kong answers | 07, 08, 09 | |
| น้ำเหนือ: "พ่อ วันนี้พ่อสัญญาว่าจะมารับหนูไง" | 09-10 | verbatim |
| ก้อง: "พ่อมีเคสด่วนลูก รออีกแป๊บเดียว" | 11 | verbatim |
| น้ำเหนือ: "ทุกครั้งเลย..." | 12 | verbatim |
| ก้อง: "เดี๋ยวพ่อโทรกลับนะ" | 13 | verbatim |
| น้ำเหนือเงียบไป ก่อนวางสาย | 14 | silence, breath, end-call beep |
| เจ้าหน้าที่: "พี่ก้อง! เปิดได้แล้วครับ!" | 15 | verbatim |
| ก้องเก็บโทรศัพท์ | 16 | a deliberate pocket beat |
| The rescuer approaches the driver, who sits motionless | 06, 17 | motionless from 9.0 s |
| คนขับค่อยๆ เงยหน้าขึ้น | 18 | the earned hold |
| (Scene 02) คนขับพุ่งเข้ากัดเจ้าหน้าที่กู้ภัย | 21 | the bite is hidden, no gore |
| เสียงร้องท่ามกลางสายฝน | 21, 22, 23 | the rescuer alive; the driver still on him |
| Not shown (left to the next part) | — | Kong pushes the infected off with the crowbar; "มองหน้าพี่ไว้!"; the 60 s turn; the title card |

**Wordless additions** (none changes an event): the red flash on the radio (01); the thumb press on the battery (05); the hazard tick (06-23); the watch glance and the watch at 21:47 (07, 08, 10); the wiped screen and her contact photo (08); the failed smile (13); the call timer, her breath, the drop on her photo and the thumb hovering over "โทรกลับ" (14); the crowbar check, grip and draw (16, 20, 23); the headlamp beam and the hand twitch (17); the rescuer's relief smile (19); the rain dropout (19-20); the voiceless squelch over black (24). **No added lines.**

---

## Assets to build

### Set (1): `v3/set3d/expressway3d.py` (new; office3d pattern: 1 unit = 1 D ≈ 0.58 m, artwork from code, anchors and setters)

1. **Deck:** 3 lanes + shoulder, 26 D wide, 60 D modelled, low-poly to 160 D into mist. Wet asphalt texture (slate, lane lines, puddle patches, painted streak highlights); puddle zone for `puddle_crane`.
2. **Jersey barriers** both sides, reflectors as small emissions; sound-wall railing one side.
3. **2 LED light masts** with emissive heads (bloom); the near one motivates the key.
4. **Hero sedan** (grey-blue): crumpled hood, glass on the deck, cracked windshield texture; setters `door(angle)` (driver hinge), `hazard(t)` (amber tell-tale emission and phase for the driver tint), `chime()` (cue only). Minimal interior: seat, steering wheel ring, dash plane. Windshield and side window as **holdout glass with an opacity/crack texture** and an object-ID for the post rain mask.
5. **Pile-up:** 2 more crashed cars from the gridlock models with a crumple texture.
6. **Kong's rescue pickup:** orange-white, "กู้ภัย" livery, closed equipment-compartment doors (Scene 03/04); light bar as emissive red pods + setter `lightbar(t)` (2 Hz L-L-R-R, returns phase for actor tints); optional one red point light with shadows off.
7. **Gridlock:** 3 low-poly models (sedan, SUV, van) × 4 colourways, instanced about 40 times; taillights and hazards as emission texture swaps; one background car with a keyed wiper (shot 02).
8. **Skyline backdrop card** (navy towers, sparse windows, red aircraft beacons) and an overhead gantry with a green "ทางพิเศษ" sign.
9. **Road reflection decals:** emissive red smear decals under and behind the pickup and in the shot-02 puddle, pulsing with `lightbar(t)`; soft white smears under the masts.
10. **Anchors:** marks K1 (wide), K2 (call position by the rear quarter), K3 (rear door), the barrier mark for `high_K`, R1 (rescuer at the door), DRV (driver seat card plane). **15 camera setups:** `insert_radio`, `puddle_crane`, `wide_high`, `low_medium_K`, `insert_battery`, `door_eye`, `mcu_K`, `insert_phone`, `cu_K_eye`, `high_K`, `cu_K_low`, `track_K`, `door_depth`, `windshield_cu`, `door_low`. None is inside the cabin.

### Puppets: `v3/cast/cast_dz09.py` (new, cast_ext pattern; `puppet.py` not edited)

| Cast | Design (from `uploads/character_sheet.webp`) | States, expressions, poses |
|---|---|---|
| `kong` | Strong regular build, about 3.1 D; spiky black hair; stubble (new face extra `stubble`); orange reflective "RESCUE" vest/jacket with grey bands; Thai flag patch on the near sleeve; black cargo trousers; boots; backpack straps; **radio on the left shoulder strap** (anchor `radio`); **watch on the left wrist** (costume key, red seconds hand); **crowbar in a side loop on the left of the pack, hook at hip height** (costume element until drawn); left chest pocket | Wet variant only (fills ×0.85 value, 2-3 highlight streaks, `drip`). Expressions: determined, neutral, worried, sad, talking, stunned, shocked, angry, plus the failed small smile (`sad` brows + `smile` mouth). Poses: carry cutter (right), wipe brow, pat pocket, phone at chest, phone at ear (left), "wait" gesture, walk, check and grip the crowbar hook (left hand down and back), draw and swing the crowbar |
| `rescuer` | Younger and slimmer, about 2.95 D, no beard, rounder eyes; the same orange RESCUE vest over a dark long-sleeve shirt (reads as a teammate); **white helmet with headlamp** (anchor `lamp` for the beam card); grey gloves | Expressions: determined, worried, shouting, excited, shocked, relieved smile. Poses: lever the Halligan, crouch at the door, wave, lean in and reach (IK to the driver), pushed back and buckling, hand clamped on the left shoulder, head thrown back |
| `driver` | Ordinary commuter, about 3.0 D, stout-regular: rumpled pale-blue office shirt, loose navy tie, ID lanyard, seat-belt ribbon; no glasses or suit (never reads as คุณทศ); wet hair over the brow | **New, registered by the extension:** `infected_slump` (closed lines, slack mouth); `infected` (pupil-less ring eyes, dark grey lids, wide mouth with teeth, no brows, dark lip-corner stain); **grey head-fill key `#c5ccd6`**. Seated pose (legs hidden by sill and dash; `crouch` 0.6, feet forward). Poses: slumped, head lift, hand twitch, lunge (squash/launch/air/land), grip, bite (head into the shoulder) |
| `namnuea` | Head and hoodie collar only, drawn once for the contact photo: ponytail, maroon hoodie, `happy` | Prop texture (the full puppet comes in Scene 05) |

All three full puppets: canvas entries in `sprites.DEFAULT_CANVAS` (check `canvas_for` for the crowbar swing and the lunge), night tint `#dfe4ff`, ink `#1e142e`, `rim` support for the red flash.

**New in the cast extension (they do not exist in `puppet.py` today):** (a) the **`drip` effect** (2-3 water drops falling from hairline, chin, sleeve or antenna, `t` loop; added to `FX_TYPES` and the `_fx_spec` dispatch from `cast_dz09.py`), used in shots 01, 04, 10, 18, 23; (b) the **wet costume variant** (fills ×0.85 value plus 2-3 highlight streaks) for all three; (c) the **per-cast head fill** (the module constant `HEAD_FILL` is global, so the driver's grey `#c5ccd6` needs a hook in the head drawing keyed on the cast being drawn); (d) the **rescuer's wound states**: the dark `#3a0d14` shoulder smear (from f1072) and the helmet knocked askew with the lamp anchor following it (shot 22); (e) the expressions `infected_slump` and `infected` added to `EXPRESSIONS` with their eye and mouth drawings.

### Props (new prop types in the cast extension, plus 3D insert props in the set)

1. **Cutter/spreader** (`prop_r`, one-handed carry) + 3D insert version with the status panel (`led` 0-3 bars, button).
2. **Crowbar** (costume element in the hip loop → `prop_l`, 0.9 D, dark red-black, hooked end).
3. **Phone** (`prop_l` + 3D insert prop, 0.30 × 0.62 × 0.03 D): SVG screen states A (incoming, photo, "น้ำเหนือ", badge "4 สายที่ไม่ได้รับ"), B (in call, timer 00:12-00:13), C ("สิ้นสุดการโทร 00:13", "โทรกลับ" button). Thai UI set in a free Thai OFL face.
4. **Shoulder radio** (3D insert prop pinned to `shoulder_l`): grille, antenna, red TX LED driven by the R1 envelope.
5. **Wristwatch** (costume detail + legible in 08 and 10: 21:47, red seconds hand stepping every 24 frames).
6. **Halligan pry bar** (rescuer `prop_l`; falls as a rigid card in 21).
7. **Headlamp beam** (emissive additive cone card on the rescuer's `lamp` anchor, no light).

### Effects and post

- **P1 Z/mist pass:** `stage/render.py` does not write one today. Add a depth/mist output (a small addition in a new module or behind a flag) and an object-ID pass for the glass. Everything below depends on it.
- **Rain:** 3 post streak layers (near, mid, far; 8° wind slant; speed by depth), each occluded at its own depth by the Z pass; brightness keyed to the key and the light-bar phase (red streaks on flash frames); streak length from `post.py`'s fitted camera motion.
- **Splashes:** ring and crown sprites projected on the road plane with the true camera (about 60 live in wides, 15 in close shots); at Kong's feet in 16.
- **Drops on glass:** registered to the projected corners of the radio (01), the battery panel (05), the phone (08, 14) and the side window and windshield (06, 18, masked by object ID).
- **Depth haze and soft backgrounds:** mist toward `#1b2440`; a post depth blur in place of DOF.
- **Puppet light fakes:** per-frame `tint` curves from `lightbar(t)`, `hazard(t)`, the headlamp beam and the phone; `rim` on R frames.
- **Handheld generator:** H0-H3 keyed into the camera before render.
- **Streaked plates:** `render_layers.py` and `post.py` on the 2 whips, the crash dolly-out (21), the snap pushes (01, 10, 11, 15, 23) and the crowbar swing.
- **Red flash:** 2 frames graded to red (f1066-1067).
- **Captions:** `assemble.py`, Kanit Black, the two caption colours.

### Audio (no paid API; no new generation)

- **Voice (on disk):** R1 (edited and tempo 1.3 as in shot 01), N1, K1, N2, K2, C1 (K1 not K1b: K1b is another voice and Kong must sound the same in shots 11 and 13). The phone filter (300-3400 Hz + her room tone) and the radio filter (300-3000 Hz, crackle, dropouts) are made locally. The driver's throat creak and the rescuer's exhale come from CC0 sources or a local recording.
- **SFX (on disk):** rain_heavy_road, rain_on_hood (inside-car drum), radio_static_cut, phone_vibrate, car_door_pry, hydraulic_cutter (cooling tick), heartbeat_low, zombie_lunge, man_scream_bite, sirens_city_far, car_alarm_far, hit_trailer (low-passed sub only), `beep.wav` (end call).
- **To synthesise locally (numpy or sox) or source CC0:** hazard relay tick (1.5 Hz), light-bar relay tick (shot 02), squelch open and close clicks, accept tone, battery button click and ready chirp ×3, door-open dash chime, Halligan clang, door pop and hinge squeal, boots in water, crowbar scrape and clink, seat creak, sub drone, car horns (shots 02, 03, 11), drops ticking on glass and the drip click on the phone (08, 13), wet scuffle thump under "เฮ้ย!" (01), Kong's exhale and breaths (09, 23), the eye-open wet click, car-body thud and muted impact (21). All cues are placed by frame in `sfx_cues.json`.

---

## Budget and gates

| Part | Frames | Est. CPU s / frame | CPU s |
|---|---|---|---|
| 3D picture shots 01-23 | 1242 | 15-17 (12 samples, direct light only, 1 shadowed sun + at most 1 shadowless red point) | ≈ 19,900 |
| Dissolve handles (1 dissolve, both sides) | 8 | 16 | ≈ 130 |
| Plate and matte passes for streaked frames | ≈ 90 | 8 | ≈ 720 |
| Sprites (at most 3 actors per frame) | — | — | ≈ 250 |
| Post: rain, splashes, drops, haze, depth blur, grade (≈ 1.0 s/frame) | 1278 | 1.0 | ≈ 1,280 |
| Captions, mix, encode | — | — | ≈ 150 |
| **Total** | | | **≈ 22,400 CPU s ≈ 6.2 CPU h ≈ 1.6 h wall on 4 cores** (17.5 CPU s per final frame against 18 s) |

**Gates before the full render**
1. 24 fps conversion of every frame constant in `timing.py`, `film.py`, `post.py` and the QA thresholds (seconds × FPS) comes first. Check with `qa_motion.py` using converted thresholds.
2. Time 3 frames each of `wide_high` (03: the most geometry), `windshield_cu` (18: glass) and `door_depth` (17: cards next to car surfaces). If any is over 18 CPU s, apply in this order: (a) glass as a pure holdout with opacity, (b) the red point light off (decals and tint only), (c) render `wide_high` at 540x960 and upscale with Lanczos.
3. Stage with `probe.py` before rendering: head sizes, head centre 0.35-0.59 H, whole heads above y 880, registration error 0 for the pinned phone, battery, radio, the Halligan fork and the crowbar hook; IK `error` under 0.01 for the crowbar grip and draw, the phone at the ear and the rescuer's reach.
4. Check the infected faces (`infected_slump`, `infected`, the grey fill) on their own sheet before animating.
5. `hue_report.py` on each batch: expect it to flag the night frames (see risk 6). Judge on a sheet against the EP.1 grammar and record the numbers with the reason.

---

## Prototype cut (first 5 s)

**Build first: shots 01, 02 and 03** (0.00-5.75 s, f0-137, rendered in full so the 03 cut can be judged; the prototype is reviewed at 0.00-5.00 s, f0-119).

| Shot | Time in the prototype | What it proves |
|---|---|---|
| 01 radio in the dark | 0.00-2.50 | The near-black hook holds: R1 edited and at tempo 1.3 with "เฮ้ย!" by 2.15 s; captions from frame 0; LED keyed to the envelope; the 1.30 s red wash; the snap push onto the LED; drops on the grille; the static-burst cut at 2.50 |
| 02 red on wet asphalt | 2.50-3.75 | The emissive puddle decal + post splashes read as a red reflection; the 12-frame crane-up reveals the gridlock by 3.00 s; post rain occluded by the new Z pass |
| 03 the gridlock (first 1.25 s in the 5 s review) | 3.75-5.00 (full shot to 5.75) | The expressway set, the instanced jam, the light bar, the mist haze, and two tiny acting puppets (Kong turning his head, the rescuer prying) with whole-figure shadows on the wet deck; the render-time gate for `wide_high` |

The prototype therefore exercises the riskiest new pieces at once: the 24 fps conversion, the new set, the Z/mist pass and post rain, the emissive decals, the light-bar tint on cards, the radio edit, the Kanit captions in two colours and the first 3-second retention test. Measure retention on a real phone in daylight before building shot 04 onward.

---

## Risks (honest)

1. **30 fps pipeline.** `timing.py`, `film.py`, `post.py` and the QA tools hard-code `/30` and the reference grammar in 30 fps frames. Until every constant is in seconds × FPS, a 24 fps render drifts. This is the first job.
2. **The radio line forces a 2.50 s cut, not 2.25.** The R1 take is 4.13 s raw. Even edited and at tempo 1.3, "เฮ้ย!" starts at about 2.15 s. If the edited take measures longer, either raise the tempo to 1.4 (radio band-limiting hides most artefacts) or let "เฮ้ย!" and the static carry over the cut into shot 02. The second option bends "จอดำ" slightly and needs the owner's OK. A dark first 2.5 s can still lose swipers on a dim phone; the fallback is lifting the radio shade to about V 0.12.
3. **No night exterior exists yet.** `expressway3d` is the largest single build (about 45 objects, 40 instances, glass, decals, a light bar). The render estimate scales from the office set (about 5 s per frame there) and is untested here. Hence the gates.
4. **Cards are never lit.** The red flash, hazard amber, headlamp and phone glow on the puppets are uniform per-frame tints plus a red rim. They may read as a colour filter rather than light from a direction, especially the headlamp "finding" the driver's face in 17-18. Judge on a still sheet against the set before the full render. A gradient tint would need a small extension to the sprite page.
5. **Post rain and glass.** The Z pass handles cars and actors, but rain under the pickup's overhang or inside the cabin may show. Mask the glass with the object-ID pass and keep inserts sparse. Splash projection assumes a flat deck.
6. **Colour band.** The LOOK_SPEC hue and value band was measured on daylight interiors. This night exterior will run bluer and darker on purpose (value about 0.25-0.35, blue over 45 %, 25-40 % of pixels under V 0.25, 70-85 % in shot 01). `hue_report.py` will flag every shot; the EP.1 grammar wins, and the numbers are reported with the reason.
7. **The infected faces may read as comic.** The stickman vocabulary is comic in origin. The scare must come from timing (the 8-frame hold, the no-blink swap, 1 frame of silence, the red double flash) and sound, not from the drawing. Review the drawings alone first.
8. **The bite is a contact between two cards.** The driver's card moves 0.8 D through the rescuer's plane, and a `depth_bias` order switch mid-move can pop. It is covered by the door pillar, the driver's head, H3 and the 2 red frames, but a frame-by-frame review may still catch it. Fallback: draw both figures into one combined sprite for f1070-1100.
9. **Cards next to the car.** The driver sits close to the door, dash and pillar (stage trap 3). Use `yaw_fixed` for his card, keep camera yaw under 30° off it (`door_depth`, `windshield_cu`, `door_low` are planned inside that), and let the sill and dash hide the legs. No back views anywhere; the bite stays in profile.
10. **IK reach.** Phone at the ear with the watch facing the lens, the crowbar hook at the hip, the draw and swing, and the rescuer's reach to a world point are all near the 0.74 D arm. Probe each with `probe.py` before blocking. The new prop types (cutter, crowbar, phone, Halligan) do not exist yet.
11. **Voice performance.** The takes on disk are TTS and were generated earlier (no new calls are made). Kong's two lines must come from one voice (K1 + K2; K1b was another voice). They may lack the guilt in "รออีกแป๊บเดียว" and the drawn-out "นะ" that the failed smile depends on. Re-time acting and captions to the final mix. A recorded human take can replace any line without changing the plan (the times move with it). The scream is a library SFX.
12. **Crowbar continuity with Scene 04.** The crowbar rides on Kong's pack (it earns the Scene 02 push). Scene 04 has him choose a ชะแลง (and the cutter) from the truck compartment. Flag this to the screenplay owner: either he restows his kit when he runs back to the truck in Scene 03, or Scene 04 shows a second bar. The hook leaves the cutter in his right hand and the crowbar in his left at the cut; the Scene 02 staging must decide where the cutter goes when he drags the rescuer back.
13. **Pacing risk in the call.** The call runs 15.0-31.25 s. The threat stays in frame or in the ear (the rescuer in depth in 07, 10, 11 and 13, the hazard tick, the driver planted at 9 s), but the breath shot (12) is still the likeliest dip. A cut-down saves 0.75 s without losing a line: trim 12 to 2.25 s and 14 to 2.50 s.
14. **Wet look.** Drips and darker fills may not read as soaked at 40-160 px heads. If the wides read dry, add constant thin highlight streaks on hair and shoulders.
15. **Title card.** The default cut has none (faithful). If the hook is posted alone without one, the brand may not register. The standalone variant (shot 24) moves the card ahead of its screenplay place and needs the owner's approval.
16. **Thai type.** Kanit Black is in `fonts/`. The phone UI needs a lighter Thai face (Sarabun or Noto Sans Thai via `@fontsource`, free, offline). Check tone-mark stacking in Chromium for "เดี๋ยว", "ก้อง" and "แป๊บ".
