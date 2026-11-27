# Render-team worker brief, film 24 (ไอ้เรือเต่า: Korea's turtle ship, Admiral Yi Sun-sin, 1592)

Follow film/WORKER.md for section 1 (setup), section 4 (delivery) and section 5 (rules). The film-24 differences below take precedence.
Work autonomously: the client has approved the set and the render. Do not ask for confirmation.

## Inputs
- **Brief and shots:** PROJ/film24/BRIEF.md (the story, the client's hard rules and the look) and PROJ/film24/shot_plan.md (17 shots).
- **Client checklist:** PROJ/CLIENT_CHECKLIST.md. Every rule applies to every frame.
- **Narration:** PROJ/film24/audio/narration.wav (65.0 s), placed at +0.10 s.
- **Captions:** PROJ/film24/script/captions.json. Sentence starts are in PROJ/film24/audio/timing.json.
- **Frames:** N = 1950, g = round(t*30). Shot bounds use round(t0*30); in-shot events use round((t+0.10)*30).

## Look (client: "R9 look")
- Cycles path tracing with GI, one warm soft sun, sky fill and thin haze, all provided by the set.
- Render 24 adaptive samples with OIDN at 540x960. Then `J.post()` upscales to 720x1280 and applies the grade (bloom on hot spots, saturation, S-curve, vignette).
- Every delivered frame is the post() output at 720x1280.
- DOF only on the three macro inserts (shots 2, 8a, 9a), using the preset's fstop. Everything else stays sharp, characters always sharp.
- **Never** use QA_TEAM.md §G-§M or DETAIL_SPEC.md; they are void for this film.

## Set
PROJ/v3/set3d24/joseon.py. READ API.md first and look at contact.jpg.
- Locations: `yard` and `sea`. One location per process.
- Hooks: set_spikes, set_ports, set_dragon_smoke, set_cannon_smoke, set_fleet_chase, set_korean_turn, set_damage, set_special('board'|'solo'), ship_root, clear_keys.
- Key every hook on every rendered frame. Smoke hooks must be called EVERY frame.
- Cameras stay inside the ±1500 haze box.
- Never edit joseon.py. Do any runtime set dressing from your shot.py.

## Cast
PROJ/v3/cast24. Read API.md and look at sheet.jpg.
- **Members:**
  - yi24
  - jp_cmd24 (the commander)
  - ashi_a24..ashi_d24 (Japanese soldiers)
  - kor_a24..kor_d24 (Korean workers and crew)
- **Poses:** STORY24 `<cast>_<pose>`.
- **Replace placeholders:** swap every placeholder card the set stages with a real cast24 card.
- **Ships:** cards on ships are parented to `J.ship_root(ship)` so they ride the swell.
- **Kneel, crawl and plank poses:** put `anchors["ground"]` on the surface.
- **Mouths:**
  - jp_cmd24 only, and only inside the quote windows 16.1-21.4 s and 34.8-37.0 s (talk_mouth).
  - Everywhere else, mouths hold.

## Worked example (read before building anything)
- PROJ/v3/film24/common.py holds the shared helpers: Take, final_loop, make_actor, place, head_report. Its gotchas are at the top.
- PROJ/v3/film24/s01/ holds shot.py, QA.md, meta.json and contact.jpg (shots 1-2: yard roof_low plus the macro_dragon insert).
- Copy its structure.

## Client hard rules (failing any one is a reject)
- **Nothing floats.** Feet, knees and ship hulls touch their surface. Every person has a contact shadow.
- **Camera:**
  - No shake.
  - One slow eased move per shot.
  - Never static for more than 6 frames.
  - Nothing is parented to the camera.
  - Foreground props are world-fixed.
- **Movement:** anyone who moves steps with the legs (walk/crawl cycles), otherwise feet are planted. No sliding.
- **Characters:**
  - No two identical characters in one frame: vary member, pose, size and mirroring.
  - Near figures are bigger than far ones.
  - Whole heads stay above y 880.
  - No face fills the frame for more than about 1 s.
- **Cuts:** hard cuts only (transition_in {"type":"cut","frames":0}).
- **Tone:** comic and bloodless: no injury, no bodies, no fire (only smoke and muzzle flashes).

## Assignments
| team | takes (sNN = first shot) | shots | g range | frames |
|---|---|---|---|---|
| director (worked example) | s01 | 1, 2 | 0-150 | 151 |
| team 1 | s03, s04, s05, s08 | 3; 4; 5+6; 8a+8b | 151-287, 288-430, 431-643, 734-918 | 678 |
| team 2 | s07, s09, s10, s11, s12 | 7; 9a+9; 10; 11; 12 | 644-733, 919-1001, 1002-1112, 1113-1256, 1257-1412 | 584 |
| team 3 | s13, s14, s15 | 13; 14; 15 | 1413-1606, 1607-1766, 1767-1949 | 537 |

Render 6 handle frames on each side of every take, except before g 0 and after g 1949.

### Shot notes (from the SET gate)
- **s03 fleet_wide:**
  - Fleet sails +x.
  - Slow lateral slide with it (set_fleet_chase keyed every frame).
- **s04 yard_wide:**
  - Yi (yi24 stand_arms_behind, later nod) on the quay in front.
  - 2-3 varied kor_* workers at small size, planted or walking with real steps.
- **s05 (shots 5 and 6) flag_deck / flag_deck_b on jflag:**
  - Shot 5: jp_cmd24_laugh_big, head back.
  - Shot 6: point_mock, then finger_up_promise. Lip-sync only from 16.1 to 21.4 s; the boss line starts at 14.37, so the mouth stays closed before 16.1.
  - Two different ashi_* behind him in shot 5.
- **s07 flag_deck_crew:** 3-4 different ashi_* laugh_point. Hips bounce, feet planted. Use the anchors in set API.md.
- **s08 (shots 8a and 8b):**
  - 8a is macro_spikes: set_spikes stage 1 at g round((26.4+0.1)*30), stage 2 at 27.6 and stage 3 at 28.3. A hammer clink lands on each.
  - 8b is roof_top: set_spikes 3, and set_ports 0→1 over g round(29.6*30)±6.
  - Workers kneel on the roof edge: kor_* kneel_hammer, ground anchor on the roof.
- **s09 (shots 9a and 9):**
  - 9a is macro_oar, special 'solo'.
  - 9 is hansan_high: Korean ships flee ahead (set_korean_turn 0), and the Japanese follow.
- **s10 flag_bow:** jp_cmd24_shout_forward with the gunbai; lip-sync 34.8-37.0 s only.
- **s11 chase:** 3 varied ashi_* sword_raise on j_near's bow, planted.
- **s12 board:**
  - Soldiers at j_board's rail peer_worried.
  - Then 1-2 take real steps back (walk cycle backwards, feet stepping).
  - A ladder carried by ashi_d24_ladder_front and ashi_b24_ladder_back.
  - The push ends on the spikes.
- **s13 reveal_top:** set_korean_turn 0→1 over about 2 s, then set_cannon_smoke rising, and set_damage creeping 0→0.35.
- **s14 aftermath:** set_damage 1, smoke, listing ships, turtle ship sailing through.
- **s15 shore:**
  - jp_cmd24_plank_cling on the plank, riding the water (parent to the plank's swell).
  - Hard cut inside the take to the sand: crawl_a/crawl_b alternating about every 8 frames, moving forward 0.45 D per half step.
  - wet24 1. The take ends exactly at g 1949; there is no out-handle.

## Overlays and detail (client, second reference R10)
- Motion-graphic overlays (red ✗ marks and a "47 : 0" tally) are composited by the director in conform, NOT in Blender. Keep the top third of shots 13 and 14 free of key action from g 1560 on.
- s13 and s14 must also write `overlay.json` in the take folder, a list per frame of every Japanese ship that set_damage has hit: {"g":…, "ships":[{"name":…, "hit_g":…, "x":…, "y":…}]}. x and y are the screen px of the ship's deck centre at 720x1280; use bpy_extras.object_utils.world_to_camera_view on the ship root. The ✗ marks pop onto those points.
- Prop detail: where the camera is close to a prop or a deck (flag_deck*, board, chase, roof shots), add cheap surface detail from your shot.py if it is missing: plank seams, nail heads, rope wraps, iron rivets. Do not add heavy geometry.
- The 3 macro inserts must be crisp at the focus plane and detailed. Check the focus distance on the subject.

## QA (before delivering every take)
1. Run `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <in-take cut g's>`. Fix every FAIL, then add QA_AUTO.md and phone_sheet.jpg to the take folder.
2. Run `python3 PROJ/qa_jitter.py` on every take with a camera move, a walk or a crawl. It must report no shake and no slide.
3. Review every frame yourself as 6 fps contact strips, plus ±3 frames around every cut. Check:
   - heads above y 880
   - contact shadows
   - feet planted or stepping
   - no floating
   - no identical duplicates
   - perspective size
   - mouths only in the quote windows
   - continuity with the neighbouring takes in shot_plan.md
4. Write QA.md, as in s01.

## Delivery
- Put each take in PROJ/v3/film24/sNN/: shot.py, meta.json, cues.json, contact.jpg, QA.md, QA_AUTO.md, phone_sheet.jpg and take.mkv.
  - meta.json holds g0, g1, first_g, n_frames, and transition_in {"type":"cut","frames":0}.
  - If take.mkv is over 45 MB, split it with `split -b 40M take.mkv take.mkv.part`.
- Encode with `ffmpeg -framerate 30 -start_number <first_g> -i frames/g_%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv`.
- Keep frames/, raw/ and work/ out of git with a .gitignore in each take folder. The repo is near its size quota.
- Push each take to your own branch as soon as it is final. Do not open pull requests.
- **Processes:** at most 2 render processes with 2 threads each.
- **Network:** no network calls except git and pip, and no paid APIs.
- Finish with a short report: the takes delivered, frame ranges, s/frame, and anything that differs from the plan.

## Second pass: Look A (client wants two versions; do this AFTER all your B takes are delivered)
- Pull film24/main into your branch first (`git fetch origin film24/main && git merge --no-edit FETCH_HEAD`). It brings the Look A switch in joseon.py and common.py.
- For each of your takes, in the same take folder:
  1. Move the B frames aside: `mv raw raw_B; mv frames frames_B`. Keep take.mkv and meta.json untouched.
  2. Re-render the same frames with `JOSEON_LOOK=A python3 shot.py final ...`. Same shot.py, no edits: it means no haze, no DOF, 8 samples, full 720x1280, and no post(). Expect about 10 s per frame on 4 cores.
  3. Deliver as `take_A.mkv` (same ffmpeg line but `-crf 12` to save repo space, `-i frames_A/g_%04d.png` after `mv frames frames_A`), plus `meta_A.json` (same g0/g1/first_g/n_frames), `contact_A.jpg` and `QA_A.md`. Run qa_auto on take_A.mkv.
  4. Do NOT grade Look A frames: the director applies the v1.1 grade in conform.
- Push them to your branch. If time runs short, B always comes first.

---
# VERSION C (turtle_C): client-approved board_C2, full render. Read this section first; it overrides the sections above where they differ.
Read: PROJ/LIGHT_SPEC.md, PROJ/film24/shot_plan_C.md (incl. UPDATE and UPDATE 2), PROJ/v3/set3d24/API.md sections "Look C" and "Look C, round 2", PROJ/v3/set3d24/board_C2.jpg, PROJ/v3/kit/README.md.

## Wait for the set
- Prepare and test now (shot.py, drafts at 12 samples).
- Start FINAL renders only after `git fetch origin film24/main && git merge --no-edit FETCH_HEAD` brings `PROJ/v3/set3d24/C_READY` (the set builder's production fixes). Re-check your draft once after that merge.

## Look C
- Env `JOSEON_LOOK=C` on every render (or `J.set_look('C')` before build). Same Take/final_loop as before: 24 samples at 540x960 + `J.post()` (it applies the C grade) → 720x1280.
- Cards: use `J.card_rim()` on the sun side when backlit. Contact shadows as before.
- Fire, fireballs and burning ships ARE allowed now. Still bloodless: no injury, no bodies. Sailors jump into the sea comically.
- Every client hard rule above still applies.

## Timing (the film is now 71.9 s, N = 2158)
- Takes s01-s07 keep their g. s08 is replaced by the build-up s08C (g 734-1126).
- Takes from s09 on keep their OLD shot.py timing: render the same old g range exactly as before, because all their narration moved together. Deliver `meta_C.json` with every g **+208** (g0, g1, first_g), so conform places them correctly.
- g1 is EXCLUSIVE (= the next take's g0).

## Takes and changes
| team | take | old g (render) | new g (meta_C) | shot | what to do |
|---|---|---|---|---|---|
| 1 | s01 | 0-150 | same | 1, 2 | relight only (same shot.py, look C) |
| 1 | s03 | 151-287 | same | 3 | relight only |
| 1 | s05 | 431-643 | same | 5, 6 | relight only (rigging shadows, rim on jp_cmd24) |
| 1 | s07 | 644-733 | same | 7 | relight only |
| 1 | s11 | 1113-1256 | 1321-1464 | 11 | relight only, +208 in meta |
| 1 | s12 | 1257-1412 | 1465-1620 | 12 | relight only, +208 in meta |
| 2 | s04 | 288-430 | same | 4 | **NEW HERO 1**: preset `hero_yard`; slow eased low push-in, the ship looming; Yi (yi24 stand_arms_behind, then nod at his old cue) at anchor `yi_hero`, rim + contact shadow; dragon smoke every frame |
| 2 | s08C | — | 734-1126 | build-up | **NEW**: location/preset `build_dock`; `J.set_build_g(g, frame)` every frame; camera `J.build_cam((g-734)/392)`; schedule from `J.build_schedule()`. Also write `build_anchors.json`: per frame {"g", "stage", "x", "y"} from `J.build_anchor(stage)` (px at 720x1280) |
| 2 | s09 | 919-1001 | 1127-1209 | 9a, 9 | relight only, +208 |
| 2 | s10 | 1002-1112 | 1210-1320 | 10 | relight only, +208 |
| 3 | s13 | 1413-1606 | 1621-1814 | 13a, 13b, 13c | **SPLIT into 3 shots with hard cuts at old g 1527 and 1560**. 13a 1413-1526: keep the accepted aerial U move, relit. 13b 1527-1559: preset `cannon_close`, `set_broadside` firing 3-4 ports in sequence, a slow slide. 13c 1560-1606: preset `hit_close`, `set_hit_explosion` peaking at old g ~1567, ashigaru A jumps with `jump_arc` + `set_jump_splash` (one in the air, one at the rail who then jumps), slow push |
| 3 | s14 | 1607-1766 | 1815-1974 | 14 | **NEW HERO 2**: preset `hero_orbit`, `J.orbit_cam(u)` slow eased; burning fleet behind; top third calm for the tally (old g 1718-1766) |
| 3 | s15 | 1767-1949 | 1975-2157 | 15 | relight only, +208; ends exactly at the last frame |

- In-take cuts for qa_auto: s13 at 1527 and 1560 (old g). The old in-take cuts of the other takes are unchanged.

## Overlays
- s13 writes `overlay_C.json` for **13c only**: the hit ship's deck point once the explosion peaks (hit_g ≈ old 1567). There is no ✗ in 13a or 13b.
- s14 writes `overlay_C.json` with every visible burning ship.
- Same format as before ({"g", "ships":[{"name", "hit_g", "x", "y"}]}), with g in OLD numbering; conform adds 208.

## Delivery (in each take folder; old A/B files stay untouched)
- Files: `take_C.mkv` (`-crf 12`, from frames_C/), `meta_C.json`, `contact_C.jpg`, `QA_C.md`, `QA_AUTO_C.md`, plus overlay_C.json or build_anchors.json where listed.
- Keep raw/frames out of git: rename frames to frames_C before encoding (frames_C/ and raw_C/ are already ignored or need adding to .gitignore). Split anything over 45 MB as `take_C.mkv.part*`.
- Make your shot.py C changes as `shot_C.py` when the shot changed (s04, s08C, s13, s14). Relight-only takes reuse shot.py with JOSEON_LOOK=C.
- Push to your branch render24/cK (K = team) as each take is final. Report: takes, s/frame, deviations.
