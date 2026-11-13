"""SVG artwork for the Thonburi rooftop set (roof3d.py), rasterised by Chromium (one launch for all jobs). Cached by content hash in roof_tex/.
Every generator returns an SVG string; city facades come in pairs (colour, glow mask) so lit windows can emit."""
import os, json, hashlib, base64, subprocess, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'roof_tex')
RASTER = os.path.join(os.path.dirname(HERE), 'v3', 'set3d', 'raster.js')
FDIR = '/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/mw/hf/rig/assets/fonts'
_F2 = base64.b64encode(open(os.path.join(FDIR, 'f2.ttf'), 'rb').read()).decode()
_F3 = base64.b64encode(open(os.path.join(FDIR, 'f3.ttf'), 'rb').read()).decode()
FONT = (f"<style>@font-face{{font-family:KB;src:url(data:font/ttf;base64,{_F2})}}@font-face{{font-family:KK;src:url(data:font/ttf;base64,{_F3})}}"
        "text{font-family:KK}.b{font-family:KB}</style>")

def svg(w, h, body, font=False, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block">'
            f'{FONT if font else ""}<defs>{defs}</defs>{body}</svg>')

R = random.Random
def grain(fid, freq, color, k, off, octv=3, seed=1, op=1.0):
    """Filter: fractal noise -> one colour whose alpha = k * (noise - off). Use with <rect filter=...>."""
    c = color.lstrip('#'); r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (f'<filter id="{fid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB"><feTurbulence type="fractalNoise" baseFrequency="{freq}" '
            f'numOctaves="{octv}" seed="{seed}" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 {r:.3f} 0 0 0 0 {g:.3f} 0 0 0 0 {b:.3f} {k} 0 0 0 {-k*off:.3f}"/>'
            f'<feComponentTransfer><feFuncA type="linear" slope="{op}"/></feComponentTransfer></filter>')

def noise_layers(W, H, specs, seed0=1):
    """specs: list of (freq, colour, k, off, octaves). Returns (defs, body)."""
    d = ''; b = ''
    for i, (fr, col, k, off, oc) in enumerate(specs):
        fid = f'n{seed0}_{i}'; d += grain(fid, fr, col, k, off, oc, seed0 + i * 7)
        b += f'<rect width="{W}" height="{H}" filter="url(#{fid})"/>'
    return d, b

def walk(r, x, y, n, step, ang, jit):
    pts = [(x, y)]
    for _ in range(n):
        ang += r.uniform(-jit, jit); x += math.cos(ang) * step * r.uniform(0.5, 1.3); y += math.sin(ang) * step * r.uniform(0.5, 1.3); pts.append((x, y))
    return 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts)

def blob(r, cx, cy, rx, ry, n=9):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n; k = r.uniform(0.7, 1.15); pts.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    d = f'M{(pts[0][0]+pts[-1][0])/2:.0f},{(pts[0][1]+pts[-1][1])/2:.0f}'
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]; d += f' Q{p[0]:.0f},{p[1]:.0f} {(p[0]+q[0])/2:.0f},{(p[1]+q[1])/2:.0f}'
    return d + 'Z'

# ----------------------------------------------------------------------------- roof slab: wet stained concrete, 2048 px = 9 m
def roof_floor(W=2048, seed=5):
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="#86837e"/>']
    d, b = noise_layers(W, W, [(0.0025, '#4c4b4e', 2.2, 0.42, 4), (0.004, '#a9a59e', 2.0, 0.55, 3), (0.06, '#3e3c3c', 1.6, 0.5, 2), (0.11, '#b5b0a8', 1.4, 0.58, 2)], seed)
    o.append(b)
    for k in range(22):   # repair patches / slab tones
        x, y, w, h = r.uniform(0, W), r.uniform(0, W), r.uniform(80, 360), r.uniform(60, 280)
        for dx in (-W, 0, W):
            for dy in (-W, 0, W):
                if k % 3 == 0: o.append(f'<rect x="{x+dx:.0f}" y="{y+dy:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#9a968e" opacity=".35" stroke="#55524f" stroke-width="3" stroke-opacity=".5" transform="rotate({r.uniform(-4,4):.1f} {x+dx:.0f} {y+dy:.0f})"/>')
                else: o.append(f'<path d="{blob(r, x+dx, y+dy, w*.7, h*.5)}" fill="{r.choice(["#5d5a58","#6b6762","#9b978f","#605048"])}" opacity="{r.uniform(.12,.28):.2f}"/>')
    J = W / 3   # expansion joints every 3 m
    for i in range(4):
        o.append(f'<path d="M{i*J:.0f},0V{W}M0,{i*J:.0f}H{W}" stroke="#2c2a2b" stroke-width="10"/><path d="M{i*J+6:.0f},0V{W}M0,{i*J+6:.0f}H{W}" stroke="#a8a49c" stroke-width="2" opacity=".5"/>')
    for _ in range(26):   # cracks
        x, y = r.uniform(0, W), r.uniform(0, W); p = walk(r, x, y, r.randint(6, 16), 30, r.uniform(0, 6.3), 0.8)
        o.append(f'<path d="{p}" stroke="#2a2828" stroke-width="{r.uniform(1.5,3.5):.1f}" fill="none" opacity=".75"/>')
    for _ in range(30):   # rust stains, dirt
        x, y = r.uniform(0, W), r.uniform(0, W); o.append(f'<path d="{blob(r, x, y, r.uniform(15,70), r.uniform(10,50))}" fill="{r.choice(["#7a4c2c","#5c4a34","#3f4a30"])}" opacity="{r.uniform(.2,.45):.2f}"/>')
    # puddles: irregular dark wet patches (several merged blobs), dim sky reflections, a wet halo
    for k in range(7):
        x, y = r.uniform(0, W), r.uniform(0, W); rr = R(seed * 100 + k); sz = r.uniform(0.6, 1.5)
        parts = [(rr.uniform(-120, 120) * sz, rr.uniform(-80, 80) * sz, rr.uniform(70, 170) * sz, rr.uniform(40, 110) * sz, rr.randint(0, 999)) for _ in range(rr.randint(3, 5))]
        for dx in (-W, 0, W):
            for dy in (-W, 0, W):
                cx, cy = x + dx, y + dy
                if cx < -500 or cx > W + 500 or cy < -500 or cy > W + 500: continue
                for (px, py, rx, ry, sd) in parts: o.append(f'<path d="{blob(R(sd), cx+px, cy+py, rx*1.25+20, ry*1.3+16, 12)}" fill="#5a5754" opacity=".5"/>')
                for (px, py, rx, ry, sd) in parts: o.append(f'<path d="{blob(R(sd+1), cx+px, cy+py, rx, ry, 12)}" fill="#3e3f48"/>')
                for (px, py, rx, ry, sd) in parts[:2]: o.append(f'<path d="{blob(R(sd+2), cx+px-rx*.15, cy+py-ry*.2, rx*.55, ry*.35, 9)}" fill="#55586e" opacity=".7"/>')
                for j in range(5):
                    (px, py, rx, ry, sd) = parts[j % len(parts)]; sx = cx + px + rr.uniform(-rx * .5, rx * .5); sy = cy + py + rr.uniform(-ry * .4, ry * .4)
                    o.append(f'<path d="M{sx-rx*.3:.0f},{sy:.0f}h{rx*.6:.0f}" stroke="#7a7e9a" stroke-width="{rr.uniform(2,5):.0f}" stroke-linecap="round" opacity=".5"/>')
                    o.append(f'<ellipse cx="{sx+rr.uniform(-30,30):.0f}" cy="{sy+rr.uniform(-20,20):.0f}" rx="{rr.uniform(8,20):.0f}" ry="{rr.uniform(3,7):.0f}" fill="none" stroke="#9a9eb8" stroke-width="2" opacity=".45"/>')
    for _ in range(140):   # litter, leaves, pebbles
        x, y = r.uniform(0, W), r.uniform(0, W); c = r.choice(['#6a5a2e', '#8a6a3a', '#3a3634', '#c8c2b8', '#2e2c2a'])
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3,12):.0f}" ry="{r.uniform(2,6):.0f}" fill="{c}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})" opacity=".85"/>')
    return svg(W, W, ''.join(o), defs=d)

# ----------------------------------------------------------------------------- concrete wall (parapet, plinths), 1024 x 512 = 4 m x 2 m
def concrete_wall(W=1024, H=512, seed=8, base='#9a958c', paint=None):
    r = R(seed); o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']
    d, b = noise_layers(W, H, [(0.006, '#5a5652', 2.0, 0.5, 4), (0.08, '#3e3c3a', 1.4, 0.55, 2), (0.012, '#bdb8ae', 1.8, 0.58, 3)], seed)
    o.append(b)
    for y in (H * 0.33, H * 0.66): o.append(f'<path d="M0,{y:.0f}H{W}" stroke="#6a665f" stroke-width="3" opacity=".5"/>')
    for x in range(0, W, 256): o.append(f'<path d="M{x},0V{H}" stroke="#6a665f" stroke-width="3" opacity=".4"/>')
    for _ in range(46):   # water streaks from the top
        x = r.uniform(0, W); l = r.uniform(60, H); w = r.uniform(3, 18)
        o.append(f'<path d="M{x:.0f},0 q{r.uniform(-8,8):.0f},{l/2:.0f} {r.uniform(-6,6):.0f},{l:.0f}" stroke="#3c3a40" stroke-width="{w:.0f}" opacity="{r.uniform(.12,.35):.2f}" fill="none" stroke-linecap="round"/>')
    o.append(f'<rect width="{W}" height="26" fill="#2e2c32" opacity=".45"/>')
    for _ in range(14):   # black mould at the foot
        x = r.uniform(0, W); o.append(f'<path d="{blob(r, x, H, r.uniform(30,110), r.uniform(20,60))}" fill="#2a2e26" opacity="{r.uniform(.35,.6):.2f}"/>')
    for _ in range(8):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<path d="{walk(r, x, y, 8, 18, 1.5, 0.9)}" stroke="#2a2828" stroke-width="2" fill="none" opacity=".7"/>')
    for _ in range(5):   # spalled patches with rebar rust
        x, y = r.uniform(0, W), r.uniform(60, H - 60); o.append(f'<path d="{blob(r, x, y, 30, 18)}" fill="#6e6a62"/><path d="M{x-20:.0f},{y:.0f}h40" stroke="#8a4a24" stroke-width="5"/><path d="M{x:.0f},{y:.0f}v{r.uniform(40,120):.0f}" stroke="#8a4a24" stroke-width="7" opacity=".35"/>')
    return svg(W, H, ''.join(o), defs=d)

