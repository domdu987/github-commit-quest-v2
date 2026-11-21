import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 7
fs = sorted(glob.glob(os.path.join(d, 'g_*.png')))
if len(sys.argv) > 4: fs = fs[::int(sys.argv[4])]
im0 = Image.open(fs[0]); w, h = im0.size; s = 360 / w if w > 360 else 1; w, h = int(w * s), int(h * s)
rows = (len(fs) + cols - 1) // cols; sh = Image.new('RGB', (cols * w, rows * h), 'black')
for i, f in enumerate(fs):
    t = Image.open(f).convert('RGB').resize((w, h)); ImageDraw.Draw(t).text((4, 4), os.path.basename(f)[2:6], fill='yellow'); sh.paste(t, ((i % cols) * w, (i // cols) * h))
sh.save(out, quality=88)
