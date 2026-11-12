# s10 QA: film 2, shot 10 (rod in / rod out montage), tower set DAY, spire

Delivered: `take.mkv` (g 713..805, 93 frames, first_g 713, 720x1280, 12 samples, 2 threads, libx264rgb crf 6) from `frames/` (not in git). g 719..798 = shot 10 ([g0, g1) = [719, 799)); g 713..718 = 6-frame in-handle (9-frame dissolve from shot 9), g 799..805 = 7-frame out-handle (10-frame dissolve into shot 11), both rendered in 3D. `meta.json`, `cues.json` (15 cues), `contact.jpg`. Scripts: `shot.py`, `deliver.py`.

## Timing (four beats, one set-up each, 4-frame quint snaps between them)
| beat | g | set-up | action | narration |
|---|---|---|---|---|
| 1 OUT | 713-739 | A: spire_insert-like, from the south-west (dist 3.1 -> 2.8, slow push) | rod stands in the finial; padre's hand swings in from frame-right (719-726), grabs it 0.55 D above its base and yanks it up and out (726-732), rod and hand leave frame; empty finial | "บาทหลวงสั่งถอน" g 722 |
| 2 IN | 740-771 | B: s01's close from the south-east (yaw -50 -> -45) | nico kneels on the spire tip and hammers the rod back in: hits g 746, 756, 767, rod drops one step (0.15 D) per hit, camera jolt per hit | "เขาก็ปีนขึ้นไปตอก" 745/754, "ใหม่" 767 |
| 3 OUT | 772-785 | C: low, looking up the spire from the terrace (pitch +34..37) | the hand comes in from frame-left, yanks it out again at g 778 | "ถอนอีก" 778 |
| 4 IN | 786-805 | D: wider from the south (dist 4.9 -> 4.5) | nico hammers again: hits g 790, 801 | "ตอกอีก" 790 |
Framing changes: 713 (push), 740-743, 772-775, 786-789 (snaps): gaps 0.9, 1.07, 0.47 s, then the drift of D into the handle. The plan's "every ~0.6 s" is kept inside the beats by the pull and hammer events (726, 746, 756, 767, 778, 790, 801: 0.33-0.67 s apart). Frame change min 0.52 / median 4.93 levels: no still runs, no pops. Nico is hidden in the OUT beats and during the first frames of each snap into B and D (the snap flies the camera past him; he appears on the last snap frame).

## Staging
| beat | nico head width px | centre x | centre y (H) |
|---|---|---|---|
| 2 (g 743-771) | 257-287 | 260-270 | 588-612 (0.46-0.48) |
| 4 (g 789-805) | 182-201 | 328-343 | 578-601 (0.45-0.47) |
No head below y 880, head_flip False (key from screen-left as in s01). Pins: left hand on the rod max 0.068 D, hammer head on the rod on strike frames max 0.053 D (the set-ups B/D differ from s01's yaw by up to 26 deg, so the arm reach limits it slightly; under 15 px).
Padre's hand: built in 3D in the puppet language (stout limb): ink ball r 0.11 D and ink arm r 0.05 D (`#3a2832`) with a violet-grey edge (`#8a7f9a`, padre's `limb_edge`) and a black cassock cuff (`#24212b`) at the frame edge; emission only, no shadow. Enlarged over the true puppet scale (r 0.065) so it reads at 3 D distance. The rod is the set's own rod object (set_rod(1)), moved/rotated about its base and hidden after it leaves frame.

## Colour (hue_report.row on the 93 final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s10 g 713-805                                  21.4    9.4    0.6    3.1    0.0   63.5    1.1    0.8  0.50 0.67 0.02   OUT: red,orange,blue,sat,val,dark
ref a t0062                                    56.9   30.5    2.4    0.0    0.0    0.0    0.0   10.2  0.50 0.70 0.26
```
Day exterior against the open sky (the rod is shown against the sky by design, as in s01 shot 1: blue 44-63 there too): blue above band, few darks; violet and magenta in band, shade on the spire tiles blue-violet. Set-ups B and D look down on the town (less sky) to limit the blue.
Seconds per frame: 8.05 s wall / 15.46 s CPU mean.

## Differences from the plan
- Four beats (out / in / out / in) instead of five (in / out / in / out / in), timed to the narration words ("สั่งถอน", "ตอก", "ใหม่", "ถอนอีก", "ตอกอีก"); the take opens on rod OUT because the line starts with the priest's order.
- Padre's hand is a 3D puppet-style arm, not his actor card (his body would be out of reach of the spire).
- No motion-streak post on the snaps (4 frames each; the take is delivered unstreaked).
