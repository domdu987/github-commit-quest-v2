# Render-team worker brief, film 18 (ไอ้เสมียนวัว — Tian Dan's fire oxen at Jimo, 279 BC)

Follow film/WORKER.md exactly: section 1 setup, section 4 delivery, section 5 rules. The film-18 differences are below. In WORKER.md read every `film2` path as `film18`: takes go in PROJ/v3/film18/sNN.

## Inputs
- **Shot plan (your shots):** PROJ/film18/shot_plan.md (26 shots). Facts and dramatisations: PROJ/film18/FACTS.md.
- **Look:** wide or medium framings that show the dense lit set; an always-moving camera; warm fire against blue moon-shade. Sharp, NO depth of field, NO text anywhere.
- **Narration:** PROJ/film18/audio/narration.wav (70.10 s), laid at +0.10 s. Film end 70.40 s, N = 2112, g = round(t*30) for shot boundaries; events at x -> round((x+0.1)*30).
- **Captions:** PROJ/film18/script/captions.json (phrase times "t").
- **Sentence windows (start-end, s):**

  | sentence | window (s) |
  |---|---|
  | hook | 0.00-5.15 |
  | pivot | 5.20-15.25 |
  | count | 15.30-19.84 |
  | boss | 19.90-28.38 |
  | nickname | 28.44-31.40 |
  | false | 31.45-40.10 |
  | turn | 40.15-43.58 |
  | attack | 43.63-50.45 |
  | reveal | 50.51-60.20 |
  | aha | 60.25-65.21 |
  | ending | 65.27-70.09 |

## Camera rhythm (client rule from film 15 on, production-lessons §10; this is checked at the FINAL gate)
- **Every shot has a clear eased push or pull** of 6-10 % of the framing per second, plus a lateral slide of about 40 px/s. No near-static hold longer than 1 s. Quick push-ins on punch lines; whip and snap where the plan says.
- **Measurement:** the in-shot median frame-diff must be ≥ 4 and p90 ≥ 12. Use 90x160 grey frames, mean abs diff ×255 between consecutive frames.
  - Measure your take and write the numbers in QA.md.
  - Film 2's figures are median 5.3 and p90 19.1.
  - Characters keep secondary motion. Laughing characters bounce 0.06 D at about 3 Hz, and nobody stands frozen.
- **Foreground props:** a prop 1-2 D from the lens in most shots. The set's shot cameras already carry them.

## Set (approved by QA-art at the SET gate; the client delegated approval to QA-art on 2026-11-19)
PROJ/v3/set3d18/jimo.py. READ these first:
- API.md: cameras, marks, setters, world.
- QA_ART_SET.md and QA_TECH.md: the set-gate notes, including the non-blocking fixes to apply in your takes.

Each shot is a camera:
- `J.build(location, 'sNN')`
- `J.key_camera('sNN')`, which keys the planned move from the shot's first film frame.
- You may extend the move with handles.

Setters:
- `set_holes`, `set_gate`, `set_party`, `set_rout`, `set_pennants(k, side)`, `set_qi_return`
- `animate(setter, f0, f1, v0, v1)`
- `flicker(frame)`
- `flame_card(parent, scale)` / `set_flame_card`: flame plus a warm light on an ox card
- `jimo_shots.herd(n, a, b, width, seed)`: ox marks
- `debug_ox()`: NEVER in a final.

Key every animated setter on every rendered frame. Replace the set's placeholder cards with real cast18 cards at the marks in API.md. One location per process.

## Cast
PROJ/v3/cast18. Read API.md.
- **Humans:** tiandan, general, yan_soldier_a/b/c, old_man, woman, child, envoy, qi_soldier. Poses are in STORY18.
- **Oxen:** `ox_figure(state='plain'|'dragon', view='side'|'three_quarter', gait=..., frame=..., flame=-1|0|1|2, blades=True)` and `OX_CANVAS`.
  - Gallop with the 8 drawings at about 12 fps.
  - Flame flicker cycles through 0-2 every 2-3 frames.
  - Herds of 10-60 visible oxen: vary the phase and scale ±5 %. Use silhouettes far away.
- **Mouths move ONLY on the general's two quotes**, in the lip-sync poses general_arms_wide / general_boast / general_toast / general_carve with `talk_mouth(g)`:
  - quote 1: 22.45-28.38 s
  - quote 2: 36.99-40.10 s
  - Everywhere else mouths are still. Townsfolk beating pots use shout drawings, which do not lip-sync.
- **Comic and bloodless.**
  - Oxen charge, tents collapse, soldiers scatter and fall on their bottoms, pots and helmets fly.
  - No one is hit by a blade or horn, no blood, no bodies.
  - The blades never touch anyone.

## Worked example and helpers
- Use PROJ/v3/film8/s01/shot.py + QA.md and PROJ/v3/film8/common.py as the worked example. Read their gotchas: moves must move, key every hook every frame, one location per process.
- Make your OWN helper module inside your take folder (for example PROJ/v3/film18/sNN/c18.py) by copying film8/common.py and switching it to cast18 and set3d18/jimo.py.
- No shared film18/common.py.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
1. Before delivering, run `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <planned cut g's>` and fix every FAIL.
2. Add QA_AUTO.md and phone_sheet.jpg to the take folder.
3. Check every frame yourself at 6 fps, plus every cut ±3 frames:
   - heads above y 880
   - contact shadows
   - hooves and feet on the ground
   - props held
   - eye-lines
   - flames attached to the tails
   - continuity with the neighbouring takes (time of day, wall holes, dress state of the oxen)
   - mouths only in the quote windows
4. Write the frame-diff numbers in QA.md.

The director's QA-tech re-checks every take. QA-art must pass the key takes: s01-02 (hook), s07, s13-15 (false payoff), s19-22 (reveal), s26 (ending).

## Delivery
- meta.json holds g0, g1, first_g, n_frames and transition_in {"type":"cut"|"dissolve"|"whip","frames":n}, following the plan's "trans in" column.
- Render handle frames: half the dissolve + 2 on each dissolved side; use 6 if unsure.
- Push each take as soon as it is final to your outcome branch. Do not open pull requests.
- Work autonomously and do not ask for confirmation. The client delegated approval to QA-art, and the SET gate has passed.
