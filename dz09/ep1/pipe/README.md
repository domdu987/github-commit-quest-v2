# ep1/pipe: the hook pipeline generalised to a multi-scene episode

Nothing in `v10/film`, `v11` or `v8` is edited: they are imported. `PROJ` = the `dz09` folder, `PIPE` = `PROJ/ep1/pipe`.
Proved end to end on a dummy scene (`sc99`, 60 frames); no EP.1 scene has been rendered through it yet.

## Files

| File | What it does |
|---|---|
| `epcommon.py` | Scene timing (no bpy): loads a cut table, `activate("sc02")` points v10's `common.shot_range / shot_of / word / mouth` at the scene so `stage.Stage` and `shots/base.py` work unchanged; shot-module loader; render classes |
| `cut.py` | **Shot-table tool**: `plan/shots_ep1.json` + a caption-timing file -> `cut/scNN.json` (cut-on-word). Without `--timing` it uses the plan's estimated times |
| `mouth.py` | **Mouth envelope** from a narration wav -> `cut/mouth_scNN.json`; speaker per sentence; synthetic envelope when there is no wav |
| `epbase.py` | Base of 3D shot modules: everything of the hook's `shots/base.py` + `W(caption)`, `CUE(name)`, `talk(actor, g)`, `speaker(g)`, `T0(F)` |
| `ep2d.py` | Base of class C1 shots (drawn frames): `Ctx`, `font`, `rain`, `vignette` |
| `stage_ep.py` | `LOCATIONS` / `CAST` registries; `build(loc, tier, W, H, ...)`. Only `X1` (the hook's stage) is registered |
| `run_ep.py` | Renderer: per scene / shot / frame range, tiers, classes, workers, supervisor, resume, logs, manifests |
| `finish_ep.py` | Conform: `scene` (comp + captions + audio + encode), `master` (hook mezzanine + scenes), `sheet`, `missing` |
| `backup.sh` | Source + audio archive without frame folders, under 150 MB, into `PROJ/ep1/backup/` |
| `cut/sc02..sc06.json` | The five scenes' shot tables **from the plan's estimates** (identical frame numbers to `shots_ep1.json`) |
| `cut/sc99.json`, `sc99.cfg.json`, `mouth_sc99.json`, `sc99_plan.json` | The dummy scene: table from its "recording", its cfg, its mouth track, and the plan-estimate table for comparison |
| `dummy/` | `make_dummy.py` (dummy plan, timing, placeholder audio: numpy buzz, not a voice) and what it wrote |
| `shots/sc99/s901.py s902.py s904.py s903.py` | Three 3D shots on the hook set and cast, one drawn C1 insert |
| `proof.mp4`, `proof_sheet.png` | The dummy scene conformed (60 frames, 2.5 s, 720x1280 from a 360x640 draft) |
| `proof_master.mp4`, `.json`, `.ass` | Master conform test: the last 3 s of `v10/film/draft_v3.mp4` + the dummy scene |
| `out/` | Frames, logs, manifests (not in the backup, except logs and manifests) |

Shot modules and cut tables are looked for in `PROJ/ep1/shots`, `PROJ/ep1/cut` first, then here. Frames go to `PIPE/out` unless
`DZ09_EP1_OUT` is set.

## Clocks

- A scene's frames are **scene-local** (0-based, end exclusive). Files are named by the frame **within the shot**: `<SHOT>/f_0001.png`.
- The stage frame is `g = g_base + local`, `g_base = scene number x 10000` (sc02 = 20000). A shot's `frame(F, g, t, u)` gets `t = g / 24`.
  `W("caption")` and `CUE("name")` answer on that same clock, so `ramp(t, W("ก็ลืมตา") - 0.2, W("ก็ลืมตา"))` is correct whatever the recording does.
- Re-timing one scene never renames or invalidates another scene's frames.

## Adding a scene

1. **Timing.** Record the scene; write `PROJ/audio/ep1/sc02/captions_timing.json` in the hook's shape
   (`[{"id": "s17", "text": "เหลืออีก", "t0": 0.0, "t1": 0.63}, ...]`, seconds from the start of the narration wav). Every caption of
   `narration_ep1.json` must be there with the same sentence id and text, or `cut.py` stops and lists what is missing.
2. **Cfg** (optional) `cut/sc02.cfg.json`: `narr0` (lead-in before the wav; default = the plan's), `mix`, `narration_wav` (paths from PROJ),
   `hard_cuts` (shots that START on a hard cut; all other cuts get the hook's 3-frame blurred push), `cues`
   (`{"bite": {"word": "...", "sid": "s35", "dt": 0.1}}` or seconds), `pin` (`{"S36": {"word": "30 วินาที", "dt": -0.3}}` or `{"S47": {"t": 46.0}}`),
   `fx` for the conform (`flash`, `fade_out`, `fade_in`, `dim`, each on a `word` / `cue` / `t`), `end`.
3. **Shot table.** `python3 cut.py --scene 02 --timing PROJ/audio/ep1/sc02/captions_timing.json` -> `cut/sc02.json` and a printed table
   (frames per shot against the plan, the rule each cut used, short-shot warnings, the scene's new CPU-hour estimate).
   It first checks that `shots_ep1.json` and `narration_ep1.json` name the same captions and stops, writing nothing, when they do not.
   Rules: first shot at 0; a shot whose `cut_on` is one of its captions starts on that caption; a picture-beat shot keeps the plan's
   proportion between the word cuts round it; the scene ends at the last caption + the plan's tail; a `pin` overrides.
4. **Mouth track.** `python3 mouth.py --scene sc02 --wav PROJ/audio/ep1/sc02/narr_final.wav`. Run it again after every `cut.py`;
   a track older than the cut (other length or caption timing) is never used: it is rebuilt in memory from the same wav, with a warning.
5. **Shot modules** `PROJ/ep1/shots/sc02/s025.py` (S25 of the plan is `S025` here):

```python
from epbase import *
CLASS = "A"            # optional: the cut table's class is used when absent.  A 100 %, B 75 %, C2 75 % + 4 spp at the final tier
LOC = "X1"             # optional: the cut table's set
PPD = {"kong": 420}    # as in the hook; PCT / SPP dicts override the class
def setup(F): ...
def frame(F, g, t, u):
    F.camera(...)
    kong_phone(F, t, g, F.PM, face, view="front", talk=False, **talk("kong", g, "o"))   # mouth moves only on Kong's own lines
    return {"exposure": 1.6}
def late(F, g, t, u): ...
```

   A class **C1** shot imports `ep2d` instead and has `draw(ctx) -> PIL image` at `ctx.W x ctx.H` (`ctx.k, n, u, g, t, scene, frame_path(shot, k)`).
6. New sets and characters register themselves: `stage_ep.LOCATIONS["CAB"] = builder`, `stage_ep.CAST["praew"] = adder`; a module names them in `LOC` / `CAST`.

## Rendering

```
python3 run_ep.py --scene sc02 --tier draft --size 360x640 --spawn 2          # supervisor: niced workers, restarts a dead one up to 3 times
python3 run_ep.py --scene sc02 --tier final --size 720x1280 --spawn 4
python3 run_ep.py --scene sc02 --shots S025,S026 | --frames 120:180 | --shots S031 --at 0.5 --tag look
python3 run_ep.py --scene sc02 --tier final --size 720x1280 --status          # done / missing per shot, CPU per frame; writes manifest.json
```

- Order inside a worker: C1, then B and C2, then A. Workers share shots in blocks of 6 scene frames (`--worker i/n`).
- One location per Blender process; a worker whose frames span several locations runs one child per location.
- Frame = done when the PNG opens at the asked size. PNGs are rendered under `.tmp_w<i>_p<pid>_...` and renamed; on restart only the
  leftovers of DEAD processes are removed.
- One live supervisor and one live worker per slot `i/n` of an output folder (`.supervisor.lock`, `.worker_<i>of<n>.lock`, held by the
  process, dropped by the kernel when it dies). A supervisor that is killed leaves its workers rendering (they are their own sessions);
  a second `--spawn` then refuses to start (exit 4) and names their pids instead of rendering every frame twice.
- A shot whose START moved in the scene (same length, same words) keeps its frames when it is complete; a partly rendered one is purged,
  because its remaining frames would be on a shifted stage clock (shake, on-twos phase, blinks).
- `sig.json` per shot: hash of the module + `epbase.py` + `ep2d.py` (+ a module's `DEPS` files), frame count, class, tier, size, pct, spp, levels,
  and every word / cue / mouth value the shot actually looked up, relative to the shot's first frame. If any of it changed the shot's frames are
  purged and rendered again (`--keep-stale` to refuse). A re-timed scene therefore re-renders only the shots whose length or looked-up words moved.
  Changes in `v10/film`, `v11`, `v8` are NOT in the hash.
- `log_<worker>.jsonl`: one line per frame: `cpu` (CPU seconds of the process and its children for the frame), `wall`, `stage`, `cpu_render`, `cpu_post`,
  `pct`, `spp`, `heads`; a `_build` line per stage build.

## Conform

```
python3 finish_ep.py scene  --scene sc02 --tier draft --size 720x1280 --base-size 360x640 --out sc02_draft.mp4 --sheet sc02_sheet.png
python3 finish_ep.py scene  --scene sc02 --tier final --size 720x1280 --out PROJ/deliver/ep1_sc02_v1.mp4
python3 finish_ep.py comp   --scene sc02 --tier final --size 720x1280 --worker 0/2      # comp can be split
python3 finish_ep.py master --hook PROJ/deliver/ep1_sc01_hook_final.mp4 --scenes sc02,sc03,sc04,sc05,sc06 --tier final --size 720x1280 --out PROJ/deliver/ep1_master_v1.mp4
```

- Captions: the hook's style (Kanit Black 88, white, 5 px outline, centre at y 900 of 1280); a caption with an `emph` word from `narration_ep1.json`
  colours that word amber or red and pops 12 % for 3 frames. No icons are drawn anywhere.
- Audio: the cfg's `mix`, else the narration wav at `narr0`, else silence; one static gain to -14 LUFS with the encoded true peak <= -1 dBTP.
- A C1 shot is drawn again at the conform size when the draft was rendered smaller.
- Master: the hook mp4 is decoded and re-encoded together with the scenes' finished frames (captions burnt per scene) in one CRF 15 encode;
  the audio is the hook's track + the scene mixes at their scene gains, then one gain over the whole. `--scene-mp4 sc02=file.mp4` uses a scene
  mezzanine when its frames are gone; `--hook-tail S` is for tests.
- Encode: libx264 CRF 15, tune animation, preset slow, yuv420p, AAC 320 kb/s.

## Backup

`bash backup.sh [label]` -> `PROJ/ep1/backup/dz09_src_<date>_<label>.tar.gz` + `.manifest.txt` + `.sha256`. Source and text under 3 MB a file, fonts,
`uploads/`, `tex/` folders, manifests and logs, then audio folders in order of value while the total stays under the limit (`LIMIT_MB`, default 150).
It fails with exit 3 if the archive is over the limit. Nothing is sent anywhere.

## Measured (dummy scene, draft 360x640, 2 spp, 2 workers while the hook final ran on all 4 cores)

| | |
|---|---|
| Class B frame (S901, 14 frames) | 10.5 CPU s, 10.7 wall s |
| Class A frames (S902, S904, 31 frames) | 11.5 CPU s, 11.7 wall s |
| Class C1 frame (15 frames, 360x640) | 0.11 CPU s |
| Stage build per worker start | 28-33 CPU s (paid again on every restart and for every location) |
| Scene conform (60 frames to 720x1280, encode, sheet) | 17 s wall |
| Backup | 88 MB, 906 files, 16 s |

Checker's re-run (same tier, 2 workers, machine load 7-9): B 12.5 CPU s, A 11.6 CPU s, C1 0.11 CPU s, stage build 34 CPU s;
wall was 26-29 s a frame and 80 s a build under that load. All 60 re-rendered frames are bit-identical to the first run's.

Final tier, three single stills through `run_ep.py --at 0.5` (`proof_final_stills.png`): class B S901 rendered at 75 %, 5 spp, 47.2 CPU s;
class A S902 at 100 %, 73.7 CPU s; class A S904 at 100 %, 75.5 CPU s. Each is the FIRST frame of its shot in the process (it pays the
middle-frame staging and the puppet raster), so they sit above the plan's 36.6 / 68.2 CPU s steady-state figures and do not replace them.

Restore test: the backup archive unpacked to an empty folder rendered S902 k=8 and S903 k=7 (draft) bit-identical to the originals.

## Not done / weak

- Only three final-tier stills went through `run_ep.py` (B at 75 %, A at 100 %: confirmed in the log). No final-tier SEQUENCE and no
  class C2 shot (4 spp) has run.
- `cut/sc06.json` is from the plan as it stood at 07:40. `plan/narration_ep1.json` was changed at 10:25 (s101 'แต่เขาจะฟาด' -> 'แต่เขาจะหวด')
  and `plan/shots_ep1.json` (S159) was not: `cut.py --scene 06` now stops and says so. Rebuild sc06 once the two plan files agree.
- `stage_ep` has one location and the hook's four actors. The multi-location child-process path and `CAST` builders are written, not run.
- The plan's gate "the hook re-conforms through the new finish to the same picture" was not attempted: the hook is taken as a finished mp4,
  so in the master its picture is a second-generation encode. Joining from the hook's frame folders is not implemented.
- The master test used a draft of the hook and 3 seconds of it; the full 5-minute join has not been run. Scene boundaries are hard cuts.
- The lip sync follows loudness only (five mouth drawings), as in the hook; it was checked on stills, not in playback. A sentence's
  frames run from its first caption's start to its last caption's end.
- The watch drawing in `s903.py` is a sketch to prove the C1 path, not the plan's watch card.
- The dummy "recording" is hand-written timing; `cut.py` has not seen a real EP.1 recording. A simulated one (every caption 0.8-1.3x) rebuilt sc02 without error.
- The stale purge trusts the recorded look-ups: a shot that reads timing some other way (a literal second) is not caught.

## USER DECISION 2026-11-28: cut like a film (do not revert)
The user: "every time the camera angle changes there is a quick zoom into the character; it is not like a film".
- NO zoom push / radial blur across cuts. finish.py and ep1/pipe/finish_ep.py now have JOIN = [0, 0, 0]: every cut is a straight cut.
- NO fast camera start. Do not open a shot with ease_out(...) on a camera push, dolly or lens change (it starts fast and settles,
  which reads as a snap zoom right after the cut). Use smooth(...) (ease in and out) or a slow linear move; a push changes the
  subject size by at most about 10 % over the whole shot, and by under 2 % in the first 6 frames.
- No snap zooms or punch-ins except a single, motivated story beat the plan names (none planned in EP.1). Static and slow moves
  are the default, like live-action cinema. Shake only where the plan says handheld, and it settles without a push.
