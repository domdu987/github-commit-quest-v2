# QA-tech sA2 (hard-defects rule, team5 7748ab4)

**FAIL** (g80-159, 80 frames)

Hard defects:
1. **g102 -> g103: camera roll flip.** The view turns 180 degrees in one frame. Rotating g103 by 180 degrees matches g102 (diff 40 vs 55 unrotated), and ORB gives rot 175.8. Cause: the top-down dive passes the nadir, so the look-at up-vector flips (gimbal). Fix: give the camera an explicit roll/up-vector or a continuous quaternion path through the nadir, or lift the dive angle so it never reaches -90 degrees.
2. **g123-g125: unplanned splice through a dark frame.** The dive ends in tree shadow (g124 mean luma 41), then g125 is a different ground-level shot (ORB shows no overlap, 125 -> 126 is stable). This is a camera position/angle jump that is not a planned cut (meta lists only the cut in at g80). Fix: continue the swoop physically to the g125 medium pose (pass through the trunks with a short dissolve), or declare it a planned hide-cut in meta/rhythm.

Not defects:
- The dive g80-g102 and g103-g121 is fast but smooth (no frame-to-frame sign-flipping shake). The "jitter 11.7 px" in second 0 and the qa_auto blur at g96-103 and g123-124 are fast-dive motion blur and the dark pass.
- g126-159: stable push, no frozen run (diff about 2 per frame).
