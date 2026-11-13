#!/usr/bin/env python3
"""deliver.py -- assemble the take of this folder (s17, s18 or s20; render worker 4) from raw/: frames/g_NNNN.png (shot 18 -> 19
dissolve mixed in s18), take.mkv, meta.json, cues.json, contact.jpg, compare.jpg, work/hue.txt.   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v2", "shots"))
from anim import smoothstep_mix

TAKE = os.path.basename(HERE)
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")
G17, G18, G19, G20, G_END, H = 1522, 1600, 1687, 1836, 1968, 7
DISS19 = 12; D19 = G19 - DISS19 // 2

CFG = {
    "s17": dict(shots=[17], first=G17 - H, last=G18 + H - 1, g0=G17, g1=G18, light="NIGHT",
                transition_in={"type": "dissolve", "frames": 10, "note": "in-handle g 1515..1521 rendered in 3D (shot 17 camera before its start)"},
                transition_out={"type": "cut_or_dissolve", "frames": 10, "note": "out-handle g 1600..1606 rendered in 3D (shot 17 camera continues)"},
                pairs=[(17, 1540, 121, "60 s"), (17, 1580, 123, "61 s")]),
    "s18": dict(shots=[18, 19], first=G18 - H, last=G20 + H - 1, g0=G18, g1=G20, light="NIGHT (shot 18), DAY (shot 19)",
                transition_in={"type": "cut_or_dissolve", "frames": 10, "note": "in-handle g 1593..1599 rendered in 3D"},
                transition_out={"type": "dissolve", "frames": 10, "note": "out-handle g 1836..1842 rendered in 3D (shot 19 camera continues)"},
                pairs=[(18, 1625, 99, "49 s"), (18, 1665, 103, "51 s"), (19, 1710, 105, "52 s"), (19, 1750, 107, "53 s"), (19, 1785, 109, "54 s"), (19, 1820, 101, "50 s")]),
    "s20": dict(shots=[20], first=G20 - H, last=G_END - 1, g0=G20, g1=G_END, light="DAWN",
                transition_in={"type": "dissolve", "frames": 10, "note": "in-handle g 1829..1835 rendered in 3D (shot 20 camera before its start)"},
                transition_out={"type": "end", "frames": 0, "note": "film ends at g 1967 (N = 1968)"},
                pairs=[(20, 1845, 125, "62 s"), (20, 1900, 127, "63 s"), (20, 1960, 129, "64 s")]),
}[TAKE]


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, "*.png")):
    os.remove(f)
src = {}
for g in range(CFG["first"], CFG["last"] + 1):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if TAKE == "s18" and D19 <= g < D19 + DISS19:
        w = smoothstep_mix(g - D19 + 1, DISS19)
        a = np.asarray(Image.open(raw(18, g)).convert("RGB"), dtype=np.float32)
        b = np.asarray(Image.open(raw(19, g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst); src[g] = "s18*%.3f+s19*%.3f" % (1 - w, w)
    else:
        s = CFG["shots"][0] if TAKE != "s18" else (18 if g < D19 else 19)
        shutil.copyfile(raw(s, g), dst); src[g] = "s%d" % s

rows = []
for s in CFG["shots"]:
    for js in glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")):
        rows.append(json.load(open(js)))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

mkv = os.path.join(HERE, "take.mkv")
if os.path.exists(mkv):
    os.remove(mkv)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(CFG["first"]), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)

ranges = {17: [G17, G18 - 1], 18: [G18, G19 - 1], 19: [G19, G20 - 1], 20: [G20, G_END - 1]}
trans = []
if TAKE == "s18":
    trans = [{"at": G19, "type": "dissolve", "frames": DISS19, "mixed": [D19, D19 + DISS19 - 1], "from_shot": 18, "to_shot": 19,
              "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 18 to g 1692, shot 19 from g 1681 (raw/)"}]
cuts = {"s17": [{"at": 1554, "type": "cut_in_shot", "note": "shot 17 A (low wide) -> B (low at the open base, huddled people)"}],
        "s18": [{"at": 1641, "type": "cut_in_shot", "note": "shot 18 A (whole cutaway) -> B (middle storeys)"},
                {"at": 1731, "type": "cut_in_shot", "note": "shot 19 A -> B (middle storeys + arrows)"},
                {"at": 1767, "type": "cut_in_shot", "note": "shot 19 B -> C (lower pillar as a pendulum)"},
                {"at": 1804, "type": "cut_in_shot", "note": "shot 19 C -> D (high angle down onto the swinging foot)"}],
        "s20": []}[TAKE]
meta = {"take": TAKE, "shots": CFG["shots"], "first_g": CFG["first"], "n_frames": CFG["last"] - CFG["first"] + 1,
        "g0": CFG["g0"], "g1": CFG["g1"], "handle_in": CFG["g0"] - CFG["first"], "handle_out": CFG["last"] + 1 - CFG["g1"],
        "transition_in": CFG["transition_in"], "transition_out": CFG["transition_out"], "transitions": trans + cuts,
        "shot_ranges": {str(s): ranges[s] for s in CFG["shots"]},
        "set": "v3/set3d4/pagoda.py v2 (shot.py adds only the shot-19 diagram veil and arrows)", "light": CFG["light"],
        "narration": "film4/audio/narration_bankky.wav", "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


if TAKE == "s17":
    add(1515, 1607, "night quake rumbling on (lower than shot 16), the pagoda's timbers creak and groan rhythmically with the sway", "ambience")
    add(1515, 1607, "wind bells on all five eaves jangle, paper lanterns rattle on their hooks", "ambience")
    add(1546, 1556, "'swaying like a snake': a long woody creak per swing", "accent", peak_frame=1546)
    add(1554, 1554, "cut to the open base: townspeople whimpering, huddled", "cut")
    add(1569, 1569, "'but not one storey fell': the creak settles into the rhythm (no crash)", "accent")
elif TAKE == "s18":
    add(1593, 1693, "inside the pagoda: muffled quake rumble, deep wooden knocking of the storeys, chain of the pillar creaking", "ambience")
    add(1641, 1641, "cut closer: storeys slide one way, the pillar the other", "cut")
    add(1641, 1660, "'dancing out of the way': a soft rhythmic swish per swing", "accent", peak_frame=1641)
    add(D19, D19 + DISS19, "dissolve to the day diagram: the rumble falls away, a calm explanatory music bed starts", "dissolve")
    add(1687, 1843, "diagram: soft whooshes as the arrows flip with each sway (every 1.0 s at 0.5 Hz)", "ambience")
    for g in (1731, 1767, 1804):
        add(g, g, "cut inside the diagram (soft swoosh)", "cut")
    add(1808, 1820, "'pendulum': a slow tick-tock creak of the hanging pillar", "accent", peak_frame=1808)
else:
    add(1829, 1968, "dawn: birds, a light breeze, quiet; settling timber creaks under the master's feet", "ambience")
    add(1889, 1889, "'looking at the central pillar': faint creak of the chain as the pillar swings", "accent")
    add(1930, 1968, "the pillar's gentle swing: a soft slow wooden creak; music resolves to the end", "ambience")
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film4/audio/narration_bankky.wav at +0.10 s, captions_bankky.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

N = CFG["last"] - CFG["first"] + 1
gs = [CFG["first"] + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:14]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = CFG["pairs"]
w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for shot, g, tref, sec in PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %d  g %d (%.2f s)" % (shot, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as HR
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    for s in CFG["shots"]:
        fl = sorted(glob.glob(os.path.join(RAW, "s%d" % s, "g_*.png")))
        HR.row("%s shot %d" % (TAKE, s), fl)
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
open(os.path.join(HERE, "work", "hue.txt"), "w").write(buf.getvalue())
print(buf.getvalue())
print("delivered %s: %d frames g %d..%d; mean wall %.2f s, cpu %.2f s" % (TAKE, N, CFG["first"], CFG["last"], np.mean(walls), np.mean(cpus)))
