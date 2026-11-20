# QA-tech round 12 s17: FAIL

Checked: all 91 frames extracted; 14 frames at 6 fps (g1309-1387) on a sheet with the y 860 line; full-size looks at g1333, g1363, g1387; zoom crops of the fg bundle (g1333) and the tie (g1387). Pixel measurements on the rendered frames.

## Blockers
1. g1309-1339 (and the small bundles after) - fg reed bundle still has no shading and no contact shadow (explicit ask). Zoom of g1333: the big bundle is one flat mustard fill with a navy outline and line strokes; no light/dark side, no darker underside, and no shadow on the ground under it (the ground beneath is the same violet right up to the outline). The small bundles at g1345-1387 (x 40-120, y 1120-1280) are the same flat fill. Fix: lit toon shading on the stalks (2-3 tones from the fire/lamp side), a soft dark contact-shadow quad (~40 % opacity, 20 px blur) under every bundle, and a warm rim light.

## Previous blockers
- `mygap` tan slab: GONE. No tan trapezoid anywhere. Note: at g1309-1345 a darker violet ground area with a hard diagonal edge (g1333: from x 0,y 1090 to x 720,y 940) is still visible. It carries the same pebble texture, so it reads as a shadow/lit-patch change, not a slab. Soften the edge if you can.
- Tie reads: ACCEPTABLE (note). g1381-1387 the old man holds the bundle with its bound end (red ties) on the ox's tail tip, the tail's reed tassel and red ties continue from it (crop 1387). He looks at the lens, not the tail (rule 7 is a note).
- Plain road: team claim 9-15 % is NOT what I measure. Ground below y ~0.66 is ~34 % of the frame; pixels of plain ground colour (no prop, no figure): g1339 20 %, g1345 20 %, g1351 24 %, g1357 23 %, g1363 26 %, g1369 27 %, g1375 21 %; with a wider colour tolerance 29-31 % across g1315-1387 (g1363 29 %, g1387 29 %). So 20-30 %: within the 30 % gate (a note), but not 9-15 %. A dark fg prop low in frame g1351-1375 would bring it to ~20 %.

## Hard checks
- Face below y 860: none (old man's face lowest ~y 790 at g1375-1387, beard tip to ~y 880 is not the face; ox faces at y 640-820).
- Placeholders: none grey/navy. The tub at the left (g1327-1369) is flat blue-grey with no texture, a note.
- Flames on tails: the ignition has not started in this shot; orange flame at the wall base is the set's fire, not on a face. OK.
- Subject in frame: oxen and elder in frame the whole take (elder leaves x range only at g1309-1312 and at the very first frames, as before).
- No zoom pulsing seen (continuous dolly/truck). Mouths held. No text.
- Frame diff (my re-measure, 90x160): median 10.68, p90 16.74. OK.

## Notes
- Beard tip reaches y ~890-910 at g1375-1387 (caption band).
- Plain ground 20-30 % (see above); pebbles are the only dressing.
