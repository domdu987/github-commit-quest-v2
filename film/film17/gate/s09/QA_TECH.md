# QA-tech s09 (film 17 shots 22-23) - FAIL

Checked: 38 frames of f6 (every 5th plus cut neighbourhood g1270-1278) as 360x640 sheets, full-size crops of g1220, g1260, g1310. Laplacian not measured. Heads all well above y 880. No black/blank frames. Dissolve g1190-1200 and hard cut g1275 land correctly. rhythm / qa_auto taken from the brief (PASS).

## Issues
1. g1190-1274 (shot 22), coverage: nobody enters. All four figures stand in the same line from the first frame (positions unchanged g1190 -> g1270; only the camera moves). No walk/escort motion, the door behind is never passed. Fix: animate the group walking in through measure_door (gendarmes stepping, dupont between them), the inspector following a beat later.
2. g1215-1274 (shot 22), inspector: arms folded, flat/sullen face, half hidden behind the green gendarme from g1245 and nearly out of frame; the "smirk" does not read (moustache-flat mouth, heavy lids). Fix: visible one-sided grin / raised brow, keep him in frame, not behind the gendarme's shoulder.
3. g1275-1345 (shot 23), inspector does not grin at Bertillon: face turned to camera, eyes flat/closed (g1330-1345), mouth hidden under the moustache; no eye-line toward Bertillon. Plan beat missed. Fix: turn his head/eyes to Bertillon with a readable grin.
4. g1275-1345 (shot 23), stray thin white crossed rods float above the table next to dupont (x~290-350 of 360 at g1275, drifting to the chair at g1300-1335). Team says these are set props, but they read as an unattached floating X: no stand, nothing holds them, and from g1305 they cross in front of dupont's chair arm and torso. Fix: rest them on the table/rack or in Bertillon's hand, or remove; at minimum keep them behind dupont.
5. g1280-1335 (shot 23), foreground table covers dupont's legs/lap (g1300-1335 almost the whole lower body); what shows below the seat is a single thin teal stub (g1275-1295), reads as a broken leg. Fix: lower/shift the foreground table, or hide legs cleanly; give dupont two visible legs.
6. g1275-1345 (shot 23), shake head: dupont's head only tilts slightly; the "no" shake is not readable at 6 fps (shrug with raised hands is fine). Fix: clear +-8 degree yaw/roll shake x2 with mouth closed.
7. g1275-1345, dupont's mouth shape alternates between a small smile (g1280, 1290, 1305, 1330) and a flat line (g1295, 1315), and Bertillon/inspector mouths shift slightly: minor mouth jitter outside any quote. Fix: lock mouth state.
8. g1240-1274 (shot 22), left edge: inspector-side gendarme (blue) is cut by the frame while his arm still holds dupont (g1250-1274: only his arm and sliver of face). Fix: slide less or keep both gendarmes in frame (hands on arms must be seen with the gendarme).
9. g1275-1345, tiny stray white specks at left edge (x 0-25, y ~1280-1330 of 1280 on the sheet, e.g. g1275, g1330): dust layer, low contrast. Minor: remove or dim.
10. Shot 22 opening size: group ~300 px tall at g1190 (OK, plan 280); shot 23 dupont head ~170 px wide at g1340: fine. Bertillon cropped by right edge at g1340-1345 (head half out). Minor: reframe slightly right.
11. Continuity: costume/props consistent with neighbours (dupont beret/brown coat, satchel only in shot 22 -> missing in shot 23, no longer at his side g1275+). Minor: satchel vanishes at the cut.

## Verdict: FAIL (blockers: 1, 2, 3, 4, 5)
