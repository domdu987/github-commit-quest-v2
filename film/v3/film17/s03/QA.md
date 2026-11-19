# film17 s03 (shots 7-8, g 336..445, frames g 330..450, 121)
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg); magenta 0 %. Planned cut g 390 flagged "no change within +-2" only because the metric is coarse: contact.jpg shows aisle -> desk.
- rhythm.py take.mkv --first_g 330 --cuts 390: in-shot median 5.50, p90 12.93 (pass: >=4 / >=12). One snap per shot (shot 7 g364-376 pan/dolly, shot 8 g418-431 push toward the clerk) on top of the drift.
- Heads (from render json): centre y 540-700, max chin 734 (< 880); all in frame.
- Shot 7: records_aisle high, pull-out + slide, spilled card piles and card stacks (runtime dressing), two figures lost in the canyon (bertillon aisle1, prisoner_a aisle_far; no spare clerk card). During the snap the preset's gas bracket (fg) swings close and blooms white.
- Shot 8: records_desk insert, custom camera; two drawn photo cards (same face, right one with a big moustache, no text) leaning on the desk; Bertillon scratches his head (cast has no separate clerk). Moustache card is partly cut at the left edge by g 440+.
- No mouths move (no quote window). 12 samples + OIDN, 720x1280, ~75 s/frame (2 procs x 2 threads).
