# QA, segment A1 (BIGZOOM 1, first half) - g 0..80 (+3 handles g81..83), film start

- **Camera:** one travelling move from `K.cam_path`, keys: a pre-roll key at g-24 (so the ease-in happens before g0 and the film opens already moving), `P_A` at g80, `hill_over` at g159 (so g81-83 continue the move for the D6 join). Start = the valley_wide pose, EXTREME WIDE and high (445, 244, 361 -> 64.8, 44.7, 0.2). End at g80 = **P_A exactly** (290, 205, 170 -> 120, 110, 10, 22 mm), written in meta.json `cam_out`.
- **World:** `K.build_world(['valley_wide','hill_over'], fg=False)`: loop, bridge with the English column (`place_troops bridge`, walking +y 1.3 m/s), camp, Abbey Craig with the Scots line and saltire banners, farms. No cast cards (the Scots are the set's tiny slope line, under 5 % of the frame).
- **Samples:** 32 (OIDN), 720x1280, 84 frames, ~90-120 s per frame.
- **Grade:** VIVID eased by `cam_path`; luma was 122 raw, so one constant extra gamma 1.459 per segment (`post_luma.py`, same as a higher VIVID gamma; raw frames kept) -> luma 100.0.
- **Numbers (`take.mkv`):** `qa_stats2`: saturation 0.773, vivid % 84.9, luma 100.0, motion median 6.31, p90 8.15, still % 0. `rhythm.py`: in-shot median 8.25, **p90 9.70 (below the 12 target)**: the swoop is one smooth monotone move, so the frame-diff is even rather than spiky; there is no near-still frame. `qa_auto`: PASS (QA_AUTO.md, phone_sheet.jpg).
- **Not in this segment:** the Scots medium on the shelf (that is A2, team 5, from P_A).
- **Known:** the colours are very saturated by design (director's VIVID grade). The knights on the bridge are 3D riders (static legs), tiny at this distance.
