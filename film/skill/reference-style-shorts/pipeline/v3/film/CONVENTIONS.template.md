# Film production conventions (every shot agent follows these exactly)

<!-- TEMPLATE. Copy to CONVENTIONS.md and fill every {{...}}. Film 1's filled version is CONVENTIONS.md beside this file.
     The colour band below is the acceptance band of the bundled look spec (references/look.md); replace it only if the new
     references were measured as a different style. -->

Project root: PROJ = __PROJ__

## Authority
- What each shot shows, when, from where, with which transition: PROJ/plan/shot_plan.md and shot_plan.json ({{N_SHOTS}} shots, verified). Do not redesign shots; if something is impossible, do the nearest thing and write what you changed in your QA.md.
- How to stage, pose, move the camera and render: PROJ/v3/README.md ("How to add a shot"), PROJ/v3/stage/API.md + REVIEW.md, the set API.md + REVIEW.md of the set you use, PROJ/v3/cast/API.md. {{OPENING_SHOT_SCRIPT}} is the worked example: copy its structure.
- Look targets: PROJ/spec/LOOK_SPEC.md section 5 (camera, staging, animation, transitions).

## Clock
- Narration: {{NARRATION_WAV}}, caption phrase times in {{NARRATION_TIMING_JSON}}. The narration is laid at +{{AUDIO_OFFSET}} s.
- Film frame g is 0-based, 30 fps, 720x1280. The film is {{N_FRAMES}} frames (g 0..{{N_FRAMES_MINUS_1}}). A plan time t (position in the narration) falls on film frame round((t + {{AUDIO_OFFSET}}) * 30) for in-shot events; shot boundaries t0/t1 of the plan fall on round(t * 30), so every cut leads its word by about 3 frames.

## Where a take lives
PROJ/v3/film/sNN/ (NN = number of the first shot of the take, two digits), owned by ONE agent:
- shot.py: the take (camera, acting, set state per frame g), built on the helpers of PROJ/v3/shots and PROJ/v3/stage (import them; do not edit them).
- frames/g_%04d.png: FINAL picture frames, 720x1280, no captions, no audio, named by global film frame g. Include handle frames outside your own range [g0, g1) wherever your transition in or out is a dissolve: half the dissolve length plus 2 frames on that side.
- plate/ and matte/ for the fast "streak" frames if actors are in frame (see PROJ/v3/shots/render_layers.py and post.py); deliver the frames already streaked.
- meta.json: {"take": "sNN", "shots": [..], "g0": first film frame, "g1": last film frame + 1, "handle_in": n, "handle_out": n, "transition_in": {"type": ..., "frames": n}, "set": ..., "light": ..., "samples": 12}
- cues.json: every visible event that should make a sound, with film time in seconds, duration and a label.
- contact.jpg (12 or more evenly spaced final frames with g and time in a strip above the picture) and QA.md (head sizes and positions, near/far ratio, registration error of pinned props, framing-change times, static and linear runs from qa_motion, popcheck, the hue_report row, light numbers where they matter, seconds per frame).
- Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. Never render or add a background blur; the motion streak on fast camera moves stays.

## Working order
1. Stage with numbers (probe), then 360x640 drafts at 6 samples; LOOK at a contact sheet next to the reference frames the plan names for the shot; fix.
2. Final quality only when the draft is right: 12 samples, 720x1280, a resumable render loop, at most 2 threads per process and ONE render process per agent.
3. Check the final frames: no pops, no stale sprites, no black or magenta cards, pinned props on target, whole heads above y = 880, main head centre 0.35-0.59 of the frame height, nobody's back to the camera, mouths moving only where the brief allows.

## Colour
Run python3 PROJ/v3/tools/hue_report.py <your frames folder>. Target share of chroma: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10; saturation 0.38-0.48; value 0.45-0.63; pixels darker than V 0.25: 8-15 percent. Shade must read blue-violet, never magenta. {{WHICH SHOTS MAY DIFFER (exterior, night, storm, map inserts) and why}}

## Hard rules
- Write ONLY inside your own folder(s) named in your task. Sets, stage, cast, plan and other takes are read-only for you.
- No MCP or connector tools, no network calls of any kind, no Freestyle, no EEVEE.
- Captions, dissolves between takes and sound are added later by the conform step; do not add them.
