# Ref D: camera and composition, with 8 shot templates for EP.1

Source: `ref/d/ref.mp4` (720x1280, 30 fps, 2135 frames, 71.2 s). `vNNNN` is a 0-based video frame (t = N/30). `f2_NNN` is `ref/d/frames2/f_NNN.png`. **Measured offset: f2_NNN = video frame (NNN-1)*15 + 7** (matched against the video at 180x320 for f2_002, 020, 060, 100 and 141, the minimum absolute difference is at +7 every time). All px are at 720x1280. D = head diameter. Lens values are Blender `lens` in mm with `sensor_width = 36` and `sensor_fit = 'AUTO'`, so on a portrait frame `lens = f_px * 36 / 1280` (the same convention as `refC_camera.md`).

We copy framing, lens, height, movement and timing only. We do not copy the reference's characters, uniforms, insignia, logo, text or WW2 subject.

Scripts and scratch output are in `scratchpad/rdcam/`, outside the project: `small.npy` (all frames at 180x320), `flow.py` / `flow.npy` (per-frame Farneback similarity fit, caption and watermark masked), `stats.py` (per-shot motion), `dof.py` / `dof.json` (re-blur defocus tiles, the same estimator as ref C `dof2.py`), `vp.py` (LSD + RANSAC vanishing points), contact sheets `cs_*.jpg` (every 6th frame), `cuts_a.jpg` / `cuts_b.jpg` (7 frames around each doubtful cut), `key_*.jpg` / `key2_*.jpg` (half-res stills). I looked at the full contact sheets and at the stills f2_003, 008, 011, 013, 014, 019, 025, 028, 035, 042, 046, 051, 053, 058, 062, 072, 077, 082, 086, 090, 094, 097, 101, 104, 107, 112, 115, 119, 121, 125, 129, 131.

How ref D differs from ref C (`refC_camera.md`):
1. **It is calm.** The median frame-corner speed is 83 px/s (ref C 231). 41 % of frames are near static (ref C 22 %). Only 33 frames (1.5 %) go above 1200 px/s; ref C has 37 % snaps.
2. **It cuts instead of flying.** There are 21 hard cuts (ref C has 3). The fly-through one-takes exist only at the open (v0-123, v178-395).
3. **It holds tableaux.** Frontal, symmetric, eye-level sets are held still for 2-4 s while the characters act (v474-595, v1096-1190, v1250-1318).
4. **Depth of field is strong only on prop macros and POVs.** On the macro inserts the background goes to sigma 13-20 px. Every shot with a character keeps the background at sigma 1.5 px or less.
5. **It uses props as framing.** Rifle sights, a thermometer on a trunk, a log, a shoulder, a lantern and a scope fill 25-45 % of the frame in 11 of the 35 setups.

---

## 1. Cuts (hard cuts from frame differences)

Detection: the grey mean absolute difference at 90x160 and the HSV histogram distance between consecutive frames. The median difference is 4-5, and a cut reads 50-115 (v123 67, v178-180 65/87, v395 77, v595 49, v658 58, v732 54, v879 71, v1190 71, v1250 105, v1318 54, v1377 56, v1483 54, v1567 68, v1622 57, v1824 64, v1908 82, v2004 115, v2041 114, v2107 72). v1024 reads only 30 because the two shots share the same white snow; it was confirmed by eye (`cuts_a.jpg`). These are **not** cuts:
- Long runs of 20-40 from v7-48, v307-348, v1416-1440, v1500-1531 and v1730-1786: these are camera moves and character motion.
- v213-217: a 4-frame radial crash zoom inside a shot.
- v1074: a histogram jump of 0.7 with a difference of 7.8, which is the day-to-night time-lapse grade inside one shot.
- v1236-1249: a smoke/fog wipe that crosses the frame; the hard cut follows at v1250.
- v1881-1885: rifle recoil shake.

**22 shots, 21 hard cuts. There are no dissolves.** Shot lengths in seconds: 4.10, 1.83, 7.23, 6.67, 2.10, 2.47, 4.90, 4.83, 2.40, 3.13, 2.00, 2.27, 1.97, 3.53, 2.80, 1.83, 6.73, 2.80, 3.20, 1.23, 2.20 and 0.93. The median is **2.6 s** and the mean 3.2 s. Splitting the shots at their framing changes gives 35 setups, with a median of **1.8 s** and a mean of 2.0 s.

