"""Finish the welder look test: 720x1280 Blender frames -> 1080x1920 with captions, HUD, battery, flash, badge; mix VO + music + SFX.
usage: python3 lt_finish.py mix | frames | mux <out.mp4>"""
import os, sys, json, re, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); MW = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'mw')
sys.path.insert(0, HERE); import lt_look as LK
FONT = os.path.join(os.path.dirname(HERE), 'fonts', 'Kanit_900Black.ttf'); FPS = 30; DUR = LK.DUR; SR = 48000
F = lambda n: ImageFont.truetype(FONT, n, layout_engine=ImageFont.Layout.RAQM)
LINES = {l['id']: l for l in json.load(open(os.path.join(MW, 'lt2', 'lines.json')))}
DURS = json.load(open(os.path.join(MW, 'lt2', 'vo', 'durations.json')))
IDS = ['e1_01', 'e1_02', 'e1_03', 'e1_04', 'e1_05']; START = {}
t = 0.3
for i in IDS: START[i] = t; t += DURS[i] + 0.25
CAPS = []
for i in IDS:
    parts = LINES[i]['cap'].split(' / '); w = [len(re.sub(r'[\[\]{}…\s]', '', p)) + 2 for p in parts]; acc = 0
    for p, k in zip(parts, w): CAPS.append((START[i] + DURS[i] * acc / sum(w), p)); acc += k
    CAPS.append((START[i] + DURS[i] + 0.05, None))
def cap_at(t):
    cur = None
    for a, txt in CAPS:
        if t >= a: cur = txt
    return cur

def draw_cap(im, txt, y=1300, size=64):
    d = ImageDraw.Draw(im); f = F(size); segs = []
    for m in re.finditer(r'\{([^}]*)\}|\[([^\]]*)\]|([^\[\]{}]+)', txt):
        if m.group(1) is not None: segs.append((m.group(1), 'box'))
        elif m.group(2) is not None: segs.append((m.group(2), 'yel'))
        else: segs.append((m.group(3), 'w'))
    W = sum(d.textlength(s, font=f) + (24 if k == 'box' else 0) for s, k in segs); x = (1080 - W) / 2
    for s, k in segs:
        w = d.textlength(s, font=f)
        if k == 'box':
            d.rounded_rectangle((x, y - size * 0.62, x + w + 24, y + size * 0.62), radius=12, fill=(214, 64, 52)); x += 12
            d.text((x, y), s, font=f, fill='white', anchor='lm'); x += w + 12
        else:
            d.text((x, y), s, font=f, fill=(255, 214, 74) if k == 'yel' else 'white', anchor='lm', stroke_width=8, stroke_fill=(24, 16, 28)); x += w

def panel(im, box, r, fill, outline=None):
    L = Image.new('RGBA', im.size); ImageDraw.Draw(L).rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=2); im.alpha_composite(L)

HUDS = [(0.0, [('แรงดันไฟในตัว', (236, 226, 206)), ('พุ่งทะลุขีดจำกัด!', (255, 120, 100)), ('|', (120, 110, 120)), ('ค่าแรงวันนี้', (236, 226, 206)), ('450 บาท', (242, 197, 92))]),
        (5.6, [('แรงดันไฟในตัว', (236, 226, 206)), ('25%', (120, 220, 255)), ('|', (120, 110, 120)), ('ชาร์จไฟอัตโนมัติ', (242, 197, 92))]),
        (11.15, [('อาชีพ', (236, 226, 206)), ('ช่างเชื่อม', (255, 255, 255)), ('|', (120, 110, 120)), ('ค่าแรง', (236, 226, 206)), ('450 บาท', (242, 197, 92))]),
        (21.0, [('หนี้มอเตอร์ไซค์', (236, 226, 206)), ('ค้างชำระ', (255, 120, 100)), ('|', (120, 110, 120)), ('ค่าแรง', (236, 226, 206)), ('450 บาท', (242, 197, 92))])]