# ----------------------------------------------------------------------------- painted steel with rust, 512 = 1 m (beams)
def steel(W=512, seed=11, base='#7c808a', rust=True):
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="{base}"/>']
    d, b = noise_layers(W, W, [(0.01, '#4c4e58', 1.8, 0.5, 3), (0.12, '#a6aab2', 1.2, 0.6, 2)], seed)
    o.append(b)
    if rust:
        for _ in range(16):
            x, y = r.uniform(0, W), r.uniform(0, W); o.append(f'<path d="{blob(r, x, y, r.uniform(6,30), r.uniform(4,20))}" fill="{r.choice(["#8a4422","#a85a2a","#6a3218"])}" opacity="{r.uniform(.6,.95):.2f}"/>')
            o.append(f'<path d="M{x:.0f},{y:.0f}v{r.uniform(30,140):.0f}" stroke="#7a3e1e" stroke-width="{r.uniform(3,9):.0f}" opacity=".35" stroke-linecap="round"/>')
    for _ in range(10): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},0V{W}" stroke="#5a5c66" stroke-width="2" opacity=".4"/>')
    return svg(W, W, ''.join(o), defs=d)

def grating(W=512):
    """Catwalk floor grating, 1 m tile, alpha holes (transparent=True)."""
    n = 20; c = W / n; o = []
    for i in range(n + 1):
        o.append(f'<rect x="{i*c-3:.1f}" y="0" width="7" height="{W}" fill="#8a8e96"/><rect x="{i*c-3:.1f}" y="0" width="2" height="{W}" fill="#b8bcc4"/>')
        if i % 2 == 0: o.append(f'<rect x="0" y="{i*c-2:.1f}" width="{W}" height="5" fill="#6e727a"/>')
    r = R(3)
    for _ in range(25): x, y = r.uniform(0, W), r.uniform(0, W); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(4,12):.0f}" fill="#8a4422" opacity=".7"/>')
    return svg(W, W, ''.join(o))

def tread_plate(W=512):
    o = [f'<rect width="{W}" height="{W}" fill="#868a92"/>']
    for j in range(16):
        for i in range(16):
            x, y = i * 32 + (j % 2) * 16, j * 32; a = 45 if (i + j) % 2 else -45
            o.append(f'<rect x="{x+6}" y="{y+13}" width="20" height="5" rx="2" fill="#a8acb4" transform="rotate({a} {x+16} {y+16})"/>')
    d, b = noise_layers(W, W, [(0.02, '#4a4c54', 1.8, 0.5, 3), (0.03, '#8a4422', 2.2, 0.62, 3)], 21)
    return svg(W, W, ''.join(o) + b, defs=d)

# ----------------------------------------------------------------------------- the billboard face, 2400 x 1200 (12 x 6 m)
def billboard(W=2400, H=1200):
    r = R(42)
    defs = ('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd23a"/><stop offset="1" stop-color="#ff9a1e"/></linearGradient>'
            '<radialGradient id="sb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2a0"/><stop offset="1" stop-color="#ffd23a" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="grime" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#3a2a20" stop-opacity="0"/><stop offset="1" stop-color="#3a2a20" stop-opacity=".45"/></linearGradient>')
    o = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    cx, cy = 1500, 560
    for i in range(24):   # sunburst rays
        a0 = 2 * math.pi * i / 24; a1 = a0 + math.pi / 24
        o.append(f'<path d="M{cx},{cy} L{cx+2600*math.cos(a0):.0f},{cy+2600*math.sin(a0):.0f} L{cx+2600*math.cos(a1):.0f},{cy+2600*math.sin(a1):.0f}Z" fill="#ffe680" opacity=".35"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="700" fill="url(#sb)"/>')
    # cartoon ornate iron gate (left)
    gx, gy, gw, gh = 70, 300, 760, 820
    o.append(f'<rect x="{gx-30}" y="{gy-40}" width="{gw+60}" height="{gh+60}" rx="20" fill="#2a3a6a"/><rect x="{gx-14}" y="{gy-24}" width="{gw+28}" height="{gh+28}" rx="12" fill="#bfe0ff"/>')
    G = []
    for i in range(9):
        x = gx + 40 + i * (gw - 80) / 8; G.append(f'<path d="M{x:.0f},{gy+60}V{gy+gh-20}" stroke="#1a1a22" stroke-width="18"/><path d="M{x:.0f},{gy+60}l-16,-40h32z" fill="#1a1a22"/>')
    for y in (gy + 60, gy + 330, gy + gh - 20): G.append(f'<path d="M{gx+20},{y}H{gx+gw-20}" stroke="#1a1a22" stroke-width="22"/>')
    for i in range(4):   # scrolls
        x = gx + 110 + i * 180; y = gy + 470
        G.append(f'<path d="M{x},{y} c60,-90 160,-40 120,30 c-30,50 -100,20 -70,-20 M{x},{y+200} c60,90 160,40 120,-30 c-30,-50 -100,-20 -70,20" stroke="#1a1a22" stroke-width="14" fill="none"/>')
        G.append(f'<circle cx="{x+90}" cy="{y+100}" r="28" fill="none" stroke="#e8b830" stroke-width="12"/>')
    G.append(f'<path d="M{gx+20},{gy+60} Q{gx+gw/2},{gy-120} {gx+gw-20},{gy+60}" stroke="#1a1a22" stroke-width="20" fill="none"/>')
    for i in range(7): x = gx + 80 + i * (gw - 160) / 6; G.append(f'<path d="M{x:.0f},{gy+60}V{gy+60-110*math.sin(math.pi*(i+0.5)/7.4):.0f}" stroke="#1a1a22" stroke-width="10"/>')
    o += G
    # lightning bolts bouncing off the gate (the joke: storm-proof)
    for (bx, by, s) in ((560, 110, 1.0), (880, 260, -0.8)):
        o.append(f'<path d="M{bx},{by} l{-60*s:.0f},120 l{50*s:.0f},0 l{-70*s:.0f},150 l{150*s:.0f},-190 l{-55*s:.0f},0 l{55*s:.0f},-80z" fill="#fff" stroke="#1a1a22" stroke-width="10"/>')
    o.append('<text x="700" y="250" font-size="70" fill="#1a1a22" transform="rotate(-12 700 250)">เปรี้ยง!</text>')
    # headline
    o.append(f'<text x="1530" y="300" text-anchor="middle" font-size="205" fill="#d4201c" stroke="#1a1a22" stroke-width="30" paint-order="stroke" stroke-linejoin="round">เหล็กดัดเจ๊หงส์</text>')
    o.append(f'<text x="1530" y="300" text-anchor="middle" font-size="205" fill="none" stroke="#fff" stroke-width="8" opacity=".85">เหล็กดัดเจ๊หงส์</text>')
    o.append(f'<path d="M930,370 L2190,370 L2150,450 L2190,530 L930,530 L970,450Z" fill="#1d4fb8" stroke="#1a1a22" stroke-width="12"/>')
    o.append(f'<text x="1560" y="500" text-anchor="middle" font-size="140" fill="#fff" stroke="#1a1a22" stroke-width="10" paint-order="stroke">ทนทุกพายุ!</text>')
    # auntie Hong (cartoon) with thumbs up, bottom right
    ax, ay = 2050, 900
    o.append(f'<circle cx="{ax}" cy="{ay}" r="230" fill="#fff" stroke="#1a1a22" stroke-width="12"/>')
    o.append(f'<path d="M{ax-170},{ay+230} Q{ax},{ay+60} {ax+170},{ay+230}Z" fill="#d42a5a" stroke="#1a1a22" stroke-width="10"/>')
    o.append(f'<ellipse cx="{ax}" cy="{ay-20}" rx="105" ry="120" fill="#ffd2a8" stroke="#1a1a22" stroke-width="10"/>')
    for k in range(9): a = math.pi * (1.05 + k / 8 * 0.9); o.append(f'<circle cx="{ax+110*math.cos(a):.0f}" cy="{ay-40+120*math.sin(a):.0f}" r="48" fill="#2a1a14"/>')
    o.append(f'<circle cx="{ax-40}" cy="{ay-30}" r="14" fill="#1a1a22"/><circle cx="{ax+40}" cy="{ay-30}" r="14" fill="#1a1a22"/><path d="M{ax-50},{ay+40} Q{ax},{ay+95} {ax+50},{ay+40}Z" fill="#c8102e" stroke="#1a1a22" stroke-width="6"/>')
    o.append(f'<circle cx="{ax-75}" cy="{ay+15}" r="18" fill="#ff7a8a" opacity=".7"/><circle cx="{ax+75}" cy="{ay+15}" r="18" fill="#ff7a8a" opacity=".7"/>')
    o.append(f'<path d="M{ax+150},{ay+40} h70 v-60 q0,-40 30,-40 q20,0 20,40 v40 h40 q30,0 30,30 v80 q0,30 -30,30 h-160z" fill="#ffd2a8" stroke="#1a1a22" stroke-width="10"/>')
    # speech bubble
    o.append(f'<path d="M1180,640 h620 q40,0 40,40 v150 q0,40 -40,40 h-380 l-60,80 l-10,-80 h-170 q-40,0 -40,-40 v-150 q0,-40 40,-40z" fill="#fff" stroke="#1a1a22" stroke-width="12"/>')
    o.append('<text x="1490" y="790" text-anchor="middle" font-size="96" fill="#1a1a22">ฟ้าผ่าก็ไม่หวั่น!</text>')
    # phone strip + badge
    o.append(f'<rect x="0" y="1060" width="{W}" height="140" fill="#1a1a22"/><text x="1200" y="1160" text-anchor="middle" font-size="96" fill="#ffd23a" class="b">โทร. 02-888-8888 · ส่งฟรีทั่วฝั่งธนฯ</text>')
    o.append(f'<g transform="translate(1000,880) rotate(-14)"><path d="' + ''.join(f'{"M" if k==0 else "L"}{(120 if k%2==0 else 95)*math.cos(math.pi*k/12):.0f},{(120 if k%2==0 else 95)*math.sin(math.pi*k/12):.0f}' for k in range(24)) + 'Z" fill="#d4201c" stroke="#1a1a22" stroke-width="8"/>'
             '<text x="0" y="-5" text-anchor="middle" font-size="56" fill="#fff">ลด</text><text x="0" y="55" text-anchor="middle" font-size="56" fill="#fff">50%</text></g>')
    # weathering: vinyl seams, rust drips from bolts, a torn peeling corner, grime
    for x in range(400, W, 400): o.append(f'<path d="M{x},0V{H}" stroke="#7a5a2a" stroke-width="4" opacity=".45"/>')
    for i in range(14):
        x = r.uniform(30, W - 30); l = r.uniform(80, 420)
        o.append(f'<circle cx="{x:.0f}" cy="22" r="9" fill="#5a3a20"/><path d="M{x:.0f},28 q{r.uniform(-6,6):.0f},{l/2:.0f} {r.uniform(-5,5):.0f},{l:.0f}" stroke="#6a3a1a" stroke-width="{r.uniform(5,14):.0f}" opacity=".5" fill="none" stroke-linecap="round"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#grime)"/>')
    o.append(f'<path d="M{W},{H-140} L{W},{H-400} Q{W-90},{H-330} {W-170},{H-250} L{W-230},{H-140}Z" fill="#7d8088"/><path d="M{W-230},{H-140} L{W-170},{H-250} Q{W-120},{H-180} {W-60},{H-200} Q{W-150},{H-150} {W-230},{H-140}Z" fill="#e8d8a0" stroke="#5a4a30" stroke-width="5"/>')
    for k in range(5):
        y = r.uniform(H-380, H-160); o.append(f'<path d="M{W-200+k*35},{y:.0f}l18,6" stroke="#5a5c66" stroke-width="5"/>')
    o.append(f'<path d="M0,{H} L0,{H-260} Q90,{H-230} 150,{H-130} L210,{H}Z" fill="#787b84"/>')
    d, b = noise_layers(W, H, [(0.004, '#4a3a2a', 1.6, 0.6, 3)], 77)
    return svg(W, H, ''.join(o) + b, font=True, defs=defs + d)

