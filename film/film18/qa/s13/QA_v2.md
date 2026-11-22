# QA s13 (film 18, render team 4)
Range g 1003-1070, take.mkv frames 994..1076 (83 frames), transition in: dissolve.
Render: 720x1280, 12 samples, OIDN, 2 threads, 17.9 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 11.52, p90 15.37, min 2.44, max 16.36, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 758, "crowd0": 695, "crowd1": 723, "crowd2": 692, "crowd3": 615, "crowd4": 603, "crowd5": 568, "crowd6": 567, "crowd7": 575, "crowd8": 613, "crowd9": 851, "crowd10": 982, "crowd11": 722, "crowd12": 694, "crowd13": 619, "sentry": 890}

## Notes
- Round 4 rework: transition dissolve 13 in. New camera behind the camp (high, pull-out 6 %/s, slide 30 px/s) looking toward the Jimo wall: the party fills the frame, no navy brazier/drums in the lower third; gridded horizon strip is hidden behind the wall and tents.
- Party: 14 cheering soldiers with raised cups, dancers mirroring every ~0.8 s; the sentry stands near the camp fire (head ~55 px), drops a real 3D spear at g 1030 and joins in; one toon-glazed wine jar with a warm light in the lower left; grey rout scatter recoloured warm.
- Two held punch-ins (+16 %, +12 %), no pulses. Mouths do not move.

See QA_AUTO.md and phone_sheet.jpg.


## V2 (client fixes: no camera shake / nothing floats)
- Camera: NO shake, NO snaps pulsing; ONE eased dolly-in (push 18 %/s, eased) + a 30 px/s truck + one held punch-in eased over 10 frames; camera moved back/higher to start (7,-120,13.5). Crowd bounce 0.02 D at 1.8 Hz (was 0.10 D at 3 Hz).
- take.mkv crf 21, first_g 994, 83 frames; transition in: {'type': 'dissolve', 'frames': 13}.
- frame diff (90x160 grey, in-shot): median 4.4 / p90 6.73 (rule: median >= 4).
- ground_check (film/v3/tools/ground_check.py through film18/gc_run.py, every 6th frame): - checked objects: 34   rows: 429   FAIL rows: 0   **result: PASS**  (full table in GROUND.md; cards are checked by bounding box, so only a floating card base can fail; shadows are the cards' contact quads).
- qa_jitter output:
```
overall median jitter px 0.13
```
