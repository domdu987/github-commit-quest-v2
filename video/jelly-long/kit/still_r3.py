"""หนวดใส ฉบับเต็ม r3 still set: every shot of every long part at 640×360 per frame (two frames per shot: 35% and 80%), in long
order, labelled with part · shot key · long time. Snaps the landscape builds (servers must be up) with snapL.cjs.
usage: python3 still_r3.py <out dir>"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
PORT = {"L1": (8981, "ep1c"), "L2": (8982, "ep2c"), "Lbr": (8988, "brc"), "L3": (8987, "ep3c"), "Lfb": (8990, "fbc"), "Lend": (8989, "endc")}
LP = json.load(open(os.path.join(J, "long", "long-parts.json")))["parts"] if os.path.exists(os.path.join(J, "long", "long-parts.json")) else None
if LP is None:
    LP = json.load(open("/home/user/github-commit-quest-v2/video/jelly-long/long-parts.json"))["parts"]
FPS = 60
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
W, H, COLS = 640, 360, 3
SHEETS = {"cold": "long-r3-1-cold-title", "title": "long-r3-1-cold-title", "ep1": "long-r3-2-ep1", "bridgeA": "long-r3-3-bridges",
          "ep2": "long-r3-4-ep2", "bridgeB": "long-r3-3-bridges", "ep3a": "long-r3-5-ep3", "secret": "long-r3-6-secret",
          "ep3b": "long-r3-5-ep3", "epi": "long-r3-7-epilogue-end", "credits": "long-r3-7-epilogue-end", "card": "long-r3-7-epilogue-end"}
items = {}
for p in LP:
    d = os.path.join(OUT, "snap", p["part"])
    port, proj = PORT[p["proj"]]
    sc = json.load(open(os.path.join(J, proj, "schedule.json")))
    a, b = p["frame0"] / FPS, (p["frame0"] + p["frames"]) / FPS
    ts = []
    for s in sc["shots"]:
        s0, s1 = max(a, s["start"]), min(b, s["start"] + s["dur"])
        if s1 - s0 < 0.2: continue
        for f in (0.35, 0.8):
            t = round(s0 + (s1 - s0) * f, 2); ts.append((t, s["key"]))
    os.makedirs(d, exist_ok=True)
    if not all(os.path.exists(os.path.join(d, f"t{t:.2f}.jpg")) for t, _ in ts): subprocess.run(["node", os.path.join(J, "snapL.cjs"), str(port), d, f"{ts[0][0]:.2f}"] + [f"{t:.2f}" for t, _ in ts],
                   env={**os.environ, "VW": "1920", "VH": "1080"}, check=True, capture_output=True)
    for t, k in ts:
        png = os.path.join(d, f"t{t:.2f}.png"); jpg = png[:-4] + ".jpg"   # keep only a 640×360 copy (the disk allowance is small)
        if os.path.exists(png): Image.open(png).convert("RGB").resize((W, H), Image.LANCZOS).save(jpg, quality=90)
        items.setdefault(SHEETS[p["part"]], []).append((jpg, f"{p['part']} · {k} · long {p['start'] + t - a:.2f}s"))
    for f in os.listdir(d):
        if f.endswith(".png"): os.remove(os.path.join(d, f))
for name, its in items.items():
    rows = (len(its) + COLS - 1) // COLS
    sh = Image.new("RGB", (COLS * W, rows * (H + 28)), "black"); g = ImageDraw.Draw(sh)
    for i, (f, lab) in enumerate(its):
        x, y = (i % COLS) * W, (i // COLS) * (H + 28)
        sh.paste(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS), (x, y + 28)); g.text((x + 6, y + 5), lab, fill="white", font=FONT)
    sh.save(os.path.join(OUT, name + ".jpg"), quality=84); print(name, len(its))
