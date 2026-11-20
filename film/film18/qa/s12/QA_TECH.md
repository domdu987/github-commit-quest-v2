# QA_TECH s12 (take g937-1010; in-shot g944-1002) - FAIL (round 2)
Checked: frames at 6 fps + first/last 3, crops at full size, 360 phone view. Frame-diff re-measured (90x160 area): median 4.89, p90 7.45 (min 3.5) - median passes, p90 < 9 but a visible eased slide-right is present (guide only). No pulsing: the old "wiggle every 11 frames" is gone, motion is steady. Caption band mean 47-56, bright max 0.38 %. No text, no mouths, no oxen, heads < 880, DUSK, no blur.
Earlier blockers: #1 wiggles FIXED; #2 bare ground NOT FIXED; #3 navy wheel FIXED (wheel gone) but new rocks/plank (see 2); #4 folk on wall NOT FIXED; #5 banner improved (cream banner ~40 px, readable only g957-985).
## Issues
1. g937-1010 - bare ground (rule 5, > 30 % blocks): the bottom about 33-38 % (y > ~800) is dark teal ground with only a few grass blades. Fix: dark fg props across the bottom, tilt up, or crop so ground <= 25 %.
2. g937-975 - rule 2 placeholders in the foreground: a flat red-brown plank/lance with a white arrow tip crosses the lower left (g937-972) and grey faceted low-poly rocks with thick navy outline fill the lower left (g952-972). They read as untextured props. Hide them or replace with lit textured props (cart wheel, baskets).
3. g957-1002 - envoy not readable / not kept in frame (rule 4 + shot check): he is about 100 px tall (head ~45 px), half hidden behind the bridge rail posts, visible only g957-985, and walks off the right edge from about g985; for the last ~0.6 s of the shot there is no envoy. Fix: keep him in frame, larger, left of the posts, banner larger.
4. g937-1010 - folk on the wall: only one clear woman (about 35-40 px wide) on the wall crest right of the tower; 1-2 more are half hidden behind pillars. Nothing in the crenel gaps. At phone size it reads as one dot. Fix: 4-6 folk along the crest, 70 px or more.
## Notes
- Gate: a pale gap at the doors is not clearly visible; gate looks closed (plan: "opens a crack").
- Bottom-left blue plank bridge/moat from g982 is a plain dark-blue strip (lit, OK).
- p90 7.45 < 9: guide only, eased slide present.
