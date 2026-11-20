# s01 QA: film 20, shot 1 (the hook) -- TOWER tower_low, DAY 1889

**This is the worked example for every film-20 render team.** Copy `c20.py` into your take folder and read its GOTCHAS first (the
same list, with the numbers, is at the end of this file). Then use `shot.py` and `deliver.py` as templates.

## Delivered
- `frames/g_0000.png .. g_0083.png` (not in git): 84 frames, 720x1280, 8 spp (the set's FINAL_SPP), 2 threads, OIDN. No captions, no audio.
- `take.mkv`: libx264rgb crf 6, 30 fps, first_g 0, 84 frames, 29 MB (under 45 MB: not split).
- Frame ranges:
  - g 0..79 = shot 1 (plan 0.00-2.67 s).
  - g 80..83 = 4-frame out-handle (cut side), rendered in 3D. The push, orbit, tilt and his idle all continue into it.
  - There are no handle frames before g 0 (the film opens here).
- `meta.json`: g0 0, g1 80 (exclusive: the hard cut to shot 2 falls at g 80), first_g 0, n_frames 84 (80 + 4), transition_in {"type":"cut","frames":0}. It also carries transition_out, events, set / cast / camera notes, head numbers, s/frame and frame-diff.
- `cues.json`: 8 cues in film seconds (`kind`, `t`, `dur`, `note`, plus frames):
  - ambience;
  - coat creak + nasal breath;
  - snap whoosh (g 25-40);
  - sour pizzicato on the face swap (g 27);
  - coat swish on the turn (g 45-53);
  - a breath-only "hmph" (g 48);
  - a "tsk" tick on the chin jerk (g 61-66);
  - the cut.
- `contact.jpg` (16 frames, cyan line = y 880), `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`.
- Scripts:
  - `c20.py`: the helper.
  - `shot.py`: `probe`, `camreport`, `stills`, `final` and `hue`.
  - `deliver.py`: `python3 deliver.py`, or `deliver.py draft` to review a draft.
- `.gitignore`: `raw/ frames/ work/ __pycache__/`.

## Shot (what the viewer sees)
| g | beat | caption (event g = round((t+0.10)*30)) |
|---|---|---|
| 0-25 | Low angle on the gravel avenue of the Champ de Mars. Maupassant (arms folded) **sneers** up-right; the **whole tower** stands behind him. A lamp-post leans across the left edge, a bench sits lower right, and kiosks, flags and crowd cards fill the lower third. The camera is already moving: push 8 %/s, slide, orbit, tilt. | "นักเขียนคนนี้" -0.01 |
| 25-40 | SNAP: push x1.4 + 18 deg orbit + 2 deg tilt. The tower whips sideways behind him. **Face swap sneer -> disgust** behind the blink: g 26 half, **g 27 closed = swap**, g 28 half. | "เกลียดหอคอย" 0.79 = g 27 |
| 45-53 | He **turns his nose away**: yaw +0.30 -> -0.85 (faces screen-left), chin up, leans back. The expression goes to `avoid` (eyes squeezed shut) at g 48, mid-turn. | "ต้นหนึ่ง" 1.45 = g 47 |
| 61-66 | "Hmph" chin jerk (pitch + head roll bump). | "ที่สุดในโลก" 1.94 = g 61 |
| 66-83 | He holds the snub with an idle sway and breathing. The camera ends with him in the left third and the tower right. Cut at g 80. | |

## Checked (all 84 frames at full size; 6 fps sheet = every 5th frame; g 24-30, 44-54 and 77-83 frame by frame)
### Heads and staging
- Head 138 -> 224 px wide.
- Head centre y 585-718 in-shot (g 0-79); 730 at g 83 (handle).
- Lowest head bottom: y 830 in-shot, 844 in the handle. No head reaches the caption band (y 880).
- Below y 880: only his coat, the path, the bench and kiosk bases.

### Tower, contact, foreground, crowd
- **Tower reads as the Eiffel Tower in every frame.** The summit is in frame from g 0 (y 45 at g 0, 138 at g 83). Also visible: the lantern, both platforms with lamp dots, the tapering lattice and the big first-level arches. The plan's "tilt up" ends past the second platform (QA-art note).
- **Contact:**
  - he stands on the gravel path (z 0.113 D, ray cast);
  - shoes on the ground;
  - contact decal (opacity 0.8) under the soles;
  - proxy shadow toward the sun.
- **Foreground:**
  - lamp-post: 2.7 D from the lens at its closest; at the left edge g 0-45, then it leaves frame left (parallax);
  - bench: lower right g 0-35, 4.3 D from the lens;
  - both are dark (preset shade materials).
- **Crowd:** 8 static crowd cards 14-34 m behind him, small in frame; they read as fairgoers standing. QA-tech N1 on the stand-in tile asked for a lamp head in frame. The lamp head is above the top edge here: at 0.16 m lens height it would cost 10+ deg of extra pitch.

### Rules
- **Mouths:** no quote in this shot. Expression mouths only (smirk, frown, frown); none are animated.
- **Nobody frozen:** his idle sway, breathing squash and head roll run every frame.
- **No DOF** (dof off at build and before every render). **No text.**
- **Continuity into shot 2** (RESTO resto_table): same Maupassant, same costume, day. A hard cut (place change) is allowed.

### Automatic checks
- `qa_auto.py take.mkv --first_g 0 --cuts 80`: **PASS**. No black, blank, magenta or frozen frames; magenta 0.0 %; no pops.
- Its only note: "planned cut g 80 has no visible change". This is expected: g 80-83 is the handle, and the cut happens in the conform.
- Sprite 'clipped' warnings: 0. Retried frames: 0.

### Colour
- `python3 shot.py hue 0 40 79` (set3d20/hue20, cast-shadow pixels): shade hue mean 252.4 (band 240-260, OK); magenta 3.15 % (limit 10). The circular median is 220 (in-band share only 13 %).
- The cast shade here is mostly his own coat and the dark bench, which pull the median toward blue-cyan. The ground shade is the set's blue-violet (approved tile T01: 239.8 / median 230). Note only.
- All three measured frames: g 0 shade hue 247.8 (median 225.9, in band 43 %, magenta 1.8 %); g 40 258.1 (221.6, 16 %, 3.4 %); g 79 252.4 (220.2, 13 %, 3.2 %). The mean is in band on every frame and magenta is far under 10 %.

## Frame-diff (production-lessons §10)
**Method** (`deliver.py framediff`, also `c20.framediff`):
- grey = mean(R, G, B), resized to 90x160 (bilinear);
- the score is the mean |diff| to the previous frame, in 0-255 levels;
- in-shot pairs only: g 1..79 (no handle).

| | median | p90 | min | max |
|---|---|---|---|---|
| **final s01** | **4.56** | **12.60** | 3.6 | 17.5 |
| target | >= 4 | >= 12 | | |
| 360x640 draft of the same camera | 4.82 | 12.70 | | |

- The p90 comes from the snap, g 27-37 (12.0-17.5).
- The median comes from the drift orbit and slide (4.0-4.8), plus the turn (5.2-6.2).
- Weakest stretch: g 67-72 (3.6-3.7), where the drift decays.
- The director asked to keep ~5 / ~14. The final is 4.56 / 12.6: it passes the WORKER20 target but sits below that reference, because the whole-tower framing has much more smooth sky than the first version had (5.0 / 14.1).

How the camera got there (drafts):

| camera | median | p90 | note |
|---|---|---|---|
| v1: preset spot, lens 0.35 m, tilt 4.5 deg/s, snap x1.45 + 6 deg tilt | 5.05 | 13.5 | tower cut at the first platform until g 33, 40 % empty ground (director: rejected) |
| v2: staging 50 m back, whole tower, tilt 2.5 deg/s, arc 3 deg/s | 3.18 | 6.33 | sky dominates; tilt is capped by the head band |
| + arc 5 deg/s, snap arc 12 deg | 4.30 | 13.04 | but **pop 50.9**: the lens drove through the bench at g 53-64 |
| + FG re-anchored, lamp-post moved off his face | 3.56 | 11.04 | |
| + arc 8 deg/s, slide 45, decay 0.1, snap arc 14 | 4.74 | 11.64 | |
| final: snap arc 18, arc0 -11, tilt 2 deg/s | 4.82 | 12.70 | |

## Seconds per frame
**9.11 s wall / 17.6 s CPU** mean at final (720x1280, 8 spp, 2 threads, two processes at once on 4 shared cores).
- Load from other jobs made earlier attempts run at 21-23 s wall.
- Build: about 41 s per process. Sprites for 42 frames: about 1-2 min.
- Draft (360x640, 4 spp): about 2.2 s wall per frame; a whole draft takes about 3 min with 2 processes.

## Gotchas for render teams (details and code in c20.py / shot.py)
1. **Key every hook on every rendered frame.** `Take()` calls `CO.clear_keys()` after the build. s01 keys `set_year(1889)` and `set_crowd(1)` per frame with `Take.key_set`.
2. **Blender frame = g + 1** (`bf`). One location per process; build the set FIRST, then the actors (`S.build` wipes the scene).
3. **Scale:** 1 D = 0.532 m (`CO.SC` 1.88). `A['cams']` / `A['marks']` are in D; the set source files (tower20.CAMS_M, site20 ...) are in metres (`CO.W()`).
4. **Mark z is not the ground.** The tower_low gravel path is 0.113 D above `maupassant_low`'s z 0. From a low lens, the shoes and the contact decal vanished into the path (s01's first final had to be thrown away). Use `C.on_ground(mark)`.
5. **The whole tower plus a head in 450-760 does not fit from tower_low's spot** (summit 68 deg up). s01 moved the whole staging 50 m back and 2 m toward the avenue centre (`shot.delta`). That means the mark, camera, FG and crowd cards all move. Then it solved height, distance, tilt and **lens shift** with a pure-math projection (`shot.project` + `C.CamPath.at`, no scene build needed) before rendering.
6. **Lens shift:** +shift_y moves the PICTURE DOWN. The preset's +0.08 put the stand-in head at y 793; s01 uses -0.12. Measure head positions with `probe` / `head_report`, never by hand.
7. **Preset FG is anchored to the preset camera and merged per material.**
   - Moving it with a moving camera can put the lens INSIDE a prop. That happened here: a 50-level frame-diff pop, frames of dark timber.
   - s01 splits the vertices by distance to the lamp spot and places the lamp-post and the bench relative to the LAST frame's lens.
   - Check lens clearance and screen x over the whole path, and keep the FG off faces.
