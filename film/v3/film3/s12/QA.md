# s12 QA: film 3, shot 12 (the foreman kicks the bucket away), harbor set WINTER

Delivered: `take.mkv` = g 1008..1138 (131 frames, first_g 1008), 720x1280, 12 samples, 2 threads, no captions or audio.
g 1008..1130 = shot 12 ([g0, g1) = [1008, 1131)); hard cut in; g 1131..1138 = 8-frame out-handle (12-frame dissolve to shot 13,
rendered in 3D, camera continues). `meta.json`, `cues.json` (kick, clatter, splash, drips, punch, quote...), `contact.jpg`.
Scripts: `shot.py`, `lib3.py` (shared, identical in all my takes), `deliver.py` (`deliver.py qa` prints the numbers below).

## Timing
| event | g | s (film) |
|---|---|---|
| hard cut in ("หัวหน้าเตะ") | 1008 | 33.60 |
| wind-up (lean back) | 1027..1032 | 34.23 |
| KICK: boot on the bucket (t 34.4), small camera jolt | 1035 | 34.50 |
| bucket flies right, lands on its side / bounce | 1047 / 1053 | 34.90 |
| snap punch-in on the foreman (quint, 8 f) | 1050..1058 | 35.0 |
| quote, mouth moves (t 35.3..37.3) | 1062..1122 | 35.40..37.40 |
| reframe left onto tommy | 1092..1104 | 36.4 |
| end (dissolve out to 13) | 1131 (+8 handle) | 37.70 |
Framing changes: 1008 cut, 1035 jolt, 1050-1058 punch, 1092-1104 reframe, slow push to the end (gaps 0.9, 0.5-0.8, 1.1, 0.9-1.2 s).

## Picture
- Custom eye-level camera on the base_eye line (looking at the bucket seam, yaw 17.8 deg) but nearer (6.4 -> 3 D) so the heads
  read: the foreman (near, smug, cigar) beside the bucket, tommy behind him at the left by the barrels, worried.
- The kick: foreman_kick with the boot swinging in over 3 frames; the boot (foot_r anchor) lands on the bucket's near side on
  g 1035 (probe: foot 512,815 px vs bucket side 545,810 px before the last 0.1 D shift); in-betweens to the smug after-pose
  over g 1042..1047 (puppet.lerp_pose, no pop). The set bucket is keyed (location/rotation Bezier) on a flight out of frame to
  the right, fill 0.3 -> 0 (sloshed out) and a glossy molasses splash grows where it stood.
- Quote: foreman thumbs over his shoulder at the tank, lip-sync cycle (talk_a / talk_b / talk_o / flat, a new drawing every
  2 frames) strictly inside g 1062..1122; mouth closed with the cigar everywhere else. Tommy never talks.
- Tommy: worried, flinches on the kick (squash, head jolt, shocked eyes for 10 frames, gaze follows the bucket), sweat.
- Drip: the set's seep dot is hidden and replaced by an animated glossy drop (swell, stretch, fall) every 22 frames: into the
  bucket before the kick, onto the ground after.

## Staging (raw/s12/*.json)
| part | main | head w px | centre y (H) | heads below y 880 |
|---|---|---|---|---|
| two-shot g 1008-1049 | foreman | 128-152 | 0.41-0.43 | none |
| | tommy | 118-137 | 0.49-0.51 | none |
| punch-in / quote g 1058-1091 | foreman | 250-267 | 0.44-0.46 | none |
| on tommy g 1104-1130 | tommy | 219-244 | 0.46 | none |
(The foreman's head rises to 0.30 H at the right edge in the final reframe, when tommy is the subject.)
Nobody's back to the camera. head_flip from the key direction (lib3.head_flip_for).

## Checks
Popcheck: no pops (the first final had one at g 1041 -> 1042, the switch from the kick pose to the after-pose: fixed with
in-betweens and re-rendered). No near-still transitions (the first final had 1045-1049 and 1058-1059: the two-shot push was
lengthened and the post-punch segment starts moving; re-rendered g 1008..1091). No black/magenta cards, no retried frames.
Render: 15.2 s wall / 29.4 s CPU per frame (mean; two render processes running).

## Colour (`hue_report.row` on the final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s12 shot 12 (g 1008-1130)                      82.2   11.8    0.0    0.0    0.0    2.6    0.5    2.9  0.42 0.53 0.06
```
The brown painted tank wall fills the background (the set's WARM base_eye measured 79 % red for the same reason,
harbor_REVIEW section 2); shade on the yard reads blue-violet, magenta 2.9 %, saturation and value in band. Dark 0.06: the
trestle / barrel shadows over the near yard.

## Differences from the plan
- Camera nearer than the base_eye anchor (same line of sight) so the two heads are 118-275 px.
- The kicked bucket leaves the frame to the right (it is not shown again in this take); the splash stays.
- The foreman's quote gesture is a thumb jab over his shoulder at the tank instead of a laugh with mouth open (mouth may only
  move inside the quote); the "laugh" sfx cue is a closed-mouth chuckle after the kick.
