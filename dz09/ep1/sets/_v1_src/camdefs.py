"""camdefs.py -- the planned camera positions of plan/shots_ep1.json for each set, as functions of the set's anchors,
with the two test puppets (rig.kong = kong_wet, rig.crew = crew_wet) standing where the shot puts its people.
fn(rig, R, u) -> dict(loc, look, lens, focus, k, post, shadow_at);  u = 0..1 along the 24-frame cost test."""
import math
from mathutils import Vector


def Z(z): return Vector((0, 0, z))


def face_to(frm, to):
    """facing degrees (0 = -Y, +90 = +X) that turns a puppet at `frm` toward `to`."""
    d = Vector(to) - Vector(frm)
    return math.degrees(math.atan2(d.x, -d.y))


def stand(rig, act, loc, look_at, **kw):
    pose = dict(expr="neutral", legs="stand", arm_n="down", arm_f="down")
    pose.update(kw)
    act.set(loc=tuple(loc), face=face_to(loc, look_at), **pose)


def hide_all(rig):
    for a in rig.acts: a.hide()


# ================================================================================================================ X1
def x1_s34(rig, R, u):
    """S34 M two-shot 35 mm, slow push 0.4 D: the junior against the rear wheel, Kong crouched pressing the wound."""
    A = R["anchors"]; ws = Vector(A["wheel_seat"]); out = Vector(A["out_side"]); back = Vector(A["out_tail"])
    kk = Vector(A["kong_kneel"])
    rig.crew.set(loc=tuple(ws + out * 0.10), face=face_to(ws, ws + out), view="front", expr="scared", legs="crouch", arm_r="lap", arm_l="lap", lean=-4)
    rig.kong.set(loc=tuple(kk), face=face_to(kk, ws), view="q", expr="serious", legs="crouch", arm_n=dict(hand=(0.55, 0.50), elbow=None, hand_shape="glove"), arm_f=dict(hand=(0.50, 0.58), elbow=None, hand_shape="glove"), lean=14)
    look = ws + out * 0.55 + Z(1.25)
    loc = ws + out * (5.4 - 0.4 * u) + back * 0.9 + Z(1.25)
    def late(rig, R):
        import beauty as B
        B.place_work_lamp_safe(rig.A, rig.cam, [tuple(rig.kong.head()), tuple(rig.crew.head())], base=tuple(A["lamp_base"])[:2], aim=tuple(A["lamp_aim"]), energy=2800.0)
    return dict(loc=loc, look=look, lens=35, focus=ws + out * 0.3 + Z(1.2), k=6.0, post={"exposure": 1.6}, shadow_at=ws + Z(1.0), late=late)


def x1_s54(rig, R, u):
    """S54 M split 35 mm, locked: the truck's rear corner is a vertical edge in the middle of the frame."""
    A = R["anchors"]; co = Vector(A["corner"]); out = Vector(A["out_side"]); back = Vector(A["out_tail"])
    sc = Vector(A["side_crouch"]); th = Vector(A["tail_hide"])
    rig.crew.set(loc=tuple(sc), face=face_to(sc, sc + out), view="q", expr="neutral", legs="crouch", arm_n="claw", arm_f="claw", lean=10)
    rig.kong.set(loc=tuple(th), face=face_to(th, th + back), view="front", expr="alarmed", legs="stand", arm_r="down", arm_l=dict(hand=(0.12, 0.95), elbow=None, hand_shape="glove"))
    d = (out + back).normalized()
    loc = co + d * 7.0 + Z(1.7)
    return dict(loc=loc, look=co + Z(1.75), lens=35, focus=co + Z(1.5), k=5.0, post={"exposure": 1.6}, shadow_at=co + Z(1.0))


