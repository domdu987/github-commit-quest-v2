# QA-art: TAKE gate round 3, film 20 key takes (2026-11-20, Opus)

Inputs: v3/film20/{s03,s09,s15,s18,s21,s27} take.mkv (rebuilt from the parts where split), meta.json, QA.md, QA_AUTO.md. Also
shot_plan.md with the §I table, QA_TEAM.md (client taste, QA-art, Stricter C, §G, §H, §I), the ref_shorts sheets and README, and my
round-2 notes TAKE2_ART.md. For the s09 match I also read the s06 tail.

Frames were pulled at 2 fps, at full size (720x1280) and at 360x640. They are in
/tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeart3/<take>/{full,ph}/, with
labelled phone rows in <take>_phone.jpg. I also extracted s27 start frames at 10 fps (s27_six.jpg) and made match.jpg, which puts the
s06 end (g 586/603) next to the s09 start (g 603/604/610). Frame numbers are global g.

Scores are 1-10:
- set: set richness
- light: light and colour
- comp: composition and phone legibility
- act: acting
- key: the key moment
- cam: camera travel / BIGZOOM
- chan: would a viewer take it for the same channel as the reference Shorts?

| take | set | light | comp | act | key | cam | chan | verdict |
|---|---|---|---|---|---|---|---|---|
| s03 BIGZOOM 1 + crane | 6 | 7 | 5 | 7 | 6 | 7 | 6 | **FIX** (2 changes) |
| s09 vow (match from s06) | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **FIX** (the join; the take itself is good) |
| s15 FALSE PAYOFF | 8 | 8 | 8 | 8 | 8 | 7 | 8 | **PASS** |
| s18 REVEAL dusk -> wire -> hut | 7 | 8 | 5 | 6 | 7 | 8 | 7 | **FIX** (2 changes) |
| s21 REVEAL 2 rings -> aha | 7 | 7 | 4 | 6 | 5 | 8 | 6 | **FIX** (3 changes) |
| s27 ENDING pull-out | 8 | 8 | 8 | 7 | 8 | 8 | 8 | **PASS** |

---

## s03: BIGZOOM 1 + crane (g 170-411): FIX

**Round-2 items:**
- **F1 start extreme wide: PARTLY FIXED.** The start is now high and far. The Trocadéro, the block rows and the four rising legs on
  their piers are in frame, and the warm lamp at the table is a findable dot. However, there is no sky and no Seine, and
  about 60 % of the frame (g 170-215) is bare orange dirt. The dirt is littered with dozens of tiny near-black scatter props, which
  read on a phone as holes or debris rather than as a busy yard.
- **F2 black pole and crane cable: FIXED.** No dark line crosses the frame or Eiffel.
- **F3 landing set: PARTLY FIXED.**
  - Fixed: the pier now has brick, a ladder, barrels, a lamp and riveters standing full-body, and the floating riveter is gone.
  - Not fixed: the plan table at g 250-275 is still a black slab with saturated blue bars across the bottom ~30 %. It reads as a
    keyboard or grille, not as plans.
- **F4 half-body on the exit: FIXED.** Eiffel exits cleanly.

**What works:** the landing medium on Eiffel (g 275-305) is good. He is proud, points up with his hand on his hip, and has a
contact shadow. The crane up the leg against deep blue, with riveters on the timber platforms (g 365-395), is on-channel.

**Fixes:**
1. **Start (g 170-215).** Pitch the start camera up about 8-10° so that a band of sky, the skyline and the Seine take the top
   20-25 %. Remove or hide the small dark scatter props more than about 15 m from the table, or replace them with a few large readable
   ones (girder stacks, carts, a forge with smoke). The ground should read as a work yard, not as a littered floor.
2. **Plan table (g 245-280).** Kill the black-and-blue slab. Either make the table top a light wood board with a cream sheet of
   plans, or keep it out of the bottom of the frame by aiming about 3° higher on the landing. Nothing black or saturated blue may sit
   in the bottom 30 %.

## s09: Maupassant's vow (g 600-760): FIX (the join only)

**The take itself is good:**
- The red-and-gold café is rich, and the tower stub reads through the window.
- The rise, the cravat tug and the folded arms read clearly.
- The lip-sync (mouth open g 690-735, flat during the rise) reads.
- The push-in on "สักครั้ง" lands at about 30 % head height, which is fine as punctuation.

