#!/usr/bin/env python3
"""Film 17 v2, take T8 (ending), part P3: g1862-2052. Real cast17 cards through stage_cast2, frame by frame (frame = g + 1).
usage: python3 render.py still <g> out.png [W H samples]      one full-res still
       python3 render.py range g0 g1 out_dir                   frames (resume: skips existing PNG > 50 kB)
The calipers are held by Bertillon's WHITE GLOVE hand (cast10 gloves10, added to his CAST entry here at runtime) and close on the red ear
(slide jaw travels g2018-2044, hold to g2052)."""
import sys, os, math, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'film/v3/set3d17')); sys.path.insert(0, os.path.join(ROOT, 'film/v3/cast17')); sys.path.insert(0, os.path.join(ROOT, 'film/v3/stage'))
import prefecture17 as P, bpy, cast17, puppet
import actors
TAKE = 'T8'

# ---------------------------------------------------------------- white glove on Bertillon (v1 ending failed: the hand drew as black bars)
puppet.CAST['bertillon']['gloves10'] = '#f6f4ee'

_prev_hand = puppet._hand
def _hand2(k, H, dirv, shape, hr=puppet.HAND_R, fold=1.0):
    C = cast17.C10.CE._CUR[0]
    if C and C.get('gloves10'): hr = hr * 1.35        # a bigger white glove: it reads at phone size
    return _prev_hand(k, H, dirv, shape, hr, fold)
puppet._hand = _hand2

