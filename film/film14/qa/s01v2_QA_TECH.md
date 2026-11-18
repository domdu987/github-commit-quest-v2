# s01 v2 QA-tech (TAKE gate, strict)  VERDICT: FAIL (2 blocking, small fixes)

Checked: 187 frames at 6 fps (37 frames, sheets at 360x640), g63-69 and g120-126, extra g0/8/16/24/32/40/44/48/60 and full-size g0/40/100/160.
Numbers: cuts at g66 (diff 53.2) and g123 (46.2) exactly on plan; one more spike at g44 (11.9) and g1 (8.5), see below. Every other frame diff 1.3-4.6 (camera always moving, no frozen run).

## v1 blocking items
1. Stray grey tub over the kid (shot 2): FIXED. Gone; kid/woman clear.
2. Foreground clutter shot 2 (fowl, leaves, pumpkin, sack): FIXED. Lower third is bare laterite plus a few grass blades and one rock.
3. Farmer + hung hive tiny in shot 2: PARTLY. Now framed with ladder, tin roof, hive and farmer in the middle third, villagers as side wedges, so "they laugh at the fence" reads. Farmer is still only ~7 % of the width and the hive ~12 %; the top 35 % is plain gradient sky (acacia only). Non-blocking now; closer camera would help.
4. Eye-lines/pointing (shot 2): PARTLY. Villagers are now side wedges, the kid (left) and old man point/lean toward the centre, the youth's arms are lowered/angled. Everyone still has squeezed-shut laughing eyes toward the lens, so no true eye-line to the hive. Acceptable for laughing cards; non-blocking.
5. Stray stick under the woman's shoe (shot 2): FIXED. No spike under feet. (Thin sticks lie on the ground bottom-right g16-60 and g130-186; read as ground litter, non-blocking.)
Non-blocking v1 items: 6 contact shadows PARTLY (woman, youth and farmer ok; kid (green) and old man feet still only faint shadows). 7 hook_close FIXED in size (farmer ~40 % width, ladder clear, woman no longer covers it). 8 shot 3 sweep PARTLY (camera drifts and his arm waves from ~g150, no real sweep to the hills; always moving, not static). 9 farmer beside hive in shot 3: FIXED (both in frame, he stands right of the ladder, hive and bees at left). 10 shot 3 corners: FIXED (no foreground props).
QA-art items: hive readable with bees (FIXED), sky share (PARTLY: g0-65 ~35 %, shot 2 ~40 %, shot 3 ~25 %), foreground cleared (FIXED), mountain/huts back in shot 1 and 3 (FIXED).

## NEW issues
A. BLOCKING g0 -> g1: hive missing at g0. Farmer holds nothing at g0 (hands out, bees floating) and the hive pops in at g1 (diff 8.5, Hook frame). Fix: have the hive in his hands from g0 (key set_uncle_hive/hive card from the first frame).
B. BLOCKING g44: hive-in-hands is swapped for the hung hive with a pop (diff 11.9), the camera also jumps framing. The hive never visibly leaves his hands, the hang beat (hook) is not shown. Fix: parent the hive to his hand until the release, then tween it onto the wire over 6-8 frames (or hide the swap with the roof wipe).
C. BLOCKING g16-65 (shot 1): green kid head is at y ~850-935 (face centre ~885-900), i.e. in the caption band, and half cut by the right edge. Fix: move the kid up/left so the head is above y 840, or drop him.
D. Farmer on ladder parenting: OK in all shots. Feet stay on rungs, ladder fixed, no slide; shot 2 the farmer's feet at the rung under the roof, ok. (Shot 3 he is off the ladder, standing on the ground: planned.)
E. Hive in hands g1-43: held at shoulder, sits behind his head/arm; left hand is on the ladder side. Reads as carried, not clipped. Non-blocking.
F. Heads: shot 2 and 3 all heads below y 880 line OK (youth ~740, old man ~730, kid ~820, woman ~630-700, farmer shot 3 ~470). Only C violates.
G. Clutter: shot 1 foreground now rocks and seedlings only. Shot 2 foreground grass tufts left of the ladder partly hide the kid's legs (minor).
H. Continuity vs s02: not available to check.
I. Mouths: no talking mouths (open laughing shapes held), OK.

## Remaining blocking (send back)
- g0-1: hive absent at g0 then pops in. Fix: hive in hands from g0.
- g44: hive swap pop; hang not shown. Fix: parent to hand then tween to the wire.
- g16-65: green kid head at y ~885-935 inside the caption band, cut by the right edge. Fix: move/raise him or remove.