def billboard_pool(W=1200, H=600, lamps=(), broken=()):
    """Light pools thrown up the face by the working lamps (glow mask, white on black)."""
    o = [f'<rect width="{W}" height="{H}" fill="#000"/>',
         '<defs><radialGradient id="p" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>']
    for u in lamps: o.append(f'<ellipse cx="{u*W:.0f}" cy="{H}" rx="{W*0.16:.0f}" ry="{H*0.95:.0f}" fill="url(#p)"/>')
    return svg(W, H, ''.join(o))

def panel_back(W=1024, H=512):
    o = [f'<rect width="{W}" height="{H}" fill="#6e727c"/>']; r = R(9)
    for x in range(0, W, 128): o.append(f'<path d="M{x},0V{H}" stroke="#4a4c56" stroke-width="6"/><path d="M{x+6},0V{H}" stroke="#9a9ea8" stroke-width="2"/>')
    for y in range(0, H, 128):
        for x in range(0, W, 64): o.append(f'<circle cx="{x+10}" cy="{y+10}" r="5" fill="#3a3c44"/>')
    d, b = noise_layers(W, H, [(0.01, '#3a3c46', 1.8, 0.5, 3), (0.02, '#8a4422', 2.4, 0.6, 3)], 12)
    for _ in range(18): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},0v{r.uniform(80,H):.0f}" stroke="#6a3418" stroke-width="{r.uniform(4,12):.0f}" opacity=".45" stroke-linecap="round"/>')
    return svg(W, H, ''.join(o) + b, defs=d)

# ----------------------------------------------------------------------------- stair hut, door, signs
def hut_wall(W=1024, H=768, seed=13):
    """Painted plaster, 4 m x 3 m: faded cream, peeling to brick, mould, a graffiti tag."""
    r = R(seed); o = [f'<rect width="{W}" height="{H}" fill="#c9b994"/>']
    d, b = noise_layers(W, H, [(0.006, '#7a6a4a', 2.0, 0.5, 4), (0.09, '#5a5040', 1.3, 0.55, 2)], seed)
    o.append(b)
    for _ in range(7):
        x, y = r.uniform(0, W), r.uniform(80, H - 80); w, h = r.uniform(60, 180), r.uniform(40, 120)
        o.append(f'<path d="{blob(r, x, y, w, h)}" fill="#a85a3a"/>')
        for j in range(int(h / 22)):
            yy = y - h * 0.8 + j * 26; o.append(f'<path d="M{x-w:.0f},{yy:.0f}H{x+w:.0f}" stroke="#d8d0c0" stroke-width="5" opacity=".7"/>')
        o.append(f'<path d="{blob(r, x, y, w*1.05, h*1.05)}" fill="none" stroke="#efe6cc" stroke-width="6"/>')
    for _ in range(40):
        x = r.uniform(0, W); l = r.uniform(80, H * 0.9); o.append(f'<path d="M{x:.0f},0 q{r.uniform(-6,6):.0f},{l/2:.0f} 0,{l:.0f}" stroke="#4a4a40" stroke-width="{r.uniform(4,16):.0f}" opacity="{r.uniform(.1,.3):.2f}" stroke-linecap="round" fill="none"/>')
    o.append(f'<rect y="{H-70}" width="{W}" height="70" fill="#3a3a30" opacity=".45"/>')
    o.append(f'<text x="{W*0.62:.0f}" y="{H*0.72:.0f}" font-size="110" fill="none" stroke="#2a6ad8" stroke-width="9" transform="rotate(-8 {W*0.6:.0f} {H*0.7:.0f})" opacity=".85">TBR</text>')
    o.append(f'<text x="{W*0.08:.0f}" y="{H*0.35:.0f}" font-size="44" fill="#c82a2a" opacity=".8" class="b">ห้ามทิ้งขยะ</text>')
    return svg(W, H, ''.join(o), font=True, defs=d)

def door(W=512, H=1024):
    r = R(17); o = [f'<rect width="{W}" height="{H}" fill="#3e6a5a"/>']
    d, b = noise_layers(W, H, [(0.01, '#203a30', 2.0, 0.5, 3), (0.025, '#8a4a24', 2.4, 0.6, 3)], 17)
    o.append(b)
    o.append(f'<rect x="30" y="30" width="{W-60}" height="{H-60}" fill="none" stroke="#2a4a3e" stroke-width="12"/><rect x="60" y="80" width="{W-120}" height="380" fill="none" stroke="#5a8a78" stroke-width="6" opacity=".6"/>')
    for i in range(10): o.append(f'<rect x="80" y="{H-300+i*24}" width="{W-160}" height="12" fill="#1e2e28"/>')
    o.append(f'<rect x="96" y="160" width="{W-192}" height="200" rx="10" fill="#f2d21e" stroke="#1a1a1a" stroke-width="8"/><text x="{W/2}" y="245" text-anchor="middle" font-size="64" fill="#1a1a1a">ทางขึ้น</text><text x="{W/2}" y="325" text-anchor="middle" font-size="64" fill="#1a1a1a">ดาดฟ้า</text>')
    for _ in range(9): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},{r.uniform(0,H):.0f}v{r.uniform(40,200):.0f}" stroke="#7a3a18" stroke-width="{r.uniform(4,10):.0f}" opacity=".5" stroke-linecap="round"/>')
    o.append(f'<rect y="{H-50}" width="{W}" height="50" fill="#5a3418" opacity=".7"/>')
    return svg(W, H, ''.join(o), font=True, defs=d)

def sign(lines, W=512, H=384, bg='#f2d21e', fg='#1a1a1a', icon=True):
    o = [f'<rect width="{W}" height="{H}" rx="18" fill="#1a1a1a"/><rect x="12" y="12" width="{W-24}" height="{H-24}" rx="12" fill="{bg}"/>']
    if icon: o.append(f'<path d="M{W/2},40 L{W/2+70},160 L{W/2-70},160Z" fill="{fg}"/><path d="M{W/2+8},70 l-24,48 h18 l-12,34 l30,-50 h-18z" fill="{bg}"/>')
    y0 = 230 if icon else H / 2 - (len(lines) - 1) * 40 + 30
    for i, t in enumerate(lines): o.append(f'<text x="{W/2}" y="{y0+i*80}" text-anchor="middle" font-size="64" fill="{fg}">{t}</text>')
    o.append(f'<path d="M{W*0.6:.0f},{H-12} q10,-60 0,-120" stroke="#7a3a18" stroke-width="10" opacity=".4" fill="none"/>')
    return svg(W, H, ''.join(o), font=True)

# ----------------------------------------------------------------------------- props
def tank(W=1024, H=512):
    """Stainless water tank wrap (circumference x height)."""
    o = [f'<rect width="{W}" height="{H}" fill="#b8bcc4"/>']; r = R(23)
    for x in range(0, W, 6): o.append(f'<path d="M{x},0V{H}" stroke="{r.choice(["#a6aab2","#c8ccd4","#9a9ea8"])}" stroke-width="3"/>')
    for y in (60, 190, 320, 450): o.append(f'<rect y="{y}" width="{W}" height="16" fill="#8a8e98"/><rect y="{y}" width="{W}" height="4" fill="#e0e4ec"/>')
    o.append(f'<rect x="380" y="210" width="260" height="96" rx="10" fill="#1d5fb8"/><text x="510" y="276" text-anchor="middle" font-size="48" fill="#fff">ทนดี 2000L</text>')
    d, b = noise_layers(W, H, [(0.01, '#5a5e48', 2.2, 0.55, 3)], 23)
    for _ in range(20): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},0v{r.uniform(60,H):.0f}" stroke="#5a5a4a" stroke-width="{r.uniform(3,10):.0f}" opacity=".3" stroke-linecap="round"/>')
    return svg(W, H, ''.join(o) + b, font=True, defs=d)

