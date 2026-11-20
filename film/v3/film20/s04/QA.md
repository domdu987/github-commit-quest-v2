# QA s04 (shot 4, SITE site_table, g 265..317; first_g 261, 61 frames, cut in/out, 4+4 handles)
- take.mkv 16.7 MB, 720x1280, 8 spp, 11.61 s/frame wall. qa_auto PASS (g 318 "no visible change" note: expected, the handle continues the move).
- Eiffel (cast20 card, C.on_ground, contact decal 0.8) stands beside the plan table, rolled blueprint in hand, raises his arm to point up g 266-274 on "วิศวกรไอเฟล" (g 268); expression determined -> proud on the closed frame of a blink (g 269-271). No mouth animation.
- Camera: preset lowered 0.75 D, 7 D closer, tilt 6 deg + 1.5 deg/s, push 10 %/s toward his head, slide 60 px/s, orbit -24 deg/s. Head 111 -> 147 px, centre y 727 -> 780 (end handle slightly lower than 760), bottom max < 880.
- Deviations: the plan table and the girder FG are not in frame (camera is closer than the table; the preset's near-black girder FG slab is hidden with visible_camera=False). Background is the pale pier wall + leg corner only. No snap (shot < 2 s); a snap test lowered the frame-diff.
- Frame-diff in shot: median 3.94, p90 5.38 -> below the 4 / 12 target (a centred hero with a plain wall).
- Not done: hue measurement; frame-by-frame review at the cuts.
