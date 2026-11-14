---
name: reference-style-shorts
description: Produce a short narrated animated clip (vertical 9:16, about 60 seconds) that looks, sounds and tells its story like reference clips the user provides. Covers the whole job - measuring the references, writing a new script on the same story formula (any language; Thai is tested), recording timed narration and captions, building flat 2D puppet characters inside a lit 3D Blender world, rendering, and mixing voice, music and sound effects - and how to run it with a team of cheaper models. Use this skill whenever the user sends a video and asks to "make a clip like this", "ทำคลิปแบบนี้", "ทำให้เหมือนคลิปที่ส่ง", wants a story short in the style of a channel, asks why a made clip does not look like the reference (colour, light, depth, camera angle, story), or wants to continue, fix or extend a clip made with this pipeline, even if they never mention Blender, animation or a pipeline.
---

# Reference-style shorts

A user sends one or two short clips and says "make me one like this". This skill is the method that got from a 50 percent look-alike to a clip the user called very good, plus the working code, specs and team templates from that production. Its purpose is to let you skip the expensive part: discovering what the reference actually is.

Reply to the user in their language. Everything below is written for you, not for them.

## The idea that makes it work

**Measure the reference, then build to the numbers. Never guess the technique.** The first production failed twice by guessing:

| Attempt | What was built | Why it did not look like the reference |
|---|---|---|
| 1 | Lit 3D characters in a plain 3D room | The reference characters are flat, unlit 2D drawings. Lit spheres read as plastic. The room was pale and empty. |
| 2 | 2D puppets on a flat painted set with 2D zoom and pan | Characters matched, but there was no light direction, no cast shadow, no perspective, one camera angle. The user named it at once: light, depth, camera angle. |
| 3 | The same 2D puppets as unlit cards standing in a real, lit 3D set | Matches: hard key light with cast shadows, real parallax, low, eye and high camera angles. |

The reference style this pipeline reproduces is therefore: **flat unlit 2D puppet characters inside a real 3D world lit by one hard key light, shot with a restless wide-lens camera, narrated wall to wall, with burned-in word captions, a quiet music bed and frequent sound effects.** If the user's references are a different kind of film, the analysis phase will tell you; keep the method and change the build.

## Before you start

1. **Ask the user early, in one message, and keep working while you wait:** narration language and voice; which paid services they have (fal.ai, ElevenLabs, Suno, others) and whether you may spend on them; whether they make the music themselves; how long the clip should be. In the first production the language was assumed to be English and the whole narration had to be redone in Thai.
2. **Set up the project:** `python3 scripts/bootstrap.py <project_dir> --uploads <folder with the reference clips>` unpacks `pipeline/` (working code, measured specs, example plan and script) and rewrites its paths. Then `sh scripts/check_env.sh`. Setup details and the network and key steps for a cloud container are in `references/environment.md`.
3. **Plan the team before spending tokens:** read `references/team-and-models.md`. Discovery and taste need the strongest model; building to a measured spec does not.

## The workflow

Each phase ends with something you show the user. Do not run phases ahead of feedback you have not received on the look: the first production lost hours building on a look the user had not seen.

### 1. Analyse the references (once per reference style)
Extract full-resolution frames every 0.5 s plus bursts of consecutive frames, read the burned-in captions, transcribe, find every cut. Then measure through lenses, one analyst each, and reconcile: characters, faces, colour and light, environments, camera and edit, captions, **sound** (voice pacing, music bed, effects), and production forensics (is it 3D, 2D, generated?). Look at full-resolution frames yourself first; a contact sheet at thumbnail size hid the fact that the characters were 2D. Details, commands and the lens briefs: `references/analysis.md`. If the user's references are the same style as the bundled specs (`pipeline/spec/LOOK_SPEC.md`), verify a few numbers and reuse them instead of re-measuring.

### 2. Story and script
The user will compare the story as well as the picture. Extract the reference's beat sheet and write the new script against it element by element (the first production found 12 elements; the first script matched only 7 and the user noticed). Three writers with different methods, three judges, one editor, one adversarial check. Deliver two texts per sentence: what the voice says, and the caption phrases. `references/story-formula.md`.

### 3. Sound first
Record the narration before any animation and cut the picture to it. Generate speech with character timestamps, verify it by transcribing it back, tighten the pauses to the reference's pacing, and derive caption timing from the timestamps. Measure the reference's music bed and effects instead of assuming there are none. `references/audio.md`.

### 4. The look: puppets in a lit 3D world
Characters are procedural SVG puppets (`pipeline/v2/puppet`), rasterised per frame and shown on emission-only cards inside a Blender scene so they cast real shadows and are never lit. Sets are real geometry built from code with SVG artwork as textures (`pipeline/v3/set3d`), one hard key light, an ambient term that turns shade blue-violet, a 22 mm camera at low, eye and high angles (`pipeline/v3/stage`). Check colour with the hue tool before showing anything: `references/look.md`.

### 5. Prototype the opening and show it
Make the first 5 seconds complete, with voice, captions, music and effects, and send it with a side-by-side sheet against the reference per aspect the user cares about (light, depth, camera angle, colour). Ask what still looks different. Fix at the source (the set, the puppet, the script), not with a grade on top, because every later shot inherits the fix.

