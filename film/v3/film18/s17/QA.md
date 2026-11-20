# QA s17 (render team 5, film 18) round 8 - frames g1309-1387 (+6 handles: take.mkv g1303-1393, 91 frames), jimo_in NIGHT
Frame-diff in-shot (n=78): median **6.66**, p90 **9.20**. qa_auto PASS.
1. Foreground reeds: `J.prop_reed_bundle` (60 stalks, 2 red cords) at 0.5 scale parented to the camera, lower-left, recoloured with a warm straw emission so it is lit at night; nothing crosses a face. The set's own flat fg slab (the camera-parented `fgreeds` prop) is hidden.
2. Tying: `STORY18["townsperson_tie_reeds"]` old man placed so his anchor `reed_tail_l` lands on the `tail_tip` anchor of ox 4 (computed from the ox card's yaw / mirror and scale); he bends with a 4-step lean cycle; about 35 % of frame height; chin about y 780-860 (< 880). A woman brings reeds, Tian Dan points.
3. Oxen: 3/4 cards facing the holes (cast has no back view); no lit tail.
4. `J.gapfill` ran; the road is warm dark earth with 4 v2 props; bare road about 35 % (not <= 30 %).
