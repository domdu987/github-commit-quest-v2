#!/usr/bin/env python3
"""deliver.py -- from raw/s17, raw/s18, raw/s19 build frames/g_%04d.png (g 1341..1672, the two in-take 10-frame dissolves blended
here), meta.json, cues.json, contact.jpg, compare.jpg and take.mkv (libx264rgb crf 6; split into 40 MB parts if over 45 MB).
    python3 deliver.py"""
import os, sys, json, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

G0, G18, G19, G1, H, XD = 1347, 1479, 1561, 1667, 6, 10
FIRST, LAST = G0 - H, G1 + H - 1
X1 = (G18 - XD // 2, G18 + XD // 2 - 1)      # 1474..1483: s17 -> s18
X2 = (G19 - XD // 2, G19 + XD // 2 - 1)      # 1556..1565: s18 -> s19
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)


def load(sid, g):
    return np.asarray(Image.open(os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.png" % g)).convert("RGB"), dtype=np.float32)


src, rows = {}, {}
for sid in (17, 18, 19):
    for f in glob.glob(os.path.join(HERE, "raw", "s%d" % sid, "g_*.json")):
        m = json.load(open(f)); rows[(sid, m["g"])] = m
for g in range(FIRST, LAST + 1):
    if X1[0] <= g <= X1[1] or X2[0] <= g <= X2[1]:
        a, b, x0 = (17, 18, X1[0]) if g <= X1[1] else (18, 19, X2[0])
        w = (g - x0 + 0.5) / XD
        img = (1 - w) * load(a, g) + w * load(b, g); src[g] = "%d>%d %.2f" % (a, b, w)
    else:
        sid = 17 if g < G18 else (18 if g < G19 else 19)
        img = load(sid, g); src[g] = str(sid)
    Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(OUT, "g_%04d.png" % g))
N = LAST - FIRST + 1


def stat(sid):
    r = [m for (s, g), m in rows.items() if s == sid]
    return {"wall": round(float(np.mean([m["wall"] for m in r])), 2), "cpu": round(float(np.mean([m["cpu"] for m in r])), 2), "frames": len(r)}


allr = list(rows.values())
meta = {"take": "s17", "film": 8, "shots": [17, 18, 19], "first_g": FIRST, "n_frames": N, "g0": G0, "g1": G1,
        "handle_in": H, "handle_out": H,
        "transition_in": {"type": "dissolve", "frames": 8, "note": "night falls after the summer dome interior (shot 16): a soft dissolve suits the reveal; 6 in-handle frames g 1341..1346 rendered in 3D (cut also fine)"},
        "transition_out": {"type": "cut", "frames": 0, "note": "plan: shot 20 (dome_wide SUMMER) follows at g 1667; out-handle g 1667..1672 rendered in 3D (the frost keeps spreading, the glide continues)"},
        "transitions": [{"at": G0, "type": "in", "handle": [FIRST, G0 - 1]},
                        {"at": G18, "type": "dissolve", "frames": XD, "range": list(X1), "note": "inside the take, shot 17 NIGHT -> shot 18 NOON (both set-ups rendered over the range, blended in deliver.py)"},
                        {"at": G19, "type": "dissolve", "frames": XD, "range": list(X2), "note": "inside the take, shot 18 NOON -> shot 19 NIGHT"},
                        {"at": G1, "type": "out", "handle": [G1, LAST]}],
        "shot_ranges": {"17": [G0, G18 - 1], "18": [G18, G19 - 1], "19": [G19, G1 - 1]},
        "setups": {"17": {"g": [FIRST, X1[1]], "set": "desert_ice plain, NIGHT, open water; custom low camera over channel 1 (z 0.55 -> 0.95) looking ENE (az 67 -> 67.5), tilting up from the water (pitch +4) to the Milky Way (pitch +30), 18 mm, 1.4 D push; stars x1.5 brilliance, twinkle 0.45; 56 runtime soft heat-wisp cards rising from the channels (the set's 26 D wisp cards hidden)"},
                   "18": {"g": [X1[0], X2[1]], "set": "desert_ice plain, NOON, thick ice in the shade; custom high camera from the north (z 9.4 -> 8.4, y 28.5 -> 26.8) looking SSW (az -160 -> -158, pitch +4.5 -> +6.5), 16 mm: the sun blazing above the 15 D wall, its long blue shadow over all five channels, the sunlit sand in front; crane down + push"},
                   "19": {"g": [X2[0], LAST], "set": "desert_ice plain, NIGHT; close over channel 2 looking east (az 79 -> 80.5, pitch -10 -> -12), 22 mm, 1.1 D glide; set_ice 0.18 -> 0.42 under a runtime frost-front mask: the crystals spread from both bank lips to the channel centre (white rim on the front); the sawn hole hidden"}},
        "events": {"wisps_lift_off_water": [FIRST, 1400], "tilt_to_milky_way": [1360, X1[1]], "dissolve_to_day": list(X1),
                   "wall_shadow_all_day": [G18, G19 - 1], "dissolve_to_night": list(X2), "frost_front_spreads": [G19 - 2, G1 - 8]},
        "set": "v3/set3d8/desert.py desert_ice plain: set_ice, set_flames, set_stars keyed per frame (common.Take.key_set); runtime from shot.py: soft heat wisps (own texture work/wisp_soft.png, 56 camera-only billboards, born on the water, rising 3-11 D, widening, fading in 12 % / out from 25 % of life, shimmer noise keyed per frame) instead of set_heat_wisps; a frost-front mask (value s17_spread) inserted into the set's ice material alpha + a frost-white rim; dressing (jars, buckets, rocks, shrubs) per set-up",
        "dof": "none (client rule: cam.data.dof.use_dof False + D.setup_dof(scene, None, None, cam=cam) at build and before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film8/audio/narration.wav at +0.10 s; captions film8/script/captions.json",
        "light": "NIGHT (17, 19), NOON (18)", "cast": "nobody on screen (no mouths)",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean([m["wall"] for m in allr])), 2),
        "s_per_frame_cpu_mean": round(float(np.mean([m["cpu"] for m in allr])), 2),
        "s_per_frame_by_setup": {str(s): stat(s) for s in (17, 18, 19)},
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)


