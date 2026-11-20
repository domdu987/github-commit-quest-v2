#!/usr/bin/env python3
"""set3d20.py : PUBLIC API of the film-20 set (Eiffel Tower, Paris 1887-1910). See API.md.

    import set3d20 as S
    A = S.build('site_wide', light='DAY')            # SITE / TOWER (this package), 'cafe_*' / 'resto_*' -> int20.build (interior builder)
    S.setup_render(S.scene(), 'final')               # 720x1280 (preview 360x640), Cycles CPU ~8 spp + OIDN, 2 threads, no DOF ever
    cam = S.make_camera(A['cams'][A['cam_name']])    # {loc, look_at, lens} in world D; every named camera of the preset is in A['cams']
    S.stage_placeholders(A, A['cam_name']); S.render('/tmp/x.png')
Hooks (key when frame=n is given): CAFE S.set_window_view / S.smoke / S.add_signature (-> int20), S.set_stage(s, frame), S.crane_swing, S.spark, S.rivet_toss, S.set_antenna, S.set_wagon, S.set_crowd, S.spark_gap, S.signal_rings, S.wire_glow, S.set_light_mix ...
CLI: python3 set3d20.py stills|final [preset[:LIGHT] ...]"""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import core20 as C
from core20 import (STATE, SC, W, setup_render, make_camera, render, project, head_pixels, placeholder_actor, stage_placeholders, clear_actors, clear_keys, apply_P, lerpP, HEIGHT)
import site20 as ST

SITE_PRESETS = list(ST.PRESETS)
TOWER_PRESETS = []          # filled by tower20
def _tower():
    import tower20 as T; return T

def scene(): return bpy.context.scene
def presets():
    return SITE_PRESETS + _tower_presets()
def _tower_presets():
    try: return list(_tower().PRESETS)
    except ImportError: return []

def build(preset, light=None):
    """Build the whole location for a preset and return A (see API.md). cafe_* / resto_* are built by int20.build (interior builder)."""
    if preset.startswith(('cafe_', 'resto_')):
        import int20
        return int20.build(preset, light)
    if preset in ST.PRESETS: A = ST.build(preset, light)
    else: A = _tower().build(preset, light)
    return A

# ---- hook shortcuts (resolved at call time against the loaded location)
def set_stage(s, frame=None): return ST.set_stage(s, frame)
def crane_swing(k, frame=None): return ST.crane_swing(k, frame)
def spark(frame=None, **kw): return ST.spark(frame, **kw)
def rivet_toss(k, frame=None): return ST.rivet_toss(k, frame)
def _t(name): return getattr(_tower(), name)
def set_antenna(on, frame=None): return _t('set_antenna')(on, frame)
def set_wagon(on, frame=None): return _t('set_wagon')(on, frame)
def set_crowd(level, frame=None): return _t('set_crowd')(level, frame)
def set_year(y, frame=None): return _t('set_year')(y, frame)
def spark_gap(on, frame=None): return _t('spark_gap')(on, frame)
def signal_rings(t, frame=None): return _t('signal_rings')(t, frame)
def wire_glow(v, frame=None): return _t('wire_glow')(v, frame)
def set_light_mix(a, b, k, frame=None): return _t('set_light_mix')(a, b, k, frame)
# CAFE hooks (interior builder): forwarded to int20 (also in A['hooks'] of every cafe_* preset)
def set_window_view(view='stub', frame=None):
    import int20; return int20.set_window_view(view, frame)
def smoke(v, frame=None, t=None):
    import int20; return int20.smoke(v, frame, t)
def add_signature(n, frame=None):
    import int20; return int20.add_signature(n, frame)
def apply_light(name, frame=None): return _t('apply_light')(name, frame)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; args = sys.argv[2:]
    if cmd in ('stills', 'final'):
        q = 'preview' if cmd == 'stills' else 'final'; out = os.path.join(HERE, 'work', cmd); os.makedirs(out, exist_ok=True)
        for spec in (args or presets()):
            pr, _, lt = spec.partition(':'); A = build(pr, lt or None); setup_render(scene(), q); nm = A['cam_name']; make_camera(A['cams'][nm]); stage_placeholders(A, nm)
            bpy.context.view_layer.update(); w, c = render(os.path.join(out, '%s_%s.png' % (pr, A['light']))); print(pr, A['light'], 'wall %.1f cpu %.1f' % (w, c), head_pixels(nm), flush=True)
    else: print(__doc__)
