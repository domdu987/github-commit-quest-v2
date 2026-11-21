"""T5a staging patch (same approach as T6b t6b_stage.py): Bertillon's over-the-shoulder back view as hair + coat (not a flat black slab).
Replaces prefecture17._back_cover for the 'bertillon' anchor only (brown hair dome with strands, ears, white shirt-collar nape, navy frock coat with lapel collar,
shoulders and seam, every piece with a dark ink outline). Other anchors keep the stock cover. Card-plane units as in _back_cover (head radius 0.56)."""
import math, sys, os
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'set3d17'))
for _p in ('stage', 'cast17'): sys.path.insert(0, os.path.join(HERE, '..', '..', _p))
import prefecture17 as P

INK = '#1a1020'
def _billboard_axes(o, ex, ey, cam):
    """the covers face the camera whatever the card yaw (cards at the +-35 deg clamp are edge-on from behind): same scale as the card axes"""
    ray = (o - Vector(cam.location)).normalized(); up = Vector((0, 0, 1)); right = ray.cross(up)
    if right.length < 1e-4: return ex, ey
    right.normalize(); return right * ex.length, -up * ey.length
def _poly_ellipse(cx, cy, rx, ry, n=28): return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]
def _grow(pts, d):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    out = []
    for x, y in pts:
        dx, dy = x - cx, y - cy; L = math.hypot(dx, dy) or 1.0; out.append((x + dx / L * d, y + dy / L * d))
    return out
def _layer(name, pts, hexc, lay, o, ex, ey, to, outline=0.035):
    """one flat polygon (star-shaped about its centroid) on the card plane, `lay` steps toward the camera; with an ink hull just under it."""
    def mk(nm, pp, col, z):
        cx = sum(p[0] for p in pp) / len(pp); cy = sum(p[1] for p in pp) / len(pp); base = o + to * z
        V = [tuple(base + ex * cx + ey * cy)] + [tuple(base + ex * x + ey * y) for x, y in pp]; n = len(pp)
        me = bpy.data.meshes.new(nm); me.from_pydata(V, [], [(0, 1 + k, 1 + (k + 1) % n) for k in range(n)]); me.update(); me.materials.append(P._flat('t6b_' + col.strip('#'), col))
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; return ob
    mk(name + '_ink', _grow(pts, outline), INK, lay - 0.003); mk(name, pts, hexc, lay)


