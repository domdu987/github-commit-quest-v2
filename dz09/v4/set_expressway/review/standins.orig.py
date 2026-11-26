"""standins.py -- put the cast (read-only import of PROJ/v4/cast_dz09/stage25) on the set's anchors for staging
drafts: Kong (wet, cutter, 3 battery bars) at A["kong_mark"], the infected driver seated at A["driver_seat"].
Not part of the set: shots own their actors. Kept here so the draft sheets show scale and the driver seat.

    import standins
    actors = standins.place(A)              # after expressway.build()
    standins.pose_all(actors, camera)       # every time the camera changes
"""
import os, sys, math
import bpy
from mathutils import Vector

PROJ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CAST = os.path.join(PROJ, "v4", "cast_dz09")
SPRITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp", "sprites")


def _st():
    if CAST not in sys.path: sys.path.insert(0, CAST)
    import stage25
    return stage25


def facing_deg(front):
    """stage25 facing: the angle about Z that turns a -Y front into the world vector `front`."""
    return math.degrees(math.atan2(front.x, -front.y))


def place(A):
    st = _st()
    th = A["hero_heading"]
    right = Vector((math.cos(th), math.sin(th), 0)); fwd = Vector((-math.sin(th), math.cos(th), 0))
    kong = st.Actor25("sb_kong", "kong_wet", gap=0.05, ppd=150, mode="25d", sprite_dir=os.path.join(SPRITES, "kong"))
    # Kong works the door, turned three-quarters toward the default cameras (which sit behind him, toward -s)
    kong.place(A["kong_mark"], facing_deg(-(right * 0.55 + fwd * 1.0).normalized()))
    drv = st.Actor25("sb_driver", "driver", gap=0.03, ppd=150, mode="25d", follow=0.35, sprite_dir=os.path.join(SPRITES, "driver"))
    drv.place(A["driver_seat"], facing_deg(fwd))
    for a in (kong, drv):
        for ob in [a.root] + list(a.root.children_recursive):
            if ob.type == "MESH": ob.pass_index = 2
    try:
        st.sync_lights(key="flood_key", rims=["beacon_red_0", "sodium_1_-1", "beacon_blue_1"], shadow="flood_key")
    except Exception as ex:
        print("sync_lights:", ex)
    return {"kong": kong, "driver": drv, "seat_z": A["driver_seat"][2]}


POSES = {
    "kong": {"expr": "determined", "arm_l": "hold", "prop_l": {"type": "cutter", "bars": 3}},
    "driver": {"expr": "still", "legs": "seated", "arm_r": "lap", "arm_l": "lap"},
}


def pose_all(actors, camera, hide=()):
    """hide: names of actors to hide for this camera (e.g. ("kong",) for the macro insert, which uses the 3D cutter)."""
    for ob in actors.pop("_hidden", []):          # restore what an earlier call hid (pose() manages its own cards)
        ob.hide_render = False
    figs = {}
    figs["kong"] = actors["kong"].pose(POSES["kong"], camera=camera)
    figs["driver"] = actors["driver"].pose(POSES["driver"], camera=camera)
    hid = []
    for k in hide:
        for ob in [actors[k].root] + list(actors[k].root.children_recursive):
            if not ob.hide_render: ob.hide_render = True; hid.append(ob)
    actors["_hidden"] = hid
    # seat the driver: drop the root so the drawing's hip point lands on the cushion
    f = figs["driver"]
    seat = f.get("seat") if isinstance(f, dict) else None
    if seat is not None and "sb_seat_done" not in actors:
        hip_h = abs(seat[1]) * 1.0
        r = actors["driver"].root
        r.location.z = actors["seat_z"] - hip_h + 0.05
        actors["sb_seat_done"] = True
    return figs
