# Film 20 rivet_v2: fix brief for the 2 render teams (client rejection of rivet_v1, 2026-11-22)

The client rejected film/release20/rivet_v1.mp4 for **floating objects, camera shake and cameras too close**.
Re-render ONLY the takes below. Narration, music, timing (g0/g1/first_g, handles, transitions) and every other take stay as they are.
Do NOT call fal.ai. Sonnet render teams; free automatic checks only.

## Read first (all on film20/main)
1. film/film20/QA_K_L.md: QA_TEAM §K (nothing floats: ground_check, contact shadows) and §L (no camera shake: qa_jitter ≤ 2.0 px every second).
2. film/v3/tools/ground_check.py + GROUND_TEST.md: run it on your shot scene (pip bpy: build the scene, then `run_cli()`; see its header). Flag only true airborne things (`obj["airborne"]=True`: birds, smoke, flags on poles).
3. Your take folder film/v3/film20/sXX/ (shot.py, meta.json, QA.md). WORKER20.md §1-8 still applies for setup, clock, delivery, self-check.
4. film/qa_jitter.py: `python3 film/qa_jitter.py take.mkv` (needs `pip install opencv-python-headless`). Every second must read ≤ 2.0 px. Declare the planned fast moves (BIGZOOM whoosh, whip) in GROUND.md if they read above.

## Rules for every take
- **Camera:** smooth eased keys only (Bezier / smoothstep). No random pan/tilt, no noise, no camrig.shake. Where the old camera shook, rebuild the move as one smooth travel with the same start and end framing so the dissolve handles still match.
- **Nothing floats:** every card and prop stands on a surface (ground_check PASS, gap ≤ 0.02). Delete or ground stray slabs, chunks and girders. Canopies and tables need legs that reach the ground.
- **Contact shadows:** every standing character card and free prop gets a soft blob/contact shadow on the ground under it.
- **No giant foreground heads or cards** that block the frame. Foreground framing objects must be props (posts, chairs), not a character's head.
- **Not too close:** no face fills the frame. Medium shot at most: head ≤ 22 % of frame height, unless the plan says close-up.
- Keep the look (set3d20/cast20 materials, light, colour). The final grade is applied at conform.

## Team A (render20/v2a): T03 (s03), T21 (s21), T18 tail (s18)
- **T03 (g170-411, BIGZOOM 1):**
  - At ~g225 (7.5 s) the white canopy/table has no legs, and a grey tower-leg slab hovers off the dirt. Give the canopy 4 legs to the ground, and ground or remove the slab.
  - 10-12 s (g300-360): the camera shakes (qa_jitter 3.9 px at 10 s, 3.1 px at 12 s). Make it one smooth crane up the leg.
  - At ~g330 (11 s) a girder chunk floats in the sky/foreground. Remove it or put it on the ground.
  - Keep the BIGZOOM timing (<5 % to ~36 % in ~3.1 s on "วิศวกรไอเฟล"), the warm marker and both 13-frame dissolve handles.
- **T21 (g1427-1663, night antenna and group):**
  - The camera shakes at 48 s and 52-54 s (3.0-3.6 px). Make the moves smooth.
  - At ~g1575 (52.5 s) the people on the cobbles have no contact shadows. Add them, and ground_check every card.
  - Keep the cut in at g1431 and the dissolve out.
- **T18 (g1210-1438):** only 46 s (g1380-1410) reads 2.1 px. Smooth that last move (partial re-render g1370-1438 is fine) and keep the hard cut out at g1431.

## Team B (render20/v2b): T09 (s09), T11 (s11), T23 (s23)
- **T09 (g600-760, window room, Maupassant's vow 22-25 s):**
  - Through the window the tower must be UNDER CONSTRUCTION (unfinished: the legs and first platform rising, scaffold and crane, as in the SITE set), standing on visible ground, not a finished purple tower floating in the sky.
  - At 24.5 s (~g735) his face fills the frame. The shot must end at a MEDIUM (head ≤ 22 % of height, chest-up or wider). A slow push that ends at medium is fine.
  - Keep the match-in from T06 and the dissolve out.
- **T11 (g745-1003, crowd and the construction, 25-33 s):**
  - At 25-26.5 s a ghost glass/window reflection covers the left of the frame (the grey vertical overlay). Remove it.
  - The tower base and the crane must stand visibly on the ground, and the framing must be wider.
  - The orange slabs and crates must be grounded, not floating, and the crowd needs contact shadows.
  - The camera shakes at 27-31 s (2.0-2.5 px). Use smooth eased moves.
- **T23 (g1648-1740, the 70-year extension at the fair, ~55-57.7 s):** at 57 s (~g1710) a giant dark head card blocks the bottom-left foreground. Remove it or push it out of frame. Keep the dissolves.

## Delivery per take
Push to your branch, with these in the take folder:
- take.mkv (split into .part files if over 95 MB) and meta.json (handles unchanged)
- QA.md with what changed
- GROUND.md (ground_check report, PASS)
- the qa_jitter output pasted into QA.md (every second ≤ 2.0 px, or declared)
- qa_auto PASS
- a 1 fps contact sheet

Reply to the director with the commit and those numbers. Keep a background waiter alive while you render. When all your takes pass, the director archives your session.
