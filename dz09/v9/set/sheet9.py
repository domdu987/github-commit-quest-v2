"""sheet9.py -- vs_ref_night.png: per shot v9 pass 1 | v9 pass 2 | closest ref D frame (labelled); plus the 16:9 pair sheet
(wide_169.png). The v6 | v9 pass-1 sheet is kept as vs_ref_night_pass1.png."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
SHOTS = ["s06", "s09", "s13", "s18", "s20", "s24"]
TITLE = {"s06": "S06 low hero", "s09": "S09 battery macro", "s13": "S13 phone MCU", "s18": "S18 POV windscreen",
         "s20": "S20 head lift Dutch", "s24": "S24 high wide"}
REF = {"s06": (76, "night campfire"), "s09": (1, "macro, bokeh"), "s13": (80, "moonlit figure"), "s18": (82, "moonlit forest"),
       "s20": (36, "warm interior"), "s24": (73, "wide, long shadows")}

def font(sz):
    try: return ImageFont.truetype(os.path.join(PROJ, "fonts", "WorkSans-Black.ttf"), sz)
    except Exception: return ImageFont.load_default()

def night(out=os.path.join(HERE, "vs_ref_night.png"), v9dir=os.path.join(HERE, "look", "out")):
    w, h, lab, g = 300, 533, 30, 6
    tw = 3 * w + 2 * g
    S = Image.new("RGB", (2 * tw + 30, 3 * (h + lab + 14) + 10), (14, 14, 18)); d = ImageDraw.Draw(S); f = font(15)
    for i, n in enumerate(SHOTS):
        x0 = (i % 2) * (tw + 30); y0 = (i // 2) * (h + lab + 14) + 4
        items = [(os.path.join(HERE, "look", "pass1", f"{n}_916.png"), f"{TITLE[n]}  v9 pass 1"),
                 (os.path.join(v9dir, f"{n}_916.png"), f"{TITLE[n]}  v9 pass 2"),
                 (os.path.join(PROJ, "ref", "d", "frames2", f"f_{REF[n][0]:03d}.png"), f"ref D f_{REF[n][0]:03d} ({REF[n][1]})")]
        for k, (p, t) in enumerate(items):
            x = x0 + k * (w + g)
            d.text((x + 3, y0 + 6), t, fill=(232, 232, 236) if k < 2 else (165, 165, 178), font=f)
            if os.path.exists(p): S.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (x, y0 + lab))
    S.save(out); return out

def wide(shots=("s06", "s24"), out=os.path.join(HERE, "wide_169.png"), v9dir=os.path.join(HERE, "look", "out")):
    w, h, lab = 900, 506, 30
    S = Image.new("RGB", (w, len(shots) * (h + lab) + 10), (14, 14, 18)); d = ImageDraw.Draw(S); f = font(18)
    for i, n in enumerate(shots):
        y = i * (h + lab)
        d.text((4, y + 6), f"{TITLE[n]}  v9 pass 2  16:9", fill=(232, 232, 236), font=f)
        p = os.path.join(v9dir, f"{n}_169.png")
        if os.path.exists(p): S.paste(Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS), (0, y + lab))
    S.save(out); return out

if __name__ == "__main__":
    print(night()); print(wide())
