# The style bible: index

The bible holds the concrete knowledge of the style that film 1 reproduced: every camera, colour, set, trick, character, caption and sound level, as numbers, names from the code and recipes you can paste. The analysis of the reference is done; do not measure the reference again unless the user's new references are a different style (`references/analysis.md`, "Is the new reference the same style").

Every chapter keeps two things apart: **Reference (measured)**, what the two reference clips do, and **Our build (film 1)**, what was built, with the names the code uses. Paths are relative to the skill's `pipeline/` folder (after `scripts/bootstrap.py`, relative to your project folder) unless they start with `__PROJ__`, which means film 1's own project: not shipped, cited only as a source. Pictures are in `assets/bible/` and come only from our own film and renders.

Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. The motion streak on fast camera moves stays.

## The chapters

**`kit-quickstart.md`: the kit.** What ships and what you regenerate, the clean start (bootstrap, `examples/setup_kit.sh`, `examples/smoke.py`), the five set families with one tested example shot each (`pipeline/examples/`), the commands a shot worker runs in order (probe, draft, render, post, contact, qa), an annotated shot file, and `examples/film_mini.py`, which turns takes into a captioned, mixed film. Read it first in a new conversation: it gets you from the unpacked skill to a rendered draft in under an hour.

**`camera.md`: angles, framings, moves.** The one lens (22 mm, 782.2 px focal length), heights and pitch by angle class, head width by shot size and the matching distance, how often the framing changes, every move type with its speed and easing, every named camera of every set with position and aim, all 26 shots of film 1 as camera data, eleven recipes (low single, push, snap, whip, crane, two-shot in depth, shake and others) and a story-beat to framing table.

**`colour-light.md`: colour and light.** The palette by role with hex, the hue band and how `v3/tools/hue_report.py` measures it, tone statistics, the key light and the blue-violet shade, glow, every light preset of the three sets with every parameter, every material and costume colour, the v1.1 grade stage by stage, the hue of every shot of film 1, and recipes for a new interior, an exterior, grey, storm and night.

**`sets.md`: the places.** How the reference builds its places and layers its depth, the machinery all sets share, the texture caches and their order, then the office, the wall map as terrain, the beach and the kitchen: dimensions, coordinates, exact sign texts, actor marks, cameras, presets, setters and tested recipes. The paper artwork registry, how to re-dress a set for another story, and the procedure and acceptance list for a new set.

**`scene-tricks.md`: transitions, overlays, gags, effects.** Every join of the reference and of film 1 (dissolve weights, wipe, flash, whip, hidden cut), the drawn overlays, 41 set gimmicks with their setter calls, 19 character effects, the motion streak rule, camera shake, callbacks, a beat-to-device decision table, the dosage per clip, and recipes for each device.

**`characters-acting.md`: the puppets.** The character design as numbers, the face vocabulary and when faces swap, movement and lip flap from loudness, head sizes, the puppet system and its pose keys, all 8 cast members with colours, 27 expressions and 19 mouths, props in hand, the acting library (32 functions), recipes R1 to R7 (a character on a mark, an expression on a word, talking, walking, a two-shot reaction, a pinned hand card, a new cast member) and an emotion-to-pose table.

**`captions-sound.md`: captions, voice, music, effects.** Caption style and size, the Thai phrase rules, the pipeline from script to burned picture, the narration pipeline and the film clock (voice at +0.100 s), the mix specification and mixer, the effect library with levels, how a take's cue becomes a mix entry, the levels and rules, all 52 mix entries of film 1, recipes (caption check, effect choice, mix check) and what to ask the user to listen for.

**`film1-shots.md`: film 1 shot by shot.** All 26 shots as a worked example: time and frames, captions, set and light, camera and move, acting, props, transition, sound cues, the reference shot it imitates and the reviews' verdict. Summary tables of the edit against the reference, the callbacks, a ranking of shots from most to least like the reference, and the edit as data.

## Reading order for each job

| Job | Read, in this order |
|---|---|
| First hour in a new conversation | `SKILL.md` (fast path and style card), `kit-quickstart.md` 1 to 3, the sheets `assets/bible/film1_shots_1.jpg` and `film1_shots_2.jpg` |
| Writing a shot plan | `film1-shots.md` 1 and 3 (the edit and the ranking; 5.3 how to write an entry), `camera.md` rules, 1.4, 4.1 (beat to framing) and 2.2 (named cameras), `scene-tricks.md` 4.1 and 4.2 (devices and dosage), `characters-acting.md` 4 (emotion to pose), `captions-sound.md` 2.3 (the film clock), `sets.md` marks and cameras of the sets you will use |
| Building or re-dressing a set | `sets.md` rules, 2 (shared machinery and caches), the section of the nearest existing set, 8 (re-dressing) or 9 (a new set and its acceptance list), `colour-light.md` 5.1 to 5.5 (swatches, lighting, the hue check), `camera.md` 2.2 (cameras to give the set), `kit-quickstart.md` 1.3 (cache order) |
| Staging and rendering a shot | `kit-quickstart.md` 2 and 3 (copy the example of the family), `camera.md` rules and recipes, `characters-acting.md` 2.6 and R1 to R5, `sets.md` marks of the set, `scene-tricks.md` 5 (the device recipes), `colour-light.md` 5.5 (hue check), the matching entry of `film1-shots.md` |
| Joining takes, captions and the grade | `kit-quickstart.md` 4 (`film_mini.py`), `scene-tricks.md` 2.1 and 5.1 (joins), `captions-sound.md` 2.1 and 4.1 (captions), `colour-light.md` 3 (the grade), `references/polish.md` |
| Mixing | `captions-sound.md` rules, 2.4 to 2.7, 3 (film 1's mix as data), 4.2 to 4.5, `scene-tricks.md` 2.7 (which devices had sounds), `references/audio.md` |
| Reviewing a version | `film1-shots.md` 3.3, each chapter's last section (what the reviews found wrong), `references/examples/QA_film.md` (read its note at the top) |
