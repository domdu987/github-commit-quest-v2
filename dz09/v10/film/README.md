# v10/film: DEAD ZONE 09, EP.1 hook film (53.32 s, 24 fps, 1280 frames) as shot scripts

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Everything here is code-drawn or code-built.
The set is `v11/set` (imported; its post has the v12 clarity levels), the cast is `v8/cast` in flat mode (imported; its raster cache stays in `v8/cast/tmp`), the on-screen graphics are the gauge tubes of `v12/gauge` (the v4 icon pops are gone), the cut is `v4/animatic/timing.py`, captions are `audio/narr_v1/preview_v2.ass`, the mix is `audio/narr_v1/mix_v3.wav` (v2; `mix.wav` is the v1 mix).

**Current draft: `draft_v3.mp4`, `draft_v3_sheet.png`, `v3_stills_720.png`, `line_test_720.mp4`, `line_test_crop.png`** (see "Draft v3" at the end; it overrides whatever the older sections say about gauges, captions, mix and levels). `draft_v2.mp4` and `draft_v1.mp4` are kept; their frames are in `out/draft_v2_360x640` and `out/draft_v1_360x640`.

## Files

| File | What |
|---|---|
| `common.py` | paths, the cut (`shot_range`, `shot_of`), easing, the narration envelope (`mouth(g)` lip-sync level, offset 0.30 s), `blink`, handheld `shake` |
| `stage.py` | `Stage`: builds the set and cast once; `Act` puppet wrapper (pose cache, camera-facing cards without re-rastering); props (radio, phone with Thai screens, 3D cutter jaws / LEDs / glove, sparks); `door()`, `lamp()` (glare-safe work lamp), `foreground()`, `camera()`, `shadows()` |
| `shots/base.py` | staging shared by shots (Kong at the cutter, Kong on the phone, crew at the door, seated driver, the attack loop) and cue times |
| `shots/s01.py` .. `s24.py` | one module per shot: `ID`, optional `setup(F)`, `cam(F, g, t, u)`, `frame(F, g, t, u)` (camera, acting; returns post options), `late(F, g, t, u)` (lamp, shadows, foreground: needs posed actors). The title is the tail of `s24.py` (camera keeps rising) plus the plate in `finish.py` |
| `run.py` | the runner (below) |
| `cutter.py` | the drawn cutter as a two-handed tool: `prop_svg` (rear D-handle, fore grip with the far glove on it, battery box, jaws) and `hold(spec, view, s, grip, tilt)` -> `arm_n`, `arm_f`, `prop_n`. `base.kong_cutter(grip=, tilt=)` uses it |
| `cues.py` | picture cues of the finish (static, lunge flash, bite, title), hard cuts, the strip box |
| `finish.py` | shot joins (blurred push), radio static, lunge and bite flashes, title plate, then the flat v13 icon strip + title mark (drawn at the output size after all blur); Ohm captions + Ohm mix; contact sheet. `--base-size 360x640` finishes a small render at a larger `--size`; `comp --worker i/n` runs in parallel |
| `stills_sheet.py` | final-tier stills with gauges and captions on them as one sheet (`v2_stills_720.png`) |
| `tex/` | phone screens (`screen_missed.png`, `screen_ended.png`, ...), `thai_glyph_check.json`, avatar |
| `out/<tier>_<W>x<H>/<shot>/f_####.png` | frames after the set's post (`####` = film frame + 1) with `f_####_depth.png` (16-bit); `comp/` = finished frames; `log_*.jsonl` = per-frame CPU and glare log |

## Rendering

