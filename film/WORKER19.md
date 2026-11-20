# Render-team worker brief, film 19 (ไอ้ช่างไม้ — John Harrison's sea clocks, 1730s-1773)

Follow film/WORKER.md for the delivery format and rules (sections 4-5), with the film-19 differences below.
The client has approved the set, the cast and the render. Work autonomously; do not ask for confirmation.

## 1. Setup
```
git clone -b film19/main <repo url> && cd <repo>          # then: git checkout -b render19/teamK   (K = your team number)
REPO=$(git rev-parse --show-toplevel); PROJ=$REPO/film      # work directly in the repo; no symlink needed
pip install -q bpy numpy pillow opencv-python-headless pythainlp
python3 -c "import bpy; print(bpy.app.version_string)"      # 5.x
node -e "require('playwright')"                             # the sprite rasteriser (stage/sprites.py); never run 'playwright install'
```
Your container has 4 cores: run at most 2 render processes with 2 threads each.

## 2. Read, in this order
1. PROJ/film19/BRIEF.md and PROJ/film19/shot_plan.md: your shot rows, the Look / Camera / Mouths / Cast-and-set sections and the marks notes under the table. Your shots: PROJ/film19/TEAMS.md.
2. **The worked example: PROJ/v3/film19/s01/** (shot 1, the hook): shot.py, c19.py (the film-19 helper), deliver.py, QA.md (gotchas), meta.json, cues.json, contact.jpg, framediff.json. Copy c19.py into YOUR take folder (do not create a shared helper, do not import s01's copy). Read the docstring of c19.py first: "API DIFFERENCES" and "GOTCHAS".
3. PROJ/v3/set3d19/API.md (presets, lights, hooks, marks, hand props) and SHIP_API.md (ship_root, deck marks, set_sea / set_roll), then QA_ART.md (the NOTE lists, section 6 below) and QA_TECH.md. `import h19 as H` (c19 does it).
4. PROJ/v3/cast19/API.md (cast keys, STORY19 poses, CANVAS19, cast19.laugh_cycle / talk_mouth / blink_at, key19() name map: sailor_a -> sailor19_a; harrison19 variants young=1 / old=1 are POSE keys).
5. PROJ/skill/reference-style-shorts/references/production-lessons.md §2 (client taste) and §10 (camera rhythm), PROJ/QA_TEAM.md "Stricter QA".

## 3. Clock
Narration PROJ/film19/audio/narration.wav (71.90 s) at +0.10 s. Captions PROJ/film19/script/captions.json. g = round(t*30); **N = 2160** (72.0 s).
Sentence starts: hook 0.00 / pivot 6.37 / boss 15.54 / nickname 25.78 / count 28.74 / reveal 33.86 / aha 46.12 / false 52.71 / crisis 55.49 / ending 61.86 / end 71.90.
A shot's g0 = round(t0*30), g1 = round(t1*30)-1. In-shot events at narration time x fall on g = round((x+0.10)*30) (c19.g_of, c19.cap_g("<caption start>")).
The plan's anchor times are CAPTION-PHRASE starts; a word in the middle of a phrase is spoken later (s01: "บอกว่านาฬิกา" starts 1.12 s = g 37, the word นาฬิกา is heard about g 44). Time snaps to the spoken word.

## 4. Look and camera (hard rules)
- Sharp, NO depth of field, NO text anywhere (dials, charts and maps have tick marks and lines only). Warm lit 3D world as the approved set.
- **Never add `caption_shade`** (the director removed it). Do not set `H.STATE['caption_shade']`; c19.Take deletes it before and after H.make_camera and before every render.
- Every shot has a clear move: drift 6-10 %/s push/pull + 20-60 px/s slide, eased, plus one eased SNAP (13-25 frames, x1.3-x3) on the strongest word in every shot over 2 s. No near-static hold over 1 s; never parked more than 6 frames (c19.CamPath.report). Foreground prop 1-2 D from the lens in most shots.
- Heads: whole heads above y 880; head centre y 450-760 (wides exempt). Laughing characters bounce ~0.06 D at ~3 Hz (cast19.laugh_cycle); nobody frozen.
- Characters stand IN the world: contact shadows, correct scale (cast19 heights are true at scale 1), feet on the floor / deck. On the SHIP, parent every deck card to ship_root with c19.ride_ship(actor, A['ship_root']) BEFORE place(), and key set_sea(t) and set_roll(t) with the same t on every frame, so the cards roll with the deck. The deck bobs up to ~1.6 D and pitches ~2-3 deg (ship_deck, measured): a camera standing on the deck must ride it too (key set_roll first, then `key_cam(f, *C.on_ship(A['ship_root'], f, loc, look))`); a world-fixed camera sees the whole ship heave. Hand props are drawn by cast19 in the cards (H4 watch, quadrant, pocket watch, quill, bucket, chart); world props are set hooks.
- Key EVERY set hook on EVERY rendered frame (set_balance(g/30) rocks the H1/H2/H3 bars; set_candles(level) flickers; set_sea/set_roll animate the sea and ship).
- Final samples: the set's own (H.STATE['samples'] after build: WORKSHOP / HALL 8, SHIP 10-12 by preset; set3d19/cost_report.txt). Do not raise them. Drafts 360x640, 6 spp.
- Comic falls only, no injury (shot 5's bailing sailors).
- Target in-shot frame-diff (90x160 grey): PER TAKE median >= 4 and p90 >= 10 (director decision 2026-11-20 after TAKE gate round 2; the production-lessons §10 target median >= 4 / p90 >= 12 is measured on the WHOLE FILM at the FINAL gate, so aim higher where you can). Measure it as s01/deliver.py does (`python3 deliver.py draft` on a draft) and report it. Tune on drafts: the final comes within ~0.5.

## 5. Mouths (lip-sync windows)
Only astro19 (the mocker) moves his mouth, and only inside his quotes (±0.15 s; c19.mouth_open_at(g)):
- boss quote, shots 8-9: 20.80-25.75 s = g 627-776 (laugh "ฮ่า ฮ่า ฮ่า!" then "นาฬิกาเนี่ยนะ! … ให้พระราชามาจับเวลาเองเลย!"); drive `mouth=cast19.talk_mouth(g)` (astro_mock_point holds talk_b; the belly laugh uses laugh_cycle's laughing mouth).
- false quote, shot 20: 54.25-55.45 s = g 1630-1667 ("ฟลุ๊ค! ต้องลองใหม่!").
Everyone else, everywhere else: a still expression mouth (set `mouth="flat"` or keep the pose's fixed mouth). The jaw drop (shot 25) is a held open mouth, not talking.

## 6. Set notes you must respect (set3d19/QA_ART.md NOTE lists, rounds 2-4; handle them by camera and staging)
SHIP
- Keep characters off the rail bulwark (#3b2723, warm brown-black inner bulwark). The rail inner shade is accepted as local colour.
- ship_rocks only at STORM_DUSK (its 450 W lantern pool turns the NOON/DAY deck orange). Rocks: the lantern bars render brass not iron, lemon glass, the hanging line glows; the fog is a flat band; the far sail is periwinkle (#6576c7) at x 0-95; the cannon is violet; one sailor stood outboard in the placeholders (stage him inboard).
- ship_rail (S05): a yellow gunport slot at x 395-440, y 920-1090; foam dots float.
- ship_aerial STORM: the wake fans read as rays; a gull sits on the bowsprit (x 220-270, y 730-790).
- ship_coast: the ship's square sails render grey; a brown disc floats on the sea (x 490-560, y 600).
- ship_hero: the bow wave is still a "sled"; keep it small in frame or behind the swell-crest foreground.
- Exterior shade exception: the hull shadow on the sea (teal 205-217) and the cream sail shade are accepted; deck / hull / sand shade stay 225-265.
HALL
- hall_table: offset Harrison's mark from the King's (at harrison_table Harrison covers the King): they must not overlap.
- The window arch is stair-stepped and its muntins fan; EVENING hall_window keeps a warm sun shaft; hall_wide has carpet medallion arcs in its bottom corners (keep them low / cropped).
WORKSHOP
- H1 half-hides William at william_bench in shop_wide: offset the mark or the camera.
- shop_bench DAY is hazy: the haze is the window-shaft volume running toward the camera; s01 hides it (`C.key_vis(H.STATE['shafts'], False, f)` on every frame).
- shop_clock DAY has hot patches under the bench (y 990-1150): frame or stage over them.
- NIGHT has no moon patch on the floor.

## 7. Delivery
- Take folder PROJ/v3/film19/sNN (NN = first shot number of the take, two digits). One take per shot unless your assignment says otherwise.
- meta.json: g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}. Render 9 handle frames each side (dissolves up to 17 f: half the dissolve + 2 at least). Joins are in the shot_plan "in" column (DIS 11 / 13 / 15, CUT).
- take.mkv (ffmpeg libx264rgb crf 6). If over 45 MB: `split -b 40M take.mkv take.mkv.part`. Frames/raw/work stay out of git (film/.gitignore already ignores v3/film*/*/raw, frames, work).
- Before delivering: `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>`, fix every FAIL, add QA_AUTO.md + phone_sheet.jpg; then check yourself at 6 fps plus every cut ±3 frames (heads, contact shadows, props held, eye-lines, mouths only in quote windows, continuity with neighbouring shots) and write QA.md (as s01/QA.md).
- Push each take as soon as it is final: `git add -A film/v3/film19/sNN; git commit; git push -u origin render19/teamK` (retry with backoff). Do not open pull requests. Write only in your own take folders.
- Final message: takes delivered, frame ranges, s/frame, frame-diff numbers, anything that differs from the plan.
