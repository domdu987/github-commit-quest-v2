# Faces, expressions and head rendering — measured spec

Lens: faces, expressions, head rendering. Reference clips A (railroad) and B (jar). All numbers were measured with
numpy/cv2 on frames decoded straight from the source videos; the frame each number came from is cited as
`a16.0` = clip A reference frame `t16.0.jpg`, `a f1652` = clip A video frame index 1652.

Working files (all inside the allowed folders):

| what | path |
|---|---|
| SVG reference implementation of everything below (runs, verified) | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/spec/face_proto/faces_ref.py` |
| its rendered sheet of 24 faces | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/spec/face_proto/out/sheet.png` |
| reference (rows 1,3) vs prototype (rows 2,4) | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/spec/face_proto/cmp_ref_vs_proto.jpg` |
| Chromium rasteriser | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/spec/face_proto/raster.js` (`NODE_PATH=/opt/node22/lib/node_modules node raster.js in.svg out.png W H`) |
| normalised reference face tiles (head upright, 0.1 D ticks) | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/ref/crops/face/norm_A_0.jpg` … `norm_A_2.jpg`, `norm_B_0.jpg` … `norm_B_2.jpg` |
| zooms / frame sequences | same folder: `zoom_eyes.jpg zoom_mouths.jpg zoom_fx1.jpg … zoom_fx4.jpg zoom_hats.jpg zoom_sweat.jpg seq_a_blink_everyframe.jpg seq_a_boss_talk.jpg seq_a_purple.jpg seq_b_inv_talk.jpg seq_b_emp.jpg seq_shock.jpg seq_Z.jpg` |
| measurement scripts and raw tables | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/ref/crops/face/tools/` (`featA.txt`, `featB.txt` are the raw per-feature tables) |
| lossless frames decoded from the videos (half-second grid; the scripts re-extract any other frame on demand) | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/ref/extra/face/` |

## 0. Conventions

- **Frame mapping (calibrated):** reference `tX.X.jpg` is video frame index `30*X + 6` in both clips, counting decoded frames from 0 (OpenCV read count; ffmpeg `select='eq(n,66)'`). E.g. `t02.0` = frame 66. Times quoted in seconds are `(index − 6)/30`, i.e. on the same clock as the reference file names.
- **D** = outer head diameter, ink to ink. Measured as `D = 2.16 * R_fill`, where `R_fill` is the radius of the circle fitted to the inner edge of the head outline over the visible lower arc (the hat hides the top).
- **Coordinates:** origin = centre of the white fill disc, `u` to the right, `v` DOWN, both in units of D, in the head's own frame (the roll of the head is removed using the line through the two eyes). Angles around the head: 0° = 3 o'clock, 90° = bottom, 180° = 9 o'clock.
- An eye "centre" is the centre of the eye's bounding box (for the half-lid eye that box includes the lid bar).

## 1. Observations

### 1.1 The head is a flat 2D drawing, not a lit sphere
- Every head in both clips is a flat disc with a thick hand-inked outline and one soft shadow crescent. There is no spherical falloff, no specular spot, no terminator (a02.0, a16.0, a46.0, a55.0, b00.0, b05.5, b17.0, b22.0). Features never foreshorten when the head turns: they keep their shape and slide sideways (a16.5, a46.0, b00.0).
- The outline is **not uniform**: thin on the left and upper left, thick on the right and lower right, as if the white disc were shifted up-left inside a black disc. It keeps that orientation even when the character sprite is mirrored (b05.0, hairpin bead on the right, still thick on the right).
- The outline wobbles like a brush line: 1.0 to 1.5 % D rms away from a circle, up to 2 to 5 % D (a16.0, a55.0, b05.5, b00.0).
- Ink is never pure black. Clip A: dark plum `#3a2a30` (a16.0, a46.0, a55.0 all within ±3 per channel). Clip B takes the scene grade: `#413c42` hall (b00.0), `#463e36` throne room (b05.5), `#55382c` warm throne (b22.0), `#311a34` night (b34.5), `#1e142e` night guard (b42.0). Outline and all features use the same ink.
- The whole head (hat included) rolls a lot for acting: +30° (a00.5), −19° (a15.0), +15° (a23.5), +16° (a37.0), +19° (b06.0), +22° (b18.5), −12° (b25.0). An upright head is the exception in dialogue shots.

### 1.2 Feature vocabulary (same in both clips)
- **Half-lid eye is the default eye.** A thick horizontal lid bar with a black U-shaped pupil hanging under it, a "T"/mushroom (a02.0, a13.5, a16.0, a20.0, a46.0, b00.0, b05.5, b17.0, b25.0). Neutral, smug, determined, angry, worried and sad all use it; only brows, lid tilt and mouth change.
- **Ring eye** for surprise or excitement: an ink ring with a white inside and a small dot pupil (a13.0, a14.0, a29.5, a33.5, a54.0, a55.0, a56.0, b00.5, b05.0, b35.5, b39.0). Pupil is 0.06 D when excited, 0.033 D when frightened.
- **Happy eye**: an upside-down U arc (a00.5, a27.5, a53.5, a58.5, b06.0, b24.0, b28.5).
- **Closed eye**: a flat line (a23.5, a28.0, a55.5, b04.5, b19.0, b22.0, b33.0). Also the middle frame of every blink.
- **Dot eye**: a tall black oval, used rarely (a45.0 boss grin, b41.0 guard).
- **Squeezed eye** `> <`: two strokes per eye converging on the nose (a03.0 hero shouting, a f506 to f510 boss before turning purple).
- **Brows** are separate strokes floating above the eyes: a solid flat-bottomed dome for the hero (a46.0), a heavy tapered stroke for the boss (a13.5, a15.0), thin strokes for clip B (b00.0). Often only ONE brow is drawn (the raised one): a46.0 boss, b05.5, b22.0, b25.0, b26.5.
- **Mouths**: short dash (a46.0 hero, a56.0), small arch frown (a13.5, a16.0), lopsided smirk (a02.0, a20.0, a47.5), small smile (a27.5, a53.5), wide crescent grin with four upper teeth (a12.5, a13.0, a45.0, a55.0, b28.5), flat wide bar (a46.0 boss), maroon open ellipse while talking (a46.5, b04.0), egg-shaped "O" (a54.0, a64.5, b41.0), clenched 4x2 tooth grid (a03.0, a17.0, a17.5, a20.5, b19.0, b36.0), wavy worried line (a37.0, b35.5, b44.5), drooping moustache that doubles as the upper lip (b05.5, b17.0, b22.0, b25.0).
- No nose, no ears, no eyelashes, no cheek line, ever.

