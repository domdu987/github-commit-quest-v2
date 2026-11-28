"""sc02b_lib.py -- staging shared by the SCENE 02 shots S38-S49 (the junior dying against the truck's rear wheel).
A private helper of s038.py .. s049.py (each lists it in DEPS, so a change here re-renders them); nothing else imports it.

Marks (the same as S031-S037, see s025.py `wheel()`): the junior sits in PROFILE in front of the lane-side rear tyre,
legs toward the tail, facing screen-left (the drawing that shows the bite on his anatomical left); Kong crouches at his
knees, facing him.  Cameras stand in the lanes looking west (screen-right = north), or south of the pair looking north
for the junior's face from the front.  Kong's mark here is 0.5 D nearer the junior than in S034 (he has to reach the
jaw and the shoulder) and 0.25 D further out into the lane (invisible from the lane side; it keeps his back at the edge
of S049).

Own actors (built once per process through stage_ep.CAST, never the hook's F.kong / F.crew, whose specs stay as they are):
    F.b_jun   the junior; its spec is swapped per shot (pale 2 -> pale 3 -> crew_infected), gauze soaked
    F.b_kong  Kong with the EP.1 kit (kong_ep1_02: watch on the left wrist, the junior's blood on gloves and right forearm)
"""
import os, sys, math
import epcommon as E
from epbase import *
for _p in (os.path.join(E.EP1, "cast"), os.path.join(E.EP1, "sets")):
    if _p not in sys.path: sys.path.insert(0, _p)
import draw8 as D8
import draw9 as D9                                         # patches draw8 (new faces, wounds, props) for this process
import stage as ST
import stage_ep

LIB = os.path.abspath(__file__)
BITE_FILM = 43.795                                         # film seconds (hook cue "scream")
SC02_FILM0 = 1280                                          # film frame of scene 02's first frame
DOOR_OPEN = 68.0
J_PALE = {"S038": 2, "S039": 2, "S040": 2, "S041": 2, "S042": 3, "S043": 3, "S045": 3, "S046": 3, "S048": 3, "S049": 4}


def jun_spec(level):
    """the junior by skin step: 2 and 3 = treated, gauze soaked through (S035 soaked it); 4 = turned (no gauze)."""
    if level >= 4: return "crew_infected"
    nm = "crew_b_p%d" % level
    if nm not in D8.SPECS:
        D8.SPECS[nm] = dict(D9.junior("treated", pale_level=level, gauze=1.0), name=nm)
    return nm


def _adder(key, spec, height):
    def add(F):
        a = ST.Act(F, key, spec, height, ppd=240)
        a._spec = spec
        setattr(F, key, a); F.cast.append(a)
    stage_ep.CAST.setdefault(key, add)


_adder("b_jun", jun_spec(2), ST.CREW_H)
_adder("b_kong", "kong_ep1_02", ST.KONG_H)
CAST_B = ["b_jun", "b_kong"]


def since_bite(g):
    """seconds since the bite at stage frame g (the 60 seconds run in real time)."""
    return (g - E.scene().g_base + SC02_FILM0) / 24.0 - BITE_FILM


def set_spec(act, name):
    if getattr(act, "_spec", None) != name:
        act.a.spec = D8.get_spec(name); act._spec = name; act.key = None


class Geo:
    pass


def prep(F, alarm=False):
    """per shot (setup): the scene-02 dressing of X1 (once per process), the alarm car, the hero car's door, own actors."""
    import sets, core, x1
    R = sets.dress(F.A, "X1")["x1"]
    core.retarget(F.cam)
    x1.alarm(bool(alarm))
    A = R["anchors"]
    G = Geo()
    G.A = A
    G.ws = Vector(A["wheel_seat"]); G.out = Vector(A["out_side"]); G.tail = Vector(A["out_tail"]); G.n = -G.tail
    G.J = G.ws + G.out * 0.10                              # the junior's hips (S031-S037's seat)
    G.K = G.ws + G.out * 0.80 + G.tail * 0.90              # Kong's soles
    F.b_geo = G
    for a in (F.b_jun, F.b_kong):
        a.a.pitch_override = 0.0                           # upright cards: hand contacts are solved in the card planes
    set_spec(F.b_jun, jun_spec(J_PALE.get(F.shot.ID, 2)))
    set_spec(F.b_kong, "kong_ep1_02")
    return G


def P(G, o=0.0, n=0.0, z=0.0, base=None):
    return (G.J if base is None else Vector(base)) + G.out * o + G.n * n + Vector((0, 0, z))


def always(F):
    """every frame: the wreck's door stays pried open, the hook's own principals are not in this part of the scene."""
    F.door(DOOR_OPEN)
    for a in (F.kong, F.crew, F.drv, F.drv_out): a.hide()


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
    return D9.build(spec, dict(pose, view=view, s=s))["anchors"]


