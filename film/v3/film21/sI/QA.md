# QA — film21 segment I (the AHA, bridge jam)

take.mkv: g 1519-1639 (121 frames @30 fps, 4.03 s), 720x1280, 32 samples, ~55 s/frame. Cut in, no handles.
World: build_world(['bridge_deck','bridge_high']) flown with cam_path (deck ride -> crane up -> snap pull-out at local f89 = "เหมือนกัน").

## Automated
- qa_auto.py: PASS (QA_AUTO.md, phone_sheet.jpg)
- rhythm.py: 0 cuts, in-shot frame-diff median 8.93, p90 31.86 (needs >=4 / >=12) OK
- qa_stats.py: saturation 0.637, brightness 104.3 OK
- qa_stats2.py: vivid 69.6 %, still 0.0 % OK

## Action (viewed on phone sheet / contact.jpg)
- Column tries to turn back (horses yaw, hop), two riders wedge nose to tail, one helmet pops off (bloodless, comic; bare-headed knight shown after f62).
- Crane shows two-by-two column along the whole bridge, nobody moving; snap pull-out on "เหมือนกัน".
- Rim light on all cards; English crimson/gold. Mouths closed; no text beyond set signs; no DOF/haze.

## Known weaknesses
- Far terrain in the crane shots is very yellow/saturated (within QA limits).
- Hero horses read small side-on in the crane view (billboard cards).
- ~30 % of frame in the ride shots is dark water.
- path_draft.mp4 = 10 fps 360x640 draft of the final camera path.
