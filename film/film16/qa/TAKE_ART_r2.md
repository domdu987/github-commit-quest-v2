# Film 16 — QA-art, TAKE gate round 2 (key shots after fixes)
Reviewer: QA-art (opus). Date 2026-11-19. Frames: 4 fps (s30 3 fps), judged at full size (720x1280) and as 360x640 phone grids.
Rules: film/QA_TEAM.md QA-art + §C, production-lessons §2 and §10, film/film16/shot_plan.md. Round 1: film/film16/qa/TAKE_ART.md.
Sources: s02, s03 render16/team1 @587ab2e; s15 render16/team4 @3b883c4; s16, s17, s18 render16/team5 @4a9a8c6; s30 render16/team8 @3ffa8d4 (one take.mkv, not split).
Skipped (still being re-rendered): s01, s10-s11, s22-s24.

Scores 1-10: D = density/ornament, L = light/colour, C = composition (incl. phone), A = acting, K = key-moment clarity. Round-1 scores in brackets.

| Take | D | L | C | A | K | Verdict |
|---|---|---|---|---|---|---|
| s02 poles + Morse | 6 (5) | 7 | 7 (5) | 6 | 7 (6) | PASS (notes) |
| s03 train + promise | 6 | 8 | 6 | 7 | 7 | PASS (notes) |
| s15 silent key | 6 (6) | 6 | 6 (5) | 6 (5) | 6 (4) | FIX (small) |
| s16 broken pipe | 5 (4) | 7 (6) | 7 (6) | – | 8 (5) | PASS (notes) |
| s17 empty bag | 6 | 7 | 6 | 6 | 4 (4) | FIX |
| s18 mocker's taunt | 5 (6) | 8 | 5 (4) | 7 (6) | 6 (4) | FIX |
| s30 ending | 7 | 7 (6) | 7 (5) | 7 | 6 (5) | FIX (small) |

All takes are still sharp, without DOF and without text in the picture. Every take keeps moving.

## Story beats on a phone (360x640)
- Train + promise (s02-s03): YES. In s02 the hero bottle cap is now big and glints, the row of capped poles shows behind him at the start, and Morse is medium and proud. In s03 the train, the grin and the point all read.
- Silent key (s15): MOSTLY. The key, the register and the crew behind the crate all read. The press itself is small, because the hand is about 12 px on a phone behind the register. The end close (worried face over the key knob) reads as "nothing happened". The knob there is not under his hand.
- Broken pipe leaking electricity (s16): YES. Cyan-white zigzag bolts crackle out of the torn wrap into the soil. It now reads as current, not water. The wire is now copper.
- Empty bag (s17): NO. The new prop reads as a cream jar or urn with two white handles (the turned-out linings look like ears or handles). Nothing falls out, Morse does not look at it, and it hangs at hip height at the frame edge.
- Mocker's taunt from the buggy (s18): PARTLY. The opening wide shows mocker, buggy and mule (good). After the reframe the buggy becomes flat green and purple slabs, he seems to stand in a box with his legs mid-stride, and he points down at nothing. The furrow, the line and Morse are never in the medium. The laughing, tears, belly bounce and lip-sync read well.
- Ending (s30): MOSTLY. The mocker yawns with Z, holds a candle and has the sash, at a medium size (head about 170 px). Morse grins in the doorway at the left edge, which reads at full size but his head is about 30 px on a phone. The register is still on the far table behind him, not beside him, and the tape heap reads as broken wooden slats.

## Per take

### s02 poles + Morse — PASS (notes)
Fixed: medium Morse (head 160-270 px), a hero bottle cap of about 150 px that glints at the top, the capped-pole row marching to the left at f002, and FG props in the lower third.
Notes (non-blocking):
1. The big FG spool dome in the lower left is a flat orange disc without texture, and on a phone it reads as a cushion or bread blob. Give it wood-grain staves and an iron band, or swap it for a crate of green bottles (which also seeds s22).
2. He points to screen right, toward the fence and his own ladder, while the pole row recedes to screen left behind him. Flip the point or the camera axis so arm and eye-line run along the capped row.
3. The hero bottle exits the top of the frame from about f005 on. Ease the crane-down so the glinting cap stays in frame until the cut.

### s03 train + promise — PASS (notes)
The eye-line to the train is fixed, and his eyes look screen right at the loco. Remaining notes from round 1: the pole still touches the right edge of his hair in f003-f006 (slide about 40 px), and the wire is still not in reach, so there is no tap. Neither blocks.

