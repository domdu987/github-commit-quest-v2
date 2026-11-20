# QA-tech round 14 s24: FAIL
Checked: all 87 frames; 6 fps phone sheet; action band (y 430-886) every 3rd frame g1801-1887; chariot 1:1 crops g1871/1881/1887; soldier chins on frames; ground sand mask; frame-diff 90x160 (director 12.14 / 17.31).

## Blockers
1. Only ONE visible fall in open ground (need >= 2). The moustached soldier at the left sits with legs splayed about g1861-1881 (x 0.05-0.30, chin ~y 800): clear. A second soldier on the ground: none. In every sampled frame g1801-1887 all other soldiers stand, run or crouch upright; none sits, falls or lies. (g1861 the left soldier is crouching into the sit; the helmet/pot props land on the ground but no second soldier.) Fix: make a second soldier at x 0.55-0.90 do a visible pratfall/sit-down held >= 12 frames in the open between g1825-1870, body >= 120 px tall, not behind the fire pit, chariot or tents.
2. Chariot pole too long: wheel+box about 120 px = 17 % of the frame width (limit 18 %: OK), but with its pole the chariot spans x ~160-392 at g1881 = 232 px = 32 % of the width (g1887 31 %), limit 25 %. Fix: shorten the pole to <= 60 % of its current length (<= 180 px total).

## Asked checks (pass)
- Ground: plain sand 3.6-8 % (sand mask g1807 / g1831 / g1851 / g1871); floor fully dressed. OK (<= 30 %).
- Chins <= 860: standing runners 700-840, the sitting soldier ~800-850; none over 860 in g1807-1882.
- Props warm and moving: pots and helmets in golden/terracotta yellow, flying in arcs (positions change each frame g1813-1887); chariot warm wood, rolling/tipping across g1840-1887. None hangs still.
- Rim: cool blue rim on every runner; fire pit key in the centre; warm + cool in frame.
- Frame-diff fine, no pulsing, mouths held, no text, no placeholders, subject in frame.

## Notes
- The scene is very wide: soldiers are only 130-190 px tall, so a fall must be big enough (>= 120 px) to read.
- Helmets/pots are flat glowing yellow (note, slightly translucent); the fire-pit flames are 3 stiff red wedges at frame centre all shot, they hide a lot of the action.
- Dense ground clutter (pots, stones, bundles) is busy but grounded.
