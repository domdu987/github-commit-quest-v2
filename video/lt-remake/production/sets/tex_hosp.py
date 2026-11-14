"""SVG artwork for the community-hospital male ward (hosp3d.py), rasterised by Chromium (one launch for all jobs). Cached by content hash in hosp_tex/.
Convention (as tex_soi): SVG y grows downward = texture v goes from 1 (top row) to 0 (bottom row).
World layout the position-dependent artwork is painted for (floor reflections, contact shadows): see hosp3d.ROOM / BEDS."""
import os, json, hashlib, subprocess, math, random
import tex_soi as TS                          # shared helpers: svg(), T() (Kanit text), blot(), crack(), streaks(), _clouds()
HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'hosp_tex')
RASTER = TS.RASTER
svg, T, blot, crack, streaks = TS.svg, TS.T, TS.blot, TS.crack, TS.streaks
R = random.Random

# world numbers shared with hosp3d.py (kept here so the painted floor lines up with the geometry)
X0, X1, Y0, Y1 = -3.5, 3.5, -2.0, 15.0
BED_Y = (1.0, 4.2, 7.4); BED_HEAD = 3.42; BED_LEN = 2.05; BED_W = 0.94; CAB_A = 1.63
WIN_Y = (-0.6, 2.6, 5.8, 9.0, 12.3); WIN_HW = 0.72
FIX_Y = (0.4, 3.0, 5.8, 8.6, 11.2)       # aisle fluorescent battens (centres)

# ----------------------------------------------------------------------------- floor
def floor(k=256):
    """Whole ward floor 7 x 17 m at k px/m: cream-grey terrazzo in 1.0 m bays with brass strips, chips, scuffs, painted reflections
    (window glare streaks, tube-light glints down the aisle, dark mirrored bed legs) and soft contact shadows under beds, cabinets, counter."""
    r = R(11); W, H = int((X1 - X0) * k), int((Y1 - Y0) * k)
    X = lambda x: (x - X0) * k; Yp = lambda y: (Y1 - y) * k
    o = ['<defs>']
    # terrazzo chip pattern (one 1 m bay), three variants
    for v, base in enumerate(['#d9d3c4', '#d3cdbf', '#ddd8ca']):
        rr = R(100 + v); o.append(f'<pattern id="tz{v}" width="{k}" height="{k}" patternUnits="userSpaceOnUse"><rect width="{k}" height="{k}" fill="{base}"/>')
        for _ in range(640):
            x, y = rr.uniform(0, k), rr.uniform(0, k); s = rr.uniform(1.0, 3.4)
            c = rr.choice(['#857d6e', '#9a9282', '#5f5a52', '#f6f2e8', '#b3a68c', '#6d7d76', '#c9ad80', '#4f4a44'])
            o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{s:.1f}" ry="{s*rr.uniform(0.5,1):.1f}" fill="{c}" transform="rotate({rr.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
        o.append('</pattern>')
    o.append('<filter id="b8"><feGaussianBlur stdDeviation="8"/></filter><filter id="b20"><feGaussianBlur stdDeviation="20"/></filter>'
             '<filter id="b40"><feGaussianBlur stdDeviation="40"/></filter><filter id="b3"><feGaussianBlur stdDeviation="3"/></filter></defs>')
    for i in range(int(X1 - X0) + 1):
        for j in range(int(Y1 - Y0) + 1):
            o.append(f'<rect x="{i*k}" y="{j*k}" width="{k}" height="{k}" fill="url(#tz{(i*7+j*3)%3})"/>')
    o.append(blot(r, W, H, 140, ['#a69e8c', '#ece6d8', '#8a8476'], 30, 160, (0.04, 0.10)))
    # brass divider strips every 1 m + 0.5 m sub-grid (lighter)
    for i in range(int(X1 - X0) + 1): o.append(f'<path d="M{i*k},0V{H}" stroke="#a88a52" stroke-width="3.5"/>')
    for j in range(int(Y1 - Y0) + 1): o.append(f'<path d="M0,{j*k}H{W}" stroke="#a88a52" stroke-width="3.5"/>')
    # border band along the walls (darker green-grey terrazzo, 0.25 m)
    for x in (0, W - 0.25 * k): o.append(f'<rect x="{x:.0f}" y="0" width="{0.25*k:.0f}" height="{H}" fill="#5f7068" opacity=".8"/>')
    # contact shadows: beds, cabinets, station counter
    sh = []
    for side in (-1, 1):
        for by in BED_Y:
            xa, xb = sorted((side * BED_HEAD, side * (BED_HEAD - BED_LEN)))
            sh.append(f'<rect x="{X(xa)+10:.0f}" y="{Yp(by+BED_W/2)+6:.0f}" width="{(xb-xa)*k-20:.0f}" height="{BED_W*k-12:.0f}" rx="30" fill="#2a2636" opacity=".62"/>')
            cx = side * (BED_HEAD - CAB_A); cy = by + side * 0.86
            sh.append(f'<rect x="{X(cx-0.26):.0f}" y="{Yp(cy+0.26):.0f}" width="{0.52*k:.0f}" height="{0.52*k:.0f}" rx="12" fill="#2e2a36" opacity=".5"/>')
    sh.append(f'<rect x="{X(-1.7):.0f}" y="{Yp(12.75):.0f}" width="{4.0*k:.0f}" height="{0.75*k:.0f}" fill="#2e2a36" opacity=".45"/>')
    o.append('<g filter="url(#b20)">' + ''.join(sh) + '</g>')
    # painted reflections: mirrored bed legs / frames (dark vertical smears under each bed foot), window glare streaks near the walls,
    # tube-light glints down the aisle
    rf = []
    for side in (-1, 1):
        for by in BED_Y:
            xf = side * (BED_HEAD - BED_LEN)
            for dy in (-0.42, 0.42):
                rf.append(f'<rect x="{X(xf)-0.05*k:.0f}" y="{Yp(by+dy)-6:.0f}" width="{0.1*k:.0f}" height="{0.45*k:.0f}" fill="#4a4652" opacity=".3"/>')
            rf.append(f'<rect x="{X(min(xf, xf+side*0.3)):.0f}" y="{Yp(by+0.48):.0f}" width="{0.3*k:.0f}" height="{0.96*k:.0f}" fill="#6a7090" opacity=".16"/>')
        for wy in WIN_Y:
            xw = side * 3.5; x0 = X(min(xw, xw - side * 1.6))
            rf.append(f'<rect x="{x0:.0f}" y="{Yp(wy+WIN_HW*0.8):.0f}" width="{1.6*k:.0f}" height="{WIN_HW*1.6*k:.0f}" rx="40" fill="#fffaf0" opacity=".30"/>')
    o.append('<g filter="url(#b40)">' + ''.join(rf) + '</g>')
    gl = []
    for fy in FIX_Y:
        gl.append(f'<ellipse cx="{X(0):.0f}" cy="{Yp(fy):.0f}" rx="{0.09*k:.0f}" ry="{0.55*k:.0f}" fill="#ffffff" opacity=".55"/>')
        gl.append(f'<ellipse cx="{X(0):.0f}" cy="{Yp(fy):.0f}" rx="{0.25*k:.0f}" ry="{0.9*k:.0f}" fill="#fffef8" opacity=".22"/>')
    o.append('<g filter="url(#b8)">' + ''.join(gl) + '</g>')
    # polished sheen down the aisle (wide soft band) and wheel tracks
    o.append(f'<rect x="{X(-0.9):.0f}" y="0" width="{1.8*k:.0f}" height="{H}" fill="#fffdf6" opacity=".10" filter="url(#b40)"/>')
    for x in (-0.45, 0.45):
        o.append(f'<path d="M{X(x):.0f},0V{H}" stroke="#6a6458" stroke-width="7" opacity=".07" filter="url(#b3)"/>')
    # scuffs, black heel marks, a few wet footprints near the door (after the storm)
    for _ in range(160):
        x, y = r.uniform(0, W), r.uniform(0, H); L = r.uniform(8, 40)
        o.append(f'<path d="M{x:.0f},{y:.0f}q{L/2:.0f},{r.uniform(-8,8):.0f} {L:.0f},{r.uniform(-4,4):.0f}" stroke="#3a3632" stroke-width="{r.uniform(1.5,3.5):.1f}" fill="none" opacity="{r.uniform(.2,.5):.2f}"/>')
    for i in range(14):
        x, y = X(0.25 * math.sin(i * 0.9) + (0.18 if i % 2 else -0.18)), Yp(-1.6 + i * 0.42)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{0.05*k:.0f}" ry="{0.12*k:.0f}" fill="#8a8a96" opacity=".22"/>')
    # puddle under the ceiling leak (y 9.6) near the right bed row
    px, py = X(1.05), Yp(9.75)
    o.append(f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{0.55*k:.0f}" ry="{0.4*k:.0f}" fill="#b6c4d8" opacity=".55" filter="url(#b3)"/>'
             f'<ellipse cx="{px-20:.0f}" cy="{py-14:.0f}" rx="{0.3*k:.0f}" ry="{0.12*k:.0f}" fill="#ffffff" opacity=".55" filter="url(#b8)"/>')
    for _ in range(10): o.append(crack(r, r.uniform(0, W), r.uniform(0, H), 5, 18, '#7a7468', 1.3, 0.4))
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- walls / ceiling
def wall_low(W=1024, H=256):
    """4 m x 1 m of the lower wall: pale mint glazed tiles (0.2 m), grout, scuffs, a grey vinyl skirting band at the bottom."""
    r = R(21); k = W / 4; o = [f'<rect width="{W}" height="{H}" fill="#7fae9a"/>']
    s = 0.2 * k
    for i in range(int(W / s) + 1):
        for j in range(int(H / s) + 1):
            c = r.choice(['#a8dcc4', '#a2d6be', '#b0e2ca', '#9cd2b9'])
            o.append(f'<rect x="{i*s+1.5:.0f}" y="{j*s+1.5:.0f}" width="{s-3:.0f}" height="{s-3:.0f}" fill="{c}"/>'
                     f'<rect x="{i*s+4:.0f}" y="{j*s+4:.0f}" width="{s*0.5:.0f}" height="3" fill="#eaf6ef" opacity=".7"/>')
    o.append(blot(r, W, H, 50, ['#6a8a7a', '#8aa898'], 8, 40, (0.05, 0.14)))
    o.append(f'<rect x="0" y="{H-0.1*k:.0f}" width="{W}" height="{0.1*k:.0f}" fill="#7f8c88"/><rect x="0" y="{H-0.1*k:.0f}" width="{W}" height="3" fill="#c8d0cc"/>')
    for _ in range(40):
        x = r.uniform(0, W); y = r.uniform(H * 0.55, H * 0.88)
        o.append(f'<path d="M{x:.0f},{y:.0f}h{r.uniform(10,50):.0f}" stroke="#4a5550" stroke-width="{r.uniform(1.5,3):.1f}" opacity=".35"/>')
    return svg(W, H, ''.join(o))

def wall_up(W=1024, H=512):
    """4 m x 2 m of the upper wall: warm off-white paint with faint roller marks, stains and a storm damp patch."""
    r = R(22); o = [f'<rect width="{W}" height="{H}" fill="#f2ecdc"/>', blot(r, W, H, 90, ['#d8ccb4', '#fffaf0', '#cfc4ac'], 20, 120, (0.05, 0.13))]
    for _ in range(26):
        x = r.uniform(0, W); o.append(f'<rect x="{x:.0f}" y="0" width="{r.uniform(30,90):.0f}" height="{H}" fill="#e6dcc6" opacity=".18"/>')
    o.append(streaks(r, 0, W, 0, H * 0.4, 1.0, '#b8a888', 10, (0.05, 0.12)))
    for _ in range(12):
        x, y = r.uniform(0, W), r.uniform(H * 0.3, H); o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,5):.1f}" fill="#9a8e7a" opacity=".5"/>')
    return svg(W, H, ''.join(o))

