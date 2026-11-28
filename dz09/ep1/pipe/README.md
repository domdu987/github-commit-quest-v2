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

## Scene 02 integration (2026-11-28)
- **Production cut** `cut/sc02.json` is built by `cut_timed.py --scene 02` from `plan/shots_ep1_timed.json` + `audio/narr_ep1_timing.json`
  (+ `cut/sc02.cfg.json`): the timed frames exactly (1776 frames, film 1280-3056), 55 captions, `narr0 = -53.3333` because
  `narr_ep1.wav` starts at film time 0, and a new key `film_f0` (1280). The plan-estimate table is kept as `cut/sc02_plan.json`.
  It equals the authors' private tables (`chk/a25`, `chk/sc02b`, `chk/sc02c`) frame for frame; `cut/mouth_sc02.json` was built by
  `mouth.py --scene sc02` from the episode wav and equals theirs level for level. `cut.py` is not used for EP.1 any more: its
  picture-beat rule differs from the timed one by a few frames on S35, S36, S44-S47, S58.
- **cfg** `cut/sc02.cfg.json`: hard cut on S050 (moot: every cut is straight since the 11-28 decision), the plan's ONE red frame on
  the cut into S049 (`fx` flash at scene 49.75 s), cue `eyes_open`, the scene mix `ep1/audio/sc02/mix_sc02.wav`.
- **stage_ep**: `build()` now wraps the hook Stage's `begin()`: every actor gets back the card pitch it was BUILT with and loses its
  walk lock before the hook's reset and the shot's `setup()` (the hook resets the seated driver only). `stage.Act.__init__` is
  wrapped once per process to remember that pitch, also for actors a shot creates lazily.
- **finish_ep**: `--ass <episode .ass>` takes a scene's captions verbatim from the episode caption file (events in the scene's film
  window, moved to the scene clock); `--sheet-u 0.5` (one frame per shot, bigger cells) and `--sheet-t-off S` for the sheet.
- Scene-02 draft conform with the hook's last 3 s: `finish_ep.py comp --scene sc02 --tier draft --size 720x1280 --base-size 360x640`,
  then `finish_ep.py master --hook PROJ/v10/film/DZ09_EP1_hook_916_v1.mp4 --hook-tail 3 --scenes sc02 --tier draft --size 720x1280
  --base-size 360x640 --ass PROJ/ep1/audio/captions_ep1.ass --out out/sc02_draft.mp4`.
- Shot-module fixes made in integration are marked `integration 11-28` in the modules (see the scene-02 report).

## USER DECISION 2026-11-28: cast stays the 2.5D paper puppets
A blocky 3D cast was tested (v16/block) and shelved by the user. Keep the puppets of ep1/cast and v8/cast. See spec/blocky_cast_decisions.md.

## USER NOTES ON THE FIRST SCENE 02 DRAFT (2026-11-28, sc02_draft.mp4 of 14:47) — must be fixed and checked
- S054 "มันมองไม่เห็นเขา": the infected junior's face sinks into the rescue truck (his head card is behind / inside
  the truck's side panel). His whole head and face must be in front of the truck body and fully visible; check every
  frame of the shot, and every other shot where a puppet stands close to a vehicle, wall or barrier, for the same fault.
Director's own notes on the same draft (fix too): S035 and S041 inserts do not read (an orange blob, a dark shape);
S029 a black figure covers almost half the frame in the foreground; S027 the driver's legs look broken in the throw;
S058 Kong's face is cut by the frame edge; S049 the turned junior grins with fangs and may read comic, he must read
frightening (open snarl, white eyes, no smile). The countdown narration (s17-s30) runs at tempo 1.10: flag if it sounds rushed.

## USER DECISION 2026-11-28: no logo
The biohazard title mark is removed too ("เอาโลโก้ออก"): noicons.SHOW_MARK = False. The title is text only (เขตปิดตาย 09 / DEAD ZONE 09). No logos or icons anywhere in the film. Current approved hook: DZ09_EP1_hook_916_v3.mp4 (v2 with the mark removed; frames from 1217 on re-composited, all earlier frames identical to v2).

