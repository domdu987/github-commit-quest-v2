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

## qa_auto blur flag: frame list and cause (answer to the director's rule)
- Flagged: g 1964-1973 (10 frames: 4 handle + 6 in shot). Laplacian-variance ratio to the take median: 0.28-0.34 on g 1964-1971, 0.43-0.49 on g 1972-73, 0.55-0.73 on g 1974-79, ~1.0 from g ~1995. It is a CONTENT effect, not motion blur: Cycles renders no motion blur here and the start frames are the sharpest-rendered but flattest picture (cloth, cream wall, orange slab) against a median set by the detailed lattice and fair. A longer ease-in would keep the flat picture on screen longer, so I did not re-ease it. Flagging for the director's call (waive, or ask for fine dressing on the start pane).
- qa_stats line: `saturation 0.607, brightness 94.8, in-shot motion median 10.97 p90 31.86` (s27); s26: `saturation 0.535, brightness 99.2, motion median 6.11 p90 12.46`.

## §I gate (2026-11-20)
- qa_stats2: `sat 0.606 vivid% 70.3 luma 94.9 contrast 31.4 detail 7.26 warm 56.4% cool 34.0% | motion med 10.97 p90 31.86 still% 11.1` (sat >= 0.50, vivid >= 45: pass; the still% is the planned near-still final 12 frames).
- Acting: re-rendered with Maupassant EATING with his eyes shut (smug_shut): the fork hand cycles plate -> mouth at ~1.3 Hz in every frame; light: low sun through the window flaring the facade and cream room, warm lamp + cool shade in frame. Blur-flag note above is unchanged (g 1964-1973, flat start pane).

## Director fix applied: hold on Maupassant, then ease into the crash (final version)
- Camera: g 1968-1975 gentle drift on Maupassant (distance -2 %, he eats with eyes shut, fork cycle), crash pull g 1976-2033 with a ~5-frame ease-in (per-frame zoom peaks ~g 1978-1980), then 12 near-still frames (frame-diff 0.2-0.9) on the whole tower. Frame-diff in shot: median 9.79, p90 26.53.
- qa_stats2 (final): `sat 0.610 vivid% 70.3 luma 95.2 contrast 32.4 detail 6.76 warm 57.6% cool 33.6% | motion med 10.92 p90 27.52 still% 14.8`.
- qa_auto "blur" STILL FAILS and is worse (16 flagged: g 1964-1979; 12 of them on screen, g 1968-1979). Measured Laplacian ratio to the take median: 0.29-0.38 on g 1964-1979, 0.48-0.59 on g 1980-81, 0.64+ from g 1982. The flagged frames are exactly the frames with the flat pane (cloth, cream wall, orange facade); the hold keeps that picture on screen longer, so the count rose (10 -> 16) although there is no motion streak at all (Cycles, no motion blur). The heuristic cannot be satisfied by easing; it needs more fine detail in the start pane (set dressing) or a waiver. Needs a director decision; I did not add set dressing.

## Director list F1/F2/F4 applied (re-render on the new set, 2026-11-20)
- F1: all `fg_*` objects (fg_iron_sh, the post) are hidden. F2: the take STARTS on the set builder's `tower_window_in` (55 mm, loc (0,-40.2,59.7) m): Maupassant medium in the clear centre pane at the RESTO table (head 194 px at g 1968, y 716, chin 813), eyes shut smug, eating (fork cycle ~1.3 Hz). Hold g 1968-1975 (drift 0.6 % of the pull range, head 194 -> ~188 px), crash pull g 1976-2033 with a ~5-frame ease-in, lens 55 -> 22 mm blended over the first third of the pull, 12 near-still frames on the whole tower (frame-diff 0.2-0.9). F4: the lit window + red awning + RESTAURANT sign stay findable until g ~2000; in the final whole-tower frames the window is a small warm dot (the tower is the picture). F3 flags are the set's tricolours (visible in the last frames).
- qa_stats2: `sat 0.627 vivid% 71.2 luma 88.5 contrast 35.6 detail 7.22 warm 58.3% cool 32.7% | motion med 9.60 p90 34.49 still% 14.8`; qa_stats saturation 0.627, luma 88.5 (in 85-110). Frame-diff median 8.84 p90 32.95.
- qa_auto blur: FAIL on 8 frames (g 1967 handle + g 1973-1979, hold end / pull start). The start pane no longer scores flat-slab like before but the interior (cloth, dark roof) still has Laplacian ratio ~0.40 of the take median through g 1979 (0.57 at g 1980, 1.0 from g 1983); that ratio is a content value (no motion blur is rendered). More than 3 frames: needs your call (waive, or set-dressing detail in the interior).
