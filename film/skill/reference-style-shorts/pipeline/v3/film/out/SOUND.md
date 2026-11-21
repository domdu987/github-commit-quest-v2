# SOUND — film_v1_thai

Mix spec: `__PROJ__/v3/film/out/mix_film.json` (built by `__PROJ__/v3/film/out/sound/build.py`), mixed with `PROJ/audio/mixer.py` into `__PROJ__/v3/film/out/film_mix.wav` (48 kHz stereo, 65.500 s) and muxed into `PROJ/deliver/film_v1_thai.mp4`. The picture stream is a stream copy of `film_silent.mp4` (the video packets have the same MD5, 1965 frames). The audio is AAC 192k.

- **Voice:** `PROJ/audio/th/full_v2/narration.wav` (the new voice) at +0.100 s, gain 1.511506647219448 (`mix_settings.json` voice_gain). The old voice and the hook's voice entry are not used.
- **Music:** `music_fit.wav` from 0.0 s to the end, bed RMS −38.0 dBFS, with a 0.4 s fade-out at the very end (65.1–65.5 s, on the drip).
- **Hook (0–5 s):** the 16 effect entries of `PROJ/v3/out/mix_opening.json` are reused unchanged. Their summed effects render with 0.0 difference from the approved hook. No other effect starts before 5.000 s.
- **After the hook:** 26 point effects (one every 2.3 s on average) plus 10 ambience layers. Every post-hook effect has its rendered peak capped at −11 dBFS (ambiences at −14). Overlaps were checked: the summed effects stay at or under −10.2 dBFS while the voice speaks.

## Measurements (`__PROJ__/v3/film/out/sound/measure.txt`)

