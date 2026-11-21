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
| S14 | RHINE | 1680 rows, 105 objects | 0 | - |
| S15 | RHINE | 1484 rows, 106 objects | 0 | - |
| S16 | RHINE | 1470 rows, 105 objects | 0 | - |
| S17 | RHINE | 1155 rows, 105 objects | 0 | - |
| S18 | RHINE | 1309 rows, 119 objects | 0 | - |

**Total: 18537 checks, 0 FAIL.**

- FIELDS bare location: - checked objects: 36   rows: 36   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_FIELDS.md)
- LANE bare location: - checked objects: 39   rows: 39   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_LANE.md)
- CAMP bare location: - checked objects: 37   rows: 37   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_CAMP.md)
- RHINE bare location: - checked objects: 101   rows: 101   FAIL rows: 0   **result: PASS** (set_work/ground/GROUND_RHINE.md)

## Allowed off the ground (flagged `airborne`)
- `tank_lift` while lifted (S12 / S13, the ONLY airborne tank); its contact blob stays on the grass and shrinks.
- `balloon_loose` (S19, the last balloon escaping).
- Cards parented to movers (jeep seats, boats, the lead tank deck) stand on their mover: they are checked, the ray hits the mover.
