# QA-tech sE1 v2 (film-13 QA, team9 86941e2)

**Verdict: FAIL** (4 blocking items, all fixable in the camera/props/framing of shot.py)

Method: all 96 frames at 360x640 (tiles of every frame g793-885), 6 fps full-size frames, and Farneback/phase-correlation global motion on every frame, checked for sign flips.

## Shake ruling
**No sign-flipping camera shake. The 9.3 / 9.8 px jitter in g790-849 comes from the fast fly-over, not from shaking.** Every frame-pair in g793-812 (drift left/down), g818-842 (rise over river, climb hill) and g843-885 (push-in) moves in one direction. The snap at g835 is one forward jump followed by speed lines g837-842; there is no 2-frame shake and no reversal after it (g843-885 flow is monotone, <3 px/frame). The measured "reversals" at g813-816 (dx +10 against -24 before) are the pole/banner foreground occluding the flow estimate, not the camera (see item 1).

## Old fails
- Bank group too small: PARTLY FIXED. g805-815 the laughing/pointing/hoeing group is large and reads. g793-803 it is still small (heads about 50 px at 720 wide) - see item 4.
- Spear pole over the right-most Scot's face: FIXED (pole at far left, g845-850; right-most Scot's face is clear g845-885). A thin golden shaft crosses the 2nd Scot's moustache g850-885 (non-blocking).
- Wallace's brow too subtle: NOT FIXED enough - see item 3.
- Scots' mouths: closed everywhere. OK. No heads at y>=880. Feet grounded (the e4 "3 cm above" is the terrain mesh, accepted).

## Blocking items
1. **g813-817 whip / black-out.** In 4 frames the view jumps from the close group (g812-813) to the campfire and then a dark pole/banner fills most of the frame (g816, about 70 % black-maroon), then the river at g817. It reads as a glitch pop, not a rise. Fix: keep the camera path continuous (rise first, slide right second) and move the flag pole/banner (prop at the camera start) out of the flight path, or fade its alpha. No single-frame jump over 40 px.
2. **g836-842 snap framing.** The snap lands at g835 (speed lines start g837, 2 frames later), and for g837-842 the Scots line is only about 60 px wide, so the punch-in does not land on them and the lines hide them. Fix: end the snap at g837 on the Scots at final push-in framing (Scots 20 % bigger), or keep the lines to the frame edges; make the speed lines start with the jump (g835).
3. **g850-880 Wallace's brow.** Still only a slight tilt, unreadable at 360x640 until g885; the first half of the hold shows a neutral face. Fix: raise the brow at about g845 and by 2-3 times (clear arch, other brow lowered), and start the push-in at g845 so the face is large by g860.
4. **g793-803 bank group too small, and g870-885 left Scot clipped.** (a) At the start the English group is about 40 % of the frame width and the mime cannot be read: start the camera closer (or lens 32-35) so the group is at least 60 % of the width. (b) A helmeted Scot at the left edge is cut by the frame from g868 to the end (the push-in crops him): pan 0.2-0.3 m left or reduce the push-in to 20 %.
