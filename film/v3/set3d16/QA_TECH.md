# QA-tech, SET gate, film 16 (set3d16)  -- VERDICT: FAIL
Checked: contact.jpg (27 tiles), individual finals (about 20 viewed at 720x1280, rest on contact), API.md, hue_report.txt, cost_report.txt, film16/shot_plan.md.
`python3 t_anim.py`: "ALL OK (76 checks)". It tests hook values only, not that the hooks are visible in the picture.
Pass: no text/lettering seen anywhere (tape is dots/dashes only); no DOF blur; no magenta/black frames; cost max 27.6 CPU s (chamber_low DAY) <= 30; magenta share <= 8.7 % everywhere (<= 10); heads: chamber_wide_high Morse chin y 855 < 880 (only one near the band).

## Issues (tile, what, fix)
1. L01/L02/L03/L04 line_close: Morse hangs in front of the ladder with straight legs dangling, feet touch no rung (floating). Fix: move morse_ladder mark onto the rungs (feet on a rung, hands on rails / pole), or pose legs bent on the ladder.
2. L10 line_trench, L11 line_trench_high: the mule team and plough are not visible (only a small blue/brown bar by Cornell; no mules, no pipe unrolling). Morse (listed in heads) not visible in L10. Plan shots 13 and 14 not met. Fix: put plough, mules and pipe-reel in frame (cams nearer / lower), show furrow length growing; check set_trench/plough_marks place the plough in the camera's view.
3. L11: cast about 25 px high (about 1/50 of frame), furrow only as a thin blue line; shot 14 counting beat unreadable. Fix: lower the start pose or put the team in mid-ground.
4. L14 trench_cut: broken geometry: flat yellow slab with a black underside floats across the frame at y 340-405 (ground cut-away edge) hiding the horizon; black discs/holes on the trench floor (y 600-700). Fix: close the cut slab / remove the stray plate, remove or texture the black discs (torn-cloth bits must read as cloth, not black holes). Sparks are tiny and far; bring the camera nearer to the split pipe.
5. L16 line_wagon: the plan's "crate of empty green beer bottles on the wagon" is not readable (only two tiny cylinders on the bed); no bottle in Morse's hand; Morse stands behind grass, feet hidden, not on the wagon bed. Fix: bottle crate large and visible at the wagon edge, Morse on morse_wagon_bed with a bottle prop held up in his hand.
6. L12/L13 line_trench_end: key/register on the crate is a 20 px blue blob, unreadable; lavender floating shovel head (x 360-420, y 900-1210) is a plain flat rectangle on a thin stick, reads as a floating sign; workers' feet hidden by grass. L13 RAIN tile shows no rain streaks at all and a saturated blue puddle (shot 21 needs rain streaks). Fix: bigger key + register on the crate, shovel head with a proper blade shape, set_rain on in the tile, desaturate puddle.
7. L15 line_road: red buggy is the same red as the barn behind it, the buggy is indistinguishable; mocker is a 68 px head, legs end in a single thin line (seat not visible), no mule visible. Fix: change buggy colour (dark green/black), move the camera so the buggy is against sky/field, show the mule, mocker seated visibly.
8. C03 chamber_low DAY: mocker is tiny (79 px head), mid-distance and half hidden behind a mail sack; plan shots 9/10 need a low angle ON the mocker with inkwell/quill foreground, quick push to a close-up. Lower half washed out by a hard-edged cream shaft plane; blank flat tan rectangle on the desk front (x 510-715, y 945-1170); mail sacks are on in a DAY tile (shot 28 only). Fix: add a preset (mocker_close) at mocker_desk about 6-8 D away, shafts off or soft for the low cams, sacks default off (on only for shot 28), remove the empty panel.
9. C05/C06 chamber_table DAY: Morse (x -5.74) and the clerk (x 5.74) are outside the frame; only the mocker's head peeks behind the telegraph with body hidden. Plan shots 26 (Morse reads the tape, congressmen crowd round) and 29 (clerk slides the instrument, mocker's face) cannot be framed from this start pose. Fix: pose/FOV or marks so Morse, clerk and mocker are all in frame; congressmen to crowd round (none present in the tile).
10. C01/C02 chamber_wide_high: tiers almost empty (one congressman at the left, none in the right bank): shot 11 "whole chamber laughs" and shot 8 "tiers of congressmen" not supported. Fix: seat at least 8-10 congressmen (hats bounce) across the tiers; cong_a..e exist but are not placed in the tile. Sun shafts are visible as flat translucent planes with hard straight edges (C01, C03, C05): fix with softer volume or fewer/rounder shafts.
11. C07 chamber_table NIGHT (shot 30): mocker cut at the left edge (half body), Morse peeking at the door not visible (door screen is empty), tape-pile OK. Fix: shift the cam so the mocker is fully in frame, Morse head in the door-screen opening, candle in the mocker's hand.
12. S02 studio_easel (shot 5): oval wife portrait, paint jars and palette/brush in hand not visible in this tile (portrait only in S01 far left); Morse has empty hands. Fix: put the portrait table into frame / change cam; give Morse a palette + brush prop.
13. S03 studio_door (shot 6): the letter is not visible, messenger is half behind Morse and empty-handed, palette already on the floor (set_palette must default off before the slip). Door opening is a black-violet blob. Fix: letter prop in the messenger's hand, messenger beside Morse, door interior with light.
14. S01 studio_wide: wood floor grain is smeared in a strong diagonal (reads as motion blur at the bottom third). Fix: re-scale the floor texture mapping / use non-anisotropic UV.
15. Caption band y > 880 not calm in all LINE tiles with foreground grass (L05-L10, L12, L15, L16, L11): high-contrast yellow/green blades and large bright foreground props (L10 crate, L15 barrel/crate, L05 orange disc bottom right, y 1040+). Fix: darker/less saturated grass tuft density in the bottom 30 %, lower-contrast FG props, or keep FG dressing to the sides.
16. Shade hue (target 240-260 outdoors) FAIL per hue_report: L01 201.7, L03 186.8, L04 202.0, L07 275.1, L08 217.5, L09 217.5, L10 268.4, L12 225.1, L15 235.4, L16 239.4 (borderline). Pass: L02 244.8, L05 254.3, L06 241.4, L11 242.5, L13 258.7, L14 240.4. Note L01-L04 have 0.3-1.4 % cast pixels, the measure is unreliable there; but the median hue is 195-190 (cyan, not violet). Fix: raise ambient blue-violet weight (#4454FF), AFTER_RAIN/RAIN sky and wet shading toward 245-255; re-run hue_report.
17. L08/L09/L05 line_rail/line_wide: train sits behind the fence with wheels hidden by fence/grass and a strip of blue/white lead pipe is already laid beside the road/rail in shots 3, 25, 27 (set_pipe 0 should hide it; wire pulse L09 is a tiny bead hard to see). Fix: set_pipe(0) default in these presets; lower fence or move the track so wheels and rods are visible; larger pulse bead.
18. Pulse (L04/L09): L04 pulse bead on pole top is large, 5 beads; L09 pulse nearly invisible at the bottle neck (shot 24/25 reveal needs a clear glow crossing the neck without leak). Fix: larger glow + bloom in L09, and a macro cam on the neck.

## Plan coverage (30 shots)
Presets present and visible: line_close, line_wide, line_rail, line_trench, line_trench_high, line_trench_end, trench_cut, line_road, line_wagon, studio x4, chamber_wide_high, chamber_low, chamber_table. Lights DAY/DUSK/RAIN/AFTER_RAIN, NIGHT, DAY->DUSK mix tile present.
Missing / not visible in a tile:
- Close-up of the mocker at his desk (shots 9, 10), mocker_desk low angle; chamber_low only has a tiny mocker.
- Macro on bottle neck (shot 24 "line_close macro"): only line_close tiles, no macro start pose.
- Mule team + plough + unrolling pipe (shots 13, 14): not visible in L10/L11.
- Bottle crate on the wagon (shot 22) and bottle in Morse's hand: not readable.
- Letter in messenger's hand, oval wife portrait (shots 5, 6).
- Rain streaks in shot 21 tile (L13).
- Clerk, Morse, congressmen crowd in chamber_table (shots 26, 29); full chamber audience (shots 8, 11).
- Buggy with mule (shot 18): buggy unreadable, mule not visible.
- Station platform with waving people (shot 27): line_rail tile shows no platform/people.
- Hooks with no visible effect in any tile: set_rain in L13, set_pipe (no pipe in L10 except a thin blue strip), set_leak 'pipe' visible only as a small cluster in L14.
## Worker blockers
- Stand marks exist (API.md) but morse_ladder is not reachable by feet (issue 1); morse_wagon_bed, morse_trench, mocker_buggy not verified in frame (issues 2, 5, 7).
- No hook starts/ends at an editable state for props held in hands (palette, letter, bottle, candle, key): render workers must attach them manually, no API listed.
- Preset start poses for shots 26/29/30 do not frame the cast (issues 9, 11).
Overrides: none.

# Re-check (after one fix round) -- VERDICT: FAIL (1 narrow blocking item, B1; everything else is notes)
Checked: contact.jpg (30 tiles visible, not 31: 30 PNGs in telegraph_work/final, tile numbering changed vs round 1), 16 finals viewed at 540x960 (L01 L09 L11 L12 L15 L16 L17 L18 L19 S01 S02 S03 C01 C03 C05 C07), API.md, hue_report.txt, cost_report.txt, shot_plan.
`python3 t_anim.py`: ALL OK (83 checks). Cost max 27.2 CPU s (C01) <= 30. Magenta max 8.75 % (L15) <= 10. Max head chin y 756 (< 880). No text, no DOF blur, no black/magenta frames.

## Status of the 18 earlier issues (old tile name -> new tile)
1. FIXED (L01-L04): Morse now stands on the ladder at the pole top, feet on rungs.
2. FIXED (L11 line_trench): plough, two mules, pipe reel and the worker/Cornell are in frame. Morse not distinguishable from Cornell (only one big figure) -> NOTE N1.
3. PARTIAL -> NOTE N2 (L12 snap1): team now visible but the cast is about 40 px high, the furrow is a thin line; counting beat still small.
4. FIXED (L17 trench_cut): slab/black discs gone; soil strata face with split pipe, cloth spikes and cyan sparks, camera near. Lower 40 % of the frame is an empty dark glossy floor -> NOTE N3.
5. FIXED (L19 line_wagon): crate of green bottles readable, Morse on the wagon bed (behind the spool). Bottle in hand is a card prop (API.md "Hand props").
6. PARTIAL: rain streaks present in L16 = FIXED; shovel-sign gone = FIXED. OPEN -> NOTE N4: key/register on the crate still small bluish blobs (L15/L16), the rain puddle is still a saturated pure blue disc (L15, L16, L19), workers' feet hidden behind the crate.
7. FIXED (L18 line_road): buggy now green with red wheels against the field, mocker seated above it, mule visible at the right edge (cut by the frame edge, NOTE N5).
8. PARTIAL -> NOTE N6 (C03): inkwell/quill foreground now present, flat tan panel gone, sacks only in C04, shafts soft. Mocker is still mid-distance (head about 100 px), no mocker_close preset / push-in start pose listed. Fine floor pinstripe (moire) on the lower third.
9. FIXED (C05/C06): Morse, mocker, clerk are all in frame behind the table (heads 62-74 px). Congressmen crowd not present -> NOTE N7.
10. FIXED (C01/C02): 14 congressmen seated in both banks; shafts now soft.
11. FIXED (C07): mocker fully in frame at the left third, doorway lit. Morse in the door is about 31 px, unreadable -> NOTE N8.
12. FIXED (S02): oval portrait in frame, paint jars/brushes in the foreground; palette in hand is a card prop.
13. FIXED (S03): messenger beside Morse, door opening is a lit cream rectangle (not a black blob); palette not on the floor. Messenger half hidden behind Morse -> NOTE N9. Letter in hand is a card prop.
14. FIXED (S01): floor grain no longer smeared.
15. OPEN -> NOTE N10: band y > 880 is still busy in L18 (large saturated yellow blades across the bottom), L11 (crate edge y 820-990 at left), L09 (blades bottom right), L19 (hard striped shadows bottom). L15/L17 calm. Render workers must frame or crop the camera so foreground dressing stays at the sides.
16. PARTIAL: report band is now 225-265. OK: L01 225.4, L04 225.0, L05, L06, L07, L08, L13, L15, L16, L19. Still outside: L02 289.6, L03 209.9, L09 195.1, L10 276.7, L11 47.8 (garbage: orange ground, 6.6 % cast), L12 269.5, L14 220.7, L17 270.0, L18 265.0 (borderline). L01-L04 have only 0.4-1.2 % cast pixels and medians 195/288/212, so the measure is unreliable there; pictures read blue-violet in shade. Only L09 (195, cast 2.9 %, shade visibly green-yellow) is a real miss -> B1.
17. PARTIAL: wide tiles no longer show laid pipe; L10 line_station shows train + platform. But L09 line_rail: the train is NOT in frame (only a loco fragment at the left edge), wheels/rods not visible, wire pulse not visible -> B1.
18. FIXED: L04 pulse trail on the wire and L05 bottle_macro with the glow parked on the glass (new tile) cover shots 24/25.

## BLOCKING (fix before render)
B1. L09 line_rail DAY: the train, its wheels/rods and the pulse bead ahead of it are not in frame (tile label claims "train, pulse ahead"); shade hue 195.1 (target 225-265). Fix: key set_train(x) so the loco is inside the start frame (or re-aim the camera), pulse at pulse_s_at_y(9.5) with a larger bead, raise ambient blue-violet; re-run hue_report. Shot 25/27 depend on it.

## NOTES (render workers handle by camera / framing / cards)
N1 L11 Morse not identifiable vs Cornell; N2 shot 14 cast tiny, use lower/nearer snap cams; N3 L17 lower half empty dark floor, frame on the pipe/sparks; N4 key/register size, puddle saturation (desaturate), feet hidden; N5 L18 reframe so the mule is not cut by the edge, grass lower; N6 chamber_low needs a mocker_close start pose (6-8 D) for shots 9/10; N7 chamber_table has no congressmen crowd for shots 26/29 (cong marks exist); N8 C07 Morse in door too small, use a framing that shows the door screen; N9 S03 messenger partly behind Morse, shift cam or mark; N10 caption-band calm in L09/L11/L18/L19; N11 hue for L02/L03/L10/L12/L14/L17 off the 240-260 target by 10-30 deg or measure-unreliable, re-check on the take frames; N12 hand props (palette, letter, bottle, candle, key) are card-only, no hook to verify attachment, TAKE gate must check.
Overrides: none.
