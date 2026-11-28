"""S025 (class A)  'เหลืออีก'  -- CU, handheld, hard shake 6 f then settling.  The driver hangs on the junior's back, teeth in
the orange collar where neck meets shoulder; the junior screams toward Kong (round mouth); Kong's two black gloves and
the orange cutter body drive in from the SOUTH side of the frame.

THIS FILE ALSO HOLDS THE SMALL LIBRARY OF S025-S037 (the other shot files of the range load it with `lib()`): the
EP.1 actors on the hook stage, the X1 dressing switch, the fight / wheel marks, the watch insert.  It is here because
stage_ep.CAST has no EP.1 actors yet and run_ep.py does not dress X1 (see the report: both belong in shared modules).

Screen axis of S025-S037 (the set's real geography, camera always on the lane side of the action looking west):
    screen RIGHT = north (+s): the driver is thrown that way, the alarm taxi `l1_b` stands there;
    screen LEFT  = south: the rescue truck, where Kong takes the junior.
The junior is drawn facing screen-left wherever he is read, because the cast package locks the bite to the side that
drawing shows.  This mirrors the plan's 'driver flies screen left / they walk screen right'.

Pass of 2026-11-28: upright cards (pitch 0) for the seated / crouched pair, hands solved onto the gauze pad on screen
(card_axes / fig_world / world_fig / reach, one correction step against the drawing's hand anchor), the pad located on
the flat drawing (just under the chin), the standing cutter on S040's mark, kit() resets pitch / walk lock of this
range's actors.  Probes and the stills runner: ep1/chk/a25 (still.py, occ.py, dbg35.py, dbg37.py, stage_all.py).
"""
from epbase import *
import os, sys, types
from stage import Act, CREW_H, KONG_H

for _p in (os.path.join(E.EP1, "cast"), os.path.join(E.EP1, "sets")):
    if _p not in sys.path: sys.path.append(_p)

CLASS = "A"
LOC = "X1"
PPD = {"e1_jun_bitten": 420, "driver_out": 420, "e1_kong_clean": 360}
EP_FPS = 24.0
BITE_FILM = 43.795                      # the hook's cue "scream": the watch counts from here
SC02_FILM0 = 1280 / 24.0                # film time of scene 02's first frame


# ================================================================================================ library (S025-S037)
def kit(F):
    """EP.1 additions on the hook stage, built once per Blender process: the X1 dressing of ep1/sets and a place for the
    EP.1 actors.  Every shot of the range calls it in setup()."""
    K = getattr(F, "_e1kit", None)
    if K is None:
        import draw9 as D9                                  # patches draw8 (new faces, wounds, watch); before any new Act is posed
        import gait9, sets, core, x1
        R = sets.dress(F.A, "X1")["x1"]
        core.retarget(F.cam)
        K = F._e1kit = types.SimpleNamespace(D9=D9, gait9=gait9, x1=x1, R=R, A={k: (Vector(v) if isinstance(v, tuple) else v) for k, v in R["anchors"].items()},
                                             acts={}, cut0=None, car0={})
    K.x1.alarm(False)                                       # a shot that wants the alarm switches it on in frame()
    for nm, m0 in K.car0.items():                           # a car rocked by S028 goes back
        bpy.data.objects[nm].matrix_world = m0
    for a in K.acts.values():                               # begin() does not reset these: standing shots get the film's pitch
        a.a.pitch_override = None
        a.a.walk_lock = None
    return K


# ---------------------------------------------------------------------------------------------- card geometry
# (upright camera-facing cards, pitch_override 0: the figure frame is x screen-right, y down from the soles, in D)
def card_axes(F, loc):
    c = F.cam.location
    nn = Vector((c.x - loc[0], c.y - loc[1], 0.0)).normalized()
    return Vector((-nn.y, nn.x, 0.0)), nn


def fig_world(F, act, loc, xy):
    r, _ = card_axes(F, loc)
    sc = act.a.sc
    return Vector(loc) + r * (xy[0] * sc) + Vector((0, 0, -xy[1] * sc))


