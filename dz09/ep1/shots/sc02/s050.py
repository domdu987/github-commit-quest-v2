"""S050 (class A)  'มันพุ่งใส่ก้อง'  -- M, 28 mm low, hard cut, shake 8 f.  From the lanes looking west (screen-right = north,
as S045-S046): the turned junior launches from the wheel straight at Kong (screen-left); Kong comes up out of his crouch,
goes back on one planted foot and snatches the cutter off the deck where S046 stood it, bringing it up across his body.

THIS FILE ALSO HOLDS THE SMALL LIBRARY OF S050-S061 (s051.py .. s061.py load it with `lib()` and list it in DEPS).
It lives here because the README asks for one file per shot and nothing in the shared modules may change.

Geography (the set's, as S031-S049 use it; one side of the line for the fight, S050-S054 and S058/S061):
    cameras stand in the lanes (east) looking west: screen-RIGHT = north (+s), the truck's side panel is the back wall,
    the rear corner and the tail are screen-LEFT.  The junior is drawn facing screen-left wherever he is read (the
    cast package locks the bite to his anatomical left neck, which that drawing shows).
    Corner frame used below: C(o, n, z) = corner + out_side * o + north * n  (o = metres*1/0.6 out of the side panel,
    n = along the truck toward its front, 0 = the tail line).
The roof chase S055-S057 crosses the jam EASTWARD (shoulder side -> lane 1): James goes from the green hatchback l3_a
over the SUV l2_b to the lane-1 car l1_a and drops down behind it; the junior follows onto l2_b and loses him there.
All three cameras stand south of the line looking north, so the run is side-on and LEFT TO RIGHT, as the plan asks.
(The plan's 'behind the bus' is replaced by 'behind the lane-1 car': the bus is 75 m up the road, out of reach of a
5-second chase that is in continuous time.)
"""
from epbase import *
import os, sys, math, types
for _p in (os.path.join(E.EP1, "cast"), os.path.join(E.EP1, "sets")):
    if _p not in sys.path: sys.path.insert(0, _p)
import draw8 as D8
import draw9 as D9                                          # patches draw8 (new faces, wounds, watch); before any new Act is posed
import gait9
import cutter as CT
import stage as ST
import stage_ep
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sc02_faces                                           # 11-28 fix pass: the turned junior's snarl (see S049); adds an
sc02_faces.install()                                        # expression, changes none

LIBF = os.path.abspath(__file__)
CLASS = "A"
LOC = "X1"
DEPS = [sc02_faces.FILE]
DOOR_OPEN = 68.0


# ================================================================================================ cast of S050-S061
def _height(spec):
    sp = D8.get_spec(spec)
    return 2.86 * (sp["legs"] + sp["torso"] + 1.0 + sp["hair"]["top"]) / 4.30 * 0.93


def _reg(spec):
    """a dict spec -> a registered name (Act takes a name)."""
    if isinstance(spec, dict):
        D8.SPECS.setdefault(spec["name"], spec)
        return spec["name"]
    return spec


def _adder(key, spec, height=None, ppd=240):
    def add(F):
        nm = _reg(spec)
        a = ST.Act(F, key, nm, height or _height(nm), ppd=ppd)
        setattr(F, key, a); F.cast.append(a)
    stage_ep.CAST.setdefault(key, add)


_adder("c_kong", "kong_ep1_02", ST.KONG_H)                  # watch on the left wrist, the junior's blood on gloves and right forearm
_adder("c_jun", "crew_infected", ST.CREW_H)                 # turned: grey-green, white eyes, red pin pupils, claws, same wound
_adder("c_james", "james_wet", D9.HEIGHTS["james"])         # green jacket, white helmet, no box
CAST_C = ["c_kong", "c_jun", "c_james"]
CAST = ["c_kong", "c_jun"]                                  # S050 itself

# the crowd (S059 / S060): the living extras roles 1-9 (role 0, the green rider, is James now) and three infected designs
_EXTRAS = D8.extras(10, seed=0)
for _i in range(1, 10):
    _adder("c_x%d" % _i, dict(_EXTRAS[_i], name="c_x%02d" % _i), 2.55 + 0.3 * C.hash01(_i, 3), ppd=160)
