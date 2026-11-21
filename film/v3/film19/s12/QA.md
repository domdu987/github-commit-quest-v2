# s12 QA (MERGED shots 12 + 13): film 19, WORKSHOP shop_clock NIGHT, set_clock(3) - one continuous take, no cut (QA_TEAM §I)
- Take g 929..1024 (96 frames, 720x1280, 8 spp). Shots: 12 = g 938..985 (31.26-32.85 s), 13 = g 986..1015 (32.85-33.86 s) with NO cut between them. In-handle g 929..937 (dissolve 11 f in from shot 11), out-handle g 1016..1024 (dissolve 11 f out into shot 14). take.mkv crf 6, first_g 929. QA_AUTO PASS. meta.json shots [12, 13], shot_ranges {12: [938, 985], 13: [986, 1015]}. The s13 folder is superseded by this take.
- Story: greying Harrison (default) taps a chisel at the H3 by candlelight (g 938-965). The camera makes a lateral whip pan along the bench (snap g 952..972 on "สิบ", caption g 960). At the PEAK of the whip (camera speed peaks at g 961-962, 30 px/frame) the SAME Harrison swaps to the old=1 look (white hair, spectacles, brown coat) at g 961, under a foreground wipe: a dark wood beam (a 0.42 D slab parented to the camera, 0.6 D from the lens) sweeps across g 957-965 and covers the centre of the frame at g 961, so the grey -> white change is never seen (g 960 grey, g 961 beam, g 962 white). Round-7 fix: the swap used to be at g 966 after the pan had settled, a visible pop. White-haired Harrison bends tired over the H3 (g 973-992), then on "จนผมหงอกทั้งหัว" (caption g 989, หงอก ~g 996) leans back and rubs his eyes with a sweat drop (g 993-1015+). He is always doing something (tapping, fidgeting, rubbing).
- Candle / light: the bench candle stub and its light sit on the foreground chest (always in frame), set_candles 1.0 -> 0.25 keyed every frame, flame emission and all lights keyed down over the whole take (luma falls). set_balance(g/30) every frame (H3 balances).
- Camera: ONE custom 22 mm path: start (2.2,-1.6,2.4), push 6 %/s, slide -60 px/s, the whip pan (k 1.05, shift 1.4 D), then the look point turns +1.0 D over g 985..1024 (camera turns, does not move), handheld sway 0.09 D at 1.5 Hz. The camera never passes x ~3.3 (the shop wall is at 4.25; an earlier version with arc / travel went through the wall and rendered black).
- Gate G: head width max 248 px (about 19-24 % of the frame height; well under 30 %), head centre y 548-592, head left edge >= 121, right edge <= 637: nobody cut by an edge, heads above y 880. No text, no DOF, no caption_shade, fixed mouth.
- Frame-diff in-shot (g 939..1015): median 5.60, p90 14.47 (per-take rule median >= 4, p90 >= 10 met). qa_stats (whole file incl. handles): saturation 0.70, brightness 66.8 (night; the conform grade lifts it).
- s/frame 17.2 wall / 33.8 CPU (two processes).
- Known: contact decal is on, but the legs still end in thin white stubs (cast rig limit). The right half of the frame after g 967 is the plain shop wall (the camera looks along the bench).

## Round 7 note
- Motion blur on the whip frames was tried (shutter 0.5-0.9) and dropped: qa_auto then lists the blurred frames under FAIL. The foreground beam alone hides the swap. QA_AUTO PASS; its only note is soft frames g 960-961 (the beam). Frame-diff in-shot median 5.60, p90 13.68. Only g 955-968 were re-rendered; everything else is unchanged.

