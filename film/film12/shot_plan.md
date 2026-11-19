# Shot plan, film 12 (ไอ้ร่มเดินได้)
Narration film12/audio/narration.wav (59.0 s), placed at +0.10 s. g = round(t*30). N = 1785 (59.5 s; hard cut on the last word).
Captions: film12/script/captions.json. Timing: film12/audio/timing.json.

| line | start (s) |
|---|---|
| hook | 0 |
| pivot | 5.75 |
| boss | 10.51 (quote 12.66-19.0) |
| nickname | 19.07 |
| count | 21.69 |
| false | 28.61 (quote 33.0-34.9) |
| reveal | 34.98 |
| aha | 44.66 |
| ending | 52.64 |
| end | 58.99 |

LOOK (client-approved style board, v3/set3d12/styleboard/board.jpg): a Georgian London street in rain, 1750s, warm amber windows
vs blue-violet rain shade, wet setts with layered puddles. Wide/medium framings that show the dense set, calm camera always moving,
new framing every 1.5-2.5 s. Sharp, NO DOF, no text anywhere. Heads above y 880. Mouths move ONLY on the head coachman's quotes
(12.66-19.0 and 33.0-34.9). Comic hits only (veg, egg, mud splash), never injury.

Set presets (v3/set3d12/street.py): street_wide, street_high, coach_low (the rank), hero_track (medium, follows the hero along the
pavement), box_seat (the head coachman up on his coach box, low angle), market (barrow + jeering crowd corner), puddle_low (camera
just above a big puddle, for the splash), rank_rush (the coach rank with a crowd rushing in), lights RAIN (grey-day rain, windows lit)
and DUSK_RAIN (lamps lit, deeper blue). States: set_crowd_umbrellas(k 0..1), set_rush(k), set_rank_busy(k 0..1: coaches full/empty),
set_pink_umbrella(on), throw props (cabbage, egg) with splat fx, mud splash wave, rain intensity.

Cast (v3/cast12): hanway (lean gentleman, tricorn, long dark-blue coat, white stock, black umbrella open/closed),
coachman (head coachman: stout, many-caped drab greatcoat, low round hat, red nose, big whip, mutton-chop whiskers),
coachman_b / coachman_c (thin and short jeerers), crowd men and women (period coats, tricorns, bonnets, some hold hats over heads),
wife (only the pink lace umbrella is shown, as a prop). Props: black umbrella, pink frilled lace umbrella, whip, cabbage, egg, coin purse.

| # | t0-t1 | preset / light | action |
|---|---|---|---|
| 1 | 0.00-2.20 | street_wide / RAIN | push in down the rainy street; Hanway walks toward camera under his black umbrella, calm |
| 2 | 2.20-3.90 | coach_low / RAIN | the coach rank: three coachmen on their boxes turn and glare at him |
| 3 | 3.90-5.75 | hero_track / RAIN | a cabbage flies in and bounces off his umbrella; he keeps walking (comic, no hurt) |
| 4 | 5.75-8.00 | street_high / RAIN crane down | the whole street in rain: every man hunched, hats over heads, soaked; only women under small umbrellas |
| 5 | 8.00-10.51 | market / RAIN | a soaked gentleman wrings his wig; a lady passes dry under a parasol-umbrella |
| 6 | 10.51-12.60 | box_seat / RAIN | the head coachman on his box bursts out laughing, belly shaking |
| 7 | 12.60-15.50 | coach_low two-shot | "ผู้ชายกางร่มเหรอ!" lip-sync, whip pointing at Hanway passing below |
| 8 | 15.50-19.07 | box_seat push-in | "...ข้าจะกางร่มลูกไม้สีชมพูของเมียข้าเอง!" lip-sync, chest out; the other coachmen roar |
| 9 | 19.07-21.69 | street_wide / RAIN, low | passers-by and coachmen point and laugh as Hanway passes ("ไอ้ร่มเดินได้") |
| 10 | 21.69-23.80 | market / RAIN | year 1: a coachman throws a cabbage leaf; it slaps the umbrella |
| 11 | 23.80-25.80 | hero_track / RAIN | year 2: an egg splats on the umbrella top, Hanway tilts it, unbothered |
| 12 | 25.80-28.61 | puddle_low / RAIN | year 3: a coach charges through the puddle; a big mud wave splashes Hanway head to toe (comic) |
| 13 | 28.61-31.50 | street_high / DUSK_RAIN | ten years on: the street crowded, ONE umbrella among many bare heads |
| 14 | 31.50-34.98 | box_seat / DUSK_RAIN | the head coachman shouts "เห็นมั้ย ไม่มีใครบ้าตามเอ็งหรอก!" lip-sync, others nod |
| 15 | 34.98-37.20 | coach_low / RAIN | close-ish on the coachman counting coins in his purse, looking at the sky, grinning |
| 16 | 37.20-40.00 | rank_rush / RAIN | REVEAL image: rain pours, the crowd rushes and fights for the coaches; coachmen grin, coins changing hands |
| 17 | 40.00-42.40 | rank_rush wide | every coach full and rolling; the coachmen are rich on a rainy day |
| 18 | 42.40-44.66 | hero_track / RAIN | Hanway strolls past the queue under his umbrella, dry, paying nothing; the coachman's grin drops |
| 19 | 44.66-47.00 | street_wide / RAIN | one gentleman watches Hanway, then opens his own umbrella |
| 20 | 47.00-49.00 | street_wide reverse | a second, a third: umbrellas pop open one by one along the pavement |
| 21 | 49.00-52.64 | street_high / RAIN crane | the whole street a sea of umbrellas (set_crowd_umbrellas 1.0); Hanway among them, smiling |
| 22 | 52.64-55.20 | coach_low / RAIN | the empty rank: coaches idle, horses bored, no customers (set_rank_busy 0) |
| 23 | 55.20-58.99 | box_seat / RAIN slow push | the head coachman sits on his empty coach under his wife's pink frilled lace umbrella, sulking; hard cut on the last word |

Sound cues: steady rain bed throughout; thunder roll at 0.0 and 37.2; laughter 10.6 and 19.1; cabbage thwack 3.9 and 22.0; egg splat
24.2; coach rumble + big splash 26.0; coins clink 35.5 and 39.0; umbrella pops 45.5, 47.2, 47.8, 48.3; sad horse snort 53.0.
