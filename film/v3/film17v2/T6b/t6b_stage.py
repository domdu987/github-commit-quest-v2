"""T6b staging patch: Dupont's over-the-shoulder back view as hair + coat (not a flat black slab).
Replaces prefecture17._back_cover for the T6 'dupont' anchor only (ginger hair dome with strands, ears, nape, red neckerchief, patched brown jacket with
collar, shoulders and seam, every piece with a dark ink outline). Other anchors keep the stock cover. Card-plane units as in _back_cover (head radius 0.56)."""
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

def clear_cast():
    """remove last frame's cast cards, back covers and T6b props (multi-frame loops in one process)"""
    import actors
    for a in list(actors.REGISTRY):
        try:
            for ch in list(a.root.children_recursive): bpy.data.objects.remove(ch, do_unlink=True)
            bpy.data.objects.remove(a.root, do_unlink=True)
        except Exception: pass
    actors.clear_registry()
    for o in [o for o in bpy.data.objects if o.name.startswith(('c2_', 'bk_', 'back_', 'cc_', 't6b_'))]: bpy.data.objects.remove(o, do_unlink=True)
    for b in [b for b in bpy.data.meshes if b.users == 0]: bpy.data.meshes.remove(b)
    keep = set(P.K._MATS.values())                      # materials cached by _flat / get_mat stay
    for m in [m for m in bpy.data.materials if m.users == 0 and m not in keep]: bpy.data.materials.remove(m)
    for im in [im for im in bpy.data.images if im.users == 0 and not im.name.startswith(('martin_', 'bottle'))]: bpy.data.images.remove(im)
    for ac in [ac for ac in bpy.data.actions if ac.users == 0]: bpy.data.actions.remove(ac)


# ======================================================= 6c / 6d / P2 re-staging (director note: card reads, nothing crosses faces)
from PIL import Image, ImageDraw, ImageFilter
import cast17, numpy as np
TEXD = os.path.join(HERE, 'tex'); os.makedirs(TEXD, exist_ok=True)
# custom story poses: Bertillon holds NO sprite card (the 3D MARTIN card is held at his raised hand); the gendarme holds the empty bottle
_b = dict(cast17.STORY17['bertillon_holding_card'][1]); _b.pop('prop_r', None); cast17.STORY17['bertillon_card_up'] = ('bertillon', _b)
_g = dict(cast17.STORY17['gendarme_standing_a'][1]); _g.update(expr='determined', arm_r=dict(hand=(0.78, 0.30), bend=-0.5, stretch=1.1, layer='front'), arm_l='behind'); cast17.STORY17['gendarme_bottle_a'] = ('gendarme_a', _g)
_g2 = dict(cast17.STORY17['gendarme_standing_b'][1]); _g2.update(expr='determined', arm_r=dict(hand=(0.78, 0.30), bend=-0.5, stretch=1.1, layer='front'), arm_l='behind'); cast17.STORY17['gendarme_bottle_b'] = ('gendarme_b', _g2)

def _tex_front():
    p = os.path.join(TEXD, 'martin_front.png')
    if not os.path.exists(p):
        im = Image.open(P.tex_hero_v2()).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT)       # un-mirror (stored mirrored for card_plane)
        d = ImageDraw.Draw(im); d.rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], outline=(26, 16, 32), width=12); im.save(p)
    return p
def _tex_back():
    p = os.path.join(TEXD, 'martin_back.png')
    if not os.path.exists(p):
        W, H = 768, 512; im = Image.new('RGB', (W, H), (232, 214, 170)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W - 1, H - 1], outline=(26, 16, 32), width=12); d.rectangle([40, 40, W - 41, H - 41], outline=(150, 120, 86), width=4)
        for y in range(120, H - 80, 46): d.line([70, y, W - 70, y], fill=(190, 168, 126), width=3)
        d.rectangle([W - 150, 0, W - 60, 46], fill=(176, 140, 96), outline=(26, 16, 32), width=6); im.save(p)       # the tab
    return p
