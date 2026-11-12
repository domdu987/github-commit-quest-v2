#!/usr/bin/env python3
"""deliver.py -- take s04 (shots 4, 5): frames/, take.mkv, meta.json, cues.json, contact.jpg, work/qa.txt.  python3 deliver.py"""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tk  # noqa: E402
_sp = importlib.util.spec_from_file_location("s04shot", os.path.join(HERE, "shot.py"))
S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)

G0, G1 = S.RANGES[4][0], S.RANGES[5][1]                     # 204 .. 366
D0 = S.G_S5 - S.DISS // 2                                    # 300
order = [(4, G0, D0 - 1), (5, D0 + S.DISS, G1)]
dissolves = [(4, 5, D0, S.DISS)]

cues = [tk.cue(G0, S.WHIP_END, "whip pan in from the town (whoosh, braking), lands in the bell chamber", "whip", peak_frame=G0)]
cues.append(tk.cue(S.G_S4, S.G_S5 + 5, "bell chamber: three ringers haul the ropes; bell swinging hard (bells loop, rope creak on every haul)", "ambience"))
for g in range(S.G_S4, S.G_S6 + S.H_OUT):
    if (g - 200) % (S.PERIOD // 2) == S.PERIOD // 4:   # bell at the end of each swing: the clapper strikes
        cues.append(tk.cue(g, g, "bell strike (big bronze bell, %s)" % ("close, in the chamber" if g < S.G_S5 else "far, across the town"),
                           "bell", impact_frame=g))
for tab, where in ((S.FLASH4, "seen through the north arch, the chamber lights up cold white"), (S.FLASH5, "forked bolt over the hills, far from town")):
    for g0, seq in tab:
        cues.append(tk.cue(g0, g0 + len(seq), "lightning flash (%s)" % where, "lightning", impact_frame=g0))
        cues.append(tk.cue(g0 + 6, g0 + 40, "thunder (rolling, %s)" % ("close crack" if tab is S.FLASH4 else "far rumble"), "thunder"))
cues.append(tk.cue(S.PUNCH[0], S.PUNCH[1], "snap punch-in on padre hauling his rope, lands on 'tong ti rakhang rua rua' (g %d)" % S.G_RUA, "camera_snap",
                   peak_frame=(S.PUNCH[0] + S.PUNCH[1]) // 2))
cues.append(tk.cue(D0, D0 + S.DISS, "dissolve to the town in the storm", "dissolve"))
cues.append(tk.cue(S.G_S5, G1 + 1, "storm over the town: wind, distant bells still ringing from the campanile", "ambience"))
cues.append(tk.cue(S.G_S6 - 6, G1 + 1, "dissolve out to the vault (shot 6)", "dissolve"))
cues.sort(key=lambda c: c["frame"])

meta = dict(shots=[4, 5], g0=S.G_S4, g1=S.G_S6, handle_in=S.H_IN, handle_out=S.H_OUT,
            transition_in=dict(type="whip", frames=0, note="whip pan braking g 204..219; g 204..210 = in-handle, still panning fast (streaked)"),
            transition_out=dict(type="dissolve", frames=12, note="handle g 359..366 rendered in 3D (shot 5 camera continues)"),
            internal=[dict(at=S.G_S5, type="dissolve", frames=S.DISS, mixed=[D0, D0 + S.DISS - 1], from_shot=4, to_shot=5,
                           mix="smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 4 to g 311, shot 5 from g 298 (raw/)")],
            shot_ranges={"4": [S.G_S4, S.G_S5 - 1], "5": [S.G_S5, S.G_S6 - 1]},
            set="v3/set3d2/tower.py", light="NIGHT_STORM", rod="set_rod(0) throughout (the belief before the rod; no rod on the spire)")

src, rows = tk.deliver(HERE, "s04", order, dissolves, G0, G1, meta, cues, cams={4: S.cam4})
qa = tk.qa_text(HERE, {4: (G0, S.G_S5 - 1), 5: (S.G_S5, G1)}, rows, {4: S.cam4, 5: S.cam5}, G0, G1, "s04")
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
open(os.path.join(HERE, "work", "qa.txt"), "w").write(qa)
print(qa)
print("streaked:", [g for g, v in src.items() if "streak" in v])
