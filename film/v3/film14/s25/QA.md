# QA s25 v2 (film 14, shot 25 only, g 1672-1770, 99 frames)
v2 fixes from the director list (shots 26-27 moved to take s26, team 3):
- Night elephants: card x0.5 with cool tint (0.62, 0.67, 0.86) on the night card dim 0.72; larger darker contact ellipses under every foot.
- Flee: the camera sits at the right end of the fence and looks along it, so the herd running left RECEDES (scale about 1.0 -> 0.4) and the shot ends on a nearly empty field (calf and herd as small specks at g 1770). The turn is keyed over 13 frames (frontal card swings away and fades, side card swings in), not a swap. Each stride throws a droplet crown + wisps, 2x larger than v1.
- qa_auto PASS. Soft frames g 1678-1680 are the keyed turn cross-fade (intended). The 1678 "no change" note is expected: g 1672-1677 are handle frames of the same shot.
- Ground mask blurred at runtime (no hard-edged pale patch); the set files are untouched in git.
- Dissolve into shot 26 (g 1760-1767) is NOT baked: shot 25 is rendered to g 1770 for the conform to blend with take s26.
- Not done: full 6 fps frame-by-frame review (contact sheet every 0.5 s + cut +-1 only). Dust crowns read somewhat spiky at the strongest strides.
