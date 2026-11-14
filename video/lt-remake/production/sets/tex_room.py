"""SVG artwork for the welder's rented room (room3d.py), rasterised by Chromium (one launch for all jobs). Cached by content hash in room_tex/.
Convention (as tex_soi): SVG y grows downward = texture v from 1 (top row) to 0 (bottom row). Wall textures: x = along the wall as seen
from inside the room, top = ceiling. Everything is a fictional brand / name; Thai text in Kanit (f2/f3), handwriting in Sriracha."""
import os, json, hashlib, base64, subprocess, math, random
from tex_soi import blot, crack, streaks, T as _T
HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'room_tex')
RASTER = os.path.join(os.path.dirname(HERE), 'v3', 'set3d', 'raster.js')
FDIR = '/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/mw/hf/rig/assets/fonts/'
_B = lambda f: base64.b64encode(open(os.path.join(FDIR, f), 'rb').read()).decode()
FONT = None
R = random.Random

def _font():
    global FONT
    if FONT is None:
        FONT = (f"<style>@font-face{{font-family:KB;src:url(data:font/ttf;base64,{_B('f2.ttf')})}}"
                f"@font-face{{font-family:KK;src:url(data:font/ttf;base64,{_B('f3.ttf')})}}"
                f"@font-face{{font-family:HW;src:url(data:font/ttf;base64,{_B('sriracha.ttf')})}} text{{font-family:KB}} .k{{font-family:KK}} .h{{font-family:HW}}</style>")
    return FONT

def svg(w, h, body, font=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block">{_font() if font else ""}{body}</svg>'

def T(x, y, s, txt, fill='#fff', anchor='middle', k=False, hw=False, rot=0, op=1.0, stroke=None, sw=0):
    if hw:
        tr = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ''
        return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{s:.0f}" fill="{fill}" text-anchor="{anchor}" class="h"{tr} opacity="{op}">{txt}</text>'
    return _T(x, y, s, txt, fill, anchor, k, stroke, sw, rot, op)

def poly(r, cx, cy, rx, ry, n=10, jit=0.3):
    return ' '.join(f'{cx+math.cos(t)*rx*r.uniform(1-jit,1):.0f},{cy+math.sin(t)*ry*r.uniform(1-jit,1):.0f}' for t in [i * 6.283 / n for i in range(n)])

# ----------------------------------------------------------------------------- walls, floor, ceiling
WALL = '#b9d3c6'      # cheap mint-green emulsion
def wall(seed, wm, hm=2.6, holes=(), W=None, kind='in', base=WALL):
    """One wall (wm x hm m). holes: (x0, x1, z0, z1) in m from the left / floor (door, window): stains run around them.
    kind 'in' = room side (damp, cracks, tape, nail holes), 'out' = corridor side (grimier, painted dado)."""
    r = R(seed); W = W or int(min(2048, 320 * wm)); k = W / wm; H = int(hm * k); X = lambda x: x * k; Z = lambda z: (hm - z) * k
    o = [f'<rect width="{W}" height="{H}" fill="{base}"/>', blot(r, W, H, int(60 * wm), ['#7a8a70', '#ffffff', '#6a7a6a', '#9aa890'], 0.1 * k, 0.6 * k, (0.04, 0.10))]
    if kind == 'out':
        o.append(f'<rect x="0" y="{Z(1.0):.0f}" width="{W}" height="{1.0*k:.0f}" fill="#7a9a8a"/><rect x="0" y="{Z(1.0):.0f}" width="{W}" height="6" fill="#3a4a40" opacity=".5"/>')
        o.append(blot(r, W, H, int(30 * wm), ['#3a3a30', '#5a5a48'], 0.1 * k, 0.5 * k, (0.06, 0.16)))
    # damp: tide-marked stains bleeding down from the ceiling (soft fill, one crisp brown tide line) and rising damp along the floor
    fid = f'd{seed}'; o.append(f'<defs><filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{0.05*k:.1f}"/></filter>'
                               f'<filter id="{fid}b" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{0.012*k:.1f}"/></filter></defs>')
    for _ in range(2 if kind == 'in' else 1):
        cx = r.uniform(0.1, 0.9) * W; rr = r.uniform(0.45, 0.9) * k
        o.append(f'<g filter="url(#{fid})">' + ''.join(f'<polygon points="{poly(r, cx, -0.05 * k, rr * (1 - j * 0.25), rr * (1.25 - j * 0.32), 22, 0.22)}" fill="{c}" opacity="{op}"/>'
                 for j, (c, op) in enumerate((('#8a7a4a', .28), ('#6a6a3a', .22), ('#4a4a2a', .25)))) + '</g>')
        o.append(f'<polygon points="{poly(r, cx, -0.05 * k, rr * 1.02, rr * 1.28, 26, 0.12)}" fill="none" stroke="#6a5226" stroke-width="3" opacity=".5" filter="url(#{fid}b)"/>')
        for _ in range(7):                                      # drip runs below the stain
            x = cx + r.uniform(-0.6, 0.6) * rr; y0 = rr * r.uniform(0.6, 1.1); L = r.uniform(0.2, 0.7) * k
            o.append(f'<path d="M{x:.0f},{y0:.0f}q{r.uniform(-6,6):.0f},{L/2:.0f} {r.uniform(-4,4):.0f},{L:.0f}" stroke="#6a6038" stroke-width="{r.uniform(3,8):.0f}" opacity="{r.uniform(.12,.25):.2f}" fill="none" stroke-linecap="round" filter="url(#{fid}b)"/>')
    o.append(f'<g filter="url(#{fid}b)"><rect x="0" y="{Z(0.22):.0f}" width="{W}" height="{0.22*k:.0f}" fill="#4a5a3a" opacity=".16"/>'
             + ''.join(f'<ellipse cx="{r.uniform(0,W):.0f}" cy="{Z(0.18):.0f}" rx="{r.uniform(0.1,0.3)*k:.0f}" ry="{r.uniform(0.05,0.12)*k:.0f}" fill="#4a5030" opacity=".14"/>' for _ in range(int(wm * 5))) + '</g>')
    for _ in range(int(wm * 220)):                          # plaster speckle and trowel texture: keeps the wall from reading as an empty colour field
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.6,1.8):.1f}" fill="{r.choice(["#5a6a5a", "#ffffff", "#7a7a60"])}" opacity="{r.uniform(.15,.4):.2f}"/>')
    for _ in range(int(wm * 14)):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<path d="M{x:.0f},{y:.0f}q{r.uniform(10,30):.0f},{r.uniform(-8,8):.0f} {r.uniform(30,70):.0f},{r.uniform(-4,4):.0f}" stroke="#ffffff" stroke-width="{r.uniform(2,5):.1f}" fill="none" opacity=".08"/>')
    o.append(f'<rect x="0" y="{Z(0.1):.0f}" width="{W}" height="{0.1*k:.0f}" fill="#4a4a40" opacity=".55"/>')   # skirting of grime
    # peeling paint showing old cream coat and grey render
    for _ in range(int(wm * 2.5)):
        x, y = r.uniform(0, W), r.uniform(Z(2.4), Z(0.3)); w = r.uniform(0.03, 0.16) * k; h = w * r.uniform(0.4, 0.9)
        if any(X(a) - 20 < x < X(b) + 20 and Z(d) - 20 < y < Z(c) + 20 for a, b, c, d in holes): continue
        o.append(f'<polygon points="{poly(r, x, y, w * 0.7, h * 0.7, 9, 0.4)}" fill="{r.choice(["#c4c8b4", "#b0b4a6", "#c8c4b0"])}" stroke="#e8eee0" stroke-width="1.5" opacity=".8"/>')
    # plaster cracks: long ones from the hole corners, hairlines elsewhere
    for (a, b, c, d) in holes:
        for (px, pz, ang) in ((a, d, -2.3), (b, d, -0.8), (a, c, 2.4), (b, c, 0.7)):
            if 0 < pz < hm and r.random() < 0.75: o.append(crack(r, X(px), Z(pz), r.randint(6, 12), 0.08 * k, '#24201a', 2.8, 0.85, ang))
    for _ in range(int(wm * 3.5)): o.append(crack(r, r.uniform(0, W), r.uniform(Z(2.5), Z(0.2)), r.randint(4, 12), 0.06 * k, '#24201a', 2.6, 0.8))
    if kind == 'in':
        for _ in range(int(wm * 6)):                        # nail holes, tape scraps, pencil marks, mosquito smears
            x, y = r.uniform(0, W), r.uniform(Z(2.2), Z(0.6)); t = r.random()
            if t < 0.3: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#2a2420"/>')
            elif t < 0.55: o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{0.05*k:.0f}" height="{0.018*k:.0f}" fill="#e8dca8" opacity=".75" transform="rotate({r.uniform(-30,30):.0f} {x:.0f} {y:.0f})"/>')
            elif t < 0.75: o.append(f'<path d="M{x:.0f},{y:.0f}l{r.uniform(-12,12):.0f},{r.uniform(-6,6):.0f}" stroke="#7a2a1a" stroke-width="3" opacity=".6"/>')
            else: o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{0.25*k:.0f}" height="{0.35*k:.0f}" fill="#000" opacity=".05"/>')   # ghost of an old poster
        for _ in range(3):
            x, y = r.uniform(0.1, 0.9) * W, r.uniform(Z(1.8), Z(0.9))
            o.append(T(x, y, 0.045 * k, r.choice(['089-5521-07', 'ค่าน้ำ 18/หน่วย', 'ห้ามตอกตะปู!', 'จ่ายห้อง 5 ทุกเดือน']), '#3a3a6a', hw=True, rot=r.uniform(-8, 8), op=.7))
    return svg(W, H, ''.join(o), font=kind == 'in')