```
python3 run.py --shots S06,S07                         # whole shots, draft tier at 360x640
python3 run.py --frames 266:302                        # film frames (0-based, end exclusive)
python3 run.py --shots S18 --at 0.1,0.5,0.9            # stills -> out/<tier>_<size>/stills/
python3 run.py --all --tier final --size 720x1280      # the whole film at final quality
python3 run.py --all --size 640x360                    # 16:9: the aspect comes from the size
for i in 0 1 2 3; do python3 run.py --all --threads 1 --worker $i/4 & done      # 4 workers (fastest on 4 cores)
python3 finish.py all --tier draft --size 720x1280 --base-size 360x640 --out draft_v2.mp4 --sheet draft_v2_sheet.png   # v2 conform
python3 stills_sheet.py --tag v2 --out v2_stills_720.png      # after run.py ... --tier final --size 720x1280 --tag v2
```

- Resumable: a frame whose PNG exists is skipped (`--force` re-renders). Frames are a pure function of the frame number, so any range can be rendered in any order by any number of workers.
- `--keep` keeps the EXR passes (`_rgb/_z/_idx/_env.exr`, `_info.json`, `_shafts.pkl`), so `render11.repost(out_noext, key=value)` can re-grade without rendering.
- `--levels RAIN=0.6,DOF=0.5` sets the clarity levels for the run (rain, haze, bloom, lens blur, tilt-shift, sharpening: `post11.LEVELS`, table in `v11/set/API.md`); `--levels v1` gives the draft-v1 look. A shot can also return a level as a post option (`{"RAIN": 0.7}`). `--pct 100` renders at full scale instead of the final tier's 75 % (about 66 instead of 40 CPU s per frame).
- A shot module may carry `PPD = {"kong": 420}`: sprite pixels per drawing unit for that shot (default 240). Close shots (S10, S12-S15, S21-S23) use 360-540 so the line art is not magnified; the first pose of each drawing costs 1-3 s more to raster, then it is cached.
- `stage.crack_window(on, center, r0, r1, floor)` thins the windscreen's crack web inside a soft window of the frame (S18).
- `--spp N` overrides the tier's samples. A shot module may carry `SPP = {"final": 4}`.

### Tiers