### 1.3 Three-quarter view
- A turn is faked by sliding eyes, brows and mouth together toward the facing side, squeezing the eye spacing and shrinking the far eye a little. The head disc itself does not change. A hair patch fills the side the face has slid away from (a16.5, a46.0, a20.0).
- Clip A mostly uses a small slide (0.03 to 0.06 D); clip B characters stand almost permanently in a strong slide (0.12 to 0.14 D) (b00.0, b05.5, b22.0, b41.0, b44.5).
- Pitch is faked the same way: looking up or proud moves everything up about 0.09 D (a16.0 low angle, b25.0, b26.5); looking down or sad moves it down about 0.07 D (b44.5).

### 1.4 Head shading
- Base fill is a single flat colour, a barely warm white `#fef7f6` in clip A (a02.0, a16.0, a46.0, a55.0, a56.0 all identical).
- One soft **lavender crescent** `#e9dceb` hugs the lower-right rim. It is widest (about 0.09 D) around 50° (lower right), about 0.07 D at 0° and 90°, 0.045 D at 135°, almost gone at 180°, absent on the upper left. Its inner edge is airbrushed over about 0.04 D (a55.0, a46.0, a16.0, b05.5, b13.5).
- The crescent is part of the head drawing, not lighting: it does not flip with a mirrored sprite (b05.0) and ignores where the scene light is. Its centre sits near 50° on most heads but drifts between about 20° (a33.5, a54.0) and 100° (a14.0: shadow from 45° to 135°; a20.0: 45° to 180°).
- There is no highlight and no rim light on white heads.
- Clip B multiplies the whole head by the scene grade and sometimes adds a soft coloured glow from a local light: cream `#f8f8ef` throne room (b05.5), cool white `#f5f9fd` hall with a yellow fire glow `#f9f7dc` creeping in from the left rim (b04.0), peach `#fce1ce` under red light (b22.0), pink `#fbc8d9` by lantern at night (b44.5), periwinkle `#b4b0e8` at night without a lamp (b42.0). The crescent stays, about 8 to 12 % darker than the base, in every case.

### 1.5 Hats and hair
- Hats are 2D drawings as well, inked like the head, painted with two or three flat tones and a glossy streak; they are not 3D-lit (a16.0, a27.5, a33.5, a55.0, a23.0).
- The hat sits low: its lower edge crosses the head at v = −0.21 (a55.0 cap), −0.25 (a16.0 bowler), −0.29 (b05.5 crown), so the top 20 to 30 % of the head is never seen and brows sit right under the brim (angry boss brows touch it, a16.0).
- Hair is a flat patch inside the head outline on the side away from the face, with a ragged inner edge: hero brown `#634025` (a46.0), boss grey `#988c98` (a15.0, a46.0).

### 1.6 Cartoon effects seen
- **Purple anger** (a17.0 to a19.5): purple rises from the chin like liquid, with a lighter wavy surface line and two or three ring bubbles, fills the head in 8 frames, then steam puffs pump out of both sides at hat-brim height for as long as the anger lasts.
- **Sweat drop** on the temple, overlapping the head outline, partly tucked under the hat brim (a29.0, a29.5, a33.5, a37.0, a47.0, a54.0, b04.5, b05.0, b35.5, b39.0).
- **Laugh tears** squirting sideways from the outer eye corners in chains of two or three drops, plus pink blush under the eyes (b06.0, b06.5, b07.0, b24.0).
- **Sleep Z** letters: three bold italic Z on screen at once, drifting up from the head in a zig-zag, fading in at the bottom, growing as they rise and fading out at the top (b33.0, b33.5, b34.0).
- **Hair standing on end** for a jump scare: 8 or 9 short ink strokes radiating from the top half of the head while the whole body leaps up (b f1084 to f1094, b36.0).
- **Focus lines**: thin white radial streaks over the background converging on the character, redrawn every frame (b f146 to f156, b05.0).
- **Stubble**: about 60 to 80 dark specks on the lower third of the face plus a cobweb, used as a "weeks later" gag (b18.5, b19.0).
- **Eye glint**: one 2 px light dot in each pupil in the dark close-up of the guard (b42.0). Not used in daylight.
- Not found in either clip: impact stars, speech bubbles, vein/anger marks, question or exclamation marks.

### 1.7 Animation of the face
- **Blink** = three drawings, one frame each: half (ring squashed to an almond, 0.22 x 0.08 D, mostly ink), closed (flat line), half, then open. 4 to 5 frames in all (a f1651 to f1655, a f1669 to f1673, a f1692 to f1694, b f1080 to f1082).
- **Every change of expression is hidden behind a blink.** The eyes close, and the new eyes and mouth are there when they open (a f1646; a f1670 to f1673 grin becomes small mouth; b f98, f108, f118, f130, f142; b f740). During lively speech this happens every 10 to 12 frames (clip B, 3.07, 3.40, 3.73, 4.13, 4.53 s); in the clip A close-up every 0.6 to 0.73 s (54.87, 55.47, 56.20 s). A character can also go 1.8 s without blinking while talking (boss, a f1380 to f1435).
- **Lip sync**: the mouth is redrawn every 1 to 3 frames while the character talks, cycling flat bar, half-open ellipse, wide-open ellipse and small round "o"; the biggest shape is held up to 4 frames (a f1399 to f1402). Eyes and brows hold still meanwhile (a f1380 to f1435).
- During a blink the mouth eases toward the next shape (grin width 0.41, 0.36, 0.32 D over a f1668 to f1671).

## 2. Measurements

### 2.1 Head disc and outline

| quantity | value | frames |
|---|---|---|
| fill radius R_fill / D | 0.463 (by definition D = 2.16 R_fill) | all |
| outline width, right (0° to 30°) | 4.4 to 6.7 % D, median 5.0 | a55.0 4.8, a56.0 4.7, a16.0 4.6, b05.5 5.4, b22.0 6.0, b17.0 5.9, b00.0 4.7, a46.0 hero 4.4 |
| outline width, lower right (30° to 90°) | 5.4 to 7.8 % D, median 6.6 | a55.0 5.4/7.4, a56.0 5.4/7.5, a16.0 6.0/7.5, b05.5 6.7/6.6, b17.0 6.2/6.8, a14.0 6.9/7.8 |
| outline width, bottom (90° to 120°) | 6.5 to 8.3 % D (inflated by the collar touching the chin) | a55.0 7.7, a56.0 8.3, a16.0 6.5, b05.5 6.5 |
| outline width, lower left (120° to 180°) | 2.0 to 4.4 % D, median 3.0 | a55.0 4.4/2.9, a16.0 3.1/2.5, b05.5 3.0/2.0, b17.0 2.5/2.1, b00.0 2.1/1.4 |
| outline width, left (180° to 210°) | 1.5 to 2.8 % D, median 2.0 | a55.0 2.2, a56.0 1.5, a16.0 1.5, b05.5 2.0, b17.0 1.6, b22.0 2.8 |
| outline width, top | cannot be measured (always under a hat or hair) | — |
| outline wobble (inner ink edge vs best circle, lower arc; includes the neck and hair junctions, so the pure line wobble is lower, about 0.5 to 0.8 %) | rms 1.0 to 1.5 % D, max 2.0 to 5.5 % D | a16.0 1.01/2.3, a55.0 1.25/3.3, a54.0 1.43/4.1, b05.5 1.06/2.9, b00.0 1.51/5.5, b17.0 1.02/2.0 |
| ink colour | `#3a2a30` clip A; scene-tinted in clip B (see 1.1) | a16.0, a46.0, a55.0 |
| head roll used for acting | −19° to +30° | a15.0, a00.5 |
| head D on screen (720x1280) | close-up 325 to 390 px (a15.0 324, a55.0 351, b05.0 377, b33.5 389); medium 190 to 250 px (a02.0 199, a16.0 190, a46.0 boss 239, a14.0 245); wide 100 to 180 px (b28.5 103, b36.0 111, a27.5 159, a13.5 167, b17.0 181) | as listed |

