# s14 QA (render team 5)
Rendered 720x1280, 14 samples + denoise, handles per meta.json. Stats (qa_stats2 on take.mkv): see below; motion median >=12, p90 >=16 (targets 4 / 12).
sat 0.499 vivid% 45.5 luma  89.0 contrast 30.6 detail 9.01 warm 32.7% cool 51.5% | motion med 12.05 p90 18.01 still%  0.0
Known deviations: s11 is a side over-the-shoulder (billboard cards cannot be seen from behind); her head exceeds 35 % for ~10 frames while the final push leaves the frame; top-third luma ~118 (limit 115). s13 stops the crane at z 11 (ceiling 14), crowd faces near 35 % in the first second. s14 end is dark navy by design (glowing lines, luma ~60) for the match dissolve; take luma 89. Shade-hue not separately measured. Plain-paper close at s11 end lasts <=0.4 s.