**Problems:**
1. **The MATCH join from s06 is a visible jump cut.** Compare s06 g 603 with s09 g 603/604 (match.jpg):
   - s06 actually ends on a WIDER, higher frame: chandelier, ceiling, Maupassant small and SEATED with a wine glass raised, and
     black smoke in the window.
   - s09 starts much closer: no chandelier, no smoke, and Maupassant in a standing crouch with no glass.
   - The cause is in s06. Its meta.json `end_cam` lists the new pose (2.618, 9.596, 1.334), but its take.mkv and QA.md still show
     the old pose (3.533, 6.506, 0.983), so the s06 tail was never re-rendered.
2. **The seat slices his body (g 600-612).** The banquette seat edge passes in front of his coat and hip. He reads as sliced by the
   seat rather than sitting on it (§G).

**Fixes:**
1. Re-render the s06 tail (g ~572-607) to the agreed end_cam, which is the same as s09's start_cam. Make the props and state at g 603
   identical on both sides: either both seated with the wine glass, or both in the crouch without it, and the same smoke value in the
   window (s06 is at 1.0; s09 has it keyed to 0).
2. In s09 g 600-612, seat him properly on the banquette, so his hips are on the cushion with the seat edge below his knees. The
   alternative is to start him standing a step in front of it. The seat edge must not cross his coat.

## s15: FALSE PAYOFF (g 988-1096): PASS

**Round-2 items:**
- **F1 document in hand: FIXED.** The official holds it out on an arm, and Eiffel holds it at his chest through the snap.
- **F2 official half-cut: FIXED.** He stays fully in frame and steps back in depth.
- **F3 tower behind Eiffel: FIXED.** The legs, the first platform and the EXPOSITION UNIVERSELLE 1889 banner stay behind him
  through the payoff.

The worried swap and the sweat drop on the snap read clearly at phone size. The crowd, the tricolours, the raking sun and the
red-orange against deep blue all look like the channel.

**Optional note:** the bottom edge of the FG back card is visible as a horizontal cut at y ≈ 1180 on g 988-1003. That is mostly
under the DIS 13, but a 2-3° lower tilt or a longer card would remove it. It does not block.

## s18: REVEAL dusk -> summit -> wire -> hut (g 1210-1434): FIX

**Round-2 items:**
- **F1 dead ground: PARTLY FIXED.** The start is closer and the wagon, figures and lit hut are in frame. The ground is still ~35 %
  of the frame at g 1210-1240.
  - New problem: a jagged dark-brown ring-shaped prop (a scrap pile or barrel stack) stands in front of the officer and two
    demolition men at g 1255-1300. It cuts them off at the waist and reads as broken geometry (§G "sliced by slabs").
- **F2 window crossing: FIXED.** No batten fills the frame, and the crossing is quick.
- **F3 inside: PARTLY FIXED.**
  - Fixed: the spark is now a blue arc between the brass balls.
  - Partly fixed: the hand is near the key, but the key is small.
  - Not fixed: the telegraphist is cut in half by the LEFT frame edge for the whole interior (g 1390-1434). He is the subject of
    the beat, and this is a §G blocking item. The desk is also blown out to a hot yellow, and the room is still flat orange.

**What works:** the dusk tower, the crane to the summit, the whip down the wires to the lit hut and the push to the hut window are
the best reveal travel in the film.

**Fixes:**
1. **Inside the hut (g 1395-1434).** Offset the final push about 0.6 D to the left, or yaw it about 10°, so the telegraphist sits
   fully in the left third, with his head around x 200-250 and both shoulders in frame. The key and the blue spark should sit between
   him and the window. Pull the desk exposure down so the top is light wood, not glowing yellow.
2. **The group at the foot (g 1250-1300).** Remove the brown ring-shaped prop in front of the group, or move it to the side, so that
   everyone stands full-body on the ground with contact shadows. If there is time, put the scrap cart or crowbars in the near ground
   to break up the bottom 30 %.

## s21: REVEAL 2 night rings -> swoop -> aha (g 1427-1663): FIX

**What works:**
- The rise up the lit lattice to the summit and the view down over lit night Paris (g 1442-1517) are beautiful and very R5.
- The swoop down the tower face to the foot is smooth and readable.

