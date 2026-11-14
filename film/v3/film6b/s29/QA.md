# s29 QA: film 6b, shots 29-31 (56.80-64.70 s, the END): the bakers' dozen sign, Henry in the pillory, 12 tomatoes

Delivered: `frames/g_1698.png .. g_1940.png` (243 frames, 720x1280, 12 samples, 2 threads, no captions/audio) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1698). Plan range g 1704..1940; g 1698..1703 is the 6-frame in-handle rendered in 3D. **No
out-handle: the film cuts on g 1940** (the last frame of the take = the last frame of the film, no hold, no fade). Also
`meta.json`, `cues.json` (16 cues, every splat), `contact.jpg` (caption line y 880 in red), `compare.jpg`. Scripts: `shot.py`,
`deliver.py`; raw renders in `raw/s29`, `raw/s30`, `raw/s31` (git-ignored).

## Framings (market MORNING; all hard cuts; camera always moving)
- **29a** g 1698-1747 low, up at Henry's shop front: a new hanging oak sign "13 =" (with a loaf icon) / "โหลของคนทำขนมปัง" swings
  on its rings over the shop opening (oven glow behind), slow pull + tilt. ("ฝรั่งเลยเรียกสิบสามว่า")
- **29b** g 1748-1790 kit in front of the shop under the sign: looks up at it, then turns to the lens with a big grin holding a loaf up;
  the loaf hops on "ขนมปัง" (g 1776). Kit head centre y 700-790... see numbers below.
- **30a** g 1791-1830 Henry (pale 0.9, sweat drops, worried) locked in the pillory on the platform; a jeering woman and farmer in the
  foreground corners raise rotten tomatoes overhead (static open jeer mouths). Slow push. ("ส่วนลุงเฮนรี่ วันนั้นได้")
- **30b** g 1831-1871 CU Henry (head ~420-475 px = 58-66 % of the width), eyes darting, "stunned" from "ของครบโหล", a gulp on "เป๊ะ";
  three raised tomatoes bob up into the bottom of the frame. Push in.
- **31** g 1872-1940 ECU Henry (head 475-510 px = 66-71 %). A tomato flies in from the lower right (g 1877-1882) and SPLATS on his
  face on "มะเขือเทศ" (g 1883); then 11 more in quick rhythm (1890 ... 1930), each a cartoon splat card stuck to his head / board,
  a flinch (head roll + eyes shut 2 frames) and a small camera knock per hit; a red tomato counter in the upper right flicks up
  1 -> 12 with a pop on each hit, reaching "12" on "เน่าสิบสองลูก" (g 1930). Cut on g 1940.

## Client rules
- **No depth of field** (common.Take: off at build and before every render). Background houses, bunting and sky sharp.
- **Heads above y 880 / main head centre 0.35-0.59 H**: Henry 585-700 px in 30-31 (0.46-0.55 H). Kit in 29b ~ 700-790 px
  (0.55-0.62 H, the sign above him needs the room; the whole head is above 880). 30a foreground townsfolk heads 700-770 px.
- **Mouths**: nobody speaks; every mouth is the static mouth of its expression (Henry's "shocked"/"stunned" open mouth is static).
- **Comic, not cruel**: splats are cartoon star-blobs with seeds and a drip (drawn in shot.py `splat_svg`; cast6's squash drawing
  read as a flat disc on a face), no injury; Henry flinches and blinks.
- **Continuity**: Henry = round bald baker, pale + sweat as the plan's `henry_in_pillory`; pillory from cast6 (`pillory=True`), the
  set's 3D board + post cut out at runtime as in film-6 s33; kit the floury boy with a loaf.
- **Thai text**: sign and counter rendered with PIL + raqm (Kanit Black, ink outline, glyph loops closed), readable at phone size.

## Notes
- Cycles `transparent_max_bounces` raised to 64 in this take: with 12 splat cards stacked on Henry's card the default 12 gave a
  black square on his face (seen in the draft, fixed).
- Hidden actors per shot are keyed `hide_render` (constant), so one market build serves all three shots.

## Differences from the plan
- 29 is split: sign alone first (the word "13 = โหล..." needs to be read), then kit grinning under it.
- Shot 30's crowd is two foreground townsfolk (woman1, man1 with tomatoes) rather than a whole crowd; the 30b tomatoes are
  hand-less tomato cards rising into frame.
