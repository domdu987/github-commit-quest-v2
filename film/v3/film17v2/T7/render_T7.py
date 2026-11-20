import sys, os, time, math, random
CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'film/v3/set3d17')); os.chdir(os.path.join(ROOT, 'film/v3/set3d17'))
sys.path.insert(0, os.path.join(ROOT, 'film/v3/stage')); sys.path.insert(0, os.path.join(ROOT, 'film/v3/cast17'))
import prefecture17 as P, bpy
from mathutils import Vector
take = 'T7'
SHADE_MUL = float(os.environ.get('T7_SHADE', 1.38)); FILL_W = float(os.environ.get('T7_FILL', 540))
P.TAKE_OVER['T7'] = {'archive': dict(shade_mul=SHADE_MUL, fill_w=FILL_W, **({'beam_k': float(os.environ['T7_BEAM'])} if 'T7_BEAM' in os.environ else {}))}           # director: raise lights (lights only)
_sd = P.K.set_drawer
P.K.set_drawer = lambda name, open=1.0, frame=None: _sd(name, min(open, 0.42) if name == 'big' else open, frame)   # drawer tip stays clear of Bertillon (x 14.35)
LOOK_DY = float(os.environ.get('T7_LOOKDY', 0.35)); DUP_DY = float(os.environ.get('T7_DUPDY', -0.3))
for k in P.TAKES['T7']['keys']:
    if k['g'] in (1689, 1792): k['look'] = (k['look'][0], k['look'][1] + LOOK_DY, k['look'][2])
def assign_for(g):
    a = {'inspector': ('inspector_shocked', {}), 'gend_b': ('gendarme_standing_b', {})}
    if g < 1792:   # 7a
        a['bertillon'] = ('bertillon_holding_card', {}); a['dupont'] = ('dupont_caught' if g < 1755 else 'dupont_innocent', {'dy': DUP_DY})
    else:          # 7b
        a['bertillon'] = ('bertillon_triumphant', {}); a['dupont'] = ('dupont_innocent', {'dy': DUP_DY})
        a['gend_a'] = ('gendarme_escort_a', {}); a['thief1'] = ('prisoner_standing_a', {}); a['thief2'] = ('prisoner_standing_b', {})
    return a
# ---------------- fake beard + moustache, pinned to Dupont's head anchor (card-local, D units, y down) ----------------
BEARD_ON, BEARD_OFF0, BEARD_OFF1 = 1697, 1745, 1755
_beard_objs = []
def _poly_mesh(name, pts, mat, o, ex, ey, to):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    V = [tuple(o + to + ex * cx + ey * cy)] + [tuple(o + to + ex * x + ey * y) for x, y in pts]; n = len(pts)
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], [(0, 1 + k, 1 + (k + 1) % n) for k in range(n)]); me.update(); me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; _beard_objs.append(ob); return ob
def _beard_shapes():
    beard = []
    for i in range(0, 41):   # cheek top-left -> bushy lower edge -> cheek top-right
        t = i / 40.0; x = -0.46 + 0.92 * t; u = abs(x) / 0.46
        y = 0.62 + 0.17 * (1 - u * u) + 0.045 * math.sin(t * 38.0) if 0.05 < t < 0.95 else 0.12 + 0.5 * (1 - min(t, 1 - t) / 0.05) * 0.0
        if t <= 0.05 or t >= 0.95: y = 0.16 + 0.3 * (0.05 - min(t, 1 - t)) / 0.05 * 0.5
        beard.append((x, y))
    top = [(0.36, 0.2), (0.18, 0.3), (0.0, 0.33), (-0.18, 0.3), (-0.36, 0.2)]      # inner edge under the moustache (right to left)
    beard = beard + top
    m = []
    for i in range(0, 21):    # moustache: bushy, tips curl up
        t = i / 20.0; x = -0.36 + 0.72 * t; u = abs(x) / 0.36
        m.append((x, 0.2 - 0.07 * u ** 3 + 0.0))
    for i in range(20, -1, -1):
        t = i / 20.0; x = -0.36 + 0.72 * t; u = abs(x) / 0.36
        m.append((x, 0.3 + 0.07 * (1 - u * u) - 0.1 * u ** 3 + 0.015 * math.sin(t * 25.0)))
    return beard, m
