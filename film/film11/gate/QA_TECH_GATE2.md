# QA-tech TAKE gate 2, film 11 (14 takes: s02 s03 s04 s06 s10 s11 s12 s13 s15 s16 s17 s26 s27 s28)
Method: qa_auto.py on every take (`--first_g F --cuts g0,g1+1`): all 14 = QA_AUTO PASS (no frozen runs, no black/magenta, no pops; magenta 0.0 %; only the expected "planned cut with no visible change" note on take boundaries). Frames at every 5th g plus g0/g1 +-3 on contact sheets with the y 880 line, plus full-res crops (s02, s06, s10-s13, s15-s17, s27).
Heads: all above y 880 in every take (lowest: s04 g314-320 James ~y 850 chin, s04 mother/James walking in).
Smoke: no blob-stack smoke visible in any of the 14 takes (chimneys visible in s03/s04/s06/s26 are bare). Lamp/herb bundle on a head: none.
Mouths: s06 towndoc mouth open only g452-476 (window starts g449, ends g546); g432-447 is the laugh_big pose (grin), not speech. No other take has talking mouths.
Sore card (viewer-side differs by pose, always the same anatomical arm: viewer-left when James faces Jenner on the left in s02/s06/s10-s15, viewer-right in s16/s17 where Jenner stands on his right): red dot s02/s06 (s04 arm not visible), blister s11/s12/s15/s16/s17, hidden s13 and during the s15 leap. Fine.

| take | verdict |
|---|---|
| s02 | PASS |
| s03 | PASS |
| s04 | PASS |
| s06 | PASS |
| s10 | PASS |
| s11 | PASS |
| s12 | PASS |
| s13 | FAIL |
| s15 | PASS |
| s16 | PASS |
| s17 | PASS |
| s26 | PASS |
| s27 | PASS |
| s28 | PASS |

## Blocking issues
### s13
1. g776-846 (whole shot, clearest g806-841): a flat 2x2 colour-patch card with a white edge stands upright beside James's head (x~100-200, y~310-400 at full res), reading as a signboard/placard on the pillow. It is presumably the quilt card over James, mis-oriented/mis-scaled. Fix: lay the quilt card flat over his body at the bed plane (or scale it to cover his body and tilt to the bed top), or hide it and tuck him under the existing quilt geometry.

## Non-blocking notes
- s02: lower ~40 % (y 760-1280) is still empty lawn with giant fence-shadow spikes (round-1 QA-art item); James's legs on the stool still stick-like; sleeve not clearly rolled. Lancet now meets the dot (good).
- s03: lower 40 % is dark empty shadow ground; goose in foreground g158-191. Villagers heads small but pocks readable.
- s04: James is clipped by the right frame edge at g314-320 and his arm/sore is not visible. Mother pulls child: reads.
- s06: a fence-post shadow falls as a flat dark-blue patch across James's cheek (g440-473); the towndoc's tall legs are thin sticks.
- s10: James is tiny at far left, behind the bed, bell-shaped lower body; mother and Jenner still stare at camera, not at his arm (round-1 note not addressed).
- s11: the thin ceiling rod with its acorn finial still shows just behind/above Jenner's wig (g669-723). Shade is gone, so not a lamp on a head, but it touches his hair line; hide the rod in room_day for this angle if cheap.
- s12: armpit rub is still a subtle arm-down gesture, wince mild.
- s13: the green lamp shade hangs 25-40 px above James's head (g826-846) but does not touch it; mother's head is clipped by the right frame edge g826-846; mother sits on a sack-like blob; lower 45 % is empty floor; subjects small.
- s15: lamp shades (room_morning) hang behind the characters, one close above James's hair at g933 but not touching; after g938 James covers mother and Jenner (Jenner's proud beat hardly visible).
- s16: lancet not visible in Jenner's raised hand (only the jar); large goose in foreground.
- s17: lancet blade is very long, tip meets the sore on James's arm; James partly hidden behind Jenner's coat; towndoc "scoff_crossed" reads as a stiff stand with arms hidden.
- s26: the queue is a row of tiny figures behind the fence (heads ~20 px at 360x640 equivalent), hut at far left edge; not a clear "queue to the hut"; lower 60 % is chickens and bare ground. Chicken pair tumbling in foreground. Poor phone legibility for a key ending shot (QA-art to judge).
- s27: Jenner with raised lancet and James are small at the hut (left); towndoc sleeve-roll is subtle; large pockmarked villager clipped at the right edge g1716-1739.
- s28: cow nose touches/clips the left frame edge g1856-1874 and tail clips the right edge; lower ~45 % is empty straw; the cow lifts her head but stays in profile, does not look at camera (the "looks round" beat is weak); warm gold light is now present.

## Round-1 issues for these takes
- s10 g621-675 lamp shade + rod on James's head: FIXED (lamp hidden; no shade; the rod ends on the bedpost).
- s12 g723-776 lamp on James's head: FIXED.
- s11 thin rod touching hair: PARTLY (shade hidden; rod + finial still behind Jenner's wig, non-blocking).
- s02/s07/s08 vs s10-s12 sore on different arms: FIXED/explained (same anatomical arm, side flips with pose; s02 dot is on the viewer-near shoulder arm and the lancet meets it).
- s02 art: empty lawn lower 40 %: NOT FIXED (non-blocking); lancet tip not meeting dot: FIXED; dot bigger and on camera-side arm: FIXED.
- s10 eye-line (stare at camera): NOT FIXED (non-blocking).
- s12 armpit rub subtle: NOT FIXED (non-blocking).
- s13 art: James barely visible: PARTLY (head and flushed face now readable, still small); night not reading: FIXED (deep-blue window, candle glow); sore card floating by head: FIXED (hidden). New defect: vertical quilt card (blocking above).
- s15 sore card floating off body: FIXED (blister on arm at start, hidden during leap); James covers Jenner after g938: NOT FIXED (non-blocking).
- s28: cow too small/dark: FIXED (cow fills frame, warm); head turn to camera: NOT FIXED (non-blocking; QA-art).
- s26/s27 (not in round 1): new, no round-1 items.
