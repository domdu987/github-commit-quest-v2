import sys; sys.path.insert(0,'/home/user/github-commit-quest-v2/film/v3/set3d13')
import chicago as C, bpy
A=C.build('street_wide')
for n in ('carts','cart_wheels','hotel','jf_static','jf_head','jf_screw'):
    o=bpy.data.objects[n]; import mathutils
    bb=[o.matrix_world@mathutils.Vector(c) for c in o.bound_box]; print(n,[round(min(b[i] for b in bb),1) for i in range(3)],[round(max(b[i] for b in bb),1) for i in range(3)], o.location.z, o.hide_render)
