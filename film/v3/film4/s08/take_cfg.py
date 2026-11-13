"""take_cfg.py -- the numbers of take s08 for deliver.py."""
TAKE = "s08"
SHOTS = [8]
G0, G1 = 480, 593                       # [g0, g1): shot 8 = 16.00 .. 19.78 s
FIRST_G, LAST_G = 480, 599              # hard cut in from s07; 7-frame out-handle (in case s09 dissolves in)
PARTS = {1: (480, 510), 2: (511, 563), 3: (564, 599)}
PART_NOTES = {1: "8A eye-level two-shot: master near (right) points at the pagoda, smug; kenta far (left); bursts out laughing on 'hua ro' g 495 (static grin)",
              2: "8B snap punch-in g 508..514 to a low angle on the master: lip-sync ONLY here, on the quote (g 511 ->); points at kenta on 'ai nu' g 547",
              3: "8C cut (plan 18.7 s): three townspeople laughing and pointing at the pagoda, the rigid tower behind them; mouths static; out-handle g 593..599"}
CUTS = [(563, 564)]
TRANS_IN = {"type": "cut", "frames": 0, "from": "s07", "note": "hard cut on the new sentence (16.0 s)"}
TRANS_OUT = {"type": "cut_or_dissolve", "frames": 10, "to": "s09",
             "note": "out-handle g 593..599 rendered in 3D (8C camera keeps moving): usable for a 10-frame dissolve into s09; for a cut use up to g 592"}
TRANSITIONS = [{"at": 480, "type": "cut_in"},
               {"at": 508, "type": "snap_punch_in", "frames": [508, 514]},
               {"at": 564, "type": "cut", "from_part": 2, "to_part": 3},
               {"at": 593, "type": "out_handle", "handle": [593, 599]}]
SHOT_RANGES = {"8": [480, 592]}
SET_NOTE = "v3/set3d4/pagoda.py v2 DAY, nothing added"
DOF = {"8A": "master head (8.0, -15.6, 2.8), f 3.0", "8B": "same point, f 3.5", "8C": "woman2 head (4.45, -17.45, 2.7), f 3.0"}
CAST = "v3/cast4: master (master_point_tower -> master_laugh + lip-sync), kenta far (worried), merchant / woman2 / farmer (town_laugh_point)"
COMPARE = [("8A", 500, 11), ("8B", 530, 13), ("8C", 580, 15), ("8C", 590, 47)]
CUES = [
    (480, 480, "hard cut to the courtyard two-shot", "cut", {}),
    (480, 600, "courtyard ambience: birds, distant hammering from the tower, light chatter", "ambience", {}),
    (493, 500, "the master bursts out laughing (big belly laugh starts) on 'hua ro'", "laugh", {"peak_frame": 495}),
    (508, 514, "snap punch-in on the master (short whoosh), middle g 511", "camera_snap", {"peak_frame": 511}),
    (511, 596, "QUOTED LINE, the master's voice (lip-sync g 511..563 on screen): 'sao thi mai kham arai nia na, ai nu, phaendin wai thi diao ko lom'", "dialogue", {}),
    (545, 552, "finger jab toward kenta on 'ai nu' (kid)", "gesture", {"peak_frame": 547}),
    (564, 564, "hard cut to the laughing townspeople (plan 18.7 s)", "cut", {}),
    (564, 600, "townspeople laughing: three overlapping laughs (merchant chuckle, woman's giggle, farmer's guffaw)", "laugh", {}),
]