def world_fig(F, act, loc, T):
    """world point T -> the point of act's card (standing at loc) that covers it on screen, in act's figure frame."""
    r, nn = card_axes(F, loc)
    c = Vector(F.cam.location); d = Vector(T) - c
    lam = (Vector(loc) - c).dot(nn) / d.dot(nn)
    p = c + d * lam
    sc = act.a.sc
    return ((p - Vector(loc)).dot(r) / sc, -(p.z - loc[2]) / sc)


_ANCH = {}


def anchors(act, pose, view, s):
    """drawing anchors (figure frame) of act in this pose; cached per pose."""
    import json as _j
    key = _j.dumps([act.name, view, s, pose], sort_keys=True, default=str)
    if key not in _ANCH:
        _ANCH[key] = F_D9().build(act.a.spec, dict(pose, view=view, s=s))["anchors"]
    return _ANCH[key]


def F_D9():
    import draw9
    return draw9


def reach(F, act, loc, T, dx=0.0, dy=0.0):
    """hand target (an arm dict's `fig`) of act standing at loc that lands on world point T on screen."""
    x, y = world_fig(F, act, loc, T)
    return (round(x + dx, 3), round(y + dy, 3))


JUNIOR = {  # key -> (state, pale level, gauze soak, blood)
    "bitten": ("bitten", 0, None, 1.0),
    "gauze0": ("treated", 0, 0.10, 1.0), "gauze1": ("treated", 0, 0.30, 1.0), "gauze2": ("treated", 0, 0.50, 1.0),
    "gauze3": ("treated", 0, 0.72, 1.0), "gauze4": ("treated", 0, 1.0, 1.0),
    "grey1": ("treated", 1, 1.0, 1.0),
}


def junior(F, key="bitten"):
    """the junior after the bite as an actor of this stage (one Act per look; all but the one a shot poses stay hidden)."""
    K = kit(F) if not hasattr(F, "_e1kit") else F._e1kit
    nm = "e1_jun_" + key
    if nm not in K.acts:
        st, lvl, gz, bl = JUNIOR[key]
        sp = K.D9.junior(st, pale_level=lvl, gauze=gz, blood=bl)
        sp = dict(sp, name="crew_%s" % key)
        a = Act(F, nm, sp, CREW_H, ppd=240)
        F.cast.append(a); K.acts[nm] = a
    return K.acts[nm]


def kong(F, blood=False):
    """Kong with the EP.1 kit: the watch on the left wrist; the junior's blood on gloves and forearm from S035 on."""
    K = kit(F) if not hasattr(F, "_e1kit") else F._e1kit
    nm = "e1_kong_blood" if blood else "e1_kong_clean"
    if nm not in K.acts:
        a = Act(F, nm, "kong_ep1_02" if blood else "kong_ep1_clean", KONG_H, ppd=240)
        F.cast.append(a); K.acts[nm] = a
    return K.acts[nm]


def film_t(t):
    """stage clock of scene 02 -> episode seconds (the watch runs on the episode clock)."""
    return t - 20000 / EP_FPS + SC02_FILM0


def alarm_on(F, t, lead=0.25):
    """the car alarm starts a quarter second before the narrator names it (S028's last frames) and never stops in this range."""
    on = t >= W("สัญญาณกันขโมย") - lead
    F._e1kit.x1.alarm(on)
    return on


def fight(F):
    """marks of the struggle at the wreck's door for S025 / S027: the pair has turned since the hook's crane shot, so the
    junior faces SOUTH (toward Kong, who comes from the phone mark) with the driver on his back, north of him."""
    b = DM0(F)
    return types.SimpleNamespace(b=b, jun=F.P(b, 0.75, 2.50), drv=F.P(b, 1.52, 2.62), kong=F.P(b, -1.05, 2.92), south=-F.fwd, north=F.fwd)