def hud(im, t):
    parts = [p for a, p in HUDS if t >= a][-1]; f = F(32); d = ImageDraw.Draw(im)
    W = sum(d.textlength(s, font=f) for s, c in parts) + 14 * (len(parts) - 1)
    panel(im, (40, 110, 40 + W + 44, 172), 20, (20, 18, 28, 205)); d = ImageDraw.Draw(im); x = 62
    for s, c in parts: d.text((x, 141), s, font=f, fill=c, anchor='lm'); x += d.textlength(s, font=f) + 14

def battery(im, t, a0=7.2, a1=10.6):
    if not (a0 <= t < a1 + 0.4): return
    k = min(1, max(0, (t - a0 - 0.3) / 1.6)); pop = min(1, (t - a0) / 0.2)
    cx, cy = 820, 560; s = 1.0 * (0.6 + 0.4 * pop); w, h = 150 * s, 270 * s
    L = Image.new('RGBA', im.size); d = ImageDraw.Draw(L)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=22 * s, fill=(28, 30, 40, 235), outline=(240, 240, 250, 255), width=int(6 * s))
    ih = (h - 30 * s) * k; col = (90, 230, 120, 255) if k >= 1 else (250, 200, 60, 255)
    d.rounded_rectangle((cx - w / 2 + 14 * s, cy + h / 2 - 15 * s - ih, cx + w / 2 - 14 * s, cy + h / 2 - 15 * s), radius=10 * s, fill=col)
    d.polygon([(cx + 10 * s, cy - 60 * s), (cx - 28 * s, cy + 8 * s), (cx - 2 * s, cy + 8 * s), (cx - 14 * s, cy + 62 * s), (cx + 30 * s, cy - 10 * s), (cx + 4 * s, cy - 10 * s)], fill=(255, 255, 255, 240))
    d.text((cx, cy + h / 2 + 46 * s), f'{int(round(100 * k))}%', font=F(int(60 * s)), fill=(255, 255, 255, 255), anchor='mm', stroke_width=7, stroke_fill=(20, 16, 28, 255))
    im.alpha_composite(L)

def badge(im):
    panel(im, (36, 1800, 380, 1846), 12, (20, 18, 28, 150)); d = ImageDraw.Draw(im); d.text((52, 1823), 'ช่างเชื่อมสายฟ้า · EP.1', font=F(26), fill=(236, 226, 206), anchor='lm')

_VIG = None
def vignette(im):
    global _VIG
    if _VIG is None:
        import numpy as np
        y, x = np.mgrid[0:1920, 0:1080]; r = np.sqrt(((x - 540) / 620.0) ** 2 + ((y - 900) / 1080.0) ** 2)
        a = np.clip((r - 0.62) / 0.55, 0, 1) ** 1.6 * 150
        _VIG = Image.new('RGBA', (1080, 1920), (14, 10, 30, 0)); _VIG.putalpha(Image.fromarray(a.astype('uint8')))
    im.alpha_composite(_VIG)

def frame(src, g):
    t = g / FPS; im = Image.open(src).convert('RGB').resize((1080, 1920), Image.LANCZOS).convert('RGBA')
    if 4.5 <= t < 4.62: im = Image.blend(im, Image.new('RGBA', im.size, (235, 245, 255, 255)), 0.85)
    elif 4.62 <= t < 4.8: im = Image.blend(im, Image.new('RGBA', im.size, (235, 245, 255, 255)), 0.35)
    vignette(im); hud(im, t); battery(im, t)
    c = cap_at(t)
    if c: draw_cap(im, c)
    badge(im); return im.convert('RGB')

def load(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-']); return np.frombuffer(raw, np.float32).copy()
def ff(x, af):
    o = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', af, '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-'], input=np.ascontiguousarray(x, np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(o, np.float32); return np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)].copy()
def level(x, db):
    r = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2) + 1e-12); return x * (10 ** (db / 20) / r)

