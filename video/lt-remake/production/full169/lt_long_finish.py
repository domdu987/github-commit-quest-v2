"""ช่างเชื่อมสายฟ้า remake · full story 16:9 (YouTube): EP.1-4 raw 1280x720 Blender frames -> 1920x1080 with captions, HUD, stamps,
chapter titles, badge; per-EP mix (VO + music + SFX); segments joined, loudness-normalised once, end card.
usage: python3 lt_long_finish.py frames <ep> | mix <ep> | seg <ep> | card | final <out.mp4> | clean <ep>"""
import os, sys, json, re, subprocess, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MW = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'mw')
FONT = os.path.join(os.path.dirname(HERE), 'fonts', 'Kanit_900Black.ttf'); FPS = 30; SR = 48000; W, H = 1920, 1080; CARD = 6.0
F = lambda n: ImageFont.truetype(FONT, n, layout_engine=ImageFont.Layout.RAQM)
LINES = {l['id']: l for l in json.load(open(os.path.join(MW, 'lt2', 'lines.json')))}
DURS = json.load(open(os.path.join(MW, 'lt2', 'vo', 'durations.json')))
DUR = {1: 94.44, 2: 118.54, 3: 63.79, 4: 80.1}
TITLE = {1: 'ค่าแรงสี่ร้อยห้าสิบ กับสายฟ้าฟาดตึกเจ็ดชั้น', 2: 'กฎสามข้อหลังฝาตู้ไฟ กับกล้วยสุกทั้งเครือ', 3: 'ทารกสามคนในตู้อบ กับกฎข้อที่สามที่ถูกฝ่าฝืน', 4: 'วิธีปิดสวิตช์เทพเจ้าสายฟ้า กับค่าแรงที่เพิ่มขึ้นหนึ่งบาท'}
FIN = lambda ep: os.path.join(HERE, 'finL', 'ep%d' % ep)

def timeline(ep):
    ids = sorted(k for k in DURS if k.startswith('e%d_' % ep)); start = {}; t = 0.3
    for i in ids: start[i] = t; t += DURS[i] + 0.25
    caps = []
    for i in ids:
        parts = LINES[i]['cap'].split(' / '); w = [len(re.sub(r'[\[\]{}…\s]', '', p)) + 2 for p in parts]; acc = 0
        for p, k in zip(parts, w): caps.append((start[i] + DURS[i] * acc / sum(w), p)); acc += k
        caps.append((start[i] + DURS[i] + 0.05, None))
    return ids, start, caps

# ----------------------------------------------------------------------------- overlays (1920x1080)
def panel(im, box, r, fill):
    L = Image.new('RGBA', im.size); ImageDraw.Draw(L).rounded_rectangle(box, radius=r, fill=fill); im.alpha_composite(L)

def draw_cap(im, txt, y=968, size=58):
    d = ImageDraw.Draw(im); f = F(size); segs = []
    for m in re.finditer(r'\{([^}]*)\}|\[([^\]]*)\]|([^\[\]{}]+)', txt):
        if m.group(1) is not None: segs.append((m.group(1), 'box'))
        elif m.group(2) is not None: segs.append((m.group(2), 'yel'))
        else: segs.append((m.group(3), 'w'))
    Wt = sum(d.textlength(s, font=f) + (24 if k == 'box' else 0) for s, k in segs); x = (W - Wt) / 2
    for s, k in segs:
        w = d.textlength(s, font=f)
        if k == 'box':
            d.rounded_rectangle((x, y - size * 0.62, x + w + 24, y + size * 0.62), radius=12, fill=(214, 64, 52)); x += 12
            d.text((x, y), s, font=f, fill='white', anchor='lm'); x += w + 12
        else:
            d.text((x, y), s, font=f, fill=(255, 214, 74) if k == 'yel' else 'white', anchor='lm', stroke_width=8, stroke_fill=(24, 16, 28)); x += w

