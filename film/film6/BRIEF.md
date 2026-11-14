# Film 6: "ไอ้สิบสาม" (the 13th loaf) — a medieval English market town, 1260s
PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj
Same style, pipeline and rules as films 2-5: read PROJ/plan2/BRIEF.md ("Rules for every worker"). Templates: set PROJ/v3/set3d5/mine.py
(+ mine_API.md) and PROJ/v3/set3d4/pagoda.py (+ pagoda_API.md section 1b: dressing density, warm in-scene emitters — that density is the bar),
cast PROJ/v3/cast5 (incl. held 2D props like the cage), shots PROJ/v3/film5/s01. Narration PROJ/film6/audio/narration_bankky.wav (105.8 s),
script PROJ/film6/script/script_th.txt, timing PROJ/film6/audio/timing.json, captions PROJ/film6/script/captions.json.
Reference look: PROJ/ref/a and PROJ/ref/b. HARD RULES FROM THE USER: images SHARP — no depth-of-field blur at all; sets dense with ornament.

## Story (a tale based on the real "baker's dozen")
In medieval England a baker who sold bread under weight was put in the pillory and pelted with rotten vegetables. Uncle Henry, the
stingiest baker in town, weighs every loaf exactly. His apprentice, a small flour-covered tray-washing boy who loves watching white steam rise
from the fresh loaves every morning, slips a 13th loaf into every customer's dozen. Henry yells; the market nicknames the boy "ไอ้สิบสาม".
Week 1 the bakery next door is pilloried, week 2 another, week 3 two more — all swore their bread was exact. Henry laughs "they cheat, I'm
honest" and bans the 13th loaf. The boy secretly re-weighs Henry's loaf in the afternoon: lighter than in the morning; every bust happened in
the afternoon. That very afternoon a hooded man buys a dozen; Henry counts exactly 12 and shoos the boy away. In the middle of the market the
man drops his hood: the King's bread inspector. He pours the basket on a big balance scale: it does not move — slightly short. Guards drag
Henry to the pillory; the crowd raises rotten veg. The boy grabs the 13th loaf, runs through the crowd shouting "the weight evaporated by itself,
I'll make it up!" and puts it on the scale: the scale slowly tips — passes. Henry pale, the inspector nods slowly. Reveal: the white "smoke" is
water evaporating out of the bread; bread weighed exact at dawn is lighter by afternoon. The other bakers never cheated. Ending: next morning
Henry himself puts the 13th loaf in the basket; that's why a "baker's dozen" is 13.

## Locations
1. bakery (interior, dawn/morning): domed brick bread oven with roaring orange mouth (warm emitter), wooden peel, long flour-dusted tables,
   racks and shelves of round loaves, flour sacks, hanging herbs/onions/copper pans, small hand balance scale with weights on the counter,
   shop window/half-door counter opening onto the street (light shafts), candles. Steam: animatable white steam wisps rising off hot loaves
   (set_steam(level 0..1)). Presets: bakery_wide, counter (over the counter toward the boy/Henry), table_insert (ECU loaves + steam),
   small_scale_insert (ECU hand balance, beam tilt animatable), window_out (from inside looking out to the street).
2. market (exterior square, afternoon warm sun + morning variant): timber-framed jettied houses, the bakery front with a hanging bread
   sign, other bakery fronts, stalls with awnings and produce (cabbages, crates), bunting, cobbles, a well; centre: wooden pillory/stocks on a
   little platform; a big public balance scale (tall wooden frame, two big pans, animatable beam tilt set_big_scale(angle_deg)); crowd
   space. Presets: market_wide (establishing, high), square_eye, pillory_low, big_scale_insert, run_lane (long lane through the crowd).
Animatable hooks wanted: set_steam, set_scale(small, angle), set_big_scale(angle), loaf piles on scale pans (count 12 or 13), oven fire flicker.

## Cast (flat 2D puppets, cast5 conventions: pose keys, mouth/eyes, held props)
- kit: the boy (8-9 y.o.), flour on face/hair/clothes, oversized apron, cap; held props: loaf, basket.
- henry: the stingy baker — round, big moustache, flour apron, bald with tuft, tiny eyes; poses: yell, laugh (smug), count (fingers), pale/scared.
- inspector: tall thin man; variant A hooded brown cloak (face shadowed), variant B hood down: royal tabard, chain of office, stern brows.
- guard1, guard2: soldiers with helmets/spears/tabards.
- townsfolk: woman1 (headscarf), man1 (farmer), holding rotten cabbage/tomato (held prop), laughing/pointing poses.
- baker2: another baker (thin, sad) shown locked in the pillory (head + hands through the board) — can be a pose of a cast piece.
