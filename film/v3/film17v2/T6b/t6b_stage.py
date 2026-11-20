"""T6b staging patch: Dupont's over-the-shoulder back view as hair + coat (not a flat black slab).
Replaces prefecture17._back_cover for the T6 'dupont' anchor only (ginger hair dome with strands, ears, nape, red neckerchief, patched brown jacket with
collar, shoulders and seam, every piece with a dark ink outline). Other anchors keep the stock cover. Card-plane units as in _back_cover (head radius 0.56)."""
import math, sys, os
import bpy
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'set3d17'))
import prefecture17 as P

INK = '#1a1020'
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

def dupont_back(a, c, cam):
    import actors
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o
    to = (Vector(cam.location) - o).normalized(); u = 0.006; z0 = 0.03; nm = 'bk_' + c['name']
    L = lambda n, pts, col, k, ol=0.055: _layer('%s_%s' % (nm, n), pts, col, z0 + u * k, o, ex, ey, to, ol)
    # coat: sloped shoulders, upper arms, hem (jacket brown #7a5a3a of cast17 dupont), darker lower half = fold in shade
    coat = [(-0.30, 0.50), (0.30, 0.50), (0.55, 0.56), (0.75, 0.68), (0.88, 0.88), (0.92, 1.2), (0.88, 1.7), (0.80, 2.0), (-0.80, 2.0), (-0.88, 1.7), (-0.92, 1.2), (-0.88, 0.88), (-0.75, 0.68), (-0.55, 0.56)]
    L('coat', coat, '#7a5a3a', 0)
    L('coat_sh', [(-0.84, 1.45), (0.84, 1.45), (0.82, 2.0), (-0.82, 2.0)], '#6a4c30', 1, 0.0)
    L('armL', [(-0.90, 0.9), (-0.66, 0.9), (-0.64, 1.9), (-0.84, 1.9)], '#6a4c30', 1, 0.0); L('armR', [(0.90, 0.9), (0.66, 0.9), (0.64, 1.9), (0.84, 1.9)], '#6a4c30', 1, 0.0)
    L('seam', [(-0.02, 0.75), (0.02, 0.75), (0.02, 2.0), (-0.02, 2.0)], '#4a3320', 2, 0.0)
    L('patch', [(-0.62, 1.05), (-0.34, 1.05), (-0.34, 1.3), (-0.62, 1.3)], '#5a86b4', 2, 0.018)       # the blue patch of the card jacket
    L('patch2', [(0.30, 1.30), (0.56, 1.30), (0.56, 1.52), (0.30, 1.52)], '#d0a040', 2, 0.018)
    L('collar', [(-0.40, 0.50), (-0.22, 0.42), (0.22, 0.42), (0.40, 0.50), (0.34, 0.74), (0, 0.84), (-0.34, 0.74)], '#6a4c30', 2)
    L('neck', [(-0.22, 0.20), (0.22, 0.20), (0.24, 0.52), (-0.24, 0.52)], '#e0a888', 3, 0.025)       # skin nape under the hair
    L('scarf', [(-0.30, 0.50), (0.0, 0.40), (0.30, 0.50), (0.26, 0.64), (0.0, 0.72), (-0.26, 0.64)], '#b8402e', 4, 0.025)   # red neckerchief knot at the nape
    # ears, then the hair dome over the head (covers the flat cap's top)
    L('earL', _poly_ellipse(-0.60, 0.04, 0.12, 0.17, 14), '#e0a888', 5, 0.025); L('earR', _poly_ellipse(0.60, 0.04, 0.12, 0.17, 14), '#e0a888', 5, 0.025)
    hair = []
    for k in range(40):   # ginger dome rx 0.60, ry 0.70, with a ragged lower edge at the nape (scallops)
        t = 2 * math.pi * k / 40; rx, ry = 0.60, 0.70; s = math.sin(t)
        edge = 1.0 - (0.07 * (1 + math.cos(10 * t)) / 2 if s > 0.15 else 0.0)
        hair.append((rx * math.cos(t) * edge, -0.06 + ry * s * (0.78 if s > 0 else 1.0) * edge))
    L('hair', hair, '#9a5a2c', 6, 0.06)
    L('hair_hi', _poly_ellipse(-0.12, -0.44, 0.26, 0.10, 20), '#b87238', 7, 0.0)                 # lit top
    for i, (x0, y0, x1, y1) in enumerate(((-0.40, -0.10, -0.30, 0.22), (-0.14, -0.20, -0.10, 0.28), (0.14, -0.20, 0.10, 0.30), (0.40, -0.10, 0.32, 0.22), (0.0, -0.50, 0.02, -0.28))):
        dx, dy = (y1 - y0), -(x1 - x0); Ln = math.hypot(dx, dy); dx, dy = dx / Ln * 0.008, dy / Ln * 0.008
        L('str%d' % i, [(x0 - dx, y0 - dy), (x1 - dx, y1 - dy), (x1 + dx, y1 + dy), (x0 + dx, y0 + dy)], '#6a3a1a', 8, 0.0)        # strand lines

_orig = P._back_cover
def _patched(a, c, cam):
    if c['name'] == 'dupont': return dupont_back(a, c, cam)
    return _orig(a, c, cam)
P._back_cover = _patched
