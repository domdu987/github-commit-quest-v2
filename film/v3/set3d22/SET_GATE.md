# SET GATE: film 22 "ไอ้ช่างวงจร" (set3d22 + cast22)

Reviewer: QA-art (Opus). The client delegated look approval to this gate. Date 2026-11-20.

**Inputs reviewed**
- Every contact still at full size (720x1280): builder A s01 s02 s04-s08 s15, builder B s03 s09-s14.
- Both phone sheets.
- hue_rows*.txt, BUILD_NOTES*.md, API.md.
- The cast22 sheet (line-up, poses, expressions, props) and cast22 API.md.
- shot_plan.md, WORLD.md, FACTS.md.
- Board QA_ART.md (round-2 carry-forward rules).
- QA_TEAM §G/§H/§I.
- R5 sheet and film 2 frames (5/20/40 s).

**Extra checks.** The contacts only show start/mid/end, so I also rendered 24 preview frames from the current shot cameras with `beck.py shot sNN <frame> preview` (output in scratch only; nothing in the repo changed): s03 205/215/240/260/290/310, s09 1120/1160/1185, s06 700/792, s10 1280, s15 1800/1840/1870, s05 530, s11 1340/1440, s01 60, s07 880, s14 1720, s13 1640, s04 400 and s08 990. I also rendered one wide test view of the noodle cavern.

## Verdict: **PASS** (render teams may start; the MANDATORY items below are part of the approval)

No location has a set-level defect that would make every take fail.

Every problem found can be fixed inside the take by the team that owns it: framing, actor placement, runtime hide/move/scale of an object, light energy, or setter timing. Those fixes are listed below as MANDATORY. A take that ignores one fails the TAKE gate.

**Film-level numbers (39 contact tiles)**

| measure | result | target |
|---|---|---|
| mean sat | 0.62 | ≥ 0.50 |
| mean vivid | 62 % | ≥ 45 % |
| mean luma | 101.9 | 85-110 |
| shade hue | 240-260 on most tiles | 240-260 |

Off-band shade hue, all fixable per take: s02 end 279, s03 end 270, s05 263, s06 end 271, s10 end 279, s11 end 142, s14 mid/end 332/315, s15 end 274.

**Other film-level checks**
- No sign claims maps were FREE. I grepped all sign painters and read every sign.
- Angle types in the plan: 8 (≥ 4 needed).
- BIGZOOMs: 2.
- Wide/medium-wide is more than half the shots.

The look sits in the same family as R5 and film 2: deep blue base, warm practicals, the four Tube colours as accents.

**Weaknesses that do not block**
- The interiors have a heavy lilac wash.
- The furniture in the publicity room and corridor is blocky.

Neither stops a take from reading.

## Scores

### Set: "rich and detailed?" (§H.3)

| location | rich & detailed? | density | light & colour | period | note |
|---|---|---|---|---|---|
| london (DUSK/NIGHT) | **yes** | 8 | 8 | 7 | Low 1930s skyline with ONE dome and ONE clock tower, river, HQ with PUBLICITY DEPT, roundel, NEWS, FLOWERS, bus, crowds. The bus roof still has red streaks (s02 mid). The near crowd at the station entrance is simple flat cards and static. |
| lodgings | **yes** | 8 | 7 | 8 | Wallpaper, shelf, cork board with circuits, OLD map (reads, MAP OF LONDON), NOTICE, line-colour ink bottles (now the right size), drafting board, lamp, window to the street. |
| publicity | **yes** (marginal) | 6 | 6 | 7 | Panelling, clock, partition with PUBLICITY DEPT, 6 clerk desks, bins, lamps. Furniture is blocky, the aisle runner floor is large, and a dark upright panel on the official's desk hides his face (see team 3). |
| corridor | **yes** (marginal) | 6 | 6 | 7 | Clock, WEMBLEY poster, notice board with circuit sheets, doors, bench, lamps. The bottom quarter is a dark bare floor and s08 end is too dark (luma 78). |
| under: shaft / noodle tunnels | **yes**, conditional on camera | 7 | 7 | n/a | The shaft and grate from below read well. The wide test render shows the cavern does hold a readable tangle of coloured tubes with lit trains. The current s03 camera flies *inside* the tubes (frames ~205-250), so the shot reads as abstract plastic, then as a plain navy tube (262-290). |
| platform | **yes** | 8 | 8 | 8 | Vault, maroon ribs, globes, clock, TO TRAINS, WAY OUT, PICCADILLY, posters (WEMBLEY now correct), red train with lit windows. MIND THE GAP edge plate is upside down/reversed from the s10 camera. |
| ticket hall | **yes** | 8 | 8 | 8 | Checker floor, pillars, globes, TICKETS, NEW MAP / TRIAL and NEW POCKET MAP signs, stand, rack of POCKET MAP boxes, REPRINT crates, falling sheets. Floor share is too high in s09. |
| carriage | **yes** (marginal) | 7 | 5 | 7 | Seats with moquette, poles, straps, a line diagram, passengers with newspapers. The ceiling panels are blown (top third luma about 130) and the windows read bright blue, not near-black tunnel. pass_man perches on a seat back. The pocket-map plane floats in front of pass_woman's head. |
| mapworld | **yes**, conditional on the walls | 7 | 7 | **4** | Strong idea: Beck's drafting table, giant ink bottles, green lamp, raised glossy lines, rings, tiny trains and passengers, city sheets with readable labels. The four `night_city` walls read as modern glass towers (the same period error the board fixed in round 1). The red train disappears on the red line. CHANGE HERE shows mirrored from behind (s12 mid). |