### 2.2 Head fill colours (lit side / centre / shadow crescent)

| frame | scene | lit side (upper left, r/R 0.6 to 0.9) | centre | shadow crescent (lower right rim) |
|---|---|---|---|---|
| a55.0 | canyon, day | `#fef7f3` | `#fef7f4` | `#e8dcec` |
| a56.0 | canyon, day | `#fef7f5` | `#fef7f5` | `#e9dced` |
| a16.0 | sky behind | `#fcf7f6` | `#fef7f6` | `#eddcea` |
| a46.0 hero | canyon, day | `#fef7f6` | `#fef7f6` | `#e9deeb` |
| a33.5 | station interior | `#fef7f6` | `#fef7f6` | `#e7dbe8` |
| b05.5 | throne room | `#f8f8ef` | `#f8f8ef` | `#ebe0e6` |
| b13.5 | balcony, day | `#f8f8f1` | `#faf7f2` | `#e8dddf` |
| b28.5 | city gate, day | `#fffbed` | `#fff8ea` | `#f5dedc` |
| b22.0 | throne, warm grade | `#fce1cd` | `#fde1ce` | `#edc6c4` |
| b04.0 | hall, fire at left | `#f9f7dc` (fire glow at the left rim) | `#f7f8fc` | `#f3ebf6` |
| b44.5 | night, lantern | `#e8c1da` | `#fbc8d9` | `#ebb1cb` |
| b42.0 | night, no lamp | `#c5b3e4` | `#b4b0e8` | `#9697dd` |
| a18.0 purple | anger | `#b769e3` (upper left) | `#af65d9` | `#7c35a8` (bottom), `#7f36aa` (lower right) |

Crescent geometry (a55.0, a46.0, a16.0, b05.5 radial profiles): inner edge at r/R_fill = 0.83 to 0.85 at 0°, 0.78 to 0.80 at 45°, 0.80 at 90°, 0.88 to 0.90 at 135°, 0.96 at 180°; full shadow colour is reached 0.08 to 0.10 R_fill further out. Crescent over base is a multiply of about (0.92, 0.89, 0.955) in clip A.

### 2.3 Feature geometry (all in D)

| feature | size (w x h) | stroke | frames |
|---|---|---|---|
| half-lid eye, whole | 0.168 to 0.181 x 0.092 to 0.104 | — | a46.0 0.168x0.092 and 0.180x0.098; a02.0 0.176x0.096; a13.5 0.174x0.091; a16.0 0.174x0.099 |
| lid bar | 0.175 to 0.181 long | 0.028 to 0.030 | a46.0, a02.0, a16.0 (row profiles) |
| pupil under the bar | 0.084 to 0.090 wide at the bar, 0.068 tall, rounded bottom (half ellipse rx 0.043, ry 0.062) | — | a46.0 0.083 to 0.088; a02.0 0.085 to 0.090; a13.5 0.085 to 0.090 |
| pupil sideways gaze shift | 0 to 0.03 | — | a02.0 +0.028, a47.0 +0.02, a46.0 0.00 |
| ring eye, outer diameter | 0.21 to 0.225 (boss shock 0.245 to 0.253) | ring 0.023 to 0.028 | a55.0 0.225x0.205; a56.0 0.221 to 0.224; a13.0 0.214 to 0.220; a54.0 0.209 to 0.218; a33.5 0.211 to 0.221; a14.0 0.245 to 0.253 |
| ring eye pupil | 0.058 to 0.068 excited; 0.032 to 0.034 frightened; offset up to 0.03 | — | a55.0 0.060; a13.0 0.058; a14.0 0.066 to 0.068 (offset +0.027,+0.03); a54.0 0.033; a33.5 0.032 to 0.034 |
| happy arc eye | 0.14 to 0.165 x 0.057 to 0.061 | 0.027 to 0.030 | a27.5 0.163x0.061; b06.0 0.163x0.058; b28.5 0.165x0.057; b24.0 0.163x0.060 |
| closed-line eye | 0.156 to 0.170 x 0.025 to 0.030 | = height | a55.5 0.161 to 0.167 x 0.027; a23.5 0.156x0.025; b22.0 0.167x0.029; b19.5 0.170x0.027 |
| blink half frame (almond) | 0.218 to 0.221 x 0.080 to 0.083 | — | a f1652, a f1670 |
| dot eye | 0.074 to 0.085 x 0.105 to 0.115 | — | a45.0 0.079 to 0.085 x 0.115; b41.0 0.074 to 0.083 x 0.105 to 0.115 |
| squeezed eye strokes | lower 0.163 to 0.177 long, upper 0.149 long at 24° | 0.029 to 0.036 | a03.0 |
| brow, hero dome | 0.153 to 0.162 x 0.038 to 0.041, flat base | filled | a46.0 |
| brow, boss stroke | 0.161 to 0.164 long | 0.048 to 0.050 | a13.5, a46.0 |
| brow, angry | 0.196 to 0.22 long, 24° (inner end down) | 0.052 to 0.057 | a14.0, a15.0 |
| brow, hero angry / worried | 0.164 to 0.178 long, 17° / 9° | 0.038 to 0.042 | a47.0, a37.0 |
| brow, clip B | 0.13 to 0.165 long, 11° to 13° | 0.025 to 0.035 | b00.0, b04.5 |
| brow, sad | 0.164 to 0.178 long, 25° to 30° outer end down | 0.037 to 0.039 | b44.5, b45.5 |
| brow height above eye centre | neutral 0.12 to 0.14; angry: inner end 0.09, outer end 0.14 to 0.15 (inner ends touch the lid bars); raised 0.20 to 0.25 | — | a13.5 0.123, a46.0 0.136 and 0.140 / a47.0 0.087 and 0.142, a15.0 0.152 / a27.5 0.20, b19.5 0.21 to 0.25, b26.5 0.236 |
| mouth, dash | 0.097 to 0.102 x 0.030 to 0.037 | = height | a56.0, a46.0 hero |
| mouth, boss arch frown | 0.121 to 0.127 x 0.036 to 0.041 | 0.034 | a13.5, a16.0 |
| mouth, smirk | 0.110 x 0.056, long axis 24° | 0.032 | a02.0 |
| mouth, small smile | 0.145 x 0.055 | 0.038 | a27.5 |
| mouth, grin crescent | 0.40 to 0.45 x 0.12 to 0.155; top edge sags 0.03 at the middle | — | a55.0 0.410x0.122; a45.0 0.436x0.133; a13.0 0.453x0.155; b28.5 0.398x0.136; a12.5 0.410x0.135 |
| grin teeth | 4 teeth, each 0.057 to 0.065 wide, gaps 0.013 to 0.019, band 0.048 to 0.060 tall, band spans 0.27 to 0.30 | — | a55.0, a45.0, a13.0, b28.5 |
| mouth, flat bar (smug, between words) | 0.286 x 0.058 | filled | a46.0 boss |
| mouth, talking | width 0.14 to 0.31, height 0.04 to 0.17; wide open 0.284 x 0.169; round "o" 0.18 x 0.12 to 0.15 | outline 0.018 | a f1380 to f1435, a46.5; b04.0 0.254x0.083 |
| mouth, "O" shock | 0.169 to 0.191 x 0.138 to 0.168 | outline 0.018 | a54.0, b41.0 |
| mouth, clenched teeth | 0.164 to 0.185 x 0.126 to 0.137 (0.206 x 0.136 in the purple close-up); 4x2 cells of 0.016 to 0.032 x 0.027 to 0.042; corner radius about 0.04 | frame 0.021 to 0.027, dividers about 0.013 | a03.0, b19.0, b19.5, a17.5 |
| mouth, wavy worried | 0.25 to 0.27 x 0.077 to 0.097 | 0.039 to 0.042 | a37.0, b35.5 |
| moustache (emperor) | 0.325 to 0.35 x 0.148 to 0.163 | 0.037 to 0.044 | b05.5, b17.0, b22.0 |
| mouth interior | `#4d2433` (a46.5), `#4c2632` (a54.0); faint tongue/teeth dashes `#7b626c` | — | a46.5, a54.0 |
| teeth | `#fef9f8` | — | a55.0 |

