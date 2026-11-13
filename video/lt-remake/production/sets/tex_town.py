"""SVG artwork for the town plaza surfaces, rasterised by Chromium (one launch for all). Cached by content hash."""
import os, json, hashlib, base64, subprocess, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'tex')
RASTER = os.path.join(os.path.dirname(HERE), 'v3', 'set3d', 'raster.js')
KANIT = base64.b64encode(open(os.path.join(os.path.dirname(HERE), 'fonts', 'Kanit_900Black.ttf'), 'rb').read()).decode()
FONT = f"<style>@font-face{{font-family:K;src:url(data:font/ttf;base64,{KANIT})}} text{{font-family:K}}</style>"

def svg(w, h, body, font=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block">{FONT if font else ""}{body}</svg>'

def rnd(seed): r = random.Random(seed); return r

def cobbles(seed=3, W=1024):
    r = rnd(seed); out = [f'<rect width="{W}" height="{W}" fill="#6e5f55"/>']
    rows = 16; ch = W / rows
    for j in range(rows):
        off = (j % 2) * ch * 0.5; x = -off
        while x < W:
            w = ch * r.uniform(0.85, 1.35); cx = x + w / 2; cy = j * ch + ch / 2
            base = r.choice(['#b9a690', '#c7b39b', '#a8957f', '#bfae95', '#b2a088', '#cbb8a0', '#9f8d78'])
            rx = w / 2 - 3; ry = ch / 2 - 3
            for dx in (-W, 0, W):
                out.append(f'<rect x="{cx-rx+dx:.1f}" y="{cy-ry:.1f}" width="{2*rx:.1f}" height="{2*ry:.1f}" rx="{ry*0.55:.1f}" fill="{base}"/>')
                out.append(f'<rect x="{cx-rx+3+dx:.1f}" y="{cy-ry+2:.1f}" width="{2*rx-8:.1f}" height="{ry*0.6:.1f}" rx="{ry*0.3:.1f}" fill="#fff" opacity=".13"/>')
                out.append(f'<path d="M{cx-rx+4+dx:.1f},{cy+ry-3:.1f}h{2*rx-8:.1f}" stroke="#4a3c34" stroke-width="3" opacity=".35"/>')
                if r.random() < 0.18: out.append(f'<path d="M{cx-rx*0.4+dx:.1f},{cy-ry*0.2:.1f}l{rx*0.3:.1f},{ry*0.5:.1f}l{rx*0.25:.1f},{-ry*0.2:.1f}" stroke="#5a4a40" stroke-width="1.6" fill="none" opacity=".5"/>')
            x += w
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, W); out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,6):.1f}" fill="#4a5a2c" opacity=".35"/>')
    return svg(W, W, ''.join(out))

def plaster(base, seed, W=1024, H=1024, timber=True, beams='#4a2e1c'):
    r = rnd(seed); o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']
    for _ in range(60):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(20,90):.0f}" ry="{r.uniform(10,50):.0f}" fill="#7a5a3a" opacity="{r.uniform(.03,.07):.3f}"/>')
    for _ in range(14):
        x, y = r.uniform(0, W), r.uniform(0, H); w = r.uniform(30, 70)
        o.append(f'<path d="M{x:.0f},{y:.0f}h{w:.0f}v{w*0.45:.0f}h{-w:.0f}z" fill="#a0846a" opacity=".18"/>')   # exposed bricks
    return o

