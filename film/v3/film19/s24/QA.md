# s24 QA: film 19, shot 24 (HALL EVENING), after the QA-art / QA-tech fix round
- take.mkv: g 1924..2036 (113 frames), shot g 1933..2027; transition in: cut.
- King19 compares the pocket watch with the H4 (both watches 1.5x, at face height, hands alternate, squint); the ten candle stubs (moved in front of the King) appear left to right and reach 10 by the snap word 'สิบสัปดาห์' (g 2006); snap there; the last frames show the King and the stub row, no blown candle. King head 115-250 px. Frame-diff median 3.95 is just under the 4 target, p90 9.96 (under 12).
- Rules: no DOF, no text, no caption_shade; set hooks keyed every frame; samples 8; heads in shot (px): {"king": {"w": [117, 217], "y": [559, 624], "x": [378, 621], "bottom_max": 694}}
- qa_auto: see QA_AUTO.md + phone_sheet.jpg. Contact sheet checked at full size.
- s/frame wall 29.83 (2 procs x 2 threads, some frames rendered while a second job ran), cpu 32.44.
- Frame-diff in shot (90x160 grey): median 3.95, p90 9.96 (target 4 / 12).
