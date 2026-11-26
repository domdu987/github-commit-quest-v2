> Worked example (first production): the look review of a version 1.1 cut against the reference and against version 1, before the fix round. The cut reviewed here was **withdrawn**: it carried a 2D background blur the client never asked for. The film of record is `deliver/film_v1_1_sharp_thai.mp4` (the sharp v1 picture with the v1.1 grade, captions and sound). Everything about the blur has been taken out of this copy. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.
> Note section 3, "What got worse": a polish pass can break things that were right, so every review of a new version looks for regressions as well as gains. Paths under PROJ name that project's working files, which are not bundled.

# QA: a version 1.1 cut (withdrawn) against the reference clips and against version 1

Independent review. Nothing in the film was changed. File reviewed: a v1.1 cut that was later withdrawn (PROJ = `__PROJ__`); the film of record is `PROJ/deliver/film_v1_1_sharp_thai.mp4`: 720x1280, 30 fps, 1965 frames (65.50 s), AAC stereo 48 kHz. Compared with `PROJ/deliver/film_v1_thai.mp4` and the v1 review `PROJ/deliver/QA_film.md`.

Working files are in `PROJ/v3/film/out_v11/review_look/`:
- `all/`: every v1.1 frame, extracted the same way as v1's `out/review/all/` (ffmpeg -q:v 2).
- `score/`: score.py on the v1.1 MP4, captions in, the same call as the v1 review.
- `hue_cmp.txt`: hue_report.py rows for v1 and v1.1 on the same frame lists as `out/review/fs/`.
- `trip/t_NNNN.jpg`: 42 full-size triptychs, each with the v1 frame, the same v1.1 frame and the nearest reference still. They cover all 26 shots.
- Crop strips at full size: `s11_face.jpg`, `s11_face_b.jpg`, `s23_fog.jpg`.
- The scripts: `trip.py`, `hue_cmp.py`, `crops.py`.

The clock is unchanged. The frame-difference series of v1 and v1.1 correlate at 0.98, and every cut and the two hard cuts (into 18 at g1123, into 24 at g1720) are on the same frames.

## 1. Light: closer than v1?

**Yes, clearly.** Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.

### 1.1 The rows that were out of range in v1 (score.py, whole film, captions in)

| Metric | v1 | **v1.1** | Reference range | A | B |
|---|---|---|---|---|---|
| Contrast (luma p95-p5) | 0.498 | **0.622** | 0.60-0.75 | 0.601 | 0.616 |
| Share of pixels V > 0.95 | 0.012 | **0.031** | 0.02-0.09 | 0.060 | 0.053 |
| Mean luma, top third | 82 | **92** | 85-135 | 118 | 94 |
| Mean luma, middle third | 103 | **117** | 105-150 | 121 | 117 |
| Saturation mean | 0.395 | **0.413** | 0.40-0.60 | 0.490 | 0.421 |
| Head fill V | 0.996 | **0.976** | 0.960-0.995 | 0.992 | 0.969 |
| Head fill S | 0.051 | 0.036 | at most 0.055 | 0.032 | 0.049 |
| Black point (luma p1) | 0.118 | 0.095 | 0.08-0.12 | 0.116 | 0.094 |
| Colourfulness | 55.0 | 65.2 | 55-100 | 86.4 | 58.8 |
| Canny edge density | 0.051 | 0.058 | 0.050-0.110 | 0.062 | 0.068 |
| Thin dark line share | 0.051 | 0.062 | 0.030-0.200 | 0.065 | 0.074 |
| Pan median px/s | 39 | 39 | 40-150 | 142 | 57 |
| Interval between framing changes (s) | 1.06 | 1.09 | 1.20-1.70 | 1.39 | 1.62 |
| Caption text height (px) | 45 | 45 | 33-40 | 36 | 37 |

**Re-measured on the film of record** (score.py on `deliver/film_v1_1_sharp_thai.mp4`, whole film, captions in, the same call): index 0.993; contrast 0.621; V > 0.95 share 0.032; top third 92; middle third 117; saturation 0.417; head fill V 0.980, S 0.052; black point 0.094; colourfulness 65.3; Canny edge density 0.060; thin dark line share 0.064; pan median 38 px/s; framing interval 1.13 s; caption height 45 px. Use these numbers for the delivered v1.1.

