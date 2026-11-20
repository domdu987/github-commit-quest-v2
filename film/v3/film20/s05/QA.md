# QA s05 (shot 5, SITE site_leg_low, g 318..403; first_g 314, 94 frames, cut in/out, 4+4 handles)
- take.mkv 39.7 MB (not split), 720x1280, 8 spp, 16.30 s/frame wall. qa_auto PASS (g 404 note expected).
- Camera: preset moved 12 m toward the leg foot, aim pitch 19 -> 27 deg by drift, +11 deg SNAP up on "สูงที่สุดในโลก" (g 344-359, ends pitch ~38 deg, sky well above 35 %), aim pans 24 deg to the right over the shot, push 8 %/s, slide 60 px/s.
- Cast: Eiffel at eiffel_leg (C.on_ground, decal) raises his arm at g 319-327 on "สูง 300 เมตร"; three riveters on the platforms leg_a..c (hammer / tongs / forge cycles). No mouth animation.
- DEVIATIONS: (1) Eiffel is only in frame about g 314-345: the tilt-up and pan push him out of the bottom-left, so his head crosses the caption band (y 880) and leaves frame in the second half (head bottom max y 1070) -> breaks "heads above 880" for part of the shot. (2) The pier's pale stone wall fills the middle of the frame (it is the leg's masonry foundation); riveter heads are tiny (14-30 px) and sit high. (3) Preset near-black FG slabs hidden (visible_camera=False). 
- Frame-diff in shot: median 4.89, p90 10.84 (p90 below the 12 target).
- Not done: hue measurement; frame-by-frame review at the cuts.
