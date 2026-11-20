# Shot plan, film 21 (ไอ้ชาวนาบนเนิน — Battle of Stirling Bridge, 11 Sept 1297)
Narration film/film21/audio/narration.wav (61.25 s), placed at +0.10 s. g = round(t_film*30), t_film = t_narr + 0.10.
**N = 1848** (61.60 s, hard cut on the last "ตูม").
Captions film/film21/script/captions.json (narration time). Timing film/film21/audio/timing.json. Facts FACTS.md.
Set film/v3/set3d21 (stirling.py + API.md; use the closest preset in API.md if a name differs). Cast film/v3/cast21.

## Sentence starts (narration time)
| line | start | end |
|---|---|---|
| hook | 0.00 | 5.14 |
| pivot | 5.19 | 13.77 |
| bridge | 13.82 | 17.97 |
| mocker | 18.02 | 26.26 |
| nickname | 26.32 | 29.34 |
| count | 29.39 | 34.65 |
| false | 34.71 | 37.89 |
| crisis | 37.94 | 41.14 |
| reveal | 41.19 | 50.47 |
| aha | 50.53 | 54.50 |
| ending | 54.55 | 61.25 |

## Quote windows (mouths move ONLY here, +-0.15 s)
- cressingham: 21.29-26.26 ("ชาวนาบนเนินไม่กี่คน! อ้อมไปเปลืองเงินหลวง ข้ามสะพานนี่แหละ เร็วดี ประหยัดดี!"). Laugh (no lip-sync, laughing pose + bounce) 20.29-21.29.
- cressingham: 36.32-37.89 ("เห็นไหม กลัวจนขยับไม่ได้!"). Camp laughs 34.71-36.32 (laughing poses, bounce, mouths in a fixed laugh drawing, no lip-sync).
- Nobody else speaks. The Scots never open their mouths (except the horn blower's cheeks puffing on the horn at 39.7-41.1).

## Hard content rules
- Comic and BLOODLESS: no wounds, no weapons striking a body, no one lying still, no one shown dying. Spears point and block; English soldiers back off, bump, wobble, fall into water and come up splashing (heads, helmets floating, spluttering).
- Cressingham's fate is NEVER shown or hinted. He appears only on the SOUTH bank (camp, money table, river bank). In the ending only his empty money table and tipping coin scale appear.
- No kilts, no blue face paint (anachronistic). Scots: knee-length tunics (brown, ochre, moss, faded red), simple iron caps or bare heads, long spears, a few round shields; Wallace tall in a mail shirt with a long sword on his back; Moray in mail and a green surcoat.
- English: knights in mail with red/blue/gold surcoats (no readable heraldry text), great helms or open bascinets, on caparisoned horses; foot soldiers in padded gambesons and kettle hats with spears; Welsh archers optional in the camp.
- No readable text anywhere (banners carry simple shapes: lions, chevrons, stripes).

## Camera rules (production-lessons §10 + bible camera.md), MANDATORY in every shot
- 22 mm, roll 0. Every shot has a clear eased move: drift push or pull 6-10 %/s with a 20-60 px/s lateral slide, or a snap (13-25 frames, x1.3-x3). Never more than 6 frames under 0.25 px/frame. No near-static hold over 1 s.
- Framing changes every 1.3-1.4 s on average (cuts + dissolves + snaps). Quick push-in on punch lines; one whip (s21); snaps on the reveal steps.
- Foreground prop 1-2 D from the lens in most shots: spear shafts, heather and gorse, rocks, tent ropes and poles, the coin chest, bridge rail posts, reeds on the bank, a banner pole.
- Transitions: 11-frame dissolve between locations or time jumps (D11); hard cut elsewhere (C).
- Heads: centre y 450-760, all heads above y 880. Laughing characters bounce about 0.06 D at about 3 Hz. Nobody is frozen: idle sway and blinks. Horses: idle head bob and tail swish, walk cycle on the bridge.
- Characters on a moving thing stay parented to it (riders to their horse).
- Acceptance: median in-shot frame-diff >= 4, p90 >= 12 (90x160 grey), shown next to film 2 at the FINAL gate.

## Locations (one coherent valley; time: morning, low warm sun from the south-east, light haze in the distance)
- `hill`: Abbey Craig: a craggy wooded hill north of the river (rocks, heather, gorse, Scots pines). The Scots stand along its lower slope and look down at the bridge.
- `bridge`: the narrow wooden trestle bridge over the Forth: plank deck, rails, timber piers in the water, two horses fill its width. North end: a short causeway into flat meadow inside the river loop. South end: the English camp.
- `valley`: the whole Forth valley seen high: a big meandering loop of the river north of the bridge (the trap), the bridge, the hill, the camp, and Stirling's castle rock in the far south-west with a small period castle. Hills and haze beyond.
- `camp`: the English camp on the south bank: pavilion tents (striped red/cream, blue/gold), banners on poles, horse lines, carts, campfire smoke, a cooking pot, weapon racks, and Cressingham's money table (coin chest, scales, stacks of coins, a ledger with no text). From the bank you look across the river to the bridge and the hill.
- `riverbank`: the north-bank meadow at the water's edge inside the loop (reeds, mud, shallow water, the bridge in the background), for the ending splash. The water is smooth and layered with foam lines, glitter and wakes; splashes are spray crowns with falling droplets (not stacks of round blobs).

## Shots (t = NARRATION time; film time = t + 0.10)
| # | t0-t1 | in | preset | action + camera move |
|---|---|---|---|---|
| 1 | 0.00-4.08 | — | BIGZOOM (valley_wide -> hill) | **BIGZOOM 1 (QA §H)**: ONE continuous eased camera move, 4.1 s. Start EXTREME WIDE high over the Forth valley (like valley_wide): the loop, the narrow bridge with English knights crossing two by two (place_troops bridge), the camp, Abbey Craig; the Scots tiny (<5 % of frame height) on its slope. Ease-in, swoop down past pines and gorse on the crag (foreground parallax) and end in a MEDIUM shot (35-60 % of frame height) of the Scots line on the shelf: Wallace in the centre, arms folded on spears, unmoving, the bridge still visible far below behind them. Build the whole valley in one scene (valley preset) and stage the Scots at the hill marks (PAD2). |
| 2 | 4.08-5.19 | C | hill_eye | quick push-in (snap 15 f, x1.4) on the Scot chewing a grass stalk on "อะไรเลยสักอย่าง"; others still. |
| 4 | 5.19-7.74 | D11 | valley_wide | establishing: the Forth valley in morning light: river loop, bridge, hill, camp, castle rock. High, crane-down + push 6 %/s. |
| 5 | 7.74-9.82 | C | camp_wide | English knights on caparisoned horses parade past tents and banners; lots of life (flags flutter, smoke). Slide 50 px/s + push; tent rope fg. |
| 6 | 9.82-11.89 | D11 | hill_low | Scots spearmen on foot among rocks and gorse, long spears up against the sky. Low 1.2 D, +14 deg, pull-out 7 %/s. |
| 7 | 11.89-13.82 | C | valley_river | eye level just above the water from the south bank: the river between the camp side and the hill side, the hill with Scots on the far side. Push 7 %/s + slide; reeds fg. |
| 8 | 13.82-16.52 | D11 | bridge_high | the long narrow wooden bridge from high above one bank: the only crossing. Push in along the bridge 8 %/s. |
| 9 | 16.52-17.97 | C | bridge_end_south | two horses side by side wedged on the deck, a knight sucks his belly in; snap push (16 f, x1.4) on "เต็มแล้ว" (17.37). |
| 10 | 17.97-21.29 | D11 | camp_table | Cressingham at his money table counting coins into the chest (coins clink); he looks up across the river and bursts out laughing at "หัวเราะลั่นว่า" (20.29, laugh + bounce). Push 8 %/s, coin chest fg. |
| 11 | 21.29-23.47 | C | camp_bank | low two-shot on the south bank: Cressingham near, points across the river at the tiny Scots on the hill, lip-sync "ชาวนาบนเนินไม่กี่คน! อ้อมไปเปลืองเงินหลวง"; old Earl Surrey behind, listening. Low 1.2 D, slow push + slide. |
| 12 | 23.47-26.32 | C | camp_bank | QUICK PUSH-IN (snap 20 f, x1.5) as Cressingham slaps the coin purse and flings an arm at the bridge: "ข้ามสะพานนี่แหละ เร็วดี ประหยัดดี!" (lip-sync), chin up. |
| 13 | 26.32-27.80 | C | camp_wide | the camp laughs: soldiers point across at the hill, one mimes a farmer hoeing with his spear (bounce 3 Hz). High-ish, pull-out 7 %/s + slide. |
| 14 | 27.80-29.39 | C | hill_eye | the nickname lands: punch-in cut on the Scots line (speed lines 6 f, 2-frame shake), Scots unbothered; Wallace raises one eyebrow. Drift push 5 %/s. |
| 15 | 29.39-31.17 | D11 | bridge_end_north | count 1 ("สิบคน"): the first ten English footmen step off the bridge onto the north causeway and glance up at the hill nervously. Push 8 %/s, rail post fg. |
| 16 | 31.17-32.75 | C | hill_eye | "ยังเงียบ": the Scots still silent; one scratches his nose. Snap pull-out (15 f, x0.7). |
| 17 | 32.75-34.71 | C | valley_loop | count 3 ("เป็นพัน"): high over the loop: the meadow inside the loop fills with English troops and knights, more still coming over the bridge; the Scots on the hill unmoved. Stepped pull-out (one 14 f step on "เป็นพัน", 32.75). |
| 18 | 34.71-36.32 | D11 | camp_bank | FALSE PAYOFF: on the south bank the waiting English laugh and point across (laughing poses, bounce out of phase). Pull-out 8 %/s + slide; banner pole fg. |
| 19 | 36.32-37.94 | C | camp_bank | quick push-in on Cressingham, lip-sync "เห็นไหม กลัวจนขยับไม่ได้!", smug, thumbs in his belt. Push 10 %/s. |
| 20 | 37.94-39.69 | C | bridge_end_north | calm before: the bridge with the column still crossing two by two, about half the army over; a knight on the causeway yawns. Longest gentle push 7 %/s, slight sway. |
| 21 | 39.69-41.19 | C | hill_low | the horn: a Scot raises a long cow-horn and blows (cheeks puff, no lip-sync); Wallace lifts his sword arm. Low angle, sky behind; snap push (14 f, x1.5) on "เสียงแตร" (39.69), 2-frame shake. |
| 22 | 41.19-43.07 | C | hill_over | WHIP (4 off, 7 on) from the horn down the slope: the Scots run down the hill with spears forward, gorse flicking past in the fg. Lens rides down the slope behind them, 5 Hz shake decaying. |
| 23 | 43.07-44.73 | C | bridge_end_north | the Scots' spear wall slams across the north end of the bridge ("ปิดหัวสะพาน", 43.78): spears level, a solid row; the English on the causeway jump back, helmets wobble. Snap push (16 f, x1.5). |
| 24 | 44.73-50.53 | C | BIGZOOM (valley_loop -> camp_bank) | **BIGZOOM 2 (QA §H) + THE ONE-IMAGE REVEAL**, ONE continuous move, 5.8 s. Start high over the loop (valley_loop): the English on the north bank boxed inside the river loop, the bridge mouth blocked by the Scots spear wall like a cork, the other half on the south bank; hold-drift 5 %/s for ~1.5 s while "ครึ่งทัพที่ข้ามมาแล้ว ถอยไม่ได้ ติดอยู่ริมน้ำ" plays, then on "อีกครึ่ง" (47.50) swoop down across the river to the south bank, past banners and tents, ending MEDIUM on Cressingham and Surrey watching helplessly: jaws drop (shocked swap behind a blink, sweat drop), soldiers on tiptoe, on "ได้แต่ยืนดู". Build the whole valley in one scene. |
| 26 | 50.53-52.50 | D11 | bridge_deck | AHA: the column tries to turn back on the bridge: two horses wedged nose to tail, everyone squeezes two at a time, a knight's helmet pops off. Push 8 %/s. |
| 27 | 52.50-54.55 | C | bridge_high | the jam from above: two-by-two stack all along the narrow deck, nobody moves. Snap pull-out (15 f, x0.7) on "เหมือนกัน" (53.5). |
| 28 | 54.55-56.88 | D11 | camp_table | ENDING: Cressingham's EMPTY money table on the south bank (nobody at it), the coin scale tips on "เร็วดี" (55.80) and the coin chest lid slams on "ประหยัดดี" (56.22). Push 9 %/s. |
| 29 | 56.88-58.86 | C | riverbank | the English on the north bank look at the blocked bridge, then at the water, then at each other; one pinches his nose. Slide 40 px/s + push. |
| 30 | 58.86-60.60 | C | riverbank | they jump into the Forth: a row of comic jumps, arms up, spray crowns; heads and helmets bob up, spluttering, and swim for the far bank. Pull-out 8 %/s. |
| 31 | 60.60-61.50 | C | river_low | "ตูม ตูม ตูม": water level, three big spray crowns in a row on each "ตูม" (60.6, 60.9, 61.2), quick push. HARD CUT on the last splash (g 1848). |

Shot count 29 in 61.6 s. BIGZOOMs (QA_TEAM §H): shot 1 (film 0.10-4.18 s, g 3-125) and shot 24 (film 44.83-50.63 s, g 1345-1519).
Angle types used: bird's-eye/high (4, 8, 17, 24, 27), low hero (6, 21), over-the-shoulder (1 end, 22), through a foreground frame (2, 9, 20, 26: rails, spears, tent ropes), side tracking (5, 15, 26), crane down (1, 4, 24).
Angle mix (approximate): establishing/vista (4, 8, 17, 24, 27) about 20 %; eye (2, 3, 7, 14, 15, 16, 20, 23, 26, 29, 30) about 38 %; low (6, 11, 12, 21) about 12 %; high camp (13) and inserts (10, 28, 31) about 15 %.
Key takes for QA-art at the TAKE gate: s01 (hook, BIGZOOM 1), s09 (reveal, BIGZOOM 2), s07 (false payoff), s11 (ending).

## Sound cues (conform; levels per captions-sound.md, music m1 at -31 dB under the voice)
hooves on planks (2, 9, 20, 26), coin clink (10, 28), crowd laugh (13, 18), horn blast (21), running feet and shouts with no words (22), spear-wall clack (23), whoosh (22, 24), wood creak (26, 27), coin scale tip and chest slam (28), splashes (30, 31, one per "ตูม").
