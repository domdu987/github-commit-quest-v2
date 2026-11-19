# s01 QA (v2, after the QA-art / TAKE gate): film 16, shot 1 (the hook) -- LINE line_close, DAY

Redone together with s23 (the callback): same camera, same marks, same bottle-hand method; s23 is AFTER_RAIN with a wet dark pole.

## What changed against v1 (QA-art: bottle merged with the head = mint-jelly blob, wire never seen on the glass, first second mostly sky)
- **Head beside the bottle:** Morse stands one rung lower along the ladder (mark shift -0.25, -0.22, -0.6 D, still on the ladder line) and holds the bottle out toward the pole top. His head is 1.2 D from the pole axis (was 0.7): the inverted bottle body stands against clean sky at the left of his head the whole take.
- **Reads as a beer bottle:** the set's own glass material is tuned at runtime (alpha 1 + transmission 0.8, deep bottle-green, lower self-glow): clear neck, shoulder, body, bright glint, no hashed-alpha grain. The held copy and the set's peg glass share the material (no pop at contact g 47).
- **Wire on the glass:** the camera keeps the glass top and the wire in frame; at g 52-64 the hand flicks the wire over the glass, it settles and the wrap ring comes on at g 65.
- **First second:** camera higher (z 5.3, pitch 25 deg vs 4.4 / 33): ground, fence, trees, poles and the ladder fill the lower half; sky about 35 %. Frame 0 shows the capped pole 2 receding.
- **Expression:** determined while capping, happy from the pose swap on the closed blink frame (g 52).
- **Hand:** after the flick the hand drops to his side (it crossed his face in v1).

## Round 2 (TAKE gate): what changed
- **Free hand below the chin:** after the cap the hand comes down the pole side to chest height, takes the wire at the coil and stays at chest height; it never goes to his face or forehead (hand pins checked: error <= 0.2 D). The v2 claim "drops to his side" was wrong; this version does it.
- **Wire falls and bounces:** the flick lifts the wire in an arc over the glass; it then falls onto the glass and bounces twice (damped) before the wrap ring appears (g 67).
- **Head clear of the glass to the cut (g 54-68):** slide / arc drift reduced, a small truck + crane-up while the wire settles keeps his head right of the glass (head-to-glass distance >= 165 px, head half-width about 130 px).
- **Pole:** unchanged (DAY, dry); the same bottle, hand and wire staging as s23.
- **Frame-diff now (in-shot):** median 7.67, p90 16.8 (target >= 4 / >= 12): MET. qa_auto PASS.

## Delivered
- take.mkv: 75 frames, g 0..74 (shot g 0..68, 6-frame out-handle g 69..74, no handle before g 0), 21.0 MB. Hard cut out at g 69.
- QA_AUTO.md, phone_sheet.jpg, contact.jpg, cues.json, meta.json, framediff.json; shot.py / deliver.py / c16.py regenerated (s23 shares the same shot.py with the shot 23 timing).

## Beats
| g | beat |
|---|---|
| 0-21 | bottle held out over the bare pole top; camera moving on frame 0 |
| 22-35 | SNAP x2.4 + pan (13 f) on "คอขวดเบียร์" (24); sun glint 24-31 |
| 34-47 | lowered mouth-down; contact g 47 (glass clink), flare 47-56 |
| 51-53 | blink: pose cap -> drape, happy |
| 52-64 | hand takes the wire at the coil and flicks it over the glass |
| 65-74 | set wire spans + wrap ring on, smile, hand at his side |

## Checked
- Heads [95, 269] px wide, centre y [486, 610], lowest head bottom 666: nothing in the caption band.
- No text, no DOF, mouths still, no magenta. Contact: he stands on the ladder rung (decal off); hand error <= 0.35 D except the flick.
- Head touches the right frame edge for a few frames at the snap peak; the face stays in frame.

## Frame-diff (in-shot g 1..68)
median 9.12  p90 13.85  (target >= 4 / >= 12): MET.

## Seconds per frame
8.76 s wall / 16.17 s CPU (720x1280, 7 spp, 2 procs x 2 threads).