On the withdrawn cut: index 0.980 -> **0.992**. Colour and tone 0.940 -> 1.000; density and light 0.987 -> 1.000; characters 0.996 -> 1.000; captions 0.944 -> 0.940.

All five light rows are now inside the range. Contrast, top third, saturation and highlights sit near the low edge. The highlight share (3.1 %) is about half the reference (5-6 %), and the top third (92) is at clip B's level, not clip A's (118). The three rows still out of range are the edit and caption rows (pan, framing interval, caption height), which v1.1 was not asked to change.

What it looks like (`trip/`):
- **Glow.** The lamp globes now carry a halo onto the shade and ceiling (g291, g815, g1150, g1850). They read as lit sources, not cut-out discs. The glow is tight and modest next to the reference candles and sun (B 01.0, A 15.5).
- **Exteriors.** The sunny beach (g418) has no sun bloom or visible haze; it looks almost the same as v1.
- **Faces.** They stay flat white without a cast (head fill S 0.036, V 0.976). Sampled face fill: v1 (249,237,242), v1.1 (251,239,244).

### 1.2 Depth

Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. Distance haze on the exteriors is barely visible: the s08 vista, g418, looks the same as v1.

### 1.3 Hue table: the corrected shots (hue_report.py, same frame lists as v1)

| Set | | red | orange | blue | violet | magenta | sat | val | dark | out of band |
|---|---|---|---|---|---|---|---|---|---|---|
| Whole film | v1 | 32.6 | 24.3 | 31.2 | 2.3 | 4.4 | 0.39 | 0.49 | 0.11 | blue |
| | v1.1 | 34.1 | 29.6 | 24.9 | 2.3 | 3.4 | 0.40 | 0.55 | 0.13 | **in band** |
| Office shots (1-7, 9-14, 17, 18) | v1 | 37.0 | 28.0 | 20.8 | 1.1 | 4.5 | 0.41 | 0.48 | 0.13 | in band |
| | v1.1 | 36.3 | 31.5 | 18.2 | 1.0 | 3.7 | 0.43 | 0.54 | 0.14 | **in band** |
| s16 | v1 | 24.0 | 4.2 | 65.4 | 1.1 | 5.2 | 0.24 | 0.65 | 0.01 | 6 of 8 |
| | v1.1 | 33.0 | 6.2 | 57.1 | 1.4 | 2.1 | 0.31 | 0.67 | 0.06 | orange, blue, sat, val, dark |
| s19 | v1 | 24.3 | 26.0 | 45.8 | 0.4 | 3.2 | 0.36 | 0.47 | 0.12 | red, blue, sat |
| | v1.1 | 33.4 | 38.0 | 26.6 | 0.4 | 1.1 | 0.38 | 0.53 | 0.12 | orange (38.0, at the edge) |
| s20 | v1 | 11.8 | 18.1 | 62.2 | 1.0 | 6.7 | 0.35 | 0.49 | 0.10 | red, orange, blue, sat |
| | v1.1 | 28.1 | 33.3 | 30.7 | 1.2 | 6.7 | 0.35 | 0.55 | 0.10 | red, blue, sat (all near the edge) |
| s21 | v1 | 15.3 | 8.7 | 67.0 | 1.3 | 7.0 | 0.28 | 0.52 | 0.12 | red, orange, blue, sat |
| | v1.1 | 33.4 | 42.8 | 19.0 | 1.1 | 2.3 | 0.34 | 0.60 | 0.12 | orange, sat |
| s23 | v1 | 21.9 | 7.7 | 3.9 | 55.3 | 11.2 | 0.30 | 0.49 | 0.01 | 7 of 8 |
| | v1.1 | 23.5 | 5.7 | 5.4 | 54.7 | 10.7 | 0.32 | 0.58 | 0.01 | 7 of 8 (violet sky kept on purpose) |
| s25 | v1 | 29.9 | 15.3 | 45.0 | 1.8 | 5.0 | 0.34 | 0.33 | 0.33 | 6 of 8 |
| | v1.1 | 28.4 | 15.9 | 43.7 | 2.7 | 6.4 | 0.33 | **0.49** | **0.08** | red, orange, blue, sat |