def ceiling(W=512):
    """1.2 m x 1.2 m of suspended ceiling: four 0.6 m fibre tiles with fissured dots, T-bar grid; one variant carries a brown leak stain."""
    r = R(31); o = [f'<rect width="{W}" height="{W}" fill="#ebe7dc"/>']
    for _ in range(900):
        x, y = r.uniform(0, W), r.uniform(0, W); o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(2,7):.0f}" height="2" fill="#9a9282" opacity=".8" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
    o.append(blot(r, W, W, 20, ['#d4ccb8'], 20, 80, (0.05, 0.12)))
    for t in (0, W / 2, W):
        o.append(f'<path d="M{t:.0f},0V{W}" stroke="#fbfbf8" stroke-width="12"/><path d="M0,{t:.0f}H{W}" stroke="#fbfbf8" stroke-width="12"/>')
        o.append(f'<path d="M{t+7:.0f},0V{W}" stroke="#7a766c" stroke-width="3"/><path d="M0,{t+7:.0f}H{W}" stroke="#7a766c" stroke-width="3"/>')
    return svg(W, W, ''.join(o))

def ceiling_stain(W=512):
    s = ceiling().replace('</svg>', '')
    r = R(32); o = ['<defs><filter id="cs"><feGaussianBlur stdDeviation="10"/></filter></defs>']
    for i, (rr, c, op) in enumerate(((150, '#c49a5a', .35), (110, '#a8783a', .35), (70, '#8a5a2a', .4))):
        pts = ' '.join(f'{W*0.42+math.cos(t)*rr*r.uniform(0.7,1.1):.0f},{W*0.55+math.sin(t)*rr*r.uniform(0.7,1.1):.0f}' for t in [j * 6.283 / 16 for j in range(16)])
        o.append(f'<polygon points="{pts}" fill="{c}" opacity="{op}" filter="url(#cs)"/><polygon points="{pts}" fill="none" stroke="#7a4a1a" stroke-width="3" opacity=".35"/>')
    return s + ''.join(o) + '</svg>'

