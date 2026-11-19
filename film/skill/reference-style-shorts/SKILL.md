---
name: reference-style-shorts
description: Produce a short narrated animated clip (vertical 9:16, about 60 seconds) that looks, sounds and tells its story like reference clips the user provides - script on the reference's story formula (Thai tested), timed narration and captions, flat 2D puppets in a lit 3D Blender world, shots made by a team of cheaper models, conform, mix, review, grade. Holds a detailed style bible (camera angles, colours and light, sets, scene tricks, characters, captions and sound, the first film shot by shot) and tested example shots, so a new conversation can make a clip in the same style at once. Use this skill whenever the user sends a video and asks to "make a clip like this", "ทำคลิปแบบนี้", "ทำให้เหมือนคลิปที่ส่ง", wants a story short in the style of a channel, asks why a made clip does not look like the reference (colour, light, depth, camera angle, story), or wants to continue, fix, re-voice, polish or extend a clip made with this pipeline, even if they never mention Blender, animation or a pipeline.
---

# Reference-style shorts

A user sends one or two short clips and says "make me one like this". This skill is the method that got from a 50 percent look-alike to a finished 65 second film that measured inside the reference range on light and colour, plus the working code, specs, briefs, team templates and a style bible from that production. Its purpose is to let you skip the expensive part: discovering what the reference actually is and how to run the production.

Reply to the user in their language. Everything below is written for you, not for them.

## Fast path: a new clip in this same style

The analysis of the reference style is done: the style bible (`references/bible/`, index `references/bible/README.md`) holds every number, name and recipe, and the style card below holds the forty that matter most. Do not re-measure the reference, rebuild the puppet, staging, camera or light systems, or redesign the grade. Re-measure only if the user's new references are a different style (`references/analysis.md`, "Is the new reference the same style").

**The first hour** (tested on a fresh project; `<skill>` is this folder, `<PROJ>` your new project folder):

```sh
python3 <skill>/scripts/bootstrap.py <PROJ> --uploads <folder with the reference clips>
#   under 1 s: "project ready at <PROJ>: N files written, 0 kept as they were"
sh <skill>/scripts/check_env.sh <PROJ>
#   one line per need: "ok ..." or "MISSING <what> -> <how to install>" (bpy, ffmpeg with libass, numpy/Pillow/cv2,
#   fontTools, Playwright with NODE_PATH, Loma and DejaVu fonts, the Kanit fonts under <PROJ>/fonts, fal.ai)
cd <PROJ> && sh examples/setup_kit.sh
#   about 80 s, about 150 MB: texture caches in order (office, paper artwork, grey/storm skies, hi-res map, beach, kitchen);
#   ends "kit ready in <PROJ>. Next: cd examples && python3 smoke.py"
cd examples && python3 smoke.py
#   about 45 s: probe and three 360x640 drafts of each of the five example shots;
#   ends "smoke: ALL PASS -> smoke.json, smoke_sheet.jpg"
```

Look at `smoke_sheet.jpg`. If a line says MISSING or the smoke test fails, fix the environment before anything else (`references/environment.md`, `references/bible/kit-quickstart.md` section 5). While the setup runs, send the user the questions of step 1 below.

**From the request to the delivered file** (chapter = `references/bible/<name>.md`):

