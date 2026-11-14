"""SVG artwork for the Thonburi soi set (soi3d.py), rasterised by Chromium (one launch for all jobs). Cached by content hash in soi_tex/.
Convention: SVG y grows downward = texture v goes from 1 (top row) to 0 (bottom row). Facade textures: x = along the wall, top = parapet."""
import os, json, hashlib, base64, subprocess, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'soi_tex')
RASTER = os.path.join(os.path.dirname(HERE), 'v3', 'set3d', 'raster.js')
FDIR = '/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/mw/hf/rig/assets/fonts/'
_B = lambda f: base64.b64encode(open(os.path.join(FDIR, f), 'rb').read()).decode()
FONT = None

def _font():
    global FONT
    if FONT is None:
        FONT = (f"<style>@font-face{{font-family:KB;src:url(data:font/ttf;base64,{_B('f2.ttf')})}}"
                f"@font-face{{font-family:KK;src:url(data:font/ttf;base64,{_B('f3.ttf')})}} text{{font-family:KB}} .k{{font-family:KK}}</style>")
    return FONT

def svg(w, h, body, font=False):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block">{_font() if font else ""}{body}</svg>'

R = random.Random
def T(x, y, s, txt, fill='#fff', anchor='middle', k=False, stroke=None, sw=0, rot=0, op=1.0, ls=0):
    st = f' stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" stroke-linejoin="round"' if stroke else ''
    tr = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ''
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{s:.0f}" fill="{fill}" text-anchor="{anchor}"{" class=\"k\"" if k else ""}{st}{tr}'
            f' opacity="{op}" letter-spacing="{ls}">{txt}</text>')

def blot(r, W, H, n, cols, rmin, rmax, op=(0.04, 0.12), sq=1.0, soft=0.35):
    """Soft stains: rotated ellipses under a Gaussian blur (hard-edged ones read as polka dots)."""
    fid = f'fb{r.randrange(10**9)}'; o = [f'<defs><filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{max(1.5, rmin * soft):.1f}"/></filter></defs><g filter="url(#{fid})">']
    for _ in range(n):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(rmin, rmax)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{a:.0f}" ry="{a*r.uniform(0.25,0.8)*sq:.0f}" fill="{r.choice(cols)}" opacity="{r.uniform(*op):.3f}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
    return ''.join(o) + '</g>'

def crack(r, x, y, n, step, col='#3a3430', w=2.0, op=0.6, ang=None):
    pts = [(x, y)]; a = ang if ang is not None else r.uniform(0, 6.28)
    for _ in range(n):
        a += r.uniform(-0.7, 0.7); x += math.cos(a) * step * r.uniform(0.5, 1.2); y += math.sin(a) * step * r.uniform(0.5, 1.2); pts.append((x, y))
    d = 'M' + 'L'.join(f'{px:.0f},{py:.0f}' for px, py in pts)
    return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}" stroke-linejoin="round"/>'

def streaks(r, x0, x1, ytop, length, k, col='#3a3028', n=10, op=(0.06, 0.18)):
    o = []
    for _ in range(n):
        x = r.uniform(x0, x1); w = r.uniform(0.04, 0.25) * k; L = length * r.uniform(0.4, 1.0)
        gid = f'g{r.randrange(10**9)}'
        o.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="{r.uniform(*op):.2f}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>'
                 f'<rect x="{x:.0f}" y="{ytop:.0f}" width="{w:.0f}" height="{L:.0f}" fill="url(#{gid})"/>')
    return ''.join(o)

# ----------------------------------------------------------------------------- ground
def road(seed, W=1024, H=4096, slow=False):
    """4.5 m x 18 m of soi concrete (227 px/m). Top of the image = far end (+y)."""
    r = R(seed); k = W / 4.5; o = [f'<defs><filter id="oil"><feGaussianBlur stdDeviation="6"/></filter></defs><rect width="{W}" height="{H}" fill="#a8a296"/>']
    slab = 4.5 * k
    for j in range(5):                              # slabs, two lanes each
        for i in range(2):
            c = r.choice(['#aca69a', '#a39d91', '#b2ac9f', '#9f998d', '#a8a194'])
            o.append(f'<rect x="{i*W/2:.0f}" y="{j*slab:.0f}" width="{W/2:.0f}" height="{slab:.0f}" fill="{c}"/>')
    o.append(blot(r, W, H, 260, ['#6a645a', '#8a8478', '#c4bdb0', '#5a564e'], 20, 140, (0.04, 0.12)))
    for j in range(5):
        y = j * slab; o.append(f'<path d="M0,{y:.0f}H{W}" stroke="#4a4640" stroke-width="7"/><path d="M0,{y+5:.0f}H{W}" stroke="#d4cec2" stroke-width="2" opacity=".5"/>')
    o.append(f'<path d="M{W/2},0V{H}" stroke="#4e4a44" stroke-width="6"/>')
    for _ in range(16): o.append(crack(r, r.uniform(0, W), r.uniform(0, H), r.randint(5, 14), r.uniform(20, 50), w=r.uniform(1.5, 3.2)))
    for _ in range(4):                              # asphalt patches
        x, y = r.uniform(-50, W - 150), r.uniform(0, H - 300); w, h = r.uniform(180, 520), r.uniform(150, 600)
        pts = ' '.join(f'{x+w*0.5+math.cos(t)*w*0.5*r.uniform(0.75,1.0):.0f},{y+h*0.5+math.sin(t)*h*0.5*r.uniform(0.75,1.0):.0f}' for t in [i * 6.283 / 14 for i in range(14)])
        o.append(f'<polygon points="{pts}" fill="#4c4a48" stroke="#2e2c2a" stroke-width="6"/>')
        for _ in range(60): o.append(f'<circle cx="{x+r.uniform(0.1,0.9)*w:.0f}" cy="{y+r.uniform(0.1,0.9)*h:.0f}" r="{r.uniform(1.5,4):.1f}" fill="{r.choice(["#6e6c66","#2a2826","#86827a"])}"/>')
    # utility trench patch (long, along the left lane)
    x = r.uniform(80, 200); o.append(f'<rect x="{x:.0f}" y="{H*0.1:.0f}" width="70" height="{H*0.55:.0f}" fill="#57544f" stroke="#38352f" stroke-width="5"/>')
    for _ in range(26):                             # oil stains
        cx, cy = r.uniform(150, W - 150), r.uniform(0, H); rr = r.uniform(15, 70)
        o.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rr:.0f}" ry="{rr*0.6:.0f}" fill="#2e2a26" opacity="{r.uniform(.12,.3):.2f}" filter="url(#oil)" transform="rotate({r.uniform(0,180):.0f} {cx:.0f} {cy:.0f})"/>')
    for tx in (0.27, 0.73):                         # tyre tracks
        o.append(f'<rect x="{W*tx-55:.0f}" y="0" width="110" height="{H}" fill="#3a3632" opacity=".07"/>')
    # edge sand, leaves, bottle caps, butts
    o.append(f'<rect x="0" y="0" width="40" height="{H}" fill="#7a6a54" opacity=".25"/><rect x="{W-40}" y="0" width="40" height="{H}" fill="#7a6a54" opacity=".25"/>')
    for _ in range(140):
        x, y = r.choice([r.uniform(0, 120), r.uniform(W - 120, W), r.uniform(0, W)]), r.uniform(0, H); t = r.random()
        if t < 0.45: o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6,14):.0f}" ry="{r.uniform(3,6):.0f}" fill="{r.choice(["#8a6a2a","#6a5a2a","#a07a3a","#5a6a2a"])}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
        elif t < 0.6: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{r.choice(["#c8302a","#3a6ac8","#e8e0d0","#d8b030"])}"/>')
        elif t < 0.75: o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="12" height="4" fill="#f0e8d8" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
        else: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,5):.1f}" fill="#5a544c" opacity=".7"/>')
    if slow:                                        # painted road text, faded
        o.append(f'<g transform="translate({W*0.5},{H*0.55}) scale(1,2.6)" opacity=".75">' + T(0, 0, 230, 'ช้าลง', '#e8c23a', k=True) + '</g>')
        o.append(blot(r, W, H, 40, ['#a8a296'], 10, 30, (0.5, 0.8)))
    return svg(W, H, ''.join(o), font=slow)

def tiles(seed, base, line='#6a5a4a', W=512, n=5, cols=None):
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="{line}"/>']; s = W / n
    for i in range(n):
        for j in range(n):
            c = r.choice(cols or [base]); o.append(f'<rect x="{i*s+3:.0f}" y="{j*s+3:.0f}" width="{s-6:.0f}" height="{s-6:.0f}" fill="{c}"/>')
            if r.random() < 0.12: o.append(crack(r, i * s + s / 2, j * s + s / 2, 4, s / 6, w=1.6))
    o.append(blot(r, W, W, 70, ['#3a2e24', '#5a4a3a', '#2a2420'], 10, 60, (0.05, 0.16)))
    return svg(W, W, ''.join(o))

def hero_floor(W=1024):
    """4 x 4 m of the iron shop's apron: concrete, burn marks, rust rings, chalk, grinding streaks."""
    r = R(77); o = [f'<rect width="{W}" height="{W}" fill="#9a958c"/>', blot(r, W, W, 160, ['#5a544c', '#7a7268', '#b8b0a2'], 20, 120, (0.05, 0.14))]
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, W); rr = r.uniform(8, 40)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="#1e1a18" opacity="{r.uniform(.2,.55):.2f}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{rr*1.6:.0f}" fill="#3a2a1e" opacity=".12"/>')
    for _ in range(20):
        x, y = r.uniform(0, W), r.uniform(0, W); rr = r.uniform(20, 90)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr*0.6:.0f}" fill="none" stroke="#8a4a22" stroke-width="{r.uniform(4,12):.0f}" opacity=".35"/>')
    for _ in range(26):                             # grinding spark fans
        x, y = r.uniform(0, W), r.uniform(0, W); a0 = r.uniform(0, 6.28)
        for _ in range(9):
            a = a0 + r.uniform(-0.4, 0.4); L = r.uniform(30, 110)
            o.append(f'<path d="M{x:.0f},{y:.0f}l{math.cos(a)*L:.0f},{math.sin(a)*L:.0f}" stroke="#3a2a20" stroke-width="2" opacity=".35"/>')
    for _ in range(10):                             # chalk marks and offcuts
        x, y = r.uniform(50, W - 50), r.uniform(50, W - 50)
        o.append(f'<path d="M{x:.0f},{y:.0f}l{r.uniform(-90,90):.0f},{r.uniform(-30,30):.0f}m-20,-20l40,40" stroke="#f4f0e4" stroke-width="5" opacity=".7"/>')
    for _ in range(90):
        x, y = r.uniform(0, W), r.uniform(0, W)
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(6,40):.0f}" height="{r.uniform(2,6):.0f}" fill="{r.choice(["#5a5450","#7a3a1a","#c0b8a8"])}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
    for _ in range(6): o.append(crack(r, r.uniform(0, W), r.uniform(0, W), 8, 40, w=2.4))
    return svg(W, W, ''.join(o))

