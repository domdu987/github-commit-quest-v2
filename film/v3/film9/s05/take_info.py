"""take_info.py -- the take-specific data deliver.py / qa.py read (film 9, take s05 = shots 5-7)."""
TAKE = "s05"
SHOTS = [5, 6, 7]
G0, G1 = 270, 507                      # plan 9.01 s .. 16.90 s (round(t * 30)); g1 = first frame of shot 8 (next take)
FIRST_G, LAST_G = 264, 512             # 6 handle frames each side, rendered in 3D
RANGES = {5: (264, 338), 6: (339, 432), 7: (433, 512)}          # raw folders (incl. handles)
SHOT_RANGES = {5: (270, 338), 6: (339, 432), 7: (433, 506)}     # the plan's shots
CUTS = [(338, 339), (432, 433)]
TRANSITION_IN = {"type": "cut", "frames": 0, "note": "in-handle g 264..269 = shot 5 set-up continued backwards (general still off screen left)"}
TRANSITION_OUT = {"type": "cut", "frames": 0, "note": "out-handle g 507..512 = shot 7 set-up continued (workers keep laughing)"}
TRANSITIONS = [{"at": 270, "type": "in", "handle": [264, 269]}, {"at": 339, "type": "cut", "note": "plan cut shot 5 -> 6 at 11.30 s"},
               {"at": 433, "type": "cut", "note": "plan cut shot 6 -> 7 at 14.44 s"}, {"at": 507, "type": "out", "handle": [507, 512]}]
SETUPS = {
    "5": {"g": [264, 338], "set": "cauldron area, DAY; custom camera from the site side west of the preset (-9.6, 24.6, 5.6) -> (-10.3, 23.6, 5.4), look (-11.8..-12, 12, 2.2), 22 mm: wok + steam, lin on his platform screen-right of the wok"},
    "6": {"g": [339, 432], "set": "two_shot_low, DAY; the preset camera pulled back 2.4 D and raised 0.9 D so the general stands in front of the plank stack (feet visible), look-at panned so lin clears the right edge: (-4.3, 24.6, 2.7) -> (-4.6, 24.0, 2.65), 22 mm. general a little in front of two_shot_general (-4.5, 19.4), lin on two_shot_lin (-7.6, 16.4)"},
    "7": {"g": [433, 512], "set": "site, DAY; closer medium on three workers (QA_TECH 7) from the tents west of the cauldron: (-25.1, 24.9, 3.6) -> (-24.8, 24.4, 3.55) look (-13.5, 13.5..13.8, 1.0), 22 mm; lin small at the cauldron between them, gate tower + scaffolds behind"},
}
EVENTS = {"general_walks_in": [264, 296], "general_stops_surprised": [296, 300], "general_belly_laugh": [300, 432],
          "quote_lipsync": [333, 432], "general_points_and_mocks": [351, 412], "second_laugh": [418, 432],
          "cut_to_two_shot": 339, "cut_to_workers": 433, "workers_laugh_peak_khanom": 488}
SET_NOTE = ("heights lin 16 / general 16 keyed every frame (before the race; month 1 = 18 / 21 in shot 10), set_cauldron_steam 1.0 and set_flames "
            "keyed every frame; no set edits")
CAST_NOTE = ("lin (shot 5, 7: STORY9 lin_stir on the lin_stir platform mark, mirrored so he stirs into the wok, hands on a 24-frame ellipse; "
             "shot 6: lin_calm, arms folded, mirrored to look at the general), general (shot 5: walk cycle 18 frames -> surprised -> "
             "general_laugh; shot 6: general_laugh -> general_mock pointing at lin -> general_laugh), worker_a / worker_b laughing, "
             "worker_c pointing (mirrored, points back at lin)")
MOUTH_NOTE = ("only the general's quote moves a mouth: g 333..432 (narration 10.98..14.43 s, 'ข้าวเหนียวเนี่ยนะ เอ็งจะทำขนมให้กำแพงกินเหรอ!'), "
              "talk_mouth driven by the narration RMS envelope (smile when silent). Before g 333 the laugh mouth is a static open talk_b; "
              "lin and the workers have static mouths (smile / laughing).")
CUES = [
    (264, 513, "Ming construction site by day: distant hammering of masons, the crackle and roar of the stove fire, the cauldron bubbling, steam hiss", "ambience", {}),
    (264, 296, "heavy armoured footsteps (lamellar armour clinking) striding in from the left", "foley", {"peak_frame": 290}),
    (296, 300, "the general stops short: armour clank, a surprised 'hm?'", "accent", {"peak_frame": 298}),
    (300, 338, "big booming belly laugh (the general), armour rattling with each laugh", "voice_fx", {"peak_frame": 310}),
    (339, 339, "cut to the low two-shot: ambience continues", "cut", {}),
    (351, 412, "the general points and mocks (narration carries the quote); a little 'wah-wah' comic tuba sting under 'ทำขนม'", "accent", {"peak_frame": 384}),
    (418, 432, "second burst of laughter from the general", "voice_fx", {"peak_frame": 424}),
    (433, 433, "cut to the workers", "cut", {}),
    (433, 512, "a crowd of workers laughing and jeering (walla), one slaps his knee", "walla", {"peak_frame": 488}),
    (486, 492, "comic 'boing' sting on 'ไอ้ช่างขนม'", "accent", {"peak_frame": 488}),
]
