# QA re-check, SET gate round 2, film 14 "ไอ้บ้าผึ้ง" (QA-art + tech items)

Reviewed: the 18 finals in `farm_work/final/` at full size (720x1280) and as phone sheets (360x640, made in scratch), `contact.jpg`,
`farm_work/hue_rows.txt`, `farm_work/final_log.txt` (heads), API.md "Round 2 changes", `cast14/sheet.jpg` (the new nose_swell strip and
`uncle_stung_close`), BRIEF.md and the client rules in production-lessons.md section 2.

## Verdict: FIX-FIRST (3 small changes, then show the client)

Round 2 is a big step up. The hook, the count beat, the crowd, the trampled field, the night sky and the ending pose all read now. No
goats at night, no clutter, and feet are on clear ground. Three problems are left, and the first one hits the client's top rule (a dense
set): the grass was cleared from the low presets but nothing replaced it, so the bottom third of those frames is bare red earth. The
other two are camera and staging fixes: the push point is hidden in `push_side`, and the nose in the payoff frame sits in the caption band.
None of the three needs new modelling. Each one is a re-aim or set dressing plus a re-render.

## Round-1 blocking items

### QA-tech
| # | item | status | note |
|---|---|---|---|
| 1 | Shade hue 240-260 | **PARTLY** | 11 of 18 tiles are in band now. Still out: fence_line fs0/fs1 267/264, fence_ring fs2/fs3 269/272, village_wide DAY 233, trunk_close 238.9, yard_crowd 232.5 (placeholder dresses). The measured shade share on DAY is only 1-2 %. This is a grade tweak, so it is not blocking. |
| 2 | Hook does not read | **FIXED** | The new `hook_close` reads: hero on the ladder with the hive at his unit, four smiling villagers plus the uncle in the mid-ground. The hero is still small (head about 65 px) compared with the villagers. See the non-blocking list. |
| 3 | Fence stages 1/2 | **FIXED** | fence_line fs0 vs fs1 is a clear change at phone size: the tin roof, the hanging hive and the short wire appear over the same posts. They are not alike, and the matched composition helps the cut. fence_ring fs2 vs fs3: the cream wire ring and the extra back roofs read at phone size. The left side of the ring is out of frame. |
| 4 | Wire push wave | **PARTLY** | At full size the wire now kinks and the hives tilt (wp0.35: about 30 deg on the second unit). wp0.7 adds the big gold cloud. At phone size the bow is small, and the matriarch's head covers the push point at x 6.0. The wire passes across her face and reads like a tusk, not a chest push. |
| 5 | Goat at NIGHT | **FIXED** | |
| 6 | Uncle field not trampled | **PARTLY** (reads now) | It reads as ravaged: bare earth, pits, dung, a broken thorn fence, a few chewed plants. But the footprints read as donuts or pot rims (dark pit plus a raised light rim), and the remaining plants look like healthy low bushes, not flattened maize. |
| 7 | Heads above y 880 | **PARTLY** | The herd is fixed (herd chins 707-777). New failures: `uncle_field_morning` uncle at 933-1008 (whole head in the caption band) and `uncle_nose_close` chin at 888, with the 1.0 nose hanging down to about y 1150. `village_wide` hero, kid and old man have chins at 890-907, but they are specks in a wide shot (minor). |
| 8 | Feet hidden by grass | **FIXED** | There is clear ground at every stand point. |
| 9 | Crowd not visible | **FIXED** | `yard_crowd` DUSK shows the uncle and 5 villagers, torches and a pot, all whole. |
| 10 | Shimmer | **NOT** (not tested) | Risk is lower (no flowers within 6 m, fewer and wider blades), but the 6-frame camera-move test still has not been run. The `push_side` foreground grass is the riskiest. Run it before the render teams start, not before the client sees the sheet. |
| 11 | Props (flames, tin sheet, stool, stray goat) | **FIXED** | No flat yellow flame cones, the slab is gone, the uncle stands ON the stool in `uncle_hang`, and the stray goat is gone. |
| 12 | Bees | **FIXED** (wide), minor | The wp0.7 cloud and trunk_close bees read as bees at full size, and near bees have wings and stripes. `hive_close` "asleep": the 14 resting bees per end cannot be seen. That is acceptable, because the line is "bees asleep, silent". |
| 13 | Night readability | **FIXED** | There is a sky gradient, a moon in frame, stars, warm lamp/fire pools, and the near grass is lit. The mid-sky in push_side is still a fairly flat lavender band (minor). |
| 14 | Jerrycans in push_side | **FIXED** | |
| 15 | Cast vs set scale | **FIXED** | `HEIGHT` now uses the cast sizes (calf 1.2, b/c/d per role), and the elephant cards are canvas-sized. A look test with the real puppets is still open (see below). |

### QA-art
| # | item | status | note |
|---|---|---|---|
| 1 | Foreground clear, subjects closer | **PARTLY** | Subjects are close and clear (yard_two_shot heads about 125 px, yard_crowd and hook_close well spaced). But the clump was replaced by an empty red-earth floor. The bottom 30-40 % is bare in hook_close, fence_line x2, hive_close, yard_two_shot and yard_crowd. fence_ring and field_night_wide have a soft, blotchy, low-detail ground band at the bottom. This is the main open issue (fix A). |
| 2 | push_side rebuild | **PARTLY** | It is now a 3/4 view along the wire, with 6 hives receding left, no goat and no clutter. The push point is still hidden (fix B). The burst starts as one cloud at the far-left hives rather than a column at each hive. |
| 3 | Ending | **PARTLY** | The cast side is FIXED: nose_swell 0..1 is now a long, ridged, trunk-like nose with nostrils that hangs to the belt, and `uncle_stung_close` (on the stool, holding the hive) is clear and funny. The set side: `uncle_nose_close` exists (head about 275 px, roof above-left, mountain, MORNING), but the face sits low and the upper 45 % is empty sky. A 1.0 nose would run through the caption band at y 900 (fix C). `uncle_hang` now has the stool under him. |
| 4 | Trampled field | **FIXED** (reads), with polish left | See tech 6. The campfire is gone. |
| 5 | Hook + count legibility | **FIXED** | See tech 2 and 3. |

