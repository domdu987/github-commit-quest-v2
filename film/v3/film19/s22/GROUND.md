# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 6 (1751, 1771, 1791, 1811, 1831, 1851)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 2   rows: 12   FAIL rows: 0   **result: PASS**
- command: `run_check frame_list=[1750, 1770, 1790, 1810, 1830, 1850] gap 0.02 skip=None`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| har_card | 1751 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| har_card | 1771 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| har_card | 1791 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| har_card | 1811 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| har_card | 1831 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| har_card | 1851 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| mock_card | 1751 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| mock_card | 1771 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| mock_card | 1791 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| mock_card | 1811 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| mock_card | 1831 | +0.0036 | OK | card/alpha | 0.041 | carpet |
| mock_card | 1851 | +0.0036 | OK | card/alpha | 0.041 | carpet |