## 2. Per-shot log

Motion columns come from `flow.npy` over each shot (2 frames trimmed at each end). The corner speed is |zoom| x 734 + pan, in px/s at 720x1280; it includes some character motion, so a static camera with a walking puppet reads 20-40. "Zoom" is the summed push (+) or pull (-) scale change over the shot. DoF is the background sigma in px at 720 wide, from `dof.json` (the estimator saturates at about 4-5 px). The strong macro blurs were measured from edge widths instead (10-90 % rise / 2.56): the trunk edge in f2_003 is 50 px wide (sigma 19 px), and the hood edge in f2_001 is 34 px wide (sigma 13 px).

Angle tags: low / eye / high / top / POV / insert / OTS / Dutch. Height is the camera height above the ground in D, judged from the horizon row against the figure, except where marked. Character size is the head D in px, and the figure height as a fraction of H = 1280 where the whole figure is visible. Lens marked **m** is measured from vanishing points (orthogonal pairs); **e** is estimated by eye from compression and convergence.

| shot | v frames | s | setup (ids) | angle | lens mm | cam height | char size | foreground framing | DoF bg sigma px | motion, speed |
|---|---|---|---|---|---|---|---|---|---|---|
| 1a | 0-12 | 0.4 | macro: cartridge standing in snow, the sniper's head blurred behind (f2_001) | insert | 45-60 e | about 0.3-0.5 D, at the prop | prop 190 px tall (0.15 H); head behind about 300 px, defocused | the prop **is** the foreground; the snow lip covers the bottom 30 % | **13-19** (edge widths) | static |
| 1b | 12-48 | 1.2 | the bullet flies; the camera follows it (f2_003) | insert | 45 e | 1-2 D | none | none | 3.5-4.5 (saturated, real >8) | whip-follow, p90 1111 px/s, 11 frames above 1200 px/s, roll sum 16 deg |
| 1c | 48-78 | 1.0 | macro along the rifle bolt | insert | 40 e | about 1 D | none | the rifle fills 60 % | 1.5-5 | push along the barrel |
| 1d | 78-123 | 1.5 | MS of the prone sniper, eyes glowing (f2_008) | eye (prone level) | 30 e | about 1 D, pitch about 10 deg down | head D about 300 (0.23 H) | the rifle crosses the lower right; snow lip | 0.3-1.0 | pull-out then drift, ending near static; speed-line overlay |
| 2 | 123-178 | 1.8 | POV down the iron sights to a tiny target (f2_011) | POV | 24-28 e | about 0.6 D (prone eye) | none | **the rifle fills the lower 45 %**, centred | far 0.2-0.8 (sharp); near rifle rows 2-4 | slow creeping zoom, +54 %/s, 443 px/s median, +147 % in total |
| 3a | 178-200 | 0.7 | high wide behind the sniper, muzzle flash (f2_013) | high | 35 e | about 8-10 D, pitch about 35 deg down | head D about 70 (0.055 H) | pine branches at the left edge | 0.8-1.0 | fast (1226 px/s) |
| 3b | 200-240 | 1.3 | chase behind the bullet low over snow, then a **4-frame radial crash zoom** (v213-216) to the target (f2_014) | high (mild) | 35 e | 1-2 D, pitch about 20 deg down | none | none | 1-4 (motion) | follow at 1000-1200 px/s plus crash zoom; 9 frames above 1200 px/s |
| 3c | 240-291 | 1.7 | frontal outhouse door opens on a figure holding a poster (f2_019) | eye | 32 e | about 2.5-3 D | figure 520 px (0.41 H), head D 140 | **the door frame and jambs frame him on both sides** (frame in a frame) | 0.5-1.0 | static, 72 static frames |
| 3d | 291-312 | 0.7 | snap push to MCU | eye | 32 e | about 3 D | head D about 300 | door jambs | motion | snap, 6 frames |
| 3e | 312-354 | 1.4 | push into the poster; the printed drawing becomes the next scene | insert | | | | the poster fills the frame | 0.1-0.7 | push, then a **graphic-match** dissolve-free morph into 3D |
| 3f | 354-395 | 1.4 | wide farm, ski tracks leading in (f2_025) | low | 30 e | about 1-1.5 D | figure about 0.12 H, head D about 80 | ski tracks run from the lower right corner (leading lines) | 0.4-0.7 | static |
| 4a | 395-430 | 1.2 | map on the table, from above (f2_028) | top (pitch about 70 deg) | **38 m** (f_px 1342) | table + about 3 D | none | **a lantern at the top-left corner, a mug at the bottom** | 0.7-1.0 (deep) | near static; arrows animate |
| 4b | 430-474 | 1.5 | tilt up and crane back from the map into the room | high to eye | | rising | | lantern passes | motion | crane, 12 frames above 1200 px/s |
| 4c | 474-595 | 4.0 | frontal two-shot in a log cabin, window centred, lamp between them (f2_035) | eye | 24-27 e (ceiling and floor both converge hard) | about 3 D (vanishing point at shoulder height) | figure 604 px (0.47 H), head D 150 | ceiling logs (top 15 %) and floor boards (bottom 20 %); lamp and crate at centre | top rows 1.5-1.7 (near ceiling), mid 0.5-0.7 | **static 4 s** (median 37 px/s is the actors) |
| 5 | 595-658 | 2.1 | MCU of the laughing officer, the farmer's helmet in the lower left (f2_042) | low + OTS | **27 m** (f_px 957) | about 1.8-2 D (listener's chest), pitch about 15 deg up (ceiling seen) | head D about 240 (0.19 H), figure cut at the hip | **the listener's helmet and shoulder fill about 25 % of the lower left**; the rifle crosses diagonally | 0.8-1.0 | static (19 px/s) |
| 6 | 658-732 | 2.5 | MS, the farmer walks into the forest with his rifle (f2_046) | eye | **26-27 m** (f_px 939-954) | about 3 D, pitch about 5 deg down | figure 500 px (0.39 H), head D 150 | snowy tree trunks at the left edge | subject 0.2, bg 0.9-1.1 | lateral track 239 px/s, pan 542 px over the shot |
| 7a | 732-774 | 1.4 | thermometer on a trunk at -40 in the foreground left, the prone sniper small at the right (f2_051) | insert + low | 35 e | about 0.8-1 D | head D about 100 | **the trunk and thermometer fill the left 40 %**, then wipe off-frame (v766-776) | 1.0-1.4 on both planes | truck right, about 100 px/s; the trunk crossing is a natural wipe |
| 7b | 774-879 | 3.5 | ground-level MCU, prone sniper puffing snow (f2_053, f2_058) | low (ground) | 30 e | about 0.5 D above the snow | head D 160 (0.125 H) | snow mound across the bottom 35 % | bg trees 0.5-1.0, fg snow 1.2-1.3 | slow push, +6.4 %/s (+131 % over 7a-7b), then a static hold of 60 frames |
| 8 | 879-1024 | 4.8 | low wide, a file of soldiers marching toward the lens; they drop (f2_062) | low | 35 e | about 1.2 D (hip), pitch about 0 deg | front figure 430 px (0.34 H), head D 140 | rails or tracks at the feet run diagonally | 0.4-1.0 | dolly back with them, 87 px/s, then hold |
| 9 | 1024-1096 | 2.4 | high wide, a line of helmets on rifles; day to night time-lapse in the shot (f2_072) | high | 35 e | about 10-15 D, pitch about 25 deg down | none | none | deep (0.5-1.5) | slow push and rise, 99 px/s, +31 % |
| 10 | 1096-1190 | 3.1 | night campfire, five figures, a pine at the left drops its snow (f2_077) | high (mild) | 30 e | about 4 D, horizon just above their heads, pitch about 5 deg down | figures 0.2 H, head D 90 | the pine and tripod lantern fill the left 30 %; long fire shadows lead to the lower right | deep (≤1.1) | **static 3.1 s** (23 px/s) |
| 11 | 1190-1250 | 2.0 | night forest, a small figure far off, a log and ski poles in the foreground; then a smoke wipe (f2_082) | eye | **26 m** (f_px 933) | about 3 D | figure 250 px (0.2 H), head D 70 | **a dark log across the bottom 25 %, ski poles at the right edge**, trees left and right | deep (0.3-1.0) | slow push, 68 px/s; smoke wipe v1236-1249 |
| 12 | 1250-1318 | 2.3 | MS of the general with binoculars, frontal, artillery behind (f2_086) | eye | 35-40 e | about 3 D (horizon across the face) | figure 810 px (**0.63 H**), head D 210 | none; the gun fills the mid-ground | subject 0.3-0.5, bg trees 1.4 | **static** (17 px/s) |
| 13 | 1318-1377 | 2.0 | gun crew firing, wide (f2_090) | high (mild) | **50 m** (f_px 1775) | about 5-6 D, pitch about 10 deg down | figures about 0.25 H, head D 100 | the gun fills the centre-left | deep (0.2-0.9) | near static, recoil shake, 50 px/s |
| 14a | 1377-1440 | 2.1 | big pine, shells exploding all round, the prone sniper tiny (f2_094) | eye | 35 e | about 2 D | head D about 60 | the pine is the subject, centred | deep (0.4-1.4) | slow push, then a fast push into the snow burst (867 px/s p90) |
| 14b | 1440-1483 | 1.4 | out of the snow cloud onto the prone sniper (f2_097) | high (mild) | 30 e | about 2 D | head D 110 | none | 0.7-1.6 | push through the burst (a wipe made of snow particles) |
| 15 | 1483-1567 | 2.8 | the enemy sniper walks in, the camera arcs with him into MCU (f2_101, f2_104) | eye | 30-35 e | about 2.5-3 D | head D 250, rising to 370 (0.29 H) | snowy pine boughs fill the top 40 % | 0.9-1.4 | arc-track then push, 268 px/s, pan 415 px, +49 % |
| 16 | 1567-1622 | 1.8 | wide, the prone farmer under the pine (f2_107) | high (mild) | 50-70 e (vp 66-72, low confidence) | about 2 D | head D 110 | none; the pine trunk sits behind the head | deep (≤0.9) | near static, 34 px/s |
| 17a | 1622-1700 | 2.6 | from behind a log, the enemy sniper prone in mid-ground (f2_112) | high (mild) | **43-48 m** (f_px 1537-1692) | about 2-2.5 D, pitch about 15 deg down | head D 160 | **the snow-covered log runs diagonally across the lower 35 %**; long shadows | 0.6-1.3 | near static |
| 17b | 1700-1824 | 4.1 | he stands up; the camera cranes and pushes into an ECU with the scope glinting (f2_115, f2_121) | low (ends looking up about 5 deg) | 30-35 e | about 2.5 D | standing 560 px (0.44 H), then head D about 420 (0.33 H) cropped | the log at the bottom, then **the rifle at the left edge** | 0.6-1.1 | crane/tilt up (pan y 360 px) plus push, 99 px/s, +76 % |
| 18 | 1824-1908 | 2.8 | POV over the iron sights at sunset, a glint far off (f2_125) | POV | 24-28 e | about 0.6 D | none | **the rifle fills the lower 45 %** | far 0.1 (sharp), **near sights sigma 4-5+** | near static (70 px/s), 1-frame recoil kick at v1884 |
| 19 | 1908-2004 | 3.2 | insert over the shoulder onto the scope glint, then a magnifier icon (f2_129, f2_131) | insert + OTS, high | 35 e | about 45 deg down onto the scope | none | **the scope fills the top-left 45 %; a barrel juts in at the lower right** | bg 2.0 | slow push, 250 px/s, +63 % |
| 20 | 2004-2041 | 1.2 | scope view: a black matte with a round iris and crosshair (2004 is a graphic cut) | POV | 100+ e (telephoto) | | target head D about 30 | the black matte (65 % of frame) | 0.3-1.2 | drift, 39 px/s |
| 21 | 2041-2107 | 2.2 | POV over the sights, glint flaring | POV | 24-28 e | about 0.6 D | none | the rifle fills the lower 45 % | deep | slow push, 137 px/s, +26 % |
| 22 | 2107-2135 | 0.9 | the opening macro again (loop match cut, f2_141/142 = v2107/2122 = v0) | insert | 45-60 e | 0.3-0.5 D | | the prop | 13-19 | static |

