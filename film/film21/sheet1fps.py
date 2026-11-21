"""usage: python3 sheet1fps.py take.mkv first_g out.jpg  -> 1 fps sheet (270x480 tiles, film timestamp + g) for the QA §K float hunter"""
import sys, subprocess, tempfile, glob, os
from PIL import Image, ImageDraw
v, fg, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
d = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vf', 'select=not(mod(n\\,30))+eq(n\\,0)', '-vsync', '0', '-frame_pts', '1', d + '/f%05d.png'], check=True)
fs = sorted(glob.glob(d + '/f*.png')); cols = min(6, len(fs)); rows = (len(fs) + cols - 1) // cols
S = Image.new('RGB', (270 * cols, 500 * rows), (20, 20, 24)); dr = ImageDraw.Draw(S)
for i, f in enumerate(fs):
    n = int(os.path.basename(f)[1:6]); g = fg + n; x, y = (i % cols) * 270, (i // cols) * 500
    S.paste(Image.open(f).convert('RGB').resize((270, 480)), (x, y + 20)); dr.text((x + 4, y + 4), f'g{g}  t={g / 30:.2f}s', fill=(255, 255, 120))
S.save(out, quality=88); print(out, len(fs), 'tiles')
