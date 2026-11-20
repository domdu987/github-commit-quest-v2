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
4. Blind viewer (sonnet): watches only the phone sheet + the narration as heard (timed sentence text; an automatic Thai transcript is too noisy and made the test fail for the wrong reason), with no beat labels or brief, and must answer correctly: what is
   strange in the hook, who mocks whom, what the mechanism is, why the ending is funny. Any wrong answer = the beat is unclear -> FIX.
### E. Overrides
The director may NOT override a FAIL alone any more. An override needs a second, independent opus reviewer that sees the frames
(not the director's opinion) and agrees; both notes go into QA_TECH.md. Every override is listed in the client report.
### F. Report to the client
Each delivery lists: what every gate checked, the numbers (STT ratios, LUFS, frozen/black counts), open non-blocking notes, and overrides.

## G. Client complaints after films 15 and 17 (2026-11-20) - blocking at TAKE and FINAL gates
Producer review vs film 2 (sky_poker_v3) found:
- film 15: saturation 0.44, brightness 132 (washed-out peach haze).
- film 17: saturation 0.38 (dull brown/navy).
- film 2: saturation 0.49, brightness 94.

1. **Colour:** mean saturation >= 0.47 (max-min/max over the frame, as in the producer's stats.py) and mean luma 85-110. Use clear blue skies or deep night, and saturated primaries (red roofs, green fields, blue water). No peach haze over the whole frame.
2. **Nothing floats:**
   - Every character's feet or body touches a surface with a contact shadow.
   - No heads or bodies hanging in the sky (film 15 had heads floating above the sand pit and stands).
   - No bars, poles or props passing through a face.
   - Characters are not sliced by grey slabs.
   - No debris hanging in mid-air without motion.
   - QA-art must check this on EVERY 0.5 s tile of the phone sheet.
3. **Camera distance ("กล้องสั้น" = too close):**
   - At least half the shots are wide or medium-wide, showing the place, as in film 2's town and tower shots.
   - No face taller than about 35 % of the frame height, i.e. no extreme close-ups (film 17 had several).
   - No character cut in half by a frame edge.
   - Do not repeat one room angle more than 3 times in a row.
4. FINAL gate: add a side-by-side contact sheet with film 2. One reviewer must answer "is it as vivid, wide and grounded as film 2?" A "no" blocks release.

## H. Client decision 2026-11-20: big zoom, interesting angles, rich 3D (EVERY film, blocking)
The client's words: "ทุกเรื่องเลยนะคือมันต้องมีฉากซูมไกลมาก เข้ามาหาตัวละครด้วย มุมกล้องให้น่าสนใจ ฉาก3d สวยละเอียด"

1. **Big zoom (at least 2 per film):**
   - One continuous camera move (not a cut) that starts EXTREME WIDE and ends on the character.
   - The start shows the whole town, valley, stadium or city from high and far, with the character tiny (under 5 % of frame height) but findable.
   - The end is a medium shot of the character (35-60 % of frame height).
   - It lasts 3-6 s with ease-in/out and passes through set detail (roofs, trees, crowds, foreground props) on the way in.
   - Use one at the opening (hook) and one at the reveal or ending. Mark them in shot_plan.md as BIGZOOM.
2. **Interesting angles:**
   - Each film uses at least 4 different angle types from: high/bird's-eye, low hero angle, over-the-shoulder, through a foreground frame (window, doorway, crowd, bars), top-down, side tracking, crane up/down.
   - No more than 2 shots in a row at the same height and angle.
   - Avoid flat, eye-level, straight-on framing as the default.
3. **Beautiful, detailed 3D set:**
   - Dense props and life: people, animals, smoke, flags, lights.
   - Layered depth (foreground / mid / far), textured surfaces and warm/cool lighting contrast.
   - No empty flat ground planes or bare backdrops.
   - QA-art scores the set "rich and detailed?". A "no" blocks the SET gate.
4. At the FINAL gate, list the BIGZOOM timecodes and the angle types used. A film missing them is blocked.

## I. Client decision 2026-11-20: match the reference Shorts in film/ref_shorts/ (EVERY film, blocking)
The client: "ได้ทุก ทำอะไรก็ได้ที่ออกมาเหมือนคลิปที่ผมส่งให้". Study film/ref_shorts/ (videos, sheets and README) before planning.

1. **CAMERA TRAVELS INSTEAD OF CUTTING.** At most 12 hard cuts per film; the target is 4-10. Move between places and beats with continuous camera travel:
   - follow a walking character through the set (R3 office)
   - crane up and out from a character to reveal the whole ship or town, then swoop on (R5)
   - push THROUGH an object (door, window, clock, porthole) into the next scene (R3, R5)
   - ride along with a vehicle or object (R7 coaster, R1 car interior)
   - whip-pan or match-dissolve only where travel is impossible

   Build connected sets so the camera can travel between locations. Render long takes of 5-15 s.
2. **LIGHTING TELLS THE STORY.** Every scene has a visible motivated key light:
   - light shafts or god rays through windows (R6, R3)
   - lamps or candles in dark rooms (R4)
   - neon reflected on wet ground (R2)
   - floodlights or headlights at night (R1, R7)

   Also required: a rim light on characters so they pop off the background, and warm and cool in the same frame. No flat even light.
3. **SIGNATURE COLOUR.** Each film picks 1-2 bold dominant colours, for example R6 hot pink, R5 deep storm blue, R2 neon purple/pink. Film saturation ≥ 0.50 and vivid % ≥ 45 (qa_stats2.py). No haze.
4. **TEXT SIGNS ARE NOW ALLOWED.** This lifts the old no-text-signs rule. Use short in-world English or Thai signs and labels that tell the viewer where we are or what a thing is, like PRIZE COUNTER, STORM OIL, CAREER DEVELOPMENT ROOM. Keep them sharp and readable on a phone.
5. **CHARACTERS ALWAYS ACT.** In every shot someone is doing something: walking, pouring, carrying, sitting cross-legged, knitting. Give them props in hand, expression changes (smile, shock, red angry face) and secondary motion. Nobody stands still for more than 1.5 s.
6. **CLOSE-UPS AS PUNCTUATION ONLY.** A fast push into a face on a punchline is fine: about 1 s, at most 3 per film. Everything else is wide or medium inside a rich set (see §G and §H).
7. **FINAL GATE.** Put the film's contact sheet next to two reference sheets. One reviewer answers: "Would a viewer believe this is from the same channel?" A "no" blocks release.

## J. Hook rules from the reference Shorts (2026-11-20). For every NEW script (film 22 on); the blind test checks them
How the 8 reference clips open, transcribed with STT:
- R1: "If you plant a tree beside an empty road, cars will steer right into it." (paradox)
- R2: "Gambling is illegal in Japan, yet there's a gambling hall on almost every street." (paradox)
- R3: "It's impossible to get fired in Japan, but companies found something way worse." (paradox + threat)
- R4: "They buried a man alive with a bell tied to his finger." (shocking action)
- R5: "He poured cooking oil into the sea with a pirate ship so close behind them, he could hear the pirates laughing." (weird action + danger in ONE sentence)
- R6: "They painted the jail cell pink, and not just any pink." (weird action + precision)
- R7: "He bent the rollercoaster's loop out of shape." (weird deliberate action)
- R8 (Thai, PANDA STORY): "วิศวกรคนนี้จงใจเว้นช่องว่างระหว่างรางรถไฟทุกๆ 39 ฟุต" (deliberate + exact number)

Rules:
1. **Sentence 1 runs 3.5 s or less.** It is [someone] + [a DELIBERATE weird act with a concrete object or number] + [danger, stakes or paradox].
   - Words that work: "จงใจ", "ทั้งที่ ...", "... ผิดกฎหมาย แต่ ...".
   - Never open with the mocker or the village laughing (film 14 did; that is weaker).
2. **After "คืออย่างนี้นะ" ("you see"), never start with a date or place** ("อเมริกาปี 1963" kills momentum). Continue with a vivid concrete image ("ถนนตรงยาวหลายไมล์ และมีต้นไม้อยู่ต้นเดียว") and slip the date in later or into the caption.
3. **By 8 s, add a twist teaser:** "แต่ ...", "จนกระทั่ง ...", "ยกเว้นวันที่ ...". Never a background paragraph.
4. **First frame:**
   - The weird act is already happening, with the character mid-motion.
   - The key object is big and readable.
   - The camera is already moving.
   - An in-world sign or number is allowed (R8's "39 FT", "MIND THE GAPS").
5. **The image illustrates every word** of the first 5 s (R5: pour, sea, pirate ship, laughing pirates).
