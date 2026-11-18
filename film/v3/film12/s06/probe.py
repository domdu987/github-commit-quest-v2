import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c12 as C
S, bpy = C.S, C.bpy
A = S.shot('box_seat', 'RAIN', u=0.5, placeholders=False, quality='preview')
cam = bpy.context.scene.camera
def pr(tag, setup, pts):
    C.key_cam(1, setup); bpy.context.scene.frame_set(1)
    print(tag, {k: [round(v) for v in S.project_px(cam, p)[:2]] for k, p in pts.items()})
P = S.STAND['box_a']['pos']; print('box_a', P, 'box_b', S.STAND['box_b']['pos'], 'box_c', S.STAND['box_c']['pos'])
PB=S.STAND['box_b']['pos']; PC=S.STAND['box_c']['pos']
hp={'a_head':(P[0],P[1],4.22+2.6),'a_seat':(P[0],P[1],4.22),'b_head':(PB[0],PB[1],4.22+2.8),'c_head':(PC[0],PC[1],4.22+2.2)}
for u in (0.0,0.3,0.6,1.0):
    pr('trio u%.1f'%u, C.cam_setup('box_trio',u), hp)
for loc,la in [((-2.2,9.0,2.2),(3.55,30.0,5.2)),((-1.0,11.0,2.4),(3.55,32.0,5.2)),((0.0,12.0,2.8),(3.55,30.0,5.2))]:
    pr('cust %s'%(loc,), dict(loc=loc,look_at=la,lens=24.0), hp)
