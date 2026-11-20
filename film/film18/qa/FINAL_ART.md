# FINAL QA-art: film 18 "ไอ้เสมียนวัว" (oxclerk_v1.mp4)

- Reviewer: QA-art (opus), FINAL gate, 2026-11-20.
- Source: `scratchpad/rel18/oxclerk_v1.mp4`, the version written at 19:59:50 UTC (md5 5ef865d4…).
- The file was re-rendered while this review was running. I compared all 141 half-second frames of the old and new versions. Only the burned-in captions differ (y 820-930); the picture is identical. Every finding below holds for the current file.
- Sheets (in this folder):
  - `final_sheet_2fps.jpg`: full-res 720x1280 tiles, 2 fps, 141 tiles, labelled with time and shot.
  - `final_phone.jpg`: 360x640 tiles every 0.5 s. Cyan lines mark the caption band at y 880/950.
  - `side_by_side_film2.jpg`: 1 fps, 270x480 tiles. Each film-18 row sits directly above the film-2 row for the same seconds.
- Timecodes are film time. g = frame number at 30 fps.

## Verdict: **FIX-FIRST** (4 blockers, all local re-renders or re-framings of one shot each)

| # | Shot | Time / frames | Blocker (rule) | Fix |
|---|---|---|---|---|
| B1 | s06 | 16.65-17.70 s, g500-530 (up to the whip at g531) | **Half-cut main character** (§G, team rule 4). Tian Dan's head and body are clipped by the LEFT frame edge for about 1 s. His cap, about 25-35 % of his face and the left half of his robe are out of frame. On the phone this reads as a broken frame right on "สิบตัว". | Re-render the tail of s06 with the lateral slide reduced, or with Tian Dan's start position about 120 px further right, so his whole head stays at least 40 px inside the edge until g531. The whip into s07 can stay. |
| B2 | s08 | about 21.4-22.4 s, g640-673 | **Pole through a face** (§G). The laughing Yan soldier who walks in behind the foreground spear rack (left third) has the spear shafts running vertically through his face. This is visible on the 21.5 s and 22.0 s phone tiles. | Move that soldier right of the general, or behind the palisade, or drop him from s08. The rack must never sit in front of a head. |
| B3 | s16 | about 42.3-43.1 s, g1268-1292 | **Face in the caption band** (§G, y 880-950). The little girl (red top, hair buns) walks down-frame. Her face sits at y 850-915 and the captions "ถูกเจาะเป็น" and "รูหลายสิบรู" cover part of it. This is clear on the 42.5 s and 43.0 s tiles. | Keep her deeper in the set (face at y ≤ 840) or route her out of the frame before g1265. Alternatively, raise the caption for these two phrases only. Re-framing is preferred. |
| B4 | s21 | 53.20-56.08 s, g1596-1683 (whole shot) | **Ghost artefact plus soft/DOF look plus untextured block** (§G). (a) The foreground row of pots and the reed bundle across the bottom 22 % of the frame renders semi-transparent: the pot bodies and handles show through each other with a soft orange glow ("x-ray pots"). On the phone this reads as a glitch, not a prop. (b) From about g1655 the "dropped cup" is a featureless beige polyhedron falling through the caption band (lower right, about 55.2-56.0 s). A second beige block is held above the right soldier's head. (c) The shot's saturation is 0.37, far below the per-shot target of 0.48, and the sky is slate grey-mauve. That breaks the s21/s22 night palette (see Continuity). | Re-render s21 with an opaque, lit, textured foreground (the same jar and reed props as s19/s20, with outline shading and no glow/emission), or drop the foreground row and keep a dark ground strip at 25 % or less. Use the bronze cup asset (the general's cup) for the dropped and raised cups. Grade s21 to s22's blue night (sky about RGB 77/79/124 with the moon visible, sat ≥ 0.48). |

Nothing else blocks. The non-blocking notes are listed further down.

## Story: per-beat read on the phone sheet

| # | Beat | Where | Reads on phone? | Notes |
|---|---|---|---|---|
| 1 | Hook: a man dressing oxen in red dragon silk and tying blades to the horns | s01, 0.0-5.2 s | **Yes** | A lit yard full of red dragon-coated oxen from 1.0 s. Tian Dan is at medium from 3.0 s, one hand on the horn, with bladed horns clearly visible at 3.5-5.0 s. The 即墨 sign helps. The strangeness reads in the first second. |
| 2 | A city that won't fall | s03-s04, 5.2-12.8 s | **Yes, weaker** | Many walled towns at dusk, pennants rising, and a push-in to the near town, which stays warm-lit and carries its own bright banner. At phone size the Yan pennants read dark-maroon/red with red rim light, not black, so they are close to Qi red. "Holds out" comes mostly from the push-in and the narration (note N1). |
| 3 | The clerk made general | s05, 12.8-15.3 s | **Yes** | At the clerk's stall the elders hand Tian Dan the red sash. The cheering townsfolk read clearly. |
| 4 | He collects 1000+ oxen | s06-s07, 15.3-19.9 s | **Yes** | Oxen are led house to house, then the whole quarter is packed with plain oxen (18.5-19.5 s). This is a strong payoff. B1 sits inside this beat. |
| 5 | The Yan general mocks "a city that fights with cows" | s08-s11, 19.9-31.4 s | **Yes** | The general laughs on the rampart, then delivers both quotes at medium with arms wide and thumb to chest. Soldiers make horns with their fingers in s11. B2 sits in s08. |
| 6 | A false surrender and the Yan camp party | s12-s15, 31.4-40.2 s | **Yes** | An envoy with a white banner on the bridge and elders on the wall. Then the night party in the camp with cheering and cups, and the general toasting under the moon. |
| 7 | Holes dug in the wall at night | s16, 40.2-43.6 s | **Yes** | Townsfolk with picks, and holes opening along the lit wall base. B3 sits here. |
| 8 | Reed bundles tied to the tails, then lit | s17-s18, 43.6-47.6 s | **Yes** | The elder ties a reed bundle to a dragon ox at a hole. At 47.5 s the tails light (flame cards at the tail tips) with Tian Dan's torch. In s18 Tian Dan is small (about 10 % of frame height), but the ignition reads. |
| 9 | The fire oxen burst out and charge | s19-s20, 47.6-53.2 s | **Yes** | Oxen burst out of the holes in the wall, then a side-tracking ox runs with its fire trailing behind it. Only one ox is visible in s20, so "herd" is carried by s19 and s21 (note N5). |
| 10 | The Yan camp's terror and comic rout | s21-s24, 53.2-62.8 s | **Yes** | A wall of glowing dragon oxen looms over black Yan silhouettes (s21). The ox hero shot follows (s22), then the elders banging pots (s23), then soldiers scattering with cups flying (s24). B4 sits in s21. |
| 11 | Qi retakes 70 towns | s25, 62.8-65.3 s | **Yes** | At dawn, bright red banners pop up over the dark ones across the plain. |
| 12 | Ending: the general runs home chased by cows, cup in hand | s26, 65.3-70.4 s | **Yes** | BIGZOOM down to the general running on the road, smoking dragon oxen behind, cup in hand and helmet askew. Clear and funny. |

## Hard rules (§G), checked on all 141 phone tiles and confirmed at full res

| Rule | Result | Timecodes |
|---|---|---|
| Nothing floats | Pass, with a note | Note N2: during BIGZOOM B, 66.3-66.5 s (g1988-1994), a torch stand overlaps the tiny general's legs and he reads as perched on the torch. There is no contact shadow while the crane is high. Transit frames only. |
| No pole through a face | **FAIL** | **B2**: s08, 21.4-22.4 s |
| No half-cut main character | **FAIL** | **B1**: s06, 16.65-17.70 s. Edge-clipped extras (s05 15.5 s, s10 25.5 s, s09 23.5 s) are not main characters and are fine. At 69.5 s about 25 % of the general's back leaves the right edge during the run. His face is fully in frame, so this is a note (N3). |
| No face in the caption band (y 880-950) | **FAIL** | **B3**: s16, 42.3-43.1 s. Elsewhere it is clear: the envoy at 33.0 s has his face at y ≤ 855 and the elder in s17 at 46.0 s has his face at y ≤ 830 (only his beard reaches the band). s01 g40-66 ox muzzles are allowed by director round 16. |
| No ghost or glitch artefacts | **FAIL** | **B4(a)**: s21, 53.2-56.1 s, translucent foreground pots. The dissolves at 20.0, 31.5, 33.5 and 58.0 s ghost as designed. The five whips have 2-4 frames of directional streak and read as whips. |
| No untextured placeholder blocks | **FAIL** | **B4(b)**: s21, about 55.2-56.0 s, beige block cups. Note N4: s23 58.5-60.0 s has a dark navy flat foreground merlon/rail at the bottom and left. It reads as a shadowed wall prop, but it is the flattest object left in the film. |

## Continuity

- **Night palette, s14/s15: consistent.** Both shots have a deep blue sky (mean sky RGB 54/99/181 and 56/99/179), the moon upper left, a warm fire at right, and sat 0.55/0.60.
- **Night palette, s21/s22: NOT consistent (part of B4).**
  - s21 is grey-mauve (sky 85/75/100, sat 0.37) with no moon and grey ground.
  - s22 is blue (sky 77/79/124) with a bright moon and warm orange ground (sat 0.54).
  - They are the same place joined by a whip, so the colour jump reads as a different location.
  - Other night shots: s16-s19 and s23 sit in a mauve-blue family, and s18, s20 and s24 in the s14 blue family. That spread is acceptable across different locations.
- **Oxen dress state: correct.**
  - Plain (no coat, no blades) in s05, s06 and s07.
  - Dragon silk plus horn blades in the s01 flash-forward and from s17 on (s17, s18, s19, s20, s21, s22, s26).
  - No oxen appear in s16 itself.
- **Wall holes: correct.** There are no holes on the inner wall in s07 (18-19.5 s) or the outer wall in s12. Holes open during s16 and stay in s17, s18 and s19.

## §G side-by-side with film 2: "As vivid, wide and grounded as film 2?" **YES, conditional on B4**

- **Vivid: yes.** I re-measured with qa_stats2.py and got the same numbers as the director:

  | | sat | vivid % | luma |
  |---|---|---|---|
  | Film 18 | 0.504 | 45.4 | 96.2 |
  | Film 2 | 0.490 | 49.4 | 94.0 |

  - On the sheet, film 18's dusk shots are richer than film 2's day plaza, and its night shots carry fire orange against moon blue, matching film 2's storm blues.
  - The vivid share is 4 points lower because of the mauve night block (s16-s19, s21, s23). s21 at 0.37 is the only shot that visibly looks grey next to film 2.
- **Wide: yes, wider than film 2.**
  - Film 18 has more wide and extreme-wide shots: s01, s03, s04, s07, s13, s16, s19, s24, s25 and s26.
  - No face is taller than 35 % of frame height. The largest are the general in s15 at about 23 % and the s22 ox at about 18 %.
  - Film 2 relies more on mediums and close mediums.
- **Grounded: yes, apart from s21.**
  - Characters stand on lit ground with shadows (s05, s09, s10, s14, s16, s26), and props sit on the floor.
  - The one shot that does not match film 2's solidity is s21 with its translucent glowing foreground (B4).

## §H BIGZOOMs and angle types

| BIGZOOM | Time (expected) | Measured | Continuous extreme wide to medium? |
|---|---|---|---|
| A, s01 | 0.0-3.6 s | 0.0-about 3.3 s, then a slow push to 5.2 s | **Yes.** One eased crane-down and push. Frame diff stays 5-18 with no cut-like spike (max 18.1 at g36, a foreground post sweeping past). It runs from high over the moonlit roofs, pens and lanterns (0.0-1.8 s), through the descent over the dragon-ox column and the 即墨 sign (1.8-2.2 s), to eye level and medium Tian Dan (about 49 % of frame height at 3.5-5.0 s). He is findable small from about 1.0 s, but at 0.0-0.5 s he is hard to pick out (note N6). The caption band is clear at the end. |
| B, s26 | 65.3-68.9 s | 65.27-about 68.9 s, then tracking with a push to 70.4 s | **Yes.** One eased crane-down (max frame diff 14.8, median 10.1, no spike). It runs from extreme wide over Jimo's gate (即墨 plaque), the road, the fields and the smoking camp, with the general about 3 % of frame height in a warm pool and oxen behind (65.3-66.5 s), down to a low medium (general about 44 % of frame height at 68.0 s, about 60 % at 68.9 s). It ends on the push-in on "วิ่งหนีวัว". |

Angle types used (more than the 4 required):
1. High or bird's-eye: s01 start, s03, s04, s07, s13, s24, s25, s26 start.
2. Eye-level medium: s05, s09, s10, s14, s15, s22.
3. Low angle: s16 (wall base), s19 (wall), s21.
4. Side tracking: s06, s20.
5. Through a foreground frame: s08 (spear rack), s11 (wine jars), s17 (reeds), s15 (jars).
6. Crane down: s01, s26.
7. Over-the-shoulder POV from behind the Yan line: s21.

## §I same channel and cuts: "Would a viewer believe this is from the same channel?" **YES**

- **Reasons:**
  - It uses the same flat-puppet cast design as R4/R5: round white heads, dot eyes, black outlines and simple robes.
  - Those puppets sit inside a lit, dense 3D cel-shaded world with warm practicals (torches, lanterns) against a blue night. That is the R5 ship and R4 snowy-town recipe.
  - The captions use the same chunky white word style with a dark outline at the same height.
  - The film has the same mix of wide establishing shots and character mediums, and in-world signs (即墨) like R4's grave plaques.
- **Differences:**
  - Film 18 holds its wides a little longer.
  - It is more orange at dusk than R5's saturated blues.
  - Neither difference breaks the family look.
  - s21's translucent foreground is the one frame set that looks off-brand (B4).
- **Hard cuts: 10** (≤ 12 passes; target 4-10). They are at s06 (g459), s09 (g674), s11 (g853), s14 (g1071), s17 (g1309), s18 (g1388), s19 (g1427), s20 (g1515), s21 (g1596) and s24 (g1807).
  - The director counted 9. The difference is s19→s20. The plan calls for "whip out / whip in", but the last 6 frames of s19 (g1509-1514) are nearly static (frame diff about 1.2) and there is no streak, so the join reads as a hard cut (note N7).
- **Whips:** all five read as whips, not glitches. Each has 2-4 frames of horizontal motion streak on both sides of the join and a matching direction, and the elevated frame diff before and after (13-26) shows a camera move, not a pop.
  - s04 (g297, vista push continues): reads as a whip.
  - s07 (g531, yard to quarter): reads as a whip. Its outgoing frames still show B1.
  - s10 (g737, quote 1a→1b): reads as a whip.
  - s15 (g1136, quote 2a→2b): reads as a whip.
  - s22 (g1683, camp to ox): reads as a whip. The incoming frames show s21's translucent pots (B4).

## Captions

- Legible on every phone tile: bold white Thai with a dark outline, centred at y 880-950, no tofu or black blobs.
- They never cover a face except at B3 (s16, 42.3-43.1 s).
- In the 19:59 re-render the caption text changed slightly at 1.0, 4.0, 7.5, 11.5, 12.0, 18.5-19.5, 22.0-23.5, 35.0, 37-38.5, 49.5, 51.5, 55.5 and 67.0 s. The new text is still within the band and legible.

## Non-blocking notes (for the client report)

- **N1 (s03-s04, 5.2-12.8 s):** The Yan pennants read dark maroon/red at phone size. They are close to the Qi red of s25, so the "who holds what" colour code is weak. Next time, use matte black with no red rim light.
- **N2 (s26, 66.3-66.5 s):** A torch stand overlaps the tiny general during the crane, and he reads as perched on it.
- **N3 (s26, about 69.5 s):** About 25 % of the general's back leaves the right edge mid-run. His face is in frame.
- **N4 (s23, 58.5-60.0 s):** The flat dark navy foreground merlon/rail has no texture.
- **N5 (s20, 50.5-53.2 s):** Only one ox is visible, so the "herd charges" feeling depends on s19 and s21. The pot and reed clutter in the field is busy but grounded.
- **N6 (s01, 0.0-0.5 s):** Tian Dan is not findable in the first two phone tiles. He is findable from about 1.0 s.
- **N7 (s19 end, g1509-1514):** These frames are near-still and the planned whip-out is missing, so the s19→s20 join plays as a hard cut.
- **N8:** Large plain ground in the lower third at s05 (13-15 s), s16 (40.5-41.5 s) and s18 (46.5-47.0 s). It is textured, so it is within the ground_share gate. This is a visual note only.
- **N9 (s22, 56.1-58.0 s):** The foreground pot at lower left is soft and glowing, like s21's but opaque. Fix it in the same pass as B4 if it is cheap.
- **N10 (QA_AUTO):** QA_AUTO.md reports "planned cuts with no visible change" at every planned g. The frame-diff spikes are in fact at the planned g (see the cut list above), so that line looks like a first_g offset in the script run, not a film problem.
