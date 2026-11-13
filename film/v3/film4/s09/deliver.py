#!/usr/bin/env python3
"""deliver.py <take> (s09 | s10 | s11): from <take>/raw/<sub>/ build <take>/frames/g_%04d.png (the 11c -> 12a dissolve mixed in),
meta.json, cues.json, contact.jpg, compare.jpg (final frame beside its ref a frame), take.mkv.  Run from anywhere."""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
FILM4 = os.path.dirname(HERE)
PROJ = os.path.normpath(os.path.join(FILM4, "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v2", "shots"))
from anim import smoothstep_mix

TAKE = sys.argv[1]
TD = os.path.join(FILM4, TAKE)
H = 7
G9, G10, G11, G12, G13 = 593, 710, 782, 920, 1055
SUBS = [("9a", 9, G9 - H, 628, "s09"), ("9b", 9, 629, 661, "s09"), ("9c", 9, 662, G10 - 1 + H, "s09"),
        ("10", 10, G10 - H, G11 - 1 + H, "s10"),
        ("11a", 11, G11 - H, 835, "s11"), ("11b", 11, 836, 876, "s11"), ("11c", 11, 877, G12 - 1 + H, "s11"),
        ("12a", 12, G12 - H, 971, "s11"), ("12b", 12, 972, 1015, "s11"), ("12c", 12, 1016, G13 - 1 + H, "s11")]
SUBS = [s for s in SUBS if s[4] == TAKE]
DISS = 10
D0 = G12 - DISS // 2                 # 915: first mixed frame of the 11 -> 12 dissolve
G_FIRST, G_LAST = SUBS[0][2], SUBS[-1][3]
OUT = os.path.join(TD, "frames")
os.makedirs(OUT, exist_ok=True)


def raw(sub, g):
    return os.path.join(TD, "raw", sub, "g_%04d.png" % g)


def owner(g):
    if TAKE == "s11" and g >= G12:
        return [s for s in SUBS if s[0].startswith("12") and s[2] <= g <= s[3]][0][0]
    if TAKE == "s11":
        return [s for s in SUBS if s[0].startswith("11") and s[2] <= g <= s[3]][0][0]
    return [s for s in SUBS if s[2] <= g <= s[3]][0][0]


