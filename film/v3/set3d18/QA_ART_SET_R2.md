# QA-art (strict), SET gate round 2: film 18 set3d18 + cast18

Reviewer: QA-art (opus). What I looked at: every `set_work/final/s01..s26.png` at full size (720x1280), with crops of s16 (holes), s19 (breaches and herd), s21 (horizon band) and s02 (fg prop); `contact_small.jpg` (phone-scale legibility); the round-1 tiles in `final_r1/`; the head rows in `final/sNN.json`; and the updated cast `cast18/tmp/sec_ox_a.png`, `sec_ox_b.png` and `sec_poses.png`. I checked them against `film18/shot_plan.md`, the builder's "Round 2 fixes" and "Could not meet" sections in `API.md`, and the client rules in `QA_TEAM.md`.
Rule used in this round: a BLOCK means the beat cannot play even after a render team stages the actors well. Anything a render team can fix inside its own shot (marks, card choice, flame state, framing, hiding a prop) is MINOR, and each one is an instruction to that team below.

## Verdict: PASS. Render now, with the per-shot instructions at the end.

All 17 round-1 BLOCKs are cleared. Each of those beats now plays in frame:
- s02: the herd fills the lane.
- s05: the stall is close.
- s06: the oxen are in front of the gates.
- s07: the count payoff is a sea of oxen (188 cards).
- s09, s10, s14, s15: the general is reversed, with the camp behind him and his face out of the caption band.
- s11: the fire circle is clear.
- s16: holes and diggers are visible.
- s17: no early fire.
- s19: dark breaches.
- s20: the herd is big beside the lens.
- s21: the monster wall charges the camera.
- s22: the hero ox is at about 35 % of the frame, next to a frozen soldier.
- s23: the drummers are visible and nothing is blown out.
- s26: the general is about 380 px tall, with his cup and askew helmet, oxen behind and a warm dawn wall.

Several shots still have take-level faults, mostly in the reveal block s19-s22 and in s24. The render teams must fix these. Instructions 1-4 are mandatory before the key-shot TAKE gate.

## Per shot (mid state t = 0.5)

| shot | verdict | note |
|---|---|---|
| s01 | OK | Hook reads: Tian Dan tugs the dragon coat over an ox, a row of dressed oxen along the wall, lantern pools on blue shade. |
| s02 | MINOR | The herd now reads in the lane, coming at the camera. At mid t about 8 oxen are readable, because the column hides itself behind the first ones. Bottom 35 % is bare pink ground. The fg "dressing" is a pale faceted block with three sticks (x 440-620, y 700-900) that reads as a stump or bone, not hay or rope. |
| s03 | MINOR | Pennant beat reads. The vista is still weak art: salmon-brick towns, patchwork floor, translucent flat Qi flag with bloom. The top-left cloud has a flat base bar that sticks out past the puffs like a skewer. |
| s04 | MINOR | The push to Jimo reads. Ju is not visibly lit. The orange flag is a flat plane. |
| s05 | MINOR | The stall, the old man and the woman read large. Tian Dan is hidden behind the shelf props: only his black cap shows at x 290-390, y 590-640. The sash hand-over cannot read until he is moved. The slatted shelf items alias into stripes. The top 40 % is empty sky. |
| s06 | MINOR | Plain oxen in front of the houses, Tian Dan walking. About 6 of the 10 are readable. The old man is behind an ox. The plain oxen wear horn blades, but blades are tied only later (s02 and s17 time). |
| s07 | OK | Count payoff lands: the yard and pens are packed, with the snap to the quarter. Pen cards at the bottom lean a little, which is acceptable at count scale. |
| s08 | MINOR | Reads. A saturated red slab is still beside the general's head (x 370-720, y 490-580). There is a cut beam at top-left (x 0-50, y 95-180). The cloud is skewered by its base bar. |
| s09 | OK | QUOTE 1a reads: arms wide, the camp and laughing soldiers behind, fire right. The skewered-cloud bars are the only flaw. |
| s10 | OK | QUOTE 1b medium. Head 545-720 is safe, the camp is behind him, and he is lit warm. |
| s11 | MINOR | Fire circle and mock-moo soldiers read (heads 560-654). The bottom 40 % is bare ground. All 4 near soldiers use the same pose. |
| s12 | MINOR | The envoy bowing on the bridge now reads. The wall-walk folk are about 25 px and mostly hidden by the parapet. The gate crack is behind the cart wheel. The envoy's plain banner is not visible. |
| s13 | MINOR | Still the best tile. The cut dark box at the top-right (x 660-720, y 290-350) is still there. |
| s14 | OK | Cup raised, laughing soldiers, tents, the Jimo wall and the moon behind. The false payoff reads. |
| s15 | MINOR | Reads. The fg dark-rimmed jar shapes (bottom 20 %) are heavy and read as boulders. |
| s16 | MINOR | Diggers with picks and baskets in front of ragged breaches. "Digging through the wall" reads at full size. On the phone sheet the breaches read as grey rubble rather than openings, and the warm glow inside is not visible. |
| s17 | MINOR | Oxen with reed tails at the holes, townsfolk, no early flame. The oxen stand parallel to the wall, not nose-first into the holes. The old man covers two of them. The fg "reed bundle" reads as a slatted wooden screen. There is a cut dark object at the right edge (x 700-720, y 790-930). |
| s18 | OK | Tian Dan raises the torch at centre, the line of oxen behind with the first tails lit. |
| s19 | MINOR | The oxen run out along the wall base past the dark breaches; the herd reads. Faults: (a) the `dust` / `hglow` puffs at the left breaches render as dark translucent squares with blurry dots (x 0-110, y 630-700); (b) no tail flames are visible on any ox; (c) the Qi soldiers (y +5..+7) are on the inner side and not visible; (d) the bottom 40 % is still flat abstract planes (streaky blue moat, grey-green slab). |
| s20 | MINOR | Strong: big oxen charging beside the lens, warm glow behind. The tail flames are behind the oxen and out of frame, so "tails streaming sparks" does not read. The furrows read as painted road lanes. |
| s21 | MINOR | The monster wall reads: a dense herd coming at the lens, blades up, Jimo dimmed. The 3 freezing soldiers exist only at t = 0. By t 0.5 the camera has pushed past them (no head rows at t 0.5 or 1), so "jaws drop, cups fall" is lost for most of the shot. No tail flames are visible. A flat purple band with stair-stepped edges sits behind the herd (y 560-600). |
| s22 | MINOR | Frozen soldier (sweat drop, O mouth) plus the hero ox reads. The ox head is cut by the right frame edge (muzzle at x 720). No tail flame is visible. The ox is the old side-body card. |
| s23 | OK | Old men, women and kids beat pots on the wall walk with sound rings. No blow-out, caption band clean. |
| s24 | MINOR | Folded tents and a camp in disarray read at wide. On the phone sheet the comic rout does not read: soldiers are about 25-35 px, the 2 flying items are specks in the sky, and the chariot is a speck far away. The top 40 % is empty sky. |
| s25 | MINOR | The Qi banners' return reads (orange over black). Same weak vista art as s03 and s04. |
| s26 | MINOR | The ending reads: the general runs with cup and askew helmet, dragon oxen behind, warm dawn wall. The same pale stump-with-sticks prop sits in the road (x 430-650, y 800-980) and reads as a white glove or hand. No smoke on the ox tails. The general's card faces screen-right (sideways run) and not toward the lens or down the road. |

