---
name: dz09-film
description: Produce and continue the Thai zombie animated series DEAD ZONE 09 / เขตปิดตาย 09 (vertical 9:16 film made with Blender Cycles, code-drawn 2.5D puppet characters, Ohm narration, Suno music, Thai captions). Use whenever the user asks to make, fix, render, review, join or deliver any scene or episode of DEAD ZONE 09, record its narration, or prepare prompts for it. It holds the user's locked decisions, the exact pipeline and commands, the quality gates, and the mistakes not to repeat.
---

# DEAD ZONE 09 — production skill

You are the director and the whole crew of **DEAD ZONE 09 / เขตปิดตาย 09**, a Thai zombie survival series. EP.1 is
"ทางด่วนนรก" (Bangkok expressway, Friday night, light rain). Everything on screen is made by code in Blender; the only
outside services are the narration voice and (optionally) AI 3D models when the user approves the cost.

Read this whole file before acting. Then read, in this order: `dz09/v10/film/README.md` (the finished hook and every
user decision), `dz09/ep1/pipe/README.md` (the episode pipeline and later decisions), `dz09/ep1/plan/PRODUCTION_PLAN.md`,
`dz09/ep1/plan/shots_ep1_timed.json`, `dz09/ep1/plan/narration_ep1.json`, `dz09/ep1/plan/continuity.md`. The READMEs are
the source of truth when they are newer than this file; the "USER DECISION" sections at their ends are never reverted.

---

## 1. Working with this user

- Reply in **Thai**. The user calls you "เพื่อน" and you call them "เพื่อน". Short, plain sentences; tables or short lists for status.
- The user watches on a **phone**. Send pictures and clips early with `SendUserFile` (stills sheet, before/after, draft clip)
  before running far ahead. "เสร็จแล้วส่งมาให้ผมดูนะเพื่อน" is a standing request.
- Every report says: what was done, what you checked yourself, **what you did not check** (you cannot hear audio; say so),
  and the weak points you can see. Never call something checked that was not. Label every time or money figure that is an
  estimate as an estimate.
- When the user names a defect from a screenshot (e.g. "ซอมบี้หน้าจมไปในรถ"), fix that defect, then sweep every shot for
  the same class of defect.
- Paid actions (TTS, AI 3D, image or video generation) happen only in the main conversation, only after the user approved
  that spend, and you report what was spent. Sub-agents and workflow agents must never call paid or network APIs.
- Never send the user's private details (email, name) to an outside service.
- The repository `domdu987/github-commit-quest-v2` is **public** and the user chose to keep it public. Commit source only
  (no frames, no videos, no WAV mixes). Work on the branch the session names; open or reuse a draft PR.

---

## 2. Locked creative decisions (do not change without a new user decision)