Wc = (236, 226, 206); SEP = ('|', (120, 110, 120)); RED = (255, 120, 100); YEL = (242, 197, 92); CY = (120, 220, 255); WH = (255, 255, 255)
HUDS = {
    1: [(0.0, [('แรงดันไฟในตัว', Wc), ('พุ่งทะลุขีดจำกัด!', RED), SEP, ('ค่าแรงวันนี้', Wc), ('450 บาท', YEL)]),
        (5.6, [('แรงดันไฟในตัว', Wc), ('25%', CY), SEP, ('ชาร์จไฟอัตโนมัติ', YEL)]),
        (11.15, [('อาชีพ', Wc), ('ช่างเชื่อม', WH), SEP, ('ค่าแรง', Wc), ('450 บาท', YEL)]),
        (21.0, [('หนี้มอเตอร์ไซค์', Wc), ('ค้างชำระ', RED), SEP, ('ค่าแรง', Wc), ('450 บาท', YEL)]),
        (42.25, [('แรงดันไฟในตัว', Wc), ('พุ่งทะลุขีดจำกัด!', RED), SEP, ('ค่าแรงวันนี้', Wc), ('450 บาท', YEL)]),
        (45.72, [('แรงดันไฟในตัว', Wc), ('25%', CY), SEP, ('สถานะ', Wc), ('ชาร์จไฟอัตโนมัติ', YEL)]),
        (75.26, [('ราคาประตู', Wc), ('ขึ้น 3 เท่า', RED), SEP, ('ค่าแรงคุณ', Wc), ('450 บาทเท่าเดิม!', YEL)])],
    2: [(0.0, [('รายได้เจ๊หงส์', Wc), ('3,000 บาท', YEL), SEP, ('ส่วนแบ่งของคุณ', Wc), ('0 บาท', RED), SEP, ('ความโกรธ', Wc), ('85%!', RED)]),
        (11.67, [('ผู้สอนวิชา', Wc), ('เฮียกิม', WH), ('(รุ่นพี่ฟ้าผ่า 40 ปีก่อน)', CY)]),
        (48.16, [('รายได้เจ๊หงส์', Wc), ('3,000 บาท', YEL), SEP, ('ส่วนแบ่งของคุณ', Wc), ('0 บาท', RED), SEP, ('ความโกรธ', Wc), ('85%!', RED)]),
        (74.6, [('แรงดันไฟความโกรธ', Wc), ('95%', RED), ('➔ ระบายลงต้นกล้วยทัน!', YEL)]),
        (85.44, None),
        (100.6, [('ผิดกฎข้อที่ 1', RED), ('จับเหล็กตอนตกใจ!', Wc), ('➔ หม้อแปลงหน้าซอยระเบิด!', YEL)])],
    3: [(0.0, [('แบตเตอรี่ตู้อบทารก', Wc), ('เหลือ 1%', RED), SEP, ('แรงดันไฟที่ต้องใช้', Wc), ('100%!', YEL)]),
        (30.29, 'pct'),
        (40.65, [('คำเตือน', RED), ('ผิดกฎข้อที่ 3 (ปล่อยไฟ 100%)!', Wc), SEP, ('ร่างกายกำลังสลายเป็นสายฟ้า!', CY)])],
    4: [(0.0, [('แรงดันไฟในตัว', Wc), ('100%', RED), ('(อันตรายถึงชีวิต)', RED), SEP, ('วิธีปิดสวิตช์', Wc), ('???', YEL)]),
        (21.46, [('นึกถึงค่าแรง 450 บาท', YEL), ('➔ หมดไฟทันที!', Wc), ('(แรงดันไฟลดเหลือ 0%)', CY)]),
        (41.58, None),
        (60.89, [('ค่าแรงใหม่', Wc), ('451 บาท', YEL), ('(+1 บาท)', CY), SEP, ('สถานะซอยฝั่งธน', Wc), ('ไม่เคยไฟดับอีกเลย', WH)])],
}
def hud(im, ep, t):
    cur = [p for a, p in HUDS[ep] if t >= a][-1]
    if cur is None: return
    if cur == 'pct':
        k = min(1.0, max(0.0, (t - 30.29) / 9.5)); pct = int(30 + 30 * k) if t < 36.4 else (60 if t < 40.0 else 99)
        cur = [('กำลังส่งกระแสไฟ', Wc), ('%d%%...' % pct, CY if pct < 99 else RED)]
    f = F(30); d = ImageDraw.Draw(im); Wt = sum(d.textlength(s, font=f) for s, c in cur) + 14 * (len(cur) - 1)
    panel(im, (40, 36, 40 + Wt + 44, 94), 18, (20, 18, 28, 205)); d = ImageDraw.Draw(im); x = 62
    for s, c in cur: d.text((x, 65), s, font=f, fill=c, anchor='lm'); x += d.textlength(s, font=f) + 14