## 3. Grammar summary (counts)

**Angles** (35 setups, 71.2 s):

| angle | setups | time | share |
|---|---|---|---|
| eye | 9 | 19.6 s | 28 % |
| high (mild 5-15 deg; strong 25-35 deg only at f2_013 and f2_072) | 9 | 16.9 s | 24 % |
| low (ground 0.5 D, or hip 1.2 D) | 4 | 13.8 s | 19 % |
| POV (through a tool or scope) | 4 | 8.1 s | 11 % |
| insert / macro (prop) | 6 | 6.3 s | 9 % |
| OTS (shoulder or prop in the foreground) | 2 | 5.3 s | 7 % |
| top (map, about 70 deg) | 1 | 1.2 s | 2 % |
| Dutch | **0** | 0 | 0 % |

Roll appears only inside the two fly-through openers (sums 16 and 23 deg over 4-7 s). Static horizons are level (roll per shot ≤0.3 deg in shots 10, 12 and 13).

**Lens.** Measured: 26, 26-27, 27, 38, 43-48 and 50 mm (and 66-72 mm, low confidence). The character MS/MCU shots measure 26-27 mm (shots 5, 6, 11). Long lenses (43-50 mm) are used for wides that stack layers (gun crew, log foreground). The POV-over-sights shots look like 24-28 mm (the barrel converges hard). Macro props are about 45-60 mm with heavy defocus. **Median about 30-35 mm**, the same as ref C's 31-37 mm.

