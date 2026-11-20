# QA-art (strict), SET gate: film 18 set3d18 + cast18

Reviewer: QA-art (opus). What I looked at, all at full size (720x1280): every `set_work/final/s01..s26.png`, `contact_small.jpg`, the cast sheets `cast18/tmp/sec_poses / sec_ox_a / sec_ox_b / sec_faces / sec_cycles.png`, compared with the client-approved finish level in `set3d10/contact_small.jpg`. I checked them against `film18/shot_plan.md`, `API.md` (marks, cameras), `set_work/hue_rows.txt` and the head rows in `set_work/final/sNN.json` (t = 0 / 0.5 / 1), and against my own style-board review `board/QA_ART.md`.
Placeholder cards stand in for the actors. A shot is judged on whether it can carry its planned beat once the real actors are in, in the frame as composed. Cards are 3D objects in the scene, so a card that is hidden in the set will also hide the actor.

## Verdict: FAIL (17 BLOCK shots, listed at the end)

The night palette is a real step up from the board: blue moon-shade, ochre pools round the fires, real layered flames, readable stars and clouds. s13 (the camp party) is at the set3d10 level. The cast is good and on model. But in 17 of the 26 shots the beat cannot play as framed:
- The subject is hidden by set pieces or by marks: the s07 herd, the s11 soldiers, the s16 holes and diggers, the s22 ox, the s23 townsfolk.
- Marks are behind the camera or inside closed courtyards: s06 herd, s07 herd_far, s21 soldiers.
- The herd cards are edge-on to the camera: s19, s21.
- Faces sit in the caption band: s10, s15.
- The frame is empty: s02, s20, s26. The shots that look into the sun at dusk are empty too: s05, s09, s10, s11.
- A fire blows out the frame: s23.

All four of the client's key-moment groups are hit: count s07, false payoff s14-15, reveal s19-22, ending s26. Render teams must not start until the BLOCK fixes are in and the 17 tiles are re-rendered and re-checked.

## Per shot (mid state t = 0.5)

