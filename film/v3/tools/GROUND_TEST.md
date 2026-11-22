# GROUND_TEST.md -- ground_check.py on two scene setups

Run with the pip `bpy` 5.3 module (same python API as `blender -b`). The real `blender` binary is not installed in this container,
so the `blender -b ... --python` command line itself was NOT run here; `run_cli()` is the same code path (it reads the argv after `--`),
and `sys.exit(1)` gave exit code 1 on the failing runs below.
Each setup is a script that builds the scene and calls `ground_check.run_cli([...])`; reproduce with
`python3 film/v3/tools/ground_test_stub.py [--fix]` and `python3 film/v3/tools/ground_test_harbor.py [--fix]`.
Both use `--every 10 --gap 0.02`, frames 1..60. Cards use placeholder sprites (a solid block): the real sprites need Chromium.

## Setup 1: stage/stubroom.py + real actors.Actor cards + props (defects planted on purpose)
Planted: `boss` floats 0.6 (card), `walker` keyed 0.35 too high on frames 21..40, `ox` sprite has 12% empty rows at the bottom
(alpha bottom measured: gap 0.291, not the 0.475 of the card edge), `pole_flag` hovers 1.0, `canopy_top` has no legs (1.6),
`thrown_pot` has airborne_frames "30:60" (frames 1/11/21 fail, 31..60 skipped), `bird` airborne=True (skipped); `crate`,
`crate_on_box` (sits on stub_box: hit = stub_box) and `hero` (feet on the floor) must pass, and do.

### 1a. check only
# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 7 (1, 11, 21, 31, 41, 51, 60)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 10   rows: 66   FAIL rows: 34   **result: FAIL (6 objects)**
- command: `blender -b ... --python ground_check.py -- --every 10 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/tools/GROUND_stub.md`

## Failing objects

| object | kind | failing frames | worst gap |
|---|---|---|---|
| boss_card | card | 1, 11, 21, 31, 41, 51, 60 | 0.4750 |
| canopy_top | prop | 1, 11, 21, 31, 41, 51, 60 | 1.6000 |
| ox_card | card | 1, 11, 21, 31, 41, 51, 60 | 0.2910 |
| pole_flag | prop | 1, 11, 21, 31, 41, 51, 60 | 1.0000 |
| thrown_pot | prop | 1, 11, 21 | 2.0000 |
| walker_card | card | 31, 41, 51 | 0.2250 |

## Skipped as airborne

- `thrown_pot` on frames 31, 41, 51, 60

<details><summary>all rows</summary>

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| boss_card | 1 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| boss_card | 11 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| boss_card | 21 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| boss_card | 31 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| boss_card | 41 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| boss_card | 51 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| boss_card | 60 | +0.4750 | FAIL | card/alpha | 0.475 | stub_floor |
| canopy_top | 1 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| canopy_top | 11 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| canopy_top | 21 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| canopy_top | 31 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| canopy_top | 41 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| canopy_top | 51 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| canopy_top | 60 | +1.6000 | FAIL | prop/bbox | 1.600 | stub_floor |
| ox_card | 1 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| ox_card | 11 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| ox_card | 21 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| ox_card | 31 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| ox_card | 41 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| ox_card | 51 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| ox_card | 60 | +0.2910 | FAIL | card/alpha | 0.291 | stub_floor |
| pole_flag | 1 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| pole_flag | 11 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| pole_flag | 21 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| pole_flag | 31 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| pole_flag | 41 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| pole_flag | 51 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| pole_flag | 60 | +1.0000 | FAIL | prop/bbox | 1.000 | stub_floor |
| thrown_pot | 1 | +2.0000 | FAIL | prop/bbox | 2.000 | stub_floor |
| thrown_pot | 11 | +2.0000 | FAIL | prop/bbox | 2.000 | stub_floor |
| thrown_pot | 21 | +2.0000 | FAIL | prop/bbox | 2.000 | stub_floor |
| walker_card | 31 | +0.2250 | FAIL | card/alpha | 0.225 | stub_floor |
| walker_card | 41 | +0.2075 | FAIL | card/alpha | 0.207 | stub_floor |
| walker_card | 51 | +0.0325 | FAIL | card/alpha | 0.032 | stub_floor |
| crate | 1 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate | 11 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate | 21 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate | 31 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate | 41 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate | 51 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate | 60 | +0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| crate_on_box | 1 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| crate_on_box | 11 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| crate_on_box | 21 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| crate_on_box | 31 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| crate_on_box | 41 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| crate_on_box | 51 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| crate_on_box | 60 | +0.0000 | OK | prop/bbox | 1.300 | stub_box |
| hero_card | 1 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| hero_card | 11 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| hero_card | 21 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| hero_card | 31 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| hero_card | 41 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| hero_card | 51 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| hero_card | 60 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| stub_box | 1 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| stub_box | 11 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| stub_box | 21 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| stub_box | 31 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| stub_box | 41 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| stub_box | 51 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| stub_box | 60 | -0.0000 | OK | prop/bbox | 0.000 | stub_floor |
| walker_card | 1 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| walker_card | 11 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
| walker_card | 21 | -0.0900 | OK | card/alpha | -0.090 | stub_floor |
| walker_card | 60 | -0.1250 | OK | card/alpha | -0.125 | stub_floor |
exit code: 1

