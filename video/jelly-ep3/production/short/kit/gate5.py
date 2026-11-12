"""EP.3 Short gate sheets: (1) first 3 s every 0.5 s, ทะเลลด EP.2 above, หนวดใส EP.3 below; (2) the three paired points
(first 3 s / peak / twist+end).  usage: python3 gate5.py <port> <out dir> <tide frames dir>"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
port, O, T = sys.argv[1:4]; d = os.path.join(O, "ours"); os.makedirs(d, exist_ok=True)
F = ImageFont.truetype(os.path.join(J, "hf/brc/assets/fonts/f3.ttf"), 22)
FIRST = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
PTS = [("0 วิ", 0.0, 0.0), ("1 วิ", 1.0, 1.0), ("2 วิ", 2.0, 2.0), ("3 วิ คำสั่ง", 3.0, 3.0),
       ("พีก: ภัยเผยตัว", 61.5, 41.9), ("หักมุม", 96.0, 51.8), ("ตอนจบ → คลิปยาว", 103.0, 101.5)]
ts = sorted({t for t in FIRST} | {p[2] for p in PTS})
subprocess.run(["node", os.path.join(J, "snap.cjs"), port, d, "5.55"] + [f"{t:.2f}" for t in ts], check=True, capture_output=True)
W, H = 360, 640
def ours(t): return Image.open(os.path.join(d, f"t{t:.2f}.png")).convert("RGB").resize((W, H), Image.LANCZOS)
def tide(t): return Image.open(os.path.join(T, f"t{t:.1f}.jpg")).convert("RGB").resize((W, H), Image.LANCZOS)
def sheet(cols, name):
    sh = Image.new("RGB", (len(cols) * W, 2 * (H + 34)), "black"); g = ImageDraw.Draw(sh)
    for i, (lab, a, b) in enumerate(cols):
        sh.paste(tide(a), (i * W, 34)); sh.paste(ours(b), (i * W, H + 68))
        g.text((i * W + 6, 6), f"ทะเลลด EP.2 · {lab} · {a:.1f}s", fill="#9ad", font=F)
        g.text((i * W + 6, H + 40), f"หนวดใส EP.3 · {lab} · {b:.2f}s", fill="#fd6", font=F)
    sh.save(os.path.join(O, name), quality=86); print(name)
sheet([(f"{t:.1f} วิ", t, t) for t in FIRST], "ep3-short-gate-first3s-v2.jpg")
sheet(PTS, "ep3-short-gate-3points-v2.jpg")
for f in os.listdir(d):
    if f.endswith(".png"): os.remove(os.path.join(d, f))
