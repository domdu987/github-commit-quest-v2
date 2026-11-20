# QA-art s21 (REVEAL B: "ในความมืด ทหารเยียนเห็นแต่สัตว์ประหลาดลายมังกร", 53.20-56.08 s), TAKE gate re-render — FIX-FIRST (reveal, strict)
I reviewed take.mkv at 6 fps (art9/gNNNN.png, g 1590-1685) at full size 720x1280 and on the 360x640 sheets art9_phone_0-2.jpg (cyan line = y 880). Snap word = g 1646.

## Earlier changes
1. Rage face: DONE. V brows, red glaring eyes, fanged roaring mouth and steam read instantly. After the snap the hero is a real monster.
2. Darkness before the flare: DONE within the director's allowance. The sky is near-black, the gate is dim, and the herd is a dull brown band until the flare at g 1630-1645 turns it blazing red. The flare reads as "out of the dark".
3. Flames: ACCEPTED. From this head-on angle the flames rise as a wall of fire BEHIND the herd (g 1645-1670), which reads as "fire behind". They no longer look like candles on the backs. Blades: bronze, per the director. But see change 3: there is no glint at all.

## Remaining problems
- **Pre-snap set, g 1590-1640:** Two flat, untextured tan posts (x 55-95 and x 615-655, y 430-790) and pale palisade spikes at both edges read as placeholder slabs (rule 2). Plain floor is about 37 % (y 800-1280). The floor is soft (QA_AUTO blur on g 1590-1629), against the client's sharp-image rule.
- **Hero face in the caption band after the snap:** The x1.5 snap and the push carry the hero ox down. Its mouth is at y about 880 at g 1650 and at y 1050-1240 at g 1670-1685. The captions "สัตว์ประหลาด / ลายมังกร" will cross the monster's mouth on the phone.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 7 | 7 | 5 | 7 | 7 |

## Verdict: FIX-FIRST
1. **Pre-snap g 1590-1640:** Hide the two tan posts and the pale edge spikes. Bring plain floor to 30 % or less with a dark lit fg prop at one lower corner (an overturned camp table, wine jars, a dropped shield). Render the floor sharp: no soft gradient patch.
2. **Snap framing g 1644-1688:** Home the snap and push on the hero's FACE, not the herd centre. Keep the chin at y 860 or above (face centre at about y 0.45) and the full face in frame through the end of the take.
3. **Blade glint:** Fire 2-3 star glints from the s22 sprite on the hero's and neighbours' blade TIPS at g 1646-1652, at least 40 px at full size, so "flashing blades" lands with the snap.

## Notes
- The three soldier silhouettes are pure black cut-outs. A thin warm rim from the fire would sit them in the light.
- The falling cup (g 1650-1660, right soldier) reads only as a small gold blob.
- At g 1685 one flame rises straight up behind the hero's horns. Shift it a little off-axis.
