# QA-tech TAKE gate round 4 (B), film 20: s18 s21 s24 s25 s27
Method: ffmpeg frames (g = first_g + index), qa_auto.py + qa_stats2.py, own frame-diff (90x160 grey), viewed at 6 fps + g0/g1 +-3 + beats + full-size strips. Takes not edited.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeqa4/

| take | sat | vivid % | luma | motion med / p90 (own) | auto | verdict |
|---|---|---|---|---|---|---|
| s18 | 0.603 | 58.5 | 99.4 | 4.79 / 23.1 | PASS (soft g1390-1395 = flat orange hut interior) | PASS |
| s21 | 0.578 | 62.4 | 84.5 (night) | 17.1 / 32.2 | PASS (soft g1566-1582 swoop) | PASS |
| s24 | 0.687 | 68.2 | 91.7 | 5.73 / 16.5 | PASS | FAIL |
| s25 | 0.566 | 51.1 | 97.7 | 4.48 / 15.9 | PASS | PASS (join mismatch charged to s24) |
| s27 | 0.627 | 71.3 | 88.5 | 10.4 / 36.0 | PASS (soft g1979) | PASS |

## s18 PASS
Round 3: 1 ground slab FIXED enough (feet at ~73 % of height, bottom ~27 %, dressed with planks, discs, kegs, wagon; aerial avenue during the wire whip is travel); 2 hut glass blown / batten crossing FIXED (window crossing g1385-1394 is clean, no white panes, no batten fill); 3 pop at glass-off FIXED; round-2 carry-overs: wagon/crowbars readable, old Eiffel white beard readable, heads ~60-90 px; crane start no longer cuts Eiffel; wire reaches the ground post; telegraphist whole in frame from g1400 with hand on key and blue arc/flashes sync (head cut by left edge only g1395-1399 during the dive-in). Brown disc/ring props from round 3 are now low discs on the ground at the sides, not in front of the group.
Notes: ground ~27-29 % at g1210-1300 (limit 25, dressed); the aerial avenue g1355-1385 is a bare grey slab for ~1 s (whip travel); brown discs look like odd low-poly slabs.

## s21 PASS
Round 3: 1 ground slab 50-55 % FIXED to ~27 % (cobble texture, group heads now ~90 px, tower behind); 2 salute/bar drop FIXED (blue crowbars falling g1607-1619 and salute g1625-1630 read at phone size); 3 edge-on ring slab FIXED (rings are thin white arcs, no slab); 4 "เสาอากาศยักษ์" glow FIXED (blue-white translucent glow on the lattice g1530-1545); 5 bars across the group phase FIXED (wire and rings are gone); 6 empty swoop: avenue now has trees, lamps, lit hut (ok).
Notes: leftmost demolition man is cut by the left frame edge g1577-1663 (an extra at the edge, half his face); mouths of the cheering men are open in cheer poses (not a quote, pose cards; same as earlier rounds); wire bar is a plain white line in the rise.

## s24 FAIL (BIGZOOM 2)
Round 3 list: 1 start not extreme wide with findable Maupassant NOT FIXED / partly; 2 landing size FIXED (continuous 3.1 s, no cut, Maupassant ~16 % head, body+table ~35 % of height); 3 "window" not a window NOT FIXED; 4 s24-end vs s25-start match NOT FIXED.
1. g1724-1777: start is now a true extreme wide (whole tower, Paris, avenue, fair), but Maupassant is NOT findable: the lit window is invisible (not distinguishable) until the dive reaches the platform at g1779 (RESTAURANT sign). Fix: start with the lit window as a visible warm dot (brighten the window, add a light beam) so a viewer can spot him.
2. g1783-1852: after passing through the RESTAURANT window he lands in a red-ceiling interior with chandeliers, not "in the clear window pane": no window, no Paris/sky behind him; behind his head orange wedge bands (lattice seen from inside, stretched) fan out across g1795-1852 and read as broken geometry; the table is a blown-white slab ~30 % of the frame at the bottom. Fix: land on the window side of the table with the pane and Paris/sky behind him, same set the s25 take uses (blue sky, red bars, clouds).
3. g1853 join: s24 last frames (interior, ceiling, chandeliers, orange glasses on a white table) vs s25 first frames (window, sky, clouds, red bars, bread basket, blue glasses): only the head position/size is similar. A 9-frame dissolve would cross-fade two different rooms. Fix: ties in with 2: render s24's landing from the same camera/pose as s25 g1847.
Good: continuous move with ease, passes the lattice and the sign, motion 5.7 / 16.5, saturation 0.69, no mouth motion (still smile), only 2 soft frames, dissolve-in clean.

## s25 PASS
Round 3: 1 red bars across the face / cloth > 30 % PARTLY FIXED: bars sit left/right of his head, never over the face; tablecloth fills the bottom ~35 % at g1847-1880 (faceted, low-poly look) then the snap push moves to a close view with the Seine, bridge and park (nice); 2 p90 FIXED (15.9). Fork bite, chew, wine sip, smile, no mouth motion; head 170-330 px, max ~30 % of frame height; snap g1877-1892 reads; blue sky/Paris behind him; handles ok.
Notes: tablecloth ~35 % at the start (a white table with faceted folds); first frames do not match s24 (charged to s24).

## s27 PASS
Round 3 notes: the lit window at the end is still tiny (the whole tower is the picture from g2000, first-floor window ~10 px, not clearly findable: brighten it ~2x, non-blocking). New check: a thin black vertical line from the chair to the bottom edge at g1964-1977 (small; conform may paint it out); flags are vertical tricolours; start is the dressed restaurant (candles, fruit, bread) with eyes shut and fork cycle; crash pull through the RESTAURANT sign to the whole tower over the fair; last 20 frames near-still; no mouth motion; no text issue; handles ok; only 1 soft frame (g1979).
