# Reference C: camera, lens and post, with targets for the EP.1 night-rain expressway

Source: `ref/c/ref.mp4` (720x1280, 30 fps, 2048 frames, 68.3 s). Video frame `vNNNN` is 0-based (t = N/30). Still `f_NNN` is `ref/c/frames2/f_NNN.png` (video frame (NNN-1)*15). All pixels are at 720x1280 (W = 720, H = 1280). D = puppet head diameter. Lens values are Blender `lens` in mm with `sensor_width = 36`, `sensor_fit = 'AUTO'`. On a portrait frame the 36 mm lies along the 1280 px side, so `f_px = lens / 36 * 1280` (verify_blender_api row 66).

Scripts and scratch output are in `scratchpad/rcam/`, outside the project: `ncc.py`, `flow.py` (Farneback similarity fit per frame at 180x320, from `spec/refC_cam/small.npy`), `dof2.py` (re-blur defocus estimator, calibrated below), `vp.py` (LSD and RANSAC vanishing points), `mb.py`, contact sheets `cs_*.jpg` (every 6th frame) and `tw1-3.jpg` (every 2nd frame around each transition). I looked at full resolution at f_005, f_012, f_027, f_033, f_040, f_047, f_062, f_067, f_082, f_089, f_102, f_120, video frames v0118, v1170 and v1290, plus 4x crops of the puppet in f_012, the caption in f_102 and the X icons in f_102.

What ref C does differently from refs A and B (`camera_motion.md`, `LOOK_SPEC.md`):
1. The camera behaves like a drone flying through one connected world. Most scene changes are fly-throughs or whips, not cuts or dissolves.
2. Puppets get motion blur with the set during fast moves (v0118, v1290). In refs A and B they stay sharp.
3. There is real optical depth of field, but only in medium close-ups and macro inserts. Wide shots are deep focus.
4. The camera holds still for 1 to 2 s when the viewer must read an icon or graphic.
5. The lens is longer than our 22 mm house lens: a median of about 31-37 mm.

---

## 1. Shot list (setups) and edit grammar

Boundaries come from the frame-to-frame NCC after alignment (`ncc.npy`, drops below 0.6), from the similarity-fit corner speed (`flow.npy`), and from reading `tw1-3.jpg` and `cs_*.jpg`. A "setup" is a stretch with one framing intent. A transition is the move or effect between two setups.

