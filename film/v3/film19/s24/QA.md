# s24 QA: film 19, shot 24 (HALL EVENING)
- take.mkv: g 1924..2036 (113 frames), shot g 1933..2027; transition in: cut.
- King19 compares the pocket watch with the H4 (hands alternate, squint); ten candle stubs appear left to right along the table edge (set_stubs 0->10); snap on 'สิบสัปดาห์' (g 2006). Known: the King is small (head 78->~170 px) at the far end; camera path chosen to avoid the candelabra (a candle passing the lens whites out the frame).
- Rules: no DOF, no text, no caption_shade; all hooks keyed every frame; samples 8; heads (in shot, px): {"king": {"w": [80, 150], "y": [565, 614], "x": [322, 575], "bottom_max": 656}}
- Mouths: only the jaw drop in s25 (held), nobody talks.
- qa_auto: PASS (see QA_AUTO.md, phone_sheet.jpg). Checked contact sheet at full size.
- s/frame wall 15.7 (2 procs x 2 threads), cpu 30.81.
- Frame-diff in shot (90x160 grey): median 4.06, p90 15.07 (target 4 / 12).