def bertillon_back(a, c, cam):
    import actors
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o
    ex, ey = _billboard_axes(o, ex, ey, cam)
    to = (Vector(cam.location) - o).normalized(); u = 0.006; z0 = 0.03; nm = 'bk_' + c['name']
    L = lambda n, pts, col, k, ol=0.055: _layer('%s_%s' % (nm, n), pts, col, z0 + u * k, o, ex, ey, to, ol)
    coat = [(-0.28, 0.50), (0.28, 0.50), (0.50, 0.56), (0.68, 0.68), (0.78, 0.88), (0.80, 1.2), (0.76, 1.7), (0.70, 2.0), (-0.70, 2.0), (-0.76, 1.7), (-0.80, 1.2), (-0.78, 0.88), (-0.68, 0.68), (-0.50, 0.56)]
    L('coat', coat, '#3c3a48', 0)                                       # frock coat, a lighter navy-grey than the card's base so the silhouette reads
    L('coat_sh', [(-0.74, 1.45), (0.74, 1.45), (0.70, 2.0), (-0.70, 2.0)], '#2c2a34', 1, 0.0)
    L('armL', [(-0.80, 0.9), (-0.58, 0.9), (-0.56, 1.9), (-0.74, 1.9)], '#2c2a34', 1, 0.0); L('armR', [(0.80, 0.9), (0.58, 0.9), (0.56, 1.9), (0.74, 1.9)], '#2c2a34', 1, 0.0)
    L('seam', [(-0.02, 0.75), (0.02, 0.75), (0.02, 2.0), (-0.02, 2.0)], '#16141a', 2, 0.0)
    L('collar', [(-0.40, 0.50), (-0.22, 0.42), (0.22, 0.42), (0.40, 0.50), (0.34, 0.74), (0, 0.84), (-0.34, 0.74)], '#403d4a', 2)          # lapel colour of the card
    L('shirt', [(-0.26, 0.30), (0.26, 0.30), (0.28, 0.52), (-0.28, 0.52)], '#f4efe4', 3, 0.025)                                   # white shirt collar band at the nape
    L('neck', [(-0.20, 0.16), (0.20, 0.16), (0.22, 0.34), (-0.22, 0.34)], '#e0b090', 3, 0.0)
    L('earL', _poly_ellipse(-0.58, 0.02, 0.11, 0.16, 14), '#e0b090', 5, 0.025); L('earR', _poly_ellipse(0.58, 0.02, 0.11, 0.16, 14), '#e0b090', 5, 0.025)
    hair = []
    for k in range(40):
        t = 2 * math.pi * k / 40; rx, ry = 0.58, 0.68; s = math.sin(t)
        edge = 1.0 - (0.06 * (1 + math.cos(10 * t)) / 2 if s > 0.15 else 0.0)
        hair.append((rx * math.cos(t) * edge, -0.06 + ry * s * (0.78 if s > 0 else 1.0) * edge))
    L('hair', hair, '#4a3830', 6, 0.06)                                                                    # brown hair (card #352720, lifted one step for the night light)
    L('hair_hi', _poly_ellipse(-0.12, -0.42, 0.26, 0.10, 20), '#7a6052', 7, 0.0)                         # shine of the card hair
    for i, (x0, y0, x1, y1) in enumerate(((-0.38, -0.10, -0.28, 0.22), (-0.14, -0.20, -0.10, 0.28), (0.14, -0.20, 0.10, 0.30), (0.38, -0.10, 0.30, 0.22), (0.0, -0.48, 0.02, -0.26))):
        dx, dy = (y1 - y0), -(x1 - x0); Ln = math.hypot(dx, dy); dx, dy = dx / Ln * 0.008, dy / Ln * 0.008
        L('str%d' % i, [(x0 - dx, y0 - dy), (x1 - dx, y1 - dy), (x1 + dx, y1 + dy), (x0 + dx, y0 + dy)], '#2a1e18', 8, 0.0)

# ---- T1a: the three bench prisoners seen from behind (hair + coat, same layering as bertillon_back). Colours from the real cards.
PRIS = {'prisoner_a': dict(coat='#6f869e', sh='#5d7389', hair='#4a3830', hi='#7a6052', str='#2a1e18', hat=None),
        'prisoner_b': dict(coat='#6e5c3c', sh='#5a4a30', hair='#4a3a28', hi='#7a6048', str='#2a1e14', hat='bowler'),
        'prisoner_q': dict(coat='#5f7e3e', sh='#4e6a32', hair='#4a3830', hi='#7a6052', str='#2a1e18', hat='cap')}
