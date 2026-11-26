# EP.1 sets: measured cost

Machine: 4 cores shared with the hook final and other builders (load 8-11 while these ran), 1 thread per Blender process, niced. CPU seconds are process CPU (render + post + staging), so they are little affected by the sharing; wall times are not given because they are.

- **Draft test**: 24 consecutive frames, 360x640, 2 spp, the set's cost camera (marked on the sheet), two v8 puppets (kong_wet, crew_wet) in frame. The mean leaves out the first frame, which pays the first scene sync and the puppet rasters.
- **Extrapolated final**: draft mean x the hook's own ratio of final to draft (draft 10.3; final 36.6 at 75 %, 68.2 at 100 %: x 3.55 and x 6.62).
- **Measured final**: ONE 720x1280 frame at the final tier (5 spp) at each render scale, first frame of a fresh process (so it includes that process's first sync; a running shot is cheaper by about the difference between the draft first frame and the draft mean).
- Plan's assumption: 36.6 (class B, 75 %) and 68.2 (class A, 100 %) CPU s per frame.

- **Steady final** (checker's re-run): the mean of 3 further consecutive final-tier frames at the shot's class scale in the same process, i.e. what a running shot pays per frame. This is the number to put in the plan; it is 3 frames, not the plan's 24.

| Set | Cost camera (class) | Stage build CPU s (deck + set) | Draft: first frame | Draft: mean of 23 | Extrapolated final 75 % / 100 % | Measured final still 75 % / 100 % | Steady final at class scale (3 frames) | Steady against the plan (its class) |
|---|---|---|---|---|---|---|---|---|
| X1 | S34 (A) | 8 | 13.1 | **12.5** | 44.3 / 82.6 | 47.9 / 82.0 | **84.3** at 100 % | +24 % |
| X1S | S63 (B) | 9 | 11.6 | **10.9** | 38.7 / 72.0 | 43.3 / 70.2 | **43.8** at 75 % | +20 % |
| X2 | S82 (B) | 8 | 10.3 | **11.0** | 39.2 / 73.0 | 39.9 / 64.4 | **39.0** at 75 % | +7 % |
| CAB | S88 (A) | 9 | 10.3 | **8.4** | 29.8 / 55.6 | 25.9 / 41.2 | **41.7** at 100 % | -39 % |
| GEAR | S100 (A) | 9 | 8.6 | **7.7** | 27.4 / 51.1 | 24.3 / 39.0 | **39.0** at 100 % | -43 % |
| STAIR | S111 (B) | 8 | 8.6 | **8.2** | 29.2 / 54.5 | 26.6 / 44.5 | **27.9** at 75 % | -24 % |
| UND | S112 (B) | 10 | 11.6 | **10.9** | 38.6 / 72.0 | 39.9 / 67.5 | **40.2** at 75 % | +10 % |

Per-frame detail is in `out/cost_<SET>.json` (24 records each) and `out/final_<SET>.json`; the frames themselves are in `out/cost/<SET>/` and `out/final/`.
