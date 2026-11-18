# Handoff: starting a new film in a NEW chat (from film 11 on)

Why a new chat: the old director chat grew so long that every turn and every wake-up re-read a huge context, which ate the weekly limit.
Each film now gets its own short chat.

## 1. First message to paste in the new chat (Thai)
> อ่าน film/HANDOFF.md แล้วเริ่มเรื่องที่ 11 ตาม skill reference-style-shorts ตอบเป็นภาษาไทย

## 2. What the new chat must do first
1. Read these, in order:
   - this file
   - `film/skill/reference-style-shorts/SKILL.md` and `references/production-lessons.md`, which hold all the client rules learned in films 2-10
   - `film/QA_TEAM.md`, including the "Stricter QA" section
   - `film/POSTING_LOG.md`
2. Set up the working copy. The old scratchpad path dies with the old session, so make a fresh one:
   `PROJ=<new scratchpad>/proj; mkdir -p $PROJ; cp -r film/. $PROJ/`
   Everything the pipeline needs is in `film/`:
   - code (conform*, align, build_narr, mixer and fal helpers in `audio/`)
   - sets `v3/set3d*`
   - cast `v3/cast*`
   - stage `v3/stage`
   - puppets `v2/puppet`
   - fonts
   - reference frames `ref/`
   - analysis `analysis/`
3. Check that the fal.ai key is set in the environment (`$Key`). Narration uses ElevenLabs v3 through fal.ai.

## 3. Client decisions in force (2026-11-18)
- Thai replies. Voice is Bankky (RwilAvCC3o05RLuACpAn), speed 1.15, original setting, atempo about 1.134.
- Captions: Kanit Black 88 px, phrase captions, centred at y 900.
- The client makes the music in Suno. Give him the Styles / Exclude styles / settings text.
- **New set for EVERY film. Never reuse a set.**
- **Agree the look in ONE round.** Before building the full set, show a style board (2-3 quick stills: palette, detail level, key preset) and get an OK.
- **Ask before rendering.** Show the set contact sheet and cast sheet, and wait for an explicit OK.
- Detail level the client asked for: rich and detailed sets. Water must be smooth and layered with foam, glitter and wakes, not big flat triangles. Use pleasing period colours, not harsh black and white. Make it dense with props and life.
- Sharp picture, no DOF, wide dense lit 3D look, reveal inside the 3D world, no text signs.

## 4. Budget rules (to stay inside the weekly limit)
| Who | Model |
|---|---|
| Set and cast building | Sonnet first, then ONE Opus review (QA-art) |
| Render teams (cloud sessions) | Sonnet |
| QA-art, script judging, the director | Opus |
| Monitoring | a cheap Sonnet child session or long intervals (60+ min) |

Do not wake the director chat every 20 minutes. Prefer letting teams report on completion.
Stricter QA stays on:
- `film/qa_auto.py` every-frame checks (free)
- QA-tech at 6 fps
- QA-art on key takes
- a 4-reviewer final gate
- no solo overrides

## 5. Pipeline order (details in the skill)
1. Story: hook, pivot "คืออย่างนี้นะ", mocker quote and promise, "ไอ้..." nickname, countable escalation, false payoff, one-image reveal, aha, and an ending that turns the mocker's own words back on him. Then a blind Sonnet tester, 3 rewrites, and a retest.
2. Narration: per sentence, STT at ≥0.97 or rerecord, then `audio/build_bk0.py` (copy from `film10/audio/`), captions and timing.
3. Write BRIEF.md and shot_plan.md. Get the style board OK, build the set and cast, pass the SET gate, get the client OK.
4. Write WORKER<N>.md from WORKER9.md. Launch render teams with `create_session` (source branch, clone_depth 1, outcome_branch renderN/teamK, Sonnet).
5. TAKE gate per take. Then conform: `conform_full.py` then `conform<N>.py`, copied from conform9.py.
6. FINAL gate (4 reviewers), then `release<N>/`, caption text, POSTING_LOG.md, and send to the client.

## 6. State at handoff
- Films 2-9 are all posted (see POSTING_LOG.md).
- Film 10 "ไอ้ช่างม้าลาย" (dazzle ships) is being finished in the old chat:
  - script, narration and shot plan are in `film10/`
  - set `v3/set3d10` (copied into the repo when approved), cast `v3/cast10`
- Ideas for film 11 and later: pick a concrete object plus a counter-intuitive true story with a mocker. Avoid explainers.

## 7. Auto-posting (client decision, 2026-11-18)
A Chrome AI extension checks `film/POST_QUEUE.md` on branch `claude/new-session-73ou27` every hour and posts READY rows to YouTube Shorts.
When a film passes the FINAL gate and is sent to the client:
1. Push the release mp4 and caption.txt to `claude/new-session-73ou27`: fetch first, then rebase.
2. Add a row with status `READY`. The Video link is
   `https://github.com/domdu987/github-commit-quest-v2/raw/claude/new-session-73ou27/film/releaseN/<file>.mp4`.
   Use a short Thai title that is unique per film, plus a `### N <Title>` caption section.
3. Never mark a row READY before the client has seen the final film, unless he has said to auto-post without review.

## 8. From film 15: film-2 camera rhythm (client decision 2026-11-18)
Read skill production-lessons §10 before planning shots, and use film/plan/shot_plan.md (film 2) as the camera-grammar example.
The voice stays Bankky at the original setting.
