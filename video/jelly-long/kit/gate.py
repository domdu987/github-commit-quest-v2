"""หนวดใส ฉบับเต็ม gate sheets: the first 3 s (every 0.5 s, and 0/1/2/3 s against ทะเลลด ฉบับเต็ม frames in <tide dir>/t0..t3.png)
and the first 30 s (every 2.5 s), snapped from the landscape builds (servers up).  usage: python3 gate.py <out dir> <tide dir>"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
J = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(J)
OUT, T = sys.argv[1], sys.argv[2]; O = os.path.join(OUT, "gate")
F = ImageFont.truetype("hf/brc/assets/fonts/f3.ttf", 22)
P = {p["part"]: p for p in json.load(open("long/long-parts.json"))["parts"]}
def snap(port, ts, d):
    os.makedirs(d, exist_ok=True)
    subprocess.run(["node", "snapL.cjs", str(port), d, "40.00"] + [f"{t:.4f}" for t in ts], env={**os.environ, "VW": "1920", "VH": "1080"}, check=True, capture_output=True)
def find(d, t):
    fs = [f for f in os.listdir(d) if f.endswith(".png") and f != "t40.00.png"]; return os.path.join(d, min(fs, key=lambda f: abs(float(f[1:-4]) - t)))
def sheet(items, out, cols=4):
    W, H = 640, 360; rows = (len(items) + cols - 1) // cols; sh = Image.new("RGB", (cols * W, rows * (H + 32)), "black"); g = ImageDraw.Draw(sh)
    for i, (f, l) in enumerate(items):
        x, y = (i % cols) * W, (i // cols) * (H + 32); sh.paste(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS), (x, y + 32)); g.text((x + 8, y + 2), l, fill="white", font=F)
    sh.save(out, quality=88)
C0 = P["cold"]["frame0"] / 60
snap(8988, [C0 + t for t in (0.02, 0.5, 1, 1.5, 2, 2.5, 3)], O + "/a")
sheet([(f"{T}/t{t}.png", f"ทะเลลด ฉบับเต็ม · {t} วิ") for t in (0, 1, 2, 3)] + [(find(O + "/a", C0 + t), f"หนวดใส ฉบับเต็ม · {round(t)} วิ") for t in (0.02, 1, 2, 3)], os.path.join(OUT, "long-gate-first3s-vs-tide.jpg"))
sheet([(find(O + "/a", C0 + t), f"long {t:.1f} วิ") for t in (0.02, 0.5, 1, 1.5, 2, 2.5, 3)], os.path.join(OUT, "long-gate-first3s.jpg"))
L = []
for t in [i * 2.5 for i in range(13)]:
    for n, port in (("cold", 8988), ("title", 8989), ("ep1", 8981)):
        p = P[n]
        if p["start"] - 1e-6 <= t < p["end"]: L.append((port, p["frame0"] / 60 + t - p["start"] + (0.02 if t == 0 else 0), t, n)); break
for port in (8988, 8989, 8981):
    ts = [x[1] for x in L if x[0] == port]
    if ts: snap(port, ts, f"{O}/{port}")
sheet([(find(f"{O}/{port}", tt), f"long {t:.1f} วิ · {lab}") for port, tt, t, lab in L], os.path.join(OUT, "long-gate-first30s.jpg"))
for d in os.listdir(O):
    for f in os.listdir(os.path.join(O, d)):
        if f.endswith(".png"): os.remove(os.path.join(O, d, f))
print("gate sheets in", OUT)