## Round 8 (QA-art round 7: age gag as the joke, real whip, slump, leg stubs) - supersedes the age-swap notes above
- Hair stays GREY through the whip pan and until the word: at g 996 ("หงอก", caption g 989 + the word ~g 996) it pops WHITE (+ spectacles, brown coat: harrison19 old=1) with a puff (the puppet's `steam` fx over g 995-1002) and a squash (1.07/0.93) plus a small hop (0.06 D). The beam wipe / motion blur of round 7 are removed (no swap under the whip any more).
- The chisel stays in his hand the whole take: he taps it until g 992, slumps, and it hangs low in his right hand (angle -> pointing down) while the LEFT hand rubs his eyes. It never vanishes.
- Tired beat: real slump g 993-1000 (lean 8 -> -15 deg back, pitch back, head roll 8, squash 1.03/0.97), then the eye-rub (blink 2) with the sweat drop.
- Camera: the whip pan (g 952-972, shift 1.4 D) overshoots and then SETTLES BACK left (second move g 970-996, -0.9 D) with the look point turning +0.9 D: Harrison sits at the right of centre and the H3 (gold wheels) is in frame at his left while he rubs his eyes; the blank right-hand wall of round 7 is gone (it is a narrow strip). The whip peak is ~45 px per frame (a 120-180 px whip would take the 22 mm camera through the shop wall; I chose the swing-back option).
- Legs: Harrison's mark is 0.2 D right of the old spot so the foreground chest (with the candle and the lantern) hides his lower legs: no white stubs float in front of the chest any more.
- Face height / frame: head width max 229.5 px, head x 199-697 (nobody cut by an edge), always above y 880. Candle burn-down and the falling lights are unchanged.
- Frame-diff in-shot: median 5.31, p90 12.24. QA_AUTO PASS. qa_stats: saturation 0.72, brightness 59.9 (night). s/frame 18.0 wall / 35.3 CPU.

## Round 9 (QA-art round 8: head ran off the right edge at g 997-1012) - g 990-1024 re-rendered
- From g 990 the look point turns a further 0.45 D toward him (ramp g 990-998), so the whole figure (hair, bow, ponytail, both steam puffs) sits well inside the frame. Checked BY EYE on a crop of x 600-720 of every frame g 990-1024 (work/rightedge.png): only plain wall is in that strip, except a hairline sliver at x ~600 in g 1015-1017, so the figure's right edge never passes x ~602 (the detector's head-x range in the earlier round, 199-697, was wrong: it misses the outline and the puffs).
- Polish: the steam puff is held g 995-1008 and pumps (t animated); the slump now tilts back (pitch -0.30, head roll 2 deg) rather than sideways. The puff size is the puppet's own (not scalable without editing the cast), so it is not 1.5x bigger.
- Frame-diff in-shot: median 5.45, p90 12.49. QA_AUTO PASS. Frames g 929-989 are unchanged from round 8.

## Round 10 (QA-art round 9: the slump tilted his card into the plaster wall at g 997-1013) - g 990-1024 re-rendered
- Cause: his sprite card (about 4 D wide) met the right plaster wall (x 4.25) while he leaned back; the wall cut the card with a straight line. Fix: while he slumps (g 990-1000, eased) his mark steps 0.3 D away from the wall (x 3.43 -> 3.13); it reads as him slumping away from the bench. The step is applied only from g 990, so g 929-989 are unchanged.
- Checked BY EYE on a crop of x 450-720 of every frame g 994-1016 (work/wallcheck.png): ponytail, bow, both puffs, the whole head and the sweat drop are intact, no straight cut, nothing meets the wall.
- Light: a small exposure lift for the payoff (all lights x1.6 over g 990-1000, in the keyed dimming); mean brightness 59.9 -> 65.7 (qa_stats). The overall trend is still a darker room than the start, with a brighter payoff. No separate rim light.
- With him 0.3 D further from the chest his white stockings and shoes show beside the chest (standing on the floor with the contact shadow) instead of hiding behind it.
- Frame-diff in-shot: median 5.94, p90 13.48. QA_AUTO PASS.

## Last pass (render19 team8): handheld sway removed
- `SWAY` default 0 (no oscillation). Candle flicker is brightness only (no camera). To keep frame-diff, a smooth one-way push 0.085 / slide -70 px/s was added (eased, no oscillation).
- Frame-diff in-shot: median 4.37, p90 12.74. qa_jitter: overall 0.7 px, no second > 2.0 (JITTER.md). qa_auto PASS. GROUND.md: characters pass.
