# QA s24 (shot 24, g 1732..1813; take g 1724..1817)
RESTO resto_wide DAY 1889. The waiter (lead gesture, towel on arm) leads Maupassant (smug) down the runner toward the window end; chair-back FG at the start, table edges FG later; trusses, chandeliers, diners from the set.
- Checked at 6 fps + both cut sides: heads 65-105 px (a wide: exempt from the 450-760 band, they sit y 590-700, all above 880); feet on the carpet with contact decals; no mouths move; blinks only; waiter walks beside/ahead, no overlap after the lateral offset.
- Walk is DIAGONAL-AWAY in three-quarter view (yaw 0.55): no waiter back card exists in cast20, so we show faces. Deviation from "backs to camera".
- Snap push x1.45 on "หลังหอเปิด" (g 1777..1792). Dissolve-in handle 8 frames, cut-out handle 4.
- Frame-diff median 3.57, p90 9.91 (target 4 / 12): slightly under, the camera moves 50 px/s + 7 %/s over a mostly static room.
- GOTCHA: cap_g("text") returns the FIRST caption with that prefix; "แทบทุกวัน" occurs at 5.24 s and 61.15 s: use g_of(t) for repeated phrases.
