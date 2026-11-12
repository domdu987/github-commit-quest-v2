# v3: the first 5 seconds in true 3D (Blender 5.3 as a Python module, Cycles CPU)

Everything lives in `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/`. v2 is imported read-only (puppet, acting helpers).

## What changed against v2

v2 shot a flat front-elevation painting with a 2D zoom and pan. v3 renders every frame in a real 3D room:

| | v2 | v3 |
|---|---|---|
| Set | one SVG painting | `set3d/office3d.py`: 46 objects with thickness, artwork from the v2 drawing code as textures |
| Light | painted | one hard sun through the window (0.45 degrees), violet ambient as emission, bulbs that bloom; real ray-traced cast shadows |
| Actors | SVG puppets in the page | the same v2 puppets, rasterised per frame to a sprite on a card standing in the room: emission only (never lit), casting a hard shadow, occluded by furniture |
| Camera | 2D zoom and pan | a 22 mm camera that moves through the room: raking insert, low angle, high angle, whip pan |
| Per frame | 0.1 s (Chromium) | about 5 s (Cycles, 12 samples, 720x1280) |

## Folders

| Path | What |
|---|---|
| `set3d/` | the office (reviewed): `office3d.py`, `API.md`, `REVIEW.md` |
| `stage/` | puppets on cards, camera rig, render loop (reviewed): `actors.py`, `sprites.py`, `camrig.py`, `render.py`, `API.md`, `REVIEW.md` |
| `shots/` | this film: timing, staging, render driver, post, captions, QA tools (below) |
| `out/` | `proto_v3.mp4`, `frames/` (finished picture frames, no captions), `raw/` (Blender frames + `meta/` per-frame json), sheets, `sfx_cues.json`, `QA.md` |
| `tmp/shots/` | drafts, sprites, logs, measurement passes |
| `make.sh` | the whole pipeline in order |

## Pipeline

```
audio/th/hook_timing.json ──> shots/timing.py ──> shots/film.py (camera, acting, track state per output frame g)
                                                      │  stage/sprites.py: v2 puppet pose -> PNG sprite (Chromium), per frame
                                                      ▼
                           shots/render_all.py A|B ──> out/raw/f_%04d.png + out/raw/meta/g_%04d.json   (Cycles, every frame in 3D)
                           shots/render_layers.py  ──> out/raw/plate/, out/raw/matte/  (the fast frames only: set without actors, actor matte)
                           shots/post.py           ──> out/frames/f_%04d.png   (camera streak on the fast frames only; actors stay sharp)
                           shots/finish.py         ──> out/proto_v3_silent.mp4 (Thai captions, proj/assemble.py) ──> out/proto_v3.mp4 (+ narration)
                           shots/sheets.py, cues.py, qa_*.py ──> sheets, sfx_cues.json, numbers for QA.md
```

Run it all: `sh make.sh` (12 samples). Or step by step from `shots/`:

```
python3 timing.py                                   # prints every beat frame derived from the Thai timing file
python3 probe.py A 0:72:4                           # staging numbers without rendering: camera, heads, registration
python3 stills.py B 100,125 0.5 6                   # quick 360x640 stills into tmp/shots/stills
python3 render_all.py A ../out/raw --samples 12 --threads 2 &     # final frames, take A (g 0..72)
python3 render_all.py B ../out/raw --samples 12 --threads 2 &     # final frames, take B (g 73..149)
python3 render_layers.py A ../out/raw               # plate + matte of the frames post.py will streak (18 frames)
python3 post.py ../out/raw ../out/frames
python3 finish.py ../out/frames ../out
python3 sheets.py ../out/proto_v3.mp4 ../out
python3 cues.py ../out/sfx_cues.json
```

`render_all.py` can be interrupted and started again: a frame counts as finished only when its PNG and its `meta/g_%04d.json` both exist (the json is written after the PNG is complete) and were rendered with the current timing file, scale and sample count. `--frames 50:60` renders a range, `--force` renders again.

## What is done outside Blender (`shots/post.py`, `shots/finish.py`)

- Camera streak. For every frame the true camera of g - 1, g, g + 1 is projected onto reference points of the set and a similarity (zoom + pan) is fitted; where it moves a frame corner by more than 60 px per frame the picture is averaged along that motion over 0.4 frame. In the whip pan (6 frames around the cut) the whole frame is streaked. On the other fast frames (snap push, pull-out, snap on the jab: 18 frames) only the plate is streaked: `render_layers.py` renders the same 3D frame without the actors (their shadows stay) and an actor matte (the set as a holdout), and the actors of the film frame are laid over the streaked plate sharp, as the reference does.
- Captions last (`proj/assemble.py` with the Thai phrases and the `caption_style_prefix` of the timing file), then the narration WAV delayed by `audio_offset`.
- Bloom, grade, shadows, depth and every camera move are rendered in Blender; nothing is painted.

## How the film is described (`shots/film.py`)

