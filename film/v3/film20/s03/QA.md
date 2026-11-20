# QA s03 (shot 3, SITE site_wide, g 178..264; first_g 169, 100 frames, 9 in-handle (dissolve 13) + 4 out-handle)
- take.mkv 43.7 MB (libx264rgb crf 6), 720x1280, 8 spp, 14.67 s/frame wall (2 processes x 2 threads). qa_auto: PASS.
- Camera: crane-down from site_wide toward site_wide_end (extended x1.7), 60 px/s slide, orbit -5 deg/s about the yard, aim down 3 deg + 12 deg during the snap; eased SNAP push on "ปี 1887" (g 213-228). Heads of the workers stay < 880 (checked with probe over the whole path).
- Cast: six riveter cards (cast20) at worker_a..g, placed with C.on_ground; hammer / tongs / forge cycles, no mouths animated. Two of them swing out of frame left during the orbit.
- Set: hid the preset's near-black FG blocks (fg_dark_sh, fg_metal_sh, fg_redlead_sh: a near-black slab at the frame edge) by visible_camera=False; the thin timber post stays at the left edge.
- Lower third of the frame is the empty shaded ground slab (caption zone), as the set notes describe.
- Frame-diff in shot: median 3.09, p90 7.86 -> BELOW the 4 / 12 target (wide shot, far subject; stronger orbit/snap pushed the workers into the caption band). Not fixed.
- Not done: hue measurement; dissolve-in continuity with shot 2 not checked frame by frame; planned-cut note from qa_auto (g 265) is expected (the handle continues the move).