for _i in (13, 9, 2):
    _adder("c_inf%d" % _i, D9.infected(_i), ppd=200)
CAST_CROWD = ["c_x%d" % i for i in range(1, 10)]
CAST_S60 = ["c_inf13", "c_inf9", "c_x7"]


def lib():
    return sys.modules[__name__]


# ================================================================================================ marks
class Geo:
    pass


def prep(F, alarm=True):
    """per shot (setup): the scene-02 dressing of X1 (once per process), the alarm car, own actors upright."""
    import sets, core, x1
    R = sets.dress(F.A, "X1")["x1"]
    core.retarget(F.cam)
    x1.alarm(bool(alarm))
    A = R["anchors"]
    G = Geo()
    G.A = A; G.R = R; G.x1 = x1
    G.ws = Vector(A["wheel_seat"]); G.out = Vector(A["out_side"]); G.tail = Vector(A["out_tail"]); G.n = -G.tail
    G.corner = Vector(A["corner"]); G.corner.z = 0.0
    G.J = G.ws + G.out * 0.10                              # the junior's hips at the wheel (S031-S049)
    G.K = G.ws + G.out * 0.80 + G.tail * 0.90              # Kong's soles, crouched at his knees (S034-S049)
    G.CUT = G.K + G.tail * 0.45 + G.out * 0.60             # the cutter standing on its battery where S046 left it
    G.KB = G.K + G.tail * 0.75                             # Kong after S050's step back: the block of S051
    G.JB = G.J + G.tail * 0.22 + G.out * 0.60              # the junior landed on him (S050 end), his card just behind Kong's (the tool reads)
    G.HIDE = C_(G, -0.15, -0.58)                           # Kong in the nook between the water barrier and the rear corner (S053-S054)
    G.CROUCH = C_(G, 0.32, 1.30)                           # the junior after the shove, crouched at the rear wheel: the corner blocks his line to the nook
    G.CONE = (G.out * 0.60 + G.tail * 1.20)                # cone_3 moved out of the fight (S050-S061), see nudge_cone()
    F.c_geo = G
    for a in (getattr(F, "c_kong", None), getattr(F, "c_jun", None), getattr(F, "c_james", None)):
        if a is not None: a.a.pitch_override = 0.0         # upright cards: contacts are solved in the card planes
    return G


def nudge_cone(F):
    """cone_3 stood where Kong backs off (between the lens and his legs in every lane-side shot): it is moved 0.8 m
    south-east for S050-S061 (begin() puts it back for every other shot)."""
    F.nudge("cone_3", tuple(F.c_geo.CONE))


def C_(G, o=0.0, n=0.0, z=0.0):
    return G.corner + G.out * o + G.n * n + Vector((0, 0, z))


def always(F, hide_extras_near=None, r=9.0, all_extras=False):
    """every frame: the wreck's door stays pried open; the hook's own principals are not in this part of the scene;
    role 0 (the green delivery rider) is James now and is never seen as a bystander; the bystanders near the action
    have run."""
    F.door(DOOR_OPEN)
    for a in (F.kong, F.crew, F.drv, F.drv_out): a.hide()
    for e in F.extras:
        if e.i == 0 or all_extras: e.hide(); continue
        if hide_extras_near is not None and any((Vector(e.home) - Vector(p)).length < r for p in hide_extras_near): e.hide()


# ------------------------------------------------------------------------------------------------ card geometry
def card_axes(F, loc):
    c = F.cam.location
    nn = Vector((c.x - loc[0], c.y - loc[1], 0.0)).normalized()
    return Vector((-nn.y, nn.x, 0.0)), nn                  # screen-right along the card, normal toward the camera


def fig_world(F, act, loc, xy):
    """figure point (x right, y down, D) of an upright camera-facing card standing at loc -> world."""
    r, _ = card_axes(F, loc)
    sc = act.a.sc
    return Vector(loc) + r * (xy[0] * sc) + Vector((0, 0, -xy[1] * sc))


