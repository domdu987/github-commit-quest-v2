# s27 QA (shot 27, LAST IMAGE, TOWER tower_window_pull -> tower_window_end, g 1968..2045; in-handle 1964-1967; film ends on the hard cut at 2046)
- Crash pull-out: camera log-distance path 6 m from the glass -> 236 m (ease-out power 1.9 over g 1968..2036), aim sweeps from the window to the tower, lens shift 0 -> 0.345 keyed; last 9 frames drift almost still (0.2 frame-diff, never frozen). Starts moving on frame 0; start camera 4 D closer than the preset, aim 3.3 D lower so his head sits at y ~600.
- Maupassant seated at the window table, eyes shut smug (maupassant_seated_eyes_shut_right), head 68 px at g 1968, clear between the X braces, nothing over his face; shrinks with the pull (tiny by design, the lit window then the whole tower).
- Last word "สักครั้ง" g 2020: pull has landed on the tower; hold with the fair, flags and crowd.
- Frame-diff in shot: median 9.63, p90 29.37. 12.4 s/frame wall.
- FG fix (director gotcha 7): the preset iron post (fg_iron_sh, 1 m ahead of the PRESET camera) was moved +4 D with the closer start so the lens never passes through it; re-rendered.
- qa_auto (old note, superseded if QA_AUTO.md says PASS): one FAIL "suspected blur" on g 1964-1972 (9 frames): relative Laplacian heuristic on the flat orange facade slabs at the start; frames checked at full size and are sharp (noisy slab texture, no motion blur, no DOF). Moving closer or shortening the pull did not change it. Flagged for the director.
- Contact/phone sheet checked; heads n/a after g ~1990.

## §7 gate (2026-11-20)
- `qa_stats.py take.mkv`: saturation 0.609, brightness 94.3, in-shot motion median 10.70 p90 31.46 (pass).
- Window bars: at g 1968 the X braces sit left and right of the table, nothing crosses his face (head 68 px, y ~600). Feet are hidden by the table; he sits on the restaurant chair behind a cloth table with contact decal.
- Camera: the pull ends on the whole tower (wide), no face taller than 35 %.

## Bookend of s24 BIGZOOM (director plan change)
- The start is now a MEDIUM of Maupassant in the clear centre pane (camera 9.5 D closer than the first version: head 128 px at g 1968, eyes shut, smug, table + cloth below; X braces left/right, only the preset iron post at the left edge 1 D from the lens). The crash pull-out then runs to the whole tower exactly as before.
- Re-measured: qa_stats sat 0.607, luma 94.8, motion median 10.97 p90 31.86; frame-diff median 9.83 p90 30.05. qa_auto still lists "suspected blur" on g 1964-1973 (10 frames, flat orange facade + cloth slab by the relative-Laplacian heuristic; frames sharp at full size).
