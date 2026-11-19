# s23 QA (v2, after the TAKE gate): film 16, shot 23 (callback of shot 1) -- LINE line_close, AFTER_RAIN

Redone together with s01 (same camera, same marks, same bottle-hand method; s01 is DAY, this is AFTER_RAIN with a wet pole).

## What changed against v1 (TAKE gate: bottle merged with his head, mint-jelly glass, wire never seen on the glass, empty sky, salmon pole)
- **Head beside the bottle:** Morse stands one rung lower along the ladder (mark shift -0.25, -0.22, -0.6 D) and holds the bottle out toward the pole: head centre 1.2 D from the pole axis instead of 0.7. The inverted bottle body now stands against clear sky at the left of his head for the whole take (>= 60 px of air at 720 wide).
- **Glass reads as glass:** the set's own 'glass' material is tuned at runtime (alpha 1.0 + transmission 0.8, deep bottle-green, less self-glow): no hashed-alpha grain, a clear neck / shoulder / body, hard glint. The held copy and the set's peg glass are the same material, so the swap at contact (g 1494) does not pop.
- **Wire on the glass:** the framing now keeps the glass top and the wire in view through the flick (g 1509-1520) and the drape (wire above the glass, falls onto it, overshoot, settles; wrap ring on from g 1521). The hand then drops to his side instead of crossing his face.
- **More ground in the first second:** camera higher (z 5.3 vs 4.4, pitch 25 deg vs 33): the pole row, trees, wheat and fence fill the lower half; sky about 35 %.
- **Wet dark pole:** the pole's texture-driven base colour is multiplied by (0.36, 0.33, 0.40) and glossier (AFTER_RAIN).
- **Expression:** determined until contact, happy from the pose swap on the closed frame of the blink (g 1499).

## Round 2 (TAKE gate): what changed
- **Free hand below the chin:** after the cap the hand comes down the pole side to chest height, takes the wire at the coil and stays at chest height; it never goes to his face or forehead (hand pins checked: error <= 0.2 D). The v2 claim "drops to his side" was wrong; this version does it.
- **Wire falls and bounces:** the flick lifts the wire in an arc over the glass; it then falls onto the glass and bounces twice (damped) before the wrap ring appears (g 1524).
- **Head clear of the glass to the cut (g 1526-1539):** slide / arc drift reduced, a small truck + crane-up while the wire settles keeps his head right of the glass (head-to-glass distance >= 165 px, head half-width about 130 px).
- **Pole:** darker and glossier (multiply 0.27, 0.25, 0.31, roughness 0.20), closer to the s24 pole.
- **Frame-diff now (in-shot):** median 6.12, p90 12.04 (target >= 4 / >= 12): MET. qa_auto PASS.

## Delivered
- take.mkv: 103 frames, g 1446..1548 (shot g 1455..1539, 9 handle frames each side), 26.5 MB. Hard cuts in (1455) and out (1540).
- QA_AUTO.md (PASS), phone_sheet.jpg, contact.jpg, cues.json, meta.json, framediff.json.

## Beats (event g = round((t+0.10)*30))
| g | beat |
|---|---|
| 1446-1472 | bottle held out over the bare pole top ("เขาเลยคว่ำ" 1458), camera moving |
| 1473-1486 | SNAP x2.4 + pan (13 f) on "คอขวดเบียร์" 1475, sun glint 1475-1482 |
| 1484-1494 | lowered mouth-down onto the pole; contact 1494 (before "บนหัวเสา" 1495): set glass on, copy off, flare 1494-1503 |
| 1498-1500 | blink, pose cap -> drape, happy |
| 1505-1520 | hand takes the wire at the coil, flicks it over the glass ("แล้วพาดลวด" 1509), settles |
| 1521 | set wire spans + wrap ring on |

## Checked
- Heads [92, 269] px wide, centre y [486, 617], lowest head bottom 717: nothing in the caption band.
- No text, no DOF, mouths still, no magenta, hand error <= 0.1 D except the flick (intended).
- Head touches the right frame edge for a few frames at the snap peak (g 1486-1490); the face stays in frame.

## Frame-diff (in-shot g 1456..1539), v3 after the director's request
median 7.18  p90 12.73  (target >= 4 / >= 12): MET (v2 was 6.88 / 10.64).
- The start framing, marks and the snap on "คอขวดเบียร์" are unchanged (callback of s01). Added: one short eased TRUCK (g 1522-1536, 14 f, 0.9 D sideways, no zoom) while the wire settles on the glass; it moves the scene right, away from the glass, so his head stays clear of the bottle (the first try, in the other direction, slid his head over the glass).
- The snap itself is x2.4 with a smaller pan (-0.55 D), so his hair no longer touches the right frame edge at the snap peak (head x <= 600 px at g 1486).
- Head at the end 190-285 px wide, centre y 452-707, lowest head bottom 674.

## Seconds per frame
10.77 s wall / 17.5 s CPU (720x1280, 7 spp, 2 procs x 2 threads).
