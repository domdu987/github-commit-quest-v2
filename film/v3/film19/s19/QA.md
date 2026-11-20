# QA s19 (shot 19, SHIP ship_coast DAY_JAMAICA, g 1468..1580 + 9 handle frames each side, take g 1459..1589)
- Frame-diff in-shot (90x160 grey): median 7.12, p90 9.77 (target 4 / 12): median OK, **p90 below target** (deviation: a harder snap or more drift pushed William into an extreme close-up whose head left the safe band, so the snap was held at x1.65).
- Heads: head centre y 530-600 after g 1497 (wide start 546), whole heads above y 880 (bottom estimate <= 775); William's head is large (~390 px) after the snap = the planned push-in on the watch.
- Camera: world-fixed (the beach is not the ship), CamPath drift push 4 %/s + arc -14 deg/s + rise, starting framed to the right and a pan-snap x1.65 (shift 1.9 D) on "แค่ห้าวินาที" (event g 1497; snap g 1495..1509). camreport: never parked.
- Set: set_sea/set_roll keyed on every frame with t = (g - first_g)/30. NOTE: keying t = g/30 (50 s) made the tide flood the beach (found on drafts); relative time keeps the shore.
- Cast: william19 (H4 raised in the right hand, tricorne in the left, grin), sailor19_a (shore_b offset) and sailor19_b cheer, arms up, ~3 Hz bounce 0.06 D. All mouths still. No text, no DOF, no caption_shade.
- Known: late in the shot (g 1560+) the straight sand/sea edge of the beach mesh shows behind the sailors (set geometry; accepted, read as a sandbank). Planned cut at g 1581 is flagged "no change within +-2 f" by qa_auto only because the handle continues the same 3D move (same as s01).
- Continuity: shot 18 (ship_hero) dissolve in 13 f; shot 20 hall hard cut out.
