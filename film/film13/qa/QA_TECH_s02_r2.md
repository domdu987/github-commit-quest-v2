# QA_TECH s02 round 2 (film 13, TAKE gate) - FAIL (minor, 3 fixes)

Checked: qa_auto (108 frames g57-164, PASS: 0 frozen/black/pop, magenta 0 %; planned cuts g63/g159 are handle boundaries, in-take cut at g108 = frame 51 is visible), 6 fps sheets, cut +-3, full-size hands crops, joins s01->s02->s04. Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qa13r2/ (s02_a.jpg, s02_b.jpg, hands.png, join1.jpg, join2.jpg). Take files untouched.

Round-1 items:
- Lady cup AND saucer: PARTLY FIXED. g 57-90 she holds saucer in one hand and the cup at her mouth (clear sip g~63-87). From g~92-107 (frames 28-40 of the take, shot 2 end) her arm stays raised at her cheek and NO cup is visible in that hand (cup vanishes / hidden by arm), saucer still in the other hand.
- Gentleman: cup + saucer at chest, held all shot 2, OK.
- Cup not clipped: NOT FIXED. Shot 3 (g108-158): left cup/saucer rim touches/crosses x=0 for the whole shot (worst ~g120-140); teapot cropped at right edge. Cups sit on the frame edges.
- Tea disc visible: FIXED (two pink mirror discs, window reflection, ripple 0). Window with rooftops + tower sliding down: FIXED, clearly readable (tower drops ~25 % of window in shot 3, also in shot 2).
- Shimmer: REDUCED but still present on the carpet in shot 2 (fine horizontal scan-line/moire on stripes, lower 25 % of frame, g57-107).
- Smeared mud / blur: none. Workers: none in this take. Heads: guest heads y ~330-560 <880 PASS. Mouths: closed smiles, no mouth motion, PASS.

Remaining issues:
1. g 108-158 (shot 3): left cup+saucer clipped at left frame edge, teapot clipped right. Fix: shift/zoom camera left-to-right so both cups sit inside x 20-700 with margin (pull back ~8 % or pan +40 px).
2. g 92-107 (shot 2): lady's cup not visible while her hand is raised (arm up at cheek, saucer below). Fix: keep the cup in the raised hand through the lower phase, or lower the cup onto the saucer by g 100.
3. g 57-107: carpet scan-line shimmer remaining (phone sheet shows it on the diagonal stripes). Fix: more samples / texture filtering on the rug.
4. g 57-107 NEW: an oversized cup+saucer on a shelf hangs outside the window at the right edge (x 640-720, y ~330-420 at full res), floating over the skyline and drifting with the street; reads as a floating object. Fix: hide that prop in shot 2 (it is the shot-3 table seen from the wrong side) or lower its y so it is below the sill.
Joins:
- s01 -> s02 (g62 -> g63): hard cut, OK.
- s02 -> s04: s02 g159-164 (frames 102-107) is the tea close-up; s04 frames show rain street_wide from its in-handle g156 (frame 0), shot proper from g162 (frame 6). Hard cut tea -> rain street, fine. Note: s02 meta says out at g159 while s04 meta g0 = 162; both takes hold handles over g156-164, so cut at either (conform must pick one consistent g, plan says 159; use s04 frame 3).
