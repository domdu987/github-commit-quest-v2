# QA-tech sI (film 21, g1519-1639, 121 frames): FAIL
Method: 6 fps (24 frames), first/last 4 frames, f62 (g1581) at full size. 121 frames confirmed. The plan row says to g1640, the take ends at g1639 (the cut at 1640 is hard, no handles), which is fine.

## Verdict
FAIL on the colour rule and the readability of the final crane shot. Technically clean otherwise (no blur, no black or magenta, no pops).

## Checks that pass
- Ride-along g1519-1600 on the deck: bridge rail, river and light, no DOF. Horses yaw and hop, a helmet pops off at about g1581 (floating above the head for about 6 frames, bare-headed knight with a surprised face, then the helmet flies out). Comic, no blood.
- Crane up g1605-1620, then a snap pull-out at the local f89 (g1608): from the column on the bridge to a wide with the bridge small, good.
- Heads under y 880 everywhere. Faces: in the ride the faces are about 10-12 % of the frame. Nobody cut at the frame edge, nothing floats (contact shadows and the bridge deck). Rim light on cards: a known limitation, noted.
- Joins: cut in and cut out (J1 hard cut at g1640). The previous take's last frame was not in this task.
- No frozen run, no magenta. Colour is very saturated (sat 0.637).

## Issues
1. g1519-1639, whole segment: English riders are NOT all crimson. Blue is everywhere. The main knight (next to the red one) wears a blue surcoat, a blue plume and a striped blue-and-white horse cloth; the crane shows a column of red, blue, yellow and white blocks (g1595-1640). The brief says "All English are crimson". Fix: recolour the cards and caparisons to crimson/gold, and the box figures too.
2. g1599-1639: the final crane view is not "straight down the bridge". From about g1610 the camera shows the bridge tiny at the top-right (8-10 % of the width), with tents filling the bottom half and a big yellow field above. The column "two by two" is unreadable at phone size. Fix: end the crane directly over the bridge, looking straight down its length at about 60 % of the frame height, with the tents out of frame.
3. g1540-1600: the "two horses wedged nose to tail" beat is not readable. The two horses stand side by side behind the rail (a blue knight on a grey horse and a red knight on a bay), with no visible wedge or jam, and the bridge rail hides both horses' legs. The wedge shows only in the high view as box shapes. Fix: lower the rail or raise the camera slightly in the ride, and push the horses nose-to-tail and tilted.
4. g1581-1595: the knights' mouths are open (shocked "o") outside any quote. This is an expression, not speech, so low-risk, but check against captions.json; close the mouths if g1581-1595 is not inside a cast quote.
5. g1608-1639: far terrain is blown out yellow (saturated, glare), and the sky is hazy blue. In the crane the yellow field (about 35 % of the frame) looks flat. Fix: darken or tint the terrain towards green, lower the exposure by about 0.3 EV in the crane.
6. g1519-1600: about 30 % of the frame is dark navy water (known by the team), with the rail covering the riders' lower body. Optional: lift the camera.
7. g1581: the popped helmet is a flat grey slab that reads as a plank in g1590-1595 (grey blade at the top-right). Optional: make it read as a helmet.

Fix list: 1, 2 must be fixed; 3 should be fixed.
