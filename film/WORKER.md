# Render-team worker brief (film 2: ไม้จิ้มฟ้า)

You are one of several parallel render workers. Each worker owns a few takes of the film, renders them in its own cloud
container, and pushes the result to its own git branch. The director session merges everything.

## 1. Set up (do this first, exactly)
```
REPO=$(git rev-parse --show-toplevel)        # this repository
PROJ=/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj
mkdir -p "$(dirname $PROJ)" && ln -sfn "$REPO/film" "$PROJ"
pip install -q bpy numpy pillow opencv-python-headless pythainlp
node -e "require('playwright')"              # preinstalled Chromium; never run 'playwright install'
```
Every script in the project uses the absolute path PROJ, which the symlink makes valid. Work only through PROJ paths.
Check: `python3 -c "import bpy; print(bpy.app.version_string)"` prints 5.x.

## 2. Read (in this order)
PROJ/plan2/BRIEF.md, PROJ/plan2/shot_plan.md (your shots), PROJ/v3/film/CONVENTIONS.md, PROJ/v3/README.md ("How to add a shot"),
PROJ/v3/film2/s01/shot.py + QA.md + meta.json + cues.json (THE worked example of this film: same set, same cast, same clock — copy its
structure and its tricks: custom cameras, hide_render of the 'market' stall, head_flip choice, shade foreground pier), PROJ/v3/stage/API.md,
the set API you use (PROJ/v3/set3d2/tower_API.md, vault_API.md, room_API.md + REVIEW files), PROJ/v3/cast2/API.md.
Look at PROJ/v3/film2/s01/contact.jpg and the reference frames PROJ/ref/a/*.jpg, PROJ/ref/b/*.jpg named in the plan.

## 3. Clock
Narration PROJ/audio/narration.wav (65.0 s) at +0.10 s. Caption phrase times: PROJ/script/captions.json ("t" = narration s).
Film frame g = round((t + 0.10) * 30) for in-shot events; the plan's shot boundaries t0/t1 fall on round(t * 30). 30 fps, 720x1280.
Render handle frames beyond your take's range for dissolves: half the dissolve length + 2 frames on that side, in 3D.

## 4. Deliver (per take sNN = number of the first shot in the take)
In PROJ/v3/film2/sNN/: shot.py, meta.json, cues.json, contact.jpg, QA.md (same formats as s01), plus
`take.mkv` = all final frames g0-handle .. g1+handle encoded with
`ffmpeg -framerate 30 -start_number <first g> -i frames/g_%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv`
and record in meta.json "first_g" (the g of the first frame in take.mkv) and "n_frames". Frames/raw/work stay out of git (.gitignore).
Then: `git add -A film/v3/film2/sNN ...; git commit; git push -u origin <your branch>` (retry pushes with backoff on network errors).

## 5. Rules
- Write only in your own take folders. Sets, stage, cast, plan, audio and other takes are read-only. If a set needs a change, do it from
  your shot.py at runtime (hide/move/add objects), never by editing the set module.
- Final: 12 samples, 720x1280. Your container has 4 cores: run at most two render processes with 2 threads each.
- Draft first (360x640, 6 samples), look at a contact sheet next to the reference frames, fix, then final.
- No network calls except git and pip; no MCP/connector tools; no paid APIs.
- Look rules: whole heads above y = 880 (captions sit there); main head centre 0.35-0.59 H (wides exempt); a framing change every 1.2-1.6 s;
  never static > 6 frames; mouths move only inside the two quoted lines (shot 9 and shot 14, padre); no anachronisms (flags etc.).
- Colour: python3 PROJ/v3/tools/hue_report.py style numbers (see s01/hue.py, which works with this film); shade blue-violet, never magenta.
- Finish with a short report in your final message: takes delivered, frame ranges, s/frame, anything that differs from the plan.
