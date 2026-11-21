# Production forensics: how the two reference clips were made

Lens: production forensics. Clip A = "Why Perfect Railroads Don't Work", clip B = "The Ancient Jar That Warned an Empire".
All frame numbers `fNNN` are 0-based decode indices of the 30 fps source (`t = f / 30`); `tSS.S` are the half-second JPEGs.
Evidence images: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/ref/crops/production-forensics/` (called `CROPS/` below).
Measurement scripts: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/ref/extra/production-forensics/work/` (`cuts.py`, `planar.py`, `rigid.py`, `klt.py`, `patch.py`, `static.py`, `wm.py`).

Frames looked at: about 30 opened at full 720x1280, all 130 one-per-second frames as contact sheets, and roughly 700 more as thumbnails inside consecutive-frame strips.

## Verdict

**Both clips are conventionally rendered: deterministic 3D scenes with unlit toon puppet characters, cut together in an editor. They are not AI video generation. Confidence 88 %.**
Remaining probability: about 7 % that some shots are AI video, about 5 % other (for example hand 2D animation over painted plates in parts of clip B).

The earlier claim "real 3D renders, not AI" survives testing for the *video frames*, with two corrections:

1. It is a 2D/3D hybrid, not pure 3D. Characters are flat, unlit, outlined puppets whose faces switch between discrete drawn states. Clip B also contains shots that are flat 2D artwork with a pan/zoom (no parallax at all).
2. "Not AI" is only established for the video itself. Whether individual *assets* (clip B's illustrated plates, the frog and dragon meshes, the scene code) were made with generative tools cannot be decided from pixels. Nothing observed requires it.

### Three strongest pieces of evidence for the verdict

1. **Typeset text that carries correct real-world data and never changes.** The wall calendar at f1090 reads "CALENDAR for the Year 1880 / MAY" with a day grid that is right for May 1880: the 1 sits under Saturday, rows run 2-8, 9-15, 16-22, 23-29, 30-31 (`CROPS/a_f1090_calendar_x4.jpg`; 1 May 1880 was a Saturday, 31 days). The newspaper at f975 reads "The Red Mesa Herald / THE CLICKETY CLACK LINE!" above a locomotive drawn from plain rectangles, circles and hatch lines (`CROPS/a_f975_newspaper_x4.jpg`). Across 30 consecutive frames (f960-f989), while the paper grows from 0.50x to 1.21x area, one homography explains it with 0.51 px median reprojection error and the rectified crops correlate at 0.957 median (`CROPS/a_newspaper_rectified.jpg`).
2. **Sub-pixel rigid multi-view geometry and a persistent world.** In the jar orbit (B f262-f291) 461 points triangulated from the first and last frame reproject into all 30 frames with 0.48 px mean RMS while moving a median 245 px; the scene is truly 3D (fundamental-matrix inliers 0.82, homography inliers 0.22). The canyon shot (A f160-f189) gives 0.77 px on 294 points. The same crate with thermometer and calendar is a macro insert at f1088 and a 40 px prop in the same continuous take at f1110-f1146 (`CROPS/a_calendar_flip_strip.jpg`), and its calendar reads JULY in the later shot at f1380.
3. **Characters behave like assets, not like generated pixels.** Head fill is `#fdf7f7` in three different shots (A t02.0, t16.0, t46.0), the boss vest is `#c89e2d`, `#c59b2c`, `#c79f2d`, `#cea32f` in four shots including an interior. The cap's stripe pattern is identical in 25 consecutive frames (f1659-f1683, `CROPS/ecc_cap_chalk_view.jpg`), the shirt shows 2 buttons in 19 of 19 frames where both are in the crop (f1660-f1678). Face features are replaced whole from one frame to the next (`CROPS/a_hero_face_consecutive_f1640_1699.jpg`), and at f605 the purple colour appears to leave the boss's head as a straight horizontal level, which is how an animated mask behaves (`CROPS/a_take_f405_655_strip.jpg`, thumbnail size only).

### Three strongest pieces of evidence against it (for AI video, or that keep it open)

1. **Two takes in clip A are exactly 8.0 s long.** Edge to edge they measure 241 frames (f112-f353) and 239 frames (f1082-f1320), and no take in either clip is longer than 8.33 s. Eight seconds is a common fixed clip length for video generators. This is weakened by the third long take, which is 250 frames (f405-f655) and verified continuous, by the fast fly-through inside the 241-frame take, and by clip B, where no shot is near a multiple of 4, 5, 8 or 10 s.
2. **Metadata proves nothing either way.** Both files are YouTube re-encodes remuxed by ffmpeg (`handler_name` "ISO Media file produced by Google Inc.", `encoder` Lavf59.27.100, fragmented MP4). Any generator tag or C2PA manifest would have been removed. No visible watermark exists, but invisible watermarks cannot be tested here.
3. **Clip B's assets look like what image and image-to-3D generators produce.** The army courtyard has thousands of soldiers that are similar but not pixel-identical (neighbour correlation 0.63-0.84 at 24-26 px spacing, `CROPS/b_f450_instancing_peaks.jpg`), the frogs are lumpy grey meshes, and text below about 10 px cap height is unreadable at 720p so garbling cannot be excluded there. One text is mirror-reversed (chalk "39 FT", f1380). This points at possible generated *assets* inside a 3D pipeline, not at generated video.

## Observations

### 1. Temporal stability of fine detail (consecutive 30 fps frames)

| Target | Frames | Result |
|---|---|---|
| Newspaper masthead, headline, drawing (A) | f960-f989, 30 frames | homography inlier ratio 0.86, reprojection RMS median 0.51 px (max 0.66), rectified NCC median 0.957, min 0.797 at the motion-blurred end; glyphs identical in every tile |
| Wall calendar (A) | f1086-f1097, 12 frames | RMS median 0.79 px, NCC median 0.957 while area scale goes 0.43-1.48 |
| Thermometer scale (A) | f1086-f1097 | RMS 0.72 px, NCC median 0.988, min 0.972 |
| Banner "FIRST LINE IN / GETS IT ALL!" (A) | f318-f347, 30 frames | tracked through a push-in from 0.44x to 1.06x; NCC median 0.919; letterforms identical once the motion blur clears (`CROPS/ecc_banner_view.jpg`) |
| Chalk "39 FT" on a tie (A) | f1366-f1395, 30 frames | strokes identical in all 30 tiles; NCC median 0.881 (low values come from perspective drift of the affine fit, not from shape change) |
| Hero cap stripes (A) | f1659-f1683, 25 frames | pattern identical in all tiles; NCC median 0.882 |
| Hero shirt, buttons, braces (A) | f1652-f1683, 32 frames | NCC median 0.979; 2 buttons detected in f1660-f1678 |
| City gate facade, crest, arrow slits (B) | f815-f844, 30 frames | RMS 0.53 px, NCC median 0.970, min 0.932 |
| Army crowd (B) | f425-f454, 30 frames | behaves as one rigid plane: RMS 0.59 px; soldiers do not change, only helmet glints twinkle (`CROPS/b_crowd_plate_sel.jpg`) |

No glyph, stripe, button or crowd member was seen to morph, merge, appear or disappear in any run.

### 2. Cross-shot consistency of character design

- Hero (A): 12 white cap stripes on the mid scanline at t02.0 and t46.0; 2 white two-hole buttons, 2 braces with dashed stitching and gold buckles, chest pocket on the viewer's left, red bandana with white dots at t02.0, t46.0 and t55.0 (`CROPS/a_hero_torsos.jpg`). Shirt colour `#38a493`, `#36c0a9`, `#35ab99`, `#36ac97` at t02.0, t21.0, t46.0, t55.0.
- Boss (A): gold vest with a watch chain from the second button to the pocket, two pocket flaps on the viewer's left, bow tie, at t16.0, t18.0, t46.0 (`CROPS/a_boss_vests.jpg`). Button and chain-link counts could not be measured reliably (caption overlap, 3/4 view); the chain has roughly 12-13 links in each.
- Head fill is one constant colour with a luma spread of 23-24 levels in clip A and 9 levels in clip B (t00.0). Characters are not lit by the scene in clip A. In clip B the inventor's robe varies more (`#2f4386`, `#475ea2`, `#232d50`, `#37427d` at t00.0, t04.0, t18.5, t44.5), so those shots are lit or graded per shot.
- Hats change with viewpoint as solid objects do: the bowler is seen from above with a full brim ellipse at f435-f465 and side-on at f475. This favours 3D proxy bodies with unlit shading over flat sprites, but the two cannot be fully separated.

### 3. Mirrored, garbled or nonsense text

- Legible and correct: "The Red Mesa Herald", "THE CLICKETY CLACK LINE!", "CALENDAR for the Year 1880", "MAY" with the correct grid, "FIRST LINE IN GETS IT ALL!", "UNION" (f335), "RED CANYON SHORT LINE" (f861), "R.C.S.L" on the crate lid (matches the car lettering).
- Mirrored: the chalk mark at f1380 is an exact mirror image of "39 FT" (39 ft is the standard US rail length). The crate-lid "R.C.S.L" in the same shot also only reads after a flip, while the hero's pocket stays on its usual side, so the frame was not flipped in the edit. A clean geometric mirror of meaningful text is a flipped-UV or back-face symptom.
- Garbled: none found. Sub-headline and body text are too small to read at 720p (cap height under about 6 px), so this is undetermined for small text.

### 4. Impossible geometry, merging, limb errors, texture swimming

None found. The canyon wall shows straight-edged triangular facets and stretched strata texture that hold still from frame to frame (`CROPS/a_t41_lowpoly_wall.jpg`). Gravel is a cell pattern with dark borders and one flat colour per cell. The explosion (f1928-f1940) and the palace dust plume (B f1400-f1456) are layered effects over an unchanged background.

### 5. Shot lengths and transitions

Clip A, 14 shots, seconds: 3.73, 7.92, 1.93, 8.18, 4.55, 2.18, 2.77, 4.88, 7.88, 3.93, 6.48, 4.98, 3.57, 2.17. Mean 4.65, median 4.24.
Clip B, 19 shots, seconds: 3.07, 4.42, 6.03, 4.38, 2.53, 2.13, 1.57, 2.73, 2.87, 2.10, 1.28, 4.12, 3.27, 5.55, 2.68, 6.75, 2.87, 3.38, 3.10. Mean 3.41, median 3.07.

- Clip A transitions: 11 cross-dissolves of 5-9 frames, 1 object wipe (the locomotive fills the frame at f107-f111), 1 hard cut (f1321, a single-frame change in the difference metric; not inspected visually). The last shot also contains a white flash into the explosion (f1928-f1932).
- Clip B transitions: 17 cross-dissolves, mostly 4-8 frames and one of about 16 frames (f1455-f1470), and 1 hard cut (f92).
- Inside a shot the camera re-frames instead of cutting: whip pans at B f159-f164 and A f638-f645, a fly-through at A f296-f317, a push through a carriage window at A f801-f813, a dive into the frog's mouth at B f600-f610.
- Clustering test: shots within 0.15 s of a multiple of 8 s are 2 of 14 in clip A and 0 of 19 in clip B; of 5 s, 2 of 14 and 0 of 19.

### 6. Container and stream metadata

| | Clip A | Clip B |
|---|---|---|
| Video | H.264 High, 720x1280, 30 fps, 1.97 Mbit/s, 65.17 s | H.264 Main, 720x1280, 30 fps, 1.14 Mbit/s, 64.83 s |
| Audio | AAC LC 44.1 kHz stereo 128 kbit/s | same |
| Tags | handler "ISO Media file produced by Google Inc.", encoder Lavf59.27.100, fragmented MP4 | same, plus an x264 core 165 SEI string |
| Generator, C2PA, JUMBF strings | none | none (one 3-byte "veo" hit inside compressed data, expected by chance in 10 MB) |
| Static overlay | none: the only persistent structure in the mean-Laplacian map is the caption band at y 906 (`CROPS/wm_meanlap_boosted_ab.png`) | same |

Frame cadence is native 30 fps: only 2 of 1954 (A) and 1 of 1944 (B) frames are isolated near-duplicates, so there is no 24-to-30 pulldown and no animation "on twos".

### 7. Camera movement and parallax

- The camera almost never rests. Median share of pixels unchanged between consecutive frames is 0.40 (A) and 0.45 (B). Only two runs of 8 or more frames per clip have over 85 % static pixels (A f1240-f1251, f1665-f1673; B f933-f949, f1756-f1774).
- Parallax is physically consistent wherever there is depth (table below). Some clip B shots have no parallax at all and are flat artwork moved in 2D: the underground cross-section (homography inliers 0.96) and the morning wide (0.98).
- Fast moves are motion-blurred (A f296-f303, f313-f316). The stair-stepped look in those frames is aligned to the 16 px codec block grid (edge energy at x mod 16 = 0 is 1.7-2.1x uniform, against 1.13 in a sharp control frame), so it is compression, and the blur method cannot be inferred from it.
- Clip B uses shallow depth of field: blurred background behind the dragon at t01.0, blurred foreground banner at f410-f422.

## Measurements

| Name | Value | Evidence frame |
|---|---|---|
| Frame size, rate | 720x1280, 30 fps, native cadence | ffprobe; whole clips |
| Clip length | A 1955 frames (65.17 s), B 1945 frames (64.83 s) | whole clips |
| Shot count | A 14, B 19 | whole clips |
| Shot length median / max | A 4.24 s / 8.18 s, B 3.07 s / 6.75 s | whole clips |
| Cross-dissolve length | 5-9 frames (0.17-0.30 s) | A f346-f353, f851-f859; B f889-f895 |
| Newspaper planar fit | RMS 0.51 px, NCC 0.957 over 30 frames | A f960-f989 |
| Calendar planar fit | RMS 0.79 px, NCC 0.957 over 12 frames | A f1086-f1097 |
| Jar orbit rigid fit | 0.48 px mean RMS, 461 points, 30 frames | B f262-f291 |
| Canyon rigid fit | 0.77 px mean RMS, 294 points, 30 frames | A f160-f189 |
| Jar orbit F vs H inliers | 0.82 vs 0.22 (true 3D) | B f240-f300 |
| Underground cross-section F vs H | 0.99 vs 0.96 (flat 2D) | B f1860-f1939 |
| Feature speed, jar orbit | 47 px per 6 frames (about 8 px/frame) | B f240-f300 |
| Feature speed, boss take | 66 px per 6 frames (about 11 px/frame) | A f415-f644 |
| Feature speed, slow push at gate | 11.5 px per 6 frames (about 2 px/frame) | B f815-f884 |
| Pixels unchanged frame to frame | median 0.40 (A), 0.45 (B) | whole clips |
| Head fill colour | `#fdf7f7` (A), `#f6fafd` (B) | A t02.0, t16.0, t46.0; B t00.0 |
| Head fill luma spread p5-p95 | 23-24 levels (A), 9 (B) | same |
| Outline ink colour | `#3e2934`, `#3c2933` (A), `#4d3d44` (B) | A t02.0, t46.0; B t00.0 |
| Outline width / head diameter | 0.057, 0.051, 0.045, 0.042 | A t02.0, t16.0, t46.0, t55.0 |
| Outline width in pixels | 8.5 px at 148 px head; 12.9 px at 284 px head | A t02.0, t46.0 |
| Hero shirt | `#38a493`, `#36c0a9`, `#35ab99`, `#36ac97` | A t02.0, t21.0, t46.0, t55.0 |
| Boss vest | `#c89e2d`, `#c59b2c`, `#c79f2d`, `#cea32f` | A t16.0, t18.0, t46.0, t35.0 |
| Banner lettering | navy `#071147`, red `#530c32`, cap height about 80 px of 720 | A f335 |
| Calendar | header `#c82928`, page `#faf3f1`, month `#db5d66` | A f1090 |
| Newspaper | paper `#fdefd7`, ink `#937c5e` | A f975 |
| Blink | eyes closed 1-2 frames with a half-open frame beside it; closures at f1645, f1653, f1671 | A f1640-f1699 |
| Mean saturation | 0.48 (A), 0.41 (B), 0.29 (v1) | 65 frames per clip; v1 frames 20, 45 |
| Mean luma | 0.45 (A), 0.44 (B), 0.65 (v1) | same |
| Canny edge-pixel share | 0.060 (A), 0.068 (B), 0.017 (v1) | same |
| v1 outline / head diameter | 0.018, 0.021 | v1_frame20.png |
| v1 head fill luma spread | 91 and 69 levels | v1_frame20.png |

## How to reproduce

The reference is the same kind of pipeline as ours: geometry and textures built from data, typeset text, a virtual camera. The values below are what to copy.

**Format and edit**
- Render 30 fps, not 24. 1950 frames for 65 s.
- Plan 14-19 shots, median 3-4 s, longest about 8 s. Give each location one continuous take and re-frame inside it with a whip of 5-8 frames; change location with a cross-dissolve of 6-8 frames (`xfade=transition=fade:duration=0.23`). Use at most one or two hard cuts.
- Keep the camera moving in every shot: aim for 2 px/frame of background motion on a slow push and 8-11 px/frame on an orbit or tracking take. Total fully static time should stay under about 1 s per clip.
- Use eased (Bezier) camera keys. v1 sets `keyframe_new_interpolation_type = 'LINEAR'`.

**Characters**
- Shade them unlit: Emission shaders with the hex values above, head `#fdf7f7`. They must look identical in every shot regardless of scene light. Whether reference characters cast ground shadows was not checked.
- Outline is attached to the model and scales with it: 4.5-5.5 % of head diameter, colour `#3d2933` (dark plum, not black). Build it as an inverted hull: Solidify modifier with `use_flip_normals=True`, `use_rim=False`, `material_offset=1`, thickness 0.05 head diameters; second material = Mix Shader driven by Geometry > Backfacing, Emission ink on front faces and Transparent BSDF on back faces; `cycles.transparent_max_bounces >= 8`. These property and socket names exist in the installed bpy 5.3.0; the recipe itself was not test-rendered. Drop Freestyle.
- Faces are discrete states. Swap whole face textures with CONSTANT keyframes; hold a mouth or eye state 2-8 frames; blink = 1-2 frames closed plus 1 half-open frame; never tween between drawings.
- Bring characters on by sliding them up from the bottom edge over about 8 frames (A f1938-f1946).

**Text and inserts**
- Typeset every sign as SVG with real fonts and correct data, rasterise, map on a quad. Banner cap height about 11 % of frame width when featured. Use two contrasting faces on one sign (heavy slab serif in navy `#071147`, decorative Western face in red `#530c32`), an old-style serif masthead over Didone capitals for newspapers (paper `#fdefd7`, ink `#937c5e`).
- Show an insert by pushing the camera into the real prop, 0.3x to 1.4x area in about 12 frames, then whip back out so the prop is seen sitting in the scene.
- Flat explanatory artwork (cross-sections, maps) can be a 2D SVG with pan and zoom only; clip B does exactly this.

**Environment**
- Target a Canny edge-pixel share of 0.05-0.07 per frame: textured ground (cell-pattern gravel from a Voronoi texture, plank grain, strata bands), repeated kit parts (ties, trusses, posts, windows), and signage. Flat-shaded low-poly facets are acceptable and present in the reference.
- Saturation about 0.41-0.48 mean, luma about 0.45 mean.

**Easy in Blender plus SVG**: typeset textures, unlit characters, inverted-hull outline, face-state swapping, eased camera paths, whip re-framing, dissolves, flat 2D inserts, procedural gravel, wood and strata, a crowd as one textured ground plane.

**Hard on 4 CPU cores, with the closest honest substitute**

| Hard property | Substitute |
|---|---|
| 1950 frames with a camera that never rests | Render characters as a separate emission-only layer (1 sample, no noise). Use true 3D camera moves for a few signature shots; for the rest render the set once oversized and move a 2D crop, accepting no parallax there. |
| Large dense worlds across many locations | Two or three rich sets built from instanced kit parts, plus SVG-textured cards for distance. Fewer locations, more props each. |
| Motion blur on whips | Blur only the 5-8 whip frames, either Cycles motion blur on those frames or a directional blur in post. |
| Fireball, dust plume, steam, sparkles | 2D sprite or SVG frame animations on camera-facing quads; the reference effects are layered over an unchanged background. |
| Soft-cloud sky | Gradient sky with blurred SVG cloud shapes as the world texture. |
| Lip sync | Three or four mouth states switched from the narration loudness envelope every 2-4 frames. |
| Shallow depth of field (clip B close-ups) | Compositor Defocus from the Z pass on those shots only. |

No generative pipeline is recommended: every property measured here is reproducible deterministically.

## Differences vs v1 (ranked by visual impact)

1. **Empty set.** v1 has an edge-pixel share of 0.017 against 0.060-0.068. The reference frame is full of textured surfaces, repeated structure and readable signage; v1 is a bare room with flat untextured walls, floor and desk.
2. **Camera barely moves.** v1 is one 0.63 m linear dolly over 72 frames. The reference changes about 60 % of its pixels every frame, orbits, pushes into props and whips between framings inside one take.
3. **Washed out and too bright.** v1 saturation 0.29 and luma 0.65 against 0.41-0.48 and 0.44-0.45.
4. **Outline too thin and the wrong kind.** v1 outline is 1.8-2.1 % of head diameter in neutral `#272727`, drawn by Freestyle at a fixed pixel width. The reference is 4.2-5.7 %, plum `#3d2933`, and scales with the character.
5. **Characters are lit.** v1 heads show a 69-91 level shading gradient; reference heads are flat within 9-24 levels and keep the same hex in every shot.
6. **24 fps with linear keys and static faces.** The reference is 30 fps, eased, with face states changing every 2-8 frames and regular blinks.
7. **No edit grammar.** v1 is a single shot; the reference averages a new shot every 3.4-4.7 s joined by 5-9 frame dissolves.

v1 already does one thing the reference does: the wall map carries typeset, correct text ("SEPT 20, 1938", "FLA.").

## Not determined

- Which renderer or engine was used. The look (flat facets, crisp textures, no path-tracing noise) is that of a rasteriser, but that is an impression, not a measurement.
- Whether characters are 3D proxies or multi-angle 2D rigs.
- How the motion blur was produced.
- Whether any asset was made with a generative tool.
- Exact button and chain-link counts on the boss.
