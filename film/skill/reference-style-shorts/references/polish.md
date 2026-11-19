# Phases 8 and 9: the review and the polish pass

Sharp picture: no depth-of-field or background blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. The motion streak on fast camera moves (whips, snaps) is part of the style and stays.

Version 1 of the film scored a likeness index of 0.980 while the light was visibly off. The polish pass to version 1.1 is the grade, the story overlays, the corrected mix and the two reviews, with no new render: it brought the index to 0.993 (score.py on the delivered sharp v1.1), all five light rows inside the reference range, and the cold map sequence from 46-67 % blue down to 19-31 %. The delivered version 1.1 (`deliver/film_v1_1_sharp_thai.mp4`) is the sharp v1 picture with the v1.1 grade, captions and sound. Shot tally "same film as the reference" in the reviews: v1 15 yes / 9 partly / 2 no; sharp v1.1 16 / 9 / 1 (inferred from the v1.1 review with its blur remarks taken out).

## 1. The independent review of version 1

- One reviewer, not the builders, measures v1 with the same tools as the analysis (`pipeline/v2/eval/score.py`, `pipeline/v3/tools/hue_report.py`, `pipeline/v3/shots/qa_parallax.py`, the edit grammar), puts frames side by side with the reference, checks the story from the picture with the sound off, and ranks the remaining differences by how much a viewer would notice, each with a cheapest fix. Worked example: `references/examples/QA_film.md`.
- **Read the out-of-range rows and the side-by-side frames, not the index.** v1 had 0.980 with contrast 0.50 against 0.60-0.62, highlights 1.2 % against 5-6 %, a dark top of frame and a cold 15 second sequence.
- Deliver version 1 to the user at once with that list. Then build version 1.1 without touching version 1: everything new goes into a new folder (`out_v11/`), and the brief names what is frozen (`pipeline/v3/film/BRIEF_POLISH.md`). Template: `workflows/14_polish_pass_v1_1.js`.

## 2. The grade

`pipeline/v3/film/out_v11/grade.py`, entry point `grade_frame(img, g)`, applied to the v1 conform frames (`out/frames/`) before the captions; stateless, so frames can be graded in parallel processes and in any order. GRADE.md has every parameter and the numbers. Stages: per-shot corrections that cross-fade over dissolves with the conform's own weight; one hue-preserving S-curve; a vibrance-style saturation lift; warm haze on the far pixels of exteriors; bloom on hot light sources plus a weak wide glow of bright areas, at fixed thresholds with no frame-adaptive normalisation (so it cannot pump); a fog-bank overlay where the story needs one; protection of strong reds and of near-white fills; a soft ceiling on highlights. Targets came from the review's out-of-range rows (contrast p95-p5 0.60-0.75, V > 0.95 share 0.02-0.09, top-third mean luma 85-135, middle third 105-150, saturation 0.40-0.60, head fill V at most 0.995) while the office shots stay inside the hue band. Measure with the same `pipeline/v2/eval/score.py` call as the review.

## 3. Captions, encode and sound in one pass

`pipeline/v3/film/out_v11/make_sharp.py` is the example of grading and encoding without intermediate files: it grades the 1965 conform frames in 3 processes, writes each graded frame to `out_v11/graded/`, pipes the frames straight into ffmpeg with the v1 caption file (`out/film_silent.ass`, libx264, crf 18), then muxes the v1.1 mix into `deliver/film_v1_1_sharp_thai.mp4`. Run it from its own folder; it needs `out/frames/`, `out/film_silent.ass`, `out_v11/film_mix.wav` and `fonts/`.

The mix is the v1 mix with three corrections (`out_v11/sound/build_v11.py`, `out_v11/mix_film.json`): voice 1 dB lower (active RMS about -17.4 dBFS), the one effect that peaked over -10 under a word turned down, the drizzle beds raised to about -34 dBFS RMS with their peaks limited to -14.

## 4. Two reviews in parallel, one fix round, a re-check

- **Look reviewer**: compares v1.1 with the reference and with v1, with the same measures and triptychs (v1 | v1.1 | nearest reference still) for every shot. Worked example: `references/examples/QA_film_v1_1.md` (read its note at the top: it reviewed a withdrawn cut, and its blur remarks have been taken out).
- **Artifact hunter**: assumes something is broken and hunts for it: ink inside faces, halos, flicker on static tiles, pops at joins, seams, washed-out faces, caption legibility, audio stems. The look reviewer saw one 4-frame ghost face (s11 g740-743) and traced it to the grade; the artifact hunter measured that the bloom greys the ink in every face (face-ink luma up by 0.07 to 0.10 in every take with faces except s16). Only the measurement showed it was the whole film, not one shot. Always run it.
- Fix round, then a re-check of each fault by number. The grade faults were fixed in `out_v11/grade.py` (parameters in `GRADE.md`, section "Fix round"): (1) the s11 ghost face and (2) the grey face ink, both by keeping the bloom out of near-white fills, closed over their dark features; (3) the flicker of the sunlit floor, by gating hot sources by saturation.

## Pitfalls found in the polish pass

1. **Bloom**: keep the glow out of near-white fills (faces, hands, paper) or the ink inside them turns grey. Gate "hot" sources by saturation, or a sunlit orange floor that sits on the threshold flickers between frames. Cross-fade bloom settings over dissolves.
2. **A take script edited after its render no longer matches the picture.** Take the camera from the render's own per-frame meta, not from the current `shot.py`.
3. **A lifted-shadow grade for a dark shot lifts the black ink of the characters too.** Mask the ink or accept grey ink there (s25: face-ink 0.20 -> 0.31, accepted for a storm shot that was too dark to read).
4. **The colour band of the references is a property of whole scenes with characters.** Map inserts, diagrams, night and storm shots fall outside it by design; say so in the QA instead of forcing them in. But do not let an explainer sequence go cold for 15 seconds: light it with the room's warm key.
5. **Do not add effects the client did not ask for.** The first v1.1 added a background blur because a review listed it as a difference from the reference; the client had it removed. Before adding a new kind of effect in a polish pass, show it on one shot and ask.

## What it cost

No paid services. The grade about 5 to 7 minutes for 1965 frames in 3 processes (make_sharp.py: grade, captions and encode in one pass); reviews and fix round most of the wall time.
