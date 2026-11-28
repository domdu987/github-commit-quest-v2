"""S18  'ในรถ คนขับนั่งนิ่ง ไม่ขยับเลยสักนิด'  -- T3 frontal through the cracked windscreen, a creeping push; the driver does
not move at all (no blink, no breath): only rain and the camera."""
from shots.base import *
import beauty as B
import bpy
ID = "S18"
PCT = {"final": 100, "final8": 100}          # a character is taller than a quarter of the frame: full render scale so the ink lines are 1:1


def setup(F):
    B.pov_windscreen(F.A, True)
    B.practical("sodium_2_1", 0.5); B.practical("sodium_2_-1", 0.5)
    F.hide_roots(["l2_b", "headlight_l2_b_-1", "headlight_l2_b_1", "cone_headlight_l2_b_-1", "cone_headlight_l2_b_1", "flood_beam"])
    import stage
    stage._windscreen_soft(True)
    for e in F.extras: e.visible = False                    # review v2: the bystanders on the horizon above the roof pulled the eye off the driver
    # v2: the driver has to read through the glass.  The crack web is thinned in a soft window over his face (it stays
    # whole around it), the teal dash glow that turned him into a green blob is nearly off, the dome light is brighter
    stage.crack_window(True, center=(0.50, 0.535), r0=0.15, r1=0.34, floor=0.0, ky=F.pick(1.35, 0.8))
    for nm, e, col in (("pov_dash", 5.0, (0.55, 0.9, 1.0)), ("pov_dome", 80.0, (1.0, 0.86, 0.66))):
        ob = bpy.data.objects.get(nm)
        if ob: ob.data.energy = e; ob.data.color = col


def cam(F, g, t, u):
    ws = Vector(F.A["windscreen"]); hc0 = Vector(F.A["driver_head"])
    loc = ws + F.fwd * (F.pick(1.95, 2.2) - 0.22 * u) - F.right * (0.30 - 0.10 * u)
    loc.z = hc0.z + 0.42 - 0.05 * u
    hc = getattr(F, "_hc18", hc0)
    look = hc + Z(F.pick(-0.10, -0.1)) - F.right * 0.05
    return F.camera(loc, look, F.pick(50, 34), focus=hc, k=8.0, kmax=18, clip=0.02)


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.door(DOOR_OPEN)
    d = driver_seated(F, t, view="front", head=(0, 10, 0.0, 0.05), lean=8)
    d.loc = tuple(Vector(d.loc) + Z(0.17))                 # sat a little higher than the seat so collar and shoulders clear the dash in this lens
    F.kong.hide(); F.crew.hide()
    return {"exposure": 1.45, "tilt": 0.6, "vignette": 0.55, "sharp_idx": [2], "flat": dict(AMB=0.62, TINT=(0.90, 0.93, 1.0), DIR=0.30)}


def late(F, g, t, u):
    if once(F):
        ws = Vector(F.A["windscreen"])
        F._hc18 = Vector(F.drv.head())
        cam(F, g, t, u)
        F.lamp(ws + F.fwd * 2.2 + F.right * 5.5, ws + F.fwd * 1.2 + Z(-0.4), 2600.0, heads=[F._hc18], head_z=2.3)
        F.fill("fill_a", tuple(F._hc18 + F.fwd * 0.9 + Z(0.45)), 110.0, (1.0, 0.93, 0.84), 0.3)       # face fill, from the dash top
        F.shadows(F._hc18, [F.drv])