def ac_front(W=512, H=384, brand='COOLMAX'):
    o = [f'<rect width="{W}" height="{H}" fill="#d8d6ce"/><rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#8a8a84" stroke-width="10"/>']
    cx, cy, rr = 200, 192, 150
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#2a2c30"/>')
    for k in range(3): a = k * 120; o.append(f'<path d="M{cx},{cy} q60,-110 120,-60 q-50,40 -120,60z" fill="#4a4e56" transform="rotate({a} {cx} {cy})"/>')
    for k in range(1, 7): o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr*k/6:.0f}" fill="none" stroke="#a8a8a2" stroke-width="5"/>')
    o.append(f'<path d="M{cx-rr},{cy}H{cx+rr}M{cx},{cy-rr}V{cy+rr}" stroke="#a8a8a2" stroke-width="5"/>')
    for i in range(14): o.append(f'<rect x="380" y="{40+i*22}" width="110" height="10" fill="#9a9a92"/>')
    o.append(f'<text x="435" y="{H-24}" text-anchor="middle" font-size="26" fill="#3a5aa8" class="b">{brand}</text>')
    d, b = noise_layers(W, H, [(0.012, '#5a5644', 2.2, 0.55, 3)], 31)
    return svg(W, H, ''.join(o) + b, font=True, defs=d)

def tarp(W=1024, seed=29):
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="#2a64b8"/>']
    for x in range(0, W, 8): o.append(f'<path d="M{x},0V{W}M0,{x}H{W}" stroke="#1e4e96" stroke-width="2" opacity=".6"/>')
    for _ in range(14):
        x0 = r.uniform(0, W); o.append(f'<path d="M{x0:.0f},0 Q{x0+r.uniform(-200,200):.0f},{W/2} {x0+r.uniform(-120,120):.0f},{W}" stroke="#1a3a78" stroke-width="{r.uniform(10,36):.0f}" opacity=".45" fill="none"/>'
                                 f'<path d="M{x0+14:.0f},0 Q{x0+r.uniform(-200,200):.0f},{W/2} {x0+r.uniform(-120,120):.0f},{W}" stroke="#5a8ad8" stroke-width="6" opacity=".35" fill="none"/>')
    for i in range(9):
        for (x, y) in ((i * W / 8, 20), (i * W / 8, W - 20), (20, i * W / 8), (W - 20, i * W / 8)): o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#d8d8d0" stroke="#5a5a5a" stroke-width="4"/>')
    o.append(f'<rect width="{W}" height="{W}" fill="none" stroke="#f0f0e8" stroke-width="26"/>')
    d, b = noise_layers(W, W, [(0.008, '#3a3a30', 2.0, 0.6, 3)], seed)
    return svg(W, W, ''.join(o) + b, defs=d)

def cylinder_label(base, band, text, sub, W=512, H=512):
    o = [f'<rect width="{W}" height="{H}" fill="{base}"/><rect width="{W}" height="90" fill="{band}"/>']
    o.append(f'<text x="{W/2}" y="300" text-anchor="middle" font-size="64" fill="#f4f0e8">{text}</text><text x="{W/2}" y="380" text-anchor="middle" font-size="40" fill="#f4f0e8" class="b">{sub}</text>')
    d, b = noise_layers(W, H, [(0.015, '#2a2620', 2.0, 0.55, 3), (0.03, '#8a5a30', 2.4, 0.64, 3)], 41)
    return svg(W, H, ''.join(o) + b, font=True, defs=d)

def machine(W=512, H=384):
    o = [f'<rect width="{W}" height="{H}" fill="#e8b81e"/><rect x="20" y="20" width="{W-40}" height="120" rx="8" fill="#2a2a2a"/><text x="{W/2}" y="100" text-anchor="middle" font-size="64" fill="#e8b81e" class="b">WELD 250A</text>']
    for i, x in enumerate((110, 256, 400)):
        o.append(f'<circle cx="{x}" cy="230" r="52" fill="#1a1a1a"/><circle cx="{x}" cy="230" r="38" fill="#d8d8d0"/><path d="M{x},230 l{24*math.cos(i+0.4):.0f},{-24*math.sin(i+0.4)-10:.0f}" stroke="#c81a1a" stroke-width="6"/>')
    o.append(f'<circle cx="120" cy="330" r="22" fill="#c81a1a"/><circle cx="200" cy="330" r="22" fill="#1a1a1a"/><rect x="300" y="310" width="160" height="40" fill="#3a3a3a"/>')
    d, b = noise_layers(W, H, [(0.015, '#4a3a1a', 2.0, 0.55, 3)], 43)
    return svg(W, H, ''.join(o) + b, font=True, defs=d)

def toolbox(W=512, H=256):
    o = [f'<rect width="{W}" height="{H}" fill="#c8241e"/><rect y="70" width="{W}" height="10" fill="#7a1410"/><rect x="200" y="90" width="112" height="44" rx="6" fill="#b8bcc4"/>']
    d, b = noise_layers(W, H, [(0.02, '#3a1a10', 2.0, 0.55, 3)], 47)
    return svg(W, H, ''.join(o) + b, defs=d)

def cloth(c1, c2, pattern, W=256, H=256):
    o = [f'<rect width="{W}" height="{H}" fill="{c1}"/>']
    if pattern == 'stripe':
        for i in range(0, W, 40): o.append(f'<rect x="{i}" width="18" height="{H}" fill="{c2}"/>')
    elif pattern == 'check':
        for i in range(0, W, 48):
            o.append(f'<rect x="{i}" width="20" height="{H}" fill="{c2}" opacity=".6"/><rect y="{i}" width="{W}" height="20" fill="{c2}" opacity=".6"/>')
    elif pattern == 'dots':
        for i in range(0, W, 40):
            for j in range(0, H, 40): o.append(f'<circle cx="{i+20}" cy="{j+20}" r="8" fill="{c2}"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="#000" opacity=".12"/>')
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- our building's facade (26 m x 24.5 m) and the city facades
def _win(o, g, r, x, y, w, h, lit, warm, grille=False, curtain=None):
    """One aluminium window. o = colour list, g = glow list."""
    o.append(f'<rect x="{x-4:.0f}" y="{y-4:.0f}" width="{w+8:.0f}" height="{h+8:.0f}" fill="#4a4c52"/>')
    if lit:
        c = '#ffc870' if warm else '#cfe0ff'; o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{c}"/>')
        g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{c}"/>')
        if curtain:
            cw = w * r.uniform(0.25, 0.5); o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{h:.0f}" fill="{curtain}"/>'); g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{h:.0f}" fill="#000" opacity=".6"/>')
        if r.random() < 0.3:   # silhouette of furniture / person
            px = x + w * r.uniform(0.3, 0.7); o.append(f'<rect x="{px-w*0.08:.0f}" y="{y+h*0.4:.0f}" width="{w*0.16:.0f}" height="{h*0.6:.0f}" rx="{w*0.06:.0f}" fill="#5a3a2a" opacity=".7"/>'); g.append(f'<rect x="{px-w*0.08:.0f}" y="{y+h*0.4:.0f}" width="{w*0.16:.0f}" height="{h*0.6:.0f}" fill="#000" opacity=".7"/>')
    else:
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#3a4462"/><path d="M{x:.0f},{y+h*0.7:.0f} L{x+w*0.4:.0f},{y:.0f} L{x+w*0.6:.0f},{y:.0f} L{x+w*0.1:.0f},{y+h:.0f} L{x:.0f},{y+h:.0f}Z" fill="#6a76a0" opacity=".45"/>')
    o.append(f'<path d="M{x+w/2:.0f},{y:.0f}V{y+h:.0f}" stroke="#4a4c52" stroke-width="4"/>')
    if grille:
        for k in range(1, 6): o.append(f'<path d="M{x+w*k/6:.0f},{y-4:.0f}V{y+h+4:.0f}" stroke="#1e1e22" stroke-width="3"/>')
        o.append(f'<path d="M{x:.0f},{y+h/2:.0f}H{x+w:.0f}" stroke="#1e1e22" stroke-width="3"/>')
        for k in range(3): cx = x + w * (k + 0.5) / 3; o.append(f'<circle cx="{cx:.0f}" cy="{y+h/2:.0f}" r="{min(w,h)*0.09:.0f}" fill="none" stroke="#1e1e22" stroke-width="3"/>')

def _ac(o, x, y, s):
    o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{s:.0f}" height="{s*0.7:.0f}" fill="#d0cec6" stroke="#6a6a64" stroke-width="2"/><circle cx="{x+s*0.38:.0f}" cy="{y+s*0.35:.0f}" r="{s*0.26:.0f}" fill="#3a3c40"/>')

def _laundry(o, r, x, y, w):
    o.append(f'<path d="M{x:.0f},{y:.0f}h{w:.0f}" stroke="#2a2a2a" stroke-width="2"/>')
    xx = x + 4
    while xx < x + w - 10:
        cw = r.uniform(10, 24); c = r.choice(['#e84a3a', '#f4f0e0', '#3a7ad8', '#f2c230', '#5aa860', '#e890b0'])
        o.append(f'<rect x="{xx:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{r.uniform(14,34):.0f}" fill="{c}"/>'); xx += cw + r.uniform(2, 8)

