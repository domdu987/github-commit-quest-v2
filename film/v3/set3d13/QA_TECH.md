# QA-tech SET gate, film 13 (set3d13): FAIL

Checked: contact.jpg, all 19 PNGs in work/final at full size, API.md, hue_rows.txt, `t_anim.py` (ALL OK, 75 checks; door gap above stair 0.10 / 1.90 / 3.70 at lift 0 / 0.5 / 1), shot_plan.md.
Automatic: no black or blank frames (0 % pixels < 12). Laplacian variance: lowest are jack_close 128, under_wide 139-151, suite_room 160 (dark, hazy content). No DOF blur or text found in any picture.

## Blocking issues
1. suite_two, hue: shade hue 236.0 is OUT of 240-260 (hue_rows.txt). Also the rich man is cut by the left frame edge (head and body half out) and the street is a thin sliver behind the rail. Fix: re-tint the shade, and move the camera or `window_l` so he is fully in frame with the street visible.
2. Magenta share above the 10 % limit: rain_street 28 %, suite_room 29 %, street_wide MORNING 14 %, tea_close 12 %, front_stair MORNING 11 %. Fix: shift the violet, magenta and pink in the sky, shade and carpet toward blue or red; the rain sky needs desaturating.
3. suite_room, scale and placement: the rich man's head sits behind and inside the teacup, and the cup (about 150 px wide) is bigger than his head (about 60 px). He is not seated or standing anywhere believable. Fix: stage him at `chair_side` or `window_l` in front of the table, and scale the cup and saucer to about 0.5 of the current size (cup roughly head-sized).
4. front_stair (plan 26, 27, 29), no visible door: the centre of the portico is a dark brick wall. The rich man stands in front of it at about 40 px tall with no door, threshold or step. The door is only visible at far right (a window with a red awning), so "steps out of the door" does not read. Fix: add a door or opening at `door` (x 0) with a visible threshold, and push the camera in so he is at least 100 px tall.
5. front_stair, telegraph pole: it runs through the centre of the frame and hides the door, the stair top and the fall zone. Fix: move or hide the pole at x about -3 to 0 for this preset (or move the camera right).
6. front_stair, fall geometry: `mud_fall` (2, -6.4, 0) is inside the stair footprint (stair x -5.4..5.4, y -9..-4, top 2.5). A man dropping from the door (y -0.9) lands on the landing or stair, not in mud. Fix: put `mud_fall` at about y -12 (past stair_foot, y -9.6) at mud z. Also note the 8 D lateral travel, so the fall needs a forward arc.
7. front_stair MORNING fill 0.5: the mud has risen and buries the lower steps, almost the same picture as DAY. Plan 28 says "fill not yet reached it" and 27 says "old stair sits ~2 m lower". Fix: render the ending with fill 0.1-0.2 so the stair and mud level show a clear 2 m drop. The gap between the portico floor and the stair top is only about 145 px; frame it taller.
8. mud_low (plan 5, 30): no character is visible (worker@cart_c and foreman@walk_b are off-frame or hidden), and the cart is only an orange polygon blob (horse rump or tail) at top-left. "Cart wheel sinks, horse struggles" and the later "sit in mud, hand the purse to pullman" cannot be shot. Fix: re-aim the camera so the cart, wheel, horse and 2 actors are in frame; add a staging mark for the sit-in-mud and pay beat.
9. jack_close (plan 22): the worker stands behind the screw and tiny (about 90 px head), with no hands on the bar. The bar is a loose diagonal stick (white leaning bar) plus a separate dark bar, so it reads as two unattached levers. Large dark blocks fill the top-left and bottom-left. Fix: stage `jack_hands` on the lever end (hands at lever height), remove the foreground obstruction, show one connected bar, and show the beam above the screw.
10. hotel_front (plan 1, 23): the jack gap and cribbing, which the plan needs "visible below", are about 40 px tall and are hidden by the characters and barrels at lift 0.7. The bottom 35 % of the frame is empty mud. The foreman (green) stands on a barrel (floating or wrong ground). Fix: lower the camera and raise the target so the gap fills y 700-900; remove the barrel at `hf_c` or move the mark; crop the empty mud.
11. street_wide MORNING (plan 28): at lift 1 the hotel reads the same as lift 0.7 (the cart, barrels and horse hide the gap), so "hotel ~2 m above the street" does not show. Fix: move the cart out of frame or re-aim so the dark gap with its jacks and cribbing shows across the base.
12. Plan coverage, tiles that do not exist or are not rendered:
    - Plan 4 and 5 use street_wide and mud_low in RAIN; only rain_street RAIN was rendered. Rain splashes, a sinking wheel and a struggling horse have no hook.
    - Plan 2: no "lady and gentleman guests" at the window. suite_two stages only the rich man (and he is the same card as in plan 11 and 19).
    - Plan 3: "rooftops sliding down" has no hook. There is no hotel in the suite street, so `set_lift` moves nothing there; it needs a camera move or a lift of the suite floor.
    - Plan 8: `set_fill` raises everything uniformly; there is no "side mound".
    - Plan 12: no stand point or hook for the rich man leaning out of a top window on the facade (hotel_front camera frames only up to the pediment, with no top window mark).
    - Plan 13, 14: no prop or mark for a carried jack or a trench entrance. Plan 7: no shovel prop or action.
    - Plan 15, 16, 25: the cellar has 230 jacks and about 70 workers; "100 / 1000 / 5000 jacks" and "500 workers" are not visible or growable. No hook for jack count.
    - Plan 17, 18 and others call for MORNING or DAY on suite presets; only SUITE exists (see item 14).
    Fix: add the missing marks, hooks or props, or change the plan.
