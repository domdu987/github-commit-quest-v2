# T1a QA self-check (g0-171), after the stage_cast2 leak fix
Render: 720x1280, 16 samples + OIDN, 2 threads; motion blur 0.5 on g152-171 only. Real cast via stage_cast2 (g105 key-still assignment) on every frame. g0-59 are from the first run (roofs, no leak seen); g60-171 were re-rendered with the leak fix (clear c2_/back_hair_/back_coat_ + actors.clear_registry() before each call).
Viewed: contact.jpg (every 8th frame, phone-size tiles) and at full size g0, 29, 102, 105 (key), 120 earlier; g60, 76, 155 only as tiles/small crops.

| g | what I see |
|---|---|
| 0, 29 | Rooftop BIGZOOM start: cobalt zinc roofs, red chimneys with smoke, lit windows, orange horizon, Notre-Dame tower. Reads well. The French window is not yet visible as the brightest spot. |
| 60-61 | Camera against a lit window: a flat yellow block fills the frame (RGB-mean 157-180; qa_auto 'blank' g61). Not a leak: it comes from the planned camera path. Defect, not fixed. |
| 72-80 | Facade with PRÉFEC sign, window with red/white awning, figures visible inside. Clean, no black polygon any more. |
| 86-96 | Through the French window into the room: clock, MARS 1882, tripod, rug, ARCHIVES door. Silhouettes of seated figures in the window foreground. Black frames gone. |
| 102, 105 | Bertillon front-on, calipers at the prisoner's ear, prisoners front-facing, feet on the floor, props in the foreground. No black slab. |
| 112-136 | Same group from the side track: Bertillon, a moustached prisoner, a hat prisoner, all readable; bench and window behind. |
| 152-160 | Motion blur on. g155-156 a yellow-white glow fills the frame (RGB-mean 188-203), then a fast swing. Defect, not fixed. |

Luma, binding metric (RGB mean at 90x160): part 112.9 (min 64.7, max 203.1); g0-95 102.3; g96-171 126.2. g96-171 is above 112 and is trimmed at conform per the director.
qa_auto: FAIL on 'blank' g61 and 'suspected blur' on 48 frames from g26 (motion blur is off there: the camera swoops over the roofs); pop at g156.
Shimmer: not checked as a clip. Not checked: BIGZOOM report, façade-sign rule (T1b).
