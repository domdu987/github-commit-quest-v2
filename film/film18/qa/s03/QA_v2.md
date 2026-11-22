# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 9.3 s wall/frame (median 8.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 5.58, p90 6.30** (min 0.76, max 6.77), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.51 %, mean luma 90.

> Set version: Vista round 4 (set3d18 from film18/main 08dc7e0).
## Round 11
- From g 238 the camera eases UP and BACK (to (-100,-125,190)); the last frames show 25+ small flags over the towns: the pennants pop near-to-far with J.vista_pennant_order / J.set_pennant_scale, the 6 nearest stay down (no diagonal pole in the bottom third / on the edges), near ones k 0.32, middle 0.7, far 1.0.
- Navy ramp / plank / pole-base strips: the town road ribbon's navy (vroad faces within 33 D of Jimo removed, c18.vista_yard_fix) and the yellow-cube lump: the set's haystack props were scaled by the camera; the take no longer passes over that spot closely.
## Deviations
- The vista's far-hill haystack lumps still appear as yellow blobs; the ramp / plank strips in the west towns (set objects) are not individually hidden. p90 below 9 guide.


## V2 fix (client: "objects float / camera shakes") - 2026-11-22, render team 5
Base: s03 round 11 (render18/team2 f0aa6b46f) rendered with film18/main's set3d18 (f7be8e4, the vista code of v1; render18/team5's own set3d18 is older for jimo_vista*). Camera: the same single eased dolly + truck (no sway).
- **Fix**: the flat white discs and brown ovals hovering over the field at 0:06 (g162-200) are the Yan siege tents (GN instances `r3_tent` / `r3_tent_b`, canvas domes with no ground contact): removed from this shot, together with nothing else; their small flags are the standing pennant poles, all of which now rest on the terrain (14 poles, up to 0.24 D too high, lowered with their cloth: `pole_shifts.json`, measured with ground_check at g296).
- **ground_check** (`gchk.py`, v3/tools/ground_check.py, every 10th frame g156-296, gap tolerance 0.05 D, pennant poles `pen_*`): **exit 0 / PASS** - 47 objects, 243 rows, 0 FAIL (GROUND.md). Instanced set props (`r3_*`: carts, huts, hay) are Geometry-Nodes point clouds and cannot be ray-checked per object; they are excluded (carts sit on the road with +0.2 lift in the set code).
- **qa_jitter.py take.mkv**: no "shake" line, overall median jitter 0.23 px.
- Frame-diff in-shot (n=140): median **5.41**, p90 6.46. qa_auto PASS. Encoded crf 20 (take 9.6 MB). `scene.cycles.transparent_max_bounces = 64`.
- Process note: the first frame rendered by every Blender process shows a stale camera (grid view); the first frames of each render chunk (g147, 185, 223, 261) were re-rendered behind a sacrificial frame, so the take has none.