### Cast: **8 / 10**

Strengths:
- Ten distinct, period-correct members on the shared puppet head.
- Strong silhouettes: Beck's glasses, red tie, waistcoat and pencil; the official's comb-over, handlebar moustache and pinstripe; the porter's roundel cap.
- 16 crowd variants.
- The full expression set, including red face and puffed.
- All story poses exist: rule_line, set_square, thumb_push, hold_circuit, read_notice, sag, knock, proud, off_stamp, laugh_back, wave_sheet, eat_mime, toss_drawer, smug_rub, peek (with pillar), jaw_drop, buried_eat (napkin, knife, fork with map).
- Props: ruler, pen, set square, T-square, roll, pocket map, stamp, fork.

What it lacks:
- Cards are static billboards, so motion depends on the render teams.
- A few placed poses go wrong in the set: Beck lies across the board in s05, and pass_man sits on a seat back in s11.

## Per-location notes (what I saw at full size)

### london (s02, s15)
- **s02 mid:** the extreme wide works. HQ findable, PUBLICITY DEPT and UNDERGROUND readable at phone size, river glitter, period roofs and chimneys.
- **Bus roof:** it still shows the red diagonal streaks (carry-forward rule 8).
- **BIGZOOM start:** no character is findable in the wide.
- **s02 end (grate top-down):** reads as orange glowing slots (luma 128, hue 279) and is opaque. s03 start, seen from inside the grate, shows dark iron bars with the shaft lit below, so the two sides of the join do not match.
- **s01 end / s02 start, near crowd:** the crowd under the canopy is a wall of simple flat cards about 15-20 % of frame height, static, not cast22. Carry-forward rule 7 allows crowd cards only below about 8 % of frame height.
- **s15:** start and mid good. The camera dives past the crowd and fills the PUBLICITY window nicely (frame 1840).
- **s15 end (BIGZOOM 2 end) is the weakest tile of the film:**
  - the official is about 12-15 % of frame height (target 35-60 %);
  - the ceiling takes the top 20 %, the desk front and floor the bottom 30 %;
  - the towers are pale;
  - sat 0.41, vivid 21 %, luma 120.

### lodgings (s01, s04, s05)
- **s01 start:** good hook framing, with the red line, set square and OLD map beside the board. The red line is short and low on the board.
- **s01 frame 60:** Beck is hidden **behind** the drafting board; only a sliver of hair shows over its top edge. This breaks the 0.65-1.82 beats.
- **s04 start:** the OLD map fills the frame, readable, which suits the match from s03. s04 end is fine.
- **s04 frame 400 (NOTICE beat):** the wastebasket of crumpled paper in the foreground hides Beck's legs and feet, so grounding cannot be seen.
- **s05 (whole take, frames 530 and end):** Beck's card lies diagonally **on the paper**, legs across the diagram. It reads as a man floating on the board.
  - The OLD map is not in the frame (the plan wants it in a corner).
  - Luma 112-113 and hue 263, both above band.

### publicity (s06, s07)
- **s06 start:** good through-the-partition composition, sign readable. The aisle runner and a paper sheet take the bottom 25 %.
- **s06 frames 700 and 792 (the PUNCH-IN on "ทั้งแผ่นเลย!"):** a dark maroon upright panel on the official's desk (the "in-tray"/desk screen) **cuts the official's face in half**. The close-up #1 is unusable as it stands.
- **s06 end:** a large anonymous purple block fills the left foreground. Beck is cut by the left edge.
- **Laughing clerks:** they are not visible during the laugh.
- **s06 → s07 join:** s06 end is a close two-shot at the desk; s07 start is a wide from the aisle. The planned join is "travel", but the cameras do not match.
- **s07 end and frame 880:** a bright blue horizontal slab (beam or partition top rail, seen from above with the ceiling off) covers about 35 % of the lower frame, plus a white strip. The clerks at their typewriters are mostly hidden. The official is cut by the top edge.

