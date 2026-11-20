# QA self-check T5a (film 17 v2, T5, g1039-1210, 172 frames)

Each frame was opened at full size (720x1280). The same frames were then looked at again in `phone6.jpg` (360x640 tiles). Only what I saw is stated.

| g | full size | phone size |
|---|---|---|
| 1039 | High angle over the gallery rail. Night archive, long carpet, desks, ledgers and a lit candle. Bertillon stands by his stool with glasses and a goatee, head slightly down. The inspector and two gendarmes are tiny at the far end. | Bertillon reads as a small figure at the desk. The far group is only dots. |
| 1111 | Over-the-shoulder view. Bertillon's back is brown hair with a shine, ears, white collar and a navy coat, with no black slab. The aisle leads to three small figures. Skylight shafts and the PETIT sign are visible. | Same, with a hair and coat silhouette. The inspector is about 10 %H, small. |
| 1150 | The inspector has his eyes squeezed shut, his mouth open under the moustache and one hand cupped by his head. He is at about 42 %H. The green gendarme at the left has a closed mouth. A trolley box and a desk pile cover his lower legs, but his face is clear. | The mouth and cupped hand read. The foreground clutter takes up the lower third. |
| 1169 | Inspector medium, mouth open, hand cupped, feet on the floor. A trolley box in the lower middle covers his knees. The green gendarme is cut at the left edge. A pale blue haze crosses the lower left. I think it is a skylight shaft. qa_auto flagged g1169-1170 as soft. | Reads clearly. The haze is faint. |
| 1196 | The inspector with arms crossed, a closed mouth and a smirk, feet on the floor, in a warmer light. No gendarme or Dupont in frame. | Same, the pose reads. |
| 1210 | Day look: warm orange wall, floor and rug. The inspector is smaller (about 25 %H), arms crossed, beside a ladder and a trolley, feet on the floor. | Reads, but the figure is small. The orange floor takes up the lower half. |

## Checks
- `check_take('T5')` has no hits and `check_face('T5')` is ok, with the director-approved camera override in `t5a_override.py`.
- `qa_auto.py` on `take.mkv`: PASS. The cuts g1045 and g1377 are reported as "no visible change", expected because g1039-1044 are same-scene handles. Soft frames: g1169, g1170. Magenta share is 0.0 %.
- `rhythm.py`: in-shot median 11.69, p90 20.72.
- RGB-mean luma over all 172 frames: mean 106.8, min 87.6, max 129.7 (target 90-108). It is slightly high. The jumps in the series (for example 89 to 124 at g1134-1135, 129 at g1168) coincide with a skylight shaft crossing the frame. I did not trace each jump to its cause.

## Known issues
- The inspector's pose switches without blending at g1120 (arms crossed to shouting) and at g1196 (shouting to arms crossed).
- The 3 Hz snicker bounce is only 0.06 m. I did not look at it frame by frame, so I cannot say whether it reads at phone size.
- Dupont and the escort gendarmes are not in frame in g1196-1210.
- Lights were raised in code: ARCHIVE_NIGHT fill_w 230, lamp_k 1.0, gasolier_k 0.7 (`t5a_override.py`). The beam strength ends at the ARCHIVE_DAY value at g1210. I did not render a frame with the beam hidden.
- No OIDN shimmer check was run, and I did not switch to 24 samples.
