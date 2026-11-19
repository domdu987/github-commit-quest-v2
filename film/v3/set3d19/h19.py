#!/usr/bin/env python3
"""h19.py : public API of set3d19 (film 19 "ไอ้ช่างไม้", John Harrison, 1730s-1773). Real 3D Blender set (bpy 5.x, Cycles CPU), flat 2D puppets in a lit 3D world.

    import h19 as H
    A = H.build('shop_wide', light=None)        # resets the scene, builds the location of that preset, applies the light
    cam = H.make_camera(A['cam'])                # 22 mm / 36 mm, DOF OFF
    H.setup_render(scene, 'final'|'preview')     # 720x1280 / 360x640, Cycles CPU, low spp + OIDN, 2 threads
    act = H.placeholder_actor('harrison', A['marks']['harrison_bench'], face_to=cam.location)
Locations: WORKSHOP (h19_shop, shop_*), SHIP (h19_ship, ship_*), HALL (h19_hall, hall_*). 1 unit = 1 D = head width, D = 1.85 x metres, Z up, floor / deck at the mark's z.
Hooks key on `frame=` when given (LINEAR; visibility CONSTANT), as in film 16. See API.md."""
import os, sys, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy
from mathutils import Vector
import h19_kit as K
from h19_kit import SC, STATE, W, make_camera, render, project, clear_keys, placeholder_actor, HEIGHT, measure_hue

SHOP_PRESETS = ['shop_wide', 'shop_bench', 'shop_clock', 'shop_door']
HALL_PRESETS = ['hall_wide', 'hall_table', 'hall_low', 'hall_window', 'hall_door']
SHIP_PRESETS = ['ship_hero', 'ship_aerial', 'ship_deck', 'ship_rail', 'ship_rocks', 'ship_coast']
PRESETS = SHOP_PRESETS + HALL_PRESETS + SHIP_PRESETS
DEFAULT_LIGHT = dict(shop='DAY', hall='DAY', ship='NOON')
DEFAULT_LIGHT_OF = {'ship_coast': 'DAY', 'ship_rocks': 'STORM_DUSK'}
LIGHTS = dict(shop=['DAY', 'NIGHT'], hall=['DAY', 'EVENING'], ship=['NOON', 'DAY', 'STORM_DUSK'])
HEIGHTS = HEIGHT

def location_of(preset):
    assert preset in PRESETS, '%s is not one of %s' % (preset, PRESETS)
    return 'shop' if preset.startswith('shop') else 'hall' if preset.startswith('hall') else 'ship'

def _mod(loc):
    if loc == 'shop': import h19_shop as M
    elif loc == 'hall': import h19_hall as M
    else:
        import h19_ship as M                                  # lazy: written by the other builder
    return M

def build(preset, light=None, clear=True):
    """Reset the scene, build the location of `preset` with its light (default per location / preset) and its set state. Returns the anchors dict (API.md)."""
    loc = location_of(preset); lk = light or DEFAULT_LIGHT_OF.get(preset) or DEFAULT_LIGHT[loc]
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True)
    K.MATS.clear(); STATE.clear(); K.ROOT = None; STATE.update(loc=loc, preset=preset, light=lk)
    M = _mod(loc); sc = bpy.context.scene
    ret = getattr(M, 'build_' + loc)(STATE, preset, lk)
    ret = ret if isinstance(ret, dict) else {}
    setup_render(sc, 'final'); K.setup_grade(sc, STATE.get('sat', 1.08))
    cams = ret.get('cams') or STATE.get('cams', {}); cn = ret.get('cam_name') or STATE.get('cam_name') or preset
    cam = ret.get('cam') or cams.get(cn) or cams[preset]
    A = dict(location=loc, preset=preset, light=STATE.get('light', lk), cams=cams, cam=dict(cam), cam_name=cn, cam_notes=STATE.get('cam_notes', {}),
             marks=ret.get('marks') or STATE.get('marks', {}), staging=ret.get('staging') or STATE.get('staging', {}), ship_root=ret.get('ship_root') or STATE.get('ship_root'),
             render=dict(samples_final=STATE.get('samples'), resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), heights=dict(HEIGHT), floor_z=STATE.get('floor_z', 0.0),
             lights=[o.name for o in bpy.data.objects if o.type == 'LIGHT'])
    STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    K.setup_render(scene, quality)

def staging(cam_name=None):
    """[(role, mark xyz)] of the preset camera"""
    A = STATE['A']; return A['staging'].get(cam_name or A['cam_name'], [])

def stage_placeholders(cam_name=None, cam_loc=None):
    A = STATE['A']; cam_name = cam_name or A['cam_name']; cam_loc = cam_loc or A['cams'][cam_name]['loc']
    return K.stage_placeholders(staging(cam_name), cam_loc, parent=None)

def head_pixels(cam_name=None):
    return K.head_pixels(staging(cam_name))

# ----------------------------------------------------------------------------- hooks (dispatch by location; ship hooks live in h19_ship)
def _loc(*ok):
    assert STATE.get('loc') in ok, 'this hook belongs to %s (current location %s)' % (ok, STATE.get('loc'))
def set_clock(n=1, frame=None): _loc('shop'); import h19_shop as S; return S.set_clock(n, frame)
def set_balance(t=0.0, frame=None): _loc('shop'); import h19_shop as S; return S.set_balance(t, frame)
def set_door(deg=78.0, frame=None): _loc('shop'); import h19_shop as S; return S.set_door(deg, frame)
def set_candles(level=1.0, frame=None):
    _loc('shop', 'hall')
    if STATE['loc'] == 'shop': import h19_shop as S
    else: import h19_hall as S
    return S.set_candles(level, frame)
def set_moneybag(state='full', frame=None): _loc('hall'); import h19_hall as S; return S.set_moneybag(state, frame)
def set_box(state='open', frame=None): _loc('hall'); import h19_hall as S; return S.set_box(state, frame)
def set_stubs(n=0, frame=None): _loc('hall'); import h19_hall as S; return S.set_stubs(n, frame)
def set_kings_chair(on=True, frame=None): _loc('hall'); import h19_hall as S; return S.set_kings_chair(on, frame)
def set_regulator(on=True, frame=None): _loc('hall'); import h19_hall as S; return S.set_regulator(on, frame)
def set_sea(t=0.0, frame=None): _loc('ship'); import h19_ship as S; return S.set_sea(t, frame)
def set_roll(t=0.0, frame=None): _loc('ship'); import h19_ship as S; return S.set_roll(t, frame)
def set_sun_overhead(k=1.0, frame=None): _loc('ship'); import h19_ship as S; return S.set_sun_overhead(k, frame)
def set_rain(on=True, frame=None): _loc('ship'); import h19_ship as S; return S.set_rain(on, frame)

def apply_light(name, frame=None):
    loc = STATE['loc']; return _mod(loc).apply_light(name, frame)

if __name__ == '__main__':
    pass
