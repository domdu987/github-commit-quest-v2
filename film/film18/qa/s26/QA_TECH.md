# QA-tech round 18 s26: FAIL
Checked: 6 fps sheet (27 frames), every frame g2015-2062 (wall band and bottom strip montages), 2x nearest-neighbour crops g2023-2033, 1.5x crops g2035/2044/2050, a flat-patch detector, mouth crops g2096/2104/2111, general crops g2066-2093. Director numbers accepted (ground 0.297, frame-diff 9.88/12.17, blur on the extreme wide accepted).

## Blocker
1. **Flat pale/untextured patches over the wall base are still there, g2023-~2050 (round-17 blocker, fixed only in part).**
   - g2023-2033: a flat mauve-grey rectangle sits on the wall base behind the herd's backs at x ~560-680, y ~545-600. It grows from ~25x40 px (g2023) to ~95x65 px (g2031-2035), with hard straight edges and no brick texture.
   - g2035-2040: same box about 90x70 px at x ~490-585 (the brick wall shows around it).
   - g2043-2046: flat smeared strips at x ~230-310 and ~440-540, y ~555-600, about 190x40 px (g2044 1.5x crop).
   - g2047-2052: a flat beige bar at the top-left of the herd (x ~130-200, y ~ 500) and a patch beside the wall base.
   - On the phone it reads as a pale brown box floating behind the herd; at full size it is plainly a glitch. This is exactly the "no flat pale or untextured patches over the wall base g2015-2062" check. The team's raycast hid `halos`/`wallpools`/`cityglow` but something else on the wall (a mauve card) is still live. Fix: ray-cast g2033 through x 560-680 / y 545-600 again, hide that mesh for the whole take, then check every frame g2015-2062 on the wall band (not only five frames).

## Round-17 blocker 1 verified FIXED
- The dark hexagonal block at g2020-2032 is gone: bottom strip g2015-2046 shows only road, an orange pot (g2015-2027) and a helmet prop (g2046). No navy slab anywhere.

## Other checks (pass)
- BIGZOOM: general ~2 % of the frame at g1958 (tiny, in a warm pool on the road, findable, clear of the gate banner and the 即墨 plaque), ~45 % at g2066, ~54 % at g2111. One continuous eased move, no cut, no pulse. The still reads, the set is rich (roofs, lanterns, banners, fields, oxen, smoke).
- No halos or colour fringes: the white rim is a clean outline.
- Ox mouths ~830-850 max (g2084-2111), <= 860. No face in y 880-950 (only the general's boot and the ground there). No pole or prop through a face.
- No glitches in frame count, no flicker.

## Notes
- g2078-2090: the general's back/armour edge is cut by the right frame edge by roughly 15-25 px; face, arm and cup stay inside, fully inside again from g2096. Not a half-cut.
- g2078-2092: a flat tan rectangle sits behind the ox head at x ~335-440, y ~640-880 (low contrast, below the wall). Same family as the blocker; hide with the same fix.
- Moire on the roof tiles in the extreme wide (g1958-1975) and banding on the field panels (g1990-2012) are accepted.
