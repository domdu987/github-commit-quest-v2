# s10 QA: film 8, shots 10-12 (night 1 thin ice, night 10 thick ice + finger tap, dawn: saw and carry): desert_ice plain

Delivered: `frames/g_0775.png .. g_0969.png` (195 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 775, 195 frames; 53.8 MB, committed as `take.mkv.partaa` + `.partab`
(`cat take.mkv.part* > take.mkv`)). g 775..780 = in-handle (cut in), g 781..839 = shot 10, g 840..881 = shot 11, g 882..963 = shot 12,
g 964..969 = out-handle (the walk continues). Plan cuts at g 840 and 882 inside the take. Three builds (one process per set-up):
shots 10-11 NIGHT (channel_ecu), shot 12 DAWN (channels_wide). Scripts: `shot.py`, `deliver.py` (-> `work/qa.txt`, `work/hue.txt`).

## What happens
- **Shot 10 (g 775-839)**: low over channel 3 (y 7.4: the channel without the sawn hole, so night 1 has no hole) looking east down the
  channel to the dome's glowing door, Milky Way in the sky. Open starlit water freezes into the thin translucent frost sheet: set_ice
  0 -> 0.25 keyed per frame g 790..830 ("แข็งเป็นแผ่นบาง ๆ" = g 812). Slow low push 1.1 D.
- **Shot 11 (g 840-881)**: night ten, thick white-blue slab. farid crouched on the north bank leans over the channel; his right index
  finger is pinned to an ice point (actors.world_to_local) and taps at g 850 / 858 / 866 ("หนาเท่านิ้ว" = g 862); excited round eyes ->
  pleased closed-eye smile (behind the blink at 873). Push + 4 deg orbit.
- **Shot 12 (g 882-969)**: dawn wide over the channels from the west: farid saws at the hole in channel 2 (stroke every 10 frames,
  g 882-911), rises with an ice block (912-921) and walks east toward the dome carrying it (922-969). Cut blocks wait on the bank.
  Warm-lit wall and dome (dawn key from the north-west, as s08 shot 9), sunrise sky. Slow push.

## Checks (`work/qa.txt`)
| set-up | head width px | centre x | centre y (H) | below 880 |
|---|---|---|---|---|
| shot 10 | no actor | | | |
| shot 11 (g 840-881) | 159-182 | 310-412 | 0.38-0.41 | none |
| shot 12 (g 882-969) | 76-98 | 486-580 | 0.50-0.55 | none |
Popcheck: only the planned cuts 839 -> 840 and 881 -> 882. Near-still: one run g 775-777 (in-handle, 3 frames, < 6). No magenta / black
frames, no retried frames. No DOF, no text signs, no mouth movement (no quote).

## Colour (`work/hue.txt`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s10 shot 10 freeze (g 781-839)                  0.8    2.8    0.0    0.0    0.0   91.0    4.4    0.8  0.54 0.52 0.00
s10 shot 11 tap (g 840-881)                     0.9    4.1    0.0    0.0    0.0   90.9    3.5    0.7  0.51 0.64 0.01
s10 shot 12 dawn carry (g 882-963)             73.1    2.3    0.0    0.0    0.0   15.3    7.9    1.4  0.44 0.74 0.00
ref a t0072 t0073 (night wide)                  0.7    0.1    0.0    0.0    0.0   93.2    5.0    1.0  0.66 0.60 0.01
ref a t0061 (sunrise)                          54.5   26.1    1.9    0.0    0.0    0.0    3.9   13.6  0.49 0.68 0.26
```
Night shots match ref a's night blue (91 vs 93); dawn shot warm red mud + violet sky, magenta 1.4.

## Seconds per frame
15.3 s wall / 29.2 s CPU (shot 10), 13.2 / 25.9 (shot 11), 12.3 / 23.4 (shot 12); two processes x 2 threads.

## Differences from the plan / known issues
- Shots 10-11 are on channel 3, not the channel_ecu preset's channel 2 (the preset's channel has the sawn hole, wrong for night 1).
- Shot 11 is a low medium of farid crouching (not an extreme close-up of a finger: user taste); the taps are small (0.22 D lift) and the
  fingertip sits at the bank edge of the ice, readable but not emphatic.
- Shot 12 shows sawing + carrying toward the dome; he does not reach the dome inside 2.7 s (40 D away).
- Dawn key direction overridden at runtime (warm-lit dome and wall instead of silhouettes), as in s08.
