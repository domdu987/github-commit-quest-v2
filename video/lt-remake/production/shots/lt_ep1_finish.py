"""Finish ช่างเชื่อมสายฟ้า EP.1: look-test frames (0..REUSE_T, overlays already burned in) + raw_ep1 Blender frames -> 1080x1920
with captions / HUD / inserts, then the YouTube end card, mixed VO + music + SFX.
usage: python3 lt_ep1_finish.py mix | frames | card | mux <out.mp4>"""
import os, sys, json, re, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lt_finish2 as F           # draw_cap, panel, battery, badge, vignette, load, ff, level
import lt_ep1 as E
MW = F.MW; FPS = 30; SR = 48000; DUR = E.DUR; CARD = 5.0
LOOK = os.path.join(HERE, 'LOOK4-welder-3d-ep1.mp4'); FIN = os.path.join(HERE, 'fin_ep1')
LINES = {l['id']: l for l in json.load(open(os.path.join(MW, 'lt2', 'lines.json')))}
DURS = json.load(open(os.path.join(MW, 'lt2', 'vo', 'durations.json')))
IDS = ['e1_%02d' % i for i in range(1, 22)]; START = {}
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

W_ = (236, 226, 206); SEP = ('|', (120, 110, 120)); RED = (255, 120, 100); YEL = (242, 197, 92); CY = (120, 220, 255)
HUDS = [(25.9, [('หนี้มอเตอร์ไซค์', W_), ('ค้างชำระ', RED), SEP, ('ค่าแรง', W_), ('450 บาท', YEL)]),
        (E.ST2, [('แรงดันไฟในตัว', W_), ('พุ่งทะลุขีดจำกัด!', RED), SEP, ('ค่าแรงวันนี้', W_), ('450 บาท', YEL)]),
        (45.72, [('แรงดันไฟในตัว', W_), ('25%', CY), SEP, ('สถานะ', W_), ('ชาร์จไฟอัตโนมัติ', YEL)]),
        (75.26, [('ราคาประตู', W_), ('ขึ้น 3 เท่า', RED), SEP, ('ค่าแรงคุณ', W_), ('450 บาทเท่าเดิม!', YEL)])]
def hud(im, t):
    parts = [p for a, p in HUDS if t >= a][-1]; f = F.F(32); d = ImageDraw.Draw(im)
    W = sum(d.textlength(s, font=f) for s, c in parts) + 14 * (len(parts) - 1)
    F.panel(im, (40, 110, 40 + W + 44, 172), 20, (20, 18, 28, 205)); d = ImageDraw.Draw(im); x = 62
    for s, c in parts: d.text((x, 141), s, font=f, fill=c, anchor='lm'); x += d.textlength(s, font=f) + 14

def stamp(im, t, t0, txt, xy, col, size=120, rot=-8):
    if t < t0: return
    k = min(1.0, (t - t0) / 0.18); s = 1.6 - 0.6 * k
    L = Image.new('RGBA', im.size); d = ImageDraw.Draw(L); f = F.F(int(size * s))
    d.text(xy, txt, font=f, fill=col + (255,), anchor='mm', stroke_width=12, stroke_fill=(30, 14, 18, 255))
    im.alpha_composite(L.rotate(rot, center=xy, resample=Image.BICUBIC))

def badge(im):
    F.panel(im, (36, 1800, 380, 1846), 12, (20, 18, 28, 150)); d = ImageDraw.Draw(im); d.text((52, 1823), 'ช่างเชื่อมสายฟ้า · EP.1', font=F.F(26), fill=(236, 226, 206), anchor='lm')