def floor(seed=11, wm=3.2, dm=4.0, ts=0.30, W=1024):
    """Worn 30 cm ceramic tiles, cream with brown flecks, grime in joints, chipped corners, a few cracked; a worn path to the door."""
    r = R(seed); k = W / wm; H = int(dm * k); o = [f'<rect width="{W}" height="{H}" fill="#4a4034"/>']; s = ts * k
    for i in range(int(wm / ts) + 1):
        for j in range(int(dm / ts) + 1):
            x, y = i * s, j * s; c = r.choice(['#d8cbb0', '#d2c4a6', '#ddd0b6', '#cfc0a2', '#d5c8ac'])
            o.append(f'<rect x="{x+2.5:.0f}" y="{y+2.5:.0f}" width="{s-5:.0f}" height="{s-5:.0f}" fill="{c}"/><path d="M{x+4:.0f},{y+s-4:.0f}V{y+4:.0f}H{x+s-4:.0f}" stroke="#f0e8d8" stroke-width="2" fill="none" opacity=".6"/>')
            for _ in range(10): o.append(f'<circle cx="{x+r.uniform(5,s-5):.0f}" cy="{y+r.uniform(5,s-5):.0f}" r="{r.uniform(1,3):.1f}" fill="{r.choice(["#8a6a4a","#a08060","#6a5040"])}" opacity=".6"/>')
            if r.random() < 0.18: cx_, cy_ = r.choice([(x + 3, y + 3), (x + s - 3, y + 3), (x + 3, y + s - 3), (x + s - 3, y + s - 3)]); o.append(f'<polygon points="{poly(r, cx_, cy_, 10, 10, 6, 0.5)}" fill="#8a7a64"/>')
            if r.random() < 0.08: o.append(crack(r, x + s * 0.2, y + s * r.uniform(0.2, 0.8), 5, s / 6, '#3a3028', 2.0, 0.7, r.uniform(-0.5, 0.5)))
    o.append(blot(r, W, H, 160, ['#3a2e24', '#5a4a3a', '#2a2420', '#8a7a5a'], 0.05 * k, 0.4 * k, (0.05, 0.13)))
    o.append(f'<ellipse cx="{W*0.55:.0f}" cy="{H*0.15:.0f}" rx="{0.5*k:.0f}" ry="{1.4*k:.0f}" fill="#4a3e30" opacity=".12"/>')    # worn path to the door (top = far wall)
    for _ in range(40):                                      # flecks of dust, hair, a coin, a bottle cap
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<path d="M{x:.0f},{y:.0f}q{r.uniform(-15,15):.0f},{r.uniform(-15,15):.0f} {r.uniform(-25,25):.0f},{r.uniform(-25,25):.0f}" stroke="#2a2420" stroke-width="1.5" fill="none" opacity=".5"/>')
    return svg(W, H, ''.join(o))

def ceiling(seed=13, wm=3.2, dm=4.0, W=1024):
    """Gypsum board 0.6 x 1.2 m panels, sagging seams, water rings, mould spots, fly dirt around the bulb."""
    r = R(seed); k = W / wm; H = int(dm * k); o = ['<defs><filter id="cb"><feGaussianBlur stdDeviation="12"/></filter><filter id="cc"><feGaussianBlur stdDeviation="1.5"/></filter></defs>', f'<rect width="{W}" height="{H}" fill="#e2ddd0"/>', blot(r, W, H, 80, ['#a89a80', '#ffffff', '#8a8a70'], 0.1 * k, 0.5 * k, (0.04, 0.1))]
    for i in range(1, int(wm / 0.6) + 1): o.append(f'<path d="M{i*0.6*k:.0f},0V{H}" stroke="#9a9484" stroke-width="5"/>')
    for j in range(1, int(dm / 1.2) + 1): o.append(f'<path d="M0,{j*1.2*k:.0f}H{W}" stroke="#9a9484" stroke-width="5"/>')
    for _ in range(4):
        cx, cy = r.uniform(0, W), r.uniform(0, H); rr = r.uniform(0.2, 0.6) * k
        o.append(f'<polygon points="{poly(r, cx, cy, rr*0.95, rr*0.75, 22, 0.15)}" fill="#a08a5a" opacity=".22" filter="url(#cb)"/>')
        for j in range(2): o.append(f'<polygon points="{poly(r, cx, cy, rr*(1-j*0.3), rr*(0.8-j*0.25), 26, 0.1)}" fill="none" stroke="#8a6a3a" stroke-width="{4-j}" opacity=".35" filter="url(#cc)"/>')
    for _ in range(120): o.append(f'<circle cx="{r.gauss(W*0.5, 0.3*k):.0f}" cy="{r.gauss(H*0.5, 0.3*k):.0f}" r="{r.uniform(1,2.5):.1f}" fill="#2a2420" opacity=".6"/>')
    for _ in range(30): o.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,H):.0f}" r="{r.uniform(2,6):.1f}" fill="#3a4a2a" opacity=".35"/>')
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- the door (0.78 x 1.98 m), both faces
def door(face='in', W=320, H=812):
    """Cheap wooden flush door, worn varnish. 'in': chain-lock plate, peephole, yantra sticker, calendar ghost, scuffs at kick height.
    'out': room number 206, a padlock hasp shadow, stickers of a water-delivery man and a Buddhist talisman, door-to-door flyers."""
    r = R(21 if face == 'in' else 22); k = W / 0.78; Z = lambda z: (1.98 - z) * k
    o = [f'<rect width="{W}" height="{H}" fill="#8a5a34"/>']
    for i in range(14):                                    # veneer grain
        x = i * W / 14 + r.uniform(-4, 4); o.append(f'<path d="M{x:.0f},0C{x+r.uniform(-12,12):.0f},{H*0.3:.0f} {x+r.uniform(-12,12):.0f},{H*0.6:.0f} {x+r.uniform(-6,6):.0f},{H}" stroke="#5a3418" stroke-width="{r.uniform(2,5):.1f}" fill="none" opacity=".45"/>')
    for _ in range(10):
        x, y = r.uniform(20, W - 20), r.uniform(20, H - 20); o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6,14):.0f}" ry="{r.uniform(18,40):.0f}" fill="none" stroke="#4a2a12" stroke-width="2" opacity=".4"/>')
    o.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#5a3418" stroke-width="5" opacity=".6"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#3a2010" stroke-width="10"/>')
    o.append(blot(r, W, H, 50, ['#2a1a0a', '#c8a070', '#1a1008'], 8, 40, (0.06, 0.18)))
    o.append(f'<rect x="0" y="{Z(0.35):.0f}" width="{W}" height="{0.35*k:.0f}" fill="#2a1a0a" opacity=".25"/>')
    for _ in range(14): x = r.uniform(10, W - 10); o.append(f'<path d="M{x:.0f},{Z(r.uniform(0.05,0.35)):.0f}l{r.uniform(-20,20):.0f},{r.uniform(-4,4):.0f}" stroke="#c8a888" stroke-width="3" opacity=".6"/>')
    hx = W - 0.09 * k if face == 'in' else 0.09 * k                 # handle side (the free edge) as seen from this face
    o.append(f'<ellipse cx="{hx:.0f}" cy="{Z(1.0):.0f}" rx="{0.07*k:.0f}" ry="{0.16*k:.0f}" fill="#1a0e06" opacity=".35"/>')   # hand grime
    if face == 'in':
        o.append(f'<rect x="{W/2-0.12*k:.0f}" y="{Z(1.9):.0f}" width="{0.24*k:.0f}" height="{0.2*k:.0f}" fill="#f4e8c0"/>'                       # yantra paper
                 f'<rect x="{W/2-0.11*k:.0f}" y="{Z(1.89):.0f}" width="{0.22*k:.0f}" height="{0.18*k:.0f}" fill="none" stroke="#c8281e" stroke-width="3"/>')
        for i in range(5): o.append(f'<path d="M{W/2-0.08*k+i*0.04*k:.0f},{Z(1.86):.0f}v{0.12*k:.0f}" stroke="#c8281e" stroke-width="2"/>')
        o.append(f'<circle cx="{W/2:.0f}" cy="{Z(1.78):.0f}" r="{0.03*k:.0f}" fill="none" stroke="#c8281e" stroke-width="3"/>')
        o.append(f'<rect x="{0.12*k:.0f}" y="{Z(1.35):.0f}" width="{0.25*k:.0f}" height="{0.35*k:.0f}" fill="#000" opacity=".08"/>')     # ghost of a calendar
        o.append(f'<rect x="{0.15*k:.0f}" y="{Z(1.25):.0f}" width="{0.22*k:.0f}" height="{0.14*k:.0f}" fill="#fff8d8" transform="rotate(-4 {0.2*k:.0f} {Z(1.2):.0f})"/>'
                 + T(0.26 * k, Z(1.17), 0.035 * k, 'ค่าห้อง 3,200', '#1a3a9a', hw=True, rot=-4) + T(0.26 * k, Z(1.13), 0.03 * k, 'จ่ายภายในวันที่ 5', '#c8281e', hw=True, rot=-4))
    else:
        o.append(f'<rect x="{W/2-0.11*k:.0f}" y="{Z(1.72):.0f}" width="{0.22*k:.0f}" height="{0.11*k:.0f}" rx="6" fill="#d8c070" stroke="#5a4a20" stroke-width="3"/>' + T(W / 2, Z(1.635), 0.085 * k, '206', '#2a1a0a', k=True))
        o.append(f'<rect x="{W*0.62:.0f}" y="{Z(1.38):.0f}" width="{0.13*k:.0f}" height="{0.09*k:.0f}" fill="#2a8ad0"/>' + T(W * 0.62 + 0.065 * k, Z(1.315), 0.03 * k, 'น้ำดื่ม', '#fff', k=True))
        o.append(f'<rect x="{W*0.2:.0f}" y="{Z(1.3):.0f}" width="{0.12*k:.0f}" height="{0.12*k:.0f}" fill="#f0d040"/><circle cx="{W*0.2+0.06*k:.0f}" cy="{Z(1.24):.0f}" r="{0.035*k:.0f}" fill="#c8281e"/>')
        for i in range(3):
            y = Z(0.95) + i * 26; o.append(f'<rect x="{W*0.25+i*10:.0f}" y="{y:.0f}" width="{0.2*k:.0f}" height="{0.1*k:.0f}" fill="{r.choice(["#fff","#f4c0c0","#c0e0f4"])}" transform="rotate({r.uniform(-12,12):.0f} {W*0.3:.0f} {y:.0f})"/>')
    return svg(W, H, ''.join(o), font=True)

