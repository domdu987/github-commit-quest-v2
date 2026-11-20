# s15 QA (round 2): film 19, shot 15 (SHIP ship_deck NOON)

## Delivered
- `take.mkv` (libx264rgb crf 6, 38 MB): g 1086..1198 = 113 frames, first_g 1086. Shot 15 = g 1096..1189; handle in g 1086..1095 (10 f, DIS 15), out g 1190..1198 (9 f). 720x1280, 11 spp. `qa_auto` PASS. meta.json, cues.json, contact.jpg, phone_sheet.jpg, framediff.json.

## Round-2 fixes (director review)
- **Sun:** a visible sun is now in frame: a bright disc + soft halo parented to the camera (top right, camera rays only, it lights nothing), faded in g 1164..1176 as the camera snaps up on "อยู่ตรงหัว" (g 1172). `set_sun_overhead` still keyed 0 -> 1 on every frame (g 1086..1176).
- **Poses:** quadrant angle -85 (straight up), William pitch -0.45 and gaze up; the captain looks up (pitch -0.40) and shades his eyes with a hand (arm at the brow).
- **Framing:** both in frame through the whole shot (no clipping): captain x >= 64 w 190 px at the end, William right edge 712. The snap is a tilt/pan up (shift up 2.0 D, x1.5, 16 f) with the heads first high in frame (y ~440) then dropping to y ~650 as the camera tilts up toward the sun, instead of the earlier zoom onto William.
- Ship ride unchanged (cards parented to ship_root with the parent inverse taken at t = 0; camera on_ship; sea / roll / sun keyed with the same t every frame).

## Checks
- Heads in shot: centre y 406-669 (the 406 is the transient before the tilt, g ~1170), width 99-218 px, bottom max 778. No head near y 880. No DOF, no text, no caption_shade.
- Frame-diff (in-shot, 90x160 grey): **median 4.55, p90 12.27** (draft 4.55 / 12.15). s/frame 22 wall / 43 cpu.
- Known: the "sun" is a screen-space glare disc, not a sun object in the set; the shadow of the sail still lies across the deck at noon (the set's sail is large). The quadrant reads as a gold fan pointing up-right.

## Round 3: colour re-render (QA_TEAM §G; set fix ff204d3 merged: ship NOON exposure -0.3, grade sat 1.18)
Re-rendered unchanged shot code on the new set. `film/qa_stats.py take.mkv`: saturation 0.398, brightness 118.4 (in-shot motion median 4.32 p90 9.40). Frame-diff (deliver.py, in-shot): 3.96 / 11.05.
