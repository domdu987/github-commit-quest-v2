# Independent review of the extended cast (`cast_ext.py`)

Reviewer's scripts and outputs: `v3/tmp/cast_review/` (`sweep.py`, `propgrid.py`, `silo.py`, `compare.py`, `stage_check.py`, plus their images and json). Nothing outside `v3/cast/` and `v3/tmp/cast_review/` was written. `v2/puppet/puppet.py` stays untouched; hero and boss SVG output is still byte-identical with and without `cast_ext` (sha1 over 96 poses, both processes `f6e139d6...`).

## Verdict

The builder's work holds up: no crash, no NaN, no pop, props attach, stage integration works, colours arrive unchanged. The review found five problems. Four were repaired in `cast_ext.py` with the names and API kept. The fifth is a gap in the builder's tests, now covered by the reviewer's sweep.

| # | Finding | Evidence | Repair |
|---|---|---|---|
| 1 | Limb strokes under the spec. `beach_woman` and `beach_kid` had `limb_w` 0.050 and `clerk` 0.052. LOOK_SPEC 2.2 allows 0.055 to 0.075, and `verify_measurements.md` row 10 measured the reference hero at 0.051 to 0.058. The builder's `measure_ext.py` passed them only because its limb range had been widened to 0.045 to 0.089. | With the range tightened to 0.050 to 0.078, measured forearms were 0.0484 (woman) and 0.0455 to 0.0496 (kid): OUT. | `limb_w` is now 0.055 for the clerk and the woman and 0.057 for the kid (the kid's thin forearm measured 0.0496 at 0.055). `measure_ext.py` uses 0.050 to 0.078. Result: 203 measurements, 0 out. |
| 2 | The clerk had the hero's silhouette. At head 110 px, in black silhouette, both were slim, 345 and 346 px tall, with round heads (the eyeshade adds nothing to the outline). | `tmp/cast_review/silhouettes110.png` | Legs 1.18 to 1.30, so the clerk is now 3.16 D, lanky and clearly taller than the hero (2.9). His canvas went from y0 -4.4375 to -4.5625 to keep 0.38 D of head room (`canvas` check ok). |
| 3 | `senior_a` did not read as clearly older. His only cues were spectacles and grey-brown hair (`#968a86`) that mostly reads as brown under the fedora at 110 px. | lineup at 110 px | New optional CAST key `age_lines`, used by both seniors: under-eye bags drawn inside the lens when the member wears spectacles, none with ring eyes, and, without a moustache, a soft crease beside the mouth. `senior_a` hair is now silver `#bdb5b8`. A first version put the bags under the glasses rim, where they crossed the creases and read as stitches at a 190 px head. It was moved and checked again (`tmp/cast_review/zoom_senior.jpg`). |
| 4 | Holding a prop with `shade` or `chin` puts the prop in front of the face (mug, pail or paper over the eyes). A raised arm with the pail makes the pail hang beside the head. | `tmp/cast_review/propgrid.png` (5 members x 13 presets) | Documented in API.md as a usage note. No code change, because the behaviour is the defined one (the prop sits at the hand). |
| 5 | Test gap. The v2 suite's fuzz picks `CASTS[it % 2]`, so with the 6 new names it only fuzzes `senior_a` and `senior_b`. | `test_puppet.py` line 366 | `tmp/cast_review/sweep.py` covers all eight names (see check 3). |

## Check 1: likeness to the reference species

`review_compare.jpg` (full size: `tmp/cast_review/review_compare_full.jpg`) shows two reference rows. Each row starts with the reference figure crop: the bowler chief of a/t16.0 (head D 190 px) and the blue-suit figure of b/t35.0 (D 196 px). The six new members follow, each at the SAME head D and head height, composited over a character-free window of the SAME frame.

They read as the same species as the reference figures: the same head disc and thick-thin plum ink, the egg or pill torso with a gradient and 5 to 7 costume elements, rubber-hose limbs with ball hands and stub feet, and the half-lid default eye. No new member copies a reference character. The only bowler is `senior_b`'s, and it is pale dove-grey with white tufts, a walrus moustache and burgundy, against the reference chief's black bowler and mustard waistcoat.

Measurements (`measure_ext.py`, the v2 `measure.py` method at 400 px per D, ranges from LOOK_SPEC 2.2 / 2.3 with the limb range fixed as in finding 1): 203 measurements, 0 outside the range (`tmp/cast_review/measure_after.txt`).
- Head outer D 0.98 to 1.01. Eye spacing 0.260 (spec 0.252 to 0.269).
- Torso contour 0.020 to 0.028 on the left and 0.038 to 0.045 on the right.
- Torso width: regular 0.70 to 0.78, stout 1.06, slim 0.56 to 0.58, child 0.51.
- Limbs 0.050 to 0.073.
- Height: senior_a 3.21, senior_b 3.01, clerk 3.16, beach_man 3.10, beach_woman 2.92, kid 2.28 in its own D (1.82 adult D at `scale_hint` 0.8).

## Check 2: individuality (head 110 px, office wall `#b5484c` and sand `#d9b27a`)

`lineup.png` (re-rendered) and `tmp/cast_review/silhouettes110.png`, which shows a black silhouette row and a mean-colour row.
- Silhouettes differ in height and hat. The heights are 346 (hero), 407 (boss), 389, 364, 365 (clerk, after the fix), 370, 346 and 200 px (kid).
- Hats: plaid newsboy, homburg with a feather, pinched fedora, round bowler with tufts, eyeshade over hair, flat boater, wide sun hat, sailor cap. The dress silhouette and the child's size need no hat to tell them apart.
- Main hue by member: hero blue-violet argyle, boss green, senior_a brown (hue 25), senior_b burgundy (351), clerk white and blue pinstripe with a green visor, beach_man navy and cream hoops, beach_woman coral polka dots, kid white middy with navy.
- Closest remaining pair: `senior_a` and `beach_man`, both regular eggs at about 3.1 D. They are told apart by the hat (crowned fedora against the flat boater) and by the brown solid against navy and cream stripes.
- Seniors against the hero and the clerk: white tufts and walrus, or silver hair, spectacles and age lines, against the young faces. Clear at 110 px after the repair.

