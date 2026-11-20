# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 10.5 s wall/frame (median 10.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO FAIL  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 8.91, p90 10.78** (min 1.32, max 12.70), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 3.76 %, mean luma 76.

## BIGZOOM ending, round 14b (client §H / §I; set film18/main 70c8a11) - measured on rendered pixels
- Move: ONE continuous eased crane-down + swing round in front of him (cylindrical interpolation about the general: azimuth 51 -> -83 deg, radius 38 -> 4.9 D, lens 34 -> 24), join to the old tracking pull at g 2066, held +19 % push from g 2068. No cut, no pulsing.
- General height: g 1958 **2.2 %** (< 5 %), g 2066 **44.8 %** (35-60 %), g 2111 54.0 %; head top y 328+ for g >= 2066. Ox mouth max y **821** (g >= 2080, <= 860). Frame diff median **9.0**, p90 11.1.
## TAKE gate 18 fix: ROOT CAUSE of the flat tan / mauve rectangles on the wall base (g 2021-2092)
- Not set geometry: hiding objects one by one showed the patch was tied to each ox card + its rim copy; the same patch appears with the denoiser OFF as a flat noise-free rectangle. Cause: the scene's `transparent_max_bounces` was 8; where several transparent card quads (4 oxen x card + rim, smoke spheres, plaque) overlap, rays ran out of transparent bounces and returned a flat colour in a rectangle. Fix in shot.py: `transparent_max_bounces = 64`. Verified at g 2033, 2045, 2085 (before / after) and on a 6-frame full-size strip of the wall base (g 2020, 2031, 2038, 2044, 2080, 2090): no flat patch. (`halos`, `wallpools`, `cityglow`, `tw_glow`, `posts` stay hidden: those were separate real glitches.)
- Framing: the general moved 0.18 D to screen-left (about 30 px) so his back is no longer clipped by the right edge at g 2078-2090.
## TAKE gate 17b fix (QA-art flat patches on the wall base g 2021-2058)
- Raycast from the camera at g 2038 through the patch pixels hit the set's `halos` mesh (JM_jimo_out_DAWN halo / halo_s / mist cards on the wall; hit points on the wall at y -16, z 8-10). `halos` is hidden for the whole take (with `wallpools`, `cityglow`, `tw_glow`, `posts`). Checked full-size crops of the wall base at g 2025, 2031, 2038, 2045, 2054: the flat beige boxes are gone (the wall brick shows). I did not re-run QA-art's per-frame blob detector (my own crude flat-pixel count also counts the road and is not meaningful); frames 2015-2062 were not all inspected at full size, only those five.
- Field warmth g 1985-2005: grade strengthened (saturation x1.7, warm gain 1.14/1.0/0.80 on the lower frame).
## TAKE gate 17 fix
- The dark-purple hexagonal prism at g 2020-2032 bottom: found by raycast from the camera at g 2026 through the prism's pixels (about x 350-570, y 1155-1280 in my frame; the director's pixel box did not hit it, it hit the ground): it is the set's `posts` mesh (bridge / road posts, hit point (9.8,-69.1,z 1.0)). `posts` is hidden for the whole take. Checked full size at g 2015, 2020, 2024, 2028, 2032, 2035: gone (only a small pot edge at the right edge of g 2032).
## TAKE gate 16 fixes (earlier render)
- **Pale translucent rectangles g 2020-2058: FIXED.** Found by hiding objects one at a time: they were the set's translucent glow quads on the city wall (`wallpools`, `cityglow`, `tw_glow`; now hidden for this take) plus the smoke cards (SVG blur filter clipped into a pale rectangle). The tail smoke is now small translucent 3D spheres (no card, no filter) and the rim copy of the oxen has no smoke. Checked at full size g 2025, 2034, 2050.
- Ground (director's ground_share.py take.mkv 1950 1958 2112 2): **max 0.296, median 0.23** (was 0.31-0.34 at g 2006-2012): ~420 warm field props (hay, baskets, pots, stones) scattered over the plain at both sides of the road.
- The dark block sliding through the bottom at g 2020-2030: it was the set's near wall-base / dressing seen over the crane; after the dressing change I saw no untextured block in the 6-frame checks, but did not check every frame.
## Round 14b fixes
1. Unsharp: no longer 330 %. Raw renders get radius 1.0, 150 % on g 1950-2061 only (moire / halos gone; raw frames are in raw_frames/, not committed).
2. Findability: the start camera is (30,60,62) looking (0,-75,-10), and the general starts 7.5 D to screen-right of the road line (blended back to the centre by g 2038), so he stands about 90 px clear of the gate banner from g 1958. His dawn pool is a double stacked warm quad (outer k 17, inner 0.55 k), lit from the first frame.
3. Rim: now a flat emissive silhouette copy (pale sky-blue 0.55 0.78 1.0, strength 1.7, 2.8 % larger, 0.05 D behind) instead of a tinted copy of the dark ink: it reads as a pale blue-white outline on the general and the oxen.
4. Wide-field colour (g 1958-2030): rendered frames get a saturation boost (up to x1.55) and a warm / brighter gain on the lower 60 % of the frame, ramped out by g 2030.
- Kept: 即墨 plaque on the gate (readable at the start), scream + fist-gripped cup, helmet wobble, cup slosh, look-back g 2070-2080, rage oxen, smoke on tails, helmet prop from g 2046.
## NOT MET
- **qa_auto reports FAIL: "suspected blur on 60 frames" (g 1950-~2010, the extreme wide)**. The director said soft wide frames are acceptable; I could not pass qa_auto's Laplacian test without a >= 330 % unsharp (which QA-tech rejected). The rest of qa_auto passes (no black / blank / magenta / frozen frames).
- p90 10.6 (guide 9: pass). Caption-band bright share and the saturation / luma numbers of the wide fields were not re-measured.
- take.mkv is crf 11 (51 MB) to stay under GitHub's 100 MB file limit.

