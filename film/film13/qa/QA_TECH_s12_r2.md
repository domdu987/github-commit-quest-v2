# QA_TECH s12 round 2 (film 13, TAKE gate) - PASS (with non-blocking notes)

Checked: qa_auto (first_g 720, cuts 726,780,843,912), 6 fps sheet, cuts 777-783 and 840-846 at 30 fps, full-size crops of g835 and g865/870 with band line, joins s10 -> s12 -> s14. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13s10r2/s12/ and /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13s10r2/full/. Take untouched. 198 frames (take.mkv complete).

Round-1 issues:
1. Pullman head in band g836-841: FIXED. No crane down; Pullman not in framing B. In shot 13 his chin tops out ~y 850-870 at g860-875 (full-size check: chins at ~790-870, band line 880) -> no crossing, but within ~10-30 px at g860-875 (margin thin, OK).
2. Extreme brick close-up: IMPROVED. Framing A (g720-779) is now a street/steps two-shot: hotel front, Pullman with the rolled plans raised toward the window, rich in the top window. Framing B (g780-842) is still ~80-85% brick/cornice with the rich small in the window (head 45 -> 95 px); sky/cornice are in frame. Non-blocking taste note (dense set, but a lot of plain brick).
3. Rich leaves frame before Q1 ends: FIXED. He stays in the window until g842, mouth moving throughout (all inside Q1; Q1 ends g846).
4. Rich rigid in window: still mostly stationary with a small arm gesture; non-blocking. In framing A he is ~15 px tall (mouth not legible, only in B).
5. Crowd chins near band (g843-917): FIXED. Foreground chins at ~790-830, Pullman < 870, nothing >= 880.
6. Crowd laugh/point: IMPROVED. ~80% laugh with arms up, smiles/open mouths, bouncing; nobody clearly points at Pullman, Pullman looks forward at camera. Bottom ~30% is plain mud (smooth, no detail) - non-blocking. Jack on shoulder attached throughout.
7. Nickname jump g895 present. OK.

Other checks:
- qa_auto "suspected blur" g809-842: FALSE POSITIVE confirmed. Full-res Laplacian var drops 770 -> 380 as the push-in fills with smooth brick; full-size crop at g835 shows crisp brick edges and window frames, no DOF. Non-blocking.
- Pullman eye-line in framing A: faces camera (scowl), not up at the window; arm/plans point up. Non-blocking.
- Pullman prop (rolled plans in A, iron jack in 13) attached. Heads < 880 all frames (shot 12 Pullman chin ~800-840).
- Cuts: 780 (street -> close brick) and 843 (brick -> crowd) are clear cuts; qa_auto 'no visible change' at 726/912 are handle/join frames. Convention per README accepted.
- Joins: s10 end (suite) -> s12 start (facade) clean; s12 end (crowd, g917) -> s14 start (street/trench, g906-912, small figures with barrels) hard cut, OK. s07 end -> s12 not adjacent.
- No frozen/black/magenta frames.
