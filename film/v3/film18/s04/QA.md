# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 19.9 s wall/frame (median 18.2); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 8.16, p90 18.75** (min 2.07, max 20.18), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.07 %, mean luma 71.

## Checks (every 5th frame at 6 fps + phone_sheet.jpg)
- Director note: the giant flat orange flag quad is now an opaque crimson cloth flag (own diffuse material, flag scaled to 0.5 about its pole foot); ALL halo cards are hidden, so there is no bloom and no blown glow stalk; Jimo reads lit through its windows and gate fires.
- Caption band: bright share (luma > 200) is the figure above (target <= 1 %); sun-lit tent faces of the siege camp were dimmed (emission x0.1) and the siege fires hidden.
- Camera: orbit about Jimo (-9 deg/s) + steady push 0.08/s + push punches every 13 frames (one on "จี๋โม่", g 354) so the push-in to Jimo reads and Jimo stays framed (the first try slid past Jimo).
## Deviations / NOT MET
- **Ju is NOT visibly lit.** From this camera Ju (far, 500 D, behind nearer towns / the horizon haze) does not appear in the frame at all (a beacon tower with a live flame at Ju was tried and never showed). Needs a set change (a second lit town in view) or a camera that frames Ju.
- Plan says "same take, snap" from s03; the s03 camera does not continue into s04, so this take is delivered as a CUT in (meta transition_in cut), 2 in-handle frames.
- Camera is more active than the plan's 7 %/s (client frame-diff rule).