def _tex_bottle():
    p = os.path.join(TEXD, 'bottle.png')
    if not os.path.exists(p):
        W, H = 240, 640; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); INKc = (26, 16, 32, 255)
        body = [(50, 620), (50, 300), (80, 230), (96, 200), (96, 60), (144, 60), (144, 200), (160, 230), (190, 300), (190, 620)]
        d.polygon(body, fill=(184, 222, 214, 255), outline=INKc); d.line(body + [body[0]], fill=INKc, width=10, joint='curve')
        d.rectangle([90, 26, 150, 66], fill=(176, 120, 70, 255), outline=INKc, width=8)                                        # cork
        d.polygon([(66, 590), (66, 320), (78, 300), (78, 590)], fill=(235, 250, 246, 255))                                    # highlight
        d.polygon([(52, 560), (188, 560), (188, 618), (52, 618)], fill=(150, 196, 188, 255)); d.line([(50, 620), (190, 620)], fill=INKc, width=10)
        im.save(p)
    return p
def _img_mat(name, path, backface_clear, alpha):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(path, check_existing=True); tx.interpolation = 'Cubic'; tx.extension = 'CLIP'
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs[1].default_value = 0.95; nt.links.new(tx.outputs[0], em.inputs[0])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mix = nt.nodes.new('ShaderNodeMixShader'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    fac = None
    if backface_clear:
        bf = nt.nodes.new('ShaderNodeNewGeometry'); fac = bf.outputs['Backfacing']
    if alpha:
        if fac is not None:
            mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
            nt.links.new(tx.outputs[1], inv.inputs[1]); nt.links.new(inv.outputs[0], mx.inputs[0]); nt.links.new(fac, mx.inputs[1]); fac = mx.outputs[0]
        else:
            inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; nt.links.new(tx.outputs[1], inv.inputs[1]); fac = inv.outputs[0]
    if fac is not None: nt.links.new(fac, mix.inputs[0])
    nt.links.new(em.outputs[0], mix.inputs[1]); nt.links.new(tr.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs[0]); return m
def _quad(name, c, ax, ay, hw, hh, mat, flipv=False):
    V = [tuple(c - ax * hw - ay * hh), tuple(c + ax * hw - ay * hh), tuple(c + ax * hw + ay * hh), tuple(c - ax * hw + ay * hh)]
    me = bpy.data.meshes.new(name); me.from_pydata(V, [], [(0, 1, 2, 3)]); me.update(); uv = me.uv_layers.new(name='UV')
    for k, (u, v) in zip(range(4), ((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[k].uv = (u, v)
    me.materials.append(mat); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; return ob
def _ss(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)

def card_turn_angle(g):
    """0 = the blank back faces the camera, 180 = MARTIN faces it. The turn runs g1594-1602 (edge-on at g1598, MARTIN almost face-on at the word, g1601; face-on from g1602)."""
    return 180.0 * _ss((g - 1594) / 8.0)
def head_frame(a, cam):
    import actors
    L2W = lambda xy: Vector(actors.local_to_world(a, xy, camera=cam)); o = L2W((0.0, 0.0)); return o, L2W((1.0, 0.0)) - o, L2W((0.0, 1.0)) - o
def martin_card(a, g, cam, width_D=1.45, ctr=(1.50, -0.34), back_off=0.0, t=0.25):
    """the held MARTIN card: a screen-facing plane beside Bertillon's head (head-local units, 1 = head diameter), 4 cm BEHIND his card plane so his raised hand
    stays in front. phi 0 = blank back toward the camera, 180 = MARTIN. Two coplanar quads, each hidden from behind (Backfacing)."""
    o, ex, ey = head_frame(a, cam); n = (Vector(cam.location) - o).normalized(); dsx = ex.length; dsy = ey.length
    right = Vector(cam.matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized(); up = Vector((0, 0, 1))
    D = dsx; c = o + right * (ctr[0] * D) + (-up) * (ctr[1] * D) - n * back_off; cl = Vector(cam.location); c = cl + (c - cl) * (1 - t); hw = (1 - t) * width_D * D / 2; hh = hw * 512 / 768   # t: toward the camera along the view ray (in front of the drawer box, same screen size)
    phi = math.radians(card_turn_angle(g)); axp = right * math.cos(phi) + n * math.sin(phi)
    cm = _img_mat('t6b_mback', _tex_back(), True, False); fm = _img_mat('t6b_mfront', _tex_front(), True, False)
    n1 = axp.cross(up).normalized(); _quad('t6b_card_back', c, axp, up, hw, hh, cm); _quad('t6b_card_front', c - n1 * 0.004 * (1 - t) , -axp, up, hw, hh, fm)   # 4 mm apart: no z-fight between the two coplanar quads
    return c, hw
def bottle_prop(a, cam, ctr=(0.95, 0.10), h_D=1.15, back_off=0.04):
    o, ex, ey = head_frame(a, cam); n = (Vector(cam.location) - o).normalized(); D = ex.length
    right = Vector(cam.matrix_world.to_3x3() @ Vector((1, 0, 0))).normalized(); up = Vector((0, 0, 1))
    c = o + right * (ctr[0] * D) + (-up) * (ctr[1] * D) - n * back_off; hh = h_D * D / 2; hw = hh * 240 / 640
    _quad('t6b_bottle', c, right, up, hw, hh, _img_mat('t6b_mbottle', _tex_bottle(), False, True)); return c

# per-frame offsets (world metres, eased): w is 0 while the camera is in the P1 close-up, ramps in g1546-1560, holds, and is released at the cut
def _w(g): return _ss((g - 1548) / 26.0)
STAGE = dict(bert=(0.62, 0.0), dup=(-0.90, 0.0), insp=(-0.30, 0.22))
_insp_dist = [0.0]
GEND_END = tuple(float(x) for x in os.environ.get('GEND', '0.55,-0.85').split(','))   # world offset of gend_a from his planned spot (13.95, 28.2) at the end of his walk-in
WALK0, WALK1 = 1616, 1617                                       # he walks in from the right edge (out of frame all through 6c), 0.5 m, then stands
def _gend_off(g):
    u = _ss((g - WALK0) / float(WALK1 - WALK0)); return GEND_END[0] * u, GEND_END[1] * u, u
def _gend_hand(g):
    """the hand of the gendarme pulling the empty bottle from his cape (g1640-1656): belt -> raised beside the card (head-local units, negative x = frame-left)"""
    u = _ss((g - 1640) / 16.0); return (-0.30 - 0.50 * u, 0.95 - 0.65 * u), u
INSP_T = 1584
def _stage_at(g, who):
    d = STAGE[who]
    if who == 'dup' and g >= 1616: d = (float(os.environ.get('DUP6', '-0.60')), 0.0)          # he turns round at g1616 (back view -> front): the step hides in the turn
    if who == 'bert' and g >= 1650: d = (d[0] + 0.50 * _ss((g - 1650) / 30.0), d[1])   # P2: he steps 0.5 m toward the inspector (behind the foreground desk in 6d) so the camera pass does not cut his raised arm at the frame edge
    if who == 'insp' and g < INSP_T:
        u = _ss((g - 1546) / float(INSP_T - 1546)); a = (-0.40, 3.0); return (a[0] + (d[0] - a[0]) * u, a[1] + (d[1] - a[1]) * u)   # T6a's offset at the join, then he walks to his mark
    if who == 'insp' and g >= 1655: k = 1.0 - _ss((g - 1655) / 16.0); d = (d[0] * k, d[1] * k)   # P2 centres on the inspector's own mark: ease his 6c offset away in 6d, off the viewer's eye line
    return d
def assign_for(g):
    w = _w(g); f = lambda who: ({'dx': _stage_at(g, who)[0], 'dy': _stage_at(g, who)[1]} if who == 'insp' and g < INSP_T else {'dx': _stage_at(g, who)[0] * w, 'dy': _stage_at(g, who)[1] * w})
    sw = dict(cast17.STORY17['dupont_caught'][1]); sw.update(sweat=1.0, fx=['sweat']); cast17.STORY17['dupont_caught_sweat'] = ('dupont', sw)
    gd = dict(cast17.STORY17['gendarme_standing_a'][1]); h, u = _gend_hand(g); ox, oy, wu = _gend_off(g)
    if False:                                      # foot-locked walk: phase advances with the distance walked (stride 0.72 m)
        dist = math.hypot(ox, oy); gd = cast17.cycle('gendarme_a', (dist / (2 * 0.72)) % 1.0, 'walk', facing=-1, base=gd, arms='none')
    elif g >= 1640: gd.update(expr='determined', arm_r=dict(hand=h, bend=-0.5 * u, stretch=1.0 + 0.1 * u, layer='front'), arm_l='behind')
    cast17.STORY17['gend_dyn'] = ('gendarme_a', gd)
    ip = dict(cast17.STORY17['inspector_arms_crossed'][1])
    if 1546 <= g < INSP_T:
        dist = sum(math.hypot(_stage_at(k, 'insp')[0] - _stage_at(k - 1, 'insp')[0], _stage_at(k, 'insp')[1] - _stage_at(k - 1, 'insp')[1]) for k in range(1547, g + 1))   # pure in g: resume-safe
        ip = cast17.cycle('inspector17', (dist / (2 * 0.72)) % 1.0, 'walk', facing=-1, base=ip, arms='none')
    cast17.STORY17['insp_dyn'] = ('inspector17', ip)
    gopt = {'dx': ox, 'dy': oy}
    dup = 'dupont_sweating' if g < 1616 else 'dupont_caught_sweat'
    if g >= 1671: return {'inspector': ('inspector_shocked', f('insp')), 'bertillon': ('bertillon_card_up', f('bert')), 'dupont': ('dupont_caught_sweat', f('dup')), 'gend_a': ('gend_dyn', gopt), 'gend_b': ('gendarme_standing_b', {})}
    return {'bertillon': ('bertillon_card_up', f('bert')), 'dupont': (dup, f('dup')), 'inspector': ('insp_dyn', f('insp')), 'gend_a': ('gend_dyn', gopt), 'gend_b': ('gendarme_standing_b', {})}
def stage_props(g, acts, cam):
    """call after stage_cast2: Bertillon's MARTIN card (+ bottle later)"""
    hide_hero_card(g)
    if 'bertillon' in acts and g >= 1550: martin_card(acts['bertillon'], g, cam)
    if 'gend_a' in acts and g >= 1646:
        h, u = _gend_hand(g); bottle_prop(acts['gend_a'], cam, ctr=(h[0] - 0.02, h[1] - 0.42), h_D=1.0)

def hide_hero_card(g):
    """from g1546 (right after T6a's P1) the lifted 3D hero card in the drawer box is gone: Bertillon holds the MARTIN card in his hand instead"""
    r = P.K.STATE['anim']['hero']['root']
    for o in [r] + list(r.children_recursive): o.hide_render = g >= 1550

def apply_cam():
    """P2 (g1695 hold): pull the push-in back so the inspector's head is <= 35 % of the frame height (the plan's 1.05 m was ~50 %); same look-at, camera 1.5x farther."""
    for k in P.TAKES['T6']['keys']:
        if k['g'] in (1695, 1701):
            lk = np.array(k['look']); lc = np.array(k['loc']); k['loc'] = tuple(lk + 1.5 * (lc - lk))
        if k['g'] in (1640, 1671): k['lens'] = float(os.environ.get('LENS6D', '16'))      # 6d three-shot: wider, so Bertillon + card, Dupont and the gendarme fit with margins
apply_cam()

_orig_face = P.cast_face
def _face(take, c, g):
    """gend_a walks into the 6d shot: face the camera (his planned facing is edge-on to it)"""
    if take == 'T6' and c['name'] == 'gend_a' and g >= WALK0:
        cam = bpy.context.scene.camera; p = P.cast_pos(c, g); ox, oy, _ = _gend_off(g); p = (p[0] + ox, p[1] + oy)
        return math.degrees(math.atan2(cam.location[1] - p[1], cam.location[0] - p[0]))
    return _orig_face(take, c, g)
P.cast_face = _face
