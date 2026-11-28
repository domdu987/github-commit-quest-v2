# QA s53 (film 25, g 1592-1635)

## Render
- 56 frames g 1586-1641 (row g 1592-1635 + handles), 58.2 s wall / frame mean (min 47.9, max 93.1), 103.9 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.474 p1 0.092 p99 0.832 lc 0.0247 sat 0.443 chroma 29.5 a +2.6 b +3.2 p98 0.96 blue 0.39 warm 0.33 neut 0.03 M 67  PASS  (guides off: p1,p99,lc,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.36
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 27.0 -> 24.5 D (scale +10.0 %), lateral camera travel 8.3 D = 28 % of the frame width per second (frame width 21.0 D at the subject)