# ------------------------------------------------------------------------------------------------ the junior
def jun_pose(spec, drawing="front", s=1, slump=0.4, limp=True, **kw):
    """seated against the wheel: pelvis on the deck.  drawing "side" = legs out along the screen, "front" / "q" / "back" =
    knees up toward the camera (only chest and head are framed in those shots)."""
    sp = D8.get_spec(spec)
    hy = sp["legs"] + 0.06 - 0.30
    if drawing == "side":
        p = D9.poses(spec, "sit_wheel", s=s, slump=slump, limp=limp)
        p.pop("view", None); p.pop("s", None)
    elif drawing == "q":
        p = dict(hip=(0.0, hy), legs="crouch", lean=-4, arm_n=dict(hand=(0.10, 0.88), elbow=None, hand_shape="open"),
                 arm_f=dict(hand=(0.06, 0.88), elbow=None, hand_shape="open"), head=(0, 6 + 10 * slump, 0, 0.03 * slump))
    else:
        p = dict(hip=(0.0, hy), legs="crouch", lean=0, arm_r="lap", arm_l="lap", head=(0, 6 + 8 * slump, 0, 0.03 * slump))
    p.update(kw)
    return p


def jun(F, loc, drawing, s, pose, idx=None):
    G = F.b_geo
    F.b_jun.set(loc=tuple(loc), face=facing(G.tail), view=drawing, s=s, idx=idx, **pose)
    return F.b_jun


# ------------------------------------------------------------------------------------------------ Kong
def kong_pose(lean=14, hip=0.52, **kw):
    p = dict(legs="crouch", hip=(0.0, hip), lean=lean)
    p.update(kw)
    return p


def kong(F, loc, drawing, s, pose, toward=None, idx=None):
    G = F.b_geo
    d = (G.J if toward is None else Vector(toward)) - Vector(loc); d.z = 0
    F.b_kong.set(loc=tuple(loc), face=facing(d), view=drawing, s=s, idx=idx, **pose)
    return F.b_kong


def reach(F, kloc, T, dx=0.0, dy=0.0):
    """Kong's hand target (figure frame, for an arm dict's `fig`) that lands on world point T on screen."""
    x, y = world_fig(F, F.b_kong, kloc, T)
    return (round(x + dx, 3), round(y + dy, 3))


# ------------------------------------------------------------------------------------------------ light, props
def wheel_lamp(F, heads, energy=2800.0, shadow_at=None, glow=0.25):
    """the tripod work lamp of the wheel side (the truck's own shadow falls there), slid clear of the heads; shadows."""
    G = F.b_geo
    F.lamp(tuple(G.A["lamp_base"])[:2], tuple(G.A["lamp_aim"]), energy, heads=heads)
    F.shadows(Vector(shadow_at) if shadow_at is not None else G.ws + Vector((0, 0, 1.0)))
    for a in (F.b_jun, F.b_kong):
        if a.visible: a.a.set_glow(WARM, glow)


def cutter_stand(F, loc, yaw_deg=0.0):
    """the 3D cutter standing on its battery end (jaws up) at a deck point, three green LEDs lit.  begin() of the next
    shot puts it back at the wreck's door (it is registered in F._moved)."""
    import bpy
    from mathutils import Matrix
    cu = F.cutter
    if cu is None: return
    F.cutter3d(True, jaw=1.0, bars=3, hand=False)
    for o, m0 in F._moved:
        if o is cu: M0 = m0; break
    else:
        bpy.context.view_layer.update(); M0 = cu.matrix_world.copy(); F._moved.append((cu, M0))
    c0 = M0.translation.copy()
    R = Matrix.Rotation(math.radians(yaw_deg), 4, "Z") @ Matrix.Rotation(math.radians(90.0), 4, "Y")      # the tool lies along X at the door, jaws toward -X
    cu.matrix_world = Matrix.Translation(Vector(loc)) @ R @ Matrix.Translation(-c0) @ M0
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in [cu] + list(cu.children_recursive) if o.type == "MESH" and not o.hide_render for c in o.bound_box]
    zmin = min(p.z for p in pts); cx = sum(p.x for p in pts) / len(pts); cy = sum(p.y for p in pts) / len(pts)
    cu.matrix_world = Matrix.Translation((loc[0] - cx, loc[1] - cy, loc[2] - zmin + 0.01)) @ cu.matrix_world


def near_extras_off(F, pts, r=9.0):
    """the bystanders who stood round the rescue zone have run: hide the hook's extras within r of any of the points."""
    for e in F.extras:
        if any((Vector(e.home) - Vector(p)).length < r for p in pts): e.hide()


def watch_lib():
    """the watch insert of S026 / S036 lives in s025.py (the S025-S037 range's library): the same card is used here."""
    import importlib.util
    p = E.find_shot_file("sc02", "S025")
    spec = importlib.util.spec_from_file_location("sc02b_watchlib", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m, p
