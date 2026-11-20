# Render-team worker brief, film 15 v2 REMAKE (ไอ้ปลาดิ้น — Dick Fosbury, Medford 1963 -> Mexico City 1968)

Follow film/WORKER.md for section 1 (setup: the PROJ symlink to the repo's film/), section 4 (delivery) and section 5 (rules). Your branch was checked out from film15/main; push to YOUR outcome branch only (render15b/teamK). Do not open pull requests. Work autonomously: the client has said the set needs no client OK once QA-art passes it, and it has passed. Do not ask for confirmation.

This is a REMAKE. v1 was rejected because it looked like a slideshow of medium shots: too many cuts, flat light, characters floating, close faces, grey slabs. v2 must match the reference channel (PROJ/ref_shorts/ sheets): LONG TAKES with a TRAVELLING camera, BIGZOOMs, rich lit 3D sets, vivid colour.

## Inputs
- **Plan (the law):** PROJ/film15/shot_plan.md (v2: takes T1-T7). Also PROJ/QA_TEAM.md sections G, H, I. Facts: PROJ/film15/FACTS.md.
- **Narration:** PROJ/film15/audio/narration.wav (69.84 s) at +0.10 s. Captions PROJ/film15/script/captions.json. Frames: N = 2095, g = round(t*30).
- **Sentence starts (s):** hook 0, pivot 6.18, boss 16.30, nickname 23.66, count 28.73, false 35.27, crisis 42.38, reveal 44.35, aha 55.08, ending 60.15, end 69.84.
- **Set QA reports:** PROJ/film15/qa/SET_v2_art.md and SET_v2_tech.md. Their render-team notes for YOUR take are mandatory.

## Teams and takes
| team | take(s) | s | g range | take folder | transition in | key take |
|---|---|---|---|---|---|---|
| 1 | T1 (BIGZOOM 1) | 0.00-16.30 | 0-489 | PROJ/v3/film15b/t1 | – | YES |
| 2 | T2 | 16.30-28.73 | 489-862 | PROJ/v3/film15b/t2 | cut | |
| 3 | T3 (BIGZOOM 2) | 28.73-35.27 | 862-1058 | PROJ/v3/film15b/t3 | dissolve 7 (push-through match) | YES |
| 4 | T4 | 35.27-44.38 | 1058-1331 | PROJ/v3/film15b/t4 | cut | |
| 5 | T5 + T6 (one continuous take) | 44.38-60.15 | 1331-1804 | PROJ/v3/film15b/t5 | cut | YES (reveal) |
| 6 | T7 | 60.15-69.84 | 1804-2095 | PROJ/v3/film15b/t7 | dissolve 11 | YES (ending) |
- Dissolves INSIDE a take (T3 season dissolve ~30.3, T3 match-dissolve into BIGZOOM 2 at 31.0, T5 rival match-dissolves 50.35 / 52.85, T7 sky-to-sky 64.6) are baked by YOU into your take.
- T2 must END pushing into the newspaper photo, T3 must START inside that same photo (team 2 and 3: use the same newspaper texture and framing at g 862; the 7-frame dissolve hides the seam). Team 5 owns T5 and T6 as one camera path, no cut between them.

## Sets (QA-art passed): PROJ/v3/set3d15/v2_a.py (+ v2_a_shots.py) and v2_b.py (+ v2_b_shots.py)
- READ PROJ/v3/set3d15/API_v2_a.md and API_v2_b.md first, then API.md (v1 hooks, still valid).
- Location A (Medford 1963): T1, T2, T3 up to 31.0, T7 from 64.6. `build_a2('HERO')` golden hour; `HERODAY` after the T3 season dissolve. BIGZOOM 1 path = `v2_a_shots` (BZ1, key_camera); rays toggle RAYS_ON, EXPO, GRADE_SAT. Grounding helpers: ground_card, ground_card_anchor, surface_z; rim_on/rim_off; newspaper(); spot().
- Location B (Mexico 1968): T3 from 31.0, T4, T5, T6, T7 to 64.6. `B2.build('NIGHT'|'TENSE'|'DAY72')`. BIGZOOM 2 = `bigzoom2(t)` / `apply_bigzoom2()`; T5 ride-along = `t5_ride(t)`, `dick_t5(t)`, `apply_t5()`. Rim: `rim(True, side=...)`. Grounding: `card`, `seat_card`, `airborne_over_mat`, `check_grounding` (must return empty on every frame you check), `spot_pool`.
- One location per process: a take that crosses locations (T3, T7) renders its parts in separate processes and dissolves them in your take.
- Sprite caches (work_v2_a/sprites, work_v2_b/sprites) are not in git; they rebuild on first use.

## Cast: PROJ/v3/cast15 (read API.md)
- Members: dick, dick_olympic (medal=1), coach, coach_stands, boy1-3, rival1-3, official1-2, photographer, crowd1-6. Flop poses: run_curved, plant, takeoff, flop_head -> flop_back -> flop -> flop_flick -> land_back -> sit_up; straddle_a/b; knock. Place airborne/lying cards by anchors['bar']/['apex']/['head'], CANVAS15_WIDE. laugh_bob for laughs.
- The coach wears the SAME maroon cap and windbreaker in 1963 and 1968.
- `lerp_pose`/`resolve_pose` drop cast15 keys: tween the numbers yourself.

## v2 RULES (QA_TEAM §G/§H/§I) — a take that breaks one goes back
1. **Camera travels.** Your take is ONE continuous camera path (follow, crane, push THROUGH objects, ride along, orbit). No hard cuts inside a take except the two WHIP pans in T4. Ease every move (no linear starts/stops). No near-static hold > 1 s.
2. **BIGZOOM** (T1 0.0-4.4, T3 31.0-35.3): starts extreme wide from high and far (character < 5 % of frame height), ends medium (character 35-60 %), eased, passing THROUGH set detail (trees, bleachers, floodlight beams, crowd). Dick must be findable at the start (spot pool / beams). Mark the frames in QA.md.
3. **Distance:** at least half of your frames wide or medium-wide. Close-ups ONLY the planned ones (23.0, 41.7, 59.8 s, about 0.8-1 s each). No face taller than 35 % of the frame otherwise.
4. **Angles:** use the angle types the plan gives your take; never the same height/angle for long. Foreground objects passing the lens for parallax.
5. **Nothing floats:** every standing card on a surface with a contact shadow; airborne jumpers only over the bar/pit with a shadow on the mat/sawdust; no bar or pole through a face; no grey slabs; no hanging debris.
6. **Light and colour:** motivated key (low sun + god rays in A; floodlight beams in B), rim light on characters (rim_on / rim()), warm + cool in the same frame. Per take: mean sat >= 0.50, vivid >= 45 %, luma 85-110, magenta <= 10 % (`python3 PROJ/qa_stats2.py take.mkv`).
7. **Characters always act** (rocking, stretching, breathing, cheering, laughing with 3 Hz bob, crowd bobbing). Nobody still > 1.5 s.
8. **Signs** are allowed and wanted: sharp and readable on a phone (MEDFORD HIGH, TRACK & FIELD, HIGH JUMP, FOSBURY FLOPS OVER BAR, MEXICO 68, 2.24 m, 1972).
9. **Facts:** 1963 = sawdust pit, never foam. No "world record". No real national flags. Comic falls only (the coach gives a thumbs-up from the sawdust). Hard cut on the last word "ขี้เลื่อย" (~69.8 s).
10. **Story beats on the narration clock** (see the plan): bar falls 13.3 (T1), flash 24.6 (T2), bar rises 32.5 / rival fails 33.8 (T3), bars fall 38.0 and 39.2 (T4), head 46.4 / back 47.2 / legs 47.8 (T5), bar does NOT move 55.1-57.4 (T6). Mouths move ONLY in the quote windows 17.80-23.55 and 40.38-42.25.
11. **Bar height in T4 low shot:** the set uses 2.46 m so the ~30 cm gap over Dick's hair reads; the board says 2.24 m.

## Cost and process
- Final: 720x1280, 12 samples, 2 processes x 2 threads. Location A ~12-20 s/frame; location B far views ~16-20 s, pit/stand views ~40 s/frame. Teams 4 and 5 have the heaviest takes: start the final render as soon as the draft passes.
- Draft first (360x640, 6 samples, every 2nd frame), make a contact sheet and run motion_check on the draft, fix, then final.

## QA (stricter, PROJ/QA_TEAM.md)
1. `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your cut g's>` -> fix every FAIL; add QA_AUTO.md and phone_sheet.jpg.
2. `python3 PROJ/film15/motion_check.py take.mkv --first_g <first_g> --cuts <cuts>` -> median >= 4, p90 >= 12.
3. `python3 PROJ/qa_stats2.py take.mkv` -> numbers in rule 6.
4. Look at every frame at 6 fps plus every seam ±3 frames: grounding, faces <= 35 %, bar position, mouths, continuity with neighbour takes.
5. In QA.md list: BIGZOOM frame ranges (if yours), angle types used with frame ranges, close-up frames, motion/colour numbers.

## Delivery
- Take folder as in the table; meta.json with g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}; 6 handle frames each side (dissolve takes: half the dissolve + 2 extra at the start).
- take.mkv over 45 MB: `split -b 40M take.mkv take.mkv.part` and commit the parts. Push as soon as final. Commit WIP regularly.
- End with a short report: frame range, s/frame, motion + colour numbers, BIGZOOM/angle list, anything that differs from the plan.
