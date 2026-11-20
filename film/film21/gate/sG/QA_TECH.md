# QA-tech sG v2 (team8 fddc54e)

**Verdict: PASS** (content only; colour numbers ignored per policy). No blocking items. 4 non-blocking fixes recommended.

## Cut / jump check (rhythm.py "1 CUT")
Frame-difference (90x160 grey, mean abs diff) over g1141-1238: there is NO isolated spike. Diff climbs smoothly 5 -> 32 (g1142-1163), peaks 58-83 at g1169-1175 (max 83.5 at g1173), then falls 50 -> 21 by g1186. Same terrain features (ridge, boulders, trees, Scots on the slope) are visible on both sides of g1172/g1173, so it is one continuous camera move, not a hard cut. The detector fires on the fast top-down arc (the whip through the light shaft), not on an edit. The planned snap is g1194-1196 (diff 15-19) and reads as a push, not a cut. Verdict: NOT a hard cut, non-blocking. Note the pitch change g1172->1173 is violent (almost a jump); see issue 1.

## Old items
1. Pine / canopy / boulder skim g1146-1160: FIXED. No pine canopy or boulder over the lens now. Remaining: a dark ledge rock at the bottom (about 25%) g1141-1156, a dark slab top-left (about 8%) at g1160. Acceptable.
2. Opening unreadable: MOSTLY FIXED. The bridge now spans the frame, the crimson/gold English column on the deck and causeway reads as two-by-two, and the army massed at the causeway mouth reads as about half over. The yawning knight is still tiny (head about 30 px at 720 wide, g1147-1160): the helmet and figure read, the yawn does not at phone size. Non-blocking (plan says "tiny but readable").
3. Top-down noise g1161-1181: PARTLY FIXED. Scots and the ridge now stay in view at g1166-1172 and g1178-1181, but g1173-1176 is still a fast top-down frame washed out by the light shaft (see issue 1).
4. Only 5 Scots / no shafts in the low shot: PARTLY FIXED. About 5 hero Scots plus 6-8 small ones along the ridge; pines and a shaft show at g1181-1185 only, low shot g1187-1238 has a sky, cloud and pine line but no visible shaft. Non-blocking.
5. Spear across faces: FIXED (no foreground spear over faces in g1187-1238).

## Checks
Heads above y 880: pass (heads about y 500-820). Face size: horn blower about 9-10% of frame height at g1206-1238, pass; the g1141-1156 Scot head is large (about 19% of frame height), fine as foreground. Nothing floats: pass. Edge cuts: the left helmeted Scot is cut by the left edge at g1141-1147 and the right-edge Scot at g1206-1238, non-blocking. Colour story: Scots blue, English crimson/gold on the bridge, pass. Acting: horn up g1196, cheeks puff, readable at g1206; Wallace lifts the sword arm; nobody else's mouth moves. Bloodless: pass.

## Issues
1. NON-BLOCKING, g1172-1177 (worst g1173-1176): a fast top-down whip, light shaft blown out, boulder and orange trunk blobs, no story. Fix: cut the shaft intensity or opacity by about 50% here, or ease the arc so peak diff stays under about 50 and the pitch change spreads over 12+ frames.
2. NON-BLOCKING, g1186-1187: motion stops dead (diff 21.7 -> 1.7) and the frame is static g1187-1193. Fix: ease out over about 6 frames, or start the push on g1187.
3. NON-BLOCKING, g1147-1160: knight's yawn not readable at phone size. Fix: scale x1.5 more or add a bigger jaw drop and hold.
4. NON-BLOCKING, g1166-1171: dark ledge box fills the lower left (about 25%) and a green canopy the right (about 20%) at g1170-1172. Fix: lateral nudge of the camera or hide the ledge prop.
5. NON-BLOCKING, g1187-1238: add a visible light shaft and 4-6 more Scots on the slope if cheap.