# ---------------------------------------------------------------- calipers whose slide jaw closes: SLIDE = x shift of the sliding jaw (0 open .. CLOSED shut on the ear)
SLIDE = [0.0]; CLOSED = 0.27; GRIP = float(os.environ.get('GRIP', 0.62)); _orig_body = cast17._calipers_body
def _body(k):
    s = SLIDE[0]; STEEL = cast17.STEEL; BRASS = cast17.BRASS; g = cast17._lin(k, "cb", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.12,-0.034 L0.88,-0.034 L0.88,0.034 L-0.12,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    tk = "".join("M%.3f,0.034 L%.3f,%.3f " % (x, x, 0.034 + (0.034 if i % 5 == 0 else 0.020)) for i, x in enumerate([0.02 + 0.04 * j for j in range(20)]))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (tk, k.c(STEEL["deep"])))
    o.append('<path d="M-0.08,-0.018 L0.84,-0.018" stroke="#ffffff" stroke-width="0.008" opacity="0.7" stroke-linecap="round"/>')
    o.append('<path d="M0.80,0.030 L0.88,0.030 L0.88,0.24 L0.835,0.27 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(STEEL["base"]), k.ink))
    o.append('<g transform="translate(%.4f 0)"><path d="M0.40,-0.050 L0.52,-0.050 L0.52,0.034 L0.52,0.22 L0.485,0.25 L0.46,0.034 L0.40,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             '<circle cx="0.46" cy="-0.075" r="0.036" fill="%s" stroke="%s" stroke-width="0.014"/><path d="M0.44,-0.085 L0.48,-0.065" stroke="%s" stroke-width="0.008"/></g>'
             % (s, k.c(STEEL["light"]), k.ink, k.c(BRASS["base"]), k.ink, k.c(BRASS["dark"])))
    return '<g transform="translate(%.3f 0)">%s</g>' % (-GRIP, "".join(o))      # the glove grips the beam GRIP behind the jaws' end, so the hand stays in frame
cast17._calipers_body = _body
_prev_prop = puppet._prop
def _prop2(k, kind, H, ang, sc=1.0):
    out = _prev_prop(k, kind, H, ang, sc)
    if kind == 'calipers':                       # the anchor = between the jaw tips of the CLOSED calipers (the ear sits there)
        an = cast17.C10.C8._POSE8["an"]; key = cast17.C10.C8._side_key(); jx, jy = cast17._rot((0.5 * (0.485 + CLOSED + 0.835) - GRIP) * sc, 0.25 * sc, ang); k.ext.append((H[0] + cast17._rot(-0.55 * sc, 0, ang)[0], H[1] + cast17._rot(-0.55 * sc, 0, ang)[1], 0.03)); an["calipers_" + key] = (H[0] + jx, H[1] + jy)
    return out
puppet._prop = _prop2

# ---------------------------------------------------------------- richer back view for the OTS gendarme (QA: the back cover must read as hair + coat, not a black slab)
def _poly(name, pts, col, layer, o, ex, ey, to):
    V = [tuple(o + to * (1.0 + 0.12 * layer) + ex * x + ey * y) for (x, y) in pts]
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], [tuple(range(len(V)))]); me.update(); me.materials.append(P._flat('cc_bk_' + col[1:], col))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
def _ell(cx, cy, rx, ry, n=24): return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]
def back_cover(a, c, cam):
    from mathutils import Vector
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o
    to = (Vector(cam.location) - o).normalized() * 0.03; nm = 'back_' + c['name']; I = '#16141a'
    layers = [(_ell(0, 0.02, 0.57, 0.57), I), (_ell(0, 0.02, 0.52, 0.52), '#5a3a26'),                      # head with ink ring + hair
              ([(-0.50, 0.55), (0.50, 0.55), (0.50, 0.62), (-0.50, 0.62)], '#5a3a26'),
              ([(-0.17, 0.40), (0.17, 0.40), (0.19, 0.66), (-0.19, 0.66)], '#d9a98c'),                       # nape of the neck
              ([(-0.80, 0.52), (0.80, 0.52), (0.84, 2.05), (-0.84, 2.05)], I),                                # cape (ink edge)
              ([(-0.77, 0.56), (0.77, 0.56), (0.80, 2.0), (-0.80, 2.0)], '#2a3a7c'),
              ([(-0.77, 0.56), (-0.20, 0.56), (-0.26, 2.0), (-0.80, 2.0)], '#34478a'),                       # lit left fold
              ([(-0.03, 0.60), (0.03, 0.60), (0.04, 2.0), (-0.04, 2.0)], '#1c2a5a'),                         # centre seam
              ([(-0.77, 1.90), (0.80, 1.90), (0.80, 2.0), (-0.80, 2.0)], '#c8402e'),                          # mustard/red lining at the hem
              ([(-0.40, 0.50), (0.40, 0.50), (0.46, 0.74), (-0.46, 0.74)], '#1c2a5a'),                       # collar
              ([(-0.70, 0.58), (-0.40, 0.58), (-0.42, 0.74), (-0.72, 0.72)], '#d8c060'),                      # epaulette gold
              ([(0.40, 0.58), (0.70, 0.58), (0.72, 0.72), (0.42, 0.74)], '#d8c060'),
              ([(-0.54, -0.60), (0.54, -0.60), (0.58, -0.12), (-0.58, -0.12)], I),                            # kepi (ink)
              (_ell(0, -0.36, 0.55, 0.30), '#34478a'), ([(-0.55, -0.34), (0.55, -0.34), (0.55, -0.12), (-0.55, -0.12)], '#34478a'),
              ([(-0.55, -0.24), (0.55, -0.24), (0.55, -0.12), (-0.55, -0.12)], '#c8402e'),                    # red band
              ([(-0.55, -0.26), (0.55, -0.26), (0.55, -0.24), (-0.55, -0.24)], '#d8dce6'),                    # piping
              (_ell(-0.18, -0.50, 0.22, 0.07), '#9ab0e0')]                                                    # shine
    for i, (pts, col) in enumerate(layers): _poly('%s_%02d' % (nm, i), pts, col, i, o, ex, ey, to)
P._back_cover = lambda a, c, cam: back_cover(a, c, cam)