def prisoner_back(a, c, cam):
    import actors
    d = PRIS[c['name']]
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o
    ex, ey = _billboard_axes(o, ex, ey, cam)
    to = (Vector(cam.location) - o).normalized(); u = 0.006; z0 = 0.03; nm = 'bk_' + c['name']
    L = lambda n, pts, col, k, ol=0.055: _layer('%s_%s' % (nm, n), pts, col, z0 + u * k, o, ex, ey, to, ol)
    coat = [(-0.28, 0.50), (0.28, 0.50), (0.50, 0.56), (0.68, 0.68), (0.78, 0.88), (0.80, 1.2), (0.76, 1.7), (0.70, 2.0), (-0.70, 2.0), (-0.76, 1.7), (-0.80, 1.2), (-0.78, 0.88), (-0.68, 0.68), (-0.50, 0.56)]
    L('coat', coat, d['coat'], 0); L('coat_sh', [(-0.74, 1.45), (0.74, 1.45), (0.70, 2.0), (-0.70, 2.0)], d['sh'], 1, 0.0)
    L('armL', [(-0.80, 0.9), (-0.58, 0.9), (-0.56, 1.9), (-0.74, 1.9)], d['sh'], 1, 0.0); L('armR', [(0.80, 0.9), (0.58, 0.9), (0.56, 1.9), (0.74, 1.9)], d['sh'], 1, 0.0)
    L('seam', [(-0.02, 0.75), (0.02, 0.75), (0.02, 2.0), (-0.02, 2.0)], '#16141a', 2, 0.0)
    L('collar', [(-0.40, 0.50), (-0.22, 0.42), (0.22, 0.42), (0.40, 0.50), (0.34, 0.74), (0, 0.84), (-0.34, 0.74)], d['sh'], 2)
    L('neck', [(-0.20, 0.16), (0.20, 0.16), (0.22, 0.50), (-0.22, 0.50)], '#e0b090', 3, 0.0)
    L('earL', _poly_ellipse(-0.58, 0.02, 0.11, 0.16, 14), '#e0b090', 5, 0.025); L('earR', _poly_ellipse(0.58, 0.02, 0.11, 0.16, 14), '#e0b090', 5, 0.025)
    # head: egg-shaped skull (narrow crown, wider cheek line, flat nape), not an oval
    hair = []
    for k in range(40):
        t = 2 * math.pi * k / 40; s_ = math.sin(t); c_ = math.cos(t)
        rx = 0.58 * (1.0 + 0.06 * s_) if s_ < 0 else 0.58 * (1.0 - 0.10 * s_)
        ry = 0.70 if s_ < 0 else 0.56
        hair.append((rx * c_, -0.06 + ry * s_))
    L('hair', hair, d['hair'], 6, 0.06)
    L('hair_hi', _poly_ellipse(-0.14, -0.40, 0.24, 0.09, 20), d['hi'], 7, 0.0)
    for i, (x0, y0, x1, y1) in enumerate(((-0.38, -0.10, -0.30, 0.20), (-0.16, -0.22, -0.12, 0.26), (0.12, -0.22, 0.10, 0.28), (0.36, -0.10, 0.30, 0.20), (0.0, -0.50, 0.02, -0.28), (-0.26, -0.40, -0.22, -0.18), (0.26, -0.38, 0.22, -0.16))):
        dx, dy = (y1 - y0), -(x1 - x0); Ln = math.hypot(dx, dy); dx, dy = dx / Ln * 0.009, dy / Ln * 0.009
        L('str%d' % i, [(x0 - dx, y0 - dy), (x1 - dx, y1 - dy), (x1 + dx, y1 + dy), (x0 + dx, y0 + dy)], d['str'], 8, 0.0)
    if d['hat'] == 'bowler':      # prisoner_b: brown bowler seen from behind: wide brim, round crown, darker band
        L('crown', [(-0.50, -0.14), (0.50, -0.14), (0.52, -0.40), (0.40, -0.68), (0.0, -0.80), (-0.40, -0.68), (-0.52, -0.40)], '#5a4630', 9, 0.06)
        L('band', [(-0.51, -0.18), (0.51, -0.18), (0.52, -0.30), (-0.52, -0.30)], '#241a12', 10, 0.0)
        L('crown_hi', _poly_ellipse(-0.14, -0.58, 0.20, 0.08, 16), '#8a6e4c', 10, 0.0)
        L('brim', _poly_ellipse(0.0, -0.14, 0.86, 0.17, 30), '#4a3824', 11, 0.06)
    elif d['hat'] == 'cap':       # prisoner_q: flat navy cap: low crown + short peak at the back
        L('crown', [(-0.56, -0.12), (0.56, -0.12), (0.58, -0.42), (0.34, -0.66), (-0.34, -0.66), (-0.58, -0.42)], '#243468', 9, 0.06)
        L('seamc', [(-0.02, -0.64), (0.02, -0.64), (0.02, -0.14), (-0.02, -0.14)], '#141c3a', 10, 0.0)
        L('crown_hi', _poly_ellipse(-0.18, -0.52, 0.18, 0.07, 16), '#4a5c9a', 10, 0.0)
        L('band', [(-0.58, -0.12), (0.58, -0.12), (0.58, -0.22), (-0.58, -0.22)], '#161e40', 10, 0.0)
