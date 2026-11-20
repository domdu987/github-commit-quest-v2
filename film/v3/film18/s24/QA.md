# QA s24 (film 18, render team 4)
Range g 1807-1881, take.mkv frames 1801..1887 (87 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 16.5 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 8.61, p90 12.09, min 2.2, max 14.56, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"run0": 684, "run1": 700, "run2": 896, "run3": 800, "run4": 798, "run5": 693, "run6": 737, "run7": 761}

## Notes
- Rout reads: camera moved behind the camp looking at the Jimo wall (sky ~28 %), 8 fleeing / falling soldiers 15-25 D from the lens (~150 px tall), 4 flying pots/helmets (1.7x), tents folding, empty chariot rolling away in the middle ground. Bloodless, nobody hit.
- First pass had three runners leaving the frame bottom (chin > 880); re-staged (all chins <= 836) and re-rendered.
- Camera: push 5 %/s, slide 40 px/s, sway, 3 punch-ins. Mouths do not move (soldiers' open shocked mouths are held drawings).
- Deviation: camera and soldier marks replaced the set's s24 camera (QA_ART_SET_R2 instruction 10); the 30 set rout items still fly as the set builds them.
- Re-render after TAKE gate rules: pulses removed (two held punch-ins); set rout items recoloured warm flat-glazed (no grey lumps).

See QA_AUTO.md and phone_sheet.jpg.
