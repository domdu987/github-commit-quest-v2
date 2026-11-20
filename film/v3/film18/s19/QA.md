# QA s19 (render team 5, film 18) round 11 - frames g1427-1514 (+6 handles: take.mkv g1421-1520, 100 frames), jimo_out NIGHT
Frame-diff in-shot (n=87): median **9.99**, p90 **13.04**. qa_auto "blur" g1505+ = whip landing (director: false positive).

## Measured per frame (c18.py `shot.py measure`, bpy_extras.world_to_camera_view on every ox's mouth anchor, g1427-1514)
- **Worst mouth y = 858 (g1485)**; no frame has a mouth below 860. (Before: 907 at g1487.) Done by moving the camera to x 14.2 (farther from the lane) and using holes x 30 / 35.5 / 41 only, so the nearest oxen stay farther from the lens (not by pitching down).
- **Flame-to-face: NOT met.** My estimate (flame segment tail->tip + half height vs a 0.75 D face circle) gives min -73 px (g1484) and is below 60 px in 68 frames of g1427-1497. I tried thinning the herd (single hole, one ox at a time) and that reaches +84 px at 24-frame spacing, but then the oxen are 8-12 % of frame height and the burst no longer reads, so I kept the denser herd. The distance is an approximate box test, not pixel-measured on the renders.
- **Plain ground measured on rendered frames (`J.ground_share`)**: 0.25 / 0.32 / 0.23 / 0.28 / 0.23 at g1430 / 1450 / 1470 / 1490 / 1500 (was 0.35-0.42). Eight `prop_pot` jars / bowls and a helmet are placed in the world in the lower band along the camera path; they are pale lavender at night (not warm), and the nearest are large.
- Purple strip: still covered (`mygap` plane, round 10).