- **Overall:** RMS −16.5 dBFS; peak −1.01 dBFS (the mixer's limiter is at 0.89, and the pre-limiter peak was 1.10).
- **Voice:** −16.0 dBFS RMS over its active frames, −16.7 dBFS over the whole file. Its raw peak is −0.38, so the limiter catches the voice peaks.
- **Mix while the voice is active:** −15.9 dBFS RMS.
- **Gaps between words:** 79 voice-silent runs of 50 ms or more, 7.15 s in all. The mix RMS in these gaps is −30.0 dBFS.
- **Music bed:** −38.0 dBFS RMS.
- **Effects placed:** 52 entries, of which 16 come from the hook, 26 are point effects and 10 are ambiences.
- **Effects over −10 dBFS while the voice speaks** (speech map = caption phrase times +0.1 s): **after 5 s, none**. The highest single effect is −11.0 and the highest summed effects are −10.2 (at 60.1 s, thunder over the wave roar). **Inside the approved hook, three entries reach or exceed −10**, unchanged from mix_opening.json:
  - thump_jab at 2.000 s, peak −8.9
  - whoosh_whip at 2.300 s, peak −10.0
  - eraser_rub at 3.133 s, rendered peak −7.8 (it is set as RMS −25)

## Placed effects

The level column shows the spec setting. The measured column shows the rendered peak and RMS in dBFS over the clip, and pk-in-speech is the effect's peak where it overlaps the phrase times.

| # | time (s) | sound | type | level (spec) | measured pk / RMS | pk in speech | cue |
|---|---|---|---|---|---|---|---|
| 1 | 0.000–0.30 | whoosh_fast | hook | peak -19.0 | -18.9 / -31.0 | -28.0 | 0.000 prop_move: arm with the red pencil swings in from the lower left (whoosh, light) |
| 2 | 0.233–0.35 | map_marker | hook | peak -16.0 | -16.0 / -30.6 | -16.0 | 0.233 pencil_draw: pencil draws the red track north, one continuous stroke (line 0 to 0.75); scratch of pencil on paper |
| 3 | 0.233–1.20 | pencil_scratch | hook | RMS -27.0 | -12.2 / -27.1 | -12.2 | 0.233 pencil_draw: pencil draws the red track north, one continuous stroke (line 0 to 0.75); scratch of pencil on paper |
| 4 | 0.310–0.76 | whoosh_fast | hook | peak -15.0 | -14.9 / -27.3 | -14.9 | 0.267 camera_snap: snap push onto the pencil point (camera whoosh in) |
| 5 | 1.170–1.65 | whoosh_whip | hook | peak -11.0 | -11.0 / -27.3 | -11.0 | 1.200 pencil_draw: pencil keeps drawing, slowing (line 0.75 to 0.92) |
| 6 | 1.200–1.83 | pencil_scratch | hook | RMS -31.0 | -16.9 / -32.2 | -16.9 | 1.200 pencil_draw: pencil keeps drawing, slowing (line 0.75 to 0.92) |
| 7 | 1.900–2.01 | pencil_scratch | hook | RMS -24.0 | -11.2 / -25.7 | -11.2 | 1.900 camera_snap: snap reframing on the jab (short whoosh in) |
| 8 | 1.930–2.23 | whoosh_fast | hook | peak -19.0 | -18.9 / -29.5 | -18.9 | 1.900 camera_snap: snap reframing on the jab (short whoosh in) |
| 9 | 2.000–2.60 | thump_jab | hook | peak -9.0 | -8.9 / -22.3 | -8.9 | 2.000 jab_impact: JAB lands on New York: pencil point hits the map, arrow head complete (hard tap / thock) |
| 10 | 2.300–2.78 | whoosh_whip | hook | peak -10.0 | -10.0 / -26.9 | -10.0 | 2.300 whip_pan: WHIP PAN to the right, cut inside it at 2.433 s, the two-shot arrives braking |
| 11 | 2.560–2.81 | thump_jab | hook | peak -22.0 | -21.9 / -31.7 | -21.9 | 2.433 prop_move: the chief steps up to the map with the eraser raised (two soft footfalls on wood) |
| 12 | 2.860–3.11 | thump_jab | hook | peak -23.0 | -22.9 / -32.7 | -22.9 | 3.133 eraser_rub: eraser rubbing stroke 1 (one back-and-forth scrub; erased 0 to 15 percent) |
| 13 | 3.133–3.33 | thump_jab | hook | peak -19.0 | -18.9 / -29.3 | -18.9 | 3.133 eraser_rub: eraser rubbing stroke 1 (one back-and-forth scrub; erased 0 to 15 percent) |
| 14 | 3.133–4.08 | eraser_rub | hook | RMS -25.0 | -7.8 / -26.8 | -7.8 | 3.133 eraser_rub: eraser rubbing stroke 1 (one back-and-forth scrub; erased 0 to 15 percent) |
| 15 | 3.600–4.40 | pop_surprise | hook | peak -11.0 | -13.7 / -30.3 | -13.7 | 3.600 camera_snap: snap push onto the hero's face (whoosh in) |
| 16 | 3.630–4.03 | whoosh_fast | hook | peak -18.0 | -17.9 / -29.8 | -17.9 | 3.633 eraser_rub: eraser rubbing stroke 4 (one back-and-forth scrub; erased 60 to 73 percent) |
| 17 | 5.000–6.65 | office_tone | ambience | RMS -34.4 | -14.1 / -35.6 | -14.1 | 4.300 whoosh: soft whoosh into the flash-back (dissolve); office bed up: clock tick, teletype chatter, lamp hum |
| 18 | 13.300–16.85 | beach_calm | ambience | RMS -33.2 | -14.0 / -33.6 | -14.0 | 13.300 surf: gentle surf loop and gulls fade in (pre-lap under the dissolve) |
| 19 | 31.600–37.45 | rain_drizzle | ambience | RMS -41.5 | -14.1 / -41.7 | -14.1 | 31.600 rain: soft rain pre-lap |
| 20 | 31.950–33.80 | office_tone | ambience | RMS -34.1 | -14.0 / -35.4 | -14.0 | 31.950 bed: kitchen tone: clock tick, kettle tail; drizzle on the pane (bed to 36.1); thin rain runs down the panes |
| 21 | 33.770–36.22 | beach_calm | ambience | RMS -34.0 | -19.0 / -39.4 | -19.0 | 33.770 bed: dull slow surf and light drizzle bed (to the end of the shot) |
| 22 | 36.200–37.44 | office_tone | ambience | RMS -33.0 | -15.7 / -34.3 | -15.7 | 36.200 bed: rain on the office window (bed), drizzle running down the panes |
| 23 | 39.620–44.62 | wind_storm | ambience | RMS -33.0 | -20.8 / -35.5 | -20.8 | 39.620 whoosh: long crash whoosh with wind: the crash push into the map (g1188-1205); office sound ducks out, open-sea wind a |
| 24 | 45.000–50.00 | wind_storm | ambience | RMS -30.0 | -17.4 / -31.5 | -17.4 | 47.500 gust: gust 1 (low): first wave of wind arrows streams past from behind the lens |
| 25 | 59.550–62.55 | rain_drizzle | ambience | RMS -41.6 | -14.1 / -42.1 | -14.1 | 59.550 crash: wave crash, white roar carried over the wipe |
| 26 | 62.550–64.40 | wave_roar | ambience | RMS -32.6 | -14.1 / -34.4 | -14.1 | 62.550 bed: muffled roar outside, house timbers groan (bed); the wall of water fills the panes |
| 27 | 6.600–7.08 | whoosh_whip | effect | peak -13.0 | -13.0 / -29.6 | -13.0 | 6.600 whip: whip whoosh: accelerating whip-tilt down-right toward the map (cut hidden in it) |
| 28 | 7.900–9.70 | thunder_low | effect | peak -20.0 | -19.0 / -33.4 | -19.0 | 7.900 thunder: far thunder roll and sub rumble (storm motif, first time) |
| 29 | 11.350–12.20 | pencil_scratch | effect | RMS -26.1 | -11.1 / -26.5 | -11.1 | 11.350 chalk: chalk scratch with a slide whistle that rises and veers away at 11.74 (the curve bends out to sea) |
| 30 | 13.050–13.30 | thump_jab | effect | peak -12.0 | -11.9 / -21.7 | -11.9 | 13.050 stamp: rubber-stamp thunk (tick mark lands on the chalk curve) |
| 31 | 14.950–15.45 | whoosh_fast | effect | peak -15.0 | -14.9 / -27.7 | -14.9 | 14.950 whoosh: whoosh: the crash push down to the sleeper (g448-473) |
| 32 | 18.400–19.30 | pencil_scratch | effect | RMS -27.5 | -11.0 / -27.8 | -11.0 | 18.400 zip: pencil zip, one bold freehand stroke north, rising |
| 33 | 21.675–22.05 | eraser_rub | effect | RMS -28.3 | -11.1 / -28.5 | -11.1 | 21.675 squeak: eraser squeak 'vroom' up the red line, toy beep-beep at the top |
| 34 | 23.250–23.85 | eraser_rub | effect | RMS -28.1 | -11.0 / -29.4 | -11.0 | 23.250 squeak: eraser squeak 1 |
| 35 | 26.500–27.98 | crowd_chuckle | effect | peak -15.0 | -15.0 / -29.2 | -15.0 | 26.500 walla: laughter walla, six to eight voices swelling (the whole building; non-verbal) |
| 36 | 28.100–28.35 | thump_jab | effect | peak -12.0 | -11.9 / -21.7 | -11.9 | 28.100 slap: paper slap (the label hits the map) |
| 37 | 29.050–31.50 | teletype | effect | RMS -33.7 | -11.1 / -34.3 | -11.1 | 29.050 clatter: teletype clatter: the official forecast feeds up out of the machine |
| 38 | 32.580–33.08 | whoosh_fast | effect | peak -17.0 | -16.9 / -29.7 | -16.9 | 32.580 whoosh: whoosh: crash pull-out from the weather box to the table framing (g977-994) |
| 39 | 36.300–37.42 | whistle_tune | effect | peak -14.0 | -13.9 / -26.1 | -13.9 | 36.300 whistle: jaunty whistled tune (the theme, non-verbal): the chief strolls in, held whistle mouth, three note glyphs |
| 40 | 37.420–37.92 | whoosh_fast | effect | peak -14.0 | -13.9 / -26.7 | -13.9 | 37.500 whoosh: crash whoosh out (zoom-out from the grin into G) |
| 41 | 39.600–42.00 | thunder_low | effect | peak -14.0 | -13.0 / -28.5 | -13.0 | 39.600 thunder: first real thunder roll; the crash push into the map begins (carries into s19) |
| 42 | 43.300–43.70 | thump_jab | effect | peak -11.1 | -11.0 / -24.1 | -11.0 | 43.300 boom: stone-wall boom with sub: the west wall locks (face vertical) |
| 43 | 46.550–46.80 | thump_jab | effect | peak -14.0 | -14.1 / -25.1 | -14.1 | 46.550 bonk: bonk and sign pop: the spinner hits the east wall, no-right-turn pictogram pops |
| 44 | 48.100–48.45 | thump_jab | effect | peak -13.0 | -12.9 / -24.0 | -12.9 | 48.100 gust: gust 3 (highest): third wave catches the spinner, it squashes flat |
| 45 | 50.600–51.08 | whoosh_whip | effect | peak -13.0 | -13.0 / -30.7 | -13.0 | 50.600 whoosh: whip whoosh: the whip pull-out to the whole western Atlantic (through the dissolve) |
| 46 | 53.720–54.72 | shimmer_reveal | effect | peak -14.0 | -12.6 / -32.7 | -12.6 | 53.720 dong: bell-like dong: the walls pulse once and start to sink back into the paper (reveal) |
| 47 | 55.790–57.35 | riser_tension | effect | peak -16.0 | -16.0 / -33.6 | -16.0 | 56.260 fog: low brass and breath swell begins (fog motif), sub rumble: the pale band on the horizon (g1688) |
| 48 | 57.350–57.70 | thump_jab | effect | peak -11.1 | -11.0 / -22.1 | -11.0 | 57.350 hit: orchestra hit on the hard cut, then 6 frames of near silence |
| 49 | 58.100–61.20 | wave_roar | effect | peak -12.0 | -11.4 / -25.9 | -11.4 | 58.400 rumble: ground rumble, timber creaks, wires whine (the shake starts, g1752) |
| 50 | 60.100–62.30 | thunder_low | effect | peak -16.0 | -15.0 / -30.2 | -15.0 | 60.100 thunder: thunder crack |
| 51 | 62.080–62.48 | thump_jab | effect | peak -12.0 | -11.9 / -23.6 | -11.9 | 62.080 impact: impact boom, ink splat and window rattle: the spinner hits the arrow head at N.Y. |
| 52 | 64.000–64.70 | paper_slide | effect | RMS -28.0 | -13.1 / -28.0 | -13.1 | 64.000 flutter: newspaper flutter under the saucer |

## Cues thinned
The point cues between 5 and 65.5 s were thinned to about one every 2.5 s. Snaps or whooshes that sit within about 1 s of a stronger event were left out, for example 12.43, 17.78, 19.40, 20.92, 24.45, 25.43, 30.15, 38.65, 41.05, 45.95, 53.37, 54.47, 57.70, 61.25 and 63.38. Repeated figures were reduced to one sound: the three pops at 9.15–9.39, the eight terrace thuds at 41.1–42.18, the two bonks and the two wall booms. The extra erase and draw strokes at 23.85, 24.85 and 25.35, the stamp at 29.92, the paper rustle at 27.60, the marker zip at 44.50 and the paper-tear zip at 59.80 were also dropped.

## Cues with no fitting sound in the library (nothing was generated or downloaded)
- **Rotating or mechanical:** the spinner ratchet and whirr (7.40, 40.30), the sign-spin ratchet (49.22), the spinner grumble (47.15) and the creak or squeeze of the walls (42.40).
- **Bells and chimes:** the glint and wink tings and the dings (9.70, 18.86, 19.95, 23.05, 25.90, 39.45, 50.40), the compass ping (45.25), the teletype carriage bell (29.70), the single wind chime (55.90) and the buoy bell (58.90).
- **Musical and comic accents:** the wood-block knocks (10.90, 11.10), the slide whistles (11.35, 37.60), the harp pluck (15.80), the rimshot (37.42), the squeeze-horn honk (39.10), the orchestra hit (57.35, a thump was used in its place) and the soft poof pass-bys (51.0–51.8).
- **Human and animal sounds:** snores (15.80, 16.40), the chief's panting (26.00), the gasps (57.50), the rooster (31.85), the gulls (34.98, 55.10, 56.60; beach_calm carries gulls only under s08 and s16), the far foghorn (35.05) and the chief's solo chuckle (22.60; crowd_chuckle was kept for the seniors at 26.5).
- **Footsteps and wood:** the heavy step and creak (20.40), the steps on boards and sand (33.85, 33.95), the heel clicks (36.52, 37.20), the running steps on sand (58.10) and the timber creaks (58.40, 62.55).
- **Cloth, paper and household:** the towel flap (14.10), the cup clink and rattle (33.15, 62.60), the radio murmur (33.40), the kettle whistle (24.85), the pointer clatter (62.30), the chair shove (62.55), the shutters banging (58.90), the window rattle and the pane crack (62.08, 64.10), the hat pop (57.60) and the calendar flutter (5.70).
- **Drops and drips:** the plips (35.60–35.90, 42.65, 65.05).
- **Other:** the chalk crumble (43.80), the neon hum (44.50), the flash hiss with its ringing tail (62.44), the doppler engine roar and whine (48.30, 51.90; wind_storm and riser_tension stand in for them) and the piano note on the drip (65.05).
