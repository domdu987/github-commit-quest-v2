# QA-art round 18 s26: FIX-FIRST
s26 is BIGZOOM B, the ending (g 1958-2111). I extracted all 162 frames (g = 1950 + n). I judged:
- a 144x256 phone sheet every 5th frame
- full size at g 2020/2026/2032/2041
- 2x nearest-neighbour crops of the wall base at g 2021/2026/2027/2032/2038/2040/2041/2046/2052/2058/2064
- a per-frame detector for flat, untextured, brown-mauve blobs (9x9 std < 1.2) on y 420-800, g 2010-2069

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa18r/ (s26_phone.jpg, s26_full.png, s26_patch.png, s26_sq.png).

## Director's list
1. **Hex block at g 2020-2032: GONE.** The bottom of the frame now shows warm jars and hay, and no dark prism.
2. **Flat patches over the wall base, g 2021-2058: NOT GONE. Smaller, but the same artifact.**
   - The pale beige boxes and the big halo panels are gone, and the brick reads elsewhere. The white blobs my first detector found are the accepted smoke-sphere puffs.
   - But a **flat, untextured, mauve-brown rectangle (RGB about 143/102/78, hard straight edges)** is still on the wall base right behind the oxen's backs. It is in the same place as round 17's patch_B:
     - g 2027-2040: x about 475-610, y about 540-595, up to 1,840 px flat (about 80 x 35 px visible between the horns; largest at g 2035-2037).
     - g 2041-2051: a second one at x about 255-340, y about 560-605 (up to 970 px), behind the general's raised arm.
     - g 2032: a smaller translucent grey square at the ox's feet (x about 480-520, y about 700-740).
   - That is about 0.8 s. On the phone it is a small blank card above the herd's backs, low in contrast but visible at g 2035-2041. At full size it is plainly an untextured placeholder (rule 2 and "no glitches").
   - Hiding `halos` did not remove it. It is a separate opaque object at the wall base.

## Everything else: good
- **The BIGZOOM gag reads:** one eased crane from the extreme wide, with 即墨 readable, to the medium general. It has the scream, the fist-gripped cup, the dropped helmet, the look-back, the rage oxen and the smoke.
- **Rim:** a clean pale blue-white rim, warm dawn against cool shade.
- **Caption band:** clear of faces at the end; only the general's legs cross it.
- **Hard rules:** no pole through a face, no fire on a head, no half-cut main character.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 7.5 | 8 | 8 | 8 |

## Verdict: FIX-FIRST (1 narrow blocker, g 2027-2051 only)
1. Find the object with a raycast from the camera at g 2036 through pixel (520, 565) and at g 2045 through (290, 580). Hide it, or give it the wall's brick material.
   - Re-render g 2025-2053 only.
   - **Conform alternative if no render time:** a tracked clean-plate or paint-out of the two boxes. The wall is behind them and the horns are in front, so a matte is needed.
   - **Pass check:** at 2x on g 2030, 2036, 2040, 2045 and 2050, there is continuous brick texture behind the herd, and no flat patch over 20 px with straight edges.
   - Nothing else in the take needs to change. With this fixed, the take is a PASS on that check alone.

## Notes (not blocking)
- The field saturation at g 1985-2005 is for the conform grade (round 17 note).
