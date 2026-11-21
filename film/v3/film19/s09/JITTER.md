# s09 JITTER.md (film/qa_jitter.py on take.mkv, every second <= 2.0 px wanted)

```
  3s shake   2.1px
overall median jitter px 1.59
```

Change in this pass: the 1.5 Hz periodic zoom pump in lens_scale is removed; only the eased one-shot punches stay (x1.10 at the deep bow g 722, x1.16 on the quote g 748, eased back). The frame-diff dropped without the pump (3.81 / 7.96), so smooth one-directional travel was added: slide 25 -> 60 px/s, orbit 7 -> 11 deg/s, snap k 1.12 -> 1.16 (peak 3.0).
Before: seconds 2 and 3 = 2.2 / 3.2 px. Now: only second 3 (g ~742-772, the snap) is listed, **2.1 px**, 0.1 px above the 2.0 limit; seconds 0-2 are under 2.0 and the overall median is 1.59 px. The remainder is the mock-royal bow sway of the actor (qa_jitter's phase correlation locks onto the large figure): see s08/JITTER.md for the measurement (camera alone 0.27 px).