def gutter(W=512, H=128):
    """2 m of grated concrete drain cover, 0.5 m wide."""
    r = R(5); o = [f'<rect width="{W}" height="{H}" fill="#8e897f"/>']
    for i in range(4):
        x = i * W / 4; o.append(f'<rect x="{x+4:.0f}" y="6" width="{W/4-8:.0f}" height="{H-12}" fill="{r.choice(["#9a958a","#888378","#a39e92"])}"/>')
        for j in range(7): o.append(f'<rect x="{x+16+j*15:.0f}" y="28" width="7" height="{H-56}" rx="3" fill="#1c1a18"/>')
    o.append(blot(r, W, H, 30, ['#3a3228', '#5a6a3a'], 8, 30, (0.1, 0.25)))
    return svg(W, H, ''.join(o))

def curb(W=512, H=64):
    r = R(6); o = []
    for i in range(4): o.append(f'<rect x="{i*W/4:.0f}" y="0" width="{W/4+1:.0f}" height="{H}" fill="{["#c8382c","#ece6d8"][i%2]}"/>')
    o.append(blot(r, W, H, 40, ['#3a3028', '#6a5a4a'], 6, 30, (0.1, 0.3)))
    return svg(W, H, ''.join(o))

def manhole(W=256):
    r = R(8); o = [f'<rect width="{W}" height="{W}" fill="#9a958a"/><circle cx="128" cy="128" r="118" fill="#4a4844"/><circle cx="128" cy="128" r="104" fill="#5a5650"/>']
    for i in range(-5, 6): o.append(f'<path d="M{128+i*18},{30}V{226}" stroke="#3e3c38" stroke-width="5" opacity=".8"/>')
    o.append(f'<circle cx="128" cy="128" r="104" fill="none" stroke="#3a3834" stroke-width="10"/>' + T(128, 140, 34, 'ท่อระบาย', '#3a3834', k=True))
    o.append(blot(r, W, W, 20, ['#7a4a22', '#2a2826'], 8, 30, (0.15, 0.3)))
    return svg(W, W, ''.join(o), font=True)

# ----------------------------------------------------------------------------- shophouse facades
FH = 11.2                                           # facade height (m), parapet top
def facade(seed, base, W=512, H=1408, wm=4.0, hero=False):
    """Wall paint for one shophouse bay (wm m wide, 11.2 m tall). Knows the layout: canopy 3.75, sills 4.9 / 8.1, floor bands."""
    r = R(seed); k = W / wm; Z = lambda z: (FH - z) * k; o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']
    o.append(blot(r, W, H, int(40 * wm), ['#6a5a48', '#8a7a62', '#ffffff', '#4a5a3a'], 0.2 * k, 1.0 * k, (0.03, 0.08)))
    for z0 in (3.75, 7.05, 10.35):                  # floor beams: slightly proud bands
        o.append(f'<rect x="0" y="{Z(z0+0.22):.0f}" width="{W}" height="{0.22*k:.0f}" fill="#000" opacity=".08"/><rect x="0" y="{Z(z0):.0f}" width="{W}" height="4" fill="#2a2018" opacity=".25"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="{0.16*k:.0f}" fill="#4a4a3a" opacity=".35"/>')          # parapet coping, mouldy
    o.append(streaks(r, 0, W, Z(11.0), 2.2 * k, k, '#2e3a22', int(8 * wm), (0.12, 0.3)))
    o.append(streaks(r, 0.3 * k, W - 0.3 * k, Z(4.85), 1.0 * k, k, '#3a2e22', int(5 * wm), (0.08, 0.22)))
    o.append(streaks(r, 0.3 * k, W - 0.3 * k, Z(8.05), 1.0 * k, k, '#3a2e22', int(5 * wm), (0.08, 0.22)))
    o.append(streaks(r, 0, W, Z(3.5), 0.8 * k, k, '#3a2e22', int(3 * wm), (0.05, 0.15)))
    for _ in range(int(3 * wm)):                    # peeling paint -> grey render / brick
        x, y = r.uniform(0, W), r.uniform(Z(10.5), Z(0.3)); w = r.uniform(0.1, 0.6) * k; h = w * r.uniform(0.3, 0.8)
        pts = ' '.join(f'{x+math.cos(t)*w*r.uniform(0.6,1):.0f},{y+math.sin(t)*h*r.uniform(0.6,1):.0f}' for t in [i * 6.283 / 9 for i in range(9)])
        o.append(f'<polygon points="{pts}" fill="#b0a898" stroke="#f6f0e2" stroke-width="2"/>')
        if r.random() < 0.4: o.append(f'<rect x="{x-w*0.3:.0f}" y="{y-h*0.2:.0f}" width="{w*0.5:.0f}" height="{h*0.4:.0f}" fill="#a0623e" opacity=".7"/>')
    o.append(f'<rect x="0" y="{Z(0.5):.0f}" width="{W}" height="{0.5*k:.0f}" fill="#3a4a2a" opacity=".22"/>')    # rising damp
    for _ in range(int(2 * wm)): o.append(crack(r, r.uniform(0, W), r.uniform(Z(10), Z(1)), 6, 0.12 * k, w=1.6, op=0.45))
    # conduits and cables clipped to the wall
    for _ in range(2):
        x = r.uniform(0.1, 0.9) * W; o.append(f'<path d="M{x:.0f},{Z(10.2):.0f}V{Z(r.uniform(4.0,7.0)):.0f}" stroke="#d8d4c8" stroke-width="{0.04*k:.0f}"/><path d="M{x:.0f},{Z(10.2):.0f}V{Z(4):.0f}" stroke="#000" stroke-width="2" opacity=".2" transform="translate(3,0)"/>')
    for _ in range(3):
        y = Z(r.uniform(4.2, 10)); o.append(f'<path d="M0,{y:.0f}Q{W/2:.0f},{y+r.uniform(-8,25):.0f} {W},{y+r.uniform(-20,20):.0f}" stroke="#1a1816" stroke-width="{r.uniform(2,4):.1f}" fill="none" opacity=".75"/>')
    # small things at eye height (between the shutter jambs and on the pier)
    if not hero:
        o.append(f'<rect x="{0.04*k:.0f}" y="{Z(3.0):.0f}" width="{0.14*k:.0f}" height="{0.1*k:.0f}" fill="#2a4a9a"/>' + T(0.11 * k, Z(2.92), 0.07 * k, f'{r.randint(10,180)}/{r.randint(1,40)}', '#fff'))
    return svg(W, H, ''.join(o), font=True)

def pier(seed, base, W=128, H=1408):
    """Party-wall pier between bays (0.36 m wide): paint, meters, posters, stickers."""
    r = R(seed); k = W / 0.36; Z = lambda z: (FH - z) * k; o = [f'<rect width="{W}" height="{H}" fill="{base}"/>', blot(r, W, H, 50, ['#5a4a38', '#ffffff', '#3a4a2a'], 10, 60, (0.04, 0.1))]
    o.append(streaks(r, 0, W, Z(11), 3 * k, k, '#2e3a22', 6, (0.1, 0.25)))
    o.append(f'<rect x="0" y="{Z(0.6):.0f}" width="{W}" height="{0.6*k:.0f}" fill="#3a4a2a" opacity=".3"/>')
    y = Z(2.2)
    for _ in range(r.randint(1, 3)):                # stuck-on notices
        h = r.uniform(0.15, 0.35) * k; c = r.choice(['#f4f0e0', '#f0e060', '#f4c0c0', '#c0e0f4'])
        o.append(f'<rect x="{r.uniform(4,20):.0f}" y="{y:.0f}" width="{W*0.75:.0f}" height="{h:.0f}" fill="{c}" transform="rotate({r.uniform(-6,6):.0f} {W/2} {y:.0f})"/>')
        for i in range(3): o.append(f'<rect x="{14:.0f}" y="{y+8+i*h/4:.0f}" width="{r.uniform(40,90):.0f}" height="{h/9:.0f}" fill="{r.choice(["#c02020","#202020","#2040a0"])}"/>')
        y += h + 10
    return svg(W, H, ''.join(o))

def shutter(seed, base, W=512, stick=True):
    """2 x 2 m of roller-shutter slats (8 cm pitch), dents, rust, stickers, tags."""
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="{base}"/>']; p = W / 25
    for i in range(25):
        y = i * p; o.append(f'<rect x="0" y="{y:.0f}" width="{W}" height="{p*0.35:.0f}" fill="#fff" opacity=".18"/><rect x="0" y="{y+p*0.72:.0f}" width="{W}" height="{p*0.28:.0f}" fill="#000" opacity=".28"/>')
    o.append(blot(r, W, W, 60, ['#5a3a20', '#2a2a2a', '#ffffff'], 10, 60, (0.04, 0.12)))
    o.append(streaks(r, 0, W, 0, W, W / 2, '#7a3a14', 12, (0.08, 0.25)))
    if stick:
        for _ in range(r.randint(2, 5)):
            x, y = r.uniform(20, W - 120), r.uniform(20, W - 80); c = r.choice(['#f4f0e0', '#f0e040', '#fff', '#80d0f0'])
            o.append(f'<g transform="rotate({r.uniform(-8,8):.0f} {x:.0f} {y:.0f})"><rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(50,110):.0f}" height="{r.uniform(26,60):.0f}" fill="{c}"/>'
                     f'<rect x="{x+6:.0f}" y="{y+8:.0f}" width="40" height="7" fill="#d02020"/><rect x="{x+6:.0f}" y="{y+20:.0f}" width="60" height="5" fill="#222"/></g>')
        for _ in range(r.randint(0, 2)):            # spray tags
            x, y = r.uniform(40, W - 200), r.uniform(150, W - 60); c = r.choice(['#1a1a1a', '#d02828', '#2848c8'])
            d = f'M{x:.0f},{y:.0f}' + ''.join(f'q{r.uniform(-30,30):.0f},{r.uniform(-60,20):.0f} {r.uniform(15,40):.0f},{r.uniform(-15,15):.0f}' for _ in range(6))
            o.append(f'<path d="{d}" stroke="{c}" stroke-width="{r.uniform(5,9):.0f}" fill="none" opacity=".8" stroke-linecap="round"/>')
    return svg(W, W, ''.join(o))

def grille(kind, col, W=512):
    """Window grille, 1 m tile, transparent background. kind: 'sun', 'diamond', 'tulip'."""
    o = []; s = f'stroke="{col}" fill="none" stroke-width="10" stroke-linecap="round"'; sh = 'stroke="#000" fill="none" stroke-width="10" opacity=".35" transform="translate(4,5)"'
    paths = [f'M0,6H{W}M0,{W-6}H{W}M6,0V{W}M{W-6},0V{W}']
    if kind == 'sun':
        for i in range(1, 4): paths.append(f'M{i*W/4:.0f},0V{W}')
        paths.append(f'M0,{W/2}H{W}')
        for cx in (W / 4, W * 3 / 4):
            paths.append(f'M{cx-60:.0f},{W/2}A60,60 0 0 1 {cx+60:.0f},{W/2}')
            for a in range(0, 181, 30): t = math.radians(a); paths.append(f'M{cx:.0f},{W/2}l{math.cos(t)*120:.0f},{-math.sin(t)*120:.0f}')
    elif kind == 'diamond':
        n = 4
        for i in range(-n, n + 1): paths.append(f'M{i*W/n:.0f},0L{i*W/n+W:.0f},{W}M{i*W/n:.0f},{W}L{i*W/n+W:.0f},0')
        for i in range(n): paths.append(f'M{(i+0.5)*W/n:.0f},{W/2-24:.0f}a24,24 0 1 0 0.1,0')
    else:
        for i in range(1, 6): paths.append(f'M{i*W/6:.0f},0V{W}')
        for i in range(6):
            cx = (i + 0.5) * W / 6
            paths.append(f'M{cx-W/12:.0f},{W*0.62:.0f}C{cx-W/12:.0f},{W*0.38:.0f} {cx:.0f},{W*0.38:.0f} {cx:.0f},{W*0.30:.0f}C{cx:.0f},{W*0.38:.0f} {cx+W/12:.0f},{W*0.38:.0f} {cx+W/12:.0f},{W*0.62:.0f}')
            paths.append(f'M{cx:.0f},{W*0.62:.0f}a16,16 0 1 0 0.1,0')
        paths.append(f'M0,{W*0.22:.0f}H{W}M0,{W*0.7:.0f}H{W}')
    d = ''.join(paths)
    return svg(W, W, f'<path d="{d}" {sh}/><path d="{d}" {s}/><path d="{d}" stroke="#fff" fill="none" stroke-width="3" opacity=".35" transform="translate(-2,-2)"/>')

