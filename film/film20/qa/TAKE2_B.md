# QA-tech TAKE gate round 2 (Stricter QA B + sections G, H, I), film 20: s18 s23 s24 s25 s26 s27
Method: all frames extracted (g = first_g + index); qa_auto.py (with --out into scratchpad, take folders untouched) and qa_stats2.py run on each take; frames viewed at 5-frame step plus cut/beat frames and crops. Takes not edited.
Numbers (sat / vivid% / luma / motion med / p90): s18 0.618/56/97.9/4.94/22.4 | s23 0.564/50/94.4/7.30/11.45 | s24 0.627/64/102/5.05/12.03 | s25 0.550/51/105.8/5.66/11.68 | s26 0.535/53/99.2/6.11/12.46 | s27 0.610/70/95.2/10.92/27.5. Handles/n_frames correct in all six. No black/magenta/frozen frames, no tofu (banner text in s23 is sharp Latin), no mouth motion, heads < 880 everywhere, no cuts inside s18.

## s18 (shots 18+19+20, travel) -- FAIL
1. g1210-1300: bottom 45-55 % is still a bare flat blue slab (round-1 issue 1 NOT fixed; limit 25 %). Fix: tilt up / lower the camera or dress the ground with props, ruts, crowd.
2. g1210-1260: figures tiny (heads 12-40 px) and clustered at the far left behind a hut; wagon + scrap cart read only as brown blobs until the crane (g1311). Old Eiffel only reads from ~g1265. Fix: start nearer the group / wider framing of the wagon with crowbars.
3. g1311-1316: old Eiffel (and the group) are cut by the bottom frame edge while the crane starts. Fix: keep him inside the frame through the crane start.
4. g1346-1356: the wire does not reach the ground, it ends at the hut roof (plan: whip DOWN the wire to the ground); also 5 soft frames g1387-1395 (limit 3 on whips). Fix: run the wire visibly to the ground post and shorten the dive blur.
5. g1388-1389: window glass blown to pure white (4 white panes); g1391-1397: black square at the window mullion junction (broken geometry). Fix: lower the glass emission, fix the junction mesh / hide the post.
6. g1396-1434: telegraphist's hand never touches the key (round-1 issue 1 NOT fixed): arms hang by his sides, lever and balls are tiled to his right. The spark arc between brass balls is now visible (ok) and flashes sync. Fix: arm to the key knob with a forearm dip on each tap.
7. g1210-1300: contact shadows under the group are weak on the slab (small figures float-ish). Fix: darker contact decals.
Beats OK: point up g1300-1306 reads; crane to summit g1311-1341; whip tilt g1346-1356 reads; through-window g1386-1400 lands on the telegraphist.

## s23 (shot 23, 1910) -- FAIL
1. g1706-1739: bowler "doff" still reads as a flat black dish at chest height (round-1 issue 2 NOT fixed). Fix: raise it to head height / hat-tip with a visible hand, or turn it so the crown shows.
2. g1693-1739: official walks out of frame right and is cut by the edge (g1693-1708), then is gone: the "hands a NEW sealed document" beat is not on screen after g1676; Eiffel already holds the seal at g1648. Fix: keep the official in frame through the hand-over.
3. g1708-1739: Eiffel is cut at the thighs/knees by the bottom edge and the tower/banner leave the frame (callback framing lost), head ~27 % ok. Fix: pull back a little at the end.
4. p90 11.45 < 12. Fix: stronger snap.
Round-1 fixes OK: black lamp-post/clipped FG at right gone; ground slab now < 25 %; old Eiffel white beard continuous.

## s24 (shot 24, BIGZOOM 2) -- FAIL
1. g1724-1779: start is not an extreme wide on Paris + whole tower with a findable Maupassant: the tower fills the frame, the window speck is invisible until g1779. Fix: start higher/further so the whole tower + Paris + the lit window are in frame.
2. g1819-1858: landing is a medium-wide (head 165 px = 13 %, body + table ~30 %), plan 35-60 %. Fix: land closer.
3. g1784-1858: the "window" is not a window: flat orange/grey bands, no pane, no Paris view, no girders, no light shaft; looks like a bare backdrop. Table is a faceted low-poly disc on a thin pole. Fix: show the clear window pane + Paris behind him and a proper table.
4. g1858 -> s25 g1853: match-dissolve framing mismatch: s24 ends on an orange band room, s25 starts on a blue sky window with red bars; head x/scale differ. Fix: same set/pose/framing at the join.
5. g1783-1791: 6 soft frames during the lattice pass (ok, <=3 allowed per whip; this is a push, acceptable if shortened).
OK: continuous move 3.2 s with no cut; dissolve in clean; motion 5.05/12.03; no mouth motion.

## s25 -- FAIL (minor)
1. g1847-1879: red bars cross behind/at the face line of Maupassant and the table (blown white cloth) is > 30 % of the frame; matched framing with s24 end absent (see s24-4).
2. p90 11.68 < 12. Fix: stronger snap push.
OK: fork bite, chew, wine sip, smile only, head 171-331 px (< 35 %), snap on g1877-1892, vivid sat.

## s26 -- PASS (minor notes)
Notes (non-blocking): g1944-1968 white tablecloth fills about 30 % at the bottom; thin black dash artifacts at the mid-right g1920-1944 (clipped geometry); red pole passes behind his head g1944-1964. Over-the-shoulder push to the window works, Paris and Seine visible, no tower, glass raised, nobody half-cut. Stats pass.

## s27 -- FAIL
1. g1964-1976: planned start "Maupassant in the clear window pane" is not there: he sits in the same bare orange-band room on a pole table with a wooden post crossing the frame at left (g1967-1976), not a window; also does not match the s26 view (blue sky/Paris window) at the hard cut g1967/1968. Fix: start on the window pane framing from tower_window_pull with nothing over him.
2. g1964-1978: qa_auto FAIL, 16 frames flagged soft (limit 3 on the crash); shorten the blur to <= 3 frames.
3. g1979-2045: end is the whole tower but Maupassant is no longer findable (plan: tiny Maupassant eating in the first-floor window); last 12 frames still ok. Fix: end framing where the lit window is findable.
4. g1964-1973: table floats on a thin pole, faceless shadows (geometry).
OK: crash pull-out reads, stats pass (motion 10.9/27.5), no mouth motion, no text.
