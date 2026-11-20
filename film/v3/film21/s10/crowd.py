"""animated 3D bridge column (rebuilt every frame): pairs of caparisoned riders on the deck, with per-horse wobble."""
import math
import numpy as np
import bpy
import stirling as K

def column(g, slots, wob=1.0, jam=0.0, seed=3, prefix="troops_bridge"):
    """ys = y of each pair. jam 0..1 = how much the riders try to turn (yaw swings +-40 deg), wob scales the idle bob."""
    K._del_prefix(prefix)
    rs = np.random.RandomState(seed); B = K.Batch(85)
    for i, (xx, yy) in enumerate(slots):
        for j, sx in enumerate((0.0,)):
            m = K.KNIGHT_MATS[(i + j) % 5]; ph = rs.uniform(0, 6.28); sp = rs.uniform(0.15, 0.3)
            coat = ['horse', 'horse_dk', 'horse'][rs.randint(0, 3)]; tint = 0.85 + 0.3 * rs.rand()
            bob = 0.10 + 0.10 * math.sin(g * sp * 2 * math.pi / 3 + ph) * wob
            yaw = 90.0 + jam * 38.0 * math.sin(g / 30.0 * 2 * math.pi * (0.5 + 0.2 * (i % 3)) + ph) + 3.0 * math.sin(g * 0.21 + ph)
            dy = 0.07 * wob * math.sin(g * 0.37 + ph); dx = 0.03 * math.sin(g * 0.29 + ph * 2)
            K.horse(B, (xx + sx + dx, yy + dy, K.DECK_Z + 0.02 * math.sin(g * 0.6 + ph)), yaw, coat=coat, trap=m[0], trim=m[1], tint=tint, rider=(m[0],), bob=bob)
    obs = B.finalize(prefix)
    return obs
