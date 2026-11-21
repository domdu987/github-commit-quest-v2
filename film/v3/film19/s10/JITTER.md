# s10 JITTER.md (film/qa_jitter.py on take.mkv, every second <= 2.0 px wanted)

```
overall median jitter px 0.26
```

Change in this pass: the `_Sway` handheld sway (0.065 D at 2.6 Hz lateral + 0.05 D at 3.4 Hz vertical) is removed completely; the camera is the plain `c19.CamPath` (shot.py `CAM`). Before: 2.6-3.3 px per second. Now: no second above 2.0 px, overall median 0.28 px (also 0.23 px on the draft without any travel, so no hidden oscillation). 
Without the sway the in-shot frame-diff fell to median 2.47 / p90 11.51 (draft). Smooth one-directional travel was added: push 3 -> 4 %/s, a crane up of 36 px/s (eased, never oscillating) and a 2 deg/s arc. (A lateral slide of 45 px/s pushed the left astronomer out of the frame.) The actor-hidden check was not needed: nothing is flagged.
