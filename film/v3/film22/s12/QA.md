# s12 QA (render team 5)
Rendered 720x1280, 14 samples + denoise, handles per meta.json. Stats (qa_stats2 on take.mkv): see below; motion median >=12, p90 >=16 (targets 4 / 12).
sat 0.598 vivid% 82.5 luma 101.8 contrast 39.6 detail 7.41 warm 67.4% cool 26.2% | motion med 12.77 p90 16.87 still%  0.0
Known deviations: s11 is a side over-the-shoulder (billboard cards cannot be seen from behind); her head exceeds 35 % for ~10 frames while the final push leaves the frame; top-third luma ~118 (limit 115). s13 stops the crane at z 11 (ceiling 14), crowd faces near 35 % in the first second. s14 end is dark navy by design (glowing lines, luma ~60) for the match dissolve; take luma 89. Shade-hue not separately measured. Plain-paper close at s11 end lasts <=0.4 s.