def facade_guild(W=1800, H=2100):
    """Guild front 9 x 10.5 D (wall to z 6.8, gable to 10.5). Pixels: 200 per unit, y down from the top (z 10.5)."""
    k = 200; Z = lambda z: (10.5 - z) * k; X = lambda x: (x + 4.5) * k
    o = plaster('#efdcb8', 11, W, H)
    bm = '#4e301c'; bw = 26
    def beam(x0, z0, x1, z1, w=bw): o.append(f'<path d="M{X(x0):.0f},{Z(z0):.0f}L{X(x1):.0f},{Z(z1):.0f}" stroke="{bm}" stroke-width="{w}" stroke-linecap="square"/>'); o.append(f'<path d="M{X(x0):.0f},{Z(z0):.0f}L{X(x1):.0f},{Z(z1):.0f}" stroke="#7a5236" stroke-width="{w*0.3:.0f}" opacity=".5" transform="translate(-4,-4)"/>')
    for x in (-4.4, -2.85, -0.05, 2.85, 4.4): beam(x, 0, x, 6.8)
    for z in (0.12, 3.35, 4.35, 6.75): beam(-4.5, z, 4.5, z, 30)
    for a, b in ((-4.4, -2.85), (2.85, 4.4)):
        beam(a, 4.35, b, 6.75, 20); beam(b, 4.35, a, 6.75, 20)
    for a, b in ((-2.85, -0.05), (-0.05, 2.85)): beam(a, 0.12, (a + b) / 2, 1.6, 18) if False else None
    # gable: rafters, king post, struts
    beam(-4.5, 6.8, 0, 10.4, 30); beam(4.5, 6.8, 0, 10.4, 30); beam(0, 6.8, 0, 10.4, 24)
    beam(-2.2, 6.8, 0, 8.6, 18); beam(2.2, 6.8, 0, 8.6, 18)
    # stone plinth
    o.append(f'<rect x="0" y="{Z(0.55):.0f}" width="{W}" height="{0.55*k:.0f}" fill="#8e8274"/>')
    r = rnd(5)
    for i in range(30):
        x = i * 64 + (i % 2) * 20; o.append(f'<rect x="{x}" y="{Z(0.55)+6:.0f}" width="{r.uniform(50,62):.0f}" height="{0.25*k:.0f}" rx="6" fill="#a3978a"/><rect x="{x+28}" y="{Z(0.28)+4:.0f}" width="{r.uniform(50,62):.0f}" height="{0.22*k:.0f}" rx="6" fill="#9a8e80"/>')
    # gable mask outside the triangle -> transparent
    o.append(f'<path d="M0,0H{X(0)-0.1:.0f}L0,{Z(6.8):.0f}Z" fill="#000" class="cut"/><path d="M{W},0H{X(0)+0.1:.0f}L{W},{Z(6.8):.0f}Z" fill="#000" class="cut"/>')
    s = svg(W, H, ''.join(o))
    return s.replace('fill="#000" class="cut"', 'fill="#000" style="mix-blend-mode:destination-out"')

