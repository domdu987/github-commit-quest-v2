# QA-tech TAKE gate (Stricter QA B), film 20, takes s15 s18 s19 s20 s21 s23 s24
Method: every frame extracted (g = first_g + index) to scratchpad takeqa/<take>/; qa_auto.py run on each take; frames viewed at 6 fps (every 5th) plus g0-3..g0+3 and g1-3..g1+3 (cut +-3) and full-res crops of suspect frames; in-shot frame-diff measured by me (90x160 grey, consecutive frames, g0..g1-1).
Handle frames: all 7 takes have the right counts (dissolve/2+2 on dissolved sides, 4 on cut sides; n_frames matches). Heads: no head crosses y 880 in any take. No text, no black/magenta/blank frames, no frozen runs in any take.

Frame-diff (median / p90; target >= 4 / >= 12): s15 5.66/7.61 | s18 2.91/3.68 | s19 1.61/3.03 | s20 2.43/18.87 (p90 only from whole-frame tap flashes) | s21 10.03/12.96 | s23 5.53/11.40 | s24 3.58/9.87.

## s15 (shot 15, 1889 permit) -- FAIL (minor)
1. g988-1063: bottom 40-45 % of the frame is an empty flat blue-grey ground slab (caption zone, phone size reads empty; QA_TECH set note N10). Fix: ochre trampled ground / FG props (barrels, stall, bench) in the nearest 25 %, or tilt up 4-6 deg so < 30 % is bare slab.
2. whole shot: p90 frame-diff 7.61 < 12 (median 5.66 ok). Fix: the move is too even outside the snap g1064-1079; add crowd/flag motion or a second eased push, or a stronger snap.
3. g988-1063: crowd is thin (about 12 tiny cards in the distance) for "crowds, flags, pavilions"; add 10-20 more cards in mid-ground.
Verified OK: tower reads as Eiffel; young Eiffel (dark beard, bowler); sealed permit with red wax seal held by official g1000-1030, in Eiffel's hand from ~1020; smile -> flat mouth + sweat drop after blink g1066-1068 (clear by 1073); no mouth motion; feet and contact shadows ok; cut 1092/1093 clean (both sides same Eiffel close-up).

