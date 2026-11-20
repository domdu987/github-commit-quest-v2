# QA s25 (film 18, render team 2)

> Set version: vista round 3 (set3d18 from film18/main >= 06c0207, J.vista_r3 applied by J.build); cloud base bars: clouds removed (cloudless gradient); s04 Jimo flag scaled to 50 %.

- Range: take g 1873..1965 (93 frames); shot g 1882..1957; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 10.0 s wall/frame (median 7.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 93 frames, 30.00 fps, g 1873-1965)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (75 pairs): **median 5.28, p90 5.45** (min 4.56, max 5.61), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 90.

## Round 7 (vista round 3)
- Set's round-3 farmland and dawn light; no navy slabs; Qi banners return one by one (set_qi_return 0 -> 1, g 1886..1952), opaque crimson cloth flags; the siege tents are now the set's smooth ones; dawn cloud stickers gone (cloudless gradient); Jimo-side halos and glints off.
- No pulses: orbit +14 deg/s + push 0.04/s with the tilt.
## Deviations
- 62 + 2 pennants (set count); p90 under the 9 guide.

