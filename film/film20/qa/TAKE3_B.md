# QA-tech TAKE gate round 3 (B), film 20: s15 s18 s21 s27
Method: ffmpeg frames (g = first_g + index), qa_auto.py + qa_stats2.py, own frame-diff (90x160 grey, in-shot), viewed at 6 fps + g0/g1 +-3 + beat times + full-size crops. Takes not edited.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeqa3/

| take | sat | vivid % | luma | diff med / p90 (own) | auto | verdict |
|---|---|---|---|---|---|---|
| s15 | 0.585 | 49.4 | 86.9 | 7.7 / 13.3 (qa_stats2 7.10 / 11.40) | PASS | PASS |
| s18 | 0.639 | 61.9 | 95.8 | 4.6 / 26.7 (first 90 f: 2.5 / 8.4) | PASS (soft g1384-1394) | FAIL |
| s21 | 0.535 | 47.9 | 88.2 | 17.7 / 33.9 | PASS | FAIL |
| s27 | 0.627 | 71.2 | 88.5 | 11.1 / 36.9 | FAIL-flag (8 soft, content) | PASS |

## s15 PASS
Round-2 issues: 1 permit floating FIXED (held out by the official g1008-1030, then at Eiffel's chest in his fist); 2 official face / banner FIXED (banner readable to ~g1075, face ~33-35 % for < 1 s); 3 frozen men FIXED (sway, wave, bow); 4 luma 84.3 FIXED (86.9), soft frames no longer flagged; 5-6 ok.
Notes (non-blocking): qa_stats2 p90 11.40 is within 10 % of 12 and the beats read (own measure 13.3); Eiffel's head ~35 % of frame height g1078-1092 (< 1 s punctuation); the fist holding the paper is a dark ball, no visible fingers.

## s18 FAIL (close)
Round-2: 1 ground slab NOT FIXED (see 1); 2 tiny figures PARTLY (old Eiffel readable with white beard from g1221, wagon + crowbars visible, heads still ~45-60 px); 3 Eiffel cut at crane start FIXED; 4 wire FIXED (wire reaches the ground post, whip g1346-1360 reads); 5 blown glass/black square PARTLY (see 2); 6 hand on key FIXED enough (arm bent to the key, blue arc + flashes sync g1396-1429); 7 contact shadows OK.
Camera: moves the whole take (push, crane, whip, dive, push-in); the low median is slow push on a smooth sky in g1221-1310 (median 2.5), whole take 4.6 / p90 26.7: judged moving, PASS on that point.
1. g1210-1300 (3 s): bottom 35-40 % is a bare blue-violet slab (limit 25 %). Fix: tilt up ~6 deg / raise horizon or dress the ground (cart, ropes, crowbars, lamp pool).
2. g1380-1383: the hut window glass is blown pure white (4 white panes) just before the crossing; g1384-1394 (11 flagged soft frames) are the camera inside flat orange battens, a vertical batten fills the centre third. Fix: lower glass emission before the dive, hide it from g1376 not g1384; shorten the batten crossing to <= 4 frames.
3. g1383-1384: pop (glass-off) visible. Fix: same as 2.

## s21 FAIL (first review)
Works: night rise along the wire up the lattice g1427-1467 reads; first ring born at the lit summit g1468 and expands over a lit Paris g1472-1530; swoop g1532-1576 lands on the group; all lit, saturated, no cuts, mouths still, white beards on old Eiffel not resolvable (see 4).
1. g1577-1655 (2.6 s, all the group phase): bare dark-blue ground fills the bottom 50-55 % (limit 25 %), characters are a thin strip at y 560-720 (heads 43-64 px) with no dressing below. Fix: lower/tilt the camera so the group sits lower with the tower behind, <= 25 % floor; add kegs, crates, cobble detail, lamp pool.
2. g1625-1630 salute and g1607-1619 drop: at phone size the officer's salute and the falling bars are 20-40 px specks (blue crowbars read as dark lines on the ground); the beats do not read. Fix: push in to a medium of Eiffel + officer for these 30 frames.
3. g1526-1529: a ring seen edge-on becomes a huge flat white slab across the frame (up to 15 % of frame height at g1528) = broken-geometry look. Fix: thin the ring or keep the camera out of its plane at that moment.
4. g1530-1539 "เสาอากาศยักษ์": the blue-white glow along the wire/lattice is not visible; the wire is a thin white line and the lattice stays dull brown-orange (not glowing red iron + blue-white glow). Fix: strong blue-white emission on the wire and lattice edges for g1530-1545, bloom, cool light on the iron.
5. g1577-1655: the white wire runs as a bright diagonal and the rings as white bars across the sky behind the group (§G "bars"), acceptable as signal but they slash the frame; old Eiffel's beard unreadable at this scale. Fix: ties in with 2 (closer framing).
6. g1550-1572: swoop passes over bare green/grey avenue with no set detail until the hut at g1572; fine but empty. Non-blocking.

## s27 PASS
Round-2: 1 start FIXED (Maupassant medium, head ~190 px, eating with fork cycle, eyes shut smug, nothing over his face, no post; he sits in the restaurant, the window pane/RESTAURANT sign appear as the pull passes g1979-1991); 2 blur: auto flags g1967, 1973-1979 (8 frames) = the static hold (flat cloth/wall, frames sharp at full size), real streak in the crash g1977-1999 is the intended pull (per-frame diff 27-42, no smear frames flagged); 3 end FIXED to the extent that the whole tower is shown and a small warm amber window with ladders sits on the first platform g2000-2045; 4 table/pole FIXED (dressed room, chandeliers, round cloth table).
Notes (non-blocking): the start reads as a restaurant interior rather than "a pane in the window" (no outside visible until the pull); the lit window at the end is only ~12 px and dim: brighten it ~2x so it is clearly findable on a phone. Last 12 frames near-still, handles ok, sat/vivid/luma pass, no mouth motion, no text issue, no cuts.
