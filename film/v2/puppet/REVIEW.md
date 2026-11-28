# Independent review and repair of the puppet system

Scope: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/puppet/` (`puppet.py`, `API.md`, `sheet.png`, `compare.jpg`).
Method: reference crops and our figures side by side at native resolution, same head size in px, same background colour (`review_compare.jpg`, single pairs in `tmp/rv/pair_*.png`); ONE image-analysis tool (`review_measure.py`) run on the reference frames and on our Chromium render (`python3 review.py measure`, tables in `tmp/rv/measure_before.txt` and `tmp/rv/measure_after.txt`); robustness sweeps (`test_puppet.py`); then repairs in `puppet.py`, re-render, re-look, re-measure. The public API of `API.md` is unchanged; additions only.

Unit: D = outer head diameter = 2.16 x R_fill (face spec definition). Angles around the head: 0 = 3 o'clock, 90 = bottom, 180 = 9 o'clock.

## 1. Verdict

The builder's puppet was a sound base: flat white head with the thick lower-right contour and the lavender crescent, measured faces, pill and egg torsos with the left-to-right gradient, ball hands, rubber-hose IK. Its own numbers reproduced (70 of 70 with `measure.py`, self-test PASS).
What the builder could not see:
- the cast was not our own: the hero's head and the boss's waistcoat were recolours of the reference hero and boss;
- its measuring tool had been calibrated against the face-spec table, not against the reference itself: with one tool on both, the head outline was 0.010 to 0.015 D too thin on the lower left;
- limbs were constant-width vector strokes of the same weight for both characters;
- the self-test skipped the one place where the rig jumped (a hand target passing its shoulder: the elbow jumped by up to 0.74 D) and never fed wrong types (76 input combinations raised exceptions).
All of these are repaired. The remaining differences (section 6) are minor or belong to the finishing grade, not to the puppet.

## 2. The ten largest differences found, ranked by visual impact

| # | difference (before the repair) | evidence | status |
|---|---|---|---|
| 1 | The hero's head was a copy of the reference hero: slate-blue cap with light lines and a grey-blue visor, brown hair crescents on the temples. Side by side with A t46.0 it read as the same person. | `tmp/rv/sheet_before_review.png`, pair A t46.0; reference cap `#44598b` + white stripes + visor `#989eb6` + hair `#9b6d49`, ours `#6c82b0` + `#b9c8e6` lines + visor `#8b9bc0` + hair `#6b452b` | fixed: ochre tweed cap `#dca63e` with cream check and brown seams, auburn hair `#a8492a`, red map pencil behind the ear. Chosen from five colourways rendered at head D = 110 px on `#a8663f`, on `#1f2a55` and under the warm tint (`tmp/rv/cap_experiment.png`) |
| 2 | The boss's waistcoat repeated the reference boss's layout in another colour: five buttons on the centre line, watch chain from the second button to a fob, three welt pockets in the same places, dot pattern, pointed hem. | pair A t44.0 before the repair | fixed: double-breasted waistcoat, chalk pinstripes, dark shawl lapels, six buttons in two columns, white pocket square, straight hem, small orange feather in the hat band. No chain, no welt-pocket trio, no dots |
| 3 | Limbs were constant-width vector strokes. The reference limbs are hand inked: width varies along the limb and the edges waver (boss legs 13 to 17 px at D = 191 px in A t16.0, 18 to 22 px at D = 310 px in A t44.0). | ours before: 0.0612 D at every sampled point of every limb (`measure_before.txt`) | fixed: each limb = core stroke + filled ribbon whose width breathes about +/-10 percent and whose centre line wavers 0.06 of the width; a fixed function of the position along the limb, so it never boils. After: hero 0.051 to 0.063 D, boss 0.069 to 0.084 D at the sampled points |
| 4 | One limb weight (0.060 D) for both characters. The reference draws the boss heavier (0.058 to 0.089 D) than the hero (0.040 to 0.065 D); our boss looked spindly at D = 190 px (11.4 px legs against 13 to 17 px). | pair A t16.0 before; anatomy spec 2.3 | fixed: per-cast default, hero 0.054, boss 0.068; pose key `limb_w` still overrides (use about 0.8 of the default in close-ups, the reference hero is 0.040 to 0.046 at D = 350 px) |
| 5 | Head outline too thin on the lower left and left. Same tool on both: at 120 degrees ours 0.037 (hero) and 0.041 (boss) against 0.051 to 0.058 in clip A; at 150 degrees 0.027 and 0.029 against 0.032 to 0.045; at 0 degrees 0.046 against 0.051. The thick-thin contrast was stronger than in the reference close-ups (A t55.0, A t46.0). | `measure_before.txt`, reference table in the same file | fixed: outline table re-calibrated. After: 120 degrees 0.045 to 0.049, 150 degrees 0.035 to 0.039, 180 degrees 0.028 to 0.029, 0 degrees 0.050 to 0.052 |
| 6 | Arms and legs (plum ink) nearly vanish on the dark office colours `#55291a` and `#1f2a55`; in a staged two-shot both pairs of legs disappeared against the wainscot and the floor. | the builder's two-shot `tmp/example_scene.png` as delivered; `sheet.png` row 7 (no rim) against row 8 (rim) | fixed as an option: pose key `rim="#rrggbb"` draws a thin light halo behind arms, hands, legs and feet only (one group behind the whole figure). Default off, so the reference look is unchanged where the background is mid-value. `example_scene.py` now uses it |
| 7 | In extreme close-ups (head D = 690 px, as in B t21.0) the head outline read as a 12-sided shape with rounded corners: the width table was eased with a cosine, which puts a plateau at every 30 degree node. | our boss rendered at D = 688 px beside B t21.0 before the fix: a soft corner every 30 degrees; the reference arc is smooth (after: `tmp/rv/crop_b21_ours.png`) | fixed: periodic spline through the table, head and torso contours as smooth closed curves instead of straight-segment polygons |
| 8 | The two heads were not the same size by the spec's own definition of D: the hero's lower-arc circle fit gave 1.027 x nominal, the boss's 0.999, because the baked wobble differs per character. Every hero ratio measured 2.7 percent small (eye spacing 0.253 instead of 0.260). | `measure_before.txt`, first row | fixed: the wobbly fill disc is re-centred and re-scaled per character so that the lower-arc fit is exactly R = 0.463 D. After: 1.003 and 0.998 |
| 9 | Costume lines and details finer than the reference: inner lines 0.008 to 0.014 D against about 0.016 D (5 px at D = 310 px), buttons 0.071 D across against about 0.085 D, torso contour 0.018 D on the left against 0.02 to 0.03 D. | pair A t44.0 before | fixed: inner lines 0.010 to 0.016 D, buttons 0.083 D with a 0.015 ring, torso contour 0.025 D nominal on the left (reads 0.019 to 0.026 without the anti-aliased pixels) and 0.042 to 0.045 D on the right |
| 10 | Hand ball 0.13 D for both characters. Reference: boss 0.13 to 0.14 D, hero about 0.11 to 0.12 D in the medium shot and smaller in the close shot; the hero's hands looked heavy beside A t55.0. Akimbo arms existed only as a sharp V, while A t44.0 shows smooth jug-handle arcs. | pairs A t55.0, A t44.0 before | fixed: hand ball follows the limb weight (hero 0.118, boss 0.141 D); `akimbo` is its own smooth preset, `hip` keeps the soft V |