def world_fig(F, act, loc, T):
    """world point T seen from the camera -> the figure point of `act` (standing at loc) that covers it on screen."""
    r, nn = card_axes(F, loc)
    c = Vector(F.cam.location); d = Vector(T) - c
    lam = (Vector(loc) - c).dot(nn) / d.dot(nn)
    p = c + d * lam
    sc = act.a.sc
    return ((p - Vector(loc)).dot(r) / sc, -p.z / sc)


def anchors(spec, pose, view, s=1):
    p = {k: v for k, v in pose.items() if not k.startswith("_")}
    return D9.build(spec, dict(p, view=view, s=s))["anchors"]


def head_frac(F, act):
    """head height (one D) as a fraction of the frame height, at the actor's head."""
    z = F.screen(act.head())[2]
    return act.a.sc * F.cam.data.lens / 36.0 / max(z, 1e-3)


# ------------------------------------------------------------------------------------------------ the cutter
def hold(act, view, s, grip=(0.42, 0.55), tilt=170.0, jaw=1.0, scale=CT.SCALE):
    """two-handed cutter for a q / side drawing (near hand on the rear D-handle at `grip`, tool `tilt` degrees from
    straight down toward his facing side, far hand on the fore grip)."""
    return CT.hold(act.a.spec, view, s, grip=grip, tilt=tilt, jaw=jaw, scale=scale)


def jaw_fig(pose, spec, view, s, along=1.06):
    """figure point of the cutter's jaws (or any point `along` the tool, in tool units) in a pose made by hold()."""
    a = anchors(spec, pose, view, s)
    near = "hand_L" if s > 0 else "hand_R"
    at = a[near]
    pr = pose.get("prop_n") or {}
    sc = pr.get("scale", CT.SCALE)
    tilt = -float(pr.get("angle", 0.0)) * s                # hold() stores angle = -s * tilt
    L = along * sc
    return (at[0] + s * math.sin(math.radians(tilt)) * L, at[1] + math.cos(math.radians(tilt)) * L)


def hang_cutter(view, s=1):
    """the cutter hanging from the RIGHT hand (anatomical): far arm in a q / side drawing facing right, arm_r in front."""
    if view in ("front", "back"):
        return dict(arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=True))
    if s > 0:
        return dict(arm_f="hold_cutter", prop_f=dict(type="cutter", bars=3, wet=True))
    return dict(arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True))


def cutter_stand(F, loc, yaw_deg=20.0):
    """the 3D cutter standing on its battery end (jaws up) at a deck point, three green LEDs lit (S046's look);
    registered in F._moved so the next shot's begin() puts it back."""
    from mathutils import Matrix
    cu = F.cutter
    if cu is None: return
    F.cutter3d(True, jaw=1.0, bars=3, hand=False)
    for o, m0 in F._moved:
        if o is cu: M0 = m0; break
    else:
        bpy.context.view_layer.update(); M0 = cu.matrix_world.copy(); F._moved.append((cu, M0))
    c0 = M0.translation.copy()
    R = Matrix.Rotation(math.radians(yaw_deg), 4, "Z") @ Matrix.Rotation(math.radians(90.0), 4, "Y")
    cu.matrix_world = Matrix.Translation(Vector(loc)) @ R @ Matrix.Translation(-c0) @ M0
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in [cu] + list(cu.children_recursive) if o.type == "MESH" and not o.hide_render for c in o.bound_box]
    zmin = min(p.z for p in pts); cx = sum(p.x for p in pts) / len(pts); cy = sum(p.y for p in pts) / len(pts)
    cu.matrix_world = Matrix.Translation((loc[0] - cx, loc[1] - cy, loc[2] - zmin + 0.01)) @ cu.matrix_world
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in [cu] + list(cu.children_recursive) if o.type == "MESH" and not o.hide_render for c in o.bound_box]
    return max(p.z for p in pts)


# ------------------------------------------------------------------------------------------------ motion
def keys(pts):
    """piecewise smooth interpolation through (t, v1, v2, ...) keys -> function t -> tuple."""
    def fn(t):
        if t <= pts[0][0]: return tuple(pts[0][1:])
        for a, b in zip(pts, pts[1:]):
            if t <= b[0]:
                k = smooth((t - a[0]) / max(b[0] - a[0], 1e-6))
                return tuple(a[i] + (b[i] - a[i]) * k for i in range(1, len(a)))
        return tuple(pts[-1][1:])
    return fn


