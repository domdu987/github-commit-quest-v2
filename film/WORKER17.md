# Render-team worker brief, film 17 (ไอ้ช่างวัดหู — Bertillon, Paris 1882-83)

Follow film/WORKER.md exactly: section 1 setup, section 4 delivery, section 5 rules. The film-17 differences are below.
PROJ = your clone's film/ folder (clone_depth 1 of branch film17/main). Push to YOUR outcome branch only.

## Inputs
- **Brief and shots:** PROJ/film17/BRIEF.md and PROJ/film17/shot_plan.md (33 shots, 13 takes; your take is in your task message).
- **Look:** wide or medium framings that show the dense set, always-moving camera, warm lit 3D world. Sharp, NO depth of field, no readable text anywhere.
- **Narration:** PROJ/film17/audio/narration.wav (67.94 s), placed at +0.10 s. **Captions:** PROJ/film17/script/captions.json (narration time).
- **Frames:** N = 2052, g = round(film_t*30), film_t = narration_t + 0.10.
- **Sentence starts** (narration time): hook 0 / pivot 4.71 / setup 11.10 / boss 14.72 / nickname 21.61 / deadline 24.08 / count 28.25 / false 34.74 / crisis 39.76 / reveal 44.65 / aha 56.40 / ending 62.19 / end 67.94.

## CAMERA RHYTHM (client rule, production-lessons §10 + bible camera.md) — your take FAILS QA without it
- Every shot has a clear eased move: drift push/pull 6-10 %/s + lateral slide 20-60 px/s, or a snap (13-25 frames, x1.3-x3). Never > 6 frames under 0.25 px/frame; no near-static hold > 1 s.
- Framing change every 1.3-1.4 s on average: add a snap or reframe inside any shot longer than 2.2 s.
- Foreground prop 1-2 D from the lens in most shots. Laughing characters bounce ~0.06 D at ~3 Hz; nobody frozen (idle sway, blink).
- Measure your take: in-shot frame-diff on 90x160 grey frames, median >= 4 and p90 >= 12 with `python3 PROJ/film17/rhythm.py take.mkv --first_g <first_g> --cuts <your cut g list>` (calibrated: film 2 = 5.1 / 18.7, film 10 = 2.2 / 5.6). Report both numbers in QA.md.
- Heads: centre y 450-760, whole head above y 880.

## Set (QA-art approved 2026-11-19)
Approved by QA-art SET gate (client delegated approval to QA-art, 2026-11-19 — see PROJ/film17/BRIEF.md). PROJ/v3/set3d17/bertillon.py.
READ FIRST: PROJ/v3/set3d17/API.md (sections 1-9 + 5b), QA_ART_SET.md (per-preset notes for render teams), FIX1.md (stand points with pixel numbers).
- Units: 1 unit = 1 m; one character height D = 1.7 units (`bertillon.D`). Card heights per API.md §1; pass `scale = HEIGHT[who]/card_height_in_head_D` to `Actor.place`, or use the set's `stage_cast()` helper (API §5b).
- Presets: measure_wide, measure_chair, measure_high, measure_door, measure_low / records_aisle, records_low, records_desk, records_ladder / drawer_big, drawer_box, card_hero / street_wide, street_wagon. Lights DAY_INT, EVENING_INT, DUSK_EXT. Each preset already has a foreground prop 1-2 units from the lens; keep it in frame while you drift.
- Hooks (key every frame when animated): set_flicker, set_smoke, set_dust, set_pendulum, set_drawer, set_box_lid, set_card_lift, set_cards_fan, key_life, clear_keys; light keys sun_k, frost, beam_k.
- Stand points: use ONLY the marks listed per preset in API §6 / FIX1.md. Never stage at aisle0, ladder_foot, door_in, door_mid. Real cast cards lean toward low/high cameras: check head y after placing (shift dx as needed).
- Notes: seated poses use `seat17=None` (the set has its own 3D chair/bench); warm rim light on Bertillon/prefect/inspector over dark backdrops (records canyon, toise corner, wagon); keep the police wagon parked, seen side/rear (no horse); shot 31 ending wide: start the camera ~55 % closer to the chair than the preset (the seated inspector is only 32 px at the preset camera); card_hero has a warm bloom on the card centre: lower the card lamp so the card reads (portraits and bottle visible) — not near-white.
- Cost ~95-150 s per 720x1280 frame at 64 samples + denoise. Draft at 360x640 first.

## Cast
PROJ/v3/cast17 (`import cast17` before `sprites`). Read API.md. Members: bertillon, inspector17 (the mocker; CAST key is inspector17, poses inspector_*), prefect, dupont, gendarme_a, gendarme_b, prisoner_a/b/c (`cast17.KEY` maps short names).
- Poses: STORY17 (bertillon neutral/measuring/writing/holding_card/pointing/triumphant/tired; inspector laughing/pointing_mock/arms_crossed/shouting/shocked/seated_stiff/red_faced (flush17); prefect neutral/finger_up_three/stern; dupont innocent/held/sweating/caught; gendarmes escort/laughing/standing; prisoners sitting/standing). Expressions via `with_expr(pose, name)`.
- Mouths closed unless `speak(pose, frame, level)` inside the quote windows; `silent(pose)` otherwise. Props: calipers, card, pen, ledger (anchors calipers_r/l, card_r/l, nib_r/l, ledger_r/l; `hand_for_anchor()` pins caliper jaws onto an ear).
- Tweening (`lerp_pose`) drops seat17/flush17/seat_w: re-add them after tweening. Faces with pince-nez/beard drift beyond yaw ±0.8: keep yaw within ±0.7.

## Mouths and acting
- Mouths move ONLY on the inspector's quotes (narration time, +-0.15 s): 16.32-21.59 and 37.48-39.74. Laugh 15.46-16.32 (laugh pose + bounce, no lip-sync).
- Comic only, no injury. The ending: the inspector sits stiff in the measuring chair while Bertillon calmly measures his ear; hard cut on the last word "ตัวเอง" (film end g 2052).

## Worked example and helpers
- Worked example: PROJ/v3/film8/s01/shot.py, QA.md and PROJ/v3/film8/common.py. Read the gotchas: moves must move, key every hook every frame, one location per process.
- Make your OWN helper module inside your take folder (for example film/v3/film17/sNN/c17.py) by copying film8/common.py and switching it to cast17 and set3d17/bertillon.py.
- Do not create a shared film/v3/film17/common.py.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
- Before delivering, run `python3 film/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>` and fix every FAIL.
- Add QA_AUTO.md and phone_sheet.jpg to the take folder.
- Then check every frame yourself at 6 fps, plus every cut ±3 frames:
  - heads above y 880
  - contact shadows
  - props held
  - eye-lines
  - continuity with the neighbouring takes
  - mouths only in the quote windows
- The director's QA-tech re-checks it, and QA-art reviews the key takes (hook, reveal, false payoff, ending).

## Delivery
- Take folders: PROJ/v3/film17/sNN.
- meta.json holds g0, g1, first_g, n_frames and transition_in {"type":"cut"|"dissolve","frames":n}.
- Render 6 handle frames each side.
- If take.mkv is over 45 MB: `split -b 40M take.mkv take.mkv.part`.
- Push each take as soon as it is final. Do not open pull requests.
- Work autonomously. Do not ask for confirmation: the client already approved the set and the render.
