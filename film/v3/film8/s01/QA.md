# s01 QA: film 8, shots 1-2 (the hook): desert_ice plain, NIGHT

Delivered: `frames/g_0000.png .. g_0183.png` (184 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 0, 184 frames). g 0..74 = shot 1 (plan 0.00-2.50 s), g 75..177 = shot 2 (plan 2.50-5.92 s),
g 178..183 = 6-frame out-handle (the finger hold and the push continue, rendered in 3D). Shot 3 (bazaar) is NOT in this take.
Two set-ups in one location and one process (same build, same light), joined by the plan's cut at g 75:
id 1 = shot 1 wide (`raw/s1`), id 2 = shot 2 medium (`raw/s2`). Only the per-frame report JSONs are kept in `raw/` (PNGs deleted after
delivery to save disk: `frames/` holds the same pixels; re-running `deliver.py` needs `shot.py final` first).
Also `meta.json` (first_g 0, n_frames 184, events, set-ups), `cues.json` (11 cues, film seconds), `contact.jpg` (16 frames, cyan line =
y 880), `compare.jpg` (g 30 beside ref a t0072: night, figure in the lit set under a starry sky; g 100 beside ref a t0083: night medium,
figure against the sky with a lit tower behind). Scripts: `shot.py` (probe / stills / final), `deliver.py`, `qa.py` (-> `work/qa.txt`),
`sheet.py`; shared helpers in `../common.py` (gotchas at its top). Drafts `work/d1..d6.jpg`, sky azimuth probe `work/sky.jpg`, pose tests
`work/pt.jpg`.

## Client rules
- **No depth of field anywhere**: `cam.data.dof.use_dof = False` and `D.setup_dof(scene, None, None, cam=cam)` at build and before every
  render (common.Take); desert never sets DOF. Everything is sharp: the dome's steps 50 D away, the stars, the lantern posts.
- **User taste**: wide / medium framings that show the set (channels running to the yakhchal with its glowing door, the Milky Way, the
  mountains and palms, lantern posts); calm moves only (shot 1 a slow push 1.8 D; shot 2 a slow push ~0.9 D + 2.5 deg orbit); no text
  signs at all.
- **Heads above the caption band**: shot 1 head centre y 737-744 (0.58 H, a wide), bottom <= 797; shot 2 636-666 (0.50-0.52 H), bottom
  <= 775. Below y 880 only legs, the pour stream, the bank and the water.
- **Mouths only on quoted lines**: shots 1-2 have no quote -> no lip-sync, static expression mouths (determined -> smile in shot 1;
  smile throughout shot 2). Expression changes sit behind blinks (g 65, 117, 162).

## Timing (captions.json, narration at +0.10 s)
| g | what | caption |
|---|---|---|
| 0-8 | farid on the bank tips the wooden bucket (pour 0.35 -> 0.85), the stream starts | "ชายคนนี้เท" (-0.01) |
| 3-66 | the stream pours into channel 4, two faint ripple rings spread where it lands | "น้ำลงร่อง" 0.65, "ตื้น ๆ" 1.30 |
| 48-66 | the bucket empties (tips on to 1.0, water 1 -> 0.15) | "กลางทะเลทราย" 1.68 |
| 62-74 | the stream stops, he straightens, satisfied smile (behind the blink at g 65) | |
| 75 | CUT to the medium (plan shot 2) | "ทุกคืน" 2.52 |
| 77-112 | looks up at the Milky Way in wonder ('excited', round eyes, gaze up), eyes drifting over the stars | "แล้วบอกทุกคนว่า" 2.98 |
| 113-125 | eyes come down to the lens ('happy', behind the blink at g 117) | "หน้าร้อนนี้" 4.08 = g 125 |
| 138-148 | the right index finger goes up beside his head | "เขาจะขาย" 4.78 = g 146 |
| 160-183 | smug tilt ('smug' behind the blink at g 162), finger keeps a small bob (handle 178-183) | "น้ำแข็ง" 5.37 = g 164 |
Camera: shot 1 from the west over channel 4 looking ENE (az 78 -> 79, pitch +2, 22 mm, z 3.1 -> 2.95), push 1.8 D; shot 2 low WSW of
him looking NE and up (az 70 -> 72.5, pitch +9 -> 9.5, 22 mm, z 2.05), push ~0.9 D + orbit. Both moves are 0.35 sine + 0.65 linear.

