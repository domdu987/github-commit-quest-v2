# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 15 (537, 546, 556, 566, 576, 586, 596, 606, 616, 626, 636, 646 ...)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 1   rows: 15   FAIL rows: 0   **result: PASS**
- command: `blender -b ... --python ground_check.py -- --frame-list 537,546,556,566,576,586,596,606,616,626,636,646,656,661,670 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/film19/s08/GROUND.md`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| ast_card | 537 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 546 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 556 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 566 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 576 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 586 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 596 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 606 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 616 | -0.2092 | OK | card/bbox | -0.172 | carpet |
| ast_card | 626 | -0.2092 | OK | card/bbox | -0.172 | carpet |
| ast_card | 636 | -0.2092 | OK | card/bbox | -0.172 | carpet |
| ast_card | 646 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 656 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 661 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| ast_card | 670 | -0.2245 | OK | card/bbox | -0.188 | carpet |