| shot | verdict | note |
|---|---|---|
| s01 | MINOR | Hook reads: lantern-lit yard, Tian Dan card next to a dressed ox under the wall, warm pools on blue shade, caption band is calm ground. The 6 "dressed ox" marks run in a column straight away from the lens (x -4..-6.7, y 14.6 -> -1.2), so only the first ox reads and the "row along the wall" is hidden behind it. The black jar plus torch stand at right (x 560-720, y 780-1100) is a heavy black blob. Fix in take: spread the ox marks along the wall in x (x -16..+8, y 6-8), shrink or drop the jar. |
| s02 | BLOCK | The reveal is "dozens of dressed oxen filling the lane", but the 34 herd marks start at x 29.8 to 44, 58-72 D from the lens, and nothing reads in the vanishing point (checked full size). The lane shows only Tian Dan, one ox, jars and racks. The bottom 45 % is bare pink ground (caption band bright, 21 k px). |
| s03 | MINOR | The pennant beat reads (black flags over many walled towns). Far terrain is "confetti": rotated overlapping quads in clashing pinks and greens (bottom 30 %), and the terrain rim/edge shows at y ~490-560. The top 40 % is an empty orange gradient. Jimo's Qi flag is a semi-transparent glowing plane with a bloom blob. Towns are salmon brick. |
| s04 | MINOR | The push to Jimo reads. The same giant translucent flag plus bloom sits at frame centre. Ju (the second lit town) is not visible / not lit in frame. Same confetti terrain under the camp tents (caption band). |
| s05 | BLOCK | Tian Dan, 3 townsfolk and the child are not readable: the stall is small at 17 D. The camera looks into the dusk sun: 60 % flat sky with a sun-halo ring artefact (curved rainbow arc y 200-400), backlit stalls. The fg "counter" reads as a strange face-like frame with two lit slits. |
| s06 | BLOCK | "สิบตัว: ten oxen" cannot show: the 10 herd marks are at y 28.6-28.8, inside the courtyards behind the house walls (gates at y 23), and no ox is visible. The townsfolk mark (89, 17) is at the lens (feet y 1432). The top 50 % is empty sky and the bottom 35 % bare ground. |
| s07 | BLOCK | Broken, confirmed. The camera is low (z ~8) facing the wall and gate tower. Pen fences fill the foreground and ~15 grey box-oxen are visible instead of "the whole quarter packed". The 90 herd_far marks (y 60-78) are behind the camera at t = 0.5 (camera y ~62, looking -y). A diagonal sun shaft cuts the right third. The count payoff does not land. |
| s08 | MINOR | The beat reads: Jimo wall behind, spear rack fg, general on the rampart. The soldier card at (1.5, -48) at frame right reads as a dark horned shape (like an ox head), which is confusing in this shot. A flat saturated red slab (x 360-720, y 540-600) sits on the far wall top. Fix in take: move that soldier to x +4 / off the right edge, tone the red slab to `#8a2a20`. |
| s09 | BLOCK | QUOTE 1a. Backlit into the dusk sun, 55 % flat sky plus halo-ring artefact. A tall fg brazier (x 400-650, y 700-1080) stands touching the general, the same size as him, so "arms wide" will collide with it. Background: one tent, a table; no camp. |
| s10 | BLOCK | QUOTE 1b. The general's face sits in the caption band: head top 868 / chin 1057 at t 0.5, and 948 / 1217 at t 1 (s10.json). 70 % of the frame is empty sky. Backlit. Caption band brightest of the set (30 k bright px). |
| s11 | BLOCK | Nickname beat: two big drums at frame centre hide the whole fire circle. All 7 cards (heads y 650-690) are behind them, and no soldier is visible. Sun glare plus halo ring top-left. |
| s12 | MINOR | Reads: gate crack glow, bridge, cart-wheel fg, dark calm caption band. The envoy is ~105 px and half behind the bridge rail. The wall-walk townsfolk (heads y 330-476) are hidden by the tower and parapet. Wall still salmon/pink under the lamps. Fix in take: envoy mark to (0, -26) in front of the rail, walk marks into the crenel gaps. |
| s13 | OK | Best tile, at set3d10 level: tents, fires in stone rings, braziers, racks, drums, crates, cups, road to the hills, warm pools on blue. Note: the dark object cut at top right (x 660-720, y 140-350) should go. |
| s14 | BLOCK | False payoff: medium on the general is fine (head 726/806), but behind him there is only an empty dark plain and sky (60 %). The camera looks -y out of the back of the camp, so none of the party (tents, fires, crowd) is behind him and the "celebration" does not read. |
| s15 | BLOCK | QUOTE 2b. The general's face is in the caption band: head 829 / chin 1008 at t 0.5, 859 / 1071 at t 1. 70 % empty sky. Same empty background as s14. |
| s16 | BLOCK | No hole and no digger is visible (checked crop). The camera grazes along the wall face, so the holes are foreshortened to nothing, and the 6 diggers stand in a line straight ahead behind a brazier and a ladder. "รูหลายสิบรู" cannot read. |
| s17 | BLOCK | The fg reed bundle is a 310 x 470 px pale cylinder, and a brazier flame sits exactly on its top, so it reads as a burning tail bundle one shot BEFORE "จุดไฟ". The black jar fills the right 25 %. The oxen at the holes are readable but small (heads y 670-726). |
| s18 | MINOR | Reads: Tian Dan centre, oxen line along the wall, braziers. A brazier flame sits exactly on top of Tian Dan's head (a crown of fire) where his torch goes up; the holes do not read behind the earth heaps. Fix in take: Tian Dan mark to (-7.4, 12.2) or the brazier 2 D along x. |
| s19 | BLOCK | Reveal opener: the breaches on the outer face read as pale stone plugs/pillars, not dark holes with fire glow behind (checked crop at h12). The ox cards are near side-on. The lower 40 % is abstract flat planes: a bright streaky water slab, a purple slab, and pixel-noise grass. |
| s20 | BLOCK | Flat empty night field confirmed: the bottom 50 % is one blue-grey plane with large blocky shadow shapes. The herd is a single row at mid distance, so "tracking beside the herd" has no ox near the lens. 97 % blue, no warm light from the tails reaches the ground. |
| s21 | BLOCK | The 3 soldier marks (y -47..-52) are behind the camera (camera y -43.5 -> -27.6, looking +y), so no jaws drop. The 60 herd cards travel toward the camera with yaw = direction of travel (side view), so they render edge-on as thin red slabs with horn slivers. The background is the brightly lit Jimo gate and bridge, not "out of the dark". |
| s22 | BLOCK | The ONE ox in full flare is completely hidden behind the soldier card (only a horn sliver shows, checked crop). The bridge rail crosses the lower half. The action is on the Jimo bridge, not at the camp. |
| s23 | BLOCK | Confirmed: a fire bowl 2-3 D from the lens (lower left) blows out ~250 x 300 px down into the caption band (6.3 k bright px). The fg torch flame adds a second hot spot. No townsfolk are visible: from y -4.5 the outer parapet blocks hide the walk (checked crop). The tower reads as a Japanese pagoda. |
| s24 | MINOR | The rout reads at wide (folding tents, chariot, fires). The flying pots/helmets are 2 tiny specks. Fleeing soldiers are barely visible. Two edge-on pennant poles read as gallows/signposts (centre right, x 380-600). The caption band holds a lit tent roof (17 k bright px). Fix in take: flying items x2 scale arcing through y 300-700, pennants turned 45 deg to the camera. |
| s25 | MINOR | The Qi return reads (orange/red flags vs black). Same confetti terrain, world rim at y ~560, Jimo bloom blob; blue "shark-fin" tent shadows read as shards at bottom left. |
| s26 | BLOCK | Ending: the general is ~55 px tall (head 658, feet 714), and the oxen ~35 px. Helmet askew, cup, oxen behind cannot read on a phone (about 25 px). The bottom 45 % is bare road. The dawn sky is washed near-white at the top, and the wall still sits in night-blue shade. |

