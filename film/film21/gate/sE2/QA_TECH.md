# QA-tech sE2 (team6 5830dbc)

**Verdict: FAIL** (2 blocking issues). Judged on content only; colour and exposure are normalized at the conform.

Count-word film g: ข้ามมาสิบคน 884, บนเนินเงียบ 912, ข้ามมาร้อยคน 938, ยังเงียบ 966, ข้ามมาเป็นพัน 985, ก็ยังเงียบ 1018, F cut at 1044.

## Beat table
| g | narration | what the frame shows | reads at phone size? |
|---|---|---|---|
| 885-911 | "ข้ามมาสิบคน" | Camera ahead of the column on the bridge mouth. About 8-10 crimson footmen with grey helmets, big faces, walking. Sky and far camp above. | Yes. Count of about 10 is clear. Faces about 6-8 % of frame height, well under 35 %. |
| 912-937 | "บนเนินเงียบ" | Column marching straight at the camera. No hill and no Scots in frame (horizon shows the English camp and far mountains). The footmen look at the lens, so the glance up at the hill does not read. | Count reads. The "silent hill" half does NOT read. |
| 938-965 | "ข้ามมาร้อยคน" | High-angle view down the bridge: two files of about 30 plus a few stragglers on the grass. The lower 50 % of the frame is empty dirt. | Reads as a long column, not "100". Weak growth step from the first beat. |
| 966-984 | "ยังเงียบ" | Camera tilts down to bare ground. Camp and hill gone. | No story. Empty dirt. |
| 985-1000 | "เป็นพัน" | g990-993 is almost pure grass and dirt with a blur streak. This is the crane move, not a hold. | Soft frames are a dead patch exactly on the key word. Fails the count. |
| 1001-1030 | crane top | Meadow with about 60-120 small real cards plus a block of 40-60 crimson pins (white-topped cylinders, static). The hill is now visible, tree-covered, with no Scots and no banners. | Crowd reads as "a lot", but the pins look like bowling pins. Late: the growth lands about 0.5 s after the word. |
| 1031-1044 | "ก็ยังเงียบ" | Same wide view, hill empty. Cut to F. | The "unbothered Scots" idea is not shown. |

## Issues
1. **BLOCKING, g885-1044: no Scots at all.** The hill is only in frame from about g1000. It has no saltire banners and no Scots figures, so "the hill is silent / waiting, unbothered, blue saltire" never reads. This is the point of the beat. Fix: keep the hill in the upper third of the frame from the start. Angle the camera back toward Abbey Craig and place about 8-12 Scots on the crest, idle (scratching, leaning on spears), plus 2-3 large saltire banners (blue with white saltire, about 90 px wide at the 44 m crane top). The banners can be oversized and the poles lengthened so they read at phone size. They must be the only blue besides the sky and river.
2. **BLOCKING, g960-1000: the count does not grow on the words, and the camera looks at bare ground.** The camera pitches down to dirt (g966-995, near-empty frames) while "ร้อยคน" and "เป็นพัน" are spoken. The thousand only appears at about g1000. Fix: keep the camera looking along the column. Add a visible step at g938 (about 100: dense block on the meadow beside the bridge). Start the crane at about g975 so the crowd fills the frame at g985. Hold the crane top clear and sharp from g1000 to g1044. Never aim at empty grass.
3. **BLOCKING if not fixed with item 2, g990-993: soft and streaked frames** from the fast crane. Judge: they are the empty-dirt patch, so they are not acceptable here. Slow the ease through g985-1000 and keep the crowd in frame, so the blur has content.
4. NON-BLOCKING, g1001-1044: crimson placeholder pins (cylinders with white caps) read as bowling pins and do not act. Fix: swap for small footman cards, or add a bob and phase offsets, and shrink the block so it blends with the real cards.
5. NON-BLOCKING, g912-965: footmen stare at the lens. Fix: turn the first 8 heads toward the hill (profile or three-quarter) at g905-935 and add a nervous glance and shuffle.
6. NON-BLOCKING, g885-965: lower 40-50 % of the frame is empty dirt. Fix: lower the camera pitch or move the horizon down so heads sit in the middle third.
7. NON-BLOCKING, g1020-1044: the left-edge crowd cards are partly cut by the frame edge at the crane top (the pin block touches x=0). Fix: pan the camera 3-5 m right.

## Checks that pass
- Heads are above y 880 in all frames. Nothing floats. Footmen cast contact shadows.
- No face is over 35 %. The English are crimson only, with no blue on them. Bloodless, nobody speaks.
- Rhythm (median 8.24, p90 18.86) is acceptable.
- Camera clearance: no wall or object clipping seen.
