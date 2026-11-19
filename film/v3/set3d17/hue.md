# film 17 set3d17: colour numbers per frame (final, 720x1280, placeholders at the stand points)

Bands: shade hue 240-260; black point (luma p1) 0.08-0.12; blue share 14-30 %; magenta <= 10 %; vivid blue (S>0.6, H200-245) < 1.5 %; head-ring luma about 95-165. The street (exterior, dusk) may leave the hue band.

| tile | red | orange | blue | magenta | shade hue | p1 | vivid % | dim 240-260 % | dim 0-45 % | val | dark | head ring luma (median) | render s | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| measure_wide [DAY_INT] | 35.7 | 29.3 | 25.2 | 6.9 | 234.1 | 0.120 | 0.0 | 29 | 1 | 0.50 | 0.03 | chair 93, clerk 66, prisoner_toise 67, bench1 124, bench2 142 | 115 | OUT: shade |
| measure_chair [DAY_INT] | 42.0 | 29.9 | 16.3 | 8.7 | 243.2 | 0.118 | 0.0 | 41 | 5 | 0.53 | 0.09 | chair 77, clerk 136 | 103 | ok |
| measure_high [DAY_INT] | 47.4 | 19.5 | 17.6 | 10.6 | 248.9 | 0.116 | 0.0 | 32 | 1 | 0.48 | 0.09 | chair 84, bench0 140, bench1 142, bench2 140, bench3 139, queue0 93 | 100 | OUT: magenta |
| measure_door [DAY_INT] | 28.6 | 52.3 | 9.4 | 1.2 | 253.1 | 0.215 | 0.0 | 7 | 16 | 0.57 | 0.00 | queue1 139, door_in 137, door_mid 136 | 101 | OUT: p1,blue |
| measure_low [DAY_INT] | 36.2 | 31.2 | 22.4 | 4.1 | 237.9 | 0.119 | 0.3 | 30 | 2 | 0.52 | 0.05 | chair 129, clerk 66 | 116 | OUT: shade |
| records_aisle [DAY_INT] | 41.6 | 10.3 | 16.8 | 17.0 | 261.4 | 0.119 | 1.3 | 8 | 12 | 0.40 | 0.16 | aisle0 66, aisle1 71, aisle2 58 | 133 | OUT: shade,magenta |
| records_low [DAY_INT] | 40.0 | 10.9 | 18.9 | 14.1 | 255.3 | 0.118 | 0.8 | 17 | 16 | 0.40 | 0.17 | low_a 92 | 128 | OUT: magenta |
| records_desk [DAY_INT] | 45.0 | 6.6 | 26.5 | 15.0 | 237.8 | 0.119 | 3.0 | 13 | 6 | 0.43 | 0.08 | desk_clerk 98, desk_stand 249 | 128 | OUT: shade,magenta,vivid |
| records_ladder [DAY_INT] | 56.7 | 14.7 | 14.1 | 10.3 | 252.3 | 0.120 | 0.2 | 30 | 25 | 0.47 | 0.13 | ladder_foot 85, ladder_up 94 | 115 | OUT: magenta |
| drawer_big [DAY_INT] | 51.5 | 19.1 | 10.2 | 13.5 | 243.9 | 0.123 | 0.0 | 10 | 8 | 0.49 | 0.05 | inspector 59 | 93 | OUT: p1,blue,magenta |
| drawer_box [DAY_INT] | 58.8 | 15.2 | 14.6 | 7.4 | 241.7 | 0.123 | 0.0 | 14 | 0 | 0.53 | 0.06 | - | 96 | OUT: p1 |
| card_hero [DAY_INT] | 61.6 | 16.3 | 9.4 | 10.5 | 240.3 | 0.138 | 0.0 | 12 | 1 | 0.53 | 0.03 | - | 103 | OUT: p1,blue,magenta |
| street_wide [DUSK_EXT] | 62.4 | 12.2 | 7.6 | 13.0 | 240.4 | 0.168 | 0.4 | 27 | 0 | 0.62 | 0.01 | wagon_door 57, street_a 117, street_b 91, street_c 111 | 77 | OUT: p1,blue,magenta |
| street_wagon [DUSK_EXT] | 33.3 | 25.3 | 22.2 | 12.0 | 240.5 | 0.120 | 0.2 | 20 | 2 | 0.55 | 0.01 | wagon_door 55, wagon_step 55, steps_top 160 | 95 | OUT: p1,magenta |
| measure_wide [EVENING_INT] | 35.8 | 29.0 | 28.6 | 4.4 | 229.6 | 0.109 | 0.0 | 15 | 1 | 0.53 | 0.01 | chair 117, clerk 73, prisoner_toise 82, bench1 104, bench2 124 | 113 | OUT: shade |
| measure_chair [EVENING_INT] | 37.9 | 45.8 | 11.7 | 2.2 | 231.3 | 0.182 | 0.0 | 7 | 21 | 0.58 | 0.00 | chair 100, clerk 156 | 106 | OUT: shade,p1,blue |
| records_aisle [EVENING_INT] | 36.0 | 6.0 | 14.6 | 18.3 | 260.1 | 0.105 | 0.2 | 17 | 10 | 0.39 | 0.09 | aisle0 67, aisle1 72, aisle2 61 | 124 | OUT: shade,magenta |
| records_desk [EVENING_INT] | 37.3 | 4.4 | 31.6 | 16.7 | 244.4 | 0.105 | 0.2 | 18 | 6 | 0.42 | 0.06 | desk_clerk 93, desk_stand 249 | 127 | OUT: blue,magenta |
| card_hero [EVENING_INT] | 56.5 | 15.6 | 13.9 | 12.0 | 235.5 | 0.143 | 0.1 | 11 | 0 | 0.51 | 0.01 | - | 106 | OUT: shade,p1,blue,magenta |
| street_wide [DAY_INT] | 17.9 | 14.3 | 46.3 | 16.1 | 250.0 | 0.154 | 0.2 | 20 | 0 | 0.60 | 0.01 | wagon_door 53, street_a 110, street_b 86, street_c 105 | 75 | OUT: p1,blue,magenta |

## Summary (honest)

- Render cost, 720x1280, 64 samples + OIDN, 4 threads, no DOF: **75-133 s per frame** (street 75-98 s, reveal 93-106 s, measure 100-119 s, records 115-148 s); build 0.3-1.1 s; 12 k (reveal) to 70 k (records) triangles.
- Met on all 20 tiles: no readable text, no DOF, black point p1 0.105-0.123 in 16 of 20 interior tiles (OUT: measure_door 0.215, card_hero 0.138/0.143, street 0.12-0.17, measure_chair EVENING 0.182), vivid blue < 1.5 % in 19 of 20 (records_desk 3.0 % from the skylight edge bloom).
- Hue bands: **only `measure_chair [DAY_INT]` passes every band**. Residual misses: shade hue 230-238 in measure_wide / measure_low / records_desk (a little too cyan), 255-261 in records_aisle (too violet); magenta 10-19 % in the records office, the reveal and the street (warm wood plus violet ambient mixes toward 320-345 degrees); blue 9-10 % in measure_door, drawer_big and card_hero (little shade in those frames).
- Head-ring luma (median luma around each placeholder head, band about 95-165): 14 of 33 staged heads are inside; the dark ones sit in the records canyon (58-98), at the toise (66-67) and in front of the police wagon (55-57). Use the bench / door / desk / street_a-c marks for acting, or raise the cabinet strips (`strip_w`) for a brighter backdrop.
- The street (exterior, dusk) is allowed to leave the interior band.