def bite_pair(F, t, jun, pull=0.0, scream=True):
    """the driver clamped on the junior's shoulder from behind, a stagger loop on twos (the hook's attack(), turned)."""
    M = fight(F)
    tt = C.on_twos(t)
    w = math.sin(tt * 2 * math.pi * 1.7); w2 = math.sin(tt * 2 * math.pi * 2.3 + 1.0)
    mo = 0.75 + 0.25 * (w > 0)
    jun.set(loc=M.jun + F.fwd * (0.05 * w), face=facing(M.south), view="q", s=-1, expr="scared", mouth=("o", mo) if scream else mo, lean=14 + 3 * w,
            legs="step", arm_n=dict(hand=(0.62, 0.30 + 0.05 * w2), elbow=None, hand_shape="open"), arm_f=dict(hand=(0.50, 0.05), elbow=None, hand_shape="open"),
            head=(0, -6 + 4 * w2, 0, 0))
    F.drv_out.set(loc=M.drv + F.fwd * (0.05 * w), face=facing(M.south), view="side", s=-1, expr="bite", legs="lunge", lean=24 + 3 * w,
                  arm_n=dict(hand=(0.50, 0.28), elbow=None, hand_shape="claw"), arm_f="claw_up", head=(0, 12, 0.10, 0.10))
    F.drv.hide()


def kong_ram(F, t, g, kg, thrust=0.0, expr="resolve", loc=None, tilt=86.0, **kw):
    """Kong planted wide, the cutter levelled as a ram in both hands; thrust 0 = drawn back, 1 = driven home."""
    M = fight(F)
    pose = dict(expr=expr, blink=0, head=(0, 2, 0.02 * thrust, 0), lean=4 + 11 * thrust, legs="lunge" if thrust > 0.5 else "wide",
                _hold=dict(grip=(round(0.12 + 0.50 * thrust, 3), 0.50), tilt=round(tilt, 1), jaw=1.0))
    pose.update(kw)
    kg.set(loc=loc if loc is not None else M.kong, face=facing(M.north), view="side", s=1, **pose)
    return kg


def wheel(F):
    """marks at the truck's lane-side rear wheel (S031-S037).  The junior sits in profile in front of the tyre, legs toward
    the tail, facing screen-left; Kong crouches at his knees, facing him.  Marks shared with S038-S049 (sc02b_lib.prep):
    seat = G.J, kong = G.K, and the standing cutter on S040's mark (G.K + tail 0.45 + out 0.60, turned 20 degrees)."""
    A = F._e1kit.A
    ws = Vector(A["wheel_seat"]); out = Vector(A["out_side"]); tail = Vector(A["out_tail"])
    return types.SimpleNamespace(seat=ws + out * 0.10, kong=ws + out * 0.80 + tail * 0.90, cutter=ws + out * 1.40 + tail * 1.35, out=out, tail=tail, hub=Vector(A["wheel_hub"]),
                                 lamp_base=Vector(A["lamp_base"]), lamp_aim=Vector(A["lamp_aim"]))


def wheel_lamp(F, heads, energy=2800.0):
    Wm = wheel(F)
    F.lamp(tuple(Wm.lamp_base)[:2], tuple(Wm.lamp_aim), energy, heads=heads)


def sit(F, jun, t, expr="pain", slump=0.3, view="side", press=False, shiver=0.0, dout=0.0, **kw):
    """the junior seated against the wheel (cast pose `sit_wheel`), facing screen-left.  Upright card (no pitch): with the
    film's pitch a high camera tipped his head back into the wheel-arch lip (S033).  dout moves him out from the tyre."""
    D9 = F._e1kit.D9
    jun.a.pitch_override = 0.0
    p = D9.poses(jun.a.spec, "sit_wheel", s=-1, slump=slump, expr=expr)
    p.pop("view", None); p.pop("s", None)
    if not press:
        p.pop("z", None)
        p["arm_n"] = dict(hand=(0.10, 0.88), elbow=None, hand_shape="open"); p["arm_f"] = dict(hand=(0.06, 0.88), elbow=None, hand_shape="open")   # hands in the lap (the "lap" preset is for a chair)
    if shiver:
        k = int(t * EP_FPS)
        hd = p["head"]
        p["head"] = (hd[0], hd[1] + (C.hash01(k, 1) - 0.5) * 3.0 * shiver, hd[2] + (C.hash01(k, 2) - 0.5) * 0.024 * shiver, hd[3] + (C.hash01(k, 3) - 0.5) * 0.016 * shiver)
        p["lean"] = p["lean"] + (C.hash01(k, 4) - 0.5) * 1.4 * shiver
    if view != "side":
        p["legs"] = "crouch"; p["lean"] = -4            # 3/4 and front drawings: knees up toward the lens (the profile legs would cross the face)
    p.update(kw)
    Wm = wheel(F)
    jun.set(loc=Wm.seat + Wm.out * dout, face=facing(Wm.tail), view=view, s=-1, **p)
    return jun