| # | frames | s | setup | angle | move |
|---|---|---|---|---|---|
| 1 | 0-12 | 0.4 | MCU, puppet with hammer | eye (slightly low) | drift, ends on impact star |
| T | 12-22 | 0.3 | impact flash + snap pull-up | | |
| 2 | 22-114 | 3.1 | wide over the tank yard (f_005) | high, pitch about 28 deg down, camera about 17 D up | slow push |
| T | 114-126 | 0.4 | whip right, flies over the fence (v0118) | | continuous, no cut |
| 3 | 126-282 | 5.2 | wide yard with Tiger (f_012) | eye, pitch about 2 deg down, horizon y 603 through the puppet's head | slow track |
| 4 | 282-318 | 1.2 | snap push to MCU at the table | eye | snap |
| 5 | 318-384 | 2.2 | arc out to the tank | eye | arc |
| cut | 384 | | hard cut | | |
| 6 | 384-474 | 3.0 | two-shot over the fence (f_027) | eye, roll at most 1-3 deg | pan, push |
| 7 | 474-506 | 1.1 | MCU, background defocused (f_033) | low-eye | drift |
| T | 506-512 | 0.2 | impact flash + white arcs | | |
| 8 | 512-556 | 1.5 | tanks from above | high | drift |
| T | 556-570 | 0.5 | fly-through whip into the teapot | | continuous |
| 9 | 570-583 | 0.4 | macro insert of the teapot | insert | push |
| T | 583-595 | 0.4 | crash pull-out (f_040) | | continuous |
| 10 | 595-628 | 1.1 | dusk yard | high (mild) | drift |
| T | 628-646 | 0.6 | torn-paper wipe to cream, then a tear reveals the next scene | | |
| 11 | 646-680 | 1.1 | hangar, frontal and symmetric | eye | push |
| 12 | 680-731 | 1.7 | crane down to the wheels, tracking (f_047) | low, insert | track |
| T | 731-738 | 0.2 | whip with a cut hidden in the blur | | |
| 13 | 738-820 | 2.7 | ground-level road behind the gun barrel, measuring tape | low (about 0.5-1 D) | push, then a rush forward at 806-820 |
| 14 | 820-976 | 5.2 | road, tank and puppet (f_062), fires, weather turns over v918-930 inside the shot | high (mild), pitch about 8 deg, camera about 6 D | drift |
| cut | 976-978 | | hard cut | | |
| 15 | 978-1000 | 0.7 | night, rain, lamp (f_067) | high, pitch about 15 deg, camera about 7 D | near static (v985-999) |
| cut | 1000 | | hard cut | | |
| 16 | 1000-1136 | 4.5 | rain, row of tanks | high (mild) | slow drift |
| T | 1136-1150 | 0.5 | torn-paper wipe to white | | |
| 17 | 1150-1180 | 1.0 | tracking a tank in the snow (v1170) | low | fast track, 30-60 px per frame |
| T | 1180-1196 | 0.5 | impact + push | | |
| 18 | 1196-1242 | 1.5 | macro: wheel cracking (f_082) | insert, frontal | static for 30 f (v1204-1234) |
| T | 1242-1244 | 0.1 | white flash cut | | |
| 19 | 1244-1290 | 1.5 | low over the road wheels, puppet (v1290) | low | fast |
| 20 | 1290-1316 | 0.9 | watch insert | insert | static for 14 f |
| T | 1316-1330 | 0.5 | impact zoom with a radial burst (f_089) | | |
| 21 | 1330-1352 | 0.7 | watch open, macro | insert | near static |
| 22 | 1352-1388 | 1.2 | pull out low over the wheels | low | fast |
| 23 | 1388-1434 | 1.5 | MCU, puppet on a tank | eye | drift |
| T | 1434-1446 | 0.4 | impact ring + whip | | |
| 24 | 1446-1470 | 0.8 | tank row | eye/high | drift |
| 25 | 1470-1560 | 3.0 | long-lens row with X and check icons (f_102) | high, pitch about 22 deg, camera about 23 D | drift, then static for 38 f (v1505-1543) |
| T | 1560-1590 | 1.0 | fly-out | | continuous |
| 26 | 1590-1760 | 5.7 | very wide rows of tanks (f_108), yellow streak lines | high (mild), long lens | slow drift |
| 27 | 1760-1874 | 3.8 | tank and puppet, check and ring icons (f_120) | high | drift with near-static runs |
| T | 1874-1890 | 0.5 | fly-around | | continuous |
| 28 | 1890-2048 | 5.3 | final two-shot | eye | static end hold of 59 f (v1906-1965) |

Numbers:
- 28 setups and 16 transitions in 68 s. Framing changes (setups plus transitions) number 41: median 34 frames (1.13 s), mean 1.67 s. Setup holds alone have a median of about 46 frames (1.5 s).
- Transitions: 6 continuous fly-throughs or whips (12-16 frames), 5 impact-flash snaps (6-16 frames), 2 torn-paper wipes (14 and 18 frames), 1 whip with a hidden cut (7 frames), 1 two-frame white-flash cut, and 3 plain hard cuts (around the 0.7 s night insert). **There is no cross-dissolve at all.** The median transition is 14 frames.
- Time by angle: high 42 % (about 29 s), eye 30 % (about 21 s), low 13 % (about 9 s), insert/macro 5 % (about 3.6 s), transitions 9 % (about 6 s). There is no true top-down shot (the steepest is about 28-35 deg, f_005, f_102) and no deliberate Dutch. The vertical-line tilt is 0-1.5 deg in f_012, f_027, f_028, f_033, f_045 and f_128. A drifting wide can roll about 5-6 deg (f_108). In f_074 the 6 deg comes from the slanted rain, not from camera roll.

## 2. Camera motion (from `flow.npy`, all frames)

