#!/usr/bin/env python3
"""deliver.py -- take s07 (shot 7): frames/, take.mkv, meta.json, cues.json, contact.jpg, work/qa.txt.  python3 deliver.py"""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s04"))
import tk  # noqa: E402
_sp = importlib.util.spec_from_file_location("s07shot", os.path.join(HERE, "shot.py"))
S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)

G0, G1 = S.RANGES[7]                                        # 441 .. 541
cues = [tk.cue(G0, G1 + 1, "bell chamber by day: wind through the arches, pigeons, slow single bell swings", "ambience")]
for g in range(G0, G1 + 1):
    if (g - 441) % 24 == 12:
        cues.append(tk.cue(g, g, "single bell strike (big bronze bell, close)", "bell", impact_frame=g))
cues += [tk.cue(G0, S.G_DEK - 6, "three ropes hauled (rope creak, wooden lever)", "rope"),
         tk.cue(S.G_DEK - 6, S.G_DEK + 1, "nico hauls hard on his rope (strained grunt, rope creak)", "rope"),
         tk.cue(S.G_DEK + 4, S.G_RAKANG, "the rope shoots up and lifts nico off his feet (rope zing / comic whoosh up)", "gag", impact_frame=S.G_DEK + 4),
         tk.cue(S.SNAP[0], S.SNAP[1], "snap tilt / push onto nico in the air (short whoosh)", "camera_snap", peak_frame=(S.SNAP[0] + S.SNAP[1]) // 2),
         tk.cue(S.G_RAKANG - 2, S.G_NOI, "nico dangles and kicks on the rope (rope creak while bobbing)", "gag"),
         tk.cue(S.G_NOI + 4, S.G_NOI + 5, "nico drops back onto the planks (small thump)", "impact", impact_frame=S.G_NOI + 5),
         tk.cue(S.G_NOI + 18, S.G_S8 + 2, "hauled up again (rope creak)", "rope"),
         tk.cue(S.G_S8 - 5, G1 + 1, "dissolve out to the book insert (shot 8)", "dissolve")]
cues.sort(key=lambda c: c["frame"])
meta = dict(shots=[7], g0=S.G_S7, g1=S.G_S8, handle_in=S.H_IN, handle_out=S.H_OUT,
            transition_in=dict(type="dissolve", frames=10, note="in-handle g 441..447 rendered in 3D"),
            transition_out=dict(type="dissolve", frames=10, note="out-handle g 535..541 rendered in 3D (nico lifted again)"),
            shot_ranges={"7": [S.G_S7, S.G_S8 - 1]}, set="v3/set3d2/tower.py", light="DAY", rod="set_rod(1) (not in view)")
src, rows = tk.deliver(HERE, "s07", [(7, G0, G1)], [], G0, G1, meta, cues, cams={7: S.cam7})
qa = tk.qa_text(HERE, {7: (G0, G1)}, rows, {7: S.cam7}, G0, G1, "s07")
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
open(os.path.join(HERE, "work", "qa.txt"), "w").write(qa)
print(qa); print("streaked:", {g: v for g, v in src.items() if "streak" in v})
