# examples: one tested shot per set family

After `scripts/bootstrap.py <PROJ>` this folder is `<PROJ>/examples/`. Every example is a complete take of 36 film frames
(g 30..65, 1.2 s) with 3 + 3 handle frames (rendered g 27..68), built only from what the skill ships plus what
`setup_kit.sh` regenerates. Tested on a fresh bootstrap: Blender 5.3.0 as the `bpy` module, Python 3.13, numpy 2.5,
Pillow 12.3, opencv 5.0, fontTools 4.68, node 22 with Playwright 1.63 (Chromium), ffmpeg 6.1, 4 cores.

| folder | set, light | runner (imported, not copied) | performers | camera move (named framings) | gimmick | ran to a picture |
|---|---|---|---|---|---|---|
| `office_day/` | office, office_day | `v3/film/s10/otake.py` | chief at `boss_mark` talks (`boss_talk` + `boss_finger_wag`), hero at `gloat_near` listens (`hero_listener`) | `low_boss` -> snap g 40..52 -> `G`, then a zoom push 22 -> 25 mm | red line grows (`set_track`), spinner turns | yes: drafts, whole-take chain, 1 final frame |
| `office_grey/` | office, office_grey (`EX_LIGHT=office_storm` or `office_day` switches) | `v3/film/s17/otake.py` | hero at `hero_mark` slumped (`hero_slumped`), chief walks to `near_mark` (`boss_walk`) | `eye_two_shot` -> crane g 36..60 -> `high_two_shot` | window rain (`set_rain`), label flutter; storm: lightning g 48 | yes: drafts (grey, storm, day), whole-take chain (grey) |
| `beach/` | beach, beach_sunny | `v3/set3d_ext/beach/bshot.py` | beach_man at `sand_a` shrugs, beach_woman at `sand_b` holds her hat in a gust | `eye_beach` -> crash pull-out g 44..60 -> `vista_high` | gust: wind 0.15 -> 0.8, sign swing, vane | yes: drafts, whole-take chain, 1 final frame |
| `kitchen/` | kitchen, kitchen_grey | `v3/set3d_kitchen/kshot.py` | the ink arm card (no puppets: the set is an insert table) | `steep` -> ease g 32..54 -> `table` | arm grips the cup, cup rattles, steam, coffee rings, drizzle | yes: drafts, whole-take chain, 1 final frame |
| `map_mech/` | office wall map + mechanism, office_grey | `v3/film/s20/mc.py` | none (table-top scale: the props perform) | `rake_spinner` -> snap g 36..48 -> `rake_north` | pressure walls rise in terraces, lane unrolls, spinner | yes: drafts, whole-take chain |

## Exact commands (from `<PROJ>`)

```sh
python3 <skill>/scripts/bootstrap.py <PROJ>          # 0.5 s: copies pipeline/ (code, specs, examples), no caches
sh <skill>/scripts/check_env.sh <PROJ>                # ffmpeg+libass, bpy, numpy/Pillow/cv2, fontTools, Playwright, fonts, (rapidocr), fal.ai, cores
sh examples/setup_kit.sh                              # ~80 s from clean, ~150 MB: fonts/th + six texture caches (below)
cd examples && python3 smoke.py                       # ~45 s: probe + 3 drafts of every example -> smoke.json, smoke_sheet.jpg, "ALL PASS"
```

`setup_kit.sh` runs, in this order (measured from clean): `v3/set3d/textures.py` 3 s (4.8 MB), `v3/paper/paper.py build` 42 s (62 MB),
`v3/set3d_ext/light/gen_tex.py` 14 s (36 MB; it always rewrites), `v3/set3d_ext/props/make_hi_map.py 2000` 5 s (part of props/tex, 11 MB with
the derived prop textures written on first build), `v3/set3d_beach/beach_tex.py` 1 s (0.3 MB), `v3/set3d_kitchen/kitchen_tex.py` 13 s (34 MB).
Puppet sprites are not a separate step: each take rasterises its own into `<take>/work/sprites` (about 18 MB per 42-frame take).

## One example, the worker's order

```sh
cd examples/office_day
python3 shot.py probe 27:68:8      # no render, ~7 s: per frame camera height, pitch, each head's width / centre / top / bottom (px at 720x1280)
python3 shot.py stills 40,52       # 360x640, 6 samples -> work/stills/, work/stills.jpg
python3 shot.py draft 27:68        # 360x640, 6 samples, resumable -> work/draft/f_%04d.png (+ meta/), work/draft_sheet.jpg; ~1.8 s a frame
python3 shot.py render             # 720x1280, 12 samples, 2 threads, resumable -> work/raw/f_%04d.png + meta/, plate/ matte/ on fast frames
python3 shot.py post               # -> frames/g_%04d.png (camera streak on fast frames), meta.json, cues.json, work/post_log.json
python3 shot.py contact            # -> contact.jpg (16 frames of g 30..65)
python3 shot.py qa                 # -> work/qa.json: moves, static and linear runs, pops, head ranges, seconds per frame, hue report
```
otake writes `f_%04d.png` with f = g + 1 in work/; every runner's `frames/` holds `g_%04d.png` with the film frame g.

