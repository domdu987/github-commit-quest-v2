# Render-team worker brief, film 22 (ไอ้ช่างวงจร: Harry Beck's Underground diagram, London 1931-33)

You are one of five parallel render teams (model: Sonnet). You own a few takes, render them in your own cloud container, and push them to your own branch `render22/teamK`. The director merges everything. Work autonomously and never ask for confirmation: the client delegated look approval to QA-art, and the SET gate has passed.

## 1. Setup (exactly)
```
REPO=$(git rev-parse --show-toplevel)
PROJ=$REPO/film                      # film 22 modules are path-relative; use PROJ paths
OLD=/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj
mkdir -p "$(dirname $OLD)" && ln -sfn "$PROJ" "$OLD"     # some older tools (hue_report.py) use this absolute path
pip install -q bpy numpy pillow opencv-python-headless pythainlp
python3 -c "import bpy; print(bpy.app.version_string)"   # 5.x
```
The set's texture cache is not in git. The first build regenerates it into `v3/set3d22/tex_beck/` in about 1 minute.

## 2. Read, in this order
1. PROJ/film22/shot_plan.md (your shots, the camera grammar, quotes and BIGZOOMs)
2. PROJ/film22/WORLD.md
3. PROJ/v3/set3d22/API.md: locations, `build`, cameras `key_camera('sNN', f0)`, marks, setters, join coordinates
4. PROJ/v3/set3d22/SET_GATE.md: the gate notes. Its "Instructions for the render teams" are MANDATORY.
5. PROJ/v3/set3d22/board/QA_ART.md, Round 2 "carry-forward rules"
6. PROJ/v3/cast22/API.md: members, STORY22 poses, props, `crowd_member`, `talk_mouth`, rim
7. PROJ/QA_TEAM.md §B, §G, §H, §I
8. The worked example of how a take is built: PROJ/v3/film8/s01/shot.py + QA.md + meta.json, and PROJ/v3/film8/common.py. Make your OWN helper module inside your take folder (for example `PROJ/v3/film22/sNN/c22.py`) by copying film8/common.py and switching it to cast22 and set3d22. Do not create a shared film22/common.py.
9. Look at PROJ/v3/set3d22/contact_sheet.jpg (the set gate stills of your shots) and the reference sheets in PROJ/ref_shorts/ (the target look).

## 3. Clock
- Narration: PROJ/film22/audio/narration.wav (62.66 s), laid at +0.10 s.
- Captions: PROJ/film22/script/captions.json (phrase time "t").
- 30 fps, 720x1280, film end 63.00 s (N = 1890).
- Shot boundary at narration time t is frame round(t*30). An event at narration time x is frame round((x+0.1)*30).
- Handle frames: render half the dissolve length + 2 frames beyond each dissolved or travel-joined side; use 6 if unsure.
- **Travel joins.** Your take's first frame must equal the previous take's last framing; the camera keys in API.md are shared for this. Keep the same move speed through the join.
- **Quotes.** Lip-sync is for the official ONLY, in these two windows; everywhere else mouths are still:
  - Q1: 23.57-27.44
  - Q2: 37.38-39.90

## 4. Look rules (blocking at the TAKE gate)
- **Camera always moving and eased.**
  - Push or pull 6-10 %/s plus about 40 px/s slide; never parked more than 1 s.
  - In-shot frame-diff on 90x160 grey frames: median ≥ 4, p90 ≥ 12. Write both in QA.md.
- **Characters always act.**
  - Props in hand, expression changes, secondary motion; nobody still more than 1.5 s.
  - Laughing characters bounce 0.06 D at about 3 Hz. Walks use the cast22 cycles.
- **Nothing floats.**
  - Every foot and body gets a contact shadow. No heads in the sky, no props through faces, nobody sliced by a slab or cut in half by the frame edge.
  - Paper that falls must land.
- **Framing.**
  - Whole heads above y 880.
  - No face taller than 35 % of the frame, except the planned 1-s punch-ins (s06 "ทั้งแผ่นเลย!", s10 jaw drop).
  - BIGZOOMs start with the character under 5 % of frame height and end at 35-60 %.
- **Colour and light.**
  - Per take: saturation ≥ 0.50, vivid ≥ 45 %, luma 85-110 (`python3 PROJ/qa_stats2.py take.mkv`), shade hue 240-260, magenta ≤ 10 %.
  - Motivated key light and rim light on every character (cast22 `rim`; see the API).
- **Signs.** Never mirrored, and readable at 360x640. Nothing in the caption band (y 880-950).
- **Sharpness.** No depth of field and no blur.
- **Tone.** Comic and gentle; nobody is hurt.

## 5. Deliver (per take sNN, folder PROJ/v3/film22/sNN/)
- **Files:**
  - `shot.py`
  - `meta.json`: g0, g1, first_g, n_frames, and transition_in {"type": "cut"|"dissolve"|"travel"|"match", "frames": n} from the plan's "trans in" column
  - `cues.json`: SFX cue suggestions with times
  - `contact.jpg`
  - `QA.md`
  - `QA_AUTO.md`
  - `phone_sheet.jpg`
  - `take.mkv`: all final frames including handles. Encode with `ffmpeg -framerate 30 -start_number <first g> -i frames/g_%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv`. Above 45 MB, `split -b 40M`.
- Frames, raw and work files stay out of git (add a .gitignore).
- **Before delivering:**
  1. Run `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <planned cut g's>` and fix every FAIL.
  2. Check every frame at 6 fps plus every cut ±3 frames against section 4 yourself. Also check continuity with the neighbouring takes: the last framing of the previous take and the first of the next.
- **Render settings:**
  - Draft first at 360x640 with 6 samples, look at it, fix, then render the final.
  - Final: 720x1280, 12-14 samples with denoise. Container has 4 cores: at most 2 render processes with 2 threads each.
  - Run long renders detached and resumable (skip existing frames).
- **Push:** push each take as soon as it is final: `git add -A film/v3/film22/sNN; git commit; git push -u origin render22/teamK`. Retry network errors 4 times with backoff. Do not open pull requests.
- **Rules:**
  - Write only in your own take folders. Sets, cast, plan and audio are read-only. Change a set at runtime from shot.py (hide, move or add objects), never by editing the set module.
  - No paid APIs and no MCP tools; only git and pip on the network.
- **Final message:** a short report: takes delivered, frame ranges, seconds per frame, the QA numbers, and anything that differs from the plan.

## 6. Teams
| team | branch | takes | location | key takes (QA-art TAKE gate) |
|---|---|---|---|---|
| 1 | render22/team1 | s01, s04, s05 | hq lodgings NIGHT | s01 (hook) |
| 2 | render22/team2 | s02, s15 | london DUSK/NIGHT (+ publicity window and interior for s15) | s02 (BIGZOOM 1), s15 (BIGZOOM 2, ending) |
| 3 | render22/team3 | s06, s07, s08 | hq publicity + corridor; Q1 lip-sync in s06 | s06 (Q1) |
| 4 | render22/team4 | s03, s09, s10 | under: shaft, tunnels, platform, ticket hall; Q2 lip-sync in s09 | s03 (BIGZOOM 1), s10 (turn) |
| 5 | render22/team5 | s11, s12, s13, s14 | carriage, mapworld, ticket hall | s11-s12 (reveal) |
