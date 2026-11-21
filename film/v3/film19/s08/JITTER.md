# s08 JITTER.md (film/qa_jitter.py on take.mkv, every second <= 2.0 px wanted)

```
  2s shake   7.5px
  3s shake   8.8px
overall median jitter px 2.82
```

Change in this pass: the 3 Hz micro-punches in lens_scale (g 611-636) are removed; only the eased one-shot punches stay (x1.17 at the laugh start, x1.14 on the quote). Smooth one-directional travel was added to keep the frame-diff (slide 45 -> 60 px/s, snap pan y -0.25 -> -0.10); the quote punch is x1.14 (was x1.10).
Before: seconds 2 and 3 = 7.4 / 9.2 px. Now 7.5 / 8.8 px: **still above 2.0**.

## Where the remaining jitter comes from (measured, not guessed)
- Same take rendered with the actor hidden (NOACT=1, the camera, lens and set unchanged): **overall median 0.27 px, no second above 2** (work/noact.mkv, python3 shot.py with NOACT=1).
- A projected fixed world point of the set (camjit.py, per-frame screen position from the keyed camera + lens): second differences median 1-3 px in these seconds (rounded to whole pixels by H.project; the snap frame itself is the 17-44 px maximum).
- Actor with hop = 0 and squash x1: still 6.7 / 8.7 px. So the numbers come from qa_jitter's whole-frame phase correlation locking onto the big laughing actor (3 Hz belly bounce, head roll, wig, tears), not from the camera. The camera path is a smooth CamPath plus eased lens punches.
- Reducing it further means changing the acting (bounce amplitude / head roll), which the pass told me to keep. Say if you want the laugh bounce toned down.