### 2.4 Feature positions, frontal or near-frontal heads

| frame | expression | left eye u | right eye u | eyes v | brows v | mouth (u, v) | eye spacing | eye to mouth |
|---|---|---|---|---|---|---|---|---|
| a55.0 | wide grin | −0.132 | +0.129 | +0.045 | — | (+0.002, +0.223) | 0.261 | 0.178 |
| a56.0 | wide, small mouth | −0.133 | +0.127 | +0.045 | — | (−0.004, +0.224) | 0.260 | 0.179 |
| a55.5 | blink in grin | −0.134 | +0.128 | +0.053 | — | (0.000, +0.241) | 0.262 | 0.188 |
| a02.0 | half-lid smirk | −0.105 | +0.154 | +0.056 | — | (+0.002, +0.223) | 0.259 | 0.167 |
| a13.5 | boss neutral frown | −0.125 | +0.139 | −0.019 | −0.114 / −0.142 | (+0.008, +0.167) | 0.264 | 0.186 |
| a16.0 | boss angry, low angle | −0.116 | +0.147 | −0.065 | merge with brim | (+0.007, +0.131) | 0.263 | 0.196 |
| a45.0 | boss dot-eye grin | −0.131 | +0.133 | 0.000 | — | (+0.001, +0.201) | 0.264 | 0.201 |
| a27.5 | tycoon happy | −0.123 | +0.146 | −0.031 | −0.231 / −0.229 | (+0.008, +0.160) | 0.269 | 0.191 |
| a54.0 | tycoon shock | −0.098 | +0.154 | −0.059 | — | (+0.028, +0.146) | 0.252 | 0.205 |
| a37.0 | hero worried | −0.128 | +0.139 | +0.021 | −0.112 / −0.089 | (+0.006, +0.239) | 0.267 | 0.218 |

Summary: eye spacing 0.26 D (0.252 to 0.269); eye line v = 0.00 to +0.055 in a level pose (take +0.03); mouth centre 0.18 D below the eye line (0.167 to 0.205); neutral brows 0.13 D above the eye line.

### 2.5 Three-quarter view: how far the features slide

Shift = midpoint of the two eyes; far/near = width of the far eye divided by the near eye.

| degree | frames | shift of eye midpoint | eye spacing | far/near eye size | mouth u |
|---|---|---|---|---|---|
| frontal | a55.0, a56.0, a13.5, a45.0 | 0.00 to 0.016 | 0.26 | 1.00 | 0.00 |
| slight | a46.0 boss (−0.025), a33.5 kid (−0.030) | 0.025 to 0.03 | 0.236 to 0.251 | 0.95 to 0.98 | −0.023 / −0.029 |
| medium | a46.0 hero (−0.055), a47.0 hero (−0.058), a54.5 hero (+0.074) | 0.055 to 0.075 | 0.220 to 0.230 | 0.92 to 0.93 | −0.053 / −0.069 / +0.071 |
| strong | a16.5 boss (−0.105), a29.0 (−0.080), b00.0 (+0.142), b05.5 (−0.126), b22.0 (−0.138), b44.5 (−0.124), b41.0 (+0.123) | 0.08 to 0.14 | 0.167 to 0.205 | 0.85 to 0.89 | −0.097, −0.070, +0.125, −0.096, −0.113, −0.115, +0.108 |
| pitch up (proud, low angle) | a16.0 (eyes v −0.065), b25.0 (−0.065), b26.5 (−0.097) | vertical −0.09 to −0.13 from the level +0.03 | — | — | follows |
| pitch down (sad) | b44.5 (eyes v +0.099) | vertical +0.07 | — | — | follows |

Brows and mouth slide by the same amount as the eyes (mouth 0.85 to 1.0 of the eye shift). The head disc, outline and crescent do not move.

### 2.6 Effects

