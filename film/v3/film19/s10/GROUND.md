# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 12 (765, 774, 784, 794, 804, 814, 824, 834, 844, 854, 862, 872)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 4   rows: 48   FAIL rows: 0   **result: PASS**
- command: `blender -b ... --python ground_check.py -- --frame-list 765,774,784,794,804,814,824,834,844,854,862,872 --gap 0.02 --out /home/user/github-commit-quest-v2/film/v3/film19/s10/GROUND.md`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| bb_card | 765 | -0.2060 | OK | card/bbox | -0.169 | carpet |
| bb_card | 774 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 784 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 794 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 804 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 814 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 824 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 834 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 844 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 854 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bb_card | 862 | -0.1892 | OK | card/bbox | -0.152 | carpet |
| bb_card | 872 | -0.1892 | OK | card/bbox | -0.152 | carpet |
| cc_card | 765 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| cc_card | 774 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 784 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 794 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 804 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 814 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 824 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 834 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 844 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 854 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 862 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| cc_card | 872 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| har_card | 765 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| har_card | 774 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| har_card | 784 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl2 |
| har_card | 794 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| har_card | 804 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl2 |
| har_card | 814 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl2 |
| har_card | 824 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| har_card | 834 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| har_card | 844 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl2 |
| har_card | 854 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| har_card | 862 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl2 |
| har_card | 872 | -0.1875 | OK | card/bbox | -0.188 | hall_hfl1 |
| mock_card | 765 | -0.1674 | OK | card/bbox | -0.130 | carpet |
| mock_card | 774 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 784 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 794 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 804 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 814 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 824 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 834 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 844 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 854 | -0.1760 | OK | card/bbox | -0.139 | carpet |
| mock_card | 862 | -0.2060 | OK | card/bbox | -0.169 | carpet |
| mock_card | 872 | -0.2060 | OK | card/bbox | -0.169 | carpet |