def x1_s29(rig, R, u):
    """S29 M 35 mm, slow push 0.3 D: the hatchback's alarm lamps pulsing on the wet road."""
    A = R["anchors"]; hide_all(rig)
    bn = Vector(A["alarm_bonnet"]); fr = Vector(A["alarm_front"])
    f = (fr - bn); f.z = 0; f.normalize(); side = Vector((f.y, -f.x, 0))
    loc = fr + f * (6.2 - 0.3 * u) + side * 2.4 + Z(1.25)
    stand(rig, rig.crew, fr + f * 1.3 + side * 1.6, bn, view="back", arm_n="claw", arm_f="claw")
    return dict(loc=loc, look=bn + Z(-0.15), lens=35, focus=bn, k=5.0, post={"exposure": 1.6}, frame=8, shadow_at=fr + Z(1))


def x1_s57(rig, R, u):
    """S57 W 28 mm, locked: over the roofs toward the bus the rider drops behind."""
    A = R["anchors"]
    rt = R["roof_route"]
    names = [r["name"] for r in rt]
    mid = rt[min(len(rt) - 2, max(1, len(rt) // 2))]
    p1 = Vector(mid["mid"]); p0 = Vector(rt[max(0, len(rt) // 2 - 1)]["mid"])
    rig.crew.set(loc=tuple(p0), face=face_to(p0, p1), view="side", s=1, expr="neutral", legs="crouch", arm_n="claw", arm_f="claw", lean=20)
    rig.kong.set(loc=tuple(p1), face=face_to(p1, A["bus_tail"]), view="side", s=1, expr="alarmed", legs="lunge", arm_n="raise", arm_f="down", lean=12)
    bus = Vector(A["bus_tail"])
    loc = Vector((-12.35, p0.y - 15.0, 3.3))
    return dict(loc=loc, look=Vector((-13.6, bus.y - 6.0, 3.0)), lens=28, focus=p1, k=2.5, post={"exposure": 1.6}, shadow_at=p1 + Z(1))


# =============================================================================================================== X1S
def x1s_s62(rig, R, u):
    """S62 W 28 mm, locked: road level on the shoulder behind the truck, looking back; the sedan on its side, a small
    figure at its windscreen frame; Kong in the right foreground, turning."""
    A = R["anchors"]; pm = Vector(A["praew_mark"]); ws = Vector(A["windscreen"])
    stand(rig, rig.crew, pm, ws, view="back", legs="wide", lean=-14, arm_n=dict(hand=(0.55, 0.40), elbow=None, hand_shape="grip"), arm_f=dict(hand=(0.50, 0.48), elbow=None, hand_shape="grip"))
    kp = Vector((-18.3, 5.6, 0))
    stand(rig, rig.kong, kp, pm, view="q", expr="alarmed")
    loc = Vector((-19.9, 10.6, 1.25))
    return dict(loc=loc, look=Vector((-19.6, -5.0, 1.75)), lens=28, focus=pm + Z(1.5), k=3.0, post={"exposure": 1.6}, shadow_at=pm + Z(1))


def x1s_s63(rig, R, u):
    """S63 MW low 35 mm, slow push 0.4 D: roof toward us, hazards on the upper flank, steam, glass, the briefcase."""
    A = R["anchors"]; pm = Vector(A["praew_mark"]); km = Vector(A["kong_mark"]); ws = Vector(A["windscreen"]); rm = Vector(A["roof_mid"])
    stand(rig, rig.crew, pm, ws, view="q", legs="wide", lean=-16, arm_n=dict(hand=(0.55, 0.40), elbow=None, hand_shape="grip"), arm_f=dict(hand=(0.50, 0.48), elbow=None, hand_shape="grip"))
    stand(rig, rig.kong, km + Vector((0.3, -1.2, 0)), ws, view="q", expr="serious", legs="wide", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True))
    loc = Vector((rm.x + 5.2 - 0.3 * u, ws.y + 7.4 - 0.25 * u, 1.0))
    return dict(loc=loc, look=Vector((rm.x - 0.5, ws.y + 0.4, 1.05)), lens=35, focus=pm + Z(1.4), k=4.0, post={"exposure": 1.6}, shadow_at=pm + Z(1))


def x1s_s65(rig, R, u):
    """S65 M two-shot 35 mm, locked: into the tipped cabin through the empty windscreen frame."""
    A = R["anchors"]; pm = Vector(A["praew_mark"]); ws = Vector(A["windscreen"])
    rig.kong.hide()
    stand(rig, rig.crew, pm + Vector((0.5, -0.3, 0)), ws, view="q", legs="wide", lean=-12, arm_n=dict(hand=(0.6, 0.45), elbow=None, hand_shape="grip"), arm_f="down")
    loc = ws + Vector((3.3, 3.9, 0.35))
    return dict(loc=loc, look=ws + Vector((0.0, 0.2, 0.0)), lens=35, focus=ws, k=5.0, post={"exposure": 1.7}, shadow_at=pm + Z(1))


# ================================================================================================================ X2
def x2_s82(rig, R, u):
    """S82 W low 35 mm, locked: behind the stopped rescue truck; in its headlights the box truck across every lane,
    the gate and the stair lamp at the barrier beside its cab."""
    A = R["anchors"]; tr = Vector(A["truck_rear"]); f = Vector(A["truck_fwd"]); r = Vector(A["truck_right"])
    hide_all(rig)
    g = Vector(A["gate_inside"])
    stand(rig, rig.kong, g + Vector((0.6, -2.2, 0)), g, view="back")
    stand(rig, rig.crew, g + Vector((1.5, -3.6, 0)), g, view="back")
    loc = tr - f * 0.6 + r * 4.3 + Z(0.9)
    return dict(loc=loc, look=Vector(A["lorry_side_mid"]) + Vector((-2.5, 0, -1.2)), lens=35, focus=Vector(A["lorry_side_mid"]), k=2.0, post={"exposure": 1.6}, shadow_at=g + Z(1))


def x2_s97(rig, R, u):
    """S97 POV 50 mm, slow push 0.5 D: from the cab through the left of the windscreen: the mesh gate, the landing and
    handrail going down outside the barrier, the caged lamp, the way-out sign; twelve D away."""
    A = R["anchors"]; f = Vector(A["truck_fwd"]); g = Vector(A["gate"])
    n = Vector(A["truck_nose"])
    hide_all(rig)
    stand(rig, rig.crew, Vector(A["gate_inside"]) + Vector((1.0, -5.5, 0)), g, view="side", s=-1, arm_n="claw", arm_f="claw", lean=14)
    loc = n - f * (2.3 - 0.5 * u) + Vector((-0.6, 0, 1.25))
    return dict(loc=loc, look=g + Z(1.9), lens=50, focus=g + Z(1.5), k=3.0, post={"exposure": 1.6}, shadow_at=g + Z(1))


def x2_s98(rig, R, u):
    """S98 W 28 mm, locked, high three-quarter: the truck's median side and rear (where the horde beats on it), the
    taxi against its barrier side, the jam behind."""
    A = R["anchors"]; t = Vector(A["truck"]); f = Vector(A["truck_fwd"]); r = Vector(A["truck_right"])
    stand(rig, rig.kong, Vector(A["truck_right_side"]) + f * 0.6, t, view="back", arm_n="raise", arm_f="raise")
    stand(rig, rig.crew, Vector(A["truck_rear"]) + r * 0.5, t, view="back", arm_n="raise", arm_f="claw")
    loc = t + r * 8.6 - f * 10.5 + Z(6.2)
    return dict(loc=loc, look=t + f * 1.0 + Z(1.6), lens=28, focus=t + Z(1.5), k=2.0, post={"exposure": 1.6}, shadow_at=t + r * 3 + Z(1))


def x2_s107(rig, R, u):
    """S107 M 35 mm, locked (set X2c): the barrier side of the truck, the hand-span between its crew door and the taxi's
    smashed window."""
    A = R["anchors"]; cd = Vector(A["crew_door_out"]); f = Vector(A["truck_fwd"]); tw = Vector(A["taxi_window"])
    stand(rig, rig.crew, cd + f * 0.5, cd + f * 4, view="q")
    stand(rig, rig.kong, cd - f * 1.2, cd + f * 4, view="q", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True))
    loc = cd + f * 6.4 + Vector((-0.25, 0, 1.75))
    return dict(loc=loc, look=cd - f * 0.4 + Z(1.6), lens=35, focus=cd + Z(1.6), k=4.0, post={"exposure": 1.7}, shadow_at=cd + Z(1))


# =============================================================================================================== CAB
def _seated(rig, act, name, **kw):
    import cab
    A = cab._S["R"]["anchors"]
    legs = (act.a.spec["legs"] + 0.06) * act.a.sc
    pose = dict(expr="neutral", legs=dict(seated=True), arm_r="lap", arm_l="lap", arm_n="lap", arm_f="lap")
    pose.update(kw)
    act.a.pitch_override = 0.0
    act.set(loc=cab.seat(name, legs), face=rig.ST.facing(Vector(A["fwd"])), **pose)


def _cabW(p):
    import cab
    return cab._S["R"]["root"].matrix_world @ Vector(p)


def cab_s78(rig, R, u):
    """S78 CU 50 mm, locked: from inside at the right-hand rear side window; a face pressed to the wet, breath-fogged
    glass outside.  (From the bench the driver's own window is behind his seat back; Kong's profile edge needs the
    camera on the passenger seat, see API.)"""
    import cab
    A = R["anchors"]; F = cab.F
    cab.wipers(None); cab.mirror(None); cab.fog(0.7, "rear_right"); cab.switch("siren", False)
    _seated(rig, rig.kong, "drv", view="back", expr="guilty", arm_r="wheel", arm_l="wheel")
    wd = Vector(A["win_rear_right"]); od = wd + Vector(A["right"]) * 0.55; od.z = 0
    rig.crew.a.pitch_override = 0.0
    rig.crew.set(loc=tuple(od + Vector(A["right"]) * -0.38), face=face_to(od, wd), view="front", expr="shouting", legs="stand", arm_r=dict(hand=(0.45, 0.25), elbow=None, hand_shape="claw"), arm_l=dict(hand=(0.45, 0.30), elbow=None, hand_shape="claw"))
    loc = _cabW((-0.55, -1.15, F + 2.5))
    return dict(loc=loc, look=wd + Z(0.25), lens=50, focus=wd, k=5.0, clip=0.02, post={"exposure": 1.8, "sparkle": 0.0}, shadow_at=od + Z(1.5))


def cab_s81(rig, R, u):
    """S81 POV 24 mm, locked to the cab: through the windscreen, wipers beating; ahead in the headlights the lorry."""
    import cab
    A = R["anchors"]; F = cab.F
    cab.wipers(0.2 + u * 0.9); cab.mirror(None); cab.fog(0)
    _seated(rig, rig.kong, "drv", view="back", arm_r="wheel", arm_l="wheel")
    _seated(rig, rig.crew, "pas", view="back")
    loc = _cabW((0.05, -0.75, F + 2.42))
    return dict(loc=loc, look=_cabW((0.0, 6.0, F + 1.85)), lens=24, focus=_cabW((0, 14, 1.5)), k=2.0, clip=0.02, post={"exposure": 1.7, "sparkle": 0.0}, shadow_at=None)


def cab_s84(rig, R, u):
    """S84 INSERT 85 mm: the console; the red rocker under its hand-lettered label (siren on: LED lit)."""
    import cab
    A = R["anchors"]; F = cab.F
    hide_all(rig)
    cab.switch("siren", True); cab.switch("beacon", True); cab.wipers(None)
    sw = Vector(A["switch_siren"])
    loc = sw + Vector(A["right"]) * 0.40 - Vector(A["fwd"]) * 1.0 + Z(0.60)
    return dict(loc=loc, look=sw + Vector(A["right"]) * 0.12 + Z(-0.07), lens=70, focus=sw, k=9.0, clip=0.02, post={"exposure": 1.9, "rain": False, "sparkle": 0.0})


def cab_s88(rig, R, u):
    """S88 CU 50 mm: from the dash looking back; a figure leaning forward between the front seats from the rear bench,
    the driver's shoulder, the roll shutter of the equipment wall behind."""
    import cab, gear
    A = R["anchors"]; F = cab.F
    cab.switch("siren", True); cab.switch("beacon", True); cab.fog(0); gear.shutter(0.0)
    _seated(rig, rig.kong, "drv", view="q", s=-1, expr="alarmed", arm_n="wheel", arm_f="wheel")
    legs = (rig.crew.a.spec["legs"] + 0.06) * rig.crew.a.sc
    p = _cabW((-0.05, -0.80, cab.CUSH + 0.17 - legs))
    rig.crew.a.pitch_override = 0.0
    rig.crew.set(loc=tuple(p), face=rig.ST.facing(Vector(A["fwd"])), view="front", expr="shouting", legs=dict(seated=True), arm_r="shout", arm_l="lap", lean=10)
    loc = _cabW((-0.30, 1.45 - 0.1 * u, F + 2.45))
    return dict(loc=loc, look=_cabW((0.05, -0.8, F + 2.40)), lens=35, focus=_cabW((-0.05, -0.8, F + 2.4)), k=6.0, clip=0.02, post={"exposure": 1.7, "rain": True, "sparkle": 0.0}, shadow_at=None)


# ============================================================================================================== GEAR
def gear_s101(rig, R, u):
    """S101 INSERT pan 35 mm, pan right 0.8 D: across the shelves, shutter up, the strip lamp on."""
    import cab, gear
    F = cab.F; hide_all(rig)
    gear.shutter(1.0)
    for n in ("cutter", "crowbar", "radio", "pouch"): gear.take(n, False)
    x = -0.45 + 0.8 * u
    loc = _cabW((x, -0.80, F + 2.05))
    return dict(loc=loc, look=_cabW((x + 0.05, cab.Y0 - 0.5, F + 1.95)), lens=35, focus=_cabW((x, cab.Y0 - 0.4, F + 2.0)), k=6.0, clip=0.02, post={"exposure": 1.8, "rain": False, "sparkle": 0.0})


def gear_s102(rig, R, u):
    """S102 INSERT 50 mm: one of the four setups: the crowbar in its clips over the rope and the helmets."""
    import cab, gear
    F = cab.F; hide_all(rig)
    gear.shutter(1.0)
    loc = _cabW((0.55, -1.05, F + 2.95))
    return dict(loc=loc, look=_cabW((0.42, cab.Y0 - 0.14, F + 2.98)), lens=50, focus=_cabW((0.4, cab.Y0 - 0.14, F + 3.0)), k=8.0, clip=0.02, post={"exposure": 1.8, "rain": False, "sparkle": 0.0})


def gear_wall(rig, R, u):
    """the whole wall (not a planned shot): 20 mm from between the front seats, shutter up, all four items in place."""
    import cab, gear
    F = cab.F; hide_all(rig)
    gear.shutter(1.0)
    for n in ("cutter", "crowbar", "radio", "pouch"): gear.take(n, False)
    loc = _cabW((0.0, -0.55, F + 2.35))
    return dict(loc=loc, look=_cabW((0.0, cab.Y0 - 0.3, F + 2.33)), lens=20, focus=_cabW((0, cab.Y0 - 0.3, F + 2.3)), k=3.0, clip=0.02, post={"exposure": 1.8, "rain": False, "sparkle": 0.0})


def gear_s100(rig, R, u):
    """S100 M 28 mm: from the front of the cab at the equipment wall; the shutter half up, two of the four items already
    gone (cutter, pouch), a figure at the wall, another ducking aside on the bench."""
    import cab, gear
    A = R["anchors"]; F = cab.F
    gear.shutter(0.55 + 0.45 * u); gear.take("cutter", True); gear.take("pouch", True); gear.take("crowbar", False); gear.take("radio", False)
    legs = (rig.kong.a.spec["legs"] + 0.06) * rig.kong.a.sc
    rig.kong.a.pitch_override = 0.0
    rig.kong.set(loc=tuple(_cabW((0.55, -1.25, cab.CUSH + 0.25 - legs))), face=rig.ST.facing(-Vector(A["fwd"])), view="back", expr="serious", legs=dict(seated=True), arm_r="raise", arm_l="reach")
    _seated(rig, rig.crew, "rl", view="q", s=1, expr="scared", lean=-8)
    loc = _cabW((0.15, 1.30, F + 2.75))
    return dict(loc=loc, look=_cabW((0.1, cab.Y0, F + 2.25)), lens=28, focus=_cabW((0, cab.Y0, F + 2.0)), k=4.0, clip=0.02, post={"exposure": 1.8, "rain": False, "sparkle": 0.0})


# ====================================================================================================== STAIR / UND
DARK_FLAT = {"GLOW": 0.07, "AMB": 0.30}        # v8 puppets in a dark set: the default white halo (GLOW 0.20) outlines them like stickers
UND_POST = {"exposure": 1.6, "RAIN": 0.0, "SPLASH": 0.0, "sparkle": 0.0, "flat": DARK_FLAT}


def stair_s111(rig, R, u):
    """S111 W side 28 mm, crane down 1.0 D with them: the deck edge and the top two flights from the street side, rain
    falling past, the gate lamp; figures on the treads."""
    import stair
    T = stair._S["T"]; A = T["anchors"]
    p0 = Vector(stair.tread(0, 5)); p1 = Vector(stair.tread(1, 3))
    rig.kong.a.pitch_override = 0.0; rig.crew.a.pitch_override = 0.0
    rig.kong.set(loc=tuple(p0), face=face_to(p0, p0 + Vector((0, -1, 0))), view="side", s=-1, expr="serious", legs="step", arm_n="down", arm_f="down")
    rig.crew.set(loc=tuple(p1), face=face_to(p1, p1 + Vector((0, 1, 0))), view="side", s=1, expr="scared", legs="step", arm_n="down", arm_f="down")
    cy = (A["s_a"] + A["s_b"]) / 2
    loc = Vector((-39.5, cy + 0.6, -2.6 - 1.0 * u))
    return dict(loc=loc, look=Vector((A["x_out"], cy, -2.9 - 1.0 * u)), lens=28, focus=p0 + Z(1.5), k=2.5, post={"exposure": 1.9, "RAIN": 0.2, "SPLASH": 0.0, "flat": DARK_FLAT}, shadow_at=p0 + Z(1.5))


def stair_low(rig, R, u):
    """under the deck from the next pier (not a planned shot): the lower flights against the rain curtain."""
    import stair
    T = stair._S["T"]; A = T["anchors"]
    p0 = Vector(stair.tread(8, 4)); p1 = Vector(stair.tread(9, 6))
    rig.kong.a.pitch_override = 0.0; rig.crew.a.pitch_override = 0.0
    rig.kong.set(loc=tuple(p0), face=face_to(p0, p0 + Vector((0, -1, 0))), view="side", s=1, legs="step")
    rig.crew.set(loc=tuple(p1), face=face_to(p1, p1 + Vector((0, 1, 0))), view="side", s=-1, legs="step")
    cy = (A["s_a"] + A["s_b"]) / 2
    loc = Vector((-9.0, cy - 3.0, -27.6))
    return dict(loc=loc, look=Vector((A["x_in"] - 1.7, cy, -25.5)), lens=35, focus=p0 + Z(1.5), k=2.5, post=dict(UND_POST), shadow_at=p0 + Z(1.5))


def und_s112(rig, R, u):
    """S112 EW 24 mm, locked: the street between the piers, almost black; rain sheets at both deck edges, drips along the
    joint, puddles holding the one far sodium lamp; the group very small at the stair foot."""
    import under
    A = under._S["U"]["anchors"]; g = Vector(A["group_mark"])
    stand(rig, rig.kong, g, g + Vector((0, 10, 0)), view="q")
    stand(rig, rig.crew, g + Vector((1.6, -1.0, 0)), g + Vector((0, 10, 0)), view="q")
    under.fill(0.0); under.bounce(under.BOUNCE_W, (g.x + 2.4, g.y - 2.5, A["ground_z"] + 5.5))
    loc = Vector((-11.5, g.y - 46.0, A["ground_z"] + 2.0))
    return dict(loc=loc, look=Vector((-13.5, g.y + 40.0, A["ground_z"] + 6.5)), lens=24, focus=g + Z(1.5), k=1.5, post=dict(UND_POST), shadow_at=g + Z(1.5))


def und_s122(rig, R, u):
    """S122 W 28 mm, locked: the dark street; one small bright rectangle (the phone) is the only light near them and
    throws a shadow up the pier.  The phone is a stand-in point light here (und_fill at chest height)."""
    import under
    A = under._S["U"]["anchors"]; g = Vector(A["group_mark"]); pf = Vector(A["pier_face_200"])
    kp = Vector((-7.0, 204.5, A["ground_z"]))
    stand(rig, rig.kong, kp, kp + Vector((0, -5, 0)), view="q", arm_n="phone_look")
    stand(rig, rig.crew, kp + Vector((-3.2, 2.6, 0)), kp, view="q")
    under.fill(22.0, tuple(kp + Vector((0.25, -0.45, 1.75)))); under.bounce(110.0, tuple(kp + Vector((-4.0, -3.0, 5.5))))
    loc = Vector((-13.5, 194.0, A["ground_z"] + 1.7))
    return dict(loc=loc, look=kp + Vector((1.2, 0, 2.4)), lens=28, focus=kp + Z(1.5), k=2.5, post=dict(UND_POST), shadow_at=kp + Z(1.5))


def und_s133(rig, R, u):
    """S133 EW 35 mm, slow track right: along the piers; figures in single file on the black side, walking toward the
    pale glow at the far end."""
    import under
    A = under._S["U"]["anchors"]; z = A["ground_z"]
    p = Vector((-13.4, 236.0, z))
    under.fill(0.0); under.bounce(under.BOUNCE_W, (p.x - 3.0, p.y - 2.5, z + 5.5))
    stand(rig, rig.kong, p, p + Vector((0, 10, 0)), view="back", legs="step")
    stand(rig, rig.crew, p + Vector((0.3, 3.4, 0)), p + Vector((0, 10, 0)), view="back", legs="step")
    loc = Vector((-17.5 + 1.0 * u, 212.0, z + 1.9))
    return dict(loc=loc, look=Vector((-12.0, 300.0, z + 4.2)), lens=35, focus=p + Z(1.5), k=2.0, post=dict(UND_POST), shadow_at=p + Z(1.5))


CAMS = {
    "STAIR": [dict(name="S111", cls="B", cost=True, fn=stair_s111), dict(name="LOW", cls="B", fn=stair_low)],
    "UND": [dict(name="S112", cls="B", cost=True, fn=und_s112), dict(name="S122", cls="B", fn=und_s122), dict(name="S133", cls="B", fn=und_s133)],
    "CAB": [dict(name="S78", cls="A", fn=cab_s78), dict(name="S81", cls="B", fn=cab_s81), dict(name="S84", cls="B", fn=cab_s84), dict(name="S88", cls="A", cost=True, fn=cab_s88)],
    "GEAR": [dict(name="S101", cls="B", fn=gear_s101), dict(name="S102", cls="B", fn=gear_s102), dict(name="S100", cls="A", cost=True, fn=gear_s100), dict(name="WALL", cls="B", fn=gear_wall)],
    "X2": [dict(name="S82", cls="B", cost=True, fn=x2_s82), dict(name="S97", cls="B", fn=x2_s97), dict(name="S98", cls="B", fn=x2_s98), dict(name="S107", cls="A", fn=x2_s107)],
    "X1": [dict(name="S34", cls="A", cost=True, fn=x1_s34), dict(name="S54", cls="A", fn=x1_s54), dict(name="S29", cls="B", fn=x1_s29), dict(name="S57", cls="B", fn=x1_s57)],
    "X1S": [dict(name="S62", cls="B", fn=x1s_s62), dict(name="S63", cls="B", cost=True, fn=x1s_s63), dict(name="S65", cls="A", fn=x1s_s65)],
}
