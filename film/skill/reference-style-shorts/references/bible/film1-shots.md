# Film 1 shot by shot: a complete worked example

The rules in brief:

1. Film 1 ("the Storm Expressway") is 26 shots in 65.4 s of narration (1965 film frames at 30 fps, 720x1280), cut from 23 takes (s04-s26, one per shot) plus the 3-shot opening (hook takes A and B): 25 takes in all. Every shot is true 3D (office, beach, kitchen); the flat compositor only adds textures and overlays.
2. One clock rules everything: the narration wav is laid at +0.100 s. A shot boundary at clock t0 is film frame round(t0 x 30), so the picture leads its first word by 3 frames. An in-shot event at clock x is film frame round((x + 0.1) x 30). Sound cues are written in film seconds (clock + 0.1).
3. Each shot is built on one caption phrase group and one story-formula element, with one named framing, one move class (drift or snap) and at least one prop or set device firing on a word.
4. Shots change framing about every 1.26 s (plan count; the picture tool reads 1.06-1.09 s). That is busier than both references (A 1.39 s, B 1.62 s by the same tool): next time aim at 1.3-1.4 s.
5. Callbacks carry the story: the gloat framing G (10, 18, 25), the beach framing (16, 23), the table framing (15, 26), the corridor view (9, 19, 20, 22) and the forecast words on three papers (14, 15, 26).
6. Imitate first the shots the reviews rated closest: 3, 17, 10, 2, 8, 13, 26, 24 (section 3.3). Avoid the patterns of 16, 21, 20, 19, 7, 5: cold explainer diagrams, empty sky, tiny grey props, full-frame smears.
7. Where the plan and the take differ, this chapter describes the take (what the film shows) and gives the plan value beside it.

Pictures (graded final frames without captions, `out_v11/graded/`, sharp, the picture of `deliver/film_v1_1_sharp_thai.mp4`, one per shot, labelled with shot, film frame, time, set and light, camera class and name):
- `../../assets/bible/film1_shots_1.jpg`: shots 1-13.
- `../../assets/bible/film1_shots_2.jpg`: shots 14-26.