# ---------------------------------------------------------------- poses
S = cast17.STORY17
def _ss(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def _ramp(g, a, b): return (g - a) / float(b - a)
I_c, I_p = S['inspector_seated_stiff']
S['insp_red_seated'] = (I_c, dict(I_p, expr='furious', mouth='clench', flush17=1.0, fx=['sweat'], seat17='chair', pitch=0.0, yaw=0.10, gaze=(-0.8, 0.0)))   # red-faced, sitting stiff
B_c, B_p = S['bertillon_measuring']
BDX0 = float(os.environ.get('BDX0', -1.25)); BHS = float(os.environ.get('BHS', 1.0))
BDXE = float(os.environ.get('BDXE', -1.1)); BDX2 = float(os.environ.get('BDX2', -1.2)); SHY = float(os.environ.get('SHY', 0.14)); SHG0 = int(os.environ.get('SHG0', 1868)); SHG1 = int(os.environ.get('SHG1', 1892)); BDX3 = float(os.environ.get('BDX3', -1.1)); PFDX = float(os.environ.get('PFDX', -0.6)); BDG0 = int(os.environ.get('BDG0', 2030))
def bnudge(g):
    """Bertillon's offset from his anchor ML(1.3,1.85): beside the chair on the inspector's right (screen-left), nearer the camera than the head so the jaws draw in front;
    he steps toward the chair for the clamp (g2012-2040) so the glove stays in frame as the camera pushes in."""
    return (BDX0 + (BDXE - BDX0) * _ss(_ramp(g, 2012, 2040)) + (BDX2 - BDXE) * _ss(_ramp(g, BDG0, 2040)) + (BDX3 - BDX2) * _ss(_ramp(g, 2040, 2052)), -0.10)     # dx, dy (m): Bertillon stands beside the chair (not in front of the inspector's face), same depth as the chair
EAR_X = 0.52; EAR_ANG = float(os.environ.get('EAR_ANG', -30))


def bertillon_pose(g):
    """calm until 1958; g1958-2018 the arm rises with the open calipers; g2018-2044 the jaws close on the ear; held to 2052."""
    rest = dict(B_p, mirror=False, arm_r=dict(hand=(0.50, 1.05), bend=0.3, stretch=1.0, layer='front'), prop_r=dict(B_p['prop_r'], angle=70), pitch=0.0, expr='determined', mouth='flat')
    ear = cast17.hand_for_anchor(B_c, dict(B_p, mirror=False, prop_r=dict(B_p['prop_r'], angle=EAR_ANG)), 'r', 'calipers_r', ear_target(g))
    t = _ss(_ramp(g, 1958, 2012)); a = rest['arm_r']['hand']; b = ear['arm_r']['hand']
    pose = dict(rest, arm_r=dict(rest['arm_r'], hand=(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), bend=0.3 + (ear['arm_r'].get('bend', -0.2) - 0.3) * t),
                prop_r=dict(rest['prop_r'], angle=70 + (EAR_ANG - 70) * t))
    SLIDE[0] = CLOSED * _ss(_ramp(g, 2022, 2044))
    return pose
def _bert_story(g):
    S['bertillon_t8'] = (B_c, bertillon_pose(g)); return 'bertillon_t8'

def _addo(d, tag, g):
    """director fix 2/3: step the swept / cut-off crowd members out of the crane's path over g1890-1932 (in 1890-1900, out 1924-1932)."""
    v = os.environ.get(tag, DEF_OFF.get(tag, '0,0')); dx, dy = [float(x) for x in v.split(',')]
    a0, a1, b0, b1 = WIN.get(tag, (1890, 1900, 1924, 1932)); w = _ss(_ramp(g, a0, a1)) * (1 - _ss(_ramp(g, b0, b1))); d = dict(d); d['dx'] = d.get('dx', 0.0) + dx * w; d['dy'] = d.get('dy', 0.0) + dy * w; return d
DEF_OFF = {'C2': '-1.8,1.2', 'GB': '-1.6,0.8'}; WIN = {'C2': (1880, 1892, 1926, 1932), 'GB': (1880, 1892, 1922, 1932)}
def assign_for(g):
    cl = 'gendarme_laughing_a'; clb = 'gendarme_laughing_b'
    grin = lambda nm, base: (nm, {})
    t = _ss(_ramp(g, 1985, 2006)); gn = {'dx': 1.0 * t, 'dy': 2.0 * t}     # the OTS gendarme steps aside as the camera passes (his head would leave the top edge)
    a = {'inspector': ('insp_red_seated', {'seated': 'chair', 'dy': -0.14}), 'bertillon': (_bert_story(g), {'dx': bnudge(g)[0], 'dy': bnudge(g)[1], 'H': P.K.CAST_H['bertillon'] * (1 - (1 - BHS) * _ss(_ramp(g, 2012, 2040)))}),
         'gend_a': (cl, _addo(gn, 'GA', g)), 'gend_b': (clb, _addo({}, 'GB', g)), 'crowd2': (cl, _addo({}, 'C2', g)),
         'crowd1': ('prisoner_standing_a', {'expr': 'laugh'}), 'crowd3': ('prisoner_standing_c', {'expr': 'laugh'}), 'prefect': ('prefect_neutral', {'dx': PFDX * _ss(_ramp(g, 2010, 2030))})}
    return a
# expression overrides: opts 'expr' for the prisoners' grin
def add_ears(a, cam):
    """the inspector's red ears (the puppet has none): one each side, behind the head disc so only the outer half shows; the calipers close on the screen-left one."""
    from mathutils import Vector
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); ex = L2W((1.0, 0.0)) - o; ey = L2W((0.0, 1.0)) - o; to = (Vector(cam.location) - o).normalized() * 0.03
    for sgn in (-1, 1):
        cx = sgn * EAR_X
        _poly('back_ear_o%d' % sgn, _ell(cx, 0.06, 0.15, 0.22), '#16141a', 2, o, ex, ey, to * -0.2); _poly('back_ear_f%d' % sgn, _ell(cx, 0.06, 0.125, 0.195), '#e23f2a', 1, o, ex, ey, to * -0.2)
        _poly('back_ear_i%d' % sgn, _ell(cx + sgn * 0.02, 0.07, 0.06, 0.12), '#a8281c', 0, o, ex, ey, to * -0.2)
