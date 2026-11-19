# Phase 7: running production

The finished run: 26 shots, 1965 frames, 30 fps, 720x1280. The 3 opening shots were made first (phase 5); the other 23 were takes, one folder per take (`PROJ/v3/film/sNN/`). Production of the 23 takes took about 4 hours of wall time with 4 to 5 workers on the one-tier-down model, after two restarts caused by a late change of a design choice. This file is how to run it so the next production does not need the restarts.

## What every worker gets

- **One shared brief** for all shot workers (`pipeline/v3/film/BRIEF_SHOTS.md`) plus **the conventions file** (`pipeline/v3/film/CONVENTIONS.md`). Together they hold the clock (how a plan time maps to a film frame), the folder layout, what a finished take is, the colour band, the hard rules and the client decisions. A change of course is an edit of the brief, never a message to a worker.
- **A finished take** is: `frames/g_%04d.png` named by global film frame, with handle frames on every side that has a dissolve (half the dissolve plus 2 frames); `meta.json` (range, handles, transition, set, light, samples); `cues.json` (every visible event that should make a sound); `contact.jpg` (12 or more frames, frame number and time above the picture); `QA.md` (head sizes and positions, near/far ratio, registration error of pinned props, framing-change times, static and linear runs, pops, the hue row, seconds per frame). Examples: `pipeline/v3/film/s10/`, `s24/`, `s26/`.
- **The prompt of each worker** only names its lane, its shots and its folders, and points to the brief. Shot-specific hints (which takes share marks, which finished take to match across a dissolve) go in one or two sentences. Templates: `workflows/11_production_lanes_office_shots.js`, `workflows/12_production_extra_lane_claimed.js`, `workflows/13_production_lanes_and_finish.js`.
- **The return value is a schema**: per take `take, g0, g1, frames_rendered, complete, hue_row, notes`, plus `deviations_from_plan` and `known_gaps`.

## Adapting to a new film

The briefs and workflow scripts in the package are film 1's, filled in: its story, its 26 shots and 1965 frames, its client decisions with dates, its file names. Handed to a worker unchanged they give stale orders. Per file:

| File | Keep | Rewrite or delete |
|---|---|---|
| `pipeline/v3/film/BRIEF_SHOTS.md` | nothing as is: start from `BRIEF_SHOTS.template.md` | story, client decisions, the dated sections "work that already exists" and "the voice was re-recorded" (write them only when they happen), shot numbers, the names of sets, lights, props and quoted lines |
| `pipeline/v3/film/CONVENTIONS.md` | start from `CONVENTIONS.template.md`; the colour band and folder rules are generic | shot and frame counts, narration paths, audio offset, the worked example |
| `pipeline/v3/film/BRIEF_FINISH.md` | levels and rules | input paths, the dated voice section, the take list, the film length, the delivery file names (and pass them to `watch_prod.sh`) |
| `pipeline/v3/film/BRIEF_POLISH.md` | the structure: frozen folders, build order (grade, captions and encode in one pass, sound), rules, the sharp-picture rule | "where we are" from your own v1 review, frozen paths, per-shot instructions |
| `workflows/01` to `14` | the shape (stages, schemas, `complete` flags, the claim rule, model per stage) | every prompt text: lane names, shot numbers, set and cast names, paths such as `/media/...` or `__SCRATCH__/proj/...` that bootstrap does not create. Each file starts with a comment saying so. |
| `pipeline/v3/shots/film.py`, `timing.py` | the structure | beats, trigger words, props, acting (see `pipeline/v3/README.md`) |
| `pipeline/v3/film/sNN/` | as examples of a finished take | everything: they are film 1's shots. Several do not run after bootstrap (s10 reads film 1's narration WAV through `acting.loudness`, which is not shipped; `s20/post.py` knows only s20-s22). Start a new shot from `pipeline/examples/<family>/shot.py` (`references/bible/kit-quickstart.md`) |
| `pipeline/audio/th/build_narration_v2.py` | as an example | use `pipeline/audio/build_narration.py` instead |

