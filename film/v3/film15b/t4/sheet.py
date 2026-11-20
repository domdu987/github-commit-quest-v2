import sys, os
from PIL import Image
d = sys.argv[1]; out = sys.argv[2]; fr = sorted(f for f in os.listdir(d) if f.endswith('.png'))
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8; w = 180; h = 320
rows = (len(fr) + cols - 1) // cols; S = Image.new('RGB', (cols * w, rows * h))
for i, f in enumerate(fr): S.paste(Image.open(os.path.join(d, f)).convert('RGB').resize((w, h)), ((i % cols) * w, (i // cols) * h))
S.save(out, quality=88); print(len(fr))