def badge(im, ep):
    panel(im, (36, 1028, 380, 1066), 12, (20, 18, 28, 140)); ImageDraw.Draw(im).text((52, 1047), 'ช่างเชื่อมสายฟ้า · EP.%d' % ep, font=F(24), fill=Wc, anchor='lm')

def title(im, ep, t):
    if not 0.15 <= t < 3.4: return
    a = min(1.0, (t - 0.15) / 0.3, (3.4 - t) / 0.35); L = Image.new('RGBA', im.size); d = ImageDraw.Draw(L)
    f1, f2 = F(44), F(64); t2 = TITLE[ep]; w2 = d.textlength(t2, font=f2); cx = W / 2
    d.rounded_rectangle((cx - w2 / 2 - 40, 120, cx + w2 / 2 + 40, 300), 26, fill=(20, 18, 28, int(215 * a)))
    d.text((cx, 168), 'EP.%d' % ep + ('  ตอนจบ' if ep == 4 else ''), font=f1, fill=(255, 214, 74, int(255 * a)), anchor='mm')
    d.text((cx, 246), t2, font=f2, fill=(255, 255, 255, int(255 * a)), anchor='mm'); im.alpha_composite(L)

def battery(im, t, a0, a1, cx=1600, cy=420):
    if not (a0 <= t < a1 + 0.4): return
    k = min(1, max(0, (t - a0 - 0.3) / 1.6)); pop = min(1, (t - a0) / 0.2); s = 0.85 * (0.6 + 0.4 * pop); w, h = 150 * s, 270 * s
    L = Image.new('RGBA', im.size); d = ImageDraw.Draw(L)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=22 * s, fill=(28, 30, 40, 235), outline=(240, 240, 250, 255), width=int(6 * s))
    ih = (h - 30 * s) * k; col = (90, 230, 120, 255) if k >= 1 else (250, 200, 60, 255)
    d.rounded_rectangle((cx - w / 2 + 14 * s, cy + h / 2 - 15 * s - ih, cx + w / 2 - 14 * s, cy + h / 2 - 15 * s), radius=10 * s, fill=col)
    d.polygon([(cx + 10 * s, cy - 60 * s), (cx - 28 * s, cy + 8 * s), (cx - 2 * s, cy + 8 * s), (cx - 14 * s, cy + 62 * s), (cx + 30 * s, cy - 10 * s), (cx + 4 * s, cy - 10 * s)], fill=(255, 255, 255, 240))
    d.text((cx, cy + h / 2 + 46 * s), f'{int(round(100 * k))}%', font=F(int(60 * s)), fill=(255, 255, 255, 255), anchor='mm', stroke_width=7, stroke_fill=(20, 16, 28, 255))
    im.alpha_composite(L)

def stamp(im, t, t0, t1, txt, xy, col, size=120, rot=-8):
    if not t0 <= t < t1: return
    k = min(1.0, (t - t0) / 0.18); s = 1.6 - 0.6 * k
    L = Image.new('RGBA', im.size); d = ImageDraw.Draw(L); f = F(int(size * s))
    d.text(xy, txt, font=f, fill=col + (255,), anchor='mm', stroke_width=12, stroke_fill=(30, 14, 18, 255))
    im.alpha_composite(L.rotate(rot, center=xy, resample=Image.BICUBIC))

_VIG = None
def vignette(im):
    global _VIG
    if _VIG is None:
        y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / 1050.0) ** 2 + ((y - H * 0.47) / 640.0) ** 2)
        a = np.clip((r - 0.62) / 0.55, 0, 1) ** 1.6 * 150
        _VIG = Image.new('RGBA', (W, H), (14, 10, 30, 0)); _VIG.putalpha(Image.fromarray(a.astype('uint8')))
    im.alpha_composite(_VIG)