def rel_side(F, loc, face_deg):
    """+1 when an actor at loc facing face_deg is seen facing screen-right."""
    c = F.cam.location
    dx, dy = c.x - loc[0], c.y - loc[1]
    rel = (math.degrees(math.atan2(dx, -dy)) - face_deg + 180) % 360 - 180
    return rel


def seq_put(F, act, cyc, t, start, d, view="side", base=None, upd=None, lock=True, s=None):
    """a gait9 take (Seq / Run / Sprint / roof_run) on the straight line start + d * x: place, side, pose.
    lock = the card lies in the motion plane (planted soles stay world points; stage it near side-on)."""
    d = Vector((d[0], d[1], 0.0)).normalized()
    x, z = cyc.root(t)
    sc = act.a.sc
    loc = Vector(start) + d * (x * sc) + Vector((0, 0, z * sc))
    fd = facing(d)
    rel = rel_side(F, loc, fd)
    if s is None:
        s = -1 if rel > 0 else 1
    p = cyc.pose(t, s=s, view=view, **({"base": base} if base else {}))
    p.pop("_planted", None); p.pop("view", None); p.pop("s", None)
    if upd: p.update(upd)
    act.set(loc=tuple(loc), face=fd, view=view, s=s, **p)
    act.a.walk_lock = (90.0 if rel >= 0 else -90.0) if lock else None
    return loc, s, p


def roof_profile(F, p0, p1, sc, n=240, floor=0.0):
    """surface height under the straight path p0 -> p1 (world), as a function of the distance along it in D of an actor
    of scale sc (ray casts down; light cones, steam and rain cards are not surfaces)."""
    import numpy as np
    p0 = Vector((p0[0], p0[1], 0.0)); p1 = Vector((p1[0], p1[1], 0.0))
    L = (p1 - p0).length
    dg = bpy.context.evaluated_depsgraph_get()
    bad = ("beam", "steam", "cone", "rain", "shaft", "glow", "halo", "smoke", "spark", "fog", "x1_burst")
    xs, zs = [], []
    for k in range(n + 1):
        q = p0 + (p1 - p0) * (k / float(n))
        z = floor
        o = Vector((q.x, q.y, 9.0))
        for _ in range(6):
            hit, loc, nrm, i, ob, m = F.sc.ray_cast(dg, o, Vector((0, 0, -1)))
            if not hit: break
            if ob is not None and (any(b in ob.name.lower() for b in bad) or ob.pass_index == 2 or not ob.visible_camera):
                o = loc + Vector((0, 0, -0.01)); continue
            z = max(floor, loc.z); break
        xs.append(L * k / float(n) / sc); zs.append(z / sc)
    xs = np.array(xs); zs = np.array(zs)
    return (lambda x: float(np.interp(x, xs, zs))), L / sc


# ------------------------------------------------------------------------------------------------ light
def work_lamp(F, heads, aim=None, energy=2800.0, shadow_at=None, glow=0.25, acts=()):
    """the tripod work lamp of the wheel side (the truck's own shadow falls there), slid clear of the heads; shadows."""
    G = F.c_geo
    F.lamp(tuple(G.A["lamp_base"])[:2], tuple(aim if aim is not None else G.A["lamp_aim"]), energy, heads=heads)
    F.shadows(Vector(shadow_at) if shadow_at is not None else G.ws + Vector((0, 0, 1.0)))
    for a in acts:
        if a.visible: a.a.set_glow(WARM, glow)


def rig_post(**kw):
    d = {"exposure": 1.6, "sharp_idx": [2]}
    d.update(kw)
    return d


# ------------------------------------------------------------------------------------------------ the junior
def jun_sit(spec, s=-1, slump=0.0, **kw):
    """seated against the wheel in profile (cast pose `sit_wheel`), facing screen-left (s = -1)."""
    p = D9.poses(spec, "sit_wheel", s=s, slump=slump)
    p.pop("view", None); p.pop("s", None); p.pop("z", None)
    p.update(kw)
    return p


