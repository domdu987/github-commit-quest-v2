# QA s23 v3 (shot 23, TOWER tower_fair DAY 1910, g 1656..1731 + handles g 1648..1655 (dissolve in) and 1732..1739 (dissolve out into shot 24))
After TAKE_ART (F1-F3 callback), TAKE_B and QA_TEAM §G. Checked at 6 fps contact + phone sheet.
- `qa_stats.py take.mkv`: **saturation 0.575, brightness 93.4, in-shot motion median 6.98 p90 10.61** (sat/luma met; p90 1.4 short). In-shot only (g 1657..1731): median 6.01, p90 9.46, max ~18.
- Callback of s15 v3: same staging (camera 3.5 D from Old Eiffel, cam z 1.6; the official 0.5 D nearer and 1.25 D right, steps back g 1684-1702; gent back card FG bottom-left; 40 crowd cards bobbing; preset lamp-post/bench out of frame: the black rectangles and pole of v1 are gone), as a PULL 10 %/s + arc 17 deg/s + snap x1.6 on 'อีก 70 ปี' (g 1706).
- Heads: Old Eiffel head width 173-263 px (centre y 536-638, chin <= 742); no head cut by the frame edge. Mouths never move.
- Beat: the official hands the NEW sealed document (g 1664-1676), Eiffel takes it, moves it to the left hand behind a blink (g 1696); g 1706 blink swap worried -> proud and the bowler comes off (hat_off) and is held out in the right hand.
- NOT FIXED: the bowler still reads as a dark dish held at chest height. The cast20 arm rig clamps the hand near chest height (hand y > ~1.0 has no effect), so it cannot be raised to the head; the prop is the cast20 `bowler_held` as the director asked. The dark ball on the document is the left fist holding it.
- 1910 vs 1889: carried by Old Eiffel (white beard) and the new document; set_year(1910) differs little in this framing.
- take.mkv 31.4 MB (single file).

## v4 (QA_TEAM §I client decision)
- Same banner "EXPOSITION UNIVERSELLE 1889", fluttering pennants and low raking sun as s15 v4 (callback), crowd + flags move.
- `qa_stats2.py take.mkv`: sat 0.568, vivid 50.1 % (>= 45), luma 93.4, warm 39.9 % / cool 31.5 %, motion median 6.92 p90 10.74, still 0 %. In-shot g 1657..1731: median 5.89, p90 9.51 (p90 short of 12).
- Bowler is still the flat dish (arm rig limit, see above).
- take.mkv 31.2 MB.

## v5
- Re-rendered with more orbit (24 deg/s) and slide (-75 px/s). `qa_stats2.py take.mkv`: **sat 0.564, vivid 50.0 %, luma 94.4, warm 35.3 % / cool 35.8 %, motion med 7.30 p90 11.45, still 0 %**. In-shot g 1657..1731: median 6.44, p90 10.30. Head width 175-275 px, centre y 519-639, chin <= 743. take.mkv 29.0 MB.

## v6 (TAKE2_B s23 fixes)
- Bowler: raised overhead. Cause of the old "flat dish": cast20 arm hand y is DOWNWARD-positive (point_up uses y -0.8), so my earlier tweens had pushed the hand down; now arm_r goes to (0.58, -0.45) with bend -0.5, stretch 1.25 and the bowler_held prop (rim visible) is held above his head, bare head + proud smile (blink swap g 1705-1707).
- Official: stays in frame the whole shot (head x 455-593 at the end, widest 232 px, right edge < 720; he only steps back 1.6 D g 1684-1702), so the new-document hand-over g 1664-1676 (stretched arm, Eiffel's hand takes it, doc moves to his left hand behind a blink g 1696) stays on screen.
- Framing: wider (5.2 D, was 3.5): Eiffel is shown at the thighs at the end, the tower legs, first platform and banner stay behind him; head width 140-262 px (centre y 543-652, chin <= 724). Snap x1.9 with a 0.55 D pan toward the official keeps both in frame.
- `qa_stats2.py take.mkv`: sat 0.544, vivid 47.2 %, luma 97.7, warm 47.4 % / cool 25.3 %, motion med 6.32 **p90 12.16**, still 0 %. In-shot g 1657..1731: median 5.44, p90 11.57. take.mkv 34.0 MB.
- The set flags: my pennants are vertical blue-white-red tricolours; the preset flags are the set builder's.

## v7 (director re-request; set flag fix d1511f7 merged)
- Re-rendered with the merged set: the preset flags are vertical blue-white-red tricolours now (my own pennant poles already were). All v6 fixes stand (raised bowler with rim visible, official in frame, document passes hand to hand on screen, wider with the tower behind).
- `qa_stats2.py take.mkv`: sat 0.544, vivid 47.2 %, luma 97.6, warm 47.4 % / cool 25.3 %, motion med 6.43 **p90 12.25**, still 0 %. In-shot g 1657..1731: median 5.52, p90 11.61. Head width 140-262 px, chin <= 724. take.mkv 34.0 MB.

## v2 fix (client rejection of rivet_v1)
- The giant dark head card in the bottom-left foreground (`fgh`, a back-turned gent card) is removed completely (actor, placement, sprites). Nothing blocks the frame.
- Camera made gentler: the x1.9 snap at "อีก 70 ปี" is now a longer x1.5 eased push (g1692-1722), the earlier x1.25 snap a x1.15 drift. Crowd idle bob 0.10 -> 0.015 D (cards no longer leave the ground).
- Banner pole bottoms (were 1.2 D underground) now end at the ground; pennants and the hut lamp are tagged airborne. ground_check PASS (GROUND.md, 0 FAIL rows).
- qa_jitter: no second above 2.0 px (overall median 0.21). qa_auto PASS. qa_stats sat 0.529, luma 108.6, frame-diff median 5.60 / p90 6.62.
- Timing, 8/8 handles, both dissolves unchanged (meta.json).

## v2b (director's float-hunter items)
1. Certificate: one person holds it the whole time. The official holds it until the handover, then it is in Eiffel's RIGHT hand (arm out beside him, visible) until the hat flourish; it moves to his LEFT hand (arm out, visible) on the same closed-blink frame as the hat swap (g1706) and stays there. The old transfer at g1696 (where it vanished / sat flat on his chest) is removed.
2. Bowler: the raised hat is on the end of his right arm (hand to the right of his head at brim height, arm visibly raised), no longer floating beside the head.
Re-rendered the whole take (same camera, timing, handles). ground_check PASS (gc.py), qa_auto PASS, qa_jitter see above (no second above 2.0 px).

## v2c (batch-3 float hunter: hand-held props read as floating, so none remain)
- Certificate deleted from every frame. Hat raise dropped: Eiffel keeps the bowler ON, hands on hips, worried -> proud on the blink swap (g1706) with a happy nod. Official no longer steps back, so both heads keep the same scale (camera push softened to x1.3).
- Whole take re-rendered. ground_check PASS, qa_jitter median 0.23 px (no second above 2.0), qa_auto PASS, qa_stats sat 0.522 luma 106.9.