def window(seed, W=256, H=320):
    r = R(seed); cur = r.choice(['#e07a8a', '#7aa0d8', '#e8c860', '#f0ece0', '#8ac080', '#c8a0e0'])
    o = [f'<rect width="{W}" height="{H}" fill="#26303e"/>', f'<path d="M0,{H*0.3:.0f}L{W},{H*0.05:.0f}V{H*0.25:.0f}L0,{H*0.5:.0f}Z" fill="#7a90a8" opacity=".35"/>']
    if r.random() < 0.8:                            # curtains, half drawn
        a = r.uniform(0.25, 0.5) * W; o.append(f'<rect x="0" y="0" width="{a:.0f}" height="{H}" fill="{cur}"/>')
        for i in range(5): o.append(f'<path d="M{i*a/5+5:.0f},0V{H}" stroke="#000" stroke-width="6" opacity=".18"/>')
        if r.random() < 0.6: b = r.uniform(0.15, 0.35) * W; o.append(f'<rect x="{W-b:.0f}" y="0" width="{b:.0f}" height="{H}" fill="{cur}"/>')
    if r.random() < 0.4: o.append(f'<rect x="{W*0.55:.0f}" y="{H*0.55:.0f}" width="{W*0.3:.0f}" height="{H*0.3:.0f}" fill="#d8c8a0" opacity=".7"/>')   # cardboard taped
    o.append(f'<path d="M{W/2},0V{H}M0,{H/2}H{W}" stroke="#b8bcc0" stroke-width="10"/><rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#a8acb0" stroke-width="16"/>')
    return svg(W, H, ''.join(o))

def window_glow(seed, W=256, H=320):
    """Emission mask for window(seed) at dusk: warm room light through the glass, curtains glowing in their own colour, frame and
    taped cardboard black. Consumes the random stream exactly as window() does, so curtains line up with the base texture."""
    r = R(seed); cur = r.choice(['#e07a8a', '#7aa0d8', '#e8c860', '#f0ece0', '#8ac080', '#c8a0e0'])
    room = R(seed * 7 + 1).choice(['#ffd08a', '#ffe0a8', '#ffc878', '#bfe0ff'])
    o = [f'<rect width="{W}" height="{H}" fill="{room}"/>', f'<path d="M0,{H*0.3:.0f}L{W},{H*0.05:.0f}V{H*0.25:.0f}L0,{H*0.5:.0f}Z" fill="#000" opacity=".15"/>']
    if r.random() < 0.8:
        a = r.uniform(0.25, 0.5) * W; o.append(f'<rect x="0" y="0" width="{a:.0f}" height="{H}" fill="{cur}" opacity=".85"/>')
        for i in range(5): o.append(f'<path d="M{i*a/5+5:.0f},0V{H}" stroke="#000" stroke-width="6" opacity=".35"/>')
        if r.random() < 0.6: b = r.uniform(0.15, 0.35) * W; o.append(f'<rect x="{W-b:.0f}" y="0" width="{b:.0f}" height="{H}" fill="{cur}" opacity=".85"/>')
    if r.random() < 0.4: o.append(f'<rect x="{W*0.55:.0f}" y="{H*0.55:.0f}" width="{W*0.3:.0f}" height="{H*0.3:.0f}" fill="#000"/>')
    o.append(f'<path d="M{W/2},0V{H}M0,{H/2}H{W}" stroke="#000" stroke-width="10"/><rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#000" stroke-width="16"/>')
    return svg(W, H, ''.join(o))

def tower_glow(W=2048, H=2048, wm=20.0, hm=24.5):
    """Emission mask for tower_facade(): about 60 percent of the flats lit (warm, a few cold TV-blue), curtains, the lit ground-floor
    shops and the blue LED name sign. Same window grid as the base texture."""
    r = R(122); kx = W / wm; ky = H / hm; Z = lambda z: (hm - z) * ky; o = [f'<rect width="{W}" height="{H}" fill="#000"/>']
    for f in range(7):
        z0 = 3.5 * f
        if f == 0:
            for i in range(5):
                x = (0.4 + i * 3.9) * kx
                if i != 2: o.append(f'<rect x="{x:.0f}" y="{Z(3.0):.0f}" width="{3.4*kx:.0f}" height="{2.6*ky:.0f}" fill="{r.choice(["#e8f4ff", "#fff0c8", "#d8ecff"])}"/>')
            continue
        for i in range(8):
            x = (0.55 + i * 2.45) * kx; zz = z0 + 1.0
            if r.random() < 0.6:
                c = r.choice(['#ffd08a', '#ffc070', '#ffe0a8', '#ffd08a', '#a8d0ff']); o.append(f'<rect x="{x:.0f}" y="{Z(zz+1.5):.0f}" width="{1.5*kx:.0f}" height="{1.5*ky:.0f}" fill="{c}"/>')
                if r.random() < 0.6: o.append(f'<rect x="{x:.0f}" y="{Z(zz+1.5):.0f}" width="{r.uniform(0.3,0.75)*kx:.0f}" height="{1.5*ky:.0f}" fill="{r.choice(["#e07a6a","#7aa0d8","#e8c860","#f0ece0"])}" opacity=".8"/>')
                o.append(f'<path d="M{x:.0f},{Z(zz+0.75):.0f}h{1.5*kx:.0f}M{x+0.75*kx:.0f},{Z(zz+1.5):.0f}v{1.5*ky:.0f}" stroke="#000" stroke-width="8"/>')
                for g in range(5): o.append(f'<path d="M{x+g*0.375*kx:.0f},{Z(zz+1.5):.0f}v{1.5*ky:.0f}" stroke="#000" stroke-width="4" opacity=".8"/>')
    o.append(f'<rect x="{W*0.3:.0f}" y="{Z(5.4):.0f}" width="{W*0.4:.0f}" height="{1.1*ky:.0f}" fill="#1e5ad0"/>' + T(W / 2, Z(4.6), 0.75 * ky, 'ร่วมใจ แมนชั่น', '#ffffff', k=True))
    return svg(W, H, ''.join(o), font=True)

def ac_front(W=256, H=192):
    o = [f'<rect width="{W}" height="{H}" fill="#e4e2da"/><circle cx="{W*0.4:.0f}" cy="{H/2}" r="{H*0.4:.0f}" fill="#3a3c40"/>']
    for i in range(-8, 9): o.append(f'<path d="M{W*0.4-H*0.4:.0f},{H/2+i*H*0.045:.0f}h{H*0.8:.0f}" stroke="#b8b8b0" stroke-width="2.5"/>')
    o.append(f'<circle cx="{W*0.4:.0f}" cy="{H/2}" r="12" fill="#8a8a88"/>')
    for i in range(10): o.append(f'<rect x="{W*0.8:.0f}" y="{20+i*15}" width="{W*0.15:.0f}" height="6" fill="#9a9a94"/>')
    o.append(f'<path d="M0,{H}h{W}" stroke="#6a4a2a" stroke-width="20" opacity=".4"/>')
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- signs
def sign_hero(W=2048, H=416):
    """Main sign of the iron shop (8 m x 1.6 m): red board, yellow lettering, phone number."""
    r = R(31); o = [f'<rect width="{W}" height="{H}" fill="#d0281e"/><rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#f6d23a" stroke-width="14"/>']
    o.append(f'<rect x="0" y="{H-96}" width="{W}" height="96" fill="#f6d23a"/>')
    # wrought-iron scroll emblems both ends
    for cx in (150, W - 150):
        o.append(f'<circle cx="{cx}" cy="{H*0.4:.0f}" r="96" fill="#f6d23a"/><path d="M{cx-60},{H*0.4+40:.0f}c0,-90 120,-90 120,-30c0,40 -60,40 -60,10c0,-20 30,-20 30,-5" stroke="#1a1a1a" stroke-width="14" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{cx-70},{H*0.4+60:.0f}h140" stroke="#1a1a1a" stroke-width="14"/>')
    o.append(T(W / 2, H * 0.55, 172, 'ร้านเหล็กดัด เจ๊หงส์', '#fff3a0', k=True, stroke='#5a0a06', sw=18))
    o.append(T(W / 2, H - 24, 72, 'รับทำประตู • หน้าต่าง • เหล็กดัด   โทร. 089-472-6158', '#b01a12', k=True))
    o.append(blot(r, W, H, 50, ['#3a2010', '#ffffff'], 20, 90, (0.04, 0.12)))
    o.append(streaks(r, 0, W, H - 96, 96, 40, '#5a3a18', 30, (0.1, 0.3)))
    o.append(f'<rect x="0" y="0" width="{W}" height="22" fill="#3a1a10" opacity=".4"/>')
    return svg(W, H, ''.join(o), font=True)

def sign_board(W=1024, H=512):
    """Services board standing on the apron (1.2 x 0.6 m), yellow with red/black text."""
    o = [f'<rect width="{W}" height="{H}" fill="#f6d23a"/><rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="#c8281e" stroke-width="12"/>',
         T(W / 2, 120, 92, 'รับเชื่อม ทุกชนิด', '#c8281e', k=True), T(W / 2, 225, 64, 'ประตูรั้ว • ประตูม้วน • หลังคา', '#1a1a1a'),
         T(W / 2, 315, 64, 'ราวบันได • กันสาด • ซ่อมด่วน', '#1a1a1a'), f'<rect x="40" y="355" width="{W-80}" height="110" rx="20" fill="#c8281e"/>',
         T(W / 2, 438, 78, '089-472-6158', '#fff', k=True)]
    r = R(4); o.append(blot(r, W, H, 30, ['#3a2a10'], 20, 70, (0.05, 0.15)))
    return svg(W, H, ''.join(o), font=True)

