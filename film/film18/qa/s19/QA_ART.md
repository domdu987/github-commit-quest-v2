# QA-art s19 (attack: oxen burst out of the wall holes, 47.56-50.51 s), TAKE gate re-render — FIX-FIRST (reveal, strict)
Reviewed: take.mkv at 6 fps (every 5th frame, art6/gNNNN.png = global frame g) at full size 720x1280 and on the 360x640 phone sheet art_phone.jpg. Scores 1-10.

## Earlier changes
1. Nearest ox at least 2.5 D away and at most 50 % of frame height: DONE, but overcorrected. The oxen are now about 8-12 % of frame height (y 760-960), small on the phone.
2. Flames on the tail tips, capped, leaning back: PARTLY done. They are on the tips, but the tails curl up over the back, so each flame is a small (about 25x45 px) upright torch tip above the rump. The tails look like held torches, not burning tails. Flame size is about 1/8 of the body, against the 1/3 asked for.
3. No empty-wall frames before the whip: DONE (the whip starts at g 1498 with oxen in frame).
4. Warm light from the tails: weak. Small pools are visible under the oxen at g 1441-1471. Good, but faint.

New problems:
- A flat untextured purple stripe runs diagonally across the lower left (x 0-560, y 1000-1280) in every frame, and a navy band sits along the bottom edge at g 1421-1456. This breaks rule 2.
- Translucent teal low-poly spikes (grass?) stand on the ground and read as ice shards (rule 2).
- Plain ground is about 35 % of the frame.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 6 | 6 | 5 | 6 | 6 |

## Changes
1. **Placeholders, whole take:** Hide the purple diagonal stripe and the navy bottom band, or replace them with the textured moat bank/bridge. Hide or retexture the teal spikes as dark green-brown grass tufts.
2. **Flames, whole take:** Make the tail pose trail BEHIND the ox (tail out level and backward, not curled up over the back), with the flame card about 1/3 of the body length, streaming horizontally backward with sparks. Raise the per-tail light so each ox throws an orange pool and rims its own rump and coat. On a phone, "fire on the tail, behind the ox" must be readable in this shot.
3. **Framing, g 1427-1498:** Move the camera to about 10-12 D from the holes (from 16+ D) and lower the look-at, so the oxen leaving the holes are 18-25 % of frame height and plain ground is 25 % or less. Keep the nearest ox below 50 % height and out of the lens path.
