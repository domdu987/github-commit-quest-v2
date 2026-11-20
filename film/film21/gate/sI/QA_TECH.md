# QA-tech sI v2 (redo, team12 bc7db28)

Segment sI, g1519-1639, 121 frames, 720x1280. Method: contact.jpg, phone_sheet.jpg, f6 frames (every 5th), full-size checks of g1549, g1579, g1584, g1594, g1604, g1634. Luma, saturation and yellow cast are not judged (normalised at the conform).

## Verdict: PASS

## Against the old list
1. English all crimson/gold: FIXED. Both riders have crimson surcoats, red plumes and gold/red checked caparisons. The column in the crane is red tabards on gold, with no blue. The only non-crimson item is the grey helmet, which reads as steel. The earlier blue-and-white horse cloth is gone.
2. Crane ends straight down the bridge: FIXED. From g1609 to g1639 the camera looks straight down the deck and the column reads as red/gold pairs filling the frame vertically. There are no tents. The bridge is narrow (about 15-20 % of the width), but the two-by-two rhythm still reads at phone size.
3. Two horses jammed (should-fix): PARTLY. The camera is higher and horse legs and heads show. But in g1540-1580 the two horses still read as side by side behind the rail, not nose into rump. The jam reads mainly from the stalled column. Non-blocking.

## Checks
- Heads: ride heads at about y 450-620, crane heads far below 880. PASS.
- Floating: ride shows bridge posts with contact splash, riders seated on horses. The helmet is deliberately airborne, g1579-1596. PASS.
- Edge: the left-edge column fragments are partially cut, but they are background extras. The two main riders are fully in frame. PASS.
- Face size: about 8-10 %. PASS.
- Mouths: no speech. A shocked open "o" on both knights, held still, g1579-1595. Acceptable.
- Bloodless: PASS. The popped helmet has a red plume and a slow spin.
- Camera: continuous ride g1519-1600, then the crane. The big framing change at g1594-1604 is the intended snap pull-out (plan: "เหมือนกัน" at 53.5 s), not a pop. PASS.
- Palette: the far field is hills, sea and sand, consistent with the set. PASS.

## Issues
A. Non-blocking, g1594-1639 (the crane): the white zig-zag lines on the water are crisp, constant-width, geometric. They read as a neon grid or a wire pattern, not water glitter or foam, and look like a set artefact. They are very visible, especially g1609-1639 at the right. Fix: lower the glitter-line opacity or width, or use a soft foam noise texture. Do not re-render just for this unless the segment is redone anyway.
B. Non-blocking, g1584-1599: the popped helmet reads as a helmet at the top (g1584), but at g1594 it is a dark grey angular slab (a boomerang shape) with white streak lines. Fix: hold the helmet side-on (bascinet silhouette) until it exits, or lighten the grey.
C. Non-blocking, g1540-1580: nose-to-tail not clear (see 3). Fix: tilt the second horse and overlap it onto the first one's rump.
D. Non-blocking, g1604-1639: a few riders drift or turn askew at the left of the column (the "tries to turn back" beat). It is tiny at phone size and reads as noise. Optional: enlarge the turning pair.
E. Info: about 30 % of the ride frames is dark water. Not a content failure.
