# Film 18 — rules for every render team from the TAKE gate (2026-11-19 23:15 UTC)
1. NO ZOOM PULSING. Do not add in-out punch "pulses" to raise frame-diff. Get motion from a real eased push/pull + slide, tracking, actor motion, and at most 1-2 HELD punch-ins on beats (+15-20 %, then hold). QA-art reads pulses as a zoom glitch.
2. NO UNLIT PLACEHOLDER PROPS. No grey/navy untextured slabs, planks, beams, lumps or translucent low-poly rocks anywhere in frame. Hide them or replace with lit, textured period props.
3. FLAMES ON THE TAILS. Every flame card is parented to its ox's tail tip, trails backward, never covers a face, never floats free, size capped; each lit tail has a warm point light. Fire is BEHIND the oxen (the film's key idea).
4. KEEP THE SUBJECT IN FRAME for the whole take (no slide carrying the main actor off an edge).
5. Bottom of frame: no large bare/blank ground; at most ~25 % plain ground, with dark fg props.
6. Continuity: oxen are PLAIN (no coats, no blades) in s05-s07; dragon-dressed from s01-s02 (hook flash-forward) and s16 on.
7. Characters look at what they act on (the ox, the cup, the herd), not at the lens, except a deliberate reaction glance.
Frame-diff targets stay (median >= 4, p90 >= 12) but must come from rules 1 and 4, not pulses.

## Camera recipe (added 2026-11-20 00:20 UTC): how to reach frame-diff WITHOUT pulsing
Several takes either pulsed (FAIL rule 1) or became too static once pulses were removed (s05, s06: median ~3.2, p90 ~5). Do this instead:
- DOLLY, not zoom: move the camera itself 8-10 % of the subject distance per second toward/away (e.g. subject 6 D away -> 0.5-0.6 D/s), eased in/out, AND truck sideways 0.25-0.4 D/s at the same time. Combined with a foreground prop 1-2 D from the lens, the parallax produces frame-diff p90 >= 12 on its own.
- Keep the fg prop in frame the whole shot and let it slide across (it is the main frame-diff source).
- Characters never freeze: idle sway, blinks, bounce 0.06 D at ~3 Hz when laughing; oxen tails swish, flames flicker every 2-3 frames.
- One held snap on the planned beat only (+15-20 %, eased 4-6 frames, then HOLD).
- Measure before rendering finals: draft the whole move at 180x320, compute frame-diff (90x160 grey, area), and adjust the dolly/truck speed until median >= 4 and p90 >= 12. Then render.
- Bare ground: aim the look-at so the horizon / main action sits at y 0.40-0.50 and put a dark fg prop low in frame; plain ground <= 25 %.

## Frame-diff gate clarified (director, 2026-11-20 01:05 UTC)
The client rule (production-lessons §10) is a FILM-level number: median in-shot frame-diff >= 4 and p90 >= 12 across the whole film, checked at the FINAL gate.
Per take, the TAKE gate now requires: median >= 4 (hard), no pulsing (hard), and p90 >= 9 as a guide (a take below 9 must show a visible eased dolly + slide; a take at 9-12 is fine).
High-motion shots (s10, s14, s15, s19, s21, s24, the charge) carry the film's p90. Do NOT add pulses to reach 12 in calm shots.

## Gate calibration (director, 2026-11-20 01:25 UTC)
- Rule 7 (eye-line) is a NOTE, not a blocker: this puppet style often plays to camera. Only a character who must visibly react to something (the general to the herd, soldiers to the oxen) must look at it.
- Bare ground: <= 25 % target; 25-30 % is a note; > 30 % blocks.

## Director decisions, round 12 (2026-11-20 10:30 UTC) — list these in the client report
- s19: flame-to-face relaxed from >= 60 px to "no overlap, >= 15 px gap", checked on rendered pixels (a dense herd cannot hold 60 px and still read).
- s20: lead ox 25-30 % of frame height (not 35-40 %), side view, whole head in frame, flame ends <= x 700 and >= 120 px (the cast ox is ~1.45x longer than tall, so the old framing could not fit).
- s21: dark unlit ground before the snap up to 35 % is a NOTE (deep-night opening); blur on the dark opening frames accepted as design; glints optional.
- s22: glints optional.