_orig = P._back_cover
def _patched(a, c, cam):
    if c['name'] == 'bertillon': return bertillon_back(a, c, cam)
    if c['name'] in PRIS: return prisoner_back(a, c, cam)
    return _orig(a, c, cam)
P._back_cover = _patched

def clear_cast():
    import actors
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'back_hair_', 'back_coat_', 'bk_'))]: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()

# ---- white-out / flat-colour fixes (camera path untouched): per frame, drop the faces of the one mesh the lens is inside of, within R of the camera
#   ext_glow_win g55-64 (lit roof-window quad at 0.13 m), ext_stone g57-64 (roof block wall at 0.14 m), measure_glow_gas g145-165 (gasolier glow at 0.07 m)
CULL = {'measure_glow_gas': (145, 165, 1.6)}
_ST = {}
CLIP = {}   # camera grazes a roof-block wall at 0.14 m in g59-61: clip it
def fix_whiteouts(g, cam):
    import bmesh
    cam.data.clip_start = CLIP.get(g, 0.05)
    pu = bpy.data.objects.get('ext_puddle')
    if pu is not None: pu.hide_render = True            # director: puddles off (match T1b)
    for nm, (a, b) in (('measure_beam_fx', (76, 171)),):   # director: beam fx off for all interior frames; window glow off on g60-61 only
        o_ = bpy.data.objects.get(nm)
        if o_ is not None: o_.hide_render = a <= g <= b
    cp = cam.matrix_world.translation
    for name, (g0, g1, R) in CULL.items():
        ob = bpy.data.objects.get(name)
        if ob is None: continue
        if name not in _ST: _ST[name] = [ob.data.copy(), False]
        orig, applied = _ST[name]; on = g0 <= g <= g1
        if on:
            b = bmesh.new(); b.from_mesh(orig); mw = ob.matrix_world
            kill = [f for f in b.faces if (mw @ f.calc_center_median() - cp).length < R or min((mw @ v.co - cp).length for v in f.verts) < R * 0.6]; bmesh.ops.delete(b, geom=kill, context='FACES'); b.to_mesh(ob.data); b.free(); _ST[name][1] = True
        elif applied:
            b = bmesh.new(); b.from_mesh(orig); b.to_mesh(ob.data); b.free(); _ST[name][1] = False

# ---- edge-on rule (director): a cast card whose plane is under ~20 deg to the camera ray reads as a dark sliver -> hide card + back cover for that frame
def edge_on_hide(acts, cam, thresh=0.34, cover_ok=None):
    cover_ok = cover_ok or {}
    import actors
    hid = []
    for name, a in acts.items():
        o, x, y, z, s = actors.card_state(a, cam)
        ray = (o + z * 0.8 * s - cam.matrix_world.translation).normalized()
        if abs(y.normalized().dot(ray)) < thresh:
            hid.append(name)
            if False:       # back view: the camera-facing cover stands in, only the edge-on card art goes
                if a.card is not None: a.card.hide_render = True
                continue
            def walk(ob):
                ob.hide_render = True
                for ch in ob.children: walk(ch)
            walk(a.root)
            for ob in bpy.data.objects:
                if ob.name.startswith('bk_' + name + '_') or ob.name.startswith('back_hair_' + name) or ob.name.startswith('back_coat_' + name): ob.hide_render = True
    for name, a in acts.items():       # any cast member with a camera-facing back cover: the cover stands in for the card art (no card edge peeks out)
        if any(ob.name.startswith('bk_' + name + '_') for ob in bpy.data.objects) and a.card is not None: a.card.hide_render = True
    return hid
