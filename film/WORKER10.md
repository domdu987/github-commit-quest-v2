# Render-team worker brief, film 10 (ไอ้ช่างม้าลาย — WWI dazzle ships, 1917)

Follow film/WORKER.md exactly: section 1 setup, section 4 delivery, section 5 rules. The film-10 differences are below.

## Inputs
- **Brief and shots:** PROJ/film10/BRIEF.md (the story, plus USER TASTE as in film 9) and PROJ/film10/shot_plan.md (23 shots).
- **Look:** wide or medium framings that show the dense set, a calm camera that is always moving, and a warm lit 3D world. Sharp, NO depth of field, no text.
- **Narration:** PROJ/film10/audio/narration.wav (60.0 s), placed at +0.10 s.
- **Captions:** PROJ/film10/script/captions.json.
- **Frames:** N = 1815, g = round(t*30).
- **Sentence starts:**

  | line | start (s) |
  |---|---|
  | hook | 0 |
  | pivot | 4.48 |
  | boss | 9.76 |
  | nickname | 17.92 |
  | count | 20.63 |
  | false | 26.27 |
  | attack | 33.27 |
  | reveal | 36.35 |
  | aha | 47.59 |
  | ending | 54.24 |
  | end | 60.0 |

## Set (client-approved, 2026-11-18)
PROJ/v3/set3d10/harbour.py. READ API.md first; its top sections cover rounds 2-3. Also read QA_TECH.md and QA_ART.md (the take notes).

**Presets**

| Location | Presets | Light |
|---|---|---|
| harbour | harbour_wide, hull_side, quay_low, hull_plank, beauty_harbour | DAY, DUSK |
| sea | convoy_wide, periscope_close, periscope_pov, topdown_sea, torpedo_chase, bridge_deck, beauty_sea | SEA_DAY |

**Hooks**
- Harbour: set_stripes(stage 0..3, fractional = painting in progress), set_harbour_dazzle(k).
- Sea: set_convoy, set_torpedo / torpedo_u / torpedo_cam, set_ghost, set_ghost_marker, set_lead_marker, set_uboat(dive, periscope), set_hit, set_smoke, periscope_overlay.
- Utility: ship_root(name), which parents cards to moving ships; and clear_keys. This clear_keys keeps drivers, so do NOT borrow clear_keys from the film 8/9 helpers, which delete the drivers.
- Key every animated hook on every frame.

**Set limits**
- The client chose the round-2 sea, which is smooth teal. Do NOT change the water.
- Cost is about 20-30 CPU s per final frame. topdown_sea is at the limit, so do not add geometry to it.
- Use set_aim_lines() no longer. It is a no-op: there are NO dashed lines or arrows. The reveal uses buoys, the ghost ship and the wake.

## Cast
PROJ/v3/cast10. Read its API.md.
- Characters: painter10 (Norman), admiral, sailor_a/b/c, uboat_captain.
- Pose keys are in STORY10; mouth=cast10.talk_mouth(g) runs only in the lip-sync poses.
- Canvases: CANVAS10_PLANK for plank poses, CANVAS10_SCOPE for the periscope pose.
- Pose keys: paint_spots (the admiral at the end), plank, periscope, brush_paint.
- Replace the set's placeholder cards with real cast10 cards. Background workers may use sailor_* idle and laugh poses at small size.

## Mouths and acting
- Mouths move ONLY on the admiral's quotes:
  - boss quote, about 11.33-17.90 s
  - false quote, "เห็นมั้ย เป้าชัดแจ๋วเลย!", about 31.60-33.25 s
- Everywhere else the mouths are still.
- The ending is comic: the admiral on the plank with brush and paint spots, sheepish. Hard cut on the last word "เอง" at about 59.9 s.

## Worked example and helpers
- Worked example: PROJ/v3/film8/s01/shot.py, QA.md and PROJ/v3/film8/common.py. Read the gotchas: moves must move, key every hook every frame, one location per process.
- Make your OWN helper module inside your take folder (for example film/v3/film10/sNN/c10.py) by copying film8/common.py and switching it to cast10 and harbour.py.
- Do not create a shared film/v3/film10/common.py.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
- Before delivering, run `python3 film/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>` and fix every FAIL.
- Add QA_AUTO.md and phone_sheet.jpg to the take folder.
- Then check every frame yourself at 6 fps, plus every cut ±3 frames:
  - heads above y 880
  - contact shadows
  - props held
  - eye-lines
  - continuity with the neighbouring takes
  - mouths only in the quote windows
- The director's QA-tech re-checks it, and QA-art reviews the key takes (hook, reveal, false payoff, ending).

## Delivery
- Take folders: PROJ/v3/film10/sNN.
- meta.json holds g0, g1, first_g, n_frames and transition_in {"type":"cut"|"dissolve","frames":n}.
- Render 6 handle frames each side.
- If take.mkv is over 45 MB: `split -b 40M take.mkv take.mkv.part`.
- Push each take as soon as it is final. Do not open pull requests.
- Work autonomously. Do not ask for confirmation: the client already approved the set and the render.
