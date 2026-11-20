# s16 QA (round 2): film 19, shot 16 (SHIP ship_deck NOON)

## Delivered
- `take.mkv` (libx264rgb crf 6, 34.5 MB): g 1181..1288 = 108 frames, first_g 1181. Shot 16 = g 1190..1279; handle in g 1181..1189 (CUT in), out g 1280..1288. 720x1280, 11 spp. `qa_auto` PASS. meta.json, cues.json, contact.jpg, phone_sheet.jpg, framediff.json.

## Round-2 fixes (director review)
- **H4:** prop scale 2.0 (about 0.48 D, ~55 px at the start, ~110-130 px at the end), held centred at chest height in front of William (hand at chest, yaw toward the lens); tick marks and hands read from g ~1215.
- **Snap:** x1.6 (a tilt down from the sails onto the pair, 20 f, g 1212..1232) with the captain staged close beside William (mark offset +1.5 / +1.1 D) so both stay in frame: William right edge <= 660, captain left edge >= 0 for the whole shot (captain 299 px wide at the very end).
- **Sun continuity:** `set_sun_overhead(1)` on every frame (as at the end of s15); the camera starts from the framing s15 ends on (same rest-frame pose at g 1190, pulled back x1.8), so the sail shadow is the same short noon pattern, the deck is mostly lit.
- Ship ride as s15.

## Checks
- Heads in shot: centre y 418-765, width 112-299 px, bottom max 825 (the start frames, head at y ~760 before the tilt); heads end above y 440-460 after the tilt. No DOF, no text, no caption_shade; mouths still.
- Frame-diff: **median 4.60, p90 12.89**. s/frame 21 wall / 41 cpu.
- Known: the captain looks larger than William at the end (he is a little nearer the lens); the watch is held in front of William's chest rather than centred on the screen axis (the pair is centred).

## Round 3: colour re-render (QA_TEAM §G; set fix ff204d3 merged: ship NOON exposure -0.3, grade sat 1.18)
Re-rendered unchanged shot code on the new set. `film/qa_stats.py take.mkv`: saturation 0.458, brightness 127.3 (in-shot motion median 4.98 p90 11.92). Frame-diff (deliver.py, in-shot): 4.11 / 11.52.
