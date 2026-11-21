# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 7 (1008, 1021, 1041, 1061, 1081, 1096, 1105)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 14   rows: 98   FAIL rows: 0   **result: PASS**
- command: `run_check frame_list=[1007, 1020, 1040, 1060, 1080, 1095, 1104] gap 0.02 skip=lantern2f_iron|outside_props_x`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| flame_bench_flame | 1008 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_bench_flame | 1021 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_bench_flame | 1041 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_bench_flame | 1061 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_bench_flame | 1081 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_bench_flame | 1096 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_bench_flame | 1105 | -0.0409 | OK | prop/bbox | 1.998 | stub_bench_wick |
| flame_lamp_flame | 1008 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1021 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1041 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1061 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1081 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1096 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1105 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| har_card | 1008 | -0.0099 | OK | card/alpha | -0.010 | shop_floor |
| har_card | 1021 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| har_card | 1041 | -0.0009 | OK | card/alpha | -0.001 | shop_floor2 |
| har_card | 1061 | -0.0009 | OK | card/alpha | -0.001 | shop_floor |
| har_card | 1081 | -0.0058 | OK | card/alpha | -0.006 | shop_floor |
| har_card | 1096 | -0.0135 | OK | card/alpha | -0.013 | shop_floor2 |
| har_card | 1105 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| lantern2_lampg | 1008 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1021 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1041 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1061 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1081 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1096 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1105 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2g_iron | 1008 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1041 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1061 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1081 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1096 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1105 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1008 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1041 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1061 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1081 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1096 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1105 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1008 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1041 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1061 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1081 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1096 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1105 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1008 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1041 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1061 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1081 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1096 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1105 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern_lampg | 1008 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1021 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1041 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1061 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1081 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1096 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1105 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| shop_beam | 1008 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1021 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1041 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1061 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1081 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1096 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1105 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_sack | 1008 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1021 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1041 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1061 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1081 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1096 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1105 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_stone | 1008 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1021 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1041 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1061 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1081 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1096 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1105 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| stub_bench_cream | 1008 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_cream | 1021 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_cream | 1041 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_cream | 1061 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_cream | 1081 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_cream | 1096 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_cream | 1105 | -0.0348 | OK | prop/bbox | 1.720 | h1_honey |
| stub_bench_wick | 1008 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |
| stub_bench_wick | 1021 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |
| stub_bench_wick | 1041 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |
| stub_bench_wick | 1061 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |
| stub_bench_wick | 1081 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |
| stub_bench_wick | 1096 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |
| stub_bench_wick | 1105 | -0.1482 | OK | prop/bbox | 2.031 | flame_bench_flame |

## Notes (render team8)
- Skipped by regex `lantern2f_iron|outside_props_x`: the ceiling-hung lantern and the set-dressing bushes/wood beyond the window (same set objects as s12). First run without skip: the only FAIL rows were those three; the character card and bench props passed.
