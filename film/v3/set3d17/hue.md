# film 17 set3d17: colour numbers per frame (final, 720x1280, placeholders at the stand points)

Bands: shade hue 240-260; black point (luma p1) 0.08-0.12; blue share 14-30 %; magenta <= 10 %; vivid blue (S>0.6, H200-245) < 1.5 %; head-ring luma about 95-165. The street (exterior, dusk) may leave the hue band.

| tile | red | orange | blue | magenta | shade hue | p1 | vivid % | dim 240-260 % | dim 0-45 % | val | dark | head ring luma (median) | render s | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| measure_wide [DAY_INT] | 26.5 | 27.4 | 29.0 | 14.2 | 233.8 | 0.119 | 0.1 | 24 | 7 | 0.47 | 0.04 | chair 88, clerk 69, bench0 85, queue0 94, door_mid 164 | 109 | OUT: shade,magenta |
| measure_chair [DAY_INT] | 42.0 | 29.9 | 16.3 | 8.7 | 243.2 | 0.118 | 0.0 | 41 | 5 | 0.53 | 0.09 | chair 77, clerk 136 | 103 | ok |
| measure_high [DAY_INT] | 41.3 | 16.8 | 21.4 | 14.8 | 246.3 | 0.113 | 0.9 | 35 | 2 | 0.45 | 0.12 | chair 97, bench0 128, bench2 126, queue0 106, tripod 77 | 104 | OUT: magenta |
| measure_door [DAY_INT] | 34.5 | 46.8 | 10.5 | 1.3 | 247.5 | 0.215 | 0.0 | 8 | 17 | 0.58 | 0.00 | door_out 120, door_r 137 | 109 | OUT: p1,blue |
| measure_low [DAY_INT] | 29.4 | 24.6 | 37.7 | 5.9 | 234.6 | 0.119 | 2.1 | 22 | 15 | 0.45 | 0.09 | chair 98, clerk 58 | 112 | OUT: shade,blue,vivid |
| records_aisle [DAY_INT] | 40.3 | 10.1 | 18.4 | 18.0 | 258.7 | 0.119 | 1.5 | 5 | 12 | 0.40 | 0.14 | aisle1 58, aisle2 62, ladder_foot 45, aisle_far 38 | 126 | OUT: magenta |
| records_low [DAY_INT] | 40.0 | 10.9 | 18.9 | 14.1 | 255.3 | 0.118 | 0.8 | 17 | 16 | 0.40 | 0.17 | low_a 92 | 128 | OUT: magenta |
| records_desk [DAY_INT] | 47.7 | 10.6 | 19.1 | 13.8 | 242.6 | 0.119 | 3.5 | 11 | 1 | 0.43 | 0.09 | desk_clerk 90, desk_stand 84 | 144 | OUT: magenta,vivid |
| records_ladder [DAY_INT] | 61.3 | 13.9 | 8.3 | 10.5 | 259.1 | 0.119 | 0.0 | 9 | 41 | 0.45 | 0.09 | ladder_up 91 | 137 | OUT: blue,magenta |
| drawer_big [DAY_INT] | 45.5 | 11.2 | 19.6 | 19.1 | 238.1 | 0.120 | 3.9 | 12 | 2 | 0.46 | 0.08 | drawer_r 127, drawer_l 73 | 95 | OUT: shade,p1,magenta,vivid |
| drawer_box [DAY_INT] | 39.6 | 29.2 | 11.9 | 5.7 | 247.1 | 0.116 | 0.0 | 18 | 1 | 0.58 | 0.10 | - | 108 | OUT: blue |
| card_hero [DAY_INT] | 37.0 | 12.6 | 15.8 | 23.6 | 252.9 | 0.126 | 0.0 | 12 | 0 | 0.43 | 0.13 | - | 144 | OUT: p1,magenta |
| street_wide [DUSK_EXT] | 62.4 | 12.2 | 7.6 | 13.0 | 240.4 | 0.168 | 0.4 | 27 | 0 | 0.62 | 0.01 | wagon_door 57, street_a 117, street_b 91, street_c 111 | 77 | OUT: p1,blue,magenta |
| street_wagon [DUSK_EXT] | 33.3 | 25.3 | 22.2 | 12.0 | 240.5 | 0.120 | 0.2 | 20 | 2 | 0.55 | 0.01 | wagon_door 55, wagon_step 55, steps_top 160 | 95 | OUT: p1,magenta |
| measure_wide [EVENING_INT] | 27.2 | 6.4 | 40.0 | 22.2 | 233.3 | 0.105 | 1.1 | 10 | 3 | 0.38 | 0.12 | chair 80, clerk 53, bench0 43, queue0 70, door_mid 127 | 109 | OUT: shade,blue,magenta |
| measure_chair [EVENING_INT] | 43.4 | 6.8 | 30.1 | 16.1 | 235.7 | 0.136 | 1.8 | 25 | 6 | 0.41 | 0.11 | chair 63, clerk 105 | 114 | OUT: shade,p1,blue,magenta,vivid |
| records_aisle [EVENING_INT] | 9.5 | 2.2 | 32.9 | 23.3 | 254.4 | 0.105 | 2.7 | 31 | 0 | 0.30 | 0.33 | aisle1 48, aisle2 56, ladder_foot 41, aisle_far 34 | 131 | OUT: blue,magenta,vivid |
| records_desk [EVENING_INT] | 22.6 | 9.5 | 30.5 | 22.2 | 248.0 | 0.105 | 7.3 | 18 | 1 | 0.35 | 0.17 | desk_clerk 67, desk_stand 64 | 144 | OUT: blue,magenta,vivid |
| card_hero [EVENING_INT] | 23.6 | 13.5 | 24.6 | 21.6 | 250.5 | 0.112 | 1.1 | 15 | 0 | 0.38 | 0.23 | - | 103 | OUT: magenta |
| street_wide [DAY_INT] | 17.9 | 14.3 | 46.3 | 16.1 | 250.0 | 0.154 | 0.2 | 20 | 0 | 0.60 | 0.01 | wagon_door 53, street_a 110, street_b 86, street_c 105 | 75 | OUT: p1,blue,magenta |