def blend(im, col, a): return Image.blend(im, Image.new('RGBA', im.size, col + (255,)), max(0.0, min(1.0, a)))
PULSES = [(0.0, 0.10, 1), (0.10, 0.17, 0), (0.17, 0.30, 1), (0.30, 0.37, 0), (0.37, 0.47, 1)]
def strike_fx(im, t, st):
    u = t - st; on = any(a <= u < b and v for a, b, v in PULSES)
    if 0 <= u < 0.034: return blend(im, (240, 248, 255), 0.9)
    if on: return blend(im, (225, 238, 255), 0.22)
    if 0 <= u < 0.6: return blend(im, (8, 6, 24), 0.25)
    return im
def flash(im, t, t0, dur=0.35, col=(235, 242, 255), a=0.75):
    u = t - t0
    return blend(im, col, a * (1 - u / dur)) if 0 <= u < dur else im
def sepia(im, k=0.85):
    g = im.convert('L'); sp = Image.merge('RGB', (g.point(lambda v: min(255, int(v * 1.07 + 18))), g.point(lambda v: int(v * 0.93 + 10)), g.point(lambda v: int(v * 0.74)))).convert('RGBA')
    return Image.blend(im, sp, k)

def effects(im, ep, t):
    if ep == 1:
        im = strike_fx(im, t, 3.35); im = strike_fx(im, t, 42.25)
        if 44.9 <= t < 45.72: im = blend(im, (255, 255, 255), (t - 44.9) / 0.8)
        if 45.72 <= t < 46.2: im = blend(im, (255, 255, 255), 1 - (t - 45.72) / 0.48)
        if 65.9 <= t < 67.85: im = blend(im, (6, 8, 26), 0.32)
        im = flash(im, t, 65.9, 0.07, (255, 250, 230), 0.5)
    if ep == 2:
        if 44.87 <= t < 48.16: im = sepia(im)
        for t0 in (86.2, 88.3, 100.6): im = flash(im, t, t0, 0.3)
        im = flash(im, t, 110.75, 0.6, (255, 200, 120), 0.85)
        if 113.6 <= t: im = blend(im, (6, 8, 26), 0.12)
    if ep == 3:
        for t0 in (7.6, 16.2, 19.4): im = flash(im, t, t0, 0.3, a=0.55)
        im = flash(im, t, 46.37, 0.7, (240, 248, 255), 0.95); im = flash(im, t, 49.55, 0.4, (255, 240, 200), 0.6)
        if t > DUR[3] - 1.4: im = blend(im, (230, 244, 255), (t - (DUR[3] - 1.4)) / 1.4)
    if ep == 4:
        if t < 0.6: im = blend(im, (230, 244, 255), 1 - t / 0.6)
        im = flash(im, t, 12.2, 0.3, a=0.5); im = flash(im, t, 16.3, 0.3, a=0.5); im = flash(im, t, 28.0, 0.25, (200, 230, 255), 0.6)
        if t > DUR[4] - 1.0: im = blend(im, (8, 6, 20), (t - (DUR[4] - 1.0)) / 1.0 * 0.0)
    return im

def overlays(im, ep, t):
    if ep == 1:
        battery(im, t, 7.2, 10.6); battery(im, t, 50.9, 54.5)
        stamp(im, t, 76.4, 80.06, '×3', (1500, 380), (255, 214, 74), 170, -10); stamp(im, t, 81.2, 83.52, '450 บาท', (1380, 400), (255, 255, 255), 120, 8)
        for k, kt in enumerate((87.6, 88.0, 88.4)): stamp(im, t, kt, kt + 0.5, 'ก๊อก!', (760 + k * 230, 360 - k * 50), (255, 236, 200), 96, -6 + k * 7)
    if ep == 2:
        battery(im, t, 51.6, 54.2)
        stamp(im, t, 63.4, 65.16, '0 บาท', (1450, 400), (255, 120, 100), 130, 7)
        stamp(im, t, 82.9, 85.44, 'สุกทั้งเครือ!', (1420, 300), (255, 214, 74), 96, -6)
        stamp(im, t, 110.8, 113.0, 'ตูม!', (1460, 330), (255, 170, 80), 190, -8)
    if ep == 3:
        stamp(im, t, 46.4, 48.75, 'เปรี้ยง!', (1440, 330), (200, 236, 255), 180, -8)
    if ep == 4:
        stamp(im, t, 22.6, 26.94, '450 บาท', (1460, 380), (255, 214, 74), 140, -8)
        stamp(im, t, 67.0, 69.4, '451 บาท', (1440, 320), (255, 214, 74), 150, -6); stamp(im, t, 67.5, 69.4, '(+1)', (1500, 470), (120, 220, 255), 100, 6)

