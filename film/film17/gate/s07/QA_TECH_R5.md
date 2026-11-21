# QA-tech film17 s07 ROUND 5 (g844-1051, render17/team1 f528820) - VERDICT: PASS (0 blocking, 6 should-fix)

Checked: all 208 frames extracted from take.mkv (take = g-844), 720x1280. Full size: g910, 915, 920, 935, 940, 945, 960, 985, 1005, 1012, 1015, 1030, 1040, 1045 (14). Cut strips (+-2) at 900/924/948/972/996. Phone-size sheet of 14 frames plus dir5.png. Numeric: sharpness, frame diff, luma on all frames.

## Auto numbers
- Hard cuts: diff g900 56, g924 68, g948 80, g972 79, g996 77. All single-frame, clean. (QA_AUTO "no visible change at 900/924" is wrong again; all five are obvious.) g899->900 shot 16 to 17a, g923->924 17a to 17b etc. all read.
- Blur: no frame under 0.65 of median except cut frames and g966-971 (0.60-0.64 sharp ratio, 18a camera push, sharp by eye, outlines crisp). 0 blur runs >3. PASS.
- Frozen: longest near-identical run = 1 frame. PASS.
- Black/magenta: none (min mean luma > 90). Dust: single white motes (g960 x240,y780; g1040 x~950-985,y1185; g1045 x~1150/y1260 area), well under 0.5. No see-through cards, no beam shafts. PASS.
- Mouths: 18a puppets static (g948-971 frame diff is the whole-frame camera push, not mouths). Chins y <= ~700 (< 880). PASS.

## Team claims
- Sleeves run out of frame: TRUE for shot 18b glove/pen (cropped at top-right, continuous), shot 19 g1005-1046 (arm and cuff run off the right edge, no flat cut end, no floating tube). R4 B1 FIXED. Shot-19 end: sleeve enters from lower right, TRUE but see S1.
- 17a hand (g910/915/920): PARTLY TRUE. Palm, thumb, three curled fingers and the middle finger along the ruler are clearly a hand at phone size (R4 B2 finger part FIXED). Wrist/cuff are off frame left (x 0-20), so no cuff is visible. Jaw plate touches the fingertip at g915-920 (finger end x~545 meets jaw face x~550); at g910 gap about 25 px (touch lands g912-915). Glove on the bar end/knob at right edge (x 560-720, y 480-600) holds it, about half cropped at the frame edge. Acceptable.
- 17b boot (g924-947): TRUE. Side-profile boot with laces (5 white dashes), tongue, heel, sole slab, trouser leg and blue cuff running out of top. Reads as a boot at phone size (R4 B2 boot part FIXED). Block lands on the toe at g945: block x 520-545 overlaps toe tip x~545, glove (x 530-720, y 450-620) sits on the yellow handle above it. Held and touching. PASS.
- 18a g960: jaws straddle prisoner_b's ear, bar runs to Bertillon's glove at left edge with blue cuff. PASS. Held, touching.
- 18b g985: pen nib on the card at x ~1250-733=~520, y 600, glove at top-right edge holds pen, marks drawn. PASS.
- Card sinks behind drawer front: TRUE. g1005 card above drawer under glove, g1012 card half-in, g1015 glove on rim. No stray card edge at g1012-14 (R4 S3 FIXED).
- Wastebin/blue stub gone: TRUE (R4 S4 FIXED). Chair rail/armrest gone: TRUE in 17b/18a (R4 S5 orange plank: see S4, a chunk still appears).
- Samples 28: NOT VERIFIABLE. meta.json in the take still says "samples": 16 and shot.py defaults to 16. Moire still present, so it looks like 16 or a denoise issue persists. Ask team to confirm.

## Blocking
None.

## Should-fix
S1. g1034-1051 lower right corner (x 570-720, y 1130-1280; g1045 x 560-720, y 1040-1280): the "entering sleeve" is a flat-topped blue slab with yellow notch, red/yellow stripe edge and an orange stepped box. No glove or arm; reads as a floating blue panel plus crate, not clearly a sleeve. Attached to the frame edge, so not floating, but confusing for ~17 frames. Fix: add the glove/forearm shape or crop it out.
S2. Concentric ring moire on back wall still visible at full size in 17a/17b/18b: g910/915 x 250-460, y 340-520; g935/940 x 130-340, y 400-540 and x 200-400, y 200-360; g985 x 250-400, y 0-60. Faint but just visible at phone size in 17a (g905-915) and g940. Not distracting enough to block. Re-render with a smooth wall texture or true 28 samples.
S3. 17a/18b flat empty table: g900-923 y 800-1280 (about 37 % of frame) and g972-995 y 950-1280 are flat brown; 17b floor y 1000-1280 also empty yellow. Reframe lower or push in.
S4. 18a g948-971: an orange wedge/plank (x 215-420, y 1120-1240 at g960) still sits between the legs in front of the floor. Reads as a chair foot or bench, tolerable but still odd.
S5. 18a g960: dark ball at x 55-90, y 800-830 beside Bertillon's hip (hand knob), unexplained.
S6. g898/899->g900 and others: QA_AUTO cut note is wrong (cuts are visible); fix the auto check.

## Rules summary
Held by visible glove + touches target: 16 PASS (approved), 17a PASS, 17b PASS, 18a PASS, 18b PASS, 19 PASS. No floating limbs/objects (S1 borderline). Blur PASS. Frozen PASS. See-through/beams PASS. Dust PASS. Mouths PASS. Chins PASS. Black/magenta PASS. Hard cuts PASS. Rhythm 6.92 / 23.15 acceptable.
R4 status: B1 fixed, B2 fixed, S1 moire remains, S2 speckle gone, S3 fixed, S4 fixed, S5 mostly fixed, S6 remains.