**Problems:**
1. **The aha does not read on a phone (g 1577-1655).**
   - The five characters are tiny: about 23-30 px heads at 360 px wide, in a band at y 0.55-0.65.
   - The bottom ~40 % is an empty dark-blue ground slab, right where the captions sit.
   - The bar drop, the salute and Old Eiffel's proud swap are the payoff of the whole film, and they cannot be seen.
2. **The rings and wire read as white scratches, not signal.** They are flat, opaque white tubes. In the group phase two ring arcs
   and the diagonal wire slash across the sky over the tower, which is the round-2 "bars across the frame" problem again. At g 1472
   and g 1532 a thick white ring bar crosses the top of the frame.
3. **"เสาอากาศยักษ์" (g 1530) shows no glow.** The lattice stays brown-orange, so the line has no picture.

**Fixes:**
1. **Group phase (g 1580-1655).** Land the swoop about 40 % closer and lower, at roughly 9 D from the group, so the heads are about
   90-120 px at 720 wide. Keep the ground at no more than 25 % and the tower top in the upper third behind them. Keep the snap on
   "ขาดไม่ได้".
2. **Rings and wire.** Make the rings an emissive blue-white (hue ~200) with soft falloff: thinner, with alpha fading as they
   expand. Fade them out, or let them rise out of frame, before the swoop lands (by g 1575). In the group phase dim the wire to a
   thin line, or hide it behind the tower.
3. **Glow (g 1528-1545).** Pulse a blue-white emission along the lattice edges and the wire (strength ×3, 0.3 s up, 0.5 s decay), so
   the "giant antenna" beat is visible on a phone.

## s27: ENDING pull-out (g 1964-2045): PASS

**Round-2 items:**
- **F1 fg post: FIXED.** It is hidden.
- **F2 restaurant: FIXED.** It is now a dressed room: chandeliers, a round cloth table, glasses, plates and a bentwood chair in the
  FG. Maupassant eats with his eyes shut and smug, with a fork cycle.
- **F3 flags: FIXED.** They are vertical blue-white-red tricolours.
- **F4 window findable: PARTLY FIXED.** The RESTAURANT sign and the lit window carry him to about g 2000, after which the tower is the
  picture. That is accepted for the last image.

The pull-out from his window through the lattice to the whole tower over the fair is clean and on-channel, and it lands still on the
hard cut.

**Optional note:** a thin black vertical line runs from the FG chair down the floor at g 1964-1977. I accept it, but conform may
paint it out. The QA_AUTO blur flag is a content flag (flat interior against the detailed lattice), so I waive it.

## Cross-take
- Colour is on brand in all six takes: red-orange iron against deep blue or violet, with warm practicals.
- **§G re-check (every 0.5 s tile):**
  - s18: the telegraphist is half-cut, and the group is cut off at the waist by the brown prop.
  - s09: the seat slices through his coat at the start.
  - s21: white ring and wire bars cross the frame in the group phase.
  - s03, s15 and s27 are clean. s15 has only the optional card-edge note.
- **Re-submit:**
  - s03, s18 and s21 can pass on a phone sheet plus contact sheet check once the fixes are visible.
  - s09 passes once s06's tail is re-rendered and a cross-join strip (s06 g 595-603 + s09 g 604-612) shows no jump.

## s16: Maupassant laughs and jeers in the café, with the finished tower in the window (g 1093-1220): FIX

Frames: 2 fps from g 1093 (f00 = g 1093, f01 = 1108 ... f08 = 1213, f09 = 1228 handle), in
.../scratchpad/takeart3/s16/{full,ph}/, with s16_phone.jpg, pair1.png (g 1138 / 1183), pair2.png (g 1198 / 1213) and
thumb.jpg (g 1136-1146, every 2nd frame).

| set | light | comp | act | key | cam | chan | verdict |
|---|---|---|---|---|---|---|---|
| 6 | 7 | 6 | 6 | 5 | 7 | 7 | **FIX** (3 changes) |

**What works:**
- The crash pull-out from the grin to the medium-wide is a strong, on-channel move. It goes in one continuous camera with no cut.
- The red banquette, gold studs, chandelier, sconce and blue-white tiles against a clear blue sky give the room a strong colour. The
  red-and-blue contrast matches the refs.
