# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 6 (41, 71, 101, 131, 161, 191)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 21   rows: 111   FAIL rows: 12   **result: FAIL (2 objects)**
- command: `driver ground_run.py (stage_cast2 per sampled frame, frame = g+1): g 40,70,100,130,160,190`

## Failing objects

| object | kind | failing frames | worst gap |
|---|---|---|---|
| wagon_horse | prop | 41, 71, 101, 131, 161, 191 | 0.0952 |
| wagon_leather | prop | 41, 71, 101, 131, 161, 191 | 0.8010 |

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| wagon_horse | 41 | +0.0952 | FAIL | prop/bbox | 0.095 | ext_cobble |
| wagon_horse | 71 | +0.0952 | FAIL | prop/bbox | 0.095 | ext_cobble |
| wagon_horse | 101 | +0.0952 | FAIL | prop/bbox | 0.095 | ext_cobble |
| wagon_horse | 131 | +0.0952 | FAIL | prop/bbox | 0.095 | ext_cobble |
| wagon_horse | 161 | +0.0952 | FAIL | prop/bbox | 0.095 | ext_cobble |
| wagon_horse | 191 | +0.0952 | FAIL | prop/bbox | 0.095 | ext_cobble |
| wagon_leather | 41 | +0.8010 | FAIL | prop/bbox | 1.793 | wagon_iron |
| wagon_leather | 71 | +0.8010 | FAIL | prop/bbox | 1.793 | wagon_iron |
| wagon_leather | 101 | +0.8010 | FAIL | prop/bbox | 1.793 | wagon_iron |
| wagon_leather | 131 | +0.8010 | FAIL | prop/bbox | 1.793 | wagon_iron |
| wagon_leather | 161 | +0.8010 | FAIL | prop/bbox | 1.793 | wagon_iron |
| wagon_leather | 191 | +0.8010 | FAIL | prop/bbox | 1.793 | wagon_iron |
| c2_bertillon_card | 101 | -0.0147 | OK | card/alpha | 1.185 | measure_floor |
| c2_bertillon_card | 131 | -0.0147 | OK | card/alpha | 1.185 | measure_floor |
| c2_bertillon_card | 161 | -0.0146 | OK | card/alpha | 1.185 | measure_floor |
| c2_gend_room_card | 41 | -0.0277 | OK | card/alpha | 1.184 | measure_runner |
| c2_gend_room_card | 71 | -0.0277 | OK | card/alpha | 1.184 | measure_runner |
| c2_gend_room_card | 101 | -0.0157 | OK | card/alpha | 1.184 | measure_floor |
| c2_gend_room_card | 131 | -0.0157 | OK | card/alpha | 1.184 | measure_floor |
| c2_gend_room_card | 161 | -0.0164 | OK | card/alpha | 1.184 | measure_floor |
| c2_gend_room_card | 191 | -0.0157 | OK | card/alpha | 1.184 | measure_floor |
| c2_prisoner_a_card | 101 | -0.0319 | OK | card/alpha | 1.168 | measure_floor |
| c2_prisoner_a_card | 131 | -0.0319 | OK | card/alpha | 1.168 | measure_floor |
| c2_prisoner_a_card | 161 | -0.0319 | OK | card/alpha | 1.168 | measure_floor |
| c2_prisoner_b_card | 101 | -0.0461 | OK | card/alpha | 1.154 | measure_floor |
| c2_prisoner_b_card | 131 | -0.0461 | OK | card/alpha | 1.154 | measure_floor |
| c2_prisoner_b_card | 161 | -0.0463 | OK | card/alpha | 1.154 | measure_floor |
| c2_prisoner_q_card | 101 | -0.0355 | OK | card/alpha | 1.164 | measure_floor |
| c2_prisoner_q_card | 131 | -0.0355 | OK | card/alpha | 1.164 | measure_floor |
| c2_prisoner_q_card | 161 | -0.0360 | OK | card/alpha | 1.164 | measure_floor |
| ext_glow_lantern | 41 | -0.0200 | OK | prop/bbox | 1.840 | ext_brass |
| ext_glow_lantern | 71 | -0.0200 | OK | prop/bbox | 1.840 | ext_brass |
| ext_glow_lantern | 101 | -0.0200 | OK | prop/bbox | 1.840 | ext_brass |
| ext_glow_lantern | 131 | -0.0200 | OK | prop/bbox | 1.840 | ext_brass |
| ext_glow_lantern | 161 | -0.0200 | OK | prop/bbox | 1.840 | ext_brass |
| ext_glow_lantern | 191 | -0.0200 | OK | prop/bbox | 1.840 | ext_brass |
| ext_stone | 41 | -0.2900 | OK | prop/bbox | -0.150 | ext_stone_dk |
| ext_stone | 71 | -0.2900 | OK | prop/bbox | -0.150 | ext_stone_dk |
| ext_stone | 101 | -0.2900 | OK | prop/bbox | -0.150 | ext_stone_dk |
| ext_stone | 131 | -0.2900 | OK | prop/bbox | -0.150 | ext_stone_dk |
| ext_stone | 161 | -0.2900 | OK | prop/bbox | -0.150 | ext_stone_dk |
| ext_stone | 191 | -0.2900 | OK | prop/bbox | -0.150 | ext_stone_dk |
| ext_stone_dk | 41 | -0.2900 | OK | prop/bbox | -0.140 | ext_stone |
| ext_stone_dk | 71 | -0.2900 | OK | prop/bbox | -0.140 | ext_stone |
| ext_stone_dk | 101 | -0.2900 | OK | prop/bbox | -0.140 | ext_stone |
| ext_stone_dk | 131 | -0.2900 | OK | prop/bbox | -0.140 | ext_stone |
| ext_stone_dk | 161 | -0.2900 | OK | prop/bbox | -0.140 | ext_stone |
| ext_stone_dk | 191 | -0.2900 | OK | prop/bbox | -0.140 | ext_stone |
| flag_3 | 41 | -0.1898 | OK | prop/bbox | 7.409 | ext_gold |
| flag_3 | 71 | -0.1926 | OK | prop/bbox | 7.409 | ext_gold |
| flag_3 | 101 | -0.1989 | OK | prop/bbox | 7.409 | ext_gold |
| flag_3 | 131 | -0.1887 | OK | prop/bbox | 7.409 | ext_gold |
| flag_3 | 161 | -0.1959 | OK | prop/bbox | 7.409 | ext_gold |
| flag_3 | 191 | -0.1951 | OK | prop/bbox | 7.409 | ext_gold |
| flag_7 | 41 | -0.1898 | OK | prop/bbox | 7.409 | ext_gold |
| flag_7 | 71 | -0.1926 | OK | prop/bbox | 7.409 | ext_gold |
| flag_7 | 101 | -0.1989 | OK | prop/bbox | 7.409 | ext_gold |
| flag_7 | 131 | -0.1887 | OK | prop/bbox | 7.409 | ext_gold |
| flag_7 | 161 | -0.1959 | OK | prop/bbox | 7.409 | ext_gold |
| flag_7 | 191 | -0.1951 | OK | prop/bbox | 7.409 | ext_gold |
| measure_beam_fx | 41 | -0.2170 | OK | prop/bbox | 1.200 | window_leaf1_cobalt_paint |
| measure_beam_fx | 71 | -0.2170 | OK | prop/bbox | 1.200 | window_leaf1_cobalt_paint |
| measure_beam_fx | 191 | -0.2170 | OK | prop/bbox | 1.200 | window_leaf1_cobalt_paint |
| measure_ceil_beam | 41 | -0.2600 | OK | prop/bbox | 5.150 | measure_walnut |
| measure_ceil_beam | 71 | -0.2600 | OK | prop/bbox | 5.150 | measure_walnut |
| measure_ceil_beam | 101 | -0.2600 | OK | prop/bbox | 5.150 | measure_walnut |
| measure_ceil_beam | 131 | -0.2600 | OK | prop/bbox | 5.150 | measure_walnut |
| measure_ceil_beam | 161 | -0.2600 | OK | prop/bbox | 5.150 | measure_walnut |
| measure_ceil_beam | 191 | -0.2600 | OK | prop/bbox | 5.150 | measure_walnut |
| wagon_brass | 41 | -0.1532 | OK | prop/bbox | 0.437 | wagon_iron |
| wagon_brass | 71 | -0.1532 | OK | prop/bbox | 0.437 | wagon_iron |
| wagon_brass | 101 | -0.1532 | OK | prop/bbox | 0.437 | wagon_iron |
| wagon_brass | 131 | -0.1532 | OK | prop/bbox | 0.437 | wagon_iron |
| wagon_brass | 161 | -0.1532 | OK | prop/bbox | 0.437 | wagon_iron |
| wagon_brass | 191 | -0.1532 | OK | prop/bbox | 0.437 | wagon_iron |
| wagon_dark | 41 | -0.1070 | OK | prop/bbox | 0.000 | wagon_horse |
| wagon_dark | 71 | -0.1070 | OK | prop/bbox | 0.000 | wagon_horse |
| wagon_dark | 101 | -0.1070 | OK | prop/bbox | 0.000 | wagon_horse |
| wagon_dark | 131 | -0.1070 | OK | prop/bbox | 0.000 | wagon_horse |
| wagon_dark | 161 | -0.1070 | OK | prop/bbox | 0.000 | wagon_horse |
| wagon_dark | 191 | -0.1070 | OK | prop/bbox | 0.000 | wagon_horse |
| wagon_glow_gas | 41 | -0.0370 | OK | prop/bbox | 2.350 | wagon_brass |
| wagon_glow_gas | 71 | -0.0370 | OK | prop/bbox | 2.350 | wagon_brass |
| wagon_glow_gas | 101 | -0.0370 | OK | prop/bbox | 2.350 | wagon_brass |
| wagon_glow_gas | 131 | -0.0370 | OK | prop/bbox | 2.350 | wagon_brass |
| wagon_glow_gas | 161 | -0.0370 | OK | prop/bbox | 2.350 | wagon_brass |
| wagon_glow_gas | 191 | -0.0370 | OK | prop/bbox | 2.350 | wagon_brass |
| wagon_iron | 41 | -0.1100 | OK | prop/bbox | 0.040 | ext_stone |
| wagon_iron | 71 | -0.1100 | OK | prop/bbox | 0.040 | ext_stone |
| wagon_iron | 101 | -0.1100 | OK | prop/bbox | 0.040 | ext_stone |
| wagon_iron | 131 | -0.1100 | OK | prop/bbox | 0.040 | ext_stone |
| wagon_iron | 161 | -0.1100 | OK | prop/bbox | 0.040 | ext_stone |
| wagon_iron | 191 | -0.1100 | OK | prop/bbox | 0.040 | ext_stone |
| wagon_red | 41 | -0.2321 | OK | prop/bbox | 1.378 | wagon_horse |
| wagon_red | 71 | -0.2321 | OK | prop/bbox | 1.378 | wagon_horse |
| wagon_red | 101 | -0.2321 | OK | prop/bbox | 1.378 | wagon_horse |
| wagon_red | 131 | -0.2321 | OK | prop/bbox | 1.378 | wagon_horse |
| wagon_red | 161 | -0.2321 | OK | prop/bbox | 1.378 | wagon_horse |
| wagon_red | 191 | -0.2321 | OK | prop/bbox | 1.378 | wagon_horse |
| wagon_wagon | 41 | -0.0790 | OK | prop/bbox | 0.588 | wagon_wagon_red |
| wagon_wagon | 71 | -0.0790 | OK | prop/bbox | 0.588 | wagon_wagon_red |
| wagon_wagon | 101 | -0.0790 | OK | prop/bbox | 0.588 | wagon_wagon_red |
| wagon_wagon | 131 | -0.0790 | OK | prop/bbox | 0.588 | wagon_wagon_red |
| wagon_wagon | 161 | -0.0790 | OK | prop/bbox | 0.588 | wagon_wagon_red |
| wagon_wagon | 191 | -0.0790 | OK | prop/bbox | 0.588 | wagon_wagon_red |
| wagon_wagon_red | 41 | -0.1621 | OK | prop/bbox | -0.012 | ext_stone |
| wagon_wagon_red | 71 | -0.1621 | OK | prop/bbox | -0.012 | ext_stone |
| wagon_wagon_red | 101 | -0.1621 | OK | prop/bbox | -0.012 | ext_stone |
| wagon_wagon_red | 131 | -0.1621 | OK | prop/bbox | -0.012 | ext_stone |
| wagon_wagon_red | 161 | -0.1621 | OK | prop/bbox | -0.012 | ext_stone |
| wagon_wagon_red | 191 | -0.1621 | OK | prop/bbox | -0.012 | ext_stone |

## Contact shadows (cast cards)

| g | card | contact shadow object present and visible |
|---|---|---|
| 40 | bertillon | NO |
| 40 | prisoner_a | NO |
| 40 | prisoner_b | NO |
| 40 | prisoner_q | NO |
| 40 | gend_room | yes |
| 70 | bertillon | NO |
| 70 | prisoner_a | NO |
| 70 | prisoner_b | NO |
| 70 | prisoner_q | NO |
| 70 | gend_room | yes |
| 100 | bertillon | yes |
| 100 | prisoner_a | yes |
| 100 | prisoner_b | yes |
| 100 | prisoner_q | yes |
| 100 | gend_room | yes |
| 130 | bertillon | yes |
| 130 | prisoner_a | yes |
| 130 | prisoner_b | yes |
| 130 | prisoner_q | yes |
| 130 | gend_room | yes |
| 160 | bertillon | yes |
| 160 | prisoner_a | yes |
| 160 | prisoner_b | yes |
| 160 | prisoner_q | yes |
| 160 | gend_room | yes |
| 190 | bertillon | NO |
| 190 | prisoner_a | NO |
| 190 | prisoner_b | NO |
| 190 | prisoner_q | NO |
| 190 | gend_room | yes |
