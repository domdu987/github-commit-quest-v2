# s31 QA: film 7, shot 31 (the ending): louvre wall_eye, slow push to her glass, the reflection of the man in the cap

Delivered `take.mkv`: frames g 3090..3218, 129 frames at 720x1280. Render: 12 samples, 2 threads, denoise FAST. No captions or audio. Encoded libx264rgb crf 6, 30 fps.
- `meta.json`: first_g 3090, n_frames 129, transition_in "cut".
- g 3090..3095 is the 6-frame in-handle, rendered in 3D (the push is already moving).
- g 3096..3218 is shot 31 (plan 103.20 s to the end, N 3219). There is no out-handle: g 3218 is the last frame of the film.
- Also in this folder: `cues.json`, `contact.jpg` (cyan line = y 880), `compare.jpg`.
- Scripts: `shot.py` (probe / stills / final), `deliver.py`, `qa.py` (writes `work/qa.txt`), `sheet.py`. Shared helpers are in `../common.py`, unedited.

## Client rules
- **No depth of field.** C.Take sets the DOF off at build and again before every render. Everything is sharp: the damask, the gilt frame, her face, the glass sheen.
- **Mouths.** Nobody speaks. The reflection has static expression mouths only: neutral, then a small proud smile at g 3150.
- **Heads above y 880.**
  - The only head is the reflection's: its centre y is 727..824 px and its width 78..146 px. Its bottom stays above 880.
  - Her face centre (the main subject) is at y 582..603 = 0.46..0.47 H.
- **Dense set.** The salon hang surrounds her at the start. The push ends close on the frame: the gilt frame, the glass, the hooks and the plaque.

## Timing (narration at +0.10 s)
| g | what | caption |
|---|---|---|
| 3090-3218 | One continuous slow push. The camera goes from the rope (y 16.3, 24 mm) to 1.9 D from her glass, drifting slightly up and left. The ease-out keeps an 18 % linear part, so the last second still moves (no still frames: the minimum frame change is well above the still threshold) | "ยิ้มอยู่หลัง กระจก" (102.56 / 103.32 s) |
| 3134-3146 | The reflection fades in on the glass | "ไอ้มักกะโรนี" 104.38 s = g 3134 |
| 3146-3176 | The reflection holds at opacity 0.34. Small proud smile at g 3150, blink at g 3160 | "ติดกระจกให้" 105.12 s |
| 3176-3192 | The reflection fades out | "เธอครั้งแรก" 106.01 s = g 3183 |
| 3192-3218 | Her alone behind the glass, held to the end (still pushing slightly) | end 106.70 s |

**How the reflection is made.** It is a `vincenzo` actor card (normal clothes, flat cap, moustache), scaled 0.40 and placed 0.012 D in front of her glass, over the lower right of the canvas. Its card material:
- multiplies the sprite alpha by a keyed opacity;
- tints the colour 35 % toward a cool glass sheen;
- masks the card to the glass rectangle in world x/z, so it never shows on the gilt frame or the wall.

It moves a little against the painting during the push, the way a real reflection would.

## Measured (`work/qa.txt`)
- **Popcheck:** no pops. No near-still transitions. Frame change: median 5.2 levels, maximum 7.6.
- **Frames:** no magenta or black frames, no retried frames, no clipped sprites.
- **Speed:** 8.76 s wall / 17.2 s CPU per frame on average. This ran as one of two 2-thread processes at the same time.

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s31 all                                        82.5   14.9    1.5    0.1    0.0    0.1    0.2    0.6  0.70 0.63 0.01
ref a t0040 t0046 t0051                        40.7   38.0    2.8    0.3    0.0    9.8    4.3    4.1  0.41 0.46 0.13
```
Red is very high (82.5, saturation 0.70) because the push fills the frame with the set's red silk damask around her. I did not grade it. If wanted, it can be calmed in the conform. Magenta is 0.6.

## Differences from the plan / known issues
- "Slow push … hold to the end" is done as one continuous push with no cut. The brief asks for a framing change every 1.0–2.0 s; here the framing changes continuously, and there is the reflection event in the middle.
- Draft 1 had two visitors at the rope at the frame edges. Their heads sat on or below y 880, so I took them out. She is alone in the shot.
- The reflection's cap is small at this scale. The figure reads as the small moustached man; the grey cap is visible but subtle.
