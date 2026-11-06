import glob, sys
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
fs = sorted(glob.glob(d + '/t*.png'), key=lambda f: float(f.rsplit('/t', 1)[1][:-4]))
W, H = 480, 270; rows = (len(fs) + cols - 1) // cols
sh = Image.new('RGB', (cols * W, rows * (H + 20)), 'black'); g = ImageDraw.Draw(sh)
for i, f in enumerate(fs):
    x, y = (i % cols) * W, (i // cols) * (H + 20)
    sh.paste(Image.open(f).convert('RGB').resize((W, H)), (x, y + 20)); g.text((x + 4, y + 4), f"{i+1}  {f.rsplit('/t',1)[1][:-4]}s", fill='white')
sh.save(out, quality=82)