def claws(near, far, lean_w=0.0):
    return dict(arm_n=dict(hand=near, elbow=None, hand_shape="claw_glove"), arm_f=dict(hand=far, elbow=None, hand_shape="claw_glove"))


# ------------------------------------------------------------------------------------------------ the block (S051, S052)
def block(F, t, kloc, push=0.0, tilt=166.0, grip=(0.40, 0.50), kexpr="angry", jexpr="bite", klean=-6.0, jlean=26.0, along=0.80,
          jhead=(0, -10, 0.08, 0.0), front=0.40):
    """Kong (q drawing, facing north) holds the cutter across his chest; the junior (side drawing, facing south) has his
    teeth on the steel arm just under the jaws and both claws on Kong's forearms.  The junior's card stands `front` BU
    nearer the lens than the bite point, so his teeth and claws are drawn over the tool."""
    G = F.c_geo; kg, jn = F.c_kong, F.c_jun
    s = 1
    h = hold(kg, "q", s, grip=grip, tilt=tilt, jaw=1.0)
    kp = dict(expr=kexpr, blink=0, legs="wide", lean=klean + 3.0 * push, head=(0, -2, 0.0, 0.0), **h)
    kg.set(loc=tuple(kloc), face=facing(G.n), view="q", s=s, **kp); kg.a.walk_lock = None
    bx, by = jaw_fig(kp, kg.a.spec, "q", s, along=along)
    T = fig_world(F, kg, kloc, (bx, by))
    c = Vector(F.cam.location)
    Tf = c + (T - c) * (1.0 - front / max((T - c).length, 1e-3))
    jp = dict(expr=jexpr, blink=0, legs="lunge", lean=jlean, head=jhead, hip=(0.0, 0.10))
    sc = jn.a.sc
    a = anchors(jn.a.spec, jp, "side", -1)
    mx, my = a["mouth"]
    drop = (-my * sc - Tf.z) / sc
    if drop > 0:
        jp["hip"] = (0.0, 0.10 + drop); a = anchors(jn.a.spec, jp, "side", -1); mx, my = a["mouth"]
    r, _ = card_axes(F, Tf)
    jl = Tf - r * (mx * sc); jl.z = 0.0
    ka = anchors(kg.a.spec, kp, "q", s)
    for key, wr in (("arm_n", "wrist_L"), ("arm_f", "wrist_R")):
        Wp = fig_world(F, kg, kloc, ka[wr])
        fx, fy = world_fig(F, jn, jl, Wp)
        jp[key] = dict(fig=(round(fx, 3), round(fy, 3)), hand_shape="claw_glove")
    jn.set(loc=tuple(jl), face=facing(G.tail), view="side", s=-1, **jp); jn.a.walk_lock = None
    return kp, jl, jp, T


# ------------------------------------------------------------------------------------------------ the roof chase (S055-S057)
def take_cached(F, key, make):
    """a take built once per shot and process (pure function of the set: ray casts on the static jam)."""
    k = (F.shot.ID, F._begin_n, key)
    c = F.__dict__.setdefault("_c_takes", {})
    if k not in c:
        c[k] = make()
    return c[k]


def roof_take(F, act, a, b, stride=1.25, speed=6.0, x0=0.0):
    """gait9.roof_run along the straight line a -> b (world, z ignored) on the ray-cast surface heights."""
    prof, Ld = roof_profile(F, a, b, act.a.sc)
    return gait9.roof_run(act.a.spec, prof, x0, Ld, stride=stride, speed=speed)


def no_lamp(F):
    F.lamp((0, 0), (0, 0, 0), hide=True)


