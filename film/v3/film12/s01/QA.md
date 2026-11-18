# QA s01 (shots 1-3, g 0-178; render 720x1280, 20 samples, ~25 s/frame at 2 threads)
- qa_auto: PASS (see QA_AUTO.md). Its "no visible change" note at cuts 66/117 is a tool quirk: checked by eye, 65->66 street_wide->coach_low and 116->117 coach_low->hero_track are clear cuts.
- Heads: max projected head point y 741 (limit 880) on every frame; all cards are cast12 cards (hanway walk cycle, man, woman, coachmen), none are placeholders.
- Cameras always move (A->B keys per shot: street_wide push-in 66 f, coach_low 51 f, hero_track 62 f incl. handle). Hero walks on a 28-frame cycle with feet moving in the road.
- Shot 3: head coachman winds up (g<113) and releases; the 3D cabbage flies g112-120, hits the umbrella apex at g120 (thwack cue 3.9 s), bounces off; Hanway flinches 11 frames, then walks on with a leaf stuck on the umbrella (leaf_stick). No injury, no splat decal in the air.
- Mouths: no lip-sync poses used; all mouths fixed.
- Light RAIN; shade hue/magenta: qa_auto magenta 0.0 %. Rain on every frame.
- Known weaknesses: shot 2 Hanway grows large and is clipped by the left frame edge in the last ~15 frames (passing close to the camera); coachmen are static cards (glare pose switches at g80/88); the horses are the set's low-poly horses.
