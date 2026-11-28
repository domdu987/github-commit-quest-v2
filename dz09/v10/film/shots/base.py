"""base.py -- staging shared by the shot scripts: the rescue zone, the three principals' default acting."""
import math
from mathutils import Vector, Euler, Quaternion
import common as C
from common import clamp, smooth, lerp, ramp, ease_out, ease_in
from stage import facing, WARM, COOL, DRV_HIP_Z

# picture / sound-effect cues: these did not move with the Ohm narration (mix_ohm_v2 keeps every effect where it was)
BITE_T = C.CUES["cutter"]            # 15.052 the cutter bites
PHONE_T = C.CUES["phone"]            # 17.648 the phone buzzes
LIFT_T = 41.657                      # the red eye (picture cue; Ohm says "เงยหน้าขึ้น" from 41.751)
LUNGE_T = C.CUES["lunge"]            # 43.445
BITE2_T = C.CUES["scream"]           # 43.795
DOOR_OPEN = 68.0


def driver_seated(F, t, expr="still", head=(0, 14, 0.0, 0.06), lean=6, view=None, **kw):
    d = F.drv; a = d.a
    loc = Vector((F.seat.x, F.seat.y, DRV_HIP_Z - (a.spec["legs"] + 0.06) * a.sc)) + F.fwd * 0.33
    pose = dict(expr=expr, legs=dict(seated=True), arm_r="lap", arm_l="lap", head=head, lean=lean)
    pose.update(kw)
    d.set(loc=loc, face=facing(F.fwd), view=view, **pose)
    return d


def door_dir(F):
    """Kong's facing while he works: toward the door seam."""
    return F.A["kong_to_door_deg"]


def kong_cutter(F, t, g, jaw=1.0, pump=0.0, expr="serious", view="q", s="keep", loc=None, face=None, head=(0, 4, 0, 0), lean=10,
                grip=(0.30, 0.74), tilt=62.0, **kw):
    """Kong braced at the door with the cutter in BOTH hands (near hand on the rear handle, far hand on the fore grip),
    levelled at the seam.  jaw 1 open .. 0 shut; pump = recoil 0..1; grip = rear hand relative to the near shoulder
    (+x = the way he faces); tilt = degrees from straight down toward his facing side."""
    k = F.kong
    pose = dict(expr=expr, blink=C.blink("kong", t), head=head, lean=lean - 2 * pump, legs="wide",
                _hold=dict(grip=(round(grip[0] - 0.07 * pump, 3), round(grip[1], 3)), tilt=round(tilt, 1), jaw=round(jaw, 2)))
    pose.update(kw)
    k.set(loc=loc if loc is not None else F.K, face=door_dir(F) if face is None else face, view=view, s=s, **pose)
    k.breath = 0.006 * math.sin(t * 2.4)
    return k


def crew_pry(F, t, loc=None, view="q", s="keep", idx=None, **kw):
    """the crew member working the door edge with both hands while Kong is on the phone."""
    c = F.crew
    w = math.sin(C.on_twos(t) * 2 * math.pi * 1.1)
    pose = dict(expr="neutral", blink=C.blink("crew", t), lean=12 + 3 * w, legs="wide",
                arm_n=dict(hand=(0.55, 0.45 + 0.05 * w), elbow=None, hand_shape="grip"), arm_f=dict(hand=(0.42, 0.62 + 0.05 * w), elbow=None, hand_shape="grip"))
    pose.update(kw)
    c.set(loc=loc if loc is not None else F.P(F.door_mid, 0.15, 1.25, -F.door_mid.z), face=facing(-F.right), view=view, s=s, idx=idx, **pose)
    c.breath = 0.006 * math.sin(t * 2.9 + 1)
    return c


def crew_ready(F, t, loc, face, view="q", s="keep", idx=None, **kw):
    """the young crew member standing by, clear of Kong: feet apart, pry bar hand ready, watching the door (S06, S07)."""
    c = F.crew
    w = math.sin(C.on_twos(t) * 2 * math.pi * 0.7)
    pose = dict(expr="neutral", blink=C.blink("crew", t), lean=3 + 1.5 * w, legs="wide", head=(0, 3, 0, 0),
                arm_n=dict(hand=(0.34, 0.52 + 0.03 * w), elbow=None, hand_shape="grip"), arm_f="down")
    pose.update(kw)
    c.set(loc=loc, face=face, view=view, s=s, idx=idx, **pose)
    c.breath = 0.006 * math.sin(t * 2.9 + 1)
    return c