def kong_crouch(F, kg, t, expr="serious", view="q", s=1, loc=None, **kw):
    Wm = wheel(F)
    loc = Wm.kong if loc is None else Vector(loc)
    kg.a.pitch_override = 0.0
    pose = dict(expr=expr, blink=C.blink("kong", t), legs="crouch", hip=(0.0, 0.52), lean=14, head=(0, 4, 0.02, 0.0),
                arm_n=dict(hand=(0.55, 0.30), elbow=None, hand_shape="glove"), arm_f=dict(hand=(0.48, 0.42), elbow=None, hand_shape="glove"))
    pose.update(kw)
    kg.set(loc=loc, face=facing(Wm.seat - loc), view=view, s=s, **pose)
    kg.breath = 0.006 * math.sin(t * 2.4)
    return kg


PAD_XY = {"side": (0.24, -1.50), "q": (0.12, -1.52)}         # the gauze pad on the junior's neck (figure frame, s = -1 drawings)


def pad_world(F, jun):
    """world point of the gauze pad on the posed junior (his drawing's chin / near shoulder, or the table above)."""
    v = jun.view or "side"
    try:
        an = anchors(jun, jun.pose_d, v, jun.s if jun.s is not None else -1)
        ch = an["chin"]; shy = 0.5 * (an["shoulder_R"][1] + an["shoulder_L"][1])   # measured on the flat drawing: the pad sits
        xy = (ch[0] + 0.05, ch[1] + 0.35 * (shy - ch[1]))                          # just under the chin (big head on a short neck)
    except Exception:
        xy = PAD_XY.get(v, PAD_XY["side"])
    return fig_world(F, jun, jun.loc, xy)


def press_pair(F, t, jun, kg, expr_j="pain", expr_k="serious", slump=0.35, shiver=0.5, off=(0.06, 0.08), spread=-0.08, lean=18, kview="q",
               cutter=True, kkw=None, kloc=None, **jkw):
    """the wheel staging of S034-S037: the junior seated, Kong crouched at his knees with both gloves on the gauze at his
    neck.  The hands are solved onto the pad on screen (reach()); off / spread move them in Kong's figure frame (D)."""
    tt = C.on_twos(t)
    w = math.sin(tt * 2 * math.pi * 0.9)
    sit(F, jun, t, expr=expr_j, slump=slump, shiver=shiver, **jkw)
    Wm = wheel(F)
    kl = Wm.kong if kloc is None else Vector(kloc)
    kg.loc = tuple(kl)
    pad = pad_world(F, jun)
    tn = reach(F, kg, kl, pad, dx=off[0], dy=off[1] + 0.015 * w)
    tf = reach(F, kg, kl, pad, dx=off[0] - 0.10, dy=off[1] - spread + 0.015 * w)

    def pose(a, b):
        kong_crouch(F, kg, t, expr=expr_k, view=kview, lean=lean + 1.5 * w, head=(0, 8, 0.04, 0.02), **(kkw or {}),
                    loc=kl, arm_n=dict(fig=a, hand_shape="press"), arm_f=dict(fig=b, hand_shape="press"))
    pose(tn, tf)
    # one correction step: the drawing's hand anchor lands 0.1-0.15 D off the asked target (glove centre vs wrist, arm
    # length); close to the lens (S035) that is half a frame, so the targets are moved by the measured error
    try:
        an = anchors(kg, kg.pose_d, kg.view, kg.s)
        hs = [an["hand_L"], an["hand_R"]]
        hn = min(hs, key=lambda h: (h[0] - tn[0]) ** 2 + (h[1] - tn[1]) ** 2); hf = hs[1] if hn is hs[0] else hs[0]
        tn2 = (round(2 * tn[0] - hn[0], 3), round(2 * tn[1] - hn[1], 3)); tf2 = (round(2 * tf[0] - hf[0], 3), round(2 * tf[1] - hf[1], 3))
        pose(tn2, tf2)
    except Exception as ex:
        print("press_pair: no hand correction (%s)" % ex, flush=True)
    if cutter: stand_cutter(F)
    return pad


