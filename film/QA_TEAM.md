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
