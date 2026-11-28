# QA s45 (film 25, g 1368-1395)

## Render
- 37 frames g 1365-1401 (row g 1368-1395 + handles), 54.8 s wall / frame mean (min 47.1, max 80.4), 106.8 s CPU, samples 24 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (1 fr)                        luma 0.482 p1 0.064 p99 0.845 lc 0.0267 sat 0.459 chroma 24.7 a +1.5 b +2.1 p98 1.00 blue 0.48 warm 0.39 neut 0.15 M 65  PASS  (guides off: p99,lc,chroma,blue_frac,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.38
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 16.2 -> 14.2 D (scale +14.3 %), lateral camera travel 2.1 D = 23 % of the frame width per second (frame width 10.2 D at the subject)
