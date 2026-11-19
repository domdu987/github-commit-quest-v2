# Film 16 TAKE gate round 3 (re-check after fixes): QA-tech and QA-art combined
Takes: s10, s11, s12 from render16/team3 @b31fe83; s15 from render16/team4 @7d3f491; s30 from render16/team8 @10247ed (s30 is one take.mkv, not split; s11 was split and I joined it with cat).
Method: I decoded every take to full-res PNG one at a time. I checked 6 fps sheets at 360x640 with the y 880 line drawn, plus every cut ±3 frames (s15 at 10 fps). I made full-size crops of faces, hands, props, the key and the doorway. I ran film/qa_auto.py on each take and recomputed the frame-diff myself (90x160 grey, in-shot pairs). Lip-sync window: 18.32-23.20 s + 0.10 s clock = g 553-699 (±0.15 s).
Earlier reports: qa/TAKE_team3.md (s10-s12), qa/TAKE_ART_r2.md (s15, s30), qa/TAKE_r2_A.md (s30).
qa_auto reported "planned cuts with no visible change" on every take. This is expected: the handles are continuous 3D, and the cut only happens at conform.

| take | qa_auto | diff median / p90 (min, max) | heads y<880 | verdict |
|---|---|---|---|---|
| s10 | PASS | 9.04 / 15.97 (3.03, 25.6) | yes (bottom <= ~755) | PASS (notes) |
| s11 | PASS | 5.28 / 14.62 (1.22, 26.3) | yes (<= 797) | PASS (notes) |
| s12 | PASS | 5.78 / 18.36 (3.94, 23.3) | yes (<= 736) | PASS (notes) |
| s15 | PASS | 5.09 / 16.71 (3.98, 20.4) | yes | PASS (notes) |
| s30 | PASS | 5.50 / 13.81 (2.26, 27.1) | yes (<= 849) | FIX (1 blocking, small) |
All takes meet median >= 4 and p90 >= 12. I found no low-diff run (< 2 for >= 6 f), no black or magenta frames, no DOF, no text in the picture, and no pop outside the planned snaps and blink swaps.

## s10: mocker's boast close (PASS, notes)
Earlier issues:
- B1 face below 250 px, and the cut from s09 went to a smaller face: **FIXED**. The face is about 300 px from g597 and grows to 430+ px after the punch-in. The s09 g596 to s10 g597 cut goes clearly closer on the same axis.
- N6 focus lines are thin strokes: **OPEN (NOTE)**. At full size you see fine white hairlines in the top-left and top-right corners only, g672-689. On the 360x640 view they are almost gone. The punch-in itself is now only x1.3 and reads as a mild push.