The corner speed is the same measure as in `camera_motion.md`: |zoom| x 734 + pan, in px/s at 720x1280.

| metric | ref C | ref A / ref B (camera_motion.md) |
|---|---|---|
| corner speed median (IQR) | 231 px/s (68-664) | 332 / 150 |
| snap frames (> 450 px/s) | 37 % | 44 % / 17 % |
| drift frames | 41 % | 44 % / 64 % |
| near static (< 60 px/s) | 22 % | 4 % / 8 % |
| drift zoom rate, median abs (IQR) | 9.0 %/s (5.2-17.1) | 7.8 / 7.6 |
| drift pan, median | 73 px/s | 30-33 |
| drift push-in / pull-out share | 53 % / 42 % | 59/19, 39/45 |

- Fast episodes (corner speed above 40 px per frame, i.e. 1200 px/s): 30 of them, mostly 3-14 frames long. Peak measured speed is 70-130 px per frame (v114-125, v736-747, v1158-1199, v1280-1298, v1363-1374). Farneback at 180x320 under-reads blurred frames, so the true peaks are probably 1.3-1.5 times higher.
- Static holds of 7 frames or more, in frames (v = video frame): 59 (v1906-1965, the end), 38 (v1505-1543, reading the X/check icons), 30 (v1204-1234, the wheel cracking), 14 (v985-999 and v1301-1315), 12, 10, 9, 8, 7, 7.
- Zoom per frame: median 0.43 %, p90 2.7 %, p99 7.3 %. The crash moves run 6-8 % per frame (v812, v1286-1290, v1366-1370).
- Roll per frame: median 0.19 deg, p90 1.4 deg. Rolls appear only inside whips and arcs.

## 3. Field of view and camera height

Vanishing-point pairs (`vp.py`, orthogonal pairs: `f^2 = -(v1-c).(v2-c)`):

| still | f_px | Blender lens (36 mm, AUTO, portrait) | vertical / horizontal FOV |
|---|---|---|---|
| f_067 night high | 794 | 22 mm | 78 / 49 deg |
| f_062 road | 1010 | 28 mm | 65 / 39 deg |
| f_005 yard high | 1113 | 31 mm | 60 / 36 deg |
| f_102 long-lens row | 1317-1453 | 37-41 mm | 52-48 / 31-28 deg |
| f_012 yard eye | 1342 | 38 mm | 51 / 30 deg |

f_011 and f_030 gave unstable pairs and are left out. f_108 and f_120, the very wide rows, look longer still (about 50-70 mm) from the flat stacking of the rows, but this is not measured.

Camera height comes from where the horizon cuts a standing puppet (the horizon passes through points at camera height):

| shot | camera height |
|---|---|
| f_012, eye | about 2.5-3 D |
| f_033, low-eye MCU | about 1.5-2 D |
| v738-820, ground level | about 0.5-1 D |
| f_062 | about 6 D |
| f_067 | about 7 D |
| f_005 | about 17 D |
| f_102 | about 23 D |

Pitch from the horizon row: eye 0-3 deg down, high 8-30 deg down, low 0-10 deg up.

## 4. Depth of field (`dof2.py`)

The estimator is calibrated on f_102: an added Gaussian blur of sigma 0/1/2/3/4/6/8 px reads 0.38/0.80/1.77/2.82/3.92/5.7/7.6. The sky row is excluded because clouds read as soft.

- **Wide shots are deep focus.** In the 60 sampled stills with the camera moving under 8 px per frame, the median share of tiles with sigma above 1.5 px is 4 % (p90 14 %). The share above 3 px is 0 (p90 4 %). The depth cue is haze, not defocus.
- **Medium close-ups blur the background.** In f_033 (low MCU) the Laplacian energy of the background is 0.04 of the puppet's (0.11 after contrast normalisation), with sigma about 2.5-3 px on the brick wall. This is the same as clip B's dialogue close-ups (0.09-0.10).
- **Wide and medium two-shots stay mild.** The background-to-puppet energy ratio is 0.28-0.47 in f_012, f_062, f_067 and f_102.
- **Macro inserts are shallow.** Examples: the teapot (v570-583), the wheels (f_047, rows sigma 2-4 px), the watch (f_089) and the far rows behind the near tank in f_120. The subject plane is sharp (sigma 0.2-0.5) and near or far planes reach sigma 3-8 px.
- Blur in moving frames: the median share of soft tiles is 14 %, and most of it is motion blur, not focus.