### corridor (s08)
- Readable story: roll under the arm, knock, PUBLICITY sign, the hand.
- The bottom quarter is dark bare floor. End luma 78 (< 85).

### under: shaft and noodles (s03)
- The start through the grate is good. Frames 205-250 are inside translucent tubes (abstract). Frames 262-290 are a plain navy tube with fan-shaped halo quads around the lamps; the halos read as artefacts.
- **s03 end:**
  - old_gent is about 28 % of frame height (BIGZOOM end needs 35-60 %);
  - the OLD map's top (MAP OF LONDON title) is **cut by the curved vault**: the wall intersects the map plane;
  - the map reads salmon-pink (hue 270, luma 129), while it is grey-lavender in s04 start, so the match dissolve will show a colour jump;
  - the bottom 40 % is bare floor;
  - pass_man's bump at 9.81 is not in the frame.
- **Frame 310:** pass_woman's head is cut by the bottom frame edge.

### platform (s10)
- Rich and well lit. The train entry and jaw drop read.
- The foreground bench at the left reads as a pink table slab.
- The MIND THE GAP edge plate is upside down/reversed.
- WAY OUT is cut to "UT" at the end. Shade hue at the end is 279.

### ticket hall (s09, s13)
- **s09 mid:** good, with porter, pass_woman, TRIAL sign and pocket maps. pass_woman is cut by the right edge.
- **s09 frames 1120-1196 (Q2, 37.38-39.90):** **the official is not visible**. pass_man stands on the camera's line of sight to the pillar mark (-10.9, 17.4); the end camera looks at (-10.8, 17.4, 3.2) and pass_man at (-5, 8.5) sits in between. The only lip-sync of the beat is off screen.
- The bottom 35 % of s09 end is bare checker floor.
- **s13:** very good: rack full then empty, sheets on the floor, REPRINT crates, crowd. Beck (beck_proud) is not seen in any s13 frame I checked.

### carriage (s11)
- **Lighting:** the ceiling light panels blow out (mid luma 129); the windows read bright blue instead of near-black navy tunnel (carry-forward rule 5).
- **pass_man (s11 start):** he sits on top of a seat back with splayed legs, i.e. floating, not at the window.
- **s11 frame 1440 and mid:** the pocket-map plane (1.9 x 1.32 D) is poster-sized and hangs **in front of pass_woman's head**, so she is headless and there is no over-the-shoulder view.
- **s11 end:** the paper close-up (vivid 25 %, hue 142) is acceptable only as a short push-through frame.

### mapworld (s12, s14)
- **Walls:** the four `night_city` walls fill the top 30-40 % of every s12 frame and of s14 start/end. Scaled to this size they read as modern grid-windowed towers (s12 mid shows slanted skyscrapers). This repeats the round-1 skyline error.
- **s12:**
  - the lead "red train" is a red box on the red ridge and does not read as a train;
  - the bottom 40 % is the red ridge plus bare paper;
  - luma 118-124;
  - in s12 mid, CHANGE HERE is seen from behind, mirrored. In s12 end it reads correctly.
- **s14 mid/end:** good. City sheets with BANGKOK, TOKYO and LONDON readable, glowing lines. The brown table pushes the hue to 315-332 and luma to 125.

## Blocking set fixes

**None.**

The following are recommended for the builders if they touch the set again. The render teams below must work around them regardless:
1. beck_map: replace the `night_city` wall texture with a low period London row (4-6 storeys, pitched roofs, chimney pots), or drop the walls.
2. beck_map: make the CHANGE HERE tag double-sided (a correctly oriented back face).
3. beck_under: rotate the MIND THE GAP plate 180°.
4. beck_under: move the platform OLD map down about 0.8 D so the vault does not cut it.
5. beck_under: replace the lamp halo quads in the s03 tunnel with round glows.
6. beck_hq: lower or remove the dark upright panel on the official's desk.

## Instructions for the render teams (all MANDATORY)

Teams: 1 = s01 s04 s05 · 2 = s02 s15 · 3 = s06 s07 s08 · 4 = s03 s09 s10 · 5 = s11 s12 s13 s14.