def cmd_mix():
    n = int(DUR * SR); vo = np.zeros(n, np.float32)
    for i in IDS:
        x = load(os.path.join(MW, 'lt2', 'vo', i + '.wav')); a = int(START[i] * SR); vo[a:a + len(x)] += x[:n - a]
    vo = ff(vo, 'afftdn=nf=-55:nr=10:tn=1,deesser=i=0.7:m=0.6:f=0.4,treble=g=-5:f=6500:t=s:w=0.7')
    mdir = '/home/user/github-commit-quest-v2/video/lt-ep1/music/suno'
    m1 = load(os.path.join(mdir, 'tension.mp3')); m2 = load(os.path.join(mdir, 'quest.mp3'))
    mus = np.zeros(n, np.float32); cut = int(11.15 * SR); a = m1[:cut]; mus[:len(a)] = a
    b = m2[:n - cut]; mus[cut:cut + len(b)] = b
    xf = int(0.5 * SR); mus[cut - xf:cut] *= np.linspace(1, 0.2, xf); mus[cut:cut + xf] *= np.linspace(0.2, 1, xf)
    mus[:int(0.25 * SR)] *= np.linspace(0, 1, int(0.25 * SR)); mus[-int(1.0 * SR):] *= np.linspace(1, 0, int(1.0 * SR))
    mus = ff(level(mus, -30), 'treble=g=-5:f=8000:t=s:w=0.7')
    sys.path.insert(0, MW); import synth
    sfx = np.zeros(n, np.float32)
    def put(kind, t, g=1.0, af=None):
        x = np.asarray(synth.sfx(kind), np.float32)
        if x.ndim > 1: x = x.mean(axis=1)
        x = np.interp(np.arange(int(len(x) * SR / 44100)) * 44100 / SR, np.arange(len(x)), x).astype(np.float32)
        if af: x = ff(x, af)
        a = int(t * SR); sfx[a:a + len(x)] += g * x[:n - a]
    for s in LK.SHOTS[1:]:
        if s['n'] not in ('R3',): put('whoosh', s['t0'] - 0.12, 0.26, 'lowpass=f=1200')
    put('boom', 4.5, 0.9, 'lowpass=f=400'); put('pop', 4.52, 0.5, 'lowpass=f=2500')
    put('ding', 9.2, 0.35, 'lowpass=f=4000'); put('pop', 22.1, 0.35, 'lowpass=f=2500')
    sfx = level(sfx, -27)
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
    duck = 1 - 0.6 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1); duck = np.convolve(duck, np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
    mix = vo + mus * duck + sfx; pk = np.abs(mix).max()
    if pk > 0.98: mix = np.tanh(mix / pk * 1.2) * 0.95
    out = os.path.join(HERE, 'lt_mix_raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ac', '2', out], input=mix.astype(np.float32).tobytes(), check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-af', 'loudnorm=I=-13.3:TP=-2.2:LRA=11', '-ar', '48000', os.path.join(HERE, 'lt_mix.wav')], check=True)
    print('mix ok', DUR)

def cmd_frames():
    raw = LK.RAW; tmp = os.path.join(HERE, 'fin_lt'); os.makedirs(tmp, exist_ok=True)
    for f in sorted(os.listdir(raw)):
        if f.startswith('f_'):
            g = int(f[2:6]); frame(os.path.join(raw, f), g).save(os.path.join(tmp, f'g_{g:04d}.jpg'), quality=94)
    print('frames ok')

def cmd_mux(out):
    tmp = os.path.join(HERE, 'fin_lt')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, 'g_%04d.jpg'), '-i', os.path.join(HERE, 'lt_mix.wav'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
    print('wrote', out)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'mix': cmd_mix()
    elif c == 'frames': cmd_frames()
    elif c == 'mux': cmd_mux(sys.argv[2])
