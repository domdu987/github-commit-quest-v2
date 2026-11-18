# QA s08 (film 10, shot 8, g 538-618, frames g 532-624 with 6 handle frames each side)
- Set: harbour DAY, custom medium camera (21 mm) on the quay, slow push/drift; set_stripes held at 0.505 (= s09 stage at its first frame g 613; re-rendered after QA found a wall-state jump at the s08 -> s09 cut). s05 still holds 0.6. Differs from plan: not the preset harbour_wide (heads would be 9-12 px); a closer quay camera shows the sailors.
- Cast (cast10): sailor_a/b/c on the quay + 2 on the berth deck pointing/laughing at the painter (right of frame), painter10 calm, mirrored toward them. Laughing drawings are held (point-laugh <-> belly-laugh swaps every ~14 frames plus a small squash bounce). No mouth moves: no lip-sync in this shot. bgcard_7 hidden (stood at the sailors' spot).
- Heads: all above y 880 (lowest head edge 784 px); main heads 0.55-0.62 H, 55-95 px wide.
- qa_auto: PASS (no frozen/black/magenta frames, no pops; no planned cuts inside the take). See QA_AUTO.md, phone_sheet.jpg.
- Cost: 12.4 s wall / 24.5 s CPU per frame (2 processes in parallel). 93 frames, take.mkv 24 MB.
- Not run: hue_report (its reference frames are missing in this checkout). Frame-by-frame check done at 6 fps on the contact sheet.
- Notes: the sailors are grouped left and the quay in front is empty cobbles; the painter sits near the right edge.
