# QA-tech round 13 s24: FAIL
Checked: all 87 frames at 6 fps; soldier band y620-920 with y860 line every 6 frames; full 1:1 g1821/1846/1876; frame-diff re-measured 90x160 (median 11.75, p90 17.20).

## Blockers
1. Prop wider than 20 % of the frame: the tipped chariot with its pole. Measured on 1:1 frames: g1849 about 36 % of the width (x 150-410), g1876 about 61 % (x 0-440 box+pole), g1881-1886 about 75 % (x 0-540). The box alone is about 17-28 %; the long pole makes it a bar across the lower third. Fix: shorten or hide the pole (<= 0.3 of its present length) and keep the whole chariot <= 140 px wide in g1843-1886.
2. Only ONE visible fall. The moustached soldier sits with legs splayed g1850-1875 at x 0.10-0.27 (chin about y 850). I find no second soldier on the ground in any frame: soldiers at g1807-1849 stand or step in place with "O" mouths, the other soldiers in g1855-1885 stand upright. QA.md says six fall; they are not visible. Fix: make a second soldier at x 0.55-0.85 do a pratfall/sit-down held >= 12 frames in the open between g1825-1870, >= 120 px tall, not behind tents, fire pit or the chariot.
(The rout reads weakly overall: most soldiers stay within 150 px of where they started; at least 2 more should visibly run across the frame.)

## Checked and passed
- Ground: now heavily dressed (pots, stones, bundles, helmets, fire pit); no bare ground, about 0-5 % plain. Dense clutter: note.
- Props warm, not grey: pots terracotta-yellow, helmets gold, chariot warm wood. Flying pots/helmets about 90-130 px (13-18 %): OK. They move every frame (positions change per frame across g1813-1886), none hangs still.
- Chins: sitting soldier chin about 850 (g1855-1873), standing ones 700-840, none over 860.
- Frame-diff 11.75 / 17.20; no pulsing; mouths held; no text; subject in frame. Flame only the camp fire (set prop).

## Notes
- Helmets and pots are flat yellow, slightly glowing/translucent, no texture (note).
- Pale flat white cloth slabs at left (g1849-1861) and lower right (g1879+) are untextured planes (note).
- Fire pit flames are 3 stiff tall red cards (note).
