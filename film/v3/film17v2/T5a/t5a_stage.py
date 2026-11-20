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
_orig = P._back_cover
def _patched(a, c, cam):
    if c['name'] == 'bertillon': return bertillon_back(a, c, cam)
    return _orig(a, c, cam)
P._back_cover = _patched
