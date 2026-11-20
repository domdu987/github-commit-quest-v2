# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 9.9 s wall/frame (median 10.7); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 5.74, p90 7.24** (min 2.24, max 8.19), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 70.

## Round 11 (set film18/main 08dc7e0)
1. The nearest ox's mouth is now above y 860 for g 2080-2111 (measured on rendered pixels with a drawn line at 860: the mouth sits at about y 815-820 in the g 2085 frame; at g 2111 the ox is at the right frame edge with its head clear of the caption band). Done by moving that ox 0.0-2.4 D back (OX_END 5.0 D behind him) and 0.6 D less to screen-right (it ends 2.0 D right of his path). The camera was NOT raised.
2. A dropped bronze helmet (J.prop_helmet, scale 0.5) lies low in the bottom-left corner for the whole take; J.ground_share 0.21-0.23 (was 0.15-0.18 by the same tool earlier, and the director measures plain dirt differently).
## Deviations
- p90 7.2 (< 9 guide). My earlier "chin 757" meta used a head-box, not the ox's drawn mouth; this round measures rendered pixels.