### All teams
1. **(all shots) Colour per take.**
   - The take mean must reach sat ≥ 0.50, vivid ≥ 45 % and luma 85-110.
   - Shade hue 240-260 on at least 80 % of the take's frames.
   - Top-third luma ≤ 115.
   - Report the numbers with the take.
2. **(all shots) Nothing floats.**
   - Every visible foot has a contact shadow.
   - No card lies across or perches on furniture.
   - No head is sliced by a slab, pole or panel.
   - No actor is cut through the head or body by any frame edge, bottom edge included.
   - Check every 0.5 s phone tile.
3. **(all shots) Signs.**
   - Every sign that is in frame for more than 6 frames must read at 360x640 and must never show mirrored or upside down.
   - If a sign is seen from behind or reversed, hide it for those frames.
4. **(all shots) People.**
   - Named characters use cast22 poses with lip-sync only in Q1 (s06) and Q2 (s09).
   - Crowd cards nearer the camera than about 8 % of frame height must be cast22 `crowd_member(i, "pass_walk")` cards that walk.
   - Nobody is still for more than 1.5 s.

### Team 1 (s01 s04 s05)
5. **s01 frames 0-107.**
   - Beck must stay in front of or beside the drafting board for the whole take: never occluded by the board (frame 60 now shows only his hair over the board top).
   - Move his mark or the arc so his face and both hands read on 0.65 (set square snap) and 1.82 (thumb slides the tick).
   - At frame 0 the red line must be at least 25 % of frame width.
6. **s01 end, s01→s02 join.** Coordinate with team 2 (item 11). The window card `window_london.png` must be re-rendered from team 2's corrected london (walking cast22 crowd at the entrance), so s01 end equals s02 frame 107.
7. **s04 frames 390-420 (NOTICE beat).** Move the wastebasket out of the camera-to-Beck line, or raise the camera, so Beck's legs, feet and contact shadow are visible.
8. **s05 whole take.**
   - No Beck card lying on the paper.
   - Start (local 0-25): Beck upright at the board's lower edge with his head in the top of frame.
   - After that: only his forearm, hand and pen (place_tip on the line) enter from the bottom or right frame edge, with sleeve visible to the edge.
   - Keep the OLD map in a corner of frame from 18.09 s (frame ~546) to the end.
   - Lower the lamp/paper light about 10 % to reach luma ≤ 110 and hue ≤ 260.

