VERDICT: FAIL -- 1) the knocks still don't read: 2 of 4 hits start at the left frame edge, the spray comes 1-3 frames after the hit, there is no visible contact and no measurable jolt; 2) action at or below the caption line, and sky 31-42 % (regression from v5); 3) night continuity: shot 21 is now darker and greyer than shots 20 and 22, with almost no stars, so the grade jumps at g 1453.

# QA_RECHECK film 14, take s20 v6 -- shot 21 only (g 1368-1452), TAKE gate round 6 (blocking only)

Scope: shot 21 changed (n 67-151). Shot 20 (n 6-66) and shot 22 (n 152-201) were used only as grade references and to check the cuts.
Checked:
- All 383 frames extracted to scratchpad/takes/qa_s20v6/f/ (gNNNN.png, n = g - 1301).
- Every knock +-3 frames at full size (300 px tiles) and at phone size (120 px tiles), with cyan line at y 880.
- Phone sheet of every 3rd frame from g 1362 to 1461.
- Zoomed crops with a grid at g 1403-1409 and 1436-1442 (jolt and crown).
- Camera motion between hits at g 1389-1398. Cuts at g 1365-1370 and 1450-1455.
- Frame diff and white-chip bounding boxes on every frame from g 1355 to 1465.
- Sky share, sky colour, star count, warm-glow share and luma, measured on v5 and v6 side by side.

Sheets (in scratchpad/takes/qa_s20v6/):
- phone1.jpg
- knock{1388,1405,1422,1438}.jpg and knock*_phone.jpg
- jolt_zoom.jpg, crown1406.jpg, between_1389_1398.jpg
- cut1368.jpg, cut1453.jpg, grade.jpg

## Re-check of the v5 blockers

### 1. The knocks read: **NO -- BLOCKING (still open)**

| hit (claimed) | first spray | spray position (x, y) | in frame? |
|---|---|---|---|
| u3 g 1388 | g 1391 (+3) | x 0-155, y 636-821 | cut by the left frame edge |
| u2 g 1405 | g 1406 (+1) | x 251-313, y 843-882 | mid-left, on the caption line |
| u1 g 1422 | g 1424 (+2) | x 0-28, then x 0-120 at g 1425 | cut by the left frame edge |
| u0 g 1438 | g 1439 (+1) | x 282-353, y 835-875 | mid-left, on the caption line |

- **Mid-frame claim.** Only u2 and u0 land mid-frame. The spray at u3 and u1 starts at the left frame edge, so the "follow each knocking hive" claim fails on 2 of the 4 hits.
- **No visible contact.** The spray bursts at the hive's top corner in open corn. The posts are at x of about 140 and 520, and no post, frame or hive meets the hive at the burst point. The hit reads as a sparkle on the hive, not a knock against something.
- **No jolt.** The frame diff does not spike at any hit. The hit frames are local minima (6.0, 8.2, 7.5, 8.2), followed by a gradual rise of +3 to +5. The grid crops (jolt_zoom.jpg) show no 2-frame displacement of the hive, post or roof, and no camera shake. At phone size nothing jolts.
- **Camera between hits.** Between hits the camera re-aims fast. The foreground corn moves about 70-115 px per frame at g 1392-1395, 1408-1412 and 1425-1429, then nearly stops on each hit. This reads as a hunting camera rather than a hit. It is not a pop, but it covers any jolt.
- **Phone size.** The spray is a white speck of about 10-15 px sitting on the cyan line (knock*_phone.jpg).

### 2. Dust as a crown: **PASS at full size (non-blocking notes)**
- At g 1407-1411 and 1440-1444, 10-15 separated white chips spread radially in an upward arc. The crown is about 100 px wide, grows to 250-300 px with outliers up to y 447, and fades by about +7 frames. There are no square backing cards. This is fixed.
- The first frame (g 1406, 1439) is a tight white lump crossed by two long pale shards. It reads as a graphic "X" (the team noted this).
- The chips are pure white. Tinting them toward wood or dust (for example 200/170/130) would sit better in the night grade.
- At phone size the crown is too small to read (see blocker 1).

