# QA s46 (film 25, g 1396-1423)

## Render
- 34 frames g 1396-1429 (row g 1396-1423 + handles), 61.9 s wall / frame mean (min 57.9, max 86.2), 119.3 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (1 fr)                        luma 0.466 p1 0.060 p99 0.858 lc 0.0222 sat 0.444 chroma 26.9 a +2.9 b +4.0 p98 0.99 blue 0.42 warm 0.35 neut 0.09 M 64  PASS  (guides off: p99,lc,chroma,warm_frac,M)
```

## qa_jitter
```
overall median jitter px 1.2
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 21.6 -> 20.6 D (scale +4.8 %), lateral camera travel 10.4 D = 63 % of the frame width per second (frame width 18.2 D at the subject)
