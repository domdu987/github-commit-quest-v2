# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 7 (1536, 1566, 1596, 1626, 1656, 1686, 1701)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 5   rows: 20   FAIL rows: 0   **result: PASS**
- command: `ground_t6b.py (per-g scene build, ground_check.py rows; every 30)`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| c2_bertillon_card | 1536 | -0.2774 | OK | card/bbox | 1.133 | arch_carcass |
| c2_bertillon_card | 1566 | -0.0674 | OK | card/bbox | 1.133 | arch_tiles |
| c2_bertillon_card | 1596 | -0.0674 | OK | card/bbox | 1.133 | arch_tiles |
| c2_bertillon_card | 1626 | -0.0674 | OK | card/bbox | 1.133 | arch_tiles |
| c2_bertillon_card | 1656 | -0.0674 | OK | card/bbox | 1.133 | arch_tiles |
| c2_dupont_card | 1536 | -0.2786 | OK | card/bbox | 1.131 | arch_carcass |
| c2_dupont_card | 1566 | -0.2786 | OK | card/bbox | 1.131 | arch_carcass |
| c2_dupont_card | 1596 | -0.0686 | OK | card/bbox | 1.131 | arch_tiles |
| c2_dupont_card | 1626 | -0.0686 | OK | card/bbox | 1.131 | arch_tiles |
| c2_dupont_card | 1656 | -0.0686 | OK | card/bbox | 1.131 | arch_tiles |
| c2_gend_a_card | 1536 | -0.2713 | OK | card/bbox | 1.139 | arch_carcass |
| c2_gend_a_card | 1566 | -0.2713 | OK | card/bbox | 1.139 | arch_carcass |
| c2_gend_a_card | 1596 | -0.0613 | OK | card/bbox | 1.139 | arch_tiles |
| c2_gend_a_card | 1626 | -0.0613 | OK | card/bbox | 1.139 | arch_tiles |
| c2_gend_a_card | 1656 | -0.0613 | OK | card/bbox | 1.139 | arch_tiles |
| c2_gend_b_card | 1536 | -0.0685 | OK | card/bbox | 1.131 | arch_tiles |
| c2_inspector_card | 1536 | -0.0646 | OK | card/bbox | 1.135 | arch_tiles |
| c2_inspector_card | 1656 | -0.0646 | OK | card/bbox | 1.135 | arch_tiles |
| c2_inspector_card | 1686 | -0.0646 | OK | card/bbox | 1.135 | arch_tiles |
| c2_inspector_card | 1701 | -0.0646 | OK | card/bbox | 1.135 | arch_tiles |

## Scope and notes (T6b)
- Checked: every cast card (`c2_*_card`) at g1536, 1566, 1596, 1626, 1656, 1686, 1701 (every 30th g plus first and last). All gaps are negative (the sprite's bottom edge is a few cm below the floor surface = sunk in, OK); no NO SURFACE.
- Not checked (not mine / not standing): set hardware (`banner*`, `box*`, `arch_*` meshes, e.g. ceiling-hung banner rods, which would FAIL by design) and the hand-held props `t6b_*` (MARTIN card, bottle, fist), which are held by Bertillon's/the gendarme's visible hand and are tagged `gc_role = skip`.
- Contact shadows: every visible cast card has `c2_<name>_shadow` and `c2_<name>_contact` in the scene at every sampled frame (listed in the run log, `SHADOWS` lines).
- Script: `ground_t6b.py` (builds each sampled g like `render_t6b.py`, no render) with `ground_check.py` from claude/new-session-73ou27.
