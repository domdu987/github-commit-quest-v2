# QA_TECH s01 round 2 (film 13, TAKE gate) - FAIL

Checked: qa_auto (69 frames, PASS: 0 frozen/black/pop, magenta 0 %), every frame via 6 fps sheet + full-size crops g0/g62, join to s02. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13r2/ (s01_a.jpg, full/s01_crop.png, join1.jpg). Take files untouched. Cut convention round(t*30) accepted.

Round-1 items:
- R1.1 lift readable: PARTLY. A full-width glowing gap with cribbing now sits under the ground floor and grows; but climb against the pier is tiny (~50 px), the 4 columns/portico barely move. Reads as a slow crane move, not a lifted building. Not a clean fix.
- R1.2 smeared mud: NOT FIXED. Bottom ~35 % (y>~830) is still smooth brown mud with a smeared, low-detail puddle (g0-30 big blurry grey-white puddle with muddy reflection; g50-68 thin smeared streak). Reads as soft/blur at phone size.
- R1.3 workers acting in the gap: NOT FIXED. Pullman centre, a bearded man right, two workers tiny at the left pier all stand idle in the same pose for 69 frames; nobody turns a jack or works in the gap.
- Heads: PASS (Pullman head ~y 810-865 <880). Mouths: closed, PASS. No text.

Remaining issues:
1. g 0-68 NEW (violates the new rule): the dust in the gap is ~70 uniform round white/cream blobs (dozens of 15-30 px discs lined along the foundation line, e.g. g12-68), reading as cotton balls/foam, not dust. They sit static in a row and cover the jacks/cribbing and the lift gap. Fix: fine small particles (2-5 px, varied, soft, falling), far fewer, low alpha; or a few streaks of falling grit; remove the discs.
2. g 0-68 R1.2 above: mud/puddle smear. Fix: crop/pitch so foreground is plank/crib detail, or add sharp mud texture and a clean puddle reflection.
3. g 0-68 R1.3 above: no cast acting. Fix: 2-3 workers on the crib pier / in the dark gap turning jacks (arm cycles), not standing.
4. g 0-68 R1.1: lift too small to read. Fix: larger lift keyed (gap 0.3 -> 1.0 m visible), tighter framing on the base so the gap opens visibly; keep columns moving against a static crib pier.
5. People on moving things: the left pier workers (g0-68) do not move with the facade/pier relation; fine, but the left pier crib pile has a lamp-like object on top (g0-68) that is unreadable. Low priority.
Join s01 -> s02: hard cut (g62 hotel exterior / g63 suite), no continuity break. Out-handle g63-68 continues the same framing, OK.
