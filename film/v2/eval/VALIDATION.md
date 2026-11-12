# Validation of the likeness scoring tool

Scope: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/eval/score.py`, `heads.py`, `README.md` and the builder's scorecards. I did not build the tool. Everything below was re-measured in this pass; the builder's files as I found them are in `validation/orig/`, every script and intermediate result of this pass is in `validation/`.

## Verdict

The arithmetic of the tool was right: 15 picture statistics, the head outline widths, the caption box and the camera numbers reproduce by independent routes. Its judgement was wrong in six places, all repaired in `score.py` / `heads.py`:

| # | Fault found | Evidence | Repair |
|---|---|---|---|
| 1 | "Character changes while camera is steady" read 1.00 (score 1.0) on a still picture under a 2D zoom and pan: it measured leftover interpolation error, not animation | synthetic clip `validation/synth/kenburns` (one reference frame, zoom 8 percent/s, pan 30 px/s) | redefined: change in the character box after the fitted camera move, divided by local contrast, against the same for the background. Rigid picture now reads 0.00, frozen picture 0.01, reference 0.39 and 0.68 |
| 2 | Caption stroke could not tell the reference's 4 px from v1's 5 px (reference read 4.8 to 4.9, a hard 5 px outline 5.0, range 4.3 to 5.3) and jumped between 4.2 and 4.8 on parts of one clip | run-length histograms at two thresholds, `validation/stroke_probe.py` | stroke pixel = solid black (luma under 40, was 80, which took in the soft halo). Reference reads 4.03 and 4.05, hard 5 px reads 4.94; range back to the spec's 4 px (3.6 to 4.4) |
| 3 | Removing or destroying something made its group "not measured" and the index went up: captions covered 0.923 to 0.941, blurred 0.923 to 0.919 with captions and half the damage unscored | degraded variants, check 4 | caption coverage metric (no caption = captions 0, `--no-captions` for raw renders), ink edge softness metric, `index_strict` and `coverage` in every scorecard |
| 4 | Short clips were scored on noise: a 10 s piece of the reference got 0.00 on blinks (0 found in 7.5 s; the same piece re-encoded gave 1 and 2), 0.00 on pan, 0.62 on animation | check 6, pieces of the reference | minimum material per metric (value shown, "not measured" with the reason); for short inputs the ranges of the characters, camera, animation and captions groups are widened to the 10th to 90th percentile of reference pieces of that length. Colour and density keep the spec's frame targets: widening them too was tried and let v1 pass (v1 still 0.52 became 0.76) |
| 5 | A clean 11-frame dissolve between two smooth pictures was not found (11 to 18 chance feature matches of 140 exceeded the 10 percent limit) | known-truth edit `validation/synth/edit_truth` | up to 19 chance matches are now allowed whatever the feature count (real dissolves of the reference: 0 to 3 of 400; same shot: 30 to 97 percent). A plain 18 percent limit was tried first and gave one false dissolve inside the rotating shot of clip B (38 of 220), so it was not kept. The margin is thin: dissolves between two smooth, similar pictures can still be missed |
| 6 | Three ranges were wider than the spec without need or without saying so (thick ink side 0.060, contrast 0.58, caption y 899.0); the blink range was widened to the tool's under-count without saying so; head-fill saturation 0.085 had no source | check 3 | restored to the spec values; sources corrected |

Two things could not be repaired and are documented instead: the blink metric finds 3 of 7 known blinks and 5 of its 8 events are not blinks; the index can be gamed (a clip of two jittering discs on a colour card scores 0.859 after the guards, 0.865 before).

How to read a score now: for a whole film all six groups are measured and `index` = `index_strict`. For a 5 s clip the index scatters by itself: 5 s pieces of the reference score 0.81 to 0.96 with whole-film ranges (median 0.91).

## Check 1: re-run and run time

Original tool (copy in `validation/orig/`), 2 threads:

| Input | Builder's index | My re-run | Metric values | Wall time | Limit |
|---|---|---|---|---|---|
| Clip A (1955 frames) | 1.000 | 1.000 | identical, all 45 | 82 s | 240 s |
| Clip B (1945 frames) | 1.000 | 1.000 | identical | 89 s | 240 s |
| v1_frame20.png | 0.523 | 0.523 | identical | 0.4 s | 60 s |
| v1_frame45.png | 0.537 | 0.537 | identical | 0.4 s | 60 s |
| render/office (52 frames) | 0.622 | 0.622 | identical | 4.2 s | 60 s |
| proto_v2.mp4 (150 frames) | 0.967 | 0.967 | identical | 9.8 s | 60 s |
| v2/out/frames (150 PNG, no captions) | not run | 0.970, captions not measured | - | 10.7 s | 60 s |

Result: completes well inside the limits; the builder's numbers reproduce exactly. The repaired tool takes 92 s (clip A), 97 s (clip B), 11.2 s (prototype), under 1 s for a still.

## Check 2: truth of each metric (independent route against the tool)

Scripts: `validation/indep_picture.py` (PIL + numpy only: own HSV, percentiles, Canny, Gaussian, morphology), `indep_outline.py`, `indep_zoom.py` (SIFT matching and ECC), `indep_caption.py`, `stroke_probe.py`, `probe_char.py`, `make_edit_truth.py`, `heads_sheet.py`, `cmp_trans.py`. Frames: a/t16.0, a/t32.0, b/t24.5, b/t44.0, v1_frame20 unless stated.

| # | Group | Metric | Independent route | Tool against independent | Verdict | Fix |
|---|---|---|---|---|---|---|
| 1 | Colour | Saturation mean | own HSV in numpy | 0.2849 / 0.2849, 0.4089 / 0.4089, 0.5793 / 0.5793, 0.5318 / 0.5318, 0.2881 / 0.2881 | true | none |
| 2 | Colour | Luma p50, black point, contrast | own percentile code | identical to 4 decimals on all five frames (a/t16.0: 0.6453, 0.1055, 0.7781) | true | none |
| 3 | Colour | Colourfulness | own formula | 53.94 / 53.94, 64.72 / 64.72, 62.27 / 62.27, 67.79 / 67.79, 50.05 / 50.05 | true | none |
| 4 | Colour | Share S > 0.5, share V > 0.95 | own HSV | identical (a/t32.0: 0.3189, 0.1125) | true | none |
| 5 | Colour | Hue of the darkest tenth | own code | 274.46 / 274.46, 351.92 / 351.92, 356.86 / 356.86, 251.65 / 251.65, v1 25.97 / 25.97 | true, but a hue means nothing for a grey shadow | added "saturation of the darkest tenth" (spec 4.1 row 13) |
| 6 | Density | Canny edge density | own Sobel, non-maximum suppression and hysteresis | 0.0572 / 0.0574, 0.0766 / 0.0768, 0.0787 / 0.0788, 0.0955 / 0.0957, 0.0163 / 0.0163 | true | none |
| 7 | Density | Featureless 40 px blocks | own separable Gaussian and block loop | identical (0.5364, 0.0862, 0.1628, 0.2088, 0.6188) | true | none |
| 8 | Density | Mean luma of thirds; thin dark lines | own luma; own numpy black-hat | within 0.14 level; identical (0.0727, 0.0924, 0.0669, 0.1191, 0.0168) | true | none |
| 9 | Characters | Head detection | by eye on all 260 sampled frames of both clips (`validation/view/heads_A_orig_*.jpg`, `heads_B_orig_*.jpg`) | clip A: 71 marked, 70 are heads (f996: the circle spans a head and the newspaper under it, D 484), 4 circles 15 percent or more off in size (f891, f921, f1401, f1641); clearly visible pale heads missed in about 14 frames (f6, f696, f711 the officer, f951 to f981 the reader, f1626 the shocked boss, f1776). Clip B: 73 marked, all heads (one doubtful 66 px blob at f216); missed in about 15 frames (f156, f996 and f1011 sleeping close-up, f1161 behind bars, f1221 to f1296 the night guard, tinted) | precision about 98 percent, recall of clearly visible heads about 75 to 80 percent | minimum of 3 sampled frames with a head before the group is scored; recall documented as blind spot |
| 10 | Characters | Head diameter D | own fixed-threshold rays on a 4x upsample; auditors' table | a/t16.0 188 / 189 / 190 px; a/t13.5 166 / 167 / 168; b/t13.5 234 / 243 (own route has few rays there) | true | none |
| 11 | Characters | Outline thin and thick side | luma profile through the head centre of a/t16.0 (row 534, column 348), own script, auditors' table | left 4.5 px = 0.024 D (tool 0.024), right 8.8 px = 0.047 D (tool 0.046), bottom 15.3 px = 0.081 D (tool's 90th percentile 0.077, auditors 0.077). Same angles on b/t13.5: 0.065 / 0.065, 0.029 / 0.029, 0.021 / 0.021. v1: 0.019 to 0.021 all round | true | none |
| 12 | Camera | Cuts and dissolves | analysts' table `shots_def.py`; known-truth edit | original tool: clip A 13 of 15 found, clip B 17 of 21, no false one; every miss lies inside a detected snap move (train wipe, flash, punch-in, whip pan, two dissolves in fast moves), the hidden cut f276 is labelled a dissolve. Known edit: cut found on the exact frame; the 11-frame dissolve was missed | detector right on the reference, wrong on smooth pictures | up to 19 chance matches allowed; after the repair the known dissolve is found (f73 to f85 against f75 to f85); reference result below |
| 13 | Camera | Dissolve length | table; known-truth dissolve | against the table: median error +0.4 (A) and -0.6 (B) frames, single dissolves from -3 to +5; known 11-frame smoothstep read as 14.1 | good to about 3 frames per dissolve | needs 2 dissolves before it is scored |
| 14 | Camera | Zoom rate | known 2D zoom; SIFT matches on frame pairs 20 apart; ECC | known 7.71 percent/s read as 7.48. SIFT against tool over 20 frames: B f735-755 x1.154 / x1.168, B f1870-1890 x0.918 / x0.915, A f1717-1730 x1.0012 / x1.0015. In 3D push-ins the routes disagree: A f1170-1190 x1.029 (SIFT) against x1.144 (tool), ECC 16.4 against 20.5 percent/s | true for 2D moves; in a 3D scene the value depends on which depth layer the tracker follows | none (blind spot 8) |
| 15 | Camera | Pan | known 2D move | true centre speed 27.3 px/s, read as 27.4 | true | none |
| 16 | Camera | Static frames, holds, snap moves | analysts' lists, SIFT | holds of 6 frames or more in A: f1240-1252, f1408-1419, f1717-1730 (analysts' longest: f1718-1731; SIFT confirms scale x1.0012 there); static share 3.9 and 4.9 percent (analysts 3.8 and 5.5); snaps 33 and 22 (analysts 36 and 22) | true | none |
| 17 | Camera | Snap easing | known sine in-out snap (peak / mean = 1.571) | read as 1.53 | true | needs 3 snaps |
| 18 | Animation | Blinks | by eye on face strips of every event (`validation/view/blinks_tool_A.jpg`, `blinks_known_A.jpg`) | of the tool's 8 events in clip A, 3 are blinks (f1350, f1653, f1671); 5 are not (f814 and f827: smiling arc eyes, nothing changes; f1080: a sign passes during a dissolve; f1344, f1361). Of the 7 blinks the analysts list (f1350, f1383, f1399, f1420, f1654, f1672, f1694, all real) it finds 3 | not a blink rate: precision 3 of 8, recall 3 of 7 | renamed "blink-like eye events", scored only with 15 s of tracked heads, source text corrected; detector not repaired |
| 19 | Animation | Character changes while camera is steady | known-truth rigid clip (Ken Burns move on one frame), frozen clip | original: 1.00 on the rigid clip (PNG and MP4), 0.24 on a frozen picture with live captions. Repaired: 0.00 (PNG) and 0.00 (MP4) on the rigid clip, 0.01 on the frozen one; reference 0.39 (A) and 0.68 (B) | was broken | redefined (verdict table, row 1) |
| 20 | Animation | Face-drawing changes | rigid clip | 0.0 per s (PNG), 0.2 per s (MP4: 2 false events in 10 s) against 4.0 on the reference | true enough | needs 3 s of tracked heads |
| 21 | Captions | Centre x, centre y, height | own PIL implementation on a/t12.5, a/t16.5, a/t28.0, b/t24.5, b/t06.5; prototype's `.ass` file | identical on all five (a/t12.5: 359.0, 904.0, 45 px; a/t16.5: 360.0, 899.5, 36 px). Prototype placed at (360, 900): read as 359.75, 903.25 | true (the box centre sits 3 to 4 px low when a word has descenders) | none |
| 22 | Captions | Stroke width | luma profiles across stems on 8 stills; run-length histograms at luma 40 and 80 | 3 solid black pixels plus two partial ones, about 4 px. Original (luma under 80): 4.82, 4.90 on reference stills, 4.17 on the first 30 s of clip A, 5.00 on a hard 5 px outline, 3.92 on the prototype. Solid black (luma under 40): 4.03, 4.05, 4.01, 4.94, 3.86 | was unstable and blind to the 4 against 5 px difference | threshold 40, range 3.6 to 4.4 |
| 23 | Captions | Words, duration | report sheet; prototype's `.ass` timing | 11 of 11 word counts on the clip A sheet right; prototype events last 12, 12, 10, 17, 15, 18, 18, 16.5 frames, tool median 16.0 | true | duration needs 5 captions |

Transitions on the reference with the repaired tool (table numbers from `ref/extra/camera-motion/scripts/shots_def.py`):

```
table  111- 113 H occlusion wipe by passing train    MISSED
  table  276- 277 H hidden cut inside fast tilt-up     detected as dissolve f270-f281
  table 1930-1934 F explosion flash                    MISSED