### Team 2 (s02 s15)
9. **s02 mid (BIGZOOM 1 start).**
   - Put a findable character in the extreme wide: a Beck card at the lit lodgings window (`L.LODGE_WIN`), under 5 % of frame height, rim-lit.
   - Fix the bus roof: swap the roof material to a flat red (#c8201e) so no red streaks show.
10. **s02 frames 175-191 (grate).**
    - Dim the grate glow about 30 % so the iron bars read dark against the warm light (target luma ≤ 110, hue ≤ 260).
    - The last frame must match team 4's s03 frame 192. If the grille textures cannot match exactly, use a 4-frame dissolve on the grate, agreed with team 4.
11. **s02 frames 107-140 (and team 1's window card).**
    - Hide the static flat crowd cards under the station canopy within about 25 D of the camera.
    - Replace them with 12-20 cast22 `crowd_member` walking cards streaming into the entrance, with contact shadows and warm rim.
12. **s15 frames 1840-1889 (BIGZOOM 2 end).**
    - Re-key the final camera so the official is 35-60 % of frame height (head to desk line), with napkin, knife, fork and map readable.
    - Ceiling ≤ 15 % and desk front plus floor ≤ 20 % of frame.
    - `map_towers(1)` reaching the ceiling.
    - The crate lands with contact at 61.72 s.
    - Add a warm desk-lamp key and a cool window rim to reach sat ≥ 0.50, vivid ≥ 45 %, luma ≤ 110 on the end frames.
    - Mouth closed.

### Team 3 (s06 s07 s08)
13. **s06 frames 577-823 and s07 frames 823-850.**
    - Hide (or move to the desk's far-left corner) the dark upright panel or in-tray on the official's desk that cuts his face.
    - The official's whole head must be clear in the two-shot, the stamp beat and the **punch-in at 25.9-26.9 s** (close-up #1, face ≤ 35 % except this planned punch-in).
14. **s06.**
    - Hide or move the large purple foreground block at the left of the end framing.
    - Beck must not be cut by the left edge.
    - During "หัวเราะลั่น" (21.85-23.5 s) at least 2 laughing clerks must be visible through the glass, with a bounce of 0.06 D at about 3 Hz.
    - From frame 610 on, the aisle runner and floor ≤ 20 %.
15. **s06→s07 join.** s07 frame 823 must equal the s06 frame 822 camera exactly (travel join). Then crane up and back.
16. **s07 frames 850-938.**
    - Hide the bright blue slab and white strip (beam or partition top rail) that covers the lower third in the bird's-eye.
    - The clerks at the typewriters must be visible pointing and laughing.
    - The official and Beck must not be cut by the top edge.
17. **s08.**
    - Raise the corridor lamp energy about 20 % (end luma ≥ 85).
    - Keep the bare floor ≤ 20 % (camera a little lower or tilted up).
    - The hand that grabs the roll must be seen at 33.16 s.

### Team 4 (s03 s09 s10)
18. **s03 frames 200-260 (noodles).**
    - Re-key the camera to pass **outside** the tubes for at least 0.6 s, so the tangled knot of coloured tunnels with lit trains reads as a whole (as seen from about (GX, GY-6, -30) looking at (GX, GY+38, -46), lens 22). Then enter a tube.
    - Hide or replace the fan-shaped lamp halo quads.
    - Keep the near-black navy-only stretch (262-290) ≤ 0.5 s, or add the lamp string.
19. **s03 frames 282-323 (BIGZOOM 1 end).**
    - old_gent 35-60 % of frame height at 9.3 s.
    - pass_man's bump visible at 9.81 s (pose 'bump').
    - No actor cut through the head by the bottom edge (frame 310).
    - Bare floor ≤ 20 %.
    - Move the OLD map down about 0.8 D (or frame below the vault line) so no wall cuts it.
    - Light or grade the map to the cool grey-lavender of s04 start (hue 240-260, luma ≤ 110), so the match dissolve to s04 does not jump.
20. **s09 frames 1085-1197.**
    - The official must be visible at the pillar from 36.19 s and through all of Q2 (37.38-39.90), with face and lip-sync readable.
    - Move pass_man off the camera-to-pillar line, e.g. to x ≥ -2, before local frame 110.
    - Keep pass_woman inside the frame edges.
    - Raise `set_crowd` toward (30, 3) or place extras so the bare checker floor is ≤ 20 %.
21. **s10.**
    - Rotate the MIND THE GAP edge plate 180° about z (or hide it).
    - Frame the foreground bench so it reads as a bench (seat edge with legs), not a flat pink slab.
    - Keep WAY OUT either fully in frame or out of frame.
    - The end shade hue must be ≤ 260.
    - The last frames must hand over to s11 as planned ("travel from s10's train door"), agreed with team 5, or with a dissolve of at most 6 frames.

### Team 5 (s11 s12 s13 s14)
22. **s11 whole take.**
    - Dim the ceiling light panels about 40 % (top-third luma ≤ 115, take luma ≤ 110).
    - Windows near-black navy with the scrolling streaks.
    - pass_man stands at the window with nose to the glass and feet on the floor (or sits on the seat cushion, z = seat + 0.05), never on the seat back.
23. **s11 frames 1395-1485.**
    - Move and scale the pocket-map plane into pass_woman's hands at chest height, about 0.7 x 0.5 D.
    - Make it a real over-the-shoulder: her head and shoulder in the foreground, the map beyond.
    - The taps glow on 47.29 / 47.95 / 48.80.
    - The final push into the paper ends the take; the plain-paper close lasts ≤ 0.4 s.
24. **s12 and s14 (mapworld walls).**
    - Hide the four `night_city` walls (the modern towers) in every frame. Let the dark navy, the giant ink bottles and the green lamp form the horizon.
    - Or scale the walls in z to ≤ 0.35 so only a low 4-5 storey band shows.
    - No tall grid-window towers may be visible.
25. **s12.**
    - The lead train must read as a train: give it a cream roof and lit yellow windows plus a headlamp (material swap on that object).
    - Ride 2-3 D higher and slightly to the side, so the train reads against the paper and the other lines and rings fill the lower frame (bare paper or ridge ≤ 20 %).
    - Hide the CHANGE HERE tag whenever the camera sees its back (mirrored in s12 mid). It must read the right way at 50.29 s.
    - Lower the MAPWORLD key about 12 % (luma ≤ 110).
26. **s13 frames 1640-1662.** Beck (beck_proud) must be visible for at least 1 s at 54.7-55.4 s, glancing at a map in a stranger's hand, in frame and rim-lit.
27. **s14.**
    - Cool the table and lamp light (hue ≤ 260, luma ≤ 110 on the mid frames).
    - The last frames must glow, ready for the match dissolve to s15.
