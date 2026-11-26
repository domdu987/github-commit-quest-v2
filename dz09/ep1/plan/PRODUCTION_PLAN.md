# DEAD ZONE 09 / เขตปิดตาย 09, EP.1: production plan

Written 2026-11-26 by the script editor / line producer, from the screenwriter's draft and the production supervisor's audit in this folder. Paper work only: nothing was rendered or recorded, no network call was made, and nothing outside `ep1/plan/` was written.

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`

| File in `PROJ/ep1/plan/` | What it is |
|---|---|
| `narration_ep1.md`, `.json` | The edited narration (this plan's script). Draft kept as `narration_ep1_draft.*` |
| `shots_ep1.md`, `.json` | The shot list reconciled with the audit, with an asset list per shot. Draft kept as `shots_ep1_draft.*` |
| `continuity.md` | The screenwriter's continuity sheet with an "Editor's amendments" section at the end. Draft kept as `continuity_draft.md` |
| `assets_audit.md` | The supervisor's audit (unchanged) |
| `_gen_v2/edit.py`, `write2.py`, `numbers.json` | The edit tables and the generator of the files above; every number in this plan comes from `numbers.json` |

## 1. The episode in numbers

| | |
|---|---|
| Running time | **5:18.96** (7,655 frames at 24 fps). The hook is frames 0-1279 and is not touched; the new picture is **6,375 frames** (265.6 s) |
| Shots | **137** new (S25-S161), mean 1.94 s; the hook is S01-S24 |
| Narration | 85 new sentences (s17-s101), 211 captions, 62 with a coloured key word |
| Characters to record | **2,527** spoken Thai characters; **2,685** with spaces and punctuation (the billing count) |
| Final render | **91.3 CPU h = 24.7 wall h** on the 4 cores; **123.3 CPU h = 33.3 wall h** with the audit's 35 % allowance |
| Drafts | 16.8 CPU h = 4.5 wall h for one full pass at 360x640; two passes budgeted = 9.1 wall h |
| Assets to build | about 7.9 builder-days of sets, 3.75 of cast, 2.0 of motion cycles, 1.5 of pipeline, and 137 shot modules |

Frames per render class:

| Class | Shots | Frames | CPU s / frame | CPU h |
|---|---|---|---|---|
| A: a named character's face is read (and the two wound inserts), 100 % scale | 78 | 3,577 | 68.2 | 67.8 |
| B: wide, crowd, driving, environment, prop or hand insert, 75 % | 45 | 2,192 | 36.6 | 22.3 |
| C2: the hook's jaw / gauge macro re-staged, 75 %, 4 spp | 2 | 115 | 32 | 1.0 |
| C1: drawn 2D or reused frames, no Cycles render | 12 | 491 | 2 | 0.3 |
| All | 137 | 6,375 | | **91.3** |

- The per-frame costs are measured on the hook final as it was running (530 frames in `v10/film/out/final_720x1280/log_*.jsonl`, read at 07:32): 68.2 CPU s at 100 % and 36.6 at 75 %. Wall time per worker ran 6-9 % over CPU time, so wall hours here are CPU hours x 1.08 / 4.
- The total is hardly lower than the draft's 95.5 CPU h, although 376 frames went. The draft used the README's older 65 CPU s for 100 % frames; at today's measured cost the draft list is 97.2 CPU h. The saving from the reconciliation is in builder-days (section 3), not in render hours.
- A stays at 56 % of the frames because the story after the title is four people talking and hiding, and the standing decision is 100 % scale wherever a character is read.

Per scene:

| Scene | Episode time | Length | Shots | Frames (A / B / C2 / C1) | Final CPU h | Final wall h | Wall h with allowance | Draft wall h (one pass) |
|---|---|---|---|---|---|---|---|---|
| 02 rest, คนที่กลับมา | 0:53.32 - 2:05.59 | 72.3 s | 37 | 1,734 (1,126 / 441 / 0 / 167) | 25.9 | 7.0 | 9.4 | 1.2 |
| 03, รถกู้ภัยคันสุดท้าย | 2:05.59 - 3:14.42 | 68.8 s | 36 | 1,652 (993 / 609 / 50 / 0) | 25.4 | 6.9 | 9.3 | 1.3 |
| 04, สิ่งที่ต้องทิ้ง | 3:14.42 - 4:03.38 | 49.0 s | 23 | 1,175 (633 / 456 / 0 / 86) | 16.7 | 4.5 | 6.1 | 0.8 |
| 05, ลูกสาว | 4:03.38 - 4:28.71 | 25.3 s | 13 | 608 (363 / 127 / 0 / 118) | 8.2 | 2.2 | 3.0 | 0.4 |
| 06, ประตูที่ไม่เปิด | 4:28.71 - 5:18.96 | 50.2 s | 28 | 1,206 (462 / 559 / 65 / 120) | 15.1 | 4.1 | 5.5 | 0.8 |
| Total | 0:53.32 - 5:18.96 | 265.6 s | 137 | 6,375 (3,577 / 2,192 / 115 / 491) | **91.3** | **24.7** | **33.3** | 4.5 |

All times and frame numbers are estimates until the narration is recorded: the hook's own sentences ran from 6.8 to 18.1 characters per second, so a single line can be 30 % off. The cut is rebuilt from the real caption timing of each scene, as it was for the hook.

## 2. What the script edit did

Details and the full script are in `narration_ep1.md`. In short:

- **The hook's 60 seconds are counted on screen in real time.** The bite is at 0:43.80. The first words after the title are 'เหลืออีก 50 วินาที' (0:53.62), then '30 วินาที' (1:13.80), '10 วินาที' (1:33.80), and the eyes open on 'ลืมตา' at about 1:41.5, which is 57.7 s after the bite. Kong's watch shows it four times (S26, S36, S44, S47): one red second hand going round to a drop of blood on the 12 mark, with no digits to read.
- **The first 10 seconds after the title** restate the countdown, show the fight, and raise a question (the infected man drops his victim to go to a car alarm). The siren answers it at s54 and the flare uses it at s66.
- **Dialogue.** The 20 screenplay lines used are word for word. The guard's line is the only invented one. Kong does not speak in the call, as in the screenplay.
- **Four contradictions were fixed.**
  - The battery no longer blinks: the bible says three bars in EP.1. The hook's 'แบตเต็ม 3 ขีด' is paid at the hospital chain instead ('แบตยังเต็ม 3 ขีด ตัดโซ่ขาดแน่', and he still cannot use it).
  - The draft's last-scene line put a 60-second clock on Tos, who has been with the group for minutes. It now says only what Kong saw: 'น้องของเขา ใช้เวลาแค่ 60 วินาที'.
  - The junior no longer chases James over the roofs for 45 s without catching him. He loses him behind the bus and comes back to James's shout.
  - The crowbar cannot be both in Kong's hand in SCENE 02 and chosen from the truck in SCENE 04 (the screenplay has both). He shoves with the cutter he is holding.
- **Five sentences were cut, nineteen reworded or tightened, one added** ('ก้องคิดว่า เขาเสียน้องไปแล้ว', which puts Kong one step behind the audience just before the eyes open). The episode lost 16 s.
- **It ends on the cliffhanger:** 'ก้องยกชะแลงขึ้น / แต่เขาจะฟาด ใคร', black on 'ใคร', end card.

## 3. What the reconciliation with the audit did

Details are in `shots_ep1.md` ("What the reconciliation changed" and the asset register). Every shot now lists its set, cast, props and cycles, and each of those is either existing or in the register below.

| Asset group | Audit's list | This plan | How |
|---|---|---|---|
| Sets | 11-12 builder-days | **7.9** | No driving truck exterior; no sedan underside; the lorry is the set's own `truck6`; the stair is one flight module, never seen whole; the street under the expressway is only what a near-black frame shows; hospital people are silhouettes; the building site is a hall and a silhouette; no bus-window set |
| Cast | about 4.1 | **3.75** | Namnuea stays a voice; James has no box; the crowd is the ten existing roles made infected, at most twelve distinct figures in a frame |
| Motion cycles | about 12 cycles, 2-3 days | **8 cycles, 2.0** | No run toward the lens (those crowds are waist-up over the bonnets), no lying figure, no fall, no backward drag, no drive-and-brace |
| Shots | 143 | **137** | Seven cut, one added; seven changed class |

Builder-days per scene (assets only, before review):

| Scene | Sets | Cast, props, cycles | Days |
|---|---|---|---|
| 02 | X1 dressing (alarm lamps, glass burst); the watch drawings | junior bitten / dying / infected; infected transform; James; support walk, roof run and jump, sprint, survivor run, waist-up crowd | 3.5 |
| 03 | overturned sedan; X2 dressing (box truck, gate, taxi); truck exterior as a hero; cab interior | Praew; Tos; slam loop | 4.05 |
| 04 | equipment wall in the cab; service stair and the street under the expressway | Tos's torn sleeve and snag; stairs gait; flare; crowbar; map and lock screens | 3.45 |
| 05 | none new | call screens | 0.2 |
| 06 | hospital gate and facade; building site | guard | 2.5 |
| Sum | | | 13.7 |

Shot modules are extra: 137 of them, about 7-8 builder-days at 18 a day (the hook's rate was not recorded; this is the least certain labour figure). With the pipeline (1.5) and a third on top of sets and cast for review, the whole build is about 27 builder-days, which only fits the calendar below if scenes are built in parallel lanes.

## 4. Build order

### Step 0: before anything is built (today)

1. The hook final finishes and is conformed. Nothing else uses the cores until it has.
2. **Backup 0** (section 6).
3. The user answers the decisions in section 8. Recording and building wait for decision 1.

### Step 1: pipeline generalisation (about 1.5 builder-days; `v10/film` stays untouched)

A new package `PROJ/ep1/`, as the audit proposes:

1. `ep1/cut/scNN.json`: per scene, the narration offset, shots, named cues, hard cuts and emphasised words. Picture cues are written against caption phrases, not seconds.
2. `audio/ep1/scNN/`: script, takes, final narration, caption timing, mix. Audio first; the cut is derived from the caption timing.
3. `ep1/shots/scNN/sNNN.py`: the hook's shot contract plus `LOC`, `CAST`, `CLASS`.
4. `Stage(location, cast)` with a registry of location builders (`deck`, `cab`, `under`, `riverside`), so a render process builds only what its scene needs.
5. `run.py --scene scNN [--shots ...]`: one folder per shot; a frame is a pure function of its number; PNGs are written to a temporary name and renamed; existing PNGs are verified and skipped on resume; a manifest per shot (frames, code hash, CPU seconds); a queue script that restarts dead workers and moves to the next shot. Within a scene B and C shots render first, A shots last.
6. `finish.py scene scNN` gives the scene clip; `finish.py master` joins the scenes' frame sequences (not their mp4s), one caption file, one mix normalised as a whole (-14 LUFS, at most -1 dBTP).
7. The hook is referenced as `sc01`; its frames stay where they are.

Gate: the hook re-conforms through the new `finish.py` to the same picture and sound as the delivered hook, without re-rendering a frame.

### Step 2: narration recording (once, all five scenes)

After decision 1. The lead reads the service's current rate first, records s17-s101 in one session (takes differ between sessions, and a later re-record moves the cuts), checks every take against the script, and builds caption timing per scene. Then each scene's cut JSON is generated and the frame ranges in `shots_ep1.json` are replaced by the real ones.

### Step 3: per scene, the same six steps

**Assets, shots, draft, final, conform, backup.** A scene does not go to final until its draft is approved; its final is one night's unattended run.

| Step | What | Gate |
|---|---|---|
| Assets | Build the scene's sets, cast and cycles from the register in `shots_ep1.md` | Each new cycle passes the sole-drift check (`walk8.py measure`); each new set gets lookdev stills and a **24-frame cost test at final tier**, and its measured CPU s per frame replaces the estimate in this plan |
| Shots | One module per shot; continuity taken from `continuity.md` | Every line plays on its speaker; no figure with feet in frame runs at the lens |
| Draft | 360x640, 2 spp, the whole scene with captions and mix | Shown to the user; frame strips and a playback watch-through (the hook never had one) |
| Final | B and C shots first, A shots last, 4 workers, resumable shot by shot | Manifests complete; no half-written PNG |
| Conform | Scene clip with captions (Kanit Black, coloured key words), narration clearly above effects, no status icons | Loudness and caption timing checked |
| Backup | Section 6 | Done before the next scene's final starts |

Scene order and what each needs first:

1. **SCENE 02** (existing set). Junior variants, infected transform, James, watch drawings, alarm lamps; cycles: support walk, roof run and jump, sprint, survivor run. Tests before final: twelve infected figures in one frame (memory per worker and CPU).
2. **SCENE 03.** Overturned sedan, X2 dressing, truck exterior with opening door, cab interior, Praew, Tos, slam loop. Tests: through-glass shots at 6-8 spp (the audit expects +20-50 % on them); four full-size puppets seated in the cab.
3. **SCENES 04 and 05 together** (they share the cab and the set under the expressway). Equipment wall, stair module, the dark street, Tos's torn sleeve tied to the anatomical left arm, stairs gait, flare, crowbar, phone screens. Test: the dark set's noise at 5 spp.
4. **SCENE 06.** Hospital gate and facade, building site, guard. Test: the gate bars at 100 %.
5. **Master.** Join, one caption file, one mix, loudness, a full playback review, re-renders from the allowance.

### Calendar (holds only with parallel lanes and same-day draft approvals)

| Day | Daytime (build and drafts) | Night (final, 4 workers) | The user receives |
|---|---|---|---|
| 0 | Hook final ends and is conformed; decisions; backup 0; pipeline starts | (hook final) | Hook final |
| 1 | Pipeline done; narration recorded; SCENE 02 assets and shots; draft 02 (1.2 h) | Final 02 (7.0-9.4 h) | Draft 02 |
| 2 | SCENE 03 assets and shots; cost tests | Draft 03 (1.3 h) | **Scene 02 clip** |
| 3 | SCENE 03 fixes; SCENES 04-05 assets | Final 03 (6.9-9.3 h) | Draft 03 |
| 4 | SCENES 04-05 shots; draft 04-05 (1.2 h) | Final 04 and 05 (6.7-9.1 h) | **Scene 03 clip**, draft 04-05 |
| 5 | SCENE 06 assets and shots; draft 06 (0.8 h) | Final 06 (4.1-5.5 h) | **Scene 04 and 05 clips**, draft 06 |
| 6 | Master conform, mix, playback review | Re-renders | **Scene 06 clip**, then **EP.1 master** |
| 7 | Reserve | | |

Every final fits one night. A draft that is not approved the day it is shown moves every later night by one.

## 5. Deliverables

| Clip | Content | Length |
|---|---|---|
| `deliver/ep1_sc01_hook_final.mp4` | The hook as already made (S01-S24) | 53.3 s |
| `deliver/ep1_sc02_v1.mp4` | S25-S61: the 60 seconds, the junior turns, the expressway falls | 72.3 s |
| `deliver/ep1_sc03_v1.mp4` | S62-S97: the rescue, the truck, the siren | 68.8 s |
| `deliver/ep1_sc04_v1.mp4` | S98-S120: four things, the flare, the sleeve, the stair | 49.0 s |
| `deliver/ep1_sc05_v1.mp4` | S121-S133: the call | 25.3 s |
| `deliver/ep1_sc06_v1.mp4` | S134-S161: the gate, the blood, the crowbar, end card | 50.2 s |
| `deliver/ep1_master_v1.mp4` | The whole episode, 9:16, 720x1280, 24 fps | 5:19 |

Each scene clip is also sent as a draft (`..._draft.mp4`, 360x640 upscaled) before its final night. Each ends on an open question, so it can be watched alone. With every scene clip the user also gets `ep1_upto_scNN.mp4`, the film so far from frame 0.

## 6. Backup step

The project (13 GB) lives in a scratchpad under `/tmp` on a temporary container (uptime 9.9 h when this was written). A reboot or cleanup removes all of it. No durable destination exists yet: this is decision 4.

| When | What | Size |
|---|---|---|
| Backup 0, today | Source without renders (code, docs, JSON, fonts, uploads) + code-drawn textures + `audio/narr_ohm` (the paid takes and the mix) + this plan folder | about 7 MB + 25 MB + 43 MB |
| End of every working day | The same set, plus `ep1/` source and `audio/ep1/` (new paid takes the same day they are recorded) | under 150 MB |
| After every scene final, before the next final starts | The scene's shot manifests and a mezzanine of the scene (H.264 CRF 15, about 1.2 MB per second: 30-90 MB a scene, about 320 MB for the five new scenes) | under 100 MB a scene |
| Never | `out/` frame folders (0.83 MB a frame: 5.3 GB for the new frames), EXR passes, raster caches | |

If the machine is lost, source plus audio plus the cut JSON rebuild everything; the cost is re-rendering whatever was not yet in a mezzanine, which is at most one scene's night because of the "backup before the next final" rule. A mezzanine is good enough to finish the master from if a scene's frames are gone.

## 7. Narration recording cost

| | |
|---|---|
| Script | 2,685 characters with spaces and punctuation (the hook was 609) |
| With retakes | about 3,970 characters synthesised, at the hook's measured ratio of 1.48 (27 takes for 16 sentences) |
| Speech-to-text check | about 6 minutes of audio, at the hook's ratio (76.7 s checked for 50 s of narration) |
| Price | **Not recorded anywhere in the project, and not looked up** (no network call was allowed in this phase). From memory, and to be verified by the lead before recording, this kind of service bills on the order of US$0.10 per 1,000 characters and a few cents per minute checked. That would put the session at **well under US$1**, and under US$2 even if the whole script were recorded twice |
| Rule | One session for all five scenes, after the text is approved. Anything re-recorded after the picture is cut moves the cuts |

Recording is negligible beside the render: the real cost of every added sentence is about 3.4 CPU h per 10 s of picture.

## 8. Decisions that are the user's

| # | Decision | Recommendation |
|---|---|---|
| 1 | **Approve the narration text for the paid recording** (`narration_ep1.md`, "Text for the recording"). It includes four causes the screenplay does not have (a car alarm draws the infected driver off; James is the roof-runner and the turned junior follows him to the truck; a road flare gets them out of the surrounded truck; the guard's line 'เปิดไม่ได้! ใครโดนกัดมาบ้าง ก็ไม่รู้!') and the last line 'แต่เขาจะฟาด ใคร', whose force is that the audience has seen the glass cut Tos and Kong has not | Approve. Each invented cause supplies a "therefore" the screenplay leaves open and uses only the world rules |
| 2 | **Length: 5:19 against the screenplay's 06:40** | Keep 5:19. Nothing in the screenplay's story is missing; what went is travel and repetition. Reaching 06:40 would add about 28 CPU h and about 40 more shots |
| 3 | **Render budget on a temporary machine:** about 25 wall h of final (33 with the allowance) plus about 9 of drafts, over four unattended nights, with character shots at 100 % | Accept as planned. The one lever worth knowing: the 1,383 medium-shot frames at 75 % instead of 100 % would save 12.1 CPU h (3.3 wall h) at some loss of line crispness; not recommended, because crisp lines were your call |
| 4 | **Where backups go.** Nothing may be pushed anywhere without your word | A source-and-audio archive (under 150 MB) delivered to you as a file each working day, and the scene clips as they are finished. If you also want it in git, say which repository and branch |
| 5 | **Battery gauge:** three bars steady through EP.1 (the bible), or the third bar starting to blink (the draft's idea) | Steady. The script is written that way |
| 6 | **Namnuea in SCENE 05:** heard only, with her avatar on the phone as in the hook, or seen once at the evacuation bus window | Heard only. Seeing her costs a new set and her full puppet for one 3.5 s shot (about 0.4 builder-day and 1.6 CPU h), and saves her face for EP.2 |
| 7 | **The wristwatch as the visible 60-second count** (four full-frame inserts, 167 frames). It is a prop on Kong's wrist, not an overlay, but you ruled out status icons | Keep it. Without it the count is only in the captions |

Decided here, not asked: no second title card (the hook's title stays where it is; the episode closes on an end card); lines are not attributed in words, as in the hook; nobody lies on the ground, because the puppets are upright cards.

## 9. The three weakest points of this plan

1. **Most of the cost is still unmeasured.** Only the expressway has been rendered. The cab behind glass, the dark set, the bars and a twelve-figure crowd are estimates, and shot lengths can move by up to 30 % per line once the voice is recorded. The 91 CPU h could be 80 or 125. The 24-frame tests in step 3 exist to find this out one scene ahead, not after a night is lost.
2. **The calendar needs about 27 builder-days inside six days, on a machine that can vanish.** It works only with parallel lanes and a draft approved on the day it is shown; the shot-module rate (18 a day) is a guess; and until decision 4 is answered there is nowhere durable to put anything.
3. **The staging asks more of flat upright puppets, and of one voice, than the hook did.** The roof chase, the pull from the tipped car, the struggle over the arm and four people in a cab are new kinds of action; the hook's motion was never watched in playback; and in scenes 03 and 06 four people shout in one narrator's voice, with only the close-up to say who is speaking. If a draft shows a line cannot be placed, the fix is a two-word attribution in the narration, which means a paid pick-up and a moved cut.
