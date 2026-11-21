# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 15 (653, 662, 672, 682, 692, 702, 712, 722, 732, 742, 752, 762 ...)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 1   rows: 15   FAIL rows: 0   **result: PASS**
- command: `blender -b ... --python ground_check.py -- --frame-list 653,662,672,682,692,702,712,722,732,742,752,762,772,773,782 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/film19/s09/GROUND.md`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| ast_card | 653 | -0.2133 | OK | card/bbox | -0.176 | carpet |
| ast_card | 662 | -0.2235 | OK | card/bbox | -0.186 | carpet |
| ast_card | 672 | -0.2235 | OK | card/bbox | -0.186 | carpet |
| ast_card | 682 | -0.2170 | OK | card/bbox | -0.180 | carpet |
| ast_card | 692 | -0.2105 | OK | card/bbox | -0.174 | carpet |
| ast_card | 702 | -0.2105 | OK | card/bbox | -0.174 | carpet |
| ast_card | 712 | -0.2170 | OK | card/bbox | -0.180 | carpet |
| ast_card | 722 | -0.2235 | OK | card/bbox | -0.186 | carpet |
| ast_card | 732 | -0.2235 | OK | card/bbox | -0.186 | carpet |
| ast_card | 742 | -0.2170 | OK | card/bbox | -0.180 | carpet |
| ast_card | 752 | -0.2105 | OK | card/bbox | -0.174 | carpet |
| ast_card | 762 | -0.2105 | OK | card/bbox | -0.174 | carpet |
| ast_card | 772 | -0.2170 | OK | card/bbox | -0.180 | carpet |
| ast_card | 773 | -0.2133 | OK | card/bbox | -0.176 | carpet |
| ast_card | 782 | -0.2235 | OK | card/bbox | -0.186 | carpet |
