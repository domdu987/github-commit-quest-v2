"""jimo_sheet.py : contact sheets. run(): contact.jpg (all 26 finals, label under each tile, cyan line at y 880) + contact_small.jpg (1/3 size) from set_work/final/sNN.png."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'set_work')

def sheet(files, out, cols=7, small=None, scale=1.0, line=True):
    W, H = 720, 1280; tw, th = int(W * scale), int(H * scale); gap = max(4, int(10 * scale)); cap = int(34 * scale) + 6; rows = (len(files) + cols - 1) // cols
    C = Image.new('RGB', (cols * (tw + gap) + gap, rows * (th + cap + gap) + gap), (16, 16, 24)); d = ImageDraw.Draw(C)
    try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', max(11, int(26 * scale)))
    except Exception: fnt = ImageFont.load_default()
    for i, (label, fp) in enumerate(files):
        r, c = divmod(i, cols); x = gap + c * (tw + gap); y = gap + r * (th + cap + gap)
        if os.path.exists(fp):
            im = Image.open(fp).convert('RGB').resize((tw, th), Image.LANCZOS); C.paste(im, (x, y))
            if line: d.line([(x, y + int(880 * scale)), (x + tw - 1, y + int(880 * scale))], fill=(0, 230, 255), width=max(1, int(2 * scale)))
        d.text((x + 4, y + th + 4), label, fill=(235, 235, 245), font=fnt)
    C.save(out, quality=90); return out

def run(arg=()):
    sys.path.insert(0, HERE); import jimo_shots as S
    files = [('s%02d  %s %s' % (sh['n'], sh['loc'], sh['light']), os.path.join(WORK, 'final', 's%02d.png' % sh['n'])) for sh in S.SHOTS.values()]
    sheet(files, os.path.join(HERE, 'contact.jpg'), cols=7)
    sheet(files, os.path.join(HERE, 'contact_small.jpg'), cols=7, scale=1 / 3.0)
    print('contact.jpg, contact_small.jpg')

if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'drafts':
        names = sys.argv[3:]; sheet([(n, os.path.join(WORK, 'stills', n + '.png')) for n in names], sys.argv[2], cols=min(7, len(names)), scale=0.5)
    else: run()
