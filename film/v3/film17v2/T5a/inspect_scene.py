import sys, os
sys.path.insert(0, '/home/user/github-commit-quest-v2/film/v3/set3d17')
import prefecture17 as P, bpy
A = P.world_build('T5')
rows = []
for o in bpy.data.objects:
    if o.type == 'MESH': rows.append((len(o.data.vertices), o.name, o.visible_camera, round(o.bound_box[0][2] + o.location.z, 2)))
rows.sort(reverse=True)
print(len(rows), 'mesh objects')
for r in rows[:60]: print(r)
print([o.name for o in bpy.data.objects if o.type == 'MESH' and len(o.data.vertices) < 400][:80])
