# QA_TECH s09 (film 12 shot 9) RE-CHECK r2 - VERDICT: PASS
Checked: all 18 f6 frames (g566-651) at full size (f_001, 005, 009, 014, 018 opened individually, rest via the contact), phone sheet, QA_AUTO (PASS), meta. Mouth check: 9 consecutive frames (n=40-48) cropped for coachman, woman and left man, plus coachman crop every 5 frames over the whole shot (ffmpeg tmp folder, deleted).

## Earlier blocking issue
1. Mouth movement (coachman laughing mouth from g606) - FIXED. The held open-laugh face is constant for the whole shot on the coachman, the woman and the left man; consecutive frames show the same open mouth shape, only perspective/bob size change, no flapping or open-close cycle. Allowed under the brief (held laugh, no flapping, no lip-sync).
2. Whip (non-blocking) - FIXED: whip visible in the coachman's raised hand in every frame.
3. Plan coverage (non-blocking) - PARTLY: 5 passers-by (red-coat man, brown man behind him, blue Hanway, woman in red, girl in teal) and one coachman clearly visible; a second coachman/other laughers are hidden behind the coach or tiny. Pointing arms visible (left red-coat man, woman). Reads as "laugh and point" on the phone sheet.
4. Eye-lines (non-blocking) - OPEN: laughers have eyes closed (laughing), none looks at Hanway explicitly; Hanway smirks toward camera. Fine for a laugh pose.
5. Contact (non-blocking) - PARTLY: contact blobs now visible under the figures and Hanway; feet sit on the setts. Puddle noise reduced.

## New failures
None blocking. Heads: all heads y < 880 (Hanway head max ~y 640 at f_018; his shoes reach y ~890 only at the very end, feet are allowed there). No clipping (no figure cut by an edge), no blur/DOF seen, no pops, no black/frozen frames, no text, no orbs. Scale fine (Hanway grows as he approaches, umbrellas adult-sized, black umbrella in his hand, handle in hand). Props: Hanway umbrella in hand, coachman whip in hand, reins/green and red umbrellas held by the right girl/woman. Continuity: rain light, same costumes as s06/s09 r1.
Notes (non-blocking): lower 40 % of frame is empty cobbles (composition); transition_in cut.

Verdict: PASS.
