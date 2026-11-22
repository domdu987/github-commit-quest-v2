# DETAIL SPEC: depth and detail (client 2026-11-22: "ทำภาพให้สวยให้มีมิติ ให้ละเอียดกว่านี้")
Binding for every NEW film, from the set build onward. It works together with COLOUR_SPEC.md; where they overlap, COLOUR_SPEC wins on colours.
The goal is to match the reference shorts (film/ref_shorts): the frame reads as deep space that is full of things.

## 1. Depth: every shot has three layers
- **Foreground:** a prop, plant, railing, window frame or crowd edge within 0-2 m of the lens.
  - It covers 5-20 % of the frame, at the bottom or one side, and never the face.
- **Midground:** the characters, standing on the ground with contact shadows.
- **Background:** a dressed set that goes deep, never a flat wall at the back. Use:
  - a room → doorway → next room
  - a street → houses → hills → sky
- **Atmospheric perspective:** far layers get lighter and bluer with a soft mist volume or a depth fog pass (5-15 %).
- **Overlap:** objects overlap each other, so nothing stands isolated on empty floor.
- **Height:** vary the height of things. A level skyline is not allowed.

## 2. Light that shapes form
Follow COLOUR_SPEC §4: one sun, blue-violet shade.
- Every set mesh gets bevels (0.5-2 cm) so the edges catch light.
- Ambient occlusion (AO) on: corners and the space under furniture go darker.
- Contact shadows under every card and prop.
- Practical lights (lamps, windows, fires) make pools of light, and the room is darker between the pools.

## 3. Detail density
- **Surface texture:** no large flat colour areas.
  - Wood shows grain or planks.
  - Walls show brick, plaster patches or panelling.
  - Floors show tiles or boards.
  - Fabric shows folds or pattern.
  - Noise and texture stay subtle (±5-8 % value) and in the COLOUR_SPEC palette.
- **Set dressing:** at least 25 distinct props per interior set and at least 40 objects per exterior (trees, carts, fences, signs, birds, smoke).
  - Repeated props get random scale, rotation and colour variation (±10 %).
- **Life in the background:** at least 2 small moving things per shot, such as smoke, flags, birds, background people walking, flickering lamps or water.
- **Period-correct signs and text are encouraged**, since the client allows text signs.

## 4. Checks (free scripts plus 1 look)
- SET gate:
  - Render 3 test stills (wide, medium, top-down).
  - Run hue_report (COLOUR_SPEC).
  - Fill in a checklist that counts props per set and confirms the foreground, mid and background layers are present.
- Take gate: ground_check, qa_jitter and qa_auto, as before.
- One Opus look at the style board only: does it read as deep and detailed at phone size? Fix once, then build. No repeated art rounds.
