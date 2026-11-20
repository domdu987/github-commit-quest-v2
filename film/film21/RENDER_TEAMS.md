# Film 21 render teams (Sonnet cloud sessions, source film21/main, clone_depth 1, outcome branch render21/teamK)
Plan v3 (QA_TEAM.md §I camera travel), 2026-11-20. Wave 1 (11:40) and wave 2 (12:23) of plan v2 were HELD at 12:50 for §I. The same sessions get new segment assignments below.
Folder per segment: film/v3/film21/s<SEG> (sA, sB1, ...). meta.json: g0, g1, first_g, n_frames, transition_in = {"type":"cut","frames":0} for CUT or W (whips are rendered inside the segments), {"type":"dissolve","frames":6} for D6.
Handles: 3 frames past each D6 end (same move continued). No handles on cuts or whips.
| seg | g0-g1 | in | team | branch | session |
|---|---|---|---|---|---|
| A (BIGZOOM 1, hook) | 0-159 | - | 1 | render21/team1 | session_017iwyCumuEopk7yR2v7VxqP |
| B1 | 159-298 | CUT | 2 | render21/team2 | session_017iwyCueDsicSa1SXow5PeY |
| B2 | 298-418 | D6 | 5 | render21/team5 | session_017iwyCtbZ82yNcWWj7WiwA5 |
| C | 418-542 | CUT | 3 | render21/team3 | session_017iwyCws18qdxaGzgzAeH6X |
| D1 | 542-642 | CUT | 7 | render21/team7 | session_017iwyCvpzoi5TiBV4qevt9n |
| D2 (mocker) | 642-793 | W | 4 | render21/team4 | session_017iwyCucf86ZM8VKRSnau3L |
| E1 | 793-885 | D6 | 5 | render21/team5 | session_017iwyCtbZ82yNcWWj7WiwA5 |
| E2 (count) | 885-1044 | CUT | 6 | render21/team6 | session_017iwyCui16dpW5GJ7yrC9Se |
| F (false payoff) | 1044-1141 | CUT | 7 | render21/team7 | session_017iwyCvpzoi5TiBV4qevt9n |
| G1 | 1141-1194 | W | 3 | render21/team3 | session_017iwyCws18qdxaGzgzAeH6X |
| G2 (horn) | 1194-1239 | CUT | 8 | render21/team8 | session_017iwyCtvGWYHcEnV2cnVAxQ |
| H1 (charge) | 1239-1345 | CUT | 8 | render21/team8 | session_017iwyCtvGWYHcEnV2cnVAxQ |
| H2 (BIGZOOM 2, reveal) | 1345-1519 | D6 | 9 | render21/team9 | session_017iwyCtjzchAetQUqefvg7M |
| I (aha) | 1519-1640 | CUT | 10 | render21/team10 | session_017iwyCx6gATy4vJU2YUfeBA |
| J1 (ending table) | 1640-1709 | CUT | 11 | render21/team11 | session_017iwyCsYUJ5ivPtdLSfSaHu |
| J2 (ending splash) | 1709-1848 | W | 11 | render21/team11 | session_017iwyCsYUJ5ivPtdLSfSaHu |
Key segments for QA-art at the TAKE gate: A, D2, F, H1, H2, J2.
D6 joins: B1->B2 at P_CAMP (g298), D2->E1 at P_BANK (g793), H1->H2 at P_NECK (g1345). Neighbouring teams: match the pose in shot_plan.md exactly.
