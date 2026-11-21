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

## Round 3: FAIL
Checked 6 fps + cuts g545/g661 +-3 (take g536-669), qa_auto PASS. No text, no black/magenta, no frozen, no blur. Heads centre y 560-700, wig lappets end <= y ~ 830 (< 880): OK.
Earlier issues: R1-1 NOT FIXED; R1-2 mouth FIXED (flat g602-621, first opening g623, inside the g622 window); R1-3 turn FIXED (starts in 3/4, faces lens by g~560); R1-4 wig below 880 FIXED; R1-5 shadows faint, NOTE; R1-6 pointing arm now visible at the right g646-660 but weak, NOTE; R1-7 left lappet inside, FIXED.
1. g545-660 (R1-1): frame-diff (take.mkv, 90x160 grey bilinear, g546-660) median 3.82 (< 4), p90 6.60 (< 10); deliver framediff.json says 3.54 / 6.22 and QA.md reports it as a deviation. The director's per-take rule is median >= 4 and p90 >= 10: FAIL. Fix: real snap on "นาฬิกาเนี่ยนะ" (g637, x2 over 13 f, eased) plus >= 10 %/s push and a slide, orbit past the bookcases without hiding his face; re-measure.
Notes: meta g1=661 exclusive.

## Round 5: FAIL
Checked 6 fps + cuts g545/g661 +-3 (take g536-669), qa_auto PASS, no text/black/magenta/frozen/blur. Heads centre y 560-700, wig <= y ~ 830. Mouth: flat until g622, first open g623 (inside g622-781 window), OK. Frame-diff g546-660: median 4.07 (OK) / p90 7.15 (< 10).
Earlier: R3-1 median now passes, p90 NOT FIXED.
1. g545-660 (frame-diff p90 7.15 < 10): only the slow push, no accent. Fix: add the eased snap on 'นาฬิกาเนี่ยนะ' (g637, x1.8-2 over ~13 f) and a short slide so about 10 % of frames reach diff >= 10; keep his face clear of the shelves; re-measure.
NOTES: foot shadows faint; mark moved back + Board chair hidden accepted.

## Override review (independent Opus)
**DISAGREE.** Checked 45 frames (every 3rd, g536-669) plus my own diff of take.mkv.
- Motion is present: continuous orbit (window to bookcases), push, snap at g637. 0.5 s-span diffs stay 21-38 throughout, so no hold over 1 s and no static feel. The laugh bounce reads.
- The stated cause is wrong. Frames are not low-contrast: grey std is about 54 (90x160). p90 is low because the camera moves at one even, gentle rate. Only g640-645 (6 of 115 pairs) reach 10 or more. The snap is the only accent.
- Fix (no extra travel into the table): use FOV punches rather than dolly. (1) Add a punch-in x1.15-1.2 over about 8 f at the laugh onset (g603-611), framed up so the wig stays above y 880. (2) Make the g637 snap faster and longer, so that 12 or more pairs reach 10 or more. Re-measure.

## Round 6 (director QA-tech): PASS
Take g536-669 (134 frames, 720x1280, 30 fps). Frames extracted at 6 fps (/tmp/qa19_s08/p) plus every frame g600-645 (/tmp/qa19_s08/g600_645), all frames in /tmp/qa19_s08/all (index = g - 536). Contact sheets checked at 6 fps and g600-645.
1. Mouth (window starts 20.80 s = g624 on the caption clock, g627 with the +0.10 s narration offset; +-0.15 s = g622-631): flat slab mouth g536-610 (smile line at g609), a thin tilted slab g611-622, first real opening g623 (grin/eyes shut), full "ah" g625-631 and from g646 to the end. First open is 4 f before g627 and inside the g622 window of meta.json: PASS. NOTE: g611-621 the slab mouth is slightly wider/tilted (head roll in the punch), not an open mouth; I count it as flat.
2. Wig and head bottom: lappets end <= y ~ 835 by a white-mask upper bound (visual ~ 810 at g641) on every frame, all < 880: PASS. The gown and jacket cross 880 (body, not head).
3. Face height: face disc ~ 210-270 px (16-21 % of 1280, meta head_px 146-274). At the punch peaks (g609-621, g639-645) the face is <= ~ 22 %. Wig + face together reach ~ 540 px (~ 42 %) at g639-645: PASS for the face rule, NOTE only if the rule is read as head including wig.
4. Edges: lappets/wig stay inside the frame on every frame; legs and shoes are cut by the bottom edge from ~ g630 (low-angle crop, calves cut, nothing cut in half): PASS.
5. Floating: soft contact shadow under shoes g590-630; feet leave the frame from g632, no floating: PASS.
6. Pops/black/frozen: min frame mean 59 (no black), min pair diff 2.27 (no frozen), no magenta. The g603-611 punch is a continuous zoom plus roll with a bounce impulse; the largest step is g609->610 (13.7), settling at g611 (4.9). The g637 snap is a smooth eased push g637-644 (pairs 9.1 / 13.9 / 17.6 / 19.7 / 22.3 / 17.6 / 14.7), no discontinuity: reads as intentional camera moves: PASS.
7. Frame-diff (90x160 grey, bilinear, g546-660, 115 pairs): median 4.48 (>= 4), p90 10.72 (>= 10), max 22.3, 15 pairs >= 10: PASS. (Round 5: 4.07 / 7.15.)
Earlier issues: R1-1/R3-1/R5-1 FIXED (punches + snap). R1-2, R1-3, R1-4, R1-7 stay fixed.
NOTES (non-blocking): (a) small white lace-cuff bars at the sleeve (g611-641) look detached from the dark sleeve (R1-6), gone when the arm rises g646+; (b) the sheet "sections B and G" of QA_TEAM.md: no section G exists (only A-F); B and A were applied; (c) meta g1 = 661 is exclusive; (d) the pose step at g609->610 is the sharpest single-frame change, acceptable as the laugh punch.

