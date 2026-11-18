# QA-tech TAKE gate 1, film 11 (21 takes)
Method: qa_auto.py on every take (comma cut list `--cuts g0,g1+1`; all 21 = QA_AUTO PASS: no frozen runs, no black/magenta, no pops, magenta 0.0 %; the only note on every take is "planned cut with no visible change", expected because g0/g1+1 are take boundaries, not internal cuts). Frames at 6 fps + g0/g1 +-3 on contact sheets with the y 880 line, full-res crops of faces/hands/feet, mouth strips for s14 and s20.
Heads: all < y 880 (nearest is s14, ~y 560). No blob-stack smoke visible in s02 s07 s08 s09 s19 s20 s25. Sore card: red dot s02/s07/s08/s10, blister ring s11/s12/s13/s15/s18/s20: consistent with plan. Lip-sync: towndoc mouth moves only g850-898 in s14 (window 849-898 OK) and inside 14.84-18.10 in s07; s20 shock is a held O mouth with blinks, not talk; s08 towndoc off screen.

| take | verdict |
|---|---|
| s01 | PASS |
| s02 | PASS |
| s05 | PASS |
| s07 | PASS |
| s08 | PASS |
| s09 | PASS |
| s10 | FAIL |
| s11 | PASS |
| s12 | FAIL |
| s13 | PASS |
| s14 | PASS |
| s15 | PASS |
| s18 | FAIL |
| s19 | PASS |
| s20 | PASS |
| s21 | PASS |
| s22 | PASS |
| s23 | PASS |
| s24 | PASS |
| s25 | PASS |
| s28 | PASS |

## Blocking issues
### s10
1. g621-675 (whole shot): the hanging green lamp shade and its rod sit exactly on top of James's head, so it reads as a hat / James hanging from a string. Fix: hide the ceiling lamp in room_day for this shot (hide_render) or move the camera/James card so the lamp is not behind his head.
### s12
1. g723-776 (whole shot): same lamp shade + rod on James's head (clear at g743). Same fix. s11 (g672-723) has the thin rod touching his hair: hide the lamp there too for consistency.
### s18
1. g1113-1152: same green lamp shade sits like a hat on James's hair (crop g1136). Same fix.

## Non-blocking notes
- s01: subjects small in upper third, lower half empty straw with big chickens; Jenner stands upright rather than bending over the hand; jar, lancet and blistered hand do read.
- s02/s07/s08 vs s10/s11/s12: sore marker is on the viewer-left arm in the first group, viewer-right in the second. Verify it is the same arm (upper_arm_l) or flip.
- s05 g318-326: milkmaid2 and Sarah's yoke clipped by the left frame edge while walking in; scene dark/blue, not "golden barn"; flat bright yellow lantern rectangle reads as a sticker (also s22, s28).
- s10: mother/Jenner stare at camera, not at James's arm (eye-line).
- s12: armpit rub is a subtle arm-across-chest, wince mild.
- s13: very dark, subjects tiny, bottom 55 % empty floor; mother sits on a sack-like blob.
- s15: after g938 James covers most of Jenner (his "proud" beat is hardly visible).
- s18: James behind the bed and small; no food visible for "eating".
- s19: James very small in mid-distance; large dark chicken in the foreground.
- s21: pail stands in front of the udder rather than under it.
- s22: key image reads (hand blisters + clear face) but the udder is largely hidden behind the pail.
- s23: characters small, heavy empty foreground, Blossom only partly in frame at the right edge, pockmarked villagers stand in the yard not "in the door"; feet hidden behind pails.
- s24: Jenner tiny until ~g1535, top third is ceiling, a thin vertical pole touches his head, outside light pale not golden.
- s25: big goose grows in the foreground (g1610-1632) and covers the lower left.
- s28: cow turns head toward camera in the last ~12 frames, tail and ear move; plan beat delivered.
