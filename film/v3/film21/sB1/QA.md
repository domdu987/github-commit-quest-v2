# QA sB1 (film 21, plan v3): g 159-298 + 3 handle frames to 301, CUT in. Re-render on the current set (team 7)
- Re-render of team 2's B1 (their b1.py / c21.py reused) on the current set3d21 / cast21: new muted palette (no red or lime field tiles, no neon cyan edges), English camp without blue (the riders' caparisons are red/gold, footmen and knights default crimson), soft smoke plumes. Path, "ENGLISH CAMP" sign, parade and landing EXACTLY at P_CAMP at g298 unchanged; handles 299-301 continue the move.
- Content changes: removed the blue caparisons and the indigo / olive footman variants (variant21), so the camp is crimson/gold only.
- Mid-dive (g ~192-272) was murky: it looks into the shade. A bump in the VIVID exposure and gamma in this segment only (b1.py render_frame, w_ ramp) lifts it: mean luma 91 (g205), 100 (g222), 103 (g240) at 360x640 draft-style reads; segment mean luma 101.5. No whole-frame post-gamma.
- Colour (qa_stats2): sat 0.507, vivid 51.2 %, luma 101.5. Rhythm: median 11.2, p90 18.2. qa_auto: PASS (one soft frame g231, a motion streak in the steep swoop).
- Cast: 10 caparisoned riders parade from g235, 12 idle and 6 marching footmen, gold rim, contact shadows. Bloodless. The cast is tiny in the wide; no faces are large.
- Not done (optional in the request): extra tents / horse line / cart on the bare green meadow at the end. The foreground there is still a green meadow with a few tents and a flag.
- 32 samples OIDN, about 85 s/frame. take.mkv is split in take.mkv.partaa / ab (cat to rejoin).
