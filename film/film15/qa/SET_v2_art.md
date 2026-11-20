# SET gate v2, film 15 — QA-art (independent, opus)
Date 2026-11-20. Inputs: work_v2_a/sheet.jpg + stills s1-s7 + bigzoom1_strip.jpg; work_v2_b/sheet.jpg + stills (8); API_v2_a/b.md;
shot_plan.md (v2); FACTS.md; references film/ref_shorts/R2_sheet.jpg and the film-2 model film/v3/film2/s01/contact.jpg.
Note: film/QA_TEAM.md on this branch has no sections G/H/I (it ends at §F). I judged against the §G/§H/§I criteria as given in the
brief and the "Hard rules for v2" in shot_plan.md. Text signs are allowed (client rule for this remake).

## Verdicts
| | verdict |
|---|---|
| Location A (Medford 1963) | **PASS-WITH-NOTES** (one required builder fix, A-1, before T1 renders) |
| Location B (Mexico 1968 / 1972) | **PASS-WITH-NOTES** |
| Overall SET gate | **PASS-WITH-NOTES** — no blocking issue; the "rich and detailed?" question is answered YES for both locations |

## Numbers (re-measured with work_v2_a/stats.py on the current stills; B from stills_log.json)
| still | sat | vivid % | luma | shade hue | magenta % | flag |
|---|---|---|---|---|---|---|
| A s1 BZ1 start | 0.60 | 62 | 108 | 223 | 6.7 | shade hue < 240 |
| A s2 BZ1 mid | 0.58 | 67 | 101 | 232 | 1.4 | |
| A s3 BZ1 end | 0.61 | 64 | 105 | 204 | 0.8 | shade hue < 240 |
| A s4 T1 low hero | 0.54 | 53 | 110.5 | 227 | 1.2 | luma at the limit |
| A s5 T2 OTS | 0.55 | 46 | 110.2 | 185 | **10.6** | vivid barely 45, magenta > 10 %, shade hue 185 |
| A s6 T2 newspaper | 0.53 | 87 | **114.8** | 237 | 0 | luma > 110 |
| A s7 T7 buried | 0.65 | 76 | 97 | 236 | 2.0 | |
| B bz_start | 0.55 | 54 | 98 | 244 | 0.4 | |
| B bz_mid | 0.52 | 53 | 104 | 244 | 1.3 | |
| B bz_end | 0.72 | 81 | 95 | **277** | 3.2 | shade hue > 260 |
| B t4_low | 0.82 | 84 | 96 | 247 | 2.3 | very high sat |
| B t4_coach | 0.55 | 56 | 88 | 249 | 0.7 | |
| B t5_arch | 0.73 | 76 | 111 | 256 | 2.9 | luma at the limit |
| B t6_top | 0.82 | 88 | **84** | 232 | 1.3 | luma < 85 |
| B t7_day | 0.78 | 85 | 104 | 263 | 4.7 | |
All stills meet sat >= 0.50 (§I) and vivid >= 45 %. Luma misses are small and per shot (render-team grade). Shade hue misses are a
§A take-gate item; flagged now so the teams grade for it.

## Location A — Medford 1963
**§H rich and detailed? YES.** 430 houses with coloured roofs, streets, cars, water tower, church, pine hills, 400 m oval with an
active infield (tents, hurdles, runners, long jump), gym with MEDFORD HIGH, TRACK & FIELD gate, HIGH JUMP board "BAR 5'8"", maroon/gold
bunting, ~250 spectators. Clearly denser than v1 and on par with the film-2 town (R: film2 s01).
**BIGZOOM 1 (strip):** start: town from ~100 m, Dick far < 5 % — good. End: Dick medium ~36-40 % of frame height — good. Mid: frames 7-9
of the strip pass over plain grass with blotchy round tree shadows; the plan asks to go "through the pines and over the bleachers (MEDFORD
HIGH sign)", and the sign is never in the path. Workable, see T1 notes.
**§G:** saturation fine; contact shadows present on s3/s5 cards (long sun shadows), no bar through a face (s4: the bar crosses at the
neck, which is the correct arch). Faces all < 35 % (largest: s7 coach ~22 %, s5 Dick ~20 %).
**§I:** low warm sun with long shadows, blue-violet shade, warm rim on cards (yellow edge visible on s3/s5), signature amber + maroon vs
deep sky blue all read. "Same channel?" — yes, close to the film-2 model (blue sky + clouds, warm brick, chibi cards in a 3D town); it is
harder-edged and more saturated than the R2 reference, which is what the client asked for.
**Facts:** the high-jump pit is sawdust with a sawdust mound (s4, s7, newspaper photo) — correct. BUT see A-1.

### Notes A
- **A-1 (builder, REQUIRED before T1 renders; fact limit):** `v2_a.py` ~line 761 builds "pole-vault / high-jump style mats (blue)"
  — two blue 5 x 4 m foam blocks with standards in the 1963 infield. FACTS.md: no foam landing mats in the 1963 school scenes.
  Change them to a sawdust/wood-chip pile in a wooden frame (or delete). One-line fix; it is not a gate FAIL because no still shows
  them prominently, but nothing with foam may appear in T1/T2/T3/T7.
