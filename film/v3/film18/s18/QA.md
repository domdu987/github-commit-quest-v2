# QA s18 (render team 5, film 18) — frames g1388-1426 (+6 handle each side: take.mkv g1382-1432, 51 frames), jimo_in NIGHT
Render: Cycles 12 samples, 720x1280, 2 threads, ~20 s/frame under load (15.9 s/frame alone), per-frame card re-placement (c18.py).

## Frame-diff (90x160 grey, mean abs diff x255, in-shot frames g1388-1426, n=38)
median **4.34**, p90 **12.13** (min 0.23, max 14.11). Target >= 4 / >= 12: met.
Camera: push 0.07/s + slide, four quick swings (pan +-6 deg, snap 0.94 on "จุดไฟ" g1417), fg none.

## qa_auto
PASS (QA_AUTO.md, phone_sheet.jpg).

## Brief items (TEAMS.md / QA_ART_SET_R2)
- NO lit tail before "จุดไฟ" 47.13 s (g1417): checked g1388-1416 every frame, tails carry unlit reed bundles, flame=-1. Torch in Tian Dan's hand is unlit until g1413, then lit (it is a torch, not a tail).
- Tails light in a ripple after "จุดไฟ": nearest ox at g1417, one more every 2 frames (6 oxen); tail flame variants 0/1/2 cycle every 2-3 frames, real warm light at the tails of the lit oxen (lit_pools). Flames visible on screen from g1417 to the end of the take.
- Ox cards re-baked from the current cast18 (set_work/cards deleted before the first render; short bronze blades, front/3-4 view).
- Tian Dan moved to (-13, 12) so the push does not run through him (set mark was behind the lens at the end of the push). Eye-line to the torch; head top above y 880 (head y approx 330-400 of 640 tile = 660-800 px).
- Set fixes: braziers near the lens skipped, reed jars hidden (they stood next to the lens), a little ground dressing in the foreground.
- Comic / bloodless: nobody touched by blades; oxen hop (0.06 D) when their tail lights.

## Checks (6 fps look + cut +-3 frames)
heads above y 880: yes. Hooves on the ground with contact shadow: yes. Props held (torch): yes. Mouths: still (no lip-sync here). Continuity: same wall holes (set_holes 12) and dress state as s17 / s19.
Deviation: the planned fixed marks for Tian Dan were replaced; camera moves are stronger than the plan's for the frame-diff rule.