Smaller points repaired on the way: fill-edge wobble raised from 0.45 to 0.52-0.54 percent D rms (reference with the same tool 0.87 to 0.95 including the neck and hair junctions, pure line 0.5 to 0.8 per the face spec); the foot stub no longer flips the leg outline when the figure turns through the front view.

## 3. Measurements of our render, before and after (Chromium, head D = 350 px, `review.py measure`)

Reference columns: the same functions on A t16.0, A t55.0, A t46.0 (clip A) where a frame allows it, otherwise the spec.

| quantity | reference | hero before | hero after | boss before | boss after |
|---|---|---|---|---|---|
| head D = 2.16 R_fill, x nominal | 1.000 | 1.027 | 1.003 | 0.999 | 0.998 |
| outline, 0 deg (right) | 0.051 (B: 0.053-0.063) | hidden by hair | hidden by hair | 0.046 | 0.050 |
| outline, 30 deg | 0.049-0.062 | 0.053 | 0.056 | 0.063 | 0.066 |
| outline, 60 deg | 0.062-0.081 | 0.067 | 0.068 | 0.068 | 0.069 |
| outline, 90 deg (chin + collar) | 0.080-0.088 (B: 0.071-0.073) | 0.076 | 0.081 | 0.064 | 0.069 |
| outline, 120 deg | 0.051-0.058 | 0.037 | 0.045 | 0.041 | 0.048 |
| outline, 150 deg | 0.032-0.045 | 0.027 | 0.035 | 0.029 | 0.037 |
| outline, 180 deg (left) | 0.024-0.030 | hidden by hair | hidden by hair | 0.023 | 0.028 |
| fill-edge wobble, percent D rms | 0.87-0.95 with junctions | 0.45 | 0.52 | 0.45 | 0.54 |
| ink colour | `#3b2833`, `#3e2735` | `#3a2832` | `#3a2832` | `#3a2832` | `#3a2832` |
| head fill / rim crescent | `#fdf7f7` / `#eadeec` | `#fef7f6` / `#e9dceb` | same | same | same |
| eye spacing | 0.252-0.269 | 0.253 | 0.259 | 0.260 | 0.260 |
| half-lid eye, w x h | 0.168-0.181 x 0.092-0.104 | 0.173 x 0.095 | 0.177 x 0.097 | 0.177 x 0.097 | 0.177 x 0.097 |
| ring eye (excited) / grin | 0.21-0.225 / 0.40-0.45 x 0.12-0.155 | | 0.222 x 0.202 / 0.424 x 0.125 | | 0.223 / 0.426 wide |
| torso max width | hero 0.54-0.58, boss 0.99 | 0.562 | 0.575 | 1.004 | 1.005 |
| torso visible height | 0.86 / 0.87-0.93 | 0.836 | 0.848 | 0.923 | 0.916 |
| torso contour, left / right (anti-aliased pixels not counted) | 0.02-0.03 / 0.03-0.047 | 0.018 / 0.042 | 0.019 / 0.043 | 0.023 / 0.044 | 0.026 / 0.044 |
| limb stroke (sampled) | hero 0.040-0.065, boss 0.058-0.089 | 0.061 | 0.051-0.063 | 0.063 | 0.069-0.084 |
| hand ball diameter | hero about 0.11-0.12, boss 0.13-0.14 | 0.126 | 0.118 | 0.128 | 0.141 |
| total height, head top to soles | 2.9-3.4 | 2.94 | 2.98 | 3.40 | 3.40 |
| hat lower edge on the centre column (v) | cap -0.09..-0.12, bowler -0.20..-0.26 | -0.111 | -0.130 | -0.245 | -0.247 |
| hat top above the head centre | cap 0.47-0.55, bowler 0.68 | 0.542 | 0.570 | 0.713 | 0.716 |

