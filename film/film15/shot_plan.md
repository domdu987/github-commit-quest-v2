# Shot plan v2, film 15 (ไอ้ปลาดิ้น) — REMAKE to QA_TEAM §G/§H/§I (client: "ทำใหม่", 2026-11-20)
Narration, captions, script and music C are UNCHANGED (audio/narration.wav 69.84 s at +0.10 s; g = round(t*30); N = 2095).
Sentence starts: hook 0 | pivot 6.18 | boss 16.30 | nickname 23.66 | count 28.73 | false 35.27 | crisis 42.38 | reveal 44.35 | aha 55.08 | ending 60.15.
Quote windows (mouth moves only here): coach 17.80-23.55 and 40.38-42.25.
v1 is kept in shot_plan_v1.md for reference.

## Hard rules for v2 (from QA_TEAM §G, §H, §I)
- CAMERA TRAVELS, it does not cut: 7 long takes (T1-T7), 6 joins, of which at most 4 hard cuts; the rest are push-THROUGH or dissolve transitions. A take is ONE continuous camera path, even when a team renders it in parts.
- 2 BIGZOOMs (marked): extreme wide from high and far (character < 5 % of frame height) to a medium of the character (35-60 %), 3-6 s, ease in/out, through set detail.
- Angle types used: bird's-eye/high crane, low hero, over-the-shoulder, through a foreground frame (crowd, fence, newspaper), side tracking, top-down, crane up. Never 3 shots in a row at the same height/angle.
- Colour: signature colours = 1963 GOLDEN-HOUR AMBER + school MAROON vs. deep SKY BLUE; 1968 = HOT TARTAN RED + NIGHT BLUE with white floodlight shafts. Film mean saturation >= 0.50, vivid % >= 45, luma 85-110 (film/qa_stats2.py). No peach haze.
- Light: motivated key in every shot (low sun with long shadows and god rays through pines; stadium floodlights with visible beams); rim light on characters; warm + cool in the same frame.
- Grounding: every character touches a surface with a contact shadow; nothing floats; no bar or pole through a face; no grey slabs slicing characters; airborne jumpers only over the bar/pit with a shadow on the mat/sawdust.
- Distance: >= half the screen time wide or medium-wide; at most 3 punch close-ups (~1 s each); no face taller than 35 % of the frame otherwise.
- Characters always act (rocking, stretching, chalking hands, cheering, laughing with bounce); nobody still > 1.5 s.
- Text signs ALLOWED and wanted (sharp, English, readable on a phone): MEDFORD HIGH (gym wall), TRACK & FIELD, scoreboard "HIGH JUMP", newspaper headline "FOSBURY FLOPS OVER BAR" (the real 1964 headline), stadium banners "MEXICO 68", bar-height board "2.24 m", "1972" banner in T7.
- Camera-motion targets stay: median >= 4, p90 >= 12 (film/film15/motion_check.py).

