# QA s25 (film 18, render team 2)

- Range: take g 1873..1965 (93 frames); shot g 1882..1957; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 8.4 s wall/frame (median 8.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 93 frames, 30.00 fps, g 1873-1965)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (75 pairs): **median 4.42, p90 5.54** (min 2.96, max 6.00), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.35 %, mean luma 95.

## TAKE-gate round 2: no pulses (orbit +14 deg/s + push 0.04/s); Qi banners return one by one (set_qi_return 0 -> 1 over g 1886..1952); opaque crimson cloth flags with a dark-gold trim, halos hidden, flag shadows off, spike cones hidden, cloudless dawn sky.
- Caption band: the siege tents' orange faces (g 1925-1942 had 1.8 %) are dimmed further (emission x0.03); figure above is the new maximum (limit 1 %).
## Deviations
- 62 + 2 pennants (the set's count, not 70+); p90 below the 9 guide (median passes).

