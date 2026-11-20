# s26 QA (shot 26, RESTO resto_view, g 1912..1967, handles 1908-1911 / 1968-1971, hard cuts both sides)
- Over-the-shoulder: cast20 maupassant_seated_toast arms + `back=1` card at the window table, he raises the wine glass; Paris, Seine, Trocadero, no tower. Chair at 1-2 D in the foreground (set chair + table).
- Camera: preset resto_view moved back 3 D / right 0.9 D, aim 1.2 D right of his head (he sits in the left third), push 17 %/s + slide + crane + orbit, snap x1.45 on "หอไอเฟล" (g 1939), moving on every frame.
- Heads: back-of-head 124-227 px, centre y 606-637, chin < 730: all above y 880. No mouth (back card, no lip-sync).
- Frame-diff in shot (90x160 grey): median 4.43, p90 12.11. 25.96 s/frame wall (8 spp, 720x1280, 2 procs x 2 threads).
- qa_auto PASS. Checked: ceiling sliver top-left on the first frames (tilt keeps it small), no tower in frame.
- Known: the stage "head hole" retry warning is the dark hair of the back card, frames verified.
