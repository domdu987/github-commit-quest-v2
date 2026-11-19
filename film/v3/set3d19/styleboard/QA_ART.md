# QA-art: set3d19 style board (Harrison / longitude)

Compared with: film 16 board and contact sheet, film-1 bible sheets (office, beach, light presets).
All three stills are sharp with no DOF, and none has text. Each still has a working idea. None reaches the film-16 bar yet, mostly because large areas of the frames look empty or unfinished.

## sb1_workshop: FIX-FIRST
| density | light/colour | composition | materials | hero (H1) | match refs |
|---|---|---|---|---|---|
| 6 | 6 | 5 | 5 | 4 | 5 |

The warm room, beams, window shaft and wall gears work. Problems:
- The H1 reads as pale wood, not brass. Its gears show black notch artefacts, and pure-blue rods float behind and beside it. On a phone it looks like a crate of gears with wooden balls.
- The bottom 40% is bare floorboards with big white chunky "C" shavings and two white lumps (sawdust?). This looks like debris, not life.
- The shade hue is 282 (OUT) and the whole room leans mauve/purple.

Fixes:
1. **H1 to brass.** Frame posts, gear wheels and the 4 balls get a metallic brass material (base #cb9f48, metallic 1, roughness 0.3, small dark-brown occlusion tint in the crevices). The two balance bars become dark polished brass rods. Delete the 4 saturated-blue bar objects at the wall and bench (around x 540-640, y 420-470 and 630). Fix the black gear-tooth slivers: they look like z-fighting or flipped normals, so recalculate normals and add a 1 mm offset.
2. **Light the hero.** Add a small warm area light (2700 K, about 30 W, 0.3 m) above-front of H1 so the brass glints. Let the window shaft hit the H1 rather than the floor in front of the bench: rotate the sun about 8 degrees.
3. **Shavings.** Replace all white C-shapes with thin honey (#d9a85a) curled ribbons, 3x smaller and 5x more of them (about 200), clustered under and around the bench and lathe. Delete the white blobs and the sawdust discs.
4. **Fill the lower frame.** At y 950-1280 add a low workbench end or tool chest with open drawers, a basket of wood offcuts and a leaning half-built clock case frame. Put the dark foreground silhouettes at the frame edges, not in the centre-bottom.
5. **Grade.** Move the shade to 245-255 with a cooler fill on floor and walls only. Push the candle and lamp warmer, and add 2-3 more practicals (a lantern on the wall left, a candle on a shelf) so the room stays warm.
6. Add a wall shelf of jars, tins and clock parts to the left wall above the lathe. The left side reads empty behind the cards.

## sb2_ship: FIX-FIRST
| density | light/colour | composition | materials | hero (sea) | match refs |
|---|---|---|---|---|---|
| 5 | 6 | 5 | 4 | 4 | 4 |

The noon light, real cast shadows and deck perspective are good. Problems:
- The sea is the main failure. It is a saturated electric blue (#0080ff-like) covered edge to edge in white glitter speckle. That is the "noisy" look the client rejects. There is no layering (dark near, teal mid, haze far), no readable foam lines and no wake.
- The island is a flat dark-blue sliver.
- The sails are flat untextured cards and look like paper, and the clouds are lilac blobs.
- The bottom third is empty deck, and the gold sphere bottom-left is unreadable.

Fixes:
1. **Sea colour and layers.** Desaturate the sea and darken it toward deep navy-teal near the ship (#0b3f5c). Set the mid band to teal #1f7f8f and the horizon band to #8fb3c8 with real haze. Keep the turquoise only on crest backsides.
2. **Glitter.** Confine the sun glitter to ONE narrow path under the sun, about 15% of the sea width. Fade it to zero elsewhere, raise the glint threshold so there are fewer, crisper points, and remove the speckle across the whole sea.
3. **Foam and wake.** Add long thin curving foam streaks aligned with the wave direction (smooth, 2-4 px at the horizon, growing toward the camera). Add a white bow wave and a V-wake on both sides of the bow, visible past the bulwark.
4. **Sails.** Give each sail a curved, billowing mesh (simple deform bend about 0.4 m), an off-white canvas colour (#e8dcc0) with seam stripes, and warm sun on the lit side. Add the main mast, its sails and more shrouds in the upper frame so the sky is full of rigging.
5. **Foreground.** Replace the gold blob with a clear binnacle: a wooden pedestal with a brass hood. Add coiled rope, a bucket and a lantern on the deck at y 1000-1280, plus a second cannon row along the right rail.
6. **Island and sky.** Make the island a green-headed headland with a pale beach line and soft haze. Make the clouds white with blue-violet undersides, like film 16, not lilac.

## sb3_hall: FIX-FIRST
| density | light/colour | composition | materials | hero (telescope/globes) | match refs |
|---|---|---|---|---|---|
| 5 | 6 | 5 | 5 | 6 | 5 |

The crimson walls, arched window, sun shaft and globes read well. Problems:
- The bottom 35% is a flat navy rug with three plain crimson rectangles. They look like placeholders.
- The telescope is pale wood, not brass, and the chandelier is grey-white.
- The "Moon" plate reads as a perforated disc. The view outside the window is flat green.
- Film 16's chamber had a full room of furniture behind the subject. This hall has one table edge.

Fixes:
1. **Rug.** Replace the plain rug and its 3 rectangles with a patterned Georgian carpet: a navy field with a crimson-and-gold border, a central medallion and corner motifs, made as a procedural texture. Move the camera about 0.4 m lower and 1 m forward so the floor takes at most 25% of the frame.
2. **Telescope.** Make the tube brass (metallic, #cb9f48) with dark lacquer bands and lens rings. The chandelier gets gilt arms (#c9a24a) and warm flame emission, and add 6 more lit candles.
3. **Fill the room.** Put the Board table in the mid-ground with chairs on both sides, an orrery and globe on it, and a second bookcase on the left wall. Hang a wall map (no text) between the pilasters right, plus a quadrant or sextant on a stand left.
4. **Moon plate.** Replace it with a framed painted Moon picture (soft grey craters inside a gilt oval frame) or a large framed star chart.
5. **Window view.** Show Greenwich: trees, a domed observatory roof and a soft sky gradient, with a little haze.
6. Add warm practicals on the tables, side to side. The left candelabra and the right one now read small. The frame needs about 4 more glowing points to match film 16's warmth.

## Overall: FIX-FIRST
The structure is sound in all three stills. The problems are the materials (brass that reads as wood, flat sails), empty lower thirds, and above all the water. The sea is exactly the noisy, over-saturated look the client has rejected before. Re-render after the fixes and resubmit the board. The ship still is the priority.
