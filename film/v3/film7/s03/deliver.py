#!/usr/bin/env python3
"""deliver.py -- build frames/g_%04d.png from raw/s<id>/, meta.json, cues.json, contact.jpg, compare.jpg and take.mkv (libx264rgb crf 6)
for this take (s02, s03 or s04 of film 7; the take is the name of the folder; the same file sits in each).   python3 deliver.py"""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = os.path.basename(HERE)
DOF = "none (client rule: cam.data.dof.use_dof False + L.setup_dof(scene, None, None, cam=cam) at build and before every render)"

CFG = {
 "s02": dict(shots=[2], g0=72, g1=138, h_in=6, h_out=6, tin="cut", tout="cut",
    setups={1: ([66, 101], "louvre wall_eye area, GALLERY_DAY, mona False: ECU of the empty spot (four hooks, patch, plaque), pull back 34 -> 29.5 mm"),
            2: ([102, 143], "louvre wall_eye area, GALLERY_DAY, mona False: medium, the guard beside the empty spot yawning, slow push 26 mm")},
    shot_ranges={"2": [72, 137]},
    events={"ecu_empty_hooks": [66, 101], "cut_to_guard": 102, "yawn_open": [104, 112], "yawn_hold": [112, 122], "yawn_close": [122, 130]},
    light="GALLERY_DAY", cast="v3/cast7: guard (sleepy -> guard_yawn blend: arms stretch, mouth ('open') opens / holds / closes once, then sags back)",
    set="v3/set3d7/louvre.py louvre wall_eye (Salon Carre), set_mona(False) keyed every frame, set_flames keyed every frame, custom camera",
    mouths="no lip-sync (no quoted line): one yawn of the expression mouth",
    cues=[(66, 144, "ambience", "the Salon Carre, quiet: a big room's hush, distant footsteps on parquet, a clock ticking", None),
          (72, 72, "cut", "cut in from shot 1 (the street)", None),
          (66, 101, "accent", "the empty spot: a hollow low string note / 'nothing there' sting", 72),
          (102, 102, "cut", "cut to the guard (framing change)", None),
          (104, 130, "gesture", "the guard's long, loud yawn (rising then sighing off), uniform creak as he stretches", 114),
          (132, 138, "gesture", "a sleepy lip-smack", 134),
          (138, 138, "cut", "plan: cut to shot 3 (the kiosk)", None)],
    contact=None, compare=[(80, 3, "ECU object"), (116, 13, "open mouth, medium")]),
 "s03": dict(shots=[3], g0=138, g1=234, h_in=6, h_out=6, tin="cut", tout="dissolve",
    setups={1: ([132, 185], "paris kiosk area, STREET_GOLDEN (gas lamps keyed low, 0.3): the kiosk front, papers 0 -> 24 keyed per frame, push in 22 mm"),
            2: ([186, 239], "paris kiosk area: closer and a little low on the newsboy, the kiosk wall of front pages and the column behind, 24 mm")},
    shot_ranges={"3": [138, 233]},
    events={"papers_0": [132, 141], "papers_fill_0_to_24": [142, 196], "newsboy_waving_shouting": [132, 239], "cut_to_newsboy": 186},
    light="STREET_GOLDEN", cast="v3/cast7: newsboy (newsboy_shout: the Mona Lisa front page waved high, a HELD open shout mouth, no lip-sync)",
    set="v3/set3d7/louvre.py paris kiosk (the rue), set_papers 0 -> 24 keyed constant per frame (flash-forward: the only early shot with her face on the papers), set_flames 0.3 keyed every frame",
    mouths="no lip-sync: the newsboy's shout is a held open mouth",
    cues=[(132, 240, "ambience", "Paris street 1911, busy: hooves, wheels on cobbles, cafe chatter, pigeons", None),
          (138, 138, "cut", "cut in from shot 2 (the guard)", None),
          (142, 196, "prop", "papers slapped up on the kiosk one after another: a quickening run of paper 'flap / slap' hits", 150),
          (150, 230, "voice", "the newsboy's shout, NOT lip-synced, as wordless crowd walla: 'Extra! Extra!' (French: 'Edition speciale !')", 186),
          (186, 186, "cut", "cut closer on the newsboy (framing change)", None),
          (196, 234, "accent", "the 'famous all over the world' swell: brass hit + bell", 200),
          (234, 234, "cut", "plan: dissolve to shot 4 (the salon)", None)],
    compare=[(170, 56, "street with stalls, day"), (215, 85, "character near the lens, street")]),
 "s04": dict(shots=[4, 5, 6], g0=234, g1=599, h_in=6, h_out=6, tin="dissolve", tout="cut",
    setups={1: ([228, 285], "louvre gallery_wide area: establishing wide from the service-door corner, the crowd walking across, crane drift 22 mm"),
            2: ([286, 335], "louvre gallery_wide area: mid-room toward the back wall, she is small in the hang, visitors cross, push 24 mm"),
            3: ([336, 389], "louvre wall_eye area: close on the Mona Lisa pulling back 46 -> 24 mm to the big pictures round her"),
            4: ([390, 440], "louvre wall_eye: eye level at the rope, the lady strolls in, glances, walks on; the guard by the wall"),
            5: ([441, 499], "louvre wall_eye area, low angle (z 1.35): the director proud beside her, rising push 22 mm"),
            6: ([500, 539], "low angle (z 0.95) closer: the boast, finger to the sky, lip-sync, 24 mm"),
            7: ([540, 569], "ECU cut-in on the painting (her face behind glass), 50 -> 52 mm"),
            8: ([570, 604], "extreme low angle (z 0.65) on the director, finger up, lip-sync to the end of the quote, 22 mm")},
    shot_ranges={"4": [234, 335], "5": [336, 440], "6": [441, 598]},
    events={"crowd_walks_past": [228, 335], "her_small_in_the_hang": [286, 389], "lady_enters": 390, "lady_slows": [402, 408],
            "lady_glances": [408, 418], "lady_walks_on": [418, 440], "director_proud": [441, 499], "finger_up": [500, 506],
            "quote_lipsync": [500, 602], "ecu_painting": [540, 569], "quote_end": 602},
    light="GALLERY_DAY", cast="v3/cast7: lady x2, gentleman x2, newsboy (walk cycles), guard (at ease), lady (glance), director (director_proud -> director_boast, lip-sync)",
    set="v3/set3d7/louvre.py louvre gallery_wide / wall_eye (Salon Carre, one area), set_mona(True) keyed every frame, set_flames keyed every frame, one custom camera per set-up",
    mouths="ONLY the director, only inside the quote 16.57-19.95 s (g 500..602): cast7.talk_mouth driven by the narration RMS envelope (hold 2 frames); silent (< 0.12) -> the expression mouth",
    cues=[(228, 336, "ambience", "the Salon Carre busy: footsteps on parquet, rustling skirts, murmured French chatter, a cane tapping", None),
          (228, 240, "transition", "dissolve in from the kiosk: street noise crossfades into the gallery murmur", 234),
          (286, 286, "cut", "framing change: toward the back wall", None),
          (336, 336, "cut", "cut to the Mona Lisa close (shot 5)", None),
          (336, 389, "accent", "a small music-box motif for 'just a small picture'", 340),
          (390, 440, "foley", "the lady's heels on parquet, skirt rustle; she pauses ('hm') and walks on", 412),
          (441, 441, "cut", "cut to the director, low angle (shot 6)", None),
          (441, 499, "accent", "pompous brass fanfare under the director's entrance", 445),
          (500, 602, "voice", "the director's quote (narration) -- his mouth is lip-synced to it", 500),
          (540, 540, "cut", "cut-in ECU of the painting at 18.0 s", None),
          (570, 570, "cut", "back to the director, extreme low angle", None),
          (590, 602, "accent", "a smug 'ta-da' cymbal on 'Notre-Dame'", 592),
          (599, 599, "cut", "plan: cut to shot 7 (vincenzo fitting the glass)", None)],
    compare=[(260, 16, "wide hall"), (412, 46, "people in a hall"), (520, 51, "big figure, low angle"), (555, 3, "ECU object")]),
}[TAKE]