8. **Push toward the SUBJECT.** tower_low's look_at is 225 D away; CamPath pushes along camera -> subject and tilts separately (`tilt0`, `tilt_deg_s`, snap `tilt`).
9. **Tilt vs. caption band:** every tilt degree drops a near head ~14 px. A push toward a head above the lens raises the head line and buys tilt back. Moving the camera ALONG the camera->subject line changes nothing.
10. **Frame-diff with a fixed subject:** tilt + push over a big sky gave 3.2 / 6.3. **Orbit** (`arc_deg_s`, `arc0`, snap `arc`) makes the far tower slide behind him, and that carried both numbers. Tune on 360x640 drafts: they come within ~0.3 of the final.
11. **Expressions cast20 lacks** (the plan's "disgust") are registered at runtime with `C.add_expression("disgust20", ...)`. Never edit cast20.py / puppet.py. Swaps go on the closed frame of a 3-frame blink (`blink(g, [at-1])`).
12. **Cards at low angles:** keep the pitch to the card (the head line) under ~40 deg. upper_k reaches 1.09 here; s01 passes a taller canvas `(-1.75, -4.25, 1.75, 0.1875)` than CANVAS20.
13. **Contact in shade:** he stands in the preset's near-ground shade zone, so the proxy shadow barely shows. Use a stronger decal: `contact=dict(width=1.3, depth=0.55, opacity=0.8)`.
14. **Drafts vs finals:** `shot.py final ... 0.5 4` writes `work/draft` and never mixes with `raw/`. `final_loop` resumes only when scale and samples match, so after ANY staging change `rm -rf raw` before re-rendering.
15. **Do not pipe long renders through `tail`** if you want all the result lines (s01 lost two hue lines that way).

## Differs from the plan / notes
- **Tilt-up:** the plan's "tilt up the tower" is 7 deg here (pitch 32 -> 39), plus an orbit. The director asked for the whole silhouette from frame 0, so the tilt reveals more lattice under the spire rather than the spire itself.
- **Staging:** 50 m further back than the tower_low preset mark. The tower is the same; the preset's T01 tile framing is not used.
- **Lamp-post distance:** 2.7 D at its closest (rule 1-2 D). Any closer and it crosses his face in this orbit.
- **Frame-diff:** 4.56 / 12.6. It passes the target but sits below the director's ~5 / ~14 reference (see above).
