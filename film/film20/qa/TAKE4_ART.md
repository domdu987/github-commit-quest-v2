# QA-art: TAKE gate round 4, film 20 key takes (2026-11-20, Opus)

**Inputs**
- Takes: v3/film20/{s03,s15,s18,s21,s24,s27}, each with take.mkv (rebuilt from the parts where split), meta.json, QA.md and QA_AUTO.md.
- Rules and references: shot_plan.md with the §I table, QA_TEAM.md (client taste, QA-art, §G, §H, §I), and the ref_shorts sheets and README.
- My earlier reviews: TAKE3_ART.md and TAKE2_ART.md.

**Frames**
- Pulled at 2 fps, at full size (720x1280) and at 360x640.
- Saved in /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeart4/<take>/{full,ph}/.
- Labelled phone rows are in <take>_phone.jpg.
- Extra strips:
  - s03_start.jpg: g 170-206, every 4th frame.
  - s24_b.jpg: the window crossing.
  - s24_c.jpg: the bite, g 1804-1858.
  - s27_a.jpg: the start, full size.
- Frame numbers are global g.

**Scores** are 1-10:
- set: set richness
- light: light and colour
- comp: composition and phone legibility
- act: acting
- key: the key moment
- cam: camera travel / BIGZOOM
- chan: would a viewer take it for the same channel as the reference Shorts?

| take | set | light | comp | act | key | cam | chan | verdict |
|---|---|---|---|---|---|---|---|---|
| s03 BIGZOOM 1 + crane | 7 | 7 | 6 | 7 | 7 | 7 | 7 | **PASS** |
| s15 FALSE PAYOFF (flags re-render) | 8 | 8 | 8 | 8 | 8 | 7 | 8 | **PASS** |
| s18 REVEAL dusk -> wire -> hut | 7 | 8 | 7 | 7 | 7 | 8 | 8 | **PASS** |
| s21 REVEAL 2 rings -> aha | 7 | 7 | 7 | 7 | 7 | 8 | 7 | **FIX** (2 changes) |
| s24 BIGZOOM 2 (rebuilt restaurant) | 5 | 6 | 5 | 4 | 4 | 7 | 5 | **FIX** (3 changes) |
| s27 ENDING (table dressing re-render) | 8 | 8 | 8 | 7 | 8 | 8 | 8 | **PASS** |

---

## s03: BIGZOOM 1 + crane (g 170-411): PASS

**Round-3 items:**
- **F1 start: PARTLY FIXED. I accept it.**
  - Improved: the start now has sky (the top ~25 %), the block rows of Paris, two rising legs and the lamp at the table. Most of
    the small black scatter is gone.
  - Still weak: there is no Seine, and the horizon carries a peach band. The far part of the zoom is fast: 330 D to 39 D in about
    18 frames, and much of it sits inside the dissolve. The extreme wide therefore reads as a quick flash and is not held.
  - The move is still one continuous, readable "city -> man" zoom, so it meets the intent of §H.
- **F2 plan table: FIXED.** The top is light wood with a blueprint sheet on it (g 215-260). It reads as plans, not as a black
  keyboard.
- **§G:** clean on every 0.5 s tile.
  - The lamp pole stands beside Eiffel, never across him.
  - The landing medium (g 275-305) is full-body, with the point-up and a contact shadow.
  - The crane past the riveters into deep blue is on-channel.

**Optional (if the take is touched again):** hold the far wide about 6 frames longer after the dissolve, and cool the peach
horizon band toward blue.

## s15: FALSE PAYOFF (g 988-1096): PASS (unchanged)
- This is a re-render for the French flags only. The small pennants are now vertical blue-white-red tricolours, and nothing else
  changed.
- The document is in a hand, the banner reads, the worried swap with the sweat drop reads at phone size, and the tower stays
  behind Eiffel.
- The round-3 PASS stands.

## s18: REVEAL dusk -> summit -> wire -> hut (g 1210-1434): PASS

**Round-3 items:**
- **F1 inside the hut: FIXED.**
  - The telegraphist is fully in the left third with both shoulders and his headphones in frame (g 1390-1434).
  - The key and the blue spark sit between him and the window, and the dusk tower shows through the window.
  - The desk is still bright warm yellow under the lamp, but it now reads as lit wood. I accept it.
- **F2 the group at the foot: FIXED.**
  - The jagged ring prop is gone.
  - The officer, the two demolition men and Old Eiffel all stand full-body on the avenue with shadows. The wagon and horse are
    behind them.
- **§G:** clean.

**Optional:** the rope coils read as flat brown discs, like stumps (g 1225-1300), and the ground is still about 35 %. Neither
blocks.

## s21: REVEAL 2 night rings -> swoop -> aha (g 1427-1663): FIX