How to read an entry:
- **Times.** "clock" = narration clock (as the plan and the takes write them). "film" = clock + 0.100 s. "g" = 0-based film frame. Shot ranges are g0-g1 inclusive.
- **Captions.** Each phrase is shown with its delivered clock times from `audio/th/full_v2/narration_timing.json` (the second, delivered voice). The plan was cut to an earlier fit of that file; where the delivered phrase starts more than 0.05 s away from the cut, the entry says so.
- **Heads.** Outer head width in px at 720x1280, from each take's per-frame render meta.
- **Colour row.** `v3/tools/hue_report.py` share of chroma in percent: red / orange / blue / violet / magenta, then sat, val, dark. Rows are the v1 film frames per shot (`deliver/QA_film.md` 1.4, caption band excluded). Target band (office interiors): red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15. The v1.1 row is given where the v1.1 review or `GRADE.md` measured it.
- **Reviews.** v1 = `deliver/QA_film.md` section 3. v1.1 = `deliver/QA_film_v1_1.md` section 2 (it reviewed a v1.1 cut that carried an added background blur; the client had that blur removed, so the review's remarks on background softness are left out here). "Fix round" = the grade repair made after that review (`v3/film/out_v11/grade.py`).
- **Polish.** What the v1.1 grade (`v3/film/out_v11/grade.py`) did to the shot. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. The motion streak on fast moves (whips, snaps, crash moves) is part of the style and stays.
- **Sound.** "Cues" = the take's `cues.json` (film seconds). "In the mix" = the entries actually placed (`v3/film/out/SOUND.md`, numbered as there). Many cues had no fitting library sound or were thinned; one music bed (`music_fit.wav`, -38 dBFS) runs under the whole film, so the music cues in the lists are intent, not separate tracks.
- **Runner.** The module a take's `shot.py` imports to build, render and QA it.
- **Bundled or not.** The skill bundles the opening (`v3/shots/film.py`, `timing.py`) and nine takes: s10, s11, s13, s14, s17, s19, s20, s24, s26 (`pipeline/v3/film/sNN/`), with the runners `s10/otake.py`, `s14/otake.py`, `s17/otake.py`, `s20/mc.py`, `set3d_ext/beach/bshot.py`, `set3d_kitchen/kshot.py`. The other takes (s04-s09, s12, s15, s16, s18, s21-s23, s25, and `s04/otake.py`) exist only in film 1's project: their files (`grade12.py`, `make_blot.py`), take constants (`FLY`, `FLIGHT`, `ORBIT`, `SWING`, `P_START`, `P_RAKE`, `P_END`, `L_E`) and actor names (`hero4`, `chief4`, `man08`, `woman08`, `man16`, `hero18`, `boss18`, `man23`, `hero25`, `boss25`, `hand5`, `hand7`) are named here for reading, not for import.

Story formula elements (`references/story-formula.md`): 1 cold-open hook, 2 pivot and world, 3 youngest hero, 4 authority mocks (quote), 5 hero persists, 6 nickname, 7 false defeat, 8 second mocking quote, 9 the turn ("meanwhile"), 10 disaster as one physical image, 11 mechanism reveal, 12 end on an image.

---

## 1. Reference (measured): the edit the film imitates

From `deliver/QA_film.md` 1.3 and `plan/shot_plan.md` (grammar check):

| | Clip A | Clip B |
|---|---|---|
| Shots | 16 | 22 |
| Shot length mean / median / range | 3.75 / 3.65 / 0.70-7.73 s | 2.62 / 2.45 / 0.40-6.53 s |
| Cross-dissolves | 11 of 15 real transitions (73 %), 9-17 frames, median 13 | 18 of 21 (86 %), 9-23 frames, median 10.5 |
| Hard cuts | 1 (into A shot 11, f1322) | 1 |
| Special transitions | train wipe, cut hidden in a tilt (f276-277), white flash (f1930-1934) | punch-in cut with speed lines (f146-160), whip |
| In-shot snaps | 36, median 24.5 frames, 44 % of the time | 22, median 13.5 frames, 17 % of the time |
| Framing-change interval | 1.25 s mean, 1.19 median (plan count); 1.39 s (picture tool) | 1.54 / 1.26 (plan count); 1.62 s (picture tool) |
| Holds | 4, 1.30 s in all | 3, 1.03 s in all |
| Static frames / longest hold | 3.8 % / 14 frames | 5.5 % / 12 frames |
| Zoom median / pan median | 20.7 %/s / 142 px/s | 9.9 %/s / 57 px/s |
| Snap easing peak/mean | 1.87 | 1.66 |

The film borrows a shot or a move from each clip for every one of its 26 shots. The "Reference" row of each entry names the clip shot (A1 = clip A shot 1) and the still times (a/t16.0 = clip A at 16.0 s) as the plan wrote them.

---

## 2. Our build (film 1): the 26 shots

### Shot 1: the pencil insert (cold open)

| Field | Value |
|---|---|
| Time | clock 0.000-1.314; g0-38 (39 frames, 1.30 s) |
| Narration | เขาลากเส้นบนแผนที่อากาศ "He drew a line on the weather map" |
| Captions | เขาลากเส้น 0.00-0.50 / บนแผนที่อากาศ 0.50-1.46 |
| Beat | hook, element 1 (the odd physical act before we know why) |
| Set, light | office, office_day (= set preset `INTERIOR_DAY`) |
| Camera | Class insert. Hook take A (`v3/shots/film.py`, `cam_a`), one continuous move. Start: raking low insert on the pencil point at the storm symbol off FLA., distance 2.22 D, view yaw -39 deg, pitch +13 deg, already moving on g0. Snap push `SNAP1` g8-19 (quint) to 1.42 D, yaw -34, pitch +17; measured move g10-46, peak 154 px/frame at 0.47 s (peak/mean 2.35). Then follows the growing line while swinging toward frontal (yaw -39 to -10.3 deg over the shot). From g33 the pull-out `PULL` (g33-47) starts that becomes shot 2. Height 1.44-1.84 D above the floor, pitch +13 to +23 deg. End: pull-out under way (no cut). |
| Cast, marks | Hero only, card at `HERO_A` (-0.80, -0.72): hand, forearm and pencil in frame, no face. His card turns through the pencil point (yaw about 34 deg) so the pencil really touches the map. |
| Acting | Pencil lands on the storm symbol on g7 (`G_LAND`) and draws the red track north in one stroke: line 0 at g7, 0.07 at g13, 0.75 at g36 (`line_at`). Arm stretch solved per frame up to the puppet limit 1.30; pencil point registration 0.00 px (solver). |
| Props, devices | Wall map (English print DAILY WEATHER MAP, FLA., N.Y., BOSTON); red track as real geometry (`S.set_track(line, erase)`), red pencil. No spinner, chalk or label yet (cold open). |
| Transition | In: none (film start, camera already moving). Out: in-take reframe (the pull-out), no cut. |
| Sound | In the mix (hook entries, unchanged from `v3/out/mix_opening.json`): 1 whoosh_fast 0.000 (arm swings in, peak -19); 2 map_marker 0.233 (-16); 3 pencil_scratch 0.233-1.20 (RMS -27); 4 whoosh_fast 0.310 (snap push, -15); 5 whoosh_whip 1.170 (pull-out, -11); 6 pencil_scratch 1.200 (RMS -31). Plan also asked for a wall clock and far teletype room tone. |
| Heads | none |
| Reference | A1 0.0-1.5 s (a/t00.0-t01.5): the hero's odd act in close-up before we know why, push x1.72 in 0.5 s; B1 (b/t01.0-t02.0). Copied: the opening on the act, a fast push in the first 0.5 s, camera moving on frame 0. |
| Take, runner | Hook take A, `v3/shots/film.py` (beats from `v3/shots/timing.py` on `audio/th/hook_timing.json`); QA `v3/out/QA.md`. Frames `v3/out/frames/f_0001..` (f = g + 1). |
| Changed from plan | The plan asked for the hook to be rendered again with a straightened track; the client chose the hand-drawn stroke instead (`office3d.TRACK_STYLE = "hand"`), so the hook shows the wandering hand-drawn line like every later shot (`v3/set3d/office3d.py`: `TRACK_STYLE = "hand"`, commented "default, client choice"). The hook's beats were timed on the hook timing file; the delivered voice starts its second phrase 0.15 s later, so the picture leads the words a little more than 3 frames in shots 2-3 (inferred from the two timing files). |
| Colour row (v1) | 29.9 / 39.5 / 13.4 / 0.3 / 1.9, sat 0.41, val 0.49, dark 0.10: out on red, orange, blue (the map's cyan sea, 15 %) |
| Reviews | v1: Yes; the map is crisp, flat teal and tan under hard blind shadows. v1.1: Yes, almost unchanged. |
| Polish | Grade: global curve, saturation and bloom only. |

### Shot 2: the jab at New York (low)

| Field | Value |
|---|---|
| Time | clock 1.314-2.417; g39-72 (34 frames, 1.13 s) |
| Narration | ชี้ตรงเข้านิวยอร์ก "pointing straight into New York" |
| Captions | ชี้ตรงเข้า 1.46-2.05 / นิวยอร์ก 2.05-2.58 (the delivered voice starts 0.15 s after the reframe) |
| Beat | hook, element 1 |
| Set, light | office, office_day |
| Camera | Class low. Same take A, no cut. The 14-frame pull-out (`PULL` g33-47, sine) swings round the hero to 4.78 D, yaw +8, pitch +15.2, landing on the `low_medium` family: 1.17-1.20 D above the floor, pitch +15.2 to +15.9 deg; ceiling boards, a beam, the picture rail and the rug converge; the pendant lamp at (0.4, -2.6, 4.27) hangs into the top right with its bulb on g44-61. Snap push on the jab `SNAP2` g57-67 (quint) to 3.40 D (x1.35), measured move g60-64, peak 110 px/frame. Whip-off to the right over g69-72 (`WHIP_OFF`, pan 34 deg, quad-in), cut inside the whip streak at g73. End: whip. |
| Cast, marks | Hero at `HERO_A` (-0.80, -0.72), card turning to face the camera through the pull-out. |
| Acting | Draws back g55-57 (`GATHER`), jabs the pencil onto N.Y.: lands g60 (`G_JAB`), arrow head complete, squash and stretch; head turns to the viewer g62-69 (`TURN`); expression determined; blinks closed on g48 and g64. Never speaks. Hero's shadow touches 0 of 41 track samples. |
| Props, devices | Red track completes with its arrow head at N.Y. (line 0.92 to 1.0 on g55-60). Sign U.S. WEATHER BUREAU and calendar SEPTEMBER 20 behind him (English). |
| Transition | In: in-take reframe (the pull-out, 14 frames). Out: whip pan, cut inside the whip streak at g73 (4 frames off). |
| Sound | In the mix: 7 pencil_scratch 1.900 (RMS -24); 8 whoosh_fast 1.930 (snap, -19); 9 thump_jab 2.000 (jab, peak -9: approved over the -10 rule); 10 whoosh_whip 2.300 (whip, -10). Plan also asked for a cloth swish (1.75) and a small ding on the jab. |
| Heads | Hero 179-188 px at y 603-628 (0.47-0.49 H) before the snap; 252 px at y 491 (0.38 H) after it. |
| Reference | A1 1.5-3.7 s (a/t02.0-t03.0): pull back x0.70 with a pan to the low-angle hero; height from a/t16.0 (1.16 D, +15 deg). Copied: the pull-out that reveals who did the act, the low angle at about 1.2 D, the snap on the action word. |
| Take, runner | Hook take A, `v3/shots/film.py`. |
| Changed from plan | First render had no light source in frame; the camera was moved 0.6 D farther back and aimed 0.16 D higher so the pendant lamp and its bloom show (`v3/out/QA.md` pass 1). Streaked frames (snap g12-15, pull-out g35-45, jab snap g61-63) use a plate without actors plus an actor matte so the hero stays sharp; only the whip frames streak whole. |
| Colour row (v1) | 52.3 / 17.2 / 20.3 / 0.8 / 4.7, sat 0.45, val 0.47, dark 0.14: out on red, orange (red wallpaper fills the low frame) |
| Reviews | v1: Yes; red 52 %. v1.1: Yes; the lamp glows. |
| Polish | Grade: lamp bloom. |

### Shot 3: the chief rubs it out (high two-shot)

| Field | Value |
|---|---|
| Time | clock 2.417-4.305; g73-128 (56 frames, 1.87 s); tail g129-134 under the dissolve |
| Narration | แล้วหัวหน้าก็ลบทิ้งเฉยเลย "and his boss just rubbed it out" |
| Captions | แล้วหัวหน้า 2.58-3.03 / ก็ลบทิ้ง 3.03-3.59 / เฉยเลย 3.59-4.30 (delivered voice starts 0.16 s after the cut) |
| Beat | hook, element 1 (the authority wipes the act out) |
| Set, light | office, office_day |
| Camera | Class high. Hook take B (`cam_b`). Whip-on braking over 7 frames g73-79 (cubic out) into `CAM_TWO` (2.10, -5.25, 3.70) looking at (1.53, -0.95, 2.05): high two-shot 3.30-3.73 D up, pitch -20.3 to -21.3 deg, yaw -10.1 to -7.6. Slow push in which 22 % of every segment runs at constant speed (`CREEP = 0.22`) so it never parks (slowest frame 0.33 px). Snap push onto the hero's face `SNAP3` g108-120 (measured move g113-116, peak 34 px/frame) to `CAM_FACE` (2.46, -4.60, 3.32) looking at (2.01, -1.60, 2.20). End: `CAM_FACE`, creeping. |
| Cast, marks | Chief at the wall left of the track, screen left; hero at `near_mark` (2.6, -1.95), nearer and larger, screen right, mirrored (`place(flip=True)`) to face the chief. These marks grow into the gloat staging of shots 10, 18, 25. |
| Acting | Chief: smug, head roll -4 to -13 deg, eraser in the left hand (`rub` preset, stretch 1.18). Eraser touches at g94 (`G_TOUCH`), one stroke every 5 frames (`STROKE`), erase 0 to 0.60 by g109 and 1.0 at g122 (`G_DONE`), then lifts away and looks over. Hero: determined, blink g82; shocked swap behind the blink closed on g108 (`SHOCK` = `G_LAST` - 1): ring eyes, sweat drop, 2-frame squash; blink g137. No mouths. |
| Props, devices | Eraser face pinned on the upper end of what is left of the track (registration 0.00 px, 29 frames); the line vanishes from the N.Y. end and leaves the pink smudge and the ghost arrow head. |
| Transition | In: whip pan, cut inside the whip streak (4 frames off, 7 on). Out: dissolve 12 frames into shot 4 (g123-134). |
| Sound | In the mix: 11 thump_jab 2.560 (footfalls, -22); 12 thump_jab 2.860 (-23); 13 thump_jab 3.133 (felt thump on the first touch, -19); 14 eraser_rub 3.133-4.08 (set RMS -25, rendered peak -7.8: approved hook entry); 15 pop_surprise 3.600 (eye-pop, -11); 16 whoosh_fast 3.630 (snap push, -18). |
| Heads | Settled two-shot: hero 221-248 px at y 629-636 (0.49-0.50 H), chief 158-168 px at y 486-494 (0.38-0.39 H), ratio 1.40-1.47. After the snap: hero 288-310 px, chief 186-196 px (ratio 1.55-1.59 by design). |
| Reference | A5 tail (a/t19.0-t21.0: boss and hero in one frame, staged in depth); B3-4 (b/t05.0-t07.0: the shocked face, the whip pan). Copied: two-shot in depth with the near head 1.36-1.46 x the far one and lower in frame; the whip between shots; the snap onto the shocked face. |
| Take, runner | Hook take B, `v3/shots/film.py`; QA `v3/out/QA.md`. |
| Changed from plan | Two-shot moved 1 D closer and 0.1 D lower in the drafts (the first was too wide: chief 135 px, ratio 1.32). Rubbing timed to reach 0.60 before the push because after the push the chief's body hides the lower half of the erased track. |
| Colour row (v1) | 39.3 / 31.9 / 19.3 / 1.0 / 4.5, sat 0.44, val 0.50, dark 0.13: in band |
| Reviews | v1: Yes, the best match to the reference; the close-up holds the head at about 250 px against 300-385 in the reference. v1.1: Yes, still the best match in staging. |
| Polish | Grade only (no per-shot setting). |

### Shot 4: the flash-back, wide office to the calendar

| Field | Value |
|---|---|
| Time | clock 4.305-6.635; g129-198 (70 frames, 2.33 s) |
| Narration | คืออย่างนี้ กันยายน ปีหนึ่งเก้าสามแปด "You see: September 1938." |
| Captions | คืออย่างนี้ 4.30-5.00 / กันยายน 5.00-5.49 / ปี 1938 5.49-6.62 |
| Beat | pivot, element 2 (the world and the date) |
| Set, light | office, office_day; the morning before: map clean (no line, no smudge, no chalk, no label) |
| Camera | Class high, then insert. Start `wide_high` (4.4 D up, -25 deg; desk dark in the foreground, window at right), truck right and push (camera x -2.18 to -1.33, no orbit so the lamp band stays clear) g121-145. Forward flight `FLIGHT` g142-161 (clock 4.62-5.28), measured g146-158, peak 951 px/s, whole-frame streak g148-156, under the lamp shades, landing on the tear-off calendar (`calendar_cam`, 12 deg rake) on 'กันยายน'. Push about 8 %/s through 'ปี 1938' (calendar 98 px wide in the wide, 361 px at landing, 423 px at g193). Exit: whip-tilt down-right g195-198, peak 456 px/s, streaked whole. |
| Cast, marks | Hero `hero4` at `hero_mark` (-0.55, -0.42), three-quarter, chin in hand (`acting.hero_study`); chief `chief4` by the teletype at (2.25, -1.70) (`acting.boss_read_tape`). Both leave frame in the flight (last heads g151). Hero hidden from g195 so nobody shows in the whip. |
| Acting | Held poses, offset blinks. Chief tears his tape at g150 (clock 4.90). No mouths. |
| Props, devices | `set_calendar`: leaf SEPTEMBER / 20 / TUESDAY / 1938 readable 5.3-6.4 s, top leaf lifts in a draught at g171 (clock 5.60); `set_teletype`; sign U.S. WEATHER BUREAU in the wide. |
| Transition | In: dissolve 12 frames from the hook, both shots moving (g123-134). Out: cut hidden in the whip-tilt (4 accelerating frames here, s05 brakes out). |
| Sound | Cues (film s): 4.30 soft whoosh, office bed up; 4.40 clarinet and piano theme; 4.72 airy whoosh (flight); 5.00 tape tear; 5.66 date-stamp clunk on '1938'; 5.70 calendar leaf flutter; 6.60 whip whoosh. In the mix: 17 office_tone 5.000-6.65 (RMS -34.4); 27 whoosh_whip 6.600 (-13). |
| Heads | Wide: hero 96-108 px at y 453-475, chief 100-115 px at y 414-441. |
| Reference | A2 3.80-9.20 ('You see, ...': forward flight x2.92 in 1.2 s that opens the world); A10 opening a/t36.0 (calendar as a full-frame text prop); exit as A f276-277 (cut hidden in a tilt). Copied: the fly-through that opens the world on "You see", the date as a printed prop, the hidden cut. |
| Take, runner | `v3/film/s04/` (shot.py on its own `otake.py`; `qa.py`). Rendered g121-198 (handle in 8). |
| Changed from plan | Heads in the wide are 96-115 px, the plan asked 50-70 (kept from an interrupted take). In the hook the chief stands screen-left of the hero; here the hero is left (a different morning). g195-198 re-rendered because the hero's streaked head showed in the last whip frame. |
| Colour row (v1) | 45.0 / 11.6 / 31.0 / 1.1 / 8.9, sat 0.47, val 0.43, dark 0.14: out on red, orange, blue, val (two thirds of the take is the calendar on red wallpaper in window shade) |
| Reviews | v1: Partly; the wide at 4.5-5.0 s is dark and cluttered with small heads, orange only 12 %; the calendar insert is clean; two of three 0.5 s pairs read as a flat card. v1.1: Partly (unchanged); the calendar paper turned bluer and brighter (123,138,177) to (150,171,223); dark 0.19 and sat 0.49 left the band. |
| Polish | Grade only. |

### Shot 5: the storm spinner off Florida

| Field | Value |
|---|---|
| Time | clock 6.635-9.039; g199-270 (72 frames, 2.40 s) |
| Narration | เฮอริเคนลูกหนึ่ง จ่ออยู่นอกฝั่งฟลอริดา "A hurricane was sitting off the coast of Florida." |
| Captions | เฮอริเคน 6.62-7.02 / ลูกหนึ่ง 7.02-7.61 / จ่ออยู่ 7.61-7.92 / นอกฝั่ง 7.92-8.34 / ฟลอริดา 8.34-9.04 |
| Beat | pivot, element 2 (the threat placed on the map) |
| Set, light | office, office_day; clean map (`set_track(0, 0)`) |
| Camera | Class insert. Brakes out of the whip-tilt g199-207 (whole-frame radial streak). Hyper fly-in down the east coast `FLY` g199-226 (clock 6.63-7.45; quartic ease-out, peak 298 px/s) from `P_START` (3.45 D) to `P_RAKE` 0.92 D from the paper, yaw 48, pitch 10 (insert_rake family, lens below-left, FLA. lower left). `ORBIT` g226-240: orbit 5 deg + push 6 %/s. `PULL` g240-264: eased pull-back with tilt up (peak 48 px/s), dying by 8.7, opening the coast to N.Y. (N.Y. at y 52 on g241, y 448 on g277) and ending on `P_END` (1.60 D, yaw 55.5, pitch 16.3, the `coast_rake` framing). No snap. 3000 px map until g217, then the 6000 px map (lens within 1 D). |
| Cast, marks | No faces. The chief's ink arm and hand ball only (`hand5`, cast boss, a card on an arm canvas), from frame right. |
| Acting | Hand enters with the spinner at g208, pins it at g218 (clock 7.15, 'ลูกหนึ่ง'), thumb pushes the pin home (pin out 0.025 to 0 over 3 frames), hand gone by g231. Registration on the pin 0.0 px over 24 frames. |
| Props, devices | Storm spinner (new): red spiral paper disc 0.16 D on a brass pin, hard shadow; `set_spinner`, turning 0.5 rev/s with a 3 deg wobble, its phase continued into shots 6 and 7. It is the storm in every later map shot. |
| Transition | In: cut hidden in the whip-tilt (7 streaked frames, s04 g195-198 accelerate, here g199-201 brake). Out: dissolve 13 frames into shot 6 (g265-277), map to map. |
| Sound | Cues: 6.65 long whoosh with wind tail; 7.25 pin thunk; 7.40 ratchet whirr; 7.90 far thunder (storm motif, first time); 8.55 far surf and a gull. In the mix: 28 thunder_low 7.900 (-20). The pin and whirr had no library sound. |
| Heads | none |
| Reference | A3 9.27-11.53 (hyper fly-in x63 landing on the thing the sentence names, a/t09.0-t11.0), entered through A's cut hidden in a tilt; pull-back as the end of B5. Copied: the fly-in that lands on the named thing, the hidden cut. |
| Take, runner | `v3/film/s05/` (shot.py on `../s04/otake.py`). Rendered g199-279 (handle out 9). |
| Changed from plan | None of note. The hand ball reads as a dark brown silhouette in the window-bar shade. |
| Colour row (v1) | 37.9 / 26.4 / 13.9 / 0.6 / 3.7, sat 0.39, val 0.46, dark 0.15: blue just under (the map sea reads cyan 17.5 %) |
| Reviews | v1: Partly; the 27-frame fly-in is a full smear (6.7 s) and the map insert reads as a flat diagram. v1.1: Partly (unchanged). |
| Polish | Grade only. |

### Shot 6: the old hands (low wide on three)

| Field | Value |
|---|---|
| Time | clock 9.039-11.214; g271-335 (65 frames, 2.17 s) |
| Narration | รุ่นใหญ่ในกรมอุตุสหรัฐ ฟันธงว่า "The old hands at the U.S. Weather Bureau called it flat out:" |
| Captions | รุ่นใหญ่ 9.04-9.40 / ในกรมอุตุสหรัฐ 9.40-10.49 / ฟันธงว่า 10.49-11.16 |
| Beat | setup, element 2 (the authority and its certainty) |
| Set, light | office, office_day; clean map with the pinned spinner, calendar leaf 20 |
| Camera | Class low. `low_three` moved to (1.25, -5.50, 1.0): 1.0 D above the floor, looking up 13 deg, 21 deg off the wall normal. Crane up 0.25 D g262-306 (to 1.25 D, tilt 10 deg) so the sign rises from y 408 to y 381, the top third. Push toward the chief g303-323, 15 %/s of the distance falling to 0 at the whack, then a 1.2 %/s drift. No snap; nothing streaked. First frames g262-270 show the empty wall (map to map dissolve); last frames hold the pointer tip on the spinner at (503, 719), where shot 7 picks it up. |
| Cast, marks | senior_a (-2.10, -1.25) left: camel fedora, spectacles, tweed, `expr='unimpressed'`; chief (-0.95, -1.55) centre, half a pace forward, smug; senior_b (1.00, -1.05) right: bowler, walrus moustache, `expr='happy'` (eyes shut, content). Three-quarter (yaw 0.35, 0.40, -0.35). |
| Acting | Pop-ins 6 frames each (scale 0.35, 0.80, 1.12, 1.06, 0.97, 1.0): senior_a g274, chief g278, senior_b g282 (clock 9.05, 9.17, 9.29). Chief raises the pointer at g310 (10.25) and whacks it onto the spinner at g319 (10.52; disc squash 0.82 + wobble; `acting.boss_pointer_whack`). Nods together (`acting.senior_nod`) g327 and g333. Blinks: chief g292, senior_a g300. No mouths (reported speech). |
| Props, devices | Sign U.S. WEATHER BUREAU readable 9.5-10.3; pointer tip pinned on the spinner by sight line from g317 (0.0 px, 26 frames). |
| Transition | In: dissolve 13 frames from shot 5. Out: dissolve 10 frames into shot 7 (g331-340). |
| Sound | Cues: 9.03 soft whoosh; 9.10 pompous tuba vamp; 9.15, 9.27, 9.39 pop thumps; 9.70 glint ting on the sign; 10.62 pointer whack; 10.90, 11.10 wood-block knocks (nods). In the mix: none of these (the pops were reduced to one sound, then thinned; the tings and wood blocks had no library sound). |
| Heads | senior_a 145-156 px at y 541-556; chief 165-181 at y 477-488 (0.37-0.38 H); senior_b 171-194 at y 531-553. |
| Reference | A4 11.93-13.40 (the row of older men, a/t12.0-t13.0) seen from A5's low angle (a/t16.0: 1.16 D, +15 deg); move of B6 (b/t16.5-t17.5: slow crane with tilt up on the unimpressed authority). Copied: the row of authorities shot from low, the crane up. |
| Take, runner | `v3/film/s06/` (shot.py on its own `otake.py`, copied from s04). Rendered g262-342. |
| Changed from plan | Camera moved 0.9 D and the trio about 1.4 D left of the props module's marks (from the original marks the spinner sat behind the chief's belly and the pointer could not reach it, solve error 0.97 D); the camera is 0.7 D nearer, so heads are 145-194 px instead of 129-142. The plan's tilt up 60 px/s became a crane up (a true tilt pushed the sign down onto the hats). |
| Colour row (v1) | 38.5 / 15.6 / 33.4 / 1.1 / 5.3, sat 0.47, val 0.46, dark 0.13: out on orange, blue (the blue rug fills the bottom 380 px from 1 D up) |
| Reviews | v1: Yes, B-like; lamp globes blown to flat white discs, blue (rug) 33 %. v1.1: Yes; the globes now glow. |
| Polish | Grade: lamp bloom. |

### Shot 7: "it will curve out to sea" (chalk curve insert)

| Field | Value |
|---|---|
| Time | clock 11.214-13.377; g336-400 (65 frames, 2.17 s) |
| Narration | เดี๋ยวก็เลี้ยวออกทะเล ลูกไหนก็เลี้ยวทั้งนั้น "it will curve out to sea. They all curve." |
| Captions | เดี๋ยวก็เลี้ยว 11.16-11.64 / ออกทะเล 11.64-12.29 / ลูกไหนก็เลี้ยว 12.29-12.88 / ทั้งนั้น 12.88-13.38 |
| Beat | setup, element 2 (the old confidence shown on the thing itself) |
| Set, light | office, office_day; map clean apart from what this shot adds |
| Camera | Class insert, true 3D on the wall map (never square-on). (a) g329-366 `chalk_rake`: 0.92 D from the paper, lens below-left, yaw 60 to 56 deg, pitch 18, the aim following the chalk tip with a lag. (b) Snap g366-380 (clock 12.10-12.57, 14 frames, quintic + sine, peak 226 px/s, plate streak g370-374): pull back and swing toward frontal (12 deg of yaw kept) to `chalk_wide`: the whole western Atlantic with the map frame, DAILY WEATHER MAP and the sign edge; drift push about 4 %/s to the end. 6000 px map while the lens is within 1 D. |
| Cast, marks | No figures. The chief's pointer, stick and one hand ball from the lower right (`hand7`, pointer prop scale 0.65). |
| Acting | Pointer taps the spinner g340 (11.22), rides the chalk tip from g341; the curve bends north-east at g355 (11.74, 'ออกทะเล'), arrow out to sea by g366; pointer gone by g375. Registration 0.0 px over 47 frames. |
| Props, devices | White dashed chalk curve (`set_chalk`, grow control; stays for the rest of the film). Six faded ghost tracks (`set_ghost`), one every 3 frames from g375 (12.40), all curving out to sea, held at 35 %. Tick-mark stamp (`set_tick`) lands on the chalk curve at g392 (12.95, 'ทั้งนั้น') with a 3-frame settle. Spinner keeps turning. |
| Transition | In: dissolve 10 frames from shot 6. Out: dissolve 15 frames into shot 8 (g394-408, change of place). |
| Sound | Cues: 11.21 soft whoosh; 11.32 pointer tap; 11.35 chalk scratch with a slide whistle that veers away; 12.43 whoosh out; 12.50 six fwip strokes as an ascending xylophone run; 13.05 rubber-stamp thunk. In the mix: 29 pencil_scratch 11.350-12.20 (RMS -26.1); 30 thump_jab 13.050 (stamp, -12). |
| Heads | none |
| Reference | B6 b/t13.5-t16.0 (one pattern repeated many times as the reason for the old confidence) told on the thing itself as in A10 (a/t38.5-t41.0); fast pan of A6 (21.93-26.13). Copied: the repeated pattern as evidence, the pull-back that shows all of them. |
| Take, runner | `v3/film/s07/` (shot.py on `../s04/otake.py`). Rendered g329-410. |
| Changed from plan | A pop at g339-340 (aim jump of 0.024 D) was fixed by re-rendering g329-339. |
| Colour row (v1) | 28.4 / 30.4 / 15.5 / 0.5 / 2.2, sat 0.37, val 0.49, dark 0.09: out on red, sat (cyan 23 %) |
| Reviews | v1: Partly; reads as an infographic on paper (cyan 23 %, sat 0.37); the reference never holds a flat chart this long. v1.1: Partly (unchanged). |
| Polish | Grade only. |

### Shot 8: the sleeping beach (sunny)

| Field | Value |
|---|---|
| Time | clock 13.377-16.829; g401-504 (104 frames, 3.47 s) |
| Narration | แถบนิวอิงแลนด์ ไม่โดนเฮอริเคนลูกใหญ่มาแล้ว ร้อยยี่สิบกว่าปี "New England had not been hit by a major hurricane in more than 120 years." |
| Captions | แถบนิวอิงแลนด์ 13.38-14.20 / ไม่โดนเฮอริเคน 14.20-14.93 / ลูกใหญ่ 14.93-15.31 / มาแล้ว 15.31-15.63 / 120 กว่าปี 15.63-16.83 |
| Beat | setup, element 2 (complacency) |
| Set, light | beach (`v3/set3d_beach/beach3d.py` + `set3d_ext/beach`), beach_sunny (= `SUMMER_SUN`, key turned to shine from the sea side, 44 to 46 deg high, so the sleeper casts a shadow) |
| Camera | Class high, then eye. Start `beach_high` moved 3 D back along the shore and panned 10 deg toward the land, loc (-5.4, 8.6, 5.0), 15 D from the chair, pitch about -17 deg (LONG ISLAND board readable, sea at left, cottages receding at right). Crane down and push 8 %/s. Crash push `PUSH` g448-473 (clock 14.85-15.68, 25 frames, the one clip-A-length snap) to eye level `L_E` (4.75, 8.68, 1.40), 4.3 D from his head, under the umbrella; static run of 1 frame at g473; then drift. |
| Cast, marks | beach_man (`man08`) asleep in the deck chair (chair at (9.6, 8.6); heels at (9.02, 9.95)), reclining side-on with `beach_sleep` (boater over his eyes, asleep face, rising Z, chest rise). beach_woman (`woman08`) far on the porch of cottage_08 at x 16.55, pegs a towel at g423 (14.0); she leaves the scene from g456. |
| Acting | Chest rise, Z. After the push a cobweb glints and a spider lowers itself from g474 (15.70). No mouths. |
| Props, devices | LONG ISLAND board, cottage row with porches, telegraph poles, striped umbrella, deck chair, a towel line built on cottage_08's porch in this take, cobweb card with spider, calm sea. Whole-figure cast shadows on the sand. |
| Transition | In: dissolve 15 frames (change of place). Out: dissolve 13 frames into shot 9 (g499-511). |
| Sound | Cues: 13.30 surf and gulls pre-lap; 13.50 ukulele bar; 14.10 towel flap; 14.95 whoosh (crash push); 15.80 snore and harp pluck (spider); 16.40 second snore. In the mix: 18 beach_calm 13.300-16.85 (RMS -33.2); 31 whoosh_fast 14.950 (-15). |
| Heads | Man 54-64 px in the vista, about 193-199 px at 0.48 H after the push; woman 35-40 px. |
| Reference | A7 26.47-28.37 (the complacent tycoon: push x3.05 in 0.83 s, then drift 10 px/s; a/t27.0-t28.0) and a/t52.0-t54.0 (lounging under the striped umbrella); B6 second half. Copied: the long crash push onto a sleeping complacent figure, then the drift. |
| Take, runner | `v3/film/s08/` (shot.py on `set3d_ext/beach/bshot.py`). Rendered g391-513. |
| Changed from plan | Start camera 15 D from the chair, not 12, to keep the board readable; the woman is on cottage_08, not cottage_07 (out of frame), head 35-40 px not 60; key light turned (the umbrella shadow covered the chair); the end framing has the dark underside of the umbrella over about the top quarter. |
| Colour row (v1) | 35.8 / 21.7 / 38.1 / 2.4 / 1.6, sat 0.36, val 0.71, dark 0.02: sunny exterior, outside the interior band by design |
| Reviews | v1: Yes, the most reference-like exterior; no sun bloom or haze; the crash push ends with the umbrella filling the top half and the sleeper half hidden. v1.1: Yes; still no sun bloom or visible haze. |
| Polish | Grade: gain 0.93, sat 0.94, bloom 0.55, haze 0.16 at y 0.40 H. |

### Shot 9: the youngest, and his line (one take, three framings)

| Field | Value |
|---|---|
| Time | clock 16.829-20.317; g505-609 (105 frames, 3.50 s) |
| Narration | เขาเด็กที่สุดในห้อง แต่เส้นของเขาไม่เลี้ยว ตรงเป๊ะ ขึ้นเหนือ "He was the youngest in the room. But his line did not curve. Dead straight, heading north." |
| Captions | เขาเด็กที่สุด 16.83-17.37 / ในห้อง 17.37-17.88 / แต่เส้นของเขา 17.88-18.55 / ไม่เลี้ยว 18.55-19.17 / ตรงเป๊ะ 19.17-19.72 / ขึ้นเหนือ 19.72-20.32 |
| Beat | hero, element 3 (youngest in the room) |
| Set, light | office, office_day |
| Camera | Class high, then insert, then low (worm's eye). ONE take. (a) `high_wide` (-0.45, -6.45, 4.0) looking at (-0.50, -0.60, 1.40): 4.0 D up, -24 deg; push 12 %/s. (b) Crash push `CRASH` g533-548 (17.68-18.18), measured peak 224 px/frame at g540, threading between the chief and senior_a with a 0.25 D sideways arc (g538-543 streaked whole; near figures hidden where the lens reaches their cards: senior_b g539, senior_a g540, chief g541) down to `insert_front` (1.5 D from the paper, 10 deg yaw); one static frame g549; the camera climbs with the pencil point. (c) Snap swing `SWING` g575-590 (19.08-19.55), measured peak 67 px/frame at g584, to `corridor_cam` (props version, loc (0.2729, -0.45, 1.398), look `track_point(0.80)`, 0.40 D off the paper, up = wall normal): the line runs away like a road to N.Y.; drift push 10 %/s easing to near still. 6000 px map switched in at g582 inside the swing. |
| Cast, marks | Hero at `hero_mark` (-0.55, -0.42), `expr='determined'`; senior_a at `senior_a_front` (-1.55, -2.62) left, held grin; chief at `chief_front` (0.40, -2.62) right, smug; senior_b at `senior_b_front` (1.25, -3.05), cropped at the right edge. Hero seen small in the gap between them. |
| Acting | Chief jerks a thumb back at the kid g513 (17.0). Hero looks over, blinks g525 (17.4), turns to the map. Pencil lands on the spinner g550 (18.22); one bold freehand stroke north g552-579 (18.3-19.2, line 0 to 0.95) through his own arm (card at hero_mark, stretch 1.15; registration 0.00 px), passing the height of the white chalk bend at 18.76 and keeping on north. Hero lifts the pencil away from g580; his card is hidden from g584. Arrow head pops at N.Y. on g598 (19.85, 'ขึ้นเหนือ'). No mouths. |
| Props, devices | Red track growing (`set_track`), white chalk curve bending off right, six ghost tracks, tick, spinner. `set_map_res` swaps to the 6000 px map. No ruler (client change). |
| Transition | In: dissolve 13 frames (beach to office). Out: dissolve 9 frames into shot 10 (g606-614). |
| Sound | Cues: 16.83 whoosh, surf out, office bed in; 17.00 three low brass notes; 17.10 thumb; 17.40 piccolo peep; 17.78 big whoosh in; 18.32 pencil taps down; 18.40 pencil zip rising; 18.86 small ding at the bend; 19.40 whoosh with a faint engine rev; 19.95 arrow-head ding. In the mix: 32 pencil_scratch 18.400-19.30 (RMS -27.5). |
| Heads | Wide (a): hero from 128 px; senior_a from 195, chief from 198, senior_b from 213 px; all four whole, bottoms at most y 780. Insert: the hero's head is a cropped close-up at the left edge (700-815 px wide, as in the hook's insert). |
| Reference | A4 a/t11.5-t13.0 ('He's the youngest engineer on the job': small hero beside bigger men); A10 36.33-44.07 (push x2.57 into a macro on the thing itself and move along it); a/t48.0-t49.5 (rail point of view) for (c). Copied: the small figure framed between big ones, the crash push into the object, the point-of-view down the line. |
| Take, runner | `v3/film/s09/` (shot.py on `../s10/otake.py`). Rendered g496-616. |
| Changed from plan | The ruler (slap-on 18.22, whip-off 19.1) was cut: the client chose the hand-drawn stroke. With the wall normal as up vector the ceiling fills the upper third of the corridor view. A pop at g577-578 (hero card vanishing while the swing was slow) was fixed by hiding him at g584 and re-rendering g578-583. |
| Colour row (v1) | 32.4 / 25.8 / 23.7 / 0.9 / 4.2, sat 0.40, val 0.51, dark 0.12: in band (delivered ungraded at take level) |
| Reviews | v1: Yes up to 19 s; the corridor view at 19.5-20 s is a smeared raking macro that reads as abstract. v1.1: Yes (unchanged). |
| Polish | Grade only. |

### Shot 10: "Kid, hurricanes don't take the expressway" (low, then G)

| Field | Value |
|---|---|
| Time | clock 20.317-23.129; g610-693 (84 frames, 2.80 s) |
| Narration | หัวหน้าแซว “ไอ้หนู เฮอริเคนมันไม่ขึ้นทางด่วนหรอก” "The boss teased him: 'Kid, hurricanes don't take the expressway.'" |
| Captions | หัวหน้าแซว 20.32-21.01 / “ไอ้หนู 21.01-21.49 / เฮอริเคน 21.49-21.91 / มันไม่ขึ้น 21.91-22.31 / ทางด่วนหรอก” 22.31-23.13 |
| Beat | boss_quote, element 4 |
| Set, light | office, office_day |
| Camera | Class low, then eye. (1) Low single `L1` (0.30, -4.10, 1.20) looking at (0.70, -0.42, 2.30): 1.2 D up, +16.5 deg, the chief alone, map and red line at screen left, ceiling boards above. (2) Snap 20.82-21.35 (move g632-641, peak 40 px/frame at g636): pull back, rise 1.6 D to 2.85 D, pan right into G, THE GLOAT FRAMING (`G` of the props module: (1.55, -4.95, 2.85) looking at (1.25, -0.40, 2.62), 22 mm). (3) Eased push through the quote, 30 to 0 %/s, x1.3, done as a zoom 22 to 28.6 mm plus a 0.3 D truck right (a dolly would grow the near hero x1.47 and break the depth ratio), ending on `GE` (1.85, -4.95, 2.85). Static only in the out handle g697-700. |
| Cast, marks | Chief `boss10` at `boss_mark` (1.30, -0.42), far; hero `hero10` at `gloat_near` (2.4, -1.7), near, three-quarter facing screen left (`hero_listener`, `expr='unimpressed'`). |
| Acting | Chief bounces the eraser in his palm, smirk (`expr='smirk'`), facing the map (yaw -0.35). Mouth moves only inside the quote, g635-696, driven by `acting.loudness(21.07, 23.13)` through `boss_talk`. 'เฮอริเคน': drives the eraser up the red line like a toy car (eraser pinned on the track, u 0.50 to 0.92, g644-667). 'มันไม่ขึ้น': turns to the hero (yaw +0.40) over 7 frames, finger wag with the near hand. 'ทางด่วนหรอก': leans 0.12 D, held wink g692-695. Hero frozen, unimpressed half-lids, blinks (plan 21.4, 22.0, 22.8), one sideways gaze shift; his mouth never moves. |
| Props, devices | Red line complete with arrow head (no label yet), chalk curve, ghost tracks, tick, spinner, eraser (pinned, registration 0.00 px). |
| Transition | In: dissolve 9 frames (quick continuity). Out: dissolve 9 frames into shot 11 (g690-698). |
| Sound | Cues: 20.40 heavy step and waistcoat creak; 20.42 tuba answers the theme; 20.55, 20.85 eraser pats; 20.92 whoosh (snap); 21.68 eraser squeak 'vroom', toy beep-beep; 22.06 finger-wag ticks; 22.60 chuckle under the narrator; 23.05 wink ting. In the mix: 33 eraser_rub 21.675-22.05 (RMS -28.3). |
| Heads | Low single: chief 190 px at x 474 (0.40 H). G at the snap end: chief 173 px at (397, 594), hero 244 px at (620, 694), ratio 1.41. End of the push: chief 223, hero 317 px, ratio 1.42; the frame edge crops about 20 % of the hero's head at the end. |
| Reference | A5 13.83-21.50 (low-angle boss a/t16.0, then x0.50 back with a 941 px pan into the two-shot, a/t19.0-t20.5); A11 44.10-47.70 (two-shot in depth) mirrored left to right; B10 (push easing out 30 to 0 %/s, held wink). Copied: the low-angle boss, the pull-back pan into the two-shot in depth, the easing push, the wink. |
| Take, runner | `v3/film/s10/` (shot.py on its own `otake.py`, the shared office runner of s09-s13; band grade `grade.py`). Rendered g603-700. |
| Changed from plan | Framing 1 is the low single `L1`, not the props module's `low_boss` (from `low_boss` the near hero was in frame). The hero has no pencil behind his ear (no such drawing in the acting library). Delivered with the mild band grade `s10/grade.py` (red family rotated 8 deg toward orange, shadows under V 0.28 lifted up to 0.07): the raw render measured red 43-44 %, dark 0.16. |
| Colour row (v1) | 40.4 / 31.5 / 15.4 / 1.1 / 4.5, sat 0.43, val 0.49, dark 0.12: in band. v1.1: blue 12.7 (1.3 points under the 14-30 band). |
| Reviews | v1: Yes; the low angle looks into a dark ceiling where the reference's low angles look up at bright sky. v1.1: Yes. |
| Polish | Grade: lamp bloom. |

### Shot 11: erase, redraw, erase, redraw (stepped pull-out)

| Field | Value |
|---|---|
| Time | clock 23.129-26.406; g694-791 (98 frames, 3.27 s) |
| Narration | หัวหน้าลบ เขาลากใหม่ ลบอีก ลากอีก ตรงเท่าเดิม "The boss rubs it out. He draws it again. Rubbed out again. Drawn again. Just as straight." |
| Captions | หัวหน้าลบ 23.13-23.70 / เขาลากใหม่ 23.70-24.50 / ลบอีก 24.50-25.16 / ลากอีก 25.16-25.69 / ตรงเท่าเดิม 25.69-26.41 |
| Beat | persist, element 5 |
| Set, light | office, office_day |
| Camera | Class insert, then low, then high. ONE take, the stepped pull-out `PA["paths"]["persist_steps"]`. (a) `insert_rake_ny` (-1.30, -0.66, 2.55) looking at (0.30, -0.05, 2.74) on the N.Y. end. (b) Same framing; the camera slides down 0.4 D and back up with the pencil (moves g705-713 and g723-730, peaks 17 and 14 px/frame). (c) Snap out g737-746 (24.35-24.82), peak 148 px/frame, whole streak g738-743, to `low_two_wall` (0.40, -3.70, 1.2) looking at (0.40, 0, 2.12): low two-shot at the wall, +14 deg; one static frame g748. (d) Snap out and up g765-775 (25.33-25.80), peak 157, to `high_two_shot` (3.7 D, -22 deg); near still 26.0-26.27, then drift. |
| Cast, marks | (a, b) hand cards: the chief's and the hero's puppets at scale 1.5, facing the lens, 0.05 D in front of the contact point, bodies outside the frame at the right (the take-A method). (c, d) chief `boss11` at `boss_mark` (1.30, -0.42), hero `hero11` at `hero_mark` (-0.55, -0.42); the bodies enter inside the snap at g739. |
| Acting | Erase states: 0 to 0.6 in three 4-frame bites g698-711 (chief's hand); 0.6 to 0 with the hero's pencil g716-732; 0 to 0.8 in four frantic rubs g746-756 (chief, steam puffs, face reddening to purple); 0.8 to 0 in one 8-frame swipe with the pencil stub g761-769 ('ลากอีก'); chief frozen purple, one eye twitching, swaps to panting (worn eraser nub, prop scale 0.6) at g771 inside the snap. (d) Hero at ease, chin up, pencil stub in his near hand. Expressions: chief smug to purple; hero determined, unimpressed, neutral. No mouths. |
| Props, devices | `set_smudge` halo 0 to 1 to 2 to 3; `set_crumbs` 0 to 0.45 to 1 on the ledge; pencil stub and worn eraser (prop scale 0.6). Eraser and pencil pinned on the erase front of the hand-drawn track (0.0 px in the inserts; 4.7-29 px at the end of the frantic strokes, where the arm reaches its limit). |
| Transition | In: dissolve 9 frames, the chief's hand already swinging in. Out: dissolve 11 frames into shot 12 (g787-797). |
| Sound | Cues: 23.23 wood-block ostinato; 23.25, 23.38, 23.52 eraser squeaks; 23.85 pencil zip; 24.45 whoosh; 24.85 four frantic rubs with a kettle whistle; 25.35 fast zip higher; 25.43 whoosh; 25.90 ta-da ding; 26.00 panting, crumbs. In the mix: 34 eraser_rub 23.250-23.85 (RMS -28.1). |
| Heads | Hand cards 659-825 px (heads outside the frame by construction). (c) low two-shot heads 137-338 px across the snap; (d) 138-148 px (wide, as planned), hero at x about 100. |
| Reference | B14 b/t33.0-t37.0 (counted repetitions in one take, each count one step wider, ending on the accumulated result); A5 (several snaps in one take, the face going purple, a/t17.0-t18.5; low angle a/t16.0). Copied: one take that steps wider on each repetition; the purple face. |
| Take, runner | `v3/film/s11/` (shot.py on `../s10/otake.py`). Rendered g687-799. |
| Changed from plan | No ruler (client change): the hero redraws the same bold freehand stroke. The chief at `boss_mark` would physically stand in the insert's background: accepted. Hand cards cast no shadow (their scaled bodies would darken the map). |
| Colour row (v1) | 33.6 / 36.4 / 17.4 / 2.3 / 3.8, sat 0.44, val 0.48, dark 0.14: in band. v1.1: orange 40.6 (2.6 points over 38), dark 0.16 (0.01 over 0.15). |
| Reviews | v1: Yes; the purple face echoes clip A; the 23.5-24.5 s insert is dim and murky under the blind shadows. v1.1: Yes, with a new artifact: at g740-743 the hero's motion-blurred eyes and mouth turned into pale hollow rings (caused by the grade). |
| Polish | Fix round: the grade no longer lets glow land inside near-white fills (`grade.py`, constants `FILL_V`, `FILL_S`, `FILL_HOLE`, `FILL_CLOSE`), which removed the ghost face (the delivered film carries this grade). |

### Shot 12: the whole building laughs (desk foreground)

| Field | Value |
|---|---|
| Time | clock 26.406-27.957; g792-838 (47 frames, 1.57 s) |
| Narration | จนทั้งตึกเรียกเส้นนั้นว่า "Until the whole building was calling that line" |
| Captions | จนทั้งตึกเรียก 26.41-27.14 / เส้นนั้นว่า 27.14-27.91 |
| Beat | nickname, element 6 (the mockery spreads) |
| Set, light | office, office_day |
| Camera | Class eye. `desk_fg` (-1.6, -5.8, 2.25) looking at (-0.55, -0.3, 2.15), 22 mm: banker lamp, ink bottle and typed sheet in the left foreground. Eased pull back along its own axis (0.06 D in to 0.56 D back, about 8 %/s at the mid-ground) with a slide 0.34 D right (about 42 px/s, accelerating) and a 0.03 D rise and fall. No snap; no static frame. |
| Cast, marks | senior_a at `senior_a_desk` (-1.95, -3.00), 2.8 D from the lens; senior_b at (0.80, -3.25), 3.5 D; far at the wall the hero at `hero_mark` and the chief at `boss_mark`, where shot 11 left them. Three-quarter, no backs. |
| Acting | senior_a and senior_b: `acting.senior_laugh` (held laughing drawing, heads rolled 15 deg, tears, blush, body bounce 0.06 D at 3 Hz, phases 0 and 0.5), thumbs jerked back at the map g801 and g811. Chief: `boss_laugh_doubled` facing the hero (guffaw, lean 25 deg, tears, thigh slap g810, paper strip pulled from the waistcoat from g828). Hero: `hero_listener`, unimpressed, one blink g819, pencil stub in hand. No mouth moves. |
| Props, devices | Red line (line 1, erase 0) with the full smudge halo (level 3) and crumbs, showing between the hero and the chief (x 391-452). Label still hidden. |
| Transition | In: dissolve 11 frames. Out: punch-in cut into shot 13 (no mix). |
| Sound | Cues: 26.41 soft whoosh; 26.50 laughter walla of six to eight voices and a clarinet run; 27.00 thigh slap; 27.60 wheeze, paper rustle. In the mix: 35 crowd_chuckle 26.500-27.98 (peak -15). |
| Heads | senior_a 240-299 px, senior_b 224-271 px (near); chief 123-136, hero 129-144 px (far); near / far about 1.9. |
| Reference | B9 b/t22.5-t23.5 ('Now they laughed even harder': laughing faces near the lens, the butt of the joke far behind, pull back 8.2 %/s, slide 42 px/s). Copied: the staging and the move numbers. |
| Take, runner | `v3/film/s12/` (shot.py on `../s10/otake.py`; band grade `grade12.py`). Rendered g785-838. |
| Changed from plan | senior_b moved 0.6 D right and 0.45 D back from `senior_b_desk` (his head sat over the chief's); the chief kept at `boss_mark` (the module's `chief_wall12` stood him in front of the red line); his slapping hand kept 0.2 D closer to the thigh so the arm does not cover the line. |
| Colour row (v1) | 38.7 / 21.5 / 24.5 / 0.9 / 7.2, sat 0.39, val 0.45, dark 0.13: orange just under |
| Reviews | v1: Yes; the frame is crowded and heads are cut at the edges; both 0.5 s pairs read as a flat card. v1.1: the v1 verdict stands for the delivered film. |
| Polish | Grade only. |

### Shot 13: the label slap (punch-in)

| Field | Value |
|---|---|
| Time | clock 27.957-28.922; g839-867 (29 frames, 0.97 s), the shortest shot |
| Narration | “ทางด่วนพายุ” "'the Storm Expressway'" |
| Captions | “ทางด่วนพายุ” 27.91-28.92 (starts 0.05 s before the cut) |
| Beat | nickname, element 6 (the nickname made a physical object) |
| Set, light | office, office_day |
| Camera | Class insert. `label_insert` (-0.249, -1.811, 2.887) looking at (0.125, -0.05, 2.87), 22 mm, 1.84 D from the label, raked 12 deg from below-left. Punch-in: opens at 1.30 x the distance and lands in 4 frames (cubic ease-out; peak 118 px/frame at g839, plate streak g839-840); 2-frame shake on the slap (roll 0.45 then -0.30 deg, g843-844); drift push easing in to 5 %/s. |
| Cast, marks | The chief's hand only (`bossH13`, hand card at scale 1.5, body and head beyond the right or top edge in every frame). |
| Acting | Hand flies the label in (from 0.30 D right, 0.22 D off the wall, scale 1.10, accelerating), slaps it flat at g843 (28.00); label rocks +4 / -2 deg for 2 frames; lower-right corner curls 0 to 0.55 over g846-853. Red pin appears under the thumb g847, thumbed home g849-851 (28.25). Bare hand registration 2.75 px max. |
| Props, devices | THE LABEL (`set_label`, `nickname_label` art at 2400 px, res 'hi'): cream strip, red-brown Thai brush lettering ทางด่วนพายุ, hung on `label_rect` from its pin, tilt 4 deg, centred over the end of the line within 0.036 D (about 15 px). Stays for the rest of the film. White speed lines: 46 radial wedges centred on the label over g839-844, drawn in the take's post. |
| Transition | In: punch-in cut with speed lines (straight cut, conform join 10). Out: dissolve 11 frames into shot 14 (g863-873). |
| Sound | Cues: 28.03 punch-in whump; 28.06 laughter tail ducking out; 28.10 paper slap; 28.35 pin thunk; 28.40 muted trumpet wah-wah. In the mix: 36 thump_jab 28.100 (paper slap, -12). |
| Heads | none (hand card 539-714 px, head outside the frame) |
| Reference | B3 b/t05.0 (f146-160: punch-in cut with speed lines, held close, 0.4 s); a/t32.0-t33.0 (the nickname held up to the lens: THE CLICKETY CLACK LINE!). Copied: the punch-in with speed lines, the nickname as a readable prop held close. |
| Take, runner | `v3/film/s13/` (shot.py on `../s10/otake.py`). Rendered g839-874. |
| Changed from plan | Camera 1.84 D from the label, not 1.1 D (at 1.1 D the 1.15 D label would be about 820 px wide; 1.84 D keeps about 480 px). |
| Colour row (v1) | 23.8 / 36.7 / 26.5 / 0.3 / 1.8, sat 0.43, val 0.50, dark 0.07: out on red, dark. v1.1: orange 41.5. |
| Reviews | v1: Yes; a clean insert, the label reads in under a second. v1.1: Yes. |
| Polish | Grade only. |

### Shot 14: the official forecast (teletype, crash push onto the sheet)

| Field | Value |
|---|---|
| Time | clock 28.922-31.853; g868-955 (88 frames, 2.93 s) |
| Narration | แล้วคำพยากรณ์ทางการก็ออกไป ฝนตก ลมกระโชก "Then the official forecast went out: rain, gusty winds." |
| Captions | แล้วคำพยากรณ์ 28.92-29.79 / ทางการ 29.79-29.99 / ก็ออกไป 29.99-30.70 / ฝนตก 30.70-31.13 / ลมกระโชก 31.13-31.85 |
| Beat | forecast_out, element 7 (the official verdict against him) |
| Set, light | office, office_day |
| Camera | Class eye, then insert. ONE take. (a) `window_tt` (-3.2, -2.6, 2.1) looking at (2.6, -1.0, 1.85): truck right 0.30 D with a push of 8 %/s, the aim panning back left 0.55 D so both men stay in frame. (b) Crash push x3 g899-912 (29.85-30.30, 14 frames, quint/sine), peak 416 px/frame at the corners, plate streak g903-908 (actors sharp), onto `sheet_fill_camera` of the quad at fill 0.86, small arc up. (c) Tilt down from header and stamp to the two typed lines (look point 0.26 to 0.065 D above the sheet centre), a small push that dies away, creep from g951. |
| Cast, marks | Hero near, low, left at (-0.45, -1.25), frozen, `expr='worried'` (`acting.hero_listener`), one blink g891; chief by the teletype at (2.35, -1.75), 1.7 D off the map wall, three-quarter yaw -0.35 (`acting.boss_stamp_thrust`). |
| Acting | Teletype feeds the sheet up, stepped, g872-897. Chief brings the rubber stamp down on the header g898 (29.82, 'ทางการ'; prop pinned, 0.0 px over 42 frames), tears the sheet off g902, thrusts it at the lens g906, smug nod. The hi-res sheet quad takes over from the puppet's paper at g905 inside the crash; two ink finger balls on the sheet's bottom edge. Words pop (4-frame scale 1.08 and ink bloom) at g928 'ฝนตก' and g942 'ลมกระโชก'. No mouths. |
| Props, devices | Forecast sheet (`set_sheet`): English header U.S. WEATHER BUREAU / OFFICIAL FORECAST / SEPT. 20, 1938, round red Thai stamp ทางการ (`set_stamp`), typed Thai ฝนตก / ลมกระโชก. Map state at the left edge: line, smudge 3, crumbs, chalk, ghosts, tick, label, spinner. Window-bar shadows on the sheet. |
| Transition | In: dissolve 11 frames from shot 13. Out: match dissolve 13 frames, paper to paper, into shot 15 (g950-962). |
| Sound | Cues: 28.92 soft whoosh; 29.05 teletype clatter; 29.70 carriage bell; 29.92 stamp thump; 30.05 paper tear; 30.15 crash whoosh, paper snap; 30.95 typebar clack and bell ('ฝนตก'); 31.40 clack ('ลมกระโชก'); 31.60 rain pre-lap, snare roll and cymbal choke. In the mix: 37 teletype 29.050-31.50 (RMS -33.7); 19 rain_drizzle 31.600-37.45 (ambience, RMS -41.5 in v1, -34 in v1.1). |
| Heads | Hero 261-336 px in (a) (435 at g904, leaving frame left in the crash); chief 141-168 px in (a), then behind the sheet. |
| Reference | B7 b/t18.0-t20.3 (near still on the figure, then crash push x3.23 in 0.5 s onto the object); a/t31.5-t32.5 (a paper held up to the lens, printed words full frame). Copied: the crash push onto the printed verdict and the words filling the frame. |
| Take, runner | `v3/film/s14/` (shot.py on its own `otake.py`, copied from s04). Rendered g860-964. |
| Changed from plan | Chief moved to (2.35, -1.75) so the stamp reaches the header; hero moved 0.7 D back from `hero_tt` so the push does not throw him out before the stamp; crash starts g899, one frame after the stamp, so the stamp reads in the wide; fill 0.86, not 1.0, so the lines land within 20 px of the newspaper lines of shot 15 ('ฝนตก' about 440 px wide at (360, 620)); the typed words are on the sheet from the start and pop instead of appearing. |
| Colour row (v1) | 33.5 / 32.1 / 25.7 / 1.5 / 4.7, sat 0.36, val 0.57, dark 0.13: sat under (cream paper fills half the take) |
| Reviews | v1: Yes; the sheet fills the frame; saturation low (0.36). v1.1: Yes. The conform found the typed ลมกระโชก on the thrust sheet at y 880-960 under the caption ก็ออกไป for about 0.8 s (g902-925): two Thai texts overlap. |
| Polish | Grade: the brightest caption band of the film (g936, 12 % of the band above luma 0.85). |

### Shot 15: next morning, the newspaper (kitchen)

| Field | Value |
|---|---|
| Time | clock 31.853-33.767; g956-1012 (57 frames, 1.90 s) |
| Narration | เช้าวันต่อมา ที่นิวยอร์ก ลองไอแลนด์ "The next morning, in New York, Long Island" |
| Captions | เช้าวันต่อมา 31.85-32.66 / ที่นิวยอร์ก 32.66-33.21 / ลองไอแลนด์ 33.21-33.93 |
| Beat | false_defeat, element 7 |
| Set, light | kitchen (`v3/set3d_kitchen/kitchen3d.py`), kitchen_grey (key sun (0.56, 0.53, 0.54), angle 2 deg, front-left above; ambient (0.25, 0.27, 0.52) falling 1.3 x y / 9 toward the lens; window drizzle loop at emission 1.0; grade saturation 1.22) |
| Camera | Class top_down, then eye. g947-976 `steep`: 0.85 D from the weather box, about 44 deg down, drifting in 4 %/s and sliding left (1.3-1.4 px/frame). Crash pull-out g977-994 (32.48-33.05, 17 frames) into THE TABLE FRAMING (`table`: (0.225, -2.42, 1.80) looking at (0.225, -0.30, 1.07)) with a trailing tilt up and a small arc; peak 67 px/frame about g985; only g982 and g985-987 streaked (plate streaked, arm and cup sharp). g995-1021 drift push 5 %/s toward the cup. Linear runs at g947 and g1003 (disclosed). |
| Cast, marks | No figure: beach_man's ink arm and ball hand (`puppet._ink_limb`, `puppet._hand`; limb 0.058 D, hand radius 0.063 D) on a card 0.06 D in front of the saucer rim. |
| Acting | Hand enters frame right about g988, sets the cup on its saucer at g994 (33.05; ball centre 17.6-19.6 px from the rim point it holds), lets go and leaves g998-1008. The coffee shows 6 frames of faint settling rings, then stays dead still. |
| Props, devices | Newspaper weather box (Thai: header พยากรณ์อากาศวันนี้, body ฝนตก ลมกระโชก; same words as shot 14), folded, leaning back at 62 deg on a bread box; red-check oilcloth split into red (#c9402a) and orange (#dc6c26) bands; cup and saucer; calendar leaf 21; four-pane window with grey sky and sea, rain streaks; blue gingham curtains. |
| Transition | In: match dissolve 13 frames, paper to paper (change of time). Out: dissolve 13 frames into shot 16 (g1007-1019). |
| Sound | Cues: 31.85 far rooster; 31.95 kitchen tone; 32.58 whoosh; 32.72 arm swish; 32.75 newspaper rustle; 33.15 cup clink; 33.28 hand leaves; 33.40 radio murmur. In the mix: 20 office_tone 31.950-33.80 (RMS -34.1, as the kitchen tone); 38 whoosh_fast 32.580 (-17). |
| Heads | none. Text: ฝนตก 133-139 px tall in the steep start, 84-86 px in the table framing; all Thai between y 290 and 575 from g994. |
| Reference | B7-8 b/t20.0-t22.0 (crash pull-out from the goblet: "not even a ripple in the emperor's wine") and the 12-frame "next morning" dissolve into B18; a/t36.0 (time jump carried by a text prop). Copied: the pull-out from a printed word to a still cup, the paper-to-paper time jump. |
| Take, runner | `v3/film/s15/` (shot.py on `set3d_kitchen/kshot.py`; QA `kqa.py`). 8 samples (measured identical to 12). Rendered g947-1021. |
| Changed from plan | Folded newspaper (a flat page could not hold its Thai above y 600, keep ฝนตก at 70 px or more and show the window): the masthead and dateline are on the folded-back half, out of frame. Steep start 44 deg, not 70 (the page would be edge-on). Pull-out x0.6, not x0.3 (x0.3 leaves ฝนตก at about 40 px, below the 70 px shot 26 needs on the same framing). The hand brings the cup in on its saucer (an empty saucer filled a third of the steep frame). The chair is out of frame. |
| Colour row (v1) | 52.1 / 40.2 / 6.5 / 0.1 / 1.1, sat 0.43, val 0.61, dark 0.02: out on red, orange, blue, dark (all warm) |
| Reviews | v1: Partly; the whole frame is warm (red and orange 92 %, blue 6 %), no cool shade. v1.1: Partly (unchanged, blue 7 %). |
| Polish | Grade: saturation 0.93. |

### Shot 16: grey sky, drizzle (the false defeat on the beach)

| Field | Value |
|---|---|
| Time | clock 33.767-36.185; g1013-1085 (73 frames, 2.43 s) |
| Narration | ตื่นมาเจอแค่ฟ้าเทาๆ ฝนปรอยๆ "woke up to nothing but a grey sky and a drizzle." |
| Captions | ตื่นมาเจอแค่ 33.93-34.62 / ฟ้าเทาๆ 34.62-35.34 / ฝนปรอยๆ 35.34-36.19 (delivered voice starts 0.16 s after the cut) |
| Beat | false_defeat, element 7 |
| Set, light | beach, grey_drizzle (= `GREY_DRIZZLE`; rain streaks of the set, `set_rain` 0.35) |
| Camera | Class eye. THE BEACH FRAMING `beach_shore_eye`: loc (-7.4, 7.0, 2.6), azimuth -3.9 deg, pitch -3 deg (sea and horizon at left, LONG ISLAND sign mid-right, cottage_07 and poles at right). Truck right and push to 34.64 (camera x -7.40 to -6.94, pitch -3.0 to -2.6), 0.4-1.0 px/frame. Snap g1042-1056 (34.64-35.11, 14 frames) on 'ฟ้าเทาๆ': tilt up to pitch +46 deg and 22 deg right, peak 167 px/frame (weather vane and chimney of cottage_07 at the bottom edge). Creep in the sky (2.4 px/frame) to 35.30. From g1062 tilt back down, 86 easing to 9 px/frame, to pitch +6 deg by g1088. Streaked (plate + matte) g1045-1053 and g1063-1067. |
| Cast, marks | beach_man (`man16`) walks off the porch (`boss_walk` with cast beach_man: step 0.34, bob 0.30, sway 0.10, `expr='neutral'`); beach_woman far on the porch of cottage_07 at (9.15, 1.05), hand out, held (`woman_hand_out`). Faces three-quarter or profile. |
| Acting | Steps off the landing g1019 (33.85), stretches g1023 (`beach_stretch`), looks up g1038 (34.5). After the tilt: palm out g1065 (`beach_palm_out`), drops land at clock 35.50, 35.65, 35.80; shrug g1082 (`beach_shrug`, unimpressed). No mouths. |
| Props, devices | LONG ISLAND fence sign, grey sea, wet sand, no cast shadows, rain streaks, weather vane and chimney. |
| Transition | In: dissolve 13 frames (kitchen to beach). Out: dissolve 14 frames into shot 17 (g1079-1092). |
| Sound | Cues: 33.77 dull slow surf and drizzle bed; 33.85, 33.95 steps; 34.10 stretch creak; 34.74 soft whoosh; 34.98 lone gull; 35.05 far foghorn; 35.60, 35.75, 35.90 drop plips; 36.05 clarinet droop. In the mix: 21 beach_calm 33.770-36.22 (RMS -34.0). |
| Heads | beach_man 152 px at g1004 growing to 248 px at g1094, centre 0.45-0.48 H at eye level; his head leaves the bottom of the frame during the snap and tilt g1046-1076 by design; woman 46-51 px. The conform found his head rising through the caption band (y 880-950) on g1068-1078. |
| Reference | B7 b/t18.0-t20.0 ("a ball fell, but nothing happened") and a/t36.5-t38.0 (the hero looks and shrugs); tilt as B12. Copied: the anticlimax shrug, the tilt to the sky. |
| Take, runner | `v3/film/s16/` (shot.py on `set3d_ext/beach/bshot.py`). Rendered g1004-1094. |
| Changed from plan | None in staging. |
| Colour row (v1) | 24.0 / 4.2 / 65.4 / 1.1 / 5.2, sat 0.24, val 0.65, dark 0.01: out on six of eight. v1.1: 33.0 / 6.2 / 57.1 / 1.4 / 2.1, sat 0.31, val 0.67, dark 0.06 (five out). |
| Reviews | v1: No; washed out (sat 0.24, 1 % darks), and the tilt lands on an empty grey sky with half a face at the edge; no reference frame is this empty. v1.1: No; more colour and warmer sand, but the sky turned lavender-violet and the empty-sky frames at 35.0-35.3 s are still there. |
| Polish | Grade: gain 0.88, contrast 1.30, gamma 1.08, sat 1.60, white balance R 1.04 / B 0.95, lower frame -22 %, haze 0.10 at y 0.38 H, bloom 0.7, white protect at sat 0.13. Better next time: keep a face or the palm in frame through the tilt (palm in by 35.1 s), and grade toward grey, not violet. |

### Shot 17: the chief strolls in whistling (rug level)

| Field | Value |
|---|---|
| Time | clock 36.185-37.422; g1086-1122 (37 frames, 1.23 s) |
| Narration | หัวหน้าเดินผิวปากมา "The boss strolled over whistling:" |
| Captions | หัวหน้า 36.19-36.46 / เดินผิวปากมา 36.46-37.41 |
| Beat | boss_quote_2, elements 8 and 6 (set-up of the second mocking) |
| Set, light | office, office_grey (`set3d_ext/light`: `INTERIOR_DAY` sun geometry kept, key x0.3 and cool, grey sky card, bulbs on, grade desaturated) |
| Camera | Class low. Rug-level truck: lens 0.70 to 0.90 D above the floor, 4.5 D from the map wall, truck left 0.6 D, pitch +14.5 deg, pan from 11.6 to 15.4 deg right of the wall normal; the parallax carries the chief right to left across the frame. Speed 0.47-4.3 px/frame (median 3.18); no snap; settles over the last 6 frames (ease, then 0.4 %/frame creep). |
| Cast, marks | Chief `boss17` walks a diagonal from (2.20, -0.82) to `boss_mark` (1.30, -0.42) at 0.72 D/s (`acting.boss_whistle_stroll`: step 0.68 s, bob 0.47 D, sway 0.13 D, hands behind his back, pointer under the near arm), planted on a contact phase at g1116. Hero `hero17` at `gloat_near` (2.4, -1.7), three-quarter facing the map side (`acting.hero_slumped`: lean 4 deg, head down, sad, turning the pencil stub). |
| Acting | Chief: held whistle drawing (eyes shut, brows up, round pucker; never flapping); three note glyphs (`acting.note_glyphs_svg`) leave the mouth at g1098, g1107, g1116 (36.5, 36.8, 37.1). Hero: frozen, one blink g1113 (37.0); his mouth never moves. |
| Props, devices | Map: line with arrow head, smudge 3, chalk, six ghosts, tick, the Thai label pinned (top left, not featured), spinner turning; calendar leaf 21 set but off frame. The rain card on the window is just outside the frame (rain is a sound bed only). |
| Transition | In: dissolve 14 frames (beach to grey office). Out: hard cut into shot 18. |
| Sound | Cues: 36.20 rain on the window (bed); 36.30 whistled tune (the theme); 36.52, 37.20 heel clicks at the walk's contact frames, 37.40 heel settle; 37.10 very distant thunder. In the mix: 22 office_tone 36.200-37.44 (RMS -33.0); 39 whistle_tune 36.300 (peak -14). |
| Heads | Chief 175-187 px at y 381-511; hero 229-237 px at y 400-472; near / far 1.26-1.32. |
| Reference | A10's tail a/t43.0-t44.0 ('and his boss...': he strolls into frame, seen low, torso and legs), just before A's one hard cut; walk numbers from B17. Copied: the low stroll into frame right before the hard cut. |
| Take, runner | `v3/film/s17/` (shot.py on its own `otake.py`, the grey/storm office runner of s17, s18, s25). Rendered g1077-1122. |
| Changed from plan | Lens 0.70 to 0.90 D (plan 0.7 rising 0.2); pitch +14.5 (plan +16, lowered so heads sit near 0.35 H); pan turns the other way (11.6 to 15.4 deg; the plan's 20 to 10 put the hero left of centre and the chief at the edge). Chief starts 0.82 D off the wall (plan 1.3: any path 1.3 D off the wall stays behind the near hero) and emerges from behind the hero in the dissolve; his head is 175-195 px, not 230. Heel clicks at the real contact frames. |
| Colour row (v1) | 37.2 / 37.6 / 16.4 / 1.2 / 3.8, sat 0.39, val 0.47, dark 0.14: in band. v1.1: orange 40.9. |
| Reviews | v1: Yes; very short (1.2 s), the chief's near-profile torso dominates. v1.1: Yes; the closest office frame to clip B's look. |
| Polish | Grade: lamp bloom. |

### Shot 18: "Where's your Storm Expressway? Stuck in traffic?" (G again)

| Field | Value |
|---|---|
| Time | clock 37.422-39.617; g1123-1188 (66 frames, 2.20 s) |
| Narration | “ไหนล่ะ ทางด่วนพายุของแก รถติดเหรอ” "'So where is that Storm Expressway of yours? Stuck in traffic?'" |
| Captions | “ไหนล่ะ 37.41-37.75 / ทางด่วนพายุ 37.75-38.33 / ของแก 38.33-38.83 / รถติดเหรอ” 38.83-39.62 |
| Beat | boss_quote_2, elements 8 and 6 |
| Set, light | office, office_grey |
| Camera | Class eye. HARD CUT onto the chief in close-up: G's camera position at 41 mm, aimed at his head. Crash zoom-out g1125-1141 (snap easing; move g1127-1137, peak 73 px/frame) landing exactly on G at 22 mm (x0.52). G drift: 2.5 %/s lens creep plus 0.02 D/s truck. Snap g1160-1172 (move g1162-1168, peak 52) to `G_prime` (G's position, 30.36 mm, look (0.95, -0.40, 2.80)), then drift. From g1188 the crash push toward the map (s19's curve and landing pose `rake_spinner`, lens 30.8 to 22 mm), peak 146 px/frame at g1194 in the out handle. Sprite resolution switches from 512 to 320 px per D at g1131 inside the zoom-out. |
| Cast, marks | Chief `boss18` at `boss_mark`; hero `hero18` at `gloat_near` (`hero_sad_listener`). |
| Acting | Chief's mouth follows `acting.loudness(37.409, 39.617)` from g1125 to g1191 (flat smirk before and after). 'ไหนล่ะ': hand shading his eyes, mock search. 'ทางด่วนพายุ': taps the pinned label twice (clock 37.98, 38.20; pointer tip pinned on the label paper, 0.00 px, angle -100 deg), the label swings about its pin (damped 9 and 11 deg). 'ของแก': turns to the hero over 6 frames and swings the pointer at him with the same left hand (g1153-1158). 'รถติดเหรอ': `acting.boss_lean_wink(horn=True)`: leans, mimes squeezing a car horn, held wink g1184-1187. Hero: frozen, sad, eyes down; blinks 37.7, 38.3; sweat from 38.4; eyes shut 4 frames from 38.9 (mostly out of frame in G'). His mouth never moves. |
| Props, devices | Label ทางด่วนพายุ unobstructed (about 180 px in G), red line with arrow, chalk curve, pointer. |
| Transition | In: HARD CUT, 3 frames before '"ไหนล่ะ'. Out: match dissolve 12 frames inside the crash push (g1183-1194; the map behind the chief becomes the frame). |
| Sound | Cues: 37.42 the whistle stops dead (rimshot); 37.50 crash whoosh out; 37.52 tuba mocking variant; 37.60 slide-whistle rise; 38.08, 38.30 pointer taps, label flutter; 38.50 sweat plink; 38.55 pointer swish; 38.65 whoosh in; 39.10 squeeze-horn honk-honk; 39.45 wink ting; 39.60 first real thunder roll. In the mix: 40 whoosh_fast 37.420 (-14); 41 thunder_low 39.600-42.00 (-14). |
| Heads | Close-up chief 321-325 px (plan 330). In G: chief 173 px, hero 244 px, ratio 1.41. In the push handles the near hero reaches 748 px as the lens passes him. |
| Reference | A11 44.10-47.70 (hard cut in at f1322, crash zoom-out x0.30, push x1.38, drift; near hero frozen with blinks: 'See, even your gaps know you were wrong.'), mirrored; B16 (b/t40.5-t43.0). Copied: the hard cut into the second mocking, the zoom-out into the same two-shot, the x1.38 push. |
| Take, runner | `v3/film/s18/` (shot.py on `../s17/otake.py`). Rendered g1123-1196. |
| Changed from plan | The zoom-out is x0.52, not x0.30 (the 330 px close-up and G's 173 px head fix the ratio). G' crops the near hero to his cap and cheek, so his eyes-shut beat is mostly out of frame. A first final had the pointer jump hands at g1153 and vanish at g1168; g1150-1196 were rendered again. |
| Colour row (v1) | 47.1 / 27.8 / 12.4 / 1.2 / 4.1, sat 0.38, val 0.46, dark 0.15: out on red, blue, sat, dark (crimson wallpaper and the red line under the grey key) |
| Reviews | v1: Yes; the callback reads; it opens on a neutral medium shot of the chief, not the planned grin close-up. v1.1: Yes; label readable. |
| Polish | Grade only (no per-shot setting). |

### Shot 19: the mechanism (one 7.7 s take on the wall map)

| Field | Value |
|---|---|
| Time | clock 39.617-47.296; g1189-1418 (230 frames, 7.67 s), the longest shot |
| Narration | ระหว่างนั้น กลางทะเล ความกดอากาศสูงสองก้อน บีบพายุไว้ เหมือนกำแพงสองฝั่ง / เหลือช่องเดียว ตรงขึ้นเหนือ / ในช่องนั้น เลี้ยวไม่ได้ "Meanwhile, out at sea, two masses of high pressure were squeezing the storm, like walls on both sides. One corridor was left, running straight north. Inside that corridor, there is no turning." |
| Captions | ระหว่างนั้น 39.62-40.25 / กลางทะเล 40.25-40.90 / ความกดอากาศสูง 40.90-41.65 / สองก้อน 41.65-42.24 / บีบพายุไว้ 42.24-43.09 / เหมือนกำแพง 43.09-43.59 / สองฝั่ง 43.59-44.21 / เหลือช่องเดียว 44.21-45.04 / ตรงขึ้นเหนือ 45.04-45.74 / ในช่องนั้น 45.74-46.36 / เลี้ยวไม่ได้ 46.36-47.30 |
| Beat | meanwhile and mechanism, elements 9 and 11 |
| Set, light | office wall map as terrain (`office3d` + `set3d_ext/props` + `set3d_ext/mech/office_mech.py`), office_grey |
| Camera | Classes insert, high, low, top_down; one renderer. (0) g1188-1205: finishing the crash push x6 past the two men into `rake_spinner` (30 deg rake from below-left, 0.8 D from the paper); spinner 29 to 112 px at (393, 753); drift with creep and orbit g1205-1225. (1) Snap g1225-1238 on 'ความกดอากาศสูง': x0.45 back and rise into `rake_north` (35 deg rake looking north), both walls in frame, N.Y. y 516; drift push 10 %/s with an accelerating orbit g1238-1292. (2) Snap g1292-1308 on 'เหมือนกำแพง' into THE CORRIDOR VIEW (`corridor_cam`, mech version: lens 0.345 D above the paper, 0.155 D west of the chord, up = wall normal); N.Y. at (379, 652); creep u_lens -0.17 to -0.13 g1308-1328. (3) Snap g1328-1345 on 'เหลือช่องเดียว' to the plan view (`plan_view_start`, square on, roll -12 easing to 0 by g1374), truck north 0.6 D along the lane g1345-1372 (`plan_view`, N.Y. y 28 to 363). (4) Snap g1372-1385 on 'ในช่องนั้น': truck back and push x2 onto the spinner (`spinner_high`, 52 deg rake); 6-frame shakes on the bonks g1396 and g1408; near still from g1413. Snap peaks 160-358 px/frame. |
| Cast, marks | No characters. |
| Acting (props) | Spinner speeds up (`set_spinner_fx`), creeps to the foot of the line. Terraces swell out of the paper, four steps each (`set_wall`): east g1233-1251, west g1254-1269. Squeeze g1272-1293 (walls slide in, the spinner squashes tall, judders, sweats one drop). Walls lock: west g1299, east g1311. Chalk curve crumbles g1314 (`set_chalk`). Lane with white dashes unrolls g1335-1356 (`set_lane`). Compass N pings g1358 (`set_compass`). Bonks: east wall g1396, west wall g1408, with no-turn pictograms (`set_picto`; the west card turned yaw 60 / tilt 35 to face the camera). |
| Props, devices | Two pressure-wall terrace meshes with a Latin H, tops 0.50 D (gate: lens 0.35 D, PASS without fallback); lane decal; compass; pictograms; 6000 px map; the corridor bends with the hand-drawn line (0.154 D west of the chord at u 0.5). Every position follows `S.track_point(u)`. |
| Transition | In: match dissolve 12 frames inside the crash push (g1183-1194). Out: dissolve 9 frames into shot 20 (g1415-1423). |
| Sound | Cues: 39.62 long crash whoosh with wind; 40.30 spinner whirr rising; 41.05 whoosh; 41.10-42.18 eight low terrace thuds; 42.40 rubber-squeeze creak; 42.65 sweat plip; 43.30 and 43.70 stone-wall booms; 43.34 whoosh down; 43.80 chalk crumble; 44.50 road unrolling zip and neon hum; 44.55 whoosh up; 45.25 compass ping; 45.95 whoosh; 46.55 and 46.95 bonks; 47.15 spinner grumble. In the mix: 23 wind_storm 39.620-44.62 (RMS -33); 42 thump_jab 43.300 (wall boom, -11.1); 24 wind_storm 45.000-50.00 (RMS -30); 43 thump_jab 46.550 (bonk, -14). |
| Heads | none. Spinner 92-200 px across the framings; 410-440 px at the bottom right in the corridor view. |
| Reference | B19 b/t48.5-t55.0 (inside the jar: ONE 6.53 s rotating top-down take that shows the parts as the narrator names them, then goes low and close to the part that acts) for form and choreography; A12 48.23-54.23 (rail point of view, a/t48.0-t51.5) for the corridor view; A5 (7.67 s take with five snaps) for the length; A10 (a/t39.0-t43.0) for the bonk test. Copied: one long take that names the parts on their words, a point-of-view down the corridor, four snaps. |
| Take, runner | `v3/film/s19/` (shot.py on `set3d_ext/mech/office_mech.py`; `post.py`). Rendered g1181-1425. |
| Changed from plan | The gate was run on the hand-drawn corridor: lens on the line hid N.Y. behind the bend, so the lens sits 0.155 D west of the chord (`M.clear_lateral`). Walls 0.50 D (plan 0.45-0.70). The far Thai label is seen rotated by the rake's dutch angle in phases 0-1. The land wall appears in one frame at g1255 (popcheck flag), not as a swell. |
| Colour row (v1) | 24.3 / 26.0 / 45.8 / 0.4 / 3.2, sat 0.36, val 0.47, dark 0.12: out on red, blue, sat. v1.1: 33.4 / 38.0 / 26.6 / 0.4 / 1.1, sat 0.38, val 0.53, dark 0.12 (orange at the edge). |
| Reviews | v1: Partly; pale grey-lavender blocks with an "H" read as an explainer diagram (blue 46 %, sat 0.36); the reference's explainer beats keep warm light and rich material. v1.1: Partly; the lit faces of the blocks are warm pink-beige, but it is still a diagram. |
| Polish | Grade: walls 0.80 (warm key on the pale walls), sat 1.12, white balance R 1.03 / B 0.95, white protect off. Better next time: give the mechanism real materials and warm light in the render, not in the grade. |

### Shot 20: the launch past the 100 km/h sign (corridor view)

| Field | Value |
|---|---|
| Time | clock 47.296-50.529; g1419-1515 (97 frames, 3.23 s) |
| Narration | ลมในช่องซัดพายุขึ้นเหนือ เกือบร้อยกิโลเมตรต่อชั่วโมง "The wind in the corridor flung the storm north at almost 100 kilometres per hour." |
| Captions | ลมในช่อง 47.30-47.90 / ซัดพายุ 47.90-48.38 / ขึ้นเหนือ 48.38-48.91 / เกือบ 100 48.91-49.42 / กิโลเมตร 49.42-49.92 / ต่อชั่วโมง 49.92-50.53 |
| Beat | mechanism, element 11 |
| Set, light | office wall map as terrain, office_grey |
| Camera | Class low (worm's eye on the map). g1412-1443 `corridor_cam` (lens 0.35 D up, 0.15 D west of the chord, u -0.115 to -0.09), creep 6 %/s accelerating; N.Y. at (381, 647). Launch snap g1443-1467 (47.95-48.45): the lens rides 0.255 u behind the flung spinner along the line (0.50 D of travel in 1.1 s), 5 Hz shake decaying. Brake to rest (Hermite) g1467-1484 beside the speed sign, look turning to it; push with decaying shake g1484-1522 (u_lens 0.36 to 0.39). Peak 223 px/frame at g1470. |
| Cast, marks | No characters. |
| Acting (props) | Wind arrow waves (`set_wind`) at g1425, g1434, g1443; the first two flap the no-turn pictograms and fold them into the wall faces; the third squashes the spinner flat (g1440-1443); launch g1443: it rockets north tall and leaning forward (squash 1.47 to 1.12, wobble 16 deg, motion-blur disc) with the red-hot wake (`set_wake`); swerves 0.04 D west past the sign's pin and passes the sign at g1476 (49.10); the sign spins two turns (ease-out, 22 frames), rocks +-9 deg and settles on '100' at g1512 (50.30). The spinner runs on to u 0.985 by g1500. |
| Props, devices | Speed sign (`set_speed_sign`): red ring, '100', Thai กม./ชม.; readable 49.2-50.3. Conform overlay: 42 white radial speed lines about the vanishing point (360, 470), g1442-1472. |
| Transition | In: dissolve 9 frames. Out: dissolve 10 frames with the whip pull-out into shot 21 (g1511-1520). |
| Sound | Cues: 47.30 whoosh; 47.50, 47.80, 48.10 gusts rising; 48.10 cannon thwump and slingshot twang; 48.30 doppler roar bed 48.2-50.4; 49.20 pass-by vwip; 49.22 sign-spin ratchet; 50.40 sign settles (ting). In the mix: 24 wind_storm (continues to 50.00); 44 thump_jab 48.100 (gust 3; peak -13 in v1, -15 in v1.1 after the review measured -9.5 dBFS summed with the wind under a word). |
| Heads | none. Speed sign 420-435 px across at y 315-365 (plan 300 px or more, above y 600). |
| Reference | A12 (rail point of view, travel with pans, x6.3, passing a roadside figure at a/t52.0-t54.0) with A8's 5 Hz shake; B20 (b/t55.5-t58.0: the action step shown close on the object). Copied: the travelling point of view past a roadside object, the shake. |
| Take, runner | `v3/film/s20/` (shot.py on `s20/mc.py`, the map scene and camera grammar shared by s20-s22; `post.py`). Rendered g1412-1522. |
| Changed from plan | Speed sign at 0.42 D, below the 0.50 D wall tops, inside the lane (a sign above the walls made the camera look into the ceiling and lose the corridor); post moved behind the disc so it does not cross the '100'. Pictograms fold away (the lens flies through them otherwise). Sign 420 px or more, not 300. The far Thai label is seen upside down and mirrored (up = wall normal). |
| Colour row (v1) | 11.8 / 18.1 / 62.2 / 1.0 / 6.7, sat 0.35, val 0.49, dark 0.10: out on red, orange, blue, sat. v1.1: 28.1 / 33.3 / 30.7 / 1.2 / 6.7, sat 0.35, val 0.55, dark 0.10. |
| Reviews | v1: Partly; a graphic road-sign world, very blue (62 %), readable but cold. v1.1: Partly; warmer (blue 31 %), still a road-sign world. |
| Polish | Grade: walls 0.85, sat 1.32, white balance R 1.05 / B 0.93, white protect off. |

### Shot 21: hardly any storm this fast (whip pull-out, ghost storms)

| Field | Value |
|---|---|
| Time | clock 50.529-52.371; g1516-1570 (55 frames, 1.83 s) |
| Narration | แทบไม่เคยมีลูกไหนเร็วเท่านี้ "Hardly any hurricane had ever moved this fast." |
| Captions | แทบไม่เคย 50.53-51.01 / มีลูกไหน 51.01-51.65 / เร็วเท่านี้ 51.65-52.37 |
| Beat | mechanism, element 11 (the comparison) |
| Set, light | office wall map as terrain, office_grey |
| Camera | Class high (oblique). Whip pull-out x0.2 g1509-1529 (finished by 50.9), peak 403 px/frame at g1517: from a chase view inside the lane (0.30 D up behind the streak, up = wall normal) to a high oblique from the south-east (rake azimuth +16, elevation 62, 1.30 D, up = +z, north up-frame); the direction swing gives the pan. Drift push 6 %/s north g1529-1579: target travels north beside the streak (u 0.44 to 0.55), distance x 0.94^t, elevation +1.5 deg/s, azimuth -2 deg/s. Longest constant-speed run of the film: g1543-1563 (21 frames). |
| Cast, marks | No characters. |
| Acting (props) | Our storm = spinner with motion-blur disc (fast 0.95), squash 1.15, wobble 14 deg, red-hot wake 0.24 u long, replayed from u 0.25 (g1516) to 0.65 (g1571). Three grey ghost spinners (`set_ghost_spinner`, scale 0.66, alpha 0.6) crawl along their faded curved tracks at a sixth of the speed; overtaken at g1530 (ghost 2, with the snail shell `set_shell`), g1542, g1554; each wobbles and swells 22 % in the poof. Ghost tracks brightened 0.35 to 0.60. |
| Props, devices | Walls, lane, label at the top, speed sign beside the lane. |
| Transition | In: dissolve 10 frames with the whip pull-out (g1511-1520). Out: dissolve 14 frames into shot 22 (g1564-1577). |
| Sound | Cues: 50.60 whip whoosh; 50.70 racing zip (doppler); 51.00, 51.40, 51.80 soft poofs; 51.10 plodding tuba notes; 51.90 rising whine. In the mix: 45 whoosh_whip 50.600 (-13). |
| Heads | none. Storm about 300-320 px; ghosts about 40-60 px. |
| Reference | B21 first half, b/t58.5-t59.5 (f1757-1790: whip pull-out x0.20 with 1124 px of pan: the comparison of scale); A6 fast pans. Copied: the whip pull-out into a comparison. |
| Take, runner | `v3/film/s21/` (shot.py on `../s20/mc.py`, `../s20/post.py`). Rendered g1509-1579 (in parallel with s20 by accident; no effect on frames). |
| Changed from plan | The planned `atlantic_rake` (30 deg, 1.9 D) cannot see into the 0.22 D lane between 0.50 D walls (ray-cast: no lane point visible): elevation 62 deg, 1.30 D used, tighter than "the whole western Atlantic". The ghost tracks run under the east wall once they curve out, so the overtakes happen within about 0.2 D of map and read small. |
| Colour row (v1) | 15.3 / 8.7 / 67.0 / 1.3 / 7.0, sat 0.28, val 0.52, dark 0.12: the coldest shot. v1.1: 33.4 / 42.8 / 19.0 / 1.1 / 2.3, sat 0.34, val 0.60, dark 0.12 (orange over). |
| Reviews | v1: No; the coldest shot, the ghost storms illegible at phone size. v1.1: Partly (was No); the walls are sand-coloured and blue is 19 %, but the ghosts are still too small and grey. |
| Polish | Grade: walls 0.75 (lamp colour 1 / 0.87 / 0.69), sat 1.60, white balance R 1.05 / B 0.92, contrast 1.06, white protect off. Larger ghost sprites (about 120 px) were recommended and not done. |

### Shot 22: "The Storm Expressway was exactly this corridor" (reveal)

| Field | Value |
|---|---|
| Time | clock 52.371-55.475; g1571-1663 (93 frames, 3.10 s) |
| Narration | ทางด่วนพายุ ก็คือช่องนี้แหละ / แล้วที่ปลายเส้นของเขา "The Storm Expressway was exactly this corridor. And at the end of his line," |
| Captions | ทางด่วนพายุ 52.37-53.19 / ก็คือช่อง 53.19-53.63 / นี้แหละ 53.63-54.17 / แล้วที่ปลาย 54.17-54.57 / เส้นของเขา 54.57-55.28 |
| Beat | mechanism and nickname, elements 11 and 6 (the odd idea and the mechanism become one picture); the last phrase starts the disaster (element 10) |
| Set, light | office wall map, office_grey |
| Camera | Classes low, top_down, insert. Arrive g1562-1582: travel north in the lane (u 0.72 to 0.80) while below the wall tops, then rise out (0.33 to 1.5 D), the up vector turning from the wall normal to +z (a tilt, no roll flip); peak 248 px/frame at g1575. Rest on `label_end` g1582-1593 (label 587-621 px wide, centre y 473-489). Crash pull-out g1593-1609 (53.00-53.53, x0.36 by distance) to `whole_map` (about 8 deg of yaw, map frame, sign edge, ledge), small whump shake on landing. Hold 53.70-54.10 as a slow drift (never static). Snap g1626-1642 (54.10-54.63): push x4.3 with a tilt up the line onto `ny_arrow` (arrow head and Long Island); creep decays, near still from g1659. |
| Cast, marks | No characters. |
| Acting (props) | Walls pulse x1.09 in height at g1612 (53.62), then sink to height 0.12 and opacity 0.28 by g1628 (faint outlines); speed sign sinks with them g1613-1621. Lane dashes turn red g1612-1618 and fuse into the centre line g1616-1629; the pale lane fades by g1630, leaving the hand-drawn red line. Label swings on its pin from g1599 (6 deg, decaying). Arrow head trembles from g1612 (1.8 mm jitter of `track_arrow`). Spinner at u 0.65. |
| Props, devices | Label readable at 587-621 px (rest) and 209 px (whole map); N.Y. (English); Long Island shape. |
| Transition | In: dissolve 14 frames. Out: the longest dissolve, 17 frames, matched from the arrow tip on Long Island to the shore (g1656-1672). |
| Sound | Cues: 52.47 the ostinato stops, one held string note; 52.50 the roar falls away, label flutter; 53.37 whump; 53.72 bell-like dong; 53.90 marimba run; 54.20 low drone; 54.47 whoosh, riser to 55.4; 55.10 far gull, surf pre-lap. In the mix: 46 shimmer_reveal 53.720 (peak -14). |
| Heads | none |
| Reference | A13 54.73-59.13 (push down to the rail, 0.47 s hold, crash pull-out x0.27; a/t56.5-t58.5): the moment the hero's odd idea and the mechanism become one picture; B21 second half (b/t59.5-t61.0: back to the object we know, then the long dissolve). Copied: the pull-out reveal with a hold on the key word, then the long dissolve. |
| Take, runner | `v3/film/s22/` (shot.py on `../s20/mc.py`). Rendered g1562-1674. |
| Changed from plan | Final push x4.3 (plan x3) so the arrow head and Long Island fill the frame; the spinner stays in the lower part of the last framing (y about 1040), not below it. Pull-out x0.36 (plan x0.27). Faint outlines = walls at 12 % height and 28 % opacity, not a printed line. |
| Colour row (v1) | 30.0 / 31.4 / 29.6 / 0.9 / 4.1, sat 0.32, val 0.49, dark 0.08: out on sat, dark |
| Reviews | v1: Yes; the idea lands; the walls-on-the-line reveal is small in frame. v1.1: Yes (unchanged). |
| Polish | Grade only (no per-shot setting). |

### Shot 23: the fog bank (beach framing again)

| Field | Value |
|---|---|
| Time | clock 55.475-57.349; g1664-1719 (56 frames, 1.87 s) |
| Narration | คนบนหาดเห็นม่านหมอก ลอยเข้ามา "people on the beach saw a fog bank drifting in." |
| Captions | คนบนหาดเห็น 55.28-55.99 (starts 0.19 s before the cut, inside the dissolve) / ม่านหมอก 55.99-56.57 / ลอยเข้ามา 56.57-57.35 |
| Beat | disaster, element 10 (the warning image) |
| Set, light | beach, storm_approach (`set3d_ext/beach` preset `STORM_APPROACH`: sky #3a3466 to #8e7f98 with one sick yellow band, sea like glass) |
| Camera | Class eye. Starts on THE BEACH FRAMING exactly (`beach_shore_eye`, the start pose of shot 16). Push 1.55 D along the axis, 1 - (1 - x)^2.2 plus 8 % linear creep (man 145 to 197 px, x1.36), turning 4.35 deg toward the sea. 0.2 deg wind shake (two incommensurate sines on yaw and pitch), swelling at 57.0. Speed 0.4-4.8 px/frame; no snap, no streak. |
| Cast, marks | beach_man (`man23`) near at the left third, mark (-1.9, 8.0) (5.5 D from the lens), three-quarter toward the sea (`AC.beach_shade`, mirrored); beach_woman on the porch of cottage_07 at (9.15, 1.05), profile, holding her hat brim (`AC.beach_hold_hat`). |
| Acting | Man shades his eyes from g1674 (55.7); face swaps to stunned (ring eyes) behind a blink at g1713 (57.0). Woman: gust at 57.0. No mouths. |
| Props, devices | Fog: the set's ring (`set_fog_bank`) 0.06 to 0.30 on 'ม่านหมอก' (g1686-1696), then to 1.0 with the ring radius 300 to 165 D (`set_fog_near` 1 to 0.45) from g1702: a pale flat band with a straight top that thickens and comes in. Wind 0.04 to 0.59 from 57.0 (umbrella, grass, towel, vane 35 to 60 deg); LONG ISLAND sign swing 0.02 to 0.08 rad; cottage windows 0.15 to 0.90; rain 0. |
| Transition | In: dissolve 17 frames from shot 22. Out: HARD CUT into shot 24. |
| Sound | Cues: 55.50 surf drops out (dead calm); 55.60 flapping canvas, sign creak; 55.80 cloth swish; 55.90 wind chime; 56.26 low brass and breath swell (fog motif), sub rumble; 56.60 gulls fleeing; 56.80 the band slides in; 57.00 fringe and towel flutter; 57.10 stunned swap. In the mix: 47 riser_tension 55.790-57.35 (-16). |
| Heads | Man 145-197 px, centre x 130-164, y 599-609 (0.47 H); woman 46-53 px. |
| Reference | A14 59.70-62.77 (the wide calm vista before the catastrophe, push 24 %/s easing to 0; a/t59.5-t60.5), entered by A's longest dissolve (17 frames); same framing as our shot 16; B18 (b/t46.0-t47.0). Copied: the calm vista push easing to 0, the longest dissolve into it, the framing callback. |
| Take, runner | `v3/film/s23/` (shot.py on `set3d_ext/beach/bshot.py`, version 2). Rendered g1653-1719. |
| Changed from plan | The man's mark moved from y 7.45 to 8.0 and the push turns 4.35 deg seaward, so the fog band shows right of his head instead of behind it. |
| Colour row (v1) | 21.9 / 7.7 / 3.9 / 55.3 / 11.2, sat 0.30, val 0.49, dark 0.01: seven of eight out (violet sky, by design) |
| Reviews | v1: Partly; the framing callback works, but the sky is flat purple with no glow, and the fog bank is barely visible (beat 18 not readable). v1.1: Partly; a pale band now covers the yellow horizon glow, but it is a 40-60 px strip, easy to miss on a phone; the sky is still flat violet. |
| Polish | Grade: haze 0.10 at 0.44 H, plus a 2D fog bank: #c9bfd0 band on the horizon (y 600 to 612), growing 40 to 120 px tall over g1677-1719 with a smoothstep, fading in over g1671-1681, peak alpha 0.80, slow x-modulation +-16 %, behind near objects by a colour matte. Better next time: make the fog a tall wall in the render that fills a third of the frame by 57.3 s. |

### Shot 24: the wall of water (hard cut, low)

| Field | Value |
|---|---|
| Time | clock 57.349-59.607; g1720-1787 (68 frames, 2.27 s) |
| Narration | มันคือกำแพงน้ำ สูงกว่าบ้านทั้งหลัง "It was a wall of water, taller than a whole house." |
| Captions | มันคือ 57.35-57.56 / กำแพงน้ำ 57.56-58.40 / สูงกว่า 58.40-58.76 / บ้านทั้งหลัง 58.76-59.61 |
| Beat | disaster, element 10 (the one physical image) |
| Set, light | beach, storm (= `STORM`); puppets tinted #b5b5f0 (0.71, 0.71, 0.94) |
| Camera | Class low. HARD CUT onto the two shocked faces (`beach_low_wave` axis: the beach framing's -3.9 deg axis turned to azimuth 12 deg, toward the sea), man's head about 290 px. Crash pull-out `PULL` g1730-1748 (57.55-58.15) with a tilt up that keeps going as a drift; lens down to 0.70 D, pitch to +30 deg by g1775 (`HIGHER`, 'บ้านทั้งหลัง'). 5 Hz shake from g1752 (58.3). Streaked plate frames g1764, g1776. |
| Cast, marks | beach_man `man24` at (1.0, 9.0), beach_woman `woman24` at (2.3, 10.75), near-profile toward the sea, three-quarter to the lens. |
| Acting | Shocked swap behind a blink at 57.42 (`AC.beach_shocked`: ring eyes, sweat, focus lines); his boater pops off and a flying boater card takes over at g1729 (`set_boater`). Jump at 57.73 (squash 2, leap 2, hang 2, land 2 frames), then run to screen right at 6.2 D/s (the walk at double rate): man out by g1764, woman by about g1770. No mouths. |
| Props, devices | The set's wave (`set_wave`, STORM colours) fills the left 60 % with the crest at the top; one cottage with lit windows under the curl: `cottage_s24`, a copy of cottage_06 stood seaward at (19.2, 9.4), porch turned 90 deg to the lens. Conform overlays: dark-ink focus lines round the two faces g1720-1722 (opacity 0.85, 0.70, 0.45); 40 white speed lines g1730-1748. |
| Transition | In: HARD CUT, 3 frames before 'มันคือ'. Out: object wipe, 6 frames: a 2D lilac-white scalloped foam sheet crosses the lens left to right, full cover on g1787-1788 (g1785-1790). |
| Sound | Cues: 57.35 orchestra hit, then 6 frames of near silence; 57.50 two gasps; 57.60 hat pop; 57.70 crash whoosh out, roar swells; 57.83 jump; 58.10 running steps on sand; 58.40 ground rumble, timbers, wires; 58.90 shutters bang x3, buoy bell; 59.55 wave crash carried over the wipe. In the mix: 48 thump_jab 57.350 (in place of the orchestra hit, -11.1); 49 wave_roar 58.100-61.20 (-12). |
| Heads | Man about 290 px at the cut; heads about 60 px in the wide; the runners' heads at y 830-900 on about g1752-1770 (just under the 880 limit). |
| Reference | A13 a/t54.5-t58.5 (wide ring eyes, then crash pull-out x0.27), A12's popped hat (a/t54.0), A15 63.23-64.33 (the camera tilting with the fall); B18 (b/t46.5-t48.0: the column that fills the frame). Copied: the hard cut onto shocked faces, the crash pull-out that reveals the scale, the popped hat, the tilt up. |
| Take, runner | `v3/film/s24/` (shot.py on `set3d_ext/beach/bshot.py`). Rendered g1720-1792 (handle out 5). |
| Changed from plan | No wave shadow sweeps the roof (the STORM key comes from the land side). No foam crest over the lens in the take: the conform adds the foam-sheet wipe. The rowing boat and the LONG ISLAND board are hidden. The wave keeps the set's STORM colours, not the plan's plum and blue. `s24/shot.py` no longer matches the render's camera on g1721-1747 by up to 0.4 D; the depth pass used the camera saved in `raw/meta`. |
| Colour row (v1) | 8.9 / 0.3 / 83.1 / 1.8 / 4.0, sat 0.45, val 0.45, dark 0.01: night wave, outside the interior band by design |
| Reviews | v1: Yes; the night-blue drama matches clip B's night; little scale cue until 58.5 s; the faces are tinted lavender. v1.1: Yes (almost unchanged; the crest a little brighter). |
| Polish | Grade: bloom 0.8. |

### Shot 25: the storm takes the expressway into New York (G in the storm)

| Field | Value |
|---|---|
| Time | clock 59.607-62.442; g1788-1872 (85 frames, 2.83 s) |
| Narration | เฮอริเคนลูกนั้นขึ้นทางด่วนพายุ ตรงเข้านิวยอร์ก "That hurricane took the Storm Expressway, straight into New York." |
| Captions | เฮอริเคน 59.61-59.98 / ลูกนั้นขึ้น 59.98-60.73 / ทางด่วนพายุ 60.73-61.58 / ตรงเข้า 61.58-61.93 / นิวยอร์ก 61.93-62.44 |
| Beat | ending, elements 10, 12 and 6 (the nickname comes true; the line of shot 1 is fulfilled) |
| Set, light | office, office_storm (`set3d_ext/light`: office_grey with the key much lower, dark window card with lashing rain, lamps on; lightning = the key sun pulsed on g1872) |
| Camera | Class insert, then eye. Raking insert (insert_rake family): lens 1.3 D from its target, from below-left, 22 mm, creeping in 3 %/s; the target leads the spinner by u 0.16 and rises to the label by g1829 (tilt-up follow, move g1802-1826, peak 70 px/frame); the label reads g1819-1838 at 560-620 px. Snap g1838-1852 (61.15-61.62; move g1839-1850, peak 204) pulls back into G (22 mm creeping to about 23.6 mm). Impact g1862 (61.98); 5 Hz shake for 8 frames. |
| Cast, marks | Chief `boss25` at `boss_mark` (far, pointer in hand); hero `hero25` at `gloat_near` (near). |
| Acting | Spinner flat out: motion-blurred disc, 22 deg per frame and accelerating, u 0.02 to 0.52 in the insert and 0.52 to 1.0 in G, ignoring the chalk curve, hits the arrow head at g1862 with a squash. Chief: `acting.boss_shocked` (smug to shocked behind a 3-frame blink, closed frame g1863: ring eyes, sweat, mouth shut); the pointer leaves his hand at g1869. Hero: `acting.hero_stunned` (`expr='sad'`; swap g1863, eyes shut and head lowered 0.1 D from g1867); no triumph. No mouths. |
| Props, devices | Label flutters 0.35-0.75 in the storm draught and whips 16 deg on its pin at the impact. Ink blot: a lit map decal (`s25/tex/ink_blot.png` from `make_blot.py`), centred just east of the N.Y. dot over Long Island, grows to 0.5 D in 5 frames from g1862. Calendar leaf 21. Window dark with lashing rain. |
| Transition | In: object wipe 6 frames (the foam sheet clears to the map; handle in 5). Out: white flash, 5 frames to white on g1868-1872 (lerp 0.15, 0.35, 0.60, 0.85, 1.00) and 4 out on g1873-1876 (0.85, 0.55, 0.30, 0.12). |
| Sound | Cues: 59.55 water rush across the stereo field into a muffled roar; 59.55 rain lashing (bed); 59.71 whistled tune slowed, in minor; 59.80 paper-tear zip, train-like; 60.10 thunder crack; 61.00 label flap; 61.25 whoosh out; 62.08 impact boom, ink splat, window rattle; 62.30 pointer clatter; 62.40 thunder with the white flash. In the mix: 25 rain_drizzle 59.550-62.55 (RMS -41.6 in v1, -34 in v1.1); 50 thunder_low 60.100 (-16); 51 thump_jab 62.080 (impact, -12). |
| Heads | In G: chief 180-245 px, hero 255-350 px, both above y 880 (ratio 1.42). |
| Reference | A15 63.23-64.33 (the camera tilting with the train at 521 px/s into the white flash f1930-1934) and A16 (pull back x0.37 to the onlookers, a/t64.5), on the gloat framing of A11; a/t03.5 (a large object wipes the lens). Copied: the tilt-up follow of the moving threat, the pull-back to the two men, the white flash. |
| Take, runner | `v3/film/s25/` (shot.py on `../s17/otake.py`). Rendered g1783-1872. |
| Changed from plan | Snap lands on G, not G' (G' crops the near hero to a third of his head, and his stunned face must read). Plan's 520 px/s insert tilt and the wake streak overlay: the wake was left out in the conform (the spinner carries its motion-blur disc). A first version lit every frame by the lightning (no zero key before it); fixed before the final render. |
| Colour row (v1) | 29.9 / 15.3 / 45.0 / 1.8 / 5.0, sat 0.34, val 0.33, dark 0.33: six of eight out (the darkest stretch). v1.1: 28.4 / 15.9 / 43.7 / 2.7 / 6.4, sat 0.33, val 0.49, dark 0.08. |
| Reviews | v1: Partly; a third of the pixels below V 0.25, so the climax plays in murk and the two men barely react. v1.1: Partly; readable now (val 0.49, dark 8 %), the map run reads; the men still barely react. |
| Polish | Grade: lift 0.06, gamma 0.88, gain 1.04, sat 1.40. Better next time: give the two men a real reaction beat on the impact. |

### Shot 26: the forecast on the kitchen table still says rain (last image)

| Field | Value |
|---|---|
| Time | clock 62.442-65.400; g1873-1964 (92 frames, 3.07 s) |
| Narration | ส่วนคำพยากรณ์บนโต๊ะกินข้าว ยังเขียนว่า ฝนตก "And the forecast on the kitchen table still said: rain." |
| Captions | ส่วนคำพยากรณ์ 62.44-63.23 / บนโต๊ะกินข้าว 63.23-64.11 / ยังเขียนว่า 64.11-64.82 / ฝนตก 64.82-65.40 |
| Beat | ending, element 12 (end on the image and the last line) |
| Set, light | kitchen, kitchen_storm (ambient (0.050, 0.072, 0.20) falling 1.2 x y / 9; warm key sun (0.28, 0.20, 0.125), angle 2 deg; lightning = a second sun through the window at pi x 3.2 x strength with the window card x1.6; window wave sequence, 92 frames, emission 0.85; grade saturation 1.15) |
| Camera | Class eye. g1873-1900 `window_tight` (1.05 D from the window): the four panes fill the frame, drift in 2 %/s under a 5 Hz shake, 20-35 px/frame. Snap g1901-1917 (63.28-63.82, 16 frames): pull back to THE TABLE FRAMING (`table`, 2.42 D, x0.43) with the tilt trailing, peak 223 px/frame, streaked whole g1905-1914 (no actors). Settle g1918-1928 (0.6 %/s creep while the shake decays). Push g1929-1953: 15 % of the way to the weather-box centre, about 26 %/s easing to 0 at 65.0, tilt down 0.05 D so the words rise clear of y 600. Hold g1953-1964 (12 frames, static from g1954: the planned final hold). |
| Cast, marks | No characters, no hands. |
| Acting (props) | Chair shoved back (off the right edge; sound only), cup rattling g1876-1908. Lightning strengths: g1873-1876 1.0, 0.75, 0.45, 0.2; g1889-1894 0.35, 1.0, 0.8, 0.25, 0.6, 0.15; g1935-1936 0.7, 0.3. Rings race across the coffee (ring texture 0.9 rad per frame, amplitude 0.85, easing to 0.25 after the shake): the ripple that shot 15 did not have. Cup and saucer creep 0.05 D right and 0.17 D toward the lens in jerks (hops up to 0.01 D, +-3 deg). Paper flutter 0.006 D, 0.036 D from 63.9 to 64.6. Lower-right pane cracks at g1923 (grows over 4 frames). A small light-blue drop falls g1948-1951 and lands on ฝนตก at g1952 (64.95); bleed frames `newspaper_bleed` f_00-f_11 over g1952-1963, f_11 held on g1964. |
| Props, devices | Newspaper weather box: header top y 247, Thai bottom y 573 at the last frame, ฝนตก 99.5 px tall (x-height about 71 px), centred at x 360; cup at lower right; dark water and rain in the panes. |
| Transition | In: white flash (5 frames in at the end of shot 25, 4 out over g1873-1876, s26's own lightning key decays under it). Out: end of film; music fades 65.1-65.5 s on the drip. |
| Sound | Cues: 62.44 flash hiss with ringing tail; 62.55 muffled roar, timbers groan (bed); 62.55 chair shove; 62.60 cup rattling; 63.00 thunder crack; 63.38 whoosh; 64.00 newspaper flutter; 64.10 pane cracks; 65.05 single plip and one soft piano note; 65.10 everything cuts to silence. In the mix: 26 wave_roar 62.550-64.40 (RMS -32.6); 52 paper_slide 64.000 (RMS -28). |
| Heads | none |
| Reference | A16 64.50-65.20 (pull back x0.37 from the catastrophe to what is left in the foreground; end) and a/t32.0 (printed-word insert); B22 (pull-back easing to 0, last 0.4 s still); same framing as shot 15, as A11 answers A5; the cup of B8, now with its ripple. Copied: the pull-back from the catastrophe to a foreground object, the last 0.4 s still, the callback framing. |
| Take, runner | `v3/film/s26/` (shot.py on `set3d_kitchen/kshot.py`). 8 samples. The last frame g1964 was rendered and approved as a still before animating. |
| Changed from plan | Pull-back x0.43, not x0.37 (the table framing is the fixed end point shared with shot 15). Masthead not in frame (the page is folded, as in shot 15); calendar leaf 21 falls just outside the pushed-in framing. The chair is off the right edge. The wall of water is the window's exterior texture sequence: it reads as heavy water against the window more than as one towering curl. |
| Colour row (v1) | 45.2 / 19.4 / 25.2 / 0.4 / 6.2, sat 0.49, val 0.36, dark 0.22: out on red, orange, sat, val, dark (storm by design). v1.1: dark 0.40. |
| Reviews | v1: Yes; the ending lands; the "dark wall of water" in the panes reads as white puffy clouds and rain, not water. v1.1: Yes; dark share rose to 40 %; the water in the panes still reads as clouds. |
| Polish | Grade only (no per-shot setting). |

---

## 3. Summary tables

### 3.1 The edit against the references

Shot lengths (s), our film (measured, `deliver/QA_film.md` 1.3): 1.30 1.13 1.87 2.33 2.40 2.17 2.17 3.47 3.50 2.80 3.27 1.57 0.97 2.93 1.90 2.43 1.23 2.20 7.67 3.23 1.83 3.10 1.87 2.27 2.83 3.07.

| # | Length (s) | Transition in (frames) | In-shot snaps | Framing changes in the shot (transition + snaps) | Camera classes in order |
|---|---|---|---|---|---|
| 1 | 1.30 | start | 1 | 1 | insert |
| 2 | 1.13 | in-take reframe (14) | 1 | 2 | low |
| 3 | 1.87 | whip (cut in the streak) | 1 | 2 | high |
| 4 | 2.33 | dissolve 12 | 1 | 2 | high, insert |
| 5 | 2.40 | cut hidden in whip-tilt | 0 | 1 | insert |
| 6 | 2.17 | dissolve 13 | 0 | 1 | low |
| 7 | 2.17 | dissolve 10 | 1 | 2 | insert |
| 8 | 3.47 | dissolve 15 | 1 | 2 | high, eye |
| 9 | 3.50 | dissolve 13 | 2 | 3 | high, insert, low |
| 10 | 2.80 | dissolve 9 | 1 | 2 | low, eye |
| 11 | 3.27 | dissolve 9 | 2 | 3 | insert, low, high |
| 12 | 1.57 | dissolve 11 | 0 | 1 | eye |
| 13 | 0.97 | punch-in + speed lines | 0 | 1 | insert |
| 14 | 2.93 | dissolve 11 | 1 | 2 | eye, insert |
| 15 | 1.90 | match dissolve 13 | 1 | 2 | top_down, eye |
| 16 | 2.43 | dissolve 13 | 1 | 2 | eye |
| 17 | 1.23 | dissolve 14 | 0 | 1 | low |
| 18 | 2.20 | hard cut | 2 | 3 | eye |
| 19 | 7.67 | match dissolve 12 (in the crash push) | 4 | 5 | insert, high, low, top_down |
| 20 | 3.23 | dissolve 9 | 1 | 2 | low |
| 21 | 1.83 | dissolve 10 (whip pull-out) | 0 | 1 | high |
| 22 | 3.10 | dissolve 14 | 2 | 3 | low, top_down, insert |
| 23 | 1.87 | dissolve 17 | 0 | 1 | eye |
| 24 | 2.27 | hard cut | 1 | 2 | low |
| 25 | 2.83 | object wipe 6 | 1 | 2 | insert, eye |
| 26 | 3.07 | white flash 5 + 4 | 1 | 2 | eye |

| Measure | Film 1 | Clip A | Clip B | Better value next time |
|---|---|---|---|---|
| Shots / takes | 26 / 25 | 16 | 22 | 18-22 |
| Shot length mean / median / range | 2.52 / 2.30 / 0.97-7.67 s | 3.75 / 3.65 / 0.70-7.73 | 2.62 / 2.45 / 0.40-6.53 | mean 2.8-3.2 s |
| Dissolves | 17 of 24 real transitions (71 %), 9-17 frames, median 12 | 73 %, median 13 | 86 %, median 10.5 | 75-85 %, median 11-13 |
| Hard cuts | 2 (into 18, into 24) | 1 | 1 | 1-2, only into a reversal |
| Special transitions | 7 (whip, hidden cut, punch-in, wipe, flash, in-take reframe, match dissolves) | 4 | 3 | 3-4 |
| In-shot snaps | 26; new ones 13-25 frames, median 15; 22.9 % of the time | 36, median 24.5; 44 % | 22, median 13.5; 17 % | 18-24, median 14-18 |
| Framing changes | 51 (25 transitions + 26 snaps) = 0.78 per s | | | about 0.70 per s |
| Interval, plan count (mean / median) | 1.26 / 1.21 s (1.28 = 65.5 / 51) | 1.25 / 1.19 | 1.54 / 1.26 | 1.35-1.45 |
| Interval, picture tool (score.py) | 1.06 s (v1), 1.09 s (v1.1) | 1.39 | 1.62 | 1.3-1.4 |
| Static frames / longest hold | 3.2 % / 12 frames | 3.8 % / 14 | 5.5 % / 12 | as film 1 |
| Holds | 4 planned (8, 12, 6, 12 frames) | 4, 1.30 s | 3, 1.03 s | as film 1 |
| Zoom median / pan median | 11.4 %/s / 39 px/s | 20.7 / 142 | 9.9 / 57 | pans 60-140 px/s (pan is the one move under range) |
| Snap peak/mean | 1.69 | 1.87 | 1.66 | 1.7-1.9 |
| Flat-2D share of 0.5 s pairs (parallax) | 31.5 % | 11 % | 43 % | under 30 %; avoid card-like wides (shots 4, 12) |

Shot-length mean and median and the transition shares above are recomputed by the recipe in section 5 (tested). The intervals, holds and zoom/pan come from `plan/shot_plan.md` and `deliver/QA_film.md`.

### 3.2 Callbacks: what is planted and where it returns

| Callback | Planted | Returns | How it repeats | Review verdict |
|---|---|---|---|---|
| G, THE GLOAT FRAMING (chief far at `boss_mark`, hero near at `gloat_near`, camera (1.55, -4.95, 2.85) to (1.25, -0.40, 2.62), 22 mm) | 10 (day, he mocks) | 18 (grey, he mocks again and taps the label; G' at 30.36 mm), 25 (storm, the spinner hits N.Y. between them) | same camera and marks; the light changes day, grey, storm; the marks grow from the hook's two-shot (3) | Lands (v1): same axis and marks, light changes day to grey to storm |
| The erase gag | 3 (hook: the chief rubs the line out) | 11 (rubbed and redrawn twice, stepped pull-out), 12 (smudge halo and crumbs stay) | the eraser, the pink smudge, the redrawn line | not reviewed separately |
| The red line and its arrow at N.Y. | 1-2 (drawn), 3 (erased) | 9 (drawn again), 10-11, 19-22 (the corridor lies on it), 25 (the storm rides it) | the same hand-drawn track `S.track_point(u)` in every shot | the idea lands in 22 (v1) |
| The storm spinner | 5 (pinned off FLA.) | 6, 7, 9-11, 19-22, 25 | phase of its turn continued from shot to shot (5, 6, 7) | readable throughout |
| The chalk curve and old tracks | 7 (the old hands' forecast) | 9 (his line passes the bend), 19 (crumbles under the east wall), 21 (ghost tracks brightened, ghost storms), 25 (the storm ignores it) | the same geometry, crumble state, brightness controls | ghosts illegible in 21 |
| The label ทางด่วนพายุ | 13 (slapped on) | 17 (not featured), 18 (tapped), 19-22 (far, then read at 430 px+), 25 (flutters, read 19 frames in the insert) | same `label_rect` and pin in every shot | Lands (v1): readable in all three featured shots |
| The corridor view (worm's eye up the line) | 9c (props `corridor_cam`, 0.40 D) | 19 (2), 20, 22 (arrival) (mech `corridor_cam`, 0.345-0.35 D) | the same view up the line, with walls added | 9c reads as abstract (v1) |
| The forecast words ฝนตก ลมกระโชก | 14 (teletype sheet, stamp ทางการ) | 15 (newspaper weather box, same words and size), 26 (same box, the drop lands on ฝนตก) | one artwork in three places; 14 ends with the lines within 20 px of where 15 starts | Lands strongly (v1) |
| THE BEACH FRAMING (`beach_shore_eye`, loc (-7.4, 7.0, 2.6)) | 16 (grey drizzle, the false defeat) | 23 (fog bank), and its axis in 24 (`beach_low_wave`, turned 15 deg seaward) | same start pose; the light changes drizzle, violet, storm | Lands in part (v1): the man moves from centre to the left third and the camera sits a little lower, so the match is felt rather than seen |
| THE TABLE FRAMING (`table`) | 15 (still cup, no ripple) | 26 (ripples, the drop, the last frame) | same camera; the cup that did not ripple now ripples | Lands (v1) |
| Calendar leaf | 4 (SEPTEMBER 20 TUESDAY 1938) | 17, 18, 25 and the kitchen (leaf 21) | the date moves on one day | not reviewed separately |
| Quote staging: mouth moves only in the two quotes, held wink at the end | 10 | 18 | `acting.loudness` drives the mouth; `boss_lean_wink` | Lands |
| Music motifs (intent) | tuba 6, whistled theme 17 | tuba answers 10, mocking tuba 18, whistled tune slowed in minor 25 | cue lists only; the mix carries one music bed | not established |

### 3.3 Ranking: most to least like the reference

The verdict class (Yes / Partly / No) is the reviews'. The order inside a class is inferred from the reviews' wording and measurements.

| Rank | Shot | Verdict v1.1 (v1) | Why | Use next time |
|---|---|---|---|---|
| 1 | 3 | Yes (Yes) | "the best match to the reference": two-shot in depth, near/far 1.40-1.47, whip in, snap onto the shocked face | Imitate first. |
| 2 | 17 | Yes (Yes) | closest office frame to clip B's look: low lens, lamp-lit | Imitate. Make it longer than 1.2 s. |
| 3 | 10 | Yes (Yes) | low boss, pull-back pan into the two-shot in depth, zoom push keeping the ratio | Imitate; aim the low angle at something bright, not a dark ceiling. |
| 4 | 2 | Yes (Yes) | low medium with the lamp in frame, snap on the action word | Imitate. |
| 5 | 8 | Yes (Yes) | most reference-like exterior: vista, crash push x3 onto the sleeper | Imitate; keep the face clear of the umbrella at the end; add sun bloom. |
| 6 | 13 | Yes (Yes) | punch-in with speed lines, label reads in under a second | Imitate for every named prop. |
| 7 | 26 | Yes (Yes) | ending lands: pull-back to the paper, still last frames, callback framing | Imitate; make the water read as water. |
| 8 | 24 | Yes (Yes) | night drama matches clip B; hard cut, crash pull-out, scale | Imitate; give a scale cue earlier and keep faces untinted. |
| 9 | 18 | Yes (Yes) | the callback reads | Open on a real grin close-up. |
| 10 | 11 | Yes (Yes) | stepped pull-out, purple face | Imitate the step structure; light the insert. |
| 11 | 6 | Yes (Yes) | B-like low row of authorities, glowing globes | Imitate. |
| 12 | 14 | Yes (Yes) | crash push onto the verdict, words fill the frame | Imitate; keep picture text off the caption band. |
| 13 | 1 | Yes (Yes) | odd act in close-up, moving on frame 0 | Imitate. |
| 14 | 9 | Yes (Yes) | small hero between big men; crash push into the line | Imitate (a); avoid the abstract corridor macro (c). |
| 15 | 22 | Yes (Yes) | the idea lands; reveal small in frame | Make the walls-on-the-line reveal larger. |
| 16 | 12 | Yes (Yes) | B9 staging and moves; crowded frame, heads cut at the edges (the v1 verdict stands for the delivered film) | Keep the reacting faces in frame; avoid crowding the frame edge. |
| 17 | 25 | Partly (Partly) | tilt-follow and flash read; the men barely react | Give the reaction a beat. |
| 18 | 4 | Partly (Partly) | the calendar insert is clean; the wide is dark and cluttered, card-like | Avoid dark cluttered wides with small heads. |
| 19 | 23 | Partly (Partly) | framing callback works; the fog is a thin strip, the sky flat violet | Make the fog a big wall in the render. |
| 20 | 15 | Partly (Partly) | the pull-out works; the frame is all warm (blue 6-7 %) | Add a cool light or object in every interior. |
| 21 | 5 | Partly (Partly) | fly-in lands on the named thing; a full smear, flat diagram | Keep the fly-in shorter than 20 frames, and the landing object sharp. |
| 22 | 7 | Partly (Partly) | evidence pattern shown on the map; reads as an infographic | Avoid holding a flat chart; show the old hands' faces with it. |
| 23 | 19 | Partly (Partly) | one long take naming the parts; still a cold diagram | Avoid pale untextured diagram props; light them warm in the render. |
| 24 | 20 | Partly (Partly) | the launch reads; a graphic road-sign world | Same as 19. |
| 25 | 21 | Partly (No) | the comparison is illegible at phone size | Avoid comparison props under about 120 px. |
| 26 | 16 | No (No) | washed out, the tilt holds on empty sky with half a face | Never hold on an empty sky; keep a face or the acting hand in frame. |

Patterns to imitate first: two-shots in depth (3, 10, 18, 25), low single on the authority (2, 6, 10, 17), crash push onto a printed or physical object on its word (8, 13, 14), the pull-back to the result at the end of a beat (11, 22, 26), hard cut onto a face before the reversal (18, 24).

Patterns to avoid: map or diagram views that run cold and flat (5, 7, 19-21: 22 % of the film); small grey props carrying a beat (21); empty sky (16); dark, cluttered wides with small heads (4); full-frame smears longer than half a second (5); picture text in the caption band (14, g902-925); faces passing through the caption band (16, g1068-1078).

---

## 4. Polish passes that touched every shot (v1.1)

| Pass | What it did | Shots |
|---|---|---|
| Grade (`v3/film/out_v11/grade.py`, `grade_frame(img, g)`) | per-shot correction cross-faded over every dissolve, one S-curve, saturation 1.18, exterior haze, bloom of hot sources, s23 fog bank, red protect, white protect, soft ceiling | all; per-shot settings on 8, 15, 16, 19, 20, 21, 23, 24, 25 (entries above) |
| Fix round after the v1.1 review (`v3/film/out_v11/grade.py`) | grade: no glow inside near-white fills, only pale sources are hot (shot 11 ghost face) | 11 |
| Sound v1.1 (`v3/film/out_v11/mix_film.json`) | voice gain 1.512 to 1.347 (about -1 dB); rain_drizzle beds -41.5 to -34 RMS; thump at 48.1 s -13 to -15 peak | 14-16, 20, 25 |

Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.

The delivered film is `deliver/film_v1_1_sharp_thai.mp4`: the v1 conform frames (`v3/film/out/frames/`, sharp) through the v1.1 grade (fix round included), the v1 captions (`v3/film/out/film_silent.ass`) burned last, and the v1.1 mix (`v3/film/out_v11/make_sharp.py`). Measured effect of the grade (measured by GRADE.md on 448 sharp v1 conform frames graded by the pre-fix-round grade.py; the fix round (no glow in near-white fills) was not re-measured there): contrast (luma p95-p5) 0.497 to 0.623, V > 0.95 share 0.012 to 0.036, top-third mean luma 83.7 to 93.3, middle-third 104.4 to 118.2, saturation 0.392 to 0.410, head fill V 1.000 to 0.984. The delivered film itself, score.py whole film with captions (re-measured for this chapter): index 0.993, contrast 0.621, V > 0.95 0.032, top third 92, middle third 117, saturation 0.417, head fill V 0.980. The edit rows (pan median, framing interval) and the caption height (45 px against 36-37) were not changed.

---

## 5. Recipes

### 5.1 The film 1 edit as data (tested)

Paste and run with `python3 -I edit.py`. It holds every shot's frames, transition and snap count, reproduces the edit numbers of section 3.1, and gives the two clock rules the takes use.

```python
# Film 1 edit as data: (shot, first film frame g0, end frame g1 exclusive, transition in, its frames, in-shot snaps)
import statistics as st
FPS = 30
EDIT = [
 (1, 0, 39, 'start', 0, 1), (2, 39, 73, 'in_take', 0, 1), (3, 73, 129, 'whip', 0, 1),
 (4, 129, 199, 'dissolve', 12, 1), (5, 199, 271, 'hidden_cut', 0, 0), (6, 271, 336, 'dissolve', 13, 0),
 (7, 336, 401, 'dissolve', 10, 1), (8, 401, 505, 'dissolve', 15, 1), (9, 505, 610, 'dissolve', 13, 2),
 (10, 610, 694, 'dissolve', 9, 1), (11, 694, 792, 'dissolve', 9, 2), (12, 792, 839, 'dissolve', 11, 0),
 (13, 839, 868, 'punch_in', 0, 0), (14, 868, 956, 'dissolve', 11, 1), (15, 956, 1013, 'dissolve', 13, 1),
 (16, 1013, 1086, 'dissolve', 13, 1), (17, 1086, 1123, 'dissolve', 14, 0), (18, 1123, 1189, 'hard_cut', 0, 2),
 (19, 1189, 1419, 'dissolve', 12, 4), (20, 1419, 1516, 'dissolve', 9, 1), (21, 1516, 1571, 'dissolve', 10, 0),
 (22, 1571, 1664, 'dissolve', 14, 2), (23, 1664, 1720, 'dissolve', 17, 0), (24, 1720, 1788, 'hard_cut', 0, 1),
 (25, 1788, 1873, 'wipe', 6, 1), (26, 1873, 1965, 'flash', 9, 1)]

def gf(clock):            # an in-shot event at narration-clock x lands on film frame round((x + 0.1) * 30)
    return int(round((clock + 0.1) * FPS))

def dissolve_frames(gb, L):   # conform rule: mixed frames and the incoming weight (smoothstep)
    a = gb - L // 2
    ss = lambda x: x * x * (3 - 2 * x)
    return [(g, round(ss((g - a + 1) / (L + 1)), 3)) for g in range(a, a + L)]

lens = [(g1 - g0) / FPS for _, g0, g1, *_ in EDIT]
trans = [t for _, _, _, t, _, _ in EDIT[1:]]
diss = [f for _, _, _, t, f, _ in EDIT if t == 'dissolve']
snaps = sum(s for *_, s in EDIT)
changes = len(trans) + snaps
print('shots %d, length mean %.2f s, median %.2f s, range %.2f-%.2f s' % (len(lens), st.mean(lens), st.median(lens), min(lens), max(lens)))
print('dissolves %d of %d real transitions (%.0f %%), %d-%d frames, median %g' % (len(diss), len(trans) - 1, 100 * len(diss) / (len(trans) - 1), min(diss), max(diss), st.median(diss)))
print('framing changes %d = %d transitions + %d snaps; %.2f per second; mean interval %.2f s' % (changes, len(trans), snaps, changes / 65.5, 65.5 / changes))
print('s05 pin at clock 7.15 -> g', gf(7.15), '| join 1 (gb 129, L 12):', dissolve_frames(129, 12)[0], '...', dissolve_frames(129, 12)[-1])
```

Output (run in this session):

```
shots 26, length mean 2.52 s, median 2.30 s, range 0.97-7.67 s
dissolves 17 of 24 real transitions (71 %), 9-17 frames, median 12
framing changes 51 = 25 transitions + 26 snaps; 0.78 per second; mean interval 1.28 s
s05 pin at clock 7.15 -> g 218 | join 1 (gb 129, L 12): (123, 0.017) ... (134, 0.983)
```

g218 is the pin frame in `s05/QA.md`, and g123-134 are the frames the conform mixed for join 1 (`CONFORM.md`). "Real transitions" leaves out the in-take reframe. The mean interval here is film length / changes; the plan's 1.26 s is measured between change times.

### 5.2 Read the bundled takes' edit data (tested)

Run from the skill's `pipeline/` folder. Nine of the 23 takes are bundled (s10, s11, s13, s14, s17, s19, s20, s24, s26).

```bash
python3 -I -c "
import json, glob
for f in sorted(glob.glob('v3/film/s*/meta.json')):
    m = json.load(open(f))
    print(m['take'], m['g0'], m['g1'], m['set'], m['light'], m['transition_in']['type'], m['transition_in']['frames'], 'handles', m['handle_in'], m['handle_out'])
"
```

First lines of the output: `s10 610 694 office office_day dissolve 9 handles 7 7` and `s11 694 792 office office_day dissolve 9 handles 7 8`. A take renders g0 - handle_in to g1 - 1 + handle_out; a dissolve of L frames needs ceil(L / 2) + 2 frames of handle on each side (`s16/QA.md`: 13-frame dissolve, handle 9).

### 5.3 Write the next film's shot entries this way

For each shot of a new plan, fill the same rows as section 2 before rendering: time and frames; the phrases it carries; the beat and formula element; the set and light preset; start framing by name, class, every move with frames and speed, end framing; marks and the acting library function for each actor with beat frames from `gf()`; props and set controls (`set_*`) with their frames; transition in and out with lengths and handles; the cue list in film seconds; the head-width target; the reference shot and what is copied. The take's `meta.json`, `cues.json` and `QA.md` then record what was built against it (see the bundled `v3/film/s10/` for the full set).

---

## Sources

Paths relative to `__PROJ__` (the project) unless marked `pipeline/` (the skill's bundled copy).

- `plan/shot_plan.md`, `plan/shot_plan.json` (shots, times, captions per shot, snaps, camera class segments, transitions, grammar numbers, notes).
- `script_th_v2/script_en_gloss.txt`, `script_th_v2/script_th_tts.txt` (narration and gloss); `audio/th/full_v2/narration_timing.json` (delivered phrase times).
- `v3/shots/film.py`, `v3/shots/timing.py`, `v3/out/QA.md`, `v3/out/COLOUR.md` (the opening, shots 1-3); `v3/set3d/office3d.py` (TRACK_STYLE).
- Takes `v3/film/s04/` to `v3/film/s26/`: `shot.py`, `QA.md`, `meta.json`, `cues.json`; runners `s04/otake.py`, `s10/otake.py`, `s17/otake.py`, `s20/mc.py`, `set3d_ext/beach/bshot.py` (imported by s08, s16, s23, s24), `set3d_kitchen/kshot.py` (s15, s26).
- `v3/film/out/CONFORM.md`, `v3/film/out/SOUND.md`, `v3/film/out/mix_film.json`.
- `v3/film/out_v11/GRADE.md`, `v3/film/out_v11/grade.py`, `v3/film/out_v11/mix_film.json`, `v3/film/out_v11/make_sharp.py`; `deliver/film_v1_1_sharp_thai.mp4` (the film of record).
- `deliver/QA_film.md`, `deliver/QA_film_v1_1.md` (reviews).
- `pipeline/v3/film/s*/meta.json` (recipe 5.2); `references/story-formula.md`; `references/bible/camera.md` section 2.2 (camera name to coordinates, cross-checked).
- Pictures: `v3/film/out_v11/graded/g_%04d.png` at g20, 64, 100, 178, 250, 322, 395, 495, 520, 675, 760, 815, 858, 940, 1005, 1077, 1112, 1150, 1300, 1500, 1545, 1615, 1712, 1772, 1862, 1964.