def facade_house(base, seed, W=1200, H=1200, wu=6.0, hu=6.0):
    k = W / wu; o = plaster(base, seed, W, H); r = rnd(seed); bm = r.choice(['#4e301c', '#3e2a1e', '#5a3820'])
    X = lambda x: x * k; Z = lambda z: (hu - z) * k
    def beam(x0, z0, x1, z1, w=20): o.append(f'<path d="M{X(x0):.0f},{Z(z0):.0f}L{X(x1):.0f},{Z(z1):.0f}" stroke="{bm}" stroke-width="{w}" stroke-linecap="square"/>')
    n = int(wu // 1.5)
    for i in range(n + 1): beam(i * wu / n, 0, i * wu / n, hu)
    for z in (0.1, hu / 2, hu - 0.05): beam(0, z, wu, z, 24)
    for i in range(n):
        if r.random() < 0.6: a, b = i * wu / n, (i + 1) * wu / n; beam(a, hu / 2, b, hu - 0.05, 14)
    o.append(f'<rect x="0" y="{Z(0.45):.0f}" width="{W}" height="{0.45*k:.0f}" fill="#857a6c"/>')
    return svg(W, H, ''.join(o))

def roof(seed, c1='#b5452e', c2='#963822', W=1024):
    r = rnd(seed); o = [f'<rect width="{W}" height="{W}" fill="{c2}"/>']; rows = 8; h = W / rows
    for j in range(rows):
        off = (j % 2) * 18
        for i in range(-1, 18):
            x = i * 60 + off; c = r.choice([c1, c1, c1, c2])
            o.append(f'<path d="M{x},{j*h}h56v{h*0.78:.0f}q-28,{h*0.3:.0f} -56,0z" fill="{c}"/><path d="M{x+4},{j*h+h*0.7:.0f}q24,{h*0.22:.0f} 48,0" stroke="#5a1e12" stroke-width="3" fill="none" opacity=".45"/>')
    return svg(W, W, ''.join(o))

def planks(seed, base='#7a4e2e', W=512, H=1024, n=6):
    r = rnd(seed); o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']; w = W / n
    for i in range(n):
        c = r.choice(['#7a4e2e', '#6e4428', '#865632', '#704a2c'])
        o.append(f'<rect x="{i*w+2:.0f}" y="0" width="{w-4:.0f}" height="{H}" fill="{c}"/>')
        for _ in range(5): y = r.uniform(0, H); o.append(f'<path d="M{i*w+8:.0f},{y:.0f}q{w*0.4:.0f},{r.uniform(-20,20):.0f} {w-16:.0f},0" stroke="#4a2e1a" stroke-width="2" fill="none" opacity=".45"/>')
        o.append(f'<rect x="{i*w:.0f}" y="0" width="3" height="{H}" fill="#3a2414"/>')
    for y in (H * 0.18, H * 0.82): o.append(f'<rect x="0" y="{y:.0f}" width="{W}" height="26" fill="#2e2a28"/><circle cx="40" cy="{y+13:.0f}" r="7" fill="#8a8680"/><circle cx="{W-40}" cy="{y+13:.0f}" r="7" fill="#8a8680"/>')
    return svg(W, H, ''.join(o))

def sign(text, W=1600, H=320, bg='#5a3420', fg='#f2c55c'):
    b = (f'<rect width="{W}" height="{H}" rx="40" fill="#3a2214"/><rect x="18" y="18" width="{W-36}" height="{H-36}" rx="28" fill="{bg}"/>'
         f'<rect x="34" y="34" width="{W-68}" height="{H-68}" rx="20" fill="none" stroke="#d8a840" stroke-width="6" opacity=".7"/>'
         f'<text x="{W/2}" y="{H*0.68:.0f}" text-anchor="middle" font-size="{H*0.5:.0f}" fill="{fg}" stroke="#2a1608" stroke-width="10" paint-order="stroke">{text}</text>')
    return svg(W, H, b, font=True)

def board(W=1520, H=1080):
    rows = [("1", "เซอร์อาเธอร์ผู้ไม่เคยแพ้", 0), ("2", "แม่มดดอกไม้เหล็ก", 0), ("3", "ยักษ์ใจดีแห่งภูเขา", 0), ("10", "เคน · ดาบแสง", 1), ("9,999", "คุณ · จอมโกหก (F)", 2)]
    o = [f'<rect width="{W}" height="{H}" fill="#5a3420"/><rect x="26" y="26" width="{W-52}" height="{H-52}" rx="10" fill="#f1e2c0"/>',
         f'<rect x="26" y="26" width="{W-52}" height="150" fill="#6b3d22"/><text x="{W/2}" y="135" text-anchor="middle" font-size="96" fill="#f2c55c">อันดับผู้กล้า</text>']
    y = 210
    for i, (n, name, kind) in enumerate(rows):
        if i == 4: o.append(f'<text x="{W/2}" y="{y+8}" text-anchor="middle" font-size="60" fill="#8a7a66">⋮</text>'); y += 50
        fill = '#f2c55c' if kind == 1 else ('#d8d4e6' if kind == 2 else '#fbf3e0')
        o.append(f'<rect x="60" y="{y}" width="{W-120}" height="132" rx="16" fill="{fill}"/><text x="110" y="{y+92}" font-size="70" fill="#4a2a18">{n}</text><text x="{W*0.36:.0f}" y="{y+92}" font-size="66" fill="#4a2a18">{name}</text>')
        y += 152
    for x, yy in ((60, 60), (W - 60, 60), (60, H - 50), (W - 60, H - 50)): o.append(f'<circle cx="{x}" cy="{yy}" r="12" fill="#a08a5a"/>')
    # pinned notices
    o.append(f'<g transform="translate({W-210},{H-200}) rotate(6)"><rect width="150" height="120" fill="#fffaf0"/><path d="M20,35h110M20,60h90M20,85h100" stroke="#9a8a7a" stroke-width="6"/><circle cx="75" cy="10" r="9" fill="#c03a2a"/></g>')
    return svg(W, H, ''.join(o), font=True)

def shield(W=600, H=700):
    b = (f'<path d="M300,20 L570,90 Q560,470 300,680 Q40,470 30,90Z" fill="#c8362a" stroke="#3a1a10" stroke-width="22"/>'
         f'<path d="M300,70 L520,125 Q510,440 300,620 Q90,440 80,125Z" fill="none" stroke="#f2c55c" stroke-width="12"/>'
         f'<path d="M300,180 L330,300 L450,300 L350,370 L390,490 L300,415 L210,490 L250,370 L150,300 L270,300Z" fill="#f2c55c" stroke="#3a1a10" stroke-width="8"/>')
    return svg(W, H, b)

def banner(W=400, H=1100):
    b = (f'<path d="M0,0H{W}V{H-160}L{W/2},{H}L0,{H-160}Z" fill="#c8362a"/><path d="M0,0H{W}V60H0Z" fill="#8e2218"/>'
         f'<path d="M28,70V{H-200}" stroke="#f2c55c" stroke-width="10"/><path d="M{W-28},70V{H-200}" stroke="#f2c55c" stroke-width="10"/>'
         f'<circle cx="{W/2}" cy="420" r="120" fill="#f2c55c"/><path d="M{W/2},330 l25,70 75,0 -60,45 22,72 -62,-44 -62,44 22,-72 -60,-45 75,0z" fill="#c8362a"/>')
    return svg(W, H, b)

def sky(W=4096, H=1600):
    r = rnd(9)
    o = ['<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f3a78"/><stop offset=".35" stop-color="#8a5a96"/>'
         '<stop offset=".62" stop-color="#e98a6a"/><stop offset=".82" stop-color="#ffc07a"/><stop offset="1" stop-color="#ffd9a0"/></linearGradient>'
         '<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff4d0"/><stop offset=".3" stop-color="#ffd890" stop-opacity=".8"/><stop offset="1" stop-color="#ff9a60" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#g)"/>', f'<circle cx="{W*0.12:.0f}" cy="{H*0.78:.0f}" r="420" fill="url(#sun)"/>']
    for _ in range(26):   # clouds lit from below-left
        x, y = r.uniform(0, W), r.uniform(H * 0.12, H * 0.6); s = r.uniform(0.6, 1.6)
        o.append(f'<g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})" opacity=".9">' + ''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="{rx}" ry="{ry}" fill="#f3b48e"/>' for dx, dy, rx, ry in ((0, 0, 120, 40), (90, -18, 90, 46), (-80, 8, 80, 30), (30, -40, 70, 40)))
                 + '<ellipse cx="10" cy="22" rx="190" ry="16" fill="#a86a8a" opacity=".55"/></g>')
    # far mountains, two layers
    for layer, (base, col, amp) in enumerate(((H * 0.80, '#8a6a9c', 220), (H * 0.88, '#6a5a8a', 160))):
        pts = [f'0,{H}']; x = 0
        while x <= W: pts.append(f'{x:.0f},{base - abs(math.sin(x * 0.0021 + layer)) * amp - r.uniform(0, 60):.0f}'); x += 70
        pts.append(f'{W},{H}'); o.append(f'<polygon points="{" ".join(pts)}" fill="{col}"/>')
    # distant town roofs silhouette
    x = 0
    while x < W:
        w = r.uniform(90, 200); h = r.uniform(60, 160); y = H - h
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#5a4a72"/><path d="M{x-10:.0f},{y:.0f}L{x+w/2:.0f},{y-h*0.5:.0f}L{x+w+10:.0f},{y:.0f}Z" fill="#4e3f66"/>')
        if r.random() < 0.5: o.append(f'<rect x="{x+w*0.3:.0f}" y="{y+h*0.35:.0f}" width="14" height="18" fill="#ffd88a" opacity=".9"/>')
        if r.random() < 0.15: o.append(f'<rect x="{x+w*0.4:.0f}" y="{y-h*0.9:.0f}" width="{w*0.25:.0f}" height="{h*0.9:.0f}" fill="#4e3f66"/><path d="M{x+w*0.37:.0f},{y-h*0.9:.0f}l{w*0.155:.0f},{-h*0.6:.0f}l{w*0.155:.0f},{h*0.6:.0f}z" fill="#3e3156"/>')
        x += w + r.uniform(-20, 30)
    return svg(W, H, ''.join(o))

def window_pane(W=256, H=320, lit=True):
    c = '#ffd27a' if lit else '#3a4a6a'
    b = (f'<rect width="{W}" height="{H}" fill="{c}"/>' + (f'<rect x="20" y="20" width="{W-40}" height="{H*0.5:.0f}" fill="#fff0c0" opacity=".6"/>' if lit else '<path d="M20,40l60,-20v120l-60,20z" fill="#8aa0c8" opacity=".4"/>')
         + f'<path d="M{W/2},0V{H}M0,{H/2}H{W}" stroke="#3a2414" stroke-width="16"/>')
    return svg(W, H, b)

def awning(W=1024, H=512):
    o = []
    for i in range(8): o.append(f'<rect x="{i*W/8:.0f}" y="0" width="{W/8:.0f}" height="{H}" fill="{"#d84a3a" if i%2==0 else "#f4ead6"}"/>')
    for i in range(8): o.append(f'<path d="M{i*W/8:.0f},{H-60}q{W/16:.0f},60 {W/8:.0f},0" fill="{"#d84a3a" if i%2==0 else "#f4ead6"}"/>')
    return svg(W, H, ''.join(o))

def stone(seed=7, W=512):
    r = rnd(seed); o = [f'<rect width="{W}" height="{W}" fill="#9a9086"/>']; rows = 6; h = W / rows
    for j in range(rows):
        x = -(j % 2) * 40
        while x < W:
            w = r.uniform(70, 120); o.append(f'<rect x="{x+3:.0f}" y="{j*h+3:.0f}" width="{w-6:.0f}" height="{h-6:.0f}" rx="8" fill="{r.choice(["#b0a698","#a69c8e","#bab0a2","#9e9486"])}"/>'); x += w
    return svg(W, W, ''.join(o))

def water(W=512):
    o = [f'<rect width="{W}" height="{W}" fill="#4f8fb8"/>']; r = rnd(2)
    for _ in range(40): x, y = r.uniform(0, W), r.uniform(0, W); o.append(f'<path d="M{x:.0f},{y:.0f}q20,-8 40,0" stroke="#bfe6ff" stroke-width="4" fill="none" opacity=".7"/>')
    return svg(W, W, ''.join(o))

JOBS = dict(
    cobbles=(cobbles, 1024, 1024, False), guild=(facade_guild, 1800, 2100, True),
    house_a=(lambda: facade_house('#f2d7b0', 21), 1200, 1200, False), house_b=(lambda: facade_house('#e8c9a8', 22), 1200, 1200, False),
    house_c=(lambda: facade_house('#f4e6cc', 23), 1200, 1200, False), house_d=(lambda: facade_house('#dcb79a', 24), 1200, 1200, False),
    roof_r=(lambda: roof(1), 1024, 1024, False), roof_o=(lambda: roof(2, '#c8683a', '#a65230'), 1024, 1024, False), roof_b=(lambda: roof(3, '#6a6a8a', '#565676'), 1024, 1024, False),
    door=(lambda: planks(4), 512, 1024, False), planks=(lambda: planks(5, '#8a5a34', 1024, 512, 10), 1024, 512, False),
    sign=(lambda: sign('กิลด์ผู้กล้า'), 1600, 320, False), board=(board, 1520, 1080, False), shield=(shield, 600, 700, True),
    banner=(banner, 400, 1100, True), sky=(sky, 4096, 1600, False), pane_lit=(window_pane, 256, 320, False), pane_dark=(lambda: window_pane(lit=False), 256, 320, False),
    awning=(awning, 1024, 512, False), stone=(stone, 512, 512, False), water=(water, 512, 512, False),
)

def build_all(force=False):
    os.makedirs(TEX, exist_ok=True); jobs = []; paths = {}
    for name, (fn, w, h, tr) in JOBS.items():
        s = fn(); hsh = hashlib.sha1(s.encode()).hexdigest()[:10]; png = os.path.join(TEX, f'{name}_{hsh}.png'); paths[name] = png
        if force or not os.path.exists(png):
            sp = png[:-4] + '.svg'; open(sp, 'w').write(s); jobs.append(dict(src=sp, out=png, w=w, h=h, transparent=tr))
    if jobs:
        jp = os.path.join(TEX, 'jobs.json'); json.dump(jobs, open(jp, 'w'))
        subprocess.run(['node', RASTER, jp], check=True, capture_output=True)
        for j in jobs: os.remove(j['src'])
    return paths

if __name__ == '__main__':
    p = build_all(); print(json.dumps(p, indent=0))