def rescue_lamp(F, cam_side=1.0, energy=8000.0, heads=()):
    """default work lamp: beyond the car's nose, on the lane side."""
    base = F.P(F.door_mid, 5.5, 3.2 * cam_side)
    F.lamp((base.x, base.y), tuple(F.P(F.door_mid, 0, 1.0, 0)), energy, heads or [F.kong.head(), F.crew.head()])


def once(F):
    """True the first time it is called in a shot (per process): build the lamp / foreground / shadows there."""
    if F._lamp_done or getattr(F, "_once_shot", None) == (F.shot.ID, F._begin_n):
        return False
    F._once_shot = (F.shot.ID, F._begin_n)
    return True


def DM0(F):
    """ground point under the middle of the driver's door."""
    return Vector((F.door_mid.x, F.door_mid.y, 0.0))


def Z(z):
    return Vector((0, 0, z))


def hand_cam(t, amp, hz=2.2, seed=0.0):
    return C.shake(t, amp, hz, seed)


def phone_uri(F, state="missed"):
    import phone8
    k = "_uri_" + state
    if not hasattr(F, k):
        setattr(F, k, phone8.data_uri(F.screens[state]))
    return getattr(F, k)


def kong_phone(F, t, g, loc, face, view="front", s="keep", expr="guilty", talk=False, ear=True, head=(0, 6, 0, 0.02), lean=2, hip=(0, 0), idx=None, **kw):
    """Kong on the call at the phone mark: phone at his ear (near arm), lip sync when it is his line."""
    pose = dict(expr=expr, blink=C.blink("kong", t), head=head, lean=lean, hip=hip, legs="stand")
    if view in ("front", "back"):
        # v2: elbow out to the side, so the forearm does not cross the mouth (the "phone_ear" preset folds it under the chin)
        pose.update(arm_r=(dict(hand=(0.22, -0.50), elbow=1, hand_shape="grip") if view == "front" else "phone_ear") if ear else "phone_look",
                    prop_r=dict(type="phone"), arm_l="down")
    else:
        pose.update(arm_n=dict(hand=(-0.30, -0.55), elbow=None, hand_shape="grip") if ear else "phone_look", prop_n=dict(type="phone"), arm_f="down")
    if talk:
        m = C.mouth(g)
        if m > 0: pose["mouth"] = m
    pose.update(kw)
    F.kong.set(loc=loc, face=face, view=view, s=s, idx=idx, **pose)
    F.kong.breath = 0.006 * math.sin(t * 2.4)
    return F.kong


def attack(F, t, g, shake_amp=1.0, scream=False, lock=False):
    """the driver on the crew member after the bite (S22-S24): a stagger loop on twos."""
    tt = C.on_twos(t)
    w = math.sin(tt * 2 * math.pi * 1.7); w2 = math.sin(tt * 2 * math.pi * 2.3 + 1.0)
    base = DM0(F)
    cl = F.P(base, -0.35 + 0.06 * w, 1.75 + 0.08 * w2)
    mo = 0.75 + 0.25 * (w > 0)
    vw = dict(view="q", s=-1) if lock else {}               # lock: the close shot must not flip drawings as he staggers
    F.crew.set(loc=cl, face=facing(-F.right), expr="scared", mouth=("o", mo) if scream else mo, **vw, lean=-7 + 3 * w, legs="step",
               arm_n="guard", arm_f=dict(hand=(0.25, -0.35), elbow=None, hand_shape="open"), head=(0, -8 + 5 * w2, 0, 0))
    F.drv_out.set(loc=F.P(base, -0.35 + 0.06 * w, 0.95 + 0.08 * w2), face=facing(F.right), expr="bite", legs="lunge", lean=26 + 3 * w, **(dict(view="side", s=1) if lock else {}),
                  arm_n="claw", arm_f="claw_up", head=(0, 10, 0.08, 0.04))
    F.drv.hide()


def crew_at_door(F):
    return F.P(DM0(F), -0.45, 1.25)


def call_lamp(F, heads):
    """work lamp for the phone-mark shots: north-east of Kong, raking across the lane."""
    F.lamp(F.PM + Vector((5.2, 6.5, 0)), F.PM + Z(1.2), 9000.0, heads=heads)
