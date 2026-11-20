#!/usr/bin/env python3
"""deliver.py -- delivery of a film-19 HALL hall_low take (s08 / s09 / s20; the folder name picks the config) from raw/g_%04d.png (+ .json):
frames/, take.mkv (libx264rgb crf 6), meta.json, cues.json, contact.jpg, framediff.json, then qa_auto.py.  No bpy.
    python3 deliver.py            final delivery
    python3 deliver.py draft      work/draft -> work/draft_contact.jpg + frame-diff numbers (nothing delivered)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TAKE = os.path.basename(HERE)
CFG = {
 "s08": dict(shot=8, g0=545, g1=661, nxt="shot 9 (hall_low, closer)", prv="shot 7 (hall_window)",
   cues=[(545, 661, "ambience", "the Board's hall by day: room tone, far chatter, a ticking regulator, a quill scratching"),
         (603, 636, "foley", "the mocker's belly laugh: wheezy HA-HA-HA with gown and wig rustle, a stamp of a foot", 612),
         (631, 646, "accent", "snap push on 'นาฬิกาเนี่ยนะ' (g 637): a whoosh and a sarcastic honk", 637),
         (640, 661, "foley", "he straightens and points; buckles and gown swish", 648)],
   ev=dict(turn=[536, 600], belly_laugh=[598, 640], mouth_window=[622, 669], quote_word=637, snap=[632, 651], point=[640, 661])),
 "s09": dict(shot=9, g0=661, g1=773, nxt="shot 10 (hall_wide)", prv="shot 8 (same set, same mocker)",
   cues=[(661, 773, "ambience", "the Board's hall by day: room tone, a ticking regulator"),
         (661, 773, "foley", "mock-royal bow: gown swishes, a tiny gold pocket-watch tick held in his hand", 700),
         (743, 762, "accent", "snap push on 'จับเวลาเอง' (g 748): a whoosh and a cheeky watch-click", 748)],
   ev=dict(bow=[652, 722], deep_bow=[716, 748], mouth_window=[652, 781], quote_word=748, snap=[743, 762])),
 "s20": dict(shot=20, g0=1581, g1=1665, nxt="shot 21 (SHIP ship_coast DAY_BARBADOS)", prv="shot 19 (ship_coast DAY_JAMAICA)",
   cues=[(1581, 1665, "ambience", "the Board's hall by day: room tone, a ticking regulator"),
         (1609, 1625, "foley", "the shrug: gown and wig rustle, a smug 'hmph'", 1615),
         (1628, 1648, "accent", "snap push on 'ฟลุ๊ค!' (g 1633): a whoosh and a dismissive honk", 1633)],
   ev=dict(shrug=[1609, 1621], mouth_window=[1626, 1672], fluke_word=1633, snap=[1628, 1646], pump2=[1651, 1663])),
}[TAKE]
G0, G1, H = CFG["g0"], CFG["g1"], 9
F0, F1 = G0 - H, G1 + H - 1                          # first_g, last g of take.mkv
N = F1 - F0 + 1


def grey(p):
    return np.asarray(Image.open(p).convert("RGB").resize((90, 160), Image.BILINEAR), dtype=np.float32).mean(-1)


def diffs(src):
    d, prev = {}, None
    for g in range(F0, F1 + 1):
        a = grey(os.path.join(src, "g_%04d.png" % g))
        if prev is not None:
            d[g] = float(np.abs(a - prev).mean())
        prev = a
    return d


def numbers(d):
    ins = [v for g, v in d.items() if G0 < g < G1]       # pairs (g-1, g) with both frames inside the shot
    return dict(method="mean abs diff of consecutive frames, grey = mean(R,G,B), 90x160 bilinear, 0-255 levels; in-shot pairs only (no handle)",
                median=round(float(np.median(ins)), 2), p90=round(float(np.percentile(ins, 90)), 2), min=round(min(ins), 2),
                max=round(max(ins), 2), n_pairs=len(ins), target=dict(median=4.0, p90=12.0),
                per_pair={str(g): round(v, 2) for g, v in d.items()})


def contact(src, out, cols=8, w=270):
    h, lab = w * 16 // 9, 18
    gs = [int(round(F0 + i * (N - 1) / 15.0)) for i in range(16)]
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20))
    dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(src, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
        dr.text((x + 4, y + 3), "g %d  %.2f s%s" % (g, g / 30.0, "  handle" if (g < G0 or g >= G1) else ""), fill=(255, 255, 255))
    S.save(out, quality=88)


if len(sys.argv) > 1 and sys.argv[1] == "draft":
    src = os.path.join(HERE, "work", "draft")
    assert len(glob.glob(src + "/g_*.png")) == N
    contact(src, os.path.join(HERE, "work", "draft_contact.jpg"))
    nb = numbers(diffs(src))
    print("draft frame-diff median %.2f p90 %.2f (min %.2f max %.2f)" % (nb["median"], nb["p90"], nb["min"], nb["max"]))
    sys.exit(0)

RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(F0, F1 + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(RAW, "g_%04d.json" % g))))
nb = numbers(diffs(OUT))
json.dump(nb, open(os.path.join(HERE, "framediff.json"), "w"), indent=1)
walls, cpus = [r["wall"] for r in rows], [r["cpu"] for r in rows]
heads = [r["heads"]["ast"] for r in rows if "ast" in r["heads"]]
bad = [r["g"] for r in rows if (r["mouth"] not in ("flat", "smile", "smirk", "None") and not r["in_window"])]
meta = {"take": TAKE, "film": 19, "shots": [CFG["shot"]], "g0": G0, "g1": G1, "first_g": F0, "n_frames": N,
        "shot_ranges": {str(CFG["shot"]): [G0, G1 - 1]}, "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0, "note": "hard cut from %s; 9 handle frames rendered g %d..%d" % (CFG["prv"], F0, G0 - 1)},
        "transition_out": {"type": "cut", "frames": 0, "at": G1, "note": "hard cut to %s; handle g %d..%d" % (CFG["nxt"], G1, F1)},
        "set": "v3/set3d19/h19.py HALL preset hall_low, light DAY; set_candles(1.0) keyed every frame; no runtime set changes; no caption_shade",
        "cast": "v3/cast19 astro19 (the mocker) alone at mark mocker_telescope; mouth driven only inside the quote window (c19.mouth_open_at), still expression mouth elsewhere",
        "events": CFG["ev"], "dof": "none", "text": "none", "caption_shade": "none", "light": "DAY", "samples": rows[0].get("samples"),
        "resolution": [720, 1280], "threads": 2, "fps": 30, "mouth_moving_outside_window_frames": bad,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "head_px": [round(min(h["w"] for h in heads)), round(max(h["w"] for h in heads))],
        "head_centre_y": [round(min(h["y"] for h in heads)), round(max(h["y"] for h in heads))],
        "head_bottom_max_y": round(max(h["bottom"] for h in heads)),
        "framediff_in_shot": {"median": nb["median"], "p90": nb["p90"]},
        "narration": "film19/audio/narration.wav at +0.10 s; captions film19/script/captions.json"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for c in CFG["cues"]:
    a, b, kind, label = c[:4]
    e = dict(time=round(a / 30.0, 3), duration=round((b - a) / 30.0, 3), frame=a, end_frame=b, kind=kind, label=label)
    if len(c) > 4:
        e["peak_frame"] = c[4]
    ev.append(e)
ev.append(dict(time=round(G1 / 30.0, 3), duration=0.0, frame=G1, end_frame=G1, kind="cut", label="hard cut to " + CFG["nxt"]))
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film19/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
contact(OUT, os.path.join(HERE, "contact.jpg"))
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(F0), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
if os.path.getsize(mkv) > 45e6:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
r = subprocess.run([sys.executable, os.path.join(PROJ, "qa_auto.py"), mkv, "--first_g", str(F0), "--cuts", "%d,%d" % (G0, G1)],
                   capture_output=True, text=True)
print(r.stdout, r.stderr[-500:])
print("delivered %d frames, take.mkv %.1f MB; s/frame %.2f wall %.2f cpu; frame-diff median %.2f p90 %.2f; mouth outside window: %s"
      % (N, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus), nb["median"], nb["p90"], bad))
