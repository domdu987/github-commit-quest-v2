# Film 14: "ไอ้บ้าผึ้ง" (beehive fence vs elephants, Kenya, recent years)
Repo paths (work in the repo, branch film14/main): set `film/v3/set3d14/`, cast `film/v3/cast14/`, film files `film/film14/`.

Same style, pipeline and client rules as films 8-10: `film/film10/BRIEF.md`, `film/skill/reference-style-shorts/references/production-lessons.md`.
- Wide and medium framings that show a beautiful DENSE set; calm but always-moving camera.
- Warm lit 3D world, one hard key light, blue-violet shade (hue 240-260), magenta <= 10 %.
- Sharp, NO depth of field, no text signs, reveal inside the lit 3D world (never a flat diagram).
- Client-approved look: `film/v3/set3d14/styleboard/board.jpg` (code `styleboard/sb.py`). The full set grows from it and must keep its palette and light presets.

Narration: `film/film14/audio/narration.wav` (70.0 s). Script `film/film14/script/script_th.txt`, captions `script/captions.json`, timing `audio/timing.json`.

## Story and sentence times (s)
| # | beat | time | content |
|---|---|---|---|
| 0 | hook | 0.0-6.0 | The whole village laughs while a young farmer hangs a beehive on the fence round his maize field; he says the bees will chase off a whole elephant herd. |
| 1 | pivot | 6.0-13.6 | "คืออย่างนี้นะ" Kenya, recent years. Wild elephants raid fields at night; in one night the maize is gone. Villagers bang pots and wave torches; the elephants do not care. |
| 2 | boss | 13.6-22.1 | The neighbour uncle laughs loudest (QUOTE 15.4-22.0, lip-sync): "A five-ton elephant, scared of a bug the size of a bean?! If bees can chase off elephants, I'll let one sting my nose!" |
| 3 | nickname | 22.1-25.2 | The village laughs along and calls him "ไอ้บ้าผึ้ง" (crazy bee guy). |
| 4 | count | 25.3-33.3 | Day 1: one hive. Day 2: ten hives. Day 3: ONE long wire threading every hive, a ring round the field. |
| 5 | false | 33.4-40.8 | That night the whole herd comes; the matriarch walks straight to the fence. Bees asleep, silent. The uncle shouts (QUOTE 39.0-40.8, lip-sync): "See? The elephants aren't scared at all!" |
| 6 | attack | 40.8-43.5 | The matriarch pushes the wire with her chest to walk through. |
| 7 | reveal | 43.6-53.3 | The one wire links every hive: a push in one place swings the whole row, hives knock together, thousands of bees burst out and go for the softest spots: round the eyes and up the trunk. |
| 8 | aha | 53.3-61.3 | Elephant hide is an inch thick, but inside the trunk it is soft. The herd turns and runs, and remembers that buzz forever. The bee guy's field loses not one stalk. |
| 9 | ending | 61.3-70.0 | But that night the elephants raid the uncle's field instead. Next morning the uncle has to come and ask for hives; as he hangs his first hive, a bee stings his nose as promised, and it swells up like an elephant trunk. Hard cut on "งวงช้าง". |

Comic only: no injury to anyone, elephants unhurt (they flee), the sting = comic swollen nose.

## Location (one set module `set3d14/farm.py`, presets + light states DAY, DUSK, NIGHT, MORNING)
Rural Kenyan smallholding at the savanna edge, two farms side by side.
- **hero farm**: tall maize field in rows; the BEEHIVE FENCE round it: posts every ~10 m, each hive (Kenyan top-bar hive: long trapezoid wooden box) hangs under its own small corrugated-tin shade roof between two posts; ONE continuous wire runs post to post and through every hive's hanging bar. The fence is built in stages: hook `set_fence_stage(k)`: 0 = posts only, 1 = one hive, 2 = ten hives, 3 = all hives + the continuous wire ring.
- **village**: round mud huts with conical thatch, a tin-roof house, granary, fire pit, yellow jerrycans, hoes, stools, baskets of cobs, chickens, a goat, banana plants, acacias, red laterite paths, Mt Kenya-like mountain and hills.
- **uncle's farm**: next door, his own maize field with a thorn-branch fence, tin cans on strings; hook `set_uncle_field(k)`: 0 = intact, 1 = trampled and eaten (flattened stalks, broken fence, footprints).
- Hooks: `set_wire_push(t)` (0..1: the wire bows in at the push point and every hive along it swings and knocks with a damped phase delay that travels outward along the wire), `set_bees(t, burst)` (particles/cards: 0 = sleeping, rising cloud from each hive entrance after the push), `set_crowd_props`, villagers' torches/pots for the pivot.
- Presets (720x1280, 22 mm unless noted): `village_wide` (high wide, farm + huts + mountain), `fence_line` (eye level along the hive fence), `hive_close` (one hive on the wire, wire receding), `yard_two_shot` (hero and uncle in the yard), `field_night_wide` (high wide at night: herd approaching the fence ring), `fence_low_night` (low at the fence, the matriarch arriving), `push_side` (side view along the wire for the push and the swinging wave), `trunk_close` (elephant head and bees near eyes and trunk), `uncle_field_morning` (the trampled field), `uncle_hang` (uncle on a stool hanging his first hive).

## Cast (`cast14`, flat 2D puppets in the series style)
- **farmer (hero)**: young Kenyan man, slim, short hair, a faded orange T-shirt, rolled khaki trousers, rubber sandals, a beekeeper's veil hat pushed back. Poses: hanging a hive, tying the wire, calm smile, standing proud by the fence.
- **uncle (mocker)**: older, round belly, grey stubble beard, a flat cap, a checked shirt with a kikoi/shuka wrap over one shoulder, a walking stick. Poses: laugh big, point and mock (lip-sync), arms akimbo, shout at night with a torch (lip-sync), looking at his trampled field, asking sheepishly with an empty hive, on a stool hanging a hive, stung: comically SWOLLEN NOSE like a trunk (pose key `nose_swell` 0..1).
- **villagers**: 3-4 (a woman with a headwrap, a kid, an old man) laughing, banging a pot, waving a torch.
- **elephants**: a matriarch (big, tusks, wrinkled grey, flat 2D puppet card like the cast), 3-4 others + a calf. Poses: walk cycle, push with chest, trunk up trumpeting, flee/turn, ears flared. Elephants do NOT lip-sync.
- **bees**: small gold-black cards with wing blur, a swarm system.
- Mouths move only on the uncle's quotes: 15.4-22.0 and 39.0-40.8.
