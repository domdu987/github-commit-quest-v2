# Film 10: "ไอ้ช่างม้าลาย" (dazzle camouflage, WWI Britain, 1917)
PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj

Same style, pipeline and rules as films 8 and 9: PROJ/film9/BRIEF.md and PROJ/film8/BRIEF.md, including USER TASTE.
- Wide and medium framings that show a beautiful dense set.
- A calm but always-moving camera.
- A warm, lit 3D world with one hard key light and blue-violet shade.
- Sharp, NO depth of field, no text signs.
- The reveal happens inside the lit 3D world, never as a flat 2D diagram.

Templates:
- set: PROJ/v3/set3d9/wall.py (+ wall_tex.py, API) and set3d8
- cast: PROJ/v3/cast9
- shots: PROJ/v3/film8/common.py and the film 9 takes

Narration: PROJ/film10/audio/narration.wav (60.0 s, plays at +0.10 s). Script: PROJ/film10/script/script_th.txt. Timing: PROJ/film10/audio/timing.json.

## Story
1917, WWI. German U-boats sink British ships almost every day. A marine painter (Norman) paints a warship in wild black-and-white zebra/dazzle stripes, visible from far away. The admiral laughs: "Warships must be grey, to blend with the sea! If your striped ship survives, I'll paint MY ship zebra myself!" The sailors of the whole harbour nickname him "ไอ้ช่างม้าลาย" (the zebra painter).

Escalation: on day 1 he paints zigzags, on day 2 he adds staircase stripes, and by day 3 the whole ship looks like a smashed candy box.

False payoff: the striped ship sails with a convoy of grey ships, and the U-boat periscope spots it first of all. The admiral shouts "See? A crystal-clear target!"

The U-boat captain aims and fires a torpedo at the striped ship.

Reveal: a torpedo is slow, so you must aim AHEAD of the ship, at where it will be. The stripes make the bow look like the stern, so the captain guesses the wrong heading and the torpedo runs harmlessly past the stern. Show it in 3D:
- the periscope view of the dazzle ship, where the bow and stern are ambiguous
- a high wide view over the sea: a translucent "ghost" ship shows the captain's wrong guess heading the other way, the torpedo is aimed ahead of the ghost, and the wake passes behind the real ship's stern

Aha: the stripes do not hide the ship; they make the aimer read it wrong. Soon thousands of ships were painted like this (a harbour full of dazzle ships).

Ending: the last ship painted is the admiral's. He stands on a plank holding a brush, painting his own ship zebra himself. It is comic: paint on his moustache and cap. Hard cut on "เอง".

## Locations (one set module, set3d10/harbour.py, with presets and light states)
1. harbour (British naval dockyard 1917)
   - Contents:
     - a big warship hull at the quay with plank scaffolding and hanging painter's planks
     - paint buckets (black, white, grey) and ladders
     - cranes, red-brick warehouses, stacks of crates, bollards and ropes
     - a lighthouse at the harbour mouth, gulls, and other grey warships moored
   - Light: DAY and DUSK.
   - Hooks:
     - set_stripes(ship, stage 0..3): 0 = plain grey, 1 = zigzag, 2 = + staircase, 3 = full dazzle
     - set_harbour_dazzle(k): turns the moored ships into dazzle ships for the "thousands" shot
   - Presets: harbour_wide, hull_side (medium along the hull with scaffold), quay_low (low two-shot on the quay), hull_plank (the painter or admiral on a hanging plank against the hull)
2. sea (open North Atlantic)
   - Contents:
     - an animated low-poly ocean with gentle swell
     - a convoy of 4-5 grey ships plus the dazzle ship, all with bow waves and smoke from the funnels
     - clouds
   - Light: SEA_DAY (warm, low sun, hard shadows on the ships).
   - Props:
     - the U-boat: hull awash, conning tower and periscope
     - the torpedo with a white bubble wake
     - the ghost ship: translucent, emissive pale cyan copy of the dazzle ship
   - Presets:
     - convoy_wide (high wide)
     - periscope_close (low at the water: the periscope pokes up)
     - periscope_pov: the camera inside the periscope with a circular black vignette and a thin crosshair mesh; it is a lens view in 3D, with NO text
     - topdown_sea (high oblique for the reveal: ghost path vs real ship, torpedo wake passing behind the stern)
     - torpedo_chase (low behind the torpedo)
     - bridge_deck (the admiral on a grey ship's bridge with binoculars)
## Cast (cast10)
- **painter (Norman)**: lean, beret, paint-splattered overalls, rolled sleeves, a little moustache.
  - Poses: painting a stripe with a big brush, stepping back proud, calm smile, on a hanging plank.
- **admiral**: big belly, navy blue double-breasted coat with gold buttons, peaked cap with gold braid, huge white walrus moustache.
  - Poses: laugh big, point and mock (lip-sync), arms akimbo, binoculars, shout on the bridge (lip-sync).
  - Final pose: on a plank with a brush, paint spots on his face, sheepish.
- **sailors**: 2-3 in white caps, pointing and laughing.
- **uboat_captain**: grey peaked cap, beard; at the periscope handles, squinting.
- Held props: big brush, paint bucket, binoculars.
- Mouths move only during the admiral's quotes:
  - boss line, about 11.0-17.6 s
  - false line, about 31.0-33.2 s