After the repair `review.py measure` reports 0 rows outside the reference ranges, and the builder's `measure.py` 70 of 70 (its limb and hand ranges were made per cast).

Note on the two specs: the anatomy spec quotes the hero's head in A t02.0 as "about 190 px"; by the face-spec definition it is 202 px (R_fill 93.4 px). The hero ratios taken from that frame are therefore about 5 percent high (torso 110 px = 0.545 D, not 0.58). Our hero torso (0.575 D) is inside the +/-0.03 D tolerance of both readings and was left alone.

## 4. Robustness (`python3 test_puppet.py [--quick] [--strip]`)

For both cast members: every preset, expression, mouth, prop and effect; every numeric pose key swept through its whole range in 40 steps and again in 240 steps with a six times tighter bound; arm hand targets on circles of radius 0.02 to 50 D around the shoulder and on straight lines through it, with automatic and fixed bend; the same for foot targets; garbage input; 1500 random poses; determinism, id prefixes, mirror symmetry, `resolve_pose` / `lerp_pose`; speed.

| | before the repair | after |
|---|---|---|
| checks failed | 143 | 0 of 1 977 307 |
| wrong-type input (`expr=[]`, `prop_r=3.0`, `fx=True`, `{"preset": []}`, effect phase 1e308) | 76 combinations raised TypeError, AttributeError or ValueError | never raises; falls back to the default |
| hand target crossing its shoulder | hand jumped 0.18 D, elbow up to 0.74 D (the documented "singular spot") | continuous: the hand follows the target to the shoulder and the hose retracts; largest anchor step 0.030 D per 0.010 D of target travel (the elbow) |
| bend direction with a fixed `bend` | constant except across the shoulder | constant everywhere |
| numeric sweeps | no jump | no jump (tightest: 68 percent of the 240-step bound) |
| speed, slowest pose | 0.64 ms | about 1.0 ms (limit 10 ms) |
| builder's self-test `python3 puppet.py test` | PASS | PASS (6481 checks, largest step 0.026 D) |