13. suite_window, under_wide, street_wide: stale duplicates (`suite_window.png`, `under_wide.png`, `street_wide.png`, timestamps 09:01-09:49, older than the numbered finals). Delete or ignore them so they are not conformed by mistake.

## Non-blocking issues
14. Lighting continuity: street DAY is a hard-blue sky with gold clouds, MORNING is a pink and lilac sky, SUITE is a golden-hour sky (the window in suite_room and tea_close). Plan cuts 1 -> 2 -> 3 (DAY street, then suite) and 16 -> 17 flip between sky colours. Fix: give SUITE a DAY blue sky (as in suite_two top) or accept the jump; MORNING is acceptable only for plan 17 and 26-30.
15. under_rows: crowd cards at the bottom right have heads at y 1010-1140 (inside the caption band, y > 880). Fix: crop or move them out of the band, or accept that the caption covers them. The brown flat ground and dark void outside the brick pit (y 320-450) read as an empty plain.
16. crowd_street: only about 8 of the planned 24 + 8 cards are visible, and the frame is mostly pole and two low-poly grey sacks in the foreground (the sacks read as odd props). Heads are in range (y 790-870). Fix: move the camera back or widen, remove the foreground sacks.
17. suite_window: one third of the frame is the rail and floor; the street is tiny and the people are about 15 px. The look-down shows no pullman. suite_two roof edges show speckle noise (denoise or sample artefact). Raise the samples for these tiles.
18. tea_close: the cup, saucer and pot are washed to flat lavender (shade colour dominates) and the tea surface is pink or flat. It reads as a mirror, but nothing in the picture shows the "still" beat. Fix: warm the cup light or add a visible window reflection in the tea.
19. Heads and stand points: every character head in the finals is above y 880 except the under_rows crowd cards (item 15). `head_pixels` rule held for staged actors.

## Hue (hue_rows.txt)
OUT: suite_two 236.0. Borderline: under_wide 241.3, jack_close 244.4. All others 250-260.

## Verdict
FAIL on items 1-12 (hue, magenta limit, scale, missing door, fall point, unreadable beats, missing plan hooks and marks). Re-render the affected tiles and re-run the SET gate.