def clean():
    for a in list(actors.REGISTRY): pass
    for o in list(bpy.data.objects):
        if o.name.startswith(('c2_', 'back_')) or '_c2_' in o.name: bpy.data.objects.remove(o, do_unlink=True)
    actors.clear_registry()
    for blk in (bpy.data.meshes, bpy.data.images):
        for d in list(blk):
            if d.users == 0: blk.remove(d)

def ear_target(g):
    """jaw-target in Bertillon's puppet-local D: the inspector's (screen-right) ear relative to Bertillon's head, from the cast geometry."""
    ct = {c['name']: c for c in P.TAKES[TAKE]['cast']}; pi = P.cast_pos(ct['inspector'], g); pb = P.cast_pos(ct['bertillon'], g)
    hs = 1 - (1 - BHS) * _ss(_ramp(g, 2012, 2040)); sb = P.K.CAST_H['bertillon'] * hs / P.K.CAST_HD['bertillon']; si = P.K.CAST_H['inspector17'] / P.K.CAST_HD['inspector17']
    dx = (pi[0] - (pb[0] + bnudge(g)[0]) - EAR_X * si) / sb          # world +x is screen right here (camera looks +y); the ear is 0.5 D left of the inspector's head
    zi = P.FZ + P.K.HEAD_Z['chair'] + 0.10 * si; zb = P.FZ + P.K.CAST_H['bertillon'] * hs - 0.51 * sb - 0.0   # head centre height of Bertillon (head top 0.51 D above the head centre)
    return (dx + (float(os.environ.get('TX', 0.27)) + float(os.environ.get('TX2', 0.25)) * _ss(_ramp(g, 2024, 2040))), (zb - zi) / sb + float(os.environ.get('TY', 0.18)) + float(os.environ.get('TY2', 0.0)) * _ss(_ramp(g, 2024, 2040)))       # +(-0.08, +0.18) D: measured on the g2052 still (jaws onto the ear, not above it)

_orig_sc = P.K.sliding_calipers
def _sc(B, c, *a, **k):          # director: the thin light stick by the small table = calipers lying on it; hidden for T8
    if tuple(round(v, 3) for v in c) == (-0.02, -0.05, 0.808): return
    return _orig_sc(B, c, *a, **k)
