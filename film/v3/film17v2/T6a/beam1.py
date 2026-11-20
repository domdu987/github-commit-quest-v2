import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/film17v2/T6a')
import render_t6a as R, prefecture17 as P, bpy
orig = P.stage_cast2
def patched(*a, **k):
    r = orig(*a, **k)
    for o in bpy.data.objects:
        if 'beam_fx' in o.name or 'beam_fx' in (o.active_material.name if getattr(o,'active_material',None) else ''): o.hide_render = True; print('hid', o.name, flush=True)
    return r
P.stage_cast2 = patched
R.run([1400, 1440], '/home/user/github-commit-quest-v2/film/v3/film17v2/T6a/beam1')
