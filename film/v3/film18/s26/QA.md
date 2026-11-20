# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 13.7 s wall/frame (median 14.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 6.21, p90 7.69** (min 2.07, max 9.11), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 60.

## Round 6 fixes
- Camera look-at raised (z 3.0) so more of the road is dressed and less is plain; the dark silk strips are gone; warm period props (R2.dress: stones, haystacks, baskets, pots) on both verges, none in the lane. ground_share 0.15-0.18.
- Open scream mouth under the moustache (open 0.44 x 0.36), round eyes, brows up, sweat drops (fx sweat); forward lean 21; profile look-back g 2070-2080.
- The four oxen use the new cast18 face='rage'; the nearest drifts 3.4 D to screen-right from g 2040 so its face shows at his shoulder at the cut. Held +19 % push from g 2068.
## Not met
- The cup is still the cast's gold ewer (jue prop) held on a red sleeve: no separately drawn hand (the cast draws the prop over the fist). The sweat drops are the cast's small fx.
- J.dress_ground placed 0 props here (the 2.5 D keep-clear of the road/actor boxes covers the whole lane), so the verge dressing uses jimo_r2.dress instead.

