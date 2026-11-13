# s34 QA: film 6, shot 34 (next morning: Henry adds the 13th himself), bakery MORNING — render team 7

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps), first_g 2959, 122 frames g 2959..3080.
- g 2959..2964: 6-frame in-handle for the dissolve from shot 33.
- g 2965..3074: shot 34 (plan 98.83-102.50 s).
- g 3075..3080: 6-frame out-handle.

All frames, handles included, were rendered in 3D. Also included: `meta.json` (transition_in "dissolve"), `cues.json`, `contact.jpg`
(red line = y 880), `compare.jpg` (finals + ref a t0046 / t0001), `shot.py`, `deliver.py`, and `work/qa.txt`.

## What is on screen
From the street over the shutter board, in the s01 camera family (24-28 mm, custom). Kit is on his hidden stool behind the inside counter
at the left, Henry stands behind the counter at the right, and the customer's basket of 12 sits on the counter between them.
- **A** g 2959..3002 (1.47 s): Henry counts the loaves himself, his finger (one finger up) tapping along the rows; kit watches,
  worried; slow push. Captions: "เช้าวันต่อมา ลุงเฮนรี่".
- **B** g 3003..3045 (1.43 s), framing cut: punch-in on Henry and the basket.
  - He brings the **paler 13th loaf** up from under the counter (3014..3024) and looks at it, pleased (3024..3032).
  - He sets it on the very top of the pile; it lands at g 3042, on "สิบสามใส่" (g_of 101.25 = 3041). The basket card switches 12 -> 13,
    and the top loaf in the 13 drawing is pale.
- **C** g 3046..3080 (1.17 s in the take, 0.97 s of shot), framing cut: two-shot with a push toward kit. Henry turns to kit and gives
  one slow nod (3052..3072). Kit beams: grin, a little hop, fist up (from 3056).

## Client rules
- **No DOF / sharp**: DOF is off at build and before every render; steam is kept at 0.35, as in s01, so it never veils faces.
- **Heads above the caption band**: no head bottom below y 880 on any frame. Main heads: Henry 0.44..0.48 H; kit 0.41..0.48 H.
- **Mouths**: no quoted line, so static expression mouths only (Henry unimpressed -> happy; kit worried -> surprised -> grinning).
- **Continuity**: the 13th loaf is the pale one. Henry's held loaf is drawn with a pale crust (`cast6.BREAD` is patched only while
  Henry's sprites render), and the 13-loaf basket drawing has a pale top loaf.

## Set change at runtime
The hand balance (`small_*` objects) is hidden in this take, because it stood directly in front of Henry from these cameras. The set
module is not edited.

## Numbers
- Heads: Henry 172..280 px, kit 190..315 px. In B kit is out of frame at the left (punch-in on Henry).
- Popcheck: the only jumps are the two planned framing cuts (3002->3003, 3045->3046). One near-still pair at 3003->3004: the first frame
  of the B push, which then moves.
- No black or magenta frames; no retried frames.

Hue (shot frames):
- s34: red 52.6, orange 36.5, blue 0.5, violet 0.8, magenta 8.1, sat 0.44, val 0.55, dark 0.05.
- Warm interior, as the set measures it: the same look as s01 and bakery_API 7. The bakery is warmer than ref a, with almost no blue.
  Grade all bakery shots alike in the conform if needed.

## Seconds per frame
21.0 s wall / 40.6 s CPU mean, with 12 samples, 720x1280, 2 threads and two render processes on 4 cores.

## Differences from the plan / known issues
- "DAWN": the set has MORNING / AFTERNOON only, so MORNING is used (as in s01).
- The hand balance is hidden (see above).
- The counting reads as finger taps over the pile. Henry's hand is pinned near the top of the basket; the forearm is partly behind
  the basket card.
- The pale loaf is small on screen in B (about 50 px); it reads by its lighter colour against the golden pile.
