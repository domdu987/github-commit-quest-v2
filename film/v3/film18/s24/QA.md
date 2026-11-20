# QA s24 (film 18, render team 4)
Range g 1807-1881, take.mkv frames 1801..1887 (87 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 15.8 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 8.66, p90 12.19, min 2.77, max 14.49, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"run0": 682, "run1": 689, "run2": 818, "run3": 803, "run4": 814, "run5": 695, "run6": 748, "run7": 761}

## Notes
- Rout reads: camera moved behind the camp looking at the Jimo wall (sky ~28 %), 8 fleeing / falling soldiers 15-25 D from the lens (~150 px tall), 4 flying pots/helmets (1.7x), tents folding, empty chariot rolling away in the middle ground. Bloodless, nobody hit.
- First pass had three runners leaving the frame bottom (chin > 880); re-staged (all chins <= 836) and re-rendered.
- Camera: push 5 %/s, slide 40 px/s, sway, 3 punch-ins. Mouths do not move (soldiers' open shocked mouths are held drawings).
- Deviation: camera and soldier marks replaced the set's s24 camera (QA_ART_SET_R2 instruction 10); the 30 set rout items still fly as the set builds them.
- Re-render after TAKE gate rules: pulses removed (two held punch-ins); set rout items recoloured warm flat-glazed (no grey lumps).
- Round 5: rout spread over the whole shot (rout state 0.06->0.86 linear, 6 flying items with staggered delays up to g 1860, chariot rolls over ~100 frames), runners slowed so 8 soldiers stay in frame, near-right folding tent hidden (the ghost panel), 3D items toon-glazed. Ground dressing helper (film18/main) NOT applied: set files not pulled.

See QA_AUTO.md and phone_sheet.jpg.
