# s19 QA-art

## Round 7 (director QA-art) - 2026-11-20 - verdict: FIX

Take: v3/film19/s19/take.mkv (g1459-1589, 131 frames; BIGZOOM g1468-1552 = 48.93-51.73 s).
Frames: /tmp/qa19_r7art_s19/ (3 fps, f_NNN = g1459+10*NNN; full size, p_NNN at 360x640, phone_sheet.png).
Compared with ref R5_sheet.jpg (ship story) and R4_sheet.jpg. Rules checked: QA_TEAM.md sections G, H and I.

### Measured (qa_stats2.py and per-frame stats)
- Whole take: sat 0.499, vivid 55.9 %, luma 127.6, warm 46.7 %, cool 41.3 %.
- Luma is 117-138 on every frame. That breaks §G1 (85-110) all through the take. The peak is 138 at g1529, where pale sand fills the frame.
- Saturation is 0.54-0.56 in the opening wide. It drops to 0.46 from g1544 to the end, on the payoff frames. That is below §G1 (0.47) and §I3 (0.50).
- The BIGZOOM is 84 frames = 2.8 s. That is under the §H1 minimum of 3 s.
- The ease is uneven. The move is slow from g1468 to 1494 (mean frame difference 2-6), then fast and nearly constant from g1499 to 1544 (9-14), then it settles. There is a real ease-in but a short, late ease-out.

### What works
- It is one continuous move with no cut. It passes palm fronds and runs over palm shadows on the sand, so the §H rule about passing set detail is met in spirit.
- The three-masted ship and sun glitter on turquoise water make a strong, R5-like opening image. The sky is clear blue.
- The landing is a good medium three-shot. The characters are about 45-55 % of frame height, below the §G3 35 % face limit (William's face is about 14 %). All three have feet on the sand with contact shadows.
- Nothing floats, nothing passes through a face and no character is cut in half. I checked every 0.33 s tile.
- The payoff is readable on a phone by about 51.3 s (g1539): William is in the centre, the watch is up and the crew are cheering.

### Problems
1. **The start is not extreme wide (§H1).** At g1468 the view is a hilltop over a small cove, not "the whole bay from high and far". The horizon sits 27 % from the top. There is no Port Royal, no town and no headland chain. The crew are about 2 % of frame height and you can just find them as three specks by the rowboat. That part is OK, but the scale reads as "wide", not "extreme wide".
2. **The flank hill wedges look cheap. They are the main set flaw.**
   - Both brown hills are flat, untextured triangles with ruler-straight diagonal edges. They read like cardboard cut-outs framing the cove, and their flat cocoa colour is the dullest thing in the frame.
   - Hard mesh edge: at g1519-1530 (f6-f7), right edge x≈680-720, y≈470-580, a flat tan box ends in a vertical wall and the sea plane is cut off along a straight vertical line beside it. This is bare-geometry backdrop, visible at phone size just as the payoff lands (crop: /tmp/qa19_r7art_s19/crop7.png).
3. **The foreground red block (g1459-1489, lower centre) is an untextured red hip-roof box.** It is the biggest foreground object and reads as a primitive, not a hut. There are no walls, no thatch and no door. The low-poly green fronds in the bottom-left corner have the same problem.
4. **The near palm canopy renders solid black.** You can see it at g1499 top-left and at the top right from g1529 to the end. The frond undersides get no fill or bounce light, so they read as holes in the frame.
5. **Empty sand (§H3).**
   - From g1499 to g1529 the lower 40-50 % of frame is plain sand with only palm shadows on it.
   - On the landing, the lower 20-25 % is bare sand with one shell.
   - The beach has no life: no other crew, no crates, barrels, nets, flags, smoke, gulls or footprints. R5 packs every deck and quay with props.
6. **Colour is washed out on the payoff.**
   - Pale orange sand plus a pale lower sky push luma to about 130 and pull saturation to 0.46.
   - There is no rim light on the cards (§I2) and no warm/cool split on the characters, so they sit flat against the sand.
   - R5 is deep blue with hot orange accents. This frame is beige.
7. **The acting is uniform.**
   - All three characters strike the same arms-up pose with the same grin.
   - William is not set apart. He has no bigger beat and no look at the watch, and the watch reads only about 45 px wide at 720.
   - The brief says "tricornes up", but only William's tricorne goes up, because the sailors wear a bandana and a beanie. The right sailor's pompom touches the tricorne brim at g1539-1579 (a small tangent).
   - A loose blue blob between William's feet (a shell?) reads as a stray object.
8. **The move ends 0.2 s short (2.8 s against the 3 s minimum).** Most of the descent happens at constant speed over g1499-1544, so the swoop feels functional rather than spectacular. R5's crane-outs hang on the wide and then dive.

### Scores (/10)
| Area | Score |
|---|---|
| Set | 5 |
| Light and colour | 5 |
| Composition | 6 |
| Acting | 6 |
| Key moment | 6 |
| Match to references | 5 |
| **Overall** | **5.5: FIX** (blocking issues against §G1 luma/saturation, §H1 and §H3) |

### Concrete fixes (ranked)
1. **Start higher and wider.** Begin the BIGZOOM about 2-3 times higher and further back, so the whole bay is in frame: the ship, a second headland, a Port Royal strip of red roofs, a fort and flags on the far shore. Keep the crew at 2-4 % height, with a bright red bandana or a small white flash on the watch to help the eye find them. Stretch the move to 3.5-4 s: hold the wide for about 0.5 s, then use a longer ease-out on the landing, which can borrow from the 9-frame tail handle.
2. **Replace the brown wedges.**
   - Use displaced, irregular hills with rocks, grass tufts, scrub, a few palms on the ridge and a green-to-ochre gradient.
   - Or swap them for jungle masses. Break every straight silhouette edge.
   - Close or hide the right-side tan box and the cut-off sea plane (g1519-1530) by extending the water and the hill, or by placing a palm cluster or rocks over the seam.
3. **Turn the red box into a real fisherman's hut** with a thatch or plank roof texture, walls and a door, or replace it with foreground props such as barrels, a crate stencilled "H4" or "KINGSTON", nets or a rowboat. Re-light the near fronds with a fill or bounce so their undersides are dark green, not black.
4. **Dress the sand.** Fill the empty lower half: footprints, the rowboat's drag track, crates, barrels, a coil of rope and a small group of extra cheering sailors running in from the boat. Add 3-4 gulls, a flag on the ship and maybe a sign such as "PORT ROYAL" (§I4 allows signs).
5. **Fix the colour.**
   - Darken and saturate the sand toward warm gold-orange and deepen the sky gradient toward cobalt. Target luma 95-110 and saturation of at least 0.50 on every frame, including the landing.
   - Add a warm rim or back light on the character cards against a cooler sea and sky, so the payoff pops.
6. **Make William the hero of the payoff.**
   - Raise him one step, onto a crate or the boat's gunwale. Make the H4 watch about 1.5-2x bigger with a sun glint timed to about 49.8 s ("ห้าวินาที", five seconds).
   - Give the sailors different reactions, such as a hat toss, a hug and a jump.
   - Put real tricornes on at least two sailors and have them thrown up, or change the shot note to match.
   - Remove the blue blob at his feet and fix the pompom tangent.

Re-review after the fixes. Expected pass: set ≥ 7 once the wedges and box are replaced and the sand is dressed. Colour passes once luma is 110 or lower and saturation is 0.50 or higher.
