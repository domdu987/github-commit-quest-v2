import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shot as H
C=H.C; S=H.S; bpy=H.bpy
A = S.shot('street_wide_low', 'RAIN', u=0.4, placeholders=False, quality='preview')
cam = bpy.context.scene.camera
res={}
for g in (572, 611, 650):
    C.key_cam(1, H.cam_for(g)); bpy.context.scene.frame_set(1)
    for x in (-5,-3.5,-2,2,3.5,5):
        for y in (6,9,12,15):
            res.setdefault((x,y),[]).append([round(v) for v in S.project_px(cam,(x,y,0.0))[:2]]+[round(v) for v in S.project_px(cam,(x,y,3.0))[:2]])
for k,v in sorted(res.items()): print(k, v)
print('boxa', S.STAND['box_a']['pos'])