def main_facade(W=2080, H=1960, which='front'):
    """Our 7-storey building: 26 m x 24.5 m, 80 px/m, ground floor shops, 6 upper floors of apartments. Returns (colour, glow)."""
    k = 80; r = R(61 if which == 'front' else 62); o = [f'<rect width="{W}" height="{H}" fill="#cfc4ac"/>']; g = [f'<rect width="{W}" height="{H}" fill="#000"/>']
    d, b = noise_layers(W, H, [(0.004, '#6a6050', 2.0, 0.5, 4), (0.06, '#5a5448', 1.2, 0.55, 2)], 61)
    o.append(b)
    Z = lambda z: H - z * k
    fl = [0, 3.8] + [3.8 + 3.45 * i for i in range(1, 7)]
    for z in fl[1:]: o.append(f'<rect y="{Z(z)-10:.0f}" width="{W}" height="18" fill="#a89c84"/><rect y="{Z(z)+8:.0f}" width="{W}" height="6" fill="#5a5448" opacity=".5"/>')
    for x in (0, W / 4, W / 2, 3 * W / 4, W - 30): o.append(f'<rect x="{x:.0f}" width="30" height="{H}" fill="#b8ad96"/>')
    for f in range(1, 7):
        z0 = fl[f] + 0.9; wh = 1.45 * k
        for bay in range(8):
            x = bay * W / 8 + 35; w = W / 8 - 90; lit = r.random() < 0.42
            _win(o, g, r, x, Z(z0) - wh, w, wh, lit, r.random() < 0.75, grille=f <= 3 or r.random() < 0.4, curtain=r.choice([None, '#c86a6a', '#e8d8a0', '#7a9ac8']))
            if r.random() < 0.45: _ac(o, x + w * r.uniform(0.1, 0.6), Z(z0) + 16, 52)
            if r.random() < 0.25: _laundry(o, r, x, Z(z0) - wh - 6, w)
            if r.random() < 0.3:
                for p in range(3): o.append(f'<circle cx="{x+20+p*28:.0f}" cy="{Z(z0)+6:.0f}" r="14" fill="#3a7a3a"/>')
    # ground floor shops: roller shutters, one open and lit, sign boards
    names = ['ร้านเหล็กดัดเจ๊หงส์', 'ข้าวมันไก่', 'ซ่อมมือถือ', 'ร้านยา']
    for i in range(4):
        x0 = i * W / 4 + 40; x1 = (i + 1) * W / 4 - 40; open_ = i in (0, 1)
        if open_:
            o.append(f'<rect x="{x0:.0f}" y="{Z(2.9):.0f}" width="{x1-x0:.0f}" height="{2.9*k:.0f}" fill="#ffd890"/>'); g.append(f'<rect x="{x0:.0f}" y="{Z(2.9):.0f}" width="{x1-x0:.0f}" height="{2.9*k:.0f}" fill="#ffc870"/>')
            for s in range(5): o.append(f'<rect x="{x0+20+s*(x1-x0-40)/5:.0f}" y="{Z(2.4):.0f}" width="{(x1-x0)/5-30:.0f}" height="{1.9*k:.0f}" fill="#7a4a2a" opacity=".6"/>')
        else:
            o.append(f'<rect x="{x0:.0f}" y="{Z(2.9):.0f}" width="{x1-x0:.0f}" height="{2.9*k:.0f}" fill="#9ea2a8"/>')
            for yy in range(int(Z(2.9)), int(H), 10): o.append(f'<path d="M{x0:.0f},{yy}H{x1:.0f}" stroke="#6a6e76" stroke-width="3"/>')
        cols = ['#d4201c', '#1d6a3a', '#1d4fb8', '#e8b81e'][i]
        o.append(f'<rect x="{x0-10:.0f}" y="{Z(3.75):.0f}" width="{x1-x0+20:.0f}" height="{0.8*k:.0f}" fill="{cols}" stroke="#1a1a1a" stroke-width="6"/><text x="{(x0+x1)/2:.0f}" y="{Z(3.75)+50:.0f}" text-anchor="middle" font-size="44" fill="#fff">{names[i]}</text>')
        g.append(f'<rect x="{x0-10:.0f}" y="{Z(3.75):.0f}" width="{x1-x0+20:.0f}" height="{0.8*k:.0f}" fill="{cols}" opacity=".35"/>')
    for _ in range(60):   # rain streaks from the roof down
        x = r.uniform(0, W); l = r.uniform(100, H * 0.7); o.append(f'<path d="M{x:.0f},0 q{r.uniform(-10,10):.0f},{l/2:.0f} 0,{l:.0f}" stroke="#3a3a3a" stroke-width="{r.uniform(5,26):.0f}" opacity="{r.uniform(.08,.25):.2f}" stroke-linecap="round" fill="none"/>')
    o.append(f'<rect width="{W}" height="40" fill="#2e2e2e" opacity=".5"/>')
    return svg(W, H, ''.join(o), font=True, defs=d), svg(W, H, ''.join(g), font=True)

def facade(kind, seed, W=1024, H=1024):
    """City facade tiles. shop: 16 x 14 m (W 1024, H 896); flat / office / condo / old: 12 x 12 m. Returns (colour, glow)."""
    r = R(seed); o = []; g = [f'<rect width="{W}" height="{H}" fill="#000"/>']
    if kind == 'shop':
        kx = W / 16; kz = H / 14
        for u in range(4):
            col = r.choice(['#e8d4a8', '#b8d8c8', '#e8b8b0', '#b8c8e0', '#f0e0c0', '#d8c0e0', '#e0e0d0'])
            x0 = u * 4 * kx; o.append(f'<rect x="{x0:.0f}" width="{4*kx:.0f}" height="{H}" fill="{col}"/>')
            for f in range(1, 4):
                zt = H - (3.5 * f + 2.6) * kz
                for wv in range(2):
                    x = x0 + (0.4 + wv * 1.8) * kx; _win(o, g, r, x, zt, 1.4 * kx, 1.4 * kz, r.random() < 0.45, r.random() < 0.7, grille=True, curtain=r.choice([None, '#c86a6a', '#e8d8a0']))
                if r.random() < 0.6: _ac(o, x0 + r.uniform(0.3, 2.8) * kx, zt + 1.5 * kz, 40)
                if r.random() < 0.3: _laundry(o, r, x0 + 0.3 * kx, zt - 8, 3.2 * kx)
            yb = H - 2.9 * kz
            if r.random() < 0.5:
                o.append(f'<rect x="{x0+8:.0f}" y="{yb:.0f}" width="{4*kx-16:.0f}" height="{2.9*kz:.0f}" fill="#ffcf80"/>'); g.append(f'<rect x="{x0+8:.0f}" y="{yb:.0f}" width="{4*kx-16:.0f}" height="{2.9*kz:.0f}" fill="#ffc070"/>')
                for s in range(4): o.append(f'<rect x="{x0+14+s*kx:.0f}" y="{yb+30:.0f}" width="{kx*0.7:.0f}" height="{2.2*kz:.0f}" fill="#8a5a3a" opacity=".55"/>')
            else:
                o.append(f'<rect x="{x0+8:.0f}" y="{yb:.0f}" width="{4*kx-16:.0f}" height="{2.9*kz:.0f}" fill="#9a9ea6"/>')
                for yy in range(int(yb), H, 8): o.append(f'<path d="M{x0+8:.0f},{yy}h{4*kx-16:.0f}" stroke="#6a6e76" stroke-width="2"/>')
            sc = r.choice(['#d4201c', '#1d6a3a', '#1d4fb8', '#e8b81e', '#f07a1e'])
            o.append(f'<rect x="{x0+6:.0f}" y="{yb-0.7*kz:.0f}" width="{4*kx-12:.0f}" height="{0.6*kz:.0f}" fill="{sc}"/><text x="{x0+2*kx:.0f}" y="{yb-0.25*kz:.0f}" text-anchor="middle" font-size="26" fill="#fff">{r.choice(["ขายส่ง","ร้านทอง","ก๋วยเตี๋ยว","ซ่อมรถ","ยาจีน","โชห่วย","ร้านตัดผม"])}</text>')
            g.append(f'<rect x="{x0+6:.0f}" y="{yb-0.7*kz:.0f}" width="{4*kx-12:.0f}" height="{0.6*kz:.0f}" fill="{sc}" opacity=".5"/>')
            o.append(f'<rect x="{x0:.0f}" width="8" height="{H}" fill="#8a8478"/>')
        o.append(f'<rect width="{W}" height="30" fill="#7a7468"/>')
    elif kind == 'flat':
        base = r.choice(['#c8c0b0', '#b8b4a8', '#d0c8b4']); o.append(f'<rect width="{W}" height="{H}" fill="{base}"/>'); k = W / 12
        for f in range(4):
            zt = f * 3 * k
            o.append(f'<rect y="{zt+2.3*k:.0f}" width="{W}" height="{0.7*k:.0f}" fill="#8a8478"/>')
            for bay in range(4):
                x = bay * 3 * k + 0.3 * k; _win(o, g, r, x, zt + 0.6 * k, 1.5 * k, 1.5 * k, r.random() < 0.45, r.random() < 0.7, grille=r.random() < 0.6, curtain=r.choice([None, '#c86a6a', '#7a9ac8']))
                o.append(f'<rect x="{x+1.7*k:.0f}" y="{zt+1.1*k:.0f}" width="{0.8*k:.0f}" height="{1.0*k:.0f}" fill="#4a4e5a"/>')
                if r.random() < 0.5: _laundry(o, r, x, zt + 2.2 * k - 40, 2.4 * k)
                if r.random() < 0.4: _ac(o, x + 1.7 * k, zt + 2.0 * k - 10, 40)
    elif kind == 'office':
        o.append(f'<rect width="{W}" height="{H}" fill="#4a5672"/>'); k = W / 12
        for f in range(3):
            for bay in range(8):
                x = bay * 1.5 * k; zt = f * 4 * k; lit = r.random() < 0.3; c = '#d8e8ff' if r.random() < 0.7 else '#ffe0a0'
                o.append(f'<rect x="{x+3:.0f}" y="{zt+0.9*k:.0f}" width="{1.5*k-6:.0f}" height="{3.1*k:.0f}" fill="{c if lit else "#2e3a58"}"/>')
                if lit: g.append(f'<rect x="{x+3:.0f}" y="{zt+0.9*k:.0f}" width="{1.5*k-6:.0f}" height="{3.1*k:.0f}" fill="{c}" opacity="{r.uniform(.6,1):.2f}"/>')
                else: o.append(f'<path d="M{x+3:.0f},{zt+3.5*k:.0f} l{1.4*k:.0f},{-2.2*k:.0f} v{0.6*k:.0f} l{-1.4*k:.0f},{2.2*k:.0f}z" fill="#6a7aa8" opacity=".35"/>')
            o.append(f'<rect y="{f*4*k:.0f}" width="{W}" height="{0.9*k:.0f}" fill="#6a7088"/>')
        for bay in range(9): o.append(f'<rect x="{bay*1.5*k-4:.0f}" width="8" height="{H}" fill="#8a90a4"/>')
    elif kind == 'condo':
        o.append(f'<rect width="{W}" height="{H}" fill="#e4e0d8"/>'); k = W / 12
        for f in range(4):
            zt = f * 3 * k
            for bay in range(3):
                x = bay * 4 * k + 0.3 * k; _win(o, g, r, x, zt + 0.5 * k, 3.4 * k, 1.9 * k, r.random() < 0.35, r.random() < 0.55, curtain=r.choice([None, '#e8d8a0', '#a8b8d8']))
            o.append(f'<rect y="{zt+2.4*k:.0f}" width="{W}" height="{0.25*k:.0f}" fill="#b8b4ac"/><rect y="{zt+2.0*k:.0f}" width="{W}" height="{0.4*k:.0f}" fill="#8a96a8" opacity=".55"/>')
            for xx in range(0, W, 24): o.append(f'<path d="M{xx},{zt+2.0*k:.0f}v{0.4*k:.0f}" stroke="#5a6070" stroke-width="2"/>')
    else:   # old concrete block
        o.append(f'<rect width="{W}" height="{H}" fill="#9a968c"/>'); k = W / 12
        for f in range(4):
            for bay in range(6):
                x = bay * 2 * k + 0.6 * k; zt = f * 3 * k + 0.8 * k; _win(o, g, r, x, zt, 0.9 * k, 1.1 * k, r.random() < 0.35, r.random() < 0.8, grille=True)
    d, b = noise_layers(W, H, [(0.006, '#3a3a40', 0.9, 0.5, 4), (0.05, '#2e2c30', 1.0, 0.58, 2)], seed)
    for _ in range(30):
        x = r.uniform(0, W); l = r.uniform(80, H * 0.8); o.append(f'<path d="M{x:.0f},0 q{r.uniform(-8,8):.0f},{l/2:.0f} 0,{l:.0f}" stroke="#2e2e30" stroke-width="{r.uniform(4,20):.0f}" opacity="{r.uniform(.08,.25):.2f}" stroke-linecap="round" fill="none"/>')
    return svg(W, H, ''.join(o) + b, font=True, defs=d), svg(W, H, ''.join(g))