## Lanes

- A lane is a group of shots that share marks, cameras and sprites (for example the gloat framing used in shots 10, 11, 12 and 18). One worker builds the lane's first shot, the next shots reuse its staging. Put shots that must match across a dissolve in the same lane, or tell the second worker which finished frames to open.
- Two workers at a time per workflow on a 4-core machine. A second and a third workflow can run beside the first when their workers own different folders. Final renders compete for the same cores: one render process per worker, 2 threads.
- Every worker: stage with numbers (probe), draft small (360x640, 6 samples, every 4th to 6th frame), look at a contact sheet next to the reference frames the plan names, then start the final render as a **detached, resumable** process (`nohup`, a frame counts as done when its PNG and its meta exist) and stage its next shot while it renders.
- Before it renders, every worker checks that no render already runs in its folder: `ps -eo pid,lstart,cmd | grep shot.py` and `readlink /proc/PID/cwd`. A render started by an earlier, interrupted worker may still be running and still be valid.
- Render cost with several renders at once: one final frame is about 18 to 23 CPU seconds; with 3 to 5 renders at once each frame takes 25 to 45 s of wall time; total throughput is about 8 to 11 frames a minute (2,120 frames with handles for the 23 takes of film 1). Plan the order of lanes so the longest takes start first.
- The finishing workflow (conform, sound, review) runs after the last lane. Its conform step waits for missing takes rather than failing (`BRIEF_FINISH.md`, `pipeline/v3/film/out/CONFORM.md`).

## The sweeper: finish takes whose worker returned early

Workers were told never to return while a render runs. Two of them still returned early, leaving four takes (s08 and s24 of one lane, s12 and s13 of another) with their final renders still running (why they returned is not recorded; a time or budget limit is the likely cause). The detached renders finished alone and the takes sat there without post, QA or meta. A third result marked four takes `complete: false` only because those folders were claimed by another lane, which is correct: the sweeper must tell the two apart (it shows the claim files). So after every lane result, in the main conversation:

1. Read the workflow journal (`journal.jsonl` in the run folder), not the summary line, and list every take with `complete: false`. `python3 scripts/sweep_takes.py <project> <journal.jsonl> ...` does this and also shows frame counts, missing files, renders still running in the folder and claim files.
2. For each such take: wait for its render, then run the take's own post, grade (if it has one), contact, qa and QA.md commands. They are in the take's `shot.py`, its runner (`otake.py`) or `work/*.sh`; `s10/qa_md.py` writes a QA.md from the qa numbers.
3. Look at the contact sheet yourself.

This is mechanical and cheap: a cheap worker or a few shell commands. Do it before you start the next lane, so a missing take is found while there is still time to render it.

## Handing shots to an extra lane without stopping anything (CLAIMED.txt)

A running workflow cannot be edited, and its workers must never be messaged (a message forks a duplicate worker). To pull forward shots that a later worker of a running workflow will also be given:

1. Add a short rule to the shared brief: "a take folder that holds CLAIMED.txt belongs to the lane named in it; if it is not yours, do not touch it and return that take as owned by that lane". The later worker reads the brief when it starts, so the edit reaches it. See the section "Folders owned by another lane" in `BRIEF_SHOTS.md`.
2. Create the folders with a `CLAIMED.txt` that names the lane (example: `pipeline/v3/film/s13/CLAIMED.txt`).
3. Start a second workflow whose workers are told their lane name (`workflows/12_production_extra_lane_claimed.js`).

The later worker finds every shot claimed and returns at once. This saved about an hour.

## Where workflow runs live

