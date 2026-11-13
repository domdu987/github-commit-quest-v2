# s21 QA: film 6, shots 21-22 (the hooded stranger buys a dozen; Henry counts 12, shoos kit; kit eyes the spare loaf), bakery AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 1633, 220 frames = g 1633..1852, 720x1280, 12 samples, 2 threads, denoise FAST,
no captions / audio), `frames/` (local, gitignored), `meta.json`, `cues.json` (24 cues), `contact.jpg`, `compare.jpg` (g 1720 beside ref a
t0046, g 1780 beside ref a t0010), `work/qa.txt`. Scripts: `shot.py`, `deliver.py` + `deliver_lib.py`.
Range: plan 54.64-61.57 s -> [g 1639, g 1847); shot 21 = g 1639..1739, shot 22 = g 1740..1846; handles 6 + 6 rendered in 3D.

## Client rules
- **No depth of field / no blur**: DOF off at build and before every render (common.Take); no motion streaks.
- **Heads above the caption band**: every visible head bottom <= 860 (henry centre 0.49-0.57 H, inspector 0.43-0.49 H, kit 0.42-0.55 H).
- **Mouths**: nobody speaks (no quoted line here). Henry's `henry_shoo` mouth (talk_a in STORY6) is replaced by a closed static
  mouth; the inspector shows only the hood shadow + eye glints; kit's mouths are the static expression mouths.
- **Continuity**: inspector hooded throughout (hood 1, face in shadow); henry round bald baker; kit floury; the spare loaf is the PALER
  one (cast6.loaf_svg with the crust blended toward cream).

## Framings (a change every 0.9-2.1 s)
| g | framing | action | narration |
|---|---|---|---|
| 1633-1693 | 21a street side, 24 mm, slow push | the hooded man walks in from screen-left (walk cycle, 24 f) and stops at the shutter board (g 1688); henry + kit behind the counter | "บ่ายวันนั้นเอง ชายใส่ผ้าคลุมเดินเข้ามา" |
| 1694-1739 | 21b inside, low (pitch +26..28), 22 mm | the hooded face against the bright street, eye glints only; one hand comes up ("a dozen", g 1712-1740), steam off here | "ขอซื้อขนมปังหนึ่งโหล" |
| 1740-1801 | 22a street, low (pitch +13..15), 30 mm on henry | henry counts on his raised fingers 1..5, 1..5, 1..2 = twelve (g 1753-1797, one head bob per count), unimpressed -> smug | "ลุงนับให้ สิบสองก้อนพอดี" |
| 1802-1829 | 22b two-shot from the street, 24 mm | henry shoos (open hand flapping, angry, mouth closed, from g 1806); kit shrinks, hops off his stool and backs into the shop | "แล้วไล่เด็กไปหลังร้าน" |
| 1830-1852 | 22c inside by the right-wall racks, 24 mm | kit at the back of the shop, sad; g 1838 his eyes slide to the pale spare loaf on the shelf above-left -> determined | |

## Checks (`work/qa.txt`)
- Heads: henry 106-254 px, inspector 136-231 px (enters from beyond the left edge in 21a), kit 99-347 px (22c is a close-up).
- Popcheck (cuts excluded): one jump g 1805 -> 1806 (5.7 levels) = henry switching from the count pose to the shoo (the gesture starts
  on that frame; it reads as a snap into the shoo). Near-still: one pair (g 1694 -> 1695, first frame after the cut). Median frame
  change 2.4 levels. No black / magenta frames, none retried, no clipped sprites.
- Counting fingers: henry's ball hand is dark plum on the grey brick wall, small (about 45 px) -- countable, low contrast.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s21 shots 21-22 (g 1639-1846)                  42.2   38.1    0.7    0.7    0.0    7.4    3.5    7.4  0.44 0.52 0.11
s21 21a street (g 1633-1693)                   41.0   46.1    0.5    2.1    0.0    3.8    2.1    4.4  0.46 0.54 0.09
s21 21b inside low (1694-1739)                 32.8   13.4    0.0    0.0    0.0   35.6    9.4    8.7  0.37 0.49 0.15
s21 22a-b counter (g 1740-1829)                45.0   40.7    1.0    0.2    0.0    0.8    2.8    9.5  0.47 0.52 0.11
s21 22c racks (g 1830-1852)                    49.7   45.1    0.9    0.0    0.0    0.8    0.3    3.1  0.36 0.62 0.02
ref a t0001 t0046 t0047                        32.1   44.2    4.9    0.3    0.0    7.4    6.1    5.4  0.34 0.47 0.12
```
Whole take close to ref A interiors (orange 38 vs 44, val 0.52 vs 0.47, dark 0.11 vs 0.12); blue only from the street in 21b. 22c is
the warmest / lightest (candle-lit racks), as the set measures (bakery_API 7).

## Seconds per frame
18.2 s wall / 34.0 s CPU mean (2 threads, two processes at once). Sprites 400 px/D.

## Differences from the plan
- The plan puts "Henry counts 12 on fingers" in shot 21 and the shoo in 22; the narration says the count at 58.33-59.96 s, i.e. in
  shot 22's time, so: 21 = the stranger arrives + asks, 22 = count (22a), shoo (22b), spare loaf glance (22c).
- The spare loaf is on the right-wall rack shelf (the set has no shelf by the counter in that view); kit "goes to the back" first.
- 21b (inside looking out) and 22c (inside at the racks) are custom cameras, not the `counter` preset, to vary the framing.