| effect | geometry (D) | colours | frames |
|---|---|---|---|
| purple face fill | radial gradient, light centre displaced toward the upper left | `#b769e3` upper left / centre, `#a152cd` mid, `#7c35a8` to `#7f36aa` lower-right rim | a17.5, a18.0, a18.5 |
| purple specular arc | thin arc parallel to the left rim, about 0.27 long, 0.012 thick, at 170° to 220°, about 0.06 inside the outline | `#e6a0f6`, brightest `#ffbfff` | a17.5, a18.0, a18.5 |
| purple rising liquid | level rises chin to top in 8 frames (16.93 to 17.20 s); wavy surface band about 0.02 thick; 2 to 3 ring bubbles of 0.035 diameter, ring 0.008 | body `#a655cc` to `#ac53cf`, lower `#883fb4`; surface `#d49ff9`; bubbles `#db96ff` to `#e7a2ff` | a17.0, a f514 to f522 |
| steam puff | cloud of 4 to 5 lobes, 0.23 to 0.28 wide x 0.14 to 0.18 tall, ink outline about 0.014 | white `#fffeff`, underside `#e3e3f5`; outermost puff fades (`#fceae2` over orange) | a18.0 |
| steam layout | 3 puffs per side, stepping up and out from the hat brim: left (−0.36, −0.11), (−0.49, −0.24), (−0.57, −0.42); right (+0.56, −0.14), (+0.67, −0.29), a fading third about (+0.75, −0.50). First puff appears 2 frames after the head is fully purple (a f524) and the pumping continues to 19.5 s | — | a18.0, a f524 to f556 |
| sweat drop | fill 0.067 to 0.079 wide x 0.108 to 0.122 tall; outline 0.013 to 0.016; overall about 0.10 x 0.14 | fill `#b6e3ff` (b04.5), `#c9e7f8` (a29.5); lit left half `#def9ff`; outline slate `#5c647a` (b04.5), `#5c6a77` (a29.5), NOT the black ink | a29.5, a54.0, b04.5, b35.5 |
| sweat position | on the temple on the side the features slide toward (beside the far eye), straddling the outline, top hidden by the hat brim: (−0.39, −0.10) a29.5; (+0.31, −0.17) a54.0; (+0.33, −0.06) b04.5; (+0.445, −0.10) b35.5 | — | as listed, plus a33.5 and a47.0 (same side rule) |
| laugh tear | flattened drop about 0.075 to 0.10 x 0.03 to 0.045 (fill), chains of 2 (left) and 3 (right) leaving the outer eye corners; they fade to outline only, then vanish, over about 4 frames (b f734 to f738) | fill `#b8e4dc`, light `#e9ffff`, outline `#383f36` | b24.0 |
| blush | two soft ellipses 0.12 x 0.07 just below each happy eye | `#f8d7e1` on a white face | b06.0 |
| sleep Z | three at once, 0.33 apart vertically, zig-zagging ±0.1 sideways, each tilted about −10°. Lowest (0.7 to 0.9 above the head centre): outer size 0.115 x 0.13 incl. outline, dim. Middle (1.05 to 1.25 above): outer 0.14 to 0.15 x 0.155 to 0.165, fill 0.108 x 0.12, full colour. Top one is fading out and could not be measured. Outline 0.015. Rise about 0.5 D/s relative to the head (camera is moving, ±30 %), i.e. a new Z every 0.65 s | fill `#d4caf5` to `#dfcdee` at full strength, `#8a7791` then `#b4a7ce` while fading in; outline `#221a3f` (night grade) | b f996, f1002, f1008, f1011 (b33.0, b33.5), head D = 389 px |
| hair on end | 8 to 9 straight ink strokes, about 0.25 to 0.3 long, 0.035 thick, fanned over the top half of the head; held about 10 frames while the body jumps about 1 D upward and lands | ink | b f1084 to f1094 (head D only 111 px, so ±0.05) |
| focus lines | about 25 to 35 thin white wedges, 1 to 3 px wide, 60 to 250 px long, pointing at the character; different every frame | white, partly transparent | b f146 to f156 |
| stubble | about 60 to 80 specks of 1 to 2 px (0.008) on v > +0.12 | grey-brown | b19.0 |
| eye glint (night only) | one dot of about 0.01 in the upper part of each pupil | `#edeaff` | b42.0 |

### 2.7 Hats and hair (sampled colours)

| item | lit / highlight | base | shadow | frames |
|---|---|---|---|---|
| black bowler | grey band `#746b79` on about one fifth of the crown; hairline arc `#baaeb5` near the top edge | `#3f3b48` | `#282431` | a16.0 (band on the left); a46.0 (band `#706979` on the right) |
| bowler brim | thin lighter line `#aea4ae` | `#554953` | `#353244` | a16.0 |
| grey bowler | `#cfc4ba` left | `#9e9895` | `#726c6b` right | a33.5 |
| top hat | edge streak `#7f7c86` | `#37333d` | `#242028` | a27.5 |
| top-hat band | `#d1a957` | `#cfa83b` | `#8e6725` | a27.5 |
| striped cap | white stripes `#e9edf6` | blue stripes `#395a9e` | blue `#284170` toward the right | a55.0 |
| cap band | `#a5a6bd` | `#535873` | `#3c4768` | a55.0 |
| foreman cap | `#8bb0eb` on top | `#405c97` | `#34528e` | a23.0 |
| hair, hero | — | `#634025` | `#513720` | a46.0, a55.0 |
| hair, boss | — | `#988c98` | — | a15.0, a46.0 |

Hat lower edge crosses the head at v = −0.25 (a16.0), −0.21 (a55.0), −0.29 (b05.5).

### 2.8 Timing

| event | measured | frames |
|---|---|---|
| blink | open, half (1 frame), closed (1 frame), half (1 frame), open; eye height 0.22, 0.08, 0.029, 0.08, 0.22 D | a f1651 to f1655; a f1669 to f1673 |
| blink spacing, close-up | 0.60 s and 0.73 s | clip A 54.87, 55.47, 56.20 s |
| expression switch behind closed eyes | closed frames at 3.07, 3.40, 3.73, 4.13, 4.53 s | b f98, f108, f118, f130, f142 |
| lip sync | new mouth drawing every 1 to 3 frames; largest shape held up to 4 frames | a f1380 to f1435 |
| purple fill | 8 frames | a f514 to f522 |
| jump scare | squash blink 2 frames, leap up over 2 frames, hang 2 frames, land 2 frames | b f1080 to f1088 |
| outline boil | none: the inner-edge radius profile of the boss head correlates 0.99 to 1.00 between frames up to 16 apart (difference 0.07 to 0.16 % D against a wobble of 0.96 % D) | a f1386, f1387, f1390, f1396, f1402 |

### 2.9 Pixel sizes at 720x1280

| element (D units) | wide head D = 120 px | medium head D = 200 px | close-up D = 340 px |
|---|---|---|---|
| outline left 0.022 / right 0.050 / lower right 0.062 | 2.6 / 6 / 7.4 px | 4.4 / 10 / 12.4 px | 7.5 / 17 / 21 px |
| lid bar thickness 0.030 | 3.6 px | 6 px | 10 px |
| lid bar length 0.178 | 21 px | 36 px | 61 px |
| ring eye diameter 0.222, ring 0.025 | 27 px, 3 px | 44 px, 5 px | 75 px, 8.5 px |
| eye spacing 0.26 | 31 px | 52 px | 88 px |
| brow thickness 0.04 to 0.05 | 5 to 6 px | 8 to 10 px | 14 to 17 px |
| dash mouth 0.10 x 0.034 | 12 x 4 px | 20 x 7 px | 34 x 12 px |
| grin 0.42 x 0.12 | 50 x 14 px | 84 x 24 px | 143 x 41 px |
| sweat drop 0.10 x 0.14 | 12 x 17 px | 20 x 28 px | 34 x 48 px |