# ----------------------------------------------------------------------------- textiles
def curtain(seed, base, ink, ink2, W=512, H=512):
    """0.8 m x 0.8 m tile of cubicle curtain: pastel ground, printed leaves and dots (hospital print), soft fold shading in u."""
    r = R(seed); o = [f'<rect width="{W}" height="{H}" fill="{base}"/>']
    for i in range(8):                                   # folds (vertical light/dark bands)
        x = i * W / 8; o.append(f'<rect x="{x:.0f}" y="0" width="{W/16:.0f}" height="{H}" fill="#ffffff" opacity=".12"/><rect x="{x+W/16:.0f}" y="0" width="{W/16:.0f}" height="{H}" fill="#3a4a60" opacity=".06"/>')
    for gx in range(4):
        for gy in range(4):
            x, y = gx * W / 4 + (W / 8 if gy % 2 else 0) + r.uniform(-10, 10), gy * H / 4 + r.uniform(-10, 10); a = r.uniform(0, 360)
            o.append(f'<g transform="translate({x:.0f},{y:.0f}) rotate({a:.0f})">'
                     f'<path d="M0,0C14,-26 44,-30 60,-4C40,6 14,10 0,0Z" fill="{ink}" opacity=".75"/><path d="M0,0C-14,-26 -44,-30 -60,-4C-40,6 -14,10 0,0Z" fill="{ink2}" opacity=".7"/>'
                     f'<path d="M0,0C-6,20 4,36 0,50" stroke="{ink}" stroke-width="4" fill="none"/><circle cx="0" cy="-8" r="7" fill="#ffffff" opacity=".85"/></g>')
    for _ in range(70):
        o.append(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,H):.0f}" r="{r.uniform(3,6):.1f}" fill="{r.choice([ink, ink2, "#ffffff"])}" opacity=".7"/>')
    return svg(W, H, ''.join(o))

def net(W=256, H=128):
    """Mesh band at the top of the curtains (transparent holes)."""
    o = []
    for i in range(0, W, 8): o.append(f'<path d="M{i},0V{H}" stroke="#f4f6f4" stroke-width="2.4"/>')
    for j in range(0, H, 8): o.append(f'<path d="M0,{j}H{W}" stroke="#f4f6f4" stroke-width="2.4"/>')
    o.append(f'<rect x="0" y="0" width="{W}" height="14" fill="#f2f2ee"/><rect x="0" y="{H-10}" width="{W}" height="10" fill="#f2f2ee"/>')
    for i in range(0, W, 32): o.append(f'<circle cx="{i+16}" cy="7" r="4" fill="#9aa0a4"/>')
    return svg(W, H, ''.join(o))

def blanket(W=512, H=512):
    """Pale-blue hospital blanket: woven check, two darker border stripes, stamped hospital mark."""
    r = R(41); o = [f'<rect width="{W}" height="{H}" fill="#94bce6"/>']
    for i in range(0, W, 16): o.append(f'<path d="M{i},0V{H}" stroke="#c4daf0" stroke-width="5" opacity=".6"/>')
    for j in range(0, H, 16): o.append(f'<path d="M0,{j}H{W}" stroke="#8eb2d8" stroke-width="4" opacity=".45"/>')
    for y in (40, 70): o.append(f'<rect x="0" y="{y}" width="{W}" height="14" fill="#6c94c4"/>')
    for y in (H - 84, H - 54): o.append(f'<rect x="0" y="{y}" width="{W}" height="14" fill="#6c94c4"/>')
    o.append(f'<g opacity=".55">' + T(W * 0.5, H * 0.52, 44, 'รพ.บ้านนา', '#3a5a9a', k=True) + f'<circle cx="{W*0.5}" cy="{H*0.47}" r="90" fill="none" stroke="#3a5a9a" stroke-width="5"/></g>')
    o.append(blot(r, W, H, 30, ['#6a8ab4', '#d6e6f6'], 20, 70, (0.08, 0.18)))
    return svg(W, H, ''.join(o), font=True)

def sheet(W=512, H=512):
    """White bed sheet with soft creases."""
    r = R(42); o = [f'<rect width="{W}" height="{H}" fill="#f4f4f0"/>']
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(0, H); L = r.uniform(60, 220); a = r.uniform(-0.5, 0.5)
        o.append(f'<path d="M{x:.0f},{y:.0f}q{L/2:.0f},{r.uniform(-20,20):.0f} {L*math.cos(a):.0f},{L*math.sin(a):.0f}" stroke="#c8ccd8" stroke-width="{r.uniform(3,9):.0f}" fill="none" opacity=".55" stroke-linecap="round"/>')
    o.append(blot(r, W, H, 20, ['#d8dce6'], 20, 70, (0.1, 0.2)))
    o.append(f'<rect x="0" y="{H-30}" width="{W}" height="30" fill="#9ab8d8" opacity=".5"/>' + T(W - 70, H - 40, 22, 'รพ.บ้านนา', '#7a90b0'))
    return svg(W, H, ''.join(o), font=True)