SIGNS = [   # (text, sub, bg, fg, accent)
    ('ก๋วยเตี๋ยวเรือ ป้าแดง', 'น้ำตก • ต้มยำ • เย็นตาโฟ', '#f4efe2', '#c42a1e', '#2a6a3a'),
    ('ร้านตัดผมชาย ช่างเปี๊ยก', 'ตัด 80 บาท • โกนหนวด', '#2a5ab0', '#ffffff', '#e8302a'),
    ('เจริญสุข พาณิชย์', 'ของชำ • น้ำแข็ง • แก๊ส', '#1e7a44', '#fff6c0', '#f0c030'),
    ('ซ่อมรถมอเตอร์ไซค์ ปะยาง', 'เปลี่ยนน้ำมันเครื่อง', '#f2c41e', '#1a1a1a', '#c8281e'),
    ('เสริมสวย น้องนุช', 'ซอย • ดัด • ทำสี', '#f0a0c0', '#7a1a4a', '#ffffff'),
    ('ร้านขายยา สุขภาพดี', 'ยาแผนปัจจุบัน', '#ffffff', '#1a7a3a', '#1a7a3a'),
    ('ถ่ายเอกสาร • ปริ้นท์', 'เคลือบบัตร • เข้าเล่ม', '#1a3a7a', '#ffe040', '#ffffff'),
    ('ข้าวมันไก่ เฮียเล้ง', 'ไก่ต้ม • ไก่ทอด', '#c8281e', '#fff3c0', '#f0c030'),
]
def signs_atlas(W=1024, H=2048):
    """8 rows of 1024 x 256 shop signs (4:1)."""
    r = R(12); o = []
    for i, (t, sub, bg, fg, ac) in enumerate(SIGNS):
        y = i * 256
        o.append(f'<rect x="0" y="{y}" width="{W}" height="256" fill="{bg}"/><rect x="10" y="{y+10}" width="{W-20}" height="236" fill="none" stroke="{ac}" stroke-width="10"/>')
        o.append(f'<circle cx="110" cy="{y+128}" r="78" fill="{ac}"/><circle cx="110" cy="{y+128}" r="50" fill="{bg}"/>')
        o.append(T(W / 2 + 60, y + 140, 92 if len(t) < 18 else 74, t, fg, k=True))
        o.append(T(W / 2 + 60, y + 218, 46, sub, fg))
    body = ''.join(o)
    for i in range(8):
        for _ in range(25):
            x, yy = r.uniform(0, W), i * 256 + r.uniform(0, 256); a = r.uniform(20, 70)
            body += f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{a:.0f}" ry="{a*0.5:.0f}" fill="{r.choice(["#3a2a1a","#ffffff"])}" opacity="{r.uniform(.04,.14):.2f}"/>'
        body += streaks(r, 0, W, i * 256 + 200, 56, 30, '#3a2a1a', 14, (0.1, 0.25))
    return svg(W, H, body, font=True)

def soi_sign(W=512, H=256):
    o = [f'<rect width="{W}" height="{H}" rx="18" fill="#f4f4f0"/><rect x="10" y="10" width="{W-20}" height="{H-20}" rx="12" fill="#1f4fa0"/>',
         T(W / 2, 120, 92, 'ซอยร่วมใจ 17', '#fff', k=True), T(W / 2, 200, 48, 'Soi Ruam Jai 17', '#fff')]
    r = R(3); o.append(blot(r, W, H, 20, ['#3a2a1a'], 15, 50, (0.08, 0.2)))
    return svg(W, H, ''.join(o), font=True)

def posters(W=1024, H=1024):
    """4 x 4 cells of 256: small notices, election-style poster, stickers (for poles and walls)."""
    r = R(41); o = [f'<rect width="{W}" height="{H}" fill="#ece6d4"/>']
    items = [('รับซื้อของเก่า', '#f0e040', '#c8281e'), ('เงินด่วน ไม่เช็คบูโร', '#fff', '#c8281e'), ('ห้องว่าง ให้เช่า', '#fff', '#1a3a9a'), ('ช่างแอร์ ล้างแอร์', '#80d0f0', '#1a1a1a'),
             ('ห้ามจอดรถ', '#fff', '#c8281e'), ('รับสอนพิเศษ', '#f4c0d0', '#7a1a4a'), ('ประปาซ่อม ด่วน', '#e0f0c0', '#1a5a1a'), ('ขายที่ดิน', '#ffe080', '#1a1a1a'),
             ('แมวหาย!', '#fff', '#1a1a1a'), ('ปะยาง 24 ชม.', '#f2c41e', '#1a1a1a'), ('รับจ้างขนของ', '#fff', '#1a3a9a'), ('ดูดวง แม่หมอ', '#c0a0e0', '#3a1a5a'),
             ('งานวัด 25-27', '#f04030', '#fff6c0'), ('เบอร์ 7', '#ff8020', '#fff'), ('กู้ภัย 1669', '#fff', '#c8281e'), ('ทำบัตร', '#fff', '#1a1a1a')]
    for i, (t, bg, fg) in enumerate(items):
        x, y = (i % 4) * 256, (i // 4) * 256
        o.append(f'<rect x="{x+6}" y="{y+6}" width="244" height="244" fill="{bg}"/><rect x="{x+6}" y="{y+6}" width="244" height="244" fill="none" stroke="{fg}" stroke-width="6"/>')
        o.append(T(x + 128, y + 90, 40 if len(t) < 12 else 30, t, fg, k=True))
        for j in range(4): o.append(f'<rect x="{x+28}" y="{y+120+j*26}" width="{r.uniform(120,200):.0f}" height="10" fill="{fg}" opacity=".55"/>')
        o.append(f'<rect x="{x+28}" y="{y+215}" width="200" height="22" fill="{fg}"/>' + T(x + 128, y + 233, 20, f'08{r.randint(1,9)}-{r.randint(100,999)}-{r.randint(1000,9999)}', bg))
        if i == 13: o.append(f'<circle cx="{x+128}" cy="{y+150}" r="56" fill="#f2d0b0"/><circle cx="{x+108}" cy="{y+140}" r="7" fill="#222"/><circle cx="{x+148}" cy="{y+140}" r="7" fill="#222"/><path d="M{x+100},{y+168}q28,22 56,0" stroke="#222" stroke-width="6" fill="none"/><path d="M{x+72},{y+120}q56,-60 112,0" fill="#222"/>')
    o.append(blot(r, W, H, 80, ['#5a4a2a', '#ffffff'], 15, 60, (0.05, 0.16)))
    return svg(W, H, ''.join(o), font=True)

def interiors(W=1024, H=1024):
    """4 rows of 1024 x 256: back walls of other shops (4 x 1 m bands, stretched to 4 x 3 m): grocery, noodle, barber, bike repair."""
    r = R(51); o = []
    # grocery shelves
    o.append('<rect x="0" y="0" width="1024" height="256" fill="#5a4a3a"/>')
    for s in range(4):
        y = 10 + s * 62; o.append(f'<rect x="0" y="{y+52}" width="1024" height="8" fill="#c8c0b0"/>')
        x = 4
        while x < 1020:
            w = r.uniform(10, 30); h = r.uniform(20, 50); o.append(f'<rect x="{x:.0f}" y="{y+52-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{r.choice(["#e83a2a","#f0c030","#3a8ae0","#30b050","#f08030","#fff","#a040c0","#e8e0c8"])}"/><rect x="{x+2:.0f}" y="{y+52-h*0.6:.0f}" width="{w-4:.0f}" height="{h*0.25:.0f}" fill="#fff" opacity=".5"/>'); x += w + 2
    # noodle shop
    o.append('<rect x="0" y="256" width="1024" height="256" fill="#d8cdb8"/><rect x="40" y="276" width="300" height="120" fill="#fff"/>' + T(190, 320, 34, 'เมนู', '#c42a1e', k=True))
    for j in range(3): o.append(f'<rect x="70" y="{335+j*18}" width="230" height="8" fill="#555"/>')
    o.append('<rect x="380" y="300" width="80" height="80" fill="#c8a040"/><rect x="0" y="440" width="1024" height="72" fill="#8a6a4a"/>')
    for i in range(5): o.append(f'<rect x="{500+i*100}" y="{300+r.randint(0,20)}" width="70" height="100" rx="10" fill="#e8e8e8" opacity=".9"/>')
    # barber
    o.append('<rect x="0" y="512" width="1024" height="256" fill="#a8c8d8"/>')
    for i in range(3): o.append(f'<rect x="{80+i*320}" y="535" width="220" height="140" fill="#dfe8ee" stroke="#555" stroke-width="8"/><rect x="{110+i*320}" y="690" width="160" height="70" fill="#7a2a2a"/>')
    # bike repair: tyres and tools
    o.append('<rect x="0" y="768" width="1024" height="256" fill="#6a6258"/><rect x="20" y="780" width="500" height="150" fill="#b89a70"/>')
    for i in range(12): o.append(f'<path d="M{40+i*38},{800}v{r.randint(40,110)}" stroke="#2a2a2a" stroke-width="9"/>')
    for i in range(5): o.append(f'<circle cx="{620+i*80}" cy="{860}" r="60" fill="none" stroke="#1e1e1e" stroke-width="20"/>')
    o.append(blot(r, W, H, 80, ['#000'], 20, 90, (0.05, 0.15)))
    return svg(W, H, ''.join(o), font=True)

def hero_wall(W=2048, H=1024):
    """Back wall of the iron shop (8 x 4 m): soot, burn marks, pegboard of tools, calendar, welding curtain, Buddha-shelf red cloth."""
    r = R(61); k = W / 8; o = [f'<rect width="{W}" height="{H}" fill="#8e8678"/>', blot(r, W, H, 140, ['#2a2420', '#4a3a2a', '#b0a898'], 20, 160, (0.06, 0.18))]
    o.append(f'<rect x="0" y="0" width="{W}" height="{H*0.35:.0f}" fill="#1a1612" opacity=".35"/>')      # soot under the ceiling
    for _ in range(30):
        x, y = r.uniform(0, W), r.uniform(H * 0.4, H); rr = r.uniform(10, 50)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="#1a1612" opacity="{r.uniform(.2,.5):.2f}"/>')
    px, py = 0.4 * k, H * 0.3; o.append(f'<rect x="{px:.0f}" y="{py:.0f}" width="{2.4*k:.0f}" height="{1.2*k:.0f}" fill="#b89a6a"/>')     # pegboard
    for i in range(18):
        x = px + 30 + i * 32; o.append(f'<rect x="{x:.0f}" y="{py+30:.0f}" width="{r.uniform(8,22):.0f}" height="{r.uniform(60,170):.0f}" fill="{r.choice(["#3a3a3a","#c8281e","#2a5ab0","#8a8a8a","#e8a020"])}"/>')
    for i in range(6): o.append(f'<circle cx="{px+60+i*90:.0f}" cy="{py+250:.0f}" r="{r.uniform(20,36):.0f}" fill="none" stroke="#2a2a2a" stroke-width="8"/>')
    cx = 3.4 * k; o.append(f'<rect x="{cx:.0f}" y="{H*0.25:.0f}" width="180" height="260" fill="#fff"/><rect x="{cx:.0f}" y="{H*0.25:.0f}" width="180" height="90" fill="#c8281e"/>' + T(cx + 90, H * 0.25 + 62, 40, 'พ.ย. 69', '#fff', k=True))
    for j in range(5):
        for i in range(7): o.append(f'<rect x="{cx+10+i*24:.0f}" y="{H*0.25+100+j*30:.0f}" width="18" height="20" fill="{"#c8281e" if (i+j*7)==17 else "#ccc"}"/>')
    o.append(f'<rect x="{4.5*k:.0f}" y="{H*0.15:.0f}" width="{1.6*k:.0f}" height="{H*0.85:.0f}" fill="#2a6a3a" opacity=".9"/>')        # welding curtain
    for i in range(8): o.append(f'<path d="M{4.5*k+i*50:.0f},{H*0.15:.0f}V{H}" stroke="#123a20" stroke-width="10"/>')
    o.append(f'<rect x="{6.5*k:.0f}" y="{H*0.4:.0f}" width="{1.2*k:.0f}" height="{0.5*k:.0f}" fill="#e8e0c8"/>' + T(7.1 * k, H * 0.4 + 80, 50, 'ห้ามสูบบุหรี่', '#c8281e', k=True))
    o.append(T(7.1 * k, H * 0.4 + 130, 34, 'มีถังแก๊ส อันตราย', '#1a1a1a'))
    o.append(f'<rect x="0" y="{H-0.3*k:.0f}" width="{W}" height="{0.3*k:.0f}" fill="#2a2420" opacity=".4"/>')
    return svg(W, H, ''.join(o), font=True)

# ----------------------------------------------------------------------------- iron work
def gate(kind, W=1024, H=1024):
    """Ornate wrought-iron gate panel, transparent. kind: 'black' (gold tips), 'white', 'green', 'raw' (half-made: frame + a few scrolls, chalk)."""
    col = dict(black='#1e1c1e', white='#ecebe4', green='#2a6a4a', raw='#6a6a6e', red='#9a3a2a')[kind]; gold = '#e8b830'
    hi = dict(black='#5a5660', white='#ffffff', green='#5aa080', raw='#a8a8ae', red='#c87050')[kind]
    sw = 16; P = []
    P.append(f'M30,140H{W-30}M30,{H-40}H{W-30}M30,140V{H-40}M{W-30},140V{H-40}M30,{H*0.55:.0f}H{W-30}')
    full = kind != 'raw'
    n = 9
    for i in range(1, n):
        x = 30 + i * (W - 60) / n
        if full or i % 3 == 0: P.append(f'M{x:.0f},{H*0.55:.0f}V{H-40}M{x:.0f},140V{60 if full else 140}')
    # scrolls (C and S curls) in the upper band
    def scroll(cx, cy, s, flip=1):
        return (f'M{cx:.0f},{cy+s:.0f}c{-s*0.9*flip:.0f},0 {-s*0.9*flip:.0f},{-s*1.6:.0f} 0,{-s*1.6:.0f}c{s*0.7*flip:.0f},0 {s*0.7*flip:.0f},{s:.0f} {s*0.1*flip:.0f},{s:.0f}c{-s*0.4*flip:.0f},0 {-s*0.4*flip:.0f},{-s*0.5:.0f} 0,{-s*0.5:.0f}')
    m = 4 if full else 2
    for i in range(m):
        cx = 30 + (i + 0.5) * (W - 60) / m
        P.append(scroll(cx - 50, H * 0.42, 90, 1)); P.append(scroll(cx + 50, H * 0.42, 90, -1))
        if full: P.append(f'M{cx:.0f},{H*0.55:.0f}c-60,-80 -60,-150 0,-200c60,50 60,120 0,200')
    if full:
        for i in range(n - 1):                          # circles in the lower band
            cx = 30 + (i + 1) * (W - 60) / n; P.append(f'M{cx-40:.0f},{H*0.78:.0f}a40,40 0 1 0 80,0a40,40 0 1 0 -80,0')
        P.append(f'M30,{H*0.68:.0f}H{W-30}')
    d = ''.join(P); o = [f'<path d="{d}" stroke="#000" stroke-width="{sw}" fill="none" opacity=".3" transform="translate(5,6)" stroke-linecap="round"/>',
                         f'<path d="{d}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
                         f'<path d="{d}" stroke="{hi}" stroke-width="4" fill="none" opacity=".55" transform="translate(-3,-3)"/>']
    if full:
        for i in range(1, n):
            x = 30 + i * (W - 60) / n; c = gold if kind in ('black', 'green') else col
            o.append(f'<path d="M{x-22:.0f},64L{x:.0f},18L{x+22:.0f},64L{x:.0f},84Z" fill="{c}" stroke="#000" stroke-width="3"/>')
        for i in range(m):
            cx = 30 + (i + 0.5) * (W - 60) / m; o.append(f'<circle cx="{cx:.0f}" cy="{H*0.42:.0f}" r="18" fill="{gold if kind != "white" else col}"/>')
    else:
        r = R(2)
        o.append(f'<path d="M80,{H*0.62:.0f}l300,0m-260,30l200,0" stroke="#f4f0e4" stroke-width="5" opacity=".8"/>' + T(520, H * 0.65, 44, '120 x 200', '#f4f0e4'))
        for _ in range(14):                         # rust and weld beads at the joints
            x, y = r.choice([30, W - 30, W / 3, 2 * W / 3]), r.choice([140, H * 0.55, H - 40])
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(10,16):.0f}" fill="#4a3a2e"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(18,30):.0f}" fill="#1e5aa0" opacity=".25"/>')
    return svg(W, H, ''.join(o), font=not full)

