import json, os, glob
from PIL import Image, ImageDraw, ImageFont
P = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(P + "/measure_before_after.json"))
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 21)
names = sorted(M); HD, FT = 50, 150
W, H = 4 * 720 + 3 * 16, 3 * (1280 + HD + FT) + 60
im = Image.new("RGB", (W, H), (12, 14, 22)); d = ImageDraw.Draw(im)
d.text((16, 12), "DEAD ZONE 09 EP.1  rain / clarity: draft-v1 levels (BEFORE) vs v12 levels (AFTER), final tier 720x1280, same film frame", font=fb, fill=(235, 235, 240))
for i, n in enumerate(names):
    r, c = divmod(i, 2); x0 = c * (1440 + 32); y0 = 60 + r * (1280 + HD + FT)
    for j, t in enumerate(("before", "after")):
        x = x0 + j * 720
        im.paste(Image.open(f"{P}/{t}/{n}.png").convert("RGB"), (x, y0 + HD))
        d.text((x + 10, y0 + 8), "%s  %s  %s" % (n[:3], n[4:], t.upper()), font=fb, fill=(255, 210, 90) if j else (170, 180, 200))
    b, a = M[n]["before"], M[n]["after"]; y = y0 + HD + 1280 + 6
    d.text((x0 + 10, y), "region     Laplacian variance      local contrast (9px sd)   luma p5", font=fs, fill=(150, 160, 180)); y += 26
    for k in ("principal", "near", "mid", "far"):
        if not b[k]: continue
        d.text((x0 + 10, y), "%-9s %7.0f -> %7.0f x%-5.2f %6.2f -> %5.2f x%-5.2f  %3.0f -> %3.0f" % (k, b[k]["lapvar"], a[k]["lapvar"], a[k]["lapvar"] / b[k]["lapvar"], b[k]["lc"], a[k]["lc"], a[k]["lc"] / b[k]["lc"], b[k]["p5"], a[k]["p5"]), font=fs, fill=(225, 228, 235)); y += 24
    d.text((x0 + 905, y0 + HD + 1280 + 32), "shade hue %s -> %s deg\nmagenta frac %s -> %s\nrain streaks on sky %s -> %s\nf %.1f D: near<1.6f mid<6f far>6f" % (b["shade_hue"], a["shade_hue"], b["magenta_frac"], a["magenta_frac"], b["streak_sky"], a["streak_sky"], M[n]["focus_z"]), font=fs, fill=(225, 228, 235), spacing=5)
im.save(P + "/rain_before_after.png"); print(im.size)
for i, n in enumerate(names):   # full-size check tiles
    r, c = divmod(i, 2); x0 = c * 1472; y0 = 60 + r * (1280 + HD + FT)
    im.crop((x0, y0, x0 + 1440, y0 + HD + 1280 + FT)).save(P + "/check_%s.png" % n[:3])
