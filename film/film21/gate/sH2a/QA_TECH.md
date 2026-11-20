# QA-tech TAKE gate: sH2a (film 21, H2a crane up to the trap, g1342-1395)
Frames inspected: 11 at 6 fps (full + 360x640), handle frames g1342-1344 / g1393-1395, full-size crops of P_TOP. Frames in scratchpad gate/sH2a/fr and hd.

## VERDICT: FAIL (2 blocking issues, 2 non-blocking)

## qa_auto "suspected blur" (g1342-1358): NOT blur, no fail
Laplacian variance (my measure) is lowest on g1342 (342) and rises monotonically to 1132 at P_TOP; g1342 is crisp at full size (faces, moustaches, helmet rims, grass blades all sharp). The flag comes from smooth sky/water/sand at the start and fast-moving sand in the crane. Motion streak is mild and acceptable for a fast crane. No DOF in the render. Ignore the flag.

## Blocking issues
1. g1360-1395 (cork image, esp. P_TOP): colour is garish and over-bright. Meadow is a clipped yellow-orange slab (about 13-18 % of pixels have R and G both >= 250), cyan-white neon glow rim on the river, whole frame sat 0.84-0.86 from g1360 on (take 0.75 average), mean luma 111-119 at P_TOP (limit 85-110, flagged by the take's own average 109.3 hiding the end). Fix: pull the key down 1-1.5 stops and cool the sand from yellow to a warm ochre/straw, drop bloom/rim on the river edge (white rim is clipped), target end-frame sat <= 0.70 and luma <= 105, no large clipped yellow area.
2. g1372-1395 (the story read): the plan image is not readable on the phone sheet. (a) The English boxed in the loop are dark brown/black dashes on yellow, with only a few red/blue pixel heads; they do not read as crimson English. (b) The Scots spear wall at the bridge mouth is a dark cross-shaped smudge on the bridge, the only blue is one tiny saltire banner (about 6 px); no blue spear wall visible. (c) The south-bank half is two beach umbrellas at the bottom edge, not an army. The loop itself reads as a light bulb/omega, which is acceptable as the bottle-and-cork if the contents read. Fix: render the meadow army as crimson blocks (bigger, saturated crimson tabards, upright, not dark sticks), make the spear wall bigger and blue (wider ranks, blue banner flags on poles clearly visible), put a visible English group on the south bank in crimson.

## Non-blocking notes
3. g1357-1372 (mid crane): the crane passes quickly through rich set (tents, bridge, river) then abruptly to a bright flat meadow at P_TOP; the placeholder meadow army (about 10 px figures) looks like laid-down dashes. Acceptable only if issue 2 is fixed.
4. g1347-1357: grass/ground close to the lens is rather large soft shapes; fine.

## Other checks
- Floating: no. Neck troops have contact shadows (g1342-1350); meadow placeholders have shadows; nobody hangs in the air. Scots wall at g1350 stands on the sand next to the bridge.
- Text: none visible.
- Handles: g1342-1344 continue H1's descent (English crimson/blue in foreground, Scots wall + bridge behind, sky and hills): consistent. g1393-1395 drift is nearly static, fine.
- Caption band (y >= 880): at P_NECK the English heads are above 880 (nothing cut by frame edge); at P_TOP only the bridge and a few specks sit in the band.
- Camera: crane up is a strong high/top-down angle, satisfies section H angle variety; the move is smooth, no pops.
