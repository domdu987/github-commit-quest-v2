# Brief for shot workers

<!-- TEMPLATE. Copy to BRIEF_SHOTS.md and fill every {{...}}. Film 1's filled version is BRIEF_SHOTS.md beside this file:
     read it as the example, never hand it to a worker of another film. Delete the sections marked OPTIONAL that do not apply.
     Keep it short: every worker reads all of it. A change of course during production is an edit of this file, never a
     message to a worker. -->

PROJ = __PROJ__

You deliver finished takes of a {{FILM_SECONDS}} second animated film (720x1280, 30 fps, {{LANGUAGE}} narration) that must look like {{N_REFS}} reference clips (stills in PROJ/ref/...). The first {{OPENING_SECONDS}} seconds are finished and approved by the client: {{OPENING_MP4}}, contact sheet {{OPENING_CONTACT}}. Your takes must look like the same film.

## Read first, in this order
1. PROJ/v3/film/CONVENTIONS.md: the rules every worker follows (clock, folders, files to deliver, colour band, hard rules).
2. The rows of YOUR shots in PROJ/plan/shot_plan.md (camera, acting, props, transition, sound cues, reference frames to imitate) and anything they point to ({{NAMED_FRAMINGS}}).
3. PROJ/v3/README.md, section "How to add a shot", and the worked examples: {{OPENING_SHOT_SCRIPT}} and {{ONE_FINISHED_TAKE}}/shot.py (a take delivered under the conventions).
4. The APIs of what you use: {{SET_API_FILES}}, {{EXTENSION_API_FILES}}, the cast PROJ/v3/cast/API.md, the acting library PROJ/v3/acting/API.md, the staging system PROJ/v3/stage/API.md and REVIEW.md (read its limits).

## The story
{{STORY: 4 to 6 sentences, every beat a worker might have to show, in plain words}}

## Client decisions (final)
{{CLIENT_DECISIONS: one short paragraph per visible design choice the client settled on the opening (a line style, a caption size, a prop). Say what the plan says that no longer holds and how to read it instead. Name the set switch that implements each choice.}}

## Folders owned by another lane (CLAIMED.txt)
A take folder that contains a file CLAIMED.txt belongs to the lane named in that file. If your task lists such a shot and the file does not name your lane: do not write, stage or render in that folder. Return that take with complete=false, frames_rendered 0 and the note "owned by lane <name>", and spend no time on it. This is not a failure of your task. If every shot of your task is claimed by another lane, return at once.

## Work that already exists (OPTIONAL: only after an interrupt or a change of course)
Your folders may already hold the work of an earlier worker. List your folders and read what is there (shot.py, QA.md, work/) first; reuse what is sound.
- {{WHICH FINISHED TAKES STAY VALID}}
- {{WHICH FRAMES ARE WRONG: "frames that show X and are older than <date time>"}}
- A render started by an earlier worker may still be running in one of your folders. Check before you render: ps -eo pid,lstart,cmd | grep shot.py and readlink /proc/PID/cwd. If one runs in your folder and its frames are still valid, let it finish instead of starting a second one.

## How to work
- One folder per take: PROJ/v3/film/sNN/. Write only inside the folders named in your task. Shared modules are read-only: if you need a small extra prop, camera or pose, define it inside your own folder.
- Stage with numbers first (probe), then 360x640 drafts at 6 samples, LOOK at a contact sheet next to the reference frames the plan names for the shot, fix, and only then render final (12 samples, 720x1280).
- Rendering: about 18 to 23 CPU seconds per final frame. Other workers render at the same time on this {{N_CORES}}-core machine, so run ONE render process with 2 threads, make it resumable (a frame counts as done only when its PNG and its meta exist), start it detached (nohup), and stage your next shot while it renders. Never return while a render of yours is running: wait for it and finish the take.
- The camera is never static and never linear; every framing change the plan lists must be there, at its time.
- Mouths move only in {{QUOTED_LINES: which shots, driven by the narration loudness helper of the acting library}}. Nobody shows his back. {{OTHER ACTING RULES}}
- Pinned props ({{PINNED_PROPS}}) must sit on their world targets: use the registration helper and report the error in px.
- Colour: run PROJ/v3/tools/hue_report.py on your final frames and report the row; {{WHICH LIGHTS}} must sit inside the band of CONVENTIONS.md; {{WHICH SHOTS MAY DIFFER}} may differ, say why.
- Check the final frames yourself: view a contact sheet and at least four frames at full size per take; no pops, no stale sprites, no black or magenta cards, whole heads above y = 880 (the caption band is y 880 to 950).
- Disk: when a take is final, delete its draft renders and sprite caches you no longer need.
- No network, no paid APIs, no MCP or connector tools. To look at an image use the Read tool (downscale to at most 1600 px).

## Deliver per take (see CONVENTIONS.md)
frames/g_%04d.png with dissolve handles, meta.json, cues.json, contact.jpg, QA.md. Your final message is consumed by a script: return the structured result only, with absolute paths, and complete=true only for a take whose final frames, meta.json and QA.md all exist.
