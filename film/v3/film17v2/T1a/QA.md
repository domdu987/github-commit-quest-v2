# T1a QA self-check (g0-171), final pass
Render: 720x1280, 16 samples + OIDN, 2 threads; motion blur 0.5 on g152-171 only. Real cast via stage_cast2 on every frame, with `clear_cast()` before each call (leak fix). Staging patch: `t1a_stage.py` (hair + coat back covers for Bertillon and the 3 bench prisoners, beam fx hidden g76-171, window glow hidden g60-61, `clip_start` 1.2 on g58-61, gasolier-glow faces culled near the lens g145-165). g0-55 and g62-75... see below: g0-55 are from the first run; g56-171 were re-rendered with all fixes.
Viewed at full size: g0, 29, 102, 105 (key), and the g61, g86, g155, g160 test stills (same code). Viewed at phone size: contact.jpg (every 8th frame) of the final frames. Not viewed frame by frame: g1-28, g30-55, g97-101, g106-150 except through the contact tiles.

| g | what I see |
|---|---|
| 0, 29 | Rooftop BIGZOOM start: cobalt zinc roofs, red chimneys with smoke, lit amber windows, orange horizon strip, Notre-Dame tower top-left. Reads well. The French window is not yet visible. |
| 56-60 | Façade of the Préfecture, PRÉFEC sign, shutters, café window. No flat colour (g59-61 had a wall at 0.14 m, now clipped). |
| 61 | Façade with PRÉFECTURE sign and cobbles, clean, RGB-mean 116. |
| 72-88 | Through the open French window into the room: clock, MARS 1882, tripod, rug, ARCHIVES door, a gendarme. The foreground row is seen from behind as brown hair domes and coats (hair + coat covers), no black discs. |
| 96, 105 | Camera inside. At g105 (key): Bertillon front-on with the calipers at the prisoner's ear, prisoners front-facing, feet on the floor, calipers case in the foreground. |
| 112-150 | Same group on the side track, readable faces, bench and window behind, no slab, no light beam. |
| 152-160 | Motion blur on, faces still readable at g155 (RGB-mean 131). A blurred yellow lamp streak crosses the lower left: the gasolier glow passing the lens, accepted by the director. |
| 168-171 | Fast swing over the group, hair/coat backs and a hat, blurred. Last frame shows the room through the window (clock, tripod). |

Luma, binding metric (RGB mean at 90x160): part 107.8 (min 64.7, max 134.2); g0-95 100.2; g96-171 117.3 (above 112, trimmed at conform).
qa_auto: only 'suspected blur' on 48 frames from g21 (shutter is off there; the camera swoops over the roofs; the director said to ignore it). No black, blank or pop frames.
Not checked: OIDN shimmer as a clip, BIGZOOM report (not re-run), façade-sign rule (g200-300 belongs to T1b).
