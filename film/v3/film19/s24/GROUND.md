# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 10 (1931, 1961, 1991, 2011, 2041, 2071, 2101, 2113, 2131, 2160)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 7   rows: 38   FAIL rows: 2   **result: FAIL (1 objects)**
- command: `blender -b ... --python ground_check.py -- --frame-list 1931,1961,1991,2011,2041,2071,2101,2113,2131,2160 --out GROUND.md`

## Failing objects

| object | kind | failing frames | worst gap |
|---|---|---|---|
| bag_hsack | prop | 2101, 2113 | 4.5912 |

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| bag_hsack | 2101 | +4.5912 | FAIL | prop/bbox | 8.334 | shafts_shafts |
| bag_hsack | 2113 | +0.2207 | FAIL | prop/bbox | 1.725 | hall_hbaize |
| astro_card | 2041 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| astro_card | 2071 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| bag_hcoin | 2101 | -0.1876 | OK | prop/bbox | 8.428 | bag_hsack |
| bag_hcoin | 2113 | -0.1876 | OK | prop/bbox | 1.819 | bag_hsack |
| bag_hcoin | 2131 | -0.1876 | OK | prop/bbox | 1.538 | bag_hsack |
| bag_hcoin | 2160 | -0.1876 | OK | prop/bbox | 1.538 | bag_hsack |
| bag_hsack | 2131 | -0.0611 | OK | prop/bbox | 1.443 | hall_hbaize |
| bag_hsack | 2160 | -0.0611 | OK | prop/bbox | 1.443 | hall_hbaize |
| bag_hwax | 2101 | -0.2590 | OK | prop/bbox | 9.081 | bag_hsack |
| bag_hwax | 2113 | -0.2590 | OK | prop/bbox | 2.472 | bag_hsack |
| bag_hwax | 2131 | -0.2590 | OK | prop/bbox | 2.190 | bag_hsack |
| bag_hwax | 2160 | -0.2590 | OK | prop/bbox | 2.190 | bag_hsack |
| har_card | 2101 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| har_card | 2113 | -0.0645 | OK | card/bbox | -0.028 | carpet |
| har_card | 2131 | -0.1750 | OK | card/bbox | -0.138 | carpet |
| har_card | 2160 | -0.1977 | OK | card/bbox | -0.161 | carpet |
| king_card | 1931 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 1961 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 1991 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 2011 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 2041 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 2071 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 2101 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 2113 | -0.2316 | OK | card/bbox | -0.195 | carpet |
| king_card | 2131 | -0.2245 | OK | card/bbox | -0.188 | carpet |
| king_card | 2160 | -0.2282 | OK | card/bbox | -0.191 | carpet |
| table_panel | 1931 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 1961 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 1991 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2011 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2041 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2071 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2101 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2113 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2131 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
| table_panel | 2160 | -0.0070 | OK | prop/bbox | 0.030 | carpet |
