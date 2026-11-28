> Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. The film of record of version 1.1 is `deliver/film_v1_1_sharp_thai.mp4` (the sharp v1 picture with the v1.1 grade, captions and sound).

> Worked example (first production): the independent review of version 1, written by a reviewer who did not build the film. Use it as the model for the review in phase 8: the measured tables, the per-shot verdicts, and the ranked list of differences with the cheapest fix for each. Paths under PROJ name that project's working files (frames, sheets), which are not bundled.

# QA: film_v1_thai.mp4 against reference clips A and B

Independent review. The film was not changed. File reviewed: `PROJ/deliver/film_v1_thai.mp4` (PROJ = `__PROJ__`): 720x1280, 30 fps, 1965 frames (65.50 s), AAC stereo 48 kHz.

Images: `PROJ/deliver/film_contact.jpg` has 48 frames, evenly spaced from g0 to g1964, with time, frame and shot number (#) above each. `PROJ/deliver/film_vs_reference.jpg` has six rows: light, depth, camera angle, colour, character close-up and disaster. Each row shows a reference frame beside our closest frame, with frame statistics.
Working files: `PROJ/v3/film/out/review/`. This folder holds the scorecard (`score/`), the parallax rows (`parallax_film.json`), the hue tables (`hue_film.txt`, `hue_takes.txt`), the audio measurements (`audio_qa.txt`), the 0.5 s contact sheets (`film_half_*.jpg`, `ref_a_*.jpg`, `ref_b_*.jpg`) and the scripts that made them.

## 1. Measured tables

### 1.1 score.py (whole film, captions in)

| Group | Score |
|---|---|
| Characters (0.30) | 0.996 |
| Colour and tone (0.15) | 0.940 |
| Density and light structure (0.15) | 0.987 |
| Camera and edit (0.20) | 0.989 |
| Animation life (0.10) | 1.000 |
| Captions (0.10) | 0.944 |
| **Index / strict index / coverage** | **0.980 / 0.980 / 100 %** |

Metrics outside the reference range. The index cannot see light quality, shadows, perspective or story, so these rows are the useful part:

| Metric | Ours | Reference range | A | B |
|---|---|---|---|---|
| Contrast (luma p95-p5) | **0.498** | 0.60-0.75 | 0.601 | 0.616 |
| Share of pixels V > 0.95 (highlights) | **0.012** | 0.02-0.09 | 0.060 | 0.053 |
| Mean luma, top third | **82** | 85-135 | 118 | 94 |
| Mean luma, middle third | **103** | 105-150 | 121 | 117 |
| Saturation mean | 0.395 | 0.40-0.60 | 0.490 | 0.421 |
| Head fill V | 0.996 | 0.960-0.995 | 0.992 | 0.969 |
| Pan median px/s | 39 | 40-150 | 142 | 57 |
| Interval between framing changes (s) | **1.06** | 1.20-1.70 | 1.39 | 1.62 |
| Caption text height (px) | **45** | 33-40 | 36 | 37 |
| Canny edge density | 0.051 (at the floor) | 0.050-0.110 | 0.062 | 0.068 |
| Thin dark line share | 0.051 | 0.030-0.200 | 0.065 | 0.074 |

### 1.2 Parallax: share of 0.5 s frame pairs that a flat 2D zoom or pan explains

This is `qa_parallax.py run_seq` on the 131 stills taken every 0.5 s (RATIO 0.51, calibrated on the references).

| Set | Flat 2D share |
|---|---|
| Reference A | 11 % (published 12) |
| Reference B | 43 % |
| **Film** | **31.5 % (41 of 130 pairs; 124 matched; medians F 0.51, H 0.31, S 0.15)** |
| Film, pairs inside one shot | 25 % (26 of 105) |

Flat pairs per shot (flat / pairs inside the shot): 1 0/2, 2 0/1, 3 0/3, **4 3/4**, 5 0/4, 6 1/3, 7 0/3, 8 1/6, 9 2/6, 10 2/5, 11 1/5, **12 2/2**, 13 1/1, 14 2/5, 15 1/3, 16 1/4, 17 0/1, 18 2/4, 19 2/14, 20 2/6, 21 0/2, 22 1/5, 23 0/3, 24 1/4, 25 1/4, 26 0/5. The film sits between the two clips, so it does not read as flat 2D. Shots 4 and 12 are the most card-like.

### 1.3 Edit against camera_motion.md

| | Film | Clip A | Clip B | Plan |
|---|---|---|---|---|
| Shots | 26 (25 takes) | 16 | 22 | 26 |
| Shot length mean / median / range | 2.52 / 2.30 / 0.97-7.67 s | 3.75 / 3.65 / 0.70-7.73 | 2.62 / 2.45 / 0.40-6.53 | 2.52 / 2.29 |
| Cross-dissolves | 17 of 24 real transitions = 71 %, 9-17 frames, median 12 | 11 of 15 = 73 %, median 13 | 18 of 21 = 86 %, median 10.5 | 17 |
| Hard cuts | 2 (into shot 18, into shot 24) | 1 | 1 | 2 |
| Other transitions | whip (3), hidden cut in whip-tilt (5), punch-in (13), wipe (25), white flash (26) | train wipe, hidden cut, flash | punch-in, whip | same |
| Interval between framing changes, score.py reading | 1.06 s (24 transitions + 37 snaps detected) | 1.39 | 1.62 | 1.26 by plan count |
| Static frames / longest hold | 3.2 % / 12 frames | 3.8 % / 14 | 5.5 % / 12 | |
| Zoom median / pan median | 11.4 %/s / 39 px/s | 20.7 / 142 | 9.9 / 57 | |
| Snap easing peak/mean | 1.69 | 1.87 | 1.66 | |

Shot lengths in seconds, shots 1-26: 1.30 1.13 1.87 2.33 2.40 2.17 2.17 3.47 3.50 2.80 3.27 1.57 0.97 2.93 1.90 2.43 1.23 2.20 7.67 3.23 1.83 3.10 1.87 2.27 2.83 3.07.
On the same tool the framing changes 24 % more often than in clip A and 35 % more often than in clip B. The cut is busier than either reference.

### 1.4 Colour: hue_report.py

Share of chroma by hue family. Target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15. The per-shot rows are film frames (captions in, caption band excluded). The take rows are each take's own frames, every 3rd frame inside g0..g1.

| Set | red | orange | blue | violet | magenta | sat | val | dark | out of band |
|---|---|---|---|---|---|---|---|---|---|
| Ref A whole | 33.6 | 23.1 | 29.1 | 2.7 | 9.7 | 0.48 | 0.63 | 0.08 | sat, val, dark |
| Ref B whole | 24.5 | 34.1 | 28.6 | 4.5 | 5.0 | 0.41 | 0.57 | 0.08 | red, dark |
| **Film whole** | 32.6 | 24.3 | 31.2 | 2.3 | 4.4 | 0.39 | 0.49 | 0.11 | blue (31.2) |
| shot 1 | 29.9 | 39.5 | 13.4 | 0.3 | 1.9 | 0.41 | 0.49 | 0.10 | red, orange, blue (cyan 15) |
| shot 2 | 52.3 | 17.2 | 20.3 | 0.8 | 4.7 | 0.45 | 0.47 | 0.14 | red, orange |
| shot 3 | 39.3 | 31.9 | 19.3 | 1.0 | 4.5 | 0.44 | 0.50 | 0.13 | in band |
| s04 | 45.0 | 11.6 | 31.0 | 1.1 | 8.9 | 0.47 | 0.43 | 0.14 | red, orange, blue, val |
| s05 | 37.9 | 26.4 | 13.9 | 0.6 | 3.7 | 0.39 | 0.46 | 0.15 | blue (cyan 17.5) |
| s06 | 38.5 | 15.6 | 33.4 | 1.1 | 5.3 | 0.47 | 0.46 | 0.13 | orange, blue |
| s07 | 28.4 | 30.4 | 15.5 | 0.5 | 2.2 | 0.37 | 0.49 | 0.09 | red, sat (cyan 23) |
| s08 | 35.8 | 21.7 | 38.1 | 2.4 | 1.6 | 0.36 | 0.71 | 0.02 | orange, blue, sat, val, dark (sunny exterior) |
| s09 | 32.4 | 25.8 | 23.7 | 0.9 | 4.2 | 0.40 | 0.51 | 0.12 | in band |
| s10 | 40.4 | 31.5 | 15.4 | 1.1 | 4.5 | 0.43 | 0.49 | 0.12 | in band |
| s11 | 33.6 | 36.4 | 17.4 | 2.3 | 3.8 | 0.44 | 0.48 | 0.14 | in band |
| s12 | 38.7 | 21.5 | 24.5 | 0.9 | 7.2 | 0.39 | 0.45 | 0.13 | orange (21.5) |
| s13 | 23.8 | 36.7 | 26.5 | 0.3 | 1.8 | 0.43 | 0.50 | 0.07 | red, dark |
| s14 | 33.5 | 32.1 | 25.7 | 1.5 | 4.7 | 0.36 | 0.57 | 0.13 | sat |
| s15 | 52.1 | 40.2 | 6.5 | 0.1 | 1.1 | 0.43 | 0.61 | 0.02 | red, orange, blue, dark (all warm) |
| s16 | 24.0 | 4.2 | 65.4 | 1.1 | 5.2 | **0.24** | 0.65 | **0.01** | red, orange, blue, sat, val, dark |
| s17 | 37.2 | 37.6 | 16.4 | 1.2 | 3.8 | 0.39 | 0.47 | 0.14 | in band |
| s18 | 47.1 | 27.8 | 12.4 | 1.2 | 4.1 | 0.38 | 0.46 | 0.15 | red, blue, sat, dark |
| s19 | 24.3 | 26.0 | 45.8 | 0.4 | 3.2 | 0.36 | 0.47 | 0.12 | red, blue, sat |
| s20 | 11.8 | 18.1 | 62.2 | 1.0 | 6.7 | 0.35 | 0.49 | 0.10 | red, orange, blue, sat |
| s21 | 15.3 | 8.7 | 67.0 | 1.3 | 7.0 | 0.28 | 0.52 | 0.12 | red, orange, blue, sat |
| s22 | 30.0 | 31.4 | 29.6 | 0.9 | 4.1 | 0.32 | 0.49 | 0.08 | sat, dark |
| s23 | 21.9 | 7.7 | 3.9 | **55.3** | 11.2 | 0.30 | 0.49 | 0.01 | 7 of 8 (violet sky) |
| s24 | 8.9 | 0.3 | **83.1** | 1.8 | 4.0 | 0.45 | 0.45 | 0.01 | red, orange, blue, val, dark (night wave) |
| s25 | 29.9 | 15.3 | 45.0 | 1.8 | 5.0 | 0.34 | **0.33** | **0.33** | red, orange, blue, sat, val, dark |
| s26 | 45.2 | 19.4 | 25.2 | 0.4 | 6.2 | 0.49 | 0.36 | 0.22 | red, orange, sat, val, dark |

Take frames, for checking the conform: s01_hook in band; s04 out on 6; s05 2; s06 4; s07 1; s08 4; s09-s12 in band; s13 2; s14 1; s15 4; s16 6; s17 2; s18 4; s19 3; s20 4; s21 4; s22 1; s23 7; s24 5; s25 6; s26 5 (`review/hue_takes.txt`). The take rows match the film rows within 1 to 3 points, so the conform did not shift colour.
Overall the film is close to the band. The colour problem is uneven: shots 16, 19-21, 23 and 25 swing far from the reference palette, and they make up 22 s of the 65 s.

### 1.5 Captions

| | Film | Reference |
|---|---|---|
| Centre x / centre y | 359.5 / 899.5 px | 359.5 / 900 |
| Fill / stroke | white 0 levels off / 4.0 px black | white / 4 px |
| Text height (white box) | **45 px** (Kanit Black fs88, Thai with vowel and tone marks) | 36-37 px (Latin) |
| Words per caption / median duration | 1.03 / 18 frames | 1.24-1.34 / 11 frames |
| Frames with a caption / full size on first frame | 100 % / 100 % | 96-100 % / 98-99 % |

Position, colour and stroke match. The Thai captions are about 25 % taller and visibly heavier than the reference's Latin words. That follows the brief's fs88, so a change needs the client's decision.

### 1.6 Sound (against BRIEF_FINISH.md)

The voice was isolated by fitting `narration.wav` to the mix: lag 0.102 s (the brief specifies 0.100 s), fitted gain 1.500 (spec 1.512), correlation 0.98. The music was isolated by fitting `music_fit.wav` to what remained.

| | Film | Brief / reference |
|---|---|---|
| Voice RMS (active 50 ms windows) | **-16.4 dBFS** | about -17.4 |
| Mix RMS / integrated loudness / LRA / true peak | -16.5 dBFS / -13.9 LUFS / 1.7 LU / -0.8 dBFS | |
| Music bed RMS | -38.0 dBFS, from the first frame (-37.2 in 0-0.5 s), fades in the last 0.4 s | -38, first frame to end |
| Voice gaps of 150 ms or more | 9, 1.65 s in all, longest 0.25 s | effects go in the gaps |
| Mix RMS / peak in the gaps | -29.9 / -13.3 dBFS | |
| Non-voice peaks over -10 dBFS while the voice speaks | 0.35 s (-8.4), 2.0 s (-7.0): approved hook entries; **48.1 s (-9.5)**: gust thump plus wind, music included | at or under -10 |
| Effect cadence | 26 point effects after the hook, one every 2.3 s, plus 10 ambiences (SOUND.md); bursts with peaks over -22 dBFS about every 1.1 s, longest quiet stretch 3.85 s at 14.6 s | every 2.5-3 s |
| Ambiences | rain -41.5, wind -33/-30, room tone -34, wave roar -32.6 RMS | -34 to -30 |

The voice is 1 dB hotter than the reference. The new narration hardly pauses, so the effects necessarily sit under words. The drizzle beds at -41.5 are below the ambience band and inaudible on a phone.

## 2. Story check with the script (from the picture, sound off)

| Beat (gloss line) | Shot | Readable from the picture? |
|---|---|---|
| 1 hook: line drawn into New York, boss rubs it out | 1-3 | Yes, clearly |
| 2 September 1938, hurricane off Florida | 4-5 | Yes (calendar SEPTEMBER 20 1938; spinner pinned off FLA.) |
| 3 old hands: it will curve out to sea | 6-7 | Yes (three seniors; chalk curve bending out) |
| 4 New England not hit for 120 years | 8 | Half: a calm sunny beach with a LONG ISLAND sign reads; "120 years" is only in the voice |
| 5 youngest; his line goes straight north | 9 | Yes |
| 6 boss quote 1 | 10 | Yes (gloat framing, chief talking) |
| 7 rubbed out, drawn again | 11 | Yes (eraser, pencil, purple-faced boss) |
| 8 nickname | 12-13 | Yes (laughing seniors; label ทางด่วนพายุ slapped on) |
| 9 official forecast: rain, gusty winds | 14 | Yes (sheet ฝนตก ลมกระโชก fills the frame) |
| 10 next morning: grey sky, drizzle | 15-16 | Mostly; 35.0 s is an empty grey sky with half a head at the edge |
| 11 boss quote 2 | 17-18 | Yes |
| 12 two highs squeeze the storm like walls | 19 | Yes as a diagram (two blocks marked H close in on the spinner); 7.7 s long and cold |
| 13-15 one corridor, no turning, nearly 100 km/h | 19-20 | Yes (no-turn signs, 100 km/h sign) |
| 16 hardly any hurricane this fast | 21 | Weak: the ghost spinners being overtaken are too small and grey to read on a phone |
| 17 Storm Expressway = this corridor | 22 | Yes (label, then pull-out: walls on the red line) |
| 18 people on the beach see a fog bank | 23 | **No: the fog bank is a faint pale strip at the horizon and is easy to miss** |
| 19 wall of water taller than a house | 24 | Yes |
| 20 straight into New York | 25 | Yes on the map; the impact in the gloat framing has little reaction |
| 21 forecast on the kitchen table still says rain | 26 | Yes |

Callbacks:
- **Gloat framing (10 > 18 > 25): lands.** Same axis and marks, with the chief at the back left and the hero near at the right, and the light changes from day to grey to storm. In 18 the planned "grin close-up" opens on a neutral face.
- **Label (13 > 18, 22, 25): lands.** It is readable in all three.
- **Beach framing (16 > 23): lands in part.** The sign, porch and poles repeat, but the man moves from centre to left third and the camera sits a little lower, so the match is felt rather than seen.
- **Forecast paper (14 > 15 > 26): lands strongly.** The same ฝนตก ลมกระโชก print appears on the teletype sheet, in the newspaper and in the last frame.

## 3. The 26 shots: same film as the reference? Most visible difference

1. 0.0-1.3 pencil insert: **Yes.** The map is crisp, flat teal and tan under hard blind shadows; reference inserts carry haze.
2. 1.3-2.4 hero jab, low: **Yes.** Red takes 52 %.
3. 2.4-4.3 two-shot erase, shocked hero: **Yes.** This is the best match to the reference. The "close-up" holds the head at about 250 px against 300-385 in the reference.
4. 4.3-6.6 wide office, then the calendar: **Partly.** The wide frame at 4.5-5.0 s is dark and cluttered with 50-70 px heads, and orange is only 12 %. The calendar insert is clean. Two of three pairs read as a flat card.
5. 6.6-9.0 fly-in to the Florida spinner: **Partly.** The 27-frame fly-in is a full smear (6.7 s), and the map insert reads as a flat diagram (cyan 17 %).
6. 9.0-11.2 three seniors, low: **Yes.** The look is B-like. The lamp globes are blown flat white discs with no glow, and blue (the rug) is 33 %.
7. 11.2-13.4 chalk curve insert: **Partly.** It reads as an infographic on paper (cyan 23 %, sat 0.37). The reference never holds a flat chart this long.
8. 13.4-16.8 sunny beach: **Yes.** This is the most reference-like exterior. The sky has no sun bloom or haze, and the crash push ends with the umbrella filling the top half while the sleeper is half hidden.
9. 16.8-20.3 youngest, the line, corridor view: **Yes** up to 19 s. The corridor view at 19.5-20 s is a raking macro that reads as abstract.
10. 20.3-23.1 low on the chief, then the gloat framing: **Yes.** The low angle looks into a dark ceiling, where the reference's low angles look up at bright sky.
11. 23.1-26.4 erase, draw again: **Yes.** The purple face echoes clip A. The 23.5-24.5 s insert is dim and murky under the blind shadows.
12. 26.4-28.0 laughing seniors: **Yes.** The frame is crowded and heads are cut at the edges. Both pairs read as a flat card.
13. 28.0-28.9 label slap: **Yes.** This is a clean insert, and the label reads in under a second.
14. 28.9-31.9 teletype and forecast sheet: **Yes.** The sheet fills the frame; saturation is low (0.36).
15. 31.9-33.8 kitchen newspaper: **Partly.** The whole frame is warm (red and orange 92 %, blue 6 %), with no cool shade.
16. 33.8-36.2 grey beach drizzle: **No.** It is washed out (sat 0.24, 1 % darks), and the tilt lands on an empty grey sky with half a face at the edge. No reference frame is this empty.
17. 36.2-37.4 chief strolls in whistling: **Yes.** The shot is very short (1.2 s), and the chief's near-profile torso dominates.
18. 37.4-39.6 second gloat: **Yes.** The callback reads. It opens on a neutral medium shot of the chief, not the planned grin close-up.
19. 39.6-47.3 map as terrain, two highs: **Partly.** Pale grey-lavender blocks with an "H" read as an explainer diagram (blue 46 %, sat 0.36). The reference's explainer beats (B pendulum, B cross-section) keep warm light and rich material.
20. 47.3-50.5 corridor launch, 100 km/h sign: **Partly.** This is a graphic road-sign world, very blue (62 %); readable but cold.
21. 50.5-52.4 storm races past the ghosts: **No.** It is the coldest shot (blue 67 %, sat 0.28), and the ghost storms are illegible at phone size.
22. 52.4-55.5 label, pull-out to the whole map: **Yes.** The idea lands. The walls-on-the-line reveal is small in frame.
23. 55.5-57.3 beach under a violet sky, fog: **Partly.** The framing callback works, but the sky is flat purple (violet 55 %) with no glow, and the fog bank is barely visible.
24. 57.3-59.6 wall of water: **Yes.** The night-blue drama matches clip B's night. There is little scale cue until 58.5 s, and the faces are tinted lavender.
25. 59.6-62.4 spinner up the line, impact in the gloat framing: **Partly.** It is the darkest stretch (a third of pixels below V 0.25, val 0.33), so the climax plays in murk and the two men barely react.
26. 62.4-65.5 kitchen window, then the table: **Yes.** The ending lands. The "dark wall of water" in the panes reads as white puck clouds and rain, not water.

Tally: 15 yes, 9 partly, 2 no (16, 21).

## 4. The ten largest remaining differences, ranked by how much a viewer would notice

| # | Difference | Takes | Evidence | Cheapest fix |
|---|---|---|---|---|
| 1 | **Light quality.** No bloom, haze or glowing light sources; highlights are clipped flat (lamp globes are white discs) and the picture is low in contrast. The reference keys every scene with a sun or a lamp that glows and blooms. | All, worst in the office takes (s01_hook, s04-s14, s17, s18) | V > 0.95 share 1.2 % against 5-6 %; contrast 0.50 against 0.60-0.62; top-third luma 82 against 94-118 | A conform-only grade, no re-render: highlight bloom (threshold V 0.85, blur about 30 px, add 0.3) and an S-curve that lifts the top end until contrast reaches 0.60 and the V > 0.95 share reaches 3-5 %. Check with score.py. |
| 2 | **Depth.** No aerial perspective: the exterior vistas have no distance haze, and close and medium shots get little separation from the wall behind. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. | s08, s16, s23 vistas; hook shots 2-3, s10, s12, s17, s18, s25 (G') | film_vs_reference rows 2 and 5 | Through staging and light only, never a blur: a distance haze pass on the s08/s16/s23 beach vistas; a dark foreground layer near the lens; stage two-shots in depth (near head 1.36 to 1.46 times the far one); keep a lit gap or a cast shadow between the actors and the back wall. |
| 3 | **The map-as-terrain sequence is cold and diagrammatic** for 14.7 s (22 % of the film): grey-lavender blocks, a blue-dominated palette and low saturation. | s19, s20, s21 | blue 46 / 62 / 67 %, sat 0.36 / 0.35 / 0.28; red 24 / 12 / 15 % | Per-take grade: warm the wall faces and highlights toward the office lamp colour, raise sat to 0.40, and bring red/orange back to 30/22 %. If time allows, a warm key light on the blocks in a re-render of s19 only. |
| 4 | **Shot 16 is washed out and has an empty frame**: flat lavender grey, almost no darks, and the tilt holds on empty sky with half a face at the edge (35.0 s). | s16 | sat 0.24, dark 1 %, val 0.65; contact sheet at 35.0 s | Grade s16 (darken the lower third and foreground, contrast +, sat to 0.33). Re-time the tilt so the palm enters by 35.1 s (re-render 73 frames), or cut the 34.9-35.3 s sky frames into the dissolve. |
| 5 | **The fog bank (beat 18) is not readable.** "People on the beach saw a fog bank" has no clear picture, so the turn to the wall of water lands cold. | s23 | 56.8 and 57.3 s stills: only a faint pale strip at the horizon | Composite in the conform: a pale (#c9bfd0) soft-edged band on the horizon, 40 px rising to 120 px tall over 55.9-57.3 s, behind the man. 56 frames, 2D. |
| 6 | **Captions are bigger and heavier than the reference.** | All | text height 45 px against 36-37; Kanit Black fs88 | Re-burn with assemble.py at about fs72 (0.8x), which gives about 36 px. This conflicts with the brief's fs88, so ask the client first. |
| 7 | **The climax is too dark to read.** The spinner tearing up the line and the impact happen in murk. | s25 | a third of pixels below V 0.25; val 0.29-0.33 against 0.45-0.63 | Grade s25: lift the shadows (+0.06 at the black end, gamma 0.9) while keeping the lightning flash on top. |
| 8 | **Flat surfaces.** Walls, floor, sky and map have less surface detail than the reference's painted textures (stone, ballast, cloth). | Office takes, s16, s19-s21, s23 | edge density 0.051 (range floor 0.050; A 0.062, B 0.068); thin-line share 0.051 against 0.065-0.074 | A fine paper or brush grain overlay (2-3 % opacity) in the conform on the empty areas. Real texture detail needs set material work and is not cheap. |
| 9 | **Sound sits on the words.** The voice is 1 dB hot and almost continuous, the mix is loud and flat, one effect peaks over the -10 rule under a word, and the drizzle beds are inaudible. | Mix (hook entries 0.35 and 2.0 s are approved); 48.1 s gust (s20); rain beds s15, s16, s25 | voice -16.4 against -17.4; -13.9 LUFS, LRA 1.7 LU; -9.5 at 48.1 s; rain -41.5 RMS against -34 to -30 | Re-run mixer.py with voice_gain x0.89 (-1 dB), the 48.1 s thump_jab at -15 peak, and rain_drizzle at -34 RMS, then remux. No picture change. |
| 10 | **"Hardly any hurricane this fast" (beat 16) has no readable picture.** The ghost storms being overtaken are tiny and grey. | s21 | 51.0-52.0 s stills | Overlay larger ghost spinners (about 120 px, grey with the snail shell) moving at a sixth of the speed, with a short "overtake" whoosh. 2D over the existing 55 frames. |

Also noted, below the top ten:
- The framing changes every 1.06 s on the tool's reading, against 1.39 for A and 1.62 for B; the cut is busier than either reference.
- The kitchen in s15 is all warm, with blue at 6 %.
- The s05 fly-in is a full-frame smear.
- The s26 water-wall reads as clouds.
- In s18 the planned grin close-up is a neutral medium shot.
