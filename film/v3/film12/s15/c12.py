"""c12.py -- film-12 take helper (copied in spirit from film8/common.py): paths, street set + cast12, per-frame cast cards.
Cards are rebuilt every frame (cast_card rasters are cached by SVG hash, so repeated poses cost nothing): drop_cards() then new cards."""
import os, sys, math
PROJ = '/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj'
for p in (PROJ + '/v3/cast12', PROJ + '/v3/cast10', PROJ + '/v3/set3d12'):
    if p not in sys.path: sys.path.insert(0, p)
import cast12            # noqa: E402  (before anything that imports puppet / sprites)
import street as S       # noqa: E402
import bpy               # noqa: E402
from mathutils import Vector  # noqa: E402

lerp = lambda a, b, u: a + (b - a) * u
clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))
def ez(u):
    u = clamp(u); return u * u * (3 - 2 * u)
def g_of(t): return int(round((t + 0.10) * 30))       # narration-tied events
def g_bound(t): return int(round(t * 30))             # shot boundaries

_cards = []
def drop_cards():
    for ob in _cards:
        me = ob.data; mats = list(me.materials)
        bpy.data.objects.remove(ob, do_unlink=True); bpy.data.meshes.remove(me)
        for m in mats:
            imgs = [n.image for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image] if m.use_nodes else []
            bpy.data.materials.remove(m)
            for im in imgs:
                if im.users == 0: bpy.data.images.remove(im)
    _cards.clear()

def card(name, member_pose, mark, cam_loc, over=None, mirror=False, tint=None, rim=None, tilt=0.0):
    cast, pose = member_pose
    ob = S.cast_card(name, cast, pose, mark, cam_loc, tilt=tilt, over=over, mirror=mirror, tint=tint, rim=rim)
    _cards.append(ob); return ob

def cam_loc(): return bpy.context.scene.camera.matrix_world.translation.copy()

def set_cam(loc, look, lens=22.0):
    S.make_camera(dict(loc=tuple(loc), look_at=tuple(look), lens=lens))