def frame(src, g):
    t = g / FPS; im = Image.open(src).convert('RGB').resize((1080, 1920), Image.LANCZOS).convert('RGBA')
    u = t - E.ST2
    if 0 <= u < 0.034: im = Image.blend(im, Image.new('RGBA', im.size, (240, 248, 255, 255)), 0.9)
    elif E.strike_on(t): im = Image.blend(im, Image.new('RGBA', im.size, (225, 238, 255, 255)), 0.22)
    elif 0 <= u < 0.6: im = Image.blend(im, Image.new('RGBA', im.size, (8, 6, 24, 255)), 0.25)
    if 44.9 <= t < 45.72: im = Image.blend(im, Image.new('RGBA', im.size, (255, 255, 255, 255)), min(1, (t - 44.9) / 0.8))      # white-out into the hospital
    if 45.72 <= t < 46.2: im = Image.blend(im, Image.new('RGBA', im.size, (255, 255, 255, 255)), 1 - (t - 45.72) / 0.48)
    if E.BLACKOUT <= t < 67.85: im = Image.blend(im, Image.new('RGBA', im.size, (6, 8, 26, 255)), 0.32)
    if E.BLACKOUT <= t < E.BLACKOUT + 0.07: im = Image.blend(im, Image.new('RGBA', im.size, (255, 250, 230, 255)), 0.5)
    F.vignette(im); hud(im, t)
    if 50.9 <= t < 54.9: F.battery(im, t, a0=50.9, a1=54.5)
    if 76.4 <= t < 80.06: stamp(im, t, 76.4, '×3', (830, 520), (255, 214, 74), 170, -10)
    if 81.2 <= t < 83.52: stamp(im, t, 81.2, '450 บาท', (560, 520), (255, 255, 255), 120, 8)
    for k, kt in enumerate(E.KNOCK):
        if kt <= t < kt + 0.5: stamp(im, t, kt, 'ก๊อก!', (300 + k * 230, 700 - k * 60), (255, 236, 200), 96, -6 + k * 7)
    c = cap_at(t)
    if c: F.draw_cap(im, c)
    badge(im); return im.convert('RGB')

def cmd_frames():
    os.makedirs(FIN, exist_ok=True)
    n0 = int(round(E.REUSE_T * FPS))
    if not os.path.exists(os.path.join(FIN, 'g_%04d.jpg' % (n0 - 1))):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', LOOK, '-frames:v', str(n0), '-q:v', '2', os.path.join(FIN, 'g_%04d.jpg')], check=True)
        # ffmpeg numbers from 1: shift to 0-based
        for g in range(1, n0 + 1): os.replace(os.path.join(FIN, 'g_%04d.jpg' % g), os.path.join(FIN, 'h_%04d.jpg' % (g - 1)))
        for g in range(n0): os.replace(os.path.join(FIN, 'h_%04d.jpg' % g), os.path.join(FIN, 'g_%04d.jpg' % g))
    miss = []
    for g in range(n0, E.N):
        src = os.path.join(E.RAW, 'f_%04d.jpg' % g); dst = os.path.join(FIN, 'g_%04d.jpg' % g)
        if not os.path.exists(src): miss.append(g); continue
        if not os.path.exists(dst): frame(src, g).save(dst, quality=94)
    print('frames ok, missing', len(miss), miss[:5])

def cmd_card():
    """5 s YouTube end card on the blurred last frame (vertical layout of card2.py)."""
    last = os.path.join(FIN, 'g_%04d.jpg' % (E.N - 1)); bg = os.path.join(HERE, 'ep1_card_bg.png')
    Image.open(last).resize((1080, 1920)).save(bg)
    out = os.path.join(FIN, 'card'); os.makedirs(out, exist_ok=True)
    subprocess.run(['python3', os.path.join(os.path.dirname(os.path.dirname(HERE)), 'card2.py'), bg, out, 'ช่างเชื่อมสายฟ้า · EP.1', 'V', str(CARD)], check=True)
    n = len([f for f in os.listdir(out) if f.endswith('.png')])
    for i in range(n): Image.open(os.path.join(out, '%04d.png' % i)).convert('RGB').save(os.path.join(FIN, 'g_%04d.jpg' % (E.N + i)), quality=94)
    print('card frames', n)

