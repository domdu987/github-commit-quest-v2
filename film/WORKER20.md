# Render-team worker brief, film 20 (ไอ้ช่างหมุด — Eiffel's tower and the 1887 artists' protest)

Follow film/WORKER.md for the delivery format and rules (sections 4-5), with the film-20 differences below.
The set, the cast and the look are approved (QA-art + SET gate). Work autonomously; do not ask for confirmation.

## 1. Setup
```
REPO=$(git rev-parse --show-toplevel); PROJ=$REPO/film      # work directly in the repo; no symlink needed
pip install -q bpy numpy pillow opencv-python-headless pythainlp
python3 -c "import bpy; print(bpy.app.version_string)"      # 5.x
```
Your container has 4 cores: run at most 2 render processes with 2 threads each.

## 2. Read, in this order
1. PROJ/film20/BRIEF.md and PROJ/film20/shot_plan.md: your shot rows.
2. **The worked example: PROJ/v3/film20/s01/**: shot.py, c20.py (the film-20 helper), QA.md (gotchas), meta.json, cues.json, contact.jpg. Copy c20.py into YOUR take folder (do not create a shared helper).
3. PROJ/v3/set3d20/API.md (presets, lights, hooks, marks, scale, recipes; interior part merged from API_int.md), and QA_ART.md / QA_TECH.md: their "notes for render workers" are yours to handle by camera and staging.
4. PROJ/v3/cast20/API.md (cast keys, STORY20 poses, Maupassant MOUTH_SET, props, cycles).
5. PROJ/skill/reference-style-shorts/references/production-lessons.md §2 (client taste) and §10 (camera rhythm), PROJ/QA_TEAM.md "Stricter QA".

## 3. Clock
Narration PROJ/film20/audio/narration.wav (67.79 s) at +0.10 s. Captions PROJ/film20/script/captions.json. g = round(t*30); N = 2046 (68.2 s).
Sentence starts: hook 0.00 / pivot 5.93 / boss 13.47 / nickname 25.09 / count 27.41 / false 33.21 / crisis 40.70 / reveal 43.39 / aha 52.02 / ending 57.75 / end 67.79.
A shot's g0 = round(t0*30), g1 = round(t1*30)-1. In-shot events at narration time x fall on g = round((x+0.10)*30).

## 4. Look and camera (hard rules)
- Sharp, NO depth of field, NO text anywhere (newspapers and the protest sheet are greeked scribbles). Warm lit 3D world as the approved set.
- Every shot has a clear move: drift 6-10 %/s push/pull + 20-60 px/s slide, eased, plus one eased SNAP (13-25 frames, x1.3-x3) on the strongest word in every shot over 2 s. Never parked more than 6 frames. Foreground prop 1-2 D from the lens in most shots.
- Heads: whole heads above y 880; head centre y 450-760 (wides exempt). Laughing characters bounce ~0.06 D at ~3 Hz; nobody frozen.
- Characters stand IN the world (contact shadows, correct scale, feet on the floor/ground marks). Hand props attached to hands (cast20 cards draw them).
- Mouths move ONLY on Maupassant's quotes: 22.62-25.11 s (shot 10; shot 9 ends before it) and the laugh + 37.12-40.67 s (shots 16-17), ±0.15 s. Everywhere else mouths are still.
- The tower must read as the Eiffel Tower whenever it is in frame. Time states: 1887 site stage 0 + café 'stub' view; count shot 14 stages 1->2->3; 1889 fair + café 'full' view + restaurant; 1909 dusk/night with OLD Eiffel (eiffel_old), antenna on, wagon on; 1910 day (shot 23).
- Comic falls only, no injury.
- Target in-shot frame-diff (90x160 grey): median >= 4, p90 >= 12. Measure it as s01/QA.md shows and report it.

## 5. Delivery
- Take folder PROJ/v3/film20/sNN (NN = shot number, two digits). One take per shot.
- meta.json: g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n} (dissolve lengths from the plan's "in" column, on the shot that is dissolved INTO). Render handle frames = dissolve/2 + 2 on each dissolved side (render them in 3D, the move continues), 4 frames on cut sides.
- take.mkv (ffmpeg libx264rgb crf 6). If over 45 MB: `split -b 40M take.mkv take.mkv.part`. Frames/raw/work stay out of git (.gitignore).
- cues.json: sound cues in film seconds (kind, t, note), one for every prop event that matters.
- Before delivering: `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>`, fix every FAIL, add QA_AUTO.md + phone_sheet.jpg; then check yourself at 6 fps plus every cut ±3 frames (heads, contact shadows, props held, eye-lines, mouths only in quote windows, continuity with neighbouring shots) and write QA.md.
- Push each take as soon as it is final: `git add -A film/v3/film20/sNN; git commit; git push -u origin <your branch>` (retry with backoff). Do not open pull requests.
- Final message: takes delivered, frame ranges, s/frame, frame-diff numbers, anything that differs from the plan.

## 6. Self-check before delivering (added after TAKE gate round 1: 18 of 19 checks failed on these)
- **Ground / ceiling / floor <= 25 % of the frame** at every 6-fps sample. No flat bare slab in the bottom third: tilt up, lower the camera, or dress it (crowd cards, props in light).
- **Principals readable on a phone**: the main character's head >= 60 px (wides >= 40 px), never cut by the frame edge mid-shot, never hidden behind foreground props. Foreground props sit at the SIDES, never over faces.
- **The planned beat must happen on screen**: walks actually travel, hands touch what they use (Morse key), points point at the thing, the reveal reveals (start where the thing is NOT yet visible).
- **The Eiffel Tower (or its legs/scaffolds) is in frame on every SITE/TOWER shot** and reads as the tower; compare with the approved set tiles in v3/set3d20/contact.jpg.
- **No broken geometry, black slabs, unlit low-poly voids, blown streaks, duplicate props, moire.** Hide or move what you cannot fix.
- **Frame-diff measured on the final frames** (90x160 grey, in-shot): median >= 4 AND p90 >= 12, from real camera motion (push/slide/orbit + one snap), not from flashes or jitter alone.
- Look at your own phone_sheet.jpg (360x640) and ask: would the client understand this beat in 1 second? If not, fix it before pushing.

## 7. QA_TEAM.md §G (client complaints after films 15/17, 2026-11-20) — BLOCKING at TAKE and FINAL gates
Measure every take with `python3 PROJ/qa_stats.py take.mkv` and report the line in QA.md:
- **Colour:** mean saturation >= 0.47 and mean luma 85-110 (film 2: 0.49 / 94). Night shots (s20, s21, s22) may sit darker but not below ~70 and must stay saturated; no peach haze over the frame.
- **Nothing floats:** feet/body on a surface with a contact shadow; no heads hanging in the sky; no bars, poles or props through a face; no character sliced by a slab; no debris hanging still in the air.
- **Camera distance:** prefer wide / medium-wide that shows the place; no face taller than ~35 % of the frame height; no character cut in half by a frame edge.
