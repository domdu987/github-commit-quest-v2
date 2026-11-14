"""Finish the Part-2 3D look test: raw 1280x720 -> 1920x1080 with captions + badge; VO s19 + s22, music, SFX; mux.
usage: python3 p2finish.py frames | mix | mux <out.mp4>"""
import os, sys, json, re, subprocess, random
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'lt3d'))
import lt_long_finish as LF
FPS = 30; SR = 48000; DUR = 13.5; W, H = 1920, 1080; RAW = os.path.join(HERE, 'raw'); FIN = os.path.join(HERE, 'fin')
MWJ = os.path.join(LF.MW, 'jk2', 'seq')
LINES = {l['id']: l for l in json.load(open('/home/user/github-commit-quest-v2/video/jk-long/production/sequel/lines.json'))}
def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
IDS = ['s19', 's22']; START = {'s19': 0.3}; START['s22'] = 0.3 + dur(os.path.join(MWJ, 'vo_clean', 's19.wav')) + 0.25
CAPS = []
for i in IDS:
    d = dur(os.path.join(MWJ, 'vo_clean', i + '.wav')); parts = LINES[i]['cap'].split(' / '); w = [len(re.sub(r'[\[\]{}…\s]', '', p)) + 2 for p in parts]; acc = 0
    for p, k in zip(parts, w): CAPS.append((START[i] + d * acc / sum(w), p)); acc += k
    CAPS.append((START[i] + d + 0.05, None))

def badge(im):
    LF.panel(im, (36, 1028, 520, 1066), 12, (20, 18, 28, 140)); ImageDraw.Draw(im).text((52, 1047), 'สกิลจอมโกหก ภาค 2 · อัศวินถังไม้', font=LF.F(24), fill=LF.Wc, anchor='lm')

def cmd_frames():
    os.makedirs(FIN, exist_ok=True); N = int(round(DUR * FPS)); miss = []
    for g in range(N):
        src = os.path.join(RAW, 'f_%04d.jpg' % g); dst = os.path.join(FIN, 'g_%04d.jpg' % g)
        if os.path.exists(dst): continue
        if not os.path.exists(src): miss.append(g); continue
        t = g / FPS; im = Image.open(src).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
        if 2.95 <= t < 3.15: im = LF.blend(im, (255, 236, 200), 0.35 * (1 - (t - 2.95) / 0.2))
        if t < 0.4: im = LF.blend(im, (0, 0, 0), 1 - t / 0.4)
        LF.vignette(im)
        cur = None
        for a, txt in CAPS:
            if t >= a: cur = txt
        if cur: LF.draw_cap(im, cur)
        badge(im); im.convert('RGB').save(dst, quality=93)
    print('frames missing', len(miss), miss[:5])

def cmd_mix():
    n = int(DUR * SR); vo = np.zeros(n, np.float32)
    for i in IDS:
        x = LF.load(os.path.join(MWJ, 'vo_clean', i + '.wav')); a = int(START[i] * SR); vo[a:a + len(x)] += x[:n - a]
    vo = LF.ff(vo, 'afftdn=nf=-55:nr=10:tn=1,deesser=i=0.7:m=0.6:f=0.4,treble=g=-5:f=6500:t=s:w=0.7')
    md = '/home/user/github-commit-quest-v2/video/lt-ep1/music/suno'; mus = LF.load(os.path.join(md, 'tension.mp3'))[int(8 * SR): int(8 * SR) + n]
    mus = np.pad(mus, (0, n - len(mus))); fd = int(0.4 * SR); mus[:fd] *= np.linspace(0, 1, fd); mus[-fd:] *= np.linspace(1, 0, fd)
    mus = LF.ff(LF.level(mus, -29), 'treble=g=-5:f=8000:t=s:w=0.7')
    sys.path.insert(0, LF.MW); import synth
    sfx = np.zeros(n, np.float32)
    def put(kind, t, g=1.0, af=None):
        x = np.asarray(synth.sfx(kind), np.float32)
        if x.ndim > 1: x = x.mean(axis=1)
        x = np.interp(np.arange(int(len(x) * SR / 44100)) * 44100 / SR, np.arange(len(x)), x).astype(np.float32)
        if af: x = LF.ff(x, af)
        a = int(t * SR); sfx[a:a + len(x)] += g * x[:max(0, n - a)]
    for c in (2.9, 5.6, 9.2): put('whoosh', c - 0.12, 0.25, 'lowpass=f=1200')
    put('boom', 2.95, 0.9, 'lowpass=f=300'); put('boom', 3.05, 0.6, 'lowpass=f=200,atempo=0.8'); put('riser', 1.0, 0.25, 'lowpass=f=2000')
    put('pop', 7.6, 0.4, 'lowpass=f=2500'); put('ding', 11.0, 0.45, 'lowpass=f=5000'); put('ding', 11.25, 0.3, 'lowpass=f=6000')
    sfx = LF.level(sfx, -27)
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
    duck = 1 - 0.6 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1); duck = np.convolve(duck, np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
    mix = vo + mus * duck + sfx; pk = np.abs(mix).max()
    if pk > 0.98: mix = np.tanh(mix / pk * 1.2) * 0.95
    raw = os.path.join(HERE, 'mix_raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ac', '2', raw], input=mix.astype(np.float32).tobytes(), check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', 'loudnorm=I=-14:TP=-2:LRA=11', '-ar', '48000', os.path.join(HERE, 'mix.wav')], check=True); print('mix ok')

def cmd_mux(out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(FIN, 'g_%04d.jpg'), '-i', os.path.join(HERE, 'mix.wav'), '-map', '0:v', '-map', '1:a',
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True); print('wrote', out)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'frames': cmd_frames()
    elif c == 'mix': cmd_mix()
    elif c == 'mux': cmd_mux(sys.argv[2])