def city_roof(W=1024, seed=71):
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="#7e7a74"/>']
    d, b = noise_layers(W, W, [(0.005, '#3e3c40', 2.0, 0.5, 4), (0.05, '#a8a49c', 1.3, 0.58, 2)], seed)
    o.append(b)
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(0, W); t = r.random()
        if t < 0.35: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(12,28):.0f}" fill="#c8ccd4" stroke="#5a5e66" stroke-width="4"/>')
        elif t < 0.6: o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(20,40):.0f}" height="{r.uniform(14,28):.0f}" fill="#d0cec6" stroke="#5a5a54" stroke-width="3"/>')
        elif t < 0.8: o.append(f'<path d="{blob(r, x, y, r.uniform(20,60), r.uniform(15,40))}" fill="#30344a" opacity=".8"/>')
        else: o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(40,120):.0f}" height="{r.uniform(40,90):.0f}" fill="#2a5ab0" opacity=".85"/>')
    o.append(f'<rect width="{W}" height="{W}" fill="none" stroke="#9a968c" stroke-width="18"/>')
    return svg(W, W, ''.join(o), defs=d)

def ground(W=2048):
    """60 m city tile: a 10 m road along two edges (crossing at the corner), sidewalks, a soi through the block. Returns (colour, glow)."""
    k = W / 60; r = R(81); o = [f'<rect width="{W}" height="{W}" fill="#45444a"/>']; g = [f'<rect width="{W}" height="{W}" fill="#000"/>']
    d, b = noise_layers(W, W, [(0.01, '#2a2a30', 2.0, 0.5, 3), (0.08, '#6a6a70', 1.2, 0.6, 2)], 81)
    o.append(b)
    road = 10 * k
    o.append(f'<rect width="{W}" height="{road:.0f}" fill="#2e2e34"/><rect width="{road:.0f}" height="{W}" fill="#2e2e34"/>')
    o.append(f'<rect y="{road:.0f}" width="{W}" height="{2*k:.0f}" fill="#77746e"/><rect x="{road:.0f}" width="{2*k:.0f}" height="{W}" fill="#77746e"/>')
    for x in range(int(road + 2 * k), W, 60): o.append(f'<path d="M{x},{road/2:.0f}h34" stroke="#e8e0c8" stroke-width="6"/><path d="M{road/2:.0f},{x}v34" stroke="#e8e0c8" stroke-width="6"/>')
    o.append(f'<path d="M0,{road/2-8:.0f}H{W}" stroke="#d8b02a" stroke-width="4" opacity=".0"/>')
    for i in range(6): o.append(f'<rect x="{i*14+4:.0f}" y="{road+4:.0f}" width="8" height="{2*k-8:.0f}" fill="#e8e0c8"/>')
    o.append(f'<rect x="{30*k:.0f}" y="{road:.0f}" width="{3*k:.0f}" height="{W-road:.0f}" fill="#3a3a40"/>')
    for x in range(int(road + 4 * k), W, int(12 * k)):   # street lights + car lights
        g.append(f'<circle cx="{x}" cy="{road+k:.0f}" r="{2.5*k:.0f}" fill="#ffb060" opacity=".22"/><circle cx="{x}" cy="{road+k:.0f}" r="{0.5*k:.0f}" fill="#ffd8a0"/>')
        g.append(f'<circle cx="{road+k:.0f}" cy="{x}" r="{2.5*k:.0f}" fill="#ffb060" opacity=".22"/><circle cx="{road+k:.0f}" cy="{x}" r="{0.5*k:.0f}" fill="#ffd8a0"/>')
    for _ in range(14):
        x = r.uniform(0, W); lane = r.choice([0.27, 0.73]); c = '#ff3a2a' if lane < 0.5 else '#fff4d8'
        g.append(f'<rect x="{x:.0f}" y="{road*lane-6:.0f}" width="{r.uniform(20,60):.0f}" height="10" fill="{c}"/><rect x="{road*lane-6:.0f}" y="{x:.0f}" width="10" height="{r.uniform(20,60):.0f}" fill="{c}"/>')
        o.append(f'<rect x="{x:.0f}" y="{road*lane-14:.0f}" width="{4.2*k:.0f}" height="{1.8*k:.0f}" rx="8" fill="{r.choice(["#c8c8c8","#3a3a3a","#d42a2a","#2a5ab0","#e8e0d0"])}"/>')
    return svg(W, W, ''.join(o), defs=d), svg(W, W, ''.join(g))

def river(W=2048, H=1024):
    """Chao Phraya water, 200 x 100 m tile. Returns (colour, glow)."""
    r = R(91); o = [f'<rect width="{W}" height="{H}" fill="#2a3048"/>']; g = [f'<rect width="{W}" height="{H}" fill="#000"/>']
    d, b = noise_layers(W, H, [(0.004, '#1a1e30', 2.0, 0.5, 3), (0.02, '#4a5070', 1.8, 0.6, 2)], 91)
    o.append(b)
    for _ in range(500):
        x, y = r.uniform(0, W), r.uniform(0, H); w = r.uniform(20, 90)
        o.append(f'<path d="M{x:.0f},{y:.0f}q{w/2:.0f},-5 {w:.0f},0" stroke="{r.choice(["#5a6290","#7a82b0","#3a4060"])}" stroke-width="{r.uniform(2,5):.0f}" fill="none" opacity=".7"/>')
    for _ in range(40):   # light reflections (streaky)
        x, y = r.uniform(0, W), r.uniform(0, H); c = r.choice(['#ffc070', '#ffd890', '#cfe0ff', '#ff8a5a'])
        for j in range(6):
            s = f'<rect x="{x+r.uniform(-12,12):.0f}" y="{y+j*14:.0f}" width="{r.uniform(10,40):.0f}" height="5" fill="{c}" opacity="{0.9-j*0.13:.2f}"/>'; o.append(s); g.append(s)
    for _ in range(5):   # boats with wakes
        x, y = r.uniform(0, W), r.uniform(0, H)
        o.append(f'<path d="M{x:.0f},{y:.0f} l-160,-30 m160,30 l-160,30" stroke="#a8b0d8" stroke-width="4" opacity=".6" fill="none"/><rect x="{x:.0f}" y="{y-8:.0f}" width="60" height="16" rx="6" fill="#3a2a20"/>')
        g.append(f'<circle cx="{x+50:.0f}" cy="{y:.0f}" r="5" fill="#ffe0a0"/>')
    return svg(W, H, ''.join(o), defs=d), svg(W, H, ''.join(g))

def expressway(W=1024, H=256):
    """Side of the elevated deck, 40 m x 10 m (parapet with lamp posts and a light strip). Returns (colour, glow)."""
    r = R(95); o = [f'<rect width="{W}" height="{H}" fill="#a29e96"/>']; g = [f'<rect width="{W}" height="{H}" fill="#000"/>']
    d, b = noise_layers(W, H, [(0.01, '#4a4a50', 2.0, 0.5, 3)], 95)
    o.append(b)
    o.append(f'<rect y="{H*0.55:.0f}" width="{W}" height="{H*0.45:.0f}" fill="#7a7670"/><rect y="{H*0.52:.0f}" width="{W}" height="10" fill="#5a5650"/>')
    for x in range(0, W, 128): o.append(f'<path d="M{x},{H*0.55:.0f}V{H}" stroke="#5a5650" stroke-width="5"/>')
    for _ in range(20): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},{H*0.55:.0f}v{r.uniform(20,H*0.45):.0f}" stroke="#3a3a3e" stroke-width="{r.uniform(4,14):.0f}" opacity=".3"/>')
    o.append(f'<rect y="0" width="{W}" height="{H*0.5:.0f}" fill="none"/>')
    for x in range(64, W, 256):
        o.append(f'<path d="M{x},{H*0.5:.0f}V8h40" stroke="#5a5a5e" stroke-width="6" fill="none"/><rect x="{x+30}" y="4" width="22" height="10" fill="#ffd8a0"/>'); g.append(f'<rect x="{x+30}" y="4" width="22" height="10" fill="#ffd8a0"/><circle cx="{x+40}" cy="12" r="26" fill="#ffb060" opacity=".25"/>')
    for _ in range(10):
        x = r.uniform(0, W); c = r.choice(['#ff3a2a', '#fff4d8']); o.append(f'<rect x="{x:.0f}" y="{H*0.38:.0f}" width="{r.uniform(30,80):.0f}" height="8" fill="{c}"/>'); g.append(f'<rect x="{x:.0f}" y="{H*0.38:.0f}" width="{r.uniform(30,80):.0f}" height="8" fill="{c}"/>')
    return svg(W, H, ''.join(o), defs=d), svg(W, H, ''.join(g))