## s18 (shot 18, dusk 1909 wagon) -- FAIL (major)
1. g1210-1305: bottom 45-55 % is a flat, saturated pure-blue slab (reads as a void, not dusk ground). Fix: warm/desaturate the dusk ground (cobbles/dirt, luma/sat like the lit part of the set), add ruts, planks, ropes, stones in FG; raise camera aim so the slab is < 30 %.
2. g1225-1305: the demolition wagon + scrap cart are not readable. What reads is a brown wicker/barrel-like blob at left and a jagged brown plank spear in the FG (broken geometry, torn edges, no shadow, g1260-1305 large). Planned beat "wagon with crowbars, ropes and scrap cart waits at the foot" is missing. Fix: frame the wagon (wheels, bed, crowbars, rope coils, scrap heap) beside the group, delete/repair the torn plank FG.
3. g1210-1305: no visible contact shadows under Eiffel/officer/riveters on the blue slab (feet float on flat colour). Fix: contact decals with dusk-dark shadow.
4. g1254-1305: calm -> worried swap is not readable (half-lidded face, no sweat/worry cue at 1285). Fix: stronger worried eyes/brows or a sweat drop on the blink g1253-1255.
5. whole shot: frame-diff median 2.91, p90 3.68 (target 4/12); camera push is slow and the 15-frame snap x1.3 at g1252-1267 is nearly invisible. Fix: raise the snap to x1.6+, add sway.
6. g1210-1260: figures are tiny (heads 15-40 px at start) and clustered at far left; the shot reads as tower + empty blue. Fix: move the group 2-3 m closer / lower camera.
Verified OK: old Eiffel white beard and bowler; tower + lights read as Eiffel; antenna wires visible; no mouth motion; cuts 1221 and 1302 land cleanly (same framing as the next take's start).

## s19 (shot 19, antenna whip-tilt) -- FAIL (major)
1. g1343-1352: the planned "whip-tilt down along the wire to the ground" is not what is shown. It is a 9-frame sideways slide/slight tilt that drops the tower out of frame left; the wire ends at the hut roof (not the ground) and the move never follows the wire. Fix: start framing the summit, whip aim summit -> wire foot at 'จากยอดหอ' (1343) with the wire visibly crossing frame to the ground.
2. g1298-1342: starts on a wide of the whole tower with Eiffel tiny at the hut; plan says start on the summit. Fix: start tight on the summit.
3. g1353-1385: after the whip the frame is 45-60 % flat blue slab with the hut on a stripe; static (diff ~1.1-1.5), plank-free ground, no contact detail. Fix: same as s18-1, and keep a move (push + sway) after the whip.
4. g1298-1343: Old Eiffel's "points up" does not read: hand at head level, looks like a salute/scratch; head is 83-110 px but mixed with hut. Fix: arm clearly extended up toward the summit.
5. whole shot: frame-diff median 1.61, p90 3.03 (target 4/12; the whip g1344-1350 is the only motion, diff 11-23).
6. wires: 4 solid white 4-6 px bars (g1298-1385), brighter than s18's pale wires and s21's fat grey wire. Fix: one wire look across 18/19/21.
Verified OK: no blur on the whip frames, no mouth motion, heads < 880, cuts 1302 and 1382 clean.

## s20 (shot 20, hut spark) -- FAIL (major)
1. g1378-1434: telegraphist's hands never touch the key; arms hang at his sides while the lever and the spark gap flash several tiles away. Fix: arm/hand on the key knob, visible tap (forearm dip) on each tap g1387-1389, 1393-1395, 1399-1404, 1410-1412, 1416-1421, 1426-1428.
2. g1405-1434: soldier drifts to the left edge; his head/cap is clipped by the frame edge (g~1425-1434) and the spark gap is clipped by the FG post (g1428-1434). Fix: aim 0.65 m less to the right, keep head >= 40 px inside both edges.
3. g1388-1428: spark gap is a pale blue sphere with a white scribbled X glyph (reads as a scribble, not a blue-white spark); two brass balls are visible but no arc. Fix: arc between the balls + small halo.
4. g1378-1400: a second pair of headphones lies on the desk in FG while the soldier wears one: duplicate prop. Fix: remove the desk pair or the worn one.
5. whole shot: frame-diff median 2.43 (< 4); p90 18.9 only from the whole-frame brightening on taps (every tap frame diff ~19, luma 67 -> 93 on the whole hut). Fix: constant push + sway for the median; keep tap flash local to the gap.
6. g1378-1434: the wall/floor shows moire stripes on the planks while moving (floor y>880 striped pattern) -> shimmer risk at phone size. Fix: lower plank texture contrast / bump the texture filter.
Verified OK: flashes sync with the planned taps; head y 502-521; no mouth motion; cuts 1382 and 1431 clean.

## s21 (shot 21, night signal rings) -- FAIL (major)
1. g1427-1433 (cut frame 1431 included): the summit looks like a different, unlit low-poly dark-brown box tower over a dark flat sea; reads as not-the-Eiffel for the first 6-7 frames and the lit orange tower appears at 1434. qa_auto also flags soft frames g1427-1432 (6 frames; only 1-3 allowed). Fix: render the summit with the same lit tower geometry/materials, start the whip already moving, <= 3 blurred frames.
2. g1437-1527: the "signal rings" are 5-6 thin white arcs hung around the tower at fixed positions; between g1470 and g1503 they do not expand or spread over Paris (a ring is born every 6 f per cues but nothing visibly travels). Reads as hair-thin wires, not glowing rings rippling out over the city. Fix: bright expanding ring bands in the plane of Paris (thick glow, fading, radius growing 30 -> 560 m, visible over the rooftops).
3. g1530-1560: "lattice glows along the wire" at 'เสาอากาศยักษ์' becomes a washed grey-pink tower (loses orange, looks matte) with a thin white diagonal wire; it does not read as blue-white glow along the wire. Fix: blue-white emission running up the wire and lattice edges with the orange kept.
4. wire look is inconsistent in-shot: a fat grey 12-15 px plank g1432-1527 -> a thin white line g1537-1560. Fix: one wire material.
5. g1437-1560: lower 25 % of frame is flat dark-green ground with large tree blobs hiding the tower base after g1530 (tree in front of the legs g1532-1560). Fix: move camera/tree so the base stays visible.
Verified OK: frame-diff median 10.0, p90 13.0 (pass); no pops outside the cuts; tower reads as the Eiffel Tower g1437+; no characters; cuts 1431 and 1560 land inside motion.

## s23 (shot 23, 1910 extension) -- FAIL (minor)
1. g1648-1659: jagged black rectangles at top right (clipped FG sign/lamp bracket, x 600-720, y 0-80) and a black lamp-post pole crossing the right edge g1663-1702 (full height, 10 px, hard black, no lamp head). Fix: replace FG with a proper lit lamp post out of the move or hide it; clip/mask the handle frames.
2. g1706-1739: "bowler raised" reads as a flat black dish/tray at chest height (hat held edge-on); a black ball also sits on the document where the hand should be (g1710-1739). Fix: raise the bowler visibly to head/hat-tip height with a visible hand; show the hand on the document.
3. g1648-1700: bottom 40 % flat blue-grey ground slab (see s15-1); g1713-1739 the lower third is bare slab.
4. p90 frame-diff 11.40 (< 12, marginal; median 5.53 ok).
Verified OK: old Eiffel (white beard, bald) continues from the 1909 takes and differs from the young Eiffel of s15; 1910 DAY sunny, same framing as s15 (callback); new sealed document with red seal in the left hand from ~g1696; blink swap at 1705-1707 -> smile; no mouth motion; head y 596-700; cuts/dissolve handle 8 frames both sides present.

## s24 (shot 24, ending: waiter leads Maupassant) -- FAIL (minor)
1. whole shot: frame-diff median 3.58 (< 4), p90 9.87 (< 12) excluding the snap; characters walk in place relative to the camera (size and screen position nearly constant g1740-1814) so the planned "leads to his window table" does not progress; the window table is never reached/visible. Fix: run the cards along the runner so they visibly reach the table, increase the camera slide, stronger snap at 1779.
2. g1731-1742: Maupassant's body looks translucent/ghosted where the FG chair back overlaps (blue coat blends into the background at g1733-1735); chair back also reads half-transparent. Fix: check alpha/sort of the chair FG and the card.
3. g1794-1814: blown white light streak down the carpet (runner floor), V=1 band about 80 px wide. Fix: lower the window light/specular on the floor.
4. g1799-1814: right FG diner stand-in card is a faceless dark-blue figure cropped at the edge. Fix: remove or give it a face/turn.
Verified OK: dense warm restaurant (girders, chandeliers, white cloths, diners); no mouth motion (moustache only); heads y 604-676 < 880; feet on the runner with shadows; handle frames present (8 in / 4 out); cuts 1732 (dissolve in) and 1814 clean.

## Notes
- I ran qa_auto.py without --out, which rewrote QA_AUTO.md in some take folders (s23, s24 notes line added); I restored s23/s24 with git checkout; git status is clean. Nothing in the takes was edited or committed.
