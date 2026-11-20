# SET v2 tech QA (film 15, Blender 5.3.0 bpy, Cycles CPU)

Verdict: **PASS** for build/render/camera paths in a fresh clone (3 fixes recommended; one of them, the render-cost doc, matters for scheduling).

Method: `git clone --depth 1 -b film15/main` into /tmp/qa_tech_v2/repo (no sprites/stills/work dirs), ran the shipped stills CLI and my own camera checks (/tmp/qa_tech_v2/scr/camchk.py). Machine: 4 cores, load average 5-7 from other jobs during the final-quality timings, so wall times are inflated; CPU seconds are the reliable figure.

## 1. Fresh-clone build and render
| Item | Result |
|---|---|
| A: `build_a2('HERO')` + stills s1 (far), s3 (near), s4 (low hero), preview 360x640 | OK, build 2.5-2.9 s, no errors; sprites regenerated on the fly into work_v2_a/sprites, stills dir created |
| B: `B2.build('TENSE')` (camera checks) and `build('NIGHT')` stills bz_start, bz_end, t5_arch, preview | OK, build 3-4 s, ground_issues [] on all |
| Textures | committed tex/ present for both; B regenerates missing ones (v2_b.py:21); A textures are committed (v2_a.py tex_* check/regenerate) |
| Imports | cast15, stage, cast_test, set15*, fonts (film/fonts/*.ttf) all resolve via HERE / V3 relative paths |
| Hard-coded absolute paths | none to the repo or /home. Only system fonts, used for texture regeneration and sheets: v2_a.py:27-28 (Liberation, DejaVu), v2_b_tex.py:7-8 (DejaVu, `/usr/share/fonts/opentype/inter/Inter-Bold.otf`), v2_a_shots.py:154, v2_b_shots.py:323. Present on this image; a render node without Inter fonts would fail only if B textures have to be regenerated (they are committed). |
| Untracked after run | work_v2_a/{sprites,stills}, work_v2_b/{sprites,stills} appear as untracked (no .gitignore entry): do not `git add -A` by accident. |
| Previews looked right (checked visually): A bird's-eye, medium, low hero; B stadium far/medium | OK |

## 2. Camera paths (frame g = round(t*30))
- `key_camera` (v2_a_shots.py:35) keys every frame 0..132 (t 0.0-4.4 s) at f/30; the scene camera location matches `bigzoom1_path(f/30)` exactly (dev 0). Start (24,-12,100) m, end (4.6,-3.9,1.3) m. Matches plan BIGZOOM 1 0.0-4.4.
- `apply_bigzoom2` (v2_b_shots.py:98-114): frames 930..1059 (31.0-35.3 s), location, rotation, lens keyed per frame, LINEAR, deviation vs `bigzoom2(f/30)` = 0 (location and lens). Matches plan BIGZOOM 2 31.0-35.3. Note last key 1059 = 35.3 s, one frame past the T3 end 35.27 (frame 1058): the T4 cut must take 1059 as its own, or trim the last BIGZOOM 2 frame.
- `apply_t5` (v2_b_shots.py:115): frames 1331..1652 (44.38 -> 1331.4 rounds to 1331, 55.08 -> 1652.4 rounds to 1652), dev 0. The first/last frames are evaluated at f/30 (44.367 / 55.067), slightly outside [t0,t1] and clamped by `spline`; harmless. Frame 1652 is also the first frame of T6 per the plan (1652.4), so a one-frame overlap is possible.
- Per-frame step is smooth (BZ2 first step 0.003 D, T5 0.21 D).

## 3. Timings, solo-style settings (720x1280, 12 spl, 2 threads, OIDN; machine was shared, wall inflated)
| View | wall s | CPU s | author's log (committed) |
|---|---|---|---|
| A s1 BIGZOOM 1 start (far) | 20.4 | 40.0 | n/a |
| A s3 BIGZOOM 1 end (near) | 22.4 | 43.0 | n/a |
| B bz_start (far) | 17.2 | 32.7 | 15.6 / 30.5 |
| B bz_end (near, crowd bowl + cards) | 142.3 | 227.0 | 148.6 / 231.5 |
| B t5_arch (pit, rim card) | 107.4 | 163.2 | 151.3 / 181.4 |
CPU/2 threads puts a pit view at about 80-115 s solo; the author's own log gives 115-200 s wall for t4_low, t4_coach, t5_arch, t6_top, bz_end. Plan accordingly: T4+T5+T6 are about 750 frames of pit view, so on the order of 20+ CPU-hours at 2 threads unless samples/crowd are reduced.

## Fixes (concrete)
1. API_v2_b.md:53 (last section "Notes / limits", line "Render cost: 10-16 s wall per frame for pit views, 4-6 s for the far views") is wrong: far views are 15-20 s wall, pit/bowl views 110-200 s wall (230 CPU s) at final quality. Correct it before the render team budgets (API_v2_a.md:30 "~5 s wall/9 s CPU" is the preview figure; final is 20-22 s wall / 40-43 CPU s).
2. v2_a_shots.py:37 (`key_camera`): `sc.frame_end = max(sc.frame_end, f1)` leaves the default frame_end 250 on a fresh scene (frame_start is 0). Set `sc.frame_start, sc.frame_end = f0, f1` as `apply_path` does (v2_b_shots.py:111), otherwise a naive "render animation" gives 250 frames.
3. v2_a_shots.py `setup_bigzoom1` places no cards (docstring says place them afterwards); cards are single-frame facing (`ground_card` faces the camera at the call frame), so for animation the render team must re-orient per frame. State this in API_v2_a.md. Likewise the 1-frame boundary overlaps above (BZ2 1059 vs T4, T5 1652 vs T6): add a note to API_v2_b.md.
4. Optional: add `work_v2_*/sprites/` and `work_v2_*/stills/` to .gitignore; document that sprite and still folders are created on first run (sprite cache costs a few seconds per new pose) and that system fonts (DejaVu, Liberation, Inter) are only needed for texture regeneration.
