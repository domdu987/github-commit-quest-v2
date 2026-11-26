"""contact_A.jpg: the LOOK A finals (joseon_work/final_A/, raw, ungraded) graded with the v1.1 grade (grade_frame) for the sheet; the graded PNGs go to joseon_work/final_A_graded/.
6 columns, label under each tile, cyan y-880 line (as contact.jpg).  usage: python3 make_contact_A.py [g]   (g = film frame for the per-shot correction, default 300)"""
import os, sys, importlib.util
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
GP = os.path.join(PROJ, 'v3', 'film', 'out_v11', 'grade.py')
if not os.path.exists(GP): GP = os.path.join(PROJ, 'skill', 'reference-style-shorts', 'pipeline', 'v3', 'film', 'out_v11', 'grade.py')
spec = importlib.util.spec_from_file_location('grade_v11', GP); G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
g = int(sys.argv[1]) if len(sys.argv) > 1 else 300
src = os.path.join(HERE, 'joseon_work', 'final_A'); dst = os.path.join(HERE, 'joseon_work', 'final_A_graded'); os.makedirs(dst, exist_ok=True)
rows_ = [l.strip().split('|') for l in open(os.path.join(HERE, 'contact_order.txt')) if l.strip()]
W, H, LB, C = 720, 1280, 56, 6
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
rows = (len(rows_) + C - 1) // C
S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S)
for i, (n, lab) in enumerate(rows_):
    im = Image.open(os.path.join(src, n + '.png')).convert('RGB'); im = G.grade_frame(im, g); im.save(os.path.join(dst, n + '.png'))
    x, y = (i % C) * W, (i // C) * (H + LB); S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2)
    d.text((x + 12, y + H + 11), 'A ' + lab, fill=(235, 235, 235), font=F)
S.save(os.path.join(HERE, 'contact_A.jpg'), quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_A_small.jpg'), quality=88)
print(S.size, len(rows_))