PRESS = (0.84, 0.40)                                         # Kong's near hand on the pad, from his near shoulder (D)


def aim(F, target, dx=0.0, dz=0.0):
    """late(): turn the camera (position, lens, focus kept) onto a posed actor's head, so a close shot is framed on the
    drawing that was actually chosen; dx along the frame's right, dz up, in D."""
    cam = F.cam
    rt = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    look = Vector(target) + rt * dx + Z(dz)
    q = (look - cam.location).to_track_quat("-Z", "Y")
    e0 = cam.rotation_euler.copy()
    cam.rotation_euler = q.to_euler()
    cam["focus"] = tuple(target)
    bpy.context.view_layer.update()
    return look


def stand_cutter(F, loc=None, yaw_deg=20.0):
    """the modelled cutter standing on its battery end (jaws up) at a deck point, three green LEDs lit; the same mark and
    turn as S040 (sc02b_lib.cutter_stand).  It is registered in F._moved, so the next shot's begin() puts it back."""
    from mathutils import Matrix
    cu = F.cutter
    if cu is None: return
    if loc is None: loc = wheel(F).cutter
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


# ---------------------------------------------------------------------------------------------- the watch insert (C1)
def watch_frame(ctx, sec, smear=False, zoom=1.0, drift=(0.0, 0.0), tilt=-12.0, seed=3, drops=6, streak=None):
    """Kong's left wrist, drawn (ep1/cast `draw9.watch_svg` on a glove cuff and a white stick forearm, the cast's own ink):
    sec = seconds since the bite, the hand jumps once a second like a quartz hand.  drift in D of the drawing."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    import rast9, draw9 as D9
    import draw8 as D
    Wp, Hp = ctx.W, ctx.H
    # --- background: the wet deck out of focus, beacon red / blue breathing on a 10-frame cycle
    k = ctx.g
    ph = (k % 20) / 20.0
    red = 0.55 + 0.45 * math.sin(2 * math.pi * ph); blue = 0.55 + 0.45 * math.sin(2 * math.pi * ph + math.pi)
    sm = Image.new("RGB", (36, 64), (12, 17, 34)); d = ImageDraw.Draw(sm)
    d.ellipse([-14, 30, 22, 74], fill=(int(110 * red) + 26, 20, 28)); d.ellipse([16, -14, 52, 26], fill=(20, 34, int(140 * blue) + 36))
    d.ellipse([20, 44, 44, 60], fill=(92, 66, 26))
    bg = sm.resize((Wp, Hp), Image.BICUBIC).filter(ImageFilter.GaussianBlur(Wp / 18.0))
    # --- the drawing, in the cast's units (D); box 6.4 x 6.4 round the dial
    INK = D.INK
    o = ""
    # forearm (white stick, from the lower left), sleeve end, glove cuff and glove (to the upper right)
    o += D9.rect(-3.9, -0.30, 3.2, 0.60, "#f1efe8", INK, 0.06, rx=0.05)
    o += D9.rect(-4.6, -0.62, 1.1, 1.24, "#c8581b", INK, 0.07, rx=0.10)                         # short sleeve hem, far left
    o += D9.rect(-0.95, -0.50, 1.9, 1.0, "#2a2a31", INK, 0.06, rx=0.12)                         # glove cuff under the strap
    o += D.path("M0.80 -0.56 Q1.9 -0.86 2.9 -0.74 Q3.9 -0.60 4.3 -0.05 Q4.3 0.62 3.4 0.80 Q2.0 0.94 0.80 0.56 Z", "#24242a", INK, 0.07)   # glove
    o += D.path("M1.35 -0.66 Q1.9 -1.25 2.55 -1.05 Q2.75 -0.86 2.30 -0.72", "#24242a", INK, 0.07)                                       # thumb
    for x in (2.55, 3.05, 3.55):
        o += D.line((x, -0.52), (x + 0.10, 0.62), "#4a4a54", 0.04)
    o += D.line((-0.95, -0.50), (-0.95, 0.50), "#4a4a54", 0.05)
    o += D.path("M0.95 -0.50 Q2.0 -0.76 3.0 -0.64", "none", "#5a5a66", 0.04)                 # rim light along the glove
    sec_i = math.floor(sec)
    fr = sec - sec_i
    ang = sec_i + (0.10 if fr < 0.045 else 0.0)                                              # one frame of overshoot on the tick
    o += D9.watch_svg(ang, blood=True, smear=smear, size=1.0)
    frag = D.g(o, "rotate(%s)" % D.f(tilt))
    ppd = int(round(Wp / (5.4 / zoom)))
    im = rast9.svg_png(frag, (-3.6, -3.6, 3.6, 3.6), ppd)
    card = Image.fromarray(im)
    # cool rim light on the card: darken toward the lower left a little (paper puppet under night light)
    a = np.asarray(card).astype(np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]].astype(np.float32)
    sh = 0.80 + 0.20 * np.clip((xx / a.shape[1]) * 0.6 + (1 - yy / a.shape[0]) * 0.6, 0, 1)
    tint = np.array([0.90 + 0.10 * red, 0.92, 0.96 + 0.06 * blue], np.float32)
    a[..., :3] = np.clip(a[..., :3] * sh[..., None] * tint, 0, 255)
    card = Image.fromarray(a.astype(np.uint8))
    cx = int(Wp * 0.5 + drift[0] * ppd - card.size[0] / 2); cy = int(Hp * 0.46 + drift[1] * ppd - card.size[1] / 2)
    # soft contact shadow of the arm on the background
    shd = Image.new("L", bg.size, 0); shd.paste(card.split()[3].point(lambda v: int(v * 0.55)), (cx + int(0.10 * ppd), cy + int(0.14 * ppd)))
    bg = Image.composite(Image.new("RGB", bg.size, (2, 3, 8)), bg, shd.filter(ImageFilter.GaussianBlur(ppd * 0.10)))
    bg.paste(card, (cx, cy), card)
    d = ImageDraw.Draw(bg, "RGBA")
    # rain drops on the glass: they sit, then run down; deterministic per drop
    mx, my = Wp * 0.5 + drift[0] * ppd, Hp * 0.46 + drift[1] * ppd
    R = 0.72 * ppd
    for i in range(drops):
        born = (C.hash01(i, seed, 1) * 40 - 20)
        age = (ctx.k - born) / EP_FPS
        if age < 0: continue
        a0 = C.hash01(i, seed, 2) * 2 * math.pi; r0 = math.sqrt(C.hash01(i, seed, 3)) * 0.80 * R
        x = mx + math.cos(a0) * r0; y = my + math.sin(a0) * r0 * 0.9 + max(0.0, age - 0.5) ** 2 * 0.55 * ppd
        if (x - mx) ** 2 + (y - my) ** 2 > (0.80 * R) ** 2: continue
        rr = (0.035 + 0.02 * C.hash01(i, seed, 4)) * ppd
        d.ellipse([x - rr, y - rr * 1.25, x + rr, y + rr * 1.25], fill=(215, 228, 245, 70), outline=(120, 140, 170, 200), width=max(1, int(ppd * 0.012)))
        d.ellipse([x - rr * 0.45, y - rr * 0.8, x - rr * 0.05, y - rr * 0.3], fill=(255, 255, 255, 210))
        if age > 0.5:
            d.line([(x, y - rr), (x, my + math.sin(a0) * r0 * 0.9)], fill=(215, 228, 245, 60), width=max(1, int(rr * 0.9)))
    if streak is not None:                                   # S036: one drop cuts a clean line through the smear
        x = mx + 0.30 * ppd; y0 = my - 0.02 * ppd; y1 = y0 + streak * 0.46 * ppd
        d.line([(x, y0), (x, y1)], fill=(241, 239, 230, 235), width=max(2, int(0.05 * ppd)))
        rr = 0.05 * ppd
        d.ellipse([x - rr, y1 - rr, x + rr, y1 + rr * 1.4], fill=(225, 235, 248, 150), outline=(120, 140, 170, 220), width=max(1, int(ppd * 0.012)))
    import ep2d
    bg = ep2d.rain(bg, ctx.k, 0.2)
    return ep2d.vignette(bg, 0.5)


def lib_selftest():
    return sorted(k for k in globals() if not k.startswith("_"))


# ====================================================================================================== the shot S025
def setup(F):
    kit(F); junior(F, "bitten"); kong(F)


def frame(F, g, t, u):
    K = F._e1kit; M = fight(F)
    jun = junior(F, "bitten"); kg = kong(F)
    t0 = T0(F)
    hard = max(0.0, 1 - (t - t0) / (6 / 24.0))
    sh = tuple(a + b for a, b in zip(hand_cam(t, 0.5, 2.8), hand_cam(t, 3.2 * hard, 11.0, 3.0)))
    hc = M.jun + Z(2.28)
    loc = M.jun + F.right * 3.9 + F.fwd * (-0.55 + 0.25 * u) + Z(1.95)
    look = hc + F.fwd * 0.06 + Z(-0.26)
    F.camera(loc, look, F.pick(46, 38), roll=-5 + 2 * u, focus=hc, k=8.0, kmax=22, shake=sh)
    F.door(DOOR_OPEN)
    alarm_on(F, t)
    bite_pair(F, t, jun)
    F.kong.hide(); F.crew.hide()
    # Kong arrives: the gloves and the tool come in from the south edge over the last 14 frames
    k_in = smooth(ramp(u, 0.30, 1.0))
    kong_ram(F, t, g, kg, thrust=0.8 * k_in, loc=M.kong + F.fwd * 0.20 - F.fwd * (1.6 * (1 - k_in)))
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        M = fight(F)
        jun = junior(F, "bitten")
        F.lamp(F.P(M.b, 6.5, 7.0), M.jun + Z(1.3), 9000.0, heads=[jun.head()])
        F.shadows(M.jun + Z(1.5))
        jun.a.set_glow(WARM, 0.28)


def taxi(F):
    """the alarm car (the taxi `l1_b`, lane 1, north of the wreck): tail point on the deck, its forward and right vectors."""
    K = F._e1kit
    ob = bpy.data.objects[K.A["alarm_car"]]
    if ob.name not in K.car0:
        bpy.context.view_layer.update(); K.car0[ob.name] = ob.matrix_world.copy()
    M0 = K.car0[ob.name]
    if not any(o is ob for o, _ in F._moved):               # integration: begin() of ANY next shot puts a rocked taxi back
        F._moved.append((ob, M0))                            # (kit() only runs in this range's shots)
    body = bpy.data.objects[ob.name + "_body"]
    a = max(Vector(v).y for v in body.bound_box)
    fw = (M0.to_3x3() @ Vector((0, 1, 0))).normalized(); rt = (M0.to_3x3() @ Vector((1, 0, 0))).normalized()
    tail = M0 @ Vector((0, -a, 0)); tail.z = 0.0
    return types.SimpleNamespace(ob=ob, M0=M0, tail=tail, fwd=fw, right=rt, mark=tail - fw * 0.50)


def rock(F, amount_deg, dip=0.0):
    """the taxi on its springs: pitch about its rear axle line + a dip (pure function of the arguments)."""
    from mathutils import Matrix
    X = taxi(F)
    piv = X.tail + X.fwd * 1.2 + Z(0.6)
    X.ob.matrix_world = Matrix.Translation(piv + Z(-dip)) @ Matrix.Rotation(math.radians(amount_deg), 4, X.right) @ Matrix.Translation(-piv) @ X.M0


def lib_file():
    return os.path.abspath(__file__)
