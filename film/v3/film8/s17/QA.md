# s17 QA: film 8, shots 17-19 (the reveal): desert_ice plain, NIGHT / NOON / NIGHT

Delivered: `frames/g_1341.png .. g_1672.png` (332 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 1341, 332 frames; > 45 MB so committed as `take.mkv.partaa..` from `split -b 40M`,
rebuild with `cat take.mkv.part* > take.mkv`). Plan range g 1347..1666 (44.89-55.57 s) + 6 handle frames each side (rendered in 3D).
g 1347..1478 = shot 17, g 1479..1560 = shot 18, g 1561..1666 = shot 19. Three set-ups, joined by **10-frame dissolves** centred on the
plan cuts (g 1474..1483 and g 1556..1565; both set-ups rendered over the range, blended in `deliver.py`): night -> day -> night reads as
time passing. `meta.json` (events, set-ups, frame_source incl. the blend weights), `cues.json`, `contact.jpg` (16 frames, cyan = y 880),
`compare.jpg` (g 1440 / 1520 / 1640 beside ref a t0072 / t0061 / t0069). Scripts: `shot.py` (stills / final), `deliver.py`, `qa.py`
(-> `work/qa.txt`); helpers `../common.py`. Drafts `work/d1..d6`.

## Client rules
- **No depth of field**: off at build and before every render (common.Take). Dome steps, stars, wall bricks all sharp.
- **User taste**: wide framings showing the lit set (channels, lantern posts, the dome and its glowing door, the Milky Way; the 15 D wall
  and its shadow); calm, always-moving cameras (tilt-up 26 deg + 1.4 D push; crane down 1 D + 1.9 D push; 1.1 D glide + tilt); no text.
- **The reveal inside the lit 3D world**: the heat wisps are soft, short, translucent ribbons (see below), not the set's long cards.
- Nobody on screen: no heads, no mouths, nothing in the caption band but water / ice / sand.

## What happens
| g | shot | what | caption |
|---|---|---|---|
| 1341-1400 | 17 | low over channel 1 looking ENE along the starlit water (pitch +4): soft wisps lift off every channel | "เพราะฟ้า กลางคืนที่ใส" 44.87 |
| 1360-1483 | 17 | the camera tilts up with them (to pitch +30): the Milky Way overhead, brilliant twinkling stars (x1.5), dome + door, lanterns | "เย็นจัด ยิ่งกว่าน้ำแข็ง ... ลอยหนีขึ้นไปหาฟ้า" |
| 1474-1483 | | dissolve to day | |
| 1479-1560 | 18 | from the north: the sun blazing above the 15 D wall, its long blue shadow over all five channels (thick ice kept in the shade), sunlit sand and jars in front; crane down + push | "ส่วนกำแพงก็บังแดดไว้ทั้งวัน" 50.13 |
| 1556-1565 | | dissolve to night | |
| 1561-1672 | 19 | close over channel 2: frost crystals spread from both bank lips to the centre (white rim on the front), the thin sheet with frost needles covers the water by ~g 1640 | "น้ำเลยแข็งได้ ทั้งที่อากาศ ... ไม่ถึงศูนย์องศา" |

## Runtime additions (desert.py untouched)
- **Heat wisps** (`Wisps`): own texture `work/wisp_soft.png` (3 blurred sinuous ribbons + veil), 56 camera-only billboards (44 across
  the five channels, 12 small ones in channels 1-2 in front of the lens). Each is born on the water, rises 3-11 D (not 14-22), widens,
  fades in over 12 % and out from 25 % of its life, faded at both ends and both sides, shimmer by a 4D noise UV warp keyed per frame,
  additive at 0.24 strength. `set_heat_wisps` is off.
- **Frost front**: a value `s17_spread` inserted into the set's ice material: alpha x smoothstep(spread - distance from the nearest bank
  lip + noise fingers), plus a frost-white rim on the front; keyed -0.35 -> 1.55 with set_ice 0.18 -> 0.42 over shot 19.
- **No sawn hole on the first night**: the cut faces hidden (keyed) and the opening in the ice sheet filled with a quad of the same
  material and UV scheme, parented to the sheet (first final showed the dark hole from g ~1600: re-rendered shot 19).
- Dressing: jars, buckets, rocks, shrubs on the banks (17/19) and on the sunlit north side (18).

## Numbers (`work/qa.txt`)
s / frame (2 threads, two processes): shot 17 11.6 wall / 22.8 CPU, shot 18 6.3 / 12.3, shot 19 ~12.4 / 24.7. No pops, no near-still
frames (median change 1.26 levels), no black / magenta frames, no retried frames. Hue: night shots 91-96 % blue (ref a night 93 %),
magenta <= 1; shot 18 orange 25 / blue 62 / violet 6 (day sky + wall shade; desert_API notes day frames are bluer than ref a).
