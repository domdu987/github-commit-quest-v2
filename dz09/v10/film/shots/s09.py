"""S09  'แบตเต็ม 3 ขีด'  -- T1 macro on the battery gauge: the bars light 1-2-3 at 16.30 / 16.50 / 16.70, then a held read."""
from shots.base import *
import presets
ID = "S09"
PCT = {"final": 75, "final8": 75}          # wide / prop shot: the set's 75 % render scale
SPP = {"final": 4}
BARS = (16.30, 16.50, 16.70)


def cam(F, g, t, u):
    Ct, Wd = presets.table(F.A)
    p = dict(Ct["macro"])
    if not F.v: p.update(Wd.get("macro", {}))
    loc = Vector(p["loc"]); look = Vector(p["look"])
    loc = loc + (look - loc) * (0.06 * u)                  # 4 %/s creep
    c = F.camera(loc, look, p["lens"], focus=p["focus"], k=16.0, kmax=14, clip=p.get("clip", 0.02), shake=hand_cam(t, 0.06, 1.0))
    return c


def frame(F, g, t, u):
    cam(F, g, t, u)
    F.cutter3d(True, jaw=0.0, bars=sum(1 for b in BARS if t >= b), arms=False)
    F.sparks_at(Vector(F.A["cutter_jaw"]), g, 0.0)
    to_cam = Vector(F.cam.location) - F.K; to_cam.z = 0; to_cam.normalize()
    F.kong.set(loc=F.K - to_cam * 0.9, face=facing(to_cam), view="front", expr="determined", blink=C.blink("kong", t), arm_r="down", arm_l="down", legs="stand",
               head=(0, 8, 0, 0))
    driver_seated(F, t)
    return {"exposure": 1.2}
