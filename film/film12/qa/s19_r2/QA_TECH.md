# QA_TECH s19 (film 12 shots 19-21, g1334-1584) RE-CHECK r2 - VERDICT: PASS
Checked: all 50 f6 frames (f_001, 008, 015, 022, 027, 029, 030, 050 opened at full size, the rest through the contact), cut frames g1470_3/4/5/7 and g1410_3/4, phone sheet, QA_AUTO (PASS; its "no visible change at cuts" is a false positive, the cuts are hard and clear). Umbrella openings: consecutive-frame crops extracted with ffmpeg (shot 19 n=30-44 every 2nd frame, shot 20 n=124-138, shot 21 start); tmp folder deleted.

## Earlier blocking issues
1. Scale / empty umbrellas in shot 21 - FIXED. Each canopy now has a gentleman under it, adult-sized (about 1.2x shoulder width), handles in hands; the oversized set umbrellas are gone, nothing over the coachman. About 40-50 canopies each with a person visible in f_029-f_050.
2. "Sea of umbrellas, Hanway among them" on the phone sheet - FIXED (mostly). Dark navy, ochre, red, brown, green canopies now read as a crowd of umbrellas on the phone sheet; Hanway (blue coat, smiling, umbrella) stands inside the crowd mid-street (f_050 ~ (350,780)), small but identifiable by his blue coat. Remaining weakness (non-blocking): lower third of the frame is still empty cobbles, and the crane is high so Hanway is ~60 px.
3. Continuity across g1470 - FIXED. g1470_4 onward shows the crowd already with many open umbrellas (same colours/gentlemen as g1469), no re-pop from an empty street; ramp continues to a full street by ~g1522.
4. One-by-one progression - FIXED. Shot 19: the close gentleman watches/looks aside, his furled stick rises diagonally and opens over about 8-10 frames (g1394-1410 sequence), handle always in the raised hand, no teleport. Shot 20: foreground gentlemen open their umbrellas (g1458-1470 brown gentleman now opens his, smiling), mid-ground pops, crowd canopies grow over several frames (no pops). Hanway's own umbrella is open from the start (non-blocking: not "imitating", but reads as shared joke).
5. Floating/held umbrella - FIXED (handle visible in raised hand in all opening frames).
6. Mouths - FIXED: opening gentlemen flat mouth then small smile; no open "O" holding; crowd mouths flat. No talking movement.
7-12 (non-blocking): grain on cobbles reduced but still visible at full size in shots 19-20 (OPEN, minor); contact shadows only thin on near figures (OPEN, minor); some clipping at the frame edge: green man at the left edge f_001 (g1334), right-hand man cut at the right edge f_015 and f_022 (OPEN, minor, partial figures at edges, not a prop/head break); crowd now drifts/bobs so the end is not still (FIXED); red cart wheel left of shot 20 still saturated but smaller (minor).

## New failures
None blocking. Heads: all heads above y 880 (lowest head in shot 21 ~y 860, f_050 left-foreground gentleman; checked on f_029/f_030/f_050 and phone sheet cyan line), shots 19/20 heads max ~y 800. No blur/DOF, no black/magenta/frozen frames, no text, no orbs, rain consistent, Hanway costume continuous (blue coat, white wig, tricorne, umbrella with hooked handle). Eye-lines: gentlemen look sideways/at Hanway region, some still toward camera (minor). Minor oddity: a soft dark-blue blob on the cobbles at the lower right of shot 21 (f_029-f_030, ~(600,1110)), reads as a puddle reflection/shadow, not a sprite.

## Plan coverage (phone sheet)
- 19 gentleman watches, opens umbrella: PASS.
- 20 second, third, one by one: PASS.
- 21 sea of umbrellas, Hanway smiling among them: PASS (small Hanway, lower third empty).

Verdict: PASS.
