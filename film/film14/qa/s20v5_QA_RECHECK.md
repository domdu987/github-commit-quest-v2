VERDICT: FAIL -- 1) knocks not readable (u2 g1405 has no spray, the others happen at the right frame edge with no visible contact or jolt); 2) dust is a clump of flat cards, not a spray crown; 3) shot 21 is not graded for night and does not match shots 20/22.

# QA_RECHECK film 14, take s20 v5 -- shot 21 only (g 1368-1452), TAKE gate round 5 (blocking only)

Scope: shot 20 is replaced by s19 at conform (not reviewed beyond the cut). Shots 22-24 (g 1453-1683) unchanged.
Checked: all 383 frames extracted (n = g - 1301) to scratchpad/takes/qa_s20v5/f/. Phone sheet of every 3rd frame g 1362-1460
(180 px tiles, cyan = y 880). Every knock +-3 frames at 360 px (g 1385-1391, 1402-1408, 1419-1425, 1435-1441). Full-size
crops of the knocking hive (x 400-720, y 380-880) at g 1386-1390 and 1403-1407, plus 2x crops of the dust at 1389-1392, 1423-1426
and 1439-1442. Cuts 1365-1370 and 1450-1455. Frame diff on every frame g 1361-1461, a white-chip pixel detector over g 1368-1452,
and sky/ground share and sky colour at 10 frames.
Sheets: scratchpad/takes/qa_s20v5/{phone1,knock1388,knock1405,knock1422,knock1438,jolt_zoom,puffs_zoom,cut1368,cut1453}.jpg

## Verdict: **FAIL** (3 blocking items)

## Checks
- Swing wave down the row: **YES, acceptable.** The camera trucks along the row and each hive tilts hard in turn. The wire is
  visible and bent. As in v4, only 1-2 hives are in frame at once, so it reads as "one hive after another".
- Knocks visible: **NO -- BLOCKING (round 3 and 4 item still open).**
  - u3 at g 1388: a puff appears at the hive's entrance end in open corn. No post is at that point, so there is no visible
    contact. The puff then drifts to the right frame edge and leaves it (g 1393, x 629-719).
  - u2 at g 1405: **nothing at all.** The chip detector finds no spray in g 1402-1411, and the crops show no contact and no jolt.
  - u1 at g 1422: the puff is at x 589-719 and cut by the right frame edge at g 1426-1427.
  - u0 at g 1438: the puff is mostly hidden behind the hive (g 1440-1445).
  - Jolt: the claimed 2-frame jolt of hive, posts and roofs cannot be seen. The frame-diff curve is smooth (14-18 per frame)
    with no 2-frame spike: about +1 over neighbours at 1389 and 1438, nothing at 1405 or 1422. Side-by-side crops show no
    displacement of roof or post.
  - At phone size each puff is a 15-25 px beige smudge at the edge of the tile.
- Dust form: **FAIL -- BLOCKING.** At 2x zoom the "spray" is a dense clump of flat tan square cards with white squares on top,
  about 60-100 px. It reads as a lumpy ball stuck to the hive end. There is no crown shape, no radial spread, no separated
  droplets or chips, and no arcs. These are not round white blobs any more, but they are still a blob.
- Framing / y 880: **PASS (minor).** Sky is 21-33 % (fixed from 55 % in v4). Ground is about 20-25 % rather than the claimed 15 %.
  The knocking hives and puffs sit at y 560-845. The near hive's bottom edge dips to about y 910 around g 1404-1410 (non-blocking).
- Bees: **PASS.** No bees g 1368-1440. The first bees appear around g 1441 at u0. About 20 bees are on screen by g 1450-1452,
  leading into the shot-22 burst.
- Night grade / continuity: **FAIL -- BLOCKING.**
  - The shot 21 sky is a flat, bright periwinkle (top RGB 126/118/240) with no stars.
  - Shot 20 (g 1365-1367) and shot 22 (g 1453+, top RGB 92/87/200) are darker and starred, so the grade jumps at both cuts.
  - At g 1368-1380 a bright orange lamp band and lit hut wall still glow at y 820-900, with a white lamp sliver near x 120,
    y 850 at g 1368. The foreground pool is not dimmed enough.
  - Roof undersides glow bright orange throughout. The shot reads as dusk, not night.
- Pops / cuts: **PASS.** 1368 and 1453 are clean hard cuts (diff 45 and 37, single frame). No frozen or duplicate frames
  (minimum diff 6.6). Old minor items:
  - The yellow stick on the ground at g 1398-1406 (lower centre) is still there.
  - A roof bar sits at the top right edge at g 1368.
- Camera always moving: **PASS.** It trucks g 1368-1428, then pans slowly (about 4 px per frame, diff about 7) from g 1429-1452.
  No static run of 6 frames or more.

## Fixes
1. **Knock readable (all 4).**
   - Aim the camera about 8-10 deg further toward the knocking hive, or let it lead less, so that each hit lands at x 200-560
     and the spray stays in frame for its whole life.
   - Put the post or frame the hive hits visibly at the contact end.
   - Make the jolt real: 8-12 px for 2 frames on the hive, roof and post, plus a 2-frame camera shake of 3-4 px. It must show
     as a diff spike.
   - Add the missing spray at u2 g 1405.
2. **Dust as a spray crown.**
   - Drop the solid tan backing cards.
   - Emit 8-15 small chips/droplets (6-12 px) radially from the contact point in a 90-120 deg upward cone, with speed and
     gravity, so they arc out as a crown 150-200 px wide.
   - Add a thin, low-alpha wisp and fade everything over 6-8 frames.
3. **Night grade matching shots 20/22.**
   - Use the shot 22 world and sky grade (sky about x0.75, stars on).
   - Darken the roof undersides to the shot 22 level.
   - Cut or dim the hut/lamp glow at g 1368-1380 below y 820.
