# Film 13: "ไอ้แม่แรง" (raising the Tremont House, Chicago 1861)
Same style, pipeline and rules as films 9/10 (../film10/BRIEF.md, ../film9/BRIEF.md, USER TASTE):
- wide and medium framings that show a beautiful DENSE set, calm but always-moving camera
- warm lit 3D world, one hard key light, blue-violet shade (hue 240-260), pleasing period colours (not harsh B/W)
- sharp, NO depth of field, NO text signs; reveal inside the lit 3D world
- NEW set (v3/set3d13), new cast (v3/cast13). Never reuse a set; helper functions may be imported.

Narration: film13/audio/narration.wav (66.4 s, tempo 1.134). Script film13/script/script_th.txt. Timing film13/audio/timing.json.
Captions film13/script/captions.json.

## Facts (true) vs dramatised
Fact: Chicago in the 1850s-60s was built on lake-level mud; streets flooded, sewage could not drain (disease). From 1856 the city
raised street grades by up to ~6-8 ft to lay sewers, and buildings were jacked up to the new grade. In 1861 Ely, Smith & Pullman
(George Pullman, later of Pullman sleeping cars) raised the Tremont House, a six-storey brick hotel, about 6 ft with ~5,000
jackscrews and about 500 men (other sources 1,200); each man handled ~10 screws and gave each a half turn on a signal; the hotel
stayed open and guests reportedly did not notice. Dramatised: the rich mocker, his bet, the nickname, the tea, the comic fall.

## Story beats (sentence starts in timing.json)
0 hook 0.0 - a six-storey brick hotel rising off the ground while guests sip tea inside.
1 pivot 5.3 - Chicago 160 years ago: city on mud, rain turns streets to swamp, sewage stuck.
2 setup 12.1 - the city starts filling streets ~2 m higher; low buildings' doors would sink under the street; only way: lift the whole building.
3 boss 19.7 - rich guest on the top floor laughs (quote, lip-sync): "lift a brick building by hand?! If it moves one finger, I'll pay
  the room bill for the whole hotel!"
4 nickname 28.1 - the whole town calls him "ไอ้แม่แรง" (Mr Jack).
5 count 30.4 - jackscrews go under the building: 100, 1000, 5000; 500 workers, 10 each.
6 false 36.9 - two days later the rich man looks out the window: nothing changed, tea in the cup not even rippling: "See? Not one inch!" (quote)
7 reveal 43.3 - under the floor, at each whistle 500 men turn their jacks half a turn together; the building rises a tiny bit, level at every corner, no crack.
8 aha 51.1 - no giant machine could lift it; 5000 jacks turned a little together lifted it all.
9 ending 55.9 - day 5: he steps out the door, no ground under his foot - the hotel is ~2 m higher and the street fill hasn't reached it;
  he drops into the mud (comic, no injury) and must pay for the whole hotel, as he said himself. Hard cut on "เอง".

## Locations (one set module v3/set3d13/chicago.py)
1. street (Lake Street / Dearborn, Chicago 1861): the Tremont House - six-storey warm red-brick hotel with cream stone trim,
   cornice, tall sash windows with warm lamplight, awnings, a grand front stair - on a muddy street with plank sidewalks at two levels,
   gas lamps, horse carts stuck in mud, puddles with reflections, timber cribbing, piles of fill earth and gravel, barrels, crates,
   telegraph poles, neighbouring 3-4 storey brick and timber shops (some already raised, some sunk below the plank walk), a church
   spire and the lake/ships far away. Hooks: set_lift(h 0..1 -> 0..~2 m, whole hotel rises with exposed timber cribbing + jacks
   below the ground floor), set_fill(k street fill level), mud wetness. Light: DAY (warm afternoon), RAIN (overcast swamp street for the pivot).
   Presets: street_wide, hotel_front (low, the hotel towering), front_stair (door + stair, for the ending fall), mud_low.
2. under (the cellar crawlspace below the hotel): a forest of iron jackscrews on timber blocks in rows to the vanishing point,
   oil lamps, 500 workers (crowd cards) each by 10 jacks, the foreman with a whistle, beams of the floor above. Warm lamp light,
   blue-violet shade. Presets: under_wide (rows to infinity), jack_close (one jack + hands turning the bar).
3. suite (the rich man's top-floor room): velvet chairs, tea table with cup and saucer, window looking down on the street,
   wallpaper, chandelier, paintings (no text). Preset: suite_window, tea_close (cup, liquid flat).
