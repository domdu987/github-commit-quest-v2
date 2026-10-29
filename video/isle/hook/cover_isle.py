# cover_isle.py FRAME.png OUT.jpg "EP.n" : TikTok cover for ติดเกาะร้าง — the episode's own first frame (the object in the hands, paper headline
# already drawn by the composition) with a rotated red episode stamp; no extra darkening so the fish stays the brightest thing in the grid
import sys
from PIL import Image, ImageDraw, ImageFont
W = "/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work"
bg, out, ep = sys.argv[1:4]
im = Image.open(bg).convert("RGBA").resize((1080, 1920))
F = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f3.ttf", 70, layout_engine=ImageFont.Layout.RAQM)
F2 = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f2.ttf", 34, layout_engine=ImageFont.Layout.RAQM)
st = Image.new("RGBA", (380, 170), (0, 0, 0, 0)); ds = ImageDraw.Draw(st)
ds.rounded_rectangle([6, 6, 374, 164], 18, fill=(246, 238, 220, 235), outline=(214, 40, 40, 245), width=8)
ds.text((190, 66), ep, font=F, fill=(214, 40, 40, 245), anchor="mm", language="th"); ds.text((190, 128), "ติดเกาะร้าง", font=F2, fill=(120, 30, 30, 235), anchor="mm", language="th")
st = st.rotate(6, resample=Image.BICUBIC, expand=True); im.alpha_composite(st, (660, 410))
im.convert("RGB").save(out, quality=92); print(out)