def src_of(ep, g):
    if ep == 1: return os.path.join(HERE, 'raw_ppL' if g < 777 else 'raw_ep1L', 'f_%04d.jpg' % g)
    return os.path.join(HERE, 'raw_ep%dL' % ep, 'f_%04d.jpg' % g)

def frame(ep, g, caps):
    t = g / FPS; im = Image.open(src_of(ep, g)).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    im = effects(im, ep, t); vignette(im); hud(im, ep, t); overlays(im, ep, t)
    if ep > 1: title(im, ep, t)
    cur = None
    for a, txt in caps:
        if t >= a: cur = txt
    if cur: draw_cap(im, cur)
    badge(im, ep); return im.convert('RGB')

def cmd_frames(ep, lo=0, hi=None):
    _, _, caps = timeline(ep); N = int(round(DUR[ep] * FPS)); os.makedirs(FIN(ep), exist_ok=True); miss = []
    for g in range(lo, hi if hi is not None else N):
        dst = os.path.join(FIN(ep), 'g_%04d.jpg' % g)
        if os.path.exists(dst): continue
        if not os.path.exists(src_of(ep, g)): miss.append(g); continue
        frame(ep, g, caps).save(dst, quality=93)
    print('frames ep%d missing %d %s' % (ep, len(miss), miss[:6]))

# ----------------------------------------------------------------------------- sound
def load(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-']); return np.frombuffer(raw, np.float32).copy()
def ff(x, af):
    o = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', af, '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-'], input=np.ascontiguousarray(x, np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(o, np.float32); return np.pad(y, (0, max(0, len(x) - len(y))))[:len(x)].copy()
def level(x, db):
    r = np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2) + 1e-12); return x * (10 ** (db / 20) / r)
MUS = {2: [(0.0, 11.67, 'quest', 0.0), (11.67, 25.73, 'musicbox', 0.0), (25.73, 48.16, 'tension', 10.0), (48.16, 74.6, 'quest', 20.0), (74.6, 85.44, 'tension', 30.0), (85.44, 118.54, 'tension', 40.0)],
       3: [(0.0, 12.93, 'tension', 0.0), (12.93, 33.03, 'tension', 15.0), (33.03, 46.37, 'musicbox', 10.0), (46.37, 54.25, 'quest', 40.0), (54.25, 63.79, 'tension', 50.0)],
       4: [(0.0, 21.46, 'tension', 0.0), (21.46, 35.4, 'tension', 30.0), (35.4, 53.6, 'musicbox', 20.0), (53.6, 73.33, 'quest', 10.0), (73.33, 80.1, 'musicbox', 60.0)]}
CUTS = {2: [3.6, 7.05, 11.67, 16.42, 22.7, 25.73, 29.82, 34.66, 40.35, 44.87, 48.16, 51.3, 54.57, 58.73, 61.9, 63.4, 65.16, 69.46, 74.6, 77.0, 80.31, 85.44, 89.3, 95.63, 98.58, 104.77, 107.4, 110.48, 113.6, 116.0],
        3: [3.3, 6.72, 12.93, 15.4, 17.86, 20.79, 25.66, 30.29, 33.03, 36.25, 40.65, 46.37, 48.75, 51.5, 54.25, 59.04],
        4: [5.9, 11.53, 16.09, 18.62, 21.46, 26.94, 29.4, 31.81, 35.4, 38.5, 41.58, 47.63, 50.2, 53.6, 57.3, 60.89, 66.36, 69.4, 73.33]}
