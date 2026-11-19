# Shot plan, film 13 (ไอ้แม่แรง)
Narration film13/audio/narration.wav (66.38 s), placed at +0.10 s. g = round(t*30) (t = film time incl. +0.10). N = 1995.
Set v3/set3d13/chicago.py (see API.md for presets / stand points). Cast v3/cast13 (pullman, rich, worker A-C, guests, townsfolk).

| line | start (s, narration time) |
|---|---|
| hook 0.00 | pivot 5.30 | setup 12.13 | boss 19.70 | nickname 28.14 | count 30.41 | false 36.90 | reveal 43.27 | aha 51.13 | ending 55.89 | end 66.38 |

QUOTE windows (rich's mouth moves ONLY here, +-0.15 s): Q1 21.68-28.09 ("ตึกอิฐทั้งหลัง ... โรงแรมเลย!"); Q2 41.72-43.22 ("เห็นมั้ย ไม่ขยับสักนิ้ว!").
LOOK: wide/medium framings that show the dense set; calm always-moving camera (slow push/pan/crane, new framing every ~2-2.5 s);
sharp, NO DOF, no text; heads above y 880; warm DAY key, blue-violet shade; comic fall without injury.
Lift state continuity: hook shows lift rising 0.55->0.65 (flash-forward); pivot/setup h=0; boss/nickname h=0; count h=0->0.05;
false h=0.4 (but shot from INSIDE so the rich man can't tell); reveal h 0.4->0.8; aha h 0.9; ending h=1.0 (door ~2 m above old stair/mud).

| # | t0-t1 (narr s) | preset / light | action |
|---|---|---|---|
| 1 | 0.00-2.10 | hotel_front / DAY | low angle: the whole six-storey hotel rising slowly (h 0.55->0.65, worm's-eye, crib pier + jack in foreground), dust trickling; slow crane up |
| 2 | 2.10-3.60 | suite_two / DAY | through the window the street drifts down a hair; lady and gentleman guests sip tea calmly at the window |
| 3 | 3.60-5.30 | tea_close / DAY | teacup on saucer, tea surface mirror-still (ripple 0) while the window behind shows rooftops sliding down; slow push |
| 4 | 5.30-7.80 | street_wide / RAIN | pivot: Chicago 1861, rain, flooded mud street, carts stuck; crane down from the spire |
| 5 | 7.80-10.00 | mud_low / RAIN | low over puddles: a cart wheel sinks, a horse struggles, rain splashes |
| 6 | 10.00-12.13 | rain_street / RAIN | townsfolk hop across planks, a gentleman's boot sinks in mud (comic), muck flows nowhere |
| 7 | 12.13-14.80 | street_wide / DAY | workers shovel fill; a neighbouring shop already raised high, plank walk at the new level; pan |
| 8 | 14.80-17.00 | front_stair / DAY | the hotel door at old level; fill rising toward it (set_fill 0.2->0.5 on a side mound) to show doors would sink |
| 9 | 17.00-19.70 | street_wide / DAY | pullman walks in front of the hotel with rolled plans, looks up at it, confident nod; slow push |
| 10 | 19.70-21.68 | suite_window / DAY | rich in armchair with tea hears, looks out and bursts out laughing (laugh_big, no mouth sync) |
| 11 | 21.68-24.20 | suite_two / DAY | Q1 lip-sync: rich at the window points down mocking at pullman far below on the street |
| 12 | 24.20-28.09 | hotel_front / DAY | Q1 cont. lip-sync: medium two-shot from street — rich leaning out of the top window (mouth), pullman below calm, plans in hand; 2nd framing at 26.0 (push in) |
| 13 | 28.09-30.41 | crowd_street / DAY | nickname: townsfolk laugh and point at pullman carrying a jack; ไอ้แม่แรง lands on 29.73 |
| 14 | 30.41-32.50 | street_wide / DAY | workers file in carrying iron jacks on shoulders, down into the trench under the hotel |
| 15 | 32.50-34.70 | under_rows / DAY | count: jacks multiply in rows - 100 (32.5), 1000 (33.1), 5000 (33.6) - high angle, camera rises to reveal the rows |
| 16 | 34.70-36.90 | under_wide / DAY | 500 workers each by 10 jacks, pullman walks the aisle checking |
| 17 | 36.90-39.00 | suite_window / MORNING | two days later: rich looks out of the window, smug, cup in hand |
| 18 | 39.00-41.72 | tea_close / DAY | the tea is perfectly still (ripple 0); push in |
| 19 | 41.72-43.22 | suite_two / DAY | Q2 lip-sync: rich raises his cup, smug "เห็นมั้ย ไม่ขยับสักนิ้ว!" |
| 20 | 43.22-45.30 | under_wide / DAY | reveal: pullman blows the whistle (44.69 'นกหวีดดัง') |
| 21 | 45.30-47.10 | under_rows / DAY | 500 workers push their bars TOGETHER half a turn (set_jack_turn 0->180 deg), rows ripple in sync |
| 22 | 47.10-48.80 | jack_close / DAY | one jack: hands push the bar half a turn, the screw climbs, the beam above lifts a hair |
| 23 | 48.80-51.13 | hotel_front / DAY | outside: the whole hotel rises evenly at every corner (h 0.5->0.8, cribbing added), walls without a crack; slow crane |
| 24 | 51.13-53.30 | street_wide / DAY | aha: wide - the hotel high on its cribbing, the tiny workers beneath, no machine anywhere |
| 25 | 53.30-55.89 | under_rows / DAY | high wide over thousands of jacks turning together, lamps glowing; slow rise |
| 26 | 55.89-57.99 | front_stair / MORNING | day 5: rich steps out of the door, top hat, cane, one foot forward into the air (step_out) |
| 27 | 57.99-59.06 | front_stair / MORNING | 'ใต้เท้าไม่มีพื้น!': below his foot only air; the old stair sits ~2 m lower; freeze-ish beat, he looks down |
| 28 | 59.06-62.26 | street_wide / MORNING | wide: the hotel ~2 m above the street; fill not yet reached it; workers' heaps beside |
| 29 | 62.26-63.53 | front_stair / MORNING | he drops (fall pose, hat flying) into the mud with a splash (comic, no injury) at 62.26-63.1 |
| 30 | 63.53-66.48 | mud_low / MORNING | sit_in_mud muddy and dazed, then pay_sad: he hands his fat purse up to pullman; hard cut on 'เอง' (66.38) |

SFX cues: rain bed (4-6), cart creak/splash (5), shovels (7), laugh (10, 13 crowd), jack clank (14), metal rattle multiplying (15),
whistle 44.69, ratchet in sync (21-22), wood creak (23), door open (26), whoosh + splat 62.3, coin purse jingle 64.3.
