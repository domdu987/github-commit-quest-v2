# QA s20 (render team 5, film 18) round 11 - frames g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), jimo_out NIGHT
Frame-diff in-shot (n=80): median **4.46**, p90 **6.55** (median gate met; p90 >= 9 NOT met). qa_auto PASS.

## Measured (c18.py `shot.py measure`, every frame g1515-1595)
- Lead ox (scale 0.8): head anchor x about 0-200 px (the head is partly cut by the left edge on some frames because of the camera yaw sway), tail tip x about 470-610, lead mouth y about 620-640. My flame box (tail -> tip, 2 x flame scale) ends at x 720-860, so the lead flame is NOT guaranteed inside x <= 662: on the phone sheet the flame tongue (about 150-200 px) ends at x 640-720 on most frames. Fitting a >= 150 px flame, a 35-40 % ox and the head in frame together is not geometrically possible: the cast ox is about 1.45 x longer than tall.
- Neighbour ox in the lead's row removed (and the second row lattice at 12 D): no neighbour flame near the lead mouth in the frames I checked (not measured per pixel). The reed-bundle-in-mouth case at g1574 came from the old lattice and is gone.
- Plain ground measured (`J.ground_share`): 0.32 / 0.42 / 0.29 / 0.33 at g1530 / 1550 / 1570 / 1590: NOT <= 0.30. Dark-earth plane + warm pools are in; the 2-3 oxen cropped by the bottom edge were not added; three Qi silhouettes run behind the herd (not in the lower band: when I put them in the lower band they covered the lead ox).
- Camera: sway (yaw +-2.6 D, period about 2 s) plus an eased dolly in (lateral 9.8 -> 6.2 D); the lead ox drifts along the frame.
