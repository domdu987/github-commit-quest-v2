# QA s01 (film 18, team 1) — hook: Tian Dan dresses the ox, dressed herd along the wall
Take: g 0-77 (78 frames), first_g 0, jimo_in NIGHT, 720x1280, 12 samples, ~16.5 s/frame (2 threads, two processes at once). transition_in: start of film.
Set/cast: set3d18 R2 + cast18 round 3 cards re-baked (dragon ox, short bronze blades). tiandan_tug_cloth card rocking at 1.6 Hz (bob/roll/lean), 7 dressed oxen with sway/bob; fg torch prop (the set's lantern bag read as a dark sack, swapped for the torch).
Camera: push 9 %/s, slide -40 px/s, 5 punch-in/out snaps (5-6 frames each) on the tug beats, hand-held sway 0.015 rad; look_at moved to (-2,12.5,3.3) so Tian Dan stays in frame to the end.
## Frame-diff (90x160 grey, consecutive frames, in-shot)
median 6.09 (>= 4 OK), p90 9.23 (target >= 12: NOT MET), min 1.25, max 10.60.
## Checks
qa_auto PASS (no black/blank/magenta/pops). Phone sheet: hook reads; heads/chin above y 880 (chin ~860 at last frame); no mouth movement; no text; contact shadows from set cards; no stump prop.
Known: p90 short of 12 (snaps top out near 10); a re-render with larger snaps is the fix if QA-tech insists.