## Scores (1-10)

| area | score | why |
|---|---|---|
| Density | 5 | s13 and s24 are dense and match set3d10. s02, s05, s06, s09, s10, s14, s15, s20 and s26 are mostly empty sky or bare ground. Set3d10 fills every tile edge to edge. |
| Light and colour | 5 | Night is right: shade hue 220-245, warm pools, real flames, magenta <= 3.5 %. Dusk camp and market shots look into the sun (halo-ring artefact, flat backlit cards). s23 is blown out. The vista has bloom blobs. The s26 dawn sky is washed out. |
| Composition | 3 | Subjects are hidden or off frame in 9 shots, faces are in the caption band in 2, there are many 55-70 % empty skies, and fg props cover the subject (s09, s11, s17). |
| Period | 5 | The rammed earth still reads as tiled brick/planks, the towns are salmon brick, the s23 tower and the s07 two-storey hall read as Japanese/Ming, and the tents read as panelled boxes. Better than the board (no paper lanterns, plain banners, stone-ring fires). |
| Key moments | 3 | Hook s01-02: 5 (s01 fine, s02 no herd). Count s07: 2. False payoff s13-15: 4 (s13 great, s14-15 empty, faces in band). Reveal s19-22: 2 (holes, cards edge-on, soldiers behind camera, hero ox hidden). Ending s26: 3. |
| **Set overall** | **4** | |

## Cast (cast18): 8 / 10

