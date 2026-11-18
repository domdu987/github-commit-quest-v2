# QA-art — TAKE gate 1, film 11 "ไอ้หมอวัว" (key takes)
Reviewer: QA-art (opus). Method: every 10th frame (3 fps) at phone size 360x640, plus full-size key frames
(s01 f30/70, s02 f30/70, s13 f60, s14 f40, s15 f40/80, s21 f60, s22 f50, s23 f30/110, s28 f50/72; f = frame index inside take.mkv).
Compared with v3/set3d11/contact.jpg (approved) and analysis/sheets (jar_0 etc.). All QA_AUTO = PASS, magenta 0 %.

Scores 1-10: Dens = set density, Light = warm gold + blue-violet shade, Comp = composition/phone legibility,
Act = acting reads the beat, Key = key-moment clarity.

| take | beat | Dens | Light | Comp | Act | Key | verdict |
|---|---|---|---|---|---|---|---|
| s01 | hook: pus from milkmaid's hand | 7 | 8 | 6 | 6 | 7 | PASS (note) |
| s02 | hook: lancet on boy's arm | 4 | 7 | 5 | 6 | 5 | FIX |
| s13 | false payoff: fever night | 6 | 6 | 4 | 6 | 5 | FIX |
| s14 | false payoff: towndoc accuses | 6 | 7 | 6 | 7 | 7 | PASS (note) |
| s15 | false payoff turn: boy leaps up | 8 | 8 | 7 | 8 | 8 | PASS (note) |
| s21 | reveal start: Sarah milking | 6 | 7 | 5 | 6 | 6 | FIX (small) |
| s22 | KEY: blistered hand + clear face by udder | 7 | 7 | 7 | 6 | 7 | FIX (small) |
| s23 | reveal crowd: pockmarked vs clear | 7 | 8 | 6 | 5 | 6 | FIX |
| s28 | ending: Blossom knows the word | 7 | 5 | 5 | 6 | 5 | FIX |

## Per take

### s01 — PASS (note)
Hook reads as strange at phone size: open palm with big orange blisters, Jenner's lancet at it, jar on his chest, cow + udder behind.
Gold rim light, dust motes, ok. Weak: top ~40 % is roof; Jenner stands upright looking at camera, not at the hand; cow head is
cropped out of frame (headless body). Optional (if re-rendered anyway): Jenner examine_hand lean + eyes to the hand; tilt look-at
down ~0.3 m so less roof / more cow.

### s02 — FIX
1. Lower 40 % (y 760-1280) is empty flat lawn with giant fence-shadow spikes (f30-f90) — violates "lower third must not be empty".
   Fix: dress the foreground lawn: flower pots/basket/hens/a wooden bucket ~2-3 m in front of the camera on the grass, and/or move
   CAM0/CAM1 look-at z down from 1.9 to ~1.6 and the camera 0.8 m closer so the hut+pair fill more of the frame.
2. The lancet tip ends at Jenner's own chest (f70, x~930 y~715) while the red dot appears on James's far arm near the elbow
   (x~990 y~800), small and disconnected. Fix: place the sore card on the camera-side upper arm (upper_arm_l anchor, near the
   shoulder), ~1.5x bigger, and drive the lancet tip (hands r tip) to exactly that point at the dot's appear frame.
3. Sleeve not readable as rolled; James's legs splay forward like sticks on the stool. Minor — if cheap, use sit_sleeve legs tucked.

### s13 — FIX
1. James is barely visible: only his head peeks over a huge quilted bed-side "wall" that fills the left half (f0-f78); at phone size
   his face is ~40 px. Fix: raise the camera (z 3.0 -> ~3.6) and look down onto the bed so James lies facing camera with face,
   flush and sweat drop readable (target head ~110 px wide full-size), mother + candle at frame right.
2. Night does not read as night: the window is a peach/dusk sky and the room is mid-grey-blue. Fix: darken the window to deep
   blue-violet (or add a moon), drop fill ~30 %, and make the candle a stronger warm pool on the mother's face and James's pillow
   (bigger point light, warm 2200K) — the C look of the approved room_night tile.
3. The red sore card floats beside James's head (f60 x~135 y~565) like a bauble; hide it under the quilt in this shot or put it on
   the arm if the arm is out.