## Scores (round 1 -> round 2)
| area | r1 | r2 | note |
|---|---|---|---|
| Set density / ornament | 7 | **6** | Village, savanna, mountain, ring and hives are rich. But the low presets now have an empty floor, the opposite of the client's "beautiful dense set". The wide tiles (fence_ring, village_wide, uncle_field_morning) are dense and lovely. |
| Lighting & colour | 7 | **8** | DAY/MORNING are warm with one hard key, DUSK `hive_close` is the best frame, and NIGHT now has a gradient, moon and warm pools. Magenta max is 6.1 %. Shade hue is out of band on 7 tiles (a grade tweak). |
| Composition / framing | 4 | **6** | Subjects sit at y 450-850 with clean silhouettes. Points lost: bare lower thirds, empty upper half in uncle_nose_close, push point blocked by the head. |
| Cast appeal / acting (sheet) | 8 | **9** | The nose_swell strip is a real gag now (trunk-length, ridged, nostrils), and the new stung/stool poses are strong. |
| Key moments | 4 | **6** | hook 7, count 7, one wire 8, push wave + burst 5, bees at eyes/trunk 7, trampled field 7, swollen nose 5 (the frame works, but the caption band covers the nose). |
| Match to style board / series | 6 | **7** | Palette and light presets are kept. Medium heads are now near the set3d10 bar. The bare floors are the remaining gap. |

## FIX-FIRST: the 3 blocking changes
**A. Fill the bare bottom third of the low presets** (hook_close, fence_line, hive_close, yard_two_shot, yard_crowd, uncle_hang).
Raise each `look_at` z (or lower the camera 0.2-0.3 m and tilt up) until the floor is at most about 25 % of the frame. Then dress the
band 1.5-4.5 m from the camera at the frame edges with props already in the yard set: kale rows, baskets of cobs, pumpkins, a stool,
chickens, a hoe, low wide tufts. Keep the 1.9 m clear ring around every stand point and a central lane for the cast. Keep no flowers within
6 m (shimmer). In fence_ring and field_night_wide, crop or tilt so the soft, blotchy ground band at the bottom is out of frame, or give it
the same tuft/stone detail as the mid-ground. Check: at 360x640 no low tile has an empty floor band taller than about 20 % of the frame.

**B. push_side: make the push point and the bow visible.** Move the camera about 2-3 m toward -x and slightly higher, or stage
`matriarch_push` about 1 m nearer to the camera on the field side. The bowed span at x 6.0 should show in clear sky or against the maize,
with her chest (not her face) on the wire. The wire must not cross her head. Render a 4-frame strip, wp 0 / 0.2 / 0.4 / 0.7, and check at
phone size that the bow and the tilted hives progress along the row. If they do not, raise the swing for the hives nearest the camera. The
bees should rise from each hive entrance as the wave reaches it (the API already says this), so the burst is not only one cloud at the
far left.

**C. Payoff frame and uncle field: get the uncle out of the caption band.** In `uncle_nose_close`, re-aim (`look_at` z about -0.35 m, or
raise the camera) so the head sits at about y 330-600 and a 1.0 nose ends above about y 860. This also removes most of the empty sky. In
`uncle_field_morning`, move the uncle's stand point back about 3 m or tilt down, so his head is at y 500-800. Re-run `head_pixels` and keep
every head chin at y 880 or above it (the nose tip counts on the payoff frame).

## Not blocking: fix during shot work
- Shade hue: push the fence_line, fence_ring and village_wide DAY shade toward 250 (lower `shade_tint` saturation on DAY, or tint only
  pixels with luminance < 0.35). Bring trunk_close up about 2 deg. Re-measure yard_crowd with the real cast (the placeholder dresses skew it).
- Footprints: make them oval with 4-5 toe nicks, a lower and darker rim (not cream), and lighter, shallower pits, so they read as prints,
  not donuts. Lay 20-30 snapped maize stalks flat across the tracks so it reads as a "maize field" and not "leafy bushes".
- hook_close: the hero is about 65 px of head against the villagers' 90. Bring the ladder/unit closer, or cut in with fence_line fs1 for
  the hero read. Put the hive box (now at the left edge, partly behind the ladder) a little more into frame.
- fence_ring: the left side of the ring is cut. Widen 1-2 m or pan so all 4 sides of "a ring round the field" are in frame for fs3.
- push_side NIGHT: the mid-sky is still a flat lavender band. Lower the saturation about 10 % and add a few stars there.
- hive_close: if the "asleep" bees should be seen, enlarge the resting bees near the camera (a few 1.5x bees on the landing bar).
- Shimmer: run the 6-frame camera-move test (push_side, fence_line, hook_close) before launching the render teams.
- A cast-in-set look test with the real puppets (matriarch canvas 26 m wide in push_side and trunk_close, uncle with the 1.0 nose in
  uncle_nose_close). The placeholders are still flat cards, so occlusion of the wire by the real ears and trunk is unchecked.
- The village_wide figures are specks with chins at 890-907. Fine for a wide shot, but keep captions clear of them or nudge the camera.

After A-C: re-render the affected tiles, rebuild contact.jpg and show the client. No further QA round is needed, apart from a quick
phone-size look at A-C.
