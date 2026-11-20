# QA-art s13 (TAKE gate, key shot: false payoff) — FIX-FIRST
Reviewed every 5th frame (6 fps) at full size 720x1280 and at 360x640. Frame refs: i = take frame index (0-82), g = film frame (g = 994 + i).

| criterion | score |
|---|---|
| Beat clarity on a phone | 5 |
| Light and colour | 7 |
| Composition | 4 |
| Acting | 5 |
| Camera | 3 |

What works: warm campfires and torches against a blue night, a dense camp with tents, spear racks, drums and jars, and laughing soldiers with raised cups. It reads as a party.

Problems:
- ZOOM PULSING. There are punch-ins at i22-24, i42-44 and i62-64, each released by a pull-back over the next ~6 frames (i27-32, i47-52, i68-72). Frame-diff spikes at 17-21 confirm all three. This breaks the film-18 rule 1.
- Bottom ~35-40 % is bare ground (i0-i82) with navy low-poly lumps (stools/rocks, about y 1000-1100). From i30 on, an untextured blue low-poly brazier/tripod rises into the bottom centre (i55-i82, big at i76). This breaks rules 2 and 5.
- The horizon is a flat blue-grey ground plane with a gridded road strip running to the mountains (i0-i82, about y 300-420). It reads as an unfinished placeholder floor.
- Soldiers are about 25-40 px tall on the phone sheet. The cheering reads, but the sentry dropping his spear (g1030 = i36) cannot be found at phone size.

## Changes (practical)
1. **Camera, whole take:** remove the 3 punch-in/out pairs (i22-32, i42-52, i62-72). Keep one smooth eased pull-out of 6 %/s plus a 40 px/s slide and the light sway.
2. **Bottom third, i0-i82:** delete the navy lumps and the blue low-poly brazier. Put one lit, textured fg prop 1-2 D from the lens at lower left or lower right (wine jar or cup-laden table, warm-lit), and tilt down/raise the camera so the lit camp fills down to about y 1000. Plain ground should be at most 25 %.
3. **Horizon, about y 300-420:** hide the gridded plain and road behind a dark palisade or tent row, or drop the plane to near-black with a soft fog. No visible grid.
4. **Sentry, g1025-1040 (i31-46):** move the sentry to the mid-ground near the frame centre (head about 60-80 px tall at 720 wide), with a torch-lit rim. Make the spear drop a clear diagonal fall that lands by i46, then he raises a cup.
