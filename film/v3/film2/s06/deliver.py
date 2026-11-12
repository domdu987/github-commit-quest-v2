#!/usr/bin/env python3
"""deliver.py -- take s06 (shot 6): frames/, take.mkv, meta.json, cues.json, contact.jpg, work/qa.txt.  python3 deliver.py"""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s04"))
import tk  # noqa: E402
_sp = importlib.util.spec_from_file_location("s06shot", os.path.join(HERE, "shot.py"))
S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)
import vault as V  # noqa: E402
import bpy  # noqa: E402

G0, G1 = S.RANGES[6]                                        # 351 .. 454
A = V.build("LANTERN")
cam = lambda g: S.cam6(g, A)
cues = [tk.cue(G0, G1 + 1, "gunpowder vault: low drone, the hanging lantern creaks, a drip far off", "ambience"),
        tk.cue(G0, S.G_KEP - 4, "slow dolly along the barrel rows (soft camera creak / air)", "camera_move"),
        tk.cue(S.G_KEP - 4, S.SNAP[0], "reframe onto the soldier on guard; he shifts his weight (leather creak, boot scuff)", "gesture"),
        tk.cue(S.SNAP[0], S.SNAP[1], "snap in onto the crossed-cannon stencil (short whoosh)", "camera_snap", peak_frame=(S.SNAP[0] + S.SNAP[1]) // 2),
        tk.cue(S.G_90, S.G_90, "'kueap 90 tan' lands on the stencil insert (low boom / sting, optional)", "accent"),
        tk.cue(S.G_S7 - 5, G1 + 1, "dissolve out to the bell chamber (shot 7)", "dissolve")]
meta = dict(shots=[6], g0=S.G_S6, g1=S.G_S7, handle_in=S.H_IN, handle_out=S.H_OUT,
            transition_in=dict(type="dissolve", frames=12, note="in-handle g 351..358 rendered in 3D (dolly continues backward)"),
            transition_out=dict(type="dissolve", frames=10, note="out-handle g 448..454 rendered in 3D (slow push on the insert continues)"),
            internal=[dict(at=S.SNAP[0], type="snap", frames=S.SNAP[1] - S.SNAP[0], note="dolly_barrels -> barrel_insert inside one camera move")],
            shot_ranges={"6": [S.G_S6, S.G_S7 - 1]}, set="v3/set3d2/vault.py", light="LANTERN")
src, rows = tk.deliver(HERE, "s06", [(6, G0, G1)], [], G0, G1, meta, cues, cams={6: cam})
qa = tk.qa_text(HERE, {6: (G0, G1)}, rows, {6: cam}, G0, G1, "s06")
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
open(os.path.join(HERE, "work", "qa.txt"), "w").write(qa)
print(qa); print("streaked:", {g: v for g, v in src.items() if "streak" in v})