## 3. How to reproduce

The complete, runnable version of this section is `spec/face_proto/faces_ref.py` (path at the top). Its output was rasterised with Chromium and re-measured with the same scripts as the reference:

| quantity | reference | prototype |
|---|---|---|
| R_fill / D | 0.463 | 0.45 to 0.49 (three seeds) |
| outline 0° / 30° / 60° / 90° bins | 5.0 / 6.0 / 7.0 / 6.5 to 8.3 % D | 5.0 / 6.1 / 6.9 / 5.4 % D |
| outline 120° / 150° / 180° bins | 3.0 / 2.5 / 2.0 % D | 3.1 / 2.2 / 1.7 % D |
| inner-edge wobble | 1.0 to 1.5 % rms incl. junctions | 0.2 to 0.55 % rms, max 0.7 to 1.1 % (kept rounder on purpose; raise `wob_in` for more) |
| eye spacing, frontal | 0.26 | 0.264 |
| half-lid eye | 0.168 to 0.181 x 0.092 to 0.104 | 0.177 to 0.180 x 0.100 |
| ring eye, pupil | 0.21 to 0.225, 0.06 | 0.222, 0.060 |
| grin | 0.40 to 0.45 x 0.12 to 0.155 | 0.423 x 0.127 |
| clenched teeth | 0.164 to 0.185 x 0.126 to 0.137 | 0.177 x 0.135 |
| blink half frame | 0.22 x 0.08 | 0.223 x 0.080 |
| strong 3/4: eye midpoint shift, spacing | 0.08 to 0.14, 0.167 to 0.205 | 0.123, 0.188 |
| crescent colour over base | `#e9dceb` over `#fef7f6`, edge at r/R 0.78 to 0.85 | `#e9dceb` over `#fef7f6`, edge at r/R 0.75 to 0.85 |

### 3.1 Head (SVG, units of D, origin at the fill centre, y down)

Quick version (three circles):
```
<circle cx="0.014" cy="0.022" r="0.499" fill="#3a2a30"/>                         <!-- ink disc, shifted down-right -->
<g clip-path="circle r=0.463 at 0,0">
  <circle cx="0" cy="0" r="0.463" fill="#e9dceb"/>                               <!-- shadow colour everywhere -->
  <circle cx="-0.029" cy="-0.034" r="0.420" fill="#fef7f6" filter="blur 0.016"/> <!-- lit disc, shifted up-left -->
</g>
```
This gives an outline of 0.022 left, 0.050 right, 0.058 bottom, 0.062 lower right, 0.010 upper left.

Better version (what `faces_ref.py` does, `head_paths()`): draw the fill and the ink silhouette as 144-point polygons.
```
fill radius(θ)  = 0.463 + 0.006*cos(2θ + 0.9*seed) + 0.007*W(θ, seed)
ink radius(θ)   = fill radius(θ) + width(θ) + 0.005*W(θ, seed + 2.3)
W(θ, s)         = 0.6*sin(3θ + s) + 0.5*sin(5θ + 1.7s) + 0.3*sin(8θ + 0.6s)
width at θ = 0°, 30°, ... 330° (cosine-interpolated; 0° = 3 o'clock, 90° = bottom):
             0.044 0.054 0.070 0.068 0.040 0.025 0.019 0.018 0.019 0.021 0.026 0.034
```
The values from 210° to 330° (top of the head) are an assumption; the reference always hides that part under a hat.

- One `seed` per character, constant over the shot: the reference line does not boil from frame to frame (measured, see 2.8).
- Extra roughness on the feature edges: wrap head and features in a group with `feTurbulence type="fractalNoise" baseFrequency="3.2" numOctaves="1"` feeding `feDisplacementMap scale="0.012"` (units of D).
- Do not mirror the head disc when the character faces the other way; mirror only features, hair and hat.
- Layer order, bottom to top: ink silhouette, fill, crescent, hair patch, face features, blush/stubble, sweat drop and tears, hat, steam and Z.
- Scene grade: multiply the finished head by one colour per shot: day (1, 1, 1); warm interior (0.99, 0.91, 0.84) from b22.0; night with lamp (0.99, 0.81, 0.88) from b44.5; night without lamp (0.71, 0.71, 0.94) from b42.0.

### 3.2 Pose

```
shift   = 0.12 * yaw             # yaw in [-1, 1]:  0.25 slight, 0.5 medium, 1.0 strong (clip B default); + = features slide right
spacing = 0.26 - 0.075*|yaw|     # eye centre to eye centre
eye_y   = 0.03 + 0.07*pitch      # pitch -1.3 (proud, low angle) .. +1 (looking down)
eyes at (shift - spacing/2, eye_y) and (shift + spacing/2, eye_y)
brows at eye_y - 0.135 above their eye;  mouth at (shift, eye_y + 0.185)
far eye scale = 1 - 0.14*|yaw|   # the FAR eye is the one further from the head centre (the leading eye of the slide)
roll: rotate the whole head sprite, hat included, by -20 to +30 degrees
```
Example: features slide left (yaw −1): left eye at u = −0.21 drawn at 0.86 scale, right eye at u = −0.03 at full size (a16.5: 0.142 vs 0.166 wide; b05.5: 0.150 vs 0.175). When only one brow is drawn it always sits over the NEAR (larger, more central) eye (a46.0 boss, b05.5, b22.0, b25.0, b26.5).

### 3.3 Building blocks (cx, cy = eye centre; mx, my = mouth centre; ink `#3a2a30`)

