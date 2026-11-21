# QA-tech film17 s01 ROUND 2 (shots 1-3) - VERDICT: FAIL (2 blocking, 3 minor)
Checked: 40 frames (every 5th + cuts +-3) plus g64-71 and g124-149 pulled frame by frame from take.mkv. Accepted per director: jaws straddling ear front/back (shot 3); gendarme mid-room. Numbers accepted (soft g131-132 = whip blur, seen, OK).

## Round-1 items
1 prop on ear s1: PARTLY fixed - tip now reaches the prisoner's ear, but still no hand grips it (see R2-1).
2 headrest slab over forehead: FIXED.
3 far ear clipped s1: FIXED (both ears in frame).
4 s2 coverage: FIXED enough - queue on bench (bowler + 2 more) in frame, chandelier fg, next prisoner stands in queue; gendarme mid-room accepted; fg box/book stack bottom-left. No gas lamp fg (chandelier instead) - non-blocking.
5 s2 scale: FIXED - camera push g64-93 is smooth (checked g64-71, no pop), floor empty area reduced.
6 gendarme colour drift: not re-seen (gendarme green, constant g48-65). Closed.
7 s3 calipers on ear: FIXED in geometry (jaws on the ear, low-ish framing) - but no hand (R2-1).
8 heads in caption band: FIXED (chin y ~790 in s3/s1, nothing >=880).
9 sitter swap: PARTLY fixed - swap at g126->g127 now happens inside the whip (blur + background motion g125-132), reads as a snap. But see R2-2.
10 same bowler man as gendarme: FIXED (new sitter is green coat + blue beret).
11 stray white head top-left: FIXED (nothing at g138-149 except Bertillon's head cropped at left edge, normal).
12 calipers drift: NOT fixed, worse (R2-2).
13 eye-line: Bertillon looks at camera, minor, accept.

## New / remaining issues
R2-1 (BLOCKING) g0-47, g93-131 (also g48-93): calipers have no hand. In s3 the bar emerges from behind Bertillon's beard/chest and crosses his torso with no arm or hand holding it (a white stub at left looks like a cuff only). In s1 the rod runs over his chest, hand not visible. Fix: put a hand sprite on the caliper handle (the dark round hand already used on the actors) at the grip point and a visible forearm, in front of the torso.
R2-2 (BLOCKING) g131-149: after the snap the calipers vanish. g127-130 jaws sit on the new ear, g131 (whip peak) they are gone and never return; g132-149 the new prisoner's ear is bare, only a white blade stub by Bertillon's tie remains at g132-136. The "snap to the next ear" beat ends with no measurement. Fix: keep the calipers (jaws + bar) pinned to the new ear anchor through g149, or make them re-close at ~g138.
R2-3 g0-47, g48-93, g93-125 (minor): prisoner's coat hem / lap shows a blocky stepped notch against the chair seat (rectangular cut at the knee, visible at phone size); legs between the chair rails read as standing, not seated. Fix: re-order the chair seat/arm over the hem or smooth the mask.
R2-4 g70-90 (minor): caliper bar crosses the prisoner's eye/brow in the push-in; looks like it pokes his eye. Fix: lower the jaws to the ear or drop the bar below the face.
R2-5 g0-47 (minor): Bertillon's face has a dark polygon notch left of the beard (hair/face mask seam) at g0-47 and g93-125 close-ups. Fix: clean the head sprite mask.
Fix R2-1 and R2-2, then re-check g0-47, g93-149.