- **A-2 (builder, T1/T2/T3/T7):** god rays (`SHT.rays()`) render as white smudges/streaks across the sky and over the bunting (s2 right,
  s3 top-left, s5 left, strip end). They read as smears, not shafts through pines. Keep them in the pines only (below the horizon,
  cull quads above the tree line or seen edge-on), or lower k.
- **A-3 (builder, T7):** s7 sawdust spray: the chips are plank-sized blocks, several hang across the coach's face and in the sky; and the
  sawdust heap behind him is a flat beige card silhouette in front of the 3D mound (reads as a slab). Scale chips to ~1/3, keep the face
  clear, use the 3D mound (or shade the card to match its lit surface).
- **T1 (render):** BIGZOOM 1 mid: lower the path so it passes over the bleacher and the MEDFORD HIGH sign/bunting instead of open grass.
  s4 low hero: frame so the sawdust pit and Dick's shadow on the sawdust are in shot while he is airborne (now the pit is off-frame
  left and the bar floats against sky). Grade luma below 110.
- **T2 (render):** s5 is not an over-the-shoulder: Dick faces the camera and hides the coach (the subject). Use a back-view Dick at
  the frame edge (API says the OTS Dick is still a 3D stand-in — needs a back card), coach clear and readable. Fix magenta (10.6 %) and
  the cyan-ish shade hue in this grade. s6 newspaper: luma 114.8 — darken the paper; keep the full-frame page short (push-through
  only, ~1 s), with hands/edges or world visible as soon as the pull-back starts (client dislikes flat 2D panels).
- **T3 (render):** DAY shift (`HERODAY`) is untested by the builder — check it on the first frames for luma/sat before the full take.

## Location B — Mexico City 1968 / 1972
**§H rich and detailed? YES.** Lit city to 2.5 km, mountains and volcano cones, avenue with lamps and cars, 8 floodlight towers with
beams, 28+18 MEXICO 68 banners, 18.5k crowd with flash-bulb sparkle, cauldron, HIGH JUMP scoreboard, 2.24 m board, podium. bz_start
and bz_mid are the strongest set images of the film.
**BIGZOOM 2:** start Dick ~4 px (< 5 %), mid through the beams over the bowl, end Dick ~45 % medium. Start/mid/end all workable.
**§G:** contacts and shadows OK (check_grounding empty on all 8). Faces < 35 %. One near "bar through head" in bz_end (B-T3).
**§I:** floods + beams as motivated key, hard white rim on t5_arch, warm cauldron + cool night blue in one frame, signature hot tartan
red + night blue + white beams all there. "Same channel?" — yes in the wides; at pit level the look is louder than the references
(see sat 0.72-0.82 and the lava-like tartan in t4_low).
**Facts:** 2.24 m board/scoreboard, no "world record" anywhere (grep clean), foam mat allowed in 1968 — OK. "1972" banner on the day set — OK.

### Notes B
- **B-1 (builder, T3/T4/T5):** the orange horizon band is drawn as a curved arc high in the sky (bz_end, t4_low, t5_arch) — reads as a
  ring/rainbow over the stadium. Flatten it to the real horizon or drop it at pit-level cameras.
- **B-2 (builder, T4/T5):** tartan mottling under floods looks like molten lava in t4_low (sat 0.82). Reduce the mottle contrast and the
  orange in the near tartan.
- **B-3 (builder or render, T4):** stand crowd cards in t4_coach are one repeated face/costume (purple + red bandana or yellow) with a black
  void band behind row 6; it reads as clones. Add 4-6 more crowd card variants/colours and fill the black gap.
- **T3 (render):** bz_end: the bar runs into Dick's head at ear level (behind him, but reads as through the head) — raise/lower the
  camera or shift Dick so the bar clears his head; fix shade hue 277 in the grade.
- **T4 (render):** t4_coach: the coach is ~8 % of frame and lost in the crowd — the whip pan must land on him: put a spot/pool or a gap
  around him, centre him, and tone down the two big flash blooms near him. t4_low OK (gap ~30 cm reads, 2.24 m board in frame on the
  wider version, keep it in).
- **T5 (render):** t5_arch is the key image and works (arch, rim light, bar, HIGH JUMP board). Grade luma <= 110.
- **T6 (render):** t6_top luma 84 — lift; the frame is ~60 % empty blue mat grid (reads as a tiled floor); tilt/zoom to include the
  apron, the standard and a ring of photographers/crowd; photographers standing on the mat are fine but keep them off the landing
  zone. Two dark objects at the bottom of the mat read as debris — remove or make them clearly Dick's spikes.
- **T7 (render):** t7_day shows one jumper; plan needs three in different kits flopping one after another with smiles/thumbs up.
  Also the 1963 dissolve half (Location A) — see A-3 and A-1 (sawdust only).

## What does NOT block
All notes above are inside one take or one builder line; none needs a new set. A-1 is the only item that must be done before rendering
(fact limit), and it is a one-line change.