**Camera height.** At or below the head in 22 of 35 setups. Eye 2.5-3 D (the horizon through the face or shoulders). Low 0.5 D (ground level, prone subjects) or 1.2 D (hip, walkers). High (mild) is 2-6 D with pitch 5-15 deg. Only 2 setups go to 8-15 D (pitch 25-35 deg).

**Character size.** Full-figure shots: figure 0.34-0.47 H (head D 140-150 px). Big-hero MS: 0.63 H (head D 210). MCU: head D 240-300 (0.19-0.23 H). ECU: head D 370-420 (0.29-0.33 H). Tableau wides: 0.2 H (head D 70-90). Tiny-in-world: head D 60-110 (shots 3f, 7a, 14a, 16). Faces stay readable: head D is at least 70 px whenever the character is the story point.

**Foreground framing** appears in 19 of 35 setups. Five kinds:
- (a) A prop held up to the lens: rifle or sights (shots 1c, 2, 18, 21) or the scope (19).
- (b) A natural wipe object crossing the frame: the thermometer trunk (7a), the snow burst (14), smoke (11).
- (c) Frame in a frame: door jambs (3c), ceiling and floor (4c).
- (d) Diagonal ground pieces: a log (11, 17), ski tracks or rails (3f, 8), a snow lip (1a, 7b).
- (e) OTS: a shoulder or helmet (5).