## USER DECISION 2026-11-28: no title text either
"เอาคำนี้ออกด้วย": the title text (เขตปิดตาย 09 / DEAD ZONE 09) is removed from the hook end (finish.SHOW_TITLE = False; the navy dim under it is off too). The hook ends on the rising crane shot with no text. Current approved hook: DZ09_EP1_hook_916_v4.mp4. The copied title line was removed from ep1/audio/captions_ep1.ass. For the EP.1 master join use --hook DZ09_EP1_hook_916_v4.mp4.

## FIX PASS ON THE USER NOTES (2026-11-28, after the 14:47 draft) -- what changed, how it was checked
Every change is marked `11-28 fix pass` in the module.  Originals of the edited modules: `scratchpad/wk/orig/` (session scratch, not durable).
- **S054** (the sinking head): the half-done integration edit (`G.CROUCH + G.out * 0.45`) is the fix and is kept.  Checked by a ray-cast
  of 65 head points / 37 face points from the camera on EVERY frame (36/36): 0 hidden by the truck (old marks: 34-48 % of the head inside
  `rescue_truck_body` / `canopy`), and by looking at all 36 new draft frames and the final-tier gate still.  `out/s054_fix.png`.
- **S049 / S050 / S051 / S055** (the turned junior grins): new `shots/sc02/sc02_faces.py` adds the expressions `z_snarl` / `z_snarl_o`
  (white snapped eyes with veins and red pin pupils, brows hard down, an ARCH mouth: lip up, corners down, black inside, two jagged rows
  of teeth, no tongue, creases).  Nothing existing is changed (draw8's `snarl` / `bite` are a D-shaped laugh with a pink tongue).
- **S035**: 200 mm, pad higher in frame; PPD 1140 at the final tiers for ALL step actors (they were made in setup() after begin()
  applied PPD, so four of the five steps rastered at 240 ppd); drafts keep 780.
- **S041**: re-staged from the lane south of the junior (front drawing): black glove on the orange jacket hem and white band, not on
  black trousers against the black tyre; cone_3 sunk for this shot (it stood in the lens line).
- **S029**: camera 7.2 D back (was 3.75), driver at the tail's left corner: about a third of the frame high, not half the frame.
- **S027**: the thrown driver: legs trail together, knees bent (was the scissored `step` legs crossing at the knee on a tipped card).
- **S030**: the 5-frame whip now lands on Kong and the junior (it landed on the empty wreck door with both of them cut at the edge).
- **S055**: camera z 2.80 (was 1.75): at the gate the rider's foot stood on the junior's crown.
- **S057**: 21 mm aimed 1.6 D left: the junior ran along the left edge with his face off frame.
- **S058**: 3.35 D (was 2.85) and the head higher: the hair touched both edges.
Collision sweep: ray-cast heads / faces / hands of every visible puppet in every 3D shot, every 3rd-4th frame (light-cone volumes
ignored; 36/36 frames for S054).  Remaining set hits are hands only, plus far crowd figures in S059 / S060 passing behind car bodies
between the lanes (they are 20-50 px high, the plan's "waist up over the bonnets").
Gate: 37 frames at final tier 720x1280 (`run_ep.py --frames ... --tag gate`, 4 processes) -> `out/sc02_gate_final.png`.
Final-render estimate from the gate (scratchpad `wk/estimate.py`): A 24 shots / 1152 f, gate 49-107 CPU s (median 73), steady ~66;
B 9 / 441 f, 33-98 (median 41), steady ~40; C1 4 / 183 f, 0.5-8 CPU s.  Scene 02 = 26-30 CPU h = 6.9-8.0 h wall on 4 workers.
Draft 360x640 complete again: 1776 / 1776, every shot's sig matches its current module.
