# QA-tech sF (team1 9cc4f6f)

**Verdict: FAIL** (3 blocking, 4 non-blocking). Take checked: 98 frames, 720x1280, g1044-1141, every 5th frame plus the 8 frames around the edge cuts and the mouth start.

## Beat table
| g | narration | what is on screen | verdict |
|---|---|---|---|
| 1044-1062 | 34.71-35.3 | Side track, 4 English laughing and pointing at the river. Yellow-jerkin soldier large at centre, crimson soldier and a small one behind. Laugh bounce reads. A knight (chevron surcoat) is sliced by the RIGHT frame edge. | edge cut (B1) |
| 1062-1078 | 35.3-36.0 | Yellow soldier slides out left, Surrey (checker, tired) enters right. A tiny laugher with a pointing arm at the bank. Only 1-2 laughers visible. | thin, readable (N2) |
| 1078-1092 | 36.0-36.4 | Surrey centre (head about 24 % of frame height), mouth closed, a barrel enters from the lower left. Surrey is cut by the right edge at 1078-1085. Cressingham is half cut by the LEFT edge at 1083-1091 behind the barrel. | edge cut (B1), barrel (B2) |
| 1093-1112 | 36.42-37.0 | Cressingham in full, hands at belt. His mouth opens at 1093 (in the 36.32-37.89 window, correct). Barrel covers his lower right and the whole lower third of the frame until about 1112. | barrel (B2) |
| 1112-1141 | 37.0-37.94 | CU2 push (ease-out), crimson and gold figure, thumbs at belt, speaking, smug. Final head with hat about 30 %, face about 23 % of frame height, under 35 %. Clean frame. | PASS |

## Checks
- Mouths: Cressingham speaks only at g1093-1140 (window 1093-1140, OK). Mouth closed at g1091, open at g1093. Surrey and the others closed. The camp laughs until about g1093 and then sways. OK.
- Heads: all heads are above y 880 (highest about y 340-520, Cressingham at the end about y 600-800). OK.
- Floating: feet on the ground, contact shadows on all. Nothing floats. OK.
- Face over 35 %: none.
- Colour story: English crimson and gold (Cressingham crimson/gold, Surrey red/yellow check, crimson soldiers). No blue in the English clothing, the blue is only sky and the teal river (set). No Scots saltire in shot (the far bank is empty hills), so the "both colours" aim is only half met (N3). The bank sand is very yellow (set palette, normalized at the conform).
- Banners and smoke near the lens: none (hidden by the team). The barrel is the only foreground obstacle.
- Camera clearance: the barrel passes within about 1 m of the lens, with a dark, jagged shadow fringe at its edges (g1083-1112).
- Bloodless: yes.
- Hard cut out to G at g1141: the last frame is a clean CU, so the cut works.

## Issues
**B1 (blocking), cut by the frame edge.** The English knight at the right edge g1044-1062 (and again 1071-1078), Surrey at g1078-1085 (right edge), Cressingham at g1083-1091 (left edge, half of his body). A character is cut in half by the frame (§G).
Fix: re-stage and re-frame. Move the knight 1 m left (or out of shot) in the first 20 frames. Time the track so Surrey and Cressingham are fully inside the frame whenever they are in shot. Either hold Surrey in frame while he passes, or start Cressingham further in and have him enter earlier.

**B2 (blocking), barrel in the lens path, g1083-1112.** A red barrel fills the lower left and centre (about 25-30 % of the frame) while Cressingham speaks his first words. It hides his body and has a black fringe on its edges. This reads as a rendering fault, not as a set layer.
Fix: hide the barrel (`K.hide_near_banners`-style) or move it at least 2.5 m off the camera path, so that no prop is closer than the characters.

**B3 (blocking, same fix as B1 and B2), the beat is under-staged.** After g1062 only one tiny laugher is visible and the camera shows Surrey, who is not laughing. The "waiting English laugh and point" beat then only exists in the first 18 frames, and Cressingham is hidden until g1093.
Fix: keep 3-4 laughing and pointing English in frame to g1093, bouncing out of phase, and Cressingham standing among them from g1078.

**N1 (non-blocking), the opening laughers are small.** Heads of about 5 % of the frame height at g1044-1060. Readable, but a closer start (6 m instead of 8 m) is better for the phone.

**N2 (non-blocking), Surrey** is nearly still for about 15 frames (g1074-1089). Add a shift of weight, a sigh or a scratch.

**N3 (non-blocking), no Scots blue in view.** Add a distant saltire banner on the far hill, or leave it.

**N4 (non-blocking), the sand is very yellow.** Set palette. Normalised at the conform; if the director wants less, the sand tint belongs in the set.
