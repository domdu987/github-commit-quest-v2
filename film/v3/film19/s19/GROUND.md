# GROUND.md -- ground check

- scene: `Scene`   file: `(unsaved)`
- frames sampled: 17 (1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1556, 1560 ...)   tolerance: gap > 0.020 units FAILS   rays: straight down from the lowest contact point(s)
- checked objects: 5   rows: 79   FAIL rows: 0   **result: PASS**
- command: `run_check frame_list=[1459, 1469, 1479, 1489, 1499, 1509, 1519, 1529, 1539, 1549, 1555, 1559, 1565, 1569, 1575, 1579, 1589] gap 0.02`

## Skipped as airborne

- `sa_card` on frames 1556, 1560, 1566, 1570, 1576, 1580

## All rows

| object | frame | gap | status | kind/how | lowest z | surface under it |
|---|---|---|---|---|---|---|
| crate_w_batten | 1460 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1470 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1480 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1490 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1500 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1510 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1520 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1530 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1540 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1550 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1556 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1560 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1566 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1570 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1576 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1580 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_batten | 1590 | -0.0701 | OK | prop/bbox | 0.460 | terrain |
| crate_w_crate | 1460 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1470 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1480 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1490 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1500 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1510 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1520 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1530 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1540 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1550 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1556 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1560 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1566 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1570 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1576 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1580 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| crate_w_crate | 1590 | -0.2982 | OK | prop/bbox | 0.478 | crate_w_batten |
| sa_card | 1460 | -0.0191 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1470 | -0.0191 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1480 | -0.0191 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1490 | -0.0191 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1500 | -0.0192 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1510 | -0.0193 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1520 | -0.0188 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1530 | -0.0177 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1540 | -0.0152 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1550 | -0.0103 | OK | card/alpha | 0.471 | terrain |
| sa_card | 1590 | -0.0107 | OK | card/alpha | 0.471 | terrain |
| sb_card | 1460 | -0.1489 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1470 | -0.1489 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1480 | -0.1489 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1490 | -0.1489 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1500 | -0.1488 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1510 | -0.1488 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1520 | -0.1487 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1530 | -0.1485 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1540 | -0.1482 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1550 | -0.1479 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1556 | -0.1468 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1560 | -0.1478 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1566 | -0.1468 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1570 | -0.1478 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1576 | -0.1468 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1580 | -0.1478 | OK | card/alpha | 0.486 | shoe_sb_1 |
| sb_card | 1590 | -0.1478 | OK | card/alpha | 0.486 | shoe_sb_1 |
| wil_card | 1460 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1470 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1480 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1490 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1500 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1510 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1520 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1530 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1540 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1550 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1556 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1560 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1566 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1570 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1576 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1580 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
| wil_card | 1590 | -0.0274 | OK | card/alpha | 0.888 | crate_w_crate |
