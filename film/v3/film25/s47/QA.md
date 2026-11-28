# QA s47 (film 25, g 1424-1492)

## Render
- 81 frames g 1418-1498 (row g 1424-1492 + handles), 55.6 s wall / frame mean (min 48.4, max 74.5), 102.0 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (3 fr)                        luma 0.468 p1 0.066 p99 0.900 lc 0.0281 sat 0.445 chroma 27.9 a +2.1 b +3.2 p98 0.94 blue 0.41 warm 0.35 neut 0.06 M 69  PASS  (guides off: p99,lc,chroma,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.36
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 22.4 -> 20.5 D (scale +9.3 %), lateral camera travel 7.2 D = 17 % of the frame width per second (frame width 18.9 D at the subject)