| block | SVG recipe |
|---|---|
| half-lid eye | ellipse centre (cx+gaze, cy−0.013) rx 0.043 ry 0.062, clipped to y ≥ cy−0.035; plus line (cx−0.074, cy−0.035) to (cx+0.074, cy−0.035), stroke 0.030, round caps. gaze −0.03 to +0.03. For anger rotate the whole eye ±10° about its centre so the inner end of the bar drops |
| ring eye | circle r 0.0985, stroke 0.025, fill = head fill; pupil circle r 0.030 (excited) or 0.0165 (frightened), offset up to 0.03 |
| blink half | ellipse rx 0.111 ry 0.040 in ink, two tiny fill-coloured ellipses (rx 0.022, ry 0.013) at ±0.055 |
| closed eye | line cx−0.068 to cx+0.068, stroke 0.029, round caps |
| happy eye | path `M cx−0.068,cy+0.016 Q cx,cy−0.048 cx+0.068,cy+0.016`, stroke 0.029, round caps |
| dot eye | ellipse rx 0.041 ry 0.0575 |
| squeezed eye (left one; mirror for the right) | line (cx−0.080, cy−0.062) to (cx+0.070, cy−0.010) stroke 0.033; line (cx−0.085, cy+0.032) to (cx+0.070, cy+0.016) stroke 0.030 |
| brow dome (hero) | path `M bx−0.08,by+0.02 Q bx,by−0.06 bx+0.08,by+0.02 Z` filled |
| brow stroke | slightly bowed line, length 0.17, thickness 0.045 (heavy character), 0.038 (hero), 0.033 (light); angle: +15° determined, +24° angry (inner end down), −8° raised, −28° sad (outer end down) |
| mouth dash | line 0.07 long, stroke 0.034, round caps |
| arch frown | path `M mx−0.045,my+0.008 Q mx,my−0.014 mx+0.045,my+0.008`, stroke 0.034 |
| smirk | path `M mx−0.042,my−0.018 Q mx−0.018,my+0.026 mx+0.042,my+0.015`, stroke 0.032 (mirror to taste) |
| small smile | path `M mx−0.055,my−0.012 Q mx,my+0.040 mx+0.055,my−0.012`, stroke 0.034 |
| grin | filled ink crescent `M mx−0.21,my−0.055 Q mx,my−0.005 mx+0.21,my−0.055 Q mx,my+0.185 mx−0.21,my−0.055 Z`; teeth = four rects 0.057 wide centred at x = mx−0.111, −0.037, +0.037, +0.111, colour `#fef9f8`, clipped by the inner crescent `M mx−0.155,my−0.035 Q mx,my+0.008 mx+0.155,my−0.035 Q mx,my+0.110 mx−0.155,my−0.035 Z` |
| flat bar | ellipse rx 0.143 ry 0.029 filled ink |
| talking mouth | ellipse, fill `#4d2433`, ink stroke 0.018; four drawings: 0.25x0.045 (use the flat bar), 0.28x0.085, 0.285x0.17, round 0.18x0.13; two faint dashes `#7b626c` 0.05 long inside the open ones |
| "O" | egg path 0.19 x 0.17, narrower at the top, fill `#4d2433`, stroke 0.018, tongue dash `#7b626c` near the bottom |
| clenched teeth | rounded rect 0.18 x 0.13, rx 0.032, stroke 0.024, fill `#fef9f8`; one horizontal and three vertical ink lines 0.013 |
| wavy mouth | path `M mx−0.105,my+0.020 Q mx−0.070,my−0.045 mx−0.030,my−0.005 Q mx,my+0.022 mx+0.030,my−0.005 Q mx+0.070,my−0.045 mx+0.105,my+0.020`, stroke 0.040 |
| moustache | drooping filled arc 0.33 x 0.155 (see `moustache()` in the script) plus a 0.086 x 0.028 lip tick under its middle |

### 3.4 Expression list, ready to draw (20)

Eyes are placed by 3.2. "L/R" = viewer's left/right. Reference frames in brackets.

1. **Neutral** [a46.0 hero, a20.0]: half-lid eyes; two dome brows 0.13 above the eye line; dash mouth.
2. **Half-lidded unimpressed** [b05.5, a31.5]: half-lid eyes; ONE brow stroke over the near eye, 0.136 above, angle 0°, thickness 0.037; arch frown (or moustache for a pompous character).
3. **Smirk / cocky** [a02.0, a01.5, a47.5]: half-lid eyes with gaze +0.03; no brows; smirk mouth.
4. **Determined** [a13.5, b00.0]: half-lid eyes; both brow strokes at +15°, 0.12 above; arch frown.
5. **Angry** [a15.0, a16.0, a16.5]: half-lid eyes each rotated 10° so the inner ends drop; heavy brows length 0.19, thickness 0.052, +24°, only 0.10 above the eyes so they touch the lids and the hat brim; arch frown 0.02 higher than usual; pitch −0.9.
6. **Furious, purple with steam** [a17.5, a18.0]: as 5 with clenched teeth; head fill replaced by the purple gradient and arc (3.5); six steam puffs.
7. **Smug** [a46.0 boss, a44.5]: half-lid eyes; one raised brow over the near eye at −7°, thickness 0.048; flat bar mouth (or smirk).
8. **Talking** [a46.5, a47.0, b04.0]: any eye set held still; mouth cycles the four talking drawings.
9. **Shocked, wide-eyed** [a54.0, a33.5, a29.5, b05.0]: ring eyes with 0.033 pupils; optional short brows 0.2 above; "O" mouth (or dash for a frozen stare, a33.5); sweat drop.
10. **Stunned / realising** [a56.0, a14.0, b00.5]: ring eyes with 0.06 pupils; dash or tiny "o" mouth (0.08 x 0.04).
11. **Excited grin** [a55.0, a13.0]: ring eyes with 0.06 pupils; grin.
12. **Happy, content** [a27.5, a53.5, a58.5, a00.5]: happy arc eyes; both brows raised 0.20 above, angle −7°; small smile.
13. **Laughing with tears** [b06.0, b24.0, b06.5]: happy arc eyes; brows 0.21 above; grin 0.43 wide; blush under each eye; two tears flying from the L eye corner, three from the R; head rolled 15° to 20°.
14. **Worried, sweating** [a37.0, a29.0, b35.5]: half-lid eyes (or ring eyes, b35.5); brows at −9° (outer ends down), 0.13 above; wavy mouth; sweat drop on the temple beside the far eye.
15. **Asleep** [b33.0, b33.5, b34.0, a23.5]: closed-line eyes 0.02 lower than usual; flat brows; small dash mouth tilted 20°; three Z.
16. **Shouting, eyes squeezed** [a03.0, a f506 to f510]: squeezed eyes; clenched teeth (or wide-open talking mouth).
17. **Grinning** [a45.0, a35.0, a12.5]: dot eyes (a45.0) or closed arcs (a35.0) or half-lid (a12.5); thin brows 0.14 above at −10°; grin.
18. **Wink** [b26.5]: far eye is a happy arc, near eye stays half-lid; one brow raised 0.24 above the open eye; mouth as the character's default.
19. **Sad** [b44.5, b45.5]: half-lid or closed-line eyes; brows at −28°, 0.16 to 0.19 above; wavy mouth; pitch +1.
20. **Blink frames** [a f1652, a f1653]: half = almond eyes; closed = line eyes. Insert half, closed, half (one frame each) between any two expressions.

