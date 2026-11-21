# Shot plan, film 7 (ไอ้มักกะโรนี — the Mona Lisa theft) — same grammar as films 5-6.
# Clock: narration PROJ/film7/audio/narration_bankky.wav at +0.10 s; g = round(t*30) bounds, round((t+0.1)*30) events; N = 3219 (107.30 s).
# Sentence starts (s): hook 0, pivot 7.80, boss 14.70, hero 19.96, nickname 26.05, night 30.66, take 37.12, door 44.53, count 51.19,
# alarm 55.46, chaos 62.62, turn 68.13, spread 74.53, hide 81.48, caught 85.77, reveal 91.49, ending 99.33, end 106.70.
# Captions PROJ/film7/script/captions.json. Framing change every 1.0-2.0 s; ECU inserts of the key object (the painting, the bulge, the
# empty hooks); low angle on the director; dissolves 9-12 f between locations, hard cuts on shocks. NO depth of field. Mouths only on
# quoted lines (director shot 6, coworkers shot 9, painter shot 19). Heads above y 880. Motif: the painting <-> the empty wall with 4 hooks.

| # | t0-t1 | location / preset | action |
|---|---|---|---|
| 1 | 0.00-2.40 | louvre / exit_door -> paris street | vincenzo_smock walks out of the opened door into daylight, the bulge under his smock, nervous smile at the camera |
| 2 | 2.40-4.60 | louvre / wall_eye | the empty wall spot: four hooks, guard yawning beside it (set_mona False) |
| 3 | 4.60-7.80 | paris / kiosk | the kiosk fills with Mona Lisa front pages (set_papers 0->24 fast), newsboy shouting (no lip-sync) |
| 4 | 7.80-11.20 | louvre / gallery_wide | establishing the crowded salon, 155 frames, people walking past without stopping |
| 5 | 11.20-14.70 | louvre / wall_eye | the small Mona Lisa among bigger paintings; a lady glances and walks on |
| 6 | 14.70-19.96 | louvre / wall_eye (low) | director_boast, huge from below, lip-sync on the quote; cut-in ECU painting at 18.0 |
| 7 | 19.96-23.20 | louvre / wall_eye | vincenzo (normal clothes) fitting a glass pane on the painting, careful |
| 8 | 23.20-26.05 | louvre / gallery_wide | vincenzo small among tall coworkers carrying glass panes |
| 9 | 26.05-30.66 | louvre / gallery_wide closer | coworkers laugh and point ("ไอ้มักกะโรนี!" lip-sync), vincenzo_mocked, then a glare (hurt) |
| 10 | 30.66-34.00 | paris / street_wide DUSK -> louvre / closet | night falls on the Louvre; vincenzo_hide_closet among brooms with a lantern |
| 11 | 34.00-37.12 | louvre / gallery_wide | Monday: empty museum, only workers in white smocks walking |
| 12 | 37.12-40.50 | louvre / wall_eye | vincenzo_smock lifts the framed painting off the hooks (set_mona_lift) |
| 13 | 40.50-44.53 | louvre / staircase | in the service staircase he unframes it (frame left on the steps), hides the panel under the smock (bulge) |
| 14 | 44.53-47.80 | louvre / exit_door | the door is locked; vincenzo_sweat rattles the knob |
| 15 | 47.80-51.19 | louvre / exit_door | the plumber walks up, unlocks it with a key, greets him with a smile; door swings open on daylight (set_door) |
| 16 | 51.19-55.46 | louvre / wall_eye | the empty wall; guard shrugs ("the photographers took it"), people walk past unaware; clock time passing via light change |
| 17 | 55.46-58.80 | louvre / wall_eye | next day: the painter with his easel points at the empty hooks and asks (lip-sync none — narrated) |
| 18 | 58.80-62.62 | paris / notre_dame_view | the towers of Notre-Dame still standing (callback to the boast) -> cut to director_shocked at the empty wall |
| 19 | 62.62-65.50 | louvre / gallery_wide | police search everywhere, guards, chaos |
| 20 | 65.50-68.13 | louvre / closet (as an office) | the young painter questioned by police, indignant; vincenzo walks by unnoticed in the background |
| 21 | 68.13-71.20 | louvre / empty_wall_queue | reopening: a long queue behind velvet ropes staring at the empty wall (set_queue) |
| 22 | 71.20-74.53 | louvre / wall_eye | ECU the four hooks, a lady gasps, a gentleman takes off his bowler |
| 23 | 74.53-78.00 | paris / kiosk | newspapers and posters with her face everywhere, gentleman reading |
| 24 | 78.00-81.48 | paris / street_wide | posters on the Morris column, newsboy shouting, people humming |
| 25 | 81.48-85.77 | room / under_bed_insert -> room_wide | the trunk under the bed slides out, the lid opens, the panel inside; vincenzo_peek_bed, candlelight |
| 26 | 85.77-88.60 | room / dealer_shop | vincenzo_offer: unwraps the panel on the dealer's desk; dealer_inspect |
| 27 | 88.60-91.49 | room / dealer_shop | dealer_signal; police burst in; vincenzo_arrested |
| 28 | 91.49-95.50 | louvre / wall_eye | the painting back on the wall, now the crowd presses in (reveal) |
| 29 | 95.50-99.33 | louvre / empty_wall_queue -> wall_eye | match-dissolve: the empty-wall queue becomes the crowd at the painting; push in to her smile |
| 30 | 99.33-103.20 | louvre / empty_wall_queue (modern feel: bigger crowd) | tens of thousands queueing; phones not allowed — keep it period-ambiguous (just a huge crowd) |
| 31 | 103.20-107.30 | louvre / wall_eye | final: slow push to the Mona Lisa behind glass, a reflection of a small man in a cap on the glass for a moment; hold to the end |