def slip(W=768, H=1024):
    """Motorbike instalment bill on the bench: ใบแจ้งค่างวด with the amount."""
    r = R(91); o = [f'<rect width="{W}" height="{H}" fill="#fbf8ee"/><rect x="0" y="0" width="{W}" height="150" fill="#1e5aa0"/>',
                    T(40, 70, 42, 'บริษัท สบายใจ ลิสซิ่ง จำกัด', '#fff', 'start', k=True), T(40, 120, 30, 'สินเชื่อรถจักรยานยนต์', '#d8e8ff', 'start'),
                    T(W / 2, 230, 74, 'ใบแจ้งค่างวด', '#1a1a1a', k=True), f'<path d="M40,260H{W-40}" stroke="#1e5aa0" stroke-width="4"/>']
    rows = [('ชื่อผู้เช่าซื้อ', 'นายสายฟ้า ใจเหล็ก'), ('รถ', 'จักรยานยนต์ 110 ซีซี'), ('ทะเบียน', '1กข 4721 กทม.'), ('งวดที่', '29 / 36'), ('ครบกำหนด', '15 พ.ย. 2569')]
    y = 320
    for a, b in rows:
        o.append(T(50, y, 34, a, '#555', 'start') + T(W - 50, y, 36, b, '#1a1a1a', 'end')); o.append(f'<path d="M50,{y+16}H{W-50}" stroke="#ccc" stroke-width="2"/>'); y += 66
    o.append(f'<rect x="40" y="{y+10}" width="{W-80}" height="170" fill="#fff1d0" stroke="#d0281e" stroke-width="6"/>' + T(70, y + 70, 36, 'ยอดชำระงวดนี้', '#d0281e', 'start', k=True))
    o.append(T(W - 70, y + 150, 84, '2,890.00 บาท', '#d0281e', 'end', k=True))
    o.append(T(W / 2, y + 240, 30, 'ค้างชำระ 1 งวด  ค่าปรับ 150.00 บาท', '#1a1a1a'))
    for i in range(40): o.append(f'<rect x="{60+i*16}" y="{H-110}" width="{r.choice([4,6,8,10])}" height="70" fill="#111"/>')
    o.append(f'<ellipse cx="{W*0.7:.0f}" cy="{H*0.83:.0f}" rx="120" ry="100" fill="none" stroke="#8a5a2a" stroke-width="14" opacity=".35"/>')   # coffee ring
    o.append(f'<path d="M0,{H*0.33:.0f}L{W},{H*0.31:.0f}" stroke="#000" stroke-width="3" opacity=".12"/><path d="M{W*0.5:.0f},0L{W*0.52:.0f},{H}" stroke="#000" stroke-width="3" opacity=".1"/>')
    o.append(blot(r, W, H, 40, ['#3a2a1a', '#6a5a3a'], 10, 50, (0.03, 0.1)))
    o.append(f'<path d="M0,{H-30}l40,30h-40z M{W-60},0l60,0l0,50z" fill="#d8cfb8"/>')
    return svg(W, H, ''.join(o), font=True)

def bench_top(W=2048, H=1024):
    """2.6 x 1.0 m steel welding table top: scale, spatter, chalk, burn rainbow."""
    r = R(93); o = [f'<rect width="{W}" height="{H}" fill="#8e8a84"/>', blot(r, W, H, 120, ['#3a3836', '#9a9690', '#7a4a2a'], 10, 80, (0.08, 0.22))]
    for _ in range(900): x, y = r.uniform(0, W), r.uniform(0, H); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5,5):.1f}" fill="{r.choice(["#2a2826","#d8d4cc","#5a3a1a"])}"/>')
    for _ in range(160): x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.28); L = r.uniform(20, 140); o.append(f'<path d="M{x:.0f},{y:.0f}l{math.cos(a)*L:.0f},{math.sin(a)*L:.0f}" stroke="{r.choice(["#c8c4bc","#3a3836"])}" stroke-width="{r.uniform(1,3):.1f}" opacity=".6"/>')
    for _ in range(8): x, y = r.uniform(60, W - 60), r.uniform(60, H - 60); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(25,50):.0f}" fill="#3a5ab0" opacity=".2"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(10,25):.0f}" fill="#c8a040" opacity=".25"/>')
    for _ in range(6): x, y = r.uniform(60, W - 200), r.uniform(60, H - 60); o.append(f'<path d="M{x:.0f},{y:.0f}h{r.uniform(80,200):.0f}m-30,-15v30" stroke="#f4f0e4" stroke-width="4" opacity=".75"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#3a3836" stroke-width="16"/>')
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- pole, transformer, far tower, billboard
def pole(W=256, H=2048):
    """Concrete pole face (0.32 m x 11 m): stencil numbers, posters, stickers, cable stains."""
    r = R(101); k = W / 0.32; Z = lambda z: (11 - z) * k
    o = [f'<rect width="{W}" height="{H}" fill="#a8a49a"/>', blot(r, W, H, 80, ['#5a564e', '#c8c2b4', '#3a4a2a'], 10, 60, (0.06, 0.16))]
    o.append(streaks(r, 0, W, 0, H, W, '#3a3a30', 16, (0.05, 0.15)))
    o.append(T(W / 2, Z(2.7), 54, '17/42', '#1a1a1a', k=True))
    o.append(f'<rect x="20" y="{Z(2.45):.0f}" width="{W-40}" height="60" fill="#e8c020"/>' + T(W / 2, Z(2.45) + 46, 40, 'อันตราย', '#1a1a1a', k=True))
    y = Z(2.1)
    for i in range(6):                              # layered posters / stickers, torn
        h = r.uniform(70, 160); c = r.choice(['#f4f0e0', '#f0e040', '#f4c0c0', '#c0e0f4', '#fff'])
        o.append(f'<g transform="rotate({r.uniform(-5,5):.0f} {W/2} {y:.0f})"><rect x="{r.uniform(5,30):.0f}" y="{y:.0f}" width="{W*0.8:.0f}" height="{h:.0f}" fill="{c}"/>'
                 f'<rect x="20" y="{y+12:.0f}" width="{W*0.6:.0f}" height="16" fill="{r.choice(["#c02020","#1a1a1a","#2040a0"])}"/><rect x="20" y="{y+40:.0f}" width="{W*0.5:.0f}" height="9" fill="#333"/><rect x="20" y="{y+58:.0f}" width="{W*0.4:.0f}" height="9" fill="#333"/></g>')
        y += h * r.uniform(0.5, 0.9)
    for _ in range(30): x, yy = r.uniform(0, W), r.uniform(Z(2.4), H); o.append(f'<rect x="{x:.0f}" y="{yy:.0f}" width="{r.uniform(10,40):.0f}" height="{r.uniform(5,20):.0f}" fill="#f4f0e0" opacity=".6"/>')
    return svg(W, H, ''.join(o), font=True)

