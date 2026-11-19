import sys
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d18')
import jimo as J, bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector as V
name = sys.argv[1]; ts = [float(x) for x in (sys.argv[2:] or ['0', '0.5', '1'])]
A = J.build(None, name, None); sc = bpy.context.scene; sh = J.S.SHOTS[name]; marks = J.S.marks_for(name)
H = dict(J.HEIGHT); H.update(qi_soldier=3.2, party_crowd=3.2, sentry=3.2, herd=3.2)
for t in ts:
    cam = J.shot_camera(name, t, fg=False); out = []
    for role, lst in marks.items():
        if role not in H: continue
        for m in lst[:14]:
            p = V(m[:3]); a = world_to_camera_view(sc, cam, V((p.x, p.y, p.z + H[role]))); f = world_to_camera_view(sc, cam, p)
            if a.z <= 0: out.append((role, 'behind')); continue
            out.append((role, int(a.x * 720), int((1 - a.y) * 1280), int((1 - f.y) * 1280), 'h=%d' % int((f.y - a.y) * 1280)))
    print('t=%.2f' % t, out)