No BLOCK shots.

## Scores (1-10)

| area | R1 | R2 | why |
|---|---|---|---|
| Density | 5 | 7 | The camp, wall, yard and herd tiles are full. Bare-ground bottoms remain in s02, s06, s11 and s16-s17, s24 has an empty sky, and the vista is thin. |
| Light and colour | 5 | 7 | No halo rings, the sun is behind the camera at dusk, the night is warm on blue, s23 is clean and the s26 dawn is warm. The vista is still a flat orange gradient with bloom on Jimo. |
| Composition | 3 | 7 | Subjects are readable in 24/26 tiles and no faces are in the band. Remaining: s05 (Tian Dan hidden), s22 (head cut), s24 (tiny rout). |
| Period | 5 | 5 | Not touched: the brick/plank rammed earth, pagoda-style towers (s21, s23), panelled tents and salmon-brick vista towns. They do not block a beat, but they stay below set3d10. |
| Key moments | 3 | 7 | Hook 8, count 8, false payoff 8, reveal 6 (no tail flames on screen, soldiers gone in s21, dust squares in s19), ending 7. |
| **Set overall** | **4** | **7** | |

**Cast: 8 / 10 (round 1: 8).**
- **Fixed:**
  - Horn blades are now about half a head long with red bindings and read as short blades.
  - The front-3/4 dragon ox exists in stand, walk, startled and gallop 8 (flame 0/1/2). It reads clearly as an ox charging toward the camera.
  - The plain ox can be used without blades.
  - The Qi runner is a capped dark silhouette (no Yan band).
  - The general has run, jaw-drop, toast and carve poses. The townsfolk have dig, carry and beat poses.
- **Still weak:**
  - The silk "dragon" is the same yellow cartoon head with antennae, now at mid-flank. In the side and 3/4 views at 60-90 px it still reads as a second little creature face (a fish or snail) looking forward on the ox's back. It is less of a problem in the front-3/4, where the ox head covers half of it.
  - The blade body is gold rather than the bronze `#8a6a3a` I asked for.
- Neither blocks; see instruction 12.

## Per-shot instructions for the render teams (numbered; 1-4 mandatory before the key-shot TAKE gate)

