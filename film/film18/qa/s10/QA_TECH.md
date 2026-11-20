# QA_TECH s10 (g737-852, 116 frames) - FAIL
Checked: 6 fps frames + first/last 3; frame-diff re-measured: median 14.15, p90 18.33 (min 3.2, max 21.3). Band mean max 56, bright 0.00 %.
## Issues
1. g737-852 - rule 1 pulsing: the general stays centred while the whole background swings left-right in a pendulum (spear rack, tent and tower enter and leave the frame); measured horizontal drift reverses about every 22 frames (-95, +47, -88, +46, -65, +61 px at half res, i.e. up to ~190 px at full res), so the framing returns to the start about 5 times in 3.9 s. Frame-diff dips to 3-7 at each reversal. The high frame-diff comes from this swing, not from an eased move; it reads as a wobble. Fix: one monotonic slide (about 40 px/s) with the push, no reversal.
## Notes
- bare dark ground in the bottom ~28-30 % with no props (limit 25 %, note); the general's feet are in the band (allowed).
- mouth: lip-sync window 22.45-28.38 covers the whole take; the mouth sits under the moustache and opens only slightly (readable open in about g750-760, g790+); weak but acceptable. No other characters move their mouths except static laugh drawings of the background soldiers.
- the general looks at the lens (thumb at chest delivery, acceptable).
## Pass items
Heads/helmet well above y 880 (face ~y 430-620); subject in frame; no placeholder props (lit lamp stands, spear racks, tent); DUSK; band mid-dark; no text; no frozen/black frames; g 737-852 OK.