src = {}
for g in range(G_FIRST, G_LAST + 1):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if TAKE == "s11" and D0 <= g < D0 + DISS:
        w = smoothstep_mix(g - D0 + 1, DISS)
        a = np.asarray(Image.open(raw("11c", g)).convert("RGB"), dtype=np.float32)
        b = np.asarray(Image.open(raw("12a", g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst)
        src[g] = "11c*%.3f+12a*%.3f" % (1 - w, w)
    else:
        s = owner(g); shutil.copyfile(raw(s, g), dst); src[g] = s

rows = [json.load(open(j)) for s in SUBS for j in glob.glob(os.path.join(TD, "raw", s[0], "g_*.json"))]
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
shots = sorted({s[1] for s in SUBS})
bounds = {9: (G9, G10 - 1), 10: (G10, G11 - 1), 11: (G11, G12 - 1), 12: (G12, G13 - 1)}
g0, g1 = bounds[shots[0]][0], bounds[shots[-1]][1] + 1

tr = []
tr_in = {"s09": {"type": "dissolve", "frames": 10, "handle": [G_FIRST, g0 - 1], "note": "year 1 begins; 7-frame in-handle rendered in 3D (shot 9a camera)"},
         "s10": {"type": "cut", "frames": 0, "handle": [G_FIRST, g0 - 1], "note": "cut on 'ทั้งเมือง'; 7-frame in-handle rendered in 3D for a dissolve if wanted"},
         "s11": {"type": "dissolve", "frames": 10, "handle": [G_FIRST, g0 - 1], "note": "year 2 begins; 7-frame in-handle rendered in 3D (shot 11a camera)"}}[TAKE]
tr_out = {"type": "dissolve", "frames": 10, "handle": [g1, G_LAST], "note": "7-frame out-handle rendered in 3D (last camera continues)"}
tr.append(dict(at=g0, **{k: v for k, v in tr_in.items() if k != "note"}))
names = {"9a": "two_buildings wide", "9b": "tea cup insert", "9c": "pagoda up-shot", "10": "townspeople laugh",
         "11a": "low wide", "11b": "crack insert", "11c": "master plasters", "12a": "SUNSET wide", "12b": "crack insert, finger", "12c": "plaster again"}
for (a, *_), (b, sh, gb, *_r) in zip(SUBS[:-1], SUBS[1:]):
    if b == "12a":
        tr.append(dict(at=G12, type="dissolve", frames=DISS, mixed=[D0, D0 + DISS - 1], from_sub=a, to_sub=b,
                       mix="smoothstep P*P*(3-2P), P = i/(n+1); raw handles: 11c to g 926, 12a from g 913"))
    else:
        tr.append(dict(at=gb, type="cut", from_sub=a, to_sub=b))
tr.append(dict(at=g1, type="dissolve_out", frames=10, handle=[g1, G_LAST]))
sub_ranges = {}
for s in SUBS:
    a, b = max(s[2], g0), min(s[3], g1 - 1)
    if s[0] == "11c": b = G12 - 1
    if s[0] == "12a": a = G12
    sub_ranges[s[0]] = [a, b]
meta = {"take": TAKE, "shots": shots, "first_g": G_FIRST, "n_frames": G_LAST - G_FIRST + 1, "g0": g0, "g1": g1,
        "handle_in": g0 - G_FIRST, "handle_out": G_LAST - g1 + 1, "transition_in": tr_in, "transition_out": tr_out,
        "transitions": tr, "shot_ranges": {str(k): list(bounds[k]) for k in shots}, "sub_ranges": sub_ranges,
        "sub_names": {s[0]: names[s[0]] for s in SUBS},
        "set": "v3/set3d4/pagoda.py v2; the take adds a tea cup on a sill (9b) and a plank scaffold at the joint (11b-12c)",
        "engine": "film4/s09/shot.py (s10/s11 shot.py load it)",
        "light": {"s09": "DAY", "s10": "DAY", "s11": "DAY (11), SUNSET (12)"}[TAKE],
        "quake": "strength / sway amplitude per g in shot.py quake() / sway_amp(): year 1 sway 0.5 D (one span), year 2 0.85, year 3 1.2 (cap)",
        "narration": "film4/audio/narration_bankky.wav", "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(TD, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(a, b, label, kind, **kw):
    e = dict(time=t(a), duration=round(max(0, b - a) / 30.0, 3), frame=int(a), end_frame=int(b), kind=kind, label=label); e.update(kw); ev.append(e)


if TAKE == "s09":
    add(G_FIRST, 603, "calm courtyard: birds, wind in the banners", "ambience")
    add(603, 700, "quake 1 (small): low ground rumble, lanterns and wind bells clatter, wooden creak of the pagoda's storeys", "quake")
    add(629, 629, "hard cut to the tea cup on the tower sill: rumble drops to a muffled hum, the tea does not ripple", "cut")
    add(640, 652, "a single clear 'tink' accent as the cup sits perfectly still ('ใหญ่นิ่งสนิท')", "accent", peak_frame=644)
    add(662, 662, "hard cut: up the pagoda, rumble back up, wooden creaks left / right as the storeys sway opposite ways", "cut")
    add(688, 696, "snap punch-in to the upper storeys (whoosh), lands on 'หนึ่งคืบ'", "camera_snap", peak_frame=692)
    add(696, G_LAST, "quake fades: creaks slow down", "quake")
elif TAKE == "s10":
    add(G_FIRST, G_LAST, "courtyard after the quake: residual creak of the rocking pagoda, wind bells", "ambience")
    add(716, 781, "the townspeople burst out laughing (crowd laugh, three voices), belly-laugh rhythm", "laugh", peak_frame=726)
    add(752, 759, "snap punch-in onto the merchant and woman2 (short whoosh)", "camera_snap", peak_frame=756)
    add(762, 774, "pointing jab on 'เจดีย์เมา' (laugh peak)", "gesture", peak_frame=766)
else:
    add(G_FIRST, 786, "calm courtyard", "ambience")
    add(786, 890, "quake 2: stronger rumble, lantern and bell clatter, tile rattle, deep creaks of the swaying storeys", "quake")
    add(816, 824, "snap toward the pagoda (whoosh), lands on 'สองคืบ'", "camera_snap", peak_frame=820)
    add(836, 836, "hard cut to the tower joint: muffled rumble", "cut")
    add(856, 864, "sharp dry crack of plaster: the hairline crack appears (small camera jolt)", "crack", peak_frame=856)
    add(877, 877, "hard cut: the master on the scaffold", "cut")
    add(880, 915, "trowel scrapes on plaster, a wet slap every 12 frames; patch done g 897", "foley")
    add(D0, D0 + DISS, "dissolve to sunset, year 3", "dissolve")
    add(922, 1000, "quake 3 (biggest yet): heavy rumble, everything rattles, groaning timber", "quake")
    add(952, 959, "snap toward the pagoda (whoosh), lands on 'สามคืบ'", "camera_snap", peak_frame=956)
    add(972, 972, "hard cut to the joint: the crack is wide through the old patch", "cut")
    add(990, 1006, "the master's finger pokes into the crack (soft gritty scratch), sweat", "gesture", peak_frame=996)
    add(1016, 1016, "hard cut: plastering again", "cut")
    add(1018, G_LAST, "trowel scrapes, wet slaps; second patch lands g 1036 ('อีกชั้น' g 1041); evening birds", "foley")
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film4/audio/narration_bankky.wav at +0.10 s, captions_bankky.json",
               cues=ev), open(os.path.join(TD, "cues.json"), "w"), indent=1)

N = G_LAST - G_FIRST + 1
gs = [G_FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:16]), fill=(255, 255, 255))
S.save(os.path.join(TD, "contact.jpg"), quality=88)

PAIRS = {"s09": [("9a", 618, 39, "19 s"), ("9b", 645, 43, "21 s"), ("9c", 700, 41, "20 s")],
         "s10": [("10", 740, 47, "23 s"), ("10", 772, 47, "23 s")],
         "s11": [("11a", 830, 49, "24 s"), ("11b", 870, 51, "25 s"), ("11c", 900, 53, "26 s"),
                 ("12a", 940, 61, "30 s"), ("12b", 998, 63, "31 s"), ("12c", 1040, 65, "32 s")]}[TAKE]
w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for sub, g, tref, sec in PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s  g %d (%.2f s)" % (sub, g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, sec), fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(TD, "compare.jpg"), quality=88)

mkv = os.path.join(TD, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %s: %d frames g %d..%d; mean wall %.2f s, cpu %.2f s" % (TAKE, len(src), G_FIRST, G_LAST, np.mean(walls), np.mean(cpus)))