def other_doors(W=960, H=812):
    """Three neighbours' doors (each 320 x 812 = 0.78 x 1.98 m): steel-grille + wood, green painted wood, blue steel."""
    r = R(31); o = []; k = 320 / 0.78
    for i, (base, num, kind) in enumerate((('#7a4a2a', '204', 'grille'), ('#3a7a5a', '205', 'plain'), ('#3a5a8a', '207', 'steel'))):
        x = i * 320; o.append(f'<rect x="{x}" y="0" width="320" height="{H}" fill="{base}"/>')
        for _ in range(30):
            cx, cy = x + r.uniform(10, 310), r.uniform(10, H - 10); a = r.uniform(8, 40)
            o.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{a:.0f}" ry="{a*0.5:.0f}" fill="{r.choice(["#1a1a1a","#ffffff","#5a3a1a"])}" opacity="{r.uniform(.04,.14):.2f}"/>')
        if kind == 'grille':
            for j in range(9): o.append(f'<path d="M{x+20+j*35},20V{H-20}" stroke="#1e1e20" stroke-width="9"/>')
            for j in range(5): o.append(f'<path d="M{x+20},{20+j*190}H{x+300}" stroke="#1e1e20" stroke-width="9"/>')
        elif kind == 'steel':
            for j in range(3): o.append(f'<rect x="{x+30}" y="{40+j*250}" width="260" height="210" fill="none" stroke="#24406a" stroke-width="10"/>')
        else:
            o.append(f'<rect x="{x+30}" y="40" width="260" height="330" fill="none" stroke="#24543e" stroke-width="10"/><rect x="{x+30}" y="430" width="260" height="330" fill="none" stroke="#24543e" stroke-width="10"/>')
        o.append(f'<rect x="{x+110}" y="70" width="100" height="50" rx="5" fill="#e8e0c8" stroke="#3a3a3a" stroke-width="3"/>' + T(x + 160, 110, 40, num, '#1a1a1a', k=True))
        o.append(f'<rect x="{x}" y="{H-120}" width="320" height="120" fill="#1a1a10" opacity=".3"/><rect x="{x}" y="0" width="320" height="{H}" fill="none" stroke="#1a1a1a" stroke-width="10"/>')
        if i == 1: o.append(f'<rect x="{x+60}" y="420" width="90" height="120" fill="#c8281e"/>' + T(x + 105, 470, 22, 'ตรุษจีน', '#f0d040', k=True) + T(x + 105, 510, 30, 'ฝุ', '#f0d040', k=True))
    return svg(W, H, ''.join(o), font=True)

