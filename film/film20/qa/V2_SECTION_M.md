# Film 20 - QA_TEAM §M audit (foreground props fixed in world / no sliding characters)

Read-only audit of `film/v3/film20/<take>/shot.py` (+ frames at 6 fps, `g` = film frame, 30 fps; seconds = g / 30).
Scale: 1 D = 0.532 m (CO.SC = 1.88 D/m).

## Summary

| Take | Verdict | Object / character | Frames | Problem |
|---|---|---|---|---|
| s01 | PASS | - | - | Our lamp-post (`s01_lamp`) and the bench are placed once in world space. The lamp sweeps out of frame left (g 0-30) and is hidden from g 32. Maupassant stays planted on his mark and sways. |
| s02 | PASS | - | - | Maupassant is seated on a fixed mark. The window girders parallax with the push and snap. |
| s03 | PASS | - | - | Eiffel and the riveters are on fixed marks. The preset `fg_*` slabs are invisible to the camera. `bz_up` follows the camera but it is a light, not a prop. (Unrelated to §M: `rl_a`/`rl_d` shrink away at g 388-396.) |
| s06 | PASS | - | - | The artists and Maupassant are on fixed `SPOT`s. The quill and hands follow a world path over the sheet, not the camera. The chairs and table parallax. |
| s09 | PASS | - | - | Maupassant steps off the banquette at g 612-640, covering only 0.09 D (0.05 m) in 0.93 s, so about 0.05 m/s, below 0.2 m/s. Planted afterwards. |
| s11 | **CODE-FAIL (render PASS)** | `fg_post_s11` | whole take (g 745-1003) | `make_post()` sets `ob.parent = self.cam` (shot.py:334-338), a camera-parented foreground timber post. `C.key_vis(self.post, False, f)` hides it on every frame, so it never shows in the frames. It still breaks rule (1) and should be deleted. Everything else passes. Carriers `a`/`b` walk at 1.5 D/s (0.80 m/s) with `cast20.cycle(...,"walk")` at 1.6 cycles/s, which is 4.0 steps/m, and their legs alternate on the frames (g 850-880). The fence girders and ground stones are world-fixed and parallax. |
| s15 | **FAIL** | `fgh` (gent20 foreground head, top hat) | g 988-1096 (32.93-36.53 s), whole take | Rule (1): `fg_pos(g)` places the card each frame at camera loc + 3.0 D forward - 1.2 D right (shot.py:254-260, `C.place(self.fgh, f, self.fg_pos(g))`). It stays glued to the lower-left corner while the tower, banner and crowd swing behind it, including through the snaps at g 1003-1011 and 1064-1083. |
| s15 | **FAIL** | `off` (the official in the sash) | g 1030-1062 (34.33-35.40 s) | Rule (2): `off_pos` moves him 4.6 D back (2.45 m) in 32 frames, about 2.3 m/s on average. `official_pose` keeps `legs="wide"` with no walk cycle, and the frames show the same wide stance while he shrinks into depth: the card slides. |
| s16 | PASS | - | - | Maupassant, the artists and the patrons are on fixed marks with a laugh bounce only. The FG marble table `t16_fg` is world-fixed and parallaxes. |
| s18 | PASS | - | - | The 5 characters and the telegraphist are on fixed marks. `team8_fg` (kegs, crates, planks, lamp) is world-fixed and parallaxes (planks and coils sweep across the frame in g 1210-1300). The wagon is shifted once (`WAGON_SHIFT`). |
| s21 | **FAIL** | the merged `wagon` mesh from `CO.STATE['wagon']` (tower20._wagon: 2 carts plus **2 `horse_card`s**, plus ladders, ground crowbars, a coil and kegs) | g 1628-1663 (54.27-55.43 s); visibly sweeping behind the group at ~g 1636-1656 | shot.py:621-624 keys `ob.location = p0 + (60*u^2/SC, 0, 0)`: 60 D, about 32 m, in 1.17 s. The horse cards are rigid mesh with no leg motion, so this is a horse card sliding (rule 2). The ground props merged into the same mesh (crowbars, kegs, ladders, coil) slide with it instead of staying fixed in the world. On the frames the cart wheels, load and a brown horse shape streak left to right behind the demolition men and the officer (g 1640-1652). The group itself is planted (demo bounce only). The FG kegs `s22fg` are world-fixed and parallax. |
| s23 | PASS | - | - | The `fgh` foreground head from s15 is not built here; `fg_pos` exists but is unused. The official stays put (`off_pos` returns the mark). Crowd bob only. |
| s24 | PASS | - | - | Maupassant is on a fixed mark. The preset `fg_` post is hidden. The FG chair is set furniture (world-fixed) and moves with the push. |
| s25 | PASS | - | - | Maupassant is seated on a fixed mark. The FG chair `fg_i_woodlt` is hidden; the other furniture is world-fixed. |
| s26 | PASS | - | - | Seated Maupassant from behind, on a fixed mark. The table and railings parallax. |
| s27 | PASS | - | - | Maupassant is on a fixed mark. The preset `fg_` iron post is hidden. The crash pull-out shows parallax throughout. |

## Notes / fixes
- **s15 `fgh`:** compute the head's position once (for example `fg_pos(GF)`) and key it as a fixed world point, or delete it. Keep it clear of the lens over the whole path.
- **s15 official:** either drop the step-back (as s23 v2c did: `off_pos` returns the mark) or give him a walk cycle (`cast20.cycle(..., "walk")`) phased to the 2.45 m move, at 2 steps/m or more.
- **s21 wagon:** stop translating the whole `wagon` mesh. Roll only the cart geometry with a walking horse card (or no horse), or cut the roll. The ladders, crowbars, coil and kegs merged into that mesh must stay in place.
- **s11:** delete `make_post()` and its call. It is invisible in render now, but it is the camera-parented FG prop pattern the client complained about.
