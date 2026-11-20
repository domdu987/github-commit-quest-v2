# TAKE3 QA-tech: v3/film20/s16 (T16 = shots 16+17, g1093-1220, first_g 1089, 143 frames)
Verdict: FAIL (3 blocking, 3 minor). Method: all 143 frames extracted; sheets at 6 fps plus cut +-3; qa_auto PASS (only note: planned cut g1093 has no in-take change, expected for a hard cut-in); qa_stats2 sat 0.510, vivid 48.3 %, luma 106.7, motion med 8.28 / p90 16.05, still 0 %.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeqa3/s16/ (sheetA/B/C.jpg, mid.jpg, end.jpg; all/fNNNN.png).

## Passes
- Lip-sync: grin mouth only (not animated) g1089-1116; open/closed mouth shapes change from ~g1117 to 1223 (window 1117-1223 +-0.15 s). Nothing outside it.
- Tower: full, readable in window g1089-1200, red lattice with lamp rings. Colour numbers within limits. No motion streak above 3 (fast pull-out g1098-1105 stays sharp). Handles 4 before / 11 after present. No black/magenta/frozen frames.
- Maupassant grounded with contact shadow on the tiles; laugh bounce reads.

## Issues
1. BLOCKING, plan coverage: the artists are not in the take at all. Shot 17 says "artists laugh behind"; the medium-wide g1110-1185 shows Maupassant alone in an empty room (no artist cards in any frame). Fix: add the artists (laughing, mouths closed, acting, heads y<880) on the banquettes/tables behind him, in frame g1110-1220.
2. BLOCKING, glare/floor: g1100-1165 bottom-left floor has a blown-white sun patch (white, no tile detail) with a hard blobby shadow shape; floor is ~33-38 % of the frame g1105-1165 (rule <= 25 %). Fix: lower the sun-patch intensity or move it off-frame, tilt up / lower the camera so floor <= 25 %, and give the shadow a clean shape.
3. BLOCKING, close-up size and caption band: g1205-1220 face is about 35-37 % of the frame height and the close-up phase (1185-1220 push) runs about 1.2 s (limit 1 s, face <= 35 %). meta.json itself reports head bottom max y 890 (> 880 caption band). Fix: stop the push earlier (face <= 33 %, chin above y 880), shorten the push to <= 1 s centred on g1192 ("เศษเหล็ก" 39.72 s + 0.10 = g1195).
4. Window geometry: g1089-1099 and g1175-1195 the window frame/glass shows mis-registered panes (an offset blue rectangle over the lit frame, a dark-green slab across the lower window at g1175-1200, a white sliver at the left edge g1190). Reads as broken geometry. Fix: enlarge the glass quad / view-plane behind the window so its edges stay outside the frame, remove or move the green slab.
5. Tower at the end: g1210-1220 the tower is reduced to its top over the head, and almost hidden at g1220, while he thumbs at it. Fix: offset the push so the tower stays beside his head.
6. Thumb gesture: the thumb/arm points out to the LEFT of frame (g1140-1220) while the tower is on the RIGHT; the "over the shoulder at the tower" reads wrong. Fix: mirror the arm (right arm to frame right) or put the tower on the side he points to.

## Revision 2 (take.mkv re-extracted, 143 frames, first_g 1089; 6 fps + cut +-3; frames in .../scratchpad/takeqa3/s16r2/)
Verdict: PASS (3 non-blocking notes). qa_auto PASS (same expected cut note). qa_stats2: sat 0.555, vivid 49.7 %, luma 97.5, warm 42.2 / cool 33.5, motion med 8.32 / p90 17.63, still 0 %. meta head bottom max y 848 (< 880).
Round-3 items:
1. Artists: FIXED. Painter (red beret) and composer (white hair) laugh on the banquette behind him g1099-1230 with laugh mouths; marble table with glasses at the left edge g1105-1185.
2. Floor/glare: FIXED. Floor about 18 %, white patch reduced to a few small glints (g1105-1160), no blown slab.
3. Close-up: FIXED. Face about 30-33 % of frame height at g1205-1220, chin above y 880; the push (g1185-1220) is about 1.1 s.
4. Window geometry: mostly fixed (lawn slab/stick gone); the glass edge still shows a faint offset pane at g1089-1099 and g1190 (left edge). Non-blocking.
5. Tower at the punchline: FIXED. The whole tower with rings stands clear in the right third g1190-1230.
6. Thumb: FIXED. The mirrored arm jabs over his right shoulder toward the tower (g1136-1220); QA-art items 1-3 match.
Lip-sync still only g1117-1223 (grin/laugh mouths before; artists' mouths are laugh shapes only).
Notes (non-blocking): (a) g1105-1170 the tower's right leg is slightly clipped by the right curtain; (b) the green-suited composer shows a red banquette/table bar crossing his torso g1130-1170; (c) the artists' legs look thin and rubbery.