### 3. Night continuity: **FAIL -- BLOCKING (changed direction: shot 21 is now darker than its neighbours)**

| | shot 20 (g 1340-1367) | shot 21 v6 (g 1368-1452) | shot 22 (g 1453-1470) |
|---|---|---|---|
| sky top RGB | 73/68/183 to 94/88/202 | **94/88/165** (grey-lavender) | 101/94/207 |
| star detections | 1400-2200 | **44-513** | 3800-4100 |
| mean frame luma | 90-100 | **52-58** | 75-80 |
| luma below y 880 | 56-67 | **17-25** | 42-45 |
| warm-glow share | 2-17 % | 0-1.4 % | 12-13 % |

- The v5 problems are fixed: the shot no longer reads as dusk, the roof undersides are dull tan (about 111/77/50), and the hut windows and lamp band are gone.
- But the shot is now over-darkened and desaturated against both neighbours.
- At the cut to shot 22 (g 1452 to 1453):
  - The sky jumps from grey-lavender to saturated blue.
  - A dense star field appears.
  - The ground brightens about 2.5x.
- At g 1368-1375 a small orange lamp disc still glows behind the corn, at about x 180-300 and y 800-880 (cut1368.jpg).

## Kept from v5
- **Wave: PASS.** Each hive tilts hard in turn and the wire is visible. As before, only 1-2 hives are in frame at once.
- **Framing: FAIL -- part of blocker 2 below.**
  - Sky is now 31-42 %, measured with the same blue-pixel detector on both takes (v5 measured 21-33 %). It peaks at 41-42 % during the fast pans (g 1395, 1411, 1429).
- **Bees: PASS.** No bees from g 1368 to 1440. The first bees appear at about g 1441-1443, there are about 20 on screen by g 1450-1452, and they lead into the shot-22 burst.
- **Cuts: PASS.** g 1368 (diff 49.7) and g 1453 (diff 42.6) are clean single-frame hard cuts.
- **Camera always moving: PASS.** The minimum diff is 5.2, with no static run and no duplicate frames.

## New blocker
### 2. Action above y 880: **FAIL -- BLOCKING (regression)**
- The knocking hive's body now sits at about y 760-1000, and its lower half is below the caption band in every knock frame.
- Every spray starts at y 816-882, on the caption line (v5 had the hives at y 560-845).
- Captions burned at y about 900 will cover the hive and the hit.

## Other pops and minor notes (non-blocking)
- No unintended pops. Large near-roof triangles slide in at the top left at g 1394-1398 and 1411-1413. This is the fast pan, not a pop.
- The yellow stick on the ground (lower centre) is still there at g 1409-1412.

## Fixes
1. **Knocks.**
   - Settle the camera look point on the contact point from 3 frames before each hit to 6 frames after, with the contact at x 250-470 and y 550-800.
   - Ease out over 6-8 frames between hives instead of the 70-115 px/frame whip.
   - Fire the spray on the hit frame (g 1388, 1405, 1422, 1438). It is currently 1-3 frames late.
   - Make the contact visible: the hive end must strike its post, frame or the neighbouring hive exactly where the spray starts.
   - Jolt of 12-16 px on the hive, post and roof at hit and hit+1, plus a 4-6 px camera shake. It must show as a diff spike of at least +6 over the neighbouring frames.
   - Verify all four hits at 120 px phone size.
2. **Framing and caption line.**
   - Pitch the camera down, or raise it, so the hive bodies sit at y 550-850 and the sky is back to 21-33 %.
   - Scale the crown about 1.5x for phone legibility: chips 8-14 px, peak width 200-250 px.
   - Tint the chips toward wood or dust.
   - Make the first spray frame a small burst rather than an "X" of two shards.
3. **Night continuity.**
   - Match the sky to shot 22 (top about 100/94/205, same saturation).
   - Turn the stars on at shot-22 density and size, so they are visible at this elevation. A sky-dome star layer is fine.
   - Lift midtones and ground about 1.5-1.8x, to a luma of about 35-45 below y 880.
   - Keep the hut lamps off, and remove the orange disc at g 1368-1375.
