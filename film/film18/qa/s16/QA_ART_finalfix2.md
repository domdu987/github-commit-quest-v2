# QA FINAL-fix2 s16: PASS

Reviewer: QA-art, FINAL-fix2, 2026-11-20. Take `take.mkv`, 120 frames, g1195-1314 (in-film g1205-1308).

What I checked:
- the y 740-980 band every 3 frames, with lines at 860/880/950;
- quarter-scale sheets every 4-6 frames;
- the team phone sheet;
- old (the failed FINAL-fix take) against new in 2x crops at 12 frames;
- the ladder and digger at 1:1, g1232-1259;
- a per-frame diff of all 120 frames against the failed take and against the passed round-4 take.

Evidence is in `/tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qafix2/`.

## Blocker B3: GONE
- The girl has been removed from the whole take, handles included, so there is no pop.
- The spot where she stood (behind the basket, then behind the rubble) now shows clean basket, rubble, wall and ladder. There is no gap and no ghost. Her contact shadow went with her.
- No face enters y > 860 on any frame. The only white in the band during the caption "รูหลายสิบรู" is the elder's beard, which was already accepted, and the ground glow quad.

## Beat on a phone (holes dug in the wall at night): READS
- Six diggers swing picks at the lit base of the wall.
- Breaches open one after another from about g1214, each with a dark outline and a warm glow. By the end there is a row of them along the wall, and they stay in frame through g1308.
- On the phone sheet the breaches and diggers sit just above the caption line, and the caption does not hide them. Losing the girl costs the beat nothing, because she was half-hidden and not digging.

## Look matches the passed take
- The diff against the passed round-4 take shows only render noise outside the original girl's region. Night palette, moon-blue sky, orange wall glow, camera move, hole timing and the diggers are all the same.

## Hard rules
- Pole through a face: none. The ladder at g1238-1253 runs behind or beside the black-haired digger's head, and the pick heads stay above the heads.
- Half-cut main character: none. Edge-clipped figures are extras, for example the black-haired digger at the left edge at g1290-1296.
- Floating: none.
- See-through: none.
- Pop-in/out: none.

## Notes (non-blocking, already in v1)
- N-s16-1: the pale needle shards on the ground and the flat white-yellow glow quad on the ground (g1299-1314) are still there. Clean them up only if a re-render happens for some other reason.