g0, g1, h_in, h_out = CFG["g0"], CFG["g1"], CFG["h_in"], CFG["h_out"]
FIRST, LAST = g0 - h_in, g1 + h_out - 1
N = LAST - FIRST + 1
OUT = os.path.join(HERE, "frames")
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
src, rows = {}, []
for sid, (rg, _) in CFG["setups"].items():
    for g in range(rg[0], rg[1] + 1):
        raw = os.path.join(HERE, "raw", "s%d" % sid)
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(sid)
        rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
assert sorted(src) == list(range(FIRST, LAST + 1)), "missing frames"
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
by = {}
for m in rows:
    by.setdefault(str(m["shot"]), []).append(m)
meta = {"take": TAKE, "film": 7, "shots": CFG["shots"], "first_g": FIRST, "n_frames": N, "g0": g0, "g1": g1,
        "handle_in": h_in, "handle_out": h_out,
        "transition_in": CFG["tin"], "transition_out": CFG["tout"],
        "transitions": [{"at": g0, "type": CFG["tin"], "handle": [FIRST, g0 - 1]}]
                       + [{"at": rg[0], "type": "cut", "note": "framing change inside the take"} for sid, (rg, _) in CFG["setups"].items() if rg[0] > FIRST]
                       + [{"at": g1, "type": "out (%s per plan)" % CFG["tout"], "handle": [g1, LAST]}],
        "shot_ranges": CFG["shot_ranges"],
        "setups": {str(k): {"g": v[0], "set": v[1]} for k, v in CFG["setups"].items()},
        "events": CFG["events"], "set": CFG["set"], "dof": DOF,
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film7/audio/narration_bankky.wav at +0.10 s; captions film7/script/captions.json",
        "light": CFG["light"], "cast": CFG["cast"], "mouths": CFG["mouths"],
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "s_per_frame_by_setup": {k: {"wall": round(float(np.mean([m["wall"] for m in v])), 2), "cpu": round(float(np.mean([m["cpu"] for m in v])), 2)} for k, v in by.items()},
        "frame_source": {str(g): src[g] for g in sorted(src)}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
for a, b, kind, label, peak in CFG["cues"]:
    e = dict(time=round(a / 30.0, 3), duration=round(max(0, b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label)
    if peak is not None:
        e["peak_frame"] = peak
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film7/audio/narration_bankky.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)


def setup_of(g):
    return src[g]


gs = [FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
shot_of = {}
for sh, (a, b) in CFG["shot_ranges"].items():
    for g in range(a, b + 1):
        shot_of[g] = sh
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d %.2fs %s id %s" % (g, g / 30.0, ("shot " + shot_of[g]) if g in shot_of else "handle", setup_of(g)), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = CFG["compare"]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, what in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s g %d (%.2f s)" % (TAKE, g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%s)" % (tref, what), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %s: %d frames g %d..%d + take.mkv; mean wall %.2f s, cpu %.2f s" % (TAKE, N, FIRST, LAST, np.mean(walls), np.mean(cpus)))
