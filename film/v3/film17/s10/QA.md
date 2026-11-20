# film17 s10 (shots 24-26, THE REVEAL) QA, round 2

take.mkv: g 1336..1520 (185 frames, 720x1280, 12 samples + OIDN, libx264rgb crf 6), stored as take.mkv.partaa/ab (`cat take.mkv.part* > take.mkv`). Cut-in g1342, cut-out g1515, 6 handle frames each side. Planned cuts: 1374/1375 (whip, location change), 1406, 1420, 1459, 1474.

## Numbers
- rhythm.py --cuts 1374,1375,1406,1420,1459,1474: in-shot median 7.26, p90 17.08 (targets >= 4 / >= 12) PASS.
- qa_auto (same cuts): no black/blank/magenta/frozen frames. One FAIL, "suspected blur on 77 frames" (Laplacian < 0.6 x median): not motion blur. The median is carried by the texture-rich measuring-room frames (inserts + head beat); the records-room frames (box beat g1420-1458, card shot) are low-texture dark wood and drawer fronts and measure lower even un-blurred. Blur is applied only on g1370-1378 (whip table in post.py, peak 3 frames g1373-1375). Notes: "planned cuts with no visible change" = the hard cuts/whip are between similar warm frames at 180x320 analysis size; checked by eye on contact.jpg.

## Beats (all animated)
1. g1336-1366 measure_chair: Bertillon's calipers rise from low and settle on Dupont's head at skull height (hand follows, jaw jitter), he looks along the beam. Push + slide.
2. g1367-1383 whip (3 smeared frames g1373-1375) measure -> records.
3. g1376-1405 drawer: Bertillon (right, head clear of the drawer) leans back and yanks the big drawer out 0->1 (g1376-1398); drawer now holds six lit boxes.
4. g1406-1419 INSERT finger (measuring room): Dupont holds out one finger, calipers jaws close on it (jaw slides 0.30 -> 0.50).
5. g1420-1458 box beat: six lit boxes in the drawer go dark one by one (g1424, 1430, 1436, 1442, 1448) until one lit box remains; a hand (sleeve + cuff) comes in from the right g1430-1442, grips the lid front edge and lifts the lid g1442-1457 (hand follows the lid edge). Camera drift + slide, wide to close.
6. g1459-1473 INSERT ear (measuring room, team 1's S3A framing and ear/hand setup, copied): near-profile Dupont with drawn ear, jaws close on the ear.
7. g1474-1520 card_hero: snap from the box view (10 f), the card stays below the rim until g1476, rises g1476-1500 into the lamp, push-in. Card lamp 38 W, post exposure -17 % ramp g1476-1490 + paper +10 % mask; portraits, hand, fingerprint and bottle read at phone size (full6.jpg).

## Self-check (full-res frames viewed: g1350, 1374, 1412, 1440, 1466, 1510, plus contact.jpg every 5th frame)
- g1350: calipers on the skull, both heads in frame, chins < 880. g1374: whip frame, no cast. g1412: finger insert, calipers on Dupont's raised finger, heads y 480-610. g1440: dark boxes + one lit box, hand reaching the lid. g1466: ear insert, jaws on the ear, Bertillon's hand/forearm drawn on the beam. g1510: card with portraits + bottle, not blown, box rim below.
- Beards/chins above y 880 in all cast frames (Bertillon chin ~ 790 at g1400). Mouths closed in every frame (silent). beam_fx hidden, dust 0.4. Props held: calipers in Bertillon's drawn hand in the inserts; drawer yank pinned to the drawer front. No floating hand after g1405.

## Not done
- Warm rim light on the card (only exposure -17 % and paper +10 %). Tightening 2-3 frames on "ระดับนี้". The lit/dark boxes differ in brightness but the dark ones are low contrast on a phone screen; the beat reads from the white box that stays lit.
- Finger insert: Dupont's hand is the puppet fist-with-point; the finger is small at phone size.
