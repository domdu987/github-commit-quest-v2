# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 13.3 s wall/frame (median 13.5); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 11.91, p90 14.64** (min 3.08, max 15.08), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.03 %, mean luma 68.

## Re-done for the TAKE gate: no pulses
- The take now CONTINUES the s03 camera (starts where s03 ends: (-95,15,70) looking at Ju's beacon) and makes one eased dolly + pan to Jimo, with ONE held punch-in (+16 %) on "จี๋โม่" (g ~352) held to the end.
- **Ju is visible and lit** in the first ~1.5 s: a Qi flag (opaque cloth, x3.2) over a beacon tower with a live flame, top left of frame (a stand-in tower on Ju's spot, because the set's own Ju is lost in the haze at 500 D). Jimo reads lit (windows, ground pool) and fills the frame at the end.
- Flag is opaque, all halo cards hidden, no bloom; caption band bright share max 0.03 % (target <= 1 %); siege tents dimmed further.
- Because the camera continues s03, this take could also be a plain cut (meta says cut; the director decides).

