# T1a QA self-check (g0-190), after the TAKE-gate fixes
Render: 720x1280, 16 samples + OIDN, 2 threads; motion blur 0.5 on g152-190. Real cast via stage_cast2 on every frame with `clear_cast()` before each call. Code: `t1a_stage.py` (covers, edge-on rule, glow cull, puddles hidden, beam fx hidden g76-171), `t1a_path.py` (local camera fixes, blended into the planned path; keys g0 and g105 and all frames from g172 are the planned ones). g0-27 are from the first run (path unchanged there); g28-190 are from the final code.
Viewed: contact.jpg (every 8th frame, phone-size tiles) of the final frames; full size earlier: g0, 29, 102, 105 and the gate stills g50, 60, 92, 100, 156, 161, 170 (gate_stills/). Not viewed frame by frame: the rest.

| g | what I see |
|---|---|
| 0-32 | Rooftop BIGZOOM start: cobalt zinc roofs, red chimneys with smoke, amber windows, orange horizon, Notre-Dame tower. |
| 40-60 | Camera over the near row, then down: roofs, then the Préfecture façade with shutters, lit windows, the PRÉFEC sign and a cobbled street. Single-colour roof share about 34-44% at g40-44 and below 34% from g46 (my coarse 180x320 check). |
| 72-88 | Through the open French window: clock, MARS 1882, tripod, rug. Foreground heads from behind with hair strands, bowler and cap, camera-facing covers. |
| 96 | Large Bertillon back (dark coat, hair) at the left edge, close to the lens. |
| 100-150 | Group front-on: Bertillon with calipers at a prisoner's ear, prisoners facing the camera, feet on the floor, props in the foreground. No slab, no beam. |
| 152-165 | Over the heads, shutter blur, faces readable but smeared at the 0.5 shutter. |
| 168-190 | Out through the window and up: back views as hair/coat covers, then the façade and the PRÉFECTURE sign, lamp post. |

Luma (RGB mean 90x160): part 113.0 (min 81.0, max 146.5); g0-95 104.2; g96-190 122.0 (above 112, trimmed at conform).
qa_auto: only 'suspected blur' on 36 frames from g26 (shutter off there; the roof swoop). No black, blank or pop frames.
qa_jitter: overall median 3.88 px; shake flagged at 1 s 3.9 px, 2 s 12.3 px, 3 s 4.0 px, 5 s 16.2 px (these are the roof dive and the g152-190 swoop).
GROUND.md: 6 sampled frames (g40, 70, 100, 130, 160, 190). Cast cards all OK (feet 1.5-3 cm below the surface, none floating). FAIL: `wagon_horse` (9.5 cm bbox gap) and `wagon_leather` (a wagon part resting on `wagon_iron`, 0.8 unit bbox gap): set props of the street, not touched by me. The contact-shadow table shows NO for cards that were hidden on that frame (edge-on / back cover); yes elsewhere.
Not checked: OIDN shimmer as a clip; BIGZOOM report; façade-sign rule (g200-300 is T1b).