| Area | Decision |
|---|---|
| Format | Vertical **720x1280, 24 fps**. A 16:9 YouTube version comes later and must have MORE set detail, not a crop. Shot code takes framing through `F.pick(vertical, wide)`. |
| Sets | Detailed 3D night sets in Blender 5.3 Cycles (`dz09/v6/set`, `dz09/v11/set`, `dz09/ep1/sets`). Approved light and look: `dz09/v6/look/look.py`. |
| Characters | **Flat upright camera-facing 2.5D paper puppets drawn by code** (`dz09/v8/cast`, `dz09/ep1/cast`), matching the user's first sheet `dz09/uploads/character_sheet.webp` (round white heads, bold black outline, simple faces, spiky black hair, full costumes). Layers on parallel cards, front / 3-4 / side drawings, toon response to scene light, real shadows. |
| Blocky 3D cast | A code-built "Roblox-like" blocky cast was tested on 2026-11-28 (`dz09/v16/block`) and **rejected** ("if it can't look the same as the sheets, go back to the original characters"). Do not switch unless the user decides again. The only open route to the newer blocky sheets is AI image-to-3D (Meshy/Tripo) + rigid joint rig in Blender, which needs the user's paid accounts (see section 7). |
| Rain and post | Light rain. Approved levels in `dz09/v11/set/post11.py` `LEVELS` (RAIN 0.20, SPLASH 0.25, HAZE 0.30, TILT 0, DOF 0.25, BLOOM 0.55). Crisp line art; the cast is never lens-blurred. |
| Cuts and camera | **Straight cuts like a film.** No zoom push or radial blur at cuts (`JOIN = [0, 0, 0]` in both `finish.py` and `finish_ep.py`). No snap zooms. A camera push changes subject size at most about 10 % over a shot and under 2 % in its first 6 frames; ease with `smooth()`, never start a shot with a fast `ease_out` push. Static or slow moves by default; handheld only where the plan says, settling without a push. |
| Icons, logo, title | **No status icons, no logo, no title text anywhere.** (`noicons.SHOW_MARK = False`, `finish.SHOW_TITLE = False`.) The hook ends on the rising crane shot. |
| Captions | Kanit Black, white, 5 px outline, centre y 900 of 1280, phrase by phrase, hard swaps. Key words coloured: **amber `#ffb703` = a fact to remember, red = a threat**, with a 12 % pop for 3 frames (`EMPH` / `emph()` in `finish.py`; `emph` + `colour` per caption in `narration_ep1.json`). Screams are never captioned. |
| Narration | One narrator, voice **Ohm** (ElevenLabs v3 voice id `tKtPl8obOBs5uPMei6yN`, speed 1.15, Thai). Voice clearly above music and effects: **at least 12 dB over the bed at every moment, about 20 dB on average**, final mix about **-14 LUFS**, true peak <= -1 dBTP. |
| Music | The user's own Suno instrumentals in `dz09/audio/suno/`: `Rain_on_the_Concrete` (tension bed, hits every 8 s from 2.0 s), `Brutal_Pursuit` (chase; first used when the expressway erupts in scene 02), `Unsent_Letter` (sad piano; father-daughter moments), `The_Shadows_Pulse` (riser 0-3.8 s, hit at 3.8 s). Land a track's own hits on picture beats (see `dz09/audio/narr_ohm/mix_ohm_v3.py`). No music that "tells you to cry". |
| Countdown | The 60-second infection rule is shown by a **wristwatch prop**, never by an icon. Narration "50 / 30 / 10 วินาที" is pinned to real time after the bite (scene 02). |
| Closing line of EP.1 | "แต่เขาจะ**หวด** ใคร" (the TTS filter refused "ฟาด"). |
| Character designs | From the first sheet. Heights from the newer sheets' chart if needed: Kong 1.80, Khem 1.82, Tos 1.75, James 1.70, Praew 1.68, Namnuea 1.58, junior crew 1.74. |

Approved deliveries: `dz09/v10/film/DZ09_EP1_hook_916_v4.mp4` (hook, 53.33 s: v2 straight cuts, v3 no logo, v4 no title).
Scene 02 final: `dz09/ep1/pipe/out/DZ09_EP1_sc02_916_v1.mp4` (74.0 s), then joined after hook v4.

---

## 3. Environment and setup

- Python module **bpy 5.3** (headless Blender, Cycles CPU), numpy, PIL, cv2, ffmpeg with libass, Kanit fonts in `dz09/fonts`.
  Check: `python3 -c "import bpy; print(bpy.app.version_string)"`.
- All code finds the project root relatively (`PROJ = dz09/`), so the `dz09/` folder of the repo runs anywhere. Copy it to a
  scratch working directory before rendering; frames and videos are large and must not be committed.
- The cloud machine has **4 CPU cores and no GPU**. Final tier costs about 68 CPU s per frame at 100 % scale (about 37 at
  75 %), draft about 10. Plan renders with these numbers; a 74 s scene at final tier is roughly 8-10 wall hours on 4 workers.
- Count rendered frames with `find ... -name 'f_*.png' ! -name '*depth*'`: each frame also writes a `_depth.png`.
- Film frame `g` renders as Blender frame `g + 1`. Shots are pure functions of the frame number: any range, any order, resumable.

---

## 4. Pipeline per scene (follow in order)

Paths below are relative to `dz09/`. `run_ep.py` and `finish_ep.py` live in `ep1/pipe/`.

1. **Script and narration text.** Sentences with ids, speaker, caption phrases, `emph`/`colour`, beats and fx live in
   `ep1/plan/narration_ep1.json` (EP.1 is recorded). Show the user the reader copy (`ep1/plan/EP1_บทพากย์.md` style) and
   get approval before recording.
2. **Record (paid, main conversation only).** `audio/narr_ep1/record_ep1.py <worker> <n>`: per sentence, synthesise with
   `audio/th/tts_fal.py` (fal.ai `fal-ai/elevenlabs/tts/eleven-v3`), transcribe back with `fal-ai/elevenlabs/speech-to-text`,
   keep the best of up to 3 takes, accept >= 95 % text match. Report the character count and cost. If the content filter
   refuses a line, never try to slip it past the filter: offer the user milder wordings and record their choice.
3. **Lay the narration on the episode clock.** `ep1/audio/measure.py`, `build_narr.py`, `retime_shots.py`, `make_ass.py`,
   `check.py` -> `ep1/audio/narr_ep1.wav`, `narr_ep1_timing.json`, `ep1/plan/shots_ep1_timed.json`, `ep1/audio/captions_ep1.ass`.
   Tempo changes only within 0.92-1.10. Cuts land on the caption's first frame.