# ----------------------------------------------------------------------------- soft furnishings
def mattress(W=1024, H=512):
    """Thin foam mattress (1.0 x 2.0 m, top), faded pink-floral cotton cover, sweat stains, a cigarette burn, worn piping."""
    r = R(41); o = [f'<rect width="{W}" height="{H}" fill="#d88a8a"/>']
    for i in range(0, W, 64):
        for j in range(0, H, 64):
            cx, cy = i + 32 + (16 if (j // 64) % 2 else 0), j + 32
            o.append(f'<g transform="translate({cx},{cy})"><circle r="16" fill="#f4d0b0"/>' + ''.join(f'<ellipse cx="{math.cos(a)*14:.0f}" cy="{math.sin(a)*14:.0f}" rx="9" ry="6" fill="#c8504a" transform="rotate({math.degrees(a):.0f} {math.cos(a)*14:.0f} {math.sin(a)*14:.0f})"/>' for a in [t * 1.2566 for t in range(5)]) + '<circle r="5" fill="#f0c030"/></g>')
            o.append(f'<path d="M{cx+20},{cy+10}q14,10 26,0" stroke="#4a8a5a" stroke-width="5" fill="none"/>')
    for x in (W / 3, 2 * W / 3): o.append(f'<path d="M{x:.0f},0V{H}" stroke="#8a4a4a" stroke-width="6" opacity=".5"/>')
    o.append(blot(r, W, H, 25, ['#8a6a3a', '#6a4a2a'], 30, 120, (0.12, 0.25)))
    o.append(f'<ellipse cx="{W*0.3:.0f}" cy="{H*0.55:.0f}" rx="200" ry="120" fill="#7a5a3a" opacity=".2"/>')                         # body hollow
    o.append(f'<circle cx="{W*0.7:.0f}" cy="{H*0.3:.0f}" r="9" fill="#2a1a0a"/><circle cx="{W*0.7:.0f}" cy="{H*0.3:.0f}" r="16" fill="none" stroke="#5a3a1a" stroke-width="5"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="none" stroke="#a85a5a" stroke-width="18"/>')
    return svg(W, H, ''.join(o))

def blanket(W=512):
    """Thin plaid acrylic blanket (ผ้าห่มลายสก็อต), blue-green-red, 1 m tile."""
    r = R(43); o = [f'<rect width="{W}" height="{W}" fill="#2a4a7a"/>']
    for (c, w, sp, op) in (('#3a7a5a', 60, 128, .7), ('#c8302a', 14, 128, .85), ('#f0d070', 5, 64, .7), ('#1a2a4a', 30, 128, .6)):
        for i in range(0, W, sp):
            o.append(f'<rect x="{i+r.uniform(0,4):.0f}" y="0" width="{w}" height="{W}" fill="{c}" opacity="{op*0.6:.2f}"/><rect x="0" y="{i+r.uniform(0,4):.0f}" width="{W}" height="{w}" fill="{c}" opacity="{op*0.6:.2f}"/>')
    for i in range(0, W, 6): o.append(f'<path d="M{i},0V{W}" stroke="#000" stroke-width="1" opacity=".08"/>')
    o.append(blot(r, W, W, 20, ['#1a1a2a', '#ffffff'], 20, 70, (0.05, 0.12)))
    return svg(W, W, ''.join(o))

def pillow(W=512, H=256):
    r = R(45); o = [f'<rect width="{W}" height="{H}" fill="#e8e4f0"/>']
    for i in range(0, W, 40): o.append(f'<path d="M{i},0V{H}" stroke="#7a9ad8" stroke-width="12" opacity=".6"/>')
    o.append(f'<g transform="translate({W*0.6:.0f},{H*0.5:.0f})"><circle r="44" fill="#f0c030"/><circle cx="-14" cy="-8" r="6" fill="#1a1a1a"/><circle cx="14" cy="-8" r="6" fill="#1a1a1a"/><path d="M-18,14q18,16 36,0" stroke="#1a1a1a" stroke-width="5" fill="none"/></g>')
    o.append(f'<ellipse cx="{W*0.4:.0f}" cy="{H*0.5:.0f}" rx="160" ry="80" fill="#a89060" opacity=".25"/>')
    o.append(blot(r, W, H, 12, ['#8a7a5a'], 20, 60, (0.08, 0.2)))
    return svg(W, H, ''.join(o))

def wardrobe(W=512, H=880):
    """Zip-up canvas wardrobe front (0.85 x 1.45 m): faded print of cartoon bears, half-open zip showing clothes, sagging."""
    r = R(47); o = [f'<rect width="{W}" height="{H}" fill="#9ab8d8"/>']
    for i in range(0, W, 110):
        for j in range(0, H, 120):
            cx, cy = i + 55 + (30 if (j // 120) % 2 else 0), j + 60
            o.append(f'<g transform="translate({cx},{cy})" opacity=".7"><circle r="26" fill="#e8c8a0"/><circle cx="-20" cy="-20" r="10" fill="#e8c8a0"/><circle cx="20" cy="-20" r="10" fill="#e8c8a0"/>'
                     f'<circle cx="-8" cy="-4" r="3" fill="#2a2a2a"/><circle cx="8" cy="-4" r="3" fill="#2a2a2a"/><ellipse cy="8" rx="7" ry="5" fill="#a87a5a"/></g>')
            o.append(f'<path d="M{cx+30},{cy+40}l8,-8l8,8l-8,8z" fill="#f0f0f8" opacity=".7"/>')
    o.append(f'<path d="M{W/2},40V{H-20}" stroke="#5a6a8a" stroke-width="10"/>')
    o.append(f'<path d="M{W/2},40V{H*0.55:.0f}L{W*0.36:.0f},{H-20}H{W*0.64:.0f}L{W/2},{H*0.55:.0f}Z" fill="#2a2a34"/>')     # the open part of the zip
    for i, c in enumerate(('#1e3a6a', '#e8e4d8', '#3a3a3a', '#c8502a', '#2a5a3a')):
        x = W * 0.38 + i * 22; o.append(f'<rect x="{x:.0f}" y="{H*0.6+r.uniform(0,30):.0f}" width="20" height="{H*0.35:.0f}" fill="{c}"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="40" fill="#5a7aa0"/>' + f'<path d="M0,{H*0.5:.0f}q{W/2},40 {W},0" stroke="#000" stroke-width="3" fill="none" opacity=".15"/>')
    o.append(blot(r, W, H, 30, ['#3a4a5a', '#ffffff'], 20, 80, (0.06, 0.14)))
    return svg(W, H, ''.join(o))

def clothes(W=1024, H=512):
    """4 hanging garments on hangers (256 x 512 cells, transparent): navy work shirt with reflective tape, jeans, faded football shirt, towel."""
    r = R(49); o = []
    hang = lambda x: f'<path d="M{x+128},18q0,-14 12,-10M{x+128},22L{x+40},62H{x+216}Z" stroke="#c8c8c8" stroke-width="5" fill="none"/>'
    x = 0; o.append(hang(x) + f'<path d="M{x+40},60l60,-12q28,18 56,0l60,12l22,150l-36,8v260h-148v-260l-36,-8z" fill="#2a3a5a"/>'
                    f'<rect x="{x+54}" y="300" width="148" height="18" fill="#d8e070"/><rect x="{x+54}" y="330" width="148" height="10" fill="#c8c8c0"/>'
                    f'<path d="M{x+128},60V480" stroke="#1a2236" stroke-width="4"/>' + ''.join(f'<circle cx="{x+136}" cy="{90+i*60}" r="5" fill="#c8c8c8"/>' for i in range(6))
                    + f'<rect x="{x+150}" y="110" width="40" height="40" fill="#1e2a44"/><path d="M{x+60},400l20,-30l14,40l18,-26" stroke="#5a3a1a" stroke-width="10" fill="none" opacity=".6"/>')   # scorch holes
    x = 256; o.append(hang(x) + f'<path d="M{x+60},60h136l12,440h-62l-18,-330l-18,330h-62z" fill="#3a5a8a"/><path d="M{x+60},90h136" stroke="#2a3a5a" stroke-width="8"/>'
                      + ''.join(f'<path d="M{x+r.uniform(70,190):.0f},{r.uniform(100,480):.0f}h{r.uniform(10,30):.0f}" stroke="#8aa8c8" stroke-width="4" opacity=".7"/>' for _ in range(20)))
    x = 512; o.append(hang(x) + f'<path d="M{x+40},60l60,-12q28,18 56,0l60,12l22,110l-36,8v240h-148v-240l-36,-8z" fill="#c8302a"/><rect x="{x+60}" y="160" width="136" height="16" fill="#fff"/>'
                      + T(x + 128, 290, 90, '10', '#fff', k=True))
    x = 768; o.append(f'<path d="M{x+40},20H{x+216}" stroke="#8a8a8a" stroke-width="10"/><path d="M{x+46},20h164v300q-82,20 -164,0z" fill="#e8b830"/>'
                      + ''.join(f'<path d="M{x+46},{40+i*40}h164" stroke="#c89820" stroke-width="6"/>' for i in range(7)))
    return svg(W, H, ''.join(o), font=True)

def apron(W=384, H=640):
    """Welder's split-leather apron (0.6 x 1.0 m), transparent: scorched, burn holes, neck strap, rivets."""
    r = R(51); o = [f'<path d="M100,20h184v40q20,20 40,40v500q-130,30 -264,0v-500q20,-20 40,-40z" fill="#8a5a32" stroke="#4a2a12" stroke-width="8"/>']
    o.append(f'<path d="M100,20q92,-40 184,0" stroke="#3a2412" stroke-width="12" fill="none"/>')
    for _ in range(30):
        x, y = r.uniform(80, 300), r.uniform(80, 600); a = r.uniform(10, 50); o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{a:.0f}" ry="{a*0.6:.0f}" fill="{r.choice(["#3a2010","#b08050","#2a1a0a"])}" opacity="{r.uniform(.15,.4):.2f}"/>')
    for _ in range(9): x, y = r.uniform(90, 290), r.uniform(200, 590); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3,8):.0f}" fill="#120804"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(10,16):.0f}" fill="none" stroke="#2a1608" stroke-width="4" opacity=".6"/>')
    for (x, y) in ((70, 110), (314, 110), (70, 300), (314, 300)): o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#c8c0a8"/>')
    o.append(f'<path d="M60,300q-40,10 -55,40M324,300q40,10 55,40" stroke="#3a2412" stroke-width="10" fill="none"/>')
    o.append(f'<rect x="140" y="140" width="104" height="70" fill="#6a4020" stroke="#3a2010" stroke-width="5"/>')
    return svg(W, H, ''.join(o))

def gecko(W=192, H=192):
    o = [f'<g transform="translate(96,96) rotate(-30)"><ellipse rx="16" ry="44" fill="#c8b890"/><ellipse cy="-52" rx="13" ry="16" fill="#c8b890"/>'
         f'<circle cx="-7" cy="-58" r="3.5" fill="#1a1a1a"/><circle cx="7" cy="-58" r="3.5" fill="#1a1a1a"/>'
         f'<path d="M0,40q-10,40 14,70" stroke="#c8b890" stroke-width="10" fill="none" stroke-linecap="round"/>'
         f'<path d="M-12,-26l-26,-14l-6,-10M12,-26l26,-14l6,-10M-12,26l-26,14l-6,12M12,26l26,14l6,12" stroke="#c8b890" stroke-width="7" fill="none" stroke-linecap="round"/>'
         + ''.join(f'<circle cx="{(i%2*2-1)*5}" cy="{-30+i*10}" r="2.5" fill="#9a8a60"/>' for i in range(7)) + '</g>']
    return svg(W, H, ''.join(o))

def shoes(W=1024, H=256):
    """Top-down pairs (256 x 256 cells, transparent): blue flip-flops, cracked safety boots, pink slippers, white sneakers."""
    o = []
    def pair(x, col, strap, L=200, Wd=74, boot=False):
        s = ''
        for dx, rot in ((70, -6), (170, 8)):
            s += f'<g transform="translate({x+dx},128) rotate({rot})"><ellipse rx="{Wd/2:.0f}" ry="{L/2:.0f}" fill="{col}" stroke="#1a1a1a" stroke-width="4"/>'
            if boot: s += f'<ellipse cy="-30" rx="{Wd/2-8:.0f}" ry="44" fill="#2a1a10"/><path d="M-20,-10h40M-20,10h40M-20,30h40" stroke="#c8b070" stroke-width="5"/><ellipse cy="{L/2-30:.0f}" rx="{Wd/2-6:.0f}" ry="26" fill="#9a9aa0"/>'
            elif strap: s += f'<path d="M-{Wd/2-4:.0f},-10Q0,-70 {Wd/2-4:.0f},-10" stroke="{strap}" stroke-width="14" fill="none"/>'
            else: s += f'<path d="M-20,-40h40M-20,-20h40M-20,0h40" stroke="#c8c8c8" stroke-width="6"/><ellipse cy="{L/2-24:.0f}" rx="{Wd/2-8:.0f}" ry="20" fill="#e8e8e8"/>'
            s += '</g>'
        return s
    o.append(pair(0, '#2a6ad0', '#f0f0f0')); o.append(pair(256, '#6a4a2a', None, 230, 90, True)); o.append(pair(512, '#f0a0b0', '#e8e0e0')); o.append(pair(768, '#f0f0f0', None, 210, 80))
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- paper things
def posters(W=1536, H=724):
    """Three portrait posters (512 x 724 = 0.42 x 0.6 m): a luk-thung concert, a football team photo, a Muay Thai fight night (all fictional)."""
    r = R(61); o = []
    x = 0
    o.append(f'<rect x="{x}" y="0" width="512" height="724" fill="#f2c41e"/><rect x="{x}" y="0" width="512" height="300" fill="#c8281e"/>'
             f'<circle cx="{x+256}" cy="330" r="150" fill="#f6d0b0"/><path d="M{x+120},300q136,-200 272,0q-40,-90 -136,-100q-96,10 -136,100z" fill="#1a1a1a"/>'
             f'<circle cx="{x+206}" cy="330" r="12" fill="#1a1a1a"/><circle cx="{x+306}" cy="330" r="12" fill="#1a1a1a"/><path d="M{x+210},400q46,36 92,0" stroke="#c8281e" stroke-width="12" fill="none"/>'
             f'<path d="M{x+60},724l60,-200h272l60,200z" fill="#e83a8a"/>' + T(x + 256, 90, 64, 'คอนเสิร์ต', '#fff', k=True) + T(x + 256, 165, 56, 'ลำไย ใจสู้', '#f6d23a', k=True, stroke='#5a0a06', sw=8)
             + T(x + 256, 610, 44, 'วัดบางขุนเทียน', '#1a1a1a', k=True) + T(x + 256, 670, 38, '25 พ.ย. ฟรี!', '#c8281e', k=True))
    x = 512
    o.append(f'<rect x="{x}" y="0" width="512" height="724" fill="#1a3a8a"/><rect x="{x+20}" y="120" width="472" height="420" fill="#3a8a3a"/>')
    for row in range(2):
        for i in range(6):
            cx, cy = x + 60 + i * 78 + row * 30, 280 + row * 140
            o.append(f'<circle cx="{cx}" cy="{cy-50}" r="24" fill="#d8a878"/><rect x="{cx-26}" y="{cy-26}" width="52" height="80" rx="10" fill="#e8302a"/>' + T(cx, cy + 20, 26, str(r.randint(2, 30)), '#fff', k=True))
    o.append(T(x + 256, 80, 54, 'ธนบุรี ยูไนเต็ด', '#f6d23a', k=True) + T(x + 256, 610, 40, 'ฤดูกาล 2569', '#fff', k=True) + T(x + 256, 670, 32, 'สู้ไม่ถอย!', '#f6d23a', k=True))
    x = 1024
    o.append(f'<rect x="{x}" y="0" width="512" height="724" fill="#1a1a1a"/><path d="M{x},0L{x+512},724" stroke="#c8281e" stroke-width="140" opacity=".8"/>'
             f'<circle cx="{x+150}" cy="300" r="70" fill="#c8905a"/><circle cx="{x+362}" cy="300" r="70" fill="#8a5a3a"/><rect x="{x+90}" y="360" width="120" height="200" rx="30" fill="#c8905a"/><rect x="{x+302}" y="360" width="120" height="200" rx="30" fill="#8a5a3a"/>'
             f'<circle cx="{x+200}" cy="400" r="40" fill="#c8281e"/><circle cx="{x+312}" cy="400" r="40" fill="#1a4ac8"/>'
             + T(x + 256, 110, 70, 'มวยไทย', '#f6d23a', k=True) + T(x + 256, 190, 48, 'ศึกวันศุกร์', '#fff', k=True) + T(x + 256, 640, 40, 'เวทีราชดำเนิน', '#fff', k=True))
    o.append(blot(r, W, H, 60, ['#3a2a1a', '#ffffff'], 15, 60, (0.05, 0.14)))
    for x in (0, 512, 1024): o.append(f'<path d="M{x+30},20l40,0l-20,20z M{x+482},20l-40,0l20,20z" fill="#e8dca8" opacity=".9"/><path d="M{x},{r.uniform(300,500):.0f}l512,{r.uniform(-30,30):.0f}" stroke="#000" stroke-width="3" opacity=".12"/>')
    return svg(W, H, ''.join(o), font=True)

def calendar(W=512, H=768):
    """Shop calendar (0.42 x 0.63 m): glossy photo of a red 110 cc scooter on a beach road, month grid พฤศจิกายน 2569, the 15th circled in red."""
    r = R(63); o = [f'<rect width="{W}" height="{H}" fill="#fbfaf4"/>']
    o.append(f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a8ad8"/><stop offset="1" stop-color="#bfe4f4"/></linearGradient></defs>'
             f'<rect x="16" y="16" width="{W-32}" height="400" fill="url(#sk)"/><rect x="16" y="300" width="{W-32}" height="116" fill="#e8d098"/><path d="M16,300Q{W/2},270 {W-16},300" fill="#3a9ad8"/>')
    o.append(f'<g transform="translate({W/2-20},300)"><circle cx="-110" cy="60" r="44" fill="#1a1a1a"/><circle cx="-110" cy="60" r="22" fill="#c8c8c8"/><circle cx="120" cy="60" r="44" fill="#1a1a1a"/><circle cx="120" cy="60" r="22" fill="#c8c8c8"/>'
             f'<path d="M-150,30Q-130,-30 -40,-20L40,-20Q60,-90 90,-100L110,-100L130,40L60,40L40,10L-60,10Q-80,40 -150,30Z" fill="#d0281e"/>'
             f'<path d="M-60,-20Q-50,-50 20,-45L40,-20Z" fill="#1a1a1a"/><path d="M85,-100l20,-30h30" stroke="#1a1a1a" stroke-width="10" fill="none"/>'
             f'<path d="M-120,0Q-60,-12 0,0" stroke="#f4f0e8" stroke-width="8" fill="none"/><rect x="130" y="-70" width="18" height="12" fill="#f8f0a0"/></g>')
    o.append(T(W / 2, 60, 34, 'ร้าน เฮงเฮง มอเตอร์', '#fff', k=True, stroke='#1a1a1a', sw=6) + T(W / 2, 400, 26, 'ดาวน์ 0% ผ่อนสบาย 36 เดือน', '#c8281e', k=True))
    o.append(f'<rect x="16" y="430" width="{W-32}" height="54" fill="#c8281e"/>' + T(W / 2, 470, 34, 'พฤศจิกายน 2569', '#fff', k=True))
    days = ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส']; cw = (W - 32) / 7
    for i, d in enumerate(days): o.append(T(16 + cw * (i + 0.5), 512, 22, d, '#c8281e' if i == 0 else '#1a1a1a', k=True))
    day = 1; start = 0
    for row in range(5):
        for c in range(7):
            n = row * 7 + c - start + 1
            if 1 <= n <= 30:
                cx, cy = 16 + cw * (c + 0.5), 548 + row * 44; o.append(T(cx, cy, 26, str(n), '#c8281e' if c == 0 else '#2a2a2a'))
                if n < 14: o.append(f'<path d="M{cx-14:.0f},{cy-18}l28,22M{cx+14:.0f},{cy-18}l-28,22" stroke="#1a3a9a" stroke-width="3" opacity=".7"/>')
                if n == 15: o.append(f'<ellipse cx="{cx:.0f}" cy="{cy-8}" rx="26" ry="20" fill="none" stroke="#e8201a" stroke-width="5"/>' + T(cx + 4, cy + 14, 16, 'ผ่อน!', '#e8201a', hw=True))
    o.append(f'<circle cx="{W/2}" cy="10" r="6" fill="#3a3a3a"/>' + blot(r, W, H, 16, ['#6a5a3a'], 15, 50, (0.04, 0.1)))
    return svg(W, H, ''.join(o), font=True)

def paybook(W=1024, H=704):
    """สมุดผ่อน, open (2 pages, 0.30 x 0.21 m): table of instalments, paid stamps on 1-28, handwritten sums, a coffee ring."""
    r = R(65); o = [f'<rect width="{W}" height="{H}" fill="#f6f2e4"/><rect x="{W/2-4}" y="0" width="8" height="{H}" fill="#c8c0a8"/>']
    o.append(f'<rect x="0" y="0" width="{W/2-6:.0f}" height="90" fill="#1e5aa0"/>' + T(W / 4, 40, 30, 'สมุดผ่อนชำระ', '#fff', k=True) + T(W / 4, 76, 20, 'บ.สบายใจ ลิสซิ่ง  สัญญา 0472-118', '#d8e8ff'))
    o.append(T(W * 0.75, 50, 26, 'ตารางผ่อน งวดละ 2,890', '#1a1a1a', k=True))
    for side in range(2):
        x0 = side * W / 2 + 24; o.append(f'<path d="M{x0},{110}H{x0+W/2-48}" stroke="#1e5aa0" stroke-width="3"/>')
        for i in range(12):
            y = 140 + i * 46; n = side * 12 + i + 17
            o.append(f'<path d="M{x0},{y+16}H{x0+W/2-48}" stroke="#9ab0c8" stroke-width="2"/>' + T(x0 + 24, y + 8, 22, str(n), '#2a2a2a') + T(x0 + 130, y + 8, 20, f'15/{(n % 12) + 1:02d}/{68 + (n + 3) // 12}', '#5a5a5a') + T(x0 + 300, y + 8, 22, '2,890', '#2a2a2a'))
            if n <= 28:
                o.append(f'<g transform="rotate({r.uniform(-14,14):.0f} {x0+410:.0f} {y:.0f})"><rect x="{x0+360:.0f}" y="{y-14:.0f}" width="100" height="30" rx="4" fill="none" stroke="#1a3ac8" stroke-width="3" opacity=".75"/>' + T(x0 + 410, y + 8, 18, 'ชำระแล้ว', '#1a3ac8', k=True, op=.75) + '</g>')
            elif n == 29: o.append(T(x0 + 410, y + 8, 22, 'ค้าง!!', '#e8201a', hw=True, rot=-6))
    o.append(T(W * 0.78, H - 60, 30, '2,890 x 8 = 23,120', '#1a3a9a', hw=True, rot=-3) + f'<path d="M{W*0.62:.0f},{H-40:.0f}q120,14 300,-10" stroke="#1a3a9a" stroke-width="3" fill="none"/>')
    o.append(f'<ellipse cx="{W*0.3:.0f}" cy="{H*0.75:.0f}" rx="80" ry="70" fill="none" stroke="#8a5a2a" stroke-width="12" opacity=".3"/>')
    o.append(blot(r, W, H, 20, ['#6a5a3a'], 10, 40, (0.03, 0.08)))
    return svg(W, H, ''.join(o), font=True)

def calculator(W=192, H=288):
    o = [f'<rect width="{W}" height="{H}" rx="14" fill="#2a2a30"/><rect x="16" y="18" width="{W-32}" height="56" fill="#a8b89a"/>' + T(W - 24, 62, 36, '23120', '#1a2a1a', 'end')]
    cols = ['#5a5a64', '#5a5a64', '#5a5a64', '#e8702a']
    for i in range(5):
        for j in range(4): o.append(f'<rect x="{16+j*42}" y="{92+i*38}" width="34" height="28" rx="5" fill="{cols[j] if i else "#c8c8d0"}"/>')
    return svg(W, H, ''.join(o))

def cup(W=512, H=160):
    """Instant-noodle cup wrap (fictional 'ซดซด' brand), red with a steaming bowl and a chilli."""
    o = [f'<rect width="{W}" height="{H}" fill="#e8281e"/><rect x="0" y="{H-28}" width="{W}" height="28" fill="#f6d23a"/>']
    for x in (100, 356):
        o.append(T(x, 70, 52, 'ซดซด', '#fff', k=True, stroke='#7a0a06', sw=8) + T(x, 108, 22, 'รสต้มยำกุ้ง', '#f6d23a', k=True))
        o.append(f'<ellipse cx="{x+110}" cy="80" rx="40" ry="16" fill="#f4e8c8"/><path d="M{x+80},70q30,20 60,0" stroke="#f0a020" stroke-width="5" fill="none"/>')
    return svg(W, H, ''.join(o), font=True)

def tv_front(W=384, H=320):
    """Old 14-inch CRT front (0.42 x 0.35 m): screen off, dusty, a curved reflection of the bulb, sticker of a remote-control shop."""
    o = [f'<rect width="{W}" height="{H}" fill="#3a3a3e"/><rect x="24" y="22" width="{W-110}" height="{H-60}" rx="30" fill="#1a2024"/>'
         f'<path d="M50,60q60,-24 120,-10" stroke="#8aa0a8" stroke-width="10" fill="none" opacity=".4"/><ellipse cx="{(W-86)/2:.0f}" cy="{H/2-20:.0f}" rx="100" ry="70" fill="#2a3a40" opacity=".5"/>']
    for i in range(6): o.append(f'<circle cx="{W-50}" cy="{50+i*30}" r="9" fill="#5a5a60"/>')
    o.append(f'<rect x="{W-74}" y="{H-70}" width="48" height="20" fill="#1a1a1a"/>' + T(W / 2 - 40, H - 14, 22, 'SANWA', '#c8c8c8', k=True))
    return svg(W, H, ''.join(o), font=True)

def mask(W=256, H=320):
    """Welding helmet front (dark green fibreglass, lens window, scratched stickers)."""
    r = R(67); o = [f'<rect width="{W}" height="{H}" fill="#2a3a2e"/><rect x="58" y="110" width="140" height="62" rx="6" fill="#0e140e" stroke="#5a5a5a" stroke-width="8"/>'
                    f'<path d="M80,124h60" stroke="#3a6a5a" stroke-width="6" opacity=".7"/><rect x="40" y="220" width="70" height="40" fill="#e8b830" transform="rotate(-8 75 240)"/>' + T(75, 248, 22, 'ไฟ!', '#c8281e', k=True, rot=-8)]
    o.append(blot(r, W, H, 30, ['#5a6a5a', '#1a1a1a', '#8a6a3a'], 10, 40, (0.1, 0.3)))
    for _ in range(20): x, y = r.uniform(10, W - 10), r.uniform(10, H - 10); o.append(f'<path d="M{x:.0f},{y:.0f}l{r.uniform(-30,30):.0f},{r.uniform(-8,8):.0f}" stroke="#8a9a8a" stroke-width="2" opacity=".5"/>')
    return svg(W, H, ''.join(o), font=True)

def notice(W=512, H=724):
    """Landlord's rules (A4, 0.21 x 0.30 m), yellowed, taped; plus a list of meter readings scribbled at the bottom."""
    r = R(81); o = [f'<rect width="{W}" height="{H}" fill="#f2ecd6"/>', T(W / 2, 64, 40, 'ระเบียบหอพัก ร่วมใจ', '#1a1a1a', k=True), f'<path d="M30,84H{W-30}" stroke="#1a1a1a" stroke-width="3"/>']
    rules = ['1. ชำระค่าห้องภายในวันที่ 5', '2. ค่าไฟหน่วยละ 8 บาท', '3. ห้ามเลี้ยงสัตว์', '4. ห้ามส่งเสียงดังหลัง 4 ทุ่ม', '5. ห้ามตอกตะปูผนัง', '6. ทิ้งขยะที่ชั้นล่างเท่านั้น', '7. แขกค้างคืนแจ้งเจ้าของ']
    for i, t in enumerate(rules): o.append(T(36, 140 + i * 50, 28, t, '#1a1a1a', 'start'))
    o.append(T(W - 40, 520, 26, 'เจ้าของหอ ป้าศรี โทร 081-224-5017', '#c8281e', 'end'))
    for i in range(4): o.append(T(60, 590 + i * 34, 26, f'{["ก.ย.", "ต.ค.", "พ.ย.", ""][i]} {["1820", "1913", "2011", ""][i]}', '#1a3a9a', 'start', hw=True))
    o.append(f'<path d="M0,0h70l-70,40z M{W},0h-70l70,40z" fill="#e8dca8" opacity=".9"/>' + blot(r, W, H, 20, ['#8a6a3a'], 15, 50, (0.05, 0.14)))
    return svg(W, H, ''.join(o), font=True)

def bag(W=256, H=256):
    """White plastic shop bag print (fictional 'ซื้อดี')."""
    o = [f'<rect width="{W}" height="{H}" fill="#f0f0ec"/><circle cx="{W/2}" cy="{H*0.45:.0f}" r="56" fill="#1e8a4a"/>' + T(W / 2, H * 0.5, 34, 'ซื้อดี', '#fff', k=True) + T(W / 2, H * 0.8, 22, 'ขอบคุณที่ใช้บริการ', '#c8281e')]
    for i in range(6): o.append(f'<path d="M{20+i*40},0q10,{H/2:.0f} 0,{H}" stroke="#c8c8c0" stroke-width="3" fill="none"/>')
    return svg(W, H, ''.join(o), font=True)

def drawers(W=256, H=384):
    """Front of a 3-drawer translucent plastic cabinet (0.4 x 0.6 m): blue fronts with silhouettes of the stuff inside."""
    r = R(83); o = [f'<rect width="{W}" height="{H}" fill="#e8ecf0"/>']
    for i in range(3):
        y = 10 + i * 124; o.append(f'<rect x="12" y="{y}" width="{W-24}" height="112" rx="6" fill="#7ab0e0"/>')
        for _ in range(6): o.append(f'<rect x="{r.uniform(20,200):.0f}" y="{y+r.uniform(10,70):.0f}" width="{r.uniform(20,60):.0f}" height="{r.uniform(15,40):.0f}" fill="{r.choice(["#3a5a8a","#5a7aa8","#e8e8f0","#c86a6a"])}" opacity=".6"/>')
        o.append(f'<rect x="{W/2-30:.0f}" y="{y+8}" width="60" height="14" rx="7" fill="#2a4a7a"/>')
    return svg(W, H, ''.join(o))

def yantra(W=512, H=360):
    """ผ้ายันต์ (0.5 x 0.35 m) pinned above the door: off-white cloth, red ink grid, Buddha figure, script, scalloped edge."""
    r = R(85); o = [f'<rect width="{W}" height="{H}" fill="#f0e6cc"/><rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#b81e14" stroke-width="6"/>']
    o.append(f'<path d="M{W/2},40L{W-60},{H/2}L{W/2},{H-40}L60,{H/2}Z" fill="none" stroke="#b81e14" stroke-width="5"/>')
    for i in range(1, 4): o.append(f'<path d="M{60+i*(W-120)/4:.0f},40V{H-40}M60,{40+i*(H-80)/4:.0f}H{W-60}" stroke="#b81e14" stroke-width="2.5" opacity=".8"/>')
    o.append(f'<circle cx="{W/2}" cy="{H/2-10}" r="30" fill="none" stroke="#b81e14" stroke-width="5"/><path d="M{W/2-26},{H/2+30}q26,-30 52,0z" fill="#b81e14"/><circle cx="{W/2}" cy="{H/2-12}" r="10" fill="#b81e14"/>')
    for i in range(16): o.append(T(40 + (i % 8) * 62, 34 if i < 8 else H - 18, 22, r.choice(['นะ', 'โม', 'พุท', 'ธา', 'ยะ', 'อะ', 'อุ', 'มะ']), '#b81e14'))
    o.append(blot(r, W, H, 20, ['#8a6a3a', '#3a2a1a'], 10, 40, (0.05, 0.14)))
    return svg(W, H, ''.join(o), font=True)

def photos(W=768, H=256):
    """Three snapshots (256 x 256): mum and dad in front of a wooden house up-country, the welder with workmates at a site, the new red scooter."""
    r = R(87); o = []
    for i in range(3):
        x = i * 256; o.append(f'<rect x="{x+8}" y="8" width="240" height="240" fill="#f8f6f0"/>')
        bg = ['#7ab0d8', '#d8c090', '#8ac0e0'][i]; o.append(f'<rect x="{x+20}" y="20" width="216" height="180" fill="{bg}"/>')
        if i == 0:
            o.append(f'<rect x="{x+40}" y="80" width="170" height="100" fill="#8a5a34"/><path d="M{x+30},84l95,-50l95,50z" fill="#6a3a24"/>')
            for k, c in enumerate(('#2a5ab0', '#c8504a')): o.append(f'<circle cx="{x+95+k*60}" cy="140" r="16" fill="#c8905a"/><rect x="{x+80+k*60}" y="156" width="30" height="44" fill="{c}"/>')
        elif i == 1:
            for k in range(4): o.append(f'<circle cx="{x+50+k*50}" cy="110" r="16" fill="#b8804a"/><rect x="{x+34+k*50}" y="126" width="32" height="74" fill="{["#2a3a5a","#e8b020","#2a3a5a","#c8302a"][k]}"/>')
            o.append(f'<path d="M{x+20},60h216M{x+20},90h216" stroke="#5a5a5a" stroke-width="5"/>')
        else:
            o.append(f'<circle cx="{x+80}" cy="170" r="22" fill="#1a1a1a"/><circle cx="{x+180}" cy="170" r="22" fill="#1a1a1a"/><path d="M{x+60},160q20,-50 70,-40h40l20,-30h14l6,70h-150z" fill="#d0281e"/>')
        o.append(T(x + 128, 232, 22, ['บ้านอุดร', 'ไซต์งาน 66', 'รถคันใหม่!'][i], '#3a3a9a', hw=True))
    return svg(W, H, ''.join(o), font=True)

# ----------------------------------------------------------------------------- grille, screen, outside
def grille(W=512, H=512):
    """Window grille (1.1 x 1.1 m), transparent: white-painted flat bar, sunburst + square grid, rust at the welds."""
    r = R(71); s = 'stroke="#e8e6dc" fill="none" stroke-width="12" stroke-linecap="round"'; d = [f'M6,6H{W-6}V{H-6}H6Z']
    for i in range(1, 5): d.append(f'M{i*W/5:.0f},0V{H}')
    for j in (H * 0.35, H * 0.7): d.append(f'M0,{j:.0f}H{W}')
    cx, cy = W / 2, H * 0.35
    for a in range(0, 181, 22): t = math.radians(a); d.append(f'M{cx:.0f},{cy:.0f}l{math.cos(t)*W*0.32:.0f},{-math.sin(t)*W*0.32:.0f}')
    d.append(f'M{cx-80:.0f},{cy:.0f}A80,80 0 0 1 {cx+80:.0f},{cy:.0f}')
    for i in range(5): d.append(f'M{(i+0.5)*W/5-26:.0f},{H*0.85:.0f}a26,26 0 1 0 52,0a26,26 0 1 0 -52,0')
    p = ''.join(d)
    o = [f'<path d="{p}" stroke="#000" fill="none" stroke-width="12" opacity=".3" transform="translate(4,5)"/>', f'<path d="{p}" {s}/>']
    for _ in range(18): x, y = r.choice([W / 5, 2 * W / 5, 3 * W / 5, 4 * W / 5]), r.choice([H * 0.35, H * 0.7, 6, H - 6]); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(5,10):.0f}" fill="#8a4a1a" opacity=".8"/>')
    return svg(W, H, ''.join(o))

def screen(W=256, H=256):
    """Mosquito screen (fibreglass mesh, alpha ~0.35) with a torn corner patched with tape."""
    o = [f'<rect width="{W}" height="{H}" fill="#3a4044" opacity=".38"/>']
    for i in range(0, W, 6): o.append(f'<path d="M{i},0V{H}M0,{i}H{W}" stroke="#20262a" stroke-width="1.5" opacity=".5"/>')
    o.append(f'<path d="M{W-70},{H}L{W},{H-90}V{H}Z" fill="#000" opacity="0"/>')
    return svg(W, H, ''.join(o).replace(f'<path d="M{W-70},{H}L{W},{H-90}V{H}Z" fill="#000" opacity="0"/>', '')
               + f'<rect x="{W*0.62:.0f}" y="{H*0.66:.0f}" width="60" height="16" fill="#e8dca8" opacity=".9" transform="rotate(-30 {W*0.7:.0f} {H*0.7:.0f})"/>')

def city_window(W=1024, H=1024):
    """What the room window sees (camera-only backdrop on the plane x = 4.6, y 8 .. -1 left to right, z -3 .. 6): the neighbour's wall
    3 m away (top at z 4.2, night sky above) lit by a teal karaoke neon (y 3.1..5.7, z 0.95..1.95, where room_wide and fist_close look
    through the window), an orange massage sign, a lit window, AC compressors, pipes, cables. Display colours (camera-only emission)."""
    r = R(73); k = W / 9.0; U = lambda y: (8.0 - y) * k; V = lambda z: (6.0 - z) * k
    o = ['<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16163a"/><stop offset="1" stop-color="#4a3a68"/></linearGradient>'
         '<radialGradient id="n" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3ae0d4" stop-opacity=".6"/><stop offset="1" stop-color="#3ae0d4" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="o" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff8a3a" stop-opacity=".55"/><stop offset="1" stop-color="#ff8a3a" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{V(4.2):.0f}" fill="url(#g)"/>']
    for _ in range(40): o.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,V(4.4)):.0f}" r="{r.uniform(1,2.4):.1f}" fill="#fff" opacity="{r.uniform(.2,.6):.2f}"/>')
    o.append(f'<path d="M{U(7):.0f},{V(4.2):.0f}l40,-60h90l30,60z" fill="#1e1c34"/><rect x="{U(2.5):.0f}" y="{V(5.2):.0f}" width="70" height="{1.0*k:.0f}" fill="#22203a"/>')   # roof shack, water tank
    o.append(f'<rect x="0" y="{V(4.2):.0f}" width="{W}" height="{H-V(4.2):.0f}" fill="#2a2e44"/>')                         # the neighbour's wall
    o.append(blot(r, W, H, 70, ['#11131e', '#3e425c', '#262a3c'], 15, 80, (0.12, 0.3)))
    for z in (0.6, 3.6): o.append(f'<rect x="0" y="{V(z):.0f}" width="{W}" height="{0.16*k:.0f}" fill="#20233a"/>')
    for _ in range(8): o.append(crack(r, r.uniform(0, W), r.uniform(V(4), V(-2)), 8, 18, '#14162a', 2.5, 0.8))
    o.append(f'<ellipse cx="{U(4.4):.0f}" cy="{V(1.2):.0f}" rx="{3.6*k:.0f}" ry="{2.4*k:.0f}" fill="url(#n)"/><ellipse cx="{U(6.2):.0f}" cy="{V(2.7):.0f}" rx="{1.8*k:.0f}" ry="{1.4*k:.0f}" fill="url(#o)"/>')
    o.append(f'<rect x="{U(5.7):.0f}" y="{V(1.95):.0f}" width="{2.6*k:.0f}" height="{1.0*k:.0f}" rx="16" fill="#0c1a1c" stroke="#56fff0" stroke-width="9"/>'
             + T(U(4.4), V(1.22), 0.62 * k, 'คาราโอเกะ', '#c8fff8', k=True, stroke='#22d8cc', sw=7)
             + f'<path d="M{U(5.55):.0f},{V(1.85):.0f}h{2.3*k:.0f}" stroke="#ff5aa0" stroke-width="5" opacity=".0"/>')
    for i in range(7): o.append(f'<circle cx="{U(5.55)+i*0.37*k:.0f}" cy="{V(1.86):.0f}" r="6" fill="#ffe070"/>')               # bulb chaser
    o.append(f'<rect x="{U(6.6):.0f}" y="{V(3.0):.0f}" width="{0.8*k:.0f}" height="{0.6*k:.0f}" fill="#2a1408" stroke="#ff8a3a" stroke-width="7"/>' + T(U(6.2), V(2.55), 0.38 * k, 'นวด', '#ffd0a0', k=True))
    o.append(f'<rect x="{U(3.4):.0f}" y="{V(3.35):.0f}" width="{0.6*k:.0f}" height="{0.75*k:.0f}" fill="#f2c26a"/><rect x="{U(3.4):.0f}" y="{V(3.35):.0f}" width="{0.22*k:.0f}" height="{0.75*k:.0f}" fill="#d8706a"/>'
             f'<path d="M{U(3.1):.0f},{V(3.35):.0f}v{0.75*k:.0f}M{U(3.4):.0f},{V(2.98):.0f}h{0.6*k:.0f}" stroke="#3a2a1a" stroke-width="7"/>')          # lit window across
    for (y, z) in ((1.9, 2.0), (6.9, 0.2), (2.4, -0.6)):
        o.append(f'<rect x="{U(y):.0f}" y="{V(z):.0f}" width="{0.75*k:.0f}" height="{0.55*k:.0f}" fill="#585c70"/><circle cx="{U(y)+0.3*k:.0f}" cy="{V(z)+0.27*k:.0f}" r="{0.2*k:.0f}" fill="#262836"/>'
                 f'<path d="M{U(y)+0.75*k:.0f},{V(z)+0.15*k:.0f}h{0.3*k:.0f}v{2.2*k:.0f}" stroke="#44485c" stroke-width="9" fill="none"/>')
    for _ in range(4): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},{V(4.2):.0f}V{H}" stroke="#34384e" stroke-width="{r.uniform(10,16):.0f}"/>')
    for _ in range(6): y0 = r.uniform(V(4.0), V(2.2)); o.append(f'<path d="M0,{y0:.0f}q{W/2:.0f},{r.uniform(20,60):.0f} {W},{r.uniform(-30,30):.0f}" stroke="#0c0c16" stroke-width="3" fill="none"/>')
    return svg(W, H, ''.join(o), font=True)