| Tier | Samples | Render size | Use |
|---|---|---|---|
| `draft` | 2 spp + OIDN | 100 % of `--size` | the full-film draft at 360x640 |
| `preview` | 4 spp | 100 % | checking a shot |
| `final` | 5 spp (4 where the shot says so) | 75 % then Lanczos (the set's final tier) | delivery at 720x1280 |
| `final8` | 8 spp | 75 % | holds and inserts if there is budget |

## Conventions

- Film frame `g` (0..1279) renders as Blender frame `g + 1`; the set's beacons (12-frame cycle = 2 Hz), hazards (20 frames), fire flicker, rain, puddle rings and splashes run from that frame number.
- Drawings change on twos (`common.on_twos`), the camera and the lip sync move on ones. Breathing is a 0.6 % stretch of the card stack about the soles (no re-raster).
- Aspect-parametric: shot scripts take every framing number through `F.pick(vertical, wide)`; icons have a 16:9 table in `cues.py`. Only 9:16 has been rendered and looked at.
- Shot joins follow reference E (a 3 + 3 frame blurred push); the lunge (S21) and S22 start on hard cuts.
- The work lamp is placed per shot with `F.lamp(...)`, which slides it away from every head (`beauty.place_work_lamp_safe`); `beauty.glare_check` runs on every frame and is logged.

## State of draft v1 (`draft_v1.mp4`, `draft_sheet.png`; kept for comparison)

- All 1280 frames rendered at 360x640, draft tier, 4 workers x 1 thread: about 9.6 CPU s per frame, 3.4 CPU h in all.
- Final tier at 720x1280, 4 threads (CPU s per frame, staging + render + post): S06 37.3-38.4, S13 37.3-37.5 inside a shot; the first frame a process renders in a shot costs about 4 s more (it stages the shot's middle frame first). Measured as first frames only: S21 34.9, S24 44.3 (4 spp).
- S19 walk: drawn soles stay within 0.06 cm while on the ground (`out/s19_feet.json`, geometry check, `tmp/feet.py`).
- Thai phone strings pass the glyph check (`tex/thai_glyph_check.json`).
- Glare log: no frame has a lamp within 0.16 W of a principal's head in a character shot; S04 (lane fly-through) has 21 frames where the work lamp passes within 0.16 W of a head.
- Not done: people inside cars; 16:9 render; a watch-through of the motion (frames and the sheet were checked, not playback).

## v12: less rain, clearer picture (after the feedback on draft v1)

`draft_v1.mp4` was rendered with the old levels. The defaults now are: rain streaks at 40 % of the count, thin, back-lit only, no near-lens sheet, nearly none over actors; haze x 0.45; bloom and halo tighter; lens blur x 0.40 with a sharp zone to 1.54 x the focus distance; tilt-shift x 0.30; a light unsharp mask. Wet road, puddles, ripples, splashes and the grade are as before. Proof and numbers: `PROJ/v12/rain_before_after.png`, `PROJ/v12/measure_before_after.json`. The film has to be re-rendered to get the new look (existing frames in `out/` are the old one; use `--force` or a clean `out/`).

## Draft v2 (`draft_v2.mp4`, `draft_v2_sheet.png`, `v2_stills_720.png`)

- All 1280 frames re-rendered at 360x640, draft tier, with the v12 clarity levels (less rain, less haze and lens blur), 4 workers x 1 thread: 9.75 CPU s per frame, 3.5 CPU h. Frames: `out/draft_360x640/`; the v1 frames moved to `out/draft_v1_360x640/`.
- Conform: `finish.py all --tier draft --size 720x1280 --base-size 360x640 --name comp_v2` -> the picture is the 360x640 render scaled up (Lanczos), the gauge tubes and captions are drawn at 720x1280, audio is `mix_v3.wav` (-14.0 LUFS). Finished frames: `out/draft_from360x640_720x1280/comp_v2/`. Gauge safe report: no problems, one tube at a time.
- `v2_stills_720.png`: S03, S06, S13, S18, S20, S23 at the final tier (720x1280, 5 spp, 75 % render scale) with gauges and captions; 32.7-41.5 CPU s per frame (mean 37.4, first frame of a process in each shot).
- Shot changes: S04 extras stand ahead of where the dolly stops (none beside the lens); S06/S07 and every other `kong_cutter` shot hold the cutter in both hands (`cutter.py`), S06 reframed so the tool is in frame and points at the car; S12-S15 phone arm has the elbow out (it crossed the mouth); S15 and the other close shots raster the puppet at 360-540 px per unit; S18 crack web thinned over the face, teal dash glow nearly off, warm face fill, driver sat 0.17 higher; S20 is an over-the-shoulder from outside the opened door (Kong's back on the left, driver 0.52 forward of his seat so the B-pillar clears his face, airbag hidden in this shot).
- Not done: 16:9; a watch-through of the motion (frames, the sheet and the six stills were checked, not playback); the full film at the final tier (about 37 CPU s x 1280 = 13 CPU h).

## Draft v2, review pass (same file names: `draft_v2.mp4`, `draft_v2_sheet.png`, `v2_stills_720.png`)

432 frames re-rendered (S01, S06, S07, S09, S13, S15, S18, S21, S23, draft tier 360x640), whole film re-conformed, stills S06/S13/S18/S23 re-rendered at the final tier.
- S01, S09: lens blur cut (S01 `k` 26 -> 10, S09 `k` 70 -> 16): both shots read as blurred pictures; the city and Kong are now legible behind the prop.
- S06, S07: the crew member is hidden (he stood exactly behind Kong and read as a dark double of him).
- S13: the half-second "q" glance is gone (the arm crossed the face); S13 and S15 talk with the round mouth `("o", level)`: the open D read as a grin on the guilty / tired face.
- S15: camera aims 0.22 higher, so the chest lettering is below the caption band.
- S18: the bystanders on the horizon above the roof are hidden.
- S21, S23: the bitten crew member screams with the round mouth (it read as a laugh); S23 locks the drawings (`attack(lock=True)`): the automatic view choice flipped to a broken back view for a few frames.
- S22 and S24 call `attack()` without the new options and were not re-rendered.
- Review frames and logs: `tmp/rv2/`.

## Draft v3 (`draft_v3.mp4`, `draft_v3_sheet.png`, `v3_stills_720.png`, `line_test_720.mp4`, `line_test_crop.png`)

User decisions folded in: flat v13 status strip (no v12 tubes, no voice badge), Ohm narration, lighter rain / crisp picture, flat sheet puppets, crisp ink lines as video. Sources kept from before this pass: `tmp/v3/` (`common.py`, `cues.py`, `finish.py`, `stills_sheet.py`, `stage_before.py`, `shots_before/`, `post11_before.py`, `icons13_before.py`).

### What reads what now

| Thing | Source |
|---|---|
| lip sync (`common.mouth`), radio LED | `audio/narr_ohm/narr_final.wav` + 0.30 s |
| word cues in shots | `common.word("phrase")` = `audio/narr_ohm/captions_timing.json` + 0.30 s (S01 2.151 / 2.623, S06 11.535, S12 22.718 / 23.478, S13 26.335) |
| picture / effect cues | fixed in `common.CUES` and `cues.py`: radio cut 3.243, battery 16.30 / 16.50 / 16.70, cutter 15.052, phone 17.648, hang-up 31.75, red eye 41.657, lunge 43.445 (the driver is out of the door on frame 1045), scream 43.795, title 50.72. `mix_ohm_v2.py` places every effect where the v1 mix had it |
| captions | `captions_ohm.ass`, written by `finish.ass_path()` from the Ohm timing; title line: libass size 124 (text 485 px = 67 % of the width), centre y 612 |
| icons | `v13/icons` (`finish.icons_over`), composited last at the output size; `DZ09_NARR=narr_ohm` |
| audio | `audio/narr_ohm/mix_ohm_v2.wav` at ONE static gain (-0.40 dB), AAC 320 kb/s: -14.6 LUFS, true peak -1.0 dBTP measured on the encoded track (`mix_ohm_v2_norm.m4a` + `.json`). The source is -14.2 LUFS / -0.9 dBTP, so -14.0 and <= -1 dBTP cannot both be met without a limiter |
| encode | H.264 CRF 15, preset slow, tune animation, yuv420p |
| clarity levels | `post11.LEVELS` defaults: RAIN 0.20, SPLASH 0.25, HAZE 0.30, TILT 0, DOF 0.25, BLOOM 0.55 (`run.py --levels v2` = the draft-v2 set); S01 / S09 keep their own blur cuts |

The cut is unchanged (`v4/animatic/timing.py`, sentence starts are identical in both takes). Inside sentences three cuts no longer sit on an Ohm word boundary: S06/S07 12.618 (Ohm 12.595), S08/S09 16.215 (16.146), S23/S24 47.778 (Ohm says "เพื่อนของเขา" from 47.553, so that caption starts 5 frames before the cut to S24).

### Line quality (final tier)

- `PCT = {"final": 100}` in a shot module = render scale for that shot; `Stage.begin` applies it, `run.py --pct N` forces one for a run, the log records `pct`. 100 %: S01, S06, S07, S10, S12, S13, S15-S24 (906 frames). 75 %: S02-S05, S08, S09, S11, S14 (374 frames).
- `Stage._auto_ppd`: every puppet is rastered at no less than 1.25 x the pixels its head covers at the shot's middle frame (steps of 60, 240-780); a shot's `PPD` dict is a floor.
- The cast (object index 2) is always in `sharp_idx` (no lens blur), tilt-shift is off, motion blur is off, there is no frame blending anywhere. Not covered: puppets staged as dark foreground / background shapes with index 5 (Kong's back in S17 / S20, the crew behind Kong in S12 / S13) still take the (small) lens blur.
- `line_test.py`: 36 frames of S13 (g 608-643) -> `line_test_720.mp4` (looped 3 x, 110 frames because the loop join adds one per pass) and `line_test_crop.png`.
- Cost at 100 %: 63.9 CPU s per frame (S13, 32 frames, 1 thread each); stills with 4 threads 54-83, mean 68. Whole film at these settings: about 906 x 65 + 374 x 40 = 20 CPU h (5 h on 4 cores with 4 workers x 1 thread).

### Faces

- `stage.skin_group()`: head and face cards use their own copy of the flat shader: the even fill is pulled 70 % toward neutral and the red / blue beacon lights are light-linked away from those cards. Faces hold the sheet's paper colour (driver: grey-green); bodies still take the beacons.
- The three pale rain beads the wet specs drew on the face are removed (`stage._face_clean`); at 360-720 px the denoiser turned them into a shimmering patch between the eyes. Hair beads stay.
- `draw8.EXPR["serious"]` (added from `stage.py`): the sheet's determined brows with a flat mouth. `kong_cutter` uses it by default.

### Shots

| Shot | Change |
|---|---|
| S01 | The handset never stood on the delivery box: the ray that looked for the box top started 8 D up and hit a light cone, so it hung 7.5 D in the air. It is now held at chest height by a gloved hand with an orange sleeve (`radio_hand_root`), 28 mm from 1.3 D, Kong and the wreck sharp behind |
| S04 | starts 17 D further up the lane and higher |
| S06, S07 | serious face; the crew member stands beside Kong (`base.crew_ready`): camera-left in S06, screen-right and a step back in S07; S06 tilts up 0.2 as it closes in |
| S08 | jaws feel for the seam, bite at 15.05, ease, bite again at 15.67 with a second spark burst; a real push |
| S12 | framed 0.37 lower: the crew member's face was in the strip |
| S16 | phone 2.35 D from the lens at 0.8 scale; "call ended" dims from 31.75 and is black only from 32.27 as the hand takes it down |
| S19 | no change of its own: the skin shader keeps the face colour |
| S20 | 66 mm from 3.05 D: the driver's head is 0.41 of the frame width at the red eye; Kong's shoulder left |
| S21 | along the car's flank from behind the door, 28 mm, low: driver 3/4 with fangs (0.44-0.47 W) in front of the junior, junior's scream face above him; 8 frames of hard shake; one white / red frame on g 1045 (`cues.LUNGE_FLASH`) before the red bite flash at 43.795 |
| S22, S24 | `attack(scream=True)` |
| S23 | `F.nudge("bike_a_box", ...)`: the delivery box is smaller, on the deck and out of the frame |
| title | plate dims the picture 45 % (was 62 %); mark radius 118 at (360, 350) |
| icons | `LAYOUT["916"]`: `keep=2`, `q` 0.96, `m` 0.88 (see `v13/icons/API.md`) |

### State

- All 1280 frames re-rendered at 360x640 draft tier with the new levels (10.3 CPU s per frame, 3.7 CPU h), S01 and S06 once more after a framing nudge; conformed at 720x1280 (`out/draft_from360x640_720x1280/comp_v3`).
- `v3_stills_720.png`: S01, S06, S13, S18, S20, S23 at the final tier, 100 %, with icons and captions (`out/final_720x1280/stills_v3`); more final stills of the changed shots in `out/final_720x1280/stills_v3chk`.
- Head positions are logged per frame (`heads` in `out/draft_360x640/log_*.jsonl`). Head circles still inside the strip box (x 5-80 %, y 8-19 %): S01 frames 54-80 (Kong, after the push), S09 (the foreground face, by the icon designer's choice), S10 445-456, S16 775-785 (row faded there), S21 1060-1085 (junior's hair / forehead), S23 one frame. S12 is clear.
- Not done: the full film at the final tier; 16:9; a watch-through of the motion (frames, the sheet and stills were looked at, not playback).

## Director changes after draft v3 (user decisions, post only; do not revert)
- NO STATUS ICONS. The user saw the v13 row, the v14 cards and the v15 pictograms and then said "take the icons out".
  `finish.icons()` uses `noicons.py`: nothing is drawn until the title hit (g 1217), then the biohazard title mark only.
  A reviewer must NOT put icons back or report their absence as a defect.
- Captions colour key words (`finish.EMPH`): amber = fact, red = threat; such a line pops 12 % for 3 frames.
- MUSIC: the user supplied four Suno instrumentals (`audio/suno/`). The hook mix is now `audio/narr_ohm/mix_ohm_v3.wav`
  (built by mix_ohm_v3.py: track 1 tension bed with hits on 3.243 / 43.445, track 3 under the phone call, track 4 riser + hit on the
  title 50.72; voice over bed 20.7 dB average, 13.7 dB minimum). finish.MIX points to it. Do not go back to v2.

## Final render (`out/final_720x1280/S01..S24/f_####.png`, 1280 frames)

- Whole film at the final tier, 720x1280, per-shot PCT (100 %: 906 frames, 75 %: 374), default levels, 4 workers x 1 thread: 20.59 CPU h, 6 h 35 min wall (other jobs shared the 4 cores for the last 4 hours). Logs: `logs/final_w*.log`, `out/final_720x1280/log_*.jsonl`. No worker died. Everything that was in `out/final_720x1280` before is in `out/backup_pre_final/final_720x1280`.
- S01 changed before the render: the handset and the gloved hand holding it are one flat drawn card in the cast's style (`stage.radio_card_png`, `tex/radio_card.png`; display and LED are emissive planes on it); the box radio / box hand are gone. The push sinks 0.10 instead of rising 0.46 and tilts up 0.06 (`RISE` in `shots/s01.py`): Kong's head top stays at or below 23.6 % of the height (strip box ends at 19 %). Previous sources: `tmp/fin/stage_before_final.py`, `tmp/fin/s01_before_final.py`.
- Not finished here: `finish.py` has not been run on these frames (no conformed final mp4 yet). The draft-tier frames of S01 in `out/draft_360x640` are the OLD staging.
- Still weak (unchanged from the approved draft): box-built glove hands on the phone in S11 / S16 and on the 3D cutter in S08 / S09; S09 Kong smiles; S17 crew shout reads cheerful; S20 a hard shadow edge splits the driver's face; S24 the attack is small and the driver's back is hard to read.

## Final conform (`DZ09_EP1_hook_916_v1.mp4`, `final_sheet.png`, `final_stills.png`)
- `tmp/fin/conform.py A|B comp i/n` / `... video <out>` (finish.py itself untouched). Finished frames: `out/final_720x1280/comp_finA`, `comp_finB`.
- A = `DZ09_EP1_hook_916_v1.mp4`: finish.py as it stands (director changes above: no status icons, title mark only; coloured key words; `mix_ohm_v3.wav` with the Suno beds at -0.40 dB -> -14.7 LUFS / -1.1 dBTP encoded, `mix_ohm_v3_norm.m4a`).
- B = `DZ09_EP1_hook_916_v1_ALT_v13strip_mixv2.mp4` (+ `final_sheet_ALT_v13strip.png`, `final_stills_ALT_v13strip.png`): the draft-v3 conform (flat v13 strip, plain captions `tmp/fin/captions_ohm_plain.ass`, `mix_ohm_v2_norm.m4a`: -14.6 LUFS / -1.0 dBTP).
- Both: 1280 frames, 24 fps, H.264 High CRF 15 slow tune animation yuv420p, AAC 320k, faststart, narration at 0.300 s.
