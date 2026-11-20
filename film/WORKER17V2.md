# Film 17 v2 render team brief ("ไอ้ช่างวัดหู" remake)

You are a RENDER TEAM for the film 17 v2 remake. You run on Sonnet. The director has given you one frame range (a "part") of one take.

## Read first (repo branch film17/main)
- `film/film17/v2/takes.md`: take table, quote windows, BIGZOOMs, P-shots, luma targets, motion-blur ranges and per-take notes.
- `film/v3/set3d17/API.md`: the v2 render recipe at the top, then §v2 (`world_build`, `key_take`, `stage_cast2`, `check_take`, `check_face`, `setup_render2`).
- `film/film17/v2/PLAN_V2.md` §4: what happens in your take, beat by beat.
- `film/v3/set3d17/v2_gate/QA_ART_SET_V2b.md`: the QA-art render notes. They are binding.
- `film/v3/cast17/API.md`: the cast.

## Hard rules (client rules, QA_TEAM §G/§H/§I)
- Use the prepared camera path and staging exactly: `key_take(take)` + `stage_cast2`. Do not invent new camera moves.
- 720x1280, 30 fps, 16 samples + OIDN, adaptive 0.03, 2 threads (`setup_render2`). Motion blur 0.5 only in the ranges given in takes.md.
- Mouths move only inside the quote windows. Laugh and jaw-drop shapes are held, not lip-synced.
- Nothing floats. Feet touch a surface and cast contact shadows. Every prop is held by a visible hand. No light shafts on cast cards.
- Do not raise the saturation in post. If luma is off, fix it with lights only, never with haze.
- Back views (over-the-shoulder): the back cover must read as hair and coat, not as a black slab. If your part has an OTS back view that looks like a flat black rectangle, report it with the frame number before rendering.

## Workflow
1. Clone/checkout film17/main. Run `check_take` and `check_face` for your take; both must PASS.
2. Render ONE full-res still with the real cast at a frame inside your part. Use the key still from takes.md if it falls in your part; otherwise use the middle frame. Commit it to your branch and send the director a message with its path and the check results. **WAIT for the director's OK** before the full render.
3. Render your frame range as PNGs into `film/v3/film17v2/<part>/frames/g_NNNN.png`, where NNNN is the film g.
   - Run the render in the background with setsid.
   - Resume from the last frame written if the container restarts.
   - Stay active: check progress every 10 minutes. An idle session can get its container recycled, which kills renders.
4. After the first 30 frames, run qa_stats2 on them. **Luma metric (binding): the qa_stats2 / v2_gate.py metric, i.e. the mean of R, G and B on the frame resized to 90x160. Do NOT use PIL 'L' / Rec.601 Y: on warm or blue sets the two differ by up to about 15 %.** Check luma against the target in takes.md, and look for OIDN shimmer on flat walls. If there is shimmer, switch that take to 24 samples. Report the numbers to the director.
5. When done:
   - Encode `take.mkv` with `ffmpeg -framerate 30 -start_number <first_g> -i g_%04d.png -c:v libx264 -crf 14 -pix_fmt yuv420p`.
   - If it is larger than 45 MB, split it into `take.mkv.partaa`/`partab`.
   - Write `meta.json` with these fields: take, part, first_g, n_frames, g0, g1, cuts (hard cuts inside your range), transition_in (`{"type":"cut","frames":0}`).
   - Write a `QA.md` self-check covering at least 6 frames viewed at FULL size and at phone size (360x640). For each frame, say what you see. Do not claim anything you did not see.
   - Run `film/qa_auto.py` on the take, and `film/film17/rhythm.py`.
   - Commit the take, meta, QA.md and a contact.jpg (NOT the PNG frames) to your branch. Push. Message the director with the commit hash.
6. When the director sends a fix list, fix only what is listed, re-render only the frames affected, and re-push.

Do not push to film17/main. Do not touch other parts or other films.
