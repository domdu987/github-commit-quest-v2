# Render-team worker brief, film 25 (ไอ้ถังน้ำ: Britain's first tank, Mark I, 1915-16, Flers 15 Sep 1916)

Follow film/WORKER.md for section 1 (setup), section 4 (delivery) and section 5 (rules). The film-25 differences below take precedence.
Work autonomously: the client has approved the look and the set. Do not ask for confirmation.

## Inputs
- **Shots:** PROJ/film25/shot_plan_v2.md (58 shot rows, hard cuts only; v1 is void). The story is in PROJ/film25/script/script_th.txt; the facts are in PROJ/film25/FACTS.md.
- **Client checklist:** PROJ/CLIENT_CHECKLIST.md. Every rule applies to every frame.
- **Narration:** PROJ/film25/audio/narration.wav (69.75 s), placed at **0.00 s**. The film clock is the narration clock.
- **Captions:** PROJ/film25/script/captions.json, with t in film seconds. Sentence starts are in PROJ/film25/audio/timing.json.
- **Frames:** 30 fps, 720x1280, N = 2093 (g 0..2092). Use g = round(t*30) for both shot bounds and in-shot events. g1 is EXCLUSIVE (= the next shot's g0).

## COLOUR GATES, FINAL (producer, 28 Nov 05:21; overrides every colour target above)
- **HARD gates, checked per finished take with the characters in** (`light_metrics.py take.mkv` prints PASS/MISS on these only):
  - luma 0.46-0.56
  - mean saturation ≥ 0.42
  - no colour cast: |mean a*| and |mean b*| ≤ 6
  - no clipped channels
  - puppet faces exactly #fef7f6
- **Everything else is a printed GUIDE:** lc, p1/p99, chroma, sat p98, hue shares and colourfulness M.
- **Judge by eye against R11:** pure clean hues, nothing muddy, nothing tinted.
- **Grade:** gentle, using the set's post() (vibrance about 1.3-1.5, no hue shifts). Puppets are composited ungraded, so do NOT pass puppet pixels through any extra grade of your own.

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

## Assignments (shot plan v2.1: PROJ/film25/shot_plan_v2.md, 58 shots; it is the ONLY shot list, and v1's shot_plan.md is void)
One take per shot row. Name the take folder after the row's first shot number (row "29+30" → s29, "47-49" → s47).
The g column of shot_plan_v2.md is authoritative (g1 exclusive). Render 6 handle frames each side, except before g 0 and after g 2092.

| team | branch | locations | shot rows | frames |
|---|---|---|---|---|
| T1 | render25/t1 | FACTORY + DOCK | 1+2, 3+4, 5, 6, 13-17, 28, 29+30, 31+32, 33-38, 58, 60+61, 62, 63 | 744 |
| T2 | render25/t2 | FRONT | 7, 8+9, 10-12, 39-42, 45, 46, 47-49, 50-52, 53+54, 55-57, 59 | 716 |
| T3 | render25/t3 | TRIAL + FRONT OP + SKY + STREET | 18-27, 43, 44, 64+65, 66, 67, 68-70 | 633 |

**Order:** hero and gag shots first.
- T1: 6, 14, 29-34, 58, 62
- T2: 47-49, 50, 51, 45
- T3: 21, 23, 27, 68-70

**Framing:** the `frm` column gives the framing.
- **C (waist-up close):** the puppet card's waist sits at the frame bottom (crop the legs), with the head centre at 0.30-0.45 of the frame height.
- **Feet and heads:** in C shots the feet are below the frame edge, so the caption-band rule is met. Heads always stay above y 880.
- **Presets:** the set provides close presets (`*_close_*`, see API.md). Otherwise make your own camera near the named location preset, with no DOF and one slow eased move.

**Props and poses:** the gags use new cast25 props and poses (see cast25/API.md):
- props: watering_can25, shovel25, tin_cup25, toy_tank25, chalkboard25
- poses: *_pour_can, *_dig_a/b, *_cup_wait, *_cup_drink, general25_toy_dangle, general25_finger_wag, engineer25_shush/peek/sleeves/chalkboard_tap/proud/chart_hand, german_b25_glasses_slip, worker_b25_shocked, *_peek, worker_a25_hammer_crate, worker_c25_push_barrel

**Set hooks and presets:** factory.set_model_tank(u) with preset fac_chart; factory.set_doors(u) with fac_doors; dock_watertank; dock_deck; tank set_steam; the hull tap.

**Mouths:**
- general25 lip-sync only in 18.39-25.35 s (g 552-760) and 44.37-45.60 s (g 1331-1368).
- Lip-sync poses: point_stick, toy_dangle, finger_wag, glasses_laugh.
- Shot 23 (the imagined march) has no lip-sync: mouth open in a cheer.
- Everywhere else, mouths hold.

### Word locks (g = round(t*30); the word times are in captions.json)
- **3+4 "28 ตัน":** the hull touches the scale at about g 55, and the needle swings over g 58-70.
- **6:** the watering-can pour starts on "ถังน้ำ" (g 139).
- **14:** the model tank climbs over the groove during "ลุยข้ามไปได้" (g 366-396).
- **17:** the brush completes the stencil by g 480.
- **29+30:** the plate locks at g 882-895; rivets pop at g 902-918, one row per hammer strike.
- **31+32:** the tracks drop at g 918-933; set_drive scrolls them round at g 933-960.
- **33:** the sponson bolts on by g 978.
- **34:** the gun clunks home at about g 1005.
- **36:** the stencil goes on by g 1068.
- **39-59 crossing:** map set_crossing u continuously across rows 46, 47-49, 50 and 51:
  - u 0 at g 1396
  - nose lift from g 1424
  - grip at g 1493 ("เกาะขอบฝั่งโน้น")
  - u 1 at g 1558
  - Rows 52-59 use u = 1 (across), or the pose that their picture needs.
- **45:** set_steam puffs from g 1370.
- **52:** the wire flattens at g 1573.
- **53+54:** set_sparks over g 1605-1636.
- **56:** run_away25 for three different Germans.
- **60+61:** set_crate opens at g 1801.
- **68-70:** the take ends exactly at g 2092. No out-handle.

### Producer staging notes (still binding)
- **Hero crossing 47-49:** the tank fills 50-60 % of the frame width, side-on, with the sky behind the raised nose and the whole rhomboid visible.
- **Near grass:** ankle-to-knee height of a puppet, kept clear of the tank silhouette.
- **Tail wheels:** always attached visibly to the tank's rear.
- **Crane loads:** hang on visible chains.
- **No text anywhere:** the chalk drawing and the chart table carry lines only, and every stencil is the silhouette.

## Animation: NOT STIFF (client note, 28 Nov; binding for every shot)
- **Show the action happening in shot, never only the finished result.**
  - The plate swings in on the crane and lands with a small bounce.
  - Rivets pop in one by one, each on a hammer strike.
  - The track wraps round, links scrolling.
  - The gun slides in and clunks.
  - The brush moves and the stencil appears stroke by stroke (set_stencil fractional, keyed to the brush tip).
  - The watering can tilts and the water streams.
  - The model tank slides over the groove.
- **Characters change pose or expression at least once per phrase.** Use:
  - pose swaps (e.g. laugh/laugh_b, rivet/rivet_strike)
  - head turns (yaw)
  - blinks (blink_at)
  - gaze shifts
  - squash on landings and strikes (squash 0.92→1.05→1.0 over 4-6 frames)
  - secondary motion: flag wave t, a hanging toy tank swing, medals jiggle via the laugh bounce
  - Nobody holds one identical frame for more than about 12 frames unless the beat is a deliberate deadpan (shot 27).
- **Camera:** a slow drift, pan or push-in on most shots, eased and smooth.
  - Follow the action where it moves: pan with the plate, slide with the track.
  - No shake; qa_jitter must pass.
  - A static wide is allowed for at most 1 s.
- **Close framing:** the camera stays close (waist-up or tighter) on characters, as in the C/M rows. Widen only where the plan says W.

## Close-shot composition (producer, R11 comparison; binding)
- **SIMPLE BACKDROP behind every C and close M shot,** so the figure pops:
  - plain riveted hull plate
  - a brick wall
  - a canvas tent
  - sandbags
  - open sky
  Never put scaffolding, bunting, prop clutter or rows of clouds behind a close character. Keep busy detail for W shots. Use the set's `*_close_*` presets, or aim your own camera at a plain surface; you may hide clutter at runtime from shot.py.
- **Size:** in C shots the character's head is about 1/3 of the frame width. The camera is about 2.5-3.5 D from the card at about 40 mm, the waist is at the frame bottom, and the head stays above y 880.
- **Light:** puppets carry cast25 form shading, fabric texture and a key-side rim (pose keys `light25` and `rim25`). Set `light25` to match the sun side of your shot, so the rim faces the key.
- **Sky:** real neutral daylight; clouds varied in size and spacing, never a repeated pattern.

## Vivid = large areas of pure hue (client: "theirs is much more vivid"; binding)
- **Large pure-hue area:** every C and M shot has at least one large area (≥ 15 % of the frame) of pure, clean hue. Pick from:
  - clear saturated blue sky
  - red brick wall
  - the general's scarlet (cap band, collar tabs, sash)
  - green field
  - a yellow-ochre or teal canvas or tarp
  - red poppies
- **Close-shot backgrounds:** in close shots the khaki and brown tank sits against blue sky or green field, never against brown mud.
- **Pure hues:** no earthy mixes behind characters.
- **Per-take metrics:** every take must PASS light_metrics.py, which now also checks:
  - colourfulness M ≥ 65
  - |mean a*| ≤ 4 and |mean b*| ≤ 4
  - sat p98 ≥ 0.85
  - warm ≥ 40 % and blue ≤ 45 % of the coloured pixels
- **Colour grade:** grade only through the set's post(). Faces stay #fef7f6 and nothing clips.

## Camera moves (producer spec from R11 measurements; binding)
- **Every shot moves deliberately.** No locked-off frames, except one deadpan beat of at most 0.5 s (row 27).
- **Dialogue and reaction close-ups:** push in or pull out 8-15 % scale across the shot (about 0.3-0.5 % per frame), eased, sometimes with a slight arc.
- **Action shots:** the camera FOLLOWS the action at 20-35 % of frame width per second, leading the subject.
- **Accent beats:** a PUNCH-in of 15-25 % over 6-8 frames, or a smooth WHIP out into the next cut.
- **Per-shot moves:** the table "Camera move per shot" in shot_plan_v2.md gives each row's move. Follow it.
- **Smoothness:** smooth splines only. qa_jitter must pass: smooth intentional motion is fine, frame-to-frame wobble fails.
- **Log it:** in each take's QA.md, record the move type and the measured amount (scale % and pan % of width per second).

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
