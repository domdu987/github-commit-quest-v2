# TAKE gate round 3, QA-tech A, film 20: s02 s03 s06 s09 s11
Method: all frames extracted (g = first_g + index), qa_auto.py + qa_stats2.py, viewed at 6 fps + joins/beats. Takes not edited.
| take | sat | vivid % | luma | diff med/p90 | auto | verdict |
|---|---|---|---|---|---|---|
| s02 | 0.598 | 55.3 | 94.1 | 4.68 / 6.58 | PASS | PASS (notes) |
| s03 | 0.500 | 58.4 | 97.3 | 8.55 / 14.37 | PASS | FAIL |
| s06 | 0.545 | 47.2 | 110.4 | 14.09 / 24.54 | PASS | FAIL |
| s09 | 0.555 | 53.4 | 98.2 | 6.88 / 13.26 | PASS | FAIL (T06->T09 join) |
| s11 | 0.558 | 65.7 | 100.3 | 4.69 / 15.12 | PASS (soft g836-839) | FAIL |

## s02 PASS. Round 2: waiter in lens FIXED (gone, no streak); open waiter mouth FIXED; end pose happy face + head ~120 px FIXED; napkin NOT clearly visible (white shirt, fork only: NOTE).
Notes: p90 6.58 (< 12, snap pull-out now gentle; non-blocking since beats read); end g146-185 floor ~25-30 % and ceiling beams ~22 % (borderline).
## s03 FAIL. Round 2: Eiffel half-cut at g300 FIXED; black vertical pole mostly gone; leg geometry/roll much better; riveters visible from g374 FIXED. NOT FIXED:
1. g170-215: 50-55 % empty sand, one leg at left, no Seine; Eiffel is not findable and the start is not an extreme wide of Paris. Eiffel is <5 % only to ~g230 and reaches medium ~g266: the zoom lasts ~1.2 s (needs 3-6 s). Fix: start higher/further with Seine and all legs, land medium ~g300.
2. g248-308: pale brick wall slab fills 40-45 % of frame behind Eiffel; g254-290 black/blue blueprint table fills the bottom 25-30 % (reads as black slab). Fix: move wall out, cream plans on table, lower camera/tilt up.
3. g326-340: leg still slightly bowed with orange timber look (NOTE); sat 0.500 at the limit.
## s06 FAIL. Round 2: waiter still not visible; luma 110.4 (> 110) NOT FIXED. NOT FIXED:
1. g438-444: top-hat artist half cut by left edge; g456-474 and g480: large newspapers cover faces. Fix: keep group whole, shrink/raise papers.
2. g588-607: floor ~30 % with blown white glare bottom-left, ceiling ~20 %, Maupassant small. Fix: tilt down, push to banquette, kill glare (also lowers luma below 110).
3. Artists' mouths held open (shouting) the whole take: non-blocking if accepted.
4. Diff median 14 / p90 24.5 (sweep g508-551) high but sharp, no soft frames: NOTE. Signatures g471/g496, PROTESTATION, stub tower and smoke in window all read. Fixed vs round 2: no frame-edge cut in g590+, chair clear of faces.
## s09 FAIL. Lip-sync opens g685, stays in 22.62-25.11 s window (+-0.15): OK; mouth shut before and after; heads < 880; close-up g735-760 face ~35 % for ~0.8 s ok as punctuation.
1. T06 g603 -> T09 g604 JUMP: g603 is a wide shot (Maupassant seated, tiny, chandelier/ceiling, glare floor); g604 is a close shot, Maupassant standing, no ceiling (mean abs diff 82/255). Visible jump = FAIL. Fix: re-render T06 end (g596-607) to the pose in s09/meta.json start_cam (loc 2.618,9.596,1.334 look 1.692,13.16,1.999 / standing-seated state), or re-render T09 start from T06's actual end pose; Maupassant must also be in the same pose (seated holding glass in T06 vs standing in T09).
2. g600-680: floor ~30 % of frame (checker). Fix: tilt up a few degrees during the crane.
## s11 FAIL. Round 2: hidden-cut pop g818-819 FIXED (continuous rise); carriers' mouths now closed FIXED; Eiffel in frame, stages 1-2-3 snaps g945/969/985 read. NOT FIXED / NEW:
1. g814-822: "giant rivet" still reads as an orange mushroom/lantern (round cap, thick stem, no rivet head). Fix: iron rivet shape.
2. g820-821: broken geometry, black unlit box slab in the lower right. Fix: hide it.
3. g823-841 ground/sand 40-50 % of frame, no character (g829-841); g913 bottom ~45 % ground and shadow. Fix: raise/tilt camera up on the rise and the leg flight.
4. g919-943: rivet toss/catch still only a small yellow spark; tongs not clearly read. Fix: visible rivet + tongs arc into the bucket.
5. Diff p90 15.1 comes from three fast sweeps (g818-826 9 frames, g907-920 14 frames, g944-953); lengths exceed 3-frame streak but frames look sharp: NOTE.
