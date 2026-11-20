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

## QA_TEAM §G (producer, client complaint on films 15/17; 2026-11-20 11:40 UTC) — applies to every remaining take and the FINAL gate
- Colour: saturation >= 0.47 and luma 85-110 (film 2: 0.49 / 94). Director measured the staged takes: film mean 0.481 / 93.3 (passes), but s05 s06 s08 s09 s10 s11 s12 s13 s17 s23 are 0.37-0.44 and the night shots s16 s17 s18 s20 s21 s23 are luma 70-82. The director applies a per-shot eq grade at conform (conform18.py grade_filter) so every shot reaches sat >= 0.48 and luma 87-108; QA-art judges the graded film side by side with film 2 at FINAL. Remaining takes: keep saturated reds/blues, no haze; do not crush the night darker than the passed s14/s15.
- Nothing floats: feet/bodies on a surface with contact shadow, no poles/props through faces, no debris hanging still in mid-air. QA-art checks every 0.5 s phone tile.
- Camera distance: no face taller than 35 % of frame height, no character cut in half by an edge, >= half the shots wide/medium-wide.
- FINAL: side-by-side sheet with film 2; "as vivid, wide and grounded as film 2?" — a "no" blocks release.

## QA_TEAM §H (client decision via producer, 2026-11-20 12:00 UTC): BIGZOOM, angles, rich set — blocking at FINAL
- Two BIGZOOMs re-planned in shot_plan.md: s01 (now 0-156, merges old s01+s02; team 1) and s26 (team 2). One continuous eased move, 3-6 s, from EXTREME WIDE (character < 5 % of frame height, findable) through set detail to MEDIUM (character 35-60 % of frame height). No cut, no pulsing.
- TAKE gate for BIGZOOM: measured start height < 5 %, end 35-60 %, duration of the zoom 3-6 s, the set rich (roofs, lanterns, oxen, smoke, flags) at every stage, nothing floats, caption band clear at the end.
- Old s01, s02 and s26 PASSED takes stay as fallback until the new takes pass; the old s02 is dropped when the new s01 passes.

## QA_TEAM §I (client decision via producer, 2026-11-20 12:48 UTC): match the reference Shorts — blocking at FINAL
- Hard cuts: <= 12, target 4-10. Film 18 after the s01+s02 merge has 14 hard joins; 5 same-location joins become in-camera whips at conform (film18/qa/whips.json: s04, s07, s10, s15, s22) -> 9 hard cuts.
- Colour: film saturation >= 0.50 and vivid >= 45 % (qa_stats2.py); the conform grade now targets 0.54 per shot. Signature colours: fire orange-red + moon blue.
- Lighting: every remaining take (s19 s20 s21 s22 s24 and the BIGZOOMs s01, s26) needs a motivated key (fire / torches / lanterns / dawn sun), a RIM light on characters and oxen, and warm+cool in the same frame.
- Text signs are now ALLOWED: short in-world signs are welcome (e.g. a gate plaque 即墨 / "JIMO" on the gate in the BIGZOOMs).
- Characters always act; close-ups only as ~1 s punctuation (max 3).
- FINAL: the contact sheet next to two reference sheets; "same channel?" — a "no" blocks.

## Director decisions, round 14 (2026-11-20 13:50 UTC) — list in the client report
- s22: the terrified Yan soldier is REMOVED from s22 (after 6 rounds his position kept making the ox's tail flame read as his torch). s22 becomes a pure close-medium hero shot of the ox: dragon silk, blades glinting, flame tail clearly attached behind it. The soldiers' shock is carried by s21.
- s24: the second fall may be a NEW foreground soldier placed in clear ground; the chariot pole may be hidden.
- s01: the basket carriers may be removed.

## Ground metric is now ONE shared script (director, 2026-11-20 14:40 UTC)
`python3 film/film18/qa/ground_share.py take.mkv <first_g> <g0> <g1> [step]` — plain = low-saturation, mid-value, UNTEXTURED (9x9 std < 6) pixels below y 0.40, as a share of the whole frame. Gate: max <= 0.30 (every 10th frame). Teams and QA both use this number; dressed/textured ground (stones, straw, props, ruts) does not count as plain. Visual "does it look empty?" stays a QA-art note, not a ground-% blocker.