Foreground objects take **25-45 %** of the frame and are **dark or saturated** against a bright, hazy background.

**Depth of field** (`dof.json` over 142 stills):
- Wides and tableaux: deep. Background sigma ≤1.0 px in 70 % of stills.
- Character MS/MCU: mild. Background 0.9-1.4 px, subject 0.2-0.5 px, a ratio of about 3x. This is **less** blur than ref C's MCU (2.5-3 px).
- Scope insert: 2 px.
- POV over the sights: far plane sharp (0.1-0.8 px), near prop 2-5+ px.
- Prop macros: background **13-19 px**. These are the only shallow shots and they bookend the film.

**Motion** (all 2135 frames):
- Median corner speed 83 px/s (IQR 22-256).
- Near static (<60 px/s): 41 %. Drift (60-450 px/s): 44 %. Snap (>450 px/s): 15 %.
- Frames above 1200 px/s: 33. All of them are in the two fly-through openers (shots 1 and 3) and in the crane of 4b.
- Types: static hold ×9 (2-4 s each: 3c, 3f, 4c, 5, 10, 12, 13, 16, 17a); slow push ×9 (+6 to +24 %/s); track or arc with a walker ×3 (6, 8, 15); crane or tilt ×2 (4b, 17b); whip-follow of a prop ×2 (1b, 3b); crash zoom ×1 (4 frames); snap push ×1 (6 frames); recoil shake ×2 (1-3 frames).

**Transitions:**
- 21 hard cuts (19 plain).
- 1 graphic-match push into the poster that becomes the next scene (v312-354).
- 1 matte cut into the scope iris (v2004).
- 1 loop match cut from the last frame to the first (v2107 = v0).
- In-shot wipes: trunk (v766-776), snow burst (v1430-1450), smoke (v1236-1249).
- **No dissolves, no flashes, no torn-paper wipes.**