### s15 silent key — FIX (small)
Big improvement: the key, the register and the crew behind the crate tell the setup. The dusk dip and worried close land.
Fixes:
1. Make the press readable. In the middle part, frame so the hand on the knob is clear of the register drum (raise the camera or move Morse to the key side the camera sees). In the end close, keep his hand on the knob, pressing once more inside the close. Right now the knob is in the FG with no hand, so the silence has no cause on screen.
2. Eye-lines: Cornell and the workers still look at the camera with arms crossed. Turn heads and eyes to the register and lean them in 0.1 D. Swap the arms-crossed pose for a bent-forward "waiting" one.
3. The register reads as abstract blue blocks (a blue drum and a blue bar). Give it the period look: brass and wood, a white paper tape strip hanging out still, and a warm lantern on the crate for one warm pool in the green-violet dusk.

### s16 broken pipe — PASS (notes)
Fixed: electric crackle, copper wire, a faster dive. The mechanism reads on a phone.
Notes:
1. The bolts do not light anything, and the soil below stays a flat brown with a soft white hotspot (the lower 30-35 % is empty). Add blue emissive pools where each bolt bites the soil, and kill the white hotspot.
2. Put damp detail in that band (dark wet patches, roots, pebbles).
3. f000 is still a flat orange ground plane. Start the dive one or two frames later, or texture the plane.

### s17 empty bag — FIX
The beat still does not read. On a phone the new sack is a cream jar with two handles.
Fixes:
1. A money bag that is visibly EMPTY. Use the s12 money-bag prop (same colour and shape, so it is a callback). Morse holds it by the bottom, mouth DOWN, at chest height near frame centre, and shakes it. A puff of dust and one moth (or a single button) falls out, and the limp lining flaps out of the mouth. Drop the side "ear" linings.
2. Acting and eye-line: Morse looks INTO or down at the bag (gaze at the bag, not the camera), hopeful at the first shake and slumped at the second. Keep the bag fully inside the frame for the whole shot. It is clipped at the right edge in f004-f006 now.
3. Workers react: on the shake both visibly slump onto their shovel handles (dip 0.1 D, heads drop). They are now stiff, and the right one has arms crossed.

### s18 mocker's taunt — FIX
Better: the mocker is medium during the whole lip-sync, laughing, with tears and a belly bounce, and the mule reads in the opening wide.
Fixes:
1. Make the buggy read in the medium. The camera now sits inside the buggy box: a huge untextured green slab in the lower 40 %, purple and brown slabs, and his legs mid-stride. Put the camera low OUTSIDE the buggy side, with a red wheel and the textured side panel as FG, and seat him (or have him half rise with one hand on the rail) so the legs are not seen walking in a box.
2. Give the point a target. In the medium the furrow or trench (and ideally the line of bare poles, or a small Morse group at the trench end) must be in the background on the side he points to. Turn his head and eyes partly toward it on "ใต้ดินแล้ว", then back to the laugh. Right now he points down at an empty purple floor.
3. Opening wide (about 1.1 s): the mocker sits at the far left edge with his head about 68 px, half cut, behind FG grass. Slide so he is left of centre with clear air round him, and thin the grass in front. Or shorten the wide to about 0.6 s before the reframe.

### s30 ending — FIX (small)
Better: the medium end frame (mocker head about 170 px), the hat restored, the candle in hand, the Z, the yawn, Morse visible in the doorway, and the floor loops that read as rails are gone.
Fixes:
1. Tie him to the register. The register (the green and orange drums) is still on the far table to the right and behind. Put a small table or stool with the register at his elbow, on his depth, and run one continuous white paper ribbon from it down into the heap round his boots. Make the heap narrow, curled white paper with dot-dash marks, not the current flat tan slats that read as broken wood. Remove the big gold sack in the FG centre: on a phone it is a gourd or loaf, and it covers the heap.
2. Night contrast: the top 30 % is evenly lit ceiling beams and the doorway is the brightest area at an equal level. Darken the ceiling and walls about 40 % more. Raise the candle to chest height so a warm pool lights his yawning face and the register. Keep the windows deep blue.
3. Morse in the doorway: bring him 0.5-1 D into the door opening, away from the left frame edge, head 80-90 px at 720 (about 40+ px on a phone), backlit by the warm door with a bigger grin. He should be the last thing the eye finds at the hard cut on "เอง".

## Summary
PASS: s02 (notes), s03 (notes), s16 (notes).
FIX: s17 (beat still unreadable, top priority), s18 (buggy and pointing target), s15 (small: visible press, eye-lines, register look), s30 (small: register beside him, tape, night contrast, Morse bigger).
For the blind-viewer test: s16 now carries the mechanism. "Who mocks whom" (s18) and "why the ending is funny" (s30) are close but not there yet.
