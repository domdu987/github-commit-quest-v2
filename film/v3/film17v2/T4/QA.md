# T4 QA self-check (film 17 v2, g 844-1051, 208 frames, 720x1280, 16 samples + OIDN)

Only what I saw is claimed. Frames were viewed at full size (870, 985, 1051) and at phone size 360x640 (870, 930, 950, 985, 1010, 1051).

## Numbers
- check_take(T4) hits = [] (PASS). check_face(T4) ok (PASS). See checks.txt.
- Luma (RGB-mean at 90x160, the director's binding metric) over all 208 frames: mean 104.7, min 81.1, max 124.5 (target 95-110). Lights only: TAKE_OVER measure gain 0.68, shade_mul 0.8, fill_w 70; no haze, no saturation change.
- qa_auto: **FAIL** on the blur heuristic only: 13 frames flagged (g857-861 clock macro on a flat wall, g1010-1017 a flat wall and door frame as the camera passes the door). I looked at g859, g1004 and g1009: they are sharp-edged flat walls, not motion blur; the Laplacian-variance test reads them as soft because there is little texture. The first version of this take passed with 9 flagged frames (under the 5 % limit). Magenta 0.0 %.
- rhythm.py: in-shot median 13.29, p90 23.00.
- Shimmer: none seen; consecutive-frame wall differences follow camera motion. Stayed at 16 samples.
- Gate fixes (director): g860-920 and g960-1051 re-rendered: casement leaf closed during the clock macro, pair slid 0.75 m right over g862-914, flipped calendar page hidden, door-clip offset g994-1014, tally texture held on file 0000 (magenta gone: 0 magenta pixels on all 208 frames). Open: g870 dark disc (a cut head) at the bottom-left edge.
- g844-859 and g921-959 from the first render; g975-1051 re-rendered after the director's fix list (cabinet beat, coat stand removed, archive beam hidden), in 3 runs.

## Frames viewed
- g870 (full + phone): extreme close-up of the wall clock (10:00 face) and the 11 MESURES chart, framed pictures below. No cast visible except a dark round shape at the bottom-left edge (the edge of a card's head, cut by the frame). Reads clean otherwise; this is the clock pull-out.
- g930 (phone; also the key still, full size): Bertillon (right) holds the calipers in a visible glove, jaws on the prisoner's ear (prisoner at left). Feet on the floor with contact shadows. Chair and gasolier in view. No slab at the right edge.
- g950 (phone): the studio-camera box covers most of Bertillon's body; his face shows above it. The prisoner is at left, the calipers reach his ear. Camera box in front is the prepared path.
- g985 (full + phone): Bertillon at right, head partly at the frame edge, a record card in his left glove and a pen in his right, the pen touching the card. Prisoner stands behind in the middle. Camera and tripod at left, desk and stool. Readable.
- g1010 (phone): a coat stand with a blue coat covers most of Bertillon; his face and card hand show at the doorway on the right. Archive hall through the door.
- g1048 (contact sheet, not viewed full size): archives aisle, the cabinet with the MOYEN drawer shut, Bertillon beside it with an empty glove, a trolley with boxes in the foreground.

## Known problems (staging-side, not fixed)
- g884-887: the prisoner is off the left frame edge, so the calipers beam leaves the frame.
- (fixed) the coat stand no longer hides Bertillon (set dressing faces removed).
- g950-960: the camera box hides his body.
- (fixed) g1030-1051: a free-standing card cabinet (PETIT / MOYEN / GRAND) stands beside Bertillon; the card in his glove goes into the open MOYEN drawer g1032-1044 and the drawer is pushed shut g1045-1051. Checked on g1030, 1034, 1038, 1042, 1044, 1048. Bertillon is eased off his prepared path from g1018 and solved every frame beside the cabinet.
- g975-1051 are rendered with the archive beam mesh hidden (beam on/off differs by 14.4/255 at g1040).
- Queue cards (queue0, queue1) and the clerk are removed on frames where their head is wider than 190 px; I did not see them in any viewed frame.
- Window shaft mesh hidden and the tripod's black cloth removed for T4 (they read as a dark slab at the lens edge).