## 5. Motion blur and whips

- Whips and crash moves blur the **whole picture, puppets included**. In v0118 the puppet at right is streaked like the set. In v1290 the puppet's face and arm are streaked vertically, about 20-40 px. Captions and icons stay sharp.
- Streak length is about half to two-thirds of the per-frame displacement. Examples: v0118 moves about 35-50 px per frame and streaks about 20-40 px; v1170 tracks at 30-46 px per frame and streaks wheels 15-25 px and near snow about 40 px. This is a shutter of about 0.5 frame (180 deg).
- Whip shape: 7-16 frames, eased in and out, peak 50-130 px per frame (1500-4000 px/s), often combined with a 2-8 % per frame zoom. Fly-through whips are continuous camera paths between sets, never a pan across a cut.
- Impact transitions add a radial burst: a white star and flash for 2-4 frames, thin white arc swooshes with glow (radius 80-130 px) for 8-12 frames, and a radial zoom blur on the set (f_089).

## 6. Vignette, grain, sharpening, codec

- Vignette is weak. On the mean image of all frames, the side edges at mid-height read 0.90-0.95 of the centre and the bottom corners 0.90-1.00 (the top corners are 1.5 because of the sky). Target: -5 to -10 % at the edges, smooth, never a visible ring.
- There is no grain. The high-pass standard deviation in the flattest 16 px blocks is 0.14/255 (median) and 0.23 (p90) over 35 stills.
- There is no sharpening. Edges are soft and codec-smoothed with no halos (4x crop of f_012). The puppet ink is about 4-5 px wide with soft edges. Do not add an unsharp mask.

## 7. Icons and graphics

| icon | look | placement | animation | frames |
|---|---|---|---|---|
| red X | flat `#fb5b62`, about 90 % opaque, no outline, thick rounded strokes | **world-anchored** over each object in perspective. The nearest is 124-136 px (0.18 W); further ones shrink about 12 % per step down the row; they overlap | each pops in over **2 frames** (about 50 % on the first, 100 % on the second, no visible overshoot), one new X every 2-4 frames from near to far, then they slide with the camera (8-20 px per frame) | v1473-1513, f_102 |
| green check | `#24c434` fill, dark green outline about 3 px, 142x120 px | beside the subject at the right of centre (x 512-654, y 562-682). It replaces the nearest X on the same spot | 2-frame pop (92x69 to 140x118), then held | v1514-1570, v1790-1870 |
| measuring tape + label | yellow tape with black ticks lying on the road; "0.9 MILE" label in a yellow box with a black outline | world-anchored on the ground plane in perspective; it extends along the road | extends over about 20 frames, held about 30 | v780-820 |
| ratio counter "10 : 1" | white bold numerals with a shadow, orange "1" | upper left, y about 200-250, above the subject | pops in, held about 3 s | v1536-1570 |
| yellow streak lines | 4-6 thin yellow strokes, like trajectories | screen space, drawn from the lower left corner toward the middle | draw-on over 4-6 frames, held about 50 | v1707-1760 |
| white arc / ring | thin white arc with a soft glow, radius 80-130 px | around the object being hit or dropped | sweeps for 6-12 frames | v506-512, v744-760, v1434-1446, v1770, v1824-1870 |
| impact star | white jagged burst with an ink outline, 150-250 px | at the point of contact | 2-4 frames | v12-18, v506, v744, v1178, v1326 |

Graphic events come about every 4.5 s (about 15 in 68 s). Two can overlap only in the climaxes (X plus check plus counter). Icons never sit on the caption band. The channel watermark ("SEGMENT ZERO") is not ours and must not be copied.

## 8. Captions

