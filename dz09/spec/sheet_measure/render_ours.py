# ortho, transparent-film front renders of the v7 cast for proportion measurement (does not touch v7/cast/out)
import os, sys, json
CAST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "v7", "cast"))
sys.path.insert(0, CAST)
import lookdev7 as L
import bpy, cast7 as C
OUT = os.path.dirname(os.path.abspath(__file__))
sc, cam = L.neutral_scene(32)
sc.render.film_transparent = True
sc.objects["ground"].visible_camera = False
chars, cut = L.build_cast(C, ["kong", "crew", "driver"])
for kind in ["kong", "crew", "driver"]:
    ch = chars[kind]; L.show_only(chars, cut, kind); ch.preset(L.POSE[kind])
    ch.place((0, 0, 0), 0)
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 6.0
    cam.location = (0, -20, 2.4); L._aim(cam, (0, 0, 2.4))
    p = os.path.join(OUT, f"ours_{kind}_front_ortho.png")
    print(kind, L.render(sc, p)); m = L.meta(sc, cam, ch, p); print(m)
