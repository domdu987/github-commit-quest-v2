# QA-tech sB1 (hard-defects rule, team9 2d7500a)

**PASS** (g159-301, 143 frames)

Hard defects: none.

Checks:
- Jitter g219-248 (10.1 px): this is a dive. ORB shows a smooth, monotonic camera move (ty -52 -> +11, tx +10 -> +70, rot 1 -> 5.4 deg, scale 1.06 -> 0.97). There are no sign-flipping reversals, no jump and no frozen frames.
- g298-301: clean continuation, no black, blank or flash. The camera keeps drifting steadily (ORB ty about -12 to -17, scale 1.02-1.03, diff 10.6 -> 16.9). No dissolve is baked into these handle frames, so the dissolve into B2 must be made in the edit.
- No frozen run (diff 1-22 and rising from g160), no blank or magenta frames.

Notes only:
- g240-250: sky at the top edge is blown to white above the mountains (colour/tone only).
