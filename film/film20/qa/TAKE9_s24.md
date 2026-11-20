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
