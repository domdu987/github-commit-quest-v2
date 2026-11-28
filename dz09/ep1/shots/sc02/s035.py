"""S035 (class B)  (picture beat under 'ไหลไม่หยุด')  -- INSERT, 85 mm, locked, breathing drift.  Kong's two black gloves on the
white gauze at the junior's neck: the red spreads through the pad from the centre outward in five steps on twos
(the cast's gauze `soak` 0.10 -> 1.0, one junior actor per step), and from the third step Kong's gloves and forearm
carry the blood (kong_ep1_02 from here to the end of the scene)."""
from epbase import *
import os, sys, importlib.util


def lib():
    """the range's small library lives in s025.py (see its docstring)."""
    if "ep1_sc02_s025_lib" not in sys.modules:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s025.py")
        sp = importlib.util.spec_from_file_location("ep1_sc02_s025_lib", p); m = importlib.util.module_from_spec(sp)
        sys.modules["ep1_sc02_s025_lib"] = m; sp.loader.exec_module(m)
    return sys.modules["ep1_sc02_s025_lib"]


L = lib()
DEPS = [L.__file__]
LOC = "X1"
CLASS = "B"
PCT = {"final": 100, "final8": 100}                          # the puppets fill the frame: full scale
STEPS = ("gauze0", "gauze1", "gauze2", "gauze3", "gauze4")
PPD_FINAL = dict({"e1_jun_" + k: 1140 for k in STEPS}, e1_kong_clean=1140, e1_kong_blood=1140)
PPD = dict(PPD_FINAL)                                         # setup() sets it for the tier (begin() and the auto ppd read it)
# 11-28 fix pass: at this lens the junior's head is ~1300 px and Kong's ~1480 px on a 1280 frame; 780 ppd (the auto cap)
# magnified the drawing 1.7-2x (soft lines at the final tier).  And the five step actors and the clean Kong are made in
# setup(), AFTER begin() applies PPD, so only the two actors visible at the middle frame were raised (auto ppd): the
# other four steps were rastered at 240 ppd (5x magnified).  setup() now gives every one of them PPD explicitly.


def setup(F):
    L.kit(F)
    fin = str(F.tier).startswith("final")                  # the final tiers need 1140; a draft (half the pixels) is sharp at 780
    PPD.update({k: (v if fin else min(v, 780)) for k, v in PPD_FINAL.items()})
    acts = [L.junior(F, k) for k in STEPS] + [L.kong(F), L.kong(F, True)]
    for a in acts:
        want = PPD.get(a.name, 240)
        if a.a.ppd != want: a.a.ppd = want; a.key = None


def frame(F, g, t, u):
    Wm = L.wheel(F)
    tt = C.on_twos(t)
    uu = (tt - T0(F)) * 24.0 / max(len(range(*E.scene().local(F.shot.ID))) - 1, 1)
    step = min(len(STEPS) - 1, int(clamp(uu, 0, 0.999) * 1.18 * len(STEPS)))
    for i, k in enumerate(STEPS):
        if i != step: L.junior(F, k).hide()
    jun = L.junior(F, STEPS[step])
    blood = step >= 2
    kg = L.kong(F, blood); L.kong(F, not blood).hide()
    # the camera is aimed at the pad of the posed junior: rough camera, pose, pad, final camera (Kong's hands are solved after)
    br = 0.010 * math.sin(t * 2.2)
    F.camera(Wm.seat + Wm.out * 3.6 + Z(1.0), Wm.seat + Z(0.85), 160.0)
    L.sit(F, jun, t, expr="pain", slump=0.35, shiver=0.3)
    pad = L.pad_world(F, jun)
    loc = pad + Wm.out * 3.55 - Wm.tail * 0.45 + Z(0.14 + br)        # long lens from further off: Kong's card (nearer) tilts less
    # integration 11-28: framed ON the pad and 190 mm (was 0.18 D below it at 160 mm: the pad sat in the top quarter and the
    # insert read as an orange sleeve and a flag, not as a pad going red)
    # 11-28 fix pass (director: "S035 does not read"): 200 mm (was 190) and the pad a little higher in the frame, so the
    # blank underside of his head is a band at the top (240 mm was tried: the drawing would need ~1900 ppd to stay sharp)
    F.camera(loc, pad + Z(-0.06 + br) - Wm.tail * 0.04, 200.0, roll=-2.0, focus=pad, k=9.0, kmax=24, shake=hand_cam(t, 0.04, 1.0))
    L.alarm_on(F, t)
    F.door(DOOR_OPEN)
    F.kong.hide(); F.crew.hide(); F.drv.hide(); F.drv_out.hide()
    # Kong (off frame) kneels close beside him, his card just in front of the junior's along the lens axis (a nearer card
    # would make the gloves twice the size of the pad at this focal length, a further one draws them behind the junior):
    # a glove is bigger than the pad at this scale, so the near glove presses BESIDE it (its fingers on the pad's edge) and the
    # far one holds the chest below: the pad stays in view and goes red between them
    L.press_pair(F, t, jun, kg, shiver=0.3, off=(-0.30, 0.06), spread=-0.36, kview="side", lean=34, cutter=False,
                 kloc=Wm.seat + Wm.out * 0.68 + Wm.tail * 0.80, kkw=dict(hip=(0.0, 0.85)))
    return {"exposure": 1.6, "sharp_idx": [2]}


def late(F, g, t, u):
    if once(F):
        jun = L.junior(F, STEPS[2])
        L.wheel_lamp(F, [])
        F.shadows(L.wheel(F).seat + Z(1.2))
