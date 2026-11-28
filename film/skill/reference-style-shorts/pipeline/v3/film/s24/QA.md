# QA s24 (shot 24): beach, storm

The worker of the beach lane staged this take and started the final render, then returned before it finished. The render ended unattended (raw complete). The main loop ran `shot.py post` and `shot.py qa` at 16:28 and looked at contact.jpg. Beach set, so the red line never appears. No mouths move, so the re-recorded voice does not affect this take.

## Frames
- frames/g_1720.png .. g_1792.png: 73 frames, 720x1280. Take range g0 1720, g1 1788, handles 0 in and 5 out.
- Transitions: hard cut in; TRANSITION_OUT = object_wipe 6 f (foam sheet, added by the conform step on clean frames).
- Final quality: 12 samples. Seconds per frame: {"n": 73, "median": 29.19, "max": 41.84, "cpu_median": 22.92}.
- Streaked frames (plate + matte): [[1764, 'plate'], [1776, 'plate']]. Card retries: [].

## Staging (from the worker's notes, checked on the contact sheet)
Hard cut to the two shocked faces (man's head about 290 px), the boater pops off and flies away from g1729, crash pull-out g1730-1748 with a tilt up, they run out screen right (man out by g1764, woman by about g1770), 5 Hz shake from g1752, the wave fills the left 60 percent with the crest at the top, one cottage with lit windows under the curl.

## Motion (work/qa.json)
- static runs over 6 frames: []
- linear runs over 8 frames: []
- pops: []
- magenta or black cards: []

## Colour
hue_report: `set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        33.6   23.1    0.7    0.5    0.5   29.1    2.7    9.7  0.48 0.63 0.08   OUT: sat,val,dark
reference B, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08   OUT: red,dark
reference A interiors                          40.1   27.6    0.3    0.4    0.0   21.9    1.1    8.6  0.47 0.55 0.09   all in band
reference B interiors                          36.3   37.7    2.3    0.1    0.0   13.9    4.5    5.1  0.38 0.45 0.15   OUT: blue
target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15  (percent of chroma for hue families)
v3/film/s24/frames                              8.7    0.3    0.1    0.0    2.2   83.8    1.5    3.5  0.45 0.45 0.01   OUT: red,orange,blue,val,dark
`
Outside the office band by design (exterior).

## Deviations from the plan
- No wave shadow sweeps the roof at 58.4 (the STORM key comes from the land side).
- No foam crest over the lens in the last frames: the conform step adds the foam-sheet wipe.
- The rowing boat and the LONG ISLAND board are hidden in this take.
- The wave uses the set's STORM colours, not the plan's plum and blue.
- The runners' heads sit at y 830-900 in the wide (about g1752-1770), just under the 880 limit.

## Checked
contact.jpg (16 frames) looked at by the main loop: no pops, no stale sprites, no black or magenta cards.