Phone read: YES. The low-angle boast reads: finger up g597-661, then on the blink swap g662 the open hand thumps the chest with the chin up, the mouth talks, and there is blush. Lip-sync runs the whole shot inside the window. Mouth shapes alternate. Head centre y 409-533.
Notes:
1. Focus lines (the film's one special): draw them in the comp/deliver pass rather than with the puppet fx. Use 24-30 white wedge strokes, 6-14 px wide at the outer end and tapering toward the face, radial from the face centre, alpha 0.9, on for g672-686. That way they read at phone size.
2. The shot is now a tight close. The set shows only ceiling beams and a wood panel. That is fine for one punch line, but do not make the film tighter anywhere else.
3. Diff spikes g688-690 (17-24) are the chest-thump arm move, not a pop. g662 (25.6) is the planned blink swap.

## s11: the chamber laughs at Morse (PASS, notes)
Earlier issues:
- B2 snap pop through the instrument, Morse missing at g775: **FIXED**. The snap g764-780 is eased (max diff 26), Morse stays in frame in every frame, no props cross the lens, and it lands on Morse (about 265 px) by g778.
- B3 Morse missing from g698-775, empty lower frame, mocker unreadable: **FIXED**. Morse clutches the copper coil from the first frame (centre, 154-260 px, sad and worried). The mocker stands beside him laughing (head 130-183 px). The red congressman and the bowler-hat man laugh behind, and there are small figures on the tiers.

Team note: mocker head 130-183 px instead of 250. On the phone (about 65-90 px), the shut-eyed toothy laugh and the blush read clearly. The tears are small but visible as blue drops at the eye corners. I accept this as a medium. The laugh is the read, not the tears.
Phone read: YES, "they laugh at Morse, who hugs his coil". Mouths: the laugh pose only, no lip-sync. Morse's mouth is closed.
Notes:
1. The big red chair in the lower centre (set dressing, g698-775) is the most prominent object on the phone. It sits between the mocker and Morse, and on the snap (g770-775) it slides across the lower left as a large red block. If anything is re-rendered, hide it or move it 0.5 D out of the lane.
2. "Fingers point at Morse": the red congressman points to screen right, past Morse toward the table. Turn the arm about 20 deg so it aims at Morse's head. The plan's "whole chamber" reads as 3-4 laughers plus small tier figures (acceptable).
3. Continuity: the mocker stands beside Morse here, and in s12 he stands behind Morse at the table. This is fine.

## s12: money bag lands (PASS, notes)
Earlier issue N7 (bag overhangs the corner, no instrument): **FIXED in part**. The bag lands on the green table top g788, bounces (diff peak 23 at g790), coins spill onto the cloth and it sits with contact. Only a sliver of the instrument shows at the left edge in g785, and after that it is out of frame.
Phone read: YES, "a fat bag of money lands in front of Morse, who smiles, while the mocker sulks behind". No mouths move.
Notes: (1) The bag is huge (wider than Morse) and from g800 it covers his body and left arm. A 15 % smaller bag would let his relieved face and hands read. (2) The mocker's sour face and folded arms are small (77-97 px) but read.

## s15: the silent key (PASS, notes)
Earlier QA-art r2 fixes:
1. Make the press readable: **FIXED**. Morse stands at the key end facing it with his hand on the lever. The lever visibly dips between g972 and g978 at full size (small on the phone). The end close g999-1006 shows his outstretched hand on the knob, the lever and his worried face (about 300 px), so the silence now has a cause on screen. The third press inside the close (g996-1002) barely changes angle (diff about 4.5), so it is not really visible (note).
2. Eye-lines: **PARTLY FIXED (NOTE)**. The crew has arms down and leans in. Cornell's half-lidded eyes look down toward the register. The second worker is mostly hidden behind Cornell, and the third is cut at the left edge (g958-985). In the middle part Morse looks at the lens.
3. Register look: **FIXED in part**. It has copper coils with brass collars, a brass top, a pale tape roll, and a brass lantern with a strong warm pool on the crate (a good warm-against-dusk accent). The top bar is still a saturated flat blue.

Brightness dip on "เงียบกริบ": mean luma 92.7, falling to 80-84 over g988-996 (about x0.87, reads), together with the eased snap (diff peak 20). There is no pop.
Phone read: YES (setup, press, silent register, worried close).
Notes: (a) In the snap (g990-996) the blue register bar sweeps big across the lower left. If touched, swap it to dark wood or brass, which also fixes (c). (b) The lower 35-40 % is the plain dark crate side. (c) The blue bar.

## s30: ENDING (FIX, 1 small blocking item)
Earlier issues (TAKE_ART_r2 #1-3, TAKE_r2_A notes):
- Register at his elbow, one ribbon into the heap: **FIXED**. A walnut table sits at his right elbow, and a white dot-dash ribbon runs from it over the edge into the heap.
- Dot-dash heap, not slats: **FIXED**. The heap is curled ribbons with black dot-dash marks plus loose strips. On the phone it reads as grey curled paper loops (acceptable).
- Gold urn gone: **FIXED**.
- Night contrast and candle: **FIXED**. The walls are dark, the windows deep blue, and the warm candle (a brass chamberstick with a flame at his right hand, g2080-2095) lights his face. The ceiling is still the largest evenly lit grey-beige area in the final wide (note).
- Hat, Z, yawn, sash: OK. The yawn is the planned mouth (no lip-sync). Head bottoms are below 880.
- Morse in the doorway (bigger, away from the edge, last thing the eye finds): **OPEN, BLOCKING**. See below.

Team note "Morse head 82-104 px, not deeper in the door": the nominal size is up, but he peeks from BEHIND the right door jamb, so about half his head is hidden. In the final frames (g2070-2095) the visible face is about 32-35 px wide at 720. On the 360x640 view that is about 16-18 px, and his coat touches the left frame edge (x ~0-2). At full size the toothy grin reads (crops g2030/2060/2095). On the phone he reads as "someone peeking", not as a grin. The ending is a key shot (§C), and the brief requires "Morse grinning in the doorway" to read on a phone. It does not yet.
Fix (any one of these is enough; keep the hard cut on "เอง" g2096):
1. Do not move him deeper. Move him OUT from behind the jamb: 0.3-0.4 D toward the room, to the centre of the lit opening, so his whole head is clear of the jamb. Lean his upper body out, keep both eyes and the grin visible, and scale x1.2 if needed. The lit doorway behind him becomes his backlight.
2. Then slide or yaw the camera's final pose about 3-5 deg left (or 0.2 D truck) for g2065-2095, so the doorway sits at x 90-260 of 720 and Morse's face is >= 60 px visible at 720 (>= 30 px on the phone), clear of the left frame edge.
3. Optional: a 2-3 frame grin widen or eyebrow pop at about g2085, so he is the last motion the eye finds before the cut.
Notes: (a) The red rectangle on his vest centre is still there. (b) The near walnut instrument is dark and hard to tell apart from the bright set instrument behind. A small brass highlight or the candle pool on it would help. I could not confirm the 9-frame click on the stills. (c) The ceiling could go about 25 % darker in the final wide. (d) The snap g2024-2038 (diff peak 27) is eased, so it is not a pop.

## Summary
- s10 PASS (B1 fixed; focus lines still thin, note).
- s11 PASS (B2 and B3 fixed; mocker 130-183 px accepted, laugh and blush read on the phone; red chair and pointing direction are notes).
- s12 PASS (N7 fixed in part).
- s15 PASS (press readable, crew and register improved; blue bar and edge-cropped worker are notes).
- s30 FIX: everything from round 2 is fixed except Morse. He is half hidden behind the jamb and at the frame edge, with about 16 px of face on the phone, so the grin does not read. Bring him out from behind the jamb and shift the final framing left. Small re-render, s30 only.
Sheets and crops: /tmp/claude-0/-home-user-github-commit-quest-v2/d013e474-c7c9-591e-b74b-eccded3d274b/scratchpad/qa16/r3/<take>/ (p6_*.jpg, cuts.jpg, crops); edge frames are in r3/edges/. Frames and worktrees are deleted, and the repo is untouched (film16/main).