# ------------------------------------------------------------------------------------------------ the crowd (S059)
def sils(F, n=8):
    """far back-lit repeats: one dark card each with a thin cool rim (ep1/cast stage9.Sil), eight pre-rastered phases of a
    survivor run.  Built once per process and parked 300 BU under the deck; a shot that shows them registers them in
    F._moved, so the next shot's begin() parks them again."""
    c = F.__dict__.get("_c_sils")
    if c is None:
        import raster8
        cache0 = raster8.CACHE
        import stage9 as S9                                 # (stage9 imports rast9, which moves raster8's cache: put it back)
        raster8.CACHE = cache0
        c = []
        for i in range(n):
            role = 1 + (i * 4) % 9
            spec = dict(_EXTRAS[role], name="c_sil%02d" % i)
            D8.SPECS.setdefault(spec["name"], spec)
            G = gait9.Run(spec, ("praew", "tos", "james", "kong")[i % 4], phase=(0.17 * i) % 1.0)
            poses = []
            for k in range(8):
                p = G.pose(G.T * k / 8.0, s=1, view="side"); p.pop("_planted", None); p["expr"] = "scared"
                poses.append(p)
            sl = S9.Sil("c_sil%02d" % i, spec, poses=poses, ppd=60, s=1)
            sl.T = G.T; sl.run = G
            sl.ob.location = (0.0, 0.0, -300.0)
            c.append(sl)
        F._c_sils = c
    from mathutils import Matrix
    for sl in c:
        if not any(o is sl.ob for o, _ in F._moved):
            F._moved.append((sl.ob, Matrix.Translation((0.0, 0.0, -300.0))))
    return c


def deck_clear(F, x, y, r=0.45):
    """no car body / barrier within r of (x, y) at knee height (ray casts down; light cones and rain are not solid)."""
    dg = bpy.context.evaluated_depsgraph_get()
    bad = ("beam", "steam", "cone", "rain", "shaft", "glow", "halo", "smoke", "spark", "fog", "x1_burst", "_sil")
    for dx, dy in ((0, 0), (r, 0), (-r, 0), (0, r), (0, -r)):
        o = Vector((x + dx, y + dy, 7.0))
        for _ in range(6):
            hit, loc, nrm, i, ob, m = F.sc.ray_cast(dg, o, Vector((0, 0, -1)))
            if not hit: break
            if ob is not None and (any(b in ob.name.lower() for b in bad) or ob.pass_index == 2 or not ob.visible_camera):
                o = loc + Vector((0, 0, -0.01)); continue
            if loc.z > 0.35: return False
            break
    return True


# ================================================================================================ the shot S050
def setup(F):
    G = prep(F, alarm=True)
    nudge_cone(F)
    F._c_cut_top = cutter_stand(F, G.CUT, 20.0)           # where the tool stands (S046's mark); shown / hidden per frame
    F.cutter3d(False)


def _kong_take(F):
    """Kong out of the crouch: the far foot stays planted, the near foot steps back once; the root goes 0.80 D back."""
    sp = F.c_kong.a.spec
    root = gait9._keys([(0.0, 0.0, 0.0), (0.22, 0.0, 0.0), (0.62, -1.08, 0.0), (1.6, -1.15, 0.0)])
    feet = {"f": [(0.0, 1.6, -0.40, 0.0)],
            "n": [(0.0, 0.26, 0.28, 0.0), (0.56, 1.6, -1.75, 0.0)]}
    crouch = gait9._keys([(0.0, 0.62), (0.20, 0.55), (0.55, 0.22), (0.9, 0.14), (1.6, 0.16)])
    return gait9.Seq(sp, 1.6, lambda t: root(t), feet, None, lift=0.22, crouch=lambda t: crouch(t)[0])


