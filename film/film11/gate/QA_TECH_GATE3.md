# QA-tech TAKE gate 3, film 11 (s13 s18 s21 s22 s23 s26 s27 s28)
Method: qa_auto.py on each take (`--first_g F --cuts g0,g1+1`): all 8 = QA_AUTO PASS (no frozen runs, no black/magenta, no pops, magenta 0.0 %; only the expected "planned cut with no visible change" note on take boundaries). Frames every 5th g plus g0/g1 +-3 on contact sheets with the y 880 line, plus full-res crops (s13, s22 blink check).
Heads: all above y 880 in all 8 takes. Mouths: all closed/still in these takes (none sit in a quote window); s22 brief frames with half-lid squint are blinks (1 frame-run of ~3 frames every 40 frames). Smoke: no blob smoke visible (s26/s27 chimneys bare). Nothing on heads; no stray upright cards.

| take | verdict |
|---|---|
| s13 | PASS |
| s18 | PASS |
| s21 | PASS |
| s22 | PASS |
| s23 | PASS |
| s26 | FAIL |
| s27 | PASS |
| s28 | PASS |

## Blocking issues
### s26
1. g1624-1724 (whole shot), plan coverage: shot 26 = "a long queue of villagers to the hut, sleeves rolled". The frame still shows only ~6 small figures standing in a row behind the picket fence in the upper-middle band (heads ~25 px at 300 px width), partly hidden by fence posts; Jenner, the lancet and the hut door are not visible at all, no sleeves read, and no queue line recedes toward a hut. The lower ~50 % is bare dirt lane with puddles/stones. The round-2 QA-art FIX (re-stage as a receding diagonal queue, 9-12 villagers, heads 70-90 px at the near end, hens to the edges, Jenner + lancet at the hut door) is not done. Fix: re-stage the queue as in QA_ART_GATE2 s26 items 1-2 (camera inside/at the gate looking along the line, near figures large, line runs out of frame, Jenner at hut door at the far end), crop/lower the empty dirt.

## Non-blocking notes
- s13: the upright card is gone; James lies flat at the bed head with flush, sweat drops, pained face readable; window is deep blue (no green hill/orange panel); candle glow on mother and quilt edge. Still: subjects small, lower ~45 % empty floor, mother sits on a sack-like blob, James lies on top of the quilt (not under it), lamp shade hangs ~100 px (full res) above/left of James's head without touching. Mother not clipped at the right edge any more. Sore hidden (OK for plan: blister only needs to be consistent; hidden OK).
- s18: lamp shades hang beside/above the heads, none on a head (round-1 blocker fixed). James tiny behind the bed, laughing; no food visible ("eating"); Jenner large in front, mother clipped by the right frame edge from g1135; large cat in the foreground lower third. Sore not visible (hidden OK).
- s21: Blossom's head is now in frame; Sarah sits on the stool with hands at the udder (sarah_milk), pail under the udder; slow push-in present. Remaining: Sarah/cow occupy only the middle band, lower ~45 % is bare straw (art note); blue goose and bucket in the foreground.
- s22: open palm with 4-5 blisters beside her clear friendly face (eyes open, no sly lids), udder visible beside the hand, pail no longer in front of it. Hand is at head height (udder lower right behind the apron), so the pair reads in one glance but not touching. Large blue goose and pail in the foreground lower third. Feet/contact shadow faint.
- s23: camera trucks left to right across pockmarked group, Jenner (arm out, mouth still), clear-faced Sarah and milkmaid2, Blossom's body at right edge (head not visible, covered by milkmaid2); pockmarked man at left stands behind a barrel with feet hidden. Pocks readable only at full size. Lower ~45 % is straw with hay nest, hens (dressing). Jenner's explain pose is a single arm out.
- s27: towndoc is now the largest, unblocked figure (pockmarked villager removed); sleeve-roll is a cream strip at the cuff (subtle) and hat is off but not held in hand; Jenner with raised lancet and James at the hut at left. No queue behind the towndoc (plan says "in the queue"); legs thin white sticks with faint shadow; foreground hen/goose large g1713-1763.
- s28: cow now yaws to a three-quarter view toward camera (g1855-1870) with open round eye, half-lid + ear on g1871-1874; head still left of centre (x ~100-200 of 300) and body clipped by the right edge from g1850; lower ~45 % is empty straw; warm gold light OK. Beat delivered.

## Earlier issues, status
### QA_TECH_GATE1 (s18, s13/s21/s22/s23/s28 notes)
- s18 lamp shade on James's hair: FIXED (shade now beside, not on, his head).
- s13 g1 notes (dark, subjects tiny, floor empty, mother on sack): PARTLY (night reads, James readable; still small and empty floor).
- s21 pail in front of udder: FIXED. s22 udder hidden behind pail: FIXED. s23 characters small/feet hidden/Blossom partly in frame: PARTLY (closer camera, truck; feet of left villager hidden by barrel; cow body at edge).
- s28 cow turns head toward camera: FIXED (3/4 view toward lens g1855+); cow nose/tail edge clipping: partly (nose clear, body clipped at right edge).
### QA_TECH_GATE2
- s13 g776-846 upright 2x2 quilt patch card by James's head: FIXED (no upright card; quilt is the bed plane).
- s13 lamp shade 25-40 px above James: NOT FIXED but non-blocking (does not touch).
- s26 queue tiny/lower 60 % chickens/poor legibility: NOT FIXED (blocking above; chickens gone from foreground, queue still tiny).
- s27 villager clipped at right edge: FIXED (villager removed); s27 small Jenner/James: NOT FIXED (non-blocking).
- s28 cow nose/tail clipping, empty lower 45 %, no look at camera: look at camera FIXED; empty straw NOT FIXED (non-blocking).
### QA_ART_GATE1 / GATE2 (for these takes)
- s13 window green hill/orange panel and upright card: FIXED. Room fill still mid blue-grey (not blocking).
- s21 Blossom head cropped / Sarah beside the stool: FIXED.
- s22 udder behind pail, V-hand, sly lids: FIXED (open palm, open eyes, udder visible).
- s23 push-in + Jenner explain pose + Blossom: PARTLY (push-in/truck done; explain pose single arm; Blossom body only).
- s26 re-stage queue (diagonal, 9-12 villagers, hens to edges, Jenner at hut): NOT FIXED.
- s27 villager c in front / sleeve roll visible / hat in hand: villager removed FIXED; sleeve roll PARTLY; hat in hand NOT FIXED.
- s28 turn to lens, eye open then half-lid, head to centre: turn + eye FIXED, head still left of centre (PARTLY); empty lower area NOT FIXED.