def transformer(W=512, H=512):
    r = R(111); o = [f'<rect width="{W}" height="{H}" fill="#7e8a86"/>', blot(r, W, H, 50, ['#3a3a32', '#a8b0aa', '#7a4a22'], 10, 50, (0.08, 0.2))]
    for i in range(14): o.append(f'<rect x="{i*W/14:.0f}" y="0" width="{W/28:.0f}" height="{H}" fill="#000" opacity=".18"/>')
    o.append(f'<rect x="{W*0.3:.0f}" y="{H*0.3:.0f}" width="{W*0.4:.0f}" height="{H*0.28:.0f}" fill="#f2d020" stroke="#1a1a1a" stroke-width="6"/>' + T(W / 2, H * 0.4, 38, 'อันตราย', '#c8281e', k=True) + T(W / 2, H * 0.52, 26, 'ไฟฟ้าแรงสูง', '#1a1a1a'))
    o.append(f'<rect x="{W*0.36:.0f}" y="{H*0.66:.0f}" width="{W*0.28:.0f}" height="{H*0.1:.0f}" fill="#d8d8d0"/>' + T(W / 2, H * 0.73, 22, '160 kVA  No.4471', '#1a1a1a'))
    o.append(streaks(r, 0, W, 0, H, 60, '#5a3a1a', 18, (0.1, 0.3)))
    return svg(W, H, ''.join(o), font=True)

def tower_facade(W=2048, H=2048, wm=20.0, hm=24.5):
    """7-storey apartment block front (20 x 24.5 m): window grid, AC units, laundry, grime, ground-floor shops."""
    r = R(121); kx = W / wm; ky = H / hm; Z = lambda z: (hm - z) * ky
    o = [f'<rect width="{W}" height="{H}" fill="#c9c3b6"/>', blot(r, W, H, 200, ['#5a564a', '#8a8070', '#e8e2d4', '#3a4a30'], 20, 160, (0.05, 0.14))]
    for f in range(7):
        z0 = 3.5 * f
        o.append(f'<rect x="0" y="{Z(z0+0.35):.0f}" width="{W}" height="{0.35*ky:.0f}" fill="#9a9488"/>')
        if f == 0:
            for i in range(5):
                x = (0.4 + i * 3.9) * kx; c = r.choice(['#3a4a6a', '#5a3a2a', '#2a2a2a'])
                o.append(f'<rect x="{x:.0f}" y="{Z(3.0):.0f}" width="{3.4*kx:.0f}" height="{3.0*ky:.0f}" fill="{c}"/><rect x="{x:.0f}" y="{Z(3.4):.0f}" width="{3.4*kx:.0f}" height="{0.5*ky:.0f}" fill="{r.choice(["#c8281e","#1e5aa0","#f0c030"])}"/>')
            continue
        for i in range(8):
            x = (0.55 + i * 2.45) * kx; zz = z0 + 1.0; lit = r.random() < 0.15
            o.append(f'<rect x="{x:.0f}" y="{Z(zz+1.5):.0f}" width="{1.5*kx:.0f}" height="{1.5*ky:.0f}" fill="{"#e8c878" if lit else r.choice(["#2a3242","#36404e","#4a4a52"])}"/>')
            if r.random() < 0.6: o.append(f'<rect x="{x:.0f}" y="{Z(zz+1.5):.0f}" width="{r.uniform(0.3,0.75)*kx:.0f}" height="{1.5*ky:.0f}" fill="{r.choice(["#e07a8a","#7aa0d8","#e8c860","#f0ece0"])}" opacity=".85"/>')
            o.append(f'<path d="M{x:.0f},{Z(zz+0.75):.0f}h{1.5*kx:.0f}M{x+0.75*kx:.0f},{Z(zz+1.5):.0f}v{1.5*ky:.0f}" stroke="#d8d8d0" stroke-width="5"/>')
            for g in range(5): o.append(f'<path d="M{x+g*0.375*kx:.0f},{Z(zz+1.5):.0f}v{1.5*ky:.0f}" stroke="#e8e8e0" stroke-width="3" opacity=".8"/>')
            o.append(streaks(r, x, x + 1.5 * kx, Z(zz), 1.6 * ky, kx, '#3a3226', 4, (0.1, 0.25)))
            if r.random() < 0.5: o.append(f'<rect x="{x+1.6*kx:.0f}" y="{Z(zz+0.7):.0f}" width="{0.7*kx:.0f}" height="{0.5*ky:.0f}" fill="#e4e2da" stroke="#777" stroke-width="3"/><circle cx="{x+1.9*kx:.0f}" cy="{Z(zz+0.45):.0f}" r="{0.18*kx:.0f}" fill="#555"/>')
            if r.random() < 0.3:
                for c in range(4): o.append(f'<rect x="{x+c*0.38*kx:.0f}" y="{Z(zz+0.05):.0f}" width="{0.3*kx:.0f}" height="{0.6*ky:.0f}" fill="{r.choice(["#e83a2a","#3a8ae0","#f0c030","#fff","#30b050"])}"/>')
    o.append(f'<rect x="{W*0.3:.0f}" y="{Z(5.4):.0f}" width="{W*0.4:.0f}" height="{1.1*ky:.0f}" fill="#1e5aa0"/>' + T(W / 2, Z(4.6), 0.75 * ky, 'ร่วมใจ แมนชั่น', '#fff', k=True))
    o.append(f'<rect x="0" y="0" width="{W}" height="{0.4*ky:.0f}" fill="#3a3a32" opacity=".5"/>')
    o.append(streaks(r, 0, W, 0, H * 0.4, kx, '#3a3a2a', 40, (0.05, 0.15)))
    return svg(W, H, ''.join(o), font=True)

def billboard(W=1024, H=384):
    r = R(131); o = [f'<rect width="{W}" height="{H}" fill="#e8e2d0"/><rect x="0" y="0" width="{W*0.55:.0f}" height="{H}" fill="#2a8ad0"/>',
                     f'<circle cx="{W*0.28:.0f}" cy="{H*0.5:.0f}" r="{H*0.34:.0f}" fill="#f0c030"/>', T(W * 0.28, H * 0.6, 80, 'ว่าง', '#c8281e', k=True),
                     T(W * 0.78, H * 0.42, 70, 'ให้เช่าป้าย', '#1a1a1a', k=True), T(W * 0.78, H * 0.7, 56, '02-418-7731', '#c8281e', k=True)]
    for _ in range(9):                              # torn vinyl strips
        x = r.uniform(0, W); o.append(f'<path d="M{x:.0f},0l{r.uniform(-30,30):.0f},{r.uniform(80,300):.0f}l{r.uniform(20,60):.0f},0l{r.uniform(-20,20):.0f},{-r.uniform(80,300):.0f}z" fill="#8a8a80"/>')
    o.append(streaks(r, 0, W, 0, H, 60, '#3a2a1a', 30, (0.1, 0.3)))
    return svg(W, H, ''.join(o), font=True)

# ----------------------------------------------------------------------------- nature, cloth, misc
def banana_leaf(W=512, H=1024):
    """Two banana leaves side by side (each 256 x 1024), transparent: one whole, one torn into strips. Leaf axis = image y."""
    r = R(141); o = []; cuts = []
    for li in range(2):
        cx = li * 256 + 128; top, bot = 30, H - 10; e = []
        d = f'M{cx},{bot}C{cx-125},{bot-200} {cx-125},{top+150} {cx},{top}C{cx+125},{top+150} {cx+125},{bot-200} {cx},{bot}Z'
        e.append(f'<path d="{d}" fill="{"#4f9a3a" if li == 0 else "#6aa83e"}"/>')
        e.append(f'<path d="M{cx},{top}C{cx-120},{top+150} {cx-120},{bot-200} {cx},{bot}Z" fill="#3a7a2c" opacity=".55"/>')
        for i in range(30):
            y = top + 40 + i * (bot - top - 60) / 30
            e.append(f'<path d="M{cx},{y:.0f}q-60,-12 -120,-40M{cx},{y:.0f}q60,-12 120,-40" stroke="#2e6a22" stroke-width="2" opacity=".5"/>')
        for _ in range(8):
            y = r.uniform(top + 60, bot - 60); side = r.choice([-1, 1])
            e.append(f'<ellipse cx="{cx+side*105:.0f}" cy="{y:.0f}" rx="35" ry="60" fill="#a88a3a" opacity=".6"/>')
        e.append(f'<path d="M{cx},{top}V{bot}" stroke="#c8d890" stroke-width="10"/>')
        for _ in range(10 if li else 4):
            y = r.uniform(top + 120, bot - 80); side = r.choice([-1, 1])
            cuts.append(f'<path d="M{cx+side*8},{y:.0f}q{side*60},-14 {side*130},-46l0,{r.uniform(5,12):.0f}q{-side*70},30 {-side*130},50z" fill="#000"/>')
        o.append(f'<clipPath id="l{li}"><path d="{d}"/></clipPath><g clip-path="url(#l{li})">' + ''.join(e) + '</g>')
    return svg(W, H, f'<defs><mask id="cut"><rect width="{W}" height="{H}" fill="#fff"/>{"".join(cuts)}</mask></defs><g mask="url(#cut)">' + ''.join(o) + '</g>')

def leaves(W=512):
    """A leafy cluster card for potted plants (transparent)."""
    r = R(151); o = []
    for _ in range(46):
        x, y = r.uniform(80, W - 80), r.uniform(90, W - 40); a = r.uniform(0, 360); s = r.uniform(40, 90)
        c = r.choice(['#3a8a3a', '#2e6e2e', '#5aa848', '#4a9a3a', '#6ab84a'])
        o.append(f'<g transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})"><path d="M0,0C{s*0.4:.0f},{-s*0.3:.0f} {s*0.8:.0f},{-s*0.2:.0f} {s:.0f},0C{s*0.8:.0f},{s*0.2:.0f} {s*0.4:.0f},{s*0.3:.0f} 0,0Z" fill="{c}"/><path d="M0,0H{s:.0f}" stroke="#1e4a1e" stroke-width="2"/></g>')
    for _ in range(5): x = r.uniform(150, W - 150); o.append(f'<circle cx="{x:.0f}" cy="{r.uniform(100,300):.0f}" r="14" fill="{r.choice(["#e83a6a","#f0c030","#ffffff","#e85a2a"])}"/>')
    return svg(W, W, ''.join(o))