def temple_roof(W=512, H=512, c1='#e0702a', c2='#2a8a4a'):
    o = [f'<rect width="{W}" height="{H}" fill="{c1}"/>']
    for j in range(0, H, 32):
        for i in range(0, W, 24): o.append(f'<path d="M{i+(j//32%2)*12},{j}h22v26q-11,8 -22,0z" fill="{c1}" stroke="#8a3a14" stroke-width="2"/>')
    o.append(f'<rect width="70" height="{H}" fill="{c2}"/><rect x="{W-70}" width="70" height="{H}" fill="{c2}"/><rect y="{H-60}" width="{W}" height="60" fill="{c2}"/>')
    return svg(W, H, ''.join(o))

def temple_wall(W=512, H=512):
    o = [f'<rect width="{W}" height="{H}" fill="#f0e8d8"/><rect y="{H-60}" width="{W}" height="60" fill="#c8b890"/>']
    for x in range(40, W, 120): o.append(f'<path d="M{x},{H-60}V180q40,-90 80,0V{H-60}z" fill="#3a2a20" stroke="#d8a830" stroke-width="12"/>')
    o.append(f'<rect width="{W}" height="30" fill="#d8a830"/>')
    return svg(W, H, ''.join(o))

def prang(W=512, H=1024):
    """Porcelain-studded prang surface (Wat Arun-like), wraps a cone, tier lines across."""
    r = R(97); o = [f'<rect width="{W}" height="{H}" fill="#e8dcc4"/>']
    for y in range(0, H, 48): o.append(f'<rect y="{y}" width="{W}" height="10" fill="#b8a888"/>')
    for _ in range(1600):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,5):.1f}" fill="{r.choice(["#3a7ab8","#d8a830","#c84a3a","#3a9a6a","#f4f0e8"])}"/>')
    return svg(W, H, ''.join(o))

def neon(text, W=1024, H=256, c='#ff4a3a', bg='#1a1a24'):
    """Rooftop / facade signs on nearby buildings. Returns (colour, glow)."""
    s = (f'<rect width="{W}" height="{H}" fill="{bg}"/><rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{c}" stroke-width="10"/>'
         f'<text x="{W/2}" y="{H*0.7:.0f}" text-anchor="middle" font-size="{H*0.55:.0f}" textLength="{W*0.86:.0f}" lengthAdjust="spacingAndGlyphs" fill="{c}">{text}</text>')
    gl = (f'<rect width="{W}" height="{H}" fill="#000"/><rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{c}" stroke-width="10"/>'
          f'<text x="{W/2}" y="{H*0.7:.0f}" text-anchor="middle" font-size="{H*0.55:.0f}" textLength="{W*0.86:.0f}" lengthAdjust="spacingAndGlyphs" fill="{c}">{text}</text>')
    return svg(W, H, s, font=True), svg(W, H, gl, font=True)

def glow_disc(W=256):
    return svg(W, W, '<defs><radialGradient id="g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="#fff" stop-opacity=".45"/>'
                     '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>' + f'<rect width="{W}" height="{W}" fill="url(#g)"/>')

# ----------------------------------------------------------------------------- the storm sky (equirectangular, 4096 x 2048; u 0.75 = +y, the main view)
def sky(W=4096, H=2048, bolt_u=0.33):
    r = R(101); HZ = H / 2; deg = HZ / 90
    defs = ('<linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121226"/><stop offset=".25" stop-color="#1b1a3a"/><stop offset=".4" stop-color="#2a2858"/>'
            '<stop offset=".47" stop-color="#3e3d74"/><stop offset=".5" stop-color="#55558c"/><stop offset=".52" stop-color="#4a4a7c"/><stop offset="1" stop-color="#1e1e34"/></linearGradient>'
            '<radialGradient id="lg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e4e8ff"/><stop offset=".25" stop-color="#9aa4f0" stop-opacity=".8"/><stop offset="1" stop-color="#5a62b8" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="lg2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#b8c0ff" stop-opacity=".7"/><stop offset="1" stop-color="#5a62b8" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="rain" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a6ca0" stop-opacity=".55"/><stop offset="1" stop-color="#6a6ca0" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="cityglow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9a7a78" stop-opacity="0"/><stop offset="1" stop-color="#a08070" stop-opacity=".35"/></linearGradient>')
    o = [f'<rect width="{W}" height="{H}" fill="url(#sg)"/>', f'<rect y="{HZ-6*deg:.0f}" width="{W}" height="{6*deg:.0f}" fill="url(#cityglow)"/>']
    Y = lambda el: HZ - el * deg
    def glow(u, el, rx, ry, gid='lg', op=1.0):
        for dx in (-W, 0, W): o.append(f'<ellipse cx="{u*W+dx:.0f}" cy="{Y(el):.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#{gid})" opacity="{op}"/>')
    # internal lightning glows behind the cloud deck
    glow(bolt_u, 32, 900, 420); glow(bolt_u - 0.04, 50, 900, 300, 'lg2'); glow(bolt_u - 0.06, 66, 1500, 200, 'lg2', .8); glow(0.62, 22, 500, 180, 'lg2', .8); glow(0.9, 30, 420, 160, 'lg2', .6); glow(0.12, 16, 380, 120, 'lg2', .7)
    # cloud layers: far (high, small) to near (low, big). Each cloud = lumps with a lit top rim and a dark base.
    layers = [(62, 84, 34, ('#1e1d40', '#2a2952', '#3a3a6e'), 1.6), (38, 58, 30, ('#232248', '#302f62', '#46467e'), 1.3), (20, 36, 34, ('#2a2a54', '#38386c', '#55558c'), 1.0),
              (6, 18, 38, ('#2e2d58', '#3c3c70', '#5e5e96'), 0.8), (1, 6, 30, ('#26264a', '#323260', '#4e4e84'), 0.55)]
    gid = 0
    for (el0, el1, n, (dark, mid, rim), sc) in layers:
        for _ in range(n):
            u = r.random(); el = r.uniform(el0, el1); stretch = 1 / max(math.cos(math.radians(el)), 0.25)
            nb = min(abs(u - bolt_u), 1 - abs(u - bolt_u)); lit = max(0.0, 1 - nb / 0.14) if el < 55 else 0.0
            rimc = '#%02x%02x%02x' % tuple(int(a + (b - a) * lit) for a, b in zip(bytes.fromhex(rim[1:]), bytes.fromhex('b8c0ff')))
            gid += 1; defs += (f'<linearGradient id="c{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{rimc}"/><stop offset=".35" stop-color="{mid}"/>'
                               f'<stop offset="1" stop-color="{dark}"/></linearGradient>')
            w = r.uniform(260, 620) * sc * stretch; h = r.uniform(70, 160) * sc
            cx = u * W; cy = Y(el)
            lumps = [(r.uniform(-w / 2, w / 2), r.uniform(-h * 0.5, 0), r.uniform(0.18, 0.34) * w, r.uniform(0.5, 0.9) * h) for _ in range(7)]
            for dx in (-W, 0, W):
                g = [f'<g transform="translate({cx+dx:.0f},{cy:.0f})">']
                g.append(f'<ellipse cx="0" cy="{h*0.3:.0f}" rx="{w*0.62:.0f}" ry="{h*0.45:.0f}" fill="{dark}"/>')
                for (lx, ly, lrx, lry) in sorted(lumps, key=lambda q: q[1]): g.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{lrx:.0f}" ry="{lry:.0f}" fill="url(#c{gid})"/>')
                g.append(f'<ellipse cx="0" cy="{h*0.45:.0f}" rx="{w*0.55:.0f}" ry="{h*0.22:.0f}" fill="{dark}" opacity=".8"/>')
                g.append('</g>'); o.append(''.join(g))
    glow(bolt_u, 26, 520, 200, 'lg2', .55)
    for dx in (-W, 0, W):   # lit cloud undersides around the strike, screen-blended over the deck
        o.append(f'<ellipse cx="{bolt_u*W+dx:.0f}" cy="{Y(30):.0f}" rx="700" ry="330" fill="url(#lg2)" style="mix-blend-mode:screen" opacity=".75"/>')
        o.append(f'<ellipse cx="{(bolt_u-0.03)*W+dx:.0f}" cy="{Y(58):.0f}" rx="1100" ry="240" fill="url(#lg2)" style="mix-blend-mode:screen" opacity=".6"/>')
    # rain shafts falling from the cloud base to the horizon
    for _ in range(14):
        u = r.random(); x = u * W; w = r.uniform(120, 380)
        for dx in (-W, 0, W):
            o.append(f'<path d="M{x+dx:.0f},{Y(14):.0f} h{w:.0f} l{-w*0.3:.0f},{14*deg+40:.0f} h{-w:.0f}z" fill="url(#rain)" opacity=".35"/>')
            for k in range(int(w / 14)):
                xx = x + dx + k * 14 + r.uniform(-4, 4); o.append(f'<path d="M{xx:.0f},{Y(13):.0f} l{-w*0.3*0.6:.0f},{14*deg*0.6:.0f}" stroke="#8a8cc0" stroke-width="2" opacity=".25"/>')
    # distant forked lightning
    for (u, el, s) in ((0.62, 18, 1.0), (0.9, 24, 0.8), (0.12, 12, 0.7), (0.205, 15, 0.9)):
        x, y = u * W, Y(el); pts = [(x, y)]
        for k in range(9): x += r.uniform(-24, 24) * s; y += r.uniform(16, 30) * s; pts.append((x, y))
        p = 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts)
        o.append(f'<path d="{p}" stroke="#aab4ff" stroke-width="10" opacity=".4" fill="none"/><path d="{p}" stroke="#f0f2ff" stroke-width="3" fill="none"/>')
    # below the horizon: haze (hidden by the city ground where geometry exists)
    o.append(f'<rect y="{HZ+30:.0f}" width="{W}" height="{HZ:.0f}" fill="#22223a"/>')
    return svg(W, H, ''.join(o), defs=defs)

