# cover.py BG.png OUT.jpg EPLABEL LINE1 LINE2 [y] [scale] : TikTok cover — darkened frame, series paper headline in the centre band (profile grid crops to the middle 3:4), EP stamp
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
W = "/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work"
bg, out, ep, l1, l2 = sys.argv[1:6]; y = int(sys.argv[6]) if len(sys.argv) > 6 else 520
sc = sys.argv[7] if len(sys.argv) > 7 else "1.05"   # headline scale: long second lines need less than 1.05 to fit the width
import subprocess
subprocess.run(["python3", f"{W}/hook/headline.py", "/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work/hook/_hl.png", l1, l2, str(y), sc], check=True, capture_output=True)
im = Image.open(bg).convert("RGBA").resize((1080, 1920))
im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(0.92)).enhance(1.08)
# vignette
v = Image.new("L", (1080, 1920), 0); dv = ImageDraw.Draw(v); dv.ellipse([-300, -200, 1380, 2120], fill=255); v = v.filter(ImageFilter.GaussianBlur(160))
dark = Image.new("RGBA", (1080, 1920), (8, 6, 4, 255)); im = Image.composite(im, dark, v.point(lambda p: int(110 + p * 145 / 255)))
im.alpha_composite(Image.open(f"{W}/hook/_hl.png"))
d = ImageDraw.Draw(im)
F = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f3.ttf", 70, layout_engine=ImageFont.Layout.RAQM)
F2 = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f2.ttf", 40, layout_engine=ImageFont.Layout.RAQM)
# red rubber stamp with the episode number, rotated, top-left of the band
F2 = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f2.ttf", 34, layout_engine=ImageFont.Layout.RAQM)
st = Image.new("RGBA", (380, 170), (0, 0, 0, 0)); ds = ImageDraw.Draw(st)
ds.rounded_rectangle([6, 6, 374, 164], 18, fill=(246, 238, 220, 235), outline=(214, 40, 40, 245), width=8)
ds.text((190, 66), ep, font=F, fill=(214, 40, 40, 245), anchor="mm", language="th"); ds.text((190, 128), "เอาชีวิตรอด 99 วัน", font=F2, fill=(120, 30, 30, 235), anchor="mm", language="th")
st = st.rotate(6, resample=Image.BICUBIC, expand=True); im.alpha_composite(st, (70, y - 235))
im.convert("RGB").save(out, quality=92); print(out)
