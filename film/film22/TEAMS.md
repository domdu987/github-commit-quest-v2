# Film 22 render teams (Sonnet, outcome_branch render22/teamK, source film22/main)
Brief: film/WORKER22.md. Gate notes: v3/set3d22/SET_GATE.md (QA-art PASS, 27 mandatory items), v3/set3d22/QA_TECH.md Round 1 + Round 2 (QA-tech PASS; TAKE items mandatory).

Cross-team join items (both teams make their side match; the director checks at conform):
- J1 s01 end -> s02 start (team 1 / team 2): the same window view; s01 end key stops ~0.3 D before the pane.
- J2 s02 end -> s03 start (team 2 / team 4): the SAME iron grille. Team 4 replaces the old pill-tile plate at the s03 shaft top at runtime with the bar+rivet grate geometry of beck_london (see API.md grate layout), warm planes and lamps below; team 2 raises its end key about 1.5 D so lamp depth shows. If they still differ, conform uses a 6-frame dissolve.
- J3 s03 end -> s04 start (team 4 / team 1): the OLD map tint must match: team 4 multiplies the platform old-map material toward the lodgings' lilac-grey (compare its last frame with team 1's s04 first frame from the contact tiles contact/s04_start.png), and frames the map large (≥ 12 % width, title not cut); team 1 starts s04 about 25 % closer on the map. Conform: 9-frame eased match dissolve.
- J4 s04 end -> s05 start (team 1 internal): one continuous move.
- J5 s06 end -> s07 start (team 3 internal): one continuous move; same expressions.
- J6 s10 end -> s11 start (team 4 / team 5): travel through the train door; team 5 starts from the door view of the train interior.
- J7 s11 end -> s12 start (team 5 internal): the push into the pocket-map paper lands on the mapworld paper with the same line layout.
- s14 end -> s15 start (team 5 / team 2): match dissolve from a high, glowing London diagram to the high night city.

| team | branch | takes | location | key takes (QA-art TAKE gate) |
|---|---|---|---|---|
| 1 | render22/team1 | s01, s04, s05 | hq lodgings NIGHT | s01 (hook) |
| 2 | render22/team2 | s02, s15 | london DUSK/NIGHT (+ publicity window/interior) | s02, s15 (BIGZOOMs, ending) |
| 3 | render22/team3 | s06, s07, s08 | publicity + corridor; Q1 lip-sync in s06 | s06 |
| 4 | render22/team4 | s03, s09, s10 | under: shaft, tunnels, platform, ticket hall; Q2 lip-sync in s09 | s03, s10 |
| 5 | render22/team5 | s11, s12, s13, s14 | carriage, mapworld, ticket hall | s11, s12 |
