#!/usr/bin/env python3
"""shot_9aC.py -- s09 shot 9a (macro_oar) relit for version C: the first draft was dark navy.  Exposure +0.5 and a warm amber rim (sun side, behind the oar) plus a soft amber
bounce from the camera side, so the oar blade, hull and water read in warm light.  Same camera / splash as shot.py.  Frames go to relit9a/raw/s9 (copy over raw/s9 after).
    JOSEON_LOOK=C python3 shot_9aC.py stills a:b[:s] <out> [scale] [samples] | final a:b [scale] [samples]"""
import os, sys, json, math
os.environ.setdefault("JOSEON_LOOK", "C")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shot as S                                          # noqa: E402
import bpy                                                # noqa: E402
from mathutils import Vector                              # noqa: E402
C, J = S.C, S.J
EXPO_ADD = 0.8
J.C_EXPO["macro_oar"] = J.C_EXPO.get("macro_oar", 0.15) + EXPO_ADD


class Take9(S.Take):
    def __init__(self, shot=9):
        S.Take.__init__(self, 9)
        pc = self.A["cam"]; look = Vector(pc["look_at"]); cam = Vector(pc["loc"])
        ts = Vector(J.S["to_sun"]); h = Vector((ts.x, ts.y, 0)).normalized()
        fwd = look - cam; fwd.z = 0; fwd.normalize(); right = fwd.cross(Vector((0, 0, 1)))
        for nm, pos, watt, size, col in (("rim9a", look + h * 5.0 + Vector((0, 0, 1.6)), 900.0, 3.0, (1.0, 0.62, 0.30)),
                                         ("bounce9a", look - fwd * 3.0 + right * -2.5 + Vector((0, 0, 1.0)), 350.0, 4.0, (1.0, 0.70, 0.42))):
            ld = bpy.data.lights.new(nm, "AREA"); ld.energy = watt; ld.size = size; ld.color = col
            o = bpy.data.objects.new(nm, ld); bpy.context.scene.collection.objects.link(o); o.location = pos
            d = look - pos; o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        gs = [g for g in C.parse(sys.argv[2]) if S.RANGES[9][0] <= g <= S.RANGES[9][1]]
        Tk = Take9(); Tk.pose(9, gs)
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
        os.makedirs(out, exist_ok=True)
        for g in gs:
            st = Tk.render(9, [g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s9_g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else C.RES_PCT
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else C.preset_samples("macro_oar")
        out = os.path.join(HERE, "relit9a"); os.makedirs(out, exist_ok=True)
        C.final_loop(lambda s_: Take9(), [9], sys.argv[2], S.RANGES, out, scale=scale, samples=samples)
