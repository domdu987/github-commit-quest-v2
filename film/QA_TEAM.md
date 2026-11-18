# Picture-QA team (runs at 3 gates: SET before any render, each TAKE before conform, FINAL cut before delivery)
PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj
References: PROJ/ref/a, PROJ/ref/b (frames), film/analysis/sheets/*.jpg (8 hit shorts, 1 fps), film/analysis/DIRECTOR_REVIEW.md.
Client taste (hard rules, from the client's own feedback on films 2-8):
- SHARP image, NO depth-of-field blur anywhere (only 1-3 frames of motion streak on real whip moves).
- The client prefers the ORIGINAL look: wide/medium framings that show a beautiful DENSE set, warm lit 3D world, calm but always-moving
  camera; NOT constant extreme close-ups, NOT many text signs, NOT flat 2D infographic panels; reveals shown inside the lit 3D world.
- Thai text, if any, must render correctly (no black blobs / tofu); characters' heads fully above the caption band (y < 880 of 1280).
- Characters sit IN the world (contact shadows, correct scale, not floating, props held visibly, nothing outside cages/boxes it should be in).
- Mouths move only on quoted lines; comic falls without injury.

## QA-tech (model: sonnet) — checklist, per frame sheet
Inputs: contact.jpg / frames/ of a take (or the set contact sheet), its QA.md and meta.json, the shot plan rows it covers.
Check and list every failure with frame number: blur/DOF, heads crossing y 880, clipped sprites/props, floating feet, wrong scale,
black/magenta/blank frames, frozen runs, pops/jumps outside cuts, broken Thai text, continuity (costume, props, time of day, wall state),
mouth moving outside quotes, plan coverage (every planned beat visible at the right time).
Output: PASS or FAIL + numbered issues (frame, what, fix) in <qa_dir>/QA_TECH.md. Be strict; no praise.

## QA-art (model: opus) — aesthetic review against the references and the client's taste
Look at the frames at full size and next to the reference sheets. Score 1-10: set density/ornament, lighting & colour (warm practicals,
complementary colour, depth through light), composition/framing (shows the set, subject readable, phone-size legibility), character
acting (pose/expression reads the beat), the key moment (hook image, reveal, ending) clarity and beauty, overall match to references.
Give the 3-5 changes that would raise the lowest scores most, concretely (what, where, how). Verdict: SHIP / FIX-FIRST.
Output: <qa_dir>/QA_ART.md.

## Gates
1. SET gate: both reviewers on the set contact sheet BEFORE any team renders; director shows the client the sheet + verdict and waits
   for the client's OK.
2. TAKE gate: QA-tech on every delivered take; FAIL -> send the issues back to that render team.
3. FINAL gate: QA-tech + QA-art on the conformed film's 1 fps sheet and key frames before sending to the client.

## Stricter QA (client request, 2026-11-18) — these override anything looser above
### A. Automatic checks — film/qa_auto.py <video> --cuts <planned cut g list> --first_g <g0> (every frame, no model cost) — run on every take AND on the final cut
1. Every frame, not 2 fps: frozen runs >= 6 frames, black/blank/magenta frames, pops (frame-diff spike outside planned cuts),
   cut frames match the plan within +-2 frames.
2. Sharpness: Laplacian variance per frame vs the take median; any frame < 60 % of median = suspected blur -> list it.
3. Caption band: auto-detect faces/heads of cast cards (from the stage's projected anchor positions) -> any head y >= 880 = FAIL.
4. Colour: hue_report on 1 frame per second; shade hue 240-260 on lit sets, magenta share <= 10 %.
5. Phone-size check: make a 360x640 downscaled sheet (1 frame / 0.5 s) — the reviewers judge legibility on THIS, not full size.
### B. QA-tech (sonnet) — TAKE gate, now at 6 fps plus every cut +-3 frames
Same checklist as above, plus: hands/props attached to hands, eye-lines toward what the character looks at, prop/costume continuity
with the neighbouring takes (open the previous and next take's last/first frames), wake/smoke/water direction consistent with motion,
lip-sync only inside the quote window from captions.json (+-0.15 s).
### C. QA-art (opus) — now ALSO at the TAKE gate for key shots
Key shots = hook (first 3 s), every reveal shot, the false payoff, and the ending. QA-art must PASS them before conform.
### D. FINAL gate — four reviewers, all must pass
1. Script checks (A) on the full film.
2. Audio: per-sentence STT on the final mix vs the clean narration (every sentence >= 0.93), integrated loudness -14 to -11 LUFS (approved films measure about -12; check with ffmpeg ebur128),
   true peak <= -1 dBTP, no SFX louder than the voice inside a sentence, caption on screen within +-0.15 s of its spoken phrase,
   caption text == script text (spelling).
3. QA-art (opus) on the full-res 2 fps sheet AND the 360x640 phone sheet.
4. Blind viewer (sonnet): watches only the phone sheet + the audio transcript, with no script, and must answer correctly: what is
   strange in the hook, who mocks whom, what the mechanism is, why the ending is funny. Any wrong answer = the beat is unclear -> FIX.
### E. Overrides
The director may NOT override a FAIL alone any more. An override needs a second, independent opus reviewer that sees the frames
(not the director's opinion) and agrees; both notes go into QA_TECH.md. Every override is listed in the client report.
### F. Report to the client
Each delivery lists: what every gate checked, the numbers (STT ratios, LUFS, frozen/black counts), open non-blocking notes, and overrides.
