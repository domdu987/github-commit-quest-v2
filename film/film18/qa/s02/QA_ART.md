# QA-art s02 (hook 2: blades + herd reveal, 2.59-5.20 s), TAKE gate re-render — FIX-FIRST (hook)
I reviewed take.mkv at 6 fps (art9/gNNNN.png, g 78-163) at full size 720x1280 and on the 360x640 sheets art9_phone_0-2.jpg (cyan line = y 880).

## Earlier changes
1. Dressing material: DONE. The dressing is removed. No navy or violet spikes or lumps are left.
2. Violet band between the herd and the wall: NOT DONE (third round). A flat, unlit navy-violet sheet lies under the far rows from g 108 to g 163. At g 153 it covers x 200-500, y 420-640, and on the phone it is the largest flat shape behind the herd.
3. Woman clear of the edge: DONE. She stays whole and right of the left edge for the whole take, with her head above y 880.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 7 | 7 | 6 | 6 | 8 |

On the phone you see a calm clerk holding a bronze blade up at the horn of a dragon-silk ox. The crane then rises on a lane packed with dressed oxen under a blue moonlit sky and a warm wall. The hook reads. The only thing that looks broken is the violet sheet.

## Verdict: FIX-FIRST (one change)
1. **Violet band, g 108-163:** Use the s19 fix. In s19 the purple strip was a hole in the set's ground, and the world colour showed through it. A dark earth plane (`gapfill`) placed just under the ground fixed it. Put the same kind of plane (lane dirt colour, dark brown) under the herd lane between the herd and the wall base, and check g 153 for zero flat violet pixels behind the herd. If that fails, a warm fill light on the strip is the fallback.

## Notes (not blocking)
- Plain dirt is about 28-30 % from g 113 to the end, which is a note band. A dark fg prop (basket, trough) at a bottom corner would bring it under 25 %.
- At g 78-98 Tian Dan's face is cropped about 20 % at the left edge. It is acceptable as an over-the-shoulder start.
- The blade is held near the horn rather than visibly tied. With the narration this is fine.