4. **Shot table and mouth track.** `python3 cut.py --scene NN --timing <captions_timing.json>` then
   `python3 mouth.py --scene scNN --wav <narration wav>` (re-run mouth after every cut).
5. **Author shots** in `ep1/shots/scNN/s0XX.py` (`from epbase import *`; `setup`, `frame`, `late`; `W("caption")` and
   `CUE("name")` for timing; `talk(actor, g)` so a mouth moves only on that actor's own lines; class C1 inserts use `ep2d`).
   Split a scene among several agents by shot range; each writes only its own files.
6. **Stills check.** Render 2 draft frames per shot (start-ish and the key moment), build a labelled sheet, look at every
   frame at full size, fix. Then a **collision sweep**: start / middle / end of every shot where a puppet is near a vehicle,
   wall, door or another puppet (puppet cards can sink behind geometry: the S054 "face inside the rescue truck" defect).
7. **Draft render** `python3 run_ep.py --scene scNN --tier draft --size 360x640 --spawn 3`, `--status` to watch.
8. **Scene sound.** `ep1/audio/scNN/mix_scNN.py` (pattern: `ep1/audio/sc02/mix_sc02.py`, effects synthesised by
   `sfx_synth.py`): narration + Suno tracks placed so their hits land on picture beats + effects (rain, beacons, heartbeat,
   alarms, impacts, footsteps). Measure the voice-over-bed margin per second and report it.
9. **Draft conform and user review.** `python3 finish_ep.py scene --scene scNN --tier draft --size 720x1280 --base-size 360x640 --out scNN_draft.mp4 --sheet scNN_draft_sheet.png`.
   Send the clip and the sheet with your own list of weak points. Wait for the user's notes; write them into
   `ep1/pipe/README.md` under "USER NOTES ON ..." so every agent sees them.
10. **Final gate.** After fixes, render ONE final-tier 720x1280 frame per shot (`--tier final --at 0.5`), sheet, look at
    every frame at full size (sharpness like the hook, faces readable, nothing sunk or clipped, sets not too dark).
    Estimate the final render time from these frames' CPU seconds and tell the user.
11. **Final render** `python3 run_ep.py --scene scNN --tier final --size 720x1280 --spawn 4` (hours; resumable; restart if it dies).
12. **Final conform** without any hook frames: `finish_ep.py scene ... --tier final --size 720x1280 --out ep1/pipe/out/DZ09_EP1_scNN_916_v1.mp4`.
    Check frame count, duration, first frame, captions in sync, loudness, no black frames.
13. **Independent review** by a separate agent that did not make the shots: frames every 0.5 s and both sides of every cut,
    continuity (positions, wound side, props, wet look, watch time), captions, audio by measurement. Fix by re-rendering
    only affected frames; keep the pre-fix file as `_prefix.mp4`.
14. **Join** the approved pieces in order: `python3 finish_ep.py master --hook ../../v10/film/DZ09_EP1_hook_916_v4.mp4 --scenes sc02[,sc03,...] --tier final --size 720x1280 --out <EP1_master>.mp4`.
    Check the join (picture, voice, music continue cleanly; one loudness over the whole).
15. **Deliver and back up.** Send the clip(s). Run `bash ep1/pipe/backup.sh <label>` and send the code + narration
    archives to the user in chat (each under 10 MB). Copy the changed source into the repo's `dz09/`, commit, push.

Hook-only tools (approved hook; change only on a user request): `v10/film/run.py`, `v10/film/finish.py`; to change only
some frames of an approved clip, recompose those frames from the raw renders and hard-link the rest
(`v10/film/tools/nozoom_build.py` pattern), then verify unchanged frames are bit-identical.

---

## 5. Quality gates (every shot, every scene)

- Faces: never covered by props, foreground or geometry; head at least 12 % of frame height in medium and closer shots;
  no out-of-focus foreground blob larger than a quarter of the frame.
- No puppet layer sunk into, behind or through a vehicle, wall, door or another puppet (check renders, not reasoning).
- Walking and running: real cycles with planted feet, foot drift <= 1 cm while planted. Extras all differ (face, hair,
  clothes colour, pose); no copied faces.
- Mouths move only on that character's own lines; blink every 2-5 s; the infected stay still where the plan says (no breath).
- Infected faces must read **frightening** (white eyes, snarl), never a grin that reads comic.
- Inserts (watch, phone, cutter battery) must read in one glance on a phone; Thai text on props correct (check glyphs).
- Sets never too dark to read a face; motivated practical light (beacons, street lamps, headlamps, phone glow).
- Cuts within 3 frames of the named word boundary; straight cuts; continuity of screen direction, wound side and props.
- Audio: voice >= 12 dB over the bed every second, about -14 LUFS integrated, true peak <= -1 dBTP, no clipping, no gaps.
- Before saying "done": look at the actual output file (extract frames), not at the intermediate folders.

---

## 6. Orchestration (agents and workflows)

- Use workflows for multi-step production (author -> draft -> review). Default to pipelines; give each agent a narrow scope
  and its own files; independent reviewers check the makers' work.
- Brief every agent with: project root, the READMEs and this skill's locked decisions, "never call paid APIs or network
  services", "every character is drawn by code", the render core budget, "look at your images at full size", and
  "report what you did not check".
- The machine has 4 cores: at most 4 render processes in total across all running jobs; give a background job 2 when
  another job renders. A stopped workflow can leave Blender/render processes running: `pgrep -fa run_ep` / `run.py` and kill them.
- Do not message a running workflow agent (it creates a duplicate); stop and resume the workflow instead. When a usage
  limit stops agents, resume the same workflow script with `resumeFromRunId` so finished agents come from cache.
- Reviewers must not edit approved files (the hook's `v10/film/shots/*.py`); a reviewer once did, and its unapproved
  edits had to be reverted from `tmp/rev/shots_before/`.

---

## 7. Outside services and accounts (state on 2026-11-28)

| Service | Use | State |
|---|---|---|
| fal.ai (proxy-injected key for `fal.run`) | Ohm TTS + STT check; also hosts Meshy 7.1 image/multi-image-to-3D (textured + auto-rig about $1.40) | **Balance exhausted, account locked.** The user must top up at fal.ai before any new narration or 3D test. |
| Higgsfield (connector) | Meshy / Tripo / Hunyuan image-to-3D, rigging (`generate_3d`, `get_cost:true` to price first) | 284.98 credits, Plus plan, but blocked by "daily generation limit for your grace period" (plan renewal issue). Prices seen: Meshy 7 textured+rig 44, Tripo multiview detailed 18, rigging 5 credits. |
| ElevenLabs (connector) | Voice listing; TTS is done through fal | Content filter refuses violent wording (e.g. "ฟาด"). |
| meta.ai | The user may generate shots there themselves | Prompt book for the 24 hook shots: https://claude.ai/artifact/7b3iFtGh4F2eT5WcNou5nV (source `dz09/prompts/`). |
| Google Drive (connector) | Backups | Uploads over about 3 MB per call fail; send archives in chat instead. |

AI 3D route for blocky characters (only if the user approves the spend): crop clean front / side / back views from the
sheet onto white (`dz09/v17/kong_ai/in/` shows how), multi-view to 3D with texture and A-pose, then in Blender slice the
mesh into rigid parts at the joints and parent them to an armature (Roblox characters are rigid segments, so no skin
weights), lay a code-drawn face decal over the head for expressions and lip sync, and test in a hook shot before any switch.

---

## 8. Mistakes already made (do not repeat)

- Status icons: four designs (flat row, info cards, pictograms, title mark) were all rejected; the film has none.
- A 3-frame zoom push at every cut read as TikTok, not film: removed.
- The first blocky 3D cast was shown with a tiny face, needle hair and box hands; it should not have been shown without
  measured bars against the sheet. Show the user only proofs that pass your own comparison.
- The S054 puppet sank into the truck; collision sweeps are now mandatory.
- An agent reported 1,212 of 1,280 frames done by counting `_depth.png` files too.
- A reviewer rewrote approved hook shot files; stopped jobs left half-rendered shots. After any stop, check which frames
  and files changed before continuing.
- Planned wording can be refused by the TTS filter; keep a milder alternative ready and let the user choose.

---

## 9. Where EP.1 stands (2026-11-28) and what comes next

- Hook (scene 01 + first beat of scene 02): **approved**, `DZ09_EP1_hook_916_v4.mp4`.
- Narration for the whole of EP.1: recorded (85 sentences) and laid on the clock; the episode is 5:39.88 (8,157 frames).
- Scene 02 (S025-S061, 74.0 s): draft approved for fixes; final 720x1280 render and independent review in progress; then
  join after hook v4 and send.
- Next: scenes 03 (cab, X1s sedan, X2), 04 (cab, under the expressway), 05 (under the expressway), 06 (river / RIV and
  construction site / SITE: **these sets are not built yet**). Missing assets before scene 03-05: stair gait, kneeling,
  gauze card, Tos's briefcase, James's map phone, the guard (new minor character, not Manat), about ten living extras.
- Later: the 16:9 version with richer sets; a thumbnail.
