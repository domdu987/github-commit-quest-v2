# Film 24 shot plan (17 shots, hard cuts only)
LOOK (client, 2026-11-26): R9 reference look (film/ref_shorts/R9_sheet.jpg, recipe on branch qtest/r9): Cycles GI, warm soft sun, sky fill, thin haze, bloom on hot spots. DOF allowed; 3 macro inserts (2, 8a, 9a). Out-of-focus foreground must be world-fixed. Characters stay 2D puppet cards. Render 24 spp, 75 % + upscale, OIDN.
Frame g = round(t*30); film 0..1950 (65.0 s). Narration placed at +0.10 s (as film 10): in-shot events use g = round((t+0.10)*30).
Each shot has ONE slow eased camera move (push/pull/slide/crane, ease-in-out). No shake, no snap. Foreground props fixed in the world.

Locations (set PROJ/v3/set3d24/joseon.py): **yard** = Joseon naval yard at Yeosu (slipway, turtle ship being finished, workers);
**sea** = Hansan waters with green rocky islands, the turtle ship, Korean panokseon, the Japanese fleet; **shore** = a small island beach (part of sea).

| # | t0-t1 (s) | g0-g1 | loc / preset | picture | camera | sound cue |
|---|---|---|---|---|---|---|
| 1 | 0.00-2.60 | 0-78 | yard / roof_low | turtle ship on the slipway, low 3/4 view; a Korean worker kneeling on the roof hammering a spike in (arm only moves, knees planted); Yi stands on the quay below, arms behind back | slow push-in 8 % | hammer clinks on beats |
| 2 | 2.60-5.02 | 78-151 | yard / macro_dragon | MACRO: the carved dragon head's mouth puffs grey-yellow smoke; yard in bokeh behind | slow push 5 % | smoke hiss |
| 3 | 5.02-9.60 | 151-288 | sea / fleet_wide | the Japanese fleet: many atakebune and sekibune with banners sailing (+x), varied ships | slow lateral slide with the fleet | sea + drums far (sfx) |
| 4 | 9.60-14.37 | 288-431 | yard / yard_wide | wide yard: the finished closed-roof turtle ship on the slipway, workers, Yi on the quay in front, looking at it | slow push-in toward ship | woodwork ambience |
| 5 | 14.37-17.10 | 431-513 | sea / flag_deck | Japanese commander on his flagship deck, big belly laugh (head back); 2 soldiers behind (different) | slow push-in | laugh |
| 6 | 17.10-21.47 | 513-644 | sea / flag_deck_b | commander points mockingly (screen-right) then raises a finger for the promise; LIP-SYNC 16.1-21.4 | slow slide left | — |
| 7 | 21.47-24.45 | 644-734 | sea / flag_deck_crew | 3-4 varied Japanese soldiers on deck laughing and pointing (bounce at the hips, feet planted) | slow slide | crowd laugh |
| 8a | 24.45-28.70 | 734-861 | yard / macro_spikes | MACRO along the roof: spike rows pop in row 1 (~26.4), 2 (~27.6), 3 (~28.3); a worker's hammer hand in the soft background | slow lateral slide | clink x3 |
| 8b | 28.70-30.64 | 861-919 | yard / roof_top | high 3/4 over the full spiked roof; the side gun ports open (~29.6) and muzzles poke out; workers kneel on the roof edge | slow push | thunk of ports |
| 9a | 30.64-31.80 | 919-954 | sea / macro_oar | MACRO at water level: a Korean oar blade digs into the sea, splash and foam (the Korean ships rowing away) | slow slide | oar splash |
| 9 | 31.80-33.40 | 954-1002 | sea / hansan_high | high wide over the strait: a few Korean ships + turtle ship turn and sail away (-x); Japanese fleet behind | slow push | oars / sails |
| 10 | 33.40-37.09 | 1002-1113 | sea / flag_bow | commander on the bow of his flagship shouting, arm forward; LIP-SYNC 34.8-37.0; the fleet behind | slow push-in | shout |
| 11 | 37.09-41.91 | 1113-1257 | sea / chase | the Japanese fleet charging in open sea; on the nearest ship's bow 3 varied soldiers with raised swords (planted) | slow lateral slide with the ship | war drums (sfx) |
| 12 | 41.91-47.10 | 1257-1413 | sea / board | a Japanese ship alongside the turtle ship; soldiers at its rail with a ladder look at the spiked roof, sweat, and step back (real steps) | slow push-in onto the spikes | gulp, ladder clatter |
| 13 | 47.10-53.57 | 1413-1607 | sea / reveal_top | ONE-IMAGE REVEAL: high aerial, the Korean fleet turns into a U around the Japanese fleet; cannon smoke puffs from every side; turtle ship in front centre | slow rise and push | cannon booms |
| 14 | 53.57-58.90 | 1607-1767 | sea / aftermath | turtle ship sails through drifting smoke; Japanese ships behind listing with broken masts and smoke (no fire, no people hurt) | slow low push | creaks |
| 15 | 58.90-65.00 | 1767-1950 | sea / shore | the commander clings to a floating plank (it rides the water) near a beach, then on the sand crawls forward on hands and knees (crawl cycle, limbs alternate) | slow pull-back | splash, sand; HARD CUT on the last word |