clip A: matched 13 of 15, false 0; dissolve length error (tool - table): median +0.4, worst -3.0 / +4.8 frames
table  146- 147 C punch-out with speed lines         MISSED
  table  160- 166 H whip pan                           MISSED
  table  609- 617 D                                    MISSED
  table 1455-1467 D                                    MISSED
clip B: matched 17 of 21, false 0; dissolve length error (tool - table): median -0.6, worst -2.2 / +5.4 frames
```

## Check 3: reference ranges against LOOK_SPEC.md and verify_measurements.md

Ranges that are copied correctly (no change): saturation mean 0.40-0.60, black point 0.08-0.12, colourfulness 55-100, share S > 0.5 from 0.25, dark-tenth hue 250-345, share V > 0.95 0.02-0.09, edge density from 0.05, thin ink side 0.018-0.035 (verify row 4), head centre y 0.23-0.59 H (the correction of verify row 15 is applied), limb stroke 0.05-0.08 (verify row 10), heads above y 880 from 0.85, static share and hold (5.3), dissolve length 9-16 (5.4), snap easing 1.5-2.1, caption x 357-362, fill white, words 1-3, duration 6-18 frames.

| Metric | Builder's range | Spec | Finding | Now |
|---|---|---|---|---|
| Contrast (luma p95 - p5) | 0.58 to 0.75 | 0.60 to 0.75 (4.1 row 7) | lower bound moved without a note; the tool reads 0.601 and 0.616 | 0.60 to 0.75 |
| Head outline, thick side | 0.060 to 0.083, "widened to clip B" | 0.065 to 0.083 (verify row 4) | not needed: the tool reads 0.068 and 0.067 | 0.065 to 0.083 |
| Caption centre y | 899.0 to 905.5 | 899.5 to 905.5 (verify, other things) | 0.5 px wider without a note | 899.5 to 905.5 |
| Caption stroke | 4.3 to 5.3 px | 4 px, v1 5 px (captions.md) | range centred on a biased measure; v1's 5 px scored 1.0 | 3.6 to 4.4 with the repaired measure |
| Head fill saturation | at most 0.085 | at most 0.04 (4.1 row 16) | 0.085 has no source; clip B reads 0.049 | at most 0.055, score 0 at 0.205 (above the strongest tint of 2.4) |
| Interval between framing changes | 1.1 to 1.7 s | 1.2 to 1.5 s (5.3) | lower bound widened without need (tool: 1.39, 1.62); upper bound widened with a note, kept | 1.2 to 1.7 |
| Blinks per second | 0.2 to 1.4 | 0.5 to 1.4 (5.5 item 3), clips 1.4-1.8 and 0.4 | lower bound is the tool's under-count (0.31), not said | kept, source corrected, gated |
| Luma p50 | 0.22 to 0.47 | 0.22 to 0.45 | widened to the tool's clip A reading 0.459, said so | kept |
| Featureless blocks | at most 0.33 | at most 0.30 | widened to the tool's 0.314, said so (filter not stated in the spec) | kept |
| Head fill value | 0.96 to 0.995 | 0.97 to 0.995 | widened to clip B 0.969, said so | kept |
| Ink distance to #3a2832 | at most 8 dE | no number | holds for a whole film only: single scenes of clip B read 13 to 18 dE (brown-black under lamps, purple-black at night), as far as v1's neutral ink (11.2) | kept for films; piece range for short clips; new metric ink chroma (reference scenes 6 to 22, neutral ink 0) |
| Pan median | 40 to 150 px/s | A 133, B 57 | widened to the tool's 142, said so | kept |
| Mean shot length | 2.0 to 4.8 s | 2.62 and 3.75 s | the tool misses 2 and 4 transitions and reads 4.65 and 3.60; said so | kept |
| Dissolve share | 0.70 to 1.00 | 0.81 | the tool reads 0.92 and 0.94 for the same reason; said so | kept |
| Mean luma of thirds, thin dark lines | 85-135 / 105-150 / 60-105; 0.03-0.20 | 3.5: top eighth 40-90, brightest middle rows 105-150, bottom eighth 30-70 (interiors) | not the spec's quantities. By the spec's own definition the clips read 116 / 150 / 85 (A) and 91 / 132 / 70 (B), outside the interior targets, so the spec check cannot be used on a whole clip; the builder's thirds are calibrated on the two clips and say so | kept |
| Head diameter | 115 to 265 px | classes from 110 to 385 (verify row 15) | a clip of close-ups (300 to 385 px) scored 0.2; right for a film median only | kept; piece range for short clips |
| Not in the tool | - | 4.1 rows 2, 3, 4, 6, 10, 14, 15 (S p90, V mean, luma p5 and p95, share S < 0.15, mid-tone colour, largest cluster), ring luminance around heads, set-object count, surface detail | left out by the builder; row 13's saturation target was added (lower bound 0.30 instead of 0.35 because the tool reads 0.33 on clip B) | documented |

## Check 4: discrimination

10 s of clip A (frames 330 to 629: two dissolves, four snap moves, heads, captions), re-encoded with libx264 crf 14 (`validation/degr/`). "before" is the builder's tool, "after" the repaired one.

| Variant | Tool | Characters | Colour | Density | Camera | Animation | Captions | Index | Strict |
|---|---|---|---|---|---|---|---|---|---|
| ctrl | before | 1.000 | 0.989 | 0.946 | 0.852 | 0.624 | 1.000 | 0.923 | - |
| ctrl | after | 1.000 | 0.990 | 0.946 | 0.810 | 1.000 | 1.000 | 0.952 | 0.952 |
| desat60 | before | 1.000 | 0.741 | 0.945 | 0.889 | 0.662 | 1.000 | 0.897 | - |
| desat60 | after | 1.000 | 0.770 | 0.945 | 0.857 | 1.000 | 1.000 | 0.929 | 0.929 |
| bright_washed | before | not measured | 0.329 | 0.562 | 0.889 | not measured | 0.660 | 0.629 | - |
| bright_washed | after | not measured | 0.348 | 0.562 | 0.873 | not measured | 0.000 | 0.518 | 0.311 |
| nocap | before | 0.995 | 0.989 | 0.946 | 0.869 | 0.846 | not measured | 0.941 | - |
| nocap | after | 1.000 | 0.990 | 0.946 | 0.832 | 1.000 | 0.000 | 0.857 | 0.857 |
| blur | before | 0.972 | 0.985 | 0.744 | 0.889 | 0.981 | not measured | 0.919 | - |
| blur | after | 0.899 | 0.984 | 0.744 | 0.857 | 0.929 | 0.000 | 0.793 | 0.793 |
| frozen | before | 1.000 | 0.823 | 1.000 | 0.000 | 0.000 | 0.890 | 0.663 | - |
| frozen | after | 1.000 | 0.834 | 1.000 | 0.070 | 0.000 | 0.898 | 0.679 | 0.679 |
| frozen_livecap | before | 0.985 | 0.834 | 1.000 | 0.004 | 0.026 | 1.000 | 0.674 | - |
| frozen_livecap | after | 0.987 | 0.844 | 1.000 | 0.074 | 0.050 | 1.000 | 0.693 | 0.693 |

| Variant | Expected | Before | After |
|---|---|---|---|
| Desaturated to 60 percent | colour drops, rest stays | colour 0.99 to 0.74, others within 0.04: correct | same |
| Brightened and washed out (contrast 0.65, brightness +0.18) | colour and density drop | colour 0.33, density 0.56; heads no longer found, so characters and animation dropped out of the index | captions also 0 (stroke no longer black); characters still "not measured", so the strict index is given: 0.311 (index 0.518) |
| Captions covered | captions drop | captions "not measured", index went up from 0.923 to 0.941: wrong | captions 0.00 |
| Blurred (sigma 2.5) | density drops, characters drop | density 0.74; characters 0.97; captions not found and left out; index 0.919 against 0.923 | characters 0.90 (ink edge 6.5 px against 1.5 to 2.0), captions 0.00, index 0.793 |
| One still repeated | camera and animation drop | 0.00 and 0.00: correct | 0.07 and 0.00 |
| Still with live caption band | camera and animation drop, captions stay | 0.00, 0.03, 1.00: correct | 0.07, 0.05, 1.00 |
| One frame under a 2D zoom and pan (not asked for, added) | animation drops | animation 0.33 to 0.39 with "character changes" at 1.00: wrong | animation 0.00 (PNG), 0.08 (MP4) |

Metrics that did not move or moved the wrong way before the repair: caption group on covered captions, character-change share on a rigid picture, the whole characters group on a blurred or washed-out picture. All move the right way now except that a washed-out picture still loses its heads: the detector needs ink darker than 0.42 of the fill. That case shows as a low strict index and a line in the notes, not as a low characters score.

## Check 5: gaming

Inputs in `validation/synth/game/` (preview `validation/view/game_inputs.jpg`): `card.png` six flat colour bands whose areas hit the colour targets; `card_lines.png` the same with a 50 px grid of thin lines; `discs` 150 frames of that card under a slow zoom with two jittering white discs (plum ring, thin left and thick lower right, two dots, a stroke under them), "captions" made of white bars with a 4 px black stroke swapped every 11 frames, one dissolve; `discs_noise` the same with a brightness ramp and fine noise.

| Variant | Tool | Characters | Colour | Density | Camera | Animation | Captions | Index | Strict |
|---|---|---|---|---|---|---|---|---|---|
| card | before | not measured | 0.995 | 0.500 | not measured | not measured | not measured | 0.748 | - |
| card | after | not measured | 0.000 | 0.000 | not measured | not measured | 0.000 | 0.000 | 0.000 |
| card_lines | before | not measured | 0.871 | 0.985 | not measured | not measured | not measured | 0.928 | - |
| card_lines | after | not measured | 0.000 | 0.000 | not measured | not measured | 0.000 | 0.000 | 0.000 |
| discs | before | 0.882 | 0.925 | 1.000 | 0.727 | 0.667 | 0.981 | 0.864 | - |
| discs | after | 0.896 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.569 | 0.569 |
| discs_noise | before | 0.883 | 0.928 | 1.000 | 0.729 | 0.667 | 0.981 | 0.865 | - |
| discs_noise | after | 0.897 | 0.936 | 1.000 | 1.000 | 1.000 | 0.000 | 0.859 | 0.859 |

| Finding | Guard added | Still open |
|---|---|---|
| A flat colour card scored 0.75 (colour 0.995), with a grid 0.93 | colour entropy under 3.5 bits (reference frames 5.7 to 7.4, lowest single frame 3.7): colour and density scored 0, with a note | a ramp and a little noise defeat it (`discs_noise`) |
| White bars passed as captions (0.98) | captions made only of plain filled bars (3 or more): captions scored 0. Captions also need a fill share of 12 to 85 percent of their box | any irregular white marks with a black stroke at y 900 pass; text and typeface are not read |
| Discs with two dots are heads (characters 0.88, they lose only on the thick / thin ratio I drew wrong) | minimum of 3 sampled frames with a head, 2 heads with a measurable outline | a disc with the right ring is a head for this tool |
| Random jitter is "animation" (1.00), a constant zoom is "camera" (0.87) | none | nothing here judges what moves or why |
| Before the guards the disc clip scored 0.865; after them 0.859 | | the index is not perceptual; this is blind spot 1 of the README |

## Check 6: stability

| Test | Result |
|---|---|
| Same input twice (clip A, original tool and repaired tool) | identical: every metric value, score, transition and snap (checked on all 49 metrics) |
| MP4 against PNG frames of the prototype (original tool) | groups within 0.02; head fill value 0.992 against 1.000, ink distance 1.6 against 0.6 (chroma subsampling) |
| First 5 s against full clip A (repaired tool) | first 5 s: 1.00 / 0.97 / 1.00 / 0.88 / n/m / 1.00 (index 0.969); full: 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 (index 1.000) |
| First 5 s against full clip B | first 5 s: 1.00 / 0.86 / 0.84 / 0.98 / 1.00 / 1.00 (index 0.952); full: 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 (index 1.000) |

Pieces of the reference clips themselves, non-overlapping (`score.py CLIP --frames A:B`, runs in `validation/runs1w/`). "whole film" = scored with the ranges of the metric table; "piece" = re-scored with the piece ranges the tool now uses for inputs of that length:

| Piece length | Pieces | Ranges | Characters | Colour | Density | Camera | Animation | Captions | Index |
|---|---|---|---|---|---|---|---|---|---|
| 5 s | 25 | whole film | 0.67 to 1.00, median 0.97 (21 measured) | 0.67 to 1.00, median 0.89 (25 measured) | 0.50 to 1.00, median 0.93 (25 measured) | 0.60 to 1.00, median 0.85 (25 measured) | 1.00 to 1.00, median 1.00 (9 measured) | 0.88 to 1.00, median 1.00 (25 measured) | 0.81 to 0.96, median 0.91 (25 measured) |
| 5 s | 25 | piece | 0.78 to 1.00, median 1.00 (21 measured) | 0.67 to 1.00, median 0.89 (25 measured) | 0.50 to 1.00, median 0.93 (25 measured) | 0.80 to 1.00, median 0.98 (25 measured) | 1.00 to 1.00, median 1.00 (9 measured) | 0.90 to 1.00, median 1.00 (25 measured) | 0.84 to 0.99, median 0.95 (25 measured) |
| 10 s | 12 | whole film | 0.83 to 1.00, median 0.97 (11 measured) | 0.84 to 1.00, median 0.94 (12 measured) | 0.80 to 1.00, median 0.96 (12 measured) | 0.71 to 1.00, median 0.94 (12 measured) | 1.00 to 1.00, median 1.00 (10 measured) | 0.94 to 1.00, median 1.00 (12 measured) | 0.91 to 0.98, median 0.95 (12 measured) |
| 10 s | 12 | piece | 0.88 to 1.00, median 1.00 (11 measured) | 0.84 to 1.00, median 0.94 (12 measured) | 0.80 to 1.00, median 0.96 (12 measured) | 0.81 to 1.00, median 0.99 (12 measured) | 1.00 to 1.00, median 1.00 (10 measured) | 0.94 to 1.00, median 1.00 (12 measured) | 0.93 to 1.00, median 0.97 (12 measured) |
| 20 s | 6 | whole film | 0.81 to 1.00, median 1.00 (6 measured) | 0.87 to 1.00, median 0.96 (6 measured) | 0.90 to 1.00, median 0.99 (6 measured) | 0.73 to 1.00, median 1.00 (6 measured) | 1.00 to 1.00, median 1.00 (6 measured) | 0.96 to 1.00, median 1.00 (6 measured) | 0.93 to 1.00, median 0.97 (6 measured) |
| 20 s | 6 | piece | 0.90 to 1.00, median 1.00 (6 measured) | 0.87 to 1.00, median 0.96 (6 measured) | 0.90 to 1.00, median 0.99 (6 measured) | 0.79 to 1.00, median 1.00 (6 measured) | 1.00 to 1.00, median 1.00 (6 measured) | 0.96 to 1.00, median 1.00 (6 measured) | 0.95 to 1.00, median 0.97 (6 measured) |

| Metric | Whole-film range | 5 s pieces: mean score (values) | 10 s pieces | 20 s pieces |
|---|---|---|---|---|
| Saturation mean (HSV S) | 0.400 to 0.600 | 0.88 (0.291 to 0.606) | 0.90 or more | 0.90 or more |
| Luma p50 | 0.220 to 0.470 | 0.85 (0.207 to 0.682) | 0.90 or more | 0.90 or more |
| Black point (luma p1) | 0.080 to 0.120 | 0.86 (0.066 to 0.169) | 0.90 or more | 0.90 or more |
| Contrast (luma p95 - p5) | 0.600 to 0.750 | 0.89 (0.475 to 0.748) | 0.90 or more | 0.89 (0.520 to 0.735) |
| Hue of the darkest tenth (deg) | 250 to 345 | 0.89 (1 to 359) | 0.90 or more | 0.90 or more |
| Share of pixels with V > 0.95 | 0.020 to 0.090 | 0.79 (0.003 to 0.224) | 0.89 (0.017 to 0.200) | 0.85 (0.030 to 0.164) |
| Featureless 40 px blocks | 0.000 to 0.330 | 0.86 (0.085 to 0.718) | 0.88 (0.106 to 0.602) | 0.90 or more |
| Mean luma, top third (0-255) | 85 to 135 | 0.85 (81 to 197) | 0.90 or more | 0.90 or more |
| Mean luma, bottom third (0-255) | 60 to 105 | 0.82 (49 to 146) | 0.90 or more | 0.90 (63 to 136) |
| Head fill value (HSV V) | 0.960 to 0.995 | 0.84 (0.929 to 1.000) | 0.88 (0.937 to 0.996) | 0.90 or more |
| Head fill saturation (HSV S) | 0.000 to 0.055 | 0.84 (0.016 to 0.198) | 0.87 (0.008 to 0.197) | 0.84 (0.028 to 0.194) |
| Ink colour distance to #3a2832 (dE76) | 0.0 to 8.0 | 0.58 (1.3 to 18.0) | 0.69 (1.8 to 17.6) | 0.73 (1.5 to 16.6) |
| Zoom rate, median |percent/s| | 7.0 to 22.0 | 0.72 (3.0 to 62.9) | 0.77 (6.7 to 42.5) | 0.83 (7.5 to 31.5) |
| Pan, median px/s | 40 to 150 | 0.63 (12 to 504) | 0.73 (24 to 306) | 0.84 (43 to 189) |

The second table lists the metrics whose mean score over reference pieces is under 0.90 with whole-film ranges: these are the ones that punish a correct short clip. For the characters, camera, animation and captions groups the tool now widens the range to the 10th to 90th percentile of the pieces (`ref_windows.json`, built by `work/mkwin.py`); by construction 20 percent of the reference's own pieces still fall outside on any one metric. Colour and density are not widened: LOOK_SPEC 4.1 and 3.5 state those targets for single interior frames, and when I widened them to the reference's own scenes (which include sky and desert) the v1 still rose from 0.52 to 0.76 and the v1 frame folder from 0.62 to 0.73, that is, the tool lost its one known-bad case. The price is that a correct exterior or night scene can score low on colour and density; the scorecard says so in its notes.

Minimum material (below it the value is shown and marked "not measured"):

| Metric | Minimum | Why |
|---|---|---|
| Interval between framing changes | 8 s | in 5 s pieces the count is 2 to 5 events and the value jumps between 0.8 and 1.7 s; all 12 pieces of 10 s score 0.85 or more |
| Mean shot length | 15 s | 10 s pieces hold 2 to 3 shots; all 20 s pieces score 0.93 or more |
| Dissolve share | 4 transitions | with 1 or 2 transitions it is 0, 0.5 or 1 |
| Dissolve length | 2 dissolves | one dissolve is good to 3 to 5 frames |
| Snap easing | 3 snaps | single snaps range from 1.5 to 2.3 |
| Static share, hold, zoom, pan | 30 in-shot frames | - |
| Blink-like events | 15 s of tracked heads | the rate on the reference is 0.3 to 0.7 per s, so under 15 s fewer than 5 events are expected; a 10 s piece gave 0, 1 and 2 events in three encodes |
| Face changes | 3 s of tracked heads | 4 per s on the reference |
| Character motion | 30 steady-camera frames with a head | - |
| Caption duration, hard swap | 5 captions | - |
| Caption stroke | 200 stroke runs | - |
| Outline metrics, ink colour | 2 heads with a measurable outline (video) | - |
| Characters group | a head in 3 sampled frames (video) | - |

Groups that do not depend on length (characters, colour, density, captions) still depend on which scene the piece shows: with whole-film ranges 5 s pieces range from 0.67 to 1.00 (characters), 0.67 to 1.00 (colour), 0.50 to 1.00 (density).

## What was changed

`score.py`: metric table (ranges of check 3; new metrics saturation of the darkest tenth, ink chroma, ink edge softness, frames with a caption; character-motion metric redefined; stroke threshold); `--frames A:B`, `--no-captions`; minimum material; piece ranges for short inputs (`ref_windows.json`); `coverage` and `index_strict`; guards (flat colour card, plain-bar captions, lettering fill share, minimum head frames); dissolve chance-match limit. `heads.py`: ink edge softness per ray. `ref_clips.json` re-generated; `README.md` rewritten (`work/mkreadme2.py`); `work/mkwin.py` new. The metric count went from 45 to 49.

## The v2 prototype under the repaired tool

Metrics of `proto_v2.mp4` that are not at 1.00:

| Metric | Value | Range used | Score |
|---|---|---|---|
| Hue of the darkest tenth (deg) | 353 | 250 to 345 | 0.82 |

Not scored on 5 s: Interval between framing changes (s) (needs 8 s of video (clip is 5.0 s)); Mean shot length (s) (needs 15 s of video (clip is 5.0 s)); Blinks per second per head (needs 15 s of tracked heads (found 4.8 s)); Character moves on its own while camera is steady (needs 30 steady-camera frames with a tracked head (found 25)).

v1 frame folder, lowest metrics:

| Metric | Value | Range used | Score |
|---|---|---|---|
| Mean luma, top third (0-255) | 203 | 85 to 135 | 0.00 |
| Head flatness (luma spread) | 0.233 | 0.000 to 0.110 | 0.00 |
| Head outline, thick side / D | 0.021 | 0.063 to 0.083 (piece range) | 0.00 |
| Ink colour strength (Lab chroma) | 0.0 | 6.0 to 25.0 | 0.01 |
| Share of pixels with S > 0.5 | 0.052 | 0.250 to 0.900 | 0.01 |
| Featureless 40 px blocks | 0.626 | 0.000 to 0.330 | 0.01 |
| Luma p50 | 0.661 | 0.220 to 0.470 | 0.04 |
| Canny edge density (60/140) | 0.017 | 0.050 to 0.110 | 0.04 |
| Character moves on its own while camera is steady | 0.02 | 0.30 to 1.00 | 0.07 |
| Hue of the darkest tenth (deg) | 26 | 250 to 345 | 0.09 |
| Mean luma, bottom third (0-255) | 148 | 60 to 105 | 0.15 |
| Head outline, thick / thin ratio | 1.07 | 1.80 to 4.20 | 0.19 |
| Saturation mean (HSV S) | 0.288 | 0.400 to 0.600 | 0.25 |
| Black point (luma p1) | 0.153 | 0.080 to 0.120 | 0.45 |
| Thin dark line share | 0.017 | 0.030 to 0.200 | 0.57 |
| Head fill value (HSV V) | 1.000 | 0.947 to 0.996 (piece range) | 0.80 |

## Final score table

| Input | Characters (0.30) | Colour (0.15) | Density (0.15) | Camera (0.20) | Animation (0.10) | Captions (0.10) | Index | Strict index | Weight covered | Time |
|---|---|---|---|---|---|---|---|---|---|---|
| Reference clip A (1955 frames, 65.2 s) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 | 100 % | 91.4 s |
| Reference clip B (1945 frames, 64.8 s) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | **1.000** | 1.000 | 100 % | 96.8 s |
| v1 still, v1_frame20.png (`--no-captions`) | 0.648 | 0.514 | 0.292 | not measured | not measured | not measured | **0.526** | 0.526 | 60 % | 0.3 s |
| v1 still, v1_frame45.png (`--no-captions`) | 0.657 | 0.532 | 0.327 | not measured | not measured | not measured | **0.543** | 0.543 | 60 % | 0.2 s |
| v1 frame folder render/office (52 frames, 1.7 s, `--no-captions`) | 0.683 | 0.518 | 0.296 | 1.000 | 0.533 | not measured | **0.645** | 0.645 | 90 % | 4.4 s |
| v2 prototype, proto_v2.mp4 (150 frames, 5 s) | 1.000 | 0.980 | 1.000 | 1.000 | 1.000 | 1.000 | **0.997** | 0.997 | 100 % | 10.9 s |
| v2 prototype, frame folder v2/out/frames (no captions burned in, `--no-captions`) | 0.985 | 0.987 | 1.000 | 1.000 | 1.000 | not measured | **0.993** | 0.993 | 90 % | 11.6 s |
| Builder's synthetic control (v1 frame held 60 frames, v1-style captions) | 0.648 | 0.514 | 0.292 | 0.167 | 0.000 | 0.737 | **0.422** | 0.422 | 100 % | 5.0 s |

For comparison, the builder's tool gave: clip A 1.000, clip B 1.000, v1 stills 0.523 and 0.537, v1 frame folder 0.622, prototype 0.967, synthetic control 0.456.

How to read the table:

- Clips A and B score 1.000 by construction (ranges set on them). No third reference clip exists, so the tool's ranking of near-misses is untested.
- v1 keeps failing where the specs say it should (pale, unsaturated, empty set, shaded heads, uniform thin outline, neutral ink). Its camera score of 1.000 says only that 1.7 s of a slow push-in is inside what 5 s pieces of the reference do; pacing is not scored under 8 s.
- The prototype's 0.997 means that every number this tool checks is met on those 5 s; it was built from the same numbers. With the same piece ranges, 5 s pieces of the reference itself score 0.84 to 0.99 (median 0.95), so the prototype sits above every real piece: the tool has nothing left to say about it, which is not the same as "it looks like the reference". Four metrics could not be scored on 5 s (interval between framing changes 0.83 s against 1.2 to 1.7, mean shot length, blink-like events, character motion 0.52 on 25 frames).
- Compare inputs of similar length only, and on the strict index when their "not measured" groups differ.

## Remaining blind spots (full list in README.md)

1. Not perceptual: the disc clip of check 5 scores 0.859.
2. Reference scores 1.000 by construction; a dozen ranges rest on the tool's own readings of two clips.
3. Short clips scatter (table in check 6); colour and density of a correct exterior or night scene can score low.
4. Head detector: recall about 75 to 80 percent, misses tinted, profile and half-hidden heads and washed-out pictures; a disc with a ring and two dots is a head.
5. Blink-like events are not blinks (precision 3 of 8, recall 3 of 7 on clip A).
6. Transitions: wipes, whip pans, flashes, hidden cuts and dissolves inside fast moves are missed (2 of 15 and 4 of 21); dissolves between two smooth, similar pictures can be missed; one dissolve's length is good to 3 to 5 frames.
7. Zoom rate in a 3D scene depends on the depth layer the tracker follows; parallax is not measured.
8. Caption shadow, typeface and text are not checked.
9. Lens, depth of field, bloom, shadows, set-object count, surface detail, costume colours, mouth sync and motion blur are not checked.

The index covers measurable properties only. It is not a perceptual similarity score.
