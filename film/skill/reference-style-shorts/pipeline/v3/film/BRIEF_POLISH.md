# Brief for the polish pass: film v1.1

> **Example from film 1, not a template.** For a new film copy it and rewrite: "Where we are" (your v1 review's findings), the frozen paths, and the per-shot instructions. The structure (frozen folders, the build order, the rules) is generic. See "Adapting to a new film" in references/production.md of the skill.

PROJ = __PROJ__

## Where we are
The 65.5 s film is finished and delivered as version 1: PROJ/deliver/film_v1_thai.mp4 (720x1280, 30 fps, 1965 frames, Thai voice, Thai captions, music, effects). An independent review compared it with the two reference clips: PROJ/deliver/QA_film.md (read sections 1.1, 3 and 4 now) and PROJ/deliver/film_vs_reference.jpg (look at it now). The client's standing requirement is that the film looks like the reference in LIGHT, DEPTH, camera angle and colour. Camera and edit already match. The difference a viewer sees first is:
1. LIGHT: no glow. Light sources are flat white discs, highlights are clipped, contrast is low (p95-p5 0.50 against 0.60-0.62), the top of the frame is dark.

Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. Do not blur backgrounds in 2D or in the render; the motion streak on fast camera moves stays as it is in v1.

Version 1.1 fixes the light and the cheap items of the review's ranked list, WITHOUT any new render: everything is 2D work on the v1 conform frames.

## Frozen: never write here
- PROJ/deliver/film_v1_thai.mp4 and everything else already in PROJ/deliver/.
- PROJ/v3/film/out/ (the v1 conform, mix and review).
- PROJ/v3/film/sNN/frames/ and PROJ/v3/out/frames/ (the delivered picture of the takes and of the hook), and every take's shot.py, meta.json, cues.json, QA.md.
- Sets, cast, acting, plan, audio.
Read them, import them, copy them; do not change them.

## Must not change in v1.1
The clock (1965 frames, every cut and transition where it is), the story and acting, the hand-drawn red line, the captions (same 104 phrases, same times, same font and size fs88, same position, burned last on top of everything), the voice (the new voice), the music file and its level (-38 dBFS RMS), the content of the first 5 seconds.

## How v1.1 is built
All new work goes under PROJ/v3/film/out_v11/. The final file is PROJ/deliver/film_v1_1_sharp_thai.mp4 (film 1 first delivered a v1.1 with an added background blur, PROJ/deliver/film_v1_1_thai.mp4; the client had the blur removed, so that file is not the result).

1. INPUT: the v1 conform frames PROJ/v3/film/out/frames/g_%04d.png (1965 frames, no captions; the same joins and overlays as v1). No new conform is needed.
2. GRADE v1.1, after the conform and before the captions: PROJ/v3/film/out_v11/grade.py with one entry point grade_frame(img, g) -> img, applied to every conformed frame, result in out_v11/graded/. It holds:
   - a global light pass: bloom on light sources and bright areas, a gentle S-curve, a little warm haze in the far distance of the exteriors. Targets from QA_film.md 1.1, measured with the same score.py: contrast p95-p5 into 0.60-0.75, share of pixels with V > 0.95 into 0.02-0.09, top-third mean luma into 85-135, middle-third into 105-150, saturation mean into 0.40-0.60, while the hue band of the office shots stays inside the band of PROJ/v3/film/CONVENTIONS.md and the faces (near white already) do not clip further (head fill V stays at or under 0.995);
   - per-shot corrections for the shots the review marks: s16 (washed out), s19, s20, s21 (cold and diagram-like), s25 (too dark to read), and others only if cheap;
   - overlays: a readable fog bank in s23 (55.9-57.3 s), and if cheap the larger ghost storms in s21;
   - a fine grain on empty flat areas, if it helps the edge-density measure without shimmer.
   Grade settings that differ between two shots must cross-fade over the dissolve between them (the join list is PROJ/v3/film/out/work/joins.json), so nothing jumps.
3. CAPTIONS and encode: the same caption script as v1 (PROJ/v3/film/out/film_silent.ass) burned on the graded frames with the same encoder settings -> PROJ/v3/film/out_v11/film_silent_sharp.mp4. PROJ/v3/film/out_v11/make_sharp.py does steps 2 and 3 in one pass without intermediate video files: it grades every frame in 3 processes, writes out_v11/graded/, pipes the frames into ffmpeg with the ass filter, then muxes the v1.1 mix.
4. SOUND v1.1: a copy of PROJ/v3/film/out/mix_film.json in out_v11/ with three changes only: the voice 1 dB lower (active RMS about -17.4 dBFS), the gust thump at 48.1 s low enough that nothing but the voice is over -10 dBFS there, and the drizzle beds audible (about -34 dBFS RMS with their peaks limited so that no ambience peak is over -14). Music untouched. Mixed with PROJ/audio/mixer.py -> out_v11/film_mix.wav, muxed -> PROJ/deliver/film_v1_1_sharp_thai.mp4.

## Rules for every worker
- Write only where your task says. Report what you changed, with file paths.
- No paid services, no downloads, no MCP tools. Everything is local: Python, numpy, PIL, ffmpeg.
- The machine has 4 cores: at most 3 grading processes. Start a full-film pass detached with nohup when it will run longer than a few minutes, and never return while it is still running: wait for it.
- Look at what you make. For every changed shot view at least one before/after pair at full size, and one strip of consecutive frames for flicker.
- If something cannot be done cheaply, leave that item at its v1 state and say so. A clean v1.1 with fewer changes is worth more than a v1.1 with one visible artifact.
- Write short, plain reports: what was done, the numbers, what is still wrong.
