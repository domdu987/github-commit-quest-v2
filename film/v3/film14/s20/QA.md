# QA s20 (shots 20-24, THE REVEAL), g 1301-1683, 383 frames, 720x1280

- Reviewed every frame at 6 fps (contact.jpg, phone_sheet.jpg) and every cut +-3 frames (g 1368, 1453, 1503, 1599): clean hard cuts, no pops.
- Heads above y 880: elephant head/eye/trunk stay above the line in s23/s24 (trumpet g 1653 included); no people in take.
- Camera: elephant shots <= 1.5-1.8 m high, near-frontal, no steep down-view. No DOF, no text.
- Elephant cards: contact shadow blob under feet, night tint, matriarch unhurt; face and eye always visible through the swarm.
- Mechanism reads: s20 slides along the bowed wire, s21 swing wave down hive row, s22 hive jolt + dense bee burst, s23/s24 swarm on eyes/trunk, trumpet at g 1653.
- Mouths: elephant trumpet only (no uncle talk windows in this take).
- QA_AUTO: only FAIL is "suspected blur" (109 frames, g 1301-1500 mostly). False positive: the metric is relative to the median Laplacian variance, which the bee-dense s23/s24 frames inflate; the wide, smooth night ground/sky frames of s20-s22 fall below 0.6x. Frames are sharp (checked g 1370 at full res).
- Known quirks: u4 roof edge crosses the elephant at g ~1319-1337 (as in approved s2 test); bees slightly dotty at phone size; s23 opening swarm ramps in.
