"""beck_london.py (builder A): london exterior, DUSK + NIGHT. JOIN COORDINATES are exported here (see API.md). Full builder below is filled in progressively."""
import math
from mathutils import Vector as V

# ---- joins (london world frame: 1 unit = 1 D, Z up, street ground z = 0, +y is away from the near pavement; HQ and station entrance row is y 24..34)
GROUND_Z = 0.0
GRATE_XY = (8.0, 19.0)                 # centre of the pavement grate; the grate quad spans x 4..12, y 15.5..22.5 at z 0.06. B's shaft top = this xy, z 0 (lid opening 8 x 7)
GRATE_SIZE = (8.0, 7.0)
LODGE_WIN = dict(center=(-30.5, -4.0, 10.4), size=(4.2, 4.4), normal=(0, 1, 0))     # Beck's window in london (house x -34..-20, y -16..-4, front faces +y). Pane plane y = -4.0
ROOM_WIN = dict(center=(6.6, 14.0, 5.0), size=(4.2, 4.4), normal=(0, 1, 0))        # the same window seen from inside the lodgings room (beck_hq room frame); room->london offset (-37.1, -18.0, 5.4)
PUB_WIN = dict(center=(0.0, 24.0, 10.96), size=(11.8, 6.4), normal=(0, -1, 0))     # PUBLICITY DEPT window in the HQ front wall (real opening). The publicity room is inside the HQ block, in london coordinates
PUB_ROOM = dict(x=(-21.0, 21.0), y=(24.8, 33.4), floor=7.4, ceiling=14.5)          # publicity room box (same coordinates in the london scene and in the beck_hq 'publicity' location)
HQ_BOX = dict(x=(-22.0, 22.0), y=(24.0, 34.0), z=(0.0, 22.0))
ENTRANCE_XY = (-33.0, 19.0)            # UNDERGROUND station entrance stair top
SHOTS = {}
LOCATIONS = {}
