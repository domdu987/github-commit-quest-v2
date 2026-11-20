# QA_TECH s24 (take g1801-1887; in-shot g1807-1882) - FAIL (round 2)
Checked: 6 fps + first/last 3, full-size crop g1831, strips g1814-1828 and g1854-1868, lower-band strip. Frame-diff (90x160 area): median 10.08, p90 13.40 (min 2.6): passes. Pulsing FIXED: the strips show one continuous push/slide with no pop in/out. Heads all < 880 (no character below y 700 in the lower band; the director's run2 chin 896 is not visible in any frame). Caption band mean 72-112, bright max 0.9 %. No mouths, no blade strikes, no blood.
Earlier blockers: #1 pulses FIXED; #2 rout reads - NOT FIXED; #3 flying objects - NOT FIXED; #4 chariot - NOT FIXED; #5 bare ground - NOT FIXED.
## Issues
1. g1851-1887 - the rout disappears: from g~1846 the frame shows a calm campfire with one or two soldiers at the right edge and a single dancing soldier at left; no fleeing crowd, no falling soldiers. The 3-4 running soldiers that read (g1801-1846) are mostly 55-75 px tall at 720 w (only 2-3 foreground ones about 100-150 px at g1826-1846). Fix: keep 6+ soldiers of 70+ px running/falling in the mid-ground through g1882.
2. g1821-1862 - flying pots/helmets do not read: they are flat discs and faceted wedges in plain gold or plain grey (g1831 crop: gold disc, grey octagon, grey triangle) with no texture or shape; 1-2 at once. Fix: bronze pots with handles and plumed helmets, 3-4 in the air.
3. g1801-1830 and after - chariot: seen small and tilting at the centre-back g1801-1830 only; not seen rolling away afterwards. Fix: larger and kept in frame, rolling off.
4. g1801-1887 - tents do not visibly collapse: two leaning slabs at the left; most tents stay upright and the camp otherwise looks normal.
5. g1836-1887 - a translucent pale tile-textured panel with a dark ghost figure silhouette lies over the bottom right (rule 2 placeholder / artifact). Fix: remove or make opaque.
6. g1801-1887 - bare ground (> 30 % blocks): bottom 38-45 % (y > ~700) is plain dark dirt with a warm fire pool; fg props only at g1801-1821 (a jar with grey cap and 2 grey helmets, lumps) and none later. Fix: dark fg props, tilt up.
## Notes
- qa_auto: planned cut at g1807 shows no visible change (cut in from s23: handles).
- Panic faces on the soldiers read well at full size.
