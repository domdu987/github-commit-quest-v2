# Film production conventions (every shot agent follows these exactly)

Project root: PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj

## Authority
- What each shot shows, when, from where, with which transition: PROJ/plan/shot_plan.md and shot_plan.json (26 shots, verified). Do not redesign shots; if something is impossible, do the nearest thing and write what you changed in your QA.md.
- How to stage, pose, move the camera and render: PROJ/v3/README.md ("How to add a shot"), PROJ/v3/stage/API.md + REVIEW.md, the set API.md + REVIEW.md of the set you use, PROJ/v3/cast/API.md. The hook (shots 1-3) in PROJ/v3/shots/film.py is the worked example: copy its structure.
- Look targets: PROJ/spec/LOOK_SPEC.md section 5 (camera, staging, animation, transitions).

## Clock
- Narration: PROJ/audio/th/full_v2/narration.wav, caption phrase times in PROJ/audio/th/full_v2/narration_timing.json. The narration is laid at +0.100 s.
- Film frame g is 0-based, 30 fps, 720x1280. The film is 1965 frames (g 0..1964). A plan time t (position in the narration) falls on film frame round((t + 0.1) * 30) for in-shot events; shot boundaries t0/t1 of the plan fall on round(t * 30), so every cut leads its word by 3 frames.

## Where a take lives
PROJ/v3/film/sNN/ (NN = number of the first shot of the take, two digits), owned by ONE agent:
- shot.py: the take (camera, acting, set state per frame g), built on the helpers of PROJ/v3/shots and PROJ/v3/stage (import them; do not edit them).
- frames/g_%04d.png: FINAL picture frames, 720x1280, no captions, no audio, named by global film frame g. Include handle frames outside your own range [g0, g1) wherever your transition in or out is a dissolve: half the dissolve length plus 2 frames on that side (render them in 3D; a 2D extension is allowed only where the plan says so).
- plate/ and matte/ for the fast "streak" frames if actors are in frame (see PROJ/v3/shots/render_layers.py and post.py); deliver the frames already streaked by the same method as the hook.
- meta.json: {"take": "sNN", "shots": [..], "g0": first film frame, "g1": last film frame + 1, "handle_in": n, "handle_out": n, "transition_in": {"type": ..., "frames": n}, "set": ..., "light": ..., "samples": 12}
- cues.json: every visible event that should make a sound, with film time in seconds, duration and a label (same format as PROJ/v3/out/sfx_cues.json).
- contact.jpg (12 or more evenly spaced final frames with g and time burned in a corner strip above the picture, not on it) and QA.md (numbers: head sizes and positions, near/far ratio, registration error of pinned props, framing-change times, static and linear runs from qa_motion, popcheck, the hue_report row of your frames, light numbers where they matter, seconds per frame).

## Working order
1. Stage with numbers (probe), then 360x640 drafts at 6 samples; LOOK at a contact sheet next to the reference frames the plan names for the shot; fix.
2. Final quality only when the draft is right: 12 samples, 720x1280, a resumable render loop, at most 2 threads per process and ONE render process per agent (other agents render at the same time on this 4-core machine).
3. Check the final frames: no pops, no stale sprites, no black or magenta cards, pinned props on target, whole heads above y = 880, main head centre 0.35-0.59 of the frame height, nobody's back to the camera, mouths moving only inside the two quoted lines.

## Colour (the client's last complaint was colour)
Run python3 PROJ/v3/tools/hue_report.py <your frames folder>. Target share of chroma: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10; saturation 0.38-0.48; value 0.45-0.63; pixels darker than V 0.25: 8-15 percent. Shade must read blue-violet, never magenta. Exterior and special-light shots may differ; say why.

## Hard rules
- Write ONLY inside your own folder(s) named in your task. Sets, stage, cast, plan and other takes are read-only for you.
- No MCP or connector tools, no network calls of any kind (no fal.run, no downloads), no Freestyle, no EEVEE.
- Captions, dissolves between takes and sound are added later by the conform step; do not add them.
