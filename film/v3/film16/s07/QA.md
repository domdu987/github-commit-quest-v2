# s07 QA: film 16, shot 7 (STUDIO studio_window, DAY: the idea, coil + magnet + spark), re-render after the TAKE gate
- Frames g 392..483 (92): shot g 401..474 (13.37-15.84 s), 9 handle frames each side. Hard cut in; the shot 8 dissolve (15 f) is centred on g 475, handle g 475..483 continues the move.
- take.mkv 35.1 MB (libx264rgb crf 6), 720x1280, 6 spp, 2 threads: 11.2 s wall / 21.6 s CPU per frame.
- Frame-diff in-shot: median 6.06, p90 15.53 (target 4 / 12). qa_auto PASS.
- Fixes for the gate's blocking notes:
  1. Coil: the left hand now reaches out (arm_l hand (-0.86, 0.34)) holding the wire coil clear of the body, the right hand holds the magnet; both visible g 455-483.
  2. Window: the runtime dresses the outside (shot.py raise_road): near rooftops hidden, street / fields / trees lifted 12 D, plus a 10 m wide road ribbon, so the long road runs to the horizon between fields (clearest g 401-445).
  3. Eye-line: Morse now stands LEFT of the window facing it (yaw 0.45-0.55, gaze out to screen-right), not in front of it with eyes to camera.
  4. Grin: expr excited with mouth "smile" (closed), no teeth.
- Beats: g 401-445 he gazes out at the road; g 446-459 arms rise (coil + magnet); g 465 "พริบตา": blue spark at the magnet poles + snap push x1.8 with a 0.9 D pan; mouth still.
- Camera: pull back 8 %/s + slide -115 px/s + arc -18 deg/s + crane down 40 px/s; the canvas stack passes the lens as FG g 440-474 (hides his legs at the end).
- Notes: the spark is the cast card's glint (~40 px); the road reads as a pink ribbon, strongest in the first second. Heads 159-216 px, centre y 509-587, bottom <= 678.
