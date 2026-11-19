# QA s20 (render team 5, film 18) — frames g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), jimo_out NIGHT
Render: Cycles 12 samples 720x1280, 2 threads, ~25-35 s/frame with four renders sharing 4 cores (about 16 s alone). Cards re-placed per frame (c18.py).

## Frame-diff (90x160 grey, in-shot g1515-1595, n=80)
median **7.79**, p90 **14.32** (min 3.24, max 19.12). Target >= 4 / >= 12: met.
Camera: tracking beside the lane (cam (25,-47,1.6) -> look (5,-63,3)), push 0.07/s, whip-in pan (55 deg unwinding over 7 frames), four quick +-6 deg swings, one 0.92 snap.

## qa_auto
PASS. Only note: soft g1600-1601 (handle frames after the cut, not in shot).

## Brief items
- >= 3 visible tail flames in every frame: the herd (36 oxen, gallop 8 drawings at ~12 fps, phase and scale varied) runs across the frame; every lit ox carries the cast reed-tail flame plus an added tail flame card (3 painted variants cycled every 2-3 frames, warm pool + tail lights on the 6 nearest). Counted 3-6 flames on screen on the phone-sheet frames and in the 6 fps check.
- The 2 nearest oxen are yawed more toward the camera (card theta 50 deg instead of 34) so their tails and flames show behind the body.
- Oxen only run forward (-y toward the Yan camp), never turn back; fire is behind them (the far Jimo wall lamps and torch stakes).
- Ox cards re-baked from current cast18 (short blades, front/3-4 views); comic, bloodless, nobody under a blade.
- Caption band (y 880-950): ground only, mean low, no emitters (checked on the sheet); no head above... n/a (no humans).

## Deviations
- Camera pose differs from the plan's (look across the lane instead of down it) because the ox cards have no back view; a camera looking down the lane showed the cards' faces running away backwards.
- Tail flames are an extra painted card per lit ox (the set's flame_card did not show up at the tail positions), documented in c18.py.
