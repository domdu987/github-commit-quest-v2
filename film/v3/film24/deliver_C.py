#!/usr/bin/env python3
"""deliver_C.py <take> : frames_C from work_C/raw, take_C.mkv (crf 12), meta_C.json (+208), contact_C.jpg.  take in s13|s14|s15."""
import json, os, sys, glob, shutil, subprocess, statistics as st
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); T = sys.argv[1]; D = os.path.join(H, T)
SH = dict(s13=[(13, 1407, 1612)], s14=[(14, 1601, 1772)], s15=[(15, 1761, 1949)])
if T == "s13": SH = dict(s13=[(13, 1407, 1526), (113, 1527, 1559), (213, 1560, 1612)])
src = SH[T]
fr = os.path.join(D, "frames_C"); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
walls = []
for sid, a, b in src:
    for g in range(a, b + 1):
        base = os.path.join(D, "work_C" if T != "s15" else "work_C", "raw", "s%d" % sid, "g_%04d" % g)
        if not os.path.exists(base + ".png"): base = os.path.join(D, "raw", "s%d" % sid, "g_%04d" % g)
        shutil.copy(base + ".png", os.path.join(fr, "g_%04d.png" % g))
        walls.append(json.load(open(base + ".json")).get("wall", 0))
f0 = src[0][1]; f1 = src[-1][2]
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(f0), "-i", fr + "/g_%04d.png",
                       "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", os.path.join(D, "take_C.mkv")])
g0, g1 = dict(s13=(1413, 1607), s14=(1607, 1767), s15=(1767, 1950))[T]
meta = dict(take=T, version="C", film=24, g0=g0 + 208, g1=g1 + 208, g1_exclusive=True, first_g=f0 + 208, n_frames=f1 - f0 + 1,
            render_g=dict(g0=g0, g1=g1, first_g=f0, offset=208), transition_in=dict(type="cut", frames=0), resolution=[720, 1280], samples=24,
            s_per_frame_wall_mean=round(st.mean(walls), 1))
if T == "s13": meta.update(in_take_cuts_render_g=[1527, 1560], in_take_cuts_meta_g=[1735, 1768], shots=["13a", "13b", "13c"], overlay="overlay_C.json (13c, old g numbering)")
if T == "s14": meta.update(overlay="overlay_C.json (old g numbering)")
if T == "s15": meta.update(in_take_cuts_render_g=[1867], in_take_cuts_meta_g=[2075], no_out_handle=True)
json.dump(meta, open(os.path.join(D, "meta_C.json"), "w"), indent=1)
gs = [int(round(f0 + i * (f1 - f0) / 15.0)) for i in range(16)]
c = Image.new("RGB", (180 * 8, 640))
for i, g in enumerate(gs):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((180, 320)); ImageDraw.Draw(im).text((3, 3), str(g), fill=(255, 255, 0))
    c.paste(im, ((i % 8) * 180, (i // 8) * 320))
c.save(os.path.join(D, "contact_C.jpg"), quality=88)
print(T, "delivered", meta["n_frames"], "frames, mean wall", meta["s_per_frame_wall_mean"])
