# QA s25 (film 18, render team 2)

- Range: take g 1873..1965 (93 frames); shot g 1882..1957; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 18.7 s wall/frame (median 17.1); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 93 frames, 30.00 fps, g 1873-1965)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (75 pairs): **median 8.67, p90 22.18** (min 2.12, max 27.94), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.19 %, mean luma 89.

## Checks (every 5th frame at 6 fps + phone_sheet.jpg)
- Qi banners return one by one (set_qi_return 0 -> 1 over g 1886..1952, keyed on every frame); the black Yan pennants vanish as the opaque crimson Qi flags pop. Flags are opaque cloth with no bloom; all halo cards hidden; warm dawn kept.
- Caption band: bright share figure above (target clear). Siege tents dimmed, siege fires hidden.
- Camera: tilt down 45 D (less empty sky), orbit +9 deg/s about the plain, push 0.04/s and push punches every 11 frames (client frame-diff rule).
## Deviations
- 62 + 2 pennants (the set's count; 70+ not reached, set-level). Dawn sky clouds keep the set's flat base (only the dusk sky was repainted).

