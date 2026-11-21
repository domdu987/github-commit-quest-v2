# QA self-check T5a (film 17 v2, T5, g1039-1210, 172 frames), after fix rounds 1 and 2

Each frame was opened at full size (720x1280). The same frames were looked at again in `phone6.jpg` (360x640 tiles). Only what I saw is stated.

| g | full size | phone size |
|---|---|---|
| 1046 | The slab is gone. High angle over the gallery rail. Night archive, carpet, desks, candle. Bertillon stands by his stool, looking slightly down. The inspector and two gendarmes are small at the far end. No black rectangle. | Bertillon reads as a small figure. The far group is a few dots. |
| 1117 | Over-the-shoulder view. Bertillon's back is brown hair with a shine, ears, white collar, grey coat. The inspector and the green gendarme are small at the end of the aisle. No veil. | Same. The silhouette reads. The inspector is small. |
| 1135 | The inspector has his eyes squeezed shut, mouth open, hand cupped, at about 36 %H. The green gendarme stands behind and partly covered by his head, so half of that face is hidden. A desk pile is in front of his legs. No milky veil. | The inspector's mouth and hand read. The gendarme is only half visible. |
| 1155 | The green gendarme is fully in frame with a closed smirk. The inspector is open-mouthed. A trolley and a book pile sit in the lower frame. | Both read. The foreground takes up the lower third. |
| 1170 | The green gendarme is fully in frame with an open small mouth (the heh beat). The inspector has an open mouth and a cupped hand. A trolley box covers his knees. | Both read. The open mouth is a small dark shape. |
| 1210 | Day look, warm orange wall and floor. The inspector is small (about 25 %H), arms crossed, closed mouth. No veil or beam visible. | Reads. The figure is small and the orange floor takes up the lower half. |

## Fixes from the director (round 2)
1. Black slab g1042-1048: gone. All frames were re-rendered with `clear_cast`.
2. Beam off: `beam_off()` forces the strength to 0. Frames g1135 and g1170 show no veil.
3. Green gendarme (gend_b): constant offset (0.6 m, 0.3 m) for g<1196, eased to zero over g1196-1210. He is inside the frame in the 1155 and 1170 frames I viewed. I did not view every frame in g1153-1171.
4. Snicker: planted chuckle, with squash/stretch scale-z 0.94-1.0 at 3 Hz about the feet, a 0.04 head bob and an open small "heh" mouth on the up beat, g1111-1171. I did not look at it frame by frame, so I cannot say whether the motion reads at phone size.

## Checks
- `check_take('T5')` has no hits and `check_face('T5')` is ok, with the camera override in `t5a_override.py`.
- `qa_auto.py`: PASS. The cuts g1045 and g1377 show "no visible change", expected since g1039-1044 are same-scene handles. No soft frames. Magenta share 0.0 %.
- `rhythm.py`: in-shot median 12.65, p90 20.92.
- RGB-mean luma over all 172 frames: mean 96.0, min 78.8, max 107.5 (target 90-108). The series is smooth, with no spikes. The min is around g1117-1120.

## Known issues
- The inspector's pose switches without a blend at g1120 and g1196.
- Dupont and the escort gendarmes are not in frame in g1196-1210.
- The clerk desk and trolley partly cover the inspector's legs in g1135-1170.
- Lights were raised in code: ARCHIVE_NIGHT fill_w 230, lamp_k 1.0, gasolier_k 0.7 (`t5a_override.py`).
- No OIDN shimmer check was run, and I did not switch to 24 samples.