EVENTS = {
    2: [('zap', 1.0, 0.35), ('zap', 2.6, 0.3), ('zap', 4.4, 0.35), ('ding', 54.2, 0.35), ('pop', 56.0, 0.35), ('pop', 63.4, 0.4), ('boom', 69.6, 0.25), ('zap', 74.7, 0.4),
        ('riser', 82.0, 0.25), ('ding', 82.9, 0.4), ('boom', 86.2, 0.55), ('boom', 88.3, 0.45), ('boom', 100.6, 0.7), ('zap', 100.7, 0.6), ('riser', 104.8, 0.3),
        ('zap', 105.0, 0.45), ('zap', 108.0, 0.45), ('boom', 110.75, 1.0), ('pop', 110.76, 0.6), ('glitch', 111.0, 0.2), ('heartbeat', 116.2, 0.5)],
    3: [('heartbeat', 0.4, 0.45), ('heartbeat', 3.4, 0.45), ('boom', 7.6, 0.5), ('boom', 16.2, 0.45), ('boom', 19.4, 0.4), ('zap', 28.4, 0.5), ('zap', 30.4, 0.55), ('ding', 33.5, 0.4),
        ('ding', 34.9, 0.4), ('heartbeat', 36.5, 0.5), ('heartbeat', 38.4, 0.45), ('riser', 41.0, 0.35), ('zap', 43.5, 0.6), ('boom', 46.37, 1.0), ('pop', 46.38, 0.6), ('ding', 46.6, 0.4),
        ('riser', 49.0, 0.3), ('ding', 49.6, 0.35), ('zap', 54.4, 0.5), ('riser', 58.0, 0.35), ('zap', 59.2, 0.55)],
    4: [('zap', 0.3, 0.45), ('boom', 12.2, 0.45), ('boom', 16.3, 0.55), ('ding', 22.6, 0.35), ('glitch', 28.0, 0.3), ('pop', 28.05, 0.5), ('pop', 32.35, 0.6), ('boom', 32.36, 0.25),
        ('ding', 35.6, 0.35), ('pop', 44.6, 0.35), ('ding', 47.8, 0.35), ('ding', 67.0, 0.45), ('pop', 67.5, 0.35)],
}
def cmd_mix(ep):
    n = int(DUR[ep] * SR)
    if ep == 1:
        x = load(os.path.join(HERE, 'ep1_mix_raw.wav'))[:n]; np.save(os.path.join(HERE, 'mixL_ep1.npy'), np.pad(x, (0, n - len(x)))); print('mix ep1 reused'); return
    ids, start, _ = timeline(ep); vo = np.zeros(n, np.float32)
    for i in ids:
        x = load(os.path.join(MW, 'lt2', 'vo', i + '.wav')); a = int(start[i] * SR); vo[a:a + len(x)] += x[:n - a]
    vo = ff(vo, 'afftdn=nf=-55:nr=10:tn=1,deesser=i=0.7:m=0.6:f=0.4,treble=g=-5:f=6500:t=s:w=0.7')
    md = '/home/user/github-commit-quest-v2/video/lt-ep1/music/suno'; trk = {k: load(os.path.join(md, k + '.mp3')) for k in ('tension', 'quest', 'musicbox')}
    mus = np.zeros(n, np.float32)
    for a, b, k, off in MUS[ep]:
        src = trk[k]; ia, ib = int(a * SR), int(b * SR); L = ib - ia; o = int(off * SR) % max(1, len(src) - SR)
        seg = np.concatenate([src[o:], src])[:L] if L > 0 else np.zeros(0, np.float32); seg = np.pad(seg, (0, max(0, L - len(seg)))).copy(); fd = int(0.35 * SR)
        seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); mus[ia:ia + len(seg)] += seg[:n - ia]
    mus = ff(level(mus, -30), 'treble=g=-5:f=8000:t=s:w=0.7')
    sys.path.insert(0, MW); import synth
    sfx = np.zeros(n, np.float32)
    def put(kind, t, g=1.0, af=None):
        x = np.asarray(synth.sfx(kind), np.float32)
        if x.ndim > 1: x = x.mean(axis=1)
        x = np.interp(np.arange(int(len(x) * SR / 44100)) * 44100 / SR, np.arange(len(x)), x).astype(np.float32)
        if af: x = ff(x, af)
        a = int(t * SR); sfx[a:a + len(x)] += g * x[:max(0, n - a)]
    for c in CUTS[ep]: put('whoosh', c - 0.12, 0.24, 'lowpass=f=1200')
    for kind, t, g in EVENTS[ep]: put(kind, t, g, {'boom': 'lowpass=f=400', 'pop': 'lowpass=f=2500', 'ding': 'lowpass=f=4000', 'zap': None, 'riser': 'lowpass=f=3000', 'heartbeat': 'lowpass=f=600', 'glitch': 'lowpass=f=2000'}.get(kind))
    sfx = level(sfx, -27)
    env = np.convolve(np.abs(vo), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same')
    duck = 1 - 0.6 * np.clip(env / (np.percentile(env[env > 1e-4], 50) + 1e-9), 0, 1); duck = np.convolve(duck, np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
    mix = vo + mus * duck + sfx; np.save(os.path.join(HERE, 'mixL_ep%d.npy' % ep), mix.astype(np.float32)); print('mix ep%d' % ep, DUR[ep])

def cmd_seg(ep):
    out = os.path.join(HERE, 'segL_ep%d.mp4' % ep)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(FIN(ep), 'g_%04d.jpg'), '-frames:v', str(int(round(DUR[ep] * FPS))),
                    '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS), out], check=True)
    print('wrote', out)

def cmd_card():
    last = os.path.join(FIN(4), 'g_%04d.jpg' % (int(round(DUR[4] * FPS)) - 1)); bg = os.path.join(HERE, 'long_card_bg.png'); Image.open(last).save(bg)
    out = os.path.join(HERE, 'finL', 'card'); os.makedirs(out, exist_ok=True)
    subprocess.run(['python3', os.path.join(os.path.dirname(os.path.dirname(HERE)), 'card2.py'), bg, out, 'ช่างเชื่อมสายฟ้า · จบ', 'L', str(CARD)], check=True)
    fs = sorted(f for f in os.listdir(out) if f.endswith('.png')); step = max(1, round(len(fs) / (CARD * FPS)))
    od = os.path.join(HERE, 'finL', 'cardj'); os.makedirs(od, exist_ok=True)
    for k, f in enumerate(fs[::step]): Image.open(os.path.join(out, f)).convert('RGB').resize((W, H)).save(os.path.join(od, 'g_%04d.jpg' % k), quality=93)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(od, 'g_%04d.jpg'), '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-pix_fmt', 'yuv420p', os.path.join(HERE, 'segL_card.mp4')], check=True)
    print('card', len(fs[::step]))

