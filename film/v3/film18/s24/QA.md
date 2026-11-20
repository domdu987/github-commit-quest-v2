# QA s24 (film 18, render team 4)
Range g 1807-1881, take.mkv frames 1801..1887 (87 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 15.5 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 8.82, p90 14.11, min 2.77, max 15.64, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"run0": 820, "run1": 837, "run2": 844, "run3": 844, "run4": 825, "run5": 845, "run6": 841, "run7": 844, "run8": 773, "run9": 843, "run10": 794, "run11": 843}

## Notes
- Rout reads: camera moved behind the camp looking at the Jimo wall (sky ~28 %), 8 fleeing / falling soldiers 15-25 D from the lens (~150 px tall), 4 flying pots/helmets (1.7x), tents folding, empty chariot rolling away in the middle ground. Bloodless, nobody hit.
- First pass had three runners leaving the frame bottom (chin > 880); re-staged (all chins <= 836) and re-rendered.
- Camera: push 5 %/s, slide 40 px/s, sway, 3 punch-ins. Mouths do not move (soldiers' open shocked mouths are held drawings).
- Deviation: camera and soldier marks replaced the set's s24 camera (QA_ART_SET_R2 instruction 10); the 30 set rout items still fly as the set builds them.
- Re-render after TAKE gate rules: pulses removed (two held punch-ins); set rout items recoloured warm flat-glazed (no grey lumps).
- Round 5: rout spread over the whole shot (rout state 0.06->0.86 linear, 6 flying items with staggered delays up to g 1860, chariot rolls over ~100 frames), runners slowed so 8 soldiers stay in frame, near-right folding tent hidden (the ghost panel), 3D items toon-glazed. Ground dressing helper (film18/main) NOT applied: set files not pulled.
- Round 6: the rout now runs the WHOLE shot: 12 soldiers in waves (frozen, then panic starts staggered to g ~1859), fallen ones sit 22 frames then get up and run again, so there is fleeing/falling until the end; 8 modelled 3D pots (body, rim, ring handles) and domed helmets with plumes (toon-glazed, 1.5x) arc through the frame in staggered flights up to g 1881; set grey rout items hidden; chariot rolls over ~100 frames; camera tilted up (ground ~30 %, sky ~28 %). dress_ground not used (not pulled).
- Heads: max chin 821 in the shot; run3 891 and run7 879 occur only near the out-handle frames (check: g > 1878).
- Round 8 (must-fix list): round-8 set/cast assets pulled from film18/main. Every chin measured on rendered frames: max 845 (rule 860) incl. handles; a clamp pushes any soldier back until its projected chin is <= 835. 12 soldiers run at 3.4-4.4 D/s in all directions, 6 fall (fall_bottom, sit, get up and run); opaque J.prop_pot / J.prop_helmet fly in 8 staggered arcs (they render blue-grey in the night shade, not terracotta); J.prop_chariot (scale 0.6) tips 0 -> 0.8 over the shot, wheel rolls away; J.gapfill lays dark earth under the visible ground. Set chariots hidden.
- Not verified: bare-ground % (not measured), tents folding (set drives it; not checked).

See QA_AUTO.md and phone_sheet.jpg.