### s14 — PASS (note)
Accusation reads: red-coated towndoc in lit doorway, arm pointing at Jenner, mouth open, angry brows; Jenner grimaces, mother
worried, fire behind. Note: towndoc head is ~25 px at phone size and the sick boy is not in frame. If re-rendered for other reasons:
bring towndoc 1 m into the room (past the threshold) or push the camera so he is 1.4x bigger; show the bed edge with James in the
foreground left.

### s15 — PASS (note)
Best of the set: warm golden morning, rug, cat, James leaps up off the bed (f30-40) and runs toward camera grinning (f60-90),
mother and Jenner beaming. Note for QA-tech: the sore card floats off his body (f40 x~270 y~495 by his chest; f80 x~1120 y~695
at his waist) — re-anchor to upper_arm_l. Foreground chair partly blocks mother; acceptable.

### s21 — FIX (small)
Sarah's clear face reads, but Blossom's head is cropped at frame left (only an ear) — a headless cow in the reveal; Sarah stands
beside an empty stool rather than milking on it; lower half is bare straw floor with a bucket. Fix: pan look-at ~1 m toward -x
(CAM0/CAM1 look x -5.0 -> -6.0) so Blossom's head is in frame, seat Sarah on the stool (sarah_milk on milker_feet) with hands at the
udder, and drop the camera end point closer (CAM1 y 8.8 -> 9.6) for the push-in.

### s22 — FIX (small)
Key image works at phone size: clear smiling face + hand with 4-5 orange blisters right beside it. Missing piece: the UDDER link —
the pink udder (x~1100-1220 y~720 of f50 at full size) is half hidden behind the milk pail. Also the hand is a two-finger V
("peace sign") which reads as a pose gag, and Sarah's half-lidded smirk reads sly.
1. Move the pail ~0.6 m to screen-right/forward so the whole udder shows, and lower Sarah's hand to udder height (or step her
   right so hand and udder sit side by side) — "blistered hand next to the udder" must be in one glance.
2. Use the open palm (as in s01) instead of the V, held still for >= 1.2 s.
3. Expression: friendly/open eyes (sarah_smile) instead of the sly lids.

### s23 — FIX
Contrast is right (pockmarked left, clear rosy milkmaids right, Jenner in the middle, amber C light with violet shade, nice).
But at phone size the pock dots are ~3 px and the shot is nearly static for 4.3 s.
1. Push in: move CAM0/CAM1 ~1.5 m closer and ~1 m lower (heads ~1.4x bigger) with a slow truck left->right across the two groups
   so the eye goes pockmarked -> Jenner -> clear faces.
2. Jenner acting: give him the explain pose with one hand toward the villagers and one toward the milkmaids (currently a passive
   stand, hand at chest).
3. Keep Blossom's head+udder in frame at right (now only her rump/udder edge) — the cow is the cause. The hay nest with blue eggs
   in the lower third is fine as foreground dressing.

### s28 — FIX
The ending gag (Blossom looks round as if the word "วัว" is hers) is too small and too dark: Blossom is a mid-ground figure
(~45 px head at phone size), roof fills the top 40 %, and the take is dominated by cool blue-violet shade — not the golden barn_wide.
1. Push in: camera ~2.5 m closer to BLOSSOM (-2.8, 8.2) at head height (~1.4 m) so she fills ~60-70 % of frame width, head
   around y 550-650; keep hens/buckets in the foreground lower band.
2. Last ~20 frames (g ~1850-1870): head turns to camera, eyes to lens, ear flick, a beat of hold (smug/knowing) before the hard
   cut on "วัว" — currently her head turns but she looks down/sniffs.
3. Warm it: add golden key/sun shaft from the door onto Blossom (light A as in contact tile 1) so she is the brightest warm shape.

## Overall
Look matches the approved set (sharp, no DOF, no text, warm gold + violet shade, dense props). Key readable moments today:
s01 hand, s15 leap, s14 accusation, s22 hand+face. Blockers before conform: s02 (empty lawn + disconnected lancet/dot),
s13 (sick boy invisible, not night), s23 (reveal too small at phone size), s28 (ending punchline too small/dark).
s21/s22 small fixes (cow head in frame, udder visible, open palm).
