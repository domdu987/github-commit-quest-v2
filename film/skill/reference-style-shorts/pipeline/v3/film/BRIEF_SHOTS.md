# Brief for shot workers

> **Example from film 1, not a template.** For a new film start from BRIEF_SHOTS.template.md. The story, the client decisions, the dated "work that already exists" and "voice was re-recorded" sections, the shot numbers and file names below belong to film 1 and are wrong for any other film. See "Adapting to a new film" in references/production.md of the skill.

PROJ = __PROJ__

You deliver finished takes of a 65 second animated film (720x1280, 30 fps, Thai narration) that must look like two reference clips (stills in PROJ/ref/a and PROJ/ref/b). The first 5 seconds are finished and approved by the client: PROJ/v3/out/proto_v3.mp4, contact sheet PROJ/v3/out/contact_v3.jpg. Your takes must look like the same film.

## Read first, in this order
1. PROJ/v3/film/CONVENTIONS.md: the rules every worker follows (clock, folders, files to deliver, colour band, hard rules).
2. The rows of YOUR shots in PROJ/plan/shot_plan.md (the verified plan: camera, acting, props, transition, sound cues, reference frames to imitate) and anything they point to in props_needed, inserts_needed and the notes (named framings such as G and the beach framing).
3. PROJ/v3/README.md, section "How to add a shot", and the worked examples: PROJ/v3/shots/film.py (the hook, shots 1-3) and PROJ/v3/film/s26/shot.py (a take delivered under the conventions).
4. The APIs of what you use: the set (PROJ/v3/set3d/API.md for the office, PROJ/v3/set3d_beach/API.md for the beach), the office extensions PROJ/v3/set3d_ext/props/API.md (props, new cameras) and PROJ/v3/set3d_ext/light/API.md (office_grey, office_storm), the cast PROJ/v3/cast/API.md, the acting library PROJ/v3/acting/API.md (talk, walk, whistle, laugh, shock, sleep, run cycles), the paper artwork PROJ/v3/paper/API.md, the staging system PROJ/v3/stage/API.md and REVIEW.md (read its limits).

## The story
September 1938, U.S. Weather Bureau. A young forecaster draws a bold red hurricane track on the wall map pointing north at New York; his boss rubs it out; he redraws it every time; the office nicknames the line "ทางด่วนพายุ" (the storm expressway); the official forecast says rain; next morning Long Island wakes to a grey drizzle and the boss gloats; then the map itself shows why the line ran north (two walls of high pressure, one corridor) and the storm rides the line into New York; people on the beach take the wall of water for a fog bank; the last image is the forecast in a newspaper on a kitchen table that still says rain.

## Client decision (final): the red line is HAND-DRAWN, not ruled
The client compared both versions of the opening and chose the first: a bold freehand stroke that wanders on its way north. The approved opening is PROJ/v3/out/proto_v3.mp4 (look at it; its line is the model). The set PROJ/v3/set3d/office3d.py is already switched (TRACK_STYLE = "hand": 85 points that wander up to 0.15 D from the straight chord, 0.038 D wide). The shot plan was written for a ruler-straight line, so read it with these changes:
- There is no ruler anywhere in the film. Ignore the ruler prop and the ruler gag: where the plan has the hero redraw the line with a ruler (shots 9 and 11) he redraws the same bold stroke freehand, as fast and sure as the first time. Where the plan says "ruled line" read "the red line".
- Never assume the line is straight. Address it only through the set API (set_track, track_point(u) which returns the local heading, the map_track anchor). Pinned props, camera paths that follow the line, the corridor of the mechanism and anything that fuses into the line must follow the points the set returns. Helpers of the shared modules that interpolate between the two ends of the track (for example _track_ext and the ruler in the props extension, T0/T1 in the mechanism module) describe the chord, not the line: do not use them to place anything on the line.
- The narration still says the line does not turn and runs north. On screen that reads against the white chalk curve that bends out to sea: keep that contrast clear in every shot that shows both.

## Folders owned by another lane (CLAIMED.txt)
To save time, some shots were handed to an extra lane before the worker first assigned to them had started. A take folder that contains a file CLAIMED.txt belongs to the lane named in that file. If your task lists such a shot and the file does not name your lane: do not write, stage or render in that folder. Return that take with complete=false, frames_rendered 0 and the note "owned by lane <name>", and spend no time on it. This is not a failure of your task. If every shot of your task is claimed by another lane, return at once.

## Work that already exists (earlier workers were interrupted)
Your folders may already hold the work of a worker who was interrupted: shot.py, sprites, drafts, stills, even finished takes. Start by listing your folders and reading what is there (shot.py, QA.md, work/). Reuse everything that is sound instead of starting over; most of it was staged for the ruled line, so re-check whatever touches the red line.
- A take that has meta.json and all its frames and never shows the red line is finished: check it (frame count, contact sheet) and keep it.
- Final, raw or plate frames that show the red line and are older than 18 Nov 14:40 show the wrong line. They were deleted already; if you find one, delete it and render it again. Never deliver a take that mixes two versions of the line.
- A render started by the interrupted worker may still be running in one of your folders. Check before you render: ps -eo pid,lstart,cmd | grep shot.py and readlink /proc/PID/cwd. If one is running in your folder and the take does not show the red line, let it finish instead of starting a second one.

## The voice was re-recorded (18 Nov 14:54): same clock, new loudness curve
PROJ/audio/th/full_v2/narration.wav is now a different voice (the new voice), fitted to the same clock: every sentence starts where it did, caption phrases moved by at most 0.24 s inside their sentence (new times in narration_timing.json). Shot ranges do not change. Only what is driven by the sound itself is affected: the mouth of the boss in shots 10 and 18. A frame of those two shots rendered by a process started before 14:54:09 on 18 Nov follows the old voice: delete it and render it again.

## How to work
- One folder per take: PROJ/v3/film/sNN/. Write only inside the folders named in your task. Shared modules are read-only: if you need a small extra prop, camera or pose, define it inside your own folder.
- Stage with numbers first (probe), then 360x640 drafts at 6 samples, LOOK at a contact sheet next to the reference frames the plan names for the shot, fix, and only then render final (12 samples, 720x1280).
- Rendering: about 18 CPU seconds per final frame. Other workers render at the same time on this 4-core machine, so run ONE render process with 2 threads, make it resumable (a frame counts as done only when its PNG and its meta exist), and start the final render as soon as the draft is right rather than polishing drafts.
- The camera is never static and never linear; every framing change the plan lists must be there, at its time.
- Mouths move only in the two quoted lines of the boss (shots 10 and 18), driven by the narration loudness helper of the acting library. Nobody shows his back. The hero never speaks.
- Pinned props (pencil, eraser, pointer, label, stamp) must sit on their world targets: use the registration helper and report the error in px.
- Colour: run PROJ/v3/tools/hue_report.py on your final frames and report the row; office_day shots must sit inside the band of CONVENTIONS.md; grey, storm, beach and map-only shots may differ, say why.
- Check the final frames yourself: view a contact sheet and at least four frames at full size per take; no pops, no stale sprites, no black or magenta cards, whole heads above y = 880.
- Disk: when a take is final, delete its draft renders and sprite caches you no longer need.
- No network, no paid APIs, no MCP or connector tools. To look at an image use the Read tool (downscale to at most 1600 px).

## Deliver per take (see CONVENTIONS.md)
frames/g_%04d.png with dissolve handles, meta.json, cues.json, contact.jpg, QA.md. Your final message is consumed by a script: return the structured result only, with absolute paths.
