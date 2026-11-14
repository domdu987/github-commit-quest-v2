# Film 8: "ไอ้บ้าน้ำแข็ง" (ice in the desert — Persian yakhchal, ~1600s)
PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj
Same style, pipeline and rules as film 6 (PROJ/plan2/BRIEF.md rules). Latest templates: set PROJ/v3/set3d6/bakery.py + bakery_API.md and
PROJ/v3/set3d7/louvre.py + louvre_API.md; cast PROJ/v3/cast6 / cast7; shots PROJ/v3/film6/common.py + PROJ/v3/film6/s01.
Narration PROJ/film8/audio/narration.wav (60.8 s), script PROJ/film8/script/script_th.txt, timing PROJ/film8/audio/timing.json.
USER TASTE (from feedback on films 6-7): the user PREFERS the original film look — wide/medium framings that show the beautiful dense set,
warm lit 3D world, calm readable shots; NOT constant extreme close-ups, NOT lots of text signs, NOT flat 2D infographics. Sharp, NO depth of
field. Reveals must be shown inside the lit 3D world (like the bread reveal re-made in PROJ/v3/film6d/reveal).

## Story
Persia 400 years ago, no fridges. A man (Farid) pours water into shallow channels in the desert every night and says he'll sell ice in
summer. The richest water merchant laughs ("Ice in the desert? Madman! If you can do it, I'll buy it all!"); the bazaar nicknames him
"ไอ้บ้าน้ำแข็ง". He builds a tall mud-brick wall (3 storeys) shading the channels, and a giant mud dome (yakhchal) beside it. Night 1 the
water freezes into a thin sheet, night 10 finger-thick; every morning before sunrise he cuts the ice and stores it in the dome. One day he
oversleeps: the ice in the channel melts to mud by noon, the merchant laughs to tears ("See? No ice in the desert!"). Summer comes: every
well in town turns warm, but inside the 2 m thick dome the ice is still full. Reveal: on clear nights the sky is colder than ice; the
water's heat rises away to the sky (show as faint shimmering heat wisps rising from the channel to the stars), and the wall shades it all
day — water freezes though the air is above 0 °C. Ending: the merchant pays for the whole dome of ice, as he swore — "I'll buy it all".

## Locations
1. desert_ice (night + dawn + noon + summer day): flat desert plain with long shallow water channels (animatable: water / thin ice / thick
   ice / mud, set_ice(level)), a very tall mud-brick shade wall running east-west along the south side of the channels, a giant conical
   stepped mud dome (yakhchal) with a small door and ice blocks stacked inside (interior preset, cool blue with warm lantern), clear starry
   sky with Milky Way at night (gorgeous), sunrise glow, harsh summer sun. Presets: channels_wide, channel_ecu (ice surface), wall_low,
   dome_wide, dome_interior, sky_reveal (low angle from the channel up to the stars).
2. bazaar (day, Persian town): dense bazaar street with arches, carpets, copper pots, water jars, a fountain/well, awnings, lanterns, the
   water merchant's rich stall with big water jars; town walls and domes in the background. Presets: bazaar_wide, merchant_stall, well_eye.
Hooks: set_ice(level 0 water .. 1 thick ice, melt->mud), set_heat_wisps(level) for the reveal, time-of-day light presets NIGHT / DAWN /
NOON / SUMMER, lantern flicker, stars.
## Cast
farid (young Persian ice-maker, turban, simple tunic, sash; poses pour water bucket, cut ice with saw/pick, carry ice block, build wall,
sleep, shocked, calm smile), merchant (fat rich water merchant, big turban with jewel, rings, moustache; poses laugh big, point & mock,
laugh to tears, sweat in heat, sheepish paying with coin purse), townsfolk (2-3: woman with water jar, old man, boy; laugh, point, fan
themselves sweating), held props: bucket, ice saw, ice block, coin purse, water jar.
