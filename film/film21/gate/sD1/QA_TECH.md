# QA-tech sD1 (hard-defects rule, team2 c546fa1)

**PASS** (g542-642, 101 frames, checked frame-by-frame with ORB/phase-correlation and visual contact sheets)

Hard defects: none.

Checks:
- Splice g592/593: frame diff 18.6 -> 16.9 on a continuous ramp, same framing and pose, no jump. OK.
- Splice g603/604: diff 4.4 -> 6.2, camera unchanged, only the hand/coin pose moves. OK.
- Whip g637-642: planned. Whip right with heavy blur (tx -35, -100, -190, -220, -320 px/frame), no blank, black or magenta frames. OK.
- Jitter g602-631: the camera is not shaking. Background-only pan (right strip) is smooth and monotonic (2.5 -> 13.6 -> 4 px/frame), with no sign flips. The full-frame +/-20 px vertical oscillation (about 12-frame period) is the laughing character's body bounce. Fine.
- No frozen run, no blank frames.
