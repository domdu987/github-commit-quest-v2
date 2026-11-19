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

## Re-review (v3)
Compared again with film 16's board. All three stills are sharp, with no DOF and no text in the frame (the board captions sit outside the stills, as on film 16). The warm workshop shade is accepted as an indoor exception, like film 16's chamber.

### sb1_workshop: APPROVED
| density | light/colour | composition | materials | hero (H1) | match refs |
|---|---|---|---|---|---|
| 7 | 8 | 6 | 7 | 7 | 7 |

The look is right: a honey/terracotta room, a readable window shaft, warm practicals, and H1 balls and bars that now read as polished brass. Must-fix in the full build:
1. H1 frame and inner gears are still pale cream wood. Make them brass, like the balls.
2. Black gear-tooth slivers remain on the upper wall gear and inside H1. Find the bad faces (duplicate or overlapping geometry) and fix them.
3. Blue objects are still there: the blue-grey bars on the wall above H1 and the blue bracket inside H1. Make them iron-grey or brass.
4. The bottom 35% is still bare boards with a few big pale "C" shavings. The tool chest, offcut basket and half-built clock case listed in v2 are not visible. Bring them into frame. Tint the floor shavings honey and make them smaller.
5. The octagonal stump bottom-right is a crude low-poly block. Give it bark/grain and more sides, or replace it.

### sb2_ship: FIX-FIRST (sea only)
| density | light/colour | composition | materials | hero (sea) | match refs |
|---|---|---|---|---|---|
| 7 | 7 | 6 | 6 | 5 | 6 |

Big progress: the deck, cannons, mast, sail shadows, white clouds with violet undersides, and the far sea (layered swells, one glitter path near the horizon) are all right. The look-level problem is the near water, the largest element on the right half. The wake along the hull is a motion-blur-like texture of vertical white streaks on saturated cyan (about RGB 90/165/215). It reads as noise and speed blur, not as smooth layered water with foam. There is no curling bow wave silhouette. This is the client's main dislike, so it needs one more ship render before the build.
1. Near water: shift it toward deep teal (#0d5a6a to #1f7f8f) and lower the saturation. The cyan should only show in crest backlight.
2. Wake: replace the streak texture with 2-3 smooth, coherent foam bands that follow the hull (a lacy edge, soft-edged white, broad calm water between them). Add a readable white bow-wave roll at the stem and a turquoise underside on the wave pushed away from the hull.
3. Keep the far sea and glitter exactly as they are.
Must-fix in the build (not blocking): the bulwark is a row of flat black boxes. Add a cap rail, plank seams and a warmer, slightly lighter black (#2a2622). Give the sails a slight billow (they are still flat planes). Add a sky gradient (deeper blue at the top, warmer near the horizon) to match film 16.

### sb3_hall: APPROVED
| density | light/colour | composition | materials | hero (telescope/globes) | match refs |
|---|---|---|---|---|---|
| 7 | 7 | 6 | 7 | 8 | 7 |

The crimson walls, gilt chandelier with candles, brass telescope, globes, Greenwich dome view and warm sconces give the right period look. Must-fix in the full build:
1. The carpet and chair seats are still saturated royal blue and fight the crimson. Take them to a greyer navy (about #2c3558) and give the seats crimson or green upholstery.
2. The carpet medallion is a plain set of concentric rings that fills the bottom 30%. Add the border pattern, corner motifs and finer field ornament, and reduce the floor to about 25% of the frame.
3. The Moon picture still reads as a blue disc with holes. Use a soft grey painted Moon on a dark ground.
4. The left side is thin (only the telescope). Add the bookcase and quadrant from v2, which are not visible here, and more warm practicals left.

### Overall
Workshop and hall: look agreed, so build them. Ship: one more sea-only render. The fix is the near-hull wake and the near-water colour. Nothing else on the ship changes.

## Re-review (v6 ship)
### sb2_ship (v6 hero, from the sea): APPROVED
| density | light/colour | composition | materials | hero (sea) | match refs |
|---|---|---|---|---|---|
| 7 | 7 | 6 | 7 | 6 | 7 |

The look is now agreed. The open sea is what the client asked for: smooth, layered swells, no edge-to-edge speckle, glitter only in one path, and no streak or motion-blur texture. The ship has a strong period silhouette: three masts, billowing seamed canvas, ratlines, pennants, ochre strakes and gun ports. The white clouds with violet undersides, the deeper sky top, the gulls and the headland finish the frame. It is sharp, with no DOF. What remains is element-level work, not look-level work.

Must-fix in the full set build:
1. **Bow wave.** It is too big and too solid: about 9-10 m tall at a 42 m hull, and it reads as an iceberg or a sculpted ribbon, which also hides the stem and figurehead. Cut its height to about a third and make it a curling white roll at the stem. Break the lit face with lacy foam, and keep the turquoise only in a thin translucent band under the lip.
2. **Wake and foam field.** The foam right of and below the hull (y 740-800) is chunky, flat white blotches. Make it finer, lacier lines that follow the hull, with calm water between them. Make the V-wake behind the stern readable.
3. **Near sea.** Shift the bottom 45 % toward deep teal (#0d5a6a) with a near-to-far gradient. Calm the wobbly sky-reflection squiggles. Give the empty lower half something to read: a swell crest with a thin foam line, or frame the ship lower and larger.
4. **Headland.** It is a row of flat green triangles. Round it and add haze.
5. **Sails** are slightly pink-white. Warm them back to #e8dcc0 on the lit side.
6. **Character shots on deck** need closer cameras (mid shots at the rail, wheel and quarterdeck), using the v3 deck detail plus the bulwark cap-rail fix.
7. The board caption for the ship overlaps the hall caption. Shorten it.

### sb2_ship_v5_bow: open sea usable for the deck presets, with conditions
The far and mid sea are good and can serve as the background for the deck presets: layered swells, one glitter path to the horizon, and small crisp whitecaps. Not usable:
- The near-hull foam is a chain of white spheres with cyan rims. Replace it with the v6 bow sheet and foam bands, or keep it out of frame.
- The white ghost blob at the lower right (about x 460-720, y 1000-1150) is an artifact. Remove it.
- The clouds are the old faceted lilac stacks. Use the v6 metaball clouds.

### Overall
All three looks are approved: workshop, hall and ship. Build the full set with the must-fix lists above. Bow wave and wake come first on the ship.
