# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 15.5 s wall/frame (median 13.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 4.48, p90 5.52** (min 3.29, max 6.53), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.51 %, mean luma 83.

## Round 6
- The red-brown lance (the fg cart's wood) is hidden; the dusk cloud stickers are removed (cloudless gradient); ground_share is low (moat water + bank); 9 wall folk, envoy 4.2 D in frame to the end. No whip wiggles.
## Deviations
- The envoy is still partly behind the bridge rail posts in the middle frames; p90 below the 9 guide.