- On model with the approved series puppet look: clean line, big readable heads, 15 expressions per character, cycles 8-step. The general reads instantly (gold helmet, moustache, red-black lamellar), and the run cycle carries the cup and tilted helmet for s26. Soldiers a/b/c read as three different men; townsfolk and envoy are distinct; the poses cover every planned beat (tug cloth, tie blade, raise torch, accept sash, mock-moo, asleep, freeze, fall on bottom, flee, beat pot, dig, bow).
- **Does the ox read as an ox at phone size?** Yes. I tested it scaled to 40 / 60 / 90 px tall (the herd and s21 sizes on a 360x640 phone): the brown head with pale muzzle, ears and curved horn, the four hoofed legs and the tail fire read as an ox in a red blanket. Two problems:
  1. The gold dragon's head on the silk sits right behind the ox head. At 40-60 px it reads as a second head.
  2. The "3/4" views are still side-on bodies with the head turned. There is no front-3/4 / head-on view for the charge toward the camera (s21, s22, s26), which is why the s21 cards go edge-on.
- **Are the horn blades too big?** Yes. Each blade (gold with red bindings) is about as long as the whole head, about 1.1-1.2 D against the 0.5 D brief. At phone size horn plus blade makes one tall spike: unicorn/narwhal, or a paintbrush/quill rather than a short bronze blade. Fix: scale the blade to 50-55 % of its length, keep it angled forward, and give it a bronze body `#8a6a3a` with a bright edge line (now it is a rounded gold leaf).
- Minor: the qi_soldier silhouette wears the Yan red headband and crest, so Qi men read as Yan. Drop the red band and use a plain dark cap.

## BLOCK fixes (minimal, concrete). Re-render these tiles and re-check head rows, hue rows and caption band after them.

1. **s02 herd fills the lane.** Re-mark the herd: `herd(34, (-15, 10.5), (40, 10.5), width=6)` so the nearest ox is 6-8 D from the lens and they recede into the vanishing point. Add near-ground dressing in the bottom 30 % (dropped silk scraps, rope coils, hay, a basket) so the pink ground is broken up.
2. **s05 market lane.**
   - Camera start (-68.5, 17.0, 2.6) -> (-77, 22.5, 3.2), lens 24, so the stall front fills 50-60 % of the width and Tian Dan plus the townsfolk are 300-400 px tall.
   - Remove the sun-halo ring from the DUSK sky (the circular arc, also in s09, s10, s11).
   - Re-shape or replace the fg counter so it has no two lit slits.
3. **s06 oxen in the lane.** Herd marks from y 28.7 to the lane y 13-19 in front of the three gates (x 60-92). Move the townsfolk mark (89, 17) to (86, 19).
4. **s07 count payoff.**
   - Camera high and looking down over the yard: start (0, 46, 20) -> (0, 14, 0), end (0, 72, 32) -> (0, 14, 0), lens 20. Keep the snap.
   - Herd 120 spread over the yard x -45..45, y 13-27 and into the pens y 31-41.
   - herd_far 90 moved in front of the camera: ring lane y 5-12 plus the east quarter x 50-95.
   - Target >= 150 oxen visible at t 0.5. Remove the sun shaft.
5. **s09 / s10 / s14 / s15: reverse the general's coverage.**
   - Put the camera on the far side of the general, looking +y toward the camp and Jimo, with the table as fg: s09/s14 camera about (-8, -102, 2.8) -> general.
   - Background must show tents, fires and (s14-15) the party crowd. Sun behind or beside the camera (>= 90 deg off the view axis).
   - s09: move the fg brazier >= 3 D from the general.
   - s10 and s15: camera z 3.0-3.2, look_at z 3.0, so the head top <= 600 and chin <= 820 for the whole move, sky <= 35 %.
