# QA_TECH s11 (take g853-951 incl. 8 f out handle, 99 frames) - FAIL
Checked: 6 fps frames + first/last 3 (s11/qf/), framediff re-measured: median 13.79 (in-shot g853-943: 13.59), p90 18.38 - passes.
1. g880-905 (f035-f045 region) - ghost props: pale, semi-transparent hexagonal/stick props float in the lower third and cross the caption band (f040 at y~890-960, f045 at y~900-1000); they change position between frames and read as rendering debris / floating objects. Fix: make the ground props opaque, grounded with contact shadows, and keep them out of y 880-950.
2. g853-943 - sky: cream cloud sprites with dark triangular notches (f040 top-left, f090 top-left) read as stickers; sky top ~35 % empty. Fix: repaint/remove clouds, lower camera tilt.
3. g853-943 - plan beat: "make horns with fingers / mock-moo" is only weakly present (one soldier with hands over head at f040, others laugh/cheer); no clear finger-horns pose. Fix: use the mock_moo horns drawing on 2-3 soldiers during g880-940.
4. g915-951 (f085-f098) - continuity within shot: sky shifts from orange sunset to deep blue by f085-f098 while the fire and set stay lit; plan says DUSK throughout. Check camera tilt/sky card; keep warm band visible.
5. g920-951 - fg soldier fills the right third with feet at y 930-960 (in the band) and a basket/rock overlapping; head/chin 819 max is OK. Non-blocking.
6. caption band: bright (>170) share up to 6 % (fire edge/ground glow), >200 max 0.23 %. Non-blocking but near limit.
Pass items: heads <= y 819; no mouths on quotes (only laugh/moo drawings, no quote lip-sync); fg prop present (jar, basket, rock) and varied soldier poses; fire present; DUSK start matches s10 neighbour; handle g944-951 present; no frozen/black/magenta frames; no text; g range 853-943 (+8) matches plan.