30-frame strip (`tmp/rv/turn_strip.png`, hero yaw -1 to +1 while raising an arm): looked at frame by frame, nothing pops: the hair patch shrinks on one temple and grows on the other, the visor slides, the feet turn through a short stub, the arm rises along one arc. Pixel check: largest frame-to-frame change is 1.14 times the median change.

Still singular by nature: the DIRECTION of the forearm when a hand target sits exactly on the shoulder. Positions are continuous there; a prop held without an explicit `angle` turns over. Give the prop an angle if a hand must pass through its shoulder.

## 5. Cast design

- Distinguishable at head D = 110 px: yes. Silhouette: short slim pill with a flat cap against a tall stout egg with a brimmed hat and a feather (black silhouettes in the last row of `sheet.png`). Colour: ochre + cobalt + auburn against grey + green + red.
- On warm brown `#a8663f`: both read (the ochre cap is lighter and yellower than the wall and carries a 0.03 D ink outline; checked under the warm tint `#faded0` too). On navy `#1f2a55`: heads, hats and torsos read; limbs need the `rim` option (difference 6).
- Our own characters: after the repair, yes. What is shared with the reference is the style vocabulary only (round white head, hat drawn over the top of the head, hair patches without an inner line, pill and egg torsos, ball hands). The specific designs are ours: newsboy cap, sweater vest with argyle and tie, pencil behind the ear; homburg with band, bow and feather, moustache, double-breasted pinstripe waistcoat, bow tie, pocket square.

## 6. What remains

Minor:
- The cap is larger than the reference cap (0.88 D wide, top 0.57 D above the head centre, against 0.85 D and 0.47 to 0.55 D). Deliberate: it is a floppier hat than the engineer cap.
- At yaw +/-1 the costume slides and compresses linearly; the facing-side button column of the boss is partly cut by the torso contour.
- Hand shapes are ball, pointing index and open hand only (no thumb or cup grip); sitting and kneeling need explicit foot targets, there is no preset.
- The halo for dark backgrounds is opt-in (`rim`), the scene has to ask for it.

Cannot or should not be fixed inside the SVG puppet:
- Edge softness. The reference is video: every edge is 1 to 2 px soft and carries compression texture; ours is a crisp vector raster. This belongs to the finishing grade (a blur of about 1 px before the grain), not to the puppet.
- Frame-to-frame drift. The reference shapes drift slightly from frame to frame (anatomy spec 1.1); ours are perfectly stable. A line boil would be possible by re-seeding the wobble every few frames, but it was not added: it risks reading as flicker and no measurement of its amplitude exists.
- Painted costume highlights (the pale stripe inside the left edge of the clip B robe) are approximated by the left-to-right gradient only.

## 7. What changed in the code (all backward compatible)

- `puppet.py`: cast colours and boss costume; per-cast `limb_w` (CAST key) and hand size; hand-inked limb ribbons (`_ink_limb`); outline table, periodic spline, smooth closed head and torso contours, normalised fill disc; IK without dead zone or flip; input hardening; new pose keys `rim`, `rim_w`, `rim_opacity`; `akimbo` as its own arm preset; one more sheet row. The pre-review version is kept in `tmp/rv/puppet_before_review.py`.
- `API.md`: updated, additions marked "(review)". `measure.py`: limb and hand ranges per cast. `example_scene.py`: uses `rim`.
- New: `REVIEW.md`, `review.py`, `review_measure.py`, `test_puppet.py`, `raster_multi.js`, `review_compare.jpg`.
