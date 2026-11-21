# s11 QA (render team 5)
Rendered 720x1280, 14 samples + denoise, handles per meta.json. Stats (qa_stats2 on take.mkv (parts: take.mkv.part00.. cat to rejoin)): see below; motion median >=12, p90 >=16 (targets 4 / 12).

Known deviations: s11 is a side over-the-shoulder (billboard cards cannot be seen from behind); her head exceeds 35 % for ~10 frames while the final push leaves the frame; top-third luma ~118 (limit 115). s13 stops the crane at z 11 (ceiling 14), crowd faces near 35 % in the first second. s14 end is dark navy by design (glowing lines, luma ~60) for the match dissolve; take luma 89. Shade-hue not separately measured. Plain-paper close at s11 end lasts <=0.4 s.

## Round 2 (sections K and L)
Ground check (ground_check22, animate applied per frame): RESULT: PASS (0 failures)
Camera: no shake; eased keys only (s11 carriage rock now scrolls the window streaks only, cards sway on their feet).
qa_jitter.py output:
```
overall median jitter px 0.3
```
