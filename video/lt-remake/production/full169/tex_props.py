"""Textures for the EP.2-4 props of ช่างเชื่อมสายฟ้า remake (PIL, drawn, no AI): Kim's old fuse box, the charging-table sign,
the babies, the nursery drawing, incubator panels, control-room panels. build_all() -> {name: png path}."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'props_tex'); FD = os.path.join(os.path.dirname(HERE), 'fonts')
INK = (34, 24, 30)
def font(name, size): return ImageFont.truetype(os.path.join(FD, name), size)
def KAN(s): return font('Kanit_900Black.ttf', s)
def HAND(s): return font('sriracha.ttf', s)
def MALI(s): return font('mali7.ttf', s)

def noise_paint(W, H, base, rng, rust=0.0, scratches=0, streaks=0):
    im = Image.new('RGB', (W, H), base); d = ImageDraw.Draw(im)
    for _ in range(W * H // 900):                     # mottled paint
        x, y = rng.randrange(W), rng.randrange(H); r = rng.randint(4, 26); k = rng.uniform(-14, 14)
        d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(max(0, min(255, int(c + k))) for c in base))
    im = im.filter(ImageFilter.GaussianBlur(6)); d = ImageDraw.Draw(im)
    for _ in range(int(rust * 40)):                   # rust blooms: soft, brown, irregular
        x, y = rng.randrange(W), rng.randrange(H)
        for q in range(5):
            r = rng.randint(2, 8); ox, oy = rng.randint(-10, 10), rng.randint(-7, 7)
            d.ellipse((x + ox - r, y + oy - r * 0.7, x + ox + r, y + oy + r * 0.7), fill=(rng.randint(104, 124), rng.randint(74, 86), rng.randint(56, 66)))
    for _ in range(streaks):                          # rust running down
        x = rng.randrange(W); y = rng.randrange(H // 3); L = rng.randint(H // 6, H // 2)
        d.line((x, y, x + rng.randint(-6, 6), y + L), fill=(128, 70, 42), width=rng.randint(2, 5))
    im = im.filter(ImageFilter.GaussianBlur(1.2)); d = ImageDraw.Draw(im)
    for _ in range(scratches):
        x, y = rng.randrange(W), rng.randrange(H); a = rng.uniform(0, math.pi); L = rng.randint(10, 60)
        d.line((x, y, x + L * math.cos(a), y + L * math.sin(a)), fill=tuple(min(255, c + 40) for c in base), width=1)
    return im

def outline_box(d, box, w=6, r=10):
    d.rounded_rectangle(box, r, outline=INK, width=w)

def fuse_box(rng):
    out = {}
    W, H = 512, 704
    body = noise_paint(W, H, (98, 128, 112), rng, rust=1.0, scratches=40, streaks=10); outline_box(ImageDraw.Draw(body), (0, 0, W - 1, H - 1), 10, 4)
    out['fb_body'] = body
    door = noise_paint(W, H, (104, 136, 118), rng, rust=1.4, scratches=60, streaks=14); d = ImageDraw.Draw(door)
    outline_box(d, (6, 6, W - 7, H - 7), 10, 6)
    # yellow warning sticker, half peeled
    st = Image.new('RGBA', (300, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.polygon([(150, 18), (288, 270), (12, 270)], fill=(250, 206, 40), outline=INK); sd.line([(150, 18), (288, 270), (12, 270), (150, 18)], fill=INK, width=12)
    sd.polygon([(160, 90), (118, 180), (152, 180), (134, 246), (190, 150), (156, 150), (176, 90)], fill=INK)
    door.paste(st.rotate(4, resample=Image.BICUBIC), (106, 70), st.rotate(4, resample=Image.BICUBIC))
    d.text((W // 2, 420), 'อันตราย', font=KAN(64), fill=(200, 40, 34), anchor='mm', stroke_width=4, stroke_fill=(250, 236, 210))
    d.text((W // 2, 492), 'ไฟฟ้าแรงสูง', font=KAN(52), fill=(200, 40, 34), anchor='mm', stroke_width=4, stroke_fill=(250, 236, 210))
    d.rounded_rectangle((W - 70, H // 2 - 50, W - 40, H // 2 + 50), 8, fill=(60, 60, 66), outline=INK, width=5)       # latch
    out['fb_door_out'] = door
    # inside of the door: dark green paint, three rules in white marker (Kim's handwriting)
    inn = noise_paint(W, H, (38, 66, 56), rng, rust=0.5, scratches=30, streaks=4); d = ImageDraw.Draw(inn)
    outline_box(d, (6, 6, W - 7, H - 7), 10, 6)
    d.text((W // 2, 74), 'กฎเหล็ก 3 ข้อ', font=HAND(66), fill=(248, 240, 214), anchor='mm')
    d.line((96, 118, W - 96, 122), fill=(248, 240, 214), width=6)
    rules = [('1', 'ตกใจ', 'ห้ามจับเหล็ก!'), ('2', 'โกรธ', 'รีบกอดต้นไม้!'), ('3', 'ห้ามปล่อยไฟ', 'เต็มร้อย!')]
    for k, (n, a, b) in enumerate(rules):
        y = 200 + k * 168
        d.ellipse((34, y - 40, 110, y + 36), outline=(250, 206, 60), width=7); d.text((72, y - 2), n, font=HAND(60), fill=(250, 206, 60), anchor='mm')
        d.text((132, y - 34), a, font=HAND(54), fill=(248, 240, 214), anchor='lm'); d.text((132, y + 30), b, font=HAND(54), fill=(255, 196, 160), anchor='lm')
    d.text((W - 40, H - 46), '- กิม 2529', font=HAND(34), fill=(200, 196, 178), anchor='rm')
    out['fb_door_in'] = inn
    # the panel inside: ceramic fuses + old breakers + wires
    pn = noise_paint(W, H, (176, 170, 150), rng, rust=0.3, scratches=20); d = ImageDraw.Draw(pn)
    outline_box(d, (4, 4, W - 5, H - 5), 8, 4)
    for row in range(3):
        for col in range(4):
            x = 70 + col * 112; y = 120 + row * 170
            d.rounded_rectangle((x - 36, y - 56, x + 36, y + 56), 10, fill=(236, 230, 214), outline=INK, width=5)
            d.rectangle((x - 14, y - 20, x + 14, y + 20), fill=(30, 30, 34)); d.rectangle((x - 9, y - (16 if (row + col) % 3 else -2), x + 9, y + (2 if (row + col) % 3 else 16)), fill=(220, 60, 50))
    for k in range(7):
        x0 = rng.randint(40, W - 40); d.line((x0, H, x0 + rng.randint(-60, 60), 600, x0 + rng.randint(-30, 30), 540), fill=[(30, 30, 30), (200, 40, 34), (40, 80, 200)][k % 3], width=9, joint='curve')
    out['fb_breakers'] = pn
    # the innermost steel plate (EP.4) and what is engraved behind it
    pl = noise_paint(W, H, (150, 156, 164), rng, rust=0.4, scratches=120); d = ImageDraw.Draw(pl)
    outline_box(d, (4, 4, W - 5, H - 5), 8, 4)
    for x, y in ((30, 30), (W - 30, 30), (30, H - 30), (W - 30, H - 30)):
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(110, 112, 120), outline=INK, width=4); d.line((x - 9, y, x + 9, y), fill=INK, width=4)
    d.text((W // 2, H // 2), 'ห้ามเปิด', font=HAND(70), fill=(90, 92, 100), anchor='mm')
    out['fb_plate'] = pl
    en = noise_paint(W, H, (186, 150, 86), rng, rust=0.2, scratches=60); d = ImageDraw.Draw(en)       # brass plate, engraved
    outline_box(d, (4, 4, W - 5, H - 5), 8, 4)
    for y, txt in ((250, 'สายฟ้า'), (340, 'ไม่ได้มีไว้ฟาด'), (470, 'แต่มีไว้'), (560, 'ให้แสง')):
        f = KAN(76 if y < 400 else 84)
        d.text((W // 2 + 3, y + 4), txt, font=f, fill=(250, 226, 160), anchor='mm'); d.text((W // 2, y), txt, font=f, fill=(92, 58, 22), anchor='mm')
    d.text((W // 2, 130), '⚡', font=KAN(90), fill=(92, 58, 22), anchor='mm') if False else d.polygon([(W // 2 + 10, 80), (W // 2 - 30, 150), (W // 2, 150), (W // 2 - 16, 200), (W // 2 + 34, 126), (W // 2 + 4, 126), (W // 2 + 24, 80)], fill=(92, 58, 22))
    out['fb_engraved'] = en
    return out

def sign(price, rng):
    W, H = 640, 480; im = Image.new('RGB', (W, H), (196, 150, 98)); d = ImageDraw.Draw(im)       # cardboard
    for _ in range(40): y = rng.randrange(H); d.line((0, y, W, y + rng.randint(-3, 3)), fill=(186, 140, 90), width=2)
    outline_box(d, (6, 6, W - 7, H - 7), 12, 10)
    d.text((W // 2, 78), 'ชาร์จมือถือ', font=KAN(84), fill=(30, 40, 120), anchor='mm')
    d.text((W // 2, 170), 'เต็ม 100% ใน 3 วิ!', font=HAND(62), fill=(200, 30, 30), anchor='mm')
    if price == 20:
        d.text((W // 2, 330), 'ครั้งละ 20.-', font=KAN(104), fill=INK, anchor='mm')
    else:
        d.text((W // 2 - 120, 312), '20', font=KAN(96), fill=INK, anchor='mm'); d.line((W // 2 - 190, 290, W // 2 - 50, 340), fill=(220, 30, 30), width=14)
        d.text((W // 2 + 90, 330), '30.-', font=KAN(120), fill=(220, 30, 30), anchor='mm')
    d.text((W // 2, 430), 'ร้านเหล็กดัดเจ๊หงส์', font=HAND(40), fill=(60, 40, 30), anchor='mm')
    return im

def baby(variant, rng):
    """A swaddled newborn lying on its back, seen from the side (head left), in the puppet style: white round head, thick ink."""
    W, H = 640, 360; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    wrap = [(250, 196, 210), (176, 214, 246), (250, 230, 170)][variant % 3]
    d.rounded_rectangle((180, 120, 600, 300), 90, fill=wrap, outline=INK, width=10)                    # swaddle
    for k in range(3): d.arc((250 + k * 90, 150, 330 + k * 90, 270), 300, 60, fill=tuple(int(c * 0.82) for c in wrap), width=8)
    d.ellipse((40, 70, 260, 290), fill=(250, 248, 244), outline=INK, width=10)                           # head
    d.chord((60, 50, 240, 170), 180, 360, fill=wrap, outline=INK, width=8)                                # little cap
    d.ellipse((126, 52, 152, 78), fill=wrap, outline=INK, width=6)
    for ex in (112, 176): d.arc((ex - 22, 168, ex + 22, 200), 0, 180, fill=INK, width=7)                   # sleeping eyes
    d.ellipse((134, 218, 154, 232), fill=INK)                                                             # mouth
    for ex in (92, 196): d.ellipse((ex - 18, 206, ex + 18, 226), fill=(255, 170, 170))                     # cheeks
    return im

def drawing(rng):
    """The nurses' crayon drawing: the welder with spiky lightning hair holding three babies, 'ฮีโร่ห้องเด็กอ่อน'."""
    W, H = 720, 540; im = Image.new('RGB', (W, H), (252, 250, 240)); d = ImageDraw.Draw(im)
    def cray(pts, col, w=9):
        for k in range(3):
            q = [(x + rng.uniform(-2, 2), y + rng.uniform(-2, 2)) for x, y in pts]; d.line(q, fill=col, width=w - k * 2, joint='curve')
    cray([(0, 470), (W, 470)], (90, 180, 90), 14)
    cray([(360, 300), (360, 420)], (40, 90, 200), 16); cray([(360, 420), (320, 470)], (40, 90, 200), 12); cray([(360, 420), (400, 470)], (40, 90, 200), 12)
    for k in range(13):
        a = math.pi * (0.1 + 0.8 * k / 12); cray([(360 + 70 * math.cos(a), 220 - 70 * math.sin(a)), (360 + 150 * math.cos(a), 220 - 150 * math.sin(a))], (30, 30, 30), 10)
    d.ellipse((290, 150, 430, 290), fill=(255, 255, 255), outline=(30, 30, 30), width=8)
    d.ellipse((330, 200, 346, 216), fill=(30, 30, 30)); d.ellipse((376, 200, 392, 216), fill=(30, 30, 30)); d.arc((330, 220, 392, 262), 20, 160, fill=(220, 40, 40), width=7)
    cray([(360, 330), (250, 300)], (40, 90, 200), 10); cray([(360, 330), (470, 300)], (40, 90, 200), 10)
    for k, x in enumerate((220, 360, 500)):
        y = 300 if k != 1 else 360; d.ellipse((x - 32, y - 26, x + 32, y + 26), fill=[(255, 190, 210), (180, 214, 250), (255, 230, 160)][k], outline=(30, 30, 30), width=5)
    for x0 in (80, 640):
        cray([(x0, 60), (x0 - 30, 130), (x0 + 6, 130), (x0 - 24, 200)], (250, 190, 20), 12)
    d.text((W // 2, 54), 'ฮีโร่ห้องเด็กอ่อน', font=MALI(64), fill=(220, 40, 60), anchor='mm')
    d.text((W - 30, H - 34), 'ขอบคุณค่ะ ♡' if False else 'ขอบคุณค่ะ', font=MALI(40), fill=(60, 90, 200), anchor='rm')
    return im

def incubator_panel(on):
    W, H = 256, 128; im = Image.new('RGB', (W, H), (16, 20, 24) if not on else (14, 30, 24)); d = ImageDraw.Draw(im)
    if on:
        d.text((16, 64), '36.8°', font=KAN(64), fill=(80, 255, 150), anchor='lm'); d.ellipse((214, 50, 238, 74), fill=(80, 255, 150))
    else:
        d.text((16, 64), 'LOW', font=KAN(56), fill=(255, 70, 50), anchor='lm'); d.ellipse((214, 50, 238, 74), fill=(255, 70, 50))
    return im

def ctrl_panels(rng):
    out = {}
    W, H = 1024, 768; im = noise_paint(W, H, (124, 134, 128), rng, rust=0.4, scratches=80, streaks=6); d = ImageDraw.Draw(im)
    for col in range(4):
        x0 = 20 + col * 252; d.rounded_rectangle((x0, 20, x0 + 232, H - 20), 10, fill=(150, 160, 152), outline=INK, width=7)
        for row in range(4):
            y = 110 + row * 160; d.ellipse((x0 + 30, y - 40, x0 + 110, y + 40), fill=(240, 236, 220), outline=INK, width=6)
            a = rng.uniform(-2.4, -0.6); d.line((x0 + 70, y, x0 + 70 + 32 * math.cos(a), y + 32 * math.sin(a)), fill=(200, 30, 30), width=5)
            d.rectangle((x0 + 140, y - 30, x0 + 200, y + 30), fill=(40, 42, 48), outline=INK, width=5); d.rectangle((x0 + 160, y - 22, x0 + 180, y + 2), fill=(230, 230, 230))
        d.text((x0 + 116, 52), ['MDB-1', 'MDB-2', 'ATS', 'GEN'][col], font=KAN(36), fill=INK, anchor='mm')
    out['ctrl_panel'] = im
    lab = Image.new('RGB', (512, 256), (250, 206, 40)); d = ImageDraw.Draw(lab); outline_box(d, (6, 6, 505, 249), 10, 6)
    d.text((256, 90), 'ห้องควบคุมไฟฟ้า', font=KAN(54), fill=INK, anchor='mm'); d.text((256, 180), 'เฉพาะเจ้าหน้าที่', font=KAN(44), fill=(200, 30, 30), anchor='mm')
    out['ctrl_sign'] = lab
    gen = noise_paint(512, 384, (60, 110, 70), rng, rust=0.8, streaks=8); d = ImageDraw.Draw(gen); outline_box(d, (6, 6, 505, 377), 10, 6)
    d.text((256, 120), 'เครื่องปั่นไฟ', font=KAN(52), fill=(240, 236, 220), anchor='mm'); d.rounded_rectangle((150, 200, 362, 300), 10, fill=(30, 30, 30), outline=INK, width=6)
    d.text((256, 250), 'ERROR', font=KAN(50), fill=(255, 60, 50), anchor='mm')
    out['ctrl_gen'] = gen
    nurs = Image.new('RGB', (768, 192), (250, 246, 236)); d = ImageDraw.Draw(nurs); outline_box(d, (6, 6, 761, 185), 10, 6)
    d.text((384, 96), 'ห้องเด็กอ่อน  NURSERY', font=KAN(64), fill=(220, 80, 120), anchor='mm')
    out['nurs_sign'] = nurs
    return out

def build_all():
    os.makedirs(OUT, exist_ok=True); rng = random.Random(20261114); P = {}
    T = dict(fuse_box(rng)); T['sign20'] = sign(20, rng); T['sign30'] = sign(30, rng); T['drawing'] = drawing(rng)
    for k in range(3): T['baby%d' % k] = baby(k, rng)
    T['incub_on'] = incubator_panel(True); T['incub_off'] = incubator_panel(False); T.update(ctrl_panels(rng))
    for k, im in T.items():
        p = os.path.join(OUT, k + '.png'); im.save(p); P[k] = p
    return P

if __name__ == '__main__':
    P = build_all(); print(len(P), 'textures in', OUT)
