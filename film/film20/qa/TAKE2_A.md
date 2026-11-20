# TAKE gate round 2, QA-tech A, film 20: s02 s03 s06 s11 s15
Method: ffmpeg frames (g = first_g + index), qa_auto.py + qa_stats2.py, own frame-diff (90x160 grey, in-shot), viewed 6 fps + g0/g1 +-3 + beat times.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeqa2/

| take | sat | vivid % | luma | diff med / p90 | auto | verdict |
|---|---|---|---|---|---|---|
| s02 | 0.638 | 60.3 | 88.6 | 6.42 / 12.67 | FAIL (blur g147-164, whip) | FAIL |
| s03 | 0.500 | 55.0 | 96.3 | 8.12 / 14.64 | PASS | FAIL |
| s06 | 0.545 | 47.2 | 110.4 (limit 110) | 15.09 / 26.25 | PASS | FAIL |
| s11 | 0.556 | 65.7 | 100.8 | 5.67 / 21.79 | PASS | FAIL |
| s15 | 0.587 | 48.6 | 84.3 (limit 85) | 7.58 / 11.81 | FAIL (soft g1077+, push) | FAIL |

## s02 FAIL
1. g146-168 (22 frames): the waiter card is shoved into the lens during the pull-out and fills the whole frame (torso 100 % wide, face 40 %+ cut by the top edge); Maupassant is hidden. Whip streak is 8+ frames (diff >15 on g141-148), not <= 3. Fix: route the pull-out past/around the waiter (move him to a side), shorten the whip to <= 3 frames.
2. g148-160: the waiter's mouth is open (O shape) while nobody speaks. Fix: closed mouth.
3. g80-140: napkin tucked in the collar is not visible (plan beat); only a fork. Fix: napkin card on the collar, visible.
4. g172-185 (end pose): Maupassant tiny (head ~50 px), floor ~35 % + ceiling beam ~15 % of frame (> 25 %), mouth/moustache distorted into a dark frown; end hold is not the planned "happy eater". Fix: keep him 80+ px, tilt up, happy face.
5. g76-140: Maupassant face ~ 26 % of frame height (ok); heads < 880 ok; no cut inside; handles 4 in / 8 out ok; sat/luma pass.

## s03 FAIL
1. BIGZOOM 1 fails the spec: Eiffel is < 5 % only for g178-~210 and reaches 35 % of frame height at ~g250: the continuous in-move is 2.4 s (needs 3-6 s). Start frame is not an extreme wide of Paris: one scaffold leg fills the left, no Seine, flat white block buildings, 31 % empty sand at the bottom; Eiffel (table) is a ~15 px speck. Fix: start higher/further (4 legs, Seine, Trocadero in frame), land medium at ~g300 (4.0 s move).
2. g178-200 ground 31-55 % empty sand; g215-300 a beige wall slab fills 35-45 % of the frame, noisy texture; g240-268 black/blue blueprint table boxes fill bottom 25 %. Fix: lower the camera/tilt up, move the slab out, dress the table.
3. g300-308: Eiffel leaves frame right and is cut by the edge (g300-304 face half out) while a giant diagonal brown pole sweeps across the frame. Fix: keep him in frame until the crane-up starts, drop/shift the pole.
4. g318-372: leg geometry looks broken (bowed banana-shaped leg with detached beams at g360-372), camera rolled ~15 deg; leg reads as orange timber, not the Eiffel iron lattice. Fix: use the correct leg mesh/stage and level the roll.
5. g340-411: riveters are 40-60 px and only 3 at the very end (g390-411); the plan's "riveters on the scaffold" is barely there. Fix: more workers on the platforms in view during the crane-up.
6. g268 beat: arm only starts rising at g268 and is fully up g275 (ok). Frame-diff ok (8.12 / 14.64); frozen-ish g261-268, g274-282 (diff < 1.5, only squash): add secondary motion. Sat 0.500 is exactly at the limit.
7. Handles 8 in / 8 out ok; heads < 880 ok; no text.

