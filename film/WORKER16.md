# Render-team worker brief, film 16 (ไอ้บ้าลวด — Morse's telegraph line, 1825-1845)

Follow film/WORKER.md for the delivery format and rules (sections 4-5), with the film-16 differences below.
The client has approved the set, the cast and the render. Work autonomously; do not ask for confirmation.

## 1. Setup
```
REPO=$(git rev-parse --show-toplevel); PROJ=$REPO/film      # work directly in the repo; no symlink needed
pip install -q bpy numpy pillow opencv-python-headless pythainlp
python3 -c "import bpy; print(bpy.app.version_string)"      # 5.x
```
Your container has 4 cores: run at most 2 render processes with 2 threads each.

## 2. Read, in this order
1. PROJ/film16/BRIEF.md and PROJ/film16/shot_plan.md: your shot rows AND the "Bible addendum" at the end (snaps, angle mix, joins, devices).
2. **The worked example: PROJ/v3/film16/s01/** — shot.py, c16.py (the film-16 helper), QA.md (gotchas), meta.json, cues.json, contact.jpg. Copy c16.py into YOUR take folder (do not create a shared helper).
3. PROJ/v3/set3d16/API.md (presets, lights, hooks, marks, hand props), and QA_ART.md / QA_TECH.md (their "notes for render workers" are yours to handle by camera and staging).
4. PROJ/v3/cast16/API.md (cast keys, STORY16 poses by shot, canvases CANVAS16_POLE / CANVAS16_BUGGY, the mule via cast16.cycle("mule", ...), key16() name map: worker16_a/b, clerk16).
5. PROJ/skill/reference-style-shorts/references/production-lessons.md §2 (client taste) and §10 (camera rhythm), PROJ/QA_TEAM.md "Stricter QA".

## 3. Clock
Narration PROJ/film16/audio/narration.wav (69.85 s) at +0.10 s. Captions PROJ/film16/script/captions.json. g = round(t*30); N = 2100.
Sentence starts: hook 0.00 / pivot 5.61 / boss 15.86 / nickname 23.28 / count 26.21 / false 31.95 / crisis 40.89 / reveal 46.04 / aha 53.86 / ending 60.19 / end 69.85.
A shot's g0 = round(t0*30), g1 = round(t1*30)-1. In-shot events at narration time x fall on g = round((x+0.10)*30).

## 4. Look and camera (hard rules)
- Sharp, NO depth of field, NO text anywhere (the register tape is dots and dashes only). Warm lit 3D world as the approved set.
- Every shot has a clear move: drift 6-10 %/s push/pull + 20-60 px/s slide, eased, plus one eased SNAP (13-25 frames, x1.3-x3) on the strongest word in every shot over 2 s. Never parked more than 6 frames. Foreground prop 1-2 D from the lens in most shots.
- Heads: whole heads above y 880; head centre y 450-760 (wides exempt). Sizes per the addendum. Laughing characters bounce ~0.06 D at ~3 Hz; nobody frozen.
- Characters stand IN the world (contact shadows, correct scale, feet on the ground or on the ladder rung mark). Hand props attached to hands (cast16 cards draw them).
- Mouths move ONLY in the mocker's quotes: boss 18.32-23.20 s (shots 9-10) and false 38.46-40.80 s (shot 18), ±0.15 s. Everywhere else mouths are still.
- Comic falls only, no injury.
- Target in-shot frame-diff (90x160 grey): median >= 4, p90 >= 12. Measure it as s01/QA.md shows and report it.

## 5. Delivery
- Take folder PROJ/v3/film16/sNN (NN = first shot number of the take). One take per shot unless your assignment says otherwise.
- meta.json: g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}. Render 9 handle frames each side (dissolves up to 17 f).
- take.mkv (ffmpeg libx264rgb crf 6). If over 45 MB: `split -b 40M take.mkv take.mkv.part`. Frames/raw/work stay out of git.
- Before delivering: `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>`, fix every FAIL, add QA_AUTO.md + phone_sheet.jpg; then check yourself at 6 fps plus every cut ±3 frames (heads, contact shadows, props held, eye-lines, mouths only in quote windows, continuity with neighbouring shots) and write QA.md.
- Push each take as soon as it is final: `git add -A film/v3/film16/sNN; git commit; git push -u origin <your branch>` (retry with backoff). Do not open pull requests.
- Final message: takes delivered, frame ranges, s/frame, frame-diff numbers, anything that differs from the plan.
