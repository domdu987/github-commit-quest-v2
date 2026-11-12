"""Upscale the 3D frames to 1080x1920, draw captions / HUD / belief bar / sound words, mux the EP.2 mix (from 53.02 s). usage: python3 finish.py <raw dir> <out.mp4>"""
import os, sys, json, re, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); MW = '/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/mw'
FONT = os.path.join(os.path.dirname(HERE), 'fonts', 'Kanit_900Black.ttf'); FPS = 30; T0 = 53.02; DUR = 13.18
F = lambda n: ImageFont.truetype(FONT, n, layout_engine=ImageFont.Layout.RAQM)
lines = {l['id']: l for l in json.load(open(os.path.join(MW, 'jk2/ep2V/lines.json')))}
CAPS = []
for lid, t0, frags in (('p8', 0.0, [0, 1.69, 5.2, 6.48]), ('p9', 9.42, [0, 1.12])):
    parts = lines[lid]['cap'].split(' / ')
    for i, txt in enumerate(parts): CAPS.append((t0 + frags[i], txt))
def cap_at(t):
    cur = None
    for (a, txt) in CAPS:
        if t >= a: cur = txt
    return cur
def draw_cap(im, txt, y=1222, size=66):
    d = ImageDraw.Draw(im); f = F(size)
    segs = []; 
    for m in re.finditer(r'\{([^}]*)\}|\[([^\]]*)\]|([^\[\]{}]+)', txt):
        if m.group(1) is not None: segs.append((m.group(1), 'box'))
        elif m.group(2) is not None: segs.append((m.group(2), 'yel'))
        else: segs.append((m.group(3), 'w'))
    W = sum(d.textlength(s, font=f) + (24 if k == 'box' else 0) for s, k in segs); x = (1080 - W) / 2
    for s, k in segs:
        w = d.textlength(s, font=f)
        if k == 'box':
            d.rounded_rectangle((x, y - size * 0.62, x + w + 24, y + size * 0.62), radius=12, fill=(214, 64, 52)); x += 12
            d.text((x, y), s, font=f, fill='white', anchor='lm', stroke_width=0); x += w + 12
        else:
            d.text((x, y), s, font=f, fill=(255, 214, 74) if k == 'yel' else 'white', anchor='lm', stroke_width=8, stroke_fill=(24, 16, 28)); x += w
def panel(im, box, r, fill, outline=None):
    L = Image.new('RGBA', im.size); ImageDraw.Draw(L).rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=2); im.alpha_composite(L)
def hud(im, n):
    f1 = F(30); f2 = F(44); d = ImageDraw.Draw(im); parts = [('อันดับ', f1, (236, 226, 206)), ('9,999', f2, (255, 138, 122)), ('|', f1, (120, 110, 120)), ('คนเชื่อ', f1, (236, 226, 206)), (f'{n}/100', f2, (242, 197, 92))]
    W = sum(d.textlength(t, font=f) for t, f, c in parts) + 14 * 4
    panel(im, (44, 120, 44 + W + 44, 182), 20, (20, 18, 28, 200)); d = ImageDraw.Draw(im); x = 66
    for t, f, c in parts: d.text((x, 151), t, font=f, fill=c, anchor='lm'); x += d.textlength(t, font=f) + 14
def bar(im, pct):
    d = ImageDraw.Draw(im); x0, y0, w = 220, 268, 640
    panel(im, (x0 - 24, y0 - 62, x0 + w + 24, y0 + 62), 26, (18, 20, 30, 205), (244, 236, 216, 64)); d = ImageDraw.Draw(im)
    d.text((x0, y0 - 22), 'คนเชื่อ', font=F(30), fill=(244, 236, 216), anchor='lm'); d.text((x0 + w, y0 - 22), f'{int(round(pct))}/100', font=F(36), fill=(242, 197, 92), anchor='rm')
    d.rounded_rectangle((x0, y0 + 4, x0 + w, y0 + 38), radius=17, fill=(42, 42, 58))
    if pct > 0.5: d.rounded_rectangle((x0, y0 + 4, x0 + w * pct / 100, y0 + 38), radius=17, fill=(246, 190, 40))
def word(im, txt, xy, size, col, rot=0, alpha=255):
    f = F(size); L = Image.new('RGBA', (1080, 1920)); d = ImageDraw.Draw(L)
    d.text(xy, txt, font=f, fill=col + (alpha,), anchor='mm', stroke_width=10, stroke_fill=(40, 20, 10, alpha))
    if rot: L = L.rotate(rot, center=xy, resample=Image.BICUBIC)
    im.alpha_composite(L)
def badge(im):
    panel(im, (36, 1726, 316, 1770), 12, (20, 18, 28, 150)); d = ImageDraw.Draw(im); d.text((52, 1748), 'สกิลจอมโกหก · EP.2', font=F(26), fill=(236, 226, 206), anchor='lm')
def frame(src, g):
    t = g / FPS; im = Image.open(src).convert('RGB').resize((1080, 1920), Image.LANCZOS).convert('RGBA')
    crash = min(1, max(0, (t - 6.6) / 0.45)); n = 64 if t < 6.6 else int(round(64 * (1 - crash)))
    if t < 9.42: hud(im, n)
    else: hud(im, 0)
    if 5.2 <= t < 9.42:
        k = min(1, (t - 5.2) / 0.25); bar(im, 64 * (1 - crash) if t >= 6.6 else 64)
        if t >= 7.0: s = min(1, (t - 7.0) / 0.18); word(im, '0%', (900, 420), int(150 * (1.6 - 0.6 * s)), (230, 60, 50), rot=-8)
    if 3.0 <= t < 5.2: a = int(255 * min(1, (t - 3.0) / 0.15)); word(im, 'ฮ่าฮ่าฮ่า', (760, 560 - int(30 * ((t * 4) % 1))), 96, (255, 214, 74), rot=10, alpha=a)
    c = cap_at(t)
    if c: draw_cap(im, c)
    badge(im)
    return im.convert('RGB')
if __name__ == '__main__':
    raw, out = sys.argv[1], sys.argv[2]; tmp = os.path.join(HERE, 'fin'); os.makedirs(tmp, exist_ok=True)
    fs = sorted(f for f in os.listdir(raw) if f.startswith('f_'))
    for f in fs:
        g = int(f[2:6]); frame(os.path.join(raw, f), g).save(os.path.join(tmp, f'g_{g:04d}.jpg'), quality=95)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, 'g_%04d.jpg'), '-ss', str(T0), '-t', str(DUR), '-i', os.path.join(MW, 'jk2/ep2V/mix.wav'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-af', 'afade=t=out:st=12.6:d=0.55', '-shortest', out], check=True)
    print('wrote', out)
