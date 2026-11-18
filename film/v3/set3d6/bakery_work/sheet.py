import sys, os, glob
from PIL import Image, ImageDraw
out = sys.argv[1]; fs = sys.argv[2:]; W, H = int(os.environ.get('W', 360)), int(os.environ.get('H', 640)); cols = int(os.environ.get('COLS', 5))
rows = (len(fs) + cols - 1) // cols; sh = Image.new('RGB', (cols * W, rows * (H + 18)), (16, 16, 20)); d = ImageDraw.Draw(sh)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS); x, y = (i % cols) * W, (i // cols) * (H + 18)
    sh.paste(im, (x, y + 18)); d.text((x + 4, y + 3), os.path.basename(f)[:-4], fill=(240, 240, 240))
    if os.environ.get('CAP'): d.line([(x, y + 18 + int(900 * H / 1280)), (x + W, y + 18 + int(900 * H / 1280))], fill=(0, 255, 255), width=1)
sh.save(out, quality=90)
