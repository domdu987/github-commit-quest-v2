# QA-tech TAKE gate, film 16, render team 8 (s26, s28, s29, s30)
Method: every frame decoded; 6 fps + every cut +-3 viewed at 360x640 with y880 line; frame-diff recomputed (90x160 grey, in-shot g0..g1-1); camera-parking measured by phase correlation on the upper background; qa_auto.py run on each take.mkv (all four: PASS, 0 magenta, no black/frozen). Neighbouring takes (s25/s27/s31) belong to other teams and were not available in this worktree, so cross-take continuity was checked only between s28-s29-s30.

| take | verdict | diff median / p90 (recomputed; meta says) |
|---|---|---|
| s26 | FAIL | 5.47 / 31.14 (4.38 / 27.14) |
| s28 | FAIL | 7.00 / 18.90 (6.28 / 16.45) |
| s29 | FAIL | 4.79 / 21.95 (4.00 / 18.68) |
| s30 | FAIL | 5.62 / 17.04 (4.66 / 14.04) |

## s26 (g 1707-1766) FAIL
BLOCKING
1. g 1698-1745 (click 1 = g 1733, click 2 = g 1742): the tape does not visibly spool out. At g 1702 the tape already lies fully extended over table and floor, with the same dot/dash marks in the same places at g 1727/1732; nothing grows on either click. Plan and Bible require "tape spools on ติ๊ด". Fix: key set_tape length from ~0.35 at g 1707 to full by g 1745 with a visible jump on each click (g 1733, 1742), keep the tape end in frame during the snap.
2. g 1707-1760: "congressmen crowd round, amazed" is not delivered: only one congressman (right edge, head ~50 px) is visible beside Morse and the mocker; the other two are never in frame. Fix: stage congressman_a/b/c in depth round the table (3 distinct amazed faces on the slide to the faces, g 1747-1766) or widen the opening framing.
NOTES
3. Morse ("reads the tape") grins straight at the lens and holds a loose sheet of paper (g 1762-1772) instead of the tape; eye-line should go to the tape in g 1707-1745 (use a look-down pose, or at least have his hand on the tape).
4. Heads: opening heads are only 66 px (wide), reacting mocker reaches 288 px at g 1762+ (OK, >=250). Jaw-drop swap at g 1745 sits on the g 1744 blink, good. Head bottom max y about 800 on screen (meta says 914, probably body/hat; not a head crossing).
5. g 1742-1750 set is streaked (allowed >60 px/frame), characters sharp. No pops at g 1707 / 1767 (cut frames identical to neighbours = handles only). Mouths: only the jaw-drop open mouth at g 1745+ (planned beat); no lip movement.
6. Camera never parked (min background shift 1.0 px/frame). No text, no DOF.

## s28 (g 1805-1894) FAIL
BLOCKING
1. g 1805-1894: "sacks of letters around him" is not readable. Sacks appear only as a cream smear in the foreground at g 1812-1830 and not at all from g 1835 on (just desk, baize and ceiling). Fix: rotate the arc so 3+ sacks sit behind/beside him in frame during g 1840-1894, or lower the foreground desk, and keep at least two sacks beside his legs in the opening frames (g 1805-1820).
NOTES
2. Foreground desk hides his torso/legs for g 1810-1865 (low-angle by design); feet visible and grounded only g 1796-1830. Mail bag on the belt is visible g 1796-1830 only; sash and key ring are readable (g 1875-1894, key ring held in the hand after the g 1874 swap).
3. Head size 191-378 px, head centre y 595-676, head bottom max 864 (< 880, tight): g 1880-1894 head bottom about y 840, OK.
4. Dissolve-in handle g 1796-1804 clean; diff never below 4.2, snap g 1868-1883 present. Mouth still throughout. Eye-line to lens (proud pose) acceptable.

## s29 (g 1895-1979) FAIL
BLOCKING
1. Camera parked g 1966-1988 (23 frames, background shift 0.04-0.12 px/frame; g 1966-1979 = 14 in-shot frames) after the snap. Limit is 6 frames. Fix: continue a slow push or slide (>= 0.5 px/frame) until the cut, e.g. keep the 10 %/s push going or add a 3 deg arc through g 1988; the tremble alone does not count.
NOTES
2. g 1895-1950: mocker head only 66 px (wide), clerk at right edge about 55 px; the instrument slide (planned g 1930-1950) is not legible at this size (no visible travel across the baize relative to the table edge). Consider a closer opening (medium 170-230 px) or a clearer slide path toward the mocker.
3. Smile drop at g 1952, horror pose and sweat from g 1953, snap g 1954-1965 on the planned word (g 1956): beat OK. Reacting face 256 px at the end (>= 250, OK). Blink at g 1970 fine.
4. Costume continuity with s28 correct (sash, key ring). Heads max y 762, feet on floor with shadow at g 1960-1979. Mouth: only the horror "O" (beat). No pops; diff median 4.79 / p90 21.95 pass.

## s30 (g 1980-2095) FAIL
BLOCKING
1. g 1971-2099: the mocker has NO top hat (bare grey head) in every frame, while s26, s28 and s29 all show the black top hat. Costume continuity break across the 17 f dissolve from s29, and in the end wide the viewer cannot tell who he is. Fix: use the hatted candle/yawn pose (or put the hat back on the head); the key ring and sash are present and fine.
2. g 1980-2060 (close) and g 2065-2095 (wide): the candle he is meant to hold is not readable. In the close the right hand is a translucent flat grey/amber disc at the cuff (looks like an un-composited glow sprite), the real candle in the wide is about 6 px. Fix: draw the candle in the hand as a solid prop with a small flame, remove/shrink the disc, and give it a warm light on his face.
NOTES
3. Callback not matched: Bible says shot 30 repeats shot 26's chamber_table axis at NIGHT; the take opens in a close-up from the door side and ends in a floor-level wide toward the register, not the s26 framing. Acceptable only if the director waives it.
4. Red rectangle on the vest centre (g 1975-2060) does not exist in s28/s29: costume continuity oddity. 
5. Morse peeks from the lit door (grinning) from g 2030 on, readable in the wide; before g 2030 he is out of frame (fine, he appears on the pull-back). Tape piles round the stool boots as planned. Yawn mouth open (planned beat) alternates with nod; no other mouth action.
6. Heads: centre y 636-680, bottom max 819 (OK). Pull-back: second fast pull g 2058-2070 (diff 30) is an extra accent, fine. Parking runs only 3 and 2 frames (g 2005-2007, 2080-2081), OK. No pops at g 1980 / 2096; final frames hard-cut, in-shot diff 5.62 / 17.04 pass.
