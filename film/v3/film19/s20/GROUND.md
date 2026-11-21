# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 12 (1573, 1582, 1592, 1602, 1612, 1622, 1632, 1642, 1652, 1662, 1665, 1674)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 1   rows: 12   FAIL rows: 0   **result: PASS**
- command: `blender -b ... --python ground_check.py -- --frame-list 1573,1582,1592,1602,1612,1622,1632,1642,1652,1662,1665,1674 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/film19/s20/GROUND.md`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| ast_card | 1573 | -0.2204 | OK | card/bbox | -0.183 | carpet |
| ast_card | 1582 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1592 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1602 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1612 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1622 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1632 | -0.2195 | OK | card/bbox | -0.182 | carpet |
| ast_card | 1642 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1652 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1662 | -0.2234 | OK | card/bbox | -0.186 | carpet |
| ast_card | 1665 | -0.2136 | OK | card/bbox | -0.177 | carpet |
| ast_card | 1674 | -0.2166 | OK | card/bbox | -0.180 | carpet |
