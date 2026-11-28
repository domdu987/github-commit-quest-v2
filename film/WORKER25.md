# Render-team worker brief, film 25 (ไอ้ถังน้ำ: Britain's first tank, Mark I, 1915-16, Flers 15 Sep 1916)

Follow film/WORKER.md for section 1 (setup), section 4 (delivery) and section 5 (rules). The film-25 differences below take precedence.
Work autonomously: the client has approved the look and the set. Do not ask for confirmation.

## Inputs
- **Shots:** PROJ/film25/shot_plan.md (34 shots, hard cuts only). The story is in PROJ/film25/script/script_th.txt; the facts are in PROJ/film25/FACTS.md.
- **Client checklist:** PROJ/CLIENT_CHECKLIST.md. Every rule applies to every frame.
- **Narration:** PROJ/film25/audio/narration.wav (69.75 s), placed at **0.00 s**. The film clock is the narration clock.
- **Captions:** PROJ/film25/script/captions.json, with t in film seconds. Sentence starts are in PROJ/film25/audio/timing.json.
- **Frames:** 30 fps, 720x1280, N = 2093 (g 0..2092). Use g = round(t*30) for both shot bounds and in-shot events. g1 is EXCLUSIVE (= the next shot's g0).

## Look (client-approved "vivid", 28 Nov)
- Golden-hour key and a strong bounce, as provided by the set. Read PROJ/LIGHT_SPEC.md (v2) for the spirit.
- **Colour targets** (`python3 PROJ/film25/tools/light_metrics.py take.mkv`; they override LIGHT_SPEC's saturation range):

  | metric | target |
  |---|---|
  | mean luma | 0.48-0.55 |
  | p1 | 0.02-0.08 |
  | p99 | 0.90-0.95 |
  | local contrast | ≥ 0.038 |
  | mean saturation | 0.45-0.50 |
  | Lab chroma | ≥ 28 |
- Crisp image, NO depth of field anywhere, characters always sharp.
- **Every delivered frame is the set's post() output at 720x1280** (sharpen, clarity, grade and vibrance). Never deliver a raw render.
- **Final render settings:**
  - Try 32 adaptive samples (threshold 0.02, OIDN with albedo and normal passes) at 540x960 (75 %), then post() upscales to 720x1280.
  - Measure s/frame and the metrics on your first final frame against the set's own still (PROJ/v3/set3d25/finals/<preset>.png).
  - If the 75 % frame reads soft or flickers, use 100 %.
  - Budget about ≤ 40 s/frame on 4 cores.
- **No text of any kind,** in the world or as overlays. The only symbol is the plain water-tank silhouette stencil, which the set provides.

## Set
PROJ/v3/set3d25/. READ API.md (every section, including EXTENSION) and METRICS.md first, and look at contact.jpg.
- Entry point is set25.py (`W.build(preset)`). Locations: factory, trial, front, street, dock, sky. One location per process.
- Tank hooks are in tank25.py:
  - `set_build(H, stages, frame)` for the build-up, word-locked
  - `set_drive`
  - `setup_crossing` and `set_crossing(H, u, frame)`
  - `pose_on_ground`
  - `set_state` ('stuck', 'smoking', 'normal')
  - `set_stencil`
  - `set_sparks`
- Other hooks: `factory.set_dial`, `factory.set_crate`, `sky.set_plane`.
- Key every animated hook on EVERY rendered frame. Smoke and sparks are called every frame.
- **Never edit the set modules.** Do any runtime dressing (hide, move, add) from your shot.py.
- **Wait for the set:** final renders start only after `git fetch origin film25/main && git merge --no-edit FETCH_HEAD` brings `PROJ/v3/set3d25/READY25`. Until then, prepare and draft.

## Cast
PROJ/v3/cast25. Read API.md and look at contact.png.
- **Members:**
  - general25 (THE MOCKER)
  - engineer25 (the quiet hero; never speaks)
  - worker_a25, worker_b25, worker_c25
  - tommy_a25..tommy_d25
  - german_a25..german_c25
  - pilot25
- **Poses:** use STORY25 poses, plus `cycle()` walk/run/march, `march_flag25()` and `run_away25()`.
- **Replace stand-ins:** swap every stand-in Tommy card the set stages for the right cast25 member.
- **Mouths:** general25 only, with talk_mouth, inside his two quotes. Everywhere else, mouths hold.
  - 18.39-25.35 s (g 552-760)
  - 44.37-46.52 s (g 1331-1396)

## Helpers (no shared module)
- Copy PROJ/v3/film24/common.py into your own take folder as `c25.py`, and adapt it to set25 and cast25:
  - Take
  - final_loop
  - make_actor
  - place
  - head_report
  - feet_report
- Read its GOTCHAS at the top: key every hook every frame, Actor roots without rotation, contact decals, one location per process.
- Do NOT create a shared film/v3/film25/common.py.

## Client hard rules (failing any one is a reject)
- **Nothing floats.** Feet and tank tracks touch the ground. Crane loads hang on visible chains. Every person has a contact shadow.
- **Camera:**
  - No shake.
  - One slow eased move per shot.
  - Never static for more than 6 frames.
  - Nothing parented to the camera.
  - Foreground props are world-fixed.
- **Movement:** anyone who moves steps with the legs (walk/run/march cycles), otherwise feet are planted. No sliding. Tanks move only with set_drive or set_crossing, so the tracks scroll.
- **Characters:**
  - No two identical characters in one frame: vary member, pose, size and mirroring.
  - Near figures are bigger than far ones.
  - Whole heads stay above y 880 and feet stay out of the caption band (feet above y 860, or below the frame edge).
  - No face fills the frame for more than about 1 s.
- **Cuts:** hard cuts only (transition_in {"type":"cut","frames":0}). No dissolves.
- **Tone:** comic and bloodless. No injury and no bodies. Bullets spark and ping off the steel; Germans run away comically.
- **Literal nouns:** every spoken noun is shown on screen in its shot (see the shot_plan "picture" column).

## Assignments (one take per shot, sNN = shot number; 6 handle frames each side except before g 0 and after g 2092)
| team | branch | takes | frames |
|---|---|---|---|
| 1 FACTORY | render25/t1 | s01 s02 s03 s04 s07 s08 s14 s15 s16 s17 s18 s31 | 658 |
| 2 FRONT | render25/t2 | s05 s06 s20 s21 s22 s24 s25 s26 s27 s28 s29 s30 | 710 |
| 3 TRIAL, OP, DOCK, SKY, STREET | render25/t3 | s09 s10 s11 s12 s13 s19 s23 s32 s33 s34 | 724 |

Order inside each team: the hero shots first. Team 1: s15-s17, then s31. Team 2: s24-s26. Team 3: s10, s23, s34.

### Shot g ranges (g0-g1, g1 exclusive) and presets
| shot | g | preset | shot | g | preset |
|---|---|---|---|---|---|
| 1 | 0-44 | fac_wide | 18 | 1016-1071 | fac_crate |
| 2 | 44-84 | fac_weigh | 19 | 1071-1135 | dock_crate |
| 3 | 84-139 | fac_foreman | 20 | 1135-1211 | front_column |
| 4 | 139-154 | fac_stencil | 21 | 1211-1266 | front_halt |
| 5 | 154-232 | front_aerial | 22 | 1266-1301 | front_stuck |
| 6 | 232-316 | front_parapet | 23 | 1301-1396 | front_op |
| 7 | 316-396 | fac_side | 24 | 1396-1447 | cross_nose |
| 8 | 396-485 | fac_bench | 25 | 1447-1526 | cross_hero |
| 9 | 485-552 | trial_wide | 26 | 1526-1558 | cross_pull |
| 10 | 552-626 | trial_general | 27 | 1558-1592 | cross_wire |
| 11 | 626-676 | trial_trench | 28 | 1592-1636 | cross_hull |
| 12 | 676-760 | trial_general (new angle) | 29 | 1636-1688 | cross_flee |
| 13 | 760-838 | trial_camp | 30 | 1688-1778 | cross_bucket |
| 14 | 838-882 | fac_chassis | 31 | 1778-1880 | fac_crate_open |
| 15 | 882-918 | fac_plates | 32 | 1880-1932 | sky_plane |
| 16 | 918-960 | fac_tracks | 33 | 1932-2009 | street_wide |
| 17 | 960-1016 | fac_sponsons | 34 | 2009-2093 | street_low (ends at the last frame) |

### Word locks (g = round(t*30))
- **s02 "หนัก 28 ตัน" 1.45 s:** the hull lands on the weighbridge on the chains; the needle swings to the far end at about g 62.
- **s04 "ถังน้ำ" 4.63 s:** the brush finishes the silhouette stencil (set_stencil) by g 150.
- **s15:**
  - "แผ่นเหล็ก" 29.40: plates lock at g 882-895.
  - "หมุดย้ำ" 30.08: rivets punch in chunk by chunk at g 902-918, and the riveter's hammer (worker_a25 + hammer25) strikes on each chunk.
- **s16:**
  - "ตีนตะขาบ" 30.59: the track loop drops round the hull at g 918-933.
  - "วนรอบทั้งคัน" 31.12: set_drive scrolls the links round the loop until g 960.
- **s17:**
  - "ป้อมสองข้าง" 31.99: sponsons slide in at g 960-982.
  - "ปืนใหญ่ 6 ปอนด์" 32.74: guns slide in at g 982-1000.
- **s18 "พ่นสีว่า ถังน้ำ" 34.75-35.71:** the stencil goes on the crate (worker spray pose) at g 1043-1071.
- **s24-s26 (one continuous crossing across 3 hard cuts):**
  - Map set_crossing u from 0 at g 1396 to 1 at g 1558, eased, continuous across the cuts.
  - "ยกหัวขึ้น" 47.45 (g 1424): the nose lifts.
  - "เกาะขอบฝั่งโน้น" 49.77 (g 1493): the front track grips the far lip.
  - "ดึงทั้งคัน ข้ามไป" 50.87-51.95: the tank pulls across.
- **s27 "โดนทับแบน" 52.44 (g 1573):** the wire squashes flat under the track.
- **s28 "เด้งออกจากเหล็ก" 53.51-54.55:** set_sparks pings over g 1605-1636, with no hole and no damage.
- **s29 "วิ่งหนีกันลั่น" 55.29:** german_a/b/c25 run_away25, all different, real running steps.
- **s30:**
  - "ใส่น้ำ" 57.12: hold on the plain bucket (g 1714).
  - "ข้าม" 57.47: the push reveals the tank across the trench behind it.
- **s31 "แท็งก์" 60.03 (g 1801):** the crate lid falls open (set_crate) and the tank is inside.
- **s32 "นักบินอังกฤษ" 63.05:** the plane flies (set_plane along its path) and pilot25 leans out looking down.
- **s34:**
  - The tank rolls up the street (set_drive), Tommies march behind cheering (cycle march, varied members), and general25 march_flag25 is closest behind its tail, cheering.
  - The take ends exactly at g 2092 ("ก็คือท่านนายพล"). No out-handle.

### Producer staging notes (from the set reviews)
- **Hero crossing s25:** the tank fills 50-60 % of the frame width, side-on, with sky behind the raised nose and the whole rhomboid visible. Near grass stays ankle-to-knee height of a puppet and clear of the tank silhouette.
- **Tank tail wheels:** always attached visibly to the tank's rear, never a loose disc on screen.
- **General's scenes:**
  - s10: general25_point_stick, a quick push-in on "ของเล่น" (20.06).
  - s12: march_flag25 mime with a bum-wiggle, plain flag.
  - s23: field glasses, then glasses_laugh.
  - Staff officers are tommy_*25 members, varied.

## QA (before delivering every take)
1. Run `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <in-take cut g's or none>`. Fix every FAIL, then add QA_AUTO.md and phone_sheet.jpg.
2. Run `python3 PROJ/qa_jitter.py` on every take with a camera move, a walk or a tank move. It must report no shake and no slide.
3. Run `python3 PROJ/film25/tools/light_metrics.py take.mkv`. It must PASS; paste the line into QA.md.
4. Review every frame yourself as 6 fps contact strips, plus ±3 frames around the take ends. Check:
   - heads above y 880 and feet out of the caption band
   - contact shadows
   - feet planted or stepping
   - nothing floating (crane chains, tail wheels)
   - no identical duplicates
   - perspective size
   - mouths only in the quote windows
   - word locks on time
   - no text anywhere
5. Write QA.md.

## Delivery
- Put each take in PROJ/v3/film25/sNN/: shot.py, c25.py (or import it from your first take), meta.json, contact.jpg, QA.md, QA_AUTO.md, phone_sheet.jpg and take.mkv.
  - meta.json holds g0, g1, first_g, n_frames, and transition_in {"type":"cut","frames":0}.
- Encode with `ffmpeg -framerate 30 -start_number <first_g> -i frames/g_%04d.png -c:v libx264rgb -crf 12 -preset slow take.mkv`. Split anything over 45 MB as `take.mkv.part*`.
- **The repo is near its size quota:**
  - Keep frames/, raw/ and work/ out of git with a .gitignore in each take folder.
  - Never commit PNG frames.
- Push each take to your own branch (render25/tK) as soon as it is final. Do not open pull requests.
- **Processes:** at most 2 render processes with 2 threads each.
- **Network:** no network calls except git and pip, and no paid APIs.
- Finish with a short report: the takes delivered, frame ranges, s/frame, metric lines, and anything that differs from the plan.