## s06 FAIL
1. g437-480 and g452-470: the top-hat artist at the left is half cut by the frame edge (face half out), the brown-haired artist cut at the edge g452-470; large newspapers cover faces (g452-460, g471-480). Fix: re-aim so the group stays whole, shrink/raise the papers.
2. g590-607 (ending): ceiling ~35 % + floor ~30 % of the frame (> 25 %), blown-out white glare patch bottom-left, Maupassant only ~45 px head sitting low centre; the end is not a match framing for T09 (he should be clear, ~100 px). Fix: tilt down to ceiling <= 15 %, push in to the banquette, kill the glare.
3. g508-551: continuous diff 20-40 (44 frames of fast sweep); median 15 / p90 26 is far above target and risks motion blur; the sweep is also a roll/whip while the purple artist's face is 30-35 % of the frame (g525-545). Fix: calm the rise to ~15-20 and keep faces < 35 %.
4. Artists' mouths are held open (shouting, O mouth) for the whole take (static, not moving); strictly mouths should be closed except in quotes. Non-blocking if the director accepts a held "outrage" face.
5. luma 110.4 > 110: darken the blown floor highlights.
6. Beats: signatures land g471/g496 yes (quill on sheet, "PROTESTATION" sharp, readable), tower stub + black smoke in the window g555-607 yes, chimney smoke ramp visible by g572. Round-1 issues (ceiling/checker 25 %, chair across faces, waiter missing) partly fixed: chair no longer crosses faces; waiter still not visible.
7. Handles 8 in / 4 out ok; sat 0.545 ok.

## s11 FAIL
1. g818-819: pop inside the take (diff 33): g818 is the child's cap filling the bottom of the frame, g819 is an empty-ground view with a different camera pose. This is a hidden cut in a travel take. Fix: continuous camera path through the fence rise.
2. g819-840: ground/sand fills 45-55 % of the frame (g830 sand + a tiny cart), no character; g940: worker face ~ 30 %. Fix: raise the camera or tilt up on the rise-over-the-fence.
3. g802-812: the "giant rivet" in Eiffel's hand still reads as a red mushroom/mallet (round cap, no clear shank); speed lines OK (6 frames). Fix: rivet with a visible round head + shank.
4. g856-905: the two girder carriers' mouths are open yelling on every frame (not quotes). Fix: closed mouths.
5. g919-929: toss/catch is only a yellow slab moving on the scaffold, no tongs, no bucket catch visible. Fix: make the rivet, tongs and bucket readable.
6. g907-916 (flight through the leg): a huge plain orange bowl fills the frame g908-912 (reads as a blank slab), floor shadows only. Fix: keep the camera outside the bowl.
7. Beats: laugh + point + punch-in g802 ok, Eiffel in frame, stages 1-2-3 snaps g945/969/985 read (finished tower at end, 0.4 s of motion still g993-1003). Round-1 issues 1-3 (empty ground g745-780 gone, Eiffel in frame A) are fixed. Handles 8 in / 8 out ok; sat 0.556 ok.

## s15 FAIL
1. g1004-1030: the permit floats in the air in front of both men, no hand holds it (the official's hands are on his hips, Eiffel's too); no handover happens, and from g1024 it sits at Eiffel's chest with no hand on it. Fix: official's hand holds it out, Eiffel's hand takes it (attach to hand).
2. g1008-1035: the official's face is ~ 31-35 % of the frame height for ~0.9 s, banner "EXPOSITION UNIVERSELLE 1889" is hidden by his hat from g1008 (text only half readable). Fix: pull back a little, keep the sign readable.
3. g1020-1060: both men almost frozen (only camera motion) for 1.3 s; "characters always act". Fix: Eiffel's head/arm moves, official gestures.
4. luma 84.3 < 85; auto reports soft frames g1077-1091 (push-in blur on the worried close-up). Fix: lift exposure ~5 %, sharpen the last push.
5. g1085-1096: Eiffel's face ~ 40 % of the frame (allowed as punctuation, < 1 s: ok). Sweat drop + face swap at g1066-1068 clean.
6. Handles 8 in / 4 out ok; heads < 880 ok; feet with contact shadows g988-1008 ok.
