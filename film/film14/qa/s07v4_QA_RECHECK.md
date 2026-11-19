# s07 v4 TAKE-gate re-check (QA-art + tech), round 4   VERDICT: FAIL (1 blocker)

Checked: all 362 frames extracted (g 403-764); every 3rd frame g 655-764 and every frame g 655-670, at 720x1280 / 360x640 and at phone size (180x320);
full-size crowd crops g 667/700/730/758; per-frame crop of old man + kid g 700-723. Mean abs frame diff over the whole take.
Working files: scratchpad/takes/qa4/ (phone_every3.jpg, half_655_670.jpg, right_700_723.jpg, crop*.png).

## Tech: PASS
- Cuts: diff spikes only at g461 (30.2), g564 (40.3), g664 (64.4). Everything else 1.6-3.3. No pops, no frozen run, no black/magenta frames.
- Hand pop g661-662: GONE. The hand disc drifts down and out over g650-663 in small even steps (diff 2.1-2.4 per frame); no snap.
- Heads: all chins above y 880 in every frame of shot 10 (log heads y 467-643). Nobody clipped; framing as v3 (crowd y ~370-880, kid ends inside x 720).

## v3 blocker: shot 10 (g664-758) target of the mockery  -> STILL NOT READABLE
| check | status | evidence |
|---|---|---|
| Farmer is the target (eyes open, hive in hand) | PARTLY | Hive box is at his chest (good, continuity). But his face is half-lidded eyes + one-sided smile with a dark stick finger at his nose/cheek. It reads as smug / pleased / picking his nose, not embarrassed or stiff. At phone size he looks like he is in on the joke. |
| Uncle and old man point at him while laughing | FAIL | The uncle's screen-left arm goes over the hive and its dark finger ends ON the farmer's face (g667-758), so it reads as poking his face or as the farmer's own finger, not a point. The uncle's other (screen-right) teal arm crosses up over the OLD MAN's face and covers his mouth/beard all shot. The old man has one hand on his hip and no visible point toward the farmer. |
| Kid bangs the pot | FAIL | g700-723 frame by frame: the kid holds the grey pot to his chest with both hands; no spoon/stick is visible and there is no hit motion (only a tiny dark stub at the hand). Same as v3. |

## New problems
- The uncle's right arm now covers the old man's face (mouth, beard) for the whole shot; this hides one of the three laughers and confuses whose arm is whose.
- Nothing else new; shots 7-9 unchanged except the eased hand.

## Blocker (round 4)
1. **Shot 10 (g664-758) still does not read "the village laughs AT the farmer".** Needed, re-render shot 10 only, same framing:
   - Farmer: eyes wide open, brows up, mouth a flat/wobbly line (no smirk); remove the stick at his face; both hands on the hive.
   - Uncle: one arm straight out screen-left, finger stopping ~40-60 px SHORT of the farmer (pointing, not touching); other arm on his belly or down, NOT across the old man.
   - Old man: face clear, one arm out screen-left with index finger (it may pass in front of the uncle's body).
   - Kid: a visible spoon/stick (>=6 px thick, contrasting colour) in one hand, pot held low in the other, 2-3 clear up/down hits.

## Non-blocking (unchanged)
- Pinch hand shape in shot 8 reads as a claw; grey twigs in foreground.