| family | probe | draft | final render | post | contact / qa |
|---|---|---|---|---|---|
| office_day, office_grey (otake) | `probe a:b:s` | `draft a:b` or `a,b,c` (inclusive) -> work/draft/f_ | `render` -> work/raw/f_ | `post` -> frames/, meta.json, cues.json | `contact`; `qa` |
| beach (bshot) | `probe a:b:s` -> work/probe.json | `draft a:b:s` (b exclusive) -> work/draft/g_, work/draft_contact.jpg | `render [a:b]` -> raw/g_ + raw/meta | `post` -> frames/ | `qa` -> meta.json, cues.json, contact.jpg, work/qa.json (needs 720x1280 frames) |
| kitchen (kshot) | none (use `still <g> 50 6`) | `draft a:b:s` -> work/draft/g_ | `render [a:b]` -> raw/g_, 8 samples | `post` -> frames/ | `contact`; `qa` (kqa.py) -> meta.json, cues.json, contact.jpg |
| map_mech (mc) | `probe a:b s` | `draft a:b:s` -> work/draft/g_ | `render [a:b:s]` -> frames/g_ directly (no streak post) + work/meta | `post` (this example) -> meta.json, cues.json, contact.jpg | `motion` -> work/motion.json |

Measured final frames (720x1280, 2 threads): office_day g47 10.5 s wall, 21.4 s CPU (12 samples); beach g47 11.6 s plus a plate and
matte pass because the frame is fast; kitchen g57 6.4 s (8 samples). A 42-frame take is about 8 to 10 minutes on 2 threads.

`python3 smoke.py --chain [names]` also runs a whole take as a worker does (every frame drafted, the drafts scaled to 720x1280 used as
raw frames, then post, contact, qa) and checks that frames/, meta.json, cues.json and contact.jpg exist. All five passed.
`python3 smoke.py --clean` deletes every output. Delete `work/sprites` and `work/raw` of a take once its frames/ are checked.

## Takes to a film (`film_mini.py`)

```sh
python3 film_mini.py conform ../film_test office_day beach kitchen    # 27 s: frames/f_%04d.png, joins.json, cues_all.json
python3 film_mini.py grade ../film_test --procs 3                     # graded/: the v1.1 grade with DEFAULT settings (optional shots.json)
python3 film_mini.py captions ../film_test caps.json --frames graded   # film_silent.mp4 via assemble.py; --style th88 (default) | th72 | en
python3 film_mini.py mix ../film_test mix.json                         # film.wav + film.mp4 via audio/mixer.py
```
Tested on the three example takes: 108 frames (3.60 s), two 5-frame dissolves (g 34..38 and 70..74), 7 cues, 720x1280 H.264 + AAC.
The examples all sit on g 30..66, so the conform laid them back to back (shift -30, +6, +42); takes cut to one narration clock
(g1 of one = g0 of the next) keep their own frame numbers. `caps.json` is `[{"t0", "t1", "text"}]` on the film clock;
`mix.json` is mixer.py's spec (`voice`, `music`, `sfx` list) without duration and video, which film_mini fills in. The test used
stand-in sounds made with ffmpeg (`sine` voice, `anoisesrc` whoosh and bed); real effects come from `audio/sfx/make_sfx.py`
(fal.ai, paid) or your own files.

## Notes and limits

- `office_day` reads the chief's mouth from `common.synth_loud` (no narration yet). With a voice, use
  `acting.loudness(t0, t1, path="<narration.wav>")`; without the `path` it opens film 1's `audio/th/full_v2/narration.wav`, which
  is not shipped (film 1's take s10 fails on import for that reason).
- `kitchen`: the set has a floor plane but only what its three cameras see; there is no place in those framings for a 4 D puppet.
  For a new kitchen scene with characters, build a set (see references/look.md, "A new set").
- `map_mech`: puppets are 4 D tall and the lens works 0.35 to 1.8 D from the map; characters belong in the office shots around it.
- The paper artwork is drawn with Kanit ExtraBold and Kanit Black, shipped in `fonts/th/` (SIL Open Font License); `setup_kit.sh` fills a missing file with a copy of Kanit Black.
  Without `paper.py build` the props module silently uses magenta-striped `PLACEHOLDER_*` cards (spinner disc, label, calendar).
