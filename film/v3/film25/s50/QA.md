# QA s50 (film 25, g 1493-1525)

## Render
- 45 frames g 1487-1531 (row g 1493-1525 + handles), 82.1 s wall / frame mean (min 66.0, max 119.7), 146.5 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.460 p1 0.061 p99 0.793 lc 0.0321 sat 0.469 chroma 28.6 a +2.2 b +2.4 p98 0.98 blue 0.35 warm 0.57 neut 0.04 M 88  PASS  (guides off: p99,lc)
```

## qa_jitter
```
overall median jitter px 1.34
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 7.8 -> 7.1 D (scale +10.6 %), lateral camera travel 2.4 D = 39 % of the frame width per second (frame width 5.7 D at the subject)