- Output frame `g` is 0-based (time `g / 30`); the Blender frame is `g + 1`.
- `timing.load()` turns the Thai phrase list into beat frames: `g2` (first beat-2 phrase minus 3 frames), `g3` (first beat-3 phrase minus 3 frames, the cut), `g_jab` (first frame inside the phrase that names New York), `g_touch` (start of the phrase that says "erased"), `g_last`, `g_done`, `N`. Every constant in `film.py` (`SNAP1`, `PULL`, `GATHER`, `SNAP2`, `TURN`, `WHIP_OFF`, `WHIP_ON`, `SHOCK`, `SNAP3`) is an offset from those, so a new narration moves the whole film.
- A take is one continuous camera in one scene. Take A (`g 0..g3-1`) holds shots 1 and 2 (the raking insert and the low-angle medium are joined by a real 14-frame pull-out that swings round the hero, no cut); take B (`g3..N-1`) is shot 3. The whip pan is the last 4 frames of A and the first 7 of B.
- Pure functions of `g` give the state: `line_at(g)`, `erase_at(g)` (red track), `cam_a(g)` / `cam_b(g)` -> (camera position, look-at), `hero_a(g)`, `boss_b(g)`, `hero_b(g)` (v2 puppet poses), `tip_a(g)`, `eraser_b(g)` (world targets of the pinned props). Easing comes from `v2/shots/anim.py` (`keys`, `ease`, `blink`, `pulse`).
- `Film(take)` builds the set (`office3d.build`), the camera, the actors (`stage.actors.Actor`), keys camera and track for every frame. `Film.pose(frames)` solves the pinned hands for the camera of each frame and rasterises the sprites; `Film.render(frames, dir, ...)` renders; `Film.report(g)` returns camera height, pitch, head sizes and positions, registration.
- Registration: the pencil point (take A) and the eraser face (take B) are world points on the map (`office3d.track_point(u)`); `actors.world_to_local` cuts the sight line with the actor's card and the arm is solved to that point, so the tip covers the target exactly although the card stands in front of the wall. In the insert the hero's card is turned so that it passes through the pencil point (`card_yaw_a`), which makes the pencil really touch the map and puts its shadow next to it.
- The head's thick ink side and its crescent point away from the key light: the sun comes from screen-right, so sprites are drawn with `actor.head_flip = True` (a small addition to `stage/sprites.py` and `stage/actors.py`; default off, API unchanged).

## How to add a shot

1. Timing: add or tag the phrase in the timing file, and derive the shot's first frame in `timing.py` (a new key such as `g4`).
2. In `film.py` add a take: an entry in `TAKES` (`"C": (g_first, g_last)`), a camera function `cam_c(g) -> (loc, look_at)` built from `keys(...)` (use an anchor camera from `office3d` `A["cams"]` or `stage.camrig.cam_for(subject, head_px, "low" | "eye" | "high")` as the starting pose, keep the camera out of the furniture boxes listed in `set3d/API.md` section 4), pose functions for the actors, and a branch in `Film.__init__` (actors, `place`), `Film.pose` and `Film.apply`.
3. Stage with numbers before rendering: `python3 probe.py C a:b:4` prints head width (aim for 180 to 310 px), head centre (0.35 to 0.59 of the frame height, whole head above y = 880), near / far head ratio (1.36 to 1.46 for a two-shot), registration error (0 px while a prop is pinned; an error above 0 means the arm cannot reach: move the actor or change the prop angle).
4. Block: `python3 stills.py C a:b:3 0.5 6`, `python3 sheet.py <dir> sheet.jpg a:b:3`, look at the sheet. Then the full draft with `render_all.py C <dir> --scale 0.5 --samples 6` and `python3 popcheck.py <dir>`.
5. Camera rules to check with `python3 qa_motion.py`: a framing change every 0.6 to 1.6 s, never static for more than 6 frames (mix a constant-speed share into the keys as `cam_b` does with `CREEP`), never linear.
6. Final: `render_all.py C ../out/raw --samples 12 --threads 2`, then `post.py`, `finish.py`. Add the take to `post.py` (it loops over `film.TAKES`) and its cues to `cues.py`.
7. A transition between two takes is either a whip (end the first with an accelerating pan, start the second panned the same way and braking, as `WHIP_OFF` / `WHIP_ON`; `post.py` streaks the fast frames by itself) or a dissolve mixed from handle frames outside Blender.

## QA tools (`shots/`)

| Tool | Measures |
|---|---|
| `probe.py` | staging numbers without rendering |
| `popcheck.py <frames>` | frame-to-frame change, pops, near-still runs |
| `qa_motion.py` | camera speed per frame from the true camera path: moves (start, peak, end), static runs, linear runs, height and pitch per shot |
| `qa_light.py <dir> <g,...>` | measurement passes of film frames: same-surface shade / lit ratio, hue shift, cast-shadow edge width, the actors' own shadows, shadow on the track |
| `qa_parallax.py ref` / `seq <frames>` | share of frame pairs 0.5 s apart that a flat 2D zoom or pan explains (similarity against fundamental-matrix inliers), calibrated on the reference stills |
| `qa_regcrops.py` | 3x crops of rendered frames around the registration targets |
| `qa_trackend.py` | end of the red ink found in the actor-free plates against the registration target |
| `qa_captions.py` | caption boxes on the MP4 and their distance to the heads |
| `qa_report.py` | the tables of `out/QA.md` |

Results: `out/QA.md`.