- **s19, s20 and s21** move from cold blue to the warm band (blue 46/62/67 -> 27/31/19). s21 overshoots a little into orange (42.8).
- **s25** is now readable (val 0.33 -> 0.49, dark 33 % -> 8 %).
- **s16** gains colour and darks but is still out on five of eight.

The full 26-shot table is in `hue_cmp.txt`.

## 2. The 26 shots again: same film as the reference?

Same question as section 3 of the v1 review. Changes are in bold.

1. 0.0-1.3 pencil insert: Yes. Almost unchanged (slightly warmer).
2. 1.3-2.4 hero jab: Yes. **The lamp glows.**
3. 2.4-4.3 two-shot erase: Yes. Still the best match in staging.
4. 4.3-6.6 wide office, calendar: Partly (unchanged). The calendar paper is brighter and bluer: sampled (123,138,177) -> (150,171,223).
5. 6.6-9.0 fly-in, Florida spinner: Partly (unchanged).
6. 9.0-11.2 three seniors: Yes. **The globes now glow.**
7. 11.2-13.4 chalk curve insert: Partly (unchanged).
8. 13.4-16.8 sunny beach: Yes. There is still no sun bloom or visible haze.
9. 16.8-20.3 youngest: Yes (unchanged).
10. 20.3-23.1 chief, gloat framing: Yes.
11. 23.1-26.4 erase, draw again: Yes, **with a new artifact.** At g740-743 (24.67-24.80 s) the hero's motion-blurred eyes and mouth turn into pale hollow outlines (`s11_face_b.jpg`).
12. 26.4-28.0 laughing seniors: Yes. Every laughing face must stay readable, as in the reference laugh shot (B 06.5), including the hero's sour face, which is the point of the shot.
13. 28.0-28.9 label slap: Yes. The label is sharp.
14. 28.9-31.9 teletype, forecast sheet: Yes. The sheet is sharp; the background is unchanged.
15. 31.9-33.8 kitchen newspaper: Partly (unchanged; still all warm, blue 7 %).
16. 33.8-36.2 grey beach drizzle: No. **There is more colour (sat 0.31, 6 % darks) and the sand is warmer, but the sky turned lavender-violet** (g1060). The empty-sky frame at 35.0-35.3 s is still there.
17. 36.2-37.4 chief strolls in: Yes.
18. 37.4-39.6 second gloat: Yes (the label is readable).
19. 39.6-47.3 map as terrain, two highs: Partly. **The lit faces of the blocks are warm pink-beige, not grey-lavender.** It is still a diagram.
20. 47.3-50.5 corridor launch: Partly. **Warmer (blue 31 %).** Still a road-sign world.
21. 50.5-52.4 storm past the ghosts: **Partly (was No).** The cold palette is fixed: the walls are sand-coloured and blue is 19 %. The ghost storms are still too small and grey to read.
22. 52.4-55.5 label, pull-out: Yes (unchanged).
23. 55.5-57.3 beach, violet sky, fog: Partly. **A pale fog band now covers the yellow horizon glow behind the umbrella and poles** (`s23_fog.jpg`). It is still only a strip about 40-60 px tall and is easy to miss on a phone. The sky is still flat violet.
24. 57.3-59.6 wall of water: Yes (almost unchanged; the crest is a little brighter).
25. 59.6-62.4 spinner up the line, impact: Partly. **It is readable now (val 0.49, dark 8 %),** and the map run reads. The two men still barely react.
26. 62.4-65.5 kitchen window, table: Yes. The forecast sheet is sharp. The dark share rose from 22 % to 40 % (the window and the table cloth are deeper). It still reads, and the water in the panes still reads as clouds.

Tally for the sharp v1.1: **16 yes, 9 partly, 1 no** (v1: 15 / 9 / 2; shot 12 counted Yes as in v1, inferred, not re-reviewed).