def sky_top(W=2048, glow_uv=(0.56, 0.60)):
    """The storm cloud base seen from below, gnomonic plane (x/z, y/z) in [-2.5, 2.5]: image right = +x, image top = +y.
    Blended over the equirect sky above ~35 degrees elevation (no pinching overhead)."""
    r = R(131); o = [f'<rect width="{W}" height="{W}" fill="#1c1b3c"/>']
    gx, gy = glow_uv[0] * W, (1 - glow_uv[1]) * W
    defs = ('<radialGradient id="tg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#dfe4ff"/><stop offset=".2" stop-color="#9aa6f0" stop-opacity=".85"/><stop offset=".6" stop-color="#5a62b8" stop-opacity=".35"/><stop offset="1" stop-color="#3a3a80" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="tg2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3a3a74" stop-opacity=".9"/><stop offset="1" stop-color="#1c1b3c" stop-opacity="0"/></radialGradient>')
    o.append(f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{W*0.55:.0f}" ry="{W*0.45:.0f}" fill="url(#tg)" opacity=".75"/>')
    o.append(f'<circle cx="{W/2}" cy="{W/2}" r="{W*0.3:.0f}" fill="url(#tg2)"/>')
    # big cloud masses (clusters of lumps) with dark gaps between them where the lightning glow shows through
    for k in range(230):
        mx, my = r.uniform(-100, W + 100), r.uniform(-100, W + 100); R0 = r.uniform(60, 170)
        lumps = [(mx + r.gauss(0, R0 * 0.6), my + r.gauss(0, R0 * 0.4), r.uniform(0.3, 0.6) * R0) for _ in range(r.randint(6, 12))]
        d = math.hypot(mx - gx, my - gy) / W; lit = max(0.0, 1 - d * 1.7) ** 1.4
        rim = '#%02x%02x%02x' % (int(56 + 140 * lit), int(56 + 146 * lit), int(104 + 140 * lit))
        body = '#%02x%02x%02x' % (int(36 + 30 * lit), int(35 + 32 * lit), int(74 + 48 * lit))
        shade = '#%02x%02x%02x' % (int(24 + 14 * lit), int(23 + 15 * lit), int(50 + 24 * lit))
        ux, uy = (gx - mx), (gy - my); n = math.hypot(ux, uy) + 1e-6; ux, uy = ux / n, uy / n
        defs += (f'<linearGradient id="t{k}" x1="{0.5+0.5*ux:.2f}" y1="{0.5+0.5*uy:.2f}" x2="{0.5-0.5*ux:.2f}" y2="{0.5-0.5*uy:.2f}"><stop offset="0" stop-color="{rim}"/>'
                 f'<stop offset=".3" stop-color="{body}"/><stop offset="1" stop-color="{shade}"/></linearGradient>')
        o.append(f'<g transform="rotate({r.uniform(-35,-15):.0f} {mx:.0f} {my:.0f})">' + ''.join(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr*1.45:.0f}" ry="{rr*0.75:.0f}" fill="url(#t{k})"/>' for (x, y, rr) in lumps) + '</g>')
    for _ in range(18):   # dark scud streaks drifting across
        x, y = r.uniform(0, W), r.uniform(0, W); w = r.uniform(200, 600)
        o.append(f'<path d="{blob(r, x, y, w, w*0.12, 10)}" fill="#141330" opacity=".55" transform="rotate(-25 {x:.0f} {y:.0f})"/>')
    o.append(f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{W*0.22:.0f}" ry="{W*0.16:.0f}" fill="url(#tg)" style="mix-blend-mode:screen" opacity=".55"/>')
    for _ in range(900):   # rain seen from below: streaks radiating from the zenith
        a = r.uniform(0, 2 * math.pi); r0 = r.uniform(30, W * 0.75); l = r.uniform(40, 160) * (0.4 + r0 / W)
        x0, y0 = W / 2 + math.cos(a) * r0, W / 2 + math.sin(a) * r0
        o.append(f'<path d="M{x0:.0f},{y0:.0f} l{math.cos(a)*l:.0f},{math.sin(a)*l:.0f}" stroke="#9aa0d8" stroke-width="{r.uniform(1.5,3):.1f}" opacity="{r.uniform(.15,.35):.2f}"/>')
    return svg(W, W, ''.join(o), defs=defs)

# ----------------------------------------------------------------------------- jobs
LAMP_U = [(-5.0, True), (-3.0, False), (-1.0, True), (1.0, False), (3.0, False), (5.0, True)]   # billboard lamps: x and working?

def _jobs():
    J = dict(
        floor=(roof_floor, 2048, 2048, False), parapet=(concrete_wall, 1024, 512, False), plinth=(lambda: concrete_wall(512, 512, 9, '#8a867e'), 512, 512, False),
        steel=(steel, 512, 512, False), steel_y=(lambda: steel(512, 12, '#d8a820'), 512, 512, False), grating=(grating, 512, 512, True), tread=(tread_plate, 512, 512, False),
        board=(billboard, 2400, 1200, False), pool=(lambda: billboard_pool(lamps=[(x + 6) / 12 for x, ok in LAMP_U if ok]), 1200, 600, False), pback=(panel_back, 1024, 512, False),
        hut=(hut_wall, 1024, 768, False), door=(door, 512, 1024, False),
        sign_rain=(lambda: sign(['ห้ามขึ้น', 'ขณะฝนตก']), 512, 384, False), sign_hv=(lambda: sign(['อันตราย', 'ไฟฟ้าแรงสูง'], bg='#e8e4d8', fg='#c81a1a'), 512, 384, False),
        tank=(tank, 1024, 512, False), ac=(ac_front, 512, 384, False), ac2=(lambda: ac_front(brand='SAIJO'), 512, 384, False), tarp=(tarp, 1024, 1024, False),
        o2=(lambda: cylinder_label('#1e2a22', '#f4f0e8', 'ออกซิเจน', 'O2 · 150 BAR'), 512, 512, False), c2h2=(lambda: cylinder_label('#7a1e1e', '#d8d0c0', 'อะเซทิลีน', 'C2H2 · ไวไฟ'), 512, 512, False),
        machine=(machine, 512, 384, False), toolbox=(toolbox, 512, 256, False),
        cl1=(lambda: cloth('#e84a3a', '#f4f0e0', 'stripe'), 256, 256, False), cl2=(lambda: cloth('#3a7ad8', '#f4f0e0', 'check'), 256, 256, False),
        cl3=(lambda: cloth('#f2c230', '#e84a3a', 'dots'), 256, 256, False), cl4=(lambda: cloth('#f4f0e0', '#5aa860', 'stripe'), 256, 256, False),
        croof=(city_roof, 1024, 1024, False), troof=(temple_roof, 512, 512, False), twall=(temple_wall, 512, 512, False), prang=(prang, 512, 1024, False),
        glow=(glow_disc, 256, 256, True), sky=(sky, 4096, 2048, False), sky_top=(sky_top, 2048, 2048, False),
    )
    pairs = dict(main=(lambda: main_facade(which='front'), 2080, 1960), side=(lambda: main_facade(which='side'), 2080, 1960),
                 shop1=(lambda: facade('shop', 201), 1024, 896), shop2=(lambda: facade('shop', 202), 1024, 896), flat=(lambda: facade('flat', 203), 1024, 1024),
                 office=(lambda: facade('office', 204), 1024, 1024), condo=(lambda: facade('condo', 205), 1024, 1024), old=(lambda: facade('old', 206), 1024, 1024),
                 ground=(ground, 2048, 2048), river=(river, 2048, 1024), xway=(expressway, 1024, 256),
                 neon1=(lambda: neon('โรงแรมฟ้าใส'), 1024, 256), neon2=(lambda: neon('ร้านทองเยาวราช', c='#ffc83a'), 1024, 256), neon3=(lambda: neon('คาราโอเกะ', c='#3ad8ff'), 1024, 256),
                 neon4=(lambda: neon('ข้าวต้ม 24 ชม.', c='#ff8a2a', W=768), 768, 256))
    return J, pairs

def build_all(force=False):
    os.makedirs(TEX, exist_ok=True); jobs = []; paths = {}
    J, pairs = _jobs()
    items = []
    for name, (fn, w, h, tr) in J.items(): items.append((name, fn, w, h, tr))
    for name, (fn, w, h) in pairs.items():
        cache = {}
        def col(fn=fn, cache=cache):
            if 'v' not in cache: cache['v'] = fn()
            return cache['v'][0]
        def glo(fn=fn, cache=cache):
            if 'v' not in cache: cache['v'] = fn()
            return cache['v'][1]
        items.append((name, col, w, h, False)); items.append((name + '_g', glo, w, h, False))
    for name, fn, w, h, tr in items:
        s = fn(); hsh = hashlib.sha1(s.encode()).hexdigest()[:10]; png = os.path.join(TEX, f'{name}_{hsh}.png'); paths[name] = png
        if force or not os.path.exists(png):
            sp = png[:-4] + '.svg'; open(sp, 'w').write(s); jobs.append(dict(src=sp, out=png, w=w, h=h, transparent=tr))
    if jobs:
        jp = os.path.join(TEX, 'jobs.json'); json.dump(jobs, open(jp, 'w'))
        env = dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules'))
        res = subprocess.run(['node', RASTER, jp], capture_output=True, env=env)
        if res.returncode != 0: raise RuntimeError(res.stderr.decode()[-2000:])
        for j in jobs: os.remove(j['src'])
    return paths

if __name__ == '__main__':
    import time; t = time.time(); p = build_all(); print(len(p), 'textures', round(time.time() - t, 1), 's')
