# QA s13 (film 17 ending, shots 31-33), re-render round 2, g 1862-2051 (g0 1868, g1 2052, 6 handle frames before, none after: hard cut at 2052)
take.mkv is split (`cat take.mkv.part* > take.mkv`), 190 frames 720x1280. transition_in dissolve 11. Cuts inside: 1947, 2014.
- qa_auto PASS (magenta 0.0 %). rhythm.py (cuts 1947,2014): in-shot median 4.45, p90 12.58.
- Full-res frames for review: full/g1917 g1987 g2007 g2030 g2050.jpg.

## Changes vs round 1 (gate: QA-tech FAIL / QA-art FIX-FIRST)
- Systemic: all `beam_fx` light shafts hidden (no see-through wedge / skirt / ghost leg); dust: a quarter of the motes, k 0.4; stray floor cross gone (it was not in the new set-ups, checked g1947-1967 on the 6 fps sheet); inspector pose built with `cast17.silent()`, no `t` key (no idle mouth), so his mouth shape is constant in every frame; the only face change is blinks.
- Calipers: Bertillon now stands at the inspector's camera-LEFT, the calipers bar vertical in his right hand with the jaws pointing at the ear (one tip above, one below), pinned with hand_for_anchor. Ear drawn on the inspector sprite (screen-left ear). Shot 31: hand at waist/chest, clear of every face. Shot 32: jaws approach over g1960-2000 and clamp the ear (bar >= 250 px). Shot 33: clamped on the ear with Bertillon's hand low-left, no head disc at the edge.
- Shot 31: camera starts at 2.85 m (was 3.4) and higher/closer, floor reduced; coat rack and camera-hood slabs removed from the opening (fg is a stool with a kepi that slides out); two 11 f snaps (g1884, g1917).
- Shot 32: camera from the right-front, Bertillon never in front of the ear; inspector's eyes slide sideways toward the calipers over g1950-1972; Bertillon's gaze goes down to the ear.
- Shot 33 (shared insert spec as I read it): camera ~0.95 m, 0.3 m below ear height, swung ~60 deg to the side, ear at x ~260-330 y ~560-620, quick x1.4 push, moustache twitch (head-roll pulse) g2027-2034, no blink after g2005 (no slit-eye frame). I used the screen-left ear with the bar vertical (jaws point at the ear) instead of "bar exits frame left": team 1's shot 3 should match this geometry; please compare.
- Inspector card moved 0.28 m toward the lens (image unchanged) so the 3D headrest pad never cuts his face.

## Self-check (selfcheck.py)
6 fps sheet (every 5th frame, y 880 line) in check/sheet6fps_0.jpg, cut strips check/cut_1947.jpg, cut_2014.jpg: no spikes or frozen runs outside the cuts; heads and chins above y 880 in every sampled frame; no see-through wedge; calipers held in a hand in all sampled frames of 31 (small, at the waist), 32 and 33.
## Known remaining
- Shot 32 start (g1947-1965): the dark camera-tripod hood still shows at the top-left edge (about 20 % of the width), sliding out by about g1970. I did not re-render a third time for it.
- Shot 31 gendarme and prisoner are small in the early wide frames but taller than 180 px (card heights 1.7-1.8 m at ~2.9 m).
- I only looked at every 5th frame, not every frame, and not at full res outside the five listed frames.
