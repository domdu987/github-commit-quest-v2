# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 8 (930, 946, 961, 976, 991, 1006, 1021, 1025)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 14   rows: 112   FAIL rows: 0   **result: PASS**
- command: `run_check frame_list=[929, 945, 960, 975, 990, 1005, 1020, 1024] gap 0.02 skip=lantern2f_iron|outside_props_x`

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| flame_bench_flame | 930 | -0.0409 | OK | prop/bbox | 1.314 | stub_bench_wick |
| flame_bench_flame | 946 | -0.0405 | OK | prop/bbox | 1.282 | stub_bench_wick |
| flame_bench_flame | 961 | -0.0399 | OK | prop/bbox | 1.234 | stub_bench_wick |
| flame_bench_flame | 976 | -0.0394 | OK | prop/bbox | 1.189 | stub_bench_wick |
| flame_bench_flame | 991 | -0.0389 | OK | prop/bbox | 1.149 | stub_bench_wick |
| flame_bench_flame | 1006 | -0.0384 | OK | prop/bbox | 1.108 | stub_bench_wick |
| flame_bench_flame | 1021 | -0.0380 | OK | prop/bbox | 1.078 | stub_bench_wick |
| flame_bench_flame | 1025 | -0.0379 | OK | prop/bbox | 1.075 | stub_bench_wick |
| flame_lamp_flame | 930 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 946 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 961 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 976 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 991 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1006 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1021 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| flame_lamp_flame | 1025 | -0.0370 | OK | prop/bbox | 1.952 | shop_terra |
| har_card | 930 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| har_card | 946 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| har_card | 961 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| har_card | 976 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| har_card | 991 | -0.0078 | OK | card/alpha | -0.008 | shop_floor |
| har_card | 1006 | -0.0078 | OK | card/alpha | -0.008 | shop_floor2 |
| har_card | 1021 | -0.0078 | OK | card/alpha | -0.008 | shop_floor2 |
| har_card | 1025 | -0.0078 | OK | card/alpha | -0.008 | shop_oakd |
| lantern2_lampg | 930 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 946 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 961 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 976 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 991 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1006 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1021 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2_lampg | 1025 | +0.0092 | OK | prop/bbox | 3.385 | lantern2f_iron |
| lantern2g_iron | 930 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 946 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 961 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 976 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 991 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1006 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron | 1025 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 930 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 946 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 961 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 976 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 991 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1006 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.001 | 1025 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 930 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 946 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 961 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 976 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 991 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1006 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.002 | 1025 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 930 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 946 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 961 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 976 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 991 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1006 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1021 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern2g_iron.003 | 1025 | -0.0370 | OK | prop/bbox | 3.349 | lantern2_lampg |
| lantern_lampg | 930 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 946 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 961 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 976 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 991 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1006 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1021 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| lantern_lampg | 1025 | -0.0046 | OK | prop/bbox | 1.184 | lanternf_iron |
| shop_beam | 930 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 946 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 961 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 976 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 991 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1006 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1021 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_beam | 1025 | -0.0000 | OK | prop/bbox | 0.000 | shop_plaster |
| shop_sack | 930 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 946 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 961 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 976 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 991 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1006 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1021 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_sack | 1025 | -0.0370 | OK | prop/bbox | -0.037 | shop_floor |
| shop_stone | 930 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 946 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 961 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 976 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 991 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1006 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1021 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| shop_stone | 1025 | +0.0000 | OK | prop/bbox | 0.000 | shop_floor |
| stub_bench_cream | 930 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 946 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 961 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 976 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 991 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 1006 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 1021 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_cream | 1025 | -0.0555 | OK | prop/bbox | 1.036 | shop_oak |
| stub_bench_wick | 930 | -0.1482 | OK | prop/bbox | 1.347 | flame_bench_flame |
| stub_bench_wick | 946 | -0.1478 | OK | prop/bbox | 1.316 | flame_bench_flame |
| stub_bench_wick | 961 | -0.1472 | OK | prop/bbox | 1.268 | flame_bench_flame |
| stub_bench_wick | 976 | -0.1467 | OK | prop/bbox | 1.224 | flame_bench_flame |
| stub_bench_wick | 991 | -0.1462 | OK | prop/bbox | 1.184 | flame_bench_flame |
| stub_bench_wick | 1006 | -0.1456 | OK | prop/bbox | 1.144 | flame_bench_flame |
| stub_bench_wick | 1021 | -0.1453 | OK | prop/bbox | 1.114 | flame_bench_flame |
| stub_bench_wick | 1025 | -0.1452 | OK | prop/bbox | 1.111 | flame_bench_flame |

## Notes (render team8)
- Skipped by regex `lantern2f_iron|outside_props_x`: the ceiling-hung lantern (hangs by design) and the set-dressing bushes/wood beyond the window (bbox over uneven grass, not a character or a contact). First run without skip: the only FAIL rows were those three set objects; all character cards and bench props passed.