- The full tower with its lit rings reads in the window at phone size from g 1108 to 1198.
- The laugh reads clearly: squeezed eyes, tears and the bounce.
- He has contact shadows and his feet are on the tiles. No §G slicing is visible.
- The lip-sync mouth opens on the quote (g 1183-1213) and is closed in the grin before it.
- The close-up head is about 30-34 % of the frame height, which is under the 35 % limit.

**Problems:**
1. **He points the wrong way (g 1136-1213).** The "thumb at the tower" arm points to SCREEN-LEFT, at the empty curtain and wall,
   while the tower is behind his screen-RIGHT shoulder. He keeps the same arm pointing left through the jeer. On a phone it reads
   as him pointing at something off-screen, so the mockery loses its target. This is the key acting beat of the shot.
2. **The tower is hidden on the punchline (g 1205-1220).** The push-in for "เป็นเศษเหล็ก!" ends with his head covering the tower.
   Only the spire tip shows above his hair at g 1213. In the medium-wide (g 1123-1168), the right curtain also clips the tower's right
   leg. The false payoff needs the man and the tower side by side at the moment he calls it scrap.
3. **The floor is bare and blown out (g 1115-1170).** The bottom 30-35 % of the frame is empty tiles with a blown-white,
   amoeba-shaped sun patch that reads as a white hole on the phone sheet. The "café" has no table, glass or patron in frame (the
   ambience promises artists), so the set is thinner than s09's. There is also a small stray green stick poking in at the right edge
   of the window (g 1108-1183).

**Fixes:**
1. **Make the gesture point at the tower.** Mirror the pointing arm so the thumb jabs back over his screen-right shoulder toward the
   tower, without him looking. Keep it from g 1136 through the jeer. If mirroring the cut-out is hard, slide the tower in the window
   view to screen-left of him instead.
2. **Frame the punchline (g 1195-1220).** End the push about 0.3 D to the left, or truck it left, so his head sits in the left
   half and the whole tower, rings included, stands clear beside his head in the right third. In the medium-wide, centre the window
   view about 1 m further left so the curtain does not clip the tower's leg.
3. **Dress and expose the floor.** Bring the sun patch down to a warm cream (no clipped white). Add a café table in the near FG with
   a cloth, a glass and a chair, plus one or two seated patrons on the banquette (or dim figures at the frame edge) to fill the bottom
   30 %. Remove the green stick at the window edge.

## s16 rev2 (commit fa9f44b): PASS

Frames: 2 fps from g 1093, at full size and 360x640, in .../scratchpad/takeart3/s16r2/{full,ph}/, with s16r2_phone.jpg and pair.png
(g 1138 / 1198).

| set | light | comp | act | key | cam | chan | verdict |
|---|---|---|---|---|---|---|---|
| 7 | 8 | 7 | 8 | 8 | 7 | 8 | **PASS** |

**My three fixes:**
- **F1 gesture: FIXED.** From about g 1153 through the jeer, his arm jabs back over his screen-right shoulder at the tower, and he
  does not look at it. The mockery has its target on the phone sheet.
- **F2 punchline: FIXED.** At g 1198-1213 his head is in the left half, and the whole tower with its lit rings stands clear in the
  right third. On the phone this is the false-payoff image: man versus tower, side by side.
- **F3 floor and set: FIXED (accepted with a deviation).**
  - The floor is about 18 % of the frame.
  - The painter (red beret) and the composer laugh behind him, which fills the room and doubles the mockery.
  - The window junk is gone.
  - The grade now has a rich red, blue and gold palette.
  - I accept the director's reason for having no patrons at the FG table.

**Non-blocking notes (conform or the next pass, if time allows):**
- The banquette seat edge, a red bar, crosses both artists' coats at the waist with their legs dangling in front of the seat face
  (g 1108-1183). They read as standing behind the seat rather than sitting on it. It is minor because they are background players,
  but it is the same seat-slice as in s09.
- The FG marble table at the left edge is a bare grey disc. A glass catching the light would sell it more.
- A small blown-white floor glint remains at the bottom-left at g 1123-1153. The right curtain still clips the tower's leg in the
  mid-orbit, which is fine because the tower is clear on the punchline.
- In the close-up the composer is half off the right edge (g 1198-1220). This is accepted as part of the punch-in.