The `.js` files are scripts for Claude Code's Workflow tool (the `workflow-authoring` skill documents the script API: `agent()`, `parallel()`, `meta`, schemas, resume). Each run gets an id (`wf_...`) and a folder `WF_DIR/<run id>/` holding `journal.jsonl` (one line per finished agent, with its structured result) and one `agent-*.jsonl` transcript per worker, where `WF_DIR` is `~/.claude/projects/<project folder slug>/<conversation id>/subagents/workflows`. A run that stopped is resumed by starting the Workflow tool again with its run id: finished agents are served from the journal, only unfinished ones run again.

## Watching for stalls

- Check that work is alive, not that it is listed: compare the modification time of each worker's transcript with the clock, and count frames on disk.
- `bash scripts/watch_prod.sh <run id> ...` (with `PROJ` and `WF_DIR` set, and `FILM` and `REVIEW` set to the delivery files your finishing workflow writes, relative to `PROJ`; the defaults are film 1's `deliver/film_v1_thai.mp4` and `deliver/QA_film.md`) is a background wake-up: it exits when the film and its review exist, when nothing has been written for 30 minutes, or after 110 minutes as a heartbeat, and prints a status line per take (frames, meta, QA) and the age of each worker transcript. `scripts/watch_polish.sh` does the same for the polish pass. Restart it after each wake-up.
- Ask the user not to press stop while production runs: a user interrupt kills every background workflow.

## Restarting after an interrupt or a change of course

1. List what runs: `ps -eo pid,lstart,cmd | grep -E "shot.py|otake.py"` and the folder of each (`readlink /proc/PID/cwd`). Keep renders whose takes are still valid; kill the rest, or a stale chain overwrites good frames.
2. Delete the frames that are now wrong yourself (for example every frame showing the changed prop that is older than the change, or every frame of a lip-synced shot rendered before the voice changed). Never leave a take that mixes two versions.
3. Add a section "work that already exists" to the brief: list the folders first, reuse what is sound, keep finished takes the change does not touch, name the time before which frames of a given kind are wrong, and say to check `ps` before rendering.
4. Relaunch the workflows. Workers resume from what is on disk; a resumable render loop picks up where it stopped.

## Changing the voice without changing the picture

The narration was re-recorded with another voice after most takes were rendered. `pipeline/audio/th/build_narration_fit.py <voice_id> <voice_name> <out_dir> [speed]`:

1. Records the new voice in the same paragraph chunks as the first recording and checks each chunk with speech-to-text.
2. Tightens the silences as before.
3. Time-stretches every SENTENCE into the slot the same sentence has in the old narration (start of its first caption phrase to the start of the next sentence).

Sentence starts and the total length stay the same, so shot boundaries and every rendered frame stay valid. Caption phrase times are recomputed (they moved by 0.05 s on average, 0.24 s at most). Only what is driven by the sound itself must be redone: mouths that follow the narration loudness (two shots here). Keep the old voice in a backup folder (`audio/th/full_v2_oldvoice/`; the script reads its clock from there) so the change can be reverted in a minute. Cost: about 1,400 characters of text-to-speech in 13 takes plus 13 speech-to-text checks; this was the only paid spending of the whole second half.

## After the last lane: conform, mix, first review

About 35 minutes for this film (`workflows/13_production_lanes_and_finish.js`, brief `BRIEF_FINISH.md`):
- `pipeline/v3/film/out/conform.py`: joins takes with the planned transitions from the handle frames (CONFORM.md lists the joins and checks), `grammar.py` counts the edit grammar against the measured numbers. It is film 1's: its take list, length (1965 frames), opening and overlays are written in. For a new film start from `pipeline/examples/film_mini.py` (conform, captions, mix for any list of take folders, the same dissolve rule) and add your overlays.
- `pipeline/v3/film/out/sound/build.py` builds the effect list from the cues of every take (merged by the conform into `cues_all.json`); `pipeline/v3/film/out/sound/measure.py` measures the result; `mix_film.json` is the mixer spec (SOUND.md explains levels and choices).
- Captions burned last with `pipeline/assemble.py`.
- An independent review measured with the same tools as the analysis: `references/examples/QA_film.md`. Then the polish pass: `references/polish.md`.