P.K.sliding_calipers = _sc
_orig_ink = P.K.inkpot
def _ink(B, c, *a, **k):          # its quill reads as a thin light stick at the right edge: skipped on the small calipers table
    if tuple(round(v, 3) for v in c) == (-0.3, 0.15, 0.808): return
    return _orig_ink(B, c, *a, **k)
P.K.inkpot = _ink

from mathutils import Vector as _V, Matrix as _M
def _lookrot_smooth(loc, look, up_hint=(0, 1, 0)):
    """director fix: the stock look-at flips its up vector (+y -> +z) at |f.z| = 0.995 (a ~18 deg roll jump at g1877). Slerp between the two look-at rotations over |f.z| 0.998 -> 0.80."""
    f = (_V(look) - _V(loc)).normalized(); a = abs(f.z)
    def rot(up):
        rgt = f.cross(up).normalized(); u = rgt.cross(f); return _M((rgt, u, -f)).transposed().to_quaternion()
    if a > 0.99999: return rot(_V((0, 1, 0)))
    s = min(1.0, max(0.0, (0.998 - a) / 0.198)); s = s * s * (3 - 2 * s)
    qy = rot(_V((0, 1, 0))); qz = rot(_V((0, 0, 1)))
    if qy.dot(qz) < 0: qz.negate()
    return qy.slerp(qz, s)
_orig_lookrot = P._lookrot; P._lookrot = _lookrot_smooth
def setup(still_g=None):
    A = P.world_build(TAKE); P.key_take(TAKE); P.setup_render2((720, 1280), samples=16, threads=2)
    for o in bpy.data.objects:
        if 'beam' in o.name: o.hide_render = True; o.visible_camera = False; o.visible_shadow = False; print('hidden shaft', o.name)
    if os.environ.get('GROUND'):
        import bmesh
        me = bpy.data.meshes.new('t8_ground'); S_ = 400.0; me.from_pydata([(-S_, -S_, 0), (S_, -S_, 0), (S_, S_, 0), (-S_, S_, 0)], [], [(0, 1, 2, 3)])
        ob = bpy.data.objects.new('t8_ground', me); bpy.context.scene.collection.objects.link(ob); ob.location = (0, 0, P.FZ - 0.35)
        m = bpy.data.materials.new('t8_ground_m'); m.use_nodes = True; bs = m.node_tree.nodes['Principled BSDF']; c = os.environ.get('GCOL', '2b3562'); r, g_, b = [int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
        bs.inputs['Base Color'].default_value = (r ** 2.2, g_ ** 2.2, b ** 2.2, 1); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Emission Color'].default_value = (r ** 2.2, g_ ** 2.2, b ** 2.2, 1); bs.inputs['Emission Strength'].default_value = 1.0; ob.data.materials.append(m)
    return A

def do_frame(g, out, sprite_dir):
    bpy.context.scene.frame_set(g + 1); clean()
    bpy.context.scene.camera.data.shift_y = -SHY * (1 - _ss(_ramp(g, SHG0, SHG1)))      # director fix 2: slide the opening framing so the void band above the room is out of the picture
    acts = P.stage_cast2(TAKE, g, assign_for(g), sprite_dir=sprite_dir)
    if not os.environ.get('NOEARS'): add_ears(acts['inspector'], bpy.context.scene.camera)
    bpy.context.scene.render.filepath = out; bpy.ops.render.render(write_still=True); P.grade2(out)

if __name__ == '__main__':
    a = sys.argv[1:]; sd = os.path.join(HERE, 'sprites')
    if a[0] == 'still':
        g = int(a[1]); setup()
        if len(a) > 3: P.setup_render2((int(a[3]), int(a[4])), samples=int(a[5]), threads=2)
        do_frame(g, a[2], sd)
    elif a[0] == 'range':
        g0, g1, od = int(a[1]), int(a[2]), a[3]; os.makedirs(od, exist_ok=True); setup()
        for g in range(g0, g1 + 1):
            p = os.path.join(od, 'g_%04d.png' % g)
            if os.path.exists(p) and os.path.getsize(p) > 50000: continue
            import time; t = time.time(); do_frame(g, p, sd); print('g%d %.1fs' % (g, time.time() - t), flush=True)