def laundry(W=512, H=512):
    """4 x 2 cells (128 x 256) of hanging clothes, transparent: shirts, sarong, towel, trousers."""
    r = R(161); o = []
    for i in range(8):
        x, y = (i % 4) * 128, (i // 4) * 256; c = r.choice(['#e83a2a', '#2a6ad0', '#f0c030', '#ffffff', '#30a060', '#e880b0', '#1a1a2a', '#f08030'])
        kind = i % 4
        if kind == 0:   # t-shirt
            o.append(f'<path d="M{x+20},{y+20}l30,-12h28l30,12l14,40l-22,8v170h-72v-170l-22,-8z" fill="{c}"/><path d="M{x+50},{y+8}q14,16 28,0" stroke="#000" stroke-width="4" fill="none" opacity=".3"/>')
        elif kind == 1:   # sarong with pattern
            o.append(f'<rect x="{x+10}" y="{y+6}" width="108" height="240" fill="{c}"/>')
            for j in range(8): o.append(f'<path d="M{x+10},{y+20+j*30}h108" stroke="{r.choice(["#ffffff","#1a1a1a","#f0c030"])}" stroke-width="7" opacity=".7"/>')
        elif kind == 2:   # towel
            o.append(f'<rect x="{x+14}" y="{y+6}" width="100" height="200" fill="{c}"/><rect x="{x+14}" y="{y+170}" width="100" height="14" fill="#fff" opacity=".6"/>')
        else:   # trousers
            o.append(f'<path d="M{x+24},{y+6}h80l10,240h-40l-10,-170l-10,170h-40z" fill="{r.choice(["#2a3a6a","#5a4a3a","#1a1a1a"])}"/>')
        o.append(f'<rect x="{x}" y="{y}" width="128" height="256" fill="url(#sh)" opacity="0"/>')
        o.append(f'<path d="M{x+10},{y+240}h108" stroke="#000" stroke-width="0" />')
    return svg(W, H, ''.join(o))

def tin(seed, base='#9a9690', W=512):
    """Corrugated sheet (2 m), rusty."""
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="{base}"/>']
    for i in range(32): o.append(f'<rect x="{i*W/32:.0f}" y="0" width="{W/64:.0f}" height="{W}" fill="#fff" opacity=".18"/><rect x="{i*W/32+W/64:.0f}" y="0" width="{W/64:.0f}" height="{W}" fill="#000" opacity=".15"/>')
    o.append(blot(r, W, W, 30, ['#8a4a1a', '#6a3a14'], 10, 40, (0.12, 0.3), 0.4))
    for _ in range(26): y0 = r.uniform(-50, W * 0.6); o.append(streaks(r, 0, W, y0, r.uniform(80, 300), 20, r.choice(['#7a3a10', '#8a4a1a', '#5a2a0a']), 3, (0.25, 0.55)))
    o.append(f'<rect x="0" y="0" width="{W}" height="18" fill="#6a3010" opacity=".5"/>')
    return svg(W, W, ''.join(o))

def planks(seed, base='#7a5434', W=512, H=1024, n=8, vertical=True):
    r = R(seed); o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']; w = W / n
    for i in range(n):
        c = r.choice(['#7a5434', '#6a4628', '#86603c', '#5e4026', '#8a6a4a'])
        o.append(f'<rect x="{i*w+2:.0f}" y="0" width="{w-4:.0f}" height="{H}" fill="{c}"/>')
        for _ in range(6): y = r.uniform(0, H); o.append(f'<path d="M{i*w+6:.0f},{y:.0f}q{w*0.4:.0f},{r.uniform(-30,30):.0f} {w-12:.0f},0" stroke="#3a2414" stroke-width="2" fill="none" opacity=".5"/>')
        o.append(f'<rect x="{i*w:.0f}" y="0" width="4" height="{H}" fill="#2a180c"/>')
    o.append(blot(r, W, H, 50, ['#2a2014', '#a89a80'], 15, 70, (0.08, 0.2)))
    return svg(W, H, ''.join(o))

def bike_body(W=512, H=256):
    """Scooter body panel colour with stripes and a generic 110 decal."""
    o = [f'<rect width="{W}" height="{H}" fill="#c82a24"/><path d="M0,{H*0.55:.0f}C{W*0.3:.0f},{H*0.35:.0f} {W*0.6:.0f},{H*0.75:.0f} {W},{H*0.5:.0f}" stroke="#f4f0e8" stroke-width="18" fill="none"/>',
         f'<path d="M0,{H*0.7:.0f}C{W*0.3:.0f},{H*0.5:.0f} {W*0.6:.0f},{H*0.9:.0f} {W},{H*0.65:.0f}" stroke="#1a1a1a" stroke-width="12" fill="none"/>', T(W * 0.7, H * 0.38, 60, '110', '#f4f0e8', k=True)]
    r = R(171); o.append(blot(r, W, H, 25, ['#3a1a10', '#ffffff'], 10, 40, (0.05, 0.15)))
    return svg(W, H, ''.join(o), font=True)

def crate(W=256):
    o = [f'<rect width="{W}" height="{W}" fill="#c8302a"/>']
    for i in range(4):
        for j in range(3): o.append(f'<rect x="{20+i*58}" y="{40+j*66}" width="40" height="46" rx="8" fill="#5a1210"/>')
    return svg(W, W, ''.join(o))

def spirit(W=512):
    """Gold/red ornament for the spirit house walls and roof edges."""
    r = R(181); o = [f'<rect width="{W}" height="{W}" fill="#c8302a"/>']
    for i in range(8):
        for j in range(8):
            x, y = i * 64 + 32, j * 64 + 32; o.append(f'<path d="M{x},{y-24}l20,24l-20,24l-20,-24z" fill="#f2c040"/><circle cx="{x}" cy="{y}" r="6" fill="#2a8a5a"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="40" fill="#f2c040"/><rect x="0" y="{W-40}" width="{W}" height="40" fill="#f2c040"/>')
    o.append(blot(r, W, W, 20, ['#3a1a0a'], 20, 60, (0.06, 0.15)))
    return svg(W, W, ''.join(o))

def concrete(seed, base='#a8a296', W=512):
    r = R(seed); o = [f'<rect width="{W}" height="{W}" fill="{base}"/>', blot(r, W, W, 120, ['#5a564e', '#c8c2b4', '#3a4a2a'], 10, 70, (0.05, 0.14))]
    for _ in range(4): o.append(crack(r, r.uniform(0, W), r.uniform(0, W), 6, 30, w=1.6))
    o.append(streaks(r, 0, W, 0, W, 40, '#3a3a30', 14, (0.05, 0.15)))
    return svg(W, W, ''.join(o))

# ----------------------------------------------------------------------------- skies (equirectangular, 2:1; centre column = -x, 3/4 = +y down the soi)
def _clouds(r, cx, cy, s, body, rim, shade, n=9, flat=0.55, lit=(-0.5, -0.8)):
    """Toon cloud mass: a union of puffs in three tones (shade underneath, body, sunlit rim clipped to the body)."""
    pu = []
    for _ in range(n):
        dx = r.uniform(-1, 1) * s; dy = r.uniform(-0.55, 0.15) * s * flat * 1.4 - abs(dx) * 0.0; rr = r.uniform(0.3, 0.62) * s * (1.0 - 0.35 * abs(dx) / s)
        pu.append((cx + dx, cy + dy, rr))
    pu.append((cx, cy + 0.05 * s, 1.05 * s * flat * 0.7)); cid = f'c{r.randrange(10**9)}'
    circ = lambda ox, oy, k=1.0: ''.join(f'<circle cx="{x+ox:.0f}" cy="{y+oy:.0f}" r="{rr*k:.0f}"/>' for x, y, rr in pu)
    base = max(y + rr * 0.55 for x, y, rr in pu)
    o = [f'<defs><clipPath id="{cid}">{circ(0, 0)}<rect x="{cx-2*s:.0f}" y="0" width="0" height="0"/></clipPath></defs>',
         f'<g fill="{shade}">{circ(s*0.05, s*0.12)}</g>', f'<g fill="{body}">{circ(0, 0)}</g>',
         f'<g clip-path="url(#{cid})"><g fill="{shade}" opacity=".55"><rect x="{cx-2*s:.0f}" y="{base-s*0.25:.0f}" width="{4*s:.0f}" height="{s:.0f}"/></g><g fill="{rim}">{circ(lit[0]*s*0.16, lit[1]*s*0.16, 0.66)}</g></g>']
    return ''.join(o)

def sky(kind, W=4096, H=2048):
    r = R({'storm': 7, 'day': 8, 'night': 9, 'evening': 10}[kind]); o = []
    hz = H / 2
    if kind == 'storm':
        o.append('<defs><linearGradient id="z" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e2c5e"/><stop offset=".35" stop-color="#4e4c84"/><stop offset=".47" stop-color="#e8a878"/><stop offset=".5" stop-color="#f6c890"/><stop offset="1" stop-color="#6a5a6a"/></linearGradient>'
                 '<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff2c8"/><stop offset=".25" stop-color="#ffd890" stop-opacity=".85"/><stop offset="1" stop-color="#ff9a60" stop-opacity="0"/></radialGradient>'
                 '<linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2a58"/><stop offset=".7" stop-color="#3a3670"/><stop offset="1" stop-color="#4c4278"/></linearGradient>'
                 '<filter id="b"><feGaussianBlur stdDeviation="14"/></filter><filter id="b2"><feGaussianBlur stdDeviation="40"/></filter></defs>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#z)"/>')
        sx, sy = 0.22 * W, hz - 23.6 / 180 * H; f = W / 4096
        o.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{620*f:.0f}" fill="url(#sun)"/><circle cx="{sx+W:.0f}" cy="{sy:.0f}" r="{620*f:.0f}" fill="url(#sun)"/>')
        for _ in range(60):                          # warm lit cumulus on the sun side (u 0..0.5)
            x, y = r.uniform(0.0, 0.58) * W, r.uniform(hz - 0.3 * H, hz - 0.03 * H); s = r.uniform(40, 120) * W / 4096
            o.append(_clouds(r, x, y, s, '#d8a090', '#ffe2b8', '#8a6a8e', 8, 0.5))
        # the storm mass over +y (u 0.5 .. 1.0), dark purple-blue, towering, with warm-lit tops
        o.append(f'<g filter="url(#b2)"><ellipse cx="{0.76*W:.0f}" cy="{hz-0.12*H:.0f}" rx="{0.3*W:.0f}" ry="{0.24*H:.0f}" fill="#2c3060" opacity=".85"/></g>')
        f = W / 4096
        masses = sorted([(r.gauss(0.74, 0.11), r.uniform(0.0, 1.0)) for _ in range(190)], key=lambda m: -m[1])
        for (u, t) in masses:                        # back to front: high towers first, lower masses over them
            env = math.exp(-((u - 0.74) / 0.21) ** 2); y = hz - (0.03 + 0.36 * t * env) * H; sz = (60 + 90 * env) * r.uniform(0.7, 1.3) * f
            hi_ = t > 0.6 and env > 0.3
            o.append(_clouds(r, u * W, y, sz, '#3a386c' if hi_ else '#2e2b5e', '#e8a07c' if hi_ else '#48467e', '#1d1b3e', 12, 0.75))
        for _ in range(110):                         # the anvil spreading overhead toward the camera side (elevation 45..80 deg)
            u = r.uniform(0.38, 1.05) % 1.0; el = r.uniform(45, 82) - 25 * max(0, 0.55 - u) * 2; y = (90 - el) / 180 * H; sz = r.uniform(70, 160) * f * (1 + (el - 45) / 30)
            o.append(_clouds(r, u * W, y, sz, '#34326a', '#4e4c88', '#24224a', 10, 0.45, (0.6, 0.5)))
        for _ in range(70):                          # ragged dark scud along the base
            u = r.uniform(0.52, 0.98); y = hz - r.uniform(0.02, 0.07) * H; sz = r.uniform(40, 90) * f
            o.append(_clouds(r, u * W, y, sz, '#2c2e5a', '#464a80', '#1f2144', 9, 0.4))
        o.append(f'<rect x="{0.5*W:.0f}" y="{hz-0.045*H:.0f}" width="{0.5*W:.0f}" height="{0.05*H:.0f}" fill="#202448"/>' + ''.join(f'<circle cx="{0.5*W+i*W/180:.0f}" cy="{hz-0.045*H:.0f}" r="{r.uniform(0.012,0.03)*H:.0f}" fill="#202448"/>' for i in range(91)))
        for i in range(40):                          # rain shafts
            x = r.uniform(0.6, 0.95) * W; o.append(f'<path d="M{x:.0f},{hz-0.05*H:.0f}l{-60:.0f},{0.06*H:.0f}" stroke="#5a5a8a" stroke-width="{r.uniform(10,40)*W/4096:.0f}" opacity=".25" filter="url(#b)"/>')
        o.append(f'<rect x="0" y="{hz:.0f}" width="{W}" height="{hz:.0f}" fill="#5a4a62"/>')
    elif kind == 'day':
        o.append('<defs><linearGradient id="z" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a6ad0"/><stop offset=".38" stop-color="#5aa0e8"/><stop offset=".5" stop-color="#cfe6f4"/><stop offset="1" stop-color="#9ab0c0"/></linearGradient></defs>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#z)"/>')
        for _ in range(110):
            x, y = r.uniform(0, W), r.uniform(hz - 0.3 * H, hz - 0.03 * H); s = r.uniform(40, 130)
            o.append(_clouds(r, x, y, s, '#e8eef6', '#ffffff', '#a8bad2', 9, 0.5))
    elif kind == 'evening':
        # just after sunset behind the 7-storey block (+y, u 0.75): deep blue-violet zenith, dusk blue, a warm band low over the block
        # that fades through peach into a greyed lavender (never through saturated pink), lit undersides of a few streaks, first stars, a young moon
        o.append('<defs><linearGradient id="z" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121236"/><stop offset=".22" stop-color="#1e2058"/>'
                 '<stop offset=".36" stop-color="#2e3474"/><stop offset=".44" stop-color="#4a5490"/><stop offset=".485" stop-color="#7a7c9e"/><stop offset=".5" stop-color="#b08a7a"/>'
                 '<stop offset="1" stop-color="#2a2a40"/></linearGradient>'
                 '<radialGradient id="glow" cx=".5" cy="1" r="1" fx=".5" fy="1"><stop offset="0" stop-color="#ffc070"/><stop offset=".22" stop-color="#ffa050" stop-opacity=".95"/>'
                 '<stop offset=".45" stop-color="#f29c62" stop-opacity=".85"/><stop offset=".68" stop-color="#b8968e" stop-opacity=".55"/><stop offset="1" stop-color="#5a5a90" stop-opacity="0"/></radialGradient>'
                 '<radialGradient id="m" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f4f2e0" stop-opacity=".6"/><stop offset="1" stop-color="#8090c0" stop-opacity="0"/></radialGradient>'
                 '<filter id="b"><feGaussianBlur stdDeviation="10"/></filter></defs>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#z)"/>')
        gx, gw, gh = 0.75 * W, 0.3 * W, 0.26 * H
        for sh in (0.0, -W, W): o.append(f'<ellipse cx="{gx+sh:.0f}" cy="{hz:.0f}" rx="{gw:.0f}" ry="{gh:.0f}" fill="url(#glow)"/>')
        for _ in range(26):                          # thin altostratus streaks: warm-lit undersides near the glow, blue-violet away from it
            u = r.gauss(0.75, 0.14) % 1.0; el = r.uniform(6, 34); y = hz - el / 180 * H; L = r.uniform(120, 420) * W / 4096; t = r.uniform(4, 14) * W / 4096
            near = math.exp(-((u - 0.75) / 0.12) ** 2) * math.exp(-el / 22)
            col = '#f2a86a' if near > 0.35 else ('#a88aa0' if near > 0.12 else '#3a3c70'); body = '#2a2c60' if near < 0.35 else '#5a4a78'
            o.append(f'<g filter="url(#b)" opacity=".85"><ellipse cx="{u*W:.0f}" cy="{y:.0f}" rx="{L:.0f}" ry="{t*1.6:.0f}" fill="{body}"/></g><ellipse cx="{u*W:.0f}" cy="{y+t*0.8:.0f}" rx="{L*0.8:.0f}" ry="{t*0.5:.0f}" fill="{col}" opacity=".8"/>')
        for _ in range(220): o.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,hz*0.55):.0f}" r="{r.uniform(1,2.4):.1f}" fill="#fff" opacity="{r.uniform(.25,.8):.2f}"/>')
        for _ in range(64):                          # toon cloud banks (u 0.35 .. 0.95, elevation 28 .. 78 deg): blue-violet bodies, a dusky warm rim only low toward the sunset
            u = r.uniform(0.35, 0.95); el = r.uniform(28, 78); y = hz - el / 180 * H; sz = r.uniform(34, 80) * W / 4096 * (1 + (el - 28) / 50)
            warm = el < 44 and abs(u - 0.75) < 0.1
            o.append(_clouds(r, u * W, y, sz, '#2a2b62', '#a8806e' if warm else '#3c3e7a', '#1d1d4a', 9, 0.4, (0.0, 0.9)))
        for _ in range(18):                          # high thin cloudlets over the top of the frame
            u = r.uniform(0.6, 0.9); el = r.uniform(58, 84); y = hz - el / 180 * H; sz = r.uniform(30, 70) * W / 4096
            o.append(_clouds(r, u * W, y, sz, '#23245a', '#34367a', '#1a1a44', 7, 0.3, (0.0, 0.9)))
        mx, my = 0.62 * W, hz - 0.30 * H; o.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="160" fill="url(#m)"/><circle cx="{mx:.0f}" cy="{my:.0f}" r="34" fill="#f6f2dc"/><circle cx="{mx+12:.0f}" cy="{my-6:.0f}" r="31" fill="#262a66"/>')
        o.append(f'<rect x="0" y="{hz:.0f}" width="{W}" height="{hz:.0f}" fill="#2a2a40"/>')
    else:
        o.append('<defs><linearGradient id="z" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0c22"/><stop offset=".45" stop-color="#1a1e44"/><stop offset=".5" stop-color="#2a2a52"/><stop offset="1" stop-color="#14142a"/></linearGradient>'
                 '<radialGradient id="m" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e8ecff"/><stop offset=".2" stop-color="#c8d0f0" stop-opacity=".6"/><stop offset="1" stop-color="#8090c0" stop-opacity="0"/></radialGradient></defs>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#z)"/>')
        for _ in range(500): o.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,hz-40):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#fff" opacity="{r.uniform(.3,.9):.2f}"/>')
        mx, my = 0.2 * W, hz - 0.22 * H; o.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="300" fill="url(#m)"/><circle cx="{mx:.0f}" cy="{my:.0f}" r="44" fill="#f4f4ff"/>')
        for _ in range(30):
            x, y = r.uniform(0.45, 1.0) * W, r.uniform(hz - 0.3 * H, hz - 0.03 * H); s = r.uniform(120, 300)
            o.append(_clouds(r, x, y, s, '#1e1e40', '#3a3e6e', '#141430', 9))
    return svg(W, H, ''.join(o))