## Round (camera-shake pass, film-13 rules): PASS (4 non-blocking notes)
Take s08 (HALL, g545-660, handles g536-669), re-rendered by team 4 for camera shake. Judged only by film/skill_film13/QA_TEAM_film13.md (base checklist + §B). My frames: /tmp/qa19_r21/s08/gNNNN.png extracted from take.mkv (g600 byte-identical to /tmp/qa19_ov/s08). I ran qa_auto myself (python3 qa_auto.py take --cuts 545,661 --first_g 536): PASS (only the note "planned cuts with no visible change within +-2: g545, g661" because the handle frames are rendered in-camera; magenta 0.0 %). qa_jitter reproduced: 2s 7.5 px, 3s 8.8 px, median 2.82. GROUND.md PASS (15 rows, 0 FAIL).
Where the remaining qa_jitter number comes from (checked, not trusted): I tracked static background (bookcases, window frame, ceiling, floor) with the actor masked out (wig / coat / vest colour mask closed and dilated 41 px, LK features + RANSAC similarity fit at 720x1280, /tmp/qa19_r21/bg.py), then took the second difference of the camera's image-centre shift per frame, seconds aligned to the take start like qa_jitter:
| second (take) | g | camera median |d2| (px) | p90 | max (g) | camera speed px/f |
| 0 | 537-566 | 0.57 | 2.16 | 3.0 (g541, handle) | 4.7 |
| 1 | 567-596 | 0.39 | 0.73 | 0.9 | 3.5 |
| 2 | 597-626 | 0.12 | 0.64 | 1.0 | 2.3 |
| 3 | 627-656 | 0.09 | 4.39 | 5.7 (g639, the planned snap pan g637-646) | 2.6 |
Overall camera median 0.27 px (equals team 4's actor-hidden 0.27). In the two seconds qa_jitter flags (2 and 3) the camera's own jitter is 0.12 and 0.09 px; the only frames with camera |d2| > 2 px are g540-541, 551-552, 557 (<= 3.0 px, handle / first second) and the planned snap g637-646. So the remaining 7.5 / 8.8 px is the actor (qa_jitter's whole-frame phase correlation locks onto the large laughing figure), not the camera: confirmed.
Does the laugh bounce read as shake or as a laugh? As a laugh. Tracking the wig top (g596-644): vertical bounce at 3.4 Hz, detrended peak-to-peak ~70-100 px of 1280 (5-8 % of frame height, +-20 px at phone size), while the bookcases, window and ceiling behind move smoothly (camera 0.1 px second difference). A moving subject over a steady frame reads as a belly laugh; it would read as shake only if the background moved with it. If the client still calls it shaky, the cheap lever is the bounce amplitude (about -30 %), not the camera.
Checklist:
- Blur/DOF: none; Laplacian variance median 184, min 127 (g669, close-up); sharp.
- Heads below y 880: none (wig top y ~210-410, chin <= ~600 of 1280 even in the g650-660 close-up).
- Clipped sprites/props: in the last ~1.2 s (g~650-660, the quote punch x1.14) the figure fills the frame and the feet/legs leave the bottom edge: a crop from the punch-in, not a clipped sprite; nothing cut mid-face.
- Floating feet / contact shadows: feet on the carpet with contact shadows in g536-640 (sheet); GROUND PASS; close-up has no feet in frame.
- Pops/jumps outside cuts: none. Frame-diff in shot g546-660: median 5.05, p90 10.47, max 27.4 (the planned snap g637-640), min 3.00. Ratio jumps g608 (laugh-start punch, 3.8 -> 10.5 over 6 frames, eased), g617/g622 (bounce), g637 (x2.28, the snap on the quote word 21.14 s, planned) are all the eased one-shot punches / planned snap. No black/blank/magenta frames (luma 67.0, per frame 58.9-82.7; saturation 0.704). No frozen runs (nothing under 0.3).
- Continuity: s07 g543-544 (three astronomers, hall_window, the mocker on the left with the pointing arm) -> s08 g545 (low angle hall_low, the mocker alone, same blue star-spangled coat, red vest, wig, glasses) is the planned hard cut; s08 g659-660 (close-up) -> s09 g661 (medium, same actor/costume, same hall) planned hard cut. Eye-lines and lighting (DAY, warm candles) consistent.
- Plan coverage (shot_plan row 8, 18.17-22.02): turn toward camera, belly-laugh bounce, quote "นาฬิกาเนี่ยนะ!" with mouth from 20.80 s, low angle with push and snap on the quote: all visible (turn g536-600, laugh g598-640, quote g637, mouth window g622-669).
- Mouth: mouth open in the belly-laugh pose g598-640 is the laugh expression (meta: expression mouths only); lip-sync mouth moves only in the quote window (g622-669). OK.
- Nobody still > 1.5 s: the actor moves throughout.
Numbered notes (non-blocking): 1. qa_jitter will still print 7.5 / 8.8 px for seconds 2-3: it is the 3.4 Hz laugh bounce, verified camera-clean (0.12 / 0.09 px). 2. Bounce amplitude 70-100 px p2p; reduce ~30 % if the client reads it as shake. 3. g650-660 close-up crops the legs (brief punch, acceptable punctuation). 4. Luma 67 / saturation 0.70 (deep red hall); film-13 has no luma rule.
Verdict: PASS.
