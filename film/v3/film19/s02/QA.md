# s02 QA: film 19, the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H) -- SHIP ship_aerial, NOON

## Delivered
- `take.mkv.partaa` + `take.mkv.partab` (the take, libx264rgb crf 6, 74 MB; `cat take.mkv.part* > take.mkv`): first_g 48, 152 frames, 720x1280, 10 spp (colour-fixed set), 2 threads. No captions / audio.
- **g 57..190 = the BIGZOOM (1.91-6.37 s, 134 frames)**; g 48..56 in-handle, g 191..199 out-handle. Join in: hard cut from s01 at g 57. Join out: DISSOLVE 13 f into s04 at g 191 (handle rendered in 3D). meta.json: `bigzoom [57, 190]`, shots [2, 3] (s03 absorbed).
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts.

## The move (one continuous camera, no cut)
1. **g 57-100: extreme wide from high above and behind.** The lone warship on the glittering NOON sea (~27 % of the frame height), the long white V wake trailing toward the lens; captain19 and astro19_c on the quarterdeck are ~10 px tall (< 1 % of the frame, findable).
2. **g 100-118: the descent.** The camera sinks and pushes in over the wake, passes the stern (the spanker sail and mizzen mast ~3 D from the lens: parallax foreground) in a fast eased swoop.
3. **g ~118-150: MEDIUM on the quarterdeck, reached by 5.0 s** (spec: by ~5.9 s): captain19 holds the (blank-ish: coast and compass lines, no text) sea chart; astro19_c squints through the quadrant at the sky and, g 146-166, lowers it and scratches his head (comic puzzlement). No mouth movement. Then a slow 17 deg orbit about the pair + a gentle push to g 199 so the hold keeps moving.
- Staging: the cards ride `ship_root` (`c19.ride_ship`, inverse taken at rest) and the camera rides the deck (`c19.on_ship`); `set_sea` / `set_roll` keyed with t = g/30 on every frame. Gulls hidden. No sea edge or void (the sea grid is fitted to a virtual camera 3x farther / higher, 1500x2000 vertices; runtime only, no set edit).

## Checked
- **Heads (g 150-199):** captain head centre y 464-481 (163-181 px wide), astro19_c 541-564 (141-179 px); both stand 35-60 % of the frame height; the heads stay above y 880; feet on the deck with contact shadows (the cards had sunk 0.2 D until the shoe sole offset was added).
- DOF off, no text, no caption_shade in every raw json.
- **qa_auto: PASS** (soft frames g 112-117 are the fast pass through the stern: smooth planks and sail; 6 of 152 frames).
- **qa_stats.py (take.mkv):** saturation **0.597** (target >= 0.40), brightness **100.6** (target 70-135).
- **Frame-diff (in-shot g 58..190, 90x160 grey):** median **4.96**, p90 **10.96** (qa_stats on all frames 5.49 / 10.52). Targets: median >= 4, p90 >= 10.
- **Cost:** 25.4 s/frame wall (49 s cpu) at 2 threads: the ship_aerial preset is 16 s; the extra is the two cards and the 1500x2000 sea grid.

## Notes / deviations
- The sail pass is ~3 D (the spec asks 1-2 D): at 2.4 D or closer the cloth fills the frame, the frames get smooth and qa_auto fails "suspected blur" (the same effect that limited s17).
- Sprites report "clipped" in the steep high frames (g 57-130): the two are < 20 px tall there, so nothing is visible.
- The old s03 shot is absorbed; s03 should not be rendered.