## Takes
| take | t0-t1 (s) | in | camera path (continuous) | action / beats |
|---|---|---|---|---|
| T1 | 0.00-16.30 | – | **BIGZOOM 1** 0.0-4.4: bird's-eye 120 m above the small town of Medford at golden hour (houses, streets, cars, the school, the track); descend and push through the pines and over the bleachers (MEDFORD HIGH sign) down to the high-jump pit, ending medium on Dick at his mark at 4.4. Then low hero angle as he runs the J-curve and flops over the bar (4.45-6.1). 6.2: crane UP and slide sideways along the run-up (side tracking) past the line of boys; 11.5-13.3 low angle on Dick trying the straddle, the bar falls (bar bounces in sawdust); 13.3-16.3 orbit as he turns his back and flops cleanly. | 0-2.1 a boy straddle-rolls face-down (seen small inside the BIGZOOM, then larger as we arrive); 4.45 Dick flops; 8-11 two boys straddle; 13.3 bar falls; 15 clean flop. |
| T2 | 16.30-28.73 | cut | Over-the-shoulder from behind Dick toward the bleachers, push in on the coach (laughing, belly bounce 3 Hz) 16.3-18.8; side tracking along the bleacher front as he mimes the broken neck and points (18.8-20.7); **punch CLOSE-UP 1** on "ดูเอง" (22.9-23.6, ~0.8 s); pull back to wide, a photographer's FLASH (24.6) as Dick arches over the bar; **push THROUGH the flash into the newspaper page** (25.0-26.0): a reader holds the paper, headline FOSBURY FLOPS OVER BAR with the photo of the arched Dick; camera pulls back from the paper to reveal the boys and the coach laughing and pointing (27.9-28.7). | Coach quote 17.80-23.55 (mouth only here). |
| T3 | 28.73-35.27 | push-through | **Push INTO the newspaper photo** (28.7-29.3): the photo comes alive as training; side tracking along the pit as Dick flops again and again while the peg rises; season shift via a 11-frame dissolve (leaves fall, GOLDEN to bright DAY) at ~30.3; at 31.0 the camera rises past a "MEXICO 68" poster on the gym wall and **match-dissolves into BIGZOOM 2** (31.0-35.3): bird's-eye 150 m above the floodlit Estadio at dusk (city lights, mountains, packed stands, MEXICO 68 banners, light beams), dive down through the crowd and floodlight beams to the high-jump fan, ending medium on Dick at the runway as officials raise the bar (2.24 m board) and a rival knocks it and walks off. | 32.5 bar rises; 33.8 rival fails. |
| T4 | 35.27-44.38 | cut | Low angle beside the standard looking up: Dick with the bar ~30 cm above his head (visible gap, bar-height board 2.24 m in frame) 35.3-37.5; side tracking along the bar for attempt 1 (bar falls 38.0) and attempt 2 (bar falls 39.2), Dick lands flat on the mat, hands on face; **whip pan** up into the stands to the coach (SAME maroon cap and windbreaker as 1963, among dense crowd cards) shouting 40.38-42.25 with **punch CLOSE-UP 2** on "แค่นี้แหละ" (~41.7, 0.8 s); whip back down; 42.4-44.4 the stadium hushes: floodlight beams, dimmer crowd, slow push on Dick rocking at his mark (through a foreground frame of crowd heads). | |
| T5 | 44.38-55.08 | cut | THE REVEAL, one continuous move: low side angle, the camera **rides alongside Dick** as he runs the curve and rises (44.4-46.3), slows to a near-hover and tracks laterally with him across the bar: head over 46.4, back 47.2, legs 47.8; holds a slow orbit on the arch (head and legs hanging below the bar, hard floodlight rim on his body) 47.8-50.3; 50.35 **match-dissolve** to the same framing with a rival doing the face-down straddle, his whole body lifted flat high above the bar (50.4-52.8); 52.85 dissolve back to Dick's legs flicking over, drop onto the mat (52.9-55.1). | Every body part crosses on the spoken beat. |
| T6 | 55.08-60.15 | – (continuous from T5) | Top-down crane over the mat: Dick sits up and looks at the bar, which does NOT tremble (55.1-57.4); crane UP and out as the stadium erupts (flash bulbs, cheering crowd bob) to the podium, Dick with the gold medal (58.5-59.6); **punch CLOSE-UP 3** on the coach in the stands jaw-dropping (59.6-60.1). | |
| T7 | 60.15-69.84 | dissolve (time) | Crane over a DAY stadium with a "1972" banner: three jumpers in different kits flop one after another, land smiling with thumbs up (60.2-64.6); the camera rises into the sky and **dissolves down** (sky to sky) into the Medford school track at golden hour (64.6-65.5); the coach, sighing, at the sawdust pit (boys watching from the bench); low side tracking as he runs, turns his back and flops clumsily (66.3-68.0); TUMP into the sawdust pile with a big spray (68.0), push in to medium as he sits buried to the chin with a weak thumbs-up; hard cut on the last word. | |

Joins: T1→T2 cut, T2→T3 push-through, T3→T4 cut, T4→T5 cut, T5→T6 continuous, T6→T7 dissolve. Hard cuts total: 3 (plus 2 whip pans inside T4 and the 11-frame dissolves inside T3/T5).
BIGZOOMs: 0.0-4.4 s (Medford) and 31.0-35.3 s (Mexico City stadium). Close-ups: 23.0, 41.7, 59.8.
Angle types: bird's-eye (T1, T3), low hero (T1, T4), over-the-shoulder (T2), through a foreground frame (T2 newspaper, T4 crowd heads), side tracking (T1, T3, T4, T5), top-down (T6), crane up (T6, T7).

## Render split (6 teams, as before)
- Team 1: T1 (0-16.30, 489 frames).
- Team 2: T2 (16.30-28.73, 373 frames).
- Team 3: T3 (28.73-35.27, 196 frames; contains BIGZOOM 2 — big set view).
- Team 4: T4 (35.27-44.38, 273 frames).
- Team 5: T5 + T6 (44.38-60.15, 473 frames; the reveal).
- Team 6: T7 (60.15-69.84, 291 frames).
