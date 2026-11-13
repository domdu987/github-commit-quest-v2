# s18 QA: film 4, shots 18 (NIGHT cutaway reveal) + 19 (DAY diagram of the mechanism), pagoda set v2, render worker 4

Delivered: `take.mkv` = `frames/g_1593.png .. g_1842.png` (250 frames, 720x1280, 12 samples, 2 threads; meta.json first_g 1593, n_frames 250).
g 1600..1686 = shot 18, g 1687..1835 = shot 19; 12-frame dissolve 18 -> 19 mixed at g 1681..1692 (smoothstep, raw handles: shot 18 to g 1692,
shot 19 from g 1681). In-handle g 1593..1599 and out-handle g 1836..1842 rendered in 3D. Also `meta.json`, `cues.json`, `contact.jpg`,
`compare.jpg` (6 pairs vs ref a t0099..t0109), `work/hue.txt`. Scripts: `shot.py` (same engine as s17 / s20), `deliver.py`.
Mean 13.4 s wall / 25.6 s CPU per frame.

## Timing
| shot / part | g | what | ref a |
|---|---|---|---|
| 18 A | 1593-1640 | NIGHT, whole pagoda in cutaway against the moon: storeys sliding in alternate directions (amp 1.05 -> 0.85, 0.8 Hz), the pillar swinging the other way through the floor holes, kenta + townspeople small in the base, slow push, light shake | t0099 |
| 18 B | 1641-1692 (cut on "กำลังเต้นหลบ" g 1641) | close on storeys 1-3 cut open: floors slide one way, the pillar the other ("the drunk dance") | t0101-t0103 |
| 19 A | 1681-1730 (dissolve in) | DAY, diagram look: pale cream veil behind and over the ground, tower hidden, whole pagoda cut open; a soft white arrow on every storey (alternate directions, breathing with the 0.5 Hz sway), orange arrow on the pillar foot | t0105 |
| 19 B | 1731-1766 (cut, "กันเอง" g 1732) | middle storeys with their arrows | t0107 |
| 19 C | 1767-1803 (cut on "ส่วนเสากลาง" g 1767) | the lower pillar inside the ground storey as a pendulum, orange arrow at the foot | t0109 |
| 19 D | 1804-1842 (cut, "ลูกตุ้ม" g 1808) | high angle down onto the swinging foot over the stone (top-down as far as the canopy allows) | t0111 / t0101 |
Framing changes: 1600 (in), 1641, 1681-1692, 1731, 1767, 1804, 1836 (out): gaps 1.37, 1.5, 1.3, 1.2, 1.23, 1.07 s.

## State
Shot 18: NIGHT, cutaway on, collapse 1 (dust off), quake 0.8 -> 0.6, camera shake 0.025 D; actors hidden in B (they would sit in the caption band).
Shot 19: DAY, cutaway on, tower / rubble objects hidden, canopy pelmet + bead chains hidden (they blocked the high angle), veil (cream emission,
80 %) at y +7.5 and over the ground, 5 + 1 arrows keyed per frame (shown only while |sin| > 0.2, so they flip direction while invisible).
`soseki_shade` hidden. DOF: 18 A off, 18 B (0,0,9) f 5; 19 A/B off, C (0,0,3) f 4, D the foot f 5.

## Staging
18 A heads (tiny, wide): kenta / merchant / woman2 / farmer centres y 838-873, width ~36 px; bottoms reach ~890 (wide-shot extras).
No mouths move. head_flip False (moon key from screen-left).

## Colour (`work/hue.txt`)
18: blue 72.6, magenta 1.4 (NIGHT: blue-dominant expected). 19: red 39.3, orange 50.4, blue 3.1, violet 3.5, magenta 2.1, val 0.66, dark 0.08:
warm and light on purpose (diagram look on a pale veil); no magenta.

## Differs from the plan / reference
- The pillar swing is small on screen (the set swings the foot 0.3 x the top offset, ~0.3 D); arrows make the opposite motion readable.
- 19 D cannot be truly top-down: the pillar runs up through the camera's place; it is a ~35 deg high angle onto the foot and the gap.
- The pillar arrow is under the foot's lip in D and shows only on part of the swing.
