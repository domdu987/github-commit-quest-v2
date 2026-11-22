## K. NOTHING FLOATS: automatic ground check plus an independent float hunter (2026-11-21, BLOCKING)
The client complained again about films 18 and 20: "มุมกล้องของลอยอีกแล้ว". §G-2 was judged by eye by the same team that made the shots, and it missed:
- film 18 6 s: flat discs and flags hovering over the field
- film 18 29 s: soldiers with no feet or ground behind pots
- film 18 51.5 s: the ox's shadow detached and lying to the side; bundles hanging in the air
- film 18 54 s: black soldier silhouettes standing on nothing
- film 20 7.5 s: a canopy/table with no legs; a tower-leg slab hovering
- film 20 11 s: a girder chunk in the sky
- film 20 52.5 s: people on cobbles with no contact shadow
- film 20 57 s: a giant bald head blocking the foreground

New mandatory steps:
1. **ground_check (automatic, before every render).** Run film/v3/tools/ground_check.py on the shot scene. It samples every 10th frame. For every character card and prop that is not flagged `airborne=True` (birds, thrown things, flags on poles, smoke), it ray-casts down from the object's lowest point. It fails when the gap to the first surface is more than 2 cm in scene units, or when nothing is below the object. Fix the scene (snap to ground) until it passes. Commit the report as GROUND.md with the take.
2. **Contact shadows.** Every character card and free prop gets a soft contact shadow (a blob or shadow catcher) under its feet or base. Nobody stands on nothing.
3. **Float hunter (independent).** At the TAKE gate and again at the FINAL gate, a fresh reviewer that did not plan or render the shot gets ONLY the 1 fps sheets (scale 270x480, timestamps) and one question: "List every person or object that floats, has no contact with a surface, has a detached shadow, or is cut weirdly by the frame or foreground." Any item listed blocks the shot until fixed or explained (e.g. mid-jump).
4. **Producer check.** Before a film is sent to the client, the producer looks at 1 fps sheets too. A float found there sends the film back.

## §L NO CAMERA SHAKE (client complaint 2026-11-21: "มุมกล้องมันสั่น")
Measured with `python3 film/qa_jitter.py film.mp4` (per-second median frame-to-frame jitter, px at 720x1280):
- film 18: shaky at 13-17 s, 33-39 s (up to 7.4 px), 48-50 s, 54-62 s. Film 20: 10-12 s, 27-31 s, 46-54 s.
- reference R2: 0.26 px overall and no shaky seconds. R5 (storm) shakes only 2 s.
Rules (blocking at the TAKE and FINAL gates):
1. Camera moves are smooth: travel, dolly, crane and BIGZOOM with eased keys. No random pan or tilt keys and no LINEAR noise.
2. `camrig.shake()` is allowed only for a motivated impact (explosion, crash, stampede hit). Use amp_deg ≤ 0.15, at most 0.6 s per use, and at most 2 uses per film.
3. Every second of the final film must measure ≤ 2.0 px in qa_jitter.py, except the declared impact moments, which are listed in GROUND.md. Paste the qa_jitter output with the take.