def put_beard(g, a, cam):
    global _beard_objs
    for ob in _beard_objs:
        bpy.data.objects.remove(ob, do_unlink=True)
    _beard_objs = []
    if g < BEARD_ON or g > BEARD_OFF1: return
    import actors
    off = max(0.0, min(1.0, (g - BEARD_OFF0) / float(BEARD_OFF1 - BEARD_OFF0))); off = off * off * (3 - 2 * off)
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o
    s = 1.0 - 0.35 * off; sl = 0.9 * off                      # slide off downward and shrink
    to = (Vector(cam.location) - o).normalized() * 0.05
    beard, mous = _beard_shapes(); S = lambda pts, k=1.0: [(x * s * k, (y - 0.15) * s * k + sl) for x, y in pts]
    ol = P._flat('beard_ol', '#1a0e08'); br = P._flat('beard_fill', '#5b3516'); hi = P._flat('beard_hi', '#7a4a22'); mo = P._flat('mous_fill', '#3a200f')
    bc = (0.0, 0.42); grow = lambda pts, f: [(bc[0] + (x - bc[0]) * f, bc[1] + (y - bc[1]) * f) for x, y in pts]
    _poly_mesh('beard_ol', S(grow(beard, 1.10)), ol, o, ex, ey, to * 0.6); _poly_mesh('beard_fill', S(beard), br, o, ex, ey, to * 0.75)
    for k, x0 in enumerate((-0.28, -0.05, 0.2)):      # lighter hair strands
        _poly_mesh('beard_hi%d' % k, S([(x0, 0.45), (x0 + 0.07, 0.45), (x0 + 0.1, 0.72), (x0 + 0.02, 0.76)]), hi, o, ex, ey, to * 0.85)
    mc = (0.0, 0.25); mg = lambda pts, f: [(mc[0] + (x - mc[0]) * f, mc[1] + (y - mc[1]) * f) for x, y in pts]
    _poly_mesh('mous_ol', S(mg(mous, 1.16)), ol, o, ex, ey, to * 0.9); _poly_mesh('mous_fill', S(mous), mo, o, ex, ey, to * 1.0)
# ---------------- 7b: drawers pop open along both walls, cards fly ----------------
_POP = []
def build_pop():
    rnd = random.Random(7); z0 = P.FZ; ids = 0
    dmat = P._flat('pop_drawer', '#d9953c'); dmat2 = P._flat('pop_inside', '#3a1c16'); paper = P._flat('pop_card', '#f2e6c8'); pr = P._flat('pop_card_ol', '#3a2a22')
    for side, face, sgn in (('W', P.AX0 + 0.55 + 0.036, 1.0), ('E', P.AX1 - 0.55 - 0.036, -1.0)):
        for i, y in enumerate([2.6 + 1.05 * k for k in range(30)]):
            zc = z0 + 0.5 + rnd.choice((0.0, 0.5, 1.0, 1.5, 2.0, 2.5)) + (0 if rnd.random() < 0.7 else 0.0)
            w, h, d = 0.43, 0.23, 0.34
            me = bpy.data.meshes.new('pop'); hw, hh = w / 2, h / 2
            V = [(x, yy, zz) for x in (0, sgn * d) for yy in (-hw, hw) for zz in (-hh, hh)]
            F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (1, 5, 7, 3), (0, 2, 6, 4)]
            me.from_pydata(V, [], F); me.update(); me.materials.append(dmat)
            ob = bpy.data.objects.new('pop_%s%d' % (side, i), me); bpy.context.scene.collection.objects.link(ob); ob.location = (face - sgn * d, y, zc)
            t0 = 1796 + int(((i * 7 + (3 if side == 'E' else 0)) % 30) * 1.3) + rnd.randint(0, 3)
            cd = bpy.data.objects.new('flycard_%s%d' % (side, i), None)
            cme = bpy.data.meshes.new('fc'); cme.from_pydata([(-0.11, 0, -0.075), (0.11, 0, -0.075), (0.11, 0, 0.075), (-0.11, 0, 0.075)], [], [(0, 1, 2, 3)]); cme.update(); cme.materials.append(paper)
            card = bpy.data.objects.new('flycard_%s%d' % (side, i), cme); bpy.context.scene.collection.objects.link(card)
            _POP.append(dict(ob=ob, card=card, face=face, sgn=sgn, y=y, zc=zc, d=d, t0=t0, ang=rnd.uniform(-40, 40), tgt=(P.AX0 + 4.0 + rnd.uniform(-1.4, 1.4), y + rnd.uniform(-2.5, 2.5), 6.5 + rnd.uniform(0, 3.0))))
