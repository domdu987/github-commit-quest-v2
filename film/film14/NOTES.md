# Film 14 director notes
## Series client notes from film 10 (relayed by the film 10 director, 2026-11-18; skill production-lessons §9 on claude/new-session-73ou27)
1. Dust, smoke or water plumes must NOT be a stack of round white blobs. Use a crown of spray and droplets (here: elephant dust when the herd flees, fire smoke).
2. Characters on anything that moves must be parented to it (here: the uncle on the stool, the farmer on the ladder). Add this to the QA-tech checks.
3. The blind viewer at the FINAL gate gets the narration as heard (timed text from captions.json), not an ASR transcript.
## Pending the client's decision
- push beat: replace the high push_side view with a low side view (elephant chest against the wire) plus a cut to the hives swinging along the row.
- Auto-posting step (film 10 director's message): push the release to claude/new-session-73ou27 + POST_QUEUE.md only after asking the client (that branch is outside film14/main).
## Render teams (launched 2026-11-18 13:33 UTC after the client's explicit OK "ทำเลย"), Sonnet, source film14/main
| team | takes | session | branch |
|---|---|---|---|
| 1 | s01, s07 | session_017iwyCuwrXQ5z3eCk3oY85H | render14/team1 |
| 2 | s04, s11 | session_017iwyCu4BGKMs3pF7WQ9Mrx | render14/team2 |
| 3 | s15 | session_017iwyCvfFfjuTS5ZjjvfeGn | render14/team3 |
| 4 | s20 | session_017iwyCuhPdSWFUE5zBbj5cS | render14/team4 |
| 5 | s25 | session_017iwyCti53BRy8hjVYHsKwV | render14/team5 |
| 6 | s01 redo (after TAKE gate FAIL) | session_017iwyCtekqvVfqPAq1JhmK4 | render14/team6 |
| 7 | s11 redo (after TAKE gate FAIL) | session_017iwyCweXY8bMdDFHzPwHME | render14/team7 |
## Take status
| take | status |
|---|---|
| s04 | v2 PASS (render14/team2 @7bf169b) |
| s28 | v4 PASS (render14/team2 @0446d16) |
| s01 | v5 PASS (render14/team6 @3e0e1e1) |
| s11 | v1 FAIL -> team 7 redo |
| s25 | team 5 renders died (restarted 18:45); split: team 5 = shots 25-27 (s25, g1678-1913), team 2 = shots 28-30 (new take s28, g1914-2105) |
| s15 | team 3 renders died again (restarted 19:47); split: team 3 = shots 15-17 (s15, g1001-1167), team 6 = shots 18-19 (new take s18, g1168-1306) after s01 v3 |
| s11 | team 7 renders died again (01:00); split: team 7 = shots 11-12 (s11, g753-869), team 6 = shots 13-14 (new take s13, g858-1006) |
| s19 (new) | shots 19-20 (g1220-1373) re-done as ONE take by team 2 for continuity; at conform s18 is used for shot 18 only (to g1225), s20 from shot 21 (g1368) |