def cmd_final(out):
    segs = [os.path.join(HERE, 'segL_ep%d.mp4' % e) for e in (1, 2, 3, 4)] + [os.path.join(HERE, 'segL_card.mp4')]
    lst = os.path.join(HERE, 'segL.txt'); open(lst, 'w').write(''.join("file '%s'\n" % s for s in segs))
    mix = np.concatenate([np.load(os.path.join(HERE, 'mixL_ep%d.npy' % e)) for e in (1, 2, 3, 4)])
    md = '/home/user/github-commit-quest-v2/video/lt-ep1/music/suno'; q = load(os.path.join(md, 'quest.mp3'))[int(30 * SR): int((30 + CARD) * SR)]
    q = level(q, -30) * np.linspace(1, 0, len(q)) ** 0.5; mix = np.concatenate([mix, q])
    pk = np.abs(mix).max()
    if pk > 0.98: mix = np.tanh(mix / pk * 1.2) * 0.95
    raw = os.path.join(HERE, 'mixL_raw.wav'); fin = os.path.join(HERE, 'mixL.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-ac', '2', raw], input=mix.astype(np.float32).tobytes(), check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', 'loudnorm=I=-14:TP=-2:LRA=11', '-ar', '48000', fin], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', fin, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    print('wrote', out)

def cmd_clean(ep):
    import shutil
    shutil.rmtree(FIN(ep), ignore_errors=True); print('removed', FIN(ep))

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'frames': cmd_frames(int(sys.argv[2]), *(int(x) for x in sys.argv[3:5]))
    elif c == 'mix': cmd_mix(int(sys.argv[2]))
    elif c == 'seg': cmd_seg(int(sys.argv[2]))
    elif c == 'card': cmd_card()
    elif c == 'final': cmd_final(sys.argv[2])
    elif c == 'clean': cmd_clean(int(sys.argv[2]))
