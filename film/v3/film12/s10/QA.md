# s10 QA, round 4 (rounds 3 and 2 below)
Round 4 fixes (director TAKE gate r3; re-rendered g663-713 and g786-812 only; qa_auto PASS, magenta 0.0 %):
- Cabbage leaf: lowered onto the canopy (overlaps the dome edge), tilted to the dome tangent, still follows the umbrella-middle anchor of the walking sprite every frame.
- The large soft tan ovals were the falling spray pieces (0.6 u wide, see-through while fading) and wide landing splats. Falling pieces are now narrow (0.17 u) tapered-both-ends streaks along the fall, solid until they shrink away (gone by g809, no ghost streaks); landing splats are small, opaque, confined to his body width/height.
- Near-puddle ripples: 3 impacts x 2-3 smooth soft rings, ~35 % strength, tinted to the sky reflection (150,166,222), thinning as they spread; the wheel ripple card softened the same way.

# s10 QA, round 3 (round 2 notes below)
Round 3 fixes (director TAKE gate r2; only g645-713 and g786-866 re-rendered):
- Spray falling phase: after the apex every finger breaks into 5 separate pointed streaks that fall and fade (no slabs, no rods); all spray fades smoothly to nothing by g812 (rel 27), no one-frame vanish. Rise phase keeps the passed look (heights lowered a little so the crown stays in frame).
- Mud timing: Hanway is clean through g796; mud ramps 0 -> 1 over g796-802 as brown pointed streaks fall ONTO him from a landing sprite card in front of him (splat dots where they hit); coat, face, stockings covered (cast mud fx). The crown rises from the wheel (his right) and arcs over him.
- Near foreground puddle: flat ripple card with 7 staggered expanding rings and tiny landing droplets g788-810 (fainter than first try).
- Shot 10 leaf: seated on the canopy using the umbrella canopy-middle anchor (umb_mid_r) of the walking sprite, rides with Hanway; the flight now ends on the same anchor.
- qa_auto PASS (222 frames, magenta 0.0 %); its cut flags (714, 774) are false as before.

# s10 QA, round 2 (shots 10-12, RAIN), g 645-866 (651-858 + 6 lead + 8 dissolve-out handle)
qa_auto PASS (222 frames, magenta 0.0 %, no frozen/black frames). It lists the planned cuts 714 / 774 as "no visible change": false flags (preset change; large frame differences, checked on the contact sheet).
Fixes after the director's TAKE gate r1:
- Mud (shot 12, g774-866): the set's 3D mud hook is not used. Painted spray: ~15 curved, tapered, slightly translucent fingers in 3 brown tones with a warm rim that end in pointed TEARDROPS (no round bulbs) plus streak droplets, rising from the coach's left wheel (-1.7, 12.2) through the foreground puddle and arcing over Hanway's hat around g795, falling back by ~g815; a flat ground card adds a brown wake and three expanding ripple rings (g786-815). It builds from g786 over several frames (fingers grow out of the wheel), no one-frame pop. Hanway: smug -> shocked over 5 frames (lerped arms, umbrella angle flips over those frames), cast12 `mud` fx ramps 0.15 -> 1.0 (head to toe), then the mud-spotted soaked deadpan hold g808-866. He stands ~25 % closer (-3.8, 8.7): head centre y ~372 (720x1280), face about 90+ px.
- Egg (shot 11): coachman_c visible, the painted cream egg leaves his windup hand at g723 and flies a real arc (9 frames, spinning) to the dome; the egg splat appears on the dome at g732 exactly as the egg arrives, never both.
- Cabbage (shot 10): ONE painted cabbage sprite leaves coachman_b's windup hand at g654, 9-frame arc, hits at g663; the same green big leaf then sits on the dome (and rides with Hanway). No second cabbage, no bounce, sprite leaf_stick removed.
- Mouths: all coachmen in s10 have CLOSED mouths (frown scowl while throwing, smirk afterwards); crowd jeerers smirk; nobody speaks.
- Coach rule: nobody rides the charging coach, nothing to parent.
- Heads all above y 880 (Hanway 372-700 centre). Light RAIN, Hanway coat / umbrella consistent with s13.
- Known weak points (non-blocking): spray is flat 2D against the 3D coach; the dome leaf is a flat ellipse; thrower cards stand close to the rank.
