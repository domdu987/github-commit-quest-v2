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
| S02 | - | not run | - | - |
| S03 | - | not run | - | - |
| S04 | - | not run | - | - |
| S05 | - | not run | - | - |
| S06 | - | not run | - | - |
| S07 | LANE | 765 rows, 45 objects | 0 | balloon_loose |
| S08 | - | not run | - | - |
| S11 | - | not run | - | - |
| S12 | LANE | 530 rows, 45 objects | 0 | balloon_loose, tank_lift |
| S13 | - | not run | - | - |
| S19 | - | not run | - | - |
| S09 | - | not run | - | - |
| S10 | - | not run | - | - |
| S14 | - | not run | - | - |
| S15 | - | not run | - | - |
| S16 | - | not run | - | - |
| S17 | - | not run | - | - |
| S18 | - | not run | - | - |

**Total: 1919 checks, 0 FAIL.**


## Allowed off the ground (flagged `airborne`)
- `tank_lift` while lifted (S12 / S13, the ONLY airborne tank); its contact blob stays on the grass and shrinks.
- `balloon_loose` (S19, the last balloon escaping).
- Cards parented to movers (jeep seats, boats, the lead tank deck) stand on their mover: they are checked, the ray hits the mover.