**Round-3 items:**
- **F1 group phase: FIXED.**
  - The landing is a medium on a lit cobbled forecourt, with heads at about 85-105 px at 720 wide.
  - The bar drop (g 1607-1620), the officer's salute (g 1622-1652), the cheer and Old Eiffel's proud swap all read on the phone
    sheet.
  - The tower and the lit hut are behind the group. This is now a good payoff frame.
- **F2 rings and wire: NOT FIXED.**
  - The rings are still hard, opaque white lines. A thick white arc crosses the top of the frame on g 1472, 1487, 1502, 1517 and
    1532, and a second arc crosses the bottom on g 1502.
  - The wire is a thick white slash at g 1427, and again a full-height white bar down the right third at g 1532-1550.
  - On a phone these still read as scratches on the picture, not as radio signal.
- **F3 glow: PARTLY FIXED.** At g 1532-1547 the upper lattice is covered by a pale, milky translucent column. It reads more as a
  ghost or glass tube than as glowing iron. It is visible, which is the main thing, but it is not pretty.

**Fixes:**
1. **Rings (g 1468-1573).**
   - Turn the rings from white tubes into an emissive blue-white (hue ~200) with soft falloff, at about one third of the current
     thickness.
   - Fade the alpha to zero as each ring expands, so that no ring is ever a solid white line at the frame edge.
   - No ring may cross the frame at more than 40 % opacity.
2. **Wire and glow (g 1427-1440 and g 1528-1560).**
   - Thin the wire to 2-3 px at 720 wide, keeping it blue-white, not pure white.
   - For "เสาอากาศยักษ์", replace the milky cone with an emission pulse on the lattice edges themselves: blue-white rim on the red
     iron, 0.3 s up and 0.5 s decay.
   - The tower must stay red-orange iron with a blue edge, not a white column.

## s24: BIGZOOM 2 (g 1724-1858): FIX

**Round-2 items:**
- **F1 dressed room: PARTLY FIXED.**
  - Done: other tables with cloths, blue chairs, chandeliers and a gilt lattice frieze.
  - Not done: at the landing (g 1790-1858) the camera looks DOWN from high with the 22 mm lens at 1.8 m. The ceiling and wall
    bands fill the top 45 % as flat orange-red planes that fold into an "X" behind his head, and a blank white table fills the
    bottom 35 %.
  - The result is a warped, bandy room, not a Belle Époque restaurant, and it is the weakest landing of the two BIGZOOMs.
- **F2 window findable: PARTLY FIXED.**
  - The RESTAURANT sign and the awning whip past nicely at g 1774-1782. The facade crossing is short, so F4 is FIXED.
  - At the extreme-wide start (g 1724-1750) no warm window can be found. The eye has no target until about 1.5 s in.
- **F3 first bite: NOT FIXED.** Through g 1804-1858 the fork stays beside his shoulder and never reaches his mouth. The plate
  shows only yellow discs. "กินข้าวบนหอ" (g 1817) has no picture.

**Fixes:**
1. **Landing framing (g 1790-1858).**
   - Land at eye level with the preset tower_window_in look (55 mm at about 5 m, or tilt up about 12° and drop the camera to his
     eye height).
   - The background behind him should be the room: diners' tables, the chandelier and the gilt mirror. No bands folding into an X.
   - Keep the table at no more than 25 % of the frame.
   - Reuse the s27 table dressing (fruit bowl, bottle, candles, bread) so that his table is laden.
2. **The bite (g 1810-1830).**
   - Raise the fork with a visible chunk of food to his mouth, keyed on g 1817, with a 2-3 frame cheek-bulge chew.
   - Use the s27 fork-cycle rig (plate -> mouth), but slower and bigger: the fork head at about 20 px at 360 wide.
3. **Start target (g 1724-1755).** Make the restaurant window plus the red awning the brightest warm spot on the first platform
   (emission up), so that a warm dot is findable from the first frame.
   - The current start also carries a peach band at the horizon. Push the sky toward clear blue there.

## s27: ENDING pull-out (g 1964-2045): PASS (unchanged verdict)
- The table dressing reads well: fruit bowl, bottle, candles, bread and glasses. He eats with his eyes shut, smug, and the fork
  reaches past the bowl.
- The crash through the RESTAURANT window to the whole tower over the fair, with tricolours, still lands well.
- The thin black vertical line under the FG chair (g 1964-1977) is still there. It is optional, and conform may paint it out.
- The flat wall bands behind him are on screen for only about 0.4 s, which is acceptable here.

## Cross-take
- **Colour:** on brand in all six takes, with red-orange iron against deep blue and warm practicals. The peach horizon band
  appears only at the s03 and s24 starts, and it does not cover the whole frame.
- **§G (every 0.5 s tile):** all six takes are clean. No floating, no slicing and no half-bodies at the edge. The s21 group-phase
  left man touches the edge at g 1577 but is not cut.
- **Re-submit:**
  - s21 can pass on a phone sheet plus contact sheet check once the rings and wire are soft blue.
  - s24 needs a new take at this gate, with phone and contact sheets.
