# TAKE9 s24 (BIGZOOM 2 re-render, take g1724-1858) -- QA-tech: PASS with notes

Independent measurement from the frames (hair top to tabletop, full 720x1280, +-1.5 % reading error; team2's numbers NOT used).

| g | figure % H | | g | figure % H |
|---|---|---|---|---|
| 1724 | 3.4 | | 1810 | 21.6 |
| 1736 | 4.4 | | 1825 | 30.3 |
| 1750 | 5.3 | | 1830 | 32.0 |
| 1760 | 6.4 | | 1840 | 32.3 |
| 1775 | 9.1 | | 1846 | ~34.5 |
| 1790 | 13.3 | | 1852 (plan end) | ~35 |
| | | | 1858 | ~35.4 |

- Start <5 %: yes (3.4 % at g1724, 4.4 % at g1736, 5 % crossed ~g1748). Findable: yes, white face + moustache + lit table through the clear pane from g1724 (small, partly behind a lattice post). It is NOT a whole-tower extreme wide: the first frame is already the facade/RESTAURANT sign with the window ~1/4 of the frame; he is a legible dot.
- End >=35 %: BORDERLINE. Measured 30 % at g1825, 32 % at g1830-1840, ~35 % only in the last frames (g1852-1858). team2's 38.7 % (g1840), 42 % (g1858) and "35 % at g1829" are overstated by ~6-7 points. The figure grows only ~+0.5 %/s after g1830, so the "landing" is effectively a hold at 32-35 %. Duration 5 % -> 35 %: g1748 -> ~g1852 = 3.5 s (inside 3-6 s); <5 % -> ~35 % over the whole take 4.2 s. If the gate wants a hard >=35 % at the plan cut (g1852), it is met only at the +-1 % measurement limit.
- Continuity: one continuous move, no cut. Per-frame diff (90x160 grey): 8.8 at g1725, rising smoothly to a peak 22.1 at g1767 (facade/sign crossing, was 44 in the old take), falling to 8 by g1821, 6 at g1833, then 2-3 for the hold. Largest adjacent-frame change 4.5 (no spike, no whoosh). One speed step: ~6 -> 2.5 between g1833 and g1837 (the zoom stops abruptly; mild, reads as settle).
- First bite: the forkful is at his mouth at g1830 (also g1825 and, notably, g1750 -- he already has a forkful at the mouth at g1750 and chews through the whole approach, so "first bite" is not a clean story beat at g1830). Fork up/empty at g1858, bites repeat. Minor.
- Heads at the landing: x ~0.45-0.47 W, y ~0.45-0.50 H (g1830-1858 head centre ~y 0.40-0.45 incl. hair, face centre ~0.47). OK.

## Take checks (own run on t.mkv rebuilt from the 135 frames)
- qa_auto.py: PASS (magenta 0 %, no black/blank/frozen frames).
- qa_stats: sat 0.734 (>=0.50 ok), luma 85.6 (85-110, at the floor, ok), motion median 9.5 p90 17.3.
- qa_stats2: vivid 74.1 % (>=45 ok), warm 80.7 / cool 5.7.
- Ground (green): max 10.5 % at the start, 0.1-0.5 % from g1772 (<=25 ok; orange gallery slab at the bottom of g1724-1770 is the tower, not ground).
- Faces: head is ~20 % H at g1858 (<=35 ok). Nothing floating: he sits on the chair behind the table; diners are seated. Black seams: none in the landing frames (g1802-1858 black pixels <0.5 %). Note: two small pure-black rectangles on top of the lattice posts g1724-1760 (set geometry bits, ~0.5 % of frame, read as post caps).
- Joins: s23->s24 (g1732-1744): crowd close-up of two men dissolves into the tower facade with RESTAURANT sign; different subject and colour (blue sky -> orange), a plain dissolve that reads cleanly, no black frame, no pop. s24->s25 (g1844-1858): Maupassant seated at the table (head ~0.45 W) dissolves into s25's Maupassant on the tower (head ~0.42-0.45 W, ~0.5 H), the head positions match; the room goes from warm interior to blue sky, reads as a match-dissolve. Clean.

## Verdict: PASS with notes
Fixed vs the old take: smooth steady zoom, no whoosh, he is findable from frame 1, 3.5-4 s long, dining room behind him, no seam. Notes for the gate: (1) final figure is ~35 % (not 42 %): meets the floor only at the cut/last frame; to be safe a ~5-10 % tighter end pose (or letting the zoom run to g1852 instead of stopping at g1833) would give 38-40 %; (2) start is a facade close-up, not a whole-tower extreme wide; (3) the bite happens from g1750 on. Not committed.

---
# Round 9 (re-render: ending ~1.24x closer from g1805, post caps + black tower members removed) -- QA-tech: FAIL (duration 2.7 s < 3 s; black block remains)

Same measure as before (visible figure, hair top to far edge of the tabletop, read on the full 720x1280 frames against a 1 % grid, +-1.5 %). g1724-1804 use the identical camera, so the lower half of the old table still holds.

| g | fig % H | | g | fig % H |
|---|---|---|---|---|
| 1736 | 4.5 | | 1825 | ~35.5 |
| 1750 | 5.5 | | 1828 | ~36 |
| 1775 | ~9.5 | | 1830 | ~37 |
| 1790 | ~13.5 | | 1840 | ~39.5 |
| 1805 | ~19 | | 1850 | ~41 |
| 1815 | ~28.5 | | 1858 | ~43 |
(g1820 32.6, g1823 34.2, g1826 35.8, g1829 37.2 on the fine grid)

- Last frame <5 %: ~g1743 (4.5 % at g1736, 5.5 % at g1750). First frame >=35 %: ~g1825 (34.2 at 1823, 35.8 at 1826). Duration ~g1743 -> ~g1825 = 82 frames = **2.7 s: OUTSIDE 3-6 s** (error band about 2.4-3.1 s; team2's 3.1 s uses its own sprite-based 5.0 % at g1735, which reads ~0.7 point under my measure at the start and ~2 points under at the end). Not a pass by the same measure as last round.
- Holds >=35 % to the end: YES, grows 36 -> 43 % (g1828 -> g1858), no drop; the landing now clears the floor by 1-8 points (was borderline).
- Smoothness: per-frame grey diff (90x160) is continuous through g1795-1834: 10.8 (1795) -> 11.2 (1804) -> 10.9 (1805) -> hump 17.1 (g1814-1815, the old ramp 1804-1822 now a gentle bump) -> 8.3 (1822) -> 6.6 (1830). No step at the old ramp and no jump at g1804/1805 (11.2 -> 10.9). Max adjacent change 29 at g1764 is the lattice/sign crossing (unchanged, was 22 before; no spike in the new part). ONE mild step remains: diff 6.6 -> 1.9 between g1834 and g1835 (zoom rate falls in one frame, then a slow 2-3 drift); reads as a soft settle, but "the zoom continues without a speed step" is not literally true.
- Take checks (t.mkv rebuilt from the 135 frames): qa_auto PASS (magenta 0 %, no black/frozen frames); qa_stats sat 0.716 (ok), luma 87.3 (85-110, near the floor, ok), motion median 11.0 p90 20.6; qa_stats2 vivid 71.3 % (ok), warm 81.5 / cool 5.5.
- Defects: (1) black squares on the post tops beside the RESTAURANT sign g1724-1757: REMOVED (pure-black share 0.1-0.2 % at g1724-1740, posts clean). (2) black unlit tower members right of the window g1756-1784: NOT removed. A solid pure-black block (luma<14) still fills the right side of the window behind the lattice: 6.3k px at g1757, 8.6k g1765, 13.4k g1775, 13.8k g1784 (1.5 % of frame, x 420-719, y 370-775 at g1784); it drops to 0.12 % at g1800. It reads as a black void with lamps in front of it (possibly the dark room back wall/unlit gap rather than members, but it is the same visible defect). New artifacts: none (no seam, no floating, ground ok; landing frames clean).
- Heads at landing: x ~0.44-0.46 W, hair-to-chin centre y ~0.45-0.50 H, head ~19-21 % H (g1830-1858). OK.
- s24 -> s25 (g1847-1858 into s25 g1847+): s24 end = interior, head centre ~(0.45 W, 0.43 H); s25 = blue sky behind him, head centre ~(0.45 W, 0.54 H), head ~0.7x the size. Plain dissolve, x matches, y offset ~0.1 H and a scale step; no black frame, reads as a match-dissolve with a small drop. Acceptable.

## Round 9 verdict: FAIL
Landing size is fixed (35 % reached at g1825, 43 % at the end, holds), join/smoothness fine, post caps gone. Blockers: (a) under-5 % -> >=35 % takes ~2.7 s (<3 s): either start the zoom a bit later/slower (e.g. hold <5 % to g1750 and keep the end) or accept 35 % at ~g1833 by relaxing the ramp; (b) the black block right of the window at g1756-1784 is still there. Not committed.