def city_far(W=2048, H=1024):
    """Beyond the corridor railing (camera-only backdrop, 40 x 20 m at ~16 m): the block across the soi with lit windows, a 7-Eleven-like
    green shop sign (fictional 'ซื้อดี 24 ชม.'), a temple roof in silhouette, purple-blue night sky with city glow."""
    r = R(75); o = ['<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14163a"/><stop offset=".35" stop-color="#2e2c5e"/><stop offset=".5" stop-color="#5a4a78"/></linearGradient></defs>',
                    f'<rect width="{W}" height="{H}" fill="url(#s)"/>']
    for _ in range(60): o.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,H*0.3):.0f}" r="{r.uniform(1,2.4):.1f}" fill="#fff" opacity="{r.uniform(.2,.7):.2f}"/>')
    o.append(f'<path d="M{W*0.12:.0f},{H*0.5:.0f}l60,-90l60,90z M{W*0.12+20:.0f},{H*0.5:.0f}l40,-60l40,60z" fill="#1c1a30"/><path d="M{W*0.12+60:.0f},{H*0.41:.0f}l0,-50" stroke="#1c1a30" stroke-width="8"/>')
    x = 0
    while x < W:                                                    # the row of buildings across
        w = r.uniform(180, 380); top = r.uniform(0.32, 0.5) * H; c = r.choice(['#2a2c46', '#30304e', '#262840', '#34324c'])
        o.append(f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{H-top:.0f}" fill="{c}"/>')
        for fy in range(int(top) + 30, H - 120, 70):
            for fx in range(int(x) + 20, int(x + w) - 40, 56):
                if r.random() < 0.5:
                    col = r.choice(['#ffd890', '#ffe8b0', '#f0b860', '#a8d8ff', '#ffd890']); o.append(f'<rect x="{fx}" y="{fy}" width="34" height="40" fill="{col}"/>')
                    if r.random() < 0.5: o.append(f'<rect x="{fx}" y="{fy}" width="{r.randint(8,20)}" height="40" fill="{r.choice(["#e07a5a","#7a9ad8","#e8c860"])}"/>')
                else: o.append(f'<rect x="{fx}" y="{fy}" width="34" height="40" fill="#1a1c2c"/>')
        if r.random() < 0.5: o.append(f'<rect x="{x+20:.0f}" y="{top-30:.0f}" width="40" height="30" fill="#3a3a5a"/>')
        x += w + r.uniform(0, 20)
    o.append(f'<rect x="0" y="{H-150}" width="{W}" height="150" fill="#1a1a2a"/>')
    o.append(f'<rect x="{W*0.42:.0f}" y="{H-150}" width="{W*0.16:.0f}" height="70" fill="#1e8a4a"/>' + T(W * 0.5, H - 100, 44, 'ซื้อดี 24 ชม.', '#fff', k=True) + f'<rect x="{W*0.42:.0f}" y="{H-80}" width="{W*0.16:.0f}" height="80" fill="#f0f8f0"/>')
    o.append(f'<rect x="{W*0.7:.0f}" y="{H-160}" width="{W*0.12:.0f}" height="60" fill="#c8281e"/>' + T(W * 0.76, H - 118, 36, 'ข้าวต้ม 24 ชม.', '#fff6c0', k=True))
    for _ in range(14): x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},{H*0.6:.0f}q{r.uniform(60,200):.0f},40 {r.uniform(150,400):.0f},{r.uniform(-20,20):.0f}" stroke="#0e0e18" stroke-width="3" fill="none"/>')
    return svg(W, H, ''.join(o), font=True)

