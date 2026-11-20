import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21
from c21 import *
register_bare_knights(); patch_air_helmet()
T = Take("bridge_deck", "draft")
S = cast21.STORY21
f = 1
cam_loc = tuple(float(v) for v in sys.argv[1:4]) if len(sys.argv) > 3 else (-2.7, -2.4, 3.0)
look = (0.6, 1.6, 2.9)
T.set_cam(cam_loc, look)
a = T.actor("A", "knight_a_mtd"); b = T.actor("B", "knight_b_mtd")
a.place(f, (0.5, 3.0, K.DECK_Z), scale=M_PER_D); b.place(f, (-0.4, 0.2, K.DECK_Z), scale=M_PER_D)
pa = dict(S["knight_a_mounted_shocked"][1], mirror=True); pb = dict(S["knight_b_mounted_suck_belly"][1], mirror=True)
a.pose(f, pa, camera=T.cam); b.pose(f, pb, camera=T.cam)
T.sprites_for(192)
print(T.render(f, "/tmp/s10/t26.png"))