| # | Step | Read | Tools | Show the user |
|---|---|---|---|---|
| 1 | Ask, in one message: narration language and voice, paid services and spending, who makes the music, length | "Before you start" below | | the questions |
| 2 | Confirm the references are this style (six-row check) | `references/analysis.md` | `v3/tools/hue_report.py`, `v3/shots/qa_parallax.py` | which rows match; film 1 frames (`assets/bible/film1_shots_1.jpg`, `assets/bible/film1_shots_2.jpg`) as "the style I will build" |
| 3 | Story and script on the 12-element formula; two texts per sentence (`tts`, `captions`) | `references/story-formula.md`, captions-sound 4.1 | `workflows/05_script_by_formula.js`, the caption checker recipe in captions-sound 4.1 | the script with the formula elements, fact and dramatisation lists |
| 4 | Narration with timestamps, verified by transcription | `references/audio.md`, captions-sound 2.2 | `audio/build_narration.py ... --dry-run`, then for real (paid) | two or three voice samples first; then the narration and its cost |
| 5 | Shot plan against the narration clock | film1-shots 3 and 5.3, camera 4.1, scene-tricks 4, characters-acting 4 | `workflows/06_director_shot_plan.js` | the plan table (shot, time, set, framing, move, gag, transition) |
| 6 | Sets and cast for the new story: re-dress or build, light, check the hue | sets 8 and 9, colour-light 5, characters-acting R7, camera 2.2 | `workflows/08_assets_second_set_and_cast.js`, `hue_report.py` | stills of every set from its named cameras, with the hue row |
| 7 | The opening 5 s, complete with voice, captions, effects and music if any | kit-quickstart 3, camera recipes, characters-acting R1 to R5, scene-tricks 5 | `examples/<family>/shot.py` copied per shot, `examples/film_mini.py` | the clip and a side-by-side sheet; settle caption size (fs88 or fs72), the voice and every recurring design choice |
| 8 | All takes in lanes, swept after every lane | `references/production.md`, `references/team-and-models.md` | `workflows/11` to `13`, `scripts/sweep_takes.py`, `scripts/watch_prod.sh` | contact sheets per lane as they finish |
| 9 | Conform (every join type), captions, mix, independent review: version 1 | kit-quickstart 4, scene-tricks 2.1, captions-sound 2.4 to 4.5 | `examples/film_mini.py conform`, `captions --style th88\|th72\|en`, `mix`; `v2/eval/score.py` | version 1 with the review's list of what still differs |
| 10 | Polish: grade, story overlays, mix fixes, two reviews: version 1.1 | `references/polish.md`, colour-light 3 | `examples/film_mini.py grade [shots.json]` then `captions ... --frames graded`; `workflows/14_polish_pass_v1_1.js`. grade.py's TAKES/JOINS/SHOT/FOG are film 1's: never run grade.py or `make_sharp.py` (film 1's SRC, ASS, N=1965, OUT written in) on a new film | version 1.1 with the reviews' remaining list |

A new story needs its own sets and cast; the bundled office, beach and kitchen are film 1's and can be re-dressed (sets 8). Paid services (speech, effects, stems) stay in the main conversation; report spending as you go.

## The style card

Every value is copied from a chapter; the chapter has the source and the reference measurement beside it.

**Picture and rule.** 720x1280, 30 fps, about 65 s. Flat unlit 2D puppets on emission cards in a real lit 3D set. **Sharp picture, no depth-of-field or background blur; motion streaks on fast moves stay** (the set streaks on frames over 60 px/frame at the corners, characters never). Depth comes from real 3D parallax, cast shadows, overlap and light.

**Camera** (camera.md)
- Lens: 22 mm on a 36 mm sensor, 782.2 px focal length, 49.4 deg horizontal, 78.6 deg vertical field of view; roll 0. A head 1 D wide at depth z is 782.2 / z px.
- Low: camera 1.2 D above the floor, pitched up 13.5 to 16.5 deg. Eye: head centre + 0 to 0.3 D, 1 to 3 deg down. High: 3.3 to 4.4 D up, 20 to 25 deg down. Inserts rake across props from 0.4 to 1.9 D.
- Head width (outer D): extreme close 390-440 px (1.8-2.0 D away), close 300-350 (2.2-2.6 D), medium 170-230 (3.4-4.6 D, the default), wide 110-135 (5.8-7.1 D), establishing 30-75 px.
- Head centre y 450 to 760 (0.35-0.59 H); every whole head above y 880; caption band y 880-950 free of heads and picture text.
- Two-shot in depth: near head 1.36 to 1.46 x the far head, lower, 1.0 to 1.4 D nearer.
- Framing changes (cuts, dissolves and snaps together) every 1.2 to 1.5 s on average; aim at 1.3 to 1.4 s (film 1 ran 1.06 s). Any single interval 0.6 to 1.6 s.
- Never parked: at most 6 frames under 0.25 px/frame; never constant speed; every move eased.
- Drift: 6 to 10 %/s push or pull, 20 to 60 px/s slide, dying out before the shot ends. Snap: 13 to 25 frames, x1.3 to x3, peak speed 1.6 to 1.9 x the mean; about one snap per shot (18-24 in 65 s; A 36, B 22); snaps fill 17-44 % of the time.
- Shots: 18-22 shots, mean 2.8-3.2 s (reference A 16, mean 3.75 s; B 22, 2.62 s; film 1: 26, 2.52 s, too busy).
- Angle shares of screen time (reference): eye 35-40 %, establishing or vista 15-25 %, inserts at most 27 % (warm material objects, not flat diagrams), low 5-10 %, high 7-10 %, top-down at most one shot. Film 1 over-used low (23 %).

**Colour and light** (colour-light.md)
- Palette by role (reference, displayed): walls warm crimson and terracotta `#561e37`, `#5e2221`; floors navy `#152a63` to `#17153a` or wood `#ac825e`; wood `#976c4d`, wainscot `#491309`; cloth reds `#a1001c` to `#da0045`; metal gold `#cb9f48`; day sky `#4a78cd` to `#92b7e7`; paper cream `#fcf4e1`, never white; lamp core `#fffeec`.
- Characters: head fill `#fef7f6`, crescent `#e9dceb`, plum ink `#3a2832`; unlit, cast the sun's shadow, never bloom.
- Large surfaces are saturated mid-darks (S 0.45-0.9, V 0.30-0.75); nothing large paler than V 0.80 except sky.
- Hue band (share of chroma, `hue_report.py`): red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10 %; sat 0.38-0.48; val 0.45-0.63; dark (V < 0.25) 8-15 %. Exteriors, map close-ups, night and storm may leave it: say why.
- Key: one hard Sun, 0.45 to 1.5 deg; office day KEY (2.30, 1.65, 0.74), from camera-left. Ambient as emission, office day SHADE (0.20, 0.27, 0.54), tinted per surface. Shade hue 240-260 (reference shade `#332d40`, `#525065`), shade 0.15-0.31 of lit, cast-shadow edge 4-21 px.
- Only real emitters exceed scene-linear 1.0 and bloom (halo 12-24 px). Black point luma p1 0.08-0.12; no grain, no sharpening, vignette at most 5 %.
- Finish with the v1.1 grade: one S-curve, saturation 1.18, bloom on hot sources, red and white protection, soft ceiling 0.985. Run it as `examples/film_mini.py grade`: grade.py's TAKES/JOINS/SHOT/FOG are film 1's; replace them or use film_mini.py grade.

**Sets** (sets.md)
- Real geometry, 1 unit = 1 D. Depth layers: a dark foreground in shade within the nearest 15 % of the frame, the lit subject band, then a far wall or horizon.
- Dress where the cameras look: interior wide 20-26 distinct objects, exterior 12-18. At least one emitter in frame.
- Man-made props have thickness and a 3 px inverted-hull ink (hull = 0.00384 x camera distance in D); never ink sky, sea, sand, fog, grass or rain.
- Interior zones top to bottom: ceiling 0-18 %, upper wall 18-45, dark wainscot 45-66, floor 66-100; warm reds, browns and gold, one navy block on the floor.
- Seams and detail lines at 0.65-0.70 of the surface; plank widths 0.16-0.28 D. One or two legible text lines per prop, the rest greeked; no text in the caption band.
- Brightness (0-255): top eighth 40-90, brightest middle band 105-150, bottom eighth 30-70. Sun 35-50 deg up.

**Characters** (characters-acting.md): about 3 D tall; one torso shape, constant-width limbs, no neck; faces swap whole drawings on the closed frame of a 3-frame blink, never tween; only the quoted speaker moves his mouth (a new drawing every 2 to 6 frames, from narration loudness); listeners freeze; one gesture per shot on the caption word; no back views; set `head_flip` so the crescent and thick ink sit away from the key.

**Scene tricks** (scene-tricks.md): joins are smoothstep dissolves (81 % in the reference; 11 frames default, 9 for continuity, 13 to 17 for a change of place or time); special joins once each: 1 to 3 hard cuts on punch lines, 1 whip, 1 object wipe, 1 white flash, 1 punch-in with speed lines. Overlays only from the fixed list (sweat drop, purple face with steam, tears, sleep Z, hair on end, focus lines, eye glint, brightness dip), 1 to 4 places each; never impact stars, speech bubbles, question or exclamation marks, note glyphs. Shake on 1 to 3 shots at most. Props change state on the beat word, one sound each.

**Captions** (captions-sound.md): one line, white fill, 4 px black stroke, centred at (360, 900); Thai in Kanit Black `{\fnKanit Black\fs88}` (45 px text height; offer fs72, 37 px); English Work Sans Black `{\fnWork Sans Black\fs58}` (36 px, the reference size, measured); 4 to 14 Thai characters or 1 to 3 English words per phrase; times from `narration_timing.json` plus 0.100 s; each holds until the next; hard swaps, no animation; burned last with `assemble.py ... 30`.

**Sound** (captions-sound.md): voice wall to wall, laid at +0.100 s, first word by 0.12 s, no gap over 0.30 s (reference pace 3.3 to 3.6 English words/s; film 1's Thai: 313 syllables in 65 s at speed 1.2 and tempo 1.19), active RMS -17.4 dBFS. Music bed -38 dBFS RMS from the first frame, no drums. Point effects one every 2.3 to 3 s, peak at most -11 dBFS; ambience beds -34 to -30 RMS, peak at most -14; nothing but the voice over -10 dBFS peak while the voice speaks, effects and music counted together.

**Story** (`references/story-formula.md`): the 12 elements; the hook is one sentence of 3 to 7 s; first quote by about 30 %, nickname at 37-48 %, the turn at 51-71 %, the disaster at 71-91 % of the runtime; the nickname at least at the naming and in the second quote; only the quoted lines move a mouth; no casualty figure, no moral; end on an image. Size: 214-235 English words, or about 290-315 Thai syllables, in 60-65 s.

**The film clock** (film1-shots.md): a shot boundary at narration time t is film frame round(t x 30); an event inside a shot at narration time x is frame round((x + 0.1) x 30); takes carry handle frames (half the dissolve plus 2) on each dissolved side.

## This client's rules override the style card (films 2-17, Thai channel)

Read `references/production-lessons.md` before anything else when continuing this client's series. It records what the client decided across films 2-17. Where it disagrees with the style card or the bible, the lessons win. The main overrides:
- **Voice.** ElevenLabs v3 "Bankky" via fal.ai at its ORIGINAL setting: speed 1.15, default stability, atempo about 1.134. Not expressive.
- **Captions.** Kanit Black fs88, one phrase at a time, at y 900.
- **Music.** The client makes it in Suno: give him Styles/Exclude text. Mix it at -31 dB RMS under the voice at -14.4, not -38.
- **Sets.** Build a NEW set for every film. Agree the look in one round with a 2-3 still style board. Ask before rendering: show the set and cast sheets and wait for an explicit OK.
- **Look.** Sharp, wide and dense, with a beautiful lit set. No extreme close-ups, no text signs, no flat 2D diagrams; the reveal happens inside the 3D world. Water must be rich but not blurry; use period-correct colours.
- **Camera rhythm.** Use film 2 (ไม้จิ้มฟ้า) as the target (§10): a clear push or pull every shot, dissolves between places and times, foreground props, and median in-shot frame-diff ≥ 4. This matches this card's drift and snap numbers; use them.
- **Facts.** Web-search the facts before writing and list them in FACTS.md. Invented parts must not contradict checkable facts; comic invented endings are fine.
- **Stricter QA.** Use film/QA_TEAM.md: every-frame qa_auto, QA-tech at 6 fps, QA-art on key takes, a 4-reviewer final gate, no solo overrides.
- **Production.** Render teams run on Sonnet. Run 4 films in parallel, one director chat each, per film/HANDOFF.md. Directors keep a 60-min self-check. Releases go to film/POST_QUEUE.md as WAIT, because the client posts himself.

## The style bible

| Chapter | Answers | Read it when |
|---|---|---|
| `references/bible/README.md` | which chapter, in which order, for each job | first |
| `kit-quickstart.md` | what ships, the clean start, the five example shots, a worker's commands, takes to a film | the first hour; before any shot |
| `camera.md` | lens, heights and pitch, shot sizes, move speeds, every named camera, all 26 shots as camera data, recipes | planning shots, staging a shot |
| `colour-light.md` | palette, hue band, light presets with every parameter, materials, costume colours, the grade, per-shot hue | building or lighting a set, checking colour, grading |
| `sets.md` | the four places with coordinates, marks, cameras, signs, setters; caches; re-dressing; a new set | choosing or building sets |
| `scene-tricks.md` | joins, overlays, gimmicks, character effects, streak, shake, callbacks, dosage | planning devices per beat, staging gags, the conform |
| `characters-acting.md` | puppet design, expressions, mouths, the cast, the acting library, recipes | casting, acting a shot, adding a character |
| `captions-sound.md` | caption rules and burn, narration, film clock, mix spec, effect library, levels | script captions, narration, mixing |
| `film1-shots.md` | film 1 shot by shot, the edit against the reference, callbacks, ranking | writing a shot plan; looking for a worked example |

## The idea that makes it work

**Measure the reference, then build to the numbers. Never guess the technique.** The first production failed twice by guessing:

| Attempt | What was built | Why it did not look like the reference |
|---|---|---|
| 1 | Lit 3D characters in a plain 3D room | The reference characters are flat, unlit 2D drawings. Lit spheres read as plastic. The room was pale and empty. |
| 2 | 2D puppets on a flat painted set with 2D zoom and pan | Characters matched, but there was no light direction, no cast shadow, no perspective, one camera angle. The user named it at once: light, depth, camera angle. |
| 3 | The same 2D puppets as unlit cards standing in a real, lit 3D set | Matches: hard key light with cast shadows, real parallax, low, eye and high camera angles. |

The reference style this pipeline reproduces is therefore: **flat unlit 2D puppet characters inside a real 3D world lit by one hard key light that glows, shot with a restless wide-lens camera in a sharp picture whose depth comes from parallax, cast shadows and staging, narrated wall to wall, with burned-in word captions, a quiet music bed and frequent sound effects.** If the user's references are a different kind of film, the analysis phase will tell you; keep the method and change the build.

## Before you start

1. **Ask the user early, in one message, and keep working while you wait:** narration language and voice; which paid services they have (fal.ai, ElevenLabs, Suno, others) and whether you may spend on them; whether they make the music themselves; how long the clip should be. In the first production the language was assumed to be English and the whole narration had to be redone in Thai.
2. **Set up the project** with the four commands of the fast path. `bootstrap.py` unpacks `pipeline/` (working code, measured specs, fonts, briefs, example takes, the five example shots, plan and script) and replaces the placeholders `__PROJ__`, `__SCRATCH__` and `__UPLOADS__` with your paths. `check_env.sh <PROJ>` checks the machine; `examples/setup_kit.sh` regenerates the texture caches the skill does not ship (without it the office shows magenta placeholder cards and grey or storm light fails); `examples/smoke.py` proves a draft of every set family renders. The workflow templates in `workflows/` carry the same `__PROJ__` placeholder: replace it before you run one. **The briefs, workflow prompts, `shots/film.py` and the example takes `v3/film/sNN/` are film 1, filled in, not templates**: start a new film's briefs from `pipeline/v3/film/*.template.md`, new shots from `pipeline/examples/<family>/shot.py`, and rewrite each workflow's prompts (per-file list: `references/production.md`, "Adapting to a new film"). The watch scripts read `PROJ` and `WF_DIR` from the environment. Network and key steps for a cloud container: `references/environment.md`.
3. **Plan the team before spending tokens:** read `references/team-and-models.md`. Discovery and taste need the strongest model; building to a measured spec does not.

## The workflow

Each phase ends with something you show the user. Do not run phases ahead of feedback you have not received on the look: the first production lost hours building on a look the user had not seen.

### 1. Analyse the references (only for a new style)
For this style the analysis is done: run the six-row check in `references/analysis.md` ("Is the new reference the same style"); four or more rows match, the characters among them, and you reuse `pipeline/spec/` and the bible. For a new style: extract full-resolution frames every 0.5 s plus bursts of consecutive frames, read the burned-in captions, transcribe, find every cut, then measure through lenses, one analyst each, and reconcile: characters, faces, colour and light, environments, camera and edit, captions, **sound**, and production forensics. Look at full-resolution frames yourself first; a contact sheet at thumbnail size hid the fact that the characters were 2D. Details and the lens briefs: `references/analysis.md`.

### 2. Story and script
The user will compare the story as well as the picture. Extract the reference's beat sheet and write the new script against it element by element (the first production found 12 elements; the first script matched only 7 and the user noticed). Three writers with different methods, three judges, one editor, one adversarial check. Deliver two texts per sentence: what the voice says, and the caption phrases. `references/story-formula.md`; caption rules and a checker: `references/bible/captions-sound.md` 4.1.

### 3. Sound first
Record the narration before any animation and cut the picture to it. Generate speech with character timestamps, verify it by transcribing it back, tighten the pauses to the reference's pacing, and derive caption timing from the timestamps. Measure the reference's music bed and effects instead of assuming there are none. Tool: `pipeline/audio/build_narration.py <script.json> <voice_id> <out_dir>` (`--dry-run` first shows the characters you pay for). The skill ships no sound files: narration, effects and music are made for each film. `references/audio.md`.

### 4. The look: puppets in a lit 3D world
Characters are procedural SVG puppets (`pipeline/v2/puppet`, cast `v3/cast`, acting `v3/acting`) on emission-only cards in a Blender scene: they cast real shadows and are never lit. Sets are real geometry built from code with SVG artwork as textures (`pipeline/v3/set3d` and its extensions), one hard key light, an ambient term that turns shade blue-violet, a 22 mm camera at low, eye and high angles (`pipeline/v3/stage`). Bloom on light sources, a gentle S-curve and distance haze belong in the look from the start, and so does depth through staging (a dark foreground layer, two-shots in depth, a far wall or horizon). A new story needs its own sets and cast: one builder and one reviewer per set, with the acceptance list in `references/bible/sets.md` 9.2. Check colour with the hue tool before showing anything. `references/look.md`; what to build in from the start: `references/next-film.md`; every value: the bible.

### 5. Prototype the opening and show it
Make the first 5 seconds complete, with voice, captions, music (if the user's track is not there yet, send it without a bed and say so) and effects, and send it with a side-by-side sheet against the reference per aspect the user cares about (light, depth, camera angle, colour). Ask what still looks different. Fix at the source (the set, the puppet, the script), not with a grade on top, because every later shot inherits the fix. **Settle every visible design choice here**: show both variants of anything that recurs, the caption size and the voice, and get one answer before any take is rendered. Build the shots from `pipeline/examples/<family>/shot.py` (`references/bible/kit-quickstart.md` 3) and join them with `examples/film_mini.py`; `pipeline/v3/shots/film.py` is film 1's opening as a further example (`pipeline/v3/README.md`).

### 6. Plan every shot
Three directors plan the whole film against the narration timing (one mirrors reference A's shot grammar, one mirrors B's, one is the leanest faithful plan), judges score fidelity, feasibility and story clarity, a director merges, a checker verifies coverage and counts the grammar against the measured numbers. The plan names sets, cast, props, transitions and sound cues, and keeps heads and text in the picture out of the caption band. Example: `pipeline/plan/shot_plan.md` and `references/bible/film1-shots.md`. Template: `workflows/06_director_shot_plan.js`.

### 7. Produce the takes in lanes
One folder per take, one owner per folder. Every shot worker reads one shared brief and the conventions file (templates: `pipeline/v3/film/BRIEF_SHOTS.template.md`, `CONVENTIONS.template.md`): the clock, the folder layout, what a finished take is (frames with dissolve handles, `meta.json`, `cues.json`, `contact.jpg`, `QA.md`), the colour band, the hard rules, the client decisions. A worker's prompt only names its lane, shots and folders. Lanes group shots that share marks, cameras and sprites; two workers at a time per workflow on 4 cores, up to three workflows side by side. Every worker stages with numbers (`probe`), drafts small, looks at a contact sheet, starts the final render detached and resumable, and stages its next shot meanwhile. Sets, cast and props grow only through extension modules (`pipeline/v3/set3d_ext/`).

In the main loop, after every lane result:
- **Sweep.** Read the workflow journal (`journal.jsonl`), not the summary line. For each take with `complete: false`, wait for its render, run the take's own post, contact, qa and QA.md commands, and look at the contact sheet. `scripts/sweep_takes.py` lists what needs it. In the first film two workers returned early, leaving four takes with their renders still running.
- **Extra lanes without stopping anything.** To pull shots forward that a running workflow will also hand out, add the claim rule to the shared brief, create their folders with a `CLAIMED.txt` naming the new lane, and start a second workflow. The later worker finds them claimed and returns at once.
- **Watch for stalls** with `scripts/watch_prod.sh` (set `FILM` and `REVIEW` to your delivery file names) and check the age of each worker's transcript. Where the run folders and journals live, and how to resume a run: `references/production.md`.
- **Re-voice without touching the picture** if the voice must change: `pipeline/audio/th/build_narration_fit.py` fits every new sentence into the old sentence's slot (edit its film-1 sentence groups first); only lip-synced shots are rendered again.

The finished run: 23 takes, about 4 hours with 4 to 5 workers, most of it rendering 2,120 frames (with dissolve handles) at about 8 to 11 frames a minute. Details, restarts and templates: `references/production.md`, `workflows/11_*` to `13_*`.

### 8. Conform, mix, review, deliver version 1
Join takes with the planned transitions from their handle frames (`pipeline/examples/film_mini.py conform`; `pipeline/v3/film/out/conform.py` is film 1's, with its take list and overlays written in), burn captions last (`film_mini.py captions`, which calls `pipeline/assemble.py ... 30`; `assemble.py` reads `f_%04d.png`, so link `g_` frames to that name), mix from the takes' cue lists to the measured levels (`film_mini.py mix`, `pipeline/audio/mixer.py`; check with the mix-check recipe in `references/bible/captions-sound.md` 4.4). An independent reviewer measures the film with the analysis tools, checks the story with the sound off, and ranks what still differs by how much a viewer would notice (`references/examples/QA_film.md`). **Read the out-of-range rows and the side-by-side frames, not the likeness index**: v1 scored 0.980 while the light was visibly off. Send version 1 to the user at once with that honest list. About 35 minutes.

### 9. Polish as a separate version
Build version 1.1 without touching version 1 or rendering again (`pipeline/v3/film/BRIEF_POLISH.md`, `workflows/14_polish_pass_v1_1.js`). The polish pass is the grade, the story overlays, the corrected mix and the two reviews:
1. A grade on the v1 conform frames before the captions (`out_v11/grade.py`, `GRADE.md`): per-shot corrections cross-faded over dissolves, S-curve, saturation lift, bloom on light sources, story overlays (film 1: a fog bank), protection of reds and white fills.
2. The same captions burned last and the frames encoded in the same pass, without intermediate files (`out_v11/make_sharp.py` is the example); the same mix with the review's corrections (`out_v11/sound/build_v11.py`).
3. Two reviewers in parallel: one compares the look with the reference again, one hunts for artifacts and assumes something is broken. One fix round, then a re-check. The look reviewer saw one 4-frame ghost face; the artifact hunter measured that the bloom greyed the ink in every face: always run it.

Result in the first film: index 0.980 to 0.993 (delivered sharp v1.1), all five light rows inside the reference range, the cold sequence warmed. The delivered v1.1 is `deliver/film_v1_1_sharp_thai.mp4` (sharp v1 picture, v1.1 grade, captions and sound). Film 1's first v1.1 also added a background blur the client had not asked for and had removed: add no new kind of effect in a polish pass without showing it on one shot first. Details and pitfalls: `references/polish.md`; the v1.1 review: `references/examples/QA_film_v1_1.md`.

## Working as a team without burning the limit

The costly part of the first production was discovery on the top model: about 3.4 million subagent tokens to measure the look, 3 million to plan the shots. Building to the resulting specs is cheaper work. Use this split, and pass the model explicitly in each agent call:

| Work | Model tier |
|---|---|
| Judging likeness by eye, creative direction, final review, talking to the user | strongest available |
| Building sets, cast, shots, colour fixes, the grade, and reviews that have numeric acceptance bands | one tier down: `model: 'opus'` in every template |
| Running renders, sweeping unfinished takes, assembling, mixing, file handling, scripted checks | cheapest that follows a procedure: `model: 'sonnet'` (not tried in a workflow in film 1; example in `references/team-and-models.md`) |

A colour correction with a numeric target band took one one-tier-down worker one pass and about 260 thousand tokens; all production lanes and the polish pass ran one tier down. Cheaper workers succeed when the brief contains a measurable band and the tool that measures it, and the bible chapter that holds the values; they drift when the brief says "make it look right". Give workers one shared brief and short prompts, take results as schemas with a `complete` flag, run every review with two lenses (likeness, and a hunt for what broke), and keep paid services in the main conversation so spending is counted.

Token figures, wall times and the reusable workflow scripts: `references/team-and-models.md` and `workflows/`.

## Reporting to the user

- Send something visible at every phase: a still, a sheet, a clip. Users redirect far better from a picture than from a description.
- Say what you verified and how. You can measure audio but you cannot hear it: say so and ask the user to listen for the things only an ear can judge (voice speed, music fit, effect loudness).
- State spending on paid services as you go, and say when a figure is your estimate. To quote a cost before you start, take film 1's usage in `references/audio.md` (characters of speech, speech-to-text checks, seconds of effects) times the provider's current prices, which the skill does not record.
- Before you say work is running in the background, check that it is actually moving (see pitfalls). Before you call something like the reference, put it next to the reference.
- Deliver each version with the review's list of what still differs, and say which items the next version will address.

## Hard rules

- Sharp picture, no depth-of-field or background blur; motion streaks on fast moves stay. Depth comes from real 3D parallax, cast shadows, overlap and light.
- Characters are never lit, shaded, blurred or streaked; faces never tween.
- Keep the caption band (y 880 to 950) free of heads and picture text; captions are burned last.
- Do not reuse the reference's characters, text or frames. Match the style with your own cast, props and story; put only your own film's frames in sheets.
- Settle recurring design choices, caption size and voice on the opening, before any take is rendered.
- Paid services only from the main conversation, with the spending reported.

## Pitfalls that cost hours the first time

- **A design choice changed after production had started** (ruled line, then hand-drawn, then back): two restarts. Show both variants on the opening and get one answer before any take is rendered. If the narration describes the choice in words ("dead straight"), a changed picture leaves the words wrong: re-record those sentences or accept the mismatch knowingly. When a choice changes anyway, keep each variant behind a switch in the set file.
- **An effect the client did not ask for** (a 2D background blur in the polish pass) had to be taken out again. A review's list of differences from the reference is not an order: show a new kind of effect on one shot and ask.
- **Workers return early although told not to, and renders outlive them.** A detached render chain keeps running after its worker returns or is stopped, and a later worker may kill or duplicate it. Sweep after every lane, and have every worker check `ps` and the process folder before it renders.
- **Never message a running workflow worker.** A message to a worker's id starts a second copy of it from its transcript; the two fight over the same folder and can kill each other's renders. Stop, edit the shared brief, relaunch; or hand the shots to a new lane with `CLAIMED.txt`.
- **A user interrupt kills every background workflow**, and the task list still shows them. Ask the user not to press stop during production. After one, follow "Restarting" in `references/production.md`. Judge liveness by each agent's last activity, not by the list of names.
- **The machine may be temporary.** Send the user a source backup archive at milestones.
- **Skipped setup looks like a bad set.** Without `examples/setup_kit.sh` the paper props render as magenta placeholder cards and grey or storm light stops with a missing texture; film 1's take scripts read film 1's narration WAV, which is not shipped (pass `path=` to `acting.loudness`).
- **Colour drifts magenta.** A violet ambient plus pink walls gave 25 percent magenta against 5 to 10 in the reference. Shade must be blue-violet (hue 240 to 260); run `pipeline/v3/tools/hue_report.py` on every set. Inserts, night and storm shots may sit outside the band (say so), but do not let an explainer sequence go cold for 15 seconds.
- **The scoring tool is not a likeness judge.** `pipeline/v2/eval/score.py` scored the flat version 0.997 while light, depth and camera angle were plainly wrong, and the finished v1 0.980 with flat lamps. Use it to catch regressions and to read out-of-range rows, never as proof.
- **Bloom and grades damage ink** (glow inside faces greys the ink; a sunlit floor on the bloom threshold flickers; a lifted-shadow grade greys the characters' ink). The pitfalls of the polish pass and their fixes: `references/polish.md`.
- **Blender traps** (headless Freestyle aborts the process, stale sprite textures with persistent data, keyframe easing API, texture shimmer): `pipeline/spec/verify_blender_api.md` and `pipeline/v3/stage/REVIEW.md` list the ones already hit.

## What is bundled

| Path | Contents |
|---|---|
| `references/bible/` | the style bible: eight chapters and the index `README.md` |
| `assets/bible/` | the bible's picture sheets (film 1 frames and renders only) |
| `scripts/` | setup (`bootstrap.py`, `check_env.sh <PROJ>`), `sweep_takes.py` (takes a sweeper must finish), stall wake-ups `watch_prod.sh`, `watch_polish.sh` |
| `pipeline/examples/` | one tested shot per set family (office day, office grey or storm, beach, kitchen, map mechanism), `setup_kit.sh` (caches), `smoke.py` (smoke test), `film_mini.py` (takes to a captioned, mixed film), `common.py` |
| `pipeline/spec/` | the measured look specification (`LOOK_SPEC.md`), single-lens specs, verification notes |
| `pipeline/v2/puppet/`, `v3/cast/`, `v3/acting/` | the 2D puppet system, extra cast, the acting library (talk, walk, laugh, run, whistle stroll, shock, sleep, jump scare, nods, listeners, hand cards), with API docs |
| `pipeline/v3/set3d/`, `stage/`, `shots/`, `tools/` | the reviewed office set (with `review/`, the measuring module `qa_light.py` needs), the staging and camera system, film 1's 5 second opening with the QA tools, `hue_report.py` |
| `pipeline/v3/set3d_ext/`, `set3d_beach/`, `set3d_kitchen/`, `paper/` | set extensions (props, cameras, grey and storm light, map mechanism, beach props), two more sets, paper artwork |
| `pipeline/fonts/` | caption fonts (Kanit Black, Work Sans Black) and `th/` Kanit ExtraBold and Black for the paper artwork (SIL Open Font License, `th/OFL-Kanit.txt`) |
| `pipeline/v3/film/` | brief and conventions templates (`*.template.md`); film 1's filled briefs as examples; example takes s10 to s26 (scripts, meta, cues, QA; no frames) |
| `pipeline/v3/film/out/`, `out_v11/` | film 1's v1 conform, edit-grammar count, sound build; v1.1 grade (`grade.py`, `GRADE.md`), `make_sharp.py` (grade, captions and encode in one pass, no intermediate files), sound |
| `pipeline/v2/` (other) | the flat 2D compositor (inserts, artwork) and the scoring tool `v2/eval/` |
| `pipeline/audio/` | `build_narration.py`, speech and caption alignment (`audio/th/tts_fal.py`), film 1's opening timing file, re-voicing to an existing clock, effects builder, mixer (no sound files) |
| `pipeline/plan/`, `pipeline/script_th_v2/` | an example verified shot plan and formula-matched script |
| `workflows/` | the Workflow tool scripts of each phase, film 1's prompts in a reusable shape (11 to 13 production and finish, 14 polish) |

The references, and when to read each:
- `references/bible/README.md`: the style bible's index and reading order per job.
- `references/analysis.md`: phase 1, measuring the references, and the check whether a new reference is this style.
- `references/story-formula.md`: phase 2, the beat sheet and the script.
- `references/audio.md`: phase 3 and the mix, and when the voice changes.
- `references/look.md`: phase 4, characters, sets, light, camera, checking tools.
- `references/next-film.md`: before phases 4 to 6, what to build in from the start so it need not be repaired.
- `references/team-and-models.md`: before spending tokens, and whenever you start a workflow.
- `references/production.md`: phase 7 and 8, adapting the briefs and workflows to a new film, lanes, the sweeper, claim files, where workflow runs live, stalls, restarts, re-voicing.
- `references/polish.md`: phase 9, the grade, the overlays, the two reviews and their pitfalls.
- `references/examples/QA_film.md`, `references/examples/QA_film_v1_1.md`: when you write or brief a review; the two reviews of the first film (blur remarks taken out: sharp picture, client decision).
- `references/environment.md`: setup, network and keys, Blender traps, render budget.
