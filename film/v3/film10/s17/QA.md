# s17 QA (round 2, after QA-art FIX-FIRST): film 10, shots 17-19 (the reveal)
Delivered: take.mkv as take.mkv.part* (cat to rebuild), g 1084..1433, 350 frames, first_g 1084, g0 1090, g1 1428. qa_auto PASS.
Fixes: 
- 17: wider steeper camera (lens 14.5-15, loc z 125) keeps torpedo, ship, gold buoy in frame the whole shot; top third now sea + convoy row.
- 18: ghost laid hull-on-hull on the real ship (offset 5 s, mirrored), opacity 0.85; lens 35-36.5, camera follows the ship, ship fills ~90% of the circle; ghost rigging wires removed from the mesh.
- 19: ghost peels away left and fades to 0.3 right after the cut (g 1296-1332), then 0.1 at the end; camera holds on the crossing (g ~1320-1375, torpedo reaches the cyan buoy in clear water behind the real stern) before following the ship.
- Buoy lamp lights keyed to 0 energy: no glare streaks on the water.
Known: ship is smaller on screen in 17/19 (about 25-30% width) because torpedo, ship and buoy must share the frame.

## Round 3 (QA-tech addendum)
- 18: ghost mirrored over the real hull, offset -15 D so its reversed bow sticks out past the real stern (~23%), opacity up to 1.0 with the emissive rim; funnel cylinders and rigging wires removed (no glass look).
- 19: ghost peels left and fades to 0.3 before the pass; ONE torpedo, one soft bubble wake, passing behind the real stern.
- 17/19: torpedo 3x, arrow-like foam V removed (soft bubble wake only); both buoys 1.5x, inside the frame.

## Round 4 (QA-art round 2: shot 18 only re-rendered; 17 and 19 frames unchanged)
- 18: ghost directly over the real ship (offset 5 s, no sideways offset; slow drift to shot 19's first-frame offset), opacity 0.8 fading in over the first 1.5 s, rim kept; wires hidden.
- Last ~0.6 s (g 1278-1295): the view swings left and the cyan aim buoy enters the circle on the left (placed on the line of sight for this shot only), so the cut to 19 reads as "he aimed there".

## Round 5 (QA-tech addendum: shots 18 and 19 re-rendered, 17 unchanged)
- Ghost = flat clean cyan silhouette (constant alpha = opacity, no fresnel falloff, so the real stripes do not show through), bright rim kept; its smoke puffs (cyan discs over the funnels), funnel cylinders, rigging wires and thin rail rods removed.
- 18: lens 30 -> 31 so both ends of the real ship are inside the circle; ghost 0.8 directly over the hull; aim buoy in the circle at the end.
- 19: miss staging unchanged; only the ghost style changed.

## Round 6 (final gate): shot 18 g 1270-1295 only
- The aim buoy is cyan (body and lamp) like the ghost; its halo is cut to ~1/3 (small steady glow, no flare disc); the swing now settles with the buoy near the crosshair (pan 40 D). All other frames unchanged.
