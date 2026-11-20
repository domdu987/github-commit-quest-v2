# s26 QA (shot 26, RESTO resto_view, g 1912..1967, handles 1908-1911 / 1968-1971, hard cuts both sides)
- Over-the-shoulder: cast20 maupassant_seated_toast arms + `back=1` card at the window table, he raises the wine glass; Paris, Seine, Trocadero, no tower. Chair at 1-2 D in the foreground (set chair + table).
- Camera: preset resto_view moved back 3 D / right 0.9 D, aim 1.2 D right of his head (he sits in the left third), push 17 %/s + slide + crane + orbit, snap x1.45 on "หอไอเฟล" (g 1939), moving on every frame.
- Heads: back-of-head 124-227 px, centre y 606-637, chin < 730: all above y 880. No mouth (back card, no lip-sync).
- Frame-diff in shot (90x160 grey): median 4.43, p90 12.11. 25.96 s/frame wall (8 spp, 720x1280, 2 procs x 2 threads).
- qa_auto PASS. Checked: ceiling sliver top-left on the first frames (tilt keeps it small), no tower in frame.
- Known: the stage "head hole" retry warning is the dark hair of the back card, frames verified.

## §7 gate (2026-11-20)
- `qa_stats.py take.mkv`: saturation 0.535, brightness 99.2, in-shot motion median 6.11 p90 12.46 (pass). Raw render was sat 0.36 / luma 129 (white cloth + cream room), so deliver.py grades the frames (gain 0.9, gamma 1.2, saturation x1.5); raw/ is the ungraded render.
- Frame-diff (our script, 90x160): median 5.17, p90 12.38. Camera push 22 %/s + slide + crane + orbit and a x1.95 snap on "หอไอเฟล" (g 1939).
- Head width 125 -> 321 px (<= 25 % of frame height, under the 35 % limit); chin <= 813. WARNING: from the snap on (g ~1946-1971) his hair/shoulder touches the left frame edge (head x ~197 of 720, 5 px margin at g 1960): slightly crowded, not half-cut. The restaurant table + cloth fills the lower 35-40 % of the frame (it sits between the camera and him; a camera behind him is impossible, the window is 0.5 m away); tried lower / further-back cameras, they showed ceiling or hid the Seine.

## §I gate (2026-11-20)
- qa_stats2: `sat 0.535 vivid% 53.4 luma 99.2 contrast 50.9 detail 8.06 warm 34.5% cool 46.9% | motion med 6.11 p90 12.46 still% 0.0` (pass: sat >= 0.50, vivid >= 45; warm and cool both in frame: low sun on the parquet and cloth, cool window fill and shadows).
- Acting: he is raising his glass to the view with sway/breath on every frame (the glass lifts on g 1912-1928 and jerks up on the word at g 1939).
