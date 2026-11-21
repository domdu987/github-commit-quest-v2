# s16 QA: film 23, shot S16 (RHINE NIGHT_R)

## Delivered
`take.mkv` (libx264rgb crf 6, 30 fps, 720x1280, 125 frames g 1728..) see meta.json mkv_parts. Also `shot.py` (stills / final / ground), shared `../c23.py` `../deliver.py` `../qa_md.py`, `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md`, `QA_JITTER.txt`, `GROUND.md`, `numbers.json`. Frames / raw / work stay out of git.

## Clock (ESTIMATED timing: timing_EST.json + plan table)
- g0 1728, g1 1827 (planned, round(t*30)), g1_render 1852 (planned + 25 % tail: the move and the action continue, eased), first_g 1728 (in-handle 0), n_frames 125.
- transition_in: cut 0 frames (plan).

## Automatic QA
- `qa_auto.py`: QA_AUTO PASS  (take.mkv, 125 frames, 30.00 fps, g 1728-1852)
- `qa_jitter.py` (every second must be <= 2.0 px; no line = clean): ```overall median jitter px 0.26```
- ground_check (`--every 10` equivalent on the built scene, GROUND.md): checked objects: 155   rows: 2170   FAIL rows: 0   **result: PASS**
- frame-diff (90x160 grey, body frames): median 1.56, p90 1.93, min 0.79 (rhythm target median >= 4, p90 >= 12) -- BELOW target: dark, low-contrast night frames with the set's own slow eased camera; the camera never shakes and no frame is static (qa_auto: no frozen runs)
- luma (mean of RGB, every 5th frame): 75.7 .. 78.4 (mean 76.8)
- shade hue (target 240-260; first / mid / last): g1728 233.7, g1790 228.6, g1852 228.5 (night exterior: the director accepted shade hue 227-234 for RHINE in QA_ART_SET.md)
- heads: max head-centre y 794.6 px over the whole take (caption band starts y 880; head radius at most ~30 px): sound 705, radio 795, carry 766
- render: 720x1280, 12 samples, OIDN, 17.15 s/frame wall (19.34 s CPU), 2 threads while a second render ran.

## Look checks (contact.jpg at 6 fps, phone_sheet.jpg)
- Push along the sound truck (record spinning at 78 rpm via set_record keyed every frame), the horn; 30th / 79th INF DIV crates, a rope coil and a lantern in the foreground. Exposure lifted +0.6 EV over the set so luma stays >= 70 (QA_ART_SET director acceptance note); see the luma line.
- Cast: the sound man (gi_sound, point at the horn with a small sway), the radio man seated on a crate with the handset (held `talk_a` mouth drawing, no mouth movement), a carrier walking in with a crate. The radio man and the carrier were moved from their marks (they stood behind the truck at 55-65 D and could not be seen) to feet-on-ground spots chosen from the mid-frame camera rays (c23.ground_at_screen).

## Rules
- No mouth moves: the radio man's `talk_a` is a single held drawing. No weapons. No camera shake. No depth of field.
- Ground check PASS.

## Deviations from the plan / set
- Exposure +0.6 EV; radio man / carrier re-placed; the radio tent stays behind the truck (not visible).
- Frame-diff is below target for the same reason (night, slow push 0.07).
