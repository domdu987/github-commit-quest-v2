# s08 QA_TECH: FAIL
Shot 8, HALL hall_low DAY, take g536-669 (handles 9+9, both sides hard cut), 6 fps + cuts g545/g661 +-3 checked. qa_auto PASS. No text, no black/magenta, no blur, no frozen run (min pair diff 2.37), no pop. Heads: face centre y 560-700 in band; see issue 4 for the wig.
## Issues
1. g545-660: frame-diff median 3.38, p90 5.93 (re-measured 3.38 / 5.92) vs target >= 4 / >= 12. FAIL. Fix: stronger push (>= 10 %/s) and a real snap on "นาฬิกาเนี่ยนะ" (g637): ease x2+ over 13-15 f, plus a slide.
2. g611-621: laughing grin (teeth, closed "^ ^" eyes) starts at g611; mouth window is 20.80 s = g622 +-4.5 f. Mouth moves 11 frames (0.37 s) before the window (also a first small mouth change at g602). Fix: start the laugh_cycle mouth no earlier than g618 (keep the bounce/eyes earlier if wanted, mouth stays flat before).
3. g545-600 (the turn): plan "turns toward camera"; he already faces the lens from g536, only a head tilt; pose almost static for 55 frames (pair diffs 2.4-3). Fix: start side-on (looking at the telescope/Board) and turn to the lens by g598.
4. g643-669: wig lappets hang to y ~ 990 (g656 chin at ~ 770, wig bottom 990), i.e. the head sprite crosses y 880 (hard rule: whole heads above 880). Fix: pull the camera back or tilt down 12 % at the end of the snap so the wig bottom stays < 880 (head centre must stay in 450-760).
5. g571-606: no visible contact shadow under the shoes (white legs on the rug at y ~1150-1180 at g586), reads floating. Fix: contact decal.
6. g611-641: a stray white line floats at his sleeve/wrist (g611-641) and the planned "point [640,661]" is not visible (hand out of frame / behind the wig). Fix: raise the pointing arm into frame at g640.
7. g646-669: head grows to ~65 % of frame width and the left wig lappet is clipped at the frame edge at g656-666. Fix: reduce the snap scale or slide camera left 40 px.
8. meta.json g1 = 661 is exclusive (plan g1 = 660). Note only.