</details>

### 1b. with --fix
# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 7 (1, 11, 21, 31, 41, 51, 60)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 10   rows: 66   FAIL rows: 0   **result: PASS**
- command: `blender -b ... --python ground_check.py -- --every 10 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/tools/GROUND_stub.md --fix`

## --fix: changes made

- `boss_root` (delta_location keys) for `boss_card`: Z offset (world units) on 7 sampled frames: f1 -0.475, f11 -0.475, f21 -0.475, f31 -0.475, f41 -0.475, f51 -0.475, f60 -0.475
- `ox_root` (delta_location keys) for `ox_card`: Z offset (world units) on 7 sampled frames: f1 -0.291, f11 -0.291, f21 -0.291, f31 -0.291, f41 -0.291, f51 -0.291, f60 -0.291
- `pole_flag` (moved) for `pole_flag`: location (-4.0, -3.0, 0.0) -> (-4.0, -3.0, -1.0)
- `canopy_top` (moved) for `canopy_top`: location (3.0, -8.0, 0.0) -> (3.0, -8.0, -1.6)
- `thrown_pot` (moved) for `thrown_pot`: location (-3.0, -7.0, 2.0) -> (-3.0, -7.0, 0.0)
- `walker_root` (delta_location keys) for `walker_card`: Z offset (world units) on 3 sampled frames: f31 -0.225, f41 -0.207, f51 -0.032

Before the fix: 34 FAIL rows (6 objects).  After the fix (table below): 0 FAIL rows.

## Skipped as airborne

- `thrown_pot` on frames 31, 41, 51, 60

(table of OK rows omitted; the run ends with `exit code: 0`)

## Setup 2: the real film-3 set, set3d3/harbor.py ("WINTER", Boston waterfront) + 3 actors + the set's own props
Planted: `cart` hovers 0.8 over the yard, `mill` walks with Z up to 0.3 too high, `sailor` is put at z 0.5 on the sidewalk
(a real raised surface there, so it passes), `clerk` on the cobbles passes. The set's own `bucket` and `yard_props` are
picked up by the name rules.

### 2a. check only
# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 7 (1, 11, 21, 31, 41, 51, 60)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 8   rows: 56   FAIL rows: 19   **result: FAIL (3 objects)**
- command: `blender -b ... --python ground_check.py -- --every 10 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/tools/GROUND_harbor.md`

## Failing objects

| object | kind | failing frames | worst gap |
|---|---|---|---|
| cart | prop | 1, 11, 21, 31, 41, 51, 60 | 0.8000 |
| mill_card | card | 11, 21, 41, 51, 60 | 0.3000 |
| trestle_girders | prop | 1, 11, 21, 31, 41, 51, 60 | 2.4938 |