def frame(F, g, t, u):
    G = F.c_geo
    always(F, all_extras=True)
    t0 = T0(F)
    tt = C.on_twos(t)
    tau = tt - t0
    kg, jn = F.c_kong, F.c_jun
    # ---- camera: low in the lanes, side-on, a hard 8-frame shake from the launch
    mid = (G.J + G.KB) * 0.5
    look = mid + G.tail * 0.15 + Z(1.25)
    hard = max(0.0, 1 - (t - t0 - 0.20) / (8 / 24.0)) if t - t0 >= 0.20 else 0.0
    sh = tuple(a + b for a, b in zip(hand_cam(t, 0.35, 1.8), hand_cam(t, 2.4 * hard, 9.0, 2.0)))
    F.camera(look + G.out * 3.75 + G.n * 0.85 + Z(-0.55), look, F.pick(28, 24), focus=mid + Z(1.4), k=6.0, kmax=18, shake=sh)
    # ---- Kong
    cyc = _kong_take(F)
    if tau < 0.50:
        k = smooth(ramp(tau, 0.12, 0.46))                    # the near hand goes down for the standing tool
        upd = dict(expr="alarmed", blink=0, head=(0, -4, 0.0, 0.0), lean=lerp(16.0, -10.0, smooth(ramp(tau, 0.15, 0.50))),
                   arm_f=dict(hand=(0.40 - 0.10 * k, 0.40 + 0.35 * k), elbow=None, hand_shape="glove"),
                   arm_n=dict(hand=(0.50, 0.50), elbow=None, hand_shape="glove"))
        loc, s, _ = seq_put(F, kg, cyc, tau, G.K, G.n, view="q", upd=upd)
        tx, ty = world_fig(F, kg, loc, Vector((G.CUT.x, G.CUT.y, F._c_cut_top - 0.20)))
        a0 = anchors(kg.a.spec, kg.pose_d, "q", s)
        rest = a0["hand_L" if s > 0 else "hand_R"]
        upd["arm_n"] = dict(fig=(round(lerp(rest[0], tx, k), 3), round(lerp(rest[1], ty, k), 3)), hand_shape="grip" if k > 0.9 else "glove")
        seq_put(F, kg, cyc, tau, G.K, G.n, view="q", upd=upd)
        F.cutter3d(True, jaw=1.0, bars=3, hand=False)
    else:
        up = smooth(ramp(tau, 0.50, 1.10))                   # the tool comes up across his body
        h = hold(kg, "q", 1, grip=(lerp(0.10, 0.44, up), lerp(0.80, 0.62, up)), tilt=lerp(20.0, 128.0, up))
        upd = dict(expr="angry" if up > 0.6 else "alarmed", blink=0, lean=lerp(-10.0, -4.0, up), head=(0, -2, 0.0, 0.0), **h)
        seq_put(F, kg, cyc, tau, G.K, G.n, view="q", upd=upd)
        F.cutter3d(False)
    kg.breath = 0.008 * math.sin(t * 3.4)
    # ---- the junior: seated -> gathers -> launches (airborne: no foot on the deck) -> lands in a lunge on the cutter
    sp = jn.a.spec
    d = G.tail                                               # he faces and goes south, toward Kong
    if tau < 0.17:
        p = jun_sit(sp, s=-1, slump=0.0, expr="z_snarl", blink=0, head=(0, -10, 0.02, 0.0), **claws((0.55, 0.10), (0.45, 0.30)))
        jn.set(loc=tuple(G.J), face=facing(d), view="side", s=-1, **p)
        jn.a.walk_lock = None
    else:
        fly = keys([(0.17, 0.00, 0.00, 0.0), (0.34, 0.05, 0.10, 0.06), (0.52, 0.16, 0.42, 0.22), (0.66, 0.21, 0.58, 0.0), (1.6, 0.22, 0.60, 0.0)])
        x, o, z = fly(tau)
        leg = "crouch" if tau < 0.34 else "lunge"
        hip = (0.0, 0.55) if tau < 0.34 else (0.0, 0.10 if tau < 0.66 else 0.20)
        reach = smooth(ramp(tau, 0.30, 0.70))
        p = dict(expr="z_snarl" if tau < 0.55 else "z_snarl_o", blink=0, legs=leg,   # 11-28: was lunging / bite (a grin)
                 hip=hip, lean=lerp(22.0, 24.0, reach),
                 head=(0, -14, 0.10, 0.0), **claws((0.55 + 0.40 * reach, 0.20 - 0.30 * reach), (0.45 + 0.35 * reach, 0.36 - 0.25 * reach)))
        loc = G.J + d * x + G.out * o + Z(z)
        jn.set(loc=tuple(loc), face=facing(d), view="side", s=-1, **p)
        jn.a.walk_lock = None
    return rig_post()


def late(F, g, t, u):
    if once(F):
        G = F.c_geo
        work_lamp(F, [F.c_kong.head(), F.c_jun.head()], acts=(F.c_kong, F.c_jun))
