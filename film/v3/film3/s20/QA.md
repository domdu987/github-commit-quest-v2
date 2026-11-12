# s20 QA: film 3, shot 20 (the end), harbor set NOON

Delivered: `take.mkv` = g 1847..1967 (121 frames, first_g 1847, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), from `frames/` (not in git). g 1856..1967 = shot 20 ([g0, g1) = [1856, 1968), the last film frame is 1967); g 1847..1855 = 9-frame in-handle for the 15-frame dissolve from s18 (the camera's push runs on before g 1856, rendered in 3D). `meta.json`, `cues.json`, `contact.jpg`, `qa.json`. Scripts: `shot.py`, `fx.py`, `deliver.py` + `take_cfg.py`. Raw: `raw/s20`.

## What it shows
Low and close on tommy's tin bucket, still in its place at bucket_mark under the burst seam, brim-full and overflowing (dark glossy dribbles down its sides, fill 1.0) in a glossy sheet of molasses covering the yard and the tank's foot ring; the swollen plate (bulge 0.66 D) with the dark split seam and most of its rivets gone; glossy elongated drops keep forming at the seam strip and falling into the bucket, each leaving a ring on the surface (lands g 1867, 1897, 1926, 1955). Slow eased push in to the last frame.

## Timing / camera
| event | g |
|---|---|
| handle / dissolve in | 1847-1855 / 1849-1863 (15 f) |
| push key on "ยังวางอยู่" (speed change) | 1899 |
| drops land in the bucket | 1867, 1897, 1926, 1955 |
| "เต็มจนล้น" | 1927 |
| last frame | 1967 |
Camera (px/frame at 2.5 D): min 1.4, median 4.8, peak 7.1; no static runs. Two near-constant-speed stretches (g 1866-1880, 1922-1947): the slow push carries a 35 percent constant-speed share by design so the final hold never parks; the drops and rings keep the picture alive.
No actors (heads n/a). Popcheck: no pops, no near-still runs.

## Colour
```
                         red orange blue violet magenta  sat  val  dark
shot 20 (g 1856-1967)   92.0   0.4   1.3   3.0   3.3   0.51 0.41 0.14
all (g 1847-1967)       92.0   0.4   1.3   3.0   3.3   0.51 0.41 0.15
```
Red-dominant: the brown tank wall and the molasses fill the frame (as in s16/s18 shot 18; the paint renders at hue 16-24, harbor_REVIEW.md section 2). Shade blue-violet; magenta in band; dark share in band.

Seconds per frame: 13.5 s wall / 26.6 s CPU mean (two 2-thread processes in parallel).

## Differences from the plan / runtime changes
- After the flood the set has no aftermath state: shot.py adds a glossy molasses sheet over the yard round the foot of the wall, a glossy collar over the concrete foot ring, a few raised puddles, the split seam ribbon on the swollen plate, hides most seam rivets (popped), and gives the bucket's fill and overflow a dark glossy brown (the set's molasses read magenta in this light). The set's dot drop is replaced by fx.py's elongated falling drop.
- The bucket stands in a thin sheet, not buried: a house-high wave would have buried it, but the plan's ending image is the bucket "still in its place, overflowing".
- Rendered twice: the first pass had a hot yellow sun glint on the molasses collar and invisible dribbles; fixed (collar gloss 0, darker dribbles standing proud of the bucket).
