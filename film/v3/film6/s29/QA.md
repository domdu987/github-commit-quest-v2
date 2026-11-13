# s29 QA: film 6, shots 29-30 (the pass + Henry pale / the nod), market AFTERNOON

Delivered: `frames/g_2441.png .. g_2592.png` (152 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 2441). g 2447..2586 = shots 29-30 ([g0,g1) = [2447,2587)); g 2441..2446 and
2587..2592 are 6-frame handles (rendered in 3D for dissolves / trims). Also `meta.json` (first_g, n_frames, transition_in "cut",
events), `cues.json` (8 cues), `contact.jpg` (18 frames, caption line drawn), `compare.jpg` (beam insert vs ref a mechanism ECU;
inspector vs ref a low-angle authority). Scripts: `shot.py` (probe/stills/final), `deliver.py`; shared helpers in `../common.py`.
Raw renders + per-frame json in `raw/s29`, `raw/s30` (git-ignored).

## Shots / framings (plan 81.58-86.24 s)
- **29a** g 2441-2484 `big_scale_insert` (24 mm, slow push): the bread pan with **13 loaves (the paler 13th on top)** starts high at
  **-7** (short, "does not move"), held to g 2455, then the beam **eases to +6** by g 2492 (the bread passes), a small overshoot
  (+7.2 at g 2497) and settles at +6. `set_big_scale` keyed per frame.
- **29b** g 2485-2525 low wide (22 mm) under the whole balance, cut on "ผ่านพอดี" (82.73 s): the pan down, kit beside it (hopeful ->
  springs to a **proud** grin at g 2497, fists on hips).
- **30a** g 2526-2556 low medium (24 mm): henry held by both arms between guard1 (L) and guard2 (R); **pale 0.55 -> 1.0** on "หน้าซีด"
  (g 2529-2541), sweat + head tremble; woman1 / man1 **lower their raised tomato / cabbage** (g 2532-2555).
- **30b** g 2557-2592 low on inspector_royal (24 mm): **one slow nod** (`cast6.NOD`, 5 f/key, g 2563-2588) on "พยักหน้าช้า ๆ",
  looking down at kit (left foreground, beaming up).

## Client rules
- **No depth of field anywhere**: `cam.data.dof.use_dof=False` + `B.setup_dof(scene,None,None,cam=cam)` at build and before every
  render (common.Take.no_dof). Sharp throughout: scale frame, banners, cobbles, timber houses.
- **Dense set**: the market's own dressing kept whole (jettied houses, stalls, bunting, awnings, well, braziers, royal banners).
- **Heads above the caption band (y 880)**: lowest head bottom is kit at **875** (30b, the nearest head); every other head bottom is
  higher (henry 797, guards 726/776, inspector 665, townsfolk 795/803). Main heads centre 0.45-0.60 H.
- **Mouths only on quoted lines**: shots 29-30 have no quote -> every mouth is the static mouth of its expression (all `talk_*`
  mouths stripped by `no_mouth()`). Nobody's lips move.
- **Comic, not cruel**: the townsfolk simply lower their veg (no throw); henry is scared, not hurt.
- **Continuity**: the 13th loaf is the paler one (`set_loaves 13`); inspector is `inspector_royal` (hood already dropped in shot 23).

## Staging (`work/qa.txt`)
| actor | head width px | centre y px |
|---|---|---|
| kit (29b / 30b) | 144 -> 225 (push) | 685-762 |
| henry (30a) | 122-154 | 720 |
| guard1 / guard2 (30a) | 125-170 | 647-700 |
| inspector (30b) | 154-179 | 575-577 |
| woman1 / man1 (30a) | 80-101 | 734-752 |

Guards grab henry's hands: each guard's open hand is **pinned on henry's drawn hand** (`actors.local_to_world` of henry's
`hand_l`/`hand_r` anchors, fed as a world hand target) so the grip reads. Kit's pose is `kit_proud`; the beam uses `set_big_scale`;
13 loaves via `set_loaves(13)`.

## Pop / black-frame check (`deliver.py popcheck`)
In-shot frame-to-frame median **4.2**, max **9.4** levels (no static > 6 frames; no near-still pairs). The three internal cuts
(g 2485, 2526, 2557) read as cuts (diffs 53 / 57 / 64). No black / magenta frames, no retried or clipped sprites in the raw json.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s29 shot 29 (g 2447-2525)                      42.5   16.7    0.3    0.1    0.1   32.9    4.0    3.4  0.44 0.69 0.03
s29 shot 30 (g 2526-2586)                      44.2   13.9    0.4    0.2    0.1   31.1    5.9    4.2  0.40 0.68 0.03
reference A, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08
```
These are low-angle exteriors, so a large sky pushes **blue** to ~32 (ref 28.6) and lifts **val** / lowers **dark** vs the ref
whole-clip average (which includes night and interior shots); the red oven/banner/tabard mass raises **red** over ref. This is the
market set's own look (set contact measures the same, `bakery_API` 4), the same for every market shot 3-35, not a per-shot grade.
If the director wants the square cooler / darker to sit closer to ref A, grade all market shots together in the conform.

## Seconds per frame
**9.95 s wall / 18.1 s CPU** mean (12 samples, 2 threads, two render processes on 4 cores, denoise FAST). Sprites: kit 288 px/D,
henry/guards 224, inspector 320, townsfolk 96.

## Differences from the plan / notes
- Shot 29 is split into two framings (29a insert push, 29b low wide at the cut on "ผ่านพอดี") for the required 1.0-2.0 s framing
  change; the plan lists shot 29 as one `big_scale_insert`, so 29b is an added angle within the same beat.
- "AFTERNOON" used (the market set has AFTERNOON / MORNING; the story is mid-afternoon here).
- The transition into shot 31 (bakery) is left as a cut; out-handle g 2587-2592 is rendered in case the conform dissolves.
