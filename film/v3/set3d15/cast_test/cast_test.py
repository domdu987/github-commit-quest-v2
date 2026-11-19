"""Placement test: REAL cast15 puppet cards (emission-only) in the set3d15 scene. Writes only inside cast_test/.
usage: python3 cast_test.py [final|preview] [still ...]   stills: s10 s20 s27 s28 s36   (no args = all, then sheets via `python3 cast_test.py sheet`)
World: 1 unit = 1 D = 0.54 m (set15.DM). Cameras/marks are D; set hooks that name metres say so."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path[:0] = [os.path.join(V3, 'cast15'), os.path.join(V3, 'stage'), os.path.join(V3, 'set3d15')]
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cast15, sprites            # cast15 BEFORE sprites
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import set15 as F
import set15_shots as SH
DM = F.DM; U = F.U
SPR = os.path.join(HERE, 'sprites'); os.makedirs(SPR, exist_ok=True)
W, H = 720, 1280

def card_mat(name, png, k=1.0):
    """emission-only card: PNG colour + alpha, never lit (stage convention), no shadows cast"""
    img = bpy.data.images.load(png); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = N('ShaderNodeTexImage'); ti.image = img; ti.interpolation = 'Linear'; ti.extension = 'CLIP'
    em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(ti.outputs['Color'], em.inputs['Color']); L(ti.outputs['Alpha'], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def put(tag, cast, pose, mark=(0, 0, 0), cam_loc=(0, 0, 0), ppd=128, scale=1.0, mirror=False, yaw_off=0.0, canvas=None, shadow=(1.4, 0.45),
        anchor=None, yaw_fixed=None, dz=0.0, shadow_at=None, shadow_a=0.8):
    """real cast15 sprite -> card (metres-free: scene units are D). returns dict(world=fn(anchor_xy_local)->Vector, anchors, res, mk, yaw, scale).
    mark   : world (x, y, z) in D where the FEET point of the sprite goes (standing poses).
    anchor : (name, (x, y, z)) instead of mark: the sprite's anchor ('head', 'bar', 'apex', 'hip', 'feet' ...) lands exactly on that world point (lying / flop / buried poses).
    scale  : card scale (1 = real cast size, Dick 3.76 D); ppd = sprite pixels per D (sprite is rendered at ppd, then the card is scaled).
    shadow : (L, W) in D of the contact ellipse at `mark` (None = none); shadow_at=(x, y, z, L, W) puts it elsewhere (flop: on the pit under the arch). The card yaws to face cam_loc (yaw about Z only).
    canvas : default CANVAS15[cast] (standing) -- pass cast15.CANVAS15_WIDE for lying / flop / straddle / buried / airborne poses."""
    pose = dict(pose); pose['mirror'] = bool(mirror)
    cv = canvas or cast15.CANVAS15[cast]
    out = os.path.join(SPR, tag + '.png')
    r = sprites.render_sprites([dict(cast=cast, pose=pose, px_per_D=ppd, out=out, canvas=cv)])[0]
    assert not r['clipped'], 'sprite clipped by canvas: ' + tag
    x0, y0, x1, y1 = r['canvas']; fx, fy = r['feet']; k = scale
    X0, X1 = x0 * k, x1 * k; Z0, Z1 = -y1 * k, -y0 * k            # card rect (D) relative to the feet point, z up
    me = bpy.data.meshes.new(tag); me.from_pydata([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c
    me.materials.append(card_mat(tag + '_mat', out))
    cam = Vector(cam_loc)
    def yaw_of(p):
        if yaw_fixed is not None: return yaw_fixed
        d = cam - p; return math.atan2(d.x, -d.y) + math.radians(yaw_off)
    mk = Vector(mark) + Vector((0, 0, dz))
    if anchor is not None:
        an, wp = anchor; a = r['anchors'][an]; wp = Vector(wp)
        for _ in range(6):                                          # yaw depends on where the card ends up: iterate
            yw = yaw_of(mk); axx = Vector((math.cos(yw), math.sin(yw), 0))
            mk = wp - axx * ((a[0] - fx) * k) - Vector((0, 0, (fy - a[1]) * k))
    yaw = yaw_of(mk)
    ob = bpy.data.objects.new('actor_' + tag, me); bpy.context.scene.collection.objects.link(ob); ob.location = mk; ob.rotation_euler = (0, 0, yaw)
    ob.visible_shadow = False; F.T.no_bounce(ob) if hasattr(F.T, 'no_bounce') else None
    ax = Vector((math.cos(yaw), math.sin(yaw), 0))
    def w(a): return mk + ax * ((a[0] - fx) * k) + Vector((0, 0, (fy - a[1]) * k))
    if shadow_at is not None: _contact(tag, Vector(shadow_at[:3]), yaw, shadow_at[3], shadow_at[4], shadow_a)
    elif shadow: _contact(tag, Vector((mk.x, mk.y, mark[2] + dz if anchor is None else mk.z)), yaw, shadow[0] * k, shadow[1] * k, shadow_a)
    return dict(world=w, anchors=r['anchors'], res=r, mk=mk, yaw=yaw, scale=k)

def _contact(tag, c, yaw, L, Wd, alpha=0.8):
    """soft dark-violet ellipse flat on the ground (z + 0.03 D), L along the card's x axis (across the view), Wd deep"""
    N = 128; im = np.zeros((N, N, 4), np.float32); yy, xx = np.mgrid[0:N, 0:N]; r = np.hypot((xx - N / 2) / (N / 2), (yy - N / 2) / (N / 2))
    im[..., 3] = np.clip(1 - r, 0, 1) ** 0.8; p = os.path.join(SPR, 'contact_%s.png' % tag); Image.fromarray((im * 255).astype(np.uint8)).save(p)
    me = bpy.data.meshes.new('c_' + tag); me.from_pydata([(-L / 2, -Wd / 2, 0), (L / 2, -Wd / 2, 0), (L / 2, Wd / 2, 0), (-L / 2, Wd / 2, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, cc in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = cc
    img = bpy.data.images.load(p); img.alpha_mode = 'STRAIGHT'
    m = bpy.data.materials.new('cm_' + tag); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); Nn = nt.nodes.new; Lk = nt.links.new
    out = Nn('ShaderNodeOutputMaterial'); ti = Nn('ShaderNodeTexImage'); ti.image = img; ti.extension = 'CLIP'; em = Nn('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.03, 0.02, 0.07, 1)
    tr = Nn('ShaderNodeBsdfTransparent'); mx = Nn('ShaderNodeMixShader'); mu = Nn('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = alpha
    Lk(ti.outputs['Alpha'], mu.inputs[0]); Lk(mu.outputs[0], mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m); ob = bpy.data.objects.new('actor_c_' + tag, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (c.x, c.y, c.z + 0.03); ob.rotation_euler = (0, 0, yaw); ob.visible_shadow = False

def screen(p):
    sc = bpy.context.scene; v = world_to_camera_view(sc, sc.camera, Vector(p)); return [round(v.x * W), round((1 - v.y) * H)]

def hide_placeholders():
    for o in list(bpy.data.objects):
        if o.name.startswith('actor_'): bpy.data.objects.remove(o, do_unlink=True)

def look_cam(loc_m, look_m, lens=22.0):
    return F.make_camera(F.cam_from(tuple(c * U for c in loc_m), tuple(c * U for c in look_m), lens=lens))

def info_of(rep, names=('head', 'feet', 'bar', 'apex', 'hip', 'foot_l', 'foot_r', 'knee_l', 'knee_r', 'head_top')):
    out = {}
    for k, v in rep.items():
        a = v['anchors']; w = v['world']
        out[k] = {n: screen(w(a[n])) for n in names if n in a}
        out[k]['mk_D'] = [round(c, 3) for c in v['mk']]; out[k]['scale'] = v['scale']
    return out

# ---------------------------------------------------------------------------------------------- stills
CFG = dict(
 s10=dict(coach_dz=0.0, boys=((1.6, -1.5, 'boy1', 'laugh'), (1.2, 1.5, 'boy2', 'point_laugh'))),
 s20=dict(cam=((-2.4, 7.4, 2.15), (-1.8, 11.4, 2.05), 22.0), dick_pos=(-3.0, 20.2), yaw_off=0.0),
 s27=dict(cam=((-0.2, 9.4, 2.0), (-0.2, 11.6, 2.15), 22.0), scale=1.0, off=(0.12, 0.0), front=0.3),
 s28=dict(cam=None, off=(0.0, 0.0, 0.0)),
 s36=dict(spray_dt=9, dz=-0.6, spray=1.7),
)
POSES = cast15.STORY15

def s10(q):
    A = F.build('A', 'GOLDEN'); sc = bpy.context.scene; F.setup_render(sc, q); hide_placeholders()
    cam = SH.setup_shot(10); f0 = int(round(F.SHOTS[10]['t0'] * 30)); sc.frame_set(f0); cl = tuple(cam.location)
    M = Vector(A['marks']['coach_bleacher']); rep = {}; C = CFG['s10']
    dirv = (Vector(F.SHOTS[10]['a']['look']) - Vector(F.SHOTS[10]['a']['loc'])); dirv.z = 0; dirv.normalize(); rt = Vector((dirv.y, -dirv.x, 0))
    for i, (d, lat, cast, pn) in enumerate(C['boys']):          # boys behind the coach (further from the camera), drawn first
        p = M + dirv * d + rt * lat; p.z = M.z
        pose = cast15.pose_for(pn, cast); rep['boy%d' % i] = put('s10_b%d' % i, cast, pose, tuple(p), cl, shadow=(1.3, 0.4))
    pose = dict(cast15.pose_for('coach_laugh', 'coach'), bob=cast15.laugh_bob(f0))
    rep['coach'] = put('s10_coach', 'coach', pose, tuple(M), cl, shadow=(1.9, 0.6))
    bpy.context.view_layer.update(); return rep, 'A GOLDEN shot 10: coach laughing at the bleacher front, two boys behind', cam

def s20(q):
    A = F.build('B', 'EVE'); sc = bpy.context.scene; F.setup_render(sc, q); hide_placeholders(); C = CFG['s20']
    cam = look_cam(*C['cam']); cl = tuple(cam.location); sc.frame_set(1)
    M = Vector((C['dick_pos'][0], C['dick_pos'][1], 0.0))      # in the bar's plane (y 21.48 D), 0.5 D in front of it: bar and head have the same parallax
    pose = cast15.pose_for('stand', 'dick_olympic')
    rep = {'dick': put('s20_dick', 'dick_olympic', pose, tuple(M), cl, yaw_off=C['yaw_off'], shadow=(1.5, 0.5))}
    bpy.context.view_layer.update()
    top = rep['dick']['world'](rep['dick']['anchors']['head_top']) if 'head_top' in rep['dick']['anchors'] else M + Vector((0, 0, 3.76))
    return rep, 'B EVE shot 20: Dick by the standard, bar 0.55 D above the head', cam

def _flop(q, name, light, cast, pose_name, C, label, tag, canv=cast15.CANVAS15_WIDE, mirror=False):
    A = F.build('B', light); sc = bpy.context.scene; F.setup_render(sc, q); hide_placeholders()
    cam = look_cam(*C['cam']); cl = tuple(cam.location); sc.frame_set(1)
    bar = Vector((0.0, F.STATE['J']['y'] * U, F.bar_height_m() * U))
    bar += Vector((C['off'][0], 0, C['off'][1]))
    if C.get('front'):                       # card slightly in front of the bar so legs that cross the bar line hide it (they hang in front of it)
        t = Vector(cl) - bar; t.z = 0; bar += t.normalized() * C['front']
    pose = cast15.pose_for(pose_name, cast)
    return A, cam, cl, bar, pose

def s27(q):
    C = CFG['s27']; A, cam, cl, bar, pose = _flop(q, 's27', 'TENSE', 'dick_olympic', 'flop', C, '', 's27')
    k = C['scale']; foam = F.STATE['J']['ground'] * U
    # shadow on the foam top straight under the arch (card frame: below apex/hip)
    rep = {'dick': put('s27_dick', 'dick_olympic', pose, cam_loc=cl, ppd=192, scale=k, canvas=cast15.CANVAS15_WIDE, anchor=('bar', tuple(bar)), shadow=None)}
    r = rep['dick']; w = r['world']; a = r['anchors']; hp = w(a['hip'])
    _contact('s27', Vector((hp.x, hp.y, foam)), r['yaw'], 2.6 * k, 0.9 * k, 0.55)
    bpy.context.view_layer.update(); return rep, 'B TENSE shot 27 KEY: dick_olympic in flop on the crossbar', cam

def s28(q):
    C = CFG['s28']; A = F.build('B', 'EVE'); sc = bpy.context.scene; F.setup_render(sc, q); hide_placeholders()
    cam = SH.setup_shot(28); f0 = int(round(F.SHOTS[28]['t0'] * 30)); sc.frame_set(f0); cl = tuple(cam.location)
    bar = Vector((0.0, F.STATE['J']['y'] * U, F.bar_height_m() * U)); k = 1.0
    pose = cast15.pose_for('straddle_a', 'rival1'); foam = F.STATE['J']['ground'] * U
    # straddle: body flat; place its HEAD anchor so the whole body is above the bar (feet/belly clear by >= 0.8 D)
    rep = {'rival': put('s28_rival', 'rival1', pose, cam_loc=cl, ppd=160, scale=k, canvas=cast15.CANVAS15_WIDE, anchor=('head', (bar.x + C['off'][0], bar.y, bar.z + 1.9 + C['off'][2])), shadow=None)}
    r = rep['rival']; hp = r['world'](r['anchors']['head'])
    _contact('s28', Vector((hp.x, hp.y, foam)), r['yaw'], 3.2, 1.0, 0.45)
    bpy.context.view_layer.update(); return rep, 'B EVE shot 28: rival1 straddle_a high above the bar', cam

def s36(q):
    A = F.build('A', 'GOLDEN'); sc = bpy.context.scene; F.setup_render(sc, q); hide_placeholders(); C = CFG['s36']
    cam = SH.setup_shot(36); f0 = int(round(F.SHOTS[36]['t0'] * 30)); cl = tuple(cam.location)
    M = Vector(A['marks']['coach_end']); rep = {}
    pose = cast15.pose_for('coach_buried', 'coach')
    rep['coach'] = put('s36_coach', 'coach', pose, tuple(M), cl, canvas=cast15.CANVAS15_WIDE, dz=C['dz'], shadow=None)
    F.sawdust_spray(f0 - C['spray_dt'], (M.x, M.y, M.z + 0.2), strength=C['spray'], seed=3)
    sc.frame_set(f0); bpy.context.view_layer.update(); return rep, 'A GOLDEN shot 36: coach buried in the sawdust, spray in the air', cam

STILLS = ['s10', 's20', 's27', 's28', 's36']
LABELS = dict(s10='shot 10  A GOLDEN', s20='shot 20  B EVE', s27='shot 27  B TENSE', s28='shot 28  B EVE', s36='shot 36  A GOLDEN')

def sheets():
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30); fp = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
    LB = 56; Sh = Image.new('RGB', (W * 5, H + LB), (16, 16, 20)); d = ImageDraw.Draw(Sh)
    PW, PH, PL = 360, 640, 30; Ph = Image.new('RGB', (PW * 5, PH + PL), (16, 16, 20)); dp = ImageDraw.Draw(Ph)
    for i, n in enumerate(STILLS):
        im = Image.open(os.path.join(HERE, n + '.png')).convert('RGB'); Sh.paste(im, (i * W, 0)); d.text((i * W + 12, H + 11), LABELS[n], fill=(235, 235, 235), font=fnt)
        d.line([(i * W, 880), (i * W + W, 880)], fill=(0, 230, 255), width=2)
        Ph.paste(im.resize((PW, PH), Image.LANCZOS), (i * PW, 0)); dp.text((i * PW + 8, PH + 5), LABELS[n], fill=(235, 235, 235), font=fp)
    Sh.save(os.path.join(HERE, 'test.jpg'), quality=90); Ph.save(os.path.join(HERE, 'test_phone.jpg'), quality=90)

if __name__ == '__main__':
    q = 'final'; names = []
    for a in sys.argv[1:]:
        if a in ('final', 'preview'): q = a
        else: names.append(a)
    cfg = os.path.join(HERE, 'placement.json')
    if os.path.exists(cfg):
        for k, v in json.load(open(cfg)).items(): CFG[k].update(v)
    if names == ['sheet']: sheets(); sys.exit()
    log = {}
    for n in names or STILLS:
        rep, label, cam = globals()[n](q)
        info = info_of(rep); outp = os.path.join(HERE, '%s%s.png' % (n, '' if q == 'final' else '_prev'))
        wall, cpu = F.T.render(outp); info['_cam'] = dict(loc_m=[round(c * DM, 3) for c in cam.location], lens=cam.data.lens); info['_time'] = [round(wall, 1), round(cpu, 1)]
        print(n, q, label, json.dumps(info), flush=True)
    if not names or names == STILLS: sheets()
