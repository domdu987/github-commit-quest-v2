# QA s08 (film 17, shots 20-21: the false payoff), g 1039-1201 (163 frames incl. 6 handle frames each side)
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg). Note "cut 1127 no visible change" is a false alarm: the cut is detected by rhythm.py (diff 22) and visible on the contact sheet.
- Rhythm (rhythm.py, --first_g 1039 --cuts 1127): **in-shot median 5.93, p90 12.20** (targets >= 4 / >= 12).
- Shot 20 g 1039-1126 records_desk EVENING_INT: Bertillon tired at the desk, shaking his head, flipping two cards (no match), drawers creeping further out, candle flicker rising. Camera: pull-out + slide, whip sweep (1062-1075), push-in snap (1098-1111).
- Shot 21 g 1127-1201 records_aisle EVENING_INT: inspector (centre) shouting with cupped hand, lip-sync ONLY g 1128-1195 (narration 37.48-39.74 +0.10 s); gendarmes snicker (3 Hz bounce, laughing face, mouth held closed via silent()), Bertillon slumped at left. Snaps at 1148-1161 and 1180-1193.
- Director fixes applied: beam_fx shafts hidden, dust k 0.5, every non-quote pose wrapped in cast17.silent().
- Heads: all Bertillon/inspector/gendarme_a heads centre y 590-770, chins above 880 (first pass broke this at g 1188-1201; re-framed and re-rendered g 1181-1201). gendarme_b (background) head centre y 520-630.
- Checked: draft contact sheet + final contact sheet (every 9th frame), head report json for every frame, mouth rule by code (speak only g 1128-1195).
- Known weaknesses (honest): characters keep fixed stand points (no entrance walk; the inspector is animated only in place: bounce, cupped hand, lip-sync); the "doorway" is the aisle end with the barred window; no dedicated per-frame 6 fps eyeball pass of every frame beyond the sheets.
