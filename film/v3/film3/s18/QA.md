# s18 QA: film 3, shots 18-19 (NOON, the disaster), harbor set NOON

Delivered: `take.mkv` = g 1676..1864 (189 frames, first_g 1676, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), from `frames/` (not in git). g 1676..1855 = shots 18-19 ([g0, g1) = [1676, 1856)); g 1856..1864 = 9-frame out-handle for the 15-frame dissolve into s20 (shot 19's camera, wave and runners run on, rendered in 3D). Hard cut in (from s16) and hard cut 18 -> 19 at g 1744. `meta.json`, `cues.json` (pop-by-pop rivet shots), `contact.jpg`, `qa.json`. Scripts: `shot.py`, `fx.py` (bulge, 3D rivets, tracers), `flood.py` (the improved wave), `deliver.py` + `take_cfg.py`. Raw: `raw/s18` (g 1676-1743), `raw/s19` (g 1744-1864).

## Timing
| event | g |
|---|---|
| shot 18: strained seam, tremor, slow creep in | 1676 |
| first rivet shoots out ("หมุดเหล็กดีด") | 1697 |
| volley accelerates: 64 rivets g 1697..1734 (1-3 per frame at the end), each with a camera jolt | 1697-1734 |
| punch-in ("ออกเหมือน") | 1715-1724 |
| volley peak ("กระสุน") | 1729 |
| seam splits (jagged crack opens to 0.42 D) + gush of glossy blobs, violent shake | 1734-1743 |
| hard cut, shot 19 low down Commercial Street; wave u 0.08 -> 0.42 ("กว่าบ้าน" 1780) -> 0.72 ("เร็วกว่าคน" 1821) -> 1.0 | 1744 |
| crane up and back to the wide | 1790-1830 |
| handle out | 1856-1864 |
Framing changes: 1676, 1697 (jolts start), 1715-1724, 1734, 1744 (cut), 1790-1830, then a slow push; gaps <= 1.2 s except 1830 -> 1864 (slow push on the wide, wave and runners moving).

## Camera (px/frame, re-projected at 4 D in 18, 25 D in 19)
| shot | min | median | peak | static runs | constant-speed runs |
|---|---|---|---|---|---|
| 18 | 2.5 | 12.8 | 234 (g 1737, burst shake) | none | none |
| 19 | 0.15 | 4.5 | 114 (g 1809, crane) | none | g 1845-1850 (6 frames, end of the eased push) |

## Staging (shot 19; wide exempt from the head-centre rule)
| runner | head width px | centre y | min distance ahead of the wave front |
|---|---|---|---|
| worker1 | 22-98 | 620-831 | 14.3 D |
| worker2 | 23-135 | 602-875 | 15.1 D |
| kid1 | 20-73 | 704-836 | 11.5 D |
| kid2 | 19-62 | 697-816 | 9.7 D |
No casualties: every runner stays 9.7 D or more ahead of the front on every frame and is still running at the end. worker2's head crosses y 880 on 5 transit frames of the crane (g ~1806-1810, he is passing under the rising camera). worker1 leaves frame-left for a few frames around g 1800 (passing the camera). Mouths: shocked "O" (static, no talking). head_flip False (sun behind the camera, slightly screen-left).
Popcheck: one flag, g 1744 = the hard cut. No near-still runs.

## Colour
```
                         red orange blue violet magenta  sat  val  dark
shot 18 (g 1676-1743)   94.0   0.8   3.3   0.5   1.5   0.53 0.50 0.05
shot 19 (g 1744-1855)   26.5  21.0  45.7   4.1   2.0   0.40 0.52 0.15
all (g 1676-1864)       56.3  12.1  26.9   2.5   1.8   0.45 0.51 0.11
```
Shot 18 is the brown tank wall filling the frame (red 94: the set's paint renders at hue 16-24; harbor_REVIEW.md section 2); the tracers are near-white. Shot 19 is an exterior with sky (blue above band, as the reference exteriors); orange, violet, magenta, dark in band. Shade blue-violet.

Seconds per frame: 10.2 s wall / 19.7 s CPU mean.

## The flood (WORKER3: improve it) and other runtime changes
- The set's faceted height field is hidden. `flood.py` uses the same flow (harbor.flood_height) on a 0.35 D grid, smooth shaded, x 1.6 in height (crest ~12 D, above the 10-15 D row houses: "สูงกว่าบ้าน"), with travelling ripples and flow streaks; a rolling lip tube along the front (rotates, breathes) that overhangs the face; 36 glossy spray drops thrown forward from the lip, stretched along their velocity; material = toon key + real glossy highlight (kept low: stronger gloss bloomed yellow) + amber fresnel rim.
- Shot 18: 3D rivet heads (fx.py) pop with bright tapered tracer streaks, spin and fly at the lens; thin dark molasses squirts from every third hole; the bulge keeps swelling (0.44 -> 0.66 D); a jagged crack ribbon and a gush of blobs replace the set's rupture for the burst close-up (the set's rupture is used, pushed out over the swollen plate, in the far views of shot 19).
- The bucket is hidden in shot 19 (buried under the wave near the burst); s20 shows it again.
- Shot 18 was rendered twice: the first pass let the later pops fly from rivets outside the punched-in frame, so the volley peak was empty; the pops now come only from rivets inside the frame.
