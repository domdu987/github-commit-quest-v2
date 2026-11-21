# QA-tech sH1 (hard-defects rule, team9 f2fa8c3)

**PASS** (g1239-1348, 110 frames)

Hard defects: none.

Checks:
- Splice g1299/1300: diff 20.0 -> 23.6, ORB translation (-12,-18) -> (-16,-21), scale 1.023 -> 1.025, rot 0.1. Smooth, no jump.
- Old camera jump g1326/27: now ORB tx 4.7 -> 9.4, ty 7 -> 16 with constant scale (about 0.97). Normal drift, no jump.
- Old frozen frames g1327-1332: frame diffs are 19-21.5 every frame, so nothing is frozen.
- Old black rectangle g1308-1311: gone. The saltire banner is now lit and blue in those frames.
- Jitter second 2 (g1299-1328): this is a fast swoop dive and pan (tx about -110 to +110 px/frame, scale 1.26 -> 0.95) that reverses direction smoothly over about 5 frames. It does not alternate frame to frame. Not a shake.

Notes only:
- g1322-1348: a dark navy banner back (pole off-frame left) sits in the sky at the upper-left edge. It reads slightly odd but is cropped at the frame edge. Optionally light it or nudge the framing.
- g1316-1317: the fast swoop settles abruptly (diff 26 -> 17). Fine.
