# QA s08 round 3 (R3 notes at the end; R2 text kept below)

# QA s08 round 2 (film 17, shots 20-21), g 1039-1201 (163 frames incl. 6+6 handle), 720x1280, 12 samples + OIDN
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg); the "cut 1127 no visible change" note is a false alarm (cut at g1127 is obvious on contact.jpg).
- Rhythm (rhythm.py --first_g 1039 --cuts 1127): **R3: in-shot median 4.92, p90 14.39** (R2 was 4.77 / 12.49) (targets >= 4 / >= 12).
- Round-2 changes (answers QA-tech + QA-art):
  - Shot 21: inspector front, largest, unobstructed, mirrored to face Bertillon (camera-left), wide-open eyes (surprised, no tears), cupped hand arm, lean forward on stressed syllables, other hand points at Bertillon from g1172; open mouth only g1128-1195 (speak()), silent() elsewhere. Gendarmes behind/beside him, mouths closed (smirk, no fx), heads turned to Bertillon, 3 Hz bounce. Bertillon 0.8 m left/toward lens with a carpet gap, flinches g1130-1138 and stays slumped, cards kept in both hands. Push-in snap g1127-1141: inspector head 79 px -> 146 px (1.85x).
  - Shot 20: slumped Bertillon (head down, rounded shoulders), cards lifted to eye level and flipped every 1.25 s with a slow head shake after each flip, eyes down; shorter pull-out (head 158-185 px wide, > 1/5 frame height). Dressing at runtime: 8 extra drawers jammed open (cards 20 each) beside the desk, card pile on the desk, ~30 spilled cards on desk + floor, stub candle on a saucer (small, mostly behind the desk edge), floating quill (cream stick by the lamp, which caused the white needle ray) deleted from the mesh.
  - Ring-like prop (g1169-1189): gone; his hands now hold the two cards.
- Full-res self-check (contact 6 fps sheet + g1060, g1100, g1135, g1160, g1190 at 360x640 downscale of the finals): all heads inside the frame with chins above y 880 (every frame checked from the head report json: 0 violations); cards held in the hand in both shots; inspector clearly the speaker; no gendarme in front of him; no stray white discs or rays seen.
- Honest weak spots: inspector's cupped hand is readable as hand-by-the-face rather than a clear megaphone; gendarmes' closed-mouth smirk reads more "sneer" than "snicker" (bounce carries it); stub candle barely visible; characters still on fixed marks (no entrance).

## Round 3 (director R2 blocker + QA-art extras)
- Bertillon (shot 21): both cards are now in his hands: arms use the in-reach tired-pose hand targets (0.40,1.34) / (-0.26,1.30), cards angled -35 / -145 so each glove grips an edge; sleeves visibly connect shoulder -> hand. The earlier floating right card (hand target out of reach) is gone. Remaining: the puppet's glove draws a small thumb arc under the right hand; it is part of the hand, attached to the card edge, not a separate prop.
- Inspector head yaw 0.55 -> 0.80 from g1150, gaze (-1.0, 0.1) toward Bertillon (the cast limits the head turn, so the turn is modest).
- Sconce at the top edge g1185-1201: camera look z lowered to 1.05 / 1.00, bulb now fully inside the frame (checked g1199 top crop).
- Shot 20 candle: taller stub (0.13 m) with a larger flame and a wax drip at the desk front edge (-0.78, 1.97); the point light was moved with it.
- Right gendarme's grey box: it was the pulled drawer p5 behind him; now kept closed.
- Full-res self-check: g1144, g1169, g1194 (crops y 700-1280: hands on cards, no ring prop, only the glove thumb arc) and g1199 top crop (sconce inside frame). qa_auto PASS; 0 head violations in the previous round (head/camera unchanged except the end look).