def corr_floor(W=2048, H=256, wm=16.0, dm=2.0):
    """Corridor floor: 16 x 2 m of old green-grey terrazzo slabs (40 cm), cracked, stained by pots and drips."""
    r = R(77); k = W / wm; o = [f'<rect width="{W}" height="{H}" fill="#55605a"/>']; s = 0.4 * k
    for i in range(int(wm / 0.4) + 1):
        for j in range(int(dm / 0.4) + 1):
            o.append(f'<rect x="{i*s+2:.0f}" y="{j*s+2:.0f}" width="{s-4:.0f}" height="{s-4:.0f}" fill="{r.choice(["#9aa498","#a4ae9e","#8e9a8e","#a0a89a"])}"/>')
            for _ in range(8): o.append(f'<circle cx="{i*s+r.uniform(4,s-4):.0f}" cy="{j*s+r.uniform(4,s-4):.0f}" r="{r.uniform(1,2.5):.1f}" fill="{r.choice(["#e8e4d8","#4a5048","#6a7a6a"])}"/>')
    o.append(blot(r, W, H, 120, ['#2a2e2a', '#4a4a3a', '#6a5a3a'], 10, 60, (0.06, 0.18)))
    for _ in range(14): o.append(crack(r, r.uniform(0, W), r.uniform(0, H), 6, 14, '#2a2a26', 1.6, 0.6))
    for _ in range(10): x = r.uniform(0, W); o.append(f'<circle cx="{x:.0f}" cy="{H*0.8:.0f}" r="{r.uniform(14,22):.0f}" fill="none" stroke="#3a2a1a" stroke-width="5" opacity=".35"/>')
    return svg(W, H, ''.join(o))