add(FIRST, X1[1], "clear desert night, absolute stillness: the faintest cold breeze, a soft high airy shimmer pad (the reveal), very quiet water lapping", "ambience")
add(FIRST, 1440, "heat wisps lift off the water: a slow rising breathy whoosh, a glassy shimmer climbing in pitch with the tilt", "accent", peak_frame=1420)
add(1440, X1[1], "the Milky Way fills the frame: a wide twinkling star-chime bloom", "accent", peak_frame=1462)
add(X1[0], X1[1], "dissolve night -> blazing noon: the shimmer pad swells into warm daylight air", "transition")
add(G18, X2[1], "blazing noon by the wall: hot dry wind, cicada-like heat buzz far off, but cool calm in the long shadow", "ambience")
add(X2[0], X2[1], "dissolve noon -> night: the heat buzz fades, cold quiet returns", "transition")
add(G19, LAST, "cold night close-up: crystalline crackle and fine tinkling as frost needles spread across the water from the banks", "foley", peak_frame=1610)
add(G1, G1, "plan: cut to shot 20 (dome_wide SUMMER, the merchant arrives)", "cut")
json.dump(dict(take="s17", fps=30, note="time = film seconds (g / 30); narration PROJ/film8/audio/narration.wav at +0.10 s, captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (LAST - FIRST) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = [(1440, 72, "a"), (1520, 61, "a"), (1640, 69, "a")]
w, h, lab = 300, 533, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref, rs in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "g %d (%.2f s)" % (g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", rs, "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref %s t%04d" % (rs, tref), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
for p in glob.glob(mkv + ".part*"):
    os.remove(p)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
sz = os.path.getsize(mkv)
if sz > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
print("delivered %d frames g %d..%d + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" % (N, FIRST, LAST, sz / 1e6, meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"]))
