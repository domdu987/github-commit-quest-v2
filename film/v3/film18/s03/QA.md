# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 15.2 s wall/frame (median 16.1); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 5.96, p90 10.72** (min 2.74, max 12.65), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 93.

## Checks (every 5th frame at 6 fps + phone_sheet.jpg)
- Pennants pop one by one (set_pennants 0 -> 1 keyed on every frame over g 223..294 = 7.32 s on); Jimo's Qi flag is an opaque cloth flag, no bloom; all halo cards hidden; siege tents dimmed and siege fires hidden so the caption band stays clear (figure above).
- Clouds: dusk sky repainted at runtime (sky_fix.png) so the cloud base is a rounded underside, no flat bar / skewer.
- Camera: tilted 45 D down (less empty sky), orbit -13 deg/s about the plain, push -0.04/s (to keep the lens out of the flag forest), push punches every 10 frames.
## Deviations
- **p90 of the frame diff is below the 12 target** (median passes): an earlier, stronger setting flew the lens into the flag forest, so I traded p90 for a clean frame.
- Out handle only 2 frames (s04 is a cut).

