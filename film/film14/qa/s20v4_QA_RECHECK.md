# QA_RECHECK film 14, take s20 v4 -- shot 21 only (g 1368-1452), TAKE gate round 4 (blocking only)

Scope: shot 20 is replaced by s19 at conform (not reviewed). Shots 22-24 (g 1453-1683) must be unchanged.
Checked: every 3rd frame g 1368-1460, cut 1450-1456, every 2nd frame of the hive band (y 760-1240) g 1374-1444, full size
(g 1371/1398/1404/1410/1425/1440) and phone size (240/360 px tiles, cyan = y 880). Frame-diff on every frame g 1362-1461.
22-24 vs the v3 take (r10): mean abs diff <= 0.71/255 on every frame g 1453-1683 (encode noise only); spot views g 1500/1600/1670 identical.
Sheets: scratchpad/rq21/{p1,p2,band,f1,f2,f3,spot}.jpg

## Verdict: **FAIL** (1 blocking item: no knock)

## Checks
- Swing wave down the row: **YES, acceptable.** Camera tracks along the row; each hive tilts 30-40 deg in turn
  (u3 ~1377-1386, u2 ~1395-1402, u1 ~1410-1418, u0 ~1428-1440). Only 1-2 hives are in frame at once, so it reads as
  "one hive after another swings" rather than the whole row at once, but the travel is clear.
- Neighbouring hives knock: **NO -- BLOCKING (same as round 3).** Each hive still hangs under its own roof frame and the
  neighbours never touch. The alternating swing gives screen-space overlap only (e.g. g 1408-1410 the near hive's end
  passes in FRONT of the next one, which is a stand further back). No contact, no dust/wood puff, no shake: the frame-diff
  curve is smooth (8-10/frame) with no 2-3 frame spike anywhere in 1368-1452. The narration "swing and knock together"
  is only half shown.
- Bees: **PASS.** No bees g 1368-1443. First small puff at u1 g 1444, a few more 1446-1452, then the shot-22 burst at 1453.
- Ground: **PASS** (~15 % red dirt). New framing note (non-blocking): sky is now ~55 % of the frame and all hive action sits
  at y 900-1250, i.e. below the caption band line -- a subtitle will sit on top of the swing on a phone.
- Pops / frozen / broken: none blocking. Cuts 1368 and 1453 are clean hard cuts; no frozen runs; camera stops at g 1429
  (diff drops 9.7 -> 4.9) but hives keep moving. Minor: thin bright-yellow sliver on the ground g 1398-1406 (lower centre),
  a lone roof edge floating at the right frame edge g 1371. Blur flag from QA_AUTO is the known false positive (stars and
  board edges sharp at full size).

## Fix (one, cheap)
Make two neighbours actually collide inside the frame: put the hive pair the camera passes at g ~1405-1420 on adjacent hooks
of ONE frame (or move u1 toward u2 so their swing arcs overlap in depth), swing them out of phase so the boxes meet at the
apex 2-3 times, and on each contact add a small wood/dust puff + 2-frame camera shake. Optionally raise the camera aim
~10 deg so the hives sit above y 880.