def pillow(W=256, H=256):
    r = R(43); o = [f'<rect width="{W}" height="{H}" fill="#f7f6f2"/>', f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#bfc6d4" stroke-width="14"/>']
    for _ in range(10):
        x, y = r.uniform(30, W - 30), r.uniform(30, H - 30); o.append(f'<path d="M{x:.0f},{y:.0f}q20,{r.uniform(-10,10):.0f} {r.uniform(30,60):.0f},{r.uniform(-10,10):.0f}" stroke="#ccd2de" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- hardware, panels, furniture faces
def headwall(W=1024, H=256):
    """1.5 m x 0.375 m bed-head medical gas panel: aluminium channel, O2 (green), air (black/white), vacuum (yellow) outlets, power sockets, nurse-call."""
    o = [f'<rect width="{W}" height="{H}" fill="#dfe3e4"/><rect x="0" y="0" width="{W}" height="22" fill="#b6bcc0"/><rect x="0" y="{H-22}" width="{W}" height="22" fill="#b6bcc0"/>',
         f'<rect x="0" y="22" width="{W}" height="6" fill="#ffffff"/>']
    for x, col, lab in ((120, '#2aa04a', 'O2'), (250, '#2a2a2a', 'AIR'), (380, '#f0c428', 'VAC')):
        o.append(f'<rect x="{x-48}" y="60" width="96" height="120" rx="8" fill="#f4f4f2" stroke="#8a9094" stroke-width="3"/><circle cx="{x}" cy="112" r="30" fill="{col}"/>'
                 f'<circle cx="{x}" cy="112" r="12" fill="#c8cccc" stroke="#555" stroke-width="3"/>' + T(x, 168, 22, lab, '#333'))
    for x in (540, 640):
        o.append(f'<rect x="{x}" y="70" width="80" height="80" rx="6" fill="#fafaf8" stroke="#8a9094" stroke-width="3"/><rect x="{x+22}" y="96" width="8" height="22" fill="#333"/><rect x="{x+50}" y="96" width="8" height="22" fill="#333"/><circle cx="{x+40}" cy="132" r="6" fill="#333"/>')
    o.append(f'<rect x="770" y="70" width="80" height="80" rx="6" fill="#fafaf8" stroke="#8a9094" stroke-width="3"/><circle cx="810" cy="110" r="24" fill="#d8302a"/>' + T(810, 172, 18, 'เรียกพยาบาล', '#333'))
    o.append(f'<rect x="890" y="70" width="90" height="70" rx="6" fill="#3a3f44"/><circle cx="915" cy="105" r="9" fill="#58c060"/><rect x="935" y="95" width="34" height="8" fill="#9aa0a4"/><rect x="935" y="110" width="34" height="8" fill="#9aa0a4"/>')
    return svg(W, H, ''.join(o), font=True)

def cabinet(W=256, H=512):
    """Front of a bedside locker (0.45 x 0.85 m): pale laminate, top drawer with handle, door with handle, bed sticker, scuffs."""
    r = R(51); o = [f'<rect width="{W}" height="{H}" fill="#e9e4d6"/><rect x="0" y="0" width="{W}" height="16" fill="#b9c4cc"/>']
    o.append(f'<rect x="12" y="26" width="{W-24}" height="100" rx="6" fill="#efeadc" stroke="#9a9484" stroke-width="3"/><rect x="{W/2-40}" y="66" width="80" height="14" rx="6" fill="#8a8e92"/>')
    o.append(f'<rect x="12" y="140" width="{W-24}" height="{H-180}" rx="6" fill="#efeadc" stroke="#9a9484" stroke-width="3"/><rect x="{W-50}" y="240" width="14" height="80" rx="6" fill="#8a8e92"/>')
    o.append(f'<rect x="40" y="170" width="110" height="46" fill="#fff" stroke="#3a7ab8" stroke-width="3"/>')
    o.append(f'<rect x="0" y="{H-28}" width="{W}" height="28" fill="#5a6066"/>')
    o.append(blot(r, W, H, 18, ['#a89e8a', '#7a7468'], 8, 30, (0.08, 0.2)))
    return svg(W, H, ''.join(o))

def monitor_body(W=512, H=384):
    """Front of the patient monitor housing (0.36 x 0.30 m): pale grey plastic, rotary knob, buttons, brand strip; the screen window is drawn black
    (the live screen is a separate emissive plane in front of it)."""
    o = [f'<rect width="{W}" height="{H}" rx="26" fill="#d9dde0"/><rect x="18" y="18" width="{W-36}" height="{H-36}" rx="16" fill="#c6ccd0"/>',
         f'<rect x="34" y="34" width="{W*0.78:.0f}" height="{H*0.72:.0f}" rx="6" fill="#0c1014"/>']
    bx = 34 + W * 0.78 + 14
    for j in range(5): o.append(f'<rect x="{bx:.0f}" y="{44+j*42}" width="{W-bx-30:.0f}" height="30" rx="6" fill="{["#e8eaec","#e8eaec","#f0c030","#d8302a","#e8eaec"][j]}" stroke="#7a8288" stroke-width="2"/>')
    o.append(f'<circle cx="{bx+(W-bx-30)/2:.0f}" cy="{H-70}" r="26" fill="#3a4046"/><circle cx="{bx+(W-bx-30)/2:.0f}" cy="{H-70}" r="12" fill="#6a7076"/>')
    o.append(f'<rect x="34" y="{H-70}" width="200" height="22" rx="4" fill="#2a6ab0"/>' + T(134, H - 53, 18, 'VITALCARE 7', '#fff'))
    for i in range(6): o.append(f'<circle cx="{270+i*24}" cy="{H-58}" r="7" fill="#9aa2a8"/>')
    return svg(W, H, ''.join(o))

def monitor_screen(hr=72, spo2=98, sys_=118, dia=76, rr=18, W=512, H=384):
    """Default monitor screen (re-texture per frame via hosp3d.set_monitor_screen): ECG, pleth and resp traces, numerics."""
    o = [f'<rect width="{W}" height="{H}" fill="#05080a"/>']
    for j in range(1, 4): o.append(f'<path d="M0,{j*H/4:.0f}H{W*0.68:.0f}" stroke="#1c2a30" stroke-width="2"/>')
    def ecg(y0, amp=48):
        d = [f'M0,{y0}']; x = 0
        while x < W * 0.66:
            d += [f'L{x+20},{y0}', f'L{x+26},{y0-6}', f'L{x+32},{y0}', f'L{x+40},{y0}', f'L{x+44},{y0+8}', f'L{x+50},{y0-amp}', f'L{x+56},{y0+14}', f'L{x+62},{y0}', f'L{x+78},{y0}', f'L{x+88},{y0-12}', f'L{x+98},{y0}']
            x += 112
        return ' '.join(d)
    o.append(f'<path d="{ecg(80)}" stroke="#38f060" stroke-width="4" fill="none" stroke-linejoin="round"/>')
    pl = 'M0,190 ' + ' '.join(f'L{x},{190-28*max(0,math.sin((x%112)/112*math.pi*1.3))**1.5:.0f}' for x in range(0, int(W * 0.66), 4))
    o.append(f'<path d="{pl}" stroke="#30d8f0" stroke-width="4" fill="none"/>')
    rs = 'M0,290 ' + ' '.join(f'L{x},{290-22*math.sin(x/60):.0f}' for x in range(0, int(W * 0.66), 4))
    o.append(f'<path d="{rs}" stroke="#f0d838" stroke-width="3" fill="none"/>')
    x0 = W * 0.70
    o.append(T(x0 + 8, 34, 20, 'HR', '#38f060', 'start') + T(W - 12, 104, 86, str(hr), '#38f060', 'end') + f'<path d="M{x0+20},60l8,-10 8,10 -8,10z" fill="#ff5050"/>')
    o.append(T(x0 + 8, 146, 20, 'SpO2', '#30d8f0', 'start') + T(W - 12, 210, 66, str(spo2), '#30d8f0', 'end'))
    o.append(T(x0 + 8, 248, 20, 'NIBP', '#f4f4f4', 'start') + T(W - 12, 290, 38, f'{sys_}/{dia}', '#f4f4f4', 'end'))
    o.append(T(x0 + 8, 330, 20, 'RR', '#f0d838', 'start') + T(W - 12, 368, 44, str(rr), '#f0d838', 'end'))
    o.append(f'<path d="M{x0},0V{H}" stroke="#2a3a40" stroke-width="2"/>' + T(10, H - 10, 16, '10:24  เตียง 2', '#8aa0a8', 'start'))
    return svg(W, H, ''.join(o), font=True)

def phone_screen(level=0.15, charging=True, W=160, H=320):
    """Default phone screen (re-texture / re-tint per frame via hosp3d.set_phone_screen): lock screen with a big battery icon."""
    col = '#ff4a3a' if level < 0.2 else ('#ffd040' if level < 0.5 else '#4ae070')
    o = ['<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2a4a"/><stop offset="1" stop-color="#0a1020"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>', T(W / 2, 70, 44, '10:24', '#f0f4ff'), T(W / 2, 96, 15, 'อังคาร 14 พ.ย.', '#b0bcd8')]
    bx, by, bw, bh = W / 2 - 36, 140, 72, 120
    o.append(f'<rect x="{bx+24:.0f}" y="{by-12}" width="24" height="14" rx="3" fill="#e8ecf4"/><rect x="{bx:.0f}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="none" stroke="#e8ecf4" stroke-width="7"/>')
    fh = (bh - 16) * level; o.append(f'<rect x="{bx+8:.0f}" y="{by+bh-8-fh:.0f}" width="{bw-16}" height="{fh:.0f}" rx="4" fill="{col}"/>')
    if charging: o.append(f'<path d="M{W/2+6:.0f},{by+22}l-22,44h16l-8,36 26,-48h-16z" fill="#ffffff" stroke="#1a2a4a" stroke-width="3"/>')
    o.append(T(W / 2, by + bh + 34, 22, f'{int(level*100)}%', col))
    return svg(W, H, ''.join(o), font=True)

def station_front(W=2048, H=512):
    """Nurse-station counter front (4.0 m x 1.0 m): two-tone laminate, logo, Thai label."""
    r = R(61); k = W / 4; o = [f'<rect width="{W}" height="{H}" fill="#d8cbb0"/><rect x="0" y="0" width="{W}" height="60" fill="#3d7f9c"/><rect x="0" y="60" width="{W}" height="10" fill="#f2f0e8"/>']
    for i in range(1, 8): o.append(f'<path d="M{i*W/8:.0f},70V{H-40}" stroke="#b8aa8e" stroke-width="5"/>')
    o.append(f'<rect x="0" y="{H-40}" width="{W}" height="40" fill="#6a6e70"/>')
    o.append(f'<rect x="{W*0.32:.0f}" y="130" width="{W*0.36:.0f}" height="170" rx="14" fill="#ffffff" stroke="#3d7f9c" stroke-width="8"/>' + T(W * 0.5, 225, 86, 'เคาน์เตอร์พยาบาล', '#245a74', k=True) + T(W * 0.5, 280, 34, 'NURSE STATION', '#3d7f9c'))
    o.append(f'<circle cx="{W*0.16:.0f}" cy="230" r="80" fill="#2a8a5a"/><path d="M{W*0.16-14:.0f},180h28v36h36v28h-36v36h-28v-36h-36v-28h36z" fill="#fff"/>')
    o.append(f'<rect x="{W*0.78:.0f}" y="150" width="300" height="200" fill="#fff8e0" stroke="#c8a040" stroke-width="5"/>' + T(W * 0.78 + 150, 210, 34, 'ติดต่อสอบถาม', '#7a4a10') + T(W * 0.78 + 150, 260, 30, 'กรุณากดกริ่ง', '#7a4a10') + f'<circle cx="{W*0.78+150:.0f}" cy="305" r="20" fill="#d8302a"/>')
    o.append(blot(r, W, H, 50, ['#8a7a60', '#5a5048'], 10, 50, (0.06, 0.14)))
    return svg(W, H, ''.join(o), font=True)

def back_wall(W=2048, H=1024):
    """Far wall behind the station (7 m x 3.5 m wide band, painted): whiteboard of beds, notice board with papers, medicine-room door, chart."""
    r = R(62); k = W / 7; o = [f'<rect width="{W}" height="{H}" fill="#efe8d6"/>', blot(r, W, H, 60, ['#d8ccb0', '#fffaf0'], 30, 140, (0.05, 0.12))]
    zt = lambda z: H - z / 3.5 * H
    o.append(f'<rect x="0" y="{zt(1.0):.0f}" width="{W}" height="{zt(0)-zt(1.0):.0f}" fill="#b4d4c4"/>')
    for i in range(0, W, 26): o.append(f'<path d="M{i},{zt(1.0):.0f}V{H}" stroke="#9cbcae" stroke-width="2"/>')
    # whiteboard (bed list)
    wx, wy, ww, wh = 0.35 * k, zt(2.45), 1.9 * k, zt(1.35) - zt(2.45)
    o.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" fill="#fbfcfc" stroke="#9aa2a8" stroke-width="10"/>' + T(wx + ww / 2, wy + 50, 40, 'หอผู้ป่วยชาย  ประจำวัน', '#1a4a9a', k=True))
    for j in range(6):
        y = wy + 90 + j * 44; o.append(f'<path d="M{wx+20:.0f},{y+12:.0f}H{wx+ww-20:.0f}" stroke="#c8d0d8" stroke-width="2"/>' + T(wx + 30, y, 28, f'เตียง {j+1}', '#1a1a1a', 'start'))
        o.append(f'<path d="M{wx+170:.0f},{y-8:.0f}' + ''.join(f'l{r.uniform(10,22):.0f},{r.uniform(-8,8):.0f}' for _ in range(14)) + f'" stroke="{r.choice(["#1a4a9a","#c82a2a","#1a1a1a"])}" stroke-width="4" fill="none"/>')
    # notice board
    nx, ny, nw, nh = 2.6 * k, zt(2.5), 1.4 * k, zt(1.45) - zt(2.5)
    o.append(f'<rect x="{nx:.0f}" y="{ny:.0f}" width="{nw:.0f}" height="{nh:.0f}" fill="#b88a58" stroke="#7a5a3a" stroke-width="10"/>')
    for _ in range(9):
        x, y = r.uniform(nx + 10, nx + nw - 90), r.uniform(ny + 10, ny + nh - 110); c = r.choice(['#ffffff', '#fff6c0', '#d8f0ff', '#ffd8e0'])
        o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(70,110):.0f}" height="{r.uniform(80,120):.0f}" fill="{c}" transform="rotate({r.uniform(-6,6):.0f} {x:.0f} {y:.0f})"/><circle cx="{x+30:.0f}" cy="{y+6:.0f}" r="5" fill="#d8302a"/>')
        for j in range(4): o.append(f'<path d="M{x+10:.0f},{y+28+j*14:.0f}h{r.uniform(30,70):.0f}" stroke="#555" stroke-width="3"/>')
    # medicine room door (right)
    dx = 5.2 * k; o.append(f'<rect x="{dx:.0f}" y="{zt(2.15):.0f}" width="{1.0*k:.0f}" height="{zt(0)-zt(2.15):.0f}" fill="#9cc0d8" stroke="#5a7a90" stroke-width="10"/>'
                           f'<rect x="{dx+0.3*k:.0f}" y="{zt(1.9):.0f}" width="{0.4*k:.0f}" height="{0.3*H/3.5:.0f}" fill="#dceaf2" stroke="#5a7a90" stroke-width="6"/>'
                           f'<rect x="{dx+0.15*k:.0f}" y="{zt(2.45):.0f}" width="{0.7*k:.0f}" height="60" fill="#2a6a8a"/>' + T(dx + 0.5 * k, zt(2.45) + 44, 34, 'ห้องยา', '#fff', k=True)
                           + f'<rect x="{dx+0.82*k:.0f}" y="{zt(1.05):.0f}" width="16" height="50" rx="5" fill="#ccc"/>')
    o.append(f'<rect x="0" y="{zt(0.1):.0f}" width="{W}" height="{zt(0)-zt(0.1):.0f}" fill="#7f8c88"/>')
    return svg(W, H, ''.join(o), font=True)

def near_wall(W=2048, H=1024):
    """Camera-side end wall (7 m x 3.5 m): double doors with porthole windows, hand-wash sink poster, exit sign."""
    r = R(63); k = W / 7; zt = lambda z: H - z / 3.5 * H; o = [f'<rect width="{W}" height="{H}" fill="#efe8d6"/>', blot(r, W, H, 50, ['#d8ccb0'], 30, 140, (0.05, 0.12))]
    o.append(f'<rect x="0" y="{zt(1.0):.0f}" width="{W}" height="{zt(0)-zt(1.0):.0f}" fill="#b4d4c4"/>')
    dx0 = 2.4 * k
    o.append(f'<rect x="{dx0:.0f}" y="{zt(2.3):.0f}" width="{2.2*k:.0f}" height="{zt(0)-zt(2.3):.0f}" fill="#8fb6cf" stroke="#4f6f86" stroke-width="12"/><path d="M{dx0+1.1*k:.0f},{zt(2.3):.0f}V{H}" stroke="#4f6f86" stroke-width="8"/>')
    for cx in (dx0 + 0.55 * k, dx0 + 1.65 * k): o.append(f'<circle cx="{cx:.0f}" cy="{zt(1.55):.0f}" r="{0.17*k:.0f}" fill="#e6f2fa" stroke="#4f6f86" stroke-width="8"/>')
    o.append(f'<rect x="{dx0+0.7*k:.0f}" y="{zt(2.6):.0f}" width="{0.8*k:.0f}" height="{0.18*H/3.5:.0f}" fill="#1a9a4a"/>' + T(dx0 + 1.1 * k, zt(2.6) + 40, 34, 'ทางออก EXIT', '#fff', k=True))
    o.append(f'<rect x="{0.6*k:.0f}" y="{zt(2.1):.0f}" width="{0.8*k:.0f}" height="{0.9*H/3.5:.0f}" fill="#fff" stroke="#2a8a5a" stroke-width="6"/>' + T(1.0 * k, zt(2.1) + 50, 30, 'ล้างมือ 7 ขั้นตอน', '#2a8a5a', k=True))
    for j in range(2):
        for i in range(4): o.append(f'<circle cx="{0.7*k+30+i*50:.0f}" cy="{zt(2.1)+110+j*80:.0f}" r="20" fill="#f4c8a8" stroke="#2a8a5a" stroke-width="3"/>')
    o.append(f'<rect x="0" y="{zt(0.1):.0f}" width="{W}" height="{zt(0)-zt(0.1):.0f}" fill="#7f8c88"/>')
    return svg(W, H, ''.join(o), font=True)

def binders(W=1024, H=256):
    """Spines of ring binders and patient charts (atlas row, tiled along shelves)."""
    r = R(64); o = [f'<rect width="{W}" height="{H}" fill="#2a2a2a"/>']; x = 0
    while x < W:
        w = r.uniform(24, 48); c = r.choice(['#2a5ab0', '#d8302a', '#2a9a5a', '#f0c030', '#f4f4f0', '#8a3ab0', '#3a3a3a', '#f08a30'])
        o.append(f'<rect x="{x:.0f}" y="{r.uniform(0,30):.0f}" width="{w-2:.0f}" height="{H}" fill="{c}"/><rect x="{x+5:.0f}" y="80" width="{w-12:.0f}" height="60" fill="#fff" opacity=".9"/><circle cx="{x+w/2:.0f}" cy="200" r="7" fill="#222" opacity=".6"/>')
        x += w
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- signs, posters, clock, exterior
def signs(W=1024, H=1024):
    """Atlas, 4 rows of 1024 x 256: (0) hanging ward sign หอผู้ป่วยชาย 2, (1) no-phone sign ห้ามใช้โทรศัพท์, (2) wet floor ระวังพื้นลื่น, (3) bed plates เตียง 1-6."""
    o = []
    o.append('<rect x="0" y="0" width="1024" height="256" fill="#1f7a52"/><rect x="10" y="10" width="1004" height="236" fill="none" stroke="#fff" stroke-width="6"/>')
    o.append('<rect x="34" y="40" width="176" height="176" rx="20" fill="#fff"/>' + T(122, 182, 150, '2', '#1f7a52', k=True))
    o.append(T(610, 150, 112, 'หอผู้ป่วยชาย', '#ffffff', k=True) + T(610, 220, 44, 'MALE WARD 2', '#d6f2e2'))
    o.append('<rect x="0" y="256" width="1024" height="256" fill="#ffffff"/><rect x="8" y="264" width="1008" height="240" fill="none" stroke="#d8302a" stroke-width="10"/>')
    o.append('<circle cx="140" cy="384" r="96" fill="#fff" stroke="#d8302a" stroke-width="22"/><rect x="104" y="318" width="72" height="132" rx="12" fill="#2a2a2a"/><rect x="114" y="334" width="52" height="92" fill="#8ab8f0"/><path d="M72,452L208,316" stroke="#d8302a" stroke-width="22"/>')
    o.append(T(610, 384, 92, 'ห้ามใช้โทรศัพท์', '#d8302a', k=True) + T(610, 458, 40, 'ในหอผู้ป่วย  กรุณาปิดเสียง', '#333333'))
    o.append('<rect x="0" y="512" width="1024" height="256" fill="#ffd21e"/><path d="M60,740l100,-200 100,200z" fill="#1a1a1a"/><path d="M80,728l80,-160 80,160z" fill="#ffd21e"/>'
             '<circle cx="160" cy="626" r="14" fill="#1a1a1a"/><path d="M160,640l-10,40 30,10 M150,680l-30,30" stroke="#1a1a1a" stroke-width="12" fill="none"/>')
    o.append(T(620, 650, 110, 'ระวังพื้นลื่น', '#1a1a1a', k=True) + T(620, 720, 46, 'CAUTION WET FLOOR', '#1a1a1a'))
    for i in range(6):
        x = i * 170 + 2; o.append(f'<rect x="{x}" y="770" width="166" height="250" fill="#2a6ab0"/><rect x="{x+8}" y="778" width="150" height="234" fill="none" stroke="#fff" stroke-width="4"/>'
                                  + T(x + 83, 850, 48, 'เตียง', '#fff', k=True) + T(x + 83, 990, 140, str(i + 1), '#fff', k=True))
    return svg(W, H, ''.join(o), font=True)

def posters(W=1024, H=1024):
    """Atlas 2x2 of A2 health posters: dengue (ไข้เลือดออก), hand washing, no smoking, falls prevention."""
    r = R(71); o = []
    # 0 dengue
    o.append('<rect x="0" y="0" width="512" height="512" fill="#fff4d8"/><rect x="0" y="0" width="512" height="110" fill="#d8302a"/>' + T(256, 78, 64, 'ไข้เลือดออก', '#fff', k=True))
    o.append('<ellipse cx="256" cy="250" rx="120" ry="60" fill="#2a2a2a"/>' + ''.join(f'<path d="M{200+i*30},270l{-30+i*12},90" stroke="#2a2a2a" stroke-width="6"/>' for i in range(5)) + '<path d="M160,230l-120,-60 M350,230l120,-60" stroke="#8ab8f0" stroke-width="30" opacity=".6"/>')
    o.append(T(256, 420, 40, 'ปิด  เปลี่ยน  ปล่อย', '#d8302a', k=True) + T(256, 470, 28, 'กำจัดลูกน้ำยุงลาย ทุก 7 วัน', '#333'))
    # 1 hand washing
    o.append('<rect x="512" y="0" width="512" height="512" fill="#e6f6ff"/><rect x="512" y="0" width="512" height="100" fill="#2a7ab8"/>' + T(768, 72, 56, 'ล้างมือให้สะอาด', '#fff', k=True))
    for i in range(6):
        cx, cy = 600 + (i % 3) * 170, 180 + (i // 3) * 160; o.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="#fff" stroke="#2a7ab8" stroke-width="5"/><ellipse cx="{cx-12}" cy="{cy}" rx="26" ry="38" fill="#f4c8a8"/><ellipse cx="{cx+14}" cy="{cy+6}" rx="24" ry="36" fill="#e8b490"/>' + T(cx, cy + 92, 26, str(i + 1), '#2a7ab8'))
    # 2 no smoking
    o.append('<rect x="0" y="512" width="512" height="512" fill="#ffffff"/><circle cx="256" cy="720" r="150" fill="none" stroke="#d8302a" stroke-width="30"/><rect x="146" y="700" width="200" height="34" fill="#4a4a4a"/><rect x="346" y="700" width="30" height="34" fill="#e87a2a"/><path d="M150,610L362,830" stroke="#d8302a" stroke-width="30"/>' + T(256, 960, 56, 'เขตปลอดบุหรี่', '#d8302a', k=True))
    # 3 falls
    o.append('<rect x="512" y="512" width="512" height="512" fill="#f2ffe6"/><rect x="512" y="512" width="512" height="100" fill="#4a9a3a"/>' + T(768, 584, 50, 'ป้องกันการพลัดตกเตียง', '#fff', k=True))
    o.append('<rect x="600" y="680" width="336" height="90" rx="10" fill="#9ab8d8"/><rect x="600" y="650" width="336" height="18" fill="#7a8a9a"/><circle cx="660" cy="700" r="26" fill="#f4c8a8"/>' + T(768, 860, 34, 'ยกราวกั้นเตียงขึ้นทุกครั้ง', '#2a5a2a') + T(768, 910, 30, 'กดกริ่งเรียกพยาบาล', '#2a5a2a'))
    o.append(blot(r, W, H, 30, ['#c8b890'], 10, 40, (0.05, 0.12)))
    return svg(W, H, ''.join(o), font=True)

def clock(W=256):
    o = [f'<circle cx="128" cy="128" r="126" fill="#2a2a2e"/><circle cx="128" cy="128" r="112" fill="#fbfaf6"/>']
    for i in range(60):
        a = i * math.pi / 30; L = 16 if i % 5 == 0 else 6; w = 5 if i % 5 == 0 else 2
        o.append(f'<path d="M{128+math.sin(a)*104:.1f},{128-math.cos(a)*104:.1f}L{128+math.sin(a)*(104-L):.1f},{128-math.cos(a)*(104-L):.1f}" stroke="#222" stroke-width="{w}"/>')
    for i in range(1, 13):
        a = i * math.pi / 6; o.append(T(128 + math.sin(a) * 80, 128 - math.cos(a) * 80 + 9, 24, str(i), '#222'))
    hh, mm = 10, 24; ah = (hh + mm / 60) * math.pi / 6; am = mm * math.pi / 30
    o.append(f'<path d="M128,128L{128+math.sin(ah)*52:.0f},{128-math.cos(ah)*52:.0f}" stroke="#222" stroke-width="9" stroke-linecap="round"/>'
             f'<path d="M128,128L{128+math.sin(am)*82:.0f},{128-math.cos(am)*82:.0f}" stroke="#222" stroke-width="6" stroke-linecap="round"/>'
             f'<path d="M128,128L{128+math.sin(2.1)*90:.0f},{128-math.cos(2.1)*90:.0f}" stroke="#d8302a" stroke-width="2.5"/><circle cx="128" cy="128" r="7" fill="#d8302a"/>')
    return svg(W, W, ''.join(o), font=True)

def exterior(side, W=3072, H=1024):
    """View out of the windows (17 m x 6 m card, 4 m outside): after the storm. 'r' = toward the sun: warm haze, broken cumulus, wet palms,
    the opposite hospital wing; 'l' = away from the sun: deep blue sky with the retreating storm, mango trees, a covered walkway."""
    r = R(81 if side == 'r' else 82); k = W / 17; zt = lambda z: H - (z + 1.0) / 6.0 * H; o = []
    if side == 'r':
        o.append('<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a9ee0"/><stop offset=".55" stop-color="#bfe0f4"/><stop offset=".8" stop-color="#fff4dc"/></linearGradient>'
                 '<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fffbe8"/><stop offset=".4" stop-color="#fff0c8" stop-opacity=".6"/><stop offset="1" stop-color="#ffe0a0" stop-opacity="0"/></radialGradient></defs>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#s)"/><circle cx="{W*0.2:.0f}" cy="{H*0.1:.0f}" r="{H*0.6:.0f}" fill="url(#sun)"/>')
        for _ in range(26):
            x, y = r.uniform(0, W), r.uniform(H * 0.02, H * 0.42); o.append(TS._clouds(r, x, y, r.uniform(40, 90), '#f4f2ee', '#ffffff', '#b8c4dc', 8, 0.5))
        # opposite wing: 2 storeys, white with blue band, louvred windows, rain stains
        bx0, bx1 = 0.15 * W, 0.78 * W; o.append(f'<rect x="{bx0:.0f}" y="{zt(6.4):.0f}" width="{bx1-bx0:.0f}" height="{zt(-1)-zt(6.4):.0f}" fill="#f0ece0"/>'
                                                 f'<rect x="{bx0-20:.0f}" y="{zt(6.6):.0f}" width="{bx1-bx0+40:.0f}" height="30" fill="#c8402a"/><rect x="{bx0:.0f}" y="{zt(3.2):.0f}" width="{bx1-bx0:.0f}" height="26" fill="#3a7ab8"/>')
        for fl, z0 in enumerate((0.4, 3.8)):
            x = bx0 + 40
            while x < bx1 - 120:
                o.append(f'<rect x="{x:.0f}" y="{zt(z0+1.8):.0f}" width="110" height="{zt(z0)-zt(z0+1.8):.0f}" fill="#5a7890"/>' + ''.join(f'<path d="M{x:.0f},{zt(z0+1.8)+8+j*14:.0f}h110" stroke="#b8c8d4" stroke-width="5"/>' for j in range(int((zt(z0) - zt(z0 + 1.8)) / 14))))
                x += 170
        o.append(streaks(r, bx0, bx1, zt(6.4), H * 0.3, 3, '#7a7468', 30, (0.08, 0.2)))
        trees = [(r.uniform(0, W), r.uniform(0.6, 1.2)) for _ in range(9)]
        for (x, s) in trees:                              # coconut palms
            top = (x + r.uniform(-60, 60), zt(5.5 * s + 1)); o.append(f'<path d="M{x:.0f},{H}Q{x+20:.0f},{(H+top[1])/2:.0f} {top[0]:.0f},{top[1]:.0f}" stroke="#7a6a52" stroke-width="{18*s:.0f}" fill="none"/>')
            for j in range(9):
                a = j * 0.7 + r.uniform(-0.2, 0.2); L = r.uniform(140, 220) * s
                o.append(f'<path d="M{top[0]:.0f},{top[1]:.0f}q{math.cos(a)*L*0.6:.0f},{-abs(math.sin(a))*L*0.4-20:.0f} {math.cos(a)*L:.0f},{abs(math.sin(a))*L*0.3+20:.0f}" stroke="{r.choice(["#3a7a3a","#4a8a3a","#2e6a32"])}" stroke-width="{14*s:.0f}" fill="none" stroke-linecap="round"/>')
        for _ in range(40):                               # wet shrubs, low
            x = r.uniform(0, W); o.append(TS._clouds(r, x, zt(0.2), r.uniform(50, 90), '#3e7e3e', '#7ab85a', '#2a5a3a', 7, 0.6))
    else:
        o.append('<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a72c8"/><stop offset=".6" stop-color="#8ec0ea"/><stop offset="1" stop-color="#d8ecf4"/></linearGradient></defs>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#s)"/>')
        for _ in range(40):                               # retreating storm mass, warm-lit tops
            x, y = r.uniform(0, W), r.uniform(H * 0.05, H * 0.4); o.append(TS._clouds(r, x, y, r.uniform(60, 120), '#6a6c9e', '#f4e2d0', '#4a4a7a', 9, 0.6))
        o.append(f'<rect x="0" y="{zt(2.6):.0f}" width="{W}" height="30" fill="#b8402a"/><rect x="0" y="{zt(2.6)+30:.0f}" width="{W}" height="{zt(-1)-zt(2.6):.0f}" fill="#d8d0bc"/>')
        for i in range(30): o.append(f'<rect x="{i*W/30:.0f}" y="{zt(2.5):.0f}" width="22" height="{zt(-1)-zt(2.5):.0f}" fill="#efeadc"/>')
        for _ in range(16):                               # mango / rain trees
            x = r.uniform(0, W); top = zt(r.uniform(3.8, 5.6)); o.append(f'<rect x="{x-14:.0f}" y="{top:.0f}" width="28" height="{H-top:.0f}" fill="#5a4a3a"/>')
            for _ in range(5): o.append(TS._clouds(r, x + r.uniform(-120, 120), top + r.uniform(-30, 80), r.uniform(60, 110), '#3a7438', '#76b052', '#22502e', 8, 0.7))
    return svg(W, H, ''.join(o))

def leaves(W=512, H=768):
    """Tall potted plant card (dracaena / snake plant), transparent."""
    r = R(91); o = []
    for _ in range(34):
        x0 = W / 2 + r.uniform(-30, 30); a = r.uniform(-0.55, 0.55); L = r.uniform(300, 700); w = r.uniform(18, 34)
        x1, y1 = x0 + math.sin(a) * L, H - math.cos(a) * L; c = r.choice(['#3a8a3a', '#2e6e2e', '#5aa848', '#4a9a3a', '#7ab84a'])
        o.append(f'<path d="M{x0-w/2:.0f},{H}Q{(x0+x1)/2-w:.0f},{(H+y1)/2:.0f} {x1:.0f},{y1:.0f}Q{(x0+x1)/2+w:.0f},{(H+y1)/2:.0f} {x0+w/2:.0f},{H}Z" fill="{c}"/>'
                 f'<path d="M{x0:.0f},{H}Q{(x0+x1)/2:.0f},{(H+y1)/2:.0f} {x1:.0f},{y1:.0f}" stroke="#d8e870" stroke-width="3" fill="none" opacity=".6"/>')
    return svg(W, H, ''.join(o))

def ivbag(W=128, H=256):
    o = [f'<rect width="{W}" height="{H}" rx="20" fill="#e4f0f6"/><rect x="10" y="{H*0.35:.0f}" width="{W-20}" height="{H*0.6:.0f}" rx="12" fill="#cfe4f0"/>',
         f'<rect x="18" y="50" width="{W-36}" height="80" fill="#ffffff" stroke="#2a7ab8" stroke-width="3"/>', T(W / 2, 80, 16, '0.9% NSS', '#2a5a9a'), T(W / 2, 106, 14, '1000 ml', '#333')]
    for j in range(8): o.append(f'<path d="M{W-26},{140+j*12}h12" stroke="#2a5a9a" stroke-width="2"/>')
    return svg(W, H, ''.join(o), font=True)

def chart(W=256, H=320):
    """Clipboard chart on the footboard."""
    r = R(93); o = [f'<rect width="{W}" height="{H}" rx="10" fill="#b8865a"/><rect x="16" y="30" width="{W-32}" height="{H-46}" fill="#fbfbf6"/><rect x="{W/2-40}" y="10" width="80" height="34" rx="6" fill="#9aa0a6"/>',
         T(W / 2, 74, 22, 'บันทึกสัญญาณชีพ', '#1a4a9a')]
    for j in range(9): o.append(f'<path d="M30,{100+j*22}H{W-30}" stroke="#c0c8d8" stroke-width="2"/>')
    o.append('<path d="M34,250' + ''.join(f'L{34+i*20},{230-r.uniform(0,60):.0f}' for i in range(1, 10)) + '" stroke="#d8302a" stroke-width="4" fill="none"/>')
    return svg(W, H, ''.join(o), font=True)

def wheelchair_seat(W=256, H=256):
    o = [f'<rect width="{W}" height="{H}" fill="#2a3a5a"/>'] + [f'<path d="M0,{j}H{W}" stroke="#34466a" stroke-width="4"/>' for j in range(0, H, 14)]
    return svg(W, H, ''.join(o))

def cart(W=512, H=512):
    """Front of the red emergency (crash) cart: drawers with labels."""
    o = [f'<rect width="{W}" height="{H}" fill="#c8302a"/>']
    for j in range(5):
        y = 20 + j * 96; o.append(f'<rect x="20" y="{y}" width="{W-40}" height="84" rx="8" fill="#d8443a" stroke="#8a1a14" stroke-width="4"/><rect x="{W/2-60}" y="{y+50}" width="120" height="16" rx="6" fill="#e8e8e8"/><rect x="40" y="{y+12}" width="130" height="30" fill="#fff"/>')
    return svg(W, H, ''.join(o))

def vent(W=512, H=128):
    """Thai ventilation blocks (ช่องลม) above each window: 1.6 x 0.4 m, 8 x 2 cement blocks with a flower cut-out (transparent holes)."""
    o = []; s = H / 2
    for i in range(int(W / s)):
        for j in range(2):
            x, y = i * s, j * s; c = s / 2
            o.append(f'<path d="M{x},{y}h{s}v{s}h{-s}z M{x+c},{y+6}Q{x+s-8},{y+8} {x+s-6},{y+c}Q{x+s-8},{y+s-8} {x+c},{y+s-6}Q{x+8},{y+s-8} {x+6},{y+c}Q{x+8},{y+8} {x+c},{y+6}z" fill="#e8e4da" fill-rule="evenodd"/>'
                     f'<circle cx="{x+c}" cy="{y+c}" r="{s*0.14:.0f}" fill="#d8d4ca"/><path d="M{x},{y}h{s}v{s}h{-s}z" fill="none" stroke="#a8a49a" stroke-width="3"/>')
    return svg(W, H, ''.join(o))

# ----------------------------------------------------------------------------- job table
JOBS = dict(
    floor=(floor, 1792, 4352, False), wall_low=(wall_low, 1024, 256, False), wall_up=(wall_up, 1024, 512, False),
    ceiling=(ceiling, 512, 512, False), ceiling_stain=(ceiling_stain, 512, 512, False),
    curtain_g=(lambda: curtain(1, '#b4e2c2', '#3f9a72', '#4f88c8'), 512, 512, False), curtain_b=(lambda: curtain(2, '#b0d2f0', '#3f72c0', '#4aa878'), 512, 512, False),
    net=(net, 256, 128, True), blanket=(blanket, 512, 512, False), sheet=(sheet, 512, 512, False), pillow=(pillow, 256, 256, False),
    headwall=(headwall, 1024, 256, False), cabinet=(cabinet, 256, 512, False), monitor_body=(monitor_body, 512, 384, False),
    monitor_screen=(monitor_screen, 512, 384, False), phone_screen=(phone_screen, 160, 320, False),
    phone_screen_full=(lambda: phone_screen(0.92, False), 160, 320, False),
    station_front=(station_front, 2048, 512, False), back_wall=(back_wall, 2048, 1024, False), near_wall=(near_wall, 2048, 1024, False),
    binders=(binders, 1024, 256, False), signs=(signs, 1024, 1024, False), posters=(posters, 1024, 1024, False), clock=(clock, 256, 256, False),
    ext_r=(lambda: exterior('r'), 3072, 1024, False), ext_l=(lambda: exterior('l'), 3072, 1024, False), leaves=(leaves, 512, 768, True),
    ivbag=(ivbag, 128, 256, False), vent=(vent, 512, 128, True), chart=(chart, 256, 320, False), wc_seat=(wheelchair_seat, 256, 256, False), cart=(cart, 512, 512, False),
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
