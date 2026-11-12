# s20 QA: film 2, shots 20 + 21 (the disaster), tower NIGHT_STORM + vault BURN

Delivered: `take.mkv` = g 1660..1852 (193 frames, `first_g` 1660, 720x1280, 12 samples, 2 threads, libx264rgb crf 6). g 1660..1843 = shots 20-21 ([g0, g1) = [1660, 1844)); g 1844..1852 = out-handle (9 frames = 15/2 + 2, rendered in 3D, the lift continues) for the 15-frame dissolve into s22. In: hard cut from s19. `meta.json` (with `frame_source` and `sub_ranges`), `cues.json` (15 cues), `contact.jpg` (24 frames). Script `shot.py` (uses `../s19/fx.py`). Raw frames per sub-shot in `raw/a|b|c|d` (not in git).

## Timing (g = round((t + 0.10) * 30); cuts round(t * 30), 3 frames before their word)
| sub | g | set / camera | what | word |
|---|---|---|---|---|
| 20a | 1660-1707 | tower NIGHT_STORM, spire close (custom) | g 1660 white flash (flash card 0.92 + set flash 3.0) + bolt onto the empty finial; re-strike flicker g 1663-1667; the finial glows hot; a glowing crack starts down the spire (from g 1665); second flicker + snap punch-in g 1684-1691; camera jolts on 1660 / 1663 / 1686 | "ฟ้าผ่าลงยอด" 1663, "หอระฆังพอดี" 1686 |
| 20b | 1708-1743 | tower NIGHT_STORM, tower_side_mid (custom tilt down) | the glow runs down the west wall of the tower (crack ray-cast onto the real geometry, glowing head with an orange point light); camera tilts down after it; reaches the ground g 1737 | "ไฟวิ่งลงตามกำแพง" 1711 |
| 20c | 1744-1777 | vault BURN, crack_follow (custom pan/dolly) | `set_crack_glow` 0.02 -> 1.0, arrives at the barrels g 1771; fire flicker; barrels flare orange-white g 1771-1777 into the cut | "ลงไปถึงห้องใต้ดิน" 1747 |
| 21 | 1778-1852 | tower NIGHT_STORM, town_wide (custom push + tilt up) | hard cut, white flash; the whole bell tower (30 tower objects parented at runtime to an empty) lifts on a column of fire and smoke: 70 fire puffs, 150 smoke puffs, 36 ground-ring puffs, 44 debris pieces, two orange fire lights; rise 1.6 D burst then accelerating, about 21 D by g 1852, tilt 4.5 deg; extra jolt g 1797 | "แล้วหอระฆังทั้งหอ" 1781, "ก็ลอยขึ้นไป" 1814, "บนฟ้า" 1827 |
Framing changes: 1660 cut, 1663 restrike jolt, 1684-1691 punch, 1708 cut, 1708-1743 continuous tilt (speed change 1722), 1744 cut + pan, 1771 flare, 1778 cut, 1797 jolt, 1814 speed change: no gap over 1.2 s. No static frames (camera moves every frame; rain/fire move every frame).

## Colour (`fx.hue_rows`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s20 20 strike (g 1660-1707)                     1.2    3.6    1.2    0.0    0.0   88.9    2.6    2.5  0.53 0.51 0.00
s20 20 wall (g 1708-1743)                       1.5    1.1    0.7    0.0    0.0   93.6    2.1    1.0  0.51 0.47 0.02
s20 20 vault (g 1744-1777)                     82.3   10.1    5.4    0.0    0.0    0.0    0.3    1.9  0.59 0.76 0.03
s20 21 lift (g 1778-1852)                       2.8    3.7    1.7    0.0    0.0   86.2    2.5    3.1  0.50 0.50 0.00
s20 all (g 1660-1852)                          26.0    5.2    2.5    0.0    0.0   62.1    1.8    2.3  0.53 0.54 0.01
```
Special light, outside the day/interior band by design: the tower sub-shots are NIGHT_STORM (blue-dominant, as the set measures), with the fire and the glow as warm accents; the vault is BURN (fire only, red-orange, as vault_API measures 89.8 red). Magenta stays at 1.0-3.1 everywhere, shade blue-violet (smoke shade painted hue ~250). Dark share is low (night storm presets have no deep blacks).

Seconds per frame (final, 2 threads): mean 8.35 wall / 16.16 CPU; 20a 7.64 / 14.48, 20b 10.75 / 20.47, 20c 8.92 / 17.58, 21 7.39 / 14.51.

## Differences from the plan
- Event times follow the recorded narration (captions.json), not the plan's 57.6 s / 60.4 s: the narration says "ฟ้าผ่าลงยอด" at 55.34 s, so the white flash + strike is on the hard cut into shot 20 (g 1660) with the re-strike on the word (g 1663); "ไฟวิ่งลงตามกำแพง" 56.94 s -> wall cut g 1708; "ลงไปถึงห้องใต้ดิน" 58.13 s -> vault cut g 1744; the glow reaches the barrels at g 1771 (59.0 s), before the cut to shot 21 at 59.26 s (the plan's 60.4 lies inside shot 21).
- Shot 20 has three hard-cut sub-shots (spire / wall / vault) as the plan's action column describes; tower_side_mid and crack_follow are the set cameras moved per frame.
- Rain, flash card, crack glow on the tower, fire/smoke column, debris and the tower lift are runtime additions in shot.py (no set module edited). The crack on the spire runs down the south-west face, so near the top it passes in front of the finial ball as seen from the camera.
- No people anywhere (the town_wide square is empty; the market stall is hidden as in s01).
