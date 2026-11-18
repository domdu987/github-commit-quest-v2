# Render-team worker brief, film 13 (ไอ้แม่แรง: raising the Tremont House, Chicago 1861)

Follow film/WORKER.md section 1 (setup), section 4 (delivery) and section 5 (rules), with these differences.
Setup: `REPO=$(git rev-parse --show-toplevel); PROJ=$REPO/film` (any absolute PROJ works; sets/cast use relative imports).
`pip install -q bpy numpy pillow opencv-python-headless pythainlp`. bpy must print 5.x.

## Inputs
- Story: PROJ/film13/BRIEF.md. Shots: PROJ/film13/shot_plan.md (30 shots; YOUR shots are named in your launch message).
- Narration PROJ/film13/audio/narration.wav (66.38 s) placed at +0.10 s. Captions PROJ/film13/script/captions.json ("t" = narration s).
- Timing PROJ/film13/audio/timing.json (sent_start/sent_end, narration s).
- Clock: 30 fps, 720x1280. Film frame g = round((t_narr + 0.10) * 30). The plan's t0/t1 are narration seconds -> g0 = round((t0+0.10)*30).
  N = 1995 (g 0..1994). Hard cut on the last word "เอง" at narration 66.38 s.
- Look: wide/medium framings that show the dense set; calm camera that ALWAYS moves (slow push/pan/crane, never static > 6 frames,
  new framing every ~2 s); warm lit 3D world, one hard key, blue-violet shade 240-260, magenta <= 10 %; SHARP, NO depth of field,
  NO text anywhere; heads fully above y 880; characters stand in the world (contact shadows, correct scale, not floating).

## Set (client-approved 2026-11-18): PROJ/v3/set3d13/chicago.py
READ PROJ/v3/set3d13/API.md first, then QA_TECH.md and QA_ART.md (notes from the set gate) and look at contact.jpg.
Presets: street_wide, street_end, hotel_front, front_stair, mud_low, rain_street, crowd_street, under_wide, under_rows, jack_close,
suite_window, suite_room, tea_close, suite_two. Lights: DAY, RAIN, MORNING, CELLAR, SUITE.
Hooks: set_lift (street + cellar), set_jack_turn, set_jack_count (100/1000/5000), set_bars_visible, set_fill, set_mound, set_tea_ripple,
set_rain, set_cutaway, set_wheel_sink; stand points and marks per preset (top_window, trench_a/b, carry_a/b, jack_pile, mud_fall,
sit_mud, pay_a ...). Key every animated hook on EVERY rendered frame. One location per render process.
Never edit the set module: change things at runtime from your shot.py (hide/move/add objects).
Lift continuity (see the plan): hook h 0.55->0.65; pivot..nickname h 0; count h 0->0.05; false h 0.4 (seen from inside);
reveal h 0.4->0.8; aha h 0.9; ending h 1.0 (MORNING, fill 0.15).

## Cast: PROJ/v3/cast13 (read API.md, look at sheet.jpg)
pullman, rich, worker13_a/b/c, foreman13, lady13 / lady13_seat, gentleman13, town_a/b/c. Poses are listed in API.md
(e.g. rich_laugh_big, rich_mock_point (the ONLY lip-sync pose), rich_sit_tea, rich_look_window_smug, rich_step_out, rich_fall,
rich_sit_in_mud, rich_pay_sad; pullman_blow_whistle, pullman_point_plan, pullman_hand_on_jack_bar ...; worker_turn_bar_A/B, carry_jack).
Replace every placeholder card from the set with real cast13 cards. With worker turn_bar sprites call set_bars_visible(False) on
jacks where the sprite draws its own bar.

## Mouths and acting
- The rich man's mouth moves ONLY inside the quote windows (narration s, +-0.15): Q1 21.68-28.09, Q2 41.72-43.22. Still everywhere else.
- The fall (shot 29) is comic: arms up, hat flying, splash in mud, no injury; then dazed with stars, then handing the purse.
- Keep eye-lines to what the character looks at.

## Worked example and helpers
PROJ/v3/film8/s01/shot.py + QA.md and PROJ/v3/film8/common.py (read its GOTCHAS: moves must move, key every hook every frame,
one location per process). Make your OWN helper inside your take folder (e.g. PROJ/v3/film13/sNN/c13.py) by copying film8/common.py
and switching it to cast13 + set3d13/chicago.py. Do not create a shared film/v3/film13/common.py.

## QA (stricter: film/QA_TEAM.md "Stricter QA")
Before delivering: `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>`; fix every FAIL; add QA_AUTO.md and
phone_sheet.jpg. Then check frames yourself at 6 fps plus every cut +-3 frames (heads above y 880, contact shadows, props in hands,
eye-lines, mouths only in quote windows, continuity with neighbouring shots per the plan's lift state). Write QA.md.
The director's QA-tech re-checks every take; QA-art reviews the key takes (hook, reveal, false payoff, ending).

## Delivery
Take folders PROJ/v3/film13/sNN (NN = first shot number of the take; one take per location run is fine: s01, s02 ...).
meta.json: g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}; 6 handle frames each side.
take.mkv per WORKER.md section 4; if > 45 MB: `split -b 40M take.mkv take.mkv.part`. Also cues.json (sfx cues: t, dur, label).
Frames/raw/work stay out of git. Commit and push each take as soon as it is final to your branch. Do NOT open pull requests.
Work autonomously: the client already approved the set, cast and the render. Do not stop to ask; finish with a short report
(takes, frame ranges, s/frame, deviations from the plan).