6. **s11 nickname.** Move the drum pair out of the view axis (behind the fire or x +10). Camera (-1, -73, 2.6) -> (5.5, -86, 2.2), lens 22, so the fire circle and all 7 cards read (heads >= 70 px). Fg jar stays left.
7. **s16 holes open.** Pull the camera off the wall: start (50, 16, 2.6) -> (30, 4, 2.2), lens 22, slide -x. The breaches read as a row of dark openings and the diggers stand side-on in front of them. Remove the brazier from the lane between lens and diggers.
8. **s17 no early fire.** Fg reeds to 60 % size, laid low (bottom-left, y > 980), not upright; no flame may align with them. Drop or shrink the right fg jar to <= 12 % of frame width.
9. **s19 holes and field.**
   - Breach interiors dark earth with a warm glow from inside (the lit tails) and dust puffs; no pale plug faces visible at h12.
   - Ox cards at 3/4 toward the camera.
   - Replace the streaky bright water slab and pixel-noise grass with the board_1 moat and a darker, low-contrast field texture (stubble rows, ruts).
10. **s20 field and herd.**
    - Dress the field: furrows/stubble, scattered hay, stones, a ditch, torch stakes.
    - Re-mark the herd 3-20 D beside and ahead of the lens so 3-5 oxen are large in frame.
    - Let the flame-card lights pool warm on the ground. Target blue+violet <= 85 %.
11. **s21 monsters out of the dark.**
    - Camera start (0, -58, 2.2) -> (0, -8, 4), end (0, -46, 3.0), so the 3 soldiers are fg silhouettes (back-3/4) between the lens and the palisade gap.
    - Herd cards use the 3/4 view yawed 30-45 deg off the camera axis, never edge-on.
    - Dim the Jimo wall/gate lamps to 0.3 for s21/s22 so the herd comes out of darkness.
12. **s22 hero ox.**
    - Ox at (1, -42) in the palisade gap, 3/4 toward camera, 35-45 % of frame height. Soldier fg left at (-4.5, -48), back-3/4, not overlapping the ox.
    - Camera (-2, -52, 1.6) -> (1, -42, 2.0), lens 26. No bridge rail in frame.
13. **s23 wall-top drummers.**
    - Camera above the walk centre: start (-31, 0.6, 21.5) -> (-2, 0.6, 16.5), so the townsfolk line reads along the walk.
    - Remove every fire bowl within 6 D of the lens; fg torch flame at 0.5 scale, kept above y 500.
    - Caption band bright pixels < 2 k.
14. **s26 ending.**
    - Camera start (2.5, -84, 1.5) -> (0.5, -70, 2.6), lens 24, so the general is ~350-420 px tall with head top <= 700. Oxen marks at y -62..-56 behind him.
    - Road dressing in the bottom 40 % (ruts, a dropped helmet plume, pots, cart wheel, torch stakes).
    - Dawn sky top value <= 0.85, and a warm low key on the wall (no night-blue).
15. **Cast:**
    - Horn blades to 50-55 % length with a bronze body `#8a6a3a`.
    - Add a front-3/4 dragon ox (stand / gallop 8 / startled) for s21, s22 and s26.
    - Move the silk dragon's head back to mid-flank so it does not read as a second ox head.

## Non-blocking fixes (apply in the takes or the next set pass)

- Vista s03/s04/s25:
  - Replace the confetti quads with an aligned field grid in 3-4 close greens/ochres at lower contrast.
  - Hide the terrain rim with haze/hills.
  - Make the Jimo/Qi flag an opaque cloth with a small warm halo, not a translucent plane plus bloom.
  - Light Ju visibly in s04.
  - Towns from salmon brick to ochre earth.
  - Add a few cartoon clouds to the empty DUSK sky (like set3d10).
- s01: ox marks along the wall in x; smaller fg jar.
- s08: move the horned-looking soldier card; tone down the red slab.
- s12: envoy in front of the bridge rail; walk marks in the crenel gaps.
- s13: remove the cut object at top right.
- s18: move Tian Dan off the brazier flame line.
- s24: bigger flying props, pennants turned, darker tent roof in the caption band.
- Period, all wall shots:
  - Break the brick/plank tiling of the rammed earth into wider tamped courses with stains.
  - s23/s07 towers: straighter eaves, no pagoda finial.
  - Tents: canvas without the square-panel grid.
- qi_soldier: drop the red Yan headband.