**Rhythm.** The edit alternates **macro/POV (0.4-3 s) → tableau held still (2-4 s) → character MS/MCU (2-3 s)**. Each new location opens on a wide or high tableau (shots 3f, 4c, 8, 9, 10, 11, 13, 16), then goes closer.

## 4. Eight shot templates for EP.1 (`v4/animatic/timing.py`, 24 shots, 53.3 s)

All heights are in D (Kong's head D; Kong is about 3.5 D tall). Night and rain stay: rain haze does the depth work that snow haze does in ref D. House rules from `refC_camera.md` §9 still apply (no Cycles DoF; compositor Defocus from the Z pass).

| # | template (ref) | camera | lens | subject size | foreground | DoF bg sigma at 720 w | move | length |
|---|---|---|---|---|---|---|---|---|
| T1 | **Prop macro, bokeh behind** (shots 1a, 22; f2_001, f2_142) | 0.3-0.5 D above the surface, at the prop | 50 mm | prop 0.15-0.25 H; the character's head behind at 250-300 px, defocused | the prop is the subject; a wet lip (bumper or asphalt) covers the bottom 25-30 % | **13-19 px** (beacons become round bokeh) | static 0.4-1.0 s, or a slow push of ≤6 %/s | 0.9-1.7 s |
| T2 | **Prop-follow fly-through with crash zoom** (1b, 3b; f2_003, f2_014) | 1-2 D over the car roofs, pitch 20 deg down, chasing a moving thing (a radio wave or rain gust, a thrown flare) | 35 mm | none until it lands | none | motion blur only | follow at 900-1200 px/s, roll ≤8 deg, then a **4-frame radial crash zoom** onto the destination | 1.2-2.0 s |
| T3 | **Frontal one-point tableau, held** (3c, 4c, 12; f2_019, f2_035, f2_086) | eye 2.5-3 D, horizon across the face or shoulders, pitch 0, frame centred | 26 mm (cramped or inside a car), 35-40 mm (outside) | figure 0.41-0.63 H, head D 140-210 | frame in a frame: door pillars, windshield frame, guard-rail posts | subject 0.3-0.5, background **1.0-1.4** | **static**; only the characters move | 1.8-4.0 s |
| T4 | **Low OTS MCU** (5; f2_042) | at the listener's chest, 1.8-2 D, pitch 15 deg up (the underpass ceiling or rain in view) | 27 mm | speaker head D 240 (0.19 H), cut at the hip | the listener's helmet and shoulder take the lower-left 25 %, dark against the lit speaker | 0.8-1.0 | static, or a push of ≤3 %/s | 1.8-2.5 s |
| T5 | **Ground-level foreground wipe, then a slow push** (7a-7b; f2_051, f2_058) | 0.5-1 D, near the asphalt | 30-35 mm | head D 100, growing to 160 | a dark object (wheel, crumpled fender, fallen sign) takes the left 40 % and crosses out of frame over about 10 frames | 1.0-1.3 on both planes | truck about 100 px/s past the object, then push +6 %/s | 2.5-4.0 s |
| T6 | **Low walking track** (6, 8; f2_046, f2_062) | hip 1.2 D (toward the lens) or eye 3 D (side track), pitch 0-5 deg | 27-35 mm | figure 0.34-0.39 H, head D 140-150 | lane markings or a guard rail running diagonally at the feet | 0.9-1.1 | lateral track 200-240 px/s, or a dolly back at about 90 px/s | 2.4-4.8 s |
| T7 | **High establishing tableau** (3a, 9, 10, 13; f2_013, f2_072, f2_077, f2_090) | mild 4-6 D with 5-15 deg pitch for groups; strong 10-15 D with 25-35 deg pitch for scale | 35-50 mm (the long lens stacks the car rows) | figures 0.05-0.25 H, head D 70-100 | a near tree, sign or pillar on one side, 25-30 % | deep (≤1.0) | static or a slow push/rise at 70-100 px/s; a light change inside the shot is allowed | 2.0-3.1 s |
| T8 | **POV through the tool** (2, 18, 21; f2_011, f2_125) | the holder's eye, 0.6-1 D crouched or 3 D standing | 24-28 mm | target small and central, head D about 30-60 | **the tool fills the lower 40-45 %**, dark and centred | tool **4-5 px**, far plane sharp | creeping zoom +25 to +55 %/s, or static with a 1-3 frame kick | 1.8-2.8 s |

**Mapping to the EP.1 shot list** (captions translated):

| EP.1 | t (s) | caption (gist) | template | notes |
|---|---|---|---|---|
| S01 | 0.00-3.39 | "Centre, casualty not responding... wait! hey!" | T1, then a cut to T4 | Macro of the radio handset on the wet dash with Kong blurred behind; the "เฮ้ย" lands on a cut |
| S02 | 3.39-5.74 | "then the radio went silent" | T1 | Hold the static radio LED, 0.4 s static, then push |
| S03 | 5.74-7.53 | "Friday night, rain pounds Bangkok" | T7 strong | 12 D, pitch 25 deg, 45 mm |
| S04 | 7.53-9.30 | "on the expressway, a pile-up" | T2 | Follow a rain gust or beacon flare along the lanes; crash zoom onto the wreck |
| S05 | 9.30-11.10 | "stretching out of sight" | T7 | 50 mm stacking the rows; slow rise |
| S06 | 11.10-12.62 | "Kong, rescue worker" | T3 | Frontal, between two car pillars, 0.55 H |
| S07 | 12.62-14.41 | "standing beside the crumpled car" | T5 | Wipe past the crushed fender |
| S08 | 14.41-16.22 | "in his hand, the cordless cutter" | T1 | Cutter jaws, Kong defocused behind |
| S09 | 16.22-17.55 | "battery, 3 bars" | T1 | Static 1.0 s hold to read the bars |
| S10 | 17.55-19.05 | "the phone buzzes" | T1 | Phone in the jacket pocket |
| S11 | 19.05-22.17 | "4 missed calls from his daughter" | T8 | Kong's POV onto the phone; the hand fills the bottom |
| S12 | 22.17-24.94 | "Dad, you promised to pick me up" | T4 | Over the phone/shoulder onto Kong's face |
| S13 | 24.94-27.34 | "urgent case, wait a little" | T3 | Static MCU, head D 240-300 |
| S14 | 27.34-28.96 | "every time..." | T1 | Phone screen |
| S15 | 28.96-30.35 | "I'll call you back" | T4 | |
| S16 | 30.35-33.40 | "the line goes quiet, then hangs up" | T7 mild | Kong small in the gridlock, static 3 s |
| S17 | 33.40-34.61 | "Kong! It's open!" | T4 | The crew shouts over Kong's shoulder |
| S18 | 34.61-37.62 | "in the car the driver sits motionless" | T3 | Frontal through the windshield frame, 26 mm, static |
| S19 | 37.62-40.28 | "the young crew member leans in" | T5 | Ground level past the door edge, slow push |
| S20 | 40.28-43.45 | "the driver slowly lifts his head" | T8 | The crew's POV through the window frame; slow creep +25 %/s; the Dutch roll comes after the lift, per the brief |
| S21 | 43.45-45.30 | "it lunges and bites" | T3 | Hard cut; hold wide so the action reads; 1-3 frame shake |
| S22 | 45.30-46.43 | "Kong doesn't know yet" | T6 | Kong turned away, side track |
| S23 | 46.43-47.78 | "in 60 seconds" | T1 | The cutter battery or a stopwatch prop |
| S24 | 47.78-53.32 | "his friend won't be human anymore" + title | T7 strong | Rise to 12-15 D; optionally a loop match back to S01's macro |

Budget check for this mapping (by count): T1 7, T3 4, T4 4, T7 4, T5 2, T8 2, T2 1, T6 1. By time this is about 30 % insert/POV, 25 % eye, 20 % high, 15 % OTS/low and about 10 % other. That is close to ref D's 20 % insert/POV/top, 28 % eye, 24 % high and 26 % low/OTS, with more inserts because EP.1's captions name props (cutter, battery, phone). If a shot has to drop, cut a T1 phone insert before a T3 tableau.

**Numbers to keep:**
- Hard cuts on caption boundaries.
- Hold length: shot median 2.2-2.6 s, never under 0.9 s.
- At least 40 % of frames below 60 px/s.
- Whips only in T2.
- No dissolves.
- Character DoF ≤1.4 px; prop macros 13-19 px.
- Foreground framing in about half the setups, at 25-45 % of the frame.