### 3.5 Effects recipes
- **Purple face**: `radialGradient cx=−0.07 cy=−0.09 r=0.56` (user units of D) stops `#b769e1` 0, `#a152cd` 0.55, `#7c35a8` 1; specular arc radius 0.40 from 188° to 228°, stroke 0.012, `#f0b2ee`. Fill animation: clip the purple to y > level, level going from +0.46 to −0.46 over 8 frames, with a 0.02 band of `#d49ff9` along a sine-wobbled top edge and three ring bubbles (r 0.017, stroke 0.008, `#db96ff`).
- **Steam**: puff = 5 overlapping circles (radii 0.045 to 0.065) in white `#fffeff` over the same circles 0.014 larger in ink. Six positions as in 2.6; spawn the inner puff, move each puff to the next position over about 6 frames, fade the outer one to 0 opacity; loop.
- **Sweat drop**: teardrop path 0.075 x 0.115, fill `#b6e3ff`, stroke `#5c647a` 0.014, lighter `#def9ff` blob on its left half; place at (0.33 × sign of yaw, −0.12), under the hat layer.
- **Tear**: ellipse 0.11 x 0.06, fill `#b8e4dc`, stroke `#383f36` 0.012, highlight `#e9ffff`; chain outward from the eye corner, each next one 0.8x.
- **Z**: bold italic Z polygon (10 points, see `zzz()`), fill `#dbd1fa`, outline 0.13 of the fill height in `#221a3f`. Spawn 0.7 D above the head centre with fill height 0.10 at 40 % opacity, rise 0.5 D/s with a ±0.1 D sideways zig-zag, grow to fill height 0.13 and full opacity by 1.2 D, fade out by 1.7 D; spawn the next one every 0.65 s.
- **Blush**: ellipse 0.124 x 0.07, `#f8d7e1`, Gaussian blur 0.018.

### 3.6 Animation rules
- Hold a face drawing; never tween eye shapes. Change expression only through the three blink frames.
- Blink every 0.6 to 1.0 s in close-ups and at every change of thought; skip blinks during a short line of dialogue.
- While a character speaks, change the mouth drawing every 2 frames on average (range 1 to 3), driven by the voice track loudness: silent = bar, low = half open, high = wide open, "oo/w" = round. Keep eyes and brows fixed.
- Roll the head 10° to 20° on each new phrase and let features slide with yaw; this is where the life comes from.

### 3.7 Putting it in Blender (headless, Cycles)
- (Not render-tested here: Blender renders were off limits for this task.) Make the head a flat card, not a sphere: a plane that always faces the camera (Copy Rotation from the camera, plus a local roll), textured with the rasterised SVG (head disc, crescent and features together in one image, 1024 px for a head that is at most 390 px on screen).
- Shade it unlit: Image Texture into Emission (strength 1.0), mixed with Transparent by the image alpha; view transform Standard (v1 already uses it) so `#fef7f6` arrives as `#fef7f6`. Multiply by the scene grade colour before the Emission.
- No Freestyle on the head: the outline is in the texture.
- Expressions: one PNG per expression per character; swap by keyed visibility as v1's `set_face` does, with constant interpolation.
- Hat, hair, sweat, steam and Z are further cards in the same plane stack, a few millimetres apart toward the camera, in the layer order of 3.1.

## 4. Differences vs v1, ranked by visual impact

Measured on `v1_frame20.png` (cap man: head R = 113 px, D = 226 px).

1. **Head is a lit 3D sphere; the reference is a flat disc.** v1 runs from blown-out `#ffffff` on the lit side to beige-grey `#bdb6a5` at the bottom and `#dfd8cb` on the left. Reference: flat `#fef7f6` everywhere plus one lavender crescent `#e9dceb` on the outer 15 % of the lower-right rim. This alone makes v1 read as "3D render" instead of "cartoon cut-out".
2. **Outline far too thin and uniform.** v1: 4.1 px = 1.8 % D, constant width, neutral black (Freestyle colour 0.02 linear, about `#272727`; face-texture ink `#111`). Reference at the same head size: 4.5 px on the left growing to 12 to 14 px on the lower right (2.2 to 6.2 % D), wobbly, plum `#3a2a30`.
3. **Wrong default eye.** v1 neutral and determined faces use small dot eyes (0.05 to 0.057 x 0.10 D as rendered) with thin brows. The reference default is the half-lid eye, 0.178 x 0.10 D, more than three times wider. v1's "smug" eyes are plain lines, which in the reference means "eyes shut".
4. **Features too small, too close and too thin.** v1 eye spacing 0.15 D as rendered (0.194 in the texture) vs 0.26; brow 0.11 x 0.04 (0.0225 thick in the texture) vs 0.16 to 0.18 x 0.04 to 0.05; mouth 0.119 x 0.022 vs 0.10 x 0.034 for the smallest reference mouth and 0.42 x 0.12 for a grin. v1's ring eyes (texture radius 120 + stroke at 234 px spacing) overlap each other; reference rings leave a 0.038 D gap.
5. **Features wrap around the sphere and foreshorten.** In v1 the far eye narrows and the whole face compresses as the head turns (features end up at u = −0.14 to −0.29). The reference keeps every feature flat and only slides it by up to 0.14 D, with spacing 0.26 down to 0.185 and the far eye at 0.86 scale.
6. **No facial animation.** v1 swaps a texture at a keyframe. The reference blinks in three frames, hides every expression change behind a blink, redraws the mouth every 1 to 3 frames in speech and rolls the head 10° to 30°.
7. **Hats are 3D-shaded primitives** (v1 cap dome `#7d97c7` to `#a3c7ff` smooth gradient, bowler `#333` to `#444`). Reference hats are inked 2D shapes with two or three flat tones and a hard glossy streak, covering the top 20 to 30 % of the head.
8. **No hair patch**, so the 3/4 view has no cue apart from the features.
9. **Effects.** v1's only effect is a sweat drop baked into the face texture: saturated `#6fb6ff` with a black outline, placed inside the face. Reference: pale `#b6e3ff` with a slate `#5c647a` outline, 0.10 x 0.14 D, on the temple overlapping the head outline and tucked under the hat. Steam, purple fill, tears, Z and blush are missing.
10. **No mouth interior colour and no teeth style.** v1's angry mouth is a white rect with three dividers; reference clenched teeth are a 4x2 grid in a rounded frame, and open mouths are maroon `#4d2433`.

## 5. Not determined, and caveats

- The outline thickness at the very top of the head and the true head shape under the hat cannot be measured; no bare head appears in either clip. The lower arc fits a circle to within 1 to 1.5 % D rms.
- The vertical origin depends on that circle fit, so absolute v values carry about ±0.02 D; distances between features (spacing, eye to mouth, brow to eye) are not affected.
- The crescent is centred near 50° in most heads but nearer 100° in a14.0 and a20.0; I could not tie that cleanly to head roll, so treat 50° as the default, not a law.
- Hair-on-end and focus-line dimensions come from a 111 px head and from streaks 1 to 3 px wide; they are good to about ±20 %.
- Whether blink spacing is random or scripted cannot be told from three blinks in one shot; the "blink at every expression change" rule is solid (seen 7 times), the 0.6 to 0.73 s spacing is one close-up only.
- Steam and Z motion were timed over 30 and 15 frames with a moving camera; speeds are approximate (±30 %). The topmost Z was too faded to measure; its size is extrapolated.