The ref C captions are the same house style as `captions.md`. White heavy geometric sans (Work Sans Black is fine), black outline about 4 px with a soft halo, lower case as spoken. Measured over 133 stills: the text block runs from y 871 to 917 (centre y 892, 0.697 H), cap height about 36 px, centred on x = 360, median width about 230 px. Each caption is 1-3 words; the median change interval is 11 frames (0.37 s, p10 6, p90 16). There is no caption animation.

---

## 9. Targets for EP.1 (Bangkok expressway, night, heavy rain, gridlock, Kong with the rescue cutter)

| item | target |
|---|---|
| lens | Default **32 mm** (f 1138 px, 59 deg vertical / 35 deg horizontal). 22-24 mm only at ground level, inside a car or a cramped POV. 40-60 mm for the long-lens high angles that stack the gridlock rows (compression like f_102 / f_108) and for macro inserts (cutter jaws, battery bars, phone). |
| heights (1 BU = 1 D) | Eye 2.5-3 D with pitch 0-3 deg. Low 0.5-1.5 D pitched up 5-10 deg (Kong acting, the cutter). High 6-25 D pitched down 8-30 deg (gridlock scale, red beacons over the rows). Top-down only for the ending rise; ref C never goes past about 35 deg. |
| angle budget for a 55 s episode | about 40 % high, 30 % eye, 15 % low, 5-8 % insert/macro, 8-10 % transitions. Dutch: at most 3 deg of drift roll, except where the brief asks for 8-15 deg once the horror begins. |
| setup length | median 1.3-1.6 s; a framing change about every 1.1-1.7 s |
| transitions | Fly-through whips and impact snaps, 7-16 frames. At most 2 torn-paper or white-flash wipes per episode. Hard cuts for time jumps (like the 0.7 s night insert). No dissolves if we follow ref C. |
| drift | zoom 5-17 %/s (median 9), pan about 70 px/s, push-ins and pull-outs about evenly mixed |
| snap / whip | peak 1500-4000 px/s at the frame corner, 2-8 % zoom per frame, eased (`SINE` or `QUINT` in-out) |
| holds | Allow static holds of 30-60 frames only to read an icon (battery bars, missed-call badge, stopwatch) and for the last shot. Otherwise never static for more than 14 frames. |
| depth of field | Wides: deep focus, background sigma ≤ 1 px; depth comes from rain haze and fog. Kong MCU, low angle: background sigma 2.5-3.5 px at 720 w, background/puppet Laplacian ratio 0.04-0.11. Macro inserts: sharp subject plane, fore and back sigma 4-8 px (wet asphalt and beacons go to round bokeh). House rule (verify_blender_api row 70): no Cycles DoF. Use compositor Defocus from the Z pass, or the plate-blur method of `color_light_post.md`; if Cycles DoF is tried with the denoiser, prove the noise at 360x640 first. |
| motion blur | Shutter 0.5 frame on fast frames (corner speed above 40 px per frame). In ref C the puppets blur with the set: Cycles motion blur on the camera only, with the cards streaking, is correct for this look. Keep faces sharp on holds and drifts (do not animate cards faster than about 40 px per frame outside whips). Rain streaks should be motion-blurred lines (refC_light.md). |
| vignette | -5 to -10 % at the edges (compositor Ellipse Mask, feather about 0.5, multiply 0.92), no ring |
| grain / sharpening | none |
| icons | Emission-only cards **anchored in the 3D world** wherever they label an object: X over wrecked cars, a check on the passable lane, battery bars by the cutter, a red pupil over the driver. A metric label in the style of the "0.9 MILE" tape fits for distances, e.g. "1.2 KM to the ramp" laid on the asphalt. Screen-space only for rules: the 60 s stopwatch and the counter. Pop in **2 frames** (50 % then 100 %; a 4-frame 0 to 115 to 100 % overshoot as in the brief is acceptable but slower than ref C). Stagger a series 2-4 frames apart, near to far. Size 0.12-0.2 W for the nearest icon. Flat fill at 90 % opacity; red `#e2453b` (ref `#fb5b62`) and green check with a dark outline. About one every 4-6 s. |
| captions | centre y 892-900, cap height 36 px, 1-3 words, about 0.37 s per chunk, kept clear of icons and of heads (whole heads above y 880) |
