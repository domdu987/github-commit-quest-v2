# QA s17 (film 13 shots 17-19, the false payoff), take g 1104..1305, shots 17 g 1110-1172 / 18 g 1173-1254 / 19 g 1255-1299 (cuts at the plan g = round((t+0.10)*30); handles 6 in / 5 out)
Mean 7.5 s/frame wall (12 samples, 720x1280, 2 threads, two processes in parallel).
- qa_auto: PASS (QA_AUTO.md). The "no visible change" notes for g 1107 and 1297 are the take's outer boundaries (cuts to other takes).
- Heads: all cast heads above y 880 (cyan line on phone_sheet.jpg); rich head centre about 0.2-0.4 H in shot 17 (close, large), about 0.3 H in shot 19 (three-shot).
- Mouth: rich mouth flat in 17 and 18 (18: he is out of frame); shot 19 talk_mouth only g 1253..1301 (quote 41.72-43.22 s = g 1255..1300, +-2 frames).
- Cup: shot 17 cup and saucer in his hand (pose rich_look_window_smug); shot 19 raised in the near (right) hand toward the gentleman, little bob.
- Tea: set_tea_ripple(0) keyed on every rendered frame: mirror-still, window reflected in the surface; shot 18 slow push (lens 30, camera moves every frame).
- Street through the window: 44 cast13 townsfolk cards (real cast13 sprites, PropCards) below; chandelier hidden from camera only.
- Lift continuity: the suite room has no hotel, so lift state (h 0.4) is not visible from inside, as planned.
## Deviations from the plan
- Plan lists MORNING (17) and DAY (18, 19): the suite location only has the SUITE light, used for all three (same blue-sky window).
- Shot 17 is a medium of the rich man standing at the window (not the high suite_window look-down, which shows no actor); shot 18 camera is above the table (tea surface visible, passes the blur check) rather than the low tea_close preset.
- Shot 19 uses rich_look_window_smug re-posed (cup raised, mouth driven) instead of rich_mock_point (pointing), because the plan asks him to raise his cup; lady and gentleman guests stand beside him.

## Round 2 (director: QA-art + QA-tech notes)
- Cuts moved +3 frames to the plan g (1110 / 1173 / 1255, end 1300); Q2 mouth window g 1255-1300 unchanged in narration time.
- Sky: stepped lime cloud slabs replaced at runtime by a cloudless gradient with soft clouds (work/sky_clean.png).
- Dressing / camera: cameras lowered and tilted up (rug about 20-25 % of the frame); shot 17 now shows wallpaper wall + painting, shot 19 shows the chandelier and velvet window frame; table/cups/tea hidden from camera in 17 and 19 (removes the cropped cup at the edge), kept in 18.
- Shot 17: morning feel (sun lower, warmer, brighter, keyed per frame); he is three-quarter to the window, gaze out of the glass; hand and fingers on the cup visible at chest height.
- Shot 19: cup raised on his open outer side (away from the gentleman), clear gap, no arm over any face; lip-sync inside Q2 (g 1257-1301).
- Shot 18 kept as is (new sky only).

## Round 3 (director: QA-art keys2, shot 19 only re-rendered; 17 and 18 untouched)
- Shot 19: rich in the left third, cup + saucer fully in frame beside his face with the hand on it, camera closer (lens 21) and tilted down so the ceiling is about 15 %; lady and gentleman fully in frame. Lip-sync unchanged (g 1257-1301).
