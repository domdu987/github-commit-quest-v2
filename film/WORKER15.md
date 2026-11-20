# Render-team worker brief, film 15 (ไอ้ปลาดิ้น — Dick Fosbury's backward high jump, 1963 -> Mexico City 1968)

Follow film/WORKER.md exactly for section 1 (setup: the PROJ symlink to the repo's film/), section 4 (delivery) and section 5 (rules). The film-15 differences are below. Your branch was checked out from film15/main; push to YOUR outcome branch only.

## Inputs
- **Brief and shots:** PROJ/film15/BRIEF.md, PROJ/film15/shot_plan.md (36 shots), PROJ/film15/FACTS.md (picture limits).
- **Narration:** PROJ/film15/audio/narration.wav (69.84 s) at +0.10 s. **Captions:** PROJ/film15/script/captions.json. **Frames:** N = 2095, g = round(t*30).
- **Sentence starts (s):** hook 0, pivot 6.18, boss 16.30, nickname 23.66, count 28.73, false 35.27, crisis 42.38, reveal 44.35, aha 55.08, ending 60.15, end 69.84.
- **Look:** wide or medium framings that show the dense set, a warm lit 3D world, sharp, NO depth of field, NO text/letters/numbers anywhere.

## Teams and takes (one take per team unless you split it; take folder = first shot number)
| team | shots | narration s | g range | take folder | key take (QA-art) |
|---|---|---|---|---|---|
| 1 | 1-4 | 0.00-6.15 | 0-184 | PROJ/v3/film15/s01 | YES (hook) |
| 2 | 5-9 | 6.15-16.30 | 184-489 | PROJ/v3/film15/s05 | |
| 3 | 10-16 | 16.30-31.05 | 489-932 | PROJ/v3/film15/s10 | |
| 4 | 17-24 | 31.05-44.30 | 932-1329 | PROJ/v3/film15/s17 | YES (false payoff 21-23) |
| 5 | 25-31 | 44.30-60.15 | 1329-1804 | PROJ/v3/film15/s25 | YES (reveal) |
| 6 | 32-36 | 60.15-69.84 | 1804-2095 | PROJ/v3/film15/s32 | YES (ending) |
Dissolves (11 frames) are where the plan says DIS: 5, 16 (+ mid-shot season DIS), 17, 28, 29, 32, 34. Render handle frames for them.

## Set (client-approved): PROJ/v3/set3d15/set15.py (+ set15_a/b/props/shots/lib)
- READ PROJ/v3/set3d15/API.md first (incl. the round-2 section), then QA_TECH.md and QA_ART.md: their "Re-check" sections hold the notes for YOUR shots (render-team notes).
- Locations: A (1963 school track) GOLDEN / DAY; B (1968 stadium) EVE / TENSE / DAY.
- `SH.setup_shot(n)` gives each shot's camera start/end keys, punch push-ins and FG props. Use it as the base, then tune.
- Hooks: set_bar_height, bar_fall, bar_reset, flash_bulb, stand_flashes, sawdust_spray, crowd / crowd_mode, torch_flicker, flag_wave, switch_light (shot 30 TENSE->EVE), set_season (shot 16), clear_keys. Key every animated hook on EVERY frame. One location per process.
- Hide the set's placeholder cards and put real cast15 cards at the marks.

## Cast: PROJ/v3/cast15 (read API.md)
- Members: dick, dick_olympic (medal=1), coach, coach_stands, boy1-3, rival1-3, official1-2, photographer, crowd1-6. Presets in STORY15 (also merged into puppet.STORY).
- Jump: run_curved(cast, phase, facing), plant, takeoff, flop_head -> flop_back -> flop -> flop_flick -> land_back -> sit_up. Straddle: straddle_a/b. Knock: knock. Place airborne/lying cards by anchors['bar'] / ['apex'] / ['head'] (NOT feet_y). Use CANVAS15_WIDE.
- `lerp_pose`/`resolve_pose` drop cast15 keys: tween the numbers yourself and re-add custom keys.
- laugh_bob(frame) drives the 3 Hz bounce for laughs (bob lifts the drawing, not feet_y: place laughing cards by the ground anchor).

## THE worked placement code: PROJ/v3/set3d15/cast_test/cast_test.py (+ README.md, test.jpg)
Copy its put() helper and the s10/s20/s27/s28/s36 placements into your own helper in your take folder (e.g. film/v3/film15/sNN/c15.py). Also read PROJ/v3/film8/common.py and PROJ/v3/film8/s01/shot.py for the take structure and gotchas (moves must move, key every hook every frame). No shared common.py.
Notes from the test (set3d15/cast_test/README.md): s27 needs the camera ~2.2 m from the bar (not the plan's 4.6 m) so the arch is >= 50 % of the width, and the card sits 0.3 D toward the camera so the round bar does not cut it; dim the TENSE spot pool on the bar so the bar is not blown to white. s20: Dick 1.3 D in front of the bar plane, camera at about head/bar height (his hair tufts reach 4.05 D). s36: push the camera in so the buried coach is at least 25 % of the frame height; make the sawdust spray denser and earlier.

## CAMERA RHYTHM — the client's new hard rule (production-lessons §10, film 2 is the model)
- Every shot has a clear move: push or pull 6-10 % of framing per second PLUS a lateral slide of about 40 px/s at 720 wide.
- PUSH! in the plan = a quick push-in of 15-25 % in 0.3-0.5 s (eased) on the punch word. WHIP = a fast pan/snap (1-3 frames of motion streak allowed).
- No near-static hold longer than 1 s (30 frames), anywhere.
- Foreground prop 1-2 D from the lens at a frame EDGE (<= 25 % of frame) in most shots, for parallax.
- Nobody stands frozen: breathing, weight shifts; laughing characters bounce ~0.06 D at ~3 Hz; the crowd bobs.
- **Acceptance per take:** `python3 PROJ/film15/motion_check.py take.mkv --first_g <first_g> --cuts <your cut g's>` must give median >= 4 and p90 >= 12 (film 2 measures 5.1/18.5). Put the numbers in QA.md. A take below this goes back.

## Hard rules for this film
- 1963 scenes (location A) show a SAWDUST pit only, never foam. No "world record", no letters, numbers or real national flags.
- The FLOP must read on a phone: in the reveal (25-29) the ∩ arch is at least half the frame width, the bar against the dark upper stand, head and legs hanging BELOW the bar. Part by part in shot 26: head over at 46.4 s, back at 47.2 s, legs at 47.8 s.
- Shot 20: a visible gap (~0.55 D) between Dick's head top and the bar.
- Shot 21 and 22: the bar falls (bar_fall) on the attempt; shot 7 also. In shot 30 the bar does NOT move.
- Mouths move ONLY on the coach's quotes: 17.80-23.55 s and 40.38-42.25 s (narration clock; use captions.json). Use coach_shout + talk_mouth there; still mouths elsewhere.
- Comic falls only, no injury (the coach in the sawdust gives a thumbs-up). Hard cut on the last word "ขี้เลื่อย" (~69.8 s).
- Heads above y 880. Cost: about 11-12 s wall per final frame (12 samples) with 2 processes x 2 threads. Draft first (360x640, 6 samples), contact sheet, then final.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
1. `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>` -> fix every FAIL; add QA_AUTO.md and phone_sheet.jpg.
2. `python3 PROJ/film15/motion_check.py ...` -> median >= 4, p90 >= 12, numbers in QA.md.
3. Check every frame yourself at 6 fps plus every cut ±3 frames: heads above y 880, contact shadows, props in hands, eye-lines, continuity with the neighbouring takes, mouths only in the quote windows, the bar where the story says.

## Delivery
- Take folders PROJ/v3/film15/sNN; meta.json with g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}; 6 handle frames each side (more for dissolves: half the dissolve + 2).
- take.mkv over 45 MB: `split -b 40M take.mkv take.mkv.part`. Push each take as soon as it is final. Do not open pull requests.
- Work autonomously. Do not ask for confirmation: the client has approved the set, the cast and the render.
- End with a short report: takes, frame ranges, s/frame, motion numbers, and anything that differs from the plan.