def key_pop(g0, g1):
    for p in _POP:
        for g in range(g0, g1 + 1):
            f = g + 1; t = max(0.0, min(1.0, (g - p['t0']) / 9.0)); e = 1 - (1 - t) ** 3; e = e + 0.12 * math.sin(math.pi * t) * (1 - t)   # pop with a small overshoot
            p['ob'].location = (p['face'] - p['sgn'] * p['d'] + p['sgn'] * 0.0 + p['sgn'] * p['d'] * 0.0 + p['sgn'] * (p['d'] * 0.0), p['y'], p['zc'])
            p['ob'].location.x = p['face'] - p['sgn'] * p['d'] + p['sgn'] * p['d'] * e
            p['ob'].keyframe_insert('location', frame=f)
            tf = (g - (p['t0'] + 7)) / 38.0; c = p['card']; vis = 0.0 <= tf <= 1.0
            if vis:
                a = 1 - (1 - tf) ** 2; x0 = p['face'] + p['sgn'] * p['d']
                c.location = (x0 + (p['tgt'][0] - x0) * a, p['y'] + (p['tgt'][1] - p['y']) * a, p['zc'] + (p['tgt'][2] - p['zc']) * a + 0.9 * math.sin(math.pi * a))
                c.rotation_euler = (math.radians(70 * tf), math.radians(p['ang'] * tf * 3), math.radians(360 * tf * (1 if p['sgn'] > 0 else -1)))
                c.scale = (1, 1, 1)
            else:
                c.scale = (0.0001, 0.0001, 0.0001)
            for path in ('location', 'rotation_euler', 'scale'): c.keyframe_insert(path, frame=f)
def clear_cast():
    import actors
    for o in list(bpy.data.objects):
        if o.name.startswith(('c2_', 'back_hair_', 'back_coat_')): bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
def main(gl, outdir, samples=16):
    assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']
    A = P.world_build(take)
    if True:   # director: beam_fx veils the crane (g1820 diff 9.5/255): beams off for the whole take
        for m in bpy.data.materials:
            if m.name.startswith('beam_fx') and m.node_tree: m.node_tree.nodes['strength'].inputs[1].default_value = float(os.environ.get('T7_BEAM', '0')) * 0.035
    P.key_take(take); build_pop(); key_pop(1689, 1874); P.setup_render2((720, 1280), samples=samples, threads=2)
    sc = bpy.context.scene
    for g in gl:
        fp = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(fp) and os.path.getsize(fp) > 50000: continue
        t = time.time(); sc.frame_set(g + 1)
        sc.render.use_motion_blur = 1800 <= g <= 1867
        if sc.render.use_motion_blur: sc.render.motion_blur_shutter = 0.5
        clear_cast(); acts = P.stage_cast2(take, g, assign_for(g)); put_beard(g, acts['dupont'], sc.camera); sc.render.filepath = fp
        bpy.ops.render.render(write_still=True); P.grade2(fp); print('g', g, '%.0fs' % (time.time() - t), flush=True)
if __name__ == '__main__':
    # usage: render_T7.py g0 g1 outdir [samples]   |   render_T7.py g,g,g outdir [samples]  (stills)
    if ',' in sys.argv[1] or len(sys.argv) < 4 or not sys.argv[2].isdigit(): GL = [int(x) for x in sys.argv[1].split(',')]; out = os.path.abspath(os.path.join(CWD, sys.argv[2])); smp = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    else: GL = None
    if GL is not None: main(GL, out, smp)
    else: main(list(range(int(sys.argv[1]), int(sys.argv[2]) + 1)), os.path.abspath(os.path.join(CWD, sys.argv[3])), int(sys.argv[4]) if len(sys.argv) > 4 else 16)
