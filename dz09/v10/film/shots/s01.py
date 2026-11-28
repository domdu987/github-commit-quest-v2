"""S01  radio: 'ศูนย์ครับ คนเจ็บไม่ตอบสนอง เดี๋ยว! เฮ้ย!'  -- T1 prop macro: the rescue handset held up in a gloved hand,
LED pulsing with the voice, Kong working out of focus behind; snap push on 'เดี๋ยว!', flinch on 'เฮ้ย!', dead at 3.24."""
from shots.base import *
ID = "S01"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1
T_WAIT, T_HEY, T_DEAD = C.word("เดี๋ยว!"), C.word("เฮ้ย!"), C.CUES["static2"]      # Ohm: 2.151, 2.623; the radio dies at 3.243


RISE = -0.10                                              # final: the push sinks 0.10 (it rose 0.46) and tilts up a little: Kong stays under the icon strip
HOLD_Z = 1.72                                             # v3: the handset is HELD at chest height (gloved hand, orange sleeve), above the fallen delivery box


def spot(F):
    x, y = -5.1, 31.9                                     # over bike_a's delivery box (v2 stood it "on the box", but the ray that looked for the box
    return Vector((x, y, HOLD_Z))                         # top started 8 D up and hit a light cone, so it hung in the sky with nothing under it)


def setup(F):
    F._rp = spot(F)
    F.show(F.radio, True); F.radio_light.hide_render = False
    F.put(F.radio, F._rp, (0, 0, math.radians(47)), 0.62)


def cam(F, g, t, u):
    R = F._rp + Z(0.30)
    d = Vector((0.78, -0.63, 0)).normalized()             # v3: from further round, so Kong stands right of the handset, clear of the radio icon top-left
    push = smooth(ramp(t, T_WAIT, T_WAIT + 0.22))
    # v3: a wide lens close to the handset (was 50 mm from 2.15): Kong behind is smaller and lower, under the icon strip
    dist = 1.32 - 0.12 * ramp(t, 0, T_WAIT) - 0.20 * push
    sh = hand_cam(t, 0.12, 1.0)
    k = max(0.0, 1 - (t - T_HEY) / 0.45) if t >= T_HEY else 0.0
    f = hand_cam(t, 1.6 * k, 7.0)
    sh = tuple(a + b for a, b in zip(sh, f))
    loc = R + d * dist + Z(0.30 + 0.04 * u + RISE * push)
    return F.camera(loc, R + Z(0.02 + 0.06 * push) + F.right * 0.05, F.pick(28, 24), roll=-3, focus=R, k=F.pick(10, 9), kmax=14, clip=0.03, shake=sh)


def frame(F, g, t, u):
    cam(F, g, t, u)
    # the hand holding it: a slow breath-like sway, a jolt on 'เฮ้ย!'
    kj = max(0.0, 1 - (t - T_HEY) / 0.35) if t >= T_HEY else 0.0
    sway = Vector((0.012 * math.sin(t * 2.1), 0.0, 0.016 * math.sin(t * 1.6 + 1) + 0.05 * kj * math.sin((t - T_HEY) * 40)))
    F.put(F.radio, F._rp + sway, (math.radians(2 * math.sin(t * 1.3) + 5 * kj), 0, math.radians(47 + 3 * math.sin(t * 0.9))), 0.62)
    e = float(C.envelope()[g]) if t < T_DEAD else 0.0
    if T_HEY <= t < T_DEAD and (g // 2) % 2: e *= 0.15            # stutter on 'เฮ้ย!'
    live = t < T_DEAD
    F.radio_led.node_tree.nodes["Emission"].inputs["Strength"].default_value = (1.5 + 70.0 * e) if live else 0.0
    F.radio_light.data.energy = (4.0 + 160.0 * e) if live else 0.0
    F.radio_disp.node_tree.nodes["Emission"].inputs["Strength"].default_value = 2.2 if live else (1.0 if (g % 3 == 0 and t < T_DEAD + 0.1) else 0.0)
    tt = C.on_twos(t)
    turn = tt >= T_HEY + 0.15                                       # he hears it and looks round (drawing swap)
    kong_cutter(F, t, g, view="front" if turn else "q", s=-1, expr="alarmed" if turn else "serious", head=(0, -4 if turn else 6, 0, 0),
                arm_n=dict(hand=(0.45, 0.85), elbow=None, hand_shape="grip"))
    if turn:
        F.kong.set(view="front", expr="alarmed", blink=0, head=(0, -3, 0, 0), arm_r="hold_cutter", prop_r=dict(type="cutter", bars=3, wet=True), arm_l="down", legs="wide")
    driver_seated(F, t)
    return {"exposure": 1.5, "tilt": 0.0}


def late(F, g, t, u):
    if once(F):
        F.lamp(F.P(DM0(F), 6.5, 6.0), F.K + Z(1.0), 8000.0, heads=[F.kong.head()])
        F.shadows(F.K + Z(1.5))
        F.kong.a.set_glow(WARM, 0.3)
        F.fill('fill_a', tuple(F._rp + Vector((1.2, -1.6, 1.4))), 60.0, (0.75, 0.85, 1.0), 0.4)