## Check 3: robustness

- Builder's v2 suite on the 6 names, rerun after the repairs: 1,994,570 checks, 0 failed, 179 s under load, slowest pose 1.19 ms (`tmp/cast_review/test_after.txt`; the run before the repairs gave the same count and 0 failed).
- Reviewer's sweep `tmp/cast_review/sweep.py`: 106,406 checks, 0 failed. It covers:
  - every arm preset x 6 props x 7 yaws (-1.3 to 1.3, including just around 0) x 3 squashes, with the mirror flag;
  - every expression at 3 yaws x 3 pitches with all six effects;
  - hand targets on circles of radius 0.05 to 1e6 D for each prop, at prop angles 0 to 851 deg;
  - garbage values on 12 pose keys;
  - 4,000 fuzz poses over all EIGHT names.
- Continuity: 600-step sweeps of yaw, pitch, head_roll, lean and t, with a raised arm holding the pail and the other hand shading the eyes. The largest step of the bbox or of any anchor is 0.0020 D per 1/600 step (no pops).
- Turn-strip pixel pop check (`strip_ext.run` redirected into `tmp/cast_review/strip/`): ratio 1.06 to 1.35 (limit 2.2), anchor step at most 0.080 D (limit 0.12). The ribbon cross-fade holds.
- `figure()` cost 1.1 to 1.2 ms per call under load 7 (the builder measured 0.6 to 0.8 when idle).

## Check 4: stage integration (`tmp/cast_review/stage_check.py`)

- Office, `INTERIOR_DAY`, `eye_two_shot`: `clerk` at `hero_mark` with the newspaper, `senior_b` at `near_mark`. Here `sprites` is imported before `cast_ext`, so this tests the patch path. Images: `office_preview_nocomp.png` and `office_final.png`.
- Beach, `SUMMER_SUN`, `eye_beach`: `beach_man` shading his eyes at `sand_a`, `beach_kid` with the pail at `sand_b`, placed with `scale=scale_hint` (0.8). Here `cast_ext` is imported first, so this tests the import hook. Images: `beach_preview_nocomp.png` and `beach_view.png`.
- Canvases were registered on both paths and no sprite was clipped.
- Colours, with the compositor off: every flat sprite point on a 0.05 D grid (87 to 113 per actor) compared with the frame pixel through `local_to_screen`. Median difference 0 levels, 90th percentile 1 to 2. The worst cases are 5 levels on the crescent gradient edge. Cards are not lit or tinted.
- With the office grade on, the difference is 2 levels median and 8 to 9 at the 90th percentile. That is the documented grade, not the cards.
- Feet: the stubs sit on the floor or sand with the contact decal and the hard cast shadow starting at the soles (`office_feet.png`, `beach_view.png`). The kid's pail shadow is attached.
- Final-quality timing, measured once: office `fast` (12 samples, 720x1280, 4 threads) took 9.0 s wall and 17.4 s CPU. Other jobs were running (load average 6.9 to 7.2 on 4 cores), so with the machine to itself this is about 4.4 s (CPU / 4), inside the 6 s budget.

hue_report rows:

| image | red | orange | blue | violet | magenta | dark |
|---|---|---|---|---|---|---|
| office_final.png (graded, two new members) | 43.9 | 25.6 | 21.2 | 0.8 | 5.9 | 0.17 |
| beach_preview_nocomp.png | 8.0 | 35.1 | 55.5 | 0.2 | 1.0 | 0.02 |
| lineup.png (flat backgrounds dominate) | 54.3 | 42.1 | 1.6 | 0.1 | 0.6 | 0.01 |

Cast pixels alone (8 members, opaque pixels of `silo.png`): red 35.2, orange 24.0, green 10.3, blue 14.9, violet 1.2, magenta 14.3. All of the magenta is the spec ink `#3a2832` (hue 327), which hero and boss share. No costume colour of the six falls in magenta (hue 290 to 345) at saturation above 0.15. The only colours in the violet band are the low-saturation trouser greys (`#575264`, `#5e5868`, hue 257 to 262). In a full frame, magenta stays at 5.9 percent and violet at 0.8.

## Check 5: props in hands

`tmp/cast_review/propgrid.png`: kid + pail, clerk + mug, senior_a + newspaper, senior_b + forecast and beach_man + pail, each through all 13 arm presets. The sweep checks numerically, in every pose, squash and mirror and for far targets, that:
- the working point is exactly `PROP_TIP` from the hand;
- the pail hangs straight down (tip x equals hand x, tip below the hand);
- the mug tip is the hand.

All of them passed. Visually, the bail apex sits inside the hand ball, the mug is behind the hand, and the papers are held by their near edge. Exceptions: `shade` and `chin` with a prop (finding 4).

## Still open (not repaired)

- The wrappers depend on puppet.py looking up its helpers as module globals, and `_CUR` is not thread-safe. Both are as reported by the builder.
- The forecast prop's text depends on the installed serif font.
- The new hats have no hat pitch parameter (LOOK_SPEC 2.6), the same as the v2 hats.
- `beach_kid` needs `scale=0.8` at placement. Nothing applies it automatically. The sheet, the lineup and this review's beach test do apply it.
- The kid's navy cap ribbons on the far side of the head can read as a dark lock of hair next to the blond fringe in small shots. This is a judgement call and was left as is.
