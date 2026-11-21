# QA-tech s09 ROUND 3 (film 17 shots 22-23, g1190-1348, render17/team8 9ddf81d) - FAIL

Checked: 38 f6 frames as 4-up sheets at 360 px width, full-size crops of g1190/1200/1210, g1255/1265/1274, g1300/1320/1340, g1315 lower right. Every frame of take.mkv (159) measured: Laplacian variance (median 300, min 266, no frame under 60 %), mean luma 90-110 (no black/blank/magenta), frame diff max 62.9 at g1275 (the planned cut only), no frame with diff < 0.1 (no frozen run). Beret centroid tracked on all frames g1275-1348 to measure the head shake. rhythm 7.50/14.36 and QA_AUTO PASS taken from files.

## Team claims
1. Inspector visible and walking in from g1190, no pop-in: TRUE. He is visible at the right of the group from g1190 (blue kepi, handlebar moustache, one leg stepping) and stays in frame to g1274; no pop-in at g1205-1215. He stands about 100 px right of the group rather than clearly trailing through the door, minor.
2. Inspector grins at Bertillon, eyes smile arcs, head turned toward Bertillon, clear of Dupont: NOT TRUE. g1300, 1320, 1340: his eyes are flat heavy-lidded dashes under straight brows (no arcs); his head faces camera/Dupont with a small tilt, with no turn toward Bertillon, who is at the right behind the chair (x 600-700 on 720). The only smile cue is a tiny curve under the moustache (about 20 px wide). It reads as a sleepy smirk at Dupont, not a grin at Bertillon. Dupont's beret overlaps the inspector's right moustache tip and the cheek/chin edge in all shot-23 frames (g1280-1348, about 30-45 px at 720 wide). This is not "slight, g1310-1330 only" and it is not minor: it cuts into the one feature of the face that carries the beat.
3. Blue gendarme fully in frame through g1274: TRUE with a caveat. Head, kepi and body are inside the frame at g1255, g1265 and g1274; the cape tip and rear foot touch x 0-4 at g1265-1274. Pass.
4. Ring with blue dot and rod with square clip gone, dust off: TRUE. g1300-1315 lower right is clean, the clamp is present in all frames g1280-1345, and no ring or rod is seen. At g1210 a bright dot hangs near the chandelier at top left and there are 1-2 px specks at the right edge at g1310 (x about 715, y about 490); both are negligible.
5. Dupont's face fixed, flat closed mouth: TRUE. g1280-1345 show the same flat dash mouth, half-lidded eyes and blush. No switching. R2-7 is fixed.
6. Head shake, two bursts at 2.5 Hz: NOT TRUE. Beret x per frame (g:x) runs 1275:270, 1288:255, 1292:261, 1300:235, 1310:230, 1316:238, 1323:270, 1328:256, 1332:268, 1338:247, 1348:249. That is slow sway of 20-40 px with a period of about 20-30 frames (1-1.5 Hz), not two bursts at 2.5 Hz (a 12-frame period). Roll changes by roughly 15 degrees across the shot. At phone size it reads as swaying or looking around, not a clear "no". Hands-out shrug reads and is fine.
7. Legs still thin stubs: CONFIRMED. At g1280-1345 only one short thin teal stub shows under the coat hem (about 12 px wide, 25 px long at 720 wide), and the second leg is not visible. Not minor: it reads as a broken or missing leg. Should-fix.

## Round 1/2 items
R1-1 fixed. R1-2 fixed (inspector visible and in frame, arms folded; smirk is weak but readable as smug). R1-3/R2-3 inspector grin at Bertillon: NOT FIXED. R1-4/R2-3/R2-4 rod and ring: fixed. R1-5 legs: partly. R1-6 shake: partly (see 6). R1-7/R2-7 mouth: fixed. R1-8 gendarme crop: fixed. R1-9 dust: fixed. R1-10 Bertillon in frame: fixed (head and glasses fully inside through g1348). R1-11 satchel: accepted. R2-1 pop-in: fixed. R2-2 inspector hidden behind Dupont: partly (face is visible, but the beret overlaps the moustache tip).

## Standard checks
- Mouths: none move; no quote window. PASS.
- Props: Dupont's arms are held by the gendarme and the green gendarme in shot 22 (hands touch his arms). Table clamp, jar and stool are on their surfaces. No floating props. PASS.
- No see-through cards, no beam shafts on characters. PASS (soft floor light patches in shot 23 sit on the floor only).
- Chins above y 880: shot 22 chins at about y 540-620 of 1280; shot 23 Dupont's chin at about y 700, Bertillon's at about y 570. PASS.
- Blur: no frame below 60 % of the median Laplacian; no blur run. PASS.
- Frozen: none (no frame diff < 0.1). Pass.
- Blank/black/magenta: none. Pass. Cut g1275 is a hard cut at the planned frame; the g1190-1200 dissolve is fine.
- Phone-size read: shot 22 reads (two gendarmes escort Dupont, inspector behind with a smug face). Shot 23 reads the shrug and the flat innocent face; the shake reads only as a sway and the inspector's grin at Bertillon does not read.

## Verdict: FAIL

### Blocking
B1. g1275-1348 (shot 23), inspector beat "grins at Bertillon" is still missing (R2 item 3 carried over). His eyes are flat dashes, not smile arcs; his head is not turned toward Bertillon (eye-line goes to the camera/Dupont); the smile is hidden under the moustache. Fix: swap in the smile-arc eye card, rotate his head 15-20 degrees yaw/roll toward the right, and raise the mouth/cheek above the moustache so a grin shows. Beret overlap: move him up or left by about 40 px, or lower Dupont's beret, so the moustache tips and lower face are clear.
B2. g1275-1348, Dupont's head shake does not meet the plan, and the claimed 2.5 Hz is not present: the measured motion is a slow sway of 1-1.5 Hz with only about 1.5 cycles. Fix: two or more clear left-right bursts at a 10-14 frame period (at least +-8 degrees roll and +-25 px), each side held 2 or more frames, mouth kept flat. Because the plan names "shakes head", this is blocking.

### Should-fix
S1. g1280-1345, Dupont's legs: one thin teal stub, second leg missing. Add two legs of the width used in shot 22, about 25 px.
S2. g1274, the blue gendarme's cape tip touches x 0; start the camera 10 px further right.
S3. g1190-1210, the inspector is about 100 px right of the group, not behind it in the door line; offset him 40-60 px toward the group so "trailing" reads.
