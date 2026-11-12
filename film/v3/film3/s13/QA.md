# s13 QA: film 3, shots 13 and 14 (the unusually warm morning), harbor set WARM

Delivered: `take.mkv` = g 1123..1336 (214 frames, first_g 1123), 720x1280, 12 samples, 2 threads, no captions or audio.
g 1131..1229 = shot 13, g 1230..1329 = shot 14 ([g0, g1) = [1131, 1330)). In-handle g 1123..1130 (12-frame dissolve from
shot 12, rendered in 3D), out-handle g 1330..1336 (10-frame dissolve to shot 15, rendered in 3D). The 10-frame dissolve
13 -> 14 is mixed inside the take (g 1225..1234, smoothstep as film 2; raw shot 13 to g 1236, shot 14 from g 1223 in raw/).
`meta.json` (frame_source per g), `cues.json`, `contact.jpg`. Scripts: `shot.py`, `lib3.py` (shared, identical in all my takes),
`deliver.py` (`deliver.py qa` prints the numbers below).

## Timing
| event | g | s (film) |
|---|---|---|
| in-handle / dissolve from shot 12 | 1123..1138 (mix 1125..1136 at conform) | 37.43 |
| shot 13 starts ("แล้วเช้าวันหนึ่ง") | 1131 | 37.70 |
| crane: second segment (speed change on "อากาศอุ่น") | 1188 | 39.60 |
| dissolve 13 -> 14 (mixed here) | 1225..1234 | 40.83 |
| shot 14 starts ("ที่เด็กคนนั้นไม่รู้") | 1230 | 41.00 |
| push: second segment ("ถังใบนี้ไม่") | 1273 | 42.43 |
| shot 15 starts (out-handle to 1336) | 1330 | 44.33 |

## Picture
- Shot 13: crane from the street_wide position (2, -62, 21) down to street level (1.6, -41, 1.5), looking up the street at the
  brown tank; two eased segments with a 25 % constant-speed share. WARM preset (bright, higher sun). Melting: kerb snow heaps
  sink (height x0.95 -> x0.35), five snow mounds by the kerbs shrink and flatten, eight wet glossy blue patches grow on the
  cobbles. worker1 (happy) and worker2 (smirk) walk toward the camera in shirt sleeves, no coats; kid1 / kid2 play.
- Shot 14: custom low camera at the tank foot (tank_low family, 0.7 D high, pitched up 19-22 deg): tommy beside his bucket
  (back under the drip, fill 0.45), worried, head tilted back toward the wall; the riveted wall with seep strips, ladder and
  cage at the upper right, rim against the sky; slow push in two segments. The drip is the animated glossy drop (lib3.Drip:
  swells at the strip end, stretches, falls into the bucket every 20 frames). A barrel in shade (key gain 0) passes the right
  edge in the first second (foreground dark mass, parallax).

## Staging (raw/*/g_*.json)
| shot | actor | head w px | centre y (H) | heads below y 880 |
|---|---|---|---|---|
| 13 (wide, crane) | worker1 / worker2 | 20-64 | 0.52-0.67 | none |
| 13 | kid1 / kid2 | 16-31 | 0.56-0.62 | none |
| 14 (main) | tommy | 147-183 | 0.54-0.56 | none |
Shot 13 is a wide establishing crane (centre band exempt); at the end of the crane the workers' heads are at 0.52-0.53 H.
No mouths move. Nobody's back to the camera. head_flip set per frame from the key direction (lib3.head_flip_for).

## Checks
Popcheck: no pops. No near-still transitions. No black/magenta cards, no retried frames.
Render: shot 13 8.6 s wall / 16.9 s CPU, shot 14 13.5 s wall / 26.4 s CPU per frame (two render processes running).

## Colour (`hue_report.row` on the final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s13 shot 13 (g 1131-1229)                      35.1    7.1    0.0    0.6    0.2   52.5    3.2    1.3  0.39 0.57 0.08
s13 shot 14 (g 1230-1329)                      81.8   12.6    0.0    0.0    0.0    3.6    0.6    1.4  0.47 0.52 0.06
```
Shot 13: an exterior with sky, blue above the interior band as all set exteriors (set WARM street_low: 50 % blue); red, violet,
magenta, dark in band. Shot 14: the brown painted tank fills the frame (the set's WARM base_eye measured 79 % red for the same
reason, harbor_REVIEW section 2); shade reads blue-violet, magenta 1.4 %. Dark 0.06 (the barrel and the yard shadows).

## Differences from the plan
- Shot 13 ends at a street-level view a little nearer the tank than street_low (y -41 instead of -50) so the workers in shirt
  sleeves read; "sun bright" = the WARM preset as built.
- Shot 14 uses a custom low camera (not the exact tank_low anchor, which points almost straight up the wall and cannot hold
  tommy's head in 0.35-0.59 H). His eyes are the puppet's worried half-lid; "looking up" is carried by the head tilt and pose.