## Staging (`work/qa.txt`)
| set-up | head width px | centre x | centre y (H) |
|---|---|---|---|
| shot 1 wide (g 0-74) | 85 -> 105 | 391-460 | 0.58 |
| shot 2 medium (g 75-183) | 175 -> 217 | 210-232 | 0.50-0.52 |
Farid stands at (-6, 11.6), the bank lane between channels 4 and 5 (not D's farid_pour mark (-6, 8.8): the x -9 lantern post sat across
him for any camera west of him, see common.py gotchas). Sprites 256 px/D (shot 1), 320 px/D (shot 2).
Popcheck: one jump, the planned cut 74 -> 75 (40 levels). Near-still pairs only at g 0-1 and 77-78 (isolated, no run > 2); frame change
median 0.53 levels. No black / magenta frames, no retried frames. `clipped` sprite warnings g 6-28 are the pour stream running past the
canvas bottom (0.125 D below the feet) -- the clipped end lies at the water line on screen, checked at full size (g 7, 30, 66).

## Fixed after looking at full size
- Draft 1 used D's farid_pour mark and a camera from the WNW: the x -9 lantern post and its halo covered the bucket and the stream.
  Farid moved to the next bank lane, channel 4.
- Draft 1 shot 2 (camera z 2.15 looking up 19 deg): head centre at 0.62-0.66 H, chin under the caption band. Camera z 2.05, pitch 9.
- The preset direction showed no Milky Way; a sky probe (`work/sky.jpg`) found the core at az ~60-75 (desert_API says 35). Both
  set-ups now look ENE: Milky Way core + band, dome and glowing door in every frame.
- Looking up: 'happy' (closed arcs) and 'neutral' (half lids, read smug) hid the look; 'excited' + gaze (0.4, -1) reads as wonder.
- The raised finger on the far arm (arm_l) hid behind the head; now arm_r (screen-right, free sky side). To keep the bucket in the right
  hand across the cut, the emptied bucket stands on the bank as a 3D prop (D._bucket) in set-up 2, partly behind his leg.
- Ripples: first version (3 thick rings) read as a target; now 2 thin faint rings that fade out as they grow.
- First full final rejected by qa.py: 15 near-still frames in a row (g 168-182) and runs at g 0-9, 75-80, 90-96 (sine-eased small
  pushes, still holds). Moves made mostly linear and larger, idle life added; all 184 frames re-rendered.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 shot 1 wide (g 0-74)                        0.3    1.7    0.0    0.0    0.0   95.0    2.8    0.2  0.60 0.49 0.00
s01 shot 2 medium (g 75-177)                    1.5    4.6    0.0    0.0    0.0   90.3    2.5    1.1  0.61 0.50 0.01
s01 all (g 0-183)                               1.0    3.5    0.0    0.0    0.0   92.2    2.6    0.7  0.61 0.49 0.01
ref a t0072 t0073 (night wide)                  0.7    0.1    0.0    0.0    0.0   93.2    5.0    1.0  0.66 0.60 0.01
ref a t0083 t0084 (night medium)                1.2    1.5    0.1    0.0    0.0   70.9   18.5    7.8  0.53 0.62 0.02
```
Night blue like ref a's night wide (blue 95 / 93, sat 0.60 / 0.66); warm accents from the dome door, the lanterns and the turban
(orange 1.7-4.6). Value 0.49 is a little under the ref's 0.60 (the set's NIGHT preset; not graded here -- do it in the conform if wanted).
Magenta <= 1.1.

## Seconds per frame
9.62 s wall / 18.9 s CPU mean (2 threads, two render processes at once on 4 cores, denoise FAST, 12 samples): shot 1 wide 9.39 s wall /
18.4 s CPU, shot 2 medium 9.79 s / 19.3 s. Whole take 184 frames in ~15 min wall with two processes.

## Differences from the plan / known issues
- Shot 1 "channels_wide, slow push" is a custom camera, not the preset's (the preset looks ESE and down: no Milky Way, figure 60 px).
- Shot 2's bucket changes from the hand (end of shot 1) to the bank (shot 2): a time ellipsis across the cut.
- The stream's splash is two ripple rings (the set has no splash); no water-level rise in the channel.
- A lantern post at the far right edge of shot 1 is partly cropped in the first frames (warm practical, left as framing).