### 6. Plan every shot
Three directors plan the whole film against the narration timing (one mirrors reference A's shot grammar, one mirrors B's, one is the leanest faithful plan), judges score fidelity, feasibility and story clarity, a director merges, a checker verifies coverage and counts the grammar against the measured numbers. The plan names sets, cast, props, transitions and sound cues. Example: `pipeline/plan/shot_plan.md`. Template: `workflows/06_director_shot_plan.js`.

### 7. Produce in lanes
One worker per take, each owning one folder, all following `pipeline/v3/film/CONVENTIONS.md`. Sets, cast and props are extended through extension modules, never by two workers editing one file. Draft at 360x640, render final only when the draft is right. A final 720x1280 frame costs about 18 CPU seconds, so 2,000 frames need about 2.5 hours on 4 cores: plan the order of renders around that.

### 8. Conform, mix, check, deliver
Join takes with the planned transitions, burn captions last, mix voice, music and effects to the measured levels (`pipeline/audio/mixer.py`), then check against the reference with the bundled tools and with your own eyes on full-size frames. Send the clip with an honest list of what still differs.

## Client-tested rules from films 2-9 (read first when continuing this client's series)

`references/production-lessons.md` holds what nine productions taught: the story formula measured on 8 hit shorts, the client's hard
rules (sharp picture, original wide dense look, reveal inside the 3D world, Bankky voice at the original setting, big phrase captions,
ask before rendering, never cut scenes silently), the render-team system, the re-cut technique, SFX ducking and the picture-QA gates.

## Working as a team without burning the limit

The costly part of the first production was discovery on the top model: about 3.4 million subagent tokens to measure the look, 3 million to plan the shots. Building to the resulting specs is cheaper work. Use this split, and pass the model explicitly in each agent call:

| Work | Model tier |
|---|---|
| Judging likeness by eye, creative direction, final review, talking to the user | strongest available |
| Building sets, cast, shots, colour fixes and reviews that have numeric acceptance bands | one tier down (Opus class) |
| Running renders, assembling, mixing, file handling, scripted checks | cheapest that follows a procedure (Sonnet class) |

A colour correction with a numeric target band was done in one pass by an Opus-class worker for about 260 thousand tokens. Cheaper workers succeed when the brief contains a measurable band and the tool that measures it; they drift when the brief says "make it look right". Rules, token figures and the reusable workflow scripts: `references/team-and-models.md` and `workflows/`.

## Reporting to the user

- Send something visible at every phase: a still, a sheet, a clip. Users redirect far better from a picture than from a description.
- Say what you verified and how. You can measure audio but you cannot hear it: say so and ask the user to listen for the things only an ear can judge (voice speed, music fit, effect loudness).
- State spending on paid services as you go, and say when a figure is your estimate.
- Before you say work is running in the background, check that it is actually moving (see pitfalls). Before you call something like the reference, put it next to the reference.

## Pitfalls that cost hours the first time

- **Background work can die silently.** A user interrupt or an idle session stops background agents; the task list still shows them. Check the age of each agent's last activity, not the list of names. After a restart, files survive but running work does not: resume workflows from their run id.
- **The machine may be temporary.** Send the user a source backup archive at milestones.
- **Colour drifts magenta.** A violet ambient plus pink walls gave 25 percent magenta against 5 to 10 in the reference. Shade must be blue-violet (hue 240 to 260). Run `pipeline/v3/tools/hue_report.py` on every set.
- **The scoring tool is not a likeness judge.** `pipeline/v2/eval/score.py` scored the flat version 0.997 while light, depth and camera angle were plainly wrong, because it does not measure them. Use it to catch regressions, never as proof.
- **Blender traps** (headless Freestyle aborts the process, stale sprite textures with persistent data, keyframe easing API, texture shimmer): `pipeline/spec/verify_blender_api.md` and `pipeline/v3/stage/REVIEW.md` list the ones already hit.
- **Do not reuse the reference's characters or text.** Match the style with your own cast, props and story.

## What is bundled

| Path | Contents |
|---|---|
| `scripts/bootstrap.py`, `scripts/check_env.sh` | project setup and environment check |
| `pipeline/spec/` | the measured look specification (`LOOK_SPEC.md`), single-lens specs, verification notes |
| `pipeline/v2/puppet/`, `pipeline/v3/cast/` | the 2D puppet system and extra cast, with API docs |
| `pipeline/v3/set3d/`, `pipeline/v3/stage/`, `pipeline/v3/shots/` | a reviewed 3D set, the staging and camera system, a complete worked 5 second film with QA tools |
| `pipeline/v2/` (other) | the flat 2D compositor, still useful for inserts and artwork, and the scoring tool in `v2/eval/` |
| `pipeline/audio/` | narration through fal.ai with timestamps, caption alignment, effect library builder, mixer |
| `pipeline/plan/`, `pipeline/script_th_v2/` | an example verified shot plan and formula-matched script |
| `workflows/` | the multi-agent workflow scripts used at each phase, as templates |
| `references/` | the detail for each phase; read the one for the phase you are in |
