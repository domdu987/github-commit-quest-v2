# s04 QA: film 6b, shots 4-7 (the pivot: the market, short weight, the pillory, the tomato), market AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, 203 frames g 117..319, **first_g 117**, 78.7 MB -> split per WORKER6B into
`take.mkv.partaa` `take.mkv.partab`; rejoin with `cat take.mkv.part* > take.mkv`; the unsplit file is not committed), `meta.json`
(g0 123, g1 314, first_g 117, n_frames 203, transition_in cut), `cues.json` (13 cues), `contact.jpg`, `compare.jpg` (g 150 beside ref a
t0031; g 298 beside ref a t0011), `shot.py`, `take_cfg.py`, `deliver.py`, `qa.py` (-> work/qa.txt), `lib6b.py`, `sheet.py`.
Shots: 4 = g 123-179 (in-handle g 117-122: the crane slightly higher), 5 = g 180-227, 6 = g 228-272, 7 = g 273-313, out-handle g 314-319
(push, splat drip, laughter continue). All handles rendered in 3D.

## What is on screen (word-literal)
| g | picture | caption |
|---|---|---|
| 117-179 | crane down from the sky (clouds) over the rooftops into the medieval square: bunting, stalls, braziers, the pillory and the big balance; townsfolk walk across | "คืออย่างนี้นะ อังกฤษยุคนั้น" |
| 180-227 | CU baker2 beside the big public balance with his loaves (head 275-339 px = 38-47 % W), push in: the beam tips to the weights side (190-200, bounce), he goes worried -> shocked + sweat, hands up; Thai sign "ขาดน้ำหนัก!" drops in on its cords and swings (203-209) | "ใครขายขนมปัง ขาดน้ำหนัก" |
| 228-272 | low push on the pillory: baker2 locked in the board (struggling head wobble), guard with spear, sign on the post "ห้ามขายขาดน้ำหนัก!" | "โดนจับใส่ ขื่อกลางตลาด" |
| 273-319 | CU baker2 in the pillory between two laughing townsfolk (edge of frame): a rotten tomato flies in from screen-right (285-295) and SPLATS on his face (296, tomato_svg squash 0.55 -> 1.0, drips slide down); he flinches (eyes shut), they laugh | "ให้คนปาผัก เน่าใส่" |

## Rules
- No depth of field anywhere (camera dof off + B.setup_dof(None) before every render). Sharp; no motion streaks.
- Mouths: no quote in s04 -> static expression mouths only (pointing / jeering poses have mouth=None; laughing / shocked are expression mouths).
- Heads above y 880: main heads always (baker2 centre 0.41-0.47 H). Exceptions: shot 4 is the crane-down wide (exempt; tiny 34-65 px
  townsfolk low in frame at the start); shot 7 the laughing townswoman at the right frame edge (head 372-454 px, centre 0.52-0.54 H) has her
  chin just below y 880 on g 298-319. Actors not in a shot are parked 30 D under the ground (qa lists their invisible 17 px "heads" in shot 5).
- Comic, not cruel: cartoon splat (no injury), pillory = humiliation.
- Thai signs: Kanit Black via Chromium (embedded font), red text with white + ink outline on a cream board, readable at phone size.
- Popcheck: no pops outside the planned cuts; one near-still transition (g 181, first frames of the slow push in shot 5); no black / magenta
  frames; no retried frames.

## Numbers (work/qa.txt)
```
set                     red orange yellow green cyan blue violet magent  sat  val dark
s04 all                37.8  22.0   0.6   0.5  0.1 23.4   8.2    7.4  0.40 0.67 0.04
refs of compare.jpg    35.6  15.8   1.6   0.5  0.5 30.9   7.3    7.9  0.22 0.58 0.06
```
Warm gold sun / red bunting vs blue sky + blue shade (complementary). Shot 7 magenta 13.9 = the tomato red. Lighter than the refs
(market set look, bakery_API 7). Mean 13.8 s wall / 26.8 s CPU per frame (2 processes x 2 threads); shot 7 19 s.

## Differs from the plan
- Shot 4: no flags added (bunting and the set's royal banners only; WORKER rule "no anachronisms").
- Shot 5: the "short scale" is the market's big public balance (set_big_scale -7, 12 loaves) rather than a separate small scale.
- Shot 7: the thrower is off-frame screen-right (the tomato enters from there); the two visible townsfolk laugh after the splat.
