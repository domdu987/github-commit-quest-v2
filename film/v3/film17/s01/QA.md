# film17 s01 (shots 1-3, hook) QA
- 720x1280, 12 samples, ~52 s/frame; g 0-143 + 6 handle frames (144-149); cuts at g 48, 93.
- qa_auto: PASS (magenta 0 %). Note: planned cuts 48/93 reported as no visible change within +-2 frames by the tool (rhythm.py detects 2 hard cuts).
- rhythm (rhythm.py --cuts 48,93): in-shot median 6.44, p90 14.61 (target >= 4 / >= 12). Draft was 6.36 / 13.85.
- Shot 1: Bertillon (left) closes the calipers on the seated prisoner_a's left ear, push + slide. Shot 2: wide, queue + gendarme, pull-out + slide.
  Shot 3: raking ear insert, snap g120-135 (swap of sitter to prisoner_b at g127 inside the snap) on "ทีละหู".
- The puppet has no ears: s01 draws cartoon ears as sprite underlay (ears_svg in shot.py) on the prisoners.
- Known weaknesses: shot 2 bench prisoner is at the left edge/partly out of frame; calipers jaws read small in shot 1; swap hidden only by the snap motion.
- Mouths closed throughout. Reassemble: cat take.mkv.part* > take.mkv