def meter(W=256, H=320):
    o = [f'<rect width="{W}" height="{H}" fill="#c8c8c0"/><rect x="40" y="40" width="{W-80}" height="{H-120}" fill="#e8e8e0" stroke="#5a5a5a" stroke-width="6"/><circle cx="{W/2}" cy="130" r="50" fill="#f4f4f0" stroke="#2a2a2a" stroke-width="4"/>'
         f'<rect x="80" y="190" width="96" height="30" fill="#1a1a1a"/>' + T(W / 2, 214, 24, '04721', '#e8e8e0') + T(W / 2, H - 40, 30, '206', '#c8281e', k=True)]
    return svg(W, H, ''.join(o), font=True)

# ----------------------------------------------------------------------------- job table
JOBS = dict(
    wall_far=(lambda: wall(101, 3.2, holes=((1.25, 2.05, 0.0, 2.0),)), 1024, 832, False),
    wall_right=(lambda: wall(102, 4.0, holes=((0.9, 2.0, 0.95, 2.05),)), 1280, 832, False),
    wall_left=(lambda: wall(103, 4.0), 1280, 832, False),
    wall_near=(lambda: wall(104, 3.2), 1024, 832, False),
    wall_out=(lambda: wall(105, 16.0, holes=((3.8, 4.6, 0, 2.0), (7.55, 8.35, 0, 2.0), (11.4, 12.2, 0, 2.0)), W=2048, kind='out', base='#c8d8c8'), 2048, 332, False),
    floor=(floor, 1024, 1280, False), ceiling=(ceiling, 1024, 1280, False),
    door_in=(lambda: door('in'), 320, 812, False), door_out=(lambda: door('out'), 320, 812, False), doors=(other_doors, 960, 812, False),
    mattress=(mattress, 1024, 512, False), blanket=(blanket, 512, 512, False), pillow=(pillow, 512, 256, False),
    wardrobe=(wardrobe, 512, 880, False), clothes=(clothes, 1024, 512, True), apron=(apron, 384, 640, True), gecko=(gecko, 192, 192, True),
    shoes=(shoes, 1024, 256, True), posters=(posters, 1536, 724, False), calendar=(calendar, 512, 768, False), paybook=(paybook, 1024, 704, False),
    calc=(calculator, 192, 288, False), cup=(cup, 512, 160, False), tv=(tv_front, 384, 320, False), mask=(mask, 256, 320, False),
    grille=(grille, 512, 512, True), screen=(screen, 256, 256, True), city_win=(city_window, 1024, 1024, False), city_far=(city_far, 2048, 1024, False),
    corr_floor=(corr_floor, 2048, 256, False), meter=(meter, 256, 320, False), notice=(notice, 512, 724, False), yantra=(yantra, 512, 360, False), photos=(photos, 768, 256, False), bag=(bag, 256, 256, False), drawers=(drawers, 256, 384, False),
)

def build_all(force=False, only=None):
    os.makedirs(TEX, exist_ok=True); jobs = []; paths = {}
    for name, (fn, w, h, tr) in JOBS.items():
        if only and name not in only: continue
        s = fn(); hsh = hashlib.sha1(s.encode()).hexdigest()[:10]; png = os.path.join(TEX, f'{name}_{hsh}.png'); paths[name] = png
        if force or not os.path.exists(png):
            sp = png[:-4] + '.svg'; open(sp, 'w').write(s); jobs.append(dict(src=sp, out=png, w=w, h=h, transparent=tr))
    if jobs:
        jp = os.path.join(TEX, 'jobs.json'); json.dump(jobs, open(jp, 'w'))
        env = dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules'))
        subprocess.run(['node', RASTER, jp], check=True, capture_output=True, env=env)
        for j in jobs: os.remove(j['src'])
    return paths

if __name__ == '__main__':
    import sys, time
    t = time.time(); p = build_all(only=sys.argv[1:] or None); print(len(p), 'textures', round(time.time() - t, 1), 's')
