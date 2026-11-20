# Film 20 render teams (Sonnet cloud sessions, source film20/main, outcome render20/teamK)
| Team | Shots (one take each) | Location |
|---|---|---|
| s01 | 1 (worked example) | TOWER tower_low, DAY 1889 (hook) |
| team1 | 15, 23 | TOWER tower_fair (1889 permit, 1910 extension) |
| team2 | 2, 24, 25 | RESTO (hook eat, ending enter, eat) |
| team3 | 26, 27 | RESTO resto_view + TOWER tower_window_pull (last image) |
| team4 | 3, 4, 5 | SITE wide / table / leg_low (stage 0) |
| team5 | 11, 12, 13, 14 | SITE fence (nickname), girders, rivet, rise (stages 1-3 snaps) |
| team6 | 6, 7, 8 | CAFE wide / table insert / window (stub view, smoke) |
| team7 | 9, 10, 16, 17 | CAFE Maupassant (low / low_close; lip-sync quotes; stub then full view) |
| team8 | 18, 19, 20 | TOWER dusk 1909 (wagon, summit wire whip-tilt, hut spark) |
| team9 | 21, 22 | TOWER night (signal rings), dusk/night aha |

## Director notes per team (from the SET gate; also read set3d20/QA_ART.md + QA_TECH.md "notes for render workers")
- team3 / shot 27 (tower_window_pull): at the start pose the window's X-brace crosses Maupassant's face. Offset the camera (or the start look-at) so he sits clear in one quarter of the X (head >= 40 px, nothing over his face), already moving on frame 0; the crash pull-out then reveals the whole tower (T13 framing). Last 12 frames near still.
- team8 / shots 18-19, team9 / shot 22: use camera tower_dusk_chars (T14) for character beats; the board camera puts heads at y 1200.
- team4 / shot 4 site_table: lower the camera, tilt up ~8 deg so leg + scaffold fill the background. Shot 5 site_leg_low: the tilt-up must end at >= 35 % sky.
- team5 / shot 12 site_girders: camera ~1.0 m high, 2-3 m from the pile; frame out bare ground and any dark box.
- team6 / shot 8 cafe_window: move the artist card ~0.5 D so it does not cover the window; smoke 1.0 on "ปล่องโรงงานสีดำ".
- team9 / shot 21: hold the summit start <= 4 frames before the whip pull-out.
- all CAFE shots: keep the checker floor <= 25 % of the frame. Hut (shot 20): check a 360x640 draft strip for plank shimmer while moving.

## Sessions (launched 2026-11-20 09:58 UTC, claude-sonnet-5-5, source film20/main, outcome render20/teamK)
team1 session_017iwyCtBTXZTXrX2LuZMoVQ | team2 session_017iwyCwXPB9F594dd5BvZBL | team3 session_017iwyCwUvMJVnTUwHpGzRwf
team4 session_017iwyCts7F4GoxGxK4cYZT3 | team5 session_017iwyCsuowzvp1zKchKgP4a | team6 session_017iwyCwmYUF3MQX3kqxy9YG
team7 session_017iwyCuDik3vbdfHWshYiW4 | team8 session_017iwyCwBY532MzoskoffqzP | team9 session_017iwyCsmmkdTRxH31aAqzUF
s01 worked example: director's local Opus agent (film/v3/film20/s01).
