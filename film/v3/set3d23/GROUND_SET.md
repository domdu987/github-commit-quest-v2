# GROUND_SET.md : "nothing floats" (film/v3/tools/ground_check.py on the film-23 set)

Run: `python3 ghost.py ground` (ghost_ground.py).  Tolerance 0.02 D (1 D = one head).  Per shot: build(shot) with its placeholder cards, the
shot's action state (ghost_shot_table.ACTION: deflate, jeep, lift, pile, boats, inflating rows, riding cyclists) and the keyed camera, sampled every
10th frame of the x1.25 take (first and last always), `ground_check.run_check` on each sample.  Per location: `ground_check.run_cli` on the bare
build (reports in set_work/ground/GROUND_<LOC>.md).  Every prop is placed by `ground_snap` (ray cast) and has a `contact_shadow`; merged scenery
(terrain, lane strips, hedges, trees, houses) is tagged gc_role "ground" and is not a prop.  The fine dressing (grass tufts, flowers, pebbles,
glints, light-pool decals, mist, smoke) is HIDDEN from the rays while snapping and checking, so nothing may rest on a grass blade.

| shot | location | samples x objects checked | FAIL | airborne (flagged, skipped) |
|---|---|---|---|---|
| S01 | FIELDS | 624 rows, 39 objects | 0 | - |
| S02 | LANE | 774 rows, 43 objects | 0 | balloon_loose |
| S03 | LANE | 630 rows, 42 objects | 0 | balloon_loose |
| S04 | LANE | 756 rows, 42 objects | 0 | balloon_loose |
| S05 | LANE | 900 rows, 50 objects | 0 | balloon_loose |
| S06 | LANE | 473 rows, 43 objects | 0 | balloon_loose |
| S07 | LANE | 765 rows, 45 objects | 0 | balloon_loose |
| S08 | LANE | 540 rows, 45 objects | 0 | balloon_loose |
| S11 | LANE | 520 rows, 40 objects | 0 | balloon_loose |
| S12 | LANE | 530 rows, 45 objects | 0 | balloon_loose, tank_lift |
| S13 | LANE | 810 rows, 45 objects | 0 | balloon_loose, tank_lift |
| S19 | LANE | 2559 rows, 145 objects | 0 | balloon_loose |
| S09 | CAMP | 779 rows, 41 objects | 0 | - |
| S10 | CAMP | 779 rows, 41 objects | 0 | - |
| S14 | RHINE | 2320 rows, 145 objects | 0 | - |
| S15 | RHINE | 2114 rows, 151 objects | 14 | - |
| S16 | RHINE | 2170 rows, 155 objects | 0 | - |
| S17 | RHINE | 1595 rows, 145 objects | 0 | - |
| S18 | RHINE | 1815 rows, 165 objects | 0 | - |

**Total: 21453 checks, 14 FAIL.**

- FIELDS bare location: - checked objects: 36   rows: 36   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_FIELDS.md)
- LANE bare location: - checked objects: 39   rows: 39   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_LANE.md)
- CAMP bare location: - checked objects: 37   rows: 37   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_CAMP.md)
- RHINE bare location: - checked objects: 141   rows: 141   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_RHINE.md)

## Remaining fails

| shot | frame | object | gap | hit |
|---|---|---|---|---|
| S15 | 1 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 11 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 21 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 31 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 41 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 51 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 61 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 71 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 81 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 91 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 101 | fg_coil.096 | 0.1987 | fg_pump.097 |
| S15 | 111 | fg_coil.096 | 0.1987 | fg_pump.097 |

## Allowed off the ground (flagged `airborne`)
- `tank_lift` while lifted (S12 / S13, the ONLY airborne tank); its contact blob stays on the grass and shrinks.
- `balloon_loose` (S19, the last balloon escaping).
- Cards parented to movers (jeep seats, boats, the lead tank deck) stand on their mover: they are checked, the ray hits the mover.
