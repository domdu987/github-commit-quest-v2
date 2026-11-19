"""sheet.py <out.jpg> <h> files... : quick labelled contact strip (no Blender)."""
import sys, os
from PIL import Image, ImageDraw
out, h = sys.argv[1], int(sys.argv[2]); fs = sys.argv[3:]; w = int(h * 720 / 1280); cols = min(len(fs), 8); rows = (len(fs) + cols - 1) // cols
S = Image.new('RGB', (cols * (w + 4), rows * (h + 18)), (18, 18, 22)); d = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    x, y = (i % cols) * (w + 4), (i // cols) * (h + 18); d.text((x + 3, y + 3), os.path.basename(f), fill=(255, 255, 255))
    S.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y + 18))
S.save(out, quality=88)
