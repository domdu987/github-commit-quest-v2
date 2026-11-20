# T4 QA self-check (film 17 v2, g 844-1051, 208 frames, 720x1280, 16 samples + OIDN)

Only what I saw is claimed. Frames were viewed at full size (870, 985, 1051) and at phone size 360x640 (870, 930, 950, 985, 1010, 1051).

## Numbers
- check_take(T4) hits = [] (PASS). check_face(T4) ok (PASS). See checks.txt.
- Luma over all 208 frames: mean 101.1, min 75.5, max 126.7 (target 95-110). g844-880 (clock close-up) reads 116-127. g985-1010 reads about 78. Lights only: TAKE_OVER measure gain 0.68, shade_mul 0.8, fill_w 70; no haze, no saturation change.
- qa_auto: PASS. Soft frames: g858, g1003-1007, g1014-1016 (the camera passes the coat stand). Magenta 0.0 %.
- rhythm.py: in-shot median 13.29, p90 23.00.
- Shimmer: none seen; consecutive-frame wall differences follow camera motion. Stayed at 16 samples.
- Two processes rendered the take (g844-947, g948-1051); the first 24 frames were discarded and re-rendered after a light change.

## Frames viewed
- g870 (full + phone): extreme close-up of the wall clock (10:00 face) and the 11 MESURES chart, framed pictures below. No cast visible except a dark round shape at the bottom-left edge (the edge of a card's head, cut by the frame). Reads clean otherwise; this is the clock pull-out.
- g930 (phone; also the key still, full size): Bertillon (right) holds the calipers in a visible glove, jaws on the prisoner's ear (prisoner at left). Feet on the floor with contact shadows. Chair and gasolier in view. No slab at the right edge.
- g950 (phone): the studio-camera box covers most of Bertillon's body; his face shows above it. The prisoner is at left, the calipers reach his ear. Camera box in front is the prepared path.
- g985 (full + phone): Bertillon at right, head partly at the frame edge, a record card in his left glove and a pen in his right, the pen touching the card. Prisoner stands behind in the middle. Camera and tripod at left, desk and stool. Readable.
- g1010 (phone): a coat stand with a blue coat covers most of Bertillon; his face and card hand show at the doorway on the right. Archive hall through the door.
- g1051 (full + phone): archives aisle; Bertillon at the left holds the record card up against the cabinet wall. The card is next to the drawers but I could not see it entering a drawer. A trolley with boxes in the foreground, a clerk at the right edge cut by the frame.

## Known problems (staging-side, not fixed)
- g884-887: the prisoner is off the left frame edge, so the calipers beam leaves the frame.
- g997-1007: the coat stand hides Bertillon almost completely.
- g950-960: the camera box hides his body.
- g1030-1051: the card is held at the cabinet wall, not shown sliding into a drawer.
- Queue cards (queue0, queue1) and the clerk are removed on frames where their head is wider than 190 px; I did not see them in any viewed frame.
- Window shaft mesh hidden and the tripod's black cloth removed for T4 (they read as a dark slab at the lens edge).