def phone(W=128, H=256):
    return svg(W, H, f'<rect width="{W}" height="{H}" rx="14" fill="#cfe4ff"/><rect x="10" y="30" width="{W-20}" height="60" fill="#fff"/><rect x="10" y="100" width="{W-20}" height="120" fill="#8ab8f0"/>')

# ----------------------------------------------------------------------------- job table
WALLS = ['#e9dcc0', '#e8c4b8', '#bcd8c0', '#bcd0dc', '#f0d890', '#e8a888', '#cfc9bd', '#d8c0e0']
JOBS = dict(
    road_a=(lambda: road(1), 1024, 4096, False), road_b=(lambda: road(2, slow=True), 1024, 4096, False),
    tile_red=(lambda: tiles(3, '#b8603e', '#6a3a2a', cols=['#b8603e', '#a8583a', '#c06a44']), 512, 512, False),
    tile_grey=(lambda: tiles(4, '#a8a69e', '#5a5850', cols=['#a8a69e', '#b4b2aa', '#9e9c94']), 512, 512, False),
    tile_white=(lambda: tiles(5, '#e0dcd0', '#8a8678', n=6, cols=['#e0dcd0', '#d8d4c6', '#e8e4d8']), 512, 512, False),
    hero_floor=(hero_floor, 1024, 1024, False), gutter=(gutter, 512, 128, False), curb=(curb, 512, 64, False), manhole=(manhole, 256, 256, False),
    fac_hero=(lambda: facade(200, '#e8e0c8', 2048, 2816, 8.0, hero=True), 2048, 2816, False),
    **{f'fac{i}': ((lambda i=i: facade(210 + i, WALLS[i])), 512, 1408, False) for i in range(8)},
    **{f'pier{i}': ((lambda i=i: pier(230 + i, WALLS[i])), 128, 1408, False) for i in range(8)},
    shut_grey=(lambda: shutter(1, '#9aa0a4'), 512, 512, False), shut_green=(lambda: shutter(2, '#5a8a72'), 512, 512, False),
    shut_blue=(lambda: shutter(3, '#4a72a0'), 512, 512, False), shut_rust=(lambda: shutter(4, '#a0603a'), 512, 512, False),
    grille_sun=(lambda: grille('sun', '#f2efe6'), 512, 512, True), grille_dia=(lambda: grille('diamond', '#2a2a2e'), 512, 512, True),
    grille_tul=(lambda: grille('tulip', '#3a7a5a'), 512, 512, True),
    **{f'win{i}': ((lambda i=i: window(300 + i)), 256, 320, False) for i in range(6)},
    ac=(ac_front, 256, 192, False), sign_hero=(sign_hero, 2048, 416, False), sign_board=(sign_board, 1024, 512, False),
    signs=(signs_atlas, 1024, 2048, False), soi_sign=(soi_sign, 512, 256, False), posters=(posters, 1024, 1024, False),
    interiors=(interiors, 1024, 1024, False), hero_wall=(hero_wall, 2048, 1024, False),
    gate_black=(lambda: gate('black'), 1024, 1024, True), gate_white=(lambda: gate('white'), 1024, 1024, True), gate_green=(lambda: gate('green'), 1024, 1024, True),
    gate_red=(lambda: gate('red'), 1024, 1024, True), gate_raw=(lambda: gate('raw'), 1024, 1024, True),
    slip=(slip, 768, 1024, False), bench_top=(bench_top, 2048, 1024, False), pole=(pole, 256, 2048, False), transformer=(transformer, 512, 512, False),
    tower=(tower_facade, 2048, 2048, False), billboard=(billboard, 1024, 384, False), banana=(banana_leaf, 512, 1024, True), leaves=(leaves, 512, 512, True),
    laundry=(laundry, 512, 512, True), tin=(lambda: tin(191), 512, 512, False), tin_blue=(lambda: tin(192, '#5a7aa8'), 512, 512, False),
    planks=(lambda: planks(193), 512, 1024, False), bike=(bike_body, 512, 256, False), crate=(crate, 256, 256, False), spirit=(spirit, 512, 512, False),
    concrete=(lambda: concrete(195), 512, 512, False), concrete_dark=(lambda: concrete(196, '#8a857a'), 512, 512, False),
    sky_storm=(lambda: sky('storm', 6144, 3072), 6144, 3072, False), sky_day=(lambda: sky('day'), 4096, 2048, False), sky_night=(lambda: sky('night'), 4096, 2048, False),
    phone=(phone, 128, 256, False),
    sky_evening=(lambda: sky('evening'), 4096, 2048, False), tower_glow=(tower_glow, 2048, 2048, False),
    **{f'win{i}_glow': ((lambda i=i: window_glow(300 + i)), 256, 320, False) for i in range(6)},
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
