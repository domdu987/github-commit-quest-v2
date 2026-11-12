# s06 QA: film 3, shots 6-7, harbor set WINTER

Delivered: `take.mkv` = g 415..619 (205 frames, first_g 415, 720x1280, 12 samples, 2 threads, libx264rgb crf 6). g 415..421 is the 7-frame in-handle for the 10-frame dissolve from shot 5, rendered in 3D with the shot 6 camera running back. Shot 6 is g 422..541 and shot 7 is g 542..619. The cut out to shot 8 is hard, so there is no out-handle. Also `meta.json` (with frame_source), `cues.json`, `contact.jpg` and the scripts: `shot.py`, `take3.py` (shared engine) and `deliver3.py`. Numbers come from `work/qa.txt`.

## Timing
| event | g | s (film) |
|---|---|---|
| dissolve in from shot 5 (10 f; in-handle 415..421) | 422 | 14.07 |
| wide: tommy (2.48 D) between worker1 / worker2 (3.2 / 3.0 D) at the tank foot, slow eased drift | 415-470 | |
| snap reframe onto tommy (12 f, quint), lands on "tae khao dai yin" 15.8 s | 471-483 (477) | 15.9 |
| tommy cups his hand behind the ear toward the tank (tommy_listen, lerped in) | 478-486 | |
| tank groans: camera jolts, tommy winces | 492, 519 | 16.4, 17.3 |
| dissolve 6 -> 7 (9 f, smoothstep, mixed in this take) | 538-546 | |
| seam insert: set_seep 0.35 -> 1, glossy drops form and fall into the bucket every 24 f; tilt down to the bucket | 542-619 | |
Framing changes: 422 (dissolve), 448 (drift change), 471-483 (snap), 505 (push change), 538-546 (dissolve), 566 and 590 (tilt down). The gaps are 0.9-1.3 s.

## Staging (final frames, `raw/*/g_*.json`)
| shot | head | width px | centre y (H) | heads below y 880 |
|---|---|---|---|---|
| 6 wide (to g 470) | tommy (main) | 90-100 | 0.52-0.54 | none |
| 6 after the snap | tommy | 188-226 | 0.50-0.53 | none |
| 6 | worker2 / worker1 (bigger, he is the smallest) | 124-213 / 81-155 | 0.45-0.51 / 0.42-0.48 | none |
| 7 | no actors | | | |
head_flip is False throughout: the key comes from screen-left at camera heading -10 to -24. Nobody turns their back to the camera, and nobody's mouth moves.

## Camera and pops
Camera speed is measured as px/frame of the fastest of 9 screen points at 8 D. Shot 6: min 0.30, median 2.65, peak 122 (g 477, the snap). Shot 7: min 0.75, median 4.1, peak 28.5 (g 578, the tilt down). No frame is static (under 0.25 px). Frames flagged by the frame-difference check are all intended motion: the snap (475-481), the groan jolts (492-495, 519-521) and the tilt down (576-583). There are no near-still frames. No frames were retried and no cards are black or magenta.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s06 shot 6 (g 422-541)                         32.1   23.0    0.1    0.2    0.0   41.3    1.1    2.2  0.31 0.54 0.07   OUT: blue,sat,dark
s06 shot 7 (g 542-619)                         10.9   60.6    0.0    0.0    0.0   18.6    0.3    9.6  0.20 0.55 0.14   OUT: red,orange,sat
s06 all (g 415-619)                            26.5   31.8    0.0    0.2    0.0   36.6    0.9    4.0  0.27 0.54 0.10   OUT: red,blue,sat
```
Shot 6: blue is high because of the WINTER sky and the long blue-violet shadows (as in the set's REVIEW). Darks reach 0.07 thanks to two shaded barrels in the near-left foreground. Shot 7: the grey steel wall fills the frame and the warm key pushes it to beige (orange), so saturation is low (0.20). Darks are in band (0.14) from the shaded barrel at the lower left. Magenta stays under 10 and shade reads blue-violet. Render time: 12.2 s wall / 24.2 s CPU per frame on average, with two processes sharing 4 cores.

## Differences from the plan / runtime set changes (harbor.py not edited)
- The set's static drop dot is shrunk to nothing. In its place, glossy elongated teardrops (take3.Drops) form at the tip of the seep strip, swell, fall with gravity while stretching, and disappear into the bucket.
- Seep strips and the bucket's molasses get darker materials. The set's glossy seep bloomed yellow in the sun, and its bucket fill read blue in shade. The bucket fill is 0.5 so the molasses shows. The inside of the tin bucket still reads blue-violet in shade (set material).
- Foreground darks: shade-only barrels (key gain 0, no cast shadow), two at the near left in shot 6, plus a barrel and post at the lower left in shot 7.
- Shot 6 uses a custom eye-level camera at heading -10 to -24 instead of `base_eye`, so the tank is screen-right for tommy_listen and the key comes from screen-left.
