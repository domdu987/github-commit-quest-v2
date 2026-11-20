# QA s01 (film 18, team 1) — hook: Tian Dan dresses the ox (round-2 rework)
Take: g 0-77 (78 frames), first_g 0, jimo_in NIGHT, 720x1280, 12 samples, ~17 s/frame. transition_in: start of film. No handles (s02 is a cut).
Round-2 changes (director ALL_TEAMS, QA-art, QA-tech): custom camera path with a real eased push + 1.3 D truck, TWO HELD punch-ins at g 8 and g 50 (+14 %, 3 frames, hold) instead of in-out pulses; Tian Dan stays about 35-55 % of frame height with torso, coat and the ox's head in frame, clear of both edges; he stands beside the ox with the silk running onto its back and the ox's own coat growing 55 -> 100 % (not a free flag), his head turned and pupils set toward the ox; navy dig tools / baskets hidden; fg lantern (emissive paper lantern + warm point light) bottom-right at 1.6 D from the lens for the whole shot, no navy planks; 4 extra dressed oxen in the yard; tug rhythm 2.2 Hz.
## Frame-diff (90x160 grey, in-shot)
median 5.18 (>= 4 OK), p90 7.04 (target >= 12: NOT MET), min 1.44, max 10.43.
## Checks
qa_auto PASS. Heads above y 880. No mouths move, no text, no flames.
Known: p90 short of 12 without pulses; the lantern reads as a plain orange can with only a faint ground pool; the fg prop is camera-parented so it does not slide across (the director's parallax recipe wants a world-fixed prop).