Answer that changed: shot 21, No -> Partly.

Within an unchanged answer, shots 2, 6, 19, 20 and 25 moved closer to the reference (light and colour).

## 3. What got worse

1. **Ghost face in shot 11, g740-743 (24.67-24.80 s, 4 frames).**
   - The hero's eyes and mouth lose their ink and become pale hollow rings. Dark pixels (luma < 80) in the face area: v1 0.078 against v1.1 0.010 at g740.
   - It comes from the grade: the ungraded frame is identical to v1; `out_v11/graded/g_0740.png` had the artifact.
   - Most likely the white-protect or hot-bloom stage treats the motion-blurred grey ink as near-white fill.
   - It is short and inside a fast move, but it is visible at full size. It is the only true artifact found.
2. **The s16 sky moved toward violet** (g1030, g1060): it now reads lavender rather than grey. With the empty-sky frame still in, this shot looks no more like the reference than in v1. Only the numbers improved.
3. **Colour that left the band** (hue rows, v1 in band -> v1.1 out):
   - s10: blue 15.4 -> 12.7
   - s11: orange 36.4 -> 40.6, dark 0.16
   - s17: orange 37.6 -> 40.9
   - s13: orange 41.5
   - s04: dark 0.19, sat 0.49
   - s26: dark 0.22 -> 0.40

   All are a few points over an edge, caused by the global warm S-curve, and none is visible as a cast. The office aggregate and the whole film are in band.
4. **The calendar insert (s4) is bluer and brighter** (paper (123,138,177) -> (150,171,223)). It still reads.
5. **Faces:** no cast found. Head fill S 0.036, sampled face fills within 2-4 levels of v1.
6. **Captions:** still readable everywhere. The caption band is brighter: mean luma 0.378 -> 0.412, frames whose band mean is over 0.6 went from 21 to 48 (every 3rd frame sampled). The brightest are the white-flash frames (g1872, g1788, as in v1) and the forecast sheet (g960-969, band mean 0.69 -> 0.75). The 4 px black stroke keeps those legible at full size (g980), but they are the lowest-contrast captions in the film.
7. **Sound:** -13.9 -> -14.8 LUFS integrated, LRA 1.8 LU, true peak -1.0 dBFS. This is consistent with the voice 1 dB lower; not re-measured in detail.

## 4. What still differs most from the reference after v1.1, ranked by how much a viewer would notice

| # | Difference | Where | Evidence |
|---|---|---|---|
| 1 | **Depth.** Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. No visible distance haze on the exteriors. | s08/s16 vistas | g418 |
| 2 | **Light is in range but at its floor.** Glow is tight round the lamps; there is no sun bloom on the beach and no warm light spill. The reference glows harder. | All, most in the exteriors | V > 0.95 3.1 % against 5-6 %; contrast 0.622; top third 92 against 94-118 |
| 3 | **Shot 16 is still empty and off-palette.** Lavender sky; the tilt still holds on empty sky. | s16 | 5 of 8 hue rows out; g1060 |
| 4 | **The map-as-terrain sequence is still a diagram**, now warm, and the ghost storms of beat 16 are still illegible. | s19-s21 | g1350, g1530 |
| 5 | **Captions are bigger and heavier** than the reference (client decision, unchanged). | All | 45 px against 36-37 |
| 6 | **The fog bank is visible but small.** | s23 | `s23_fog.jpg` |
| 7 | **The climax plays without reaction.** | s25 | g1846-1870 |
| 8 | **New: shot 11 ghost face** (section 3, item 1). | s11 | `s11_face_b.jpg` |
| 9 | **The cut is busier** than either reference. | Edit | framing interval 1.09 s against 1.39 / 1.62 |
| 10 | **Flat surfaces and other notes from v1:** all-warm kitchen (s15 blue 7 %), the water in s26 reads as clouds, the s05 smear. | s15, s26, s05 | unchanged |

Verdict: v1.1 is closer to the reference than v1. The light rows and the colour of the cold sequence are fixed. Before shipping, fix the 4-frame ghost face in shot 11 (grade; done in the fix round: no glow inside near-white fills, only pale sources are hot).