<details><summary>all rows</summary>

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| cart | 1 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| cart | 11 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| cart | 21 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| cart | 31 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| cart | 41 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| cart | 51 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| cart | 60 | +0.8000 | FAIL | prop/bbox | 0.800 | ground |
| mill_card | 11 | +0.0508 | FAIL | card/alpha | 0.051 | ground |
| mill_card | 21 | +0.1017 | FAIL | card/alpha | 0.102 | ground |
| mill_card | 41 | +0.0534 | FAIL | card/alpha | 0.203 | street |
| mill_card | 51 | +0.1042 | FAIL | card/alpha | 0.254 | street |
| mill_card | 60 | +0.3000 | FAIL | card/alpha | 0.300 | ground |
| trestle_girders | 1 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| trestle_girders | 11 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| trestle_girders | 21 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| trestle_girders | 31 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| trestle_girders | 41 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| trestle_girders | 51 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| trestle_girders | 60 | +2.4938 | FAIL | prop/bbox | 3.034 | trestle_columns |
| bucket | 1 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket | 11 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket | 21 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket | 31 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket | 41 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket | 51 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket | 60 | -0.2416 | OK | prop/bbox | -0.006 | bucket_fill |
| bucket_fill | 1 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| bucket_fill | 11 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| bucket_fill | 21 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| bucket_fill | 31 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| bucket_fill | 41 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| bucket_fill | 51 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| bucket_fill | 60 | -0.1535 | OK | prop/bbox | 0.226 | tank_foot |
| clerk_card | 1 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| clerk_card | 11 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| clerk_card | 21 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| clerk_card | 31 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| clerk_card | 41 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| clerk_card | 51 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| clerk_card | 60 | -0.0000 | OK | card/alpha | 0.000 | trestle_columns |
| mill_card | 1 | +0.0000 | OK | card/alpha | 0.000 | ground |
| mill_card | 31 | +0.0025 | OK | card/alpha | 0.153 | street |
| sailor_card | 1 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| sailor_card | 11 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| sailor_card | 21 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| sailor_card | 31 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| sailor_card | 41 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| sailor_card | 51 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| sailor_card | 60 | -0.0400 | OK | card/alpha | 0.500 | trestle_columns |
| yard_props | 1 | -0.0258 | OK | prop/bbox | -0.026 | ground |
| yard_props | 11 | -0.0258 | OK | prop/bbox | -0.026 | ground |
| yard_props | 21 | -0.0258 | OK | prop/bbox | -0.026 | ground |
| yard_props | 31 | -0.0258 | OK | prop/bbox | -0.026 | ground |
| yard_props | 41 | -0.0258 | OK | prop/bbox | -0.026 | ground |
| yard_props | 51 | -0.0258 | OK | prop/bbox | -0.026 | ground |
| yard_props | 60 | -0.0258 | OK | prop/bbox | -0.026 | ground |
exit code: 1

</details>

### 2b. with --fix
# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 7 (1, 11, 21, 31, 41, 51, 60)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 8   rows: 56   FAIL rows: 0   **result: PASS**
- command: `blender -b ... --python ground_check.py -- --every 10 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/tools/GROUND_harbor.md --fix`

## --fix: changes made

- `cart` (moved) for `cart`: location (2.0, 8.0, 0.8) -> (2.0, 8.0, 0.0)
- `trestle_girders` (moved) for `trestle_girders`: location (0.0, 0.0, 0.0) -> (0.0, 0.0, -2.4938)
- `mill_root` (delta_location keys) for `mill_card`: Z offset (world units) on 5 sampled frames: f11 -0.051, f21 -0.102, f41 -0.053, f51 -0.104, f60 -0.300

Before the fix: 19 FAIL rows (3 objects).  After the fix (table below): 0 FAIL rows.

(table of OK rows omitted; the run ends with `exit code: 0`)

## What these runs show
- Cards use the lowest VISIBLE alpha row of that frame's sprite (ox: 0.291, not 0.475). Animated actors get `delta_location` keys
  on `<name>_root`; their placement keys are untouched.
- **False positive in the real set:** `trestle_girders` (elevated-railway deck, 2.49 above its columns) is picked up because "girder"
  is in the prop name list, and `--fix` pulled the whole deck down 2.49. Tag set structure `obj["gc_role"] = "ground"` or pass
  `--skip trestle`. This is the price of name rules (film 20's "girder chunk in the sky" is what that word is for).
- `--fix` on `thrown_pot` (airborne only on frames 30..60) moved it to the ground for ALL frames, because a static object cannot be
  fixed per frame: fix such objects by hand or key them.
