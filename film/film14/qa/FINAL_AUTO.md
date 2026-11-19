# FINAL gate, automatic checks (qa_auto.py on cut1, 2106 frames)   VERDICT: PASS (flags explained)
- black/blank frame g2105: intentional hard cut to black after "งวงช้าง" (shot plan).
- "blur" on 283 frames: false positive from a film-wide median (night vs day). Re-checked per take: 60 flags, per shot: only g1503-1510 (shot 23 opening, fewer bees on screen, frames checked by eye: sharp) and g1912 (dissolve). Every take passed its own sharpness check.
- No pops outside planned cuts; no frozen runs; magenta 0 %.
- "cuts with no visible change" at g324/1062/1453/1599 are low-contrast night cuts or a matched camera (s21 -> s22, by design); g1764/1914 are dissolves.
