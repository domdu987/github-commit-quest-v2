# QA_TECH s01 (take g0-77, 78 frames) - FAIL (re-check of the re-shot)
Checked: 6 fps frames (g0,5..75) + first/last 3, framediff re-measured from take.mkv (90x160 grey, 77 in-shot pairs): median 8.42, p90 14.84 (min 1.10, max 18.67). Caption band y880-950: mean max 78.8, bright(>200) 0.00 %.
## Earlier issues (previous QA_TECH s01)
- E1 p90 < 12: FIXED (14.84).
- E2 right-edge clip at g70-77: FIXED (he is inside the frame, left edge ~25 px at g77).
- E3 eye-line (looks at the lens with a frown, not at the ox): NOT FIXED, see 1.
- E4 hook read, only 4-7 oxen: unchanged, non-blocking, see 4.
## Issues
1. g0-77 - eye-line: Tian Dan still faces the lens with the same frown in every sampled frame; the gaze never goes to the ox or the coat. Reads as posing. The plan beat is "tugs the coat over an ox". Fix: face card turned toward the ox / glance card on the tug beats.
2. g40, g45, g65 (and g60-70 hat brim) - framing: the figure is clipped at the left edge: hat brim and hair touch x=0 at g40/g45/g65, body clipped at x=0. Fix: keep his mark 60 px inside the edges at the snap peaks, or reduce the slide at the peaks.
3. g0-77 - plan beat: the red coat is held out in the air to the right as a free-standing red cloth next to an ox that already wears its coat. It reads as waving a flag, not dressing an ox. Fix: put the coat over the back of the ox he stands at, or show the ox half-dressed.
4. g0-77 - hook read (non-blocking): only 3-5 dressed oxen visible; "พันกว่าตัว" is audio only. The fg lantern is a flat saturated-orange cylinder (RGB near 255,140,0) with no glow or pool of light; it reads as a plastic can, not a lantern. Fix: lower emission, add the warm halo and pool.
5. g15-g45 (snap peaks) - framing: his face fills ~40 % of the frame width (chin ~y 825 at the peak, still < 880). The client rule is no extreme close-ups. Fix: reduce peak snap to about 1.15x.
## Pass items
heads/chin < 880 (max ~825); caption band clean, no emitters; no mouth moves (frown only); no text; ox horns have short blades and dragon coats (correct for s01); NIGHT matches plan; feet at g25-35 have contact shadows; no frozen/black/magenta frames (one low diff, 1.10 at g5, single frame); g range 0-77 matches the plan (78 frames).