def cmd_mix():
    n = int((DUR + CARD) * SR); vo = np.zeros(n, np.float32)
    for i in IDS:
        x = F.load(os.path.join(MW, 'lt2', 'vo', i + '.wav')); a = int(START[i] * SR); vo[a:a + len(x)] += x[:n - a]
    vo = F.ff(vo, 'afftdn=nf=-55:nr=10:tn=1,deesser=i=0.7:m=0.6:f=0.4,treble=g=-5:f=6500:t=s:w=0.7')
    md = '/home/user/github-commit-quest-v2/video/lt-ep1/music/suno'
    ten = F.load(os.path.join(md, 'tension.mp3')); qst = F.load(os.path.join(md, 'quest.mp3')); box = F.load(os.path.join(md, 'musicbox.mp3'))
    plan = [(0.0, 11.15, ten, 0.0), (11.15, 25.9, qst, 0.0), (25.9, 45.72, ten, 20.0), (45.72, 63.53, box, 0.0), (63.53, 83.52, qst, 15.0), (83.52, DUR, ten, 40.0), (DUR, DUR + CARD, qst, 30.0)]
    mus = np.zeros(n, np.float32)
    for a, b, src, off in plan:
        ia, ib = int(a * SR), int(b * SR); seg = src[int(off * SR): int(off * SR) + ib - ia]
        seg = np.pad(seg, (0, max(0, ib - ia - len(seg)))); fd = int(0.35 * SR)
        seg = seg.copy(); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); mus[ia:ia + len(seg)] += seg[:n - ia]
    mus[:int(0.25 * SR)] *= np.linspace(0, 1, int(0.25 * SR))
    mus[int(E.ST2 * SR):int((E.ST2 + 1.0) * SR)] *= 0.3                     # the strike punches through
    mus = F.ff(F.level(mus, -30), 'treble=g=-5:f=8000:t=s:w=0.7')
    sys.path.insert(0, MW); import synth
    sfx = np.zeros(n, np.float32)
    def put(kind, t, g=1.0, af=None):
        x = np.asarray(synth.sfx(kind), np.float32)
        if x.ndim > 1: x = x.mean(axis=1)
        x = np.interp(np.arange(int(len(x) * SR / 44100)) * 44100 / SR, np.arange(len(x)), x).astype(np.float32)
        if af: x = F.ff(x, af)
        a = int(t * SR); sfx[a:a + len(x)] += g * x[:max(0, n - a)]
    # 0..REUSE_T exactly as the approved look test
    import lt_look2 as LK
    for s in LK.SHOTS[1:]:
        if s['n'] not in ('R3', 'R3b'): put('whoosh', s['t0'] - 0.12, 0.26, 'lowpass=f=1200')
    put('boom', LK.ST, 1.0, 'lowpass=f=400'); put('pop', LK.ST + 0.01, 0.6, 'lowpass=f=2500'); put('pop', LK.ST + 0.18, 0.35, 'lowpass=f=2000'); put('pop', LK.ST + 0.38, 0.3, 'lowpass=f=2000')
    put('ding', 9.2, 0.35, 'lowpass=f=4000'); put('pop', 22.1, 0.35, 'lowpass=f=2500')
    for s in E.SHOTS:
        if s['n'] not in ('E10b', 'E10c', 'H11a') and s['t0'] > 26: put('whoosh', s['t0'] - 0.12, 0.26, 'lowpass=f=1200')
    put('boom', E.ST2, 1.0, 'lowpass=f=400'); put('pop', E.ST2 + 0.01, 0.6, 'lowpass=f=2500'); put('pop', E.ST2 + 0.18, 0.35, 'lowpass=f=2000'); put('pop', E.ST2 + 0.38, 0.3, 'lowpass=f=2000')
    for k, py in enumerate((9.4, 7.0, 4.6, 2.2)): put('ding', 51.2 + k * 0.85, 0.3, 'lowpass=f=4000')      # phones jumping to 100%
    put('pop', 57.4, 0.4, 'lowpass=f=2500'); put('riser', 61.0, 0.25, 'lowpass=f=3000')
    put('pop', E.BLACKOUT - 0.02, 0.5, 'lowpass=f=1500'); put('boom', E.BLACKOUT, 0.35, 'lowpass=f=300')
    put('pop', 68.9, 0.45, 'lowpass=f=2500'); put('pop', 71.9, 0.3, 'lowpass=f=2500'); put('ding', 73.4, 0.35, 'lowpass=f=4000')
    put('pop', 76.4, 0.45, 'lowpass=f=2500'); put('pop', 81.2, 0.45, 'lowpass=f=2000')
    for kt in E.KNOCK: put('tick', kt, 0.9, 'lowpass=f=900')
    put('whoosh', E.DOOR_OPEN[0], 0.25, 'lowpass=f=700')
    sfx = F.level(sfx, -27)
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
    duck = 1 - 0.6 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1); duck = np.convolve(duck, np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
    mix = vo + mus * duck + sfx; pk = np.abs(mix).max()
    if pk > 0.98: mix = np.tanh(mix / pk * 1.2) * 0.95
    out = os.path.join(HERE, 'ep1_mix_raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ac', '2', out], input=mix.astype(np.float32).tobytes(), check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-af', 'loudnorm=I=-13.3:TP=-2.2:LRA=11', '-ar', '48000', os.path.join(HERE, 'ep1_mix.wav')], check=True)
    print('mix ok', DUR + CARD)

def cmd_mux(out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(FIN, 'g_%04d.jpg'), '-i', os.path.join(HERE, 'ep1_mix.wav'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '256k',
                    '-af', 'afade=t=out:st=%.2f:d=0.8' % (DUR + CARD - 0.8), '-shortest', '-movflags', '+faststart', out], check=True)
    print('wrote', out)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'mix': cmd_mix()
    elif c == 'frames': cmd_frames()
    elif c == 'card': cmd_card()
    elif c == 'mux': cmd_mux(sys.argv[2])