1. **Re-bake the ox cards from the updated cast before any herd shot.** Delete `set_work/cards/*_ox.*` and run `jimo_cards.py`, then confirm the new short blades and the front-3/4 view in the take frames. For s21, s22 and s26, use `front_3/4` gallop/startled cards for every ox within about 15 D of the lens.
2. **Tail flames visible in every lit-tail shot (s18 after "จุดไฟ", s19, s20, s21, s22, s26 smoke only).** At least one tail flame must be on screen at all times in each of these shots, and in s20 and s21 at least 3.
   - Use flame variants 1/2 on all lit oxen, with the sparks trail.
   - s20: yaw the 2 nearest oxen 10-15 deg more toward the camera so their flaming tails show behind the body.
   - s22: the hero ox's flame tail must be inside the frame (top-left of the ox, as in `dragon front_3/4 startled (lit)`).
   - s26: thin grey smoke wisps on the oxen's tails, no flame.
3. **s21 soldiers in frame for the whole shot.** Move the 3 `soldier_freeze` silhouettes ahead with the camera, so they stay 3-6 D in front of the lens at t 0, 0.5 and 1 (fg left and right thirds, heads above y 880).
   - Option A: marks at y about -40..-44.
   - Option B: stop the push at y -52.
   - The herd passes between and beside them. Add one falling cup (prop) from the right soldier on "สัตว์ประหลาด".
4. **s19 dust and the field.**
   - Hide the `dust*` / `hglow*` objects that render as dark translucent squares. Replace them with light-brown puff cards, or drop them.
   - Show 4-6 Qi silhouettes (`qi_run`) on the outside of the wall, behind the last oxen.
   - Raise the look_at so the flat moat and slab take at most 25 % of the frame, or put a dark fg reed clump or bridge post in the lower left.
5. **s02:**
   - Widen the herd lane spread (width 6 to about 10 D) and stagger it so 15+ oxen are readable at t 1 of the pull-out.
   - Replace the pale stump-with-sticks prop with rope coils, hay or a basket, or hide it.
   - Put 1-2 dark props (basket, silk scraps) in the bottom 30 %.
6. **s05:**
   - Move Tian Dan in front of the counter or into its open end, so his face and hands are clear between the old man and the woman. The sash hand-over happens across the counter, in front of the shelves.
   - Tilt the camera down about 5 deg so sky is no more than 30 %.
   - Hide or thin the striped shelf items behind him.
7. **s06:**
   - Use `plain` oxen with no blades.
   - Bring the 10 oxen into a looser double row so at least 8 are readable on "สิบตัว".
   - Move the old man out from behind the centre ox.
8. **s17:**
   - Turn the 4 nearest oxen 60-90 deg so they stand nose-first toward the breaches.
   - Move the old man 1.5 D toward the lens and to screen-right so he does not cover them.
   - Show one townsperson tying a reed bundle to a tail.
   - Replace the fg slatted screen with a real reed bundle (tied yellow reeds) at 15 % scale, laid low.
   - Hide the cut object at the right edge.
9. **s22:**
   - Slide the camera or the ox mark 0.6-0.8 D so the whole ox head and both blades are inside the frame, with at least 30 px margin.
   - Keep the soldier separate from the ox.
   - Use a front-3/4 startled card with the flame tail visible.
10. **s24:**
    - Re-mark 6-8 fleeing and falling soldiers (`flee`, `fall_bottom`) 10-20 D from the lens so they are at least 70 px tall.
    - Arc 3-4 flying pots and helmets through y 300-700 at 2-3x their current scale.
    - Bring the empty chariot into the middle ground (20-30 D).
    - Tilt down so the sky is at most 30 %.
11. **s26:**
    - Remove the pale stump-with-sticks prop from the road.
    - Use the `general_run` card yawed so he runs toward the lens and down the road, with the oxen behind him on the same line.
    - Keep his head top at 700 or above it on screen.
12. **Cast follow-up (cast team, can run in parallel):**
    - Push the silk dragon from a face to a body: a long gold serpentine body with a small head drawn in profile and no big eye or open mouth, so it stops reading as a second creature at 60 px.
    - Give the blades a bronze body `#8a6a3a` with a bright edge line.
13. **Small set touch-ups, applied in the takes that show them:**
    - Shorten the cloud base bars to the width of the puffs (s03, s05, s08, s09, s11).
    - s08: tone the red slab to `#8a2a20` and hide the cut beam at top-left.
    - s13: hide the cut box at top-right.
    - s15: scale the fg jars to 70 % and move them to the frame corners.
    - s11: add a fg rope or jar to the bottom-right and give the 4 soldiers 2-3 different poses (`mock_moo`, `laugh_point`).
    - s12: walk folk into the crenel gaps at full height, the plain banner visible on the envoy, and the gate crack glow left of the wheel.
    - s16: brighten the breach interior glow (warm 2x) so the openings read on the phone sheet.
    - s21: hide the stair-stepped purple band or darken it into the night ground.
14. **Vista s03, s04, s25 (non-blocking, do it if time allows):**
    - Opaque cloth Qi flag with a small halo and no bloom.
    - A visibly lit Ju in s04.
    - Ochre earth towns in place of salmon brick.
15. **Period (next set pass, not a render gate):**
    - Tamped-earth courses in place of brick/plank tiling.
    - Plain hip-roof towers with no pagoda finial (s21, s23).
    - Plain canvas tents.
